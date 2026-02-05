---
name: rg_history
description: Search your conversation history using ripgrep. Use when you need to find previous messages, file edits, tool calls, or decisions from earlier in the session.
---

# rg_history

Search your session history with ripgrep.

## CRITICAL: Search Strategy

**Each event is one long JSON line. Full output will overwhelm you. Always start broad with limited output, then narrow in.**

### The Pattern

```bash
# 1. COUNT first - how many matches?
rg -c 'search_term' session.jsonl

# 2. SNIPPETS - get context around matches (not full lines)
rg -o '.{0,60}search_term.{0,60}' session.jsonl | head -20

# 3. NARROW - pipe to filter further
rg -o '.{0,60}search_term.{0,60}' session.jsonl | rg 'new_string'

# 4. FULL CONTEXT - only when you know what you want
rg '"name":"Edit".*search_term' session.jsonl -M 500
```

**Never run raw `rg 'pattern' file.jsonl` - you'll get walls of JSON.**

Always use one of:
- `-c` to count matches
- `-o '.{0,60}pattern.{0,60}'` for snippets
- `-M 200` to truncate lines
- `| head -20` to limit results

---

## Find Your Session Files

Run the helper script:
```bash
scripts/list-sessions.sh /path/to/project  # defaults to cwd
```

Or construct manually:
```
~/.claude/projects/{encoded_project_path}/{session_id}.jsonl
```
Where `encoded_project_path` = project path with `/` replaced by `-`.

### File Structure

```
~/.claude/projects/-Users-ramos-my-project/
├── abc123-def4-5678-....jsonl    # Main session (UUID format)
├── agent-a1b2c3d.jsonl           # Sub-agent spawned by Task tool
└── ...
```

- **Main session**: Full UUID, your conversation
- **Agent files**: `agent-{7-char-id}.jsonl`, from Task tool
- Agent IDs appear in results as `"agentId": "a1b2c3d"`

---

## JSONL Structure Reference

Each line is one JSON object. Key fields:

**Message types:**
- `"type":"user"` + `"userType":"external"` = actual human input
- `"type":"assistant"` = Claude's responses
- `"type":"tool_result"` = tool output

**Tool calls (in assistant messages):**
- `"name":"Edit"` → `"input":{"file_path":"...", "old_string":"...", "new_string":"..."}`
- `"name":"Write"` → `"input":{"file_path":"...", "content":"..."}`
- `"name":"Bash"` → `"input":{"command":"..."}`
- `"name":"Task"` → `"input":{"prompt":"...", "subagent_type":"..."}`

**Content blocks:**
- `"type":"text"` - message text
- `"type":"thinking"` - Claude's reasoning
- `"type":"tool_use"` - tool invocation

**Other fields:**
- `"timestamp":"2025-12-20T..."` - when it happened
- `"agentId":"..."` - links to agent file
- `"isCompactSummary":true` - compacted context

---

## Example Search Patterns

Remember: always use snippets or limit output!

```bash
# Find human messages (not tool results)
rg -o '.{0,40}"userType":"external".{0,40}' session.jsonl | head -10

# Find file edits
rg -c '"name":"Edit"' session.jsonl  # count first
rg -o '.{0,50}"name":"Edit".{0,50}' session.jsonl | head -10

# Find edits to specific file
rg -o '.{0,30}auth.{0,30}' session.jsonl | rg 'file_path'

# Find commands that were run
rg -o '.{0,80}"command":".{0,80}' session.jsonl | head -10

# Find code in file writes
rg -o '.{0,60}function.{0,60}' session.jsonl | rg 'new_string\|content'
```

---

## Quick Reference

| Goal | Command |
|------|---------|
| Count matches | `rg -c 'pattern' file` |
| Snippets | `rg -o '.{0,60}pattern.{0,60}' file` |
| Limit output | `\| head -20` |
| Truncate lines | `-M 200` |
| Case insensitive | `-i` |
| Chain filters | `rg 'a' \| rg 'b'` |
