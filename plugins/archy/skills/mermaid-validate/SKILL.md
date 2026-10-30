---
name: mermaid-validate
description: Validate and fix Mermaid diagrams by actually rendering them with the official Mermaid CLI. Use when a Mermaid diagram fails to render, shows a parse or syntax error, or when asked to check, validate, lint, or fix Mermaid diagrams in Markdown files or .mmd files. Also use after creating or editing a Mermaid diagram to confirm it renders before finishing.
---

# Mermaid Validate

Check that Mermaid diagrams really render, then fix the ones that don't. Rendering with the official CLI is the source of truth; a diagram that "looks right" can still fail to parse.

For syntax and diagram-type guidance when writing diagrams, use the `mermaid-diagrams` skill.

## Prerequisites

- Node.js (for `npx`) and Python 3.
- The first run downloads `@mermaid-js/mermaid-cli` and a headless Chromium, which can take a minute. If that download is blocked, install `mmdc` another way or point Puppeteer at an installed Chrome with `PUPPETEER_EXECUTABLE_PATH`. If neither works, tell the user the diagrams could not be validated; do not claim they are valid.

## Workflow

1. **Validate.** Run the script from this skill's directory against the files or folders in scope:

   ```sh
   python scripts/validate_mermaid.py docs/ README.md
   ```

   It checks every ```` ```mermaid ```` / `~~~mermaid` block in Markdown files and any `.mmd` / `.mermaid` file, prints `PASS` or `FAIL` with `file:line` and the parser error, and exits 1 if anything failed. It never edits files.

2. **Fix each failure.** Read the error (it names the offending line and what the parser expected), apply the smallest change that fixes it, and keep the diagram's meaning, node names, and layout intent.

3. **Re-validate** the same files. Repeat up to 3 times per diagram. If a diagram still fails, leave it as it was and report the error instead of guessing further.

4. **Report.** List each fixed diagram (file and line) with a one-line description of the change, and list any that could not be fixed. Show a diff before overwriting files outside the user's current task.

## Common causes

| Symptom | Likely cause and fix |
|---|---|
| Parse error near `end` | `end` is reserved in flowcharts and sequence diagrams. Use `End`, `"end"`, or rename the node. |
| Error at a `(`, `)`, `[`, `]`, `{`, `}` in a label | Special characters in labels must be quoted: `A["Create user (admin)"]`. |
| Unbalanced shape, for example `B{OK?` | Close every shape bracket. |
| Error on an edge label | Edge text is `-->|text|` or `-- text -->`; check for missing or extra `|`. |
| Sequence message fails | Messages need a colon: `A->>B: hello`. |
| Node IDs with spaces or symbols | Use a simple ID and put the display text in a label: `userSvc["User Service"]`. |
| `%%` comment trailing a statement | Comments must be on their own line. |
| Unknown diagram type | The first line must be a valid keyword (`flowchart`, `sequenceDiagram`, `classDiagram`, `erDiagram`, `C4Context`, ...). Some types need a newer Mermaid than the one installed. |
| Markdown shows the code, not a diagram | The fence must be exactly ```` ```mermaid ````, and the platform must support Mermaid. |

## Notes

- A diagram that renders with the CLI can still render differently on GitHub or another platform if that platform runs an older Mermaid version. Avoid very new diagram types when the diagram must display elsewhere.
- Do not change anything outside the Mermaid blocks.
- Diagram content stays on the user's machine; the CLI renders locally and sends nothing to an external service.
