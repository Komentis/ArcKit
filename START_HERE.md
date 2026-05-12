# ArchKit

Architecture intelligence for AI-driven development.

ArchKit continuously understands your codebase as a system, keeps that understanding
current, and uses it to design features correctly before implementation begins.

---

## Quick Start

Run `/arch-scan` in Claude with repo files pasted in to generate an architecture
document and Mermaid diagrams for any repo.

---

## Slash Commands

| Command | What it does |
|---|---|
| `/arch-scan` | Scan a repo and produce architecture docs + diagrams |
| `/arch-feature` | Design a feature against the existing architecture before writing code |
| `/arch-adr` | Create a formal Architecture Decision Record |
| `/arch-review` | Post-merge reconciliation — update architecture docs from a diff |
| `/arch-new-org` | Set up org-specific architecture commandments |

---

## How to Use /arch-scan

1. Collect structural files from a repo — README, project files, Dockerfiles,
   CI/CD config, top-level folder structure
2. Also grab boundary files — controllers, contracts, events, OpenAPI specs
3. Open a new Claude session, paste the files, then run `/arch-scan`
4. Review the output. Note anything wrong — those corrections improve the prompt
5. Save the architecture doc to `/docs/` in the repo

See the Reference Docs table below for the detailed checklists.

---

## How to Use /arch-feature

Before picking up any feature that touches architecture (new service, contract change,
new dependency, data ownership change):

1. Paste the current architecture doc for the system
2. Run `/arch-feature [describe the feature]`
3. Review the impact analysis and design
4. Approve before handing to coding agents

---

## Reference Docs

| File | Purpose |
|---|---|
| `.archkit/ARCH_COMMANDMENTS.md` | The 13 governing principles — everything operates under these |
| `.archkit/ARCH_SCAN_STRATEGY.md` | How scanning works: three passes, file prioritisation, scan modes |
| `.archkit/ARCH_DOC_TEMPLATE.md` | The output format produced by `/arch-scan` |
| `.archkit/ARCH_DIAGRAMS_GUIDE.md` | Mermaid diagram specs — C4 context, container, data flow, sequence |
| `.archkit/ARCH_COMMANDMENTS_TEMPLATE.md` | Template for creating org-specific commandments |
| `.archkit/QUICKSTART.md` | Full usage guide |

---

## Core Principle

> Read files that define boundaries, contracts, composition, and deployment first.
> Read implementation only when a boundary, change, or feature requires clarification.

---

## Project Structure