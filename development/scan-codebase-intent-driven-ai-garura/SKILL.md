---
name: scan-codebase
description: Run the deterministic codebase scanner (core/components/plays/codify/lib/scan.py) over one or more repository roots and produce a bounded scan-index.json under STM. This skill is the sole structured-input producer for every infer-*-from-code skill. No LLM is involved — it shells out to scan.py and records status. Used exclusively by the /codify play.
version: 0.1.0
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Grep, Glob
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# scan-codebase

Called by the `/codify` play before any inference agent dispatches. Produces `scan-index.json` in STM. The index is the only structured-input that downstream inference skills consume.

## Purpose

Garura's /codify play is a brownfield bootstrap — it reverse-engineers a product's LTM from an existing codebase. Before any LLM inference runs, a deterministic scan extracts structured facts: manifest data, directory tree, git signals, framework idioms, frontend detection, ADR harvest, config surface. That scan is this skill's job. Agents must never navigate source code as their primary input — they reason over the scan-index this skill produces.

## Input

Receive from the /codify play orchestrator via JSON contract.

- `repo_roots` (list[path], required) — one or more absolute repository root paths to scan. Multi-repo monorepos pass multiple entries.
- `output_path` (path, required) — `{stm_base}/{issue}/evidence/codify/scan-index.json`
- `size_limit_mb` (int, optional, default 10) — soft cap on scan-index.json size; scan writes a partial index with `scan_status: budget_exhausted` on breach.
- `time_limit_seconds` (int, optional, default 600) — soft cap on wall-clock duration.
- `extra_ignore` (list[str], optional) — additional ignore globs beyond the built-in list (node_modules, dist, .git, etc.).

## Process

### 1. Validate inputs

- Confirm every entry in `repo_roots` is an absolute path to an existing directory. Missing or non-directory → structured failure with `what_failed: invalid_repo_root` and the offending path.
- Confirm `output_path` parent directory is writable. If parent does not exist, create it. Failure to create → structured failure with `what_failed: stm_path_unwritable`.
- Confirm Python 3.8+ is on PATH. Missing → structured failure with `what_failed: python_missing`.
- Confirm `scan.py` exists at `core/components/plays/codify/lib/scan.py` relative to repo root. Missing → structured failure with `what_failed: scan_script_missing`.

### 2. Invoke scan.py

Build the command line:

```
python3 core/components/plays/codify/lib/scan.py \
    --output <output_path> \
    --size-limit-mb <size_limit_mb> \
    --time-limit-s <time_limit_seconds> \
    --path <root_1> [--path <root_2> ...] \
    [--ignore <pattern> ...]
```

Run via subprocess. Capture stdout and stderr. Honor the time-limit budget by passing `--time-limit-s` — do not wrap with a separate timeout.

### 3. Inspect status

After scan.py exits:

- Exit code 0 AND `scan-index.json` exists → scan ran to a definite status (`complete` or `budget_exhausted`).
- Exit code 2 OR `scan-index.json` missing → scan failed; structured failure with `what_failed: scan_script_error` and the captured stderr.

Read `scan-index.json`. Parse top-level fields: `scan_status`, `scan_size_bytes`, `scan_duration_seconds`, `repos`, `budget`.

### 4. Emit result

Write a small `scan-result.yaml` alongside the index at `{stm_base}/{issue}/evidence/codify/scan-result.yaml` containing:

```yaml
scan_index_path: "<output_path>"
scan_status: "complete" | "budget_exhausted"
budget_exhausted_reason: "time_limit" | "size_limit" | null
scan_duration_seconds: <float>
scan_size_bytes: <int>
repos:
  - label: "<repo-label>"
    root_path: "<abs-path>"
    file_count: <int>
    total_bytes: <int>
manifest_count: <int>
frontend_detected_any_repo: <bool>
```

Return this YAML path to the caller.

## Output

Primary artifact: `scan-index.json` at `output_path`.

Companion artifact: `scan-result.yaml` at `{stm_base}/{issue}/evidence/codify/scan-result.yaml`.

No decision manifest is produced — this skill makes no inferred decisions. It is a deterministic wrapper around scan.py.

## Failure Modes

All failures return a structured failure payload per the universal contract:

```yaml
status: failure
what_failed: "<one of: invalid_repo_root, stm_path_unwritable, python_missing, scan_script_missing, scan_script_error>"
detail: "<specific error string>"
evidence: {}
```

## Notes

- The scanner is intentionally conservative: if ripgrep or git is unavailable, those sections of the index are omitted (with an `available: false` flag) rather than failing the whole scan. Downstream skills MUST handle missing sections.
- The scanner enforces its own budgets. This skill does NOT retry on `budget_exhausted` — surfacing the partial status is the correct behavior; the play orchestrator prompts the user.
- The scan is read-only on the target codebase. It creates no files inside any `repo_root`.
