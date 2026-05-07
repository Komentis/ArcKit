# [Organisation Name] — Architecture Commandments
> Extends: ARCH_COMMANDMENTS.md (Base) v1.0
> Organisation: [Your organisation name]
> Created: [Date]
> Last updated: [Date]
> Owner: [Name / Role]

These commandments extend the base ArchKit commandments for [Organisation Name].
They define how architecture is practised specifically within this organisation,
its technology choices, team structures, and product context.

The base commandments apply in full. Where this document adds rules, they layer on top.
Where this document overrides a base commandment, the override is explicitly justified below.

---

## Table of Contents

- [Section 1 — Our System Context](#section-1--our-system-context)
- [Section 2 — Our Naming Conventions](#section-2--our-naming-conventions)
- [Section 3 — Our Technology Decisions](#section-3--our-technology-decisions)
- [Section 4 — Our Data Rules](#section-4--our-data-rules)
- [Section 5 — Our Contract Rules](#section-5--our-contract-rules)
- [Section 6 — Our Team Structure](#section-6--our-team-structure)
- [Section 7 — Our Commandment Extensions](#section-7--our-commandment-extensions)
- [Section 8 — Our Base Commandment Overrides](#section-8--our-base-commandment-overrides)
- [Section 9 — What AI Agents Must Always Do in Our Context](#section-9--what-ai-agents-must-always-do-in-our-context)
- [Version History](#version-history)

---

## Section 1 — Our System Context

> Describe your organisation's system landscape so any AI agent operating under these commandments understands the context.

**What we build:**
[One paragraph describing the product(s), domain, and purpose]

**Our system type:**
[ ] Microservices
[ ] Modular monolith
[ ] Monolith
[ ] Data pipeline / platform
[ ] Mix — describe: [_______]

**Our primary languages and frameworks:**
- Backend: [e.g. Node.js / .NET / Python / Go]
- Frontend: [e.g. React / Next.js / Vue]
- Data: [e.g. PostgreSQL / MongoDB / Snowflake]
- Infrastructure: [e.g. Azure / AWS / GCP]

**Our repo structure:**
[ ] Monorepo (all services in one repo)
[ ] Polyrepo (one repo per service)
[ ] Mixed — describe: [_______]

**Primary repo location:**
[e.g. Azure DevOps — organisation name / GitHub — org name]

---

## Section 2 — Our Naming Conventions

> AI agents must use these conventions when generating architecture docs and diagrams.

**Service naming:**
[e.g. kebab-case, prefixed by domain: "identity-auth-api", "orders-processing-worker"]

**Event / message naming:**
[e.g. PascalCase noun-verb: "OrderCreated", "UserVerified"]

**Database naming:**
[e.g. one DB per service, named after service: "identity_db", "orders_db"]

**API endpoint conventions:**
[e.g. REST, versioned at /api/v{n}, noun-based paths]

**Diagram and doc naming:**
[e.g. ARCHITECTURE_{SYSTEM_NAME}.md, updated in /docs/]

---

## Section 3 — Our Technology Decisions

> Record standing technology decisions so AI agents do not suggest alternatives that conflict with them.

| Category | Decision | Reason | Since |
|---|---|---|---|
| API style | [REST / GraphQL / gRPC] | [reason] | [date] |
| Async messaging | [e.g. Azure Service Bus / RabbitMQ / Kafka / SQS] | [reason] | [date] |
| Auth | [e.g. Azure AD / Auth0 / Cognito] | [reason] | [date] |
| Primary database | [e.g. PostgreSQL / CosmosDB / MongoDB] | [reason] | [date] |
| Cache | [e.g. Redis / Memcached / None] | [reason] | [date] |
| Observability | [e.g. Application Insights / Datadog / Grafana] | [reason] | [date] |
| Deployment | [e.g. AKS / ECS / App Service / Lambda] | [reason] | [date] |
| IaC | [e.g. Terraform / Bicep / Pulumi / CDK] | [reason] | [date] |

---

## Section 4 — Our Data Rules

> Extend Commandment V (Data Ownership) with our specific rules.

**Database per service:**
[ ] Enforced — each service has its own database/schema, no shared DB access
[ ] Partial — [describe exceptions]
[ ] Not enforced — [describe shared DB policy]

**Data sharing pattern:**
[ ] Events only — services share data via events, never direct DB reads
[ ] API calls — services request data from the owning service's API
[ ] Read replicas allowed — [describe policy]
[ ] Mixed — describe: [_______]

**PII / sensitive data rules:**
[Describe any special handling rules for personal data, payment data, health data, etc.]

**Data retention rules:**
[Any architectural decisions driven by data retention or compliance requirements]

---

## Section 5 — Our Contract Rules

> Extend Commandment VI (Contracts) with our specific standards.

**API contract format:**
[ ] OpenAPI / Swagger (required for all REST APIs)
[ ] GraphQL Schema (required for all GraphQL APIs)
[ ] Proto files (required for all gRPC services)
[ ] Informal / undocumented — [describe plan to change]

**Contract change policy:**
[ ] Breaking changes require a new API version
[ ] Breaking changes require a deprecation notice of [n] weeks
[ ] No formal policy yet — [describe]

**Contract location:**
[Where are contract files stored? e.g. /contracts folder in each repo, shared contracts repo]

**Event schema registry:**
[ ] Yes — [where / tool used]
[ ] No — schemas are in code only

---

## Section 6 — Our Team Structure

> Helps AI agents understand ownership boundaries when generating architecture or routing specs.

| Team | Owns | Repos |
|---|---|---|
| [Team name] | [Domain / services they own] | [repo names] |

**Decision-making:**
[Who approves architecture decisions? e.g. Tech Lead, Architecture Review Board, CTO]

**Architecture review process:**
[ ] Formal review required for all cross-service changes
[ ] Informal review via PR
[ ] No formal process — describe: [_______]

---

## Section 7 — Our Commandment Extensions

> Add organisation-specific commandments here. These extend the base 12.

### XIII. [Commandment Name]

**[Rule statement in bold imperative form]**

[Explanation. Why does this rule exist for your organisation? What problem does it solve?]

---

### XIV. [Commandment Name]

**[Rule statement in bold imperative form]**

[Explanation.]

---

*(Add as many as needed. Number them continuing from XII.)*

---

## Section 8 — Our Base Commandment Overrides

> If any base commandment does not apply as-is, document the override here.
> Overrides must have a justification. Undocumented overrides are not valid.

| Base Commandment | Override | Justification | Approved By |
|---|---|---|---|
| [e.g. Commandment X — One Source of Truth] | [What we do differently] | [Why] | [Name / date] |

---

## Section 9 — What AI Agents Must Always Do in Our Context

> Specific instructions for any AI agent operating within our architecture system.

- Always check [specific file/folder] first when scanning for service boundaries
- Always treat [technology/pattern] as the standard — do not suggest alternatives
- Always flag changes to [specific contracts/services] for human review
- Never generate designs that [specific constraint — e.g. "introduce a new database technology"]
- When uncertain about data ownership, default to [rule]

---

## Version History

| Version | Date | Changes | Author |
|---|---|---|---|
| 1.0 | [Date] | Initial org commandments | [Name] |

---

*This document is owned by [Name / Role]. Changes require approval from [Name / Role or process].*
