# ArchKit — Start Here
> First test: validate the scan prompt on a real repo

---

## Table of Contents

- [What you need to do](#what-you-need-to-do)
  - [1. Gather files from one repo](#1-gather-files-from-one-repo)
  - [2. Open a new Claude session](#2-open-a-new-claude-session)
  - [3. Paste the scan prompt](#3-paste-the-scan-prompt)
  - [4. Review what comes back](#4-review-what-comes-back)
  - [5. Save the output](#5-save-the-output)
- [Files in this folder](#files-in-this-folder)

---

## What you need to do

### 1. Gather files from one repo

From any repo in this project root, collect these files and copy their contents:

**Always grab:**
- `README.md`
- Any `docker-compose.yml` or `Dockerfile`
- Any `.sln`, `.csproj`, `package.json`, `go.mod`
- Any CI/CD pipeline files (`.yml` in `.github/workflows/` or `azure-pipelines.yml`)
- Top-level folder listing (run `tree -L 2` or just list the folders)

**Also grab if present:**
- `Program.cs` or main entry point
- Any files in `Controllers/`, `Endpoints/`, `Routes/`
- Any OpenAPI / Swagger files
- Any files in `Contracts/`, `Dtos/`, `Events/`

You don't need everything. Structural and boundary files only.

---

### 2. Open a new Claude session

Start fresh. Paste all the file contents you collected, clearly labelled by filename.

---

### 3. Paste the scan prompt

Copy the full contents of `ARCHKIT_SCAN_PROMPT.md` and paste it at the end of your message.

Send it.

---

### 4. Review what comes back

Check the output against what you know about the repo:
- Are all the services correct?
- Are the connections accurate?
- Did it miss anything important?
- Did it invent anything that isn't there?

Note anything wrong. Those corrections are the most valuable thing you can collect right now.

---

### 5. Save the output

Save the architecture doc and diagrams somewhere in the repo (e.g. `/docs/`).

Note what you had to correct. Feed that back as a refinement to `ARCHKIT_SCAN_PROMPT.md`.

---

## Files in this folder

| File | Purpose |
|---|---|
| `START_HERE.md` | This file |
| `ARCHKIT_SCAN_PROMPT.md` | Paste into Claude to run the scan |
| `ARCH_DOC_TEMPLATE.md` | Output format Claude will follow |
| `ARCH_DIAGRAMS_GUIDE.md` | Mermaid diagram specs |
| `ARCH_COMMANDMENTS.md` | Governing principles |
| `ARCH_SCAN_STRATEGY.md` | How the scan works (reference) |
| `QUICKSTART.md` | Full usage guide |
