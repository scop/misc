#!/usr/bin/env python3

# Copyright 2019 Ville Skyttä
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

"""Run black on Python code blocks in Markdown files."""

import fileinput
import re
import subprocess
import sys
from typing import Collection, List, Optional

BLACK_DEFAULT_OPTIONS = ["--quiet"]


def usage(exitcode: int) -> None:
    """Output usage message and exit."""
    outfile = sys.stderr if exitcode else sys.stdout
    print(
        f"""\
Usage: {sys.argv[0]} [--help|-h|-?] [black options] MARKDOWN-FILE...

Options list terminates after "--" or at first argument not starting with "-".
black options default to {' '.join(BLACK_DEFAULT_OPTIONS)}.""",
        file=outfile,
    )
    if not exitcode:
        print(
            f"""\

{sys.argv[0]} runs black on Python code blocks in Markdown files.
Be sure to have backups and inspect results afterwards, as there are no guarantees whatsoever. For example, but certainly not limited to, data loss can be easily accomplished by not having black installed and in $PATH, or Ctrl-C'ing execution of this script.""",
            file=outfile,
        )
    sys.exit(exitcode)


def guess_indent(lines: Collection[str]) -> str:
    """
    Guess indent from list of lines.

    Completely empty lines are ignored, i.e. they don't force empty guess result.
    """
    for char in (" ", "\t"):
        count = min(
            len(matcher.group("indent"))
            for matcher in (
                re.match(f"(?P<indent>{char}*)[^{char}]", line)
                for line in lines
                # Allow (ignore) unindented empty lines
                if line != "\n"
            )
            if matcher
        )
        if count:
            return char * count
    return ""


def dedent(lines: Collection[str], prefix: str) -> List[str]:
    """Dedent list of lines."""
    return [line[len(prefix) :] for line in lines]


def indent(lines: Collection[str], prefix: str) -> List[str]:
    """Indent list of lines."""
    return [f"{prefix}{line}" if line not in ("", "\n") else line for line in lines]


def main() -> None:
    """Run main entry point."""

    if len(sys.argv) < 2:
        usage(1)
    if sys.argv[1] in ("--help", "-h", "-?"):
        usage(0)

    black_options = []
    files = []
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--" or not arg.startswith("-"):
            files.extend(sys.argv[i + 1 + (1 if arg == "--" else 0) :])
            break
        black_options.append(arg)
    if not files:
        usage(1)

    black = ["black"] + (black_options or BLACK_DEFAULT_OPTIONS) + ["-"]
    buf: Optional[List[str]] = None
    with fileinput.input(files, inplace=True) as infile:
        for line in infile:

            if fileinput.isfirstline():
                if buf is not None:
                    print(
                        "# WARNING: above code block still open when file ended, "
                        "content lost:",
                        file=sys.stderr,
                    )
                    sys.stderr.write("".join(buf))
                    buf = None

            if buf is None:
                if line.strip() == "```python":
                    start = fileinput.filelineno()
                    buf = []
                sys.stdout.write(line)
                continue

            if line.strip() == "```":
                print(f"# {fileinput.filename()}:{start}", file=sys.stderr)
                prefix = guess_indent(buf)
                res = subprocess.run(  # type: ignore # mypy/typeshed bug? # nosec # pylint: disable=subprocess-run-check
                    black,
                    input="".join(dedent(buf, prefix)),
                    stdout=subprocess.PIPE,
                    text=True,
                )
                sys.stdout.write("".join(indent(res.stdout.splitlines(True), prefix)))
                buf = None
                sys.stdout.write(line)
            else:
                buf.append(line)


if __name__ == "__main__":
    main()
