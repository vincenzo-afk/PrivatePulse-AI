"""Demo document loading endpoint."""

import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel, Field
from sqlmodel import Session as DBSession, select

from config import settings
from models.database import get_session
from models.document import Document
from models.session import UserSession
from schemas.document import DocumentListResponse, DocumentSchema
from services.audit import AuditEventType, log_event
from core.exceptions import PrivatePulseError
from .documents import process_document_background
from fastapi import BackgroundTasks

router = APIRouter(prefix="/demo")

DEMO_FILES = {
    "medical": ["medical-report-sample.pdf"],
    "financial": ["financial-statement-sample.pdf"],
    "legal": ["contract-sample.pdf"],
    "all": ["medical-report-sample.pdf", "financial-statement-sample.pdf", "contract-sample.pdf"],
}


class DemoLoadRequest(BaseModel):
    """Request body for loading a synthetic demo set."""

    session_id: str | None = Field(default=None, min_length=1, max_length=36)
    demo_set: Literal["medical", "financial", "legal", "all"] = "all"


class DemoLoadError(PrivatePulseError):
    """Raised when a requested demo file is unavailable."""

    def __init__(self, filename: str):
        super().__init__("DEMO_FILE_NOT_FOUND", f"Demo file is unavailable: {filename}", {"filename": filename})


@router.post("/load", response_model=DocumentListResponse)
async def load_demo_documents(
    payload: DemoLoadRequest,
    background_tasks: BackgroundTasks,
    x_session_id: str | None = Header(default=None),
    db: DBSession = Depends(get_session),
):
    """Load synthetic documents into the caller's isolated session."""
    session_id = payload.session_id or x_session_id
    if not session_id:
        raise PrivatePulseError(
            "SESSION_ID_REQUIRED",
            "A session_id or X-Session-ID header is required",
        )

    source_dir = Path(__file__).resolve().parents[2] / "data" / "demo_documents"
    session_dir = Path(settings.upload_dir) / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    session = db.get(UserSession, session_id)
    if not session:
        session = UserSession(id=session_id)
        db.add(session)
        db.commit()

    loaded: list[Document] = []
    for filename in DEMO_FILES[payload.demo_set]:
        existing = db.exec(select(Document).where(Document.session_id == session_id, Document.file_name == filename)).first()
        if existing:
            loaded.append(existing)
            continue

        source = source_dir / filename
        if not source.is_file():
            raise DemoLoadError(filename)

        document_id = str(uuid.uuid4())
        destination = session_dir / f"{document_id}.pdf"
        shutil.copyfile(source, destination)
        now = datetime.now(timezone.utc)
        document = Document(
            id=document_id,
            session_id=session_id,
            file_name=filename,
            file_path=str(destination),
            file_size=destination.stat().st_size,
            file_type="pdf",
            status="pending",
            uploaded_at=now,
        )
        db.add(document)
        session.document_count += 1
        session.last_active_at = now
        db.commit()
        db.refresh(document)
        await log_event(
            session_id,
            AuditEventType.DEMO_LOADED,
            f"Loaded synthetic demo document {filename}",
            document_id=document_id,
            db_session=db,
            metadata={"demo_set": payload.demo_set, "file_name": filename},
        )
        background_tasks.add_task(process_document_background, document_id, destination, "pdf", session_id)
        loaded.append(document)

    return DocumentListResponse(documents=[DocumentSchema.model_validate(document) for document in loaded])
