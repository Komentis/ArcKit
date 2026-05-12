# ArchKit — Finish Workflow
> Follow these steps after all file changes are complete.

---

## Table of Contents

- [Steps](#steps)
- [PR Description Format](#pr-description-format)

---

## Steps

1. Run the deterministic verifier against the docs root (path from ARCH_CONFIG.md):
   ```
   python -m archkit verify docs/
   ```
   Fix every reported **error** before continuing. Warnings are advisory but should be reviewed.

2. Navigate to the docs root directory (e.g. `cd docs/`).

3. Stage all changes:
   ```
   git add .
   ```

4. Compose a commit message that summarises what was produced. Be specific — name the system, the type of work, and the key findings or files changed. Then commit:
   ```
   git commit -m "{summary}"
   ```

5. Push the branch:
   ```
   git push -u origin {branch-name}
   ```

6. Create a pull request to `main`. Use the PR description format below.

---

## PR Description Format

```
## Summary

{2–3 sentences describing what was done — e.g. "Bootstrap architecture scan of the Komentis platform across 4 repos. Produced full architecture document, diagrams, and supporting files."}

## Files changed

- {list each file created or updated}

## Key findings

- {bullet point any significant discoveries, risks, or gaps identified}

## How to review

- Start at docs/README.md
- Architecture entry point: docs/architecture/ARCHITECTURE.md
```
