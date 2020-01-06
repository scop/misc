import pytest

import black_markdown


@pytest.mark.parametrize(
    "lines,expected",
    [
        (("foo\n", "bar\n"), ""),
        (("foo\n", " bar\n"), ""),
        ((" foo\n", " bar\n"), " "),
        ((" foo\n", "\n", " bar\n"), " "),
        ((" foo\n", "bar\n"), ""),
        ((" foo\n", "  bar\n"), " "),
        (("foo\n", "\tbar\n"), ""),
        (("\tfoo\n", "\tbar\n"), "\t"),
        (("\tfoo\n", "bar\n"), ""),
    ],
)
def test_detect_indent(lines, expected):
    assert black_markdown.detect_indent(lines) == expected


@pytest.mark.parametrize(
    "lines,prefix,expected",
    [
        (("foo\n", "bar\n"), "", ["foo\n", "bar\n"]),
        ((" foo\n", "bar\n"), "", [" foo\n", "bar\n"]),
        ((" foo\n", " bar\n"), " ", ["foo\n", "bar\n"]),
        ((" foo\n", "  bar\n"), " ", ["foo\n", " bar\n"]),
    ],
)
def test_dedent(lines, prefix, expected):
    assert black_markdown.dedent(lines, prefix) == expected


@pytest.mark.parametrize(
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
            ["*foo\n", "*bar\n", "*\n", "*quux\n"],
        ),
    ],
)
def test_indent(lines, prefix, expected):
    assert black_markdown.indent(lines, prefix) == expected
