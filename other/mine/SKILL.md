---
name: mine
description: "Mine Claude Code session data for analytics — token usage, tool rankings, skill invocations, session search, and prompt history. Use when asked about session stats, token costs, tool frequency, skill usage patterns, or finding past sessions by prompt text."
---

# mine

Mine `~/.claude/projects/` session JSONL and index files for analytics and forensics.

## Trigger Cues
- Explicit `/mine` invocation
- "How many tokens did I use?" / "What are my most-used tools?"
- "Find the session where I discussed X"
- "Which skills do I use most?"
- "Show me token usage by project/day"

## Data Model
- Sessions: `~/.claude/projects/<project>/<session-id>.jsonl`
- Index: `~/.claude/projects/<project>/sessions-index.json`
- Memory: `~/.claude/projects/<project>/memory/`

## Scripts

All scripts are in `~/.claude/skills/mine/scripts/`. Run them via Bash.

### 1. Search sessions
Find sessions by prompt text, project, or date range.
```bash
bash ~/.claude/skills/mine/scripts/mine-sessions.sh --prompt "auth" --limit 10
bash ~/.claude/skills/mine/scripts/mine-sessions.sh --project dotfiles --since 2026-03-01
```

### 2. View session prompts
Extract user/assistant messages from a session.
```bash
bash ~/.claude/skills/mine/scripts/mine-prompts.sh --session <path-to-jsonl>
bash ~/.claude/skills/mine/scripts/mine-prompts.sh --session <path> --roles user --limit 20
```

### 3. Rank tool usage
See which tools are called most across sessions.
```bash
bash ~/.claude/skills/mine/scripts/mine-tools.sh --limit 20
bash ~/.claude/skills/mine/scripts/mine-tools.sh --project ka-ching --since 2026-03-01
```

### 4. Token usage
Summarize token consumption.
```bash
bash ~/.claude/skills/mine/scripts/mine-tokens.sh --by project --limit 10
bash ~/.claude/skills/mine/scripts/mine-tokens.sh --by day --since 2026-03-20
bash ~/.claude/skills/mine/scripts/mine-tokens.sh --by session --project dotfiles
```

### 5. Rank skill invocations
See which skills are invoked most (via Skill tool_use blocks).
```bash
bash ~/.claude/skills/mine/scripts/mine-skills.sh --limit 20
bash ~/.claude/skills/mine/scripts/mine-skills.sh --since 2026-03-01
```

## Workflow
1. Start with session search or index queries to find relevant sessions.
2. Drill into a specific session with `mine-prompts.sh`.
3. Use `mine-tools.sh`, `mine-tokens.sh`, `mine-skills.sh` for aggregate analytics.
