---
name: session-logs
description: Discover and analyze Claude Code session logs from ~/.claude/projects, including finding the current session and extracting tool calls, user messages, and conversation history
---

# Claude Code Session Logs Skill

This skill helps discover and analyze Claude Code session logs stored in `~/.claude/projects/`. Use this when you need to:

- Find the current session log
- Extract conversation history for analysis
- Verify what tools were used in a session
- Mine session data for followup suggestions
- Debug session state or tool execution

## Finding the Current Session

Sessions are stored per-project in `~/.claude/projects/` with directory names based on the working directory path.

**Project directory naming:**

- `/code/gitlab.com/agentydragon/ducktape` → `~/.claude/projects/-code-gitlab-com-agentydragon-ducktape/`
- All `/` become `-`, path is prefixed with `-`

**Important:** The current `pwd` may differ from the session's original `cwd` if directories were changed during the session. The helper script accounts for this by:

1. Searching recent sessions from ALL projects (last hour)
2. Scoring by **recency first** (most important signal)
3. Using git branch and cwd as secondary signals

**Discovery script:**

```bash
# Find current project directory
PROJECT_DIR=$(pwd | sed 's|/|-|g')
SESSION_DIR=~/.claude/projects/$PROJECT_DIR

# Get 5 recently modified session files
# NOTE: Current session may not be #1 (parallel instances, background tasks)
find $SESSION_DIR -type f -name "*.jsonl" -printf "%T@ %p\n" 2>/dev/null | \
  sort -rn | head -5 | cut -d' ' -f2-

# Check each candidate to identify current session
# Match by: recent timestamp, matching cwd, matching git branch
for session in $(find $SESSION_DIR -type f -name "*.jsonl" -printf "%T@ %p\n" 2>/dev/null | sort -rn | head -5 | cut -d' ' -f2-); do
  echo "=== $session ==="
  tail -1 "$session" | jq -r '{timestamp, cwd, gitBranch, sessionId}'
done
```

Use the helper script for convenience:

```bash
~/.claude/skills/session-logs/find-current-session.sh
```

## Session Log Format

**Structure:** JSONL (one JSON object per line)

**Key fields in each entry:**

- `type`: Entry type (`"user"`, `"assistant"`, `"tool_use"`, `"tool_result"`, etc.)
- `message`: Contains the actual content (nested structure)
- `timestamp`: ISO 8601 timestamp (e.g., `"2025-12-01T19:35:59.995Z"`)
- `sessionId`: UUID of the session
- `cwd`: Working directory at time of entry
- `gitBranch`: Current git branch

**Tool use entries:**

```json
{
  "type": "assistant",
  "message": {
    "content": [
      {
        "type": "tool_use",
        "id": "toolu_...",
        "name": "Edit",
        "input": {
          "file_path": "/path/to/file.py",
          "old_string": "...",
          "new_string": "..."
        }
      }
    ]
  },
  "timestamp": "2025-12-01T19:32:48.590Z",
  "sessionId": "9aea9a46-9010-4876-ac8c-27b08cc9cee1"
}
```

**User message entries:**

```json
{
  "type": "user",
  "message": {
    "content": [
      {
        "type": "text",
        "text": "User's message here"
      }
    ]
  },
  "timestamp": "2025-12-01T19:25:00.000Z"
}
```

## Common Queries

### Show recent Edit operations

```bash
CURRENT_SESSION=$(~/.claude/skills/session-logs/find-current-session.sh | head -1)

grep '"type":"tool_use"' "$CURRENT_SESSION" | \
  jq -r 'select(.message.content[0].name == "Edit") |
    "\(.timestamp): Edit \(.message.content[0].input.file_path)"'
```

### Show recent Bash commands

```bash
grep '"type":"tool_use"' "$CURRENT_SESSION" | \
  jq -r 'select(.message.content[0].name == "Bash") |
    "\(.message.content[0].input.description): \(.message.content[0].input.command[0:80])"'
```

### Extract all tool calls

```bash
grep '"type":"tool_use"' "$CURRENT_SESSION" | \
  jq -r '.message.content[0].name' | sort | uniq -c | sort -rn
```

### Get user messages

```bash
grep '"type":"user"' "$CURRENT_SESSION" | \
  jq -r '.message.content[0].text' | head -20
```

### Find files modified in session

```bash
grep '"type":"tool_use"' "$CURRENT_SESSION" | \
  jq -r 'select(.message.content[0].name == "Edit" or .message.content[0].name == "Write") |
    .message.content[0].input.file_path' | sort -u
```

### Session statistics

```bash
echo "Session: $CURRENT_SESSION"
echo "Session ID: $(tail -1 "$CURRENT_SESSION" | jq -r .sessionId)"
echo "Total entries: $(wc -l < "$CURRENT_SESSION")"
echo "Tool uses: $(grep -c '"type":"tool_use"' "$CURRENT_SESSION")"
echo "User messages: $(grep -c '"type":"user"' "$CURRENT_SESSION")"
```

## Use Cases

**For /followups command:**

- Verify files modified in session still exist on disk
- Extract conversation TODOs and incomplete actions
- Find all Edit/Write operations to check against git status

**For debugging:**

- Check what Bash commands were executed
- Verify tool parameters that were used
- Trace conversation flow and reasoning

**For delegation:**

- Provide session logs to subagents for analysis
- Extract specific conversation segments
- Mine historical context for decision-making

## Notes

- Session logs update in real-time as the session progresses
- Multiple sessions can be active simultaneously (parallel instances)
- Agent subprocesses create separate session files (prefixed with `agent-`)
- Session files persist across Claude Code restarts
- Very large sessions may have truncated context but full tool history
