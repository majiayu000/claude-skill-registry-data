---
name: flashback
description: Session context handoff and restart prompt generation. Consolidate memory, capture decisions/pending work, and emit a self-contained restart message. Use when the user says "flashback", "save state", "checkpoint", "wrap up", or asks for a session handoff, especially at end of session or when context is running low.
---

# Flashback

## Purpose
Generate a deterministic handoff artifact for the next session:
1. Gather current session state from memory/tasks/git.
2. Consolidate memory safely.
3. Generate a restart prompt and JSON run report.
4. Copy prompt to clipboard when available.

## Runtime
This skill uses a shared runtime-aware script. For Codex, default runtime is `codex`.
Use `--runtime claude` only for parity testing or Claude-targeted output generation.

## Quick Start

Set `FLASHBACK_EXAMPLE_REPO` to any target repo you want to use for examples, or replace it with a concrete `--repo-root` path.

Run a dry-run first:

```bash
uv run python scripts/flashback.py \
  --mode full \
  --repo-root $FLASHBACK_EXAMPLE_REPO \
  --dry-run
```

Run full flow:

```bash
uv run python scripts/flashback.py \
  --mode full \
  --repo-root $FLASHBACK_EXAMPLE_REPO
```

Quick mode (skip consolidation):

```bash
uv run python scripts/flashback.py \
  --mode quick \
  --repo-root $FLASHBACK_EXAMPLE_REPO
```

Summary-first mode (user context as primary accomplishments input):

```bash
uv run python scripts/flashback.py \
  --mode summary \
  --summary "Completed case scoring and validated warm-start handoff method" \
  --repo-root $FLASHBACK_EXAMPLE_REPO
```

## Script Interface
Use this interface for automation and manual runs:

```bash
uv run python scripts/flashback.py \
  --mode {full|quick|summary} \
  --summary "..." \
  --repo-root <path> \
  --memory-dir <path|auto> \
  --out-dir <path> \
  [--no-clipboard] \
  [--dry-run] \
  [--runtime {auto|codex|claude}]
```

## Workflow Contract
### 1. Discovery
Resolve memory path in strict order:
1. `--memory-dir` argument.
2. `FLASHBACK_MEMORY_DIR` environment variable.
3. `<repo>/MEMORY.md`.
4. `<repo>/memory/MEMORY.md`.
5. `<repo>/ai_docs/MEMORY.md`.

If unresolved:
- In `--dry-run`: fail with actionable error.
- In normal mode: ask once for a path; if unavailable, bootstrap `<repo>/MEMORY.md`.

### 2. Consolidation (full mode)
Apply the consolidation policy in `references/consolidation_policy.md`.
Key safety rules:
- Never auto-move protected sections (invariants, safety constraints, architecture map).
- Move only allowlisted sections and only when `MEMORY.md > 180` lines.
- Never delete content; only move with backlink.

### 3. Generation
Build restart prompt using `references/restart_prompt_template.md`.
Include:
- accomplishments,
- locked decisions,
- active tasks,
- pending TODOs,
- immediate next action,
- ordered files-to-read,
- warnings.

### 4. Delivery
Write timestamped outputs (never overwrite):
- Markdown: `output/flashback/flashback_YYYY-MM-DD_HHMM[_NN].md`
- JSON report: `output/flashback/flashback_YYYY-MM-DD_HHMM[_NN].json`

Clipboard copy failure is warning-only.

## Data Contract (JSON Report)
The run report includes:
- `mode`
- `memory_line_count_before`
- `memory_line_count_after`
- `active_tasks`
- `pending_todos`
- `decisions`
- `warnings`
- `files_read`
- `files_updated`
- `output_file`
- `clipboard_status`

## Compatibility and Parity
Use dual-runtime parity checks from `references/compatibility_matrix.md` and run both:

```bash
uv run python scripts/flashback.py --runtime codex --mode quick --repo-root <repo> --dry-run
uv run python scripts/flashback.py --runtime claude --mode quick --repo-root <repo> --dry-run
```

## Validation
```bash
python3 $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py \
  .
```
