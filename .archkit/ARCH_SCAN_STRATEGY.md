# ArchKit — Scan Strategy
> Reference document for all scan behaviour in ArchKit and the Architecture Bot.
> This document governs how repos are read. Every scanning agent operates under these rules.

---

## Table of Contents

- [Core Principle](#core-principle)
- [Scan Modes](#scan-modes)
  - [Bootstrap Scan](#bootstrap-scan)
  - [Incremental Scan](#incremental-scan)
  - [Feature Scan](#feature-scan)
- [The Three-Pass Process](#the-three-pass-process)
  - [Pass 1 — Structural Scan](#pass-1--structural-scan)
  - [Pass 2 — Boundary Scan](#pass-2--boundary-scan)
  - [Pass 3 — Targeted Deep Scan](#pass-3--targeted-deep-scan)
- [File Priority Ranking](#file-priority-ranking)
- [Convention-Aware Scanning](#convention-aware-scanning)
- [Incremental Update Logic](#incremental-update-logic)
- [Impact-First Feature Analysis](#impact-first-feature-analysis)
- [Fact Extraction Before Documentation](#fact-extraction-before-documentation)
- [Scan Output Specification](#scan-output-specification)
- [Design Constraints](#design-constraints)
- [Relationship to Other ArchKit Documents](#relationship-to-other-archkit-documents)

---

## Core Principle

> Read files that define boundaries, contracts, composition, and deployment first.
> Read implementation only when a boundary, change, or feature requires clarification.

Scanning is not crawling. The bot extracts architectural signal efficiently — it does not read every file. Full-file scanning is a failure mode, not a feature.

---

## Scan Modes

### Bootstrap Scan
**When:** Initial generation of the platform architecture reference. Run once (or on explicit full reset).

**Scope:** Structural scan + boundary scan across all repositories. Targeted deep scan only where structure is unclear.

**Goal:** Understand the entire organisation — repos, services, interfaces, dependencies. Produce the initial architecture model and docs.

---

### Incremental Scan
**When:** Any merge to main in any repo.

**Scope:** Changed files and directly affected architectural artefacts only. No full rebuild unless explicitly requested.

**Goal:** Keep architecture artefacts current without re-scanning the entire platform.

---

### Feature Scan
**When:** A new feature request is received.

**Scope:** Existing architecture model first. Likely impacted repos second. Deep scan only on relevant files.

**Goal:** Design the feature against the real system without redundant full discovery.

---

## The Three-Pass Process

Every scan — regardless of mode — follows the same progression. **Do not skip to a later pass. Do not run Pass 3 unless Passes 1 and 2 are insufficient.**

```
Pass 1: Structural Scan   →   low-cost, high-signal shape of the system
Pass 2: Boundary Scan     →   what services expose and consume
Pass 3: Targeted Deep     →   implementation detail, only when required
```

---

### Pass 1 — Structural Scan

**What to read:**

| File type | Examples |
|---|---|
| Documentation | README.md, architecture docs, ADRs |
| Solution/project files | .sln, .csproj, package.json, go.mod, pyproject.toml, Gemfile |
| Composition | docker-compose.yml, Dockerfile |
| Infrastructure | Bicep, Terraform, CDK, Pulumi |
| CI/CD | Azure Pipelines YAML, GitHub Actions, Jenkinsfile |
| Folder structure | Top-level tree (1–2 levels deep) |

**What to extract:**
- Repositories and projects present
- Likely services and applications
- Infrastructure footprint
- Package and project dependencies
- High-level role of each repo

**Stop condition:** If you can name every service and its role, Pass 1 is complete. Move to Pass 2 only if service boundaries are still unclear.

---

### Pass 2 — Boundary Scan

**What to read:**

| File type | Examples |
|---|---|
| API surfaces | Controllers/, Endpoints/, Routes/, Program.cs (route registration) |
| Contracts | OpenAPI/Swagger files, proto files, GraphQL schema |
| DTOs and events | Contracts/, Dtos/, Events/, Messages/, Payloads/ |
| Startup/DI | Startup.cs, Program.cs, DI registration files, app.module.ts |
| Clients | API client definitions, HTTP client configurations |
| Integration config | Queue/topic configuration, subscription definitions |
| Interfaces | Repository interfaces, service interfaces |

**What to extract:**
- What each service exposes (endpoints, events published, queues written to)
- What each service consumes (APIs called, events subscribed, queues read from)
- Repo-to-repo and service-to-service relationships
- Shared contracts and integration surfaces
- Contract format and location

**Stop condition:** If all service connections are mapped and contracts are identified, Pass 2 is complete. Move to Pass 3 only when needed.

---

### Pass 3 — Targeted Deep Scan

**Only run when:**
- A specific boundary is ambiguous after Passes 1 and 2
- A feature requires understanding a specific business flow
- An incremental update touches logic that changes architectural behaviour

**What to read:**

| File type | Examples |
|---|---|
| Handlers | Command handlers, query handlers, event handlers |
| Business logic | Domain services, application services, use case classes |
| Orchestration | Sagas, workflows, coordinators |
| Tests | Integration tests that reveal cross-service flows |
| Changed files | Only files in the git diff that affect boundaries |

**What to extract:**
- Business flow clarification
- Resolution of boundary ambiguity
- Behaviour context needed for feature design or reconciliation

---

## File Priority Ranking

Before reading any file, rank it. Read highest-priority files first. Stop reading when you have enough signal.

### High Signal — Always Prioritise
- README.md, ARCHITECTURE.md, ADRs
- Program.cs / startup / main entry point
- Dependency injection registration
- Controllers/, Endpoints/, Routes/
- Contracts/, Dtos/, Events/, Messages/
- Infrastructure/, deploy/, infra/
- Bicep, Terraform, CloudFormation, Pulumi files
- OpenAPI / Swagger / proto / GraphQL schema files
- Shared contract library projects
- docker-compose.yml, Dockerfile, pipeline YAML

### Medium Signal — Read When Relevant
- Domain services, application services
- Repository implementations
- Coordinators, orchestrators, sagas
- Tests that reveal cross-service interactions

### Low Signal — Ignore Unless Explicitly Required
- Utility helpers, extension methods
- Styling files (CSS, SCSS, LESS)
- Generated code (*.g.cs, *.generated.ts)
- Build artefacts (bin/, obj/, dist/, .next/)
- Snapshots and lock files
- node_modules/, vendor/, packages/

---

## Convention-Aware Scanning

The bot uses known conventions to guide scanning instead of rediscovering structure on every run. Org-specific conventions should be encoded in the [org commandments document](ARCH_COMMANDMENTS_TEMPLATE.md) and applied automatically.

**Built-in conventions:**

| Stack | Boundary signals |
|---|---|
| .NET API | Controllers/, Program.cs, DI registration, shared contract .csproj |
| Node.js / Express | routes/, app.js, route definitions, middleware registration |
| NestJS | modules, controllers, providers, decorators |
| Angular | app.routes.ts, feature modules, service clients, store/ |
| React / Next.js | pages/, app/router, API route files |
| Python / FastAPI | routers/, main.py, dependency injection, Pydantic models |
| Infrastructure | infra/, deploy/, Bicep, Terraform, Docker, pipeline YAML |

---

## Incremental Update Logic

For merge-to-main updates:

```
1. Get git diff (changed file list + diffs)
2. Classify each changed file by type (contract / service / infra / test / internal)
3. Map files to repos, services, contracts, and infrastructure artefacts
4. Determine whether each change has architectural significance
5. Update only the impacted portions of the model and artefacts
```

**Change type → update scope:**

| Changed file type | Architecture update needed |
|---|---|
| OpenAPI / Swagger spec | API docs, contract map, Container diagram |
| Shared DTO / contract class | Contracts map, impacted repo docs |
| Infrastructure (Bicep/Terraform) | Infra overview, deployment diagram |
| docker-compose.yml | Container diagram, service list |
| New Controller / Route | Service API surface, boundary docs |
| New service project added | Service map, Container diagram |
| Internal helper / utility | None (unless it changes a boundary) |
| Test file only | None (unless it reveals a new cross-service flow) |

---

## Impact-First Feature Analysis

When a feature request arrives:

```
1. Read the existing architecture model and docs (do not re-scan repos)
2. Identify likely impacted repos and services from the model
3. Rank affected areas by relevance to the feature
4. Inspect only the top candidate files and boundaries
5. Deep-scan implementation only when required for design clarity
```

Feature design starts from the maintained architecture reference. If the reference is current (Milestone 2 maintained), full re-scanning is never needed for feature analysis.

---

## Fact Extraction Before Documentation

The bot must never generate Markdown or Mermaid directly from raw file content. The required pipeline is:

```
Scan files  →  Extract facts into structured model  →  Generate Markdown from model  →  Generate Mermaid from model
```

**Why this matters:**
- Reduces hallucination (the model contains only confirmed facts)
- Enables diffing between scan runs
- Allows downstream automation to consume the model independently of the docs
- Makes confidence ratings computable per fact, not per document

---

## Scan Output Specification

Every scan run produces:

| Output | Description |
|---|---|
| Normalised architecture model | Structured JSON/YAML fact set: services, connections, contracts, entities |
| Scan metadata | Mode, timestamp, files read, passes executed, repos scanned |
| Impacted artefacts list | Which docs/diagrams need to be updated |
| Confidence flags | Per-relationship and per-service confidence ratings |
| Ambiguity list | Things that could not be confirmed — surfaced for human review |

The bot must explicitly label:
- **[INFERRED]** — relationship inferred from patterns, not directly observed
- **[UNCLEAR]** — boundary not determinable from available files
- **[REVIEW RECOMMENDED]** — significant change or ambiguity warrants human check

---

## Design Constraints

The scan strategy must:

- Prefer deterministic extraction over inference
- Avoid reading every file by default — volume is not a quality signal
- Support idempotent runs — same inputs always produce the same outputs
- Remain extensible for new languages, frameworks, and conventions
- Scale without degradation as the number of repos grows

---

## Relationship to Other ArchKit Documents

| Document | How scan strategy applies |
|---|---|
| `ARCHKIT_SCAN_PROMPT.md` | Implements this strategy in the manual Claude scan flow |
| `ARCH_COMMANDMENTS.md` | Commandment XIII governs scan behaviour at the principle level |
| `ARCH_DOC_TEMPLATE.md` | Is populated from the structured model produced by the scan |
| `ARCH_DIAGRAMS_GUIDE.md` | Diagrams are generated from the model, not directly from code |
| Org commandments | Encode org-specific conventions that guide pass 1 and pass 2 |
