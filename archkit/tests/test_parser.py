import tempfile
import unittest
from pathlib import Path

from archkit.parser import parse_docs, parse_tables


SAMPLE_DOC = """\
# Architecture

## Table of Contents

- [Services](#services)
- [Connections](#connections)

## Services

| Name | Type | Technology | Confidence |
|---|---|---|---|
| OrderApi | API | .NET | HIGH |
| PaymentWorker | worker | Python | MEDIUM |

## Connections

| Source | Target | Mechanism | Direction | Confidence |
|---|---|---|---|---|
| OrderApi | PaymentWorker | message queue | async | HIGH |

## Data Model

| Entity | Owner | Storage | Consumers |
|---|---|---|---|
| Order | OrderApi | Postgres | PaymentWorker, ReportingApi |

## Unknowns

- [UNKNOWN — payment retry policy not visible from code]
- Whether ReportingApi reads Order events directly is unclear.
"""


class ParseTablesTests(unittest.TestCase):
    def test_extracts_three_tables(self):
        tables = parse_tables(SAMPLE_DOC)
        self.assertEqual(len(tables), 3)

    def test_skips_tables_inside_code_fences(self):
        md = SAMPLE_DOC + "\n```\n| ignored | header |\n|---|---|\n| a | b |\n```\n"
        tables = parse_tables(md)
        self.assertEqual(len(tables), 3)


class ParseDocsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.docs_dir = Path(self.tmp.name)
        (self.docs_dir / "architecture").mkdir()
        (self.docs_dir / "architecture" / "ARCHITECTURE.md").write_text(SAMPLE_DOC, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_extracts_services(self):
        model = parse_docs(self.docs_dir)
        self.assertEqual(len(model.services), 2)
        order = next(s for s in model.services if s.name == "OrderApi")
        self.assertEqual(order.technology, ".NET")
        self.assertEqual(order.confidence, "HIGH")
        self.assertEqual(order.source_file, "architecture/ARCHITECTURE.md")

    def test_extracts_connections(self):
        model = parse_docs(self.docs_dir)
        self.assertEqual(len(model.connections), 1)
        link = model.connections[0]
        self.assertEqual(link.source, "OrderApi")
        self.assertEqual(link.target, "PaymentWorker")
        self.assertEqual(link.direction, "async")

    def test_extracts_entities(self):
        model = parse_docs(self.docs_dir)
        self.assertEqual(len(model.entities), 1)
        order = model.entities[0]
        self.assertEqual(order.name, "Order")
        self.assertIn("PaymentWorker", order.consumers)
        self.assertIn("ReportingApi", order.consumers)

    def test_extracts_unknowns(self):
        model = parse_docs(self.docs_dir)
        descriptions = [u.description for u in model.unknowns]
        self.assertTrue(any("payment retry" in d.lower() for d in descriptions))


if __name__ == "__main__":
    unittest.main()
