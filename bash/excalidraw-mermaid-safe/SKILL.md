---
name: excalidraw-mermaid-safe
description: Generate Excalidraw-compatible Mermaid flowcharts with parser-safe labels, readable grouped layouts, and conservative color classes. Use when users ask for a Mermaid diagram that imports cleanly in Excalidraw or for sanitizing broken Mermaid before Excalidraw import.
---

# Excalidraw Mermaid Safe

## Overview

Create or sanitize Mermaid flowcharts so they reliably parse in Excalidraw. This skill prioritizes parser safety, readability, deterministic validation, and conservative color styling over full Mermaid feature coverage.

Trigger examples:
- "make this mermaid import in excalidraw"
- "colored mermaid compatible with excalidraw"
- "sanitize this broken mermaid for excalidraw"
- "excalidraw diagram from markdown"

## Compatibility Contract

- Default output diagram type is `flowchart`.
- Default direction is `flowchart LR` for readability.
- Labels are quoted and sanitized.
- Markdown links and raw URLs are removed from node labels.
- Long labels are truncated before they become hard to scan.
- Styling uses conservative `classDef` / `class` declarations.
- Unsupported Mermaid diagram families are rejected instead of partially converted.

## Decision Protocol

1. Use `from-markdown` when the input is notes, an outline, a status report, or a design summary.
2. Use `sanitize-mermaid` when the input is already Mermaid or contains a Mermaid code block.
3. Use `auto` when the input type is unclear and the file extension or first non-empty line should decide.
4. Use `grouped` layout for documents with sections; use `flat` only for short linear flows.
5. Keep `--max-nodes` at `40` unless the user explicitly wants a denser map. Prefer summarizing over creating oversized diagrams.
6. Ask one clarifying question only when the intended diagram type changes the output materially, such as process flow vs. decision map.

## Completion Criteria

Before returning a diagram, ensure:

- The output starts with `flowchart`.
- Static validation passes.
- Raw URLs and Markdown links are not present in node labels.
- The diagram stays under the chosen node cap.
- If the user needs high confidence for Excalidraw import, `excalidraw-strict` validation passes or you clearly report why it could not run.

## Workflow

### 1) Generate from markdown

```bash
python3 scripts/excali_mermaid_safe.py \
  --input notes.md \
  --output diagram.mmd \
  --mode from-markdown \
  --palette safe \
  --layout grouped \
  --max-nodes 40 \
  --validate static
```

### 2) Sanitize existing mermaid

```bash
python3 scripts/excali_mermaid_safe.py \
  --input broken.mmd \
  --output fixed.mmd \
  --mode sanitize-mermaid \
  --palette safe \
  --layout grouped \
  --validate static
```

### 3) Auto detect mode

```bash
scripts/excali_mermaid_safe.sh \
  --input input.md \
  --output output.mmd \
  --mode auto \
  --palette safe \
  --layout grouped
```

### 4) Install parser dependency (one-time)

```bash
scripts/bootstrap.sh
```

### 5) Enforce strict parser check

```bash
scripts/excali_mermaid_safe.sh \
  --input notes.md \
  --output diagram.mmd \
  --mode from-markdown \
  --validate excalidraw-strict
```

## CLI

Primary command:

```bash
scripts/excali_mermaid_safe.sh \
  --input <input.md|input.mmd> \
  --output <output.mmd> \
  --mode auto \
  --palette safe \
  --layout grouped
```

Arguments:
- `--input`: source markdown or mermaid
- `--output`: output `.mmd`
- `--mode`: `auto|from-markdown|sanitize-mermaid`
- `--palette`: `safe|mono`
- `--layout`: `grouped|flat`
- `--max-nodes`: integer, default `40`
- `--validate`: `none|static|excalidraw|excalidraw-strict`, default `static`

Helper commands:

```bash
scripts/test_fixtures.sh      # run deterministic fixture regression tests
scripts/test_fixtures.sh --strict
scripts/doctor.sh             # check runtime plus static and optional strict validation
scripts/bootstrap.sh          # install optional Node parser dependency
```

## Validation

- `static` checks:
  - first non-empty line starts with `flowchart`
  - no `[[...](...)]` labels
  - no unsupported diagram declarations
  - node count does not exceed `--max-nodes`
- `excalidraw` validation:
  - attempts Node parse using `@excalidraw/mermaid-to-excalidraw`
  - if unavailable, warns and falls back to static success behavior
- `excalidraw-strict` validation:
  - attempts Node parse using `@excalidraw/mermaid-to-excalidraw`
  - fails if Node is missing, parser package is missing, or parse fails
  - depends on upstream Mermaid/Excalidraw packages; treat it as local validation for trusted diagrams unless dependency audit has been reviewed
- `scripts/test_fixtures.sh`:
  - regenerates fixture outputs in a temporary directory
  - diffs against `assets/fixtures/expected/*.mmd`
  - exits non-zero on behavioral drift

## Resources

- Parser compatibility notes: `references/excalidraw-mermaid-compat.md`
- Style templates: `assets/templates/*.mmd`
- Regression fixtures: `assets/fixtures/input/*.md` and `assets/fixtures/expected/*.mmd`

## Limitations

- Flowchart-first by design.
- Does not emit Excalidraw JSON scenes.
- Complex Mermaid features may be simplified for parser safety.
- Semantic grouping is heuristic and based on headings, bullets, tables, and common workflow keywords.
