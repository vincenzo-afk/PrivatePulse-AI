"use client";

import { useMemo, useRef } from "react";
import { FileStack, RefreshCw, ShieldCheck, UploadCloud } from "lucide-react";
import { toast } from "sonner";
import { AppShell } from "@/components/layout/AppShell";
import { DropZone } from "@/components/upload/DropZone";
import { DocumentList } from "@/components/documents/DocumentList";
import { ErrorState } from "@/components/shared/ErrorState";
import { useDocuments } from "@/lib/hooks/useDocuments";
import { useSession } from "@/lib/hooks/useSession";

function DashboardContent() {
  const uploadAnchorRef = useRef<HTMLDivElement>(null);
  const { sessionId } = useSession();
  const {
    documents,
    isLoading,
    error,
    upload,
    delete: deleteDocument,
    isUploading,
    refetch,
  } = useDocuments();

  const readyCount = useMemo(
    () => documents.filter((document) => document.status === "ready").length,
    [documents]
  );
  const processingCount = useMemo(
    () => documents.filter((document) => document.status === "pending" || document.status === "processing").length,
    [documents]
  );

  const handleUpload = async (files: File[]) => {
    try {
      await upload(files);
      toast.success(`${files.length} document${files.length === 1 ? "" : "s"} uploaded`);
    } catch {
      toast.error("Upload failed. Please try again.");
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteDocument(id);
      toast.success("Document deleted");
    } catch {
      toast.error("Could not delete that document. Please try again.");
    }
  };

  if (!sessionId) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-accent border-t-transparent" aria-label="Initializing secure session" />
      </div>
    );
  }

  return (
    <div className="mx-auto w-full max-w-6xl space-y-8 p-6 lg:p-10">
      <header className="flex flex-col gap-5 border-b border-border pb-7 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <div className="mb-3 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.18em] text-accent">
            <ShieldCheck className="h-4 w-4" />
            Private workspace
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-text-primary sm:text-4xl">Your documents</h1>
          <p className="mt-2 max-w-2xl text-sm text-text-secondary sm:text-base">
            Upload confidential files, watch them become searchable, and keep every document scoped to this browser session.
          </p>
        </div>
        <button
          type="button"
          onClick={() => uploadAnchorRef.current?.scrollIntoView({ behavior: "smooth", block: "center" })}
          className="btn-primary inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-sm"
        >
          <UploadCloud className="h-4 w-4" />
          Upload documents
        </button>
      </header>

      <section className="grid gap-3 sm:grid-cols-3" aria-label="Document summary">
        <div className="card-base flex items-center gap-3 p-4">
          <FileStack className="h-5 w-5 text-accent" />
          <div><p className="text-2xl font-semibold text-text-primary">{documents.length}</p><p className="text-xs text-text-muted">Total documents</p></div>
        </div>
        <div className="card-base flex items-center gap-3 p-4">
          <ShieldCheck className="h-5 w-5 text-accent" />
          <div><p className="text-2xl font-semibold text-text-primary">{readyCount}</p><p className="text-xs text-text-muted">Ready to query</p></div>
        </div>
        <div className="card-base flex items-center gap-3 p-4">
          <RefreshCw className={`h-5 w-5 text-warning ${processingCount > 0 ? "animate-spin" : ""}`} />
          <div><p className="text-2xl font-semibold text-text-primary">{processingCount}</p><p className="text-xs text-text-muted">Processing</p></div>
        </div>
      </section>

      <section ref={uploadAnchorRef} className="card-base p-5 sm:p-6">
        <div className="mb-5 flex items-start justify-between gap-4">
          <div>
            <h2 className="text-lg font-semibold text-text-primary">Add to your index</h2>
            <p className="mt-1 text-sm text-text-muted">PDF, DOCX, or TXT files up to 20 MB each. You can select up to 10 files.</p>
          </div>
          <UploadCloud className="hidden h-5 w-5 text-accent sm:block" />
        </div>
        <DropZone onFilesSelected={handleUpload} disabled={isUploading} />
      </section>

      <section>
        <div className="mb-4 flex items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-semibold text-text-primary">Indexed files</h2>
            <p className="mt-1 text-sm text-text-muted">Processing status updates automatically every few seconds.</p>
          </div>
          <button type="button" onClick={() => void refetch()} className="btn-ghost inline-flex items-center gap-2 rounded-lg px-3 py-2 text-xs" aria-label="Refresh documents">
            <RefreshCw className="h-3.5 w-3.5" />
            Refresh
          </button>
        </div>
        {error ? <ErrorState title="Could not load documents" message="Check that the API is running, then try again." onRetry={() => void refetch()} /> : <DocumentList documents={documents} isLoading={isLoading} onDelete={handleDelete} onUploadClick={() => uploadAnchorRef.current?.scrollIntoView({ behavior: "smooth", block: "center" })} />}
      </section>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <AppShell>
      <DashboardContent />
    </AppShell>
  );
}
