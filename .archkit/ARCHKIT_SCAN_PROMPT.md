# ArchKit — Repo Scan Prompt

> Paste this into Claude after providing your codebase context
> Governed by: ARCH_COMMANDMENTS.md and ARCH_SCAN_STRATEGY.md

---

## Table of Contents

- [Commandment Enforcement](#commandment-enforcement)
- [Document Layer Rules](#document-layer-rules)
- [Output Structure Requirement](#output-structure-requirement)
  - [Requirements for docs/README.md](#requirements-for-docsreadmemd)
  - [Table of Contents Requirement](#table-of-contents-requirement)
- [STEP 1 — Understand What You Have Been Given](#step-1--understand-what-you-have-been-given)
- [STEP 2 — Pass 1: Structural Scan](#step-2--pass-1-structural-scan)
- [STEP 3 — Pass 2: Boundary Scan](#step-3--pass-2-boundary-scan)
- [STEP 3b — Pass 3: Targeted Deep Scan](#step-3b--pass-3-targeted-deep-scan)
- [STEP 4 — Map Communication Patterns](#step-4--map-communication-patterns)
- [STEP 5 — Identify Data Models and Ownership](#step-5--identify-data-models-and-ownership)
- [STEP 6 — Identify External Dependencies](#step-6--identify-external-dependencies)
- [STEP 7 — Identify Unknowns and Gaps](#step-7--identify-unknowns-and-gaps)
- [STEP 8 — System Intent & Design Principles](#step-8--system-intent--design-principles)
- [STEP 9 — Domain Model (Conceptual)](#step-9--domain-model-conceptual)
- [STEP 10 — State Machines](#step-10--state-machines)
- [STEP 11 — Failure, Retry & Idempotency](#step-11--failure-retry--idempotency)
- [STEP 12 — AI Architecture](#step-12--ai-architecture)
- [STEP 13 — Observability & Metrics](#step-13--observability--metrics)
- [STEP 14 — DevOps & CI/CD](#step-14--devops--cicd)
- [STEP 15 — Infrastructure](#step-15--infrastructure)
- [STEP 16 — Produce the Architecture Document](#step-16--produce-the-architecture-document)
- [STEP 17 — Produce Mermaid Diagrams](#step-17--produce-mermaid-diagrams)
- [STEP 18 — Confidence Assessment](#step-18--confidence-assessment)
- [STEP 19 — Agent Summary](#step-19--agent-summary)
- [OUTPUT FORMAT](#output-format)
- [IMPORTANT RULES](#important-rules)

---

You are an expert software architect.

Your job is to analyse the codebase I have provided and produce a complete, accurate architecture document and set of Mermaid diagrams for it.

Follow this process exactly. Do not skip steps.

**Scanning discipline:** You must follow the staged scan strategy — structure first, boundaries second, implementation last. Read high-signal files before low-signal files. Do not read implementation files unless Passes 1 and 2 are insufficient. Do not invent what you have not observed.

---

## 🔴 Commandment Enforcement

Before proceeding, explicitly acknowledge:

* You will follow **ARCH_COMMANDMENTS.md**
* You will follow **ARCH_SCAN_STRATEGY.md**
* You will read **ARCH_CONFIG.md** and use its paths for all output files
* You will label all inferred information
* You will not invent missing details

---

## 🔴 Document Layer Rules

ArchKit output is split into two layers. You MUST apply these rules to every file you produce:

### Conceptual layer (stable)

Files: `docs/architecture/system-intent.md`, `docs/architecture/domain-model.md`, `docs/architecture/DIAGRAMS.md`

**Rule**: Only regenerate these files if the **fundamental architecture** has changed — new bounded contexts, major flow redesign, strategic domain model shift. Do **NOT** regenerate them for routine code changes (bug fixes, new endpoints, dependency upgrades, refactors). If existing versions of these files were provided and the architecture has not fundamentally changed, **omit them from your output** (no FILE marker = no change).

### Implementation layer (updated on code changes)

Files: `docs/architecture/ARCHITECTURE.md`, `docs/architecture/agent-summary.md`, `docs/architecture/ai-architecture.md`, `docs/architecture/failure-strategy.md`, `docs/architecture/observability.md`, `docs/architecture/state-machines.md`, `docs/architecture/devops.md`, `docs/architecture/infrastructure.md`, `docs/architecture/unknowns.md`

**Rule**: Regenerate these files whenever relevant code has changed or the file is missing. They reflect the current as-built state of the system.

---

## 🔴 Output Structure Requirement

All output paths come from **ARCH_CONFIG.md**. Read that file before writing anything.

Minimum required outputs (paths from ARCH_CONFIG.md):

* Documentation entry point (create or update — see requirements below)
* Architecture main document
* Diagrams
* Domain model
* State machines
* System intent
* AI architecture
* Failure strategy
* Observability
* DevOps & CI/CD
* Infrastructure
* Unknowns
* Agent summary

If a section cannot be completed:

* Create it anyway
* Use `[UNKNOWN — reason]`

### Requirements for `docs/README.md`

Create or update `docs/README.md`. Use exactly this structure:

```markdown
# [System Name] — [one-sentence description]

[What this system does — 2–3 sentences, plain language]

## Table of Contents

- [Conceptual Design](#conceptual-design)
- [Architecture Documentation](#architecture-documentation)
- [Repositories](#repositories)

## Conceptual Design

> Stable. Changes only when the fundamental architecture changes.

[Write 3–5 sentences describing the system's purpose, its primary actors, and how the major parts fit together. Use plain language. No implementation detail.]

### System Context

[Write 2–3 sentences explaining how this system fits into the broader organisational landscape — who uses it, what external systems it integrates with, and what value it delivers.]

```mermaid
C4Context
  title System Context — [System Name]
  [Produce a C4 Context diagram here — actors on the left, the system in the centre, external systems on the right]
```

### System Overview

[Write 2–4 sentences describing the major subsystems or bounded contexts and how they interact at a high level.]

```mermaid
C4Container
  title Container Diagram — [System Name]
  [Produce a C4 Container diagram here — one box per major service/component, showing the primary communication paths]
```

### Design Principles

[List 3–6 bullet points capturing the key architectural decisions and constraints that shape this system. Examples: event-driven, eventual consistency, CQRS, AI-first, stateless services, etc.]

- [Principle 1]
- [Principle 2]
- [Principle 3]

## Architecture Documentation

> Updated whenever code changes. Reflects the current as-built state.

| Document | Description |
|---|---|
| [Architecture Overview](./architecture/ARCHITECTURE.md) | System summary, service map, communication map |
| [System Intent](./architecture/system-intent.md) | Purpose, design principles, bounded contexts |
| [Domain Model](./architecture/domain-model.md) | Core business entities and relationships |
| [Diagrams](./architecture/DIAGRAMS.md) | Full C4 diagrams, data flow, sequence diagrams |
| [Agent Summary](./architecture/agent-summary.md) | AI agents, roles, and orchestration |
| [AI Architecture](./architecture/ai-architecture.md) | AI models, prompts, and integration patterns |
| [Failure Strategy](./architecture/failure-strategy.md) | Failure points, retry behaviour, idempotency gaps |
| [Observability](./architecture/observability.md) | Logging, telemetry, monitoring gaps |
| [State Machines](./architecture/state-machines.md) | Lifecycle states and transitions |
| [DevOps & CI/CD](./architecture/devops.md) | Pipelines, deployment strategy, environments |
| [Infrastructure](./architecture/infrastructure.md) | Cloud resources, networking, IaC, security, DR |
| [Unknowns](./architecture/unknowns.md) | Gaps and unresolved ambiguities |

## Repositories

| Repo | Description |
|---|---|
| RepoName | One-line description |
```

Rules:
- The **Conceptual Design** section MUST appear before Architecture Documentation — do not reorder.
- The Conceptual Design section contains **actual prose and Mermaid diagrams inline** — not links to other documents. Write the content directly in the README.
- The Mermaid diagrams in the README are **high-level summaries only** (C4 Context + C4 Container). Full diagrams with all detail go in `docs/architecture/DIAGRAMS.md`.
- **Conceptual Design stability rule**: If an existing `docs/README.md` is provided and the fundamental architecture has **not** changed (no new bounded contexts, no major flow redesign), preserve the existing Conceptual Design section prose and diagrams exactly — do not rewrite them. Only update the Architecture Documentation table.
- Design Principles must reflect what you actually observed in the codebase — do not invent generic principles.
- Keep descriptions in the Architecture Documentation table short and distinct — one phrase each.
- List every repo discovered under `Repos/` in the Repositories table — repo names only, no links (the docs repo does not contain the source repos).
- If a `docs/README.md` already exists, update only the architecture sections. Preserve any unrelated content.

### Table of Contents Requirement

**Every `.md` file produced must include a table of contents** immediately after the title/subtitle, before the first section. Use relative anchor links to every heading. Example:

```markdown
## Table of Contents

- [Section One](#section-one)
- [Section Two](#section-two)
  - [Subsection](#subsection)
```

---

## STEP 1 — Understand What You Have Been Given

Before writing anything, confirm:

* What type of system is this?
* What languages and frameworks are present?
* Is this a single repo or part of a larger system?
* What is the apparent purpose of the system?

State your understanding in 2–3 sentences before continuing.
If anything is unclear, ask one clarifying question before proceeding.

---

## STEP 2 — Pass 1: Structural Scan

Read only high-signal structural files.

**Read first (in this order):**

1. README.md and any existing architecture docs
2. Solution/project files
3. docker-compose.yml, Dockerfiles
4. Infrastructure files
5. CI/CD pipeline configuration
6. Top-level folder structure

Extract:

* Services and roles
* Infrastructure footprint
* Dependencies

---

## STEP 3 — Pass 2: Boundary Scan

Now inspect files that define what each service exposes and consumes. Do not read implementation files yet.

**Read (prioritised):**
- Controllers/, Endpoints/, Routes/
- OpenAPI / Swagger / proto / GraphQL schema files
- Contracts/, Dtos/, Events/, Messages/ folders
- Application startup and dependency injection files (Program.cs, main.py, main.go, server.js, app.module.ts, application.yml, etc.)
- API client definitions and HTTP client configurations
- Queue/topic configuration and subscription definitions

**Extract from Pass 2:**
- What each service exposes (endpoints, published events, queues written to)
- What each service consumes (APIs called, events subscribed, queues read)
- All service-to-service relationships
- Contract format and location

**For each service, record:**
- **Name** — what it is called
- **Type** — API / frontend / background worker / scheduled job / database / queue / gateway
- **Technology** — language, framework, runtime
- **Entry point** — the file or command that starts it
- **Primary responsibility** — what it does in one sentence
- **Port / URL** — if identifiable
- **Exposes** — endpoints, events, queues it publishes to
- **Consumes** — APIs, events, queues it reads from

---

## STEP 3b — Pass 3: Targeted Deep Scan

Only proceed to this pass if a boundary is ambiguous after Passes 1 and 2, or if you need to understand a specific business flow.

**Read only:**
- Handlers and command/query handlers near unclear boundaries
- Domain services where a flow is ambiguous
- Relevant tests that reveal cross-service interactions

**Do not perform a general deep scan. Read only what resolves the specific ambiguity.**

---

## STEP 4 — Map Communication Patterns


Using what you extracted in Steps 2–3, build the full communication map. For each connection, record:

- **Source service → Target service**
- **Mechanism** — REST, GraphQL, gRPC, message queue, event bus, direct DB read, shared cache, webhook
- **Contract** — endpoint path, queue/topic name, event name (if identifiable)
- **Direction** — synchronous (request/response) or asynchronous (fire and forget / event)
- **Confidence** — HIGH (directly observed) / MEDIUM (inferred) / LOW (assumed)

Label inferred connections as **[INFERRED]**. Do not omit them — surface them for human review.

---

## STEP 5 — Identify Data Models and Ownership

Find the key data entities in the system and record:
- **Entity name**
- **Owner** — which service owns/writes this entity
- **Storage** — what database or store it lives in (Postgres, MongoDB, Redis, S3, etc.)
- **Consumers** — which other services read it

Look for signals:
- ORM model files (`models/`, `entities/`, `schemas/`)
- Database migration files
- Zod/Joi/Pydantic schema definitions
- GraphQL type definitions
- OpenAPI/Swagger schema components

---

## STEP 6 — Identify External Dependencies

List all external systems.

---

## STEP 7 — Identify Unknowns and Gaps

Be honest. List anything you could not determine from the code provided:
Write to:

```
docs/architecture/unknowns.md
```

---

## 🔴 STEP 8 — System Intent & Design Principles

Infer:

* System purpose
* Why it is structured this way
* Design principles

Mark:

* [OBSERVED]
* [INFERRED]

Write to:

```
docs/architecture/system-intent.md
```

---

## 🔴 STEP 9 — Domain Model (Conceptual)

Define business concepts and relationships.

Write to:

```
docs/architecture/domain-model.md
```

---

## 🔴 STEP 10 — State Machines

Document:

* Document ingestion lifecycle
* Course lifecycle
* Lesson lifecycle

Write to:

```
docs/architecture/state-machines.md
```

---

## 🔴 STEP 11 — Failure, Retry & Idempotency

Analyse:

* Failure points
* Retry behaviour
* Idempotency

Write to:

```
docs/architecture/failure-strategy.md
```

---

## 🔴 STEP 12 — AI Architecture

Extract:

* Models
* Agent roles
* Interaction patterns

Write to:

```
docs/architecture/ai-architecture.md
```

---

## 🔴 STEP 13 — Observability & Metrics

Identify:

* Logging
* Monitoring
* Missing observability

Write to:

```
docs/architecture/observability.md
```

---

## 🔴 STEP 14 — DevOps & CI/CD

Document CI/CD and deployment only — do NOT include infrastructure provisioning here (that goes in STEP 15).

* CI/CD pipelines — build, test, deploy steps; triggers; environments targeted
* Deployment strategy — rolling, blue/green, canary, container vs App Service vs serverless
* Environments — dev, staging, prod; how they differ; promotion strategy
* Release process — branching strategy, approval gates, rollback procedure

Mark:

* [OBSERVED] — directly confirmed in CI/CD files
* [INFERRED] — reasonably inferred from patterns
* [UNKNOWN — reason] — not determinable from code provided

Write to:

```
docs/architecture/devops.md
```

---

## 🔴 STEP 15 — Infrastructure

Document cloud resources, networking, and security infrastructure — do NOT duplicate CI/CD content from STEP 14.

* Cloud resources — resource types, SKUs, scaling config, notable cost drivers
* Networking — VNet, subnets, DNS, CDN, load balancers, ingress rules
* Infrastructure as Code — tool (Bicep, Terraform, Pulumi, etc.), structure, what it provisions
* Security infrastructure — Key Vault, managed identities, RBAC, WAF, private endpoints
* Disaster recovery & backup — RPO/RTO targets, backup schedules, failover strategy

Mark:

* [OBSERVED] — directly confirmed in IaC files
* [INFERRED] — reasonably inferred from patterns
* [UNKNOWN — reason] — not determinable from code provided

Write to:

```
docs/architecture/infrastructure.md
```

---

## STEP 16 — Produce the Architecture Document

Write to:

```
docs/architecture/ARCHITECTURE.md
```

### 🔴 REQUIRED — System Summary (TOP OF FILE)

Include:

## System Summary

* **Purpose:** <short description>
* **System Type:** <e.g. event-driven microservices>
* **Key Technologies:** <.NET, RabbitMQ, OpenAI, etc.>

### Supporting Documents

* [Domain Model](./domain-model.md)
* [State Machines](./state-machines.md)
* [AI Architecture](./ai-architecture.md)
* [Failure Strategy](./failure-strategy.md)
* [Observability](./observability.md)
* [DevOps & CI/CD](./devops.md)
* [Infrastructure](./infrastructure.md)
* [Unknowns](./unknowns.md)
* [Agent Summary](./agent-summary.md)

### Diagrams

* [All Diagrams](./DIAGRAMS.md)

---

### Requirements

* Do NOT duplicate content — link instead
* Keep concise
* Ensure links are valid
* This is the **detailed implementation overview** — the user entry point is `docs/README.md`

---

Include:

* Service map
* Communication map
* Data model summary
* External dependencies
* Patterns
* Performance & cost

---

## STEP 17 — Produce Mermaid Diagrams

Write all diagrams as inline ` ```mermaid ` fenced code blocks inside a single file:

```
docs/architecture/DIAGRAMS.md
```

GitHub natively renders Mermaid inside `.md` files. Do NOT create separate `.mmd` files — they will not render on GitHub.

For each diagram include:
- Title
- 2–3 sentence explanation
- A ` ```mermaid ` fenced code block

---

## STEP 18 — Confidence Assessment

Include inside:

```
docs/architecture/ARCHITECTURE.md
```

---

## 🔴 STEP 19 — Agent Summary

Write to:

```
docs/architecture/agent-summary.md
```

Include:

* System purpose
* Core entities
* Key flows
* Constraints

---

## OUTPUT FORMAT

You must:

* **Only output FILE markers for files that are missing or have changed** based on what you find in the repos. If an existing file is still accurate, do NOT output it — omitting it means "no change needed".
* Maintain folder structure
* Ensure consistency across files

---

## IMPORTANT RULES

* Never invent — use [UNKNOWN]
* Never hide uncertainty
* Never collapse complexity
* Use exact names from code
* Prefer structured output
