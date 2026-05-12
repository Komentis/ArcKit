"""CLI entry point — ``python -m archkit <command> <docs-dir>``.

Commands
--------

* ``parse`` — emit the fact model as JSON
* ``validate`` — run the discipline validator
* ``lint-mermaid`` — lint embedded Mermaid blocks
* ``verify`` — run validate + lint-mermaid; non-zero exit if any errors

Exit codes
----------

* ``0`` — no errors (warnings allowed)
* ``1`` — at least one error-severity issue
* ``2`` — argument / usage problem
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .mermaid import lint_docs as lint_mermaid_docs
from .parser import parse_docs
from .validator import Issue, validate_docs


def _cmd_parse(args: argparse.Namespace) -> int:
    model = parse_docs(args.docs_dir)
    payload = model.to_dict()
    if args.output:
        args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Wrote fact model to {args.output}")
    else:
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    issues = validate_docs(args.docs_dir)
    return _report(issues, label="validator")


def _cmd_lint_mermaid(args: argparse.Namespace) -> int:
    issues = lint_mermaid_docs(args.docs_dir)
    for issue in issues:
        print(issue.format())
    if issues:
        print(f"\n{len(issues)} Mermaid issue(s)", file=sys.stderr)
        return 1
    print("Mermaid OK")
    return 0


def _cmd_verify(args: argparse.Namespace) -> int:
    rc1 = _cmd_validate(args)
    rc2 = _cmd_lint_mermaid(args)
    return rc1 or rc2


def _report(issues: list[Issue], label: str) -> int:
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    for issue in issues:
        print(issue.format())
    summary = f"\n{label}: {len(errors)} error(s), {len(warnings)} warning(s)"
    if errors:
        print(summary, file=sys.stderr)
        return 1
    print(summary)
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m archkit",
        description="Deterministic checks for ArchKit-generated architecture docs.",
    )
    parser.add_argument("--version", action="version", version=f"archkit {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_docs_arg(p: argparse.ArgumentParser) -> None:
        p.add_argument(
            "docs_dir",
            type=Path,
            help="Directory containing ArchKit-generated .md files (e.g. docs/).",
        )

    p_parse = sub.add_parser("parse", help="Emit the fact model as JSON.")
    add_docs_arg(p_parse)
    p_parse.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Write JSON to this file instead of stdout.",
    )
    p_parse.set_defaults(func=_cmd_parse)

    p_validate = sub.add_parser("validate", help="Run discipline checks.")
    add_docs_arg(p_validate)
    p_validate.set_defaults(func=_cmd_validate)

    p_lint = sub.add_parser("lint-mermaid", help="Lint embedded Mermaid diagrams.")
    add_docs_arg(p_lint)
    p_lint.set_defaults(func=_cmd_lint_mermaid)

    p_verify = sub.add_parser("verify", help="Run validate + lint-mermaid.")
    add_docs_arg(p_verify)
    p_verify.set_defaults(func=_cmd_verify)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if not args.docs_dir.exists():
        print(f"docs_dir not found: {args.docs_dir}", file=sys.stderr)
        return 2
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
