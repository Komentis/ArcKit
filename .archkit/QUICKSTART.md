# ArchKit — Quickstart Guide
> Milestone 1: Repo Scanner & Living Architecture Docs

ArchKit is the SpecKit equivalent for architecture. It gives you a repeatable, prompt-driven process to scan a codebase and produce accurate architecture documentation and Mermaid diagrams.

---

## Table of Contents

- [What You Need](#what-you-need)
- [How to Run a Scan (Direct Claude Method)](#how-to-run-a-scan-direct-claude-method)
  - [Step 1 — Start a new Claude conversation](#step-1--start-a-new-claude-conversation)
  - [Step 2 — Provide your codebase](#step-2--provide-your-codebase)
  - [Step 3 — Paste the scan prompt](#step-3--paste-the-scan-prompt)
  - [Step 4 — Review the output](#step-4--review-the-output)
  - [Step 5 — Save and iterate](#step-5--save-and-iterate)
- [What Good Output Looks Like](#what-good-output-looks-like)
- [Iterating Towards the Bot](#iterating-towards-the-bot)
- [Known Limitations (Milestone 1)](#known-limitations-milestone-1)

---

## What You Need

| File | Purpose |
|---|---|
| `ARCHKIT_SCAN_PROMPT.md` | Paste this into Claude to kick off a scan |
| `ARCH_DOC_TEMPLATE.md` | The output format Claude will produce |
| `ARCH_DIAGRAMS_GUIDE.md` | Diagram specs Claude will follow |

---

## How to Run a Scan (Direct Claude Method)

### Step 1 — Start a new Claude conversation

Open a fresh Claude session. Do not use an existing context-heavy conversation.

### Step 2 — Provide your codebase

Share your repo in one of these ways:

**Option A — Paste key files directly**
Copy and paste the most important files: entry points, service definitions, route files, schema files, Docker/CI configs. You don't need everything — focus on the structural files.

**Option B — Describe the structure**
If the codebase is too large, paste the folder/file tree (run `tree -L 3` or similar) and then paste individual files as Claude asks for them.

**Option C — Share a ZIP or specific files**
Upload files directly if your Claude interface supports it.

### Step 3 — Paste the scan prompt

Copy the full contents of `ARCHKIT_SCAN_PROMPT.md` and paste it after your codebase context. This tells Claude exactly what to analyse and produce.

### Step 4 — Review the output

Claude will produce:
- A structured architecture document (following `ARCH_DOC_TEMPLATE.md`)
- Mermaid diagrams (following `ARCH_DIAGRAMS_GUIDE.md`)

Review for accuracy. Correct anything that is wrong. These corrections become valuable — they are the kind of signal that will later improve the automated system.

### Step 5 — Save and iterate

Save the output. If something is wrong, correct it in the conversation and note what the scan missed. Over time this builds up a set of refinements to the prompt itself.

---

## What Good Output Looks Like

A successful Milestone 1 scan produces:

- **System Overview** — one paragraph describing what the system does and its core components
- **Service/Module Map** — every discrete service or module, what it does, its tech stack
- **Communication Map** — how services talk to each other (REST, events, queues, direct DB, etc.)
- **Data Model Summary** — key entities and where they live
- **External Dependencies** — third-party services, APIs, auth providers, cloud resources
- **C4 Context Diagram** — the system and its external actors (Mermaid)
- **C4 Container Diagram** — all services and how they connect (Mermaid)
- **Data Flow Diagram** — key data paths through the system (Mermaid)

---

## Iterating Towards the Bot

Once you have run this manually 3–5 times and the output quality is consistent:

1. Note which parts of the scan prompt needed fixing
2. Note which file types Claude needed to look at most
3. Note which diagram types were most useful

That refinement work directly informs the OpenClaw ArchBot system prompt and the automated repo scanner logic.

---

## Known Limitations (Milestone 1)

- Claude cannot browse a live repo — you must provide files or structure
- Very large repos need to be broken into domains/services and scanned separately
- Monorepos work best when you scan one service at a time, then produce a system-wide view

These limitations go away in the automated bot version (Milestone 2+).
