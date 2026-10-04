---
name: agent-trace-debugger
description: Parse .trace.json files and correlate with backend events and tool calls. Use when debugging agent behavior, investigating tool call patterns, or validating concurrency limits.
---

# Agent Trace Debugger

Parse and analyze LibrAgent agent session trace files (`.trace.json`).

## Trace File Location

Trace files are typically stored in:

- `~/.libragent/traces/<session_id>.trace.json`
- Session-specific directories under the app data folder

## Analysis Workflow

### 1. Load Trace File

```typescript
import { readFileSync } from 'fs';
const trace = JSON.parse(readFileSync('session.trace.json', 'utf-8'));
```

### 2. Extract Tool Call Sequence

```typescript
const toolCalls = trace.messages
  .filter((m) => m.role === 'assistant' && m.tool_calls)
  .flatMap((m) => m.tool_calls);
```

### 3. Correlate with Backend Events

Match trace tool calls with `agent:event` payloads:

- `agent:thinking` - LLM reasoning phase
- `agent:tool_start` - Tool execution start
- `agent:tool_end` - Tool execution complete
- `agent:error` - Error during execution

### 4. Identify Workflow Phases

LibrAgent uses Think-Act-Observe loop:

- **Think**: LLM generates reasoning and tool calls
- **Act**: Backend executes tools via `MCPServiceProxy`
- **Observe**: Backend adds results to conversation, loop continues

### 5. Detect Issues

- Failed tool calls without retry
- Long-running tool executions
- Missing tool results in conversation
- Cross-session state leakage (check session IDs)

## Key Patterns to Look For

```json
{
  "session_id": "uuid-here",
  "messages": [
    {
      "role": "user",
      "content": "Task description"
    },
    {
      "role": "assistant",
      "content": "Reasoning...",
      "tool_calls": [
        {
          "id": "call_123",
          "function": {
            "name": "planning_create_task",
            "arguments": "{\"title\": \"Task\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "tool_call_id": "call_123",
      "content": "Task created"
    }
  ]
}
```

## Integration with Other Tools

- `extract-log-debug` skill: Extract matching log entries for the same session
- `trace-analyzer` skill: Deep analysis of trace file structure
- `sqlite-analyzer` skill: Verify database state matches trace expectations
