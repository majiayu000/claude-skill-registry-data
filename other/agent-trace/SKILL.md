---
name: agent-trace
description: Debug agent execution with tracing — analyze traces, tool calls, durations, errors, and performance metrics. Use when investigating agent behavior.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Agent, mcp__supabase__execute_sql, mcp__openai-docs__search_openai_docs
---

Debug agent execution: $ARGUMENTS

## Before Starting

1. Read the tracing infrastructure:
   - `src/agents/shared/agent-tracer.ts` — `AgentTracer` class, event recording
   - `src/agents/shared/hooks.ts` — lifecycle hooks (onStart, onToolCall, onToolComplete, onComplete, onError)
   - `src/lib/database/schema.ts` — search for `agent_traces` and `agent_metrics` tables

## Trace Event Types

The `AgentTracer` records these events during execution:

| Event | When | Data |
|-------|------|------|
| `start` | Execution begins | message length, context availability |
| `tool_call` | Tool invoked | toolName, params preview (truncated 200 chars) |
| `tool_complete` | Tool returns | toolName, duration, success flag |
| `handoff` | Agent delegates | target agent, reason |
| `stream_delta` | First text token | (recorded once only) |
| `complete` | Execution done | output length, duration, tool count |
| `error` | Failure | message, stack (truncated) |

## Querying Traces

### Recent traces for an agent
```sql
SELECT id, agent_name, trace_type, duration, tool_calls_count, error_message,
       created_at
FROM agent_traces
WHERE agent_name = '<agent-name>'
ORDER BY created_at DESC
LIMIT 20;
```

### Traces with errors
```sql
SELECT id, agent_name, error_message, trace_data, created_at
FROM agent_traces
WHERE error_message IS NOT NULL
ORDER BY created_at DESC
LIMIT 10;
```

### Slow traces (over 10s)
```sql
SELECT id, agent_name, duration, tool_calls_count, trace_data, created_at
FROM agent_traces
WHERE duration > 10000
ORDER BY duration DESC
LIMIT 10;
```

### Tool call breakdown
```sql
SELECT
  trace_data->'events' AS events,
  tool_calls_count,
  duration
FROM agent_traces
WHERE agent_name = '<agent-name>'
  AND tool_calls_count > 0
ORDER BY created_at DESC
LIMIT 5;
```

### Agent metrics summary
```sql
SELECT agent_name, date,
       usage_count, avg_response_time, success_rate,
       cost_total, tokens_total, error_count
FROM agent_metrics
WHERE agent_name = '<agent-name>'
ORDER BY date DESC
LIMIT 30;
```

## Debug Flags

Set these environment variables to enable verbose logging:

```bash
AI_LAB_DEBUG_TOOLS=true          # Log tool selection & validation
AI_LAB_DEBUG_CONTEXT=true        # Log context receipt & changes
AI_LAB_DEBUG_INSTRUCTIONS=true   # Log assembled instructions (caution: large)
AI_LAB_DEBUG_RETRIEVAL=true      # Log file_search queries, sources, scores
```

## Analysis Patterns

### Diagnosing slow responses
1. Query traces with high duration
2. Check `events` array for tool_call → tool_complete durations
3. Identify which tool is the bottleneck
4. Check if the tool is hitting an external service (file_search, search API)
5. Consider caching or timeout adjustments

### Diagnosing tool failures
1. Query traces where `error_message` is not null
2. Look at the `tool_call` event immediately before the `error` event
3. Check if the tool params were valid
4. Check if the external service was available

### Diagnosing guardrail rejections
1. Guardrail rejections show as `error` events with the guardrail name
2. Check the `reason` field for why the message was rejected
3. Review the input message and guardrail logic

### Comparing agent performance over time
1. Query `agent_metrics` table for daily aggregates
2. Check trends in avg_response_time, success_rate, error_count
3. Correlate spikes with deployment dates or config changes

## Rules

- Use the Supabase MCP (`mcp__supabase__execute_sql`) for querying traces directly
- Never delete traces — they're the audit trail for agent behavior
- When reporting findings, include specific trace IDs for reference
- Debug flags should only be enabled temporarily — they generate large log volumes
- If traces reveal a systemic issue, recommend a fix in the relevant layer (tool, instructions, guardrail)
