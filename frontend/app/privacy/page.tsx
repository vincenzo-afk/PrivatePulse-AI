"use client";

import { ShieldCheck, LockKeyhole, Database, EyeOff, FileCheck2, ChevronDown } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { DataFlowDiagram } from "@/components/privacy/DataFlowDiagram";
import { PrivacyChecklist } from "@/components/privacy/PrivacyChecklist";

const technicalDetails = [
  ["Embeddings", "Ollama nomic-embed-text by default, with an OpenAI-compatible provider option."],
  ["Generation", "Groq Llama 3.2 90B Vision receives retrieved context rather than uploaded files."],
  ["Session isolation", "Documents, vectors, and audit events are namespaced to the browser session ID."],
  ["UI protection", "Sensitive values are masked in source previews before they are displayed."],
];

export default function PrivacyPage() {
  return (
    <AppShell>
      <div className="mx-auto w-full max-w-6xl space-y-10 p-6 lg:p-10">
        <header className="max-w-3xl">
          <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-accent/20 bg-accent/5 px-3 py-1.5 text-xs font-semibold uppercase tracking-[0.16em] text-accent">
            <ShieldCheck className="h-3.5 w-3.5" />
            Privacy model
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-text-primary sm:text-4xl">Your data stays yours.</h1>
          <p className="mt-3 text-base leading-7 text-text-secondary">
            PrivatePulse processes documents in the local application boundary and sends only retrieved context to the configured language model. Raw uploaded files are not included in model requests by the RAG query path.
          </p>
        </header>

        <section className="grid gap-4 md:grid-cols-3" aria-label="Privacy guarantees">
          <div className="card-base p-5"><LockKeyhole className="mb-4 h-5 w-5 text-accent" /><h2 className="font-semibold text-text-primary">Scoped sessions</h2><p className="mt-2 text-sm leading-6 text-text-secondary">Each browser session gets its own identifier for documents, indexes, and audit records.</p></div>
          <div className="card-base p-5"><Database className="mb-4 h-5 w-5 text-accent" /><h2 className="font-semibold text-text-primary">Minimum context</h2><p className="mt-2 text-sm leading-6 text-text-secondary">Retrieval selects a small set of relevant chunks instead of sending the entire document collection.</p></div>
          <div className="card-base p-5"><EyeOff className="mb-4 h-5 w-5 text-accent" /><h2 className="font-semibold text-text-primary">Masked previews</h2><p className="mt-2 text-sm leading-6 text-text-secondary">Source previews mask common identifiers such as SSNs, phone numbers, emails, and account numbers.</p></div>
        </section>

        <section className="grid gap-6 lg:grid-cols-[1.1fr_.9fr]">
          <DataFlowDiagram />
          <div className="card-base p-6">
            <div className="mb-5 flex items-center gap-2"><FileCheck2 className="h-4 w-4 text-accent" /><h2 className="text-lg font-semibold text-text-primary">Privacy checklist</h2></div>
            <PrivacyChecklist />
          </div>
        </section>

        <section className="card-base p-6 sm:p-8">
          <h2 className="text-xl font-semibold text-text-primary">Technical details</h2>
          <div className="mt-5 divide-y divide-border">
            {technicalDetails.map(([label, value]) => (
              <details key={label} className="group py-4 first:pt-0 last:pb-0">
                <summary className="flex cursor-pointer list-none items-center justify-between gap-4 text-sm font-medium text-text-primary">
                  {label}<ChevronDown className="h-4 w-4 text-text-muted transition-transform group-open:rotate-180" />
                </summary>
                <p className="mt-2 max-w-3xl text-sm leading-6 text-text-secondary">{value}</p>
              </details>
            ))}
          </div>
        </section>

        <section className="rounded-xl border border-warning/20 bg-warning/5 p-5 text-sm leading-6 text-text-secondary">
          <strong className="text-warning">Deployment note.</strong> PrivatePulse AI is a local-first development project, not a compliance certification. Before using regulated data, review the deployment boundary, model-provider terms, access controls, retention, logging, and applicable organizational requirements. Start with synthetic or redacted documents.
        </section>
      </div>
    </AppShell>
  );
}
