# Komentis Plugins

> A multi-tool marketplace of Claude Code and Gemini CLI plugins for AI-driven engineering work.

This repo is structured as a **plugin marketplace**. The flagship plugin is **ArchKit** (architecture intelligence). More plugins (e.g. `techlead`) live alongside it under `plugins/`.

---

## Repo layout

```
.claude-plugin/marketplace.json   ← lists every plugin (Claude Code marketplace)
plugins/
  archkit/                        ← architecture scan/design/ADR/review + verifier
    .claude-plugin/plugin.json    ← Claude Code wrapper
    skills/<name>/SKILL.md
    gemini-extension.json         ← Gemini CLI wrapper
    gemini-commands/*.toml
  techlead/                       ← placeholder for the Tech Lead orchestrator
.archkit/                         ← canonical prompts, configs, templates (tool-neutral)
archkit/                          ← Python verifier (works with either agent)
```

Each plugin folder holds **two thin wrappers** — one for Claude Code, one for Gemini CLI — around a single canonical body of prompts that lives at the repo root. The Python verifier is tool-agnostic and runs from the repo root regardless of which agent did the scan.

---

## Table of Contents

- [Install](#install)
- [Commands](#commands)
- [How it works](#how-it-works)
- [Quick start](#quick-start)
- [Workspace layout](#workspace-layout)
- [Configuration](#configuration)
- [Verify](#verify)
- [Reference](#reference)
- [Core principle](#core-principle)

---

## Install

### Claude Code

```
/plugin marketplace add Komentis/ArcKit
/plugin install archkit
```

Other plugins from this marketplace install the same way: `/plugin install <name>`.

### Gemini CLI

Each plugin under `plugins/` is also a Gemini extension. From the repo root:

```
gemini extensions install plugins/archkit
```

The same five commands become available in Gemini CLI. (Other plugins install the same way: `gemini extensions install plugins/<name>`.)

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

## Verify

ArchKit ships with a deterministic verification layer — a small Python package that parses the generated docs into a structured fact model, validates discipline markers, and lints the embedded Mermaid blocks.

```bash
python -m archkit verify docs/
```

This is what makes the anti-hallucination guarantees enforceable rather than aspirational:

- Every claim must carry `[OBSERVED]`, `[INFERRED]`, `[UNKNOWN — reason]`, or `[CLARIFIED]`
- Service tables must have a Confidence column with `HIGH`/`MEDIUM`/`LOW`
- No stub placeholders (`[TBD]`, `[FILL …]`, `???`) may survive
- Mermaid blocks must declare a valid diagram type and have balanced brackets / well-formed arrows
- Two runs over the same codebase produce diffable JSON fact models (`python -m archkit parse docs/ -o out.json`)

Zero dependencies; Python 3.10+. See [archkit/README.md](./archkit/README.md) for the full check list.

Run the test suite with:

```bash
python -m unittest discover -s archkit/tests
```

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
| [archkit/README.md](./archkit/README.md) | Deterministic verification CLI — what it checks, how to run it |
| [START_HERE.md](./START_HERE.md) | File checklist for collecting repo context before scanning |

---

## Core principle

> Read files that define boundaries, contracts, composition, and deployment first.
> Read implementation only when a boundary, change, or feature requires clarification.

This keeps scans fast and outputs grounded. Implementation files are read only when a boundary is ambiguous or a feature requires deeper understanding.
