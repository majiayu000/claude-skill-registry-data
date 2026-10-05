---
name: ha:output-compression
description: Reduce pytest/mypy/ruff/hassfest output noise (5-15% token savings) by installing rtk filters that compress test/lint/typecheck/hassfest output before it reaches Claude. Use when long CLI output floods context.
effort: low
---

# Output Compression

Home Assistant toolchain commands (`pytest tests/components/<domain>/`,
`ruff check .`, `mypy homeassistant/components/<domain>/`,
`python3 -m script.hassfest`) emit verbose, repetitive output that consumes
context fast. This skill installs [rtk](https://github.com/rtk-ai/rtk) — a CLI
proxy that filters tool output **before it lands in the transcript**.

The filters short-circuit happy paths to a single line (`pytest: all pass`)
while preserving full failure blocks, diagnostics, and tracebacks. Net win:
5-15% per-session token reduction on test/lint/hassfest-heavy workflows.

## When to use

- **Long sessions** — `/ha:work` or `/ha:full` hitting context limits from
  pytest/ruff/mypy output
- **Debugging loops** — `/ha:investigate` retrying `mypy homeassistant/components/<domain>/`/`pytest`
  repeatedly
- **Type-check-heavy work** — `mypy homeassistant/components/<domain>/` output
  dominates the transcript

## Iron Laws

1. **NEVER strip critical signals** — test failures (`FAILED`, `= N failed`),
   mypy errors (`error:`, `Found N errors`), ruff violations (rule codes like
   `F401`), hassfest errors, and tracebacks with `file:line` MUST pass through
   unchanged
2. **Verify after install** — run `rtk verify` (or `rtk verify --filter pytest`) to
   confirm the bundled test fixtures pass before declaring success
3. **Never overwrite existing `.rtk/filters.toml`** — diff and merge instead

## Workflow

### Step 1: Detect rtk

```bash
which rtk && rtk --version
```

Read `${CLAUDE_SKILL_DIR}/references/install.md` if rtk is missing — covers
homebrew install + shell hook setup.

### Step 2: Seed `.rtk/filters.toml`

Reference filters live at `${CLAUDE_SKILL_DIR}/references/rtk-filters.toml`. Six
production-tested filters covering:

- **`pytest`** — short-circuits all-pass, preserves failure blocks + tracebacks
- **`ruff`** — collapses clean runs, preserves rule-tagged violation blocks
- **`mypy`** — drops progress noise, keeps errors + summary
- **`pip-install`** — collapses "already satisfied" dependency trees
- **`hassfest`** — strips validation progress, short-circuits clean runs
- **`prek`** — collapses all-pass hook runs, preserves failed-hook output

Run this if the project has no `.rtk/filters.toml` yet:

```bash
mkdir -p .rtk
cp "${CLAUDE_SKILL_DIR}/references/rtk-filters.toml" .rtk/filters.toml
```

Read both files if one already exists. Present a diff to the user. Merge only
the filters they don't already have.

### Step 3: Verify filters work

```bash
rtk verify                    # runs all embedded [[tests.*]] fixtures
rtk verify --filter pytest    # one filter only
```

Check that all report "passed". Flag and stop if any fail — usually means the
user has a custom rtk version with regex differences.

### Step 4: Confirm shell hook

Run `rtk init zsh` (or `rtk init bash`) to install the transparent rewrite hook
that turns `pytest X`/`ruff X`/`mypy X` into `rtk pytest X`/`rtk ruff X`/etc.
Re-running is safe (idempotent). Skip this step and the commands run unfiltered.

## Customization

Add custom regex patterns to `strip_lines_matching` for project-specific noise
sources (e.g., third-party libraries in `site-packages` spamming warnings or
deprecation notices). See the inline example in
`${CLAUDE_SKILL_DIR}/references/rtk-filters.toml` (the commented
`strip_lines_matching` example in `[filters.pytest]`).

## What this is NOT

- **Not a hook** — Claude Code's `PostToolUse` hooks fire after the tool result
  is in the transcript and cannot shrink it. rtk works at the subprocess layer
  (the only layer where transcript-shortening is possible).
- **Not project-analysis** — the bundled filter set is universal across HA
  integration and ha-frontend projects. No `manifest.json` inspection needed.
- **Not telemetry** — rtk has telemetry off by default (`enabled = false` in
  `config.toml`). Filters run locally, no data leaves the machine.

## References

- `${CLAUDE_SKILL_DIR}/references/rtk-filters.toml` — bundled filter set
- `${CLAUDE_SKILL_DIR}/references/install.md` — rtk install + shell hook setup
- [rtk on GitHub](https://github.com/rtk-ai/rtk)
