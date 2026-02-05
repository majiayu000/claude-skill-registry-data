---
name: claude-session-analysis
description: Analyze Claude Code session files. Find current session ID, view timeline (tl), or search past chats.
---

# Claude Session Analysis

This is `{SKILL_DIR}/SKILL.md`. Scripts: `{SKILL_DIR}/scripts/`

| Script | Description |
|--------|-------------|
| `current-session.sh [dir] [sec]` | **My session ID** |
| `sessions.sh [--full] [-g kw] [-mmin 1440] [-n 10]` | Search sessions by keyword/time |
| `resolve-session.sh <id>` | Session ID → file path |
| `timeline.sh [-t <types>] [-w <width>] <id> [range]` | Timeline (default: all, 55 chars; range: `..m`, `m..`, `m..m`) |
| `get-by-marker.sh [--raw] [-A n] [-B n] [-C n] <id> <marker>` | Entry details (with context) |
| `file-ops.sh <id>` | Read/Write operations |
| `file-diff.sh <id> <hash> <v1> [v2]` | Diff versions (v2 omitted: vs current) |
| `summaries.sh <id>` | Session title history |

## Timeline Markers

Format: `{hash}-{type}` (e.g., `7e2451-U`) with `[+N]` for truncated chars

Types (all by default, filter with `-t`):
- **U**: User (includes /commands) | **T**: Think | **F**: File (Write: `{hash}@v{n}`)
- **W**: Web (no truncate) | **B**: Bash | **G**: Grep/Glob
- **A**: Agent | **S**: Skill | **Q**: Question | **D**: toDo

## Paths

- Sessions: `~/.claude/projects/{project-path}/{session-id}.jsonl`
- Backups: `~/.claude/file-history/{session-id}/{hash}@v{version}`

## Usage Tips

1. **Start with full timeline** (default width is enough for overview)
2. **Dive deeper** with `get-by-marker.sh` or `-w` for specific entries

⚠️ **Sandbox**: Pipes (`|`) don't work. Use `dangerouslyDisableSandbox: true` when piping output.
