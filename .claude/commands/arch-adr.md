You are an expert software architect. Create a formal Architecture Decision Record for the decision described below.

$ARGUMENTS

Read these files first:
- Output paths (authoritative): @.archkit/ARCH_CONFIG.md
- Governing principles: @.archkit/ARCH_COMMANDMENTS.md
- Pre-work git workflow (**follow this first, before reading any code**): @.archkit/shared/WORKFLOW_START.md

---

Produce the ADR in this exact format:

```markdown
# ADR-[NUMBER] — [Decision Title]

**Date:** [DATE]
**Status:** [Proposed / Accepted / Deprecated / Superseded by ADR-X]
**Deciders:** [Who was involved]

---

## Context
[What situation or problem made this decision necessary? What constraints existed?]

## Decision
[What was decided. Active voice: "We will use X" not "X was considered".]

## Rationale
[Why was this right given the context? What made it better than alternatives?]

## Consequences

**Positive:**
- [benefit]

**Negative / Trade-offs:**
- [trade-off]

**Neutral:**
- [things that change but are neither good nor bad]

## Alternatives Considered

| Option | Why rejected |
|---|---|
| [option] | [reason] |

## Affected Areas
- **Services:** [which services]
- **Contracts:** [which contracts or schemas]
- **Teams:** [who needs to know]

## Review Date
[When to revisit, or blank if not needed]
```

Be specific. Record what was NOT chosen and why — this is the most valuable part.
If this supersedes an earlier ADR, reference it.
Include honest negative trade-offs.

Save the ADR to the decisions path defined in ARCH_CONFIG.md (e.g. `docs/decisions/ADR-[NUMBER]-[kebab-case-title].md`). If the folder does not exist, create it. Number sequentially from existing ADRs in that folder, starting at ADR-001 if none exist.

Once the ADR is saved, follow: @.archkit/shared/WORKFLOW_FINISH.md
