import unittest

from archkit.mermaid import lint_block, lint_markdown


class LintBlockTests(unittest.TestCase):
    def test_valid_flowchart_passes(self):
        body = "flowchart LR\n  A --> B\n  B --> C\n"
        self.assertEqual(lint_block(body), [])

    def test_unknown_diagram_type_flagged(self):
        body = "noodlediagram\n  A --> B\n"
        issues = lint_block(body)
        self.assertTrue(any("unknown diagram type" in i.lower() for i in issues))

    def test_unbalanced_brackets_flagged(self):
        body = "flowchart LR\n  A[Node --> B\n"
        issues = lint_block(body)
        self.assertTrue(any("unclosed" in i.lower() for i in issues))

    def test_dangling_arrow_flagged(self):
        body = "flowchart LR\n  --> B\n"
        issues = lint_block(body)
        self.assertTrue(any("missing left-" in i.lower() or "missing right-" in i.lower() for i in issues))

    def test_empty_block_flagged(self):
        self.assertTrue(any("empty" in i.lower() for i in lint_block("\n")))


class LintMarkdownTests(unittest.TestCase):
    def test_extracts_block_with_correct_location(self):
        md = "# Title\n\n```mermaid\nflowchart LR\n  A --> B\n```\n"
        issues = lint_markdown("a.md", md)
        self.assertEqual(issues, [])

    def test_flags_bad_block(self):
        md = "# Title\n\n```mermaid\nfoo\n  A -->\n```\n"
        issues = lint_markdown("a.md", md)
        self.assertTrue(len(issues) >= 1)


if __name__ == "__main__":
    unittest.main()
