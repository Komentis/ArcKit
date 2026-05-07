# ArchKit — Configuration
> Edit this file to reconfigure output paths. All ArchKit commands read this file before writing anything.

---

## Table of Contents

- [Folder Roots](#folder-roots)
- [Output Files](#output-files)
- [Document Layers](#document-layers)
- [Repos Discovery](#repos-discovery)

---

## Folder Roots

Folder Roots are the single source of truth for output paths. To relocate the docs (e.g. drop the `docs/` prefix), edit only this table.

| Root | Value |
|---|---|
| Docs root | `docs/` |
| Architecture folder | `docs/architecture/` |
| Features folder | `docs/features/` |
| Decisions folder | `docs/decisions/` |

---

## Output Files

Filenames only. **Full output path = the matching Folder Roots value + the filename below.**

| File | Folder | Filename |
|---|---|---|
| Documentation entry point | Docs root | `README.md` |
| Architecture main document | Architecture folder | `ARCHITECTURE.md` |
| Diagrams | Architecture folder | `DIAGRAMS.md` |
| Domain model | Architecture folder | `domain-model.md` |
| State machines | Architecture folder | `state-machines.md` |
| System intent | Architecture folder | `system-intent.md` |
| AI architecture | Architecture folder | `ai-architecture.md` |
| Failure strategy | Architecture folder | `failure-strategy.md` |
| Observability | Architecture folder | `observability.md` |
| Unknowns | Architecture folder | `unknowns.md` |
| Agent summary | Architecture folder | `agent-summary.md` |
| DevOps & CI/CD | Architecture folder | `devops.md` |
| Infrastructure | Architecture folder | `infrastructure.md` |
| Feature design | Features folder | `[feature-name].md` |
| Architecture decision (ADR) | Decisions folder | `ADR-[number]-[kebab-title].md` |

---

## Document Layers

### Conceptual (stable — update only when architecture fundamentally changes)

These files represent **what the system is and why** — bounded contexts, primary flows, domain model. They should NOT be regenerated on routine code changes (bug fixes, new endpoints, refactors). Only regenerate when the fundamental architecture changes (new bounded context, major flow redesign, strategic model shift).

In Architecture folder:
- `system-intent.md`
- `domain-model.md`
- `DIAGRAMS.md`

### Implementation (update when code changes)

These files represent **how the system is built** — as-built detail, deployment, failure handling, observability. They MUST be regenerated whenever relevant code changes.

In Architecture folder:
- `ARCHITECTURE.md`
- `agent-summary.md`
- `ai-architecture.md`
- `failure-strategy.md`
- `observability.md`
- `state-machines.md`
- `devops.md`
- `infrastructure.md`
- `unknowns.md`

---

## Repos Discovery

| Setting | Value |
|---|---|
| Repos folder | `Repos/` |
| Fallback (if `Repos/` not found) | Scan current working directory |
