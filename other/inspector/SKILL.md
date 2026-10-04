---
name: inspector
description: "Run sentence-level traceability verification on a blog, then generate viewer.html with interactive evidence panel. No LLM needed — pure Python."
argument-hint: [PROJECT_DIR]
allowed-tools: Bash(*), Read, Write
---

# Inspector

Your job is **traceability verification**. Parse the blog HTML, extract every visible sentence, link each back to its evidence in the role JSONs, and generate a self-contained `viewer.html` that lets readers inspect the evidence chain.

## Setup

- `PROJECT_DIR` = first argument
- Resolve `SKILL_DIR` = the directory containing this `SKILL.md` (`.../skills/data2story/inspector`). Replace `SKILL_DIR` placeholders with the resolved, quoted path before running Bash. Do not hard-code machine-local paths.
- Required files in PROJECT_DIR: `index.html`, `analyst.json`, `detective.json`, `designer.json`, `editor.json`

## Step 1: Run verify.py

```bash
python3 SKILL_DIR/scripts/verify.py PROJECT_DIR --log-errors
```

Produces `PROJECT_DIR/inspector.json` (sentence→evidence mapping). The output shape (format v3: `stats`, `sentences`, `unused_ids`) is in **[`references/inspector_schema.json`](references/inspector_schema.json)**.

## Step 2: Generate viewer.html

```bash
python3 SKILL_DIR/scripts/generate_viewer.py PROJECT_DIR
```

This reads `index.html` + `inspector.json` and produces `viewer.html` — a self-contained file that works on `file://` (no server needed). You run the script; you do not reimplement it. How it works (tag → style → script ordering), its critical constraints (line-number search, lite JSON, ES5, no fetch), and the viewer UI behavior are documented in **[`references/viewer_internals.json`](references/viewer_internals.json)**.

## Running both steps

```bash
python3 SKILL_DIR/scripts/verify.py PROJECT_DIR --log-errors
python3 SKILL_DIR/scripts/generate_viewer.py PROJECT_DIR
```

## Output

- `PROJECT_DIR/inspector.json` — full traceability data (with `raw_evidence`)
- `PROJECT_DIR/viewer.html` — self-contained interactive viewer (works on `file://`)

Done when `viewer.html` opens directly in a browser (no server), shows the blog with a working 🔍 toggle, and every traced sentence has a visible ID linking to its evidence summary.

## Step 3: Log Recurring Errors (Optional)

Running with `--log-errors` auto-updates known recurring-case metadata in `skills/errors/` for patterns the script detects directly from HTML. Use **manual** logging only when you discover a new pattern the script does not know yet — and only for Critical/High-severity issues that represent **patterns**, not one-off mistakes. The full logging process, the error-case markdown template, and the common error types worth logging are in **[`references/error_logging.json`](references/error_logging.json)**.
