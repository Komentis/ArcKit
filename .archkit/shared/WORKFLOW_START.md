# ArchKit — Start Workflow
> Follow these steps before reading any code or making any file changes.

---

## Table of Contents

- [Steps](#steps)
- [Branch Naming Suggestions](#branch-naming-suggestions)

---

## Steps

1. Read **ARCH_CONFIG.md** to determine the docs root path.

2. Navigate to the docs root directory (e.g. `cd docs/`).

3. Ensure you are on `main` and up to date:
   ```
   git checkout main
   git pull
   ```

4. Ask the user:
   > "What should the feature branch be called?"

   Suggest a sensible default based on the task (see naming suggestions below). Wait for confirmation before proceeding.

5. Create and switch to the new branch:
   ```
   git checkout -b {branch-name}
   ```

6. Confirm the branch is active, then proceed with the task.

**Do not read any code or write any files until these steps are complete.**

---

## Branch Naming Suggestions

| Task | Suggested branch name |
|---|---|
| Full architecture scan | `arch/scan-DD-MM-YYYY_HH-MM-SS` |
| Post-merge review | `arch/review-{pr-or-feature-name}` |
| Feature design | `arch/feature-{feature-name}` |
| ADR | `arch/adr-{decision-title}` |

> Note: Git branch names cannot contain `/` within segments used as separators, `:`, or spaces. Use `-` in place of `:` for time. The datetime is formatted as `DD-MM-YYYY_HH-MM-SS` (e.g. `arch/scan-26-03-2026_14-30-00`).
