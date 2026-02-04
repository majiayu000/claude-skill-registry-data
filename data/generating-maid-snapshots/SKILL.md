---
name: generating-maid-snapshots
description: Generates MAID snapshot JSON for agent inspection visualization. Use when asked to create snapshot data, export agent traces, or generate JSON for the MAID inspection panel.
---

# MAID Snapshot Generator

Generate a snapshot JSON that can be imported by MAID for visualization in the InspectionPanel and ContextViewer.

## Critical Output Rules

1. **Create a file** named `maid-snapshot-<id>.json` in the current working directory, where `<id>` is a unique identifier (use epoch milliseconds from the command below)
2. Write ONLY valid JSON to the file (no markdown fences, no explanations)
3. Strict JSON: no trailing commas, no NaN/Infinity, no comments
4. Prefer OMISSION over fabrication:
   - Do NOT guess values
   - If a field is unknown, either omit it or set to null only when explicitly allowed
5. After creating the file, confirm with the file path

## Timestamps - CRITICAL

**BEFORE generating the snapshot, run these commands:**

```bash
# Get current epoch milliseconds (for exportedAt and file naming)
date +%s000

# Get current ISO 8601 UTC timestamp (for exportedAt)
date -u +"%Y-%m-%dT%H:%M:%S.000Z"
```

### Export Timestamp (`exportedAt`)
Use the ISO command above for the current time.

### Invocation Timestamps (`events[].ts`)

**Priority 1 — Extract from Amp thread data:**

Amp stores thread data at `~/.ampcode/threads/`. Each thread is a directory named by thread ID (e.g., `T-019b6f89-...`).

```bash
# List recent Amp threads (sorted by modification time)
ls -lt ~/.ampcode/threads/ | head -20

# Get mtime of thread directory in epoch ms (macOS)
stat -f %m ~/.ampcode/threads/<thread-id> | awk '{print $1 * 1000}'

# Check for any JSON files in a thread
ls ~/.ampcode/threads/<thread-id>/
```

If files were touched during the session, use file mtimes:
```bash
# Get mtime of a file in epoch ms (macOS)
stat -f %m "<file>" | awk '{print $1 * 1000}'

# Get mtime of a file in epoch ms (Linux)
stat -c %Y "<file>" | awk '{print $1 * 1000}'
```

**Priority 2 — Estimate from typical durations:**
If no source timestamps available, estimate based on realistic operation times:
- User message → Assistant thinking: +500-2000ms
- Tool call start: +100-500ms after assistant message
- File read operation: +50-200ms
- File write/edit operation: +100-500ms
- Bash command: +200-5000ms (depends on command)
- Web search/fetch: +1000-3000ms
- Assistant final response: +500-2000ms after last tool

**Rules:**
- `events[].ts` MUST be monotonic non-decreasing
- Use REAL timestamps when available, estimates only as fallback
- When estimating, ask user about approximate session duration if unclear

## Required Root Shape

```json
{
  "version": "1.0",
  "exportedAt": "<ISO timestamp UTC>",
  "model": "<model id or 'unknown'>",
  "tokenUsage": {
    "totalTokens": 0
  },
  "tools": [],
  "context": [],
  "events": []
}
```

**IMPORTANT:** `tokenUsage.totalTokens` is REQUIRED and must be a number (use `0` if unknown).

Optional tokenUsage fields (include only if known): `promptTokens`, `modelOutputTokens`, `modelReasoningTokens`, `contextLimit`, `remainingTokens`

## Model Name - REQUIRED

**Extract the model name from these sources (in priority order):**

1. **System prompt**: Look for model identifier in the agent's system prompt (e.g., "You are Claude", "powered by GPT-4")
2. **Amp thread URL**: The thread URL or thread metadata may reference the model
3. **Ask the user**: If not found, ask "Which model was used for this session?"

Common model names: `claude-sonnet-4-20250514`, `claude-3-5-sonnet`, `gpt-4o`, `gpt-4-turbo`, `o1`, `o3`

Do NOT use `"unknown"` without first attempting to extract or ask.

## Tools Array - REQUIRED

**Extract tools from these sources:**

1. **Tool calls in the conversation**: Look at every tool/function call made during the session. Each unique tool name should be in the tools array.
2. **System prompt**: The system prompt often lists available tools with descriptions.
3. **Amp's standard tools**: If this is an Amp session, common tools include:
   - `Read` - Read files or directories
   - `Grep` - Search for patterns in files  
   - `glob` - Find files by pattern
   - `edit_file` - Edit existing files
   - `create_file` - Create new files
   - `Bash` - Execute shell commands
   - `finder` - Semantic code search
   - `web_search` - Search the web
   - `read_web_page` - Read web page content
   - `Task` - Spawn sub-agents
   - `oracle` - Consult reasoning model
   - `mermaid` - Render diagrams
   - `todo_write` / `todo_read` - Task management

**For each tool used in the conversation, add an entry:**

```json
{
  "type": "function",
  "function": {
    "name": "<tool name>",
    "description": "<brief description of what it does>",
    "parameters": {
      "type": "object",
      "properties": {},
      "required": []
    }
  }
}
```

**IMPORTANT:** Populate `tools` with at least the tools that appear in tool_calls. Do NOT leave `tools: []` if tool calls exist in the conversation.

## Context Array (Chat Transcript)

Chronological list of messages. The first message MUST be the system prompt if available.

**System prompt (REQUIRED as first message if available):**
```json
{ "role": "system", "content": "<full system prompt text>" }
```

The system prompt is the initial instruction set given to the agent. It typically includes:
- Agent identity and capabilities
- Available tools and their usage guidelines
- Behavioral rules and constraints
- Response formatting instructions

**If the system prompt is not explicitly provided:** Extract it from any visible agent configuration/logs like CLAUDE.md or AGENTS.md. If no system prompt is found, use the default system prompt provided by the agent.

**User/Assistant message:**
```json
{ "role": "user" | "assistant", "content": "<string>" }
```

**Assistant with tool calls:**
```json
{
  "role": "assistant",
  "content": "<string>",
  "tool_calls": [
    {
      "id": "<string>",
      "type": "function",
      "function": {
        "name": "<tool name>",
        "arguments": "<JSON string>"
      }
    }
  ]
}
```

**Note:** Do NOT include `index` field in tool_calls.

**Tool result:**
```json
{
  "role": "tool",
  "tool_call_id": "<matches tool call id>",
  "content": "<string>"
}
```

Rules:
- Keep exact order: assistant(tool_calls) → tool(result) → assistant(final)
- Tool arguments MUST be a JSON STRING, not an object

## Events Array (Inspection Timeline)

Each event:

```json
{
  "ts": 1767103680000,
  "data": "<one-line summary>",
  "inspectionEvent": {
    "message": "<can be long>",
    "invocationId": "<uuid for grouping>",
    "children": [
      { "label": "<label>", "data": "<string>" }
    ]
  }
}
```

**IMPORTANT:** `ts` MUST be a NUMBER (epoch milliseconds), NOT a string.

### Allowed Labels

- `__INVOCATION_START__`
- `__INVOCATION_END__`
- `Content`
- `Reasoning`
- `Tool Calls`
- `Timing`
- `Token Usage`
- `Error`
- `Custom`

### Recommended Event Pattern Per Invocation

1. **Start:** `children: [{ "label": "__INVOCATION_START__", "data": "" }]`
2. **Tool execution:** Include `Reasoning` (short), `Tool Calls` (stringified JSON)
3. **Tool completed:** Include `Timing`, `Tool Calls` with results, `Token Usage`
4. **Final message:** Include `Content`, optionally `Reasoning`
5. **End:** `children: [{ "label": "__INVOCATION_END__", "data": "" }]`

## Important

- Do NOT include private chain-of-thought
- If including "Reasoning", keep it short and high-level
- Omit unknown data rather than guessing
- Output ONLY the JSON object—no markdown, no extra text
