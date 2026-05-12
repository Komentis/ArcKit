# ArchKit

> Architecture intelligence for AI-driven development.

ArchKit continuously understands your codebase as a system, keeps that understanding current, and uses it to design features correctly before implementation begins.

---

## Table of Contents

- [Install](#install)
- [Commands](#commands)
- [How it works](#how-it-works)
- [Quick start](#quick-start)
- [Workspace layout](#workspace-layout)
- [Configuration](#configuration)
- [Reference](#reference)
- [Core principle](#core-principle)

---

## Install

ArchKit ships as a Claude Code plugin.

```
/plugin marketplace add Komentis/ArcKit
/plugin install archkit
```

The five slash commands below become available in Claude Code.

---

## Commands

| Command | What it does |
|---|---|
| `/arch-scan` | Scan one or more repos and produce architecture docs + Mermaid diagrams |
| `/arch-feature` | Design a feature against the existing architecture before writing code |
| `/arch-adr` | Create a formal Architecture Decision Record |
| `/arch-review` | Reconcile architecture docs with code — post-merge or drift check |
| `/arch-new-org` | Bootstrap ArchKit for a new org — commandments, config, and repos folder |

---

## How it works

ArchKit operates in three stages:

1. **Scan** — `/arch-scan` reads boundary files (controllers, contracts, events, infrastructure) across all repos under `Repos/` and produces a complete architecture document, Mermaid diagrams, and a list of open unknowns. It uses a three-pass strategy: structure → boundary → targeted deep, so it stays cheap on large codebases.

2. **Design** — `/arch-feature` analyses a proposed feature against the current architecture, produces an impact analysis (services, contracts, data, infrastructure), and generates SpecKit inputs per repo before any code is written.

3. **Reconcile** — `/arch-review` keeps the docs honest. Run it after a merge to reconcile changes, or run it without arguments for a drift check across all repos since the last scan.

Architecture decisions made along the way are captured by `/arch-adr` as numbered ADRs with context, rationale, consequences, and rejected alternatives.

---

## Quick start

### 1. Bootstrap a new workspace

Clone this repo, then run:

```
/arch-new-org
```

It will ask for:
- Organisation context (system type, languages, infrastructure, constraints)
- Where docs should be written (the **Docs root**)
- Which repos to track — names + Git URLs, cloned into `Repos/`

This populates `.archkit/ARCH_COMMANDMENTS.md` and `.archkit/ARCH_CONFIG.md`, then sets up the `Repos/` folder.

### 2. Scan the codebase

```
/arch-scan
```

ArchKit reads every repo under `Repos/` and writes the docs under your configured Docs root (default `docs/`).

### 3. Design a feature

```
/arch-feature add lesson retry endpoint with daily limit
```

Produces a feature design file under `docs/features/` with impact analysis and per-repo SpecKit inputs.

### 4. Keep docs honest

After merging changes:

```
/arch-review PR-123
```

Or for a periodic drift check:

```
/arch-review
```

---

## Workspace layout

```
.archkit/           ← config, commandments, prompts, templates
.claude/commands/   ← slash command definitions
Repos/              ← cloned source repos (gitignored)
docs/               ← generated architecture docs (gitignored)
plugin/             ← distributable plugin package
```

`Repos/` and `docs/` are gitignored — they're working state, not source.

---

## Configuration

`.archkit/ARCH_CONFIG.md` is the single source of truth for output paths. Edit **Folder Roots** once to relocate all docs (e.g. drop the `docs/` prefix to put everything at the repo root).

Two document layers are enforced:

- **Conceptual** — `system-intent.md`, `domain-model.md`, `DIAGRAMS.md`. Stable. Only regenerated when the fundamental architecture changes (new bounded context, major flow redesign, strategic model shift).
- **Implementation** — `ARCHITECTURE.md`, `devops.md`, `infrastructure.md`, `state-machines.md`, etc. Regenerated whenever relevant code changes.

This split keeps the conceptual story stable across routine code changes while keeping the as-built picture current.

---

## Reference

| File | Purpose |
|---|---|
| [.archkit/ARCH_COMMANDMENTS.md](./.archkit/ARCH_COMMANDMENTS.md) | The governing principles — everything operates under these |
| [.archkit/ARCH_CONFIG.md](./.archkit/ARCH_CONFIG.md) | Output paths and repo discovery |
| [.archkit/ARCH_SCAN_STRATEGY.md](./.archkit/ARCH_SCAN_STRATEGY.md) | Three-pass scan strategy: structure → boundary → targeted deep |
| [.archkit/ARCH_DOC_TEMPLATE.md](./.archkit/ARCH_DOC_TEMPLATE.md) | The output format produced by `/arch-scan` |
| [.archkit/ARCH_DIAGRAMS_GUIDE.md](./.archkit/ARCH_DIAGRAMS_GUIDE.md) | Mermaid diagram specs — C4 context, container, data flow, sequence |
| [.archkit/ARCHKIT_SCAN_PROMPT.md](./.archkit/ARCHKIT_SCAN_PROMPT.md) | Detailed scan prompt used by `/arch-scan` |
| [.archkit/ARCHKIT_CLARIFY_PROMPT.md](./.archkit/ARCHKIT_CLARIFY_PROMPT.md) | Targeted clarification of open unknowns |
| [.archkit/ARCH_COMMANDMENTS_TEMPLATE.md](./.archkit/ARCH_COMMANDMENTS_TEMPLATE.md) | Template for creating org-specific commandments |
| [.archkit/QUICKSTART.md](./.archkit/QUICKSTART.md) | Full usage guide |
| [START_HERE.md](./START_HERE.md) | File checklist for collecting repo context before scanning |

---

## Core principle

> Read files that define boundaries, contracts, composition, and deployment first.
> Read implementation only when a boundary, change, or feature requires clarification.

This keeps scans fast and outputs grounded. Implementation files are read only when a boundary is ambiguous or a feature requires deeper understanding.
