---
name: persisting-bigpicture-learnings
description: Persist bigpicture synthesis as dated snapshots in a learnings hub. Maintains latest pointer + append-only archive for cross-session compound learning.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Glob
  argument-hint: "[input-path] [hub-path]"
  context: inline
  stability: development
---

# Persist Bigpicture to Learnings Hub

**Target**: $ARGUMENTS

Persists the output of `/synthesizing-cc-bigpicture` as a dated snapshot in a
learnings hub. Maintains a `latest.md` pointer (always current) and an
append-only archive for compound cross-session learning.

## Arguments

| Position | Name | Required | Default | Description |
|----------|------|----------|---------|-------------|
| 1 | `input-path` | no | `bigpicture.md` | Path to bigpicture synthesis output |
| 2 | `hub-path` | no | `docs/learnings/cc-bigpicture/` | Directory for learnings hub |

**Examples:**

```text
/persisting-bigpicture-learnings
/persisting-bigpicture-learnings ~/.claude/bigpicture.md
/persisting-bigpicture-learnings bigpicture.md docs/learnings/cc-bigpicture/
```

## Output Structure

```text
docs/learnings/cc-bigpicture/
├── latest.md          # Always the most recent synthesis
└── archive/
    ├── 2026-04-01.md
    ├── 2026-04-03.md
    └── 2026-04-06.md  # Today's snapshot
```

## Workflow

1. **Parse arguments** — Apply defaults per Arguments table.

2. **Read input** — Read `input-path`. If the file does not exist, report error
   and stop.

3. **Create hub directory** — Create `hub-path` and `hub-path/archive/` if
   absent.

4. **Write latest** — Write full synthesis content to `hub-path/latest.md`.
   Always overwrite — this is the current-state pointer.

5. **Write archive snapshot** — Determine today's date (`YYYY-MM-DD`).
   - If `hub-path/archive/YYYY-MM-DD.md` does **not** exist, create it with
     the synthesis content.
   - If it **does** exist, append a `---` separator followed by the new
     synthesis content. This preserves all snapshots from the same day.

6. **Report** — Confirm paths written and archive entry count for today.

## Integration

Runs after `/synthesizing-cc-bigpicture`. Chain the two skills:

```text
/synthesizing-cc-bigpicture all 7d bigpicture.md
/persisting-bigpicture-learnings bigpicture.md docs/learnings/cc-bigpicture/
```

## Compound Learning

Other skills can read `hub-path/latest.md` for prior synthesis context:

- **synthesizing-cc-bigpicture** — Load previous synthesis for incremental
  update instead of cold start.
- **ralph / PRD skills** — Reference latest bigpicture for strategic context.
- **compacting-context** — Include bigpicture summary when compacting at phase
  boundaries.

## Quality Check

- `latest.md` content matches the most recent archive entry
- Archive files are append-only — never overwrite, never delete
- Hub path directories created automatically
- Input file validated before any writes
