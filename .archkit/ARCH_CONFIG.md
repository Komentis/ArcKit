# ArchKit — Configuration
> Edit this file to reconfigure output paths. All ArchKit commands read this file before writing anything.

---

## Table of Contents

- [Folder Roots](#folder-roots)
- [Output Files](#output-files)
- [Repos Discovery](#repos-discovery)

---

## Folder Roots

| Setting | Value |
|---|---|
| Docs root | `docs/` |
| Architecture folder | `docs/architecture/` |
| Features folder | `docs/features/` |
| Decisions folder | `docs/decisions/` |

---

## Output Files

| File | Path |
|---|---|
| Documentation entry point | `docs/README.md` |
| Architecture main document | `docs/architecture/ARCHITECTURE.md` |
| Diagrams | `docs/architecture/DIAGRAMS.md` |
| Domain model | `docs/architecture/domain-model.md` |
| State machines | `docs/architecture/state-machines.md` |
| System intent | `docs/architecture/system-intent.md` |
| AI architecture | `docs/architecture/ai-architecture.md` |
| Failure strategy | `docs/architecture/failure-strategy.md` |
| Observability | `docs/architecture/observability.md` |
| Unknowns | `docs/architecture/unknowns.md` |
| Agent summary | `docs/architecture/agent-summary.md` |
| Feature design | `docs/features/[feature-name].md` |
| Architecture decision (ADR) | `docs/decisions/ADR-[number]-[kebab-title].md` |

---

## Repos Discovery

| Setting | Value |
|---|---|
| Repos folder | `Repos/` |
| Fallback (if `Repos/` not found) | Scan current working directory |
