---
name: ctx
description: Extract a small, high-signal context packet around ripgrep matches (bounded by hits/files/output budget) for fast LLM consumption.
---

# ctx

## Use this skill when
- You need to show the agent a *small* amount of source context around a pattern/symbol without pasting whole files.
- The repository is large and token budget matters.

## Command

```sh
ctx 'PATTERN' .
ctx 'literal string' . -F
ctx 'PATTERN' path/to/file.py
ctx 'PATTERN' . --no-scope
ctx 'PATTERN' . --prefer torch --prefer aten
ctx 'PATTERN' . --json

# (fallback if wrappers are not on PATH)
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
python3 "$CODEX_HOME/skills/ctx/scripts/ctx.py" 'PATTERN' . --no-scope -C 3 --max-hits 60 --max-files 20 --max-output-lines 500
```

## Notes
- Uses `rg --vimgrep` for fast match discovery and can stop early once `--max-hits` is reached.
- Reads each matched file at most once, merges overlapping context windows, then prints a bounded packet.
