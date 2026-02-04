---
name: agent-history
description: Search and analyze Claude Code conversation history. Use when user asks about past conversations, previous solutions, what was discussed earlier, finding something from history, or analyzing usage patterns. Triggers include "what did we discuss", "find that conversation", "search history", "past sessions", "how much time", "token usage", "which tools".
allowed-tools: Bash, Read, Grep, Glob
---

# Agent History Skill

## Setup

```bash
mkdir -p ~/.claude/skills
cp agent-history SKILL.md ~/.claude/skills/
chmod +x ~/.claude/skills/agent-history
```

Once installed, Claude Code will automatically use this skill when you ask about past conversations, usage patterns, or want to search your history.

Browse, search, and analyze Claude Code conversation history using the `agent-history` CLI tool.

## When to Activate

- User asks about **past conversations**: "what did we discuss about X", "find that conversation where we..."
- User wants to **find previous solutions**: "how did we fix that error", "what approach did we use for..."
- User asks about **usage patterns**: "how much time did I spend", "which tools do I use most"
- User wants to **export or backup**: "export my conversations", "backup this project's history"
- User references **earlier sessions**: "yesterday we talked about", "last week's work on..."

## Available Commands

### List Sessions
```bash
# Current workspace
agent-history lss

# All sources (local + WSL + Windows + remotes)
agent-history lss --ah

# Filter by workspace pattern
agent-history lss myproject

# Filter by date
agent-history lss --since 2025-11-01
agent-history lss --since 2025-11-01 --until 2025-11-30
```

### Export to Markdown
```bash
# Export current workspace sessions
agent-history export

# Export specific workspace
agent-history export myproject

# Export with date filter
agent-history export --since 2025-11-24

# Export minimal (no metadata, cleaner for reading)
agent-history export --minimal

# Export to specific directory
agent-history export -o /tmp/history-export
```

### Usage Statistics
```bash
# Summary dashboard
agent-history stats

# Time tracking (work hours per day)
agent-history stats --time

# Tool usage breakdown
agent-history stats --tools

# Model usage
agent-history stats --models

# Daily trends
agent-history stats --by-day

# Per-workspace breakdown
agent-history stats --by-workspace
```

### List Workspaces
```bash
# All local workspaces
agent-history lsw

# Filter by pattern
agent-history lsw myproject
```

## Data Location

Claude Code stores conversations in `~/.claude/projects/` as JSONL files:
- Main sessions: `{uuid}.jsonl`
- Agent tasks: `agent-{id}.jsonl`

Workspace directories are encoded paths (e.g., `-home-user-myproject` = `/home/user/myproject`).

## Search Strategy (No Built-in Search Yet)

Since the tool doesn't have a search command, use this workflow:

### Method 1: Export + Grep (Recommended)
```bash
# Export recent sessions from ALL workspaces to temp directory
agent-history export --aw --since 2025-11-24 -o /tmp/history-search --minimal

# Search the exported markdown files
grep -r -i "search term" /tmp/history-search/
```

### Method 2: Direct JSONL Search
```bash
# Find the workspace directory
ls ~/.claude/projects/ | grep myproject

# Search within JSONL files (content is in message.content)
grep -i "search term" ~/.claude/projects/-home-user-myproject/*.jsonl
```

### Method 3: Multi-term Semantic Search

For questions like "what did we discuss about database connections":

1. Generate related search terms based on the topic
2. Run multiple grep searches
3. Synthesize the findings

Example for "database connections":
```bash
# Export recent history from all workspaces first
agent-history export --aw --since 2025-11-24 -o /tmp/search --minimal

# Search for related terms
grep -r -i -l "database" /tmp/search/
grep -r -i -l "connection" /tmp/search/
grep -r -i -l "postgres\|mysql\|sqlite\|mongo" /tmp/search/
grep -r -i -l "sql" /tmp/search/
grep -r -i -l "pool\|timeout" /tmp/search/
```

Then read the matching files to find relevant conversations.

## Common Workflows

### "What did we discuss about X last week?"

1. Export recent sessions from all workspaces:
   ```bash
   agent-history export --aw --since 2025-11-24 -o /tmp/history --minimal
   ```

2. Search for the topic and variations:
   ```bash
   grep -r -i -l "TOPIC" /tmp/history/
   grep -r -i -l "RELATED_TERM1" /tmp/history/
   grep -r -i -l "RELATED_TERM2" /tmp/history/
   ```

3. Read matching files to summarize findings

### "How did we fix that error?"

1. Search for error-related terms:
   ```bash
   agent-history export --aw --since 2025-11-01 -o /tmp/history --minimal
   grep -r -i "error\|exception\|failed" /tmp/history/ | head -50
   ```

2. Look for solution patterns:
   ```bash
   grep -r -i -A5 "fixed\|resolved\|solution" /tmp/history/
   ```

### "How much time have I spent on this project?"

```bash
agent-history stats --time
```

### "Which tools do I use most?"

```bash
agent-history stats --tools
```

### "Show me my activity this month"

```bash
agent-history stats --by-day --since 2025-11-01
```

### "Export everything for backup"

```bash
agent-history export --ah --aw -o ~/claude-backup/
```

## Tips

- **Use `--minimal` for reading**: Omits UUIDs and metadata, much cleaner
- **Use `--since` to narrow scope**: Faster searches on recent history
- **Check multiple workspaces**: Use `lsw` to see all available workspaces
- **Agent files exist**: Tasks spawn `agent-*.jsonl` files with sub-conversations
- **Incremental export**: Re-running export skips unchanged files

## Output Formats

Exported markdown includes:
- Message timestamps
- User/Assistant labels
- Tool use details (name, input, output)
- Token usage (in non-minimal mode)
- Navigation links between messages (in non-minimal mode)

## Limitations

- No built-in semantic search (use grep + Claude reasoning)
- No full-text index (searches scan files each time)
- Remote sources require SSH access configured
