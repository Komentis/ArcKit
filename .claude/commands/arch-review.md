You are an expert software architect performing an ArchKit architecture review.

$ARGUMENTS

Read and follow these files before doing anything else:
- Output paths (authoritative): @.archkit/ARCH_CONFIG.md
- Governing principles: @.archkit/ARCH_COMMANDMENTS.md
- Scan strategy (what counts as architecturally significant): @.archkit/ARCH_SCAN_STRATEGY.md
- Pre-work git workflow (**follow this first, before reading any code**): @.archkit/shared/WORKFLOW_START.md

---

## Mode Detection

Determine which mode to run based on what was provided in `$ARGUMENTS`:

- **If a PR number, branch name, or merge reference was provided** → run [Post-Merge Mode](#post-merge-mode)
- **If nothing was provided, or the argument is "drift"** → run [Drift Check Mode](#drift-check-mode)

---

## Post-Merge Mode

_Use when: a specific PR or merge has just landed and you need to reconcile the docs._

Read the current architecture documents (paths from ARCH_CONFIG.md) before doing anything else.

Then reconcile the merge in this order:

1. Classify every changed file:

| File | Change type | Architectural significance |
|---|---|---|
| [file] | Added/Modified/Deleted | HIGH / MEDIUM / LOW / NONE |

Architecturally significant = new/changed service, endpoint, contract, event, schema, infrastructure, DI registration, or external dependency. Internal logic, tests, styling, and build artefacts are not significant unless they touch a boundary.

2. Determine exactly what needs updating:
- [ ] Service map
- [ ] Communication map
- [ ] Contract list
- [ ] Data model
- [ ] External dependencies
- [ ] Infrastructure / DevOps
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

Apply all updates directly to the relevant docs files (paths from ARCH_CONFIG.md). Edit only changed sections — do not rewrite whole files. Update the `> Last updated:` header in any file you touch.

---

## Drift Check Mode

_Use when: you want to check whether the architecture docs are still accurate without a specific merge to review. Runs a targeted scan across all repos since the last scan date and only updates what has drifted._

### Step 1 — Read existing docs

Read these files first (paths from ARCH_CONFIG.md):
- Architecture main document
- Agent summary
- DevOps & infrastructure
- Unknowns

Extract the **last scan date** from the `> Last updated:` header in the architecture main document.

### Step 2 — Check what changed since the last scan

For each repo discovered under `Repos/` (per ARCH_CONFIG.md):

```
git -C Repos/[RepoName] log --oneline --since="[last scan date]" --name-only
```

Build a list of files changed since the last scan date. Ignore files that are not architecturally significant (tests, styling, build artefacts, internal logic).

If nothing changed in any repo since the last scan date, state that and stop — no updates needed.

### Step 3 — Targeted scan of changed areas only

For each architecturally significant file that changed, apply the appropriate pass from ARCH_SCAN_STRATEGY.md:
- Boundary files (controllers, contracts, events, startup) → Pass 2
- Implementation files that touch a boundary → Pass 3 (targeted only)

Do not re-read files that have not changed.

### Step 4 — Compare against existing docs

For each area where changes were observed, compare the new findings against what is currently documented.

Produce a diff summary:

| Doc section | Current state | Observed state | Action |
|---|---|---|---|
| [section] | [what docs say] | [what code shows] | Update / No change / Needs review |

If no differences are found in a section, mark it **No change** and do not touch the file.

### Step 5 — Apply only the changes that differ

For each section marked **Update**:

```
## UPDATE: [File] — [Section Name]
Reason: [what drifted]

Before:
[current doc content]

After:
[corrected content]
```

Apply changes directly to the relevant docs files. Edit only the sections that drifted — do not rewrite whole files. Update the `> Last updated:` header in any file you touch.

### Step 6 — Update unknowns

If the scan resolved any previously unknown items, move them from the open table to the Confirmed table in `unknowns.md`.

If the scan revealed new unknowns, add them to the open table.

---

## Output order (both modes)

1. Mode identified + last scan date (drift mode) or PR/merge reference (post-merge mode)
2. Change classification table (post-merge) or diff summary table (drift)
3. Section updates — changed sections only
4. ADR draft if applicable
5. Items needing human review / new unknowns

---

## Rules

- Never rewrite a whole file when only a section changed.
- Never update a section where the observed facts match what is already documented.
- Mark inferred content `[INFERRED]`. Mark gaps `[UNKNOWN — reason]`.
- Every `.md` file you touch must have a table of contents. If one is missing, add it. If headings changed, update it.
- Always update the `> Last updated:` date in any file you modify.

---

Once all changes are applied, follow: @.archkit/shared/WORKFLOW_FINISH.md
