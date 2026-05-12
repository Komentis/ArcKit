"""Discipline validator for ArchKit-generated docs.

Enforces the anti-hallucination guarantees stated in
ARCH_COMMANDMENTS.md and the scan prompts:

* Every inferred fact must be tagged ``[INFERRED]``.
* Every gap must be tagged ``[UNKNOWN — reason]`` with a reason after the dash.
* Service tables must have a Confidence column with HIGH/MEDIUM/LOW.
* Stub placeholders (``[TBD]``, ``[FILL]``, ``[NUMBER]`` …) must not survive.
* Every ``.md`` file must include a Table of Contents.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Issue:
    severity: str  # "error" or "warning"
    file: str
    line: int | None
    message: str

    def format(self) -> str:
        location = self.file if self.line is None else f"{self.file}:{self.line}"
        return f"[{self.severity.upper()}] {location} — {self.message}"


_STUB_PATTERNS = [
    re.compile(r"\[TBD\]", re.IGNORECASE),
    re.compile(r"\[FILL[\w ]*\]", re.IGNORECASE),
    re.compile(r"\[INSERT[\w ]*\]", re.IGNORECASE),
    re.compile(r"\[NUMBER\]"),
    re.compile(r"\[DATE\]"),
    re.compile(r"\[TODO[\w :]*\]", re.IGNORECASE),
    re.compile(r"\?{3,}"),
]

_HEDGE_WORDS = re.compile(
    r"\b(appears to|likely|presumably|probably|seems to|it looks like|"
    r"we think|we believe|may be|might be|could be)\b",
    re.IGNORECASE,
)

_MARKER_LINE = re.compile(r"\[(OBSERVED|INFERRED|UNKNOWN|CLARIFIED)(\s*[—\-]\s*[^\]]+)?\]")
_UNKNOWN_WITH_REASON = re.compile(r"\[UNKNOWN\s*[—\-]\s*[^\]]+\]")
_UNKNOWN_BARE = re.compile(r"\[UNKNOWN\](?!\s*[—\-])")
_HEADING = re.compile(r"^(#+)\s+(.+?)\s*$")
_TOC_HINT = re.compile(r"^##\s+table of contents\s*$", re.IGNORECASE)
_CODE_FENCE = re.compile(r"^```")
_TABLE_ROW = re.compile(r"^\s*\|.+\|\s*$")

_SERVICE_HEADER_HINTS = {"service", "name", "responsibility", "role"}
_CONFIDENCE_HEADER = "confidence"

# Files that are pure config/index — they don't carry architectural claims
# and shouldn't be required to host hedge markers or a service table.
_INDEX_FILES = {"readme.md", "index.md"}


def _is_index_file(rel_path: str) -> bool:
    return Path(rel_path).name.lower() in _INDEX_FILES


def _enumerate_outside_code(text: str):
    """Yield (line_number, line) skipping fenced code blocks."""
    in_code = False
    for idx, raw in enumerate(text.splitlines(), start=1):
        if _CODE_FENCE.match(raw.strip()):
            in_code = not in_code
            continue
        if in_code:
            continue
        yield idx, raw


def _check_stubs(rel: str, text: str, issues: list[Issue]) -> None:
    for line_no, line in _enumerate_outside_code(text):
        for pattern in _STUB_PATTERNS:
            if pattern.search(line):
                issues.append(
                    Issue(
                        severity="error",
                        file=rel,
                        line=line_no,
                        message=f"Unresolved placeholder: {pattern.pattern}",
                    )
                )


def _check_unknown_form(rel: str, text: str, issues: list[Issue]) -> None:
    for line_no, line in _enumerate_outside_code(text):
        for match in _UNKNOWN_BARE.finditer(line):
            issues.append(
                Issue(
                    severity="error",
                    file=rel,
                    line=line_no,
                    message="[UNKNOWN] must include a reason: use [UNKNOWN — reason]",
                )
            )


def _check_hedging_without_marker(rel: str, text: str, issues: list[Issue]) -> None:
    if _is_index_file(rel):
        return
    for line_no, line in _enumerate_outside_code(text):
        if _HEDGE_WORDS.search(line) and not _MARKER_LINE.search(line):
            issues.append(
                Issue(
                    severity="warning",
                    file=rel,
                    line=line_no,
                    message="Hedge language without [INFERRED]/[UNKNOWN] marker",
                )
            )


def _check_toc(rel: str, text: str, issues: list[Issue]) -> None:
    if _is_index_file(rel):
        return
    if not any(_TOC_HINT.match(raw.strip()) for raw in text.splitlines()):
        issues.append(
            Issue(
                severity="warning",
                file=rel,
                line=None,
                message="Missing '## Table of Contents' section",
            )
        )


def _check_service_table_confidence(rel: str, text: str, issues: list[Issue]) -> None:
    """For any table that looks like a service map, every row must have a confidence value."""
    in_code = False
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if _CODE_FENCE.match(line.strip()):
            in_code = not in_code
            i += 1
            continue
        if in_code or not _TABLE_ROW.match(line):
            i += 1
            continue
        # Header row + separator pattern.
        if i + 1 >= len(lines) or not re.match(r"^\s*\|?\s*:?-+", lines[i + 1]):
            i += 1
            continue
        headers = [c.strip().lower() for c in line.strip().strip("|").split("|")]
        if not (set(headers) & _SERVICE_HEADER_HINTS):
            i += 2
            continue
        if _CONFIDENCE_HEADER not in headers:
            issues.append(
                Issue(
                    severity="warning",
                    file=rel,
                    line=i + 1,
                    message="Service-like table missing 'Confidence' column",
                )
            )
            # advance past rows
            j = i + 2
            while j < len(lines) and _TABLE_ROW.match(lines[j]):
                j += 1
            i = j
            continue
        confidence_idx = headers.index(_CONFIDENCE_HEADER)
        j = i + 2
        while j < len(lines) and _TABLE_ROW.match(lines[j]):
            cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
            if confidence_idx < len(cells):
                value = cells[confidence_idx].upper()
                if value not in {"HIGH", "MEDIUM", "LOW"}:
                    issues.append(
                        Issue(
                            severity="error",
                            file=rel,
                            line=j + 1,
                            message=f"Confidence must be HIGH/MEDIUM/LOW, got '{cells[confidence_idx]}'",
                        )
                    )
            j += 1
        i = j


def validate_file(rel: str, text: str) -> list[Issue]:
    issues: list[Issue] = []
    _check_stubs(rel, text, issues)
    _check_unknown_form(rel, text, issues)
    _check_hedging_without_marker(rel, text, issues)
    _check_toc(rel, text, issues)
    _check_service_table_confidence(rel, text, issues)
    return issues


def validate_docs(docs_dir: Path) -> list[Issue]:
    issues: list[Issue] = []
    for md_path in sorted(docs_dir.rglob("*.md")):
        rel = md_path.relative_to(docs_dir).as_posix()
        text = md_path.read_text(encoding="utf-8", errors="replace")
        issues.extend(validate_file(rel, text))
    return issues
