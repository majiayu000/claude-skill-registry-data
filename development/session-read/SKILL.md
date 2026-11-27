---
name: session-read
description: Read and summarize a Claude Code session's transcript by session ID. Equivalent to OpenCode's session_read.
user-invocable: true
argument-hint: "<session-id> [--last N] [--tools] [--full]"
---

# Session Read

Read a Claude Code session's transcript by session ID or partial ID. Parses the JSONL transcript files and presents a readable summary.

## Step 1 — Locate the transcript file

### By session ID (search project directories first, then global transcripts)

```bash
# Search project-scoped transcripts
find ~/.claude/projects -name "${SESSION_ID}*.jsonl" -not -path "*/subagents/*" -not -path "*/tool-results/*" 2>/dev/null

# Search global transcripts
find ~/.claude/transcripts -name "*${SESSION_ID}*.jsonl" 2>/dev/null
```

Partial IDs work — match the first N characters. If multiple matches, list them and ask which one.

## Step 2 — Read the transcript

### Recent messages (default: last 30 turns)

```bash
jq -r 'select(.message?) | select(.message.role?) | [
  (.timestamp // 0 | if . > 1000000000000 then (. / 1000 | strftime("%H:%M:%S")) elif . > 1000000000 then (. | strftime("%H:%M:%S")) else "?" end),
  .message.role,
  (if .message.content | type == "array" then
    [.message.content[] | if .type == "text" then .text[0:200] elif .type == "tool_use" then ("tool:" + .name) elif .type == "tool_result" then "result" else .type end] | join(" | ")
  elif .message.content | type == "string" then
    .message.content[0:200]
  else
    (.message.content | tostring | .[0:200])
  end)
] | @tsv' "$FILE" 2>/dev/null | tail -${LAST:-30}
```

### Tool calls only

```bash
jq -r 'select(.message?) | select(.message.content | type == "array") | .message.content[] | select(.type == "tool_use") | [.name, (.input | tostring | .[0:100])] | @tsv' "$FILE" 2>/dev/null | tail -${LAST:-30}
```

### Session metadata

```bash
head -5 "$FILE" | jq -r '[.sessionId, .cwd, .version, .gitBranch // "none"] | @tsv' 2>/dev/null | head -1
```

### Message count and date range

```bash
echo "Messages: $(wc -l < "$FILE")"
echo "First: $(head -1 "$FILE" | jq -r '.timestamp // 0 | if . > 1000000000000 then (. / 1000 | strftime("%Y-%m-%d %H:%M")) elif . > 0 then (. | strftime("%Y-%m-%d %H:%M")) else "unknown" end' 2>/dev/null)"
echo "Last: $(tail -1 "$FILE" | jq -r '.timestamp // 0 | if . > 1000000000000 then (. / 1000 | strftime("%Y-%m-%d %H:%M")) elif . > 0 then (. | strftime("%Y-%m-%d %H:%M")) else "unknown" end' 2>/dev/null)"
```

## Step 3 — Present results

Format the output as a readable conversation:
- **User** messages: show the prompt text
- **Assistant** messages: show text content, list tool calls by name
- **Timestamps**: show time for each turn
- **Truncate** long messages to keep output manageable

## Arguments

Parse `$ARGUMENTS` for:
- First positional argument: session ID or partial ID (required)
- `--last N`: show last N turns (default 30)
- `--tools`: show only tool calls
- `--full`: show complete message content (no truncation)
- `--summary`: generate a one-paragraph summary of what the session did

## Subagent transcripts

If the session has subagents, they're stored in `<session-uuid>/subagents/`. List them:

```bash
ls ~/.claude/projects/*/${SESSION_ID}*/subagents/*.meta.json 2>/dev/null | while read meta; do
  jq -r '[.agentType, .description] | @tsv' "$meta"
done
```
