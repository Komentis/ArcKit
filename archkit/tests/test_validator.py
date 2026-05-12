import unittest

from archkit.validator import validate_file


class ValidatorTests(unittest.TestCase):
    def test_flags_stub_placeholders(self):
        issues = validate_file("a.md", "## Table of Contents\n\nFoo is [TBD].\n")
        self.assertTrue(any("placeholder" in i.message.lower() for i in issues))

    def test_flags_bare_unknown(self):
        text = "## Table of Contents\n\nThe retry policy is [UNKNOWN].\n"
        issues = validate_file("a.md", text)
        self.assertTrue(any("[UNKNOWN]" in i.message for i in issues))

    def test_unknown_with_reason_is_ok(self):
        text = "## Table of Contents\n\nThe retry policy is [UNKNOWN — not in code].\n"
        issues = validate_file("a.md", text)
        self.assertFalse(any("[UNKNOWN]" in i.message for i in issues))

    def test_flags_hedge_without_marker(self):
        text = "## Table of Contents\n\nThe service likely calls Stripe.\n"
        issues = validate_file("a.md", text)
        self.assertTrue(any(i.severity == "warning" and "hedge" in i.message.lower() for i in issues))

    def test_hedge_with_inferred_marker_is_ok(self):
        text = "## Table of Contents\n\nThe service likely calls Stripe. [INFERRED]\n"
        issues = validate_file("a.md", text)
        self.assertFalse(any("hedge" in i.message.lower() for i in issues))

    def test_flags_missing_toc(self):
        text = "# Document\n\nBody without a TOC.\n"
        issues = validate_file("a.md", text)
        self.assertTrue(any("table of contents" in i.message.lower() for i in issues))

    def test_readme_does_not_need_toc(self):
        text = "# Document\n\nBody without a TOC.\n"
        issues = validate_file("README.md", text)
        self.assertFalse(any("table of contents" in i.message.lower() for i in issues))

    def test_service_table_missing_confidence(self):
        text = (
            "## Table of Contents\n\n"
            "## Services\n\n"
            "| Name | Type |\n|---|---|\n| OrderApi | API |\n"
        )
        issues = validate_file("a.md", text)
        self.assertTrue(any("confidence" in i.message.lower() for i in issues))

    def test_service_table_bad_confidence_value(self):
        text = (
            "## Table of Contents\n\n"
            "## Services\n\n"
            "| Name | Type | Confidence |\n|---|---|---|\n| OrderApi | API | sometimes |\n"
        )
        issues = validate_file("a.md", text)
        self.assertTrue(any("HIGH/MEDIUM/LOW" in i.message for i in issues))


if __name__ == "__main__":
    unittest.main()
