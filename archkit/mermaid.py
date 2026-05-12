"""Lint Mermaid blocks embedded in markdown.

This is a *syntactic* linter, not a full Mermaid parser. It catches the
common ways AI-generated diagrams break:

* unknown diagram type on the first non-empty line of the block
* unbalanced square / round / curly brackets or quotes
* arrow tokens with no left- or right-hand side
* empty blocks
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MermaidIssue:
    file: str
    block_index: int
    line: int | None
    message: str

    def format(self) -> str:
        location = f"{self.file}#mermaid[{self.block_index}]"
        if self.line is not None:
            location += f":{self.line}"
        return f"[MERMAID] {location} — {self.message}"


_VALID_DIAGRAM_HEADS = {
    "graph",
    "flowchart",
    "sequencediagram",
    "classdiagram",
    "statediagram",
    "statediagram-v2",
    "erdiagram",
    "journey",
    "gantt",
    "pie",
    "requirementdiagram",
    "gitgraph",
    "mindmap",
    "timeline",
    "c4context",
    "c4container",
    "c4component",
    "c4dynamic",
    "c4deployment",
    "quadrantchart",
    "sankey-beta",
    "xychart-beta",
    "block-beta",
    "architecture-beta",
}

_BLOCK_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
_ARROW_TOKENS = re.compile(r"(-->|---|-\.->|\.->|==>|--x|-->\||---\|)")


def _diagram_head(block: str) -> str | None:
    for raw in block.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("%%"):
            continue
        head = stripped.split()[0].lower().rstrip(":")
        return head
    return None


def _check_brackets(block: str) -> list[str]:
    """Return human-readable bracket-balance complaints."""
    errors: list[str] = []
    counts = {"[": 0, "(": 0, "{": 0}
    pairs = {"]": "[", ")": "(", "}": "{"}
    for ch in block:
        if ch in counts:
            counts[ch] += 1
        elif ch in pairs:
            counts[pairs[ch]] -= 1
            if counts[pairs[ch]] < 0:
                errors.append(f"Unbalanced '{ch}' — closing bracket without an opener")
                counts[pairs[ch]] = 0
    if counts["["] > 0:
        errors.append(f"{counts['[']} unclosed '['")
    if counts["("] > 0:
        errors.append(f"{counts['(']} unclosed '('")
    if counts["{"] > 0:
        errors.append(f"{counts['{']} unclosed '{{'")
    if block.count('"') % 2:
        errors.append("Odd number of double quotes")
    return errors


def _check_arrows(block: str) -> list[tuple[int, str]]:
    """Return ``(line_number_in_block, complaint)`` for malformed arrow lines."""
    problems: list[tuple[int, str]] = []
    for idx, raw in enumerate(block.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("%%"):
            continue
        arrows = _ARROW_TOKENS.findall(line)
        if not arrows:
            continue
        # Crude check: an arrow should be flanked by non-empty tokens.
        for arrow in arrows:
            parts = line.split(arrow, 1)
            if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
                problems.append((idx, f"Arrow '{arrow}' is missing left- or right-hand side"))
                break
    return problems


def lint_block(block: str) -> list[str]:
    """Return a list of issues for a single mermaid block body."""
    issues: list[str] = []
    body = block.strip()
    if not body:
        issues.append("Empty mermaid block")
        return issues
    head = _diagram_head(body)
    if head is None:
        issues.append("No diagram type declared")
    else:
        # Trim a known prefix like ``graph TB`` or ``flowchart LR`` to its bare head.
        if head not in _VALID_DIAGRAM_HEADS:
            issues.append(f"Unknown diagram type: '{head}'")
    issues.extend(_check_brackets(body))
    for line_no, complaint in _check_arrows(body):
        issues.append(f"line {line_no}: {complaint}")
    return issues


def lint_markdown(rel: str, text: str) -> list[MermaidIssue]:
    """Find every mermaid block in ``text`` and return all issues."""
    issues: list[MermaidIssue] = []
    for index, match in enumerate(_BLOCK_RE.finditer(text), start=1):
        body = match.group(1)
        block_start_line = text[: match.start()].count("\n") + 1
        for problem in lint_block(body):
            issues.append(
                MermaidIssue(
                    file=rel,
                    block_index=index,
                    line=block_start_line,
                    message=problem,
                )
            )
    return issues


def lint_docs(docs_dir: Path) -> list[MermaidIssue]:
    issues: list[MermaidIssue] = []
    for md_path in sorted(docs_dir.rglob("*.md")):
        rel = md_path.relative_to(docs_dir).as_posix()
        text = md_path.read_text(encoding="utf-8", errors="replace")
        issues.extend(lint_markdown(rel, text))
    return issues
