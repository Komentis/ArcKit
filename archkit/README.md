# archkit (Python package)

Deterministic verification layer for ArchKit-generated docs.

Zero dependencies — Python 3.10+ standard library only.

---

## Why it exists

ArchKit's anti-hallucination guarantees live in the prompt:

- every claim must be marked `[OBSERVED]`, `[INFERRED]`, `[UNKNOWN — reason]`, or `[CLARIFIED]`
- service tables must carry HIGH / MEDIUM / LOW confidence
- diagrams must be valid Mermaid
- two runs over the same code must produce equivalent fact models

A prompt alone can't enforce that. This package does — it parses the markdown into a structured fact model, validates discipline, and lints the Mermaid blocks.

---

## Usage

Run from the repo root:

```
python -m archkit verify docs/
```

Subcommands:

| Command | What it does |
|---|---|
| `verify` | Run `validate` + `lint-mermaid`. Exit 1 if any errors. |
| `validate` | Discipline checks: markers, hedging, stubs, confidence, TOC. |
| `lint-mermaid` | Lint embedded Mermaid blocks (header, brackets, arrows). |
| `parse` | Emit the fact model as JSON (use `-o file.json`). |

Examples:

```bash
# Full check before committing docs
python -m archkit verify docs/

# Diff fact models across runs
python -m archkit parse docs/ -o before.json
# … re-scan …
python -m archkit parse docs/ -o after.json
diff before.json after.json
```

---

## Tests

```bash
python -m unittest discover -s archkit/tests -v
```

22 tests, no external dependencies.

---

## What gets validated

| Check | Severity | Source rule |
|---|---|---|
| Unresolved stub placeholders (`[TBD]`, `[FILL …]`, `???`) | error | ARCH_COMMANDMENTS.md — never ship unresolved stubs |
| `[UNKNOWN]` without a reason | error | scan prompt — gaps must be `[UNKNOWN — reason]` |
| Hedge language without a marker (`likely`, `appears to`, …) | warning | scan prompt — every inference must be `[INFERRED]` |
| Missing `## Table of Contents` | warning | scan prompt — every `.md` produced must have a TOC |
| Service-like table without `Confidence` column | warning | scan prompt — service map must carry confidence |
| Confidence value not in `{HIGH, MEDIUM, LOW}` | error | scan prompt |
| Unknown Mermaid diagram type | mermaid error | diagrams guide — must be a valid C4/sequence/flowchart/etc. |
| Unbalanced brackets or quotes inside a Mermaid block | mermaid error | renderer requirement |
| Arrow with missing left- or right-hand side | mermaid error | renderer requirement |
| Empty Mermaid block | mermaid error | scan prompt — no empty diagrams |

---

## What gets parsed

The parser recognises markdown tables by their headers and maps them into typed records:

| Markdown table headers contain | Parsed as |
|---|---|
| `Name` + (`Type` / `Technology` / `Responsibility` / `Role`) | `Service` |
| `Source` + `Target` (+ optional `Mechanism`, `Direction`, `Confidence`) | `Connection` |
| `Entity` + (`Owner` / `Storage` / `Consumers`) | `DataEntity` |
| Lines under a `## Unknowns` heading; any `[UNKNOWN — reason]` marker | `Unknown` |

The resulting `FactModel` is JSON-serialisable via `to_dict()`.

---

## Limits

- The Mermaid linter is *syntactic*, not semantic — it won't detect, for example, that a node ID appears in the diagram but not in the service map. That kind of cross-check is a possible v0.2 feature.
- The parser does not extract bounded-context information yet — only services, connections, entities, and unknowns.
- Validation rules are heuristic on prose. Hedging detection in particular can false-positive on legitimate writing; the warning severity reflects that.
