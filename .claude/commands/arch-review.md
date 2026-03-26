You are an expert software architect performing a post-merge architecture reconciliation.

$ARGUMENTS

Read and follow these files before doing anything else:
- Output paths (authoritative): @.archkit/ARCH_CONFIG.md
- Governing principles: @.archkit/ARCH_COMMANDMENTS.md
- Architecture document template: @.archkit/ARCH_DOC_TEMPLATE.md
- Scan strategy (to understand what counts as architecturally significant): @.archkit/ARCH_SCAN_STRATEGY.md
- Pre-work git workflow (**follow this first, before reading any code**): @.archkit/shared/WORKFLOW_START.md

You must also have the current architecture document for this system. If it has not been provided, ask for it before proceeding.

---

Once you have read those files, reconcile the merge in this order:

1. Classify every changed file:

| File | Change type | Architectural significance |
|---|---|---|
| [file] | Added/Modified/Deleted | HIGH / MEDIUM / LOW / NONE |

Architecturally significant = new/changed service, endpoint, contract, event, schema, infrastructure, DI registration, or external dependency. Internal logic, tests, styling, and build artefacts are not significant unless they touch a boundary.

2. Determine exactly what needs updating in the architecture document:
- [ ] Service map
- [ ] Communication map
- [ ] Contract list
- [ ] Data model
- [ ] External dependencies
- [ ] Infrastructure overview
- [ ] Mermaid diagrams (list which)
- [ ] No update needed — state why

3. For each flagged item, produce the exact updated content:

```
## UPDATE: [Section Name]
Reason: [what changed and why this section needs updating]

Before:
[previous content or N/A if new]

After:
[new content]
```

4. Draft an ADR if the merge introduced a significant architectural decision. Use /arch-adr.

5. List anything ambiguous as [NEEDS REVIEW — reason].

---

Output order:
1. Change classification table
2. Update scope checklist
3. Section updates (changed sections only — do not rewrite the whole document)
4. ADR draft if applicable
5. Items needing human review

Apply all approved section updates directly to the architecture main document (path from ARCH_CONFIG.md). Do not rewrite the whole file — edit only the sections that changed. Update the Change Log entry at the bottom with today's date, what changed, and the trigger (merge/PR reference if provided). If diagrams changed, update the diagrams file (path from ARCH_CONFIG.md) as well.

If the merge introduced new services, repos, or significant structural changes, also update the documentation entry point (path from ARCH_CONFIG.md) to reflect the current state.

**Table of contents:** When editing any `.md` file, ensure it has a table of contents immediately after the title block. If one is missing, add it. If one exists, update it to reflect any heading changes introduced by this reconciliation.

---

Once all file changes are approved and applied, follow: @.archkit/shared/WORKFLOW_FINISH.md
