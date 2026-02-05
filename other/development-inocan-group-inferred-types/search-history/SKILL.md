---
name: search-history
description: Search Claude conversation history from JSONL files. Use when looking for previous discussions, past decisions, code solutions, or context from earlier conversations.
allowed-tools: Bash, Read
---

# Conversation History Search

Search through Claude Code conversation history to find relevant past discussions.

## When to Use

- Finding previous discussions about a topic
- Recalling past decisions or solutions
- Getting context from earlier conversations
- Looking up how something was implemented before

## How to Search

Run the search script from the services directory:

```bash
cd ~/.claude/services
python conversation-search.py "search term"
```

## Search Options

| Option | Description |
|--------|-------------|
| `--list-sessions`, `-l` | List all sessions with metadata |
| `--session ID`, `-s` | Filter to specific session (partial match) |
| `--context N`, `-c` | Show N messages before/after (default: 3) |
| `--max N`, `-m` | Maximum results (default: 20) |
| `--verbose`, `-v` | Show context messages |
| `--full`, `-f` | Show full message content |

## Examples

```bash
# List all available sessions
python conversation-search.py --list-sessions

# Basic search
python conversation-search.py "bulk upload"

# Regex search
python conversation-search.py "context.*percent|usage.*%"

# Search specific session with full output
python conversation-search.py "statusline" --session 6cabef43 --full

# Get more context around matches
python conversation-search.py "error" --context 5 --verbose --max 3
```

## Output Modes

1. **Default**: Preview snippet (50 chars before, 100 after match)
2. **Verbose** (`-v`): Adds surrounding message context
3. **Full** (`-f`): Complete message content

## Token Efficiency

The search runs externally, so searching costs 0 tokens. Only the returned results consume context.
