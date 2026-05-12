"""Structured fact model for ArchKit outputs.

These dataclasses are the canonical in-memory representation of what
ArchKit's markdown documents describe. Two runs of /arch-scan on the
same codebase should produce equivalent FactModel instances — that's
how we make architectural facts diffable.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum


class Confidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Marker(str, Enum):
    """Discipline markers — every claim must carry one (or be a heading/structural row)."""

    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    UNKNOWN = "UNKNOWN"
    CLARIFIED = "CLARIFIED"


@dataclass
class Service:
    name: str
    type: str | None = None
    technology: str | None = None
    entry_point: str | None = None
    responsibility: str | None = None
    port: str | None = None
    exposes: list[str] = field(default_factory=list)
    consumes: list[str] = field(default_factory=list)
    confidence: str | None = None
    source_file: str | None = None


@dataclass
class Connection:
    source: str
    target: str
    mechanism: str | None = None
    contract: str | None = None
    direction: str | None = None  # "sync" or "async"
    confidence: str | None = None
    source_file: str | None = None


@dataclass
class DataEntity:
    name: str
    owner: str | None = None
    storage: str | None = None
    consumers: list[str] = field(default_factory=list)
    source_file: str | None = None


@dataclass
class Unknown:
    description: str
    reason: str | None = None
    source_file: str | None = None


@dataclass
class FactModel:
    services: list[Service] = field(default_factory=list)
    connections: list[Connection] = field(default_factory=list)
    entities: list[DataEntity] = field(default_factory=list)
    unknowns: list[Unknown] = field(default_factory=list)
    source_files: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def service_names(self) -> set[str]:
        return {s.name for s in self.services}
