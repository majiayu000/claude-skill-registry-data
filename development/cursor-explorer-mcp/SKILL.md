---
name: cursor-explorer-mcp
description: Use for token-expensive operations requiring multi-file analysis - codebase exploration, broad searches, architecture understanding, tracing flows, finding implementations across files. Uses MCP cursor-agent server (company pays) with clean async interface. Do NOT use for single-file analysis, explaining code already in immediate context, or pure reasoning tasks.
allowed-tools: mcp__cursor_agent__cursor_agent_start, mcp__cursor_agent__cursor_agent_status, mcp__cursor_agent__cursor_agent_result, Read
---

# Cursor Explorer (MCP)

**Trigger immediately** when you see:
- "Find where X is..." → cursor-agent
- "How does X work?" (multi-file) → cursor-agent
- "Trace the flow of..." → cursor-agent
- Manual approach needs 3+ file reads → cursor-agent

**Skip** for: single file, pure reasoning, code in context, 1-2 line answers

## Workflow

```python
# 1. Start query (batch multiple questions)
start = mcp__cursor_agent__cursor_agent_start({
  "query": "Find where X is. Give file:line, code snippets, purpose."
})
query_id = json.loads(start)["query_id"]

# 2. Get result (blocks until done)
result = mcp__cursor_agent__cursor_agent_result({
  "query_id": query_id,
  "wait": True  # Blocks automatically, no manual monitoring needed
})
output = json.loads(result)

# 3. If completed, present findings. If failed, fall back to Read/Grep.
```

**Never retry on failure** - just fall back to manual tools.

## Query Tips

- Request file:line refs
- Ask for code snippets
- Batch related questions
- Be specific about format needed
