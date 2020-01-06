"""Tests for black_markdown."""

from typing import Collection, List

import black_markdown
import pytest  # type: ignore

# mypy: allow_any_decorated


@pytest.mark.parametrize(  # type: ignore # untyped decorator makes function untyped
    "lines,expected",
    [
        (["foo\n", "bar\n"], ""),
        (["foo\n", " bar\n"], ""),
        ([" foo\n", " bar\n"], " "),
        ([" foo\n", "\n", " bar\n"], " "),
        ([" foo\n", "bar\n"], ""),
        ([" foo\n", "  bar\n"], " "),
        (["foo\n", "\tbar\n"], ""),
        (["\tfoo\n", "\tbar\n"], "\t"),
        (["\tfoo\n", "bar\n"], ""),
    ],
)
def test_guess_indent(lines: Collection[str], expected: str) -> None:
    """Test guessing indent."""
    assert black_markdown.guess_indent(lines) == expected


@pytest.mark.parametrize(  # type: ignore # untyped decorator makes function untyped
    "lines,prefix,expected",
    [
        (["foo\n", "bar\n"], "", ["foo\n", "bar\n"]),
        ([" foo\n", "bar\n"], "", [" foo\n", "bar\n"]),
        ([" foo\n", " bar\n"], " ", ["foo\n", "bar\n"]),
        ([" foo\n", "  bar\n"], " ", ["foo\n", " bar\n"]),
    ],
)
def test_dedent(lines: Collection[str], prefix: str, expected: List[str]) -> None:
    """Test dedent."""
    assert black_markdown.dedent(lines, prefix) == expected


@pytest.mark.parametrize(  # type: ignore # untyped decorator makes function untyped
    "lines,prefix,expected",
    [
        (["foo\n", "bar\n"], "", ["foo\n", "bar\n"]),
        ([" foo\n", "bar\n"], "", [" foo\n", "bar\n"]),
        ([" foo\n", " bar\n"], "*", ["* foo\n", "* bar\n"]),
        ([" foo\n", "  bar\n"], "*", ["* foo\n", "*  bar\n"]),
        (["foo\n", "bar"], "*", ["*foo\n", "*bar"]),
        (
            ["foo\n", "bar\n", "\n", "quux\n"],
            "*",
            ["*foo\n", "*bar\n", "\n", "*quux\n"],
        ),
    ],
)
def test_indent(lines: Collection[str], prefix: str, expected: List[str]) -> None:
    """Test indent."""
    assert black_markdown.indent(lines, prefix) == expected
