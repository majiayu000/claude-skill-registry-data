---
name: session-list
description: List Claude Code sessions across all projects with metadata (names, prompts, dates, message counts). Equivalent to OpenCode's session_list.
user-invocable: true
argument-hint: "[project-filter] [--active] [--limit N]"
---

# Session List

List Claude Code sessions across all projects.

Run the helper script:

```bash
bash "${CLAUDE_SKILL_DIR}/session-list.sh" $ARGUMENTS
```

## Data sources

- **Active sessions** (`~/.claude/sessions/*.json`) — have PID, name, CWD
- **Session index** (`~/.claude/projects/*/sessions-index.json`) — have firstPrompt, messageCount, dates, branch
- **Global transcripts** (`~/.claude/transcripts/ses_*.jsonl`) — OpenCode-originated sessions and recent Claude Code sessions

## Notes

- Session names only exist for currently active sessions (set via `/rename` or `--name`)
- Historical sessions show their first prompt instead of a name
- Use session IDs from this output with `/session-read` and `/session-search`
- `--active` shows only running sessions
- `--limit N` controls max results per section (default 20)
