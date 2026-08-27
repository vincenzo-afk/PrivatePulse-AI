# PrivatePulse AI

**Privacy-first, RAG-powered document intelligence for sensitive files.**

PrivatePulse AI lets you ask natural-language questions about medical records, financial statements, legal contracts, and other confidential documents. It combines local document processing and embeddings with grounded model responses, inline citations, session isolation, entity masking, and an audit trail so that answers remain useful without unnecessarily exposing raw documents.

<p align="center">
  <video src="https://github.com/vincenzo-afk/PrivatePulse-AI/raw/refs/heads/main/docs/privatepulse-demo.mp4" controls muted playsinline preload="metadata" width="100%">
    Your browser does not support embedded video. <a href="https://github.com/vincenzo-afk/PrivatePulse-AI/raw/refs/heads/main/docs/privatepulse-demo.mp4">Download the PrivatePulse AI product video</a>.
  </video>
</p>

## Why PrivatePulse AI

Most document assistants optimize for convenience first. PrivatePulse AI is designed around a different starting point: **sensitive documents should stay under the operator’s control**. Files are ingested into an isolated workspace, retrieved context is used to ground answers, and the interface makes sources visible instead of presenting unsupported summaries.

## Capabilities

| Capability | What it provides |
| --- | --- |
| Privacy-first processing | Local document handling with only the minimum required context sent to the language model. |
| Multi-format ingestion | Support for PDF, DOCX, TXT, image uploads, and scanned-document workflows. |
| Retrieval-augmented answers | Relevant chunks are retrieved from the document index before generation. |
| Inline citations | Answers include document and page references when source metadata is available. |
| Vision and OCR fallback | Image-based questions and scanned PDFs can be routed through the vision workflow. |
| Session isolation | Each browser session receives its own isolated workspace and data context. |
| Entity masking | SSNs, credit-card numbers, and email addresses are masked in UI previews. |
| Audit trail | Operations are recorded with timestamps to support traceability. |
| Local embeddings | Ollama with `nomic-embed-text` can provide embeddings without a separate embedding API. |

## Product video

The repository includes a real, playable 18-second MP4 product video at [`docs/privatepulse-demo.mp4`](docs/privatepulse-demo.mp4), embedded directly above with an HTML5 `<video>` player. The editable, dependency-free scene source remains available at [`docs/privatepulse-demo.html`](docs/privatepulse-demo.html).

## Architecture

```text
Upload files
    ↓
Extract text / render pages / OCR when needed
    ↓
Chunk and embed with Ollama
    ↓
Index in ChromaDB
    ↓
Retrieve relevant context for a question
    ↓
Generate a grounded answer with citations
```

For image uploads and scanned PDFs, the vision path supplies multimodal understanding and OCR fallback. The frontend maintains the user session and chat experience, while the FastAPI backend owns ingestion, retrieval, masking, and model orchestration.

## Technology stack

| Layer | Technologies |
| --- | --- |
| Frontend | Next.js 14 App Router, TypeScript, Tailwind CSS, Zustand, TanStack Query |
| Backend | FastAPI, Python 3.11+, ChromaDB, SQLite, LangChain |
| Generation | Groq Llama 3.2 90B Vision |
| Embeddings | Ollama `nomic-embed-text` by default; OpenAI-compatible embeddings are also supported by configuration |
| Local development | Docker Compose, `uv`, npm |

## Quick start

### Prerequisites

Install Node.js 20 or later, Python 3.11 or later, the [`uv`](https://docs.astral.sh/uv/) package manager, and [Ollama](https://ollama.com/). Pull the default embedding model before starting the application:

```bash
ollama pull nomic-embed-text
```

### Configure and run the backend

```bash
cd backend
uv sync
cp ../.env.example .env
# Edit .env and set GROQ_API_KEY.
uv run uvicorn main:app --reload --port 8000
```

### Configure and run the frontend

In a second terminal:

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) and start a private chat session.

### Run with Docker Compose

The repository also includes `docker-compose.yml` for the containerized development path. Review the environment variables below before starting the services.

## Environment variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `GROQ_API_KEY` | Yes | — | API key used by the Groq generation and vision workflow. |
| `EMBEDDING_PROVIDER` | No | `ollama` | Selects the local Ollama or OpenAI-compatible embedding path. |
| `OLLAMA_BASE_URL` | No | `http://localhost:11434` | Ollama server URL. |
| `OLLAMA_EMBEDDING_MODEL` | No | `nomic-embed-text` | Embedding model pulled from Ollama. |
| `GROQ_MODEL` | No | `llama-3.2-90b-vision-preview` | Groq model identifier used by the backend. |
| `DATABASE_URL` | No | `sqlite:///./privatepulse.db` | SQLite database location. |

Never commit `.env`, `.env.local`, API keys, uploaded files, or generated databases. The repository’s `.gitignore` already excludes these local artifacts.

## Repository map

```text
backend/             FastAPI service, retrieval pipeline, storage, and model integrations
docs/                Architecture, API, privacy notes, setup guide, and HTML product video
frontend/             Next.js application and client-side session experience
.env.example         Root environment template
docker-compose.yml   Local multi-service development configuration
plan.md              Original implementation plan
```

## Privacy notes

PrivatePulse AI is a local-first development project, not a guarantee of regulatory compliance. Before using real medical, financial, legal, or other regulated data, review the deployment boundary, model-provider policies, access controls, retention behavior, logging, and applicable organizational requirements. The safest evaluation path is to begin with synthetic or redacted documents.

## Contributing

Keep pull requests focused, document security-sensitive changes, and avoid adding credentials or real user documents to fixtures. When changing the retrieval or masking pipeline, include a short explanation of how the change affects citations, isolation, and data exposure.

## License

PrivatePulse AI is released under the [MIT License](LICENSE).

## Topics

The repository is best described by the following GitHub topics: `artificial-intelligence`, `document-intelligence`, `fastapi`, `nextjs`, `ollama`, `privacy`, `python`, `rag`, `retrieval-augmented-generation`, and `typescript`.
