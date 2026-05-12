"""ArchKit — deterministic verification layer.

A small, zero-dependency Python package that parses ArchKit-generated
architecture docs into a structured fact model, validates that every
claim is marked with the required discipline ([OBSERVED]/[INFERRED]/
[UNKNOWN]/[CLARIFIED]), and lints embedded Mermaid blocks.

Entry point: ``python -m archkit verify <docs-dir>``
"""

__version__ = "0.1.0"

from .schema import (
    Confidence,
    Connection,
    DataEntity,
    FactModel,
    Marker,
    Service,
    Unknown,
)

__all__ = [
    "Confidence",
    "Connection",
    "DataEntity",
    "FactModel",
    "Marker",
    "Service",
    "Unknown",
]
