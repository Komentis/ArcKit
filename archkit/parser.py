"""Parse ArchKit-generated markdown into a FactModel.

The parser walks every ``.md`` file under a docs directory, extracts
GitHub-flavoured markdown tables, and maps tables with known headers
to the corresponding fact types.

The parser is intentionally permissive — unknown tables are skipped,
missing optional columns become ``None``, and the parser never throws
on malformed input. The validator is responsible for surfacing problems.
"""

from __future__ import annotations

import re
from dataclasses import fields
from pathlib import Path

from .schema import Connection, DataEntity, FactModel, Service, Unknown


_TABLE_ROW = re.compile(r"^\s*\|(.+)\|\s*$")
_SEPARATOR_ROW = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$")
_CODE_FENCE = re.compile(r"^```")
_UNKNOWN_DASH = re.compile(r"\[UNKNOWN\s*[—\-]\s*(?P<reason>[^\]]+)\]")
_UNKNOWN_BARE = re.compile(r"\[UNKNOWN\]")


def _split_cells(line: str) -> list[str]:
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [cell.strip() for cell in inner.split("|")]


def _normalise_header(header: str) -> str:
    """Lowercase, collapse whitespace, strip punctuation."""
    cleaned = re.sub(r"[^a-z0-9 ]", " ", header.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def parse_tables(markdown: str) -> list[dict]:
    """Return a list of ``{"headers": [...], "rows": [dict, ...]}``.

    Rows preserve original header text as keys so callers can match by
    semantic name. Tables inside fenced code blocks are skipped.
    """
    tables: list[dict] = []
    in_code_block = False
    headers: list[str] | None = None
    rows: list[dict] = []

    def flush() -> None:
        if headers is not None and rows:
            tables.append({"headers": headers, "rows": rows.copy()})

    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if _CODE_FENCE.match(line.strip()):
            in_code_block = not in_code_block
            i += 1
            continue
        if in_code_block:
            i += 1
            continue

        if _TABLE_ROW.match(line):
            # Header candidate — needs a separator on the next line.
            if i + 1 < len(lines) and _SEPARATOR_ROW.match(lines[i + 1]):
                flush()
                headers = _split_cells(line)
                rows = []
                i += 2
                while i < len(lines) and _TABLE_ROW.match(lines[i]):
                    cells = _split_cells(lines[i])
                    if len(cells) == len(headers):
                        rows.append({h: c for h, c in zip(headers, cells)})
                    i += 1
                continue
        i += 1
    flush()
    return tables


def _header_set(table: dict) -> set[str]:
    return {_normalise_header(h) for h in table["headers"]}


_SERVICE_REQUIRED = {"name"}
_SERVICE_HINTS = {"service", "type", "technology", "responsibility", "role", "exposes", "consumes"}
_CONNECTION_REQUIRED = {"source", "target"}
_CONNECTION_HINTS = {"mechanism", "contract", "direction"}
_ENTITY_REQUIRED = {"entity"}
_ENTITY_HINTS = {"owner", "storage", "consumers"}


def _classify_table(table: dict) -> str | None:
    headers = _header_set(table)
    if _SERVICE_REQUIRED.issubset(headers) and headers & _SERVICE_HINTS:
        return "services"
    if _CONNECTION_REQUIRED.issubset(headers):
        return "connections"
    if _ENTITY_REQUIRED.issubset(headers) and headers & _ENTITY_HINTS:
        return "entities"
    return None


def _get(row: dict, *aliases: str) -> str | None:
    """Look up a row value by any of the alias header names (case-insensitive)."""
    normalised = {_normalise_header(k): v for k, v in row.items()}
    for alias in aliases:
        value = normalised.get(_normalise_header(alias))
        if value is not None and value.strip() not in {"", "—", "-", "N/A"}:
            return value.strip()
    return None


def _split_list(value: str | None) -> list[str]:
    if not value:
        return []
    parts = re.split(r"[,;/]|<br\s*/?>", value)
    return [p.strip() for p in parts if p.strip()]


def _row_to_service(row: dict, source_file: str) -> Service | None:
    name = _get(row, "name", "service")
    if not name:
        return None
    return Service(
        name=name,
        type=_get(row, "type"),
        technology=_get(row, "technology", "tech", "stack"),
        entry_point=_get(row, "entry point", "entrypoint"),
        responsibility=_get(row, "responsibility", "role", "primary responsibility"),
        port=_get(row, "port", "port/url", "url"),
        exposes=_split_list(_get(row, "exposes")),
        consumes=_split_list(_get(row, "consumes")),
        confidence=_get(row, "confidence"),
        source_file=source_file,
    )


def _row_to_connection(row: dict, source_file: str) -> Connection | None:
    source = _get(row, "source", "source service", "from")
    target = _get(row, "target", "target service", "to")
    if not source or not target:
        return None
    return Connection(
        source=source,
        target=target,
        mechanism=_get(row, "mechanism", "protocol"),
        contract=_get(row, "contract"),
        direction=_get(row, "direction"),
        confidence=_get(row, "confidence"),
        source_file=source_file,
    )


def _row_to_entity(row: dict, source_file: str) -> DataEntity | None:
    name = _get(row, "entity", "entity name", "name")
    if not name:
        return None
    return DataEntity(
        name=name,
        owner=_get(row, "owner"),
        storage=_get(row, "storage", "store"),
        consumers=_split_list(_get(row, "consumers")),
        source_file=source_file,
    )


def _extract_unknowns(markdown: str, source_file: str) -> list[Unknown]:
    unknowns: list[Unknown] = []
    for match in _UNKNOWN_DASH.finditer(markdown):
        reason = match.group("reason").strip()
        unknowns.append(Unknown(description=reason, reason=reason, source_file=source_file))
    # Also collect bullet lines from a section literally called "Unknowns".
    # Skip bullets containing any [UNKNOWN ...] marker because those are
    # already captured by the regex pass above.
    in_unknowns = False
    for raw in markdown.splitlines():
        line = raw.strip()
        if line.lower().startswith("## ") or line.lower().startswith("# "):
            in_unknowns = "unknown" in line.lower()
            continue
        if in_unknowns and line.startswith("- ") and "[UNKNOWN" not in line.upper():
            unknowns.append(Unknown(description=line[2:].strip(), source_file=source_file))
    return unknowns


def parse_docs(docs_dir: Path) -> FactModel:
    """Walk ``docs_dir`` recursively and return a populated FactModel."""
    model = FactModel()
    for md_path in sorted(docs_dir.rglob("*.md")):
        rel = md_path.relative_to(docs_dir).as_posix()
        model.source_files.append(rel)
        text = md_path.read_text(encoding="utf-8", errors="replace")
        for table in parse_tables(text):
            kind = _classify_table(table)
            if kind == "services":
                for row in table["rows"]:
                    service = _row_to_service(row, rel)
                    if service:
                        model.services.append(service)
            elif kind == "connections":
                for row in table["rows"]:
                    connection = _row_to_connection(row, rel)
                    if connection:
                        model.connections.append(connection)
            elif kind == "entities":
                for row in table["rows"]:
                    entity = _row_to_entity(row, rel)
                    if entity:
                        model.entities.append(entity)
        model.unknowns.extend(_extract_unknowns(text, rel))
    return model
