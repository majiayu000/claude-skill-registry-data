---
name: amem
description: |
  Use the `amem` command to initialize, append, search, list, and review daily snapshots for local assistant memory (`.amem`). Use this when the user asks things like "log this with amem", "search memory", or "show today's context".
---

# amem CLI Skill

Run `amem` to operate local memory stored in `.amem`.

## Where to run

- Primary: run in the project directory the user is currently working on.
- Development fallback: use `/home/yuiseki/Workspaces/repos/amem` with `cargo run -q -- ...`.

## Pre-check

1. Check command availability with `amem --help`.
2. If not available, use this fallback:

```bash
cd /home/yuiseki/Workspaces/repos/amem
cargo run -q -- --help
```

## Core commands

### 1. Initialize

```bash
amem init
```

- Creates the `.amem` scaffold.
- Idempotent and non-destructive for existing files.

### 2. Show active memory directory

```bash
amem which
amem which --json
```

### 3. Fast append

```bash
amem keep "Went for a walk in Tokyo"
amem keep "Meeting note" --kind inbox
amem keep "Retrospective note" --date 2026-02-21 --source assistant
```

### 4. Search

```bash
amem search Tokyo --top-k 5
amem remember Tokyo --top-k 5
amem search "tomorrow plan" --json
```

### 5. List entries

```bash
amem list
amem ls --kind activity --limit 20
amem list --path "activity/**" --date 2026-02-21
```

### 6. Today snapshot

```bash
amem today
amem today --date 2026-02-21
amem today --json
```

### 7. Structured capture (explicit)

```bash
amem capture --kind activity --text "Meeting in Shibuya"
amem capture --kind inbox --text "Article to read later"
```

### 8. Task context assembly

```bash
amem context --task "tomorrow travel plan"
amem context --task "weekly review" --json
```

### 9. Rebuild/search index

```bash
amem index
amem index --rebuild
```

### 10. Watch mode

```bash
amem watch
```

### 11. Codex bridge

```bash
amem codex
amem codex --prompt "organize today's priority tasks"
amem codex --resume-only
```

### 12. Gemini bridge

```bash
amem gemini
amem gemini --prompt "organize today's priority tasks"
amem gemini --resume-only
```

### 13. Claude bridge

```bash
amem claude
amem claude --prompt "organize today's priority tasks"
amem claude --resume-only
```

### 14. Copilot bridge

```bash
amem copilot
amem copilot --prompt "organize today's priority tasks"
amem copilot --resume-only
```

## Global options

- `--memory-dir <path>`: explicitly set the memory root (instead of default `~/.amem`).
- `--json`: prefer machine-readable JSON output.

## Recommended workflow

1. First run: `amem init`
2. Daily logging: `amem keep "..."`
3. Pre-work check: `amem today`
4. Search as needed: `amem search ...` (or `amem remember ...`)
5. Periodic refresh: `amem index`

## Troubleshooting

- `amem: command not found`
  - Use `cargo run -q -- ...` in `/home/yuiseki/Workspaces/repos/amem`.
- Search results are sparse
  - Run `amem index --rebuild`.
- Need a different memory root
  - Add `--memory-dir <abs/path/to/.amem>`.
