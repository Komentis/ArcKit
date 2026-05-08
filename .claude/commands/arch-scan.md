You are an expert software architect performing an ArchKit architecture scan.

$ARGUMENTS

## Repo Discovery

Before scanning, discover all repositories to include:

1. Read the **Repos Discovery** section of `@.archkit/ARCH_CONFIG.md` to get the configured repos folder (default: `Repos/`).
2. Look for the configured repos folder in the current working directory.
3. If it exists, treat **every immediate subdirectory of that folder** as a separate repository to scan. Scan all of them.
4. If it does not exist (or the configured fallback is the current working directory), scan the current working directory itself.

Treat this as a **Bootstrap Scan** (as defined in `ARCH_SCAN_STRATEGY.md`): structural scan + boundary scan across all repositories, with targeted deep scan only where boundaries are unclear.

The output files must always be written relative to the **current working directory** (i.e. the ArcKit root), not inside any individual repo.

---

Read and follow these files before doing anything else:
- Output paths (authoritative): @.archkit/ARCH_CONFIG.md
- Governing principles: @.archkit/ARCH_COMMANDMENTS.md
- Scan strategy (how to scan, what to read, in what order): @.archkit/ARCH_SCAN_STRATEGY.md
- Output format for the architecture document: @.archkit/ARCH_DOC_TEMPLATE.md
- Diagram specifications: @.archkit/ARCH_DIAGRAMS_GUIDE.md
- Pre-work git workflow (**follow this first, before reading any code**): @.archkit/shared/WORKFLOW_START.md

---

Once you have read those files, perform the scan in this order:

1. State your understanding of the system in 2–3 sentences. If anything is unclear, ask one question before proceeding.

2. Run Pass 1 (Structural Scan) — for **each repo discovered in the configured repos folder**, read: README, project files, Docker, CI/CD, folder structure. Extract: services, roles, infrastructure footprint per repo. Stop here if you can name every service with HIGH confidence.

3. Run Pass 2 (Boundary Scan) — for **each repo**, read: controllers, contracts, events, OpenAPI, startup/DI files. Extract: what each service exposes and consumes, all connections, contract locations. Pay special attention to cross-repo contracts (shared libraries, event schemas, OpenAPI specs consumed between repos).

4. Run Pass 3 (Targeted Deep Scan) only if a boundary is still ambiguous after Pass 2. Read only what resolves the specific ambiguity.

5. Map all communication patterns. Label inferred connections [INFERRED].

6. Identify data models and ownership.

7. Identify external dependencies.

8. List all unknowns as [UNKNOWN — reason].

9. Infer and document:
   - system intent and design principles
   - conceptual domain model
   - lifecycle/state-machine behaviour where visible from events, statuses, or workflows
   - failure points, retry expectations, and idempotency requirements
   - AI architecture, if AI/LLMs/agents are present
   - observability/monitoring signals and notable gaps
   - DevOps and infrastructure: CI/CD pipelines, IaC, environments, deployment strategy, networking, security infra, DR

10. Produce the full architecture document using ARCH_DOC_TEMPLATE.md. Fill every section.

11. Produce all four Mermaid diagrams using ARCH_DIAGRAMS_GUIDE.md.

12. Produce confidence assessment: HIGH / MEDIUM / LOW per section with reasons.

---

## Output

Write all output files to the paths defined in **ARCH_CONFIG.md** (already read above). All paths are relative to the **current working directory** (the directory from which this scan was invoked — not a subdirectory discovered during scanning, even if that subdirectory contains its own `.git`).

If a path does not exist, create it.

### Required output files

All file paths come from ARCH_CONFIG.md. Required outputs are:

- Documentation entry point (create or update)
- Architecture main document
- Diagrams
- Domain model
- State machines
- System intent
- AI architecture
- Failure strategy
- Observability
- DevOps & CI/CD
- Infrastructure
- Unknowns
- Agent summary

### Requirements for the README in the configured Docs root

Create or update the `README.md` file in the configured Docs root defined by `@.archkit/ARCH_CONFIG.md`. This is the human entry point for anyone navigating the documentation.

Use exactly this structure:

```markdown
# [System Name] — [one-sentence description]

[What this system does — 2–3 sentences, plain language]

## Table of Contents

- [Architecture Documentation](#architecture-documentation)
- [Quick Links](#quick-links)
- [Repositories](#repositories)

## Architecture Documentation

- [Architecture Overview](./architecture/ARCHITECTURE.md) — main entry point

## Quick Links

| Document | Description |
|---|---|
| [Architecture Overview](./architecture/ARCHITECTURE.md) | System summary, service map, communication map |
| [Domain Model](./architecture/domain-model.md) | Core business entities and relationships |
| [State Machines](./architecture/state-machines.md) | Lifecycle states and transitions |
| [AI Architecture](./architecture/ai-architecture.md) | AI models, agents, and orchestration |
| [Failure Strategy](./architecture/failure-strategy.md) | Failure points, retry behaviour, idempotency gaps |
| [Observability](./architecture/observability.md) | Logging, telemetry, monitoring gaps |
| [DevOps & CI/CD](./architecture/devops.md) | CI/CD pipelines, environments, deployment strategy |
| [Infrastructure](./architecture/infrastructure.md) | IaC, networking, security infrastructure, DR |
| [Diagrams](./architecture/DIAGRAMS.md) | C4 context, container, data flow, sequence |
| [Unknowns](./architecture/unknowns.md) | Gaps and unresolved ambiguities |

## Repositories

| Repo | Description |
|---|---|
| RepoName | One-line description |
```

Rules:
- Keep descriptions in the Quick Links table short and distinct — one phrase each
- List every repo discovered under the configured repos folder in the Repositories table — repo names only, no links (the docs repo does not contain the source repos)
- If a `README.md` already exists, update only the architecture sections. Preserve any content not related to architecture.

---

### Requirements for the Architecture main document

Produce a single combined `.md` file containing, in this order:

1. Understanding statement + which passes you ran
2. Full architecture document (all sections from ARCH_DOC_TEMPLATE.md)
3. Embedded links to supporting architecture documents
4. Embedded links to diagrams
5. Confidence assessment table
6. Clarifying questions (max 5, if any)

At the top of `ARCHITECTURE.md`, include a **System Summary** section that contains:

- **Purpose**
- **System Type**
- **Key Technologies**

Then include a **Supporting Documents** section with relative links to:

- `./domain-model.md`
- `./state-machines.md`
- `./system-intent.md`
- `./ai-architecture.md`
- `./failure-strategy.md`
- `./observability.md`
- `./devops.md`
- `./unknowns.md`
- `./agent-summary.md`

Then include a **Diagrams** section with relative links to:

- `./DIAGRAMS.md`

Do not duplicate large sections from the supporting files unnecessarily. `ARCHITECTURE.md` must act as the main entry point and navigation hub.

### Requirements for the Diagrams file

Create a separate file containing only:

1. Context diagram
2. Container diagram
3. Data flow diagram
4. Sequence diagram

For each diagram include:
- Title
- 2–3 sentence explanation
- A ```mermaid code block

### Requirements for supporting files

Also populate these focused files at the paths defined in ARCH_CONFIG.md:

- **system-intent** — system purpose, design principles, observed vs inferred notes
- **domain-model** — conceptual/business entities and relationships
- **state-machines** — lifecycle states, transitions, triggers
- **ai-architecture** — models, agent roles, orchestration patterns, AI integration points
- **failure-strategy** — failure points, retry expectations, idempotency requirements, missing protections
- **observability** — logging, telemetry, correlation, metrics, monitoring gaps
- **devops** — CI/CD pipelines, environments, deployment strategy
- **infrastructure** — IaC, networking, security infrastructure, DR
- **unknowns** — all unknowns and unresolved ambiguities
- **agent-summary** — concise machine-friendly summary of purpose, entities, flows, and constraints

If a supporting file cannot be fully completed, still create it and write:
`[UNKNOWN — reason]`

---

## Rules

- Never invent services, boundaries, or flows not supported by evidence.
- Use exact names from the codebase.
- Mark inferred content explicitly as `[INFERRED]`.
- Mark unresolved gaps explicitly as `[UNKNOWN — reason]`.
- Preserve real complexity; do not flatten the system for convenience.
- Prefer links over duplication when content is split across files.
- **Every `.md` file produced must include a table of contents** immediately after the title/subtitle block and before the first section. The ToC must use relative anchor links to every heading in the document. Example format:

```markdown
## Table of Contents

- [Section One](#section-one)
- [Section Two](#section-two)
  - [Subsection](#subsection)
```

- Always create or update the documentation entry point (path from ARCH_CONFIG.md) as part of every scan.

---

## Finishing Up

Once all files are written, follow: @.archkit/shared/WORKFLOW_FINISH.md