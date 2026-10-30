#!/usr/bin/env python3
"""Validate Mermaid diagrams by rendering each one with the official Mermaid CLI.

Usage:
    python validate_mermaid.py <file-or-dir> [<file-or-dir> ...]

Accepts Markdown files (every ```mermaid or ~~~mermaid block is checked),
standalone .mmd/.mermaid files, or directories (searched recursively).
Never modifies the input files. Exits 1 if any diagram fails to render.

Requires Node.js. Uses `mmdc` if it is on PATH, otherwise `npx -y @mermaid-js/mermaid-cli`.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FENCE_OPEN = re.compile(r"^\s*(`{3,}|~{3,})\s*mermaid\b.*$")
STANDALONE_SUFFIXES = {".mmd", ".mermaid"}
MARKDOWN_SUFFIXES = {".md", ".markdown"}
SKIP_DIRS = {"node_modules", ".git"}
TIMEOUT_SECONDS = 90


def cli_command() -> list[str]:
    if shutil.which("mmdc"):
        return ["mmdc"]
    if shutil.which("npx"):
        return ["npx", "-y", "@mermaid-js/mermaid-cli@latest"]
    sys.exit("Node.js is required: neither `mmdc` nor `npx` was found on PATH.")


def collect_files(paths: list[str]) -> list[Path]:
    files = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if SKIP_DIRS.isdisjoint(child.parts) and child.suffix.lower() in (
                    MARKDOWN_SUFFIXES | STANDALONE_SUFFIXES
                ):
                    files.append(child)
        elif path.is_file():
            files.append(path)
        else:
            sys.exit(f"Not found: {raw}")
    return files


def extract_blocks(path: Path) -> list[tuple[int, str]]:
    """Return (1-based start line, diagram source) for each diagram in the file."""
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in STANDALONE_SUFFIXES:
        return [(1, text)]

    blocks = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        match = FENCE_OPEN.match(lines[i])
        if not match:
            i += 1
            continue
        fence = match.group(1)
        start = i + 2
        body = []
        i += 1
        closing = re.compile(rf"^\s*{re.escape(fence[0])}{{{len(fence)},}}\s*$")
        while i < len(lines) and not closing.match(lines[i]):
            body.append(lines[i])
            i += 1
        blocks.append((start, "\n".join(body)))
        i += 1
    return blocks


def short_error(output: str) -> str:
    """Keep the parser message and drop the JavaScript stack trace."""
    kept = []
    for line in output.splitlines():
        if line.startswith(("Parser.", "    at ")):
            break
        if line.strip() and not line.startswith("Generating single mermaid chart"):
            kept.append(line)
    return "\n".join(kept) or "Unknown render error"


def validate(command: list[str], source: str, workdir: Path) -> str | None:
    """Return None if the diagram renders, otherwise a short error message."""
    if not source.strip():
        return "Empty diagram"
    source_file = workdir / "diagram.mmd"
    source_file.write_text(source, encoding="utf-8")
    try:
        result = subprocess.run(
            [*command, "-q", "-i", str(source_file), "-o", str(workdir / "diagram.svg")],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return f"Timed out after {TIMEOUT_SECONDS}s"
    if result.returncode == 0:
        return None
    return short_error(result.stderr + result.stdout)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2

    files = collect_files(sys.argv[1:])
    command = cli_command()
    checked = failed = 0

    with tempfile.TemporaryDirectory() as tmp:
        for path in files:
            for start, source in extract_blocks(path):
                checked += 1
                error = validate(command, source, Path(tmp))
                if error is None:
                    print(f"PASS {path}:{start}")
                else:
                    failed += 1
                    print(f"FAIL {path}:{start}")
                    print("\n".join(f"     {line}" for line in error.splitlines()))

    print(f"\n{checked} diagram(s) checked, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
