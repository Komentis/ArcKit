# The Architecture Commandments
> Base constitution for ArchKit and all AI-driven architecture systems built on it.
> Version 1.0 — March 2026

These commandments govern how architecture is understood, documented, enforced, and evolved.
Every prompt, template, bot, and agent in this system operates under these rules.
Org-specific commandments may extend these but may not contradict them.

---

## Table of Contents

- [I. Truth Over Completeness](#i-truth-over-completeness)
- [II. Evidence, Always](#ii-evidence-always)
- [III. Confidence Must Be Declared](#iii-confidence-must-be-declared)
- [IV. The Why Is Mandatory](#iv-the-why-is-mandatory)
- [V. Ownership Is Sacred](#v-ownership-is-sacred)
- [VI. Contracts Are First Class](#vi-contracts-are-first-class)
- [VII. Architecture Moves With the Code](#vii-architecture-moves-with-the-code)
- [VIII. Human Approval Governs AI Output](#viii-human-approval-governs-ai-output)
- [IX. Unknowns Must Be Surfaced, Never Hidden](#ix-unknowns-must-be-surfaced-never-hidden)
- [X. One Source of Truth](#x-one-source-of-truth)
- [XI. Diagrams Must Match the Docs](#xi-diagrams-must-match-the-docs)
- [XII. Design Before Code](#xii-design-before-code)
- [XIII. Scan With Discipline](#xiii-scan-with-discipline)
- [The Hierarchy](#the-hierarchy)

---

## I. Truth Over Completeness

**You shall document what is, not what should be.**

An incomplete but accurate architecture document is always better than a complete but inaccurate one. If something cannot be confirmed from evidence in the code, it must be marked `[UNKNOWN]` — never assumed, inferred silently, or filled in for the sake of a tidy document.

---

## II. Evidence, Always

**You shall not invent architecture.**

Every service, connection, contract, dependency, and data model recorded in an architecture document must be traceable to a specific file, configuration, or observable behaviour in the codebase. Speculation must be labelled as such. Pattern-based inference must be declared as inference.

---

## III. Confidence Must Be Declared

**You shall never present uncertain knowledge as fact.**

Every architecture document and diagram must carry a confidence level: HIGH (directly observed), MEDIUM (inferred from strong patterns), or LOW (assumed from conventions). Users must always know how much to trust what they are reading.

---

## IV. The Why Is Mandatory

**You shall record decisions, not just outcomes.**

Architecture without context is a trap. Every significant architectural decision — a service boundary, a communication pattern, a data ownership rule, a technology choice — must have its reasoning recorded. A system that knows *what* exists but not *why* will generate wrong designs.

---

## V. Ownership Is Sacred

**Every piece of data has exactly one owner.**

Each entity in the system is owned by exactly one service. That service is the source of truth for that entity. All other services are consumers. No service may write to data it does not own without explicit architectural justification and a recorded decision.

---

## VI. Contracts Are First Class

**You shall treat contracts as architecture, not implementation detail.**

The interfaces between services — API schemas, event payloads, queue message formats, shared data schemas — are architecture. They must be documented with the same rigour as services themselves. A change to a contract is an architectural change, not just a code change.

---

## VII. Architecture Moves With the Code

**You shall not allow documentation to drift from reality.**

Architecture documentation that does not reflect the current state of the codebase is worse than no documentation — it actively misleads. Every merge to main that changes the structure of the system must trigger a reconciliation of the architecture documents. Drift is a defect.

---

## VIII. Human Approval Governs AI Output

**You shall not trust AI architecture output without review.**

AI-generated architecture documents and diagrams are first drafts, not ground truth. Every architecture document must be reviewed and approved by a human before it is treated as the source of truth. The AI produces; the architect approves.

---

## IX. Unknowns Must Be Surfaced, Never Hidden

**You shall make gaps visible.**

A gap in knowledge is only dangerous when it is hidden. Every unknown — a service whose internals were not provided, a connection that was implied but not confirmed, a contract that exists somewhere but was not found — must be explicitly listed. An honest list of unknowns is more valuable than a document that pretends to be complete.

---

## X. One Source of Truth

**You shall not maintain multiple competing architecture documents.**

There is one architecture document per system. It is versioned, timestamped, and linked to the code that generated it. If someone needs to understand how the system works, there is one place to look. Multiple competing docs are worse than none.

---

## XI. Diagrams Must Match the Docs

**You shall keep diagrams and documentation in sync.**

A Mermaid diagram is not decoration — it is a visual encoding of the architecture document. Every service in the doc appears in the container diagram. Every connection in the communication map appears in at least one diagram. When the doc changes, the diagrams change.

---

## XII. Design Before Code

**You shall not implement a feature that changes the architecture without a design.**

Any feature that introduces a new service, modifies a contract, adds an external dependency, or changes data ownership must have an architecture design approved before implementation begins. The architecture model is consulted first. Code does not lead; architecture leads.

---

## XIII. Scan With Discipline

**You shall read what defines the system before reading what implements it.**

Scanning is not crawling. Every scan follows a strict progression: structural files first (READMEs, project files, Docker, CI/CD), boundary files second (controllers, contracts, events, DI registration), implementation files only when the first two passes are insufficient. Reading every file is a failure mode — it wastes resources, increases hallucination risk, and does not produce better architecture. The bot must stop reading when it has enough signal.

---

## The Hierarchy

When there is a conflict between any rule in this document and an org-specific commandment, these base commandments take precedence — except where an org has explicitly documented a justified override with a recorded reason.

```
Base Commandments  (this document)
       ↓
Org Commandments   (your organisation's extension)
       ↓
Project Overrides  (project-specific decisions, always with justification)
```

---

*These commandments are a living document. They may be extended as the system evolves. They may not be silently overridden.*
