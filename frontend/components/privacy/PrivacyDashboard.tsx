import { Database, EyeOff, LockKeyhole } from "lucide-react";

const items = [
  {
    title: "Scoped sessions",
    description: "Each browser session gets its own identifier for documents, indexes, and audit records.",
    icon: LockKeyhole,
  },
  {
    title: "Minimum context",
    description: "Retrieval selects a small set of relevant chunks instead of sending the entire document collection.",
    icon: Database,
  },
  {
    title: "Masked previews",
    description: "Source previews mask common identifiers such as SSNs, phone numbers, emails, and account numbers.",
    icon: EyeOff,
  },
] as const;

export function PrivacyDashboard() {
  return (
    <div className="grid gap-4 md:grid-cols-3" aria-label="Privacy guarantees">
      {items.map(({ title, description, icon: Icon }) => (
        <div key={title} className="card-base p-5">
          <Icon className="mb-4 h-5 w-5 text-accent" />
          <h2 className="font-semibold text-text-primary">{title}</h2>
          <p className="mt-2 text-sm leading-6 text-text-secondary">{description}</p>
        </div>
      ))}
    </div>
  );
}
