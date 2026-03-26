You are an expert software architect performing an ArchKit feature design.

$ARGUMENTS

Read and follow these files before doing anything else:
- Output paths (authoritative): @.archkit/ARCH_CONFIG.md
- Governing principles: @.archkit/ARCH_COMMANDMENTS.md
- Architecture document template (for reference): @.archkit/ARCH_DOC_TEMPLATE.md
- Diagram specifications: @.archkit/ARCH_DIAGRAMS_GUIDE.md
- Pre-work git workflow (**follow this first, before reading any code**): @.archkit/shared/WORKFLOW_START.md

You must also have the current architecture document for this system. If it has not been provided, ask for it before proceeding.

---

Once you have read those files, design the feature in this order:

1. Confirm your understanding of the current system from the architecture doc in 2–3 sentences.

2. Impact analysis — identify affected services, contracts, data entities, new dependencies, and deployment changes. Rank by HIGH / MEDIUM / LOW impact.

3. Cross-feature conflict check — identify conflicts with existing ADRs or other in-flight features. Flag as [CONFLICT — description].

4. Produce the feature architecture design:

```
# Feature Architecture Design — [FEATURE NAME]
> Date: [DATE] | Status: DRAFT — awaiting approval

## Feature Summary
## Design Approach
## Services Involved          (table: Service | Role | Change Type)
## Contract Changes           (table: Contract | Service | Change | Breaking?)
## Data Changes               (table: Entity | Owner | Change | Consumer impact)
## New Infrastructure
## Sequence: Happy Path       (Mermaid sequence diagram)
## Risks & Constraints
## Rejected Approaches
## Open Questions
```

5. Generate SpecKit inputs per affected repo:

```
## Repo: [name]
What changes:
Contracts to implement:
Acceptance criteria:
Dependencies:
Files likely affected:
```

6. If a significant architectural decision was made, draft an ADR using /arch-adr.

---

Output order:
1. Impact analysis
2. Feature architecture design
3. SpecKit inputs per repo
4. ADR draft if applicable
5. Open questions requiring human decision

Save the output as a single `.md` file to the features path defined in ARCH_CONFIG.md (e.g. `docs/features/[feature-name].md`). Use kebab-case for the filename. If the folder does not exist, create it.

The feature design file must include a table of contents immediately after the title, with anchor links to every section heading.

Never generate SpecKit inputs before the architecture design is complete.
Flag every breaking contract change explicitly and require human approval before proceeding.

---

Once the feature design file is saved and all open questions are listed, follow: @.archkit/shared/WORKFLOW_FINISH.md
