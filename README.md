# ArchKit

> Architecture intelligence for AI-driven development.

ArchKit continuously understands your codebase as a system, keeps that understanding current, and uses it to design features correctly before implementation begins.

---

## Install

```
/plugin marketplace add Komentis/ArcKit
```

After installation, the skills below become available in Claude Code.

---

## Skills

| Skill | What it does |
|---|---|
| `arch-scan` | Scan one or more repos and produce architecture docs + Mermaid diagrams |
| `arch-feature` | Design a feature against the existing architecture before writing code |
| `arch-adr` | Create a formal Architecture Decision Record |
| `arch-review` | Reconcile architecture docs with code — post-merge or drift check |
| `arch-new-org` | Bootstrap ArchKit for a new org — commandments, config, and repos folder |

---

## Reference

See [START_HERE.md](./START_HERE.md) for the detailed usage guide and the file layout under `.archkit/`.

| File | Purpose |
|---|---|
| `.archkit/ARCH_COMMANDMENTS.md` | Governing principles |
| `.archkit/ARCH_CONFIG.md` | Output paths and repo discovery |
| `.archkit/ARCH_SCAN_STRATEGY.md` | Three-pass scan strategy |
| `.archkit/ARCH_DOC_TEMPLATE.md` | Architecture document template |
| `.archkit/ARCH_DIAGRAMS_GUIDE.md` | Mermaid diagram specs |
| `.archkit/ARCHKIT_SCAN_PROMPT.md` | Detailed scan prompt |
| `.archkit/ARCHKIT_CLARIFY_PROMPT.md` | Targeted clarification of open unknowns |

---

## Core Principle

> Read files that define boundaries, contracts, composition, and deployment first.
> Read implementation only when a boundary, change, or feature requires clarification.
