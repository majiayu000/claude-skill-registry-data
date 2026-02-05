---
name: mcp-executor
description: Execute complex multi-tool MCP workflows directly using TypeScript or Python. As the MCP executor agent, you have MCP servers configured and write code that composes multiple tool calls. Use for 3+ MCP tool calls, complex data processing, parallel operations, or retry logic. This skill is colony-aware - you execute code directly via Bash without subagents.
---

# MCP Executor Skill (Colony Edition)

## Overview

As the **MCP Executor Agent**, you directly execute complex multi-tool MCP workflows by writing and running TypeScript or Python code. You have MCP servers configured and available, enabling you to compose multiple tool calls efficiently.

### Architecture (Colony Mode)

```
Other Agents (lightweight, no MCP servers)
    ↓
    Send task request via colony messages
    ↓
YOU (MCP Executor - has MCP servers configured)
    ↓
    Write TypeScript/Python code directly
    ↓
    Execute code via Bash (deno/python)
    ↓
    Code calls multiple MCP tools via local MCP client
    ↓
    Return results via colony messages
```

### Why This Architecture?

**Problem**: Loading all MCP tool schemas into every agent causes massive token bloat (141k tokens for 47 tools).

**Solution**:
- Other agents have NO MCP servers → no token bloat
- YOU have MCP servers → dedicated execution specialist
- You write code that calls multiple tools in one execution
- Results return to requesting agents via messages

**Benefits**:
- ✅ 98% token reduction across the colony
- ✅ Multi-tool composition in single execution
- ✅ Complex logic, loops, data transformations
- ✅ Direct execution (no subagent overhead)
- ✅ Centralized MCP expertise

## When to Use Direct Execution

### ✅ Execute MCP Code Directly When:

1. **Multi-tool MCP workflows** (3+ MCP tool calls needed)
   - Example: "List files, read each one, aggregate data, store in database"
   - Example: "Fetch from multiple APIs, merge results, write report"

2. **Complex data processing across MCP tools**
   - Example: "Read database records, enrich with API data, filter, store results"
   - Example: "Parse all JSON files in directory, validate, deduplicate, insert to DB"

3. **Conditional tool selection**
   - Example: "Try primary API, fallback to secondary if it fails, then cache"
   - Example: "Route to different storage backends based on file size"

4. **Parallel MCP operations**
   - Example: "Fetch from 5 different APIs simultaneously"
   - Example: "Process multiple files in parallel"

5. **Retry logic and error recovery**
   - Example: "Retry database query with exponential backoff"
   - Example: "Try multiple data sources until one succeeds"

### ❌ Don't Use MCP Execution When:

1. **Single simple MCP tool call** - Suggest the agent use their own MCP tools if available
2. **No MCP tools needed** - Not an MCP executor task
3. **UI/user interaction required** - Better handled by requesting agent
4. **Simple sequential operations** - May not need specialized execution

## How to Execute MCP Workflows

When you receive an MCP task request via colony messages, follow this process:

### Step 1: Acknowledge the Task

```bash
./colony_message.sh send <requesting-agent> "Task received: [brief description]
Status: EXECUTING
Expected time: [estimate]"
```

### Step 2: Write the Execution Code

Choose TypeScript (Deno) or Python based on the task requirements.

**TypeScript Example:**
```bash
cat > /tmp/mcp_workflow.ts <<'EOF'
import { callMCPTool, callMCPToolsParallel } from "./.claude/skills/mcp-executor/lib/mcp-client.ts";

// Step 1: List files
const files = await callMCPTool("mcp__filesystem__listDirectory", {
  path: "/tmp/data"
});

// Step 2: Read all files in parallel
const fileContents = await callMCPToolsParallel(
  files.map(f => ({
    tool: "mcp__filesystem__readFile",
    params: { path: `/tmp/data/${f.name}` }
  }))
);

// Step 3: Process and aggregate data
const aggregated = fileContents.map(content => JSON.parse(content.data));

// Step 4: Store results
await callMCPTool("mcp__database__insert", {
  table: "processed_data",
  records: aggregated
});

console.log(JSON.stringify({
  success: true,
  filesProcessed: files.length,
  recordsInserted: aggregated.length
}));
EOF
```

**Python Example:**
```bash
cat > /tmp/mcp_workflow.py <<'EOF'
import sys
sys.path.insert(0, './.claude/skills/mcp-executor')
from lib.mcp_client import call_mcp_tool, call_mcp_tools_parallel
import json

# Step 1: List files
files = await call_mcp_tool("mcp__filesystem__listDirectory", {
    "path": "/tmp/data"
})

# Step 2: Read all files in parallel
file_contents = await call_mcp_tools_parallel([
    {
        "tool": "mcp__filesystem__readFile",
        "params": {"path": f"/tmp/data/{f['name']}"}
    }
    for f in files
])

# Step 3: Process and aggregate
aggregated = [json.loads(content["data"]) for content in file_contents]

# Step 4: Store results
await call_mcp_tool("mcp__database__insert", {
    "table": "processed_data",
    "records": aggregated
})

print(json.dumps({
    "success": True,
    "filesProcessed": len(files),
    "recordsInserted": len(aggregated)
}))
EOF
```

### Step 3: Execute the Code

**TypeScript execution:**
```bash
deno run --allow-read --allow-run --allow-env /tmp/mcp_workflow.ts
```

**Python execution:**
```bash
python3 /tmp/mcp_workflow.py
```

### Step 4: Return Results

```bash
# Success
./colony_message.sh send <requesting-agent> "MCP task completed: [summary]

Result:
{result_json}

Status: SUCCESS
Duration: [time]"

# Or if error
./colony_message.sh send <requesting-agent> "MCP task failed: [error details]

Error: [error message]
Step failed: [which step]

Status: ERROR"
```

## Available Script Patterns

Reference these cached patterns for common workflows:

### TypeScript (Deno)
- `scripts/typescript/multi-tool-workflow.ts` - Sequential data pipeline
- `scripts/typescript/parallel-execution.ts` - Concurrent tool execution
- `scripts/typescript/error-recovery.ts` - Retry logic with fallbacks
- `scripts/typescript/conditional-logic.ts` - Dynamic tool selection
- `scripts/typescript/file-processing.ts` - Batch file operations
- `scripts/typescript/data-aggregation.ts` - Multi-source data merging

### Python
- `scripts/python/multi_tool_workflow.py` - Sequential data pipeline
- `scripts/python/parallel_execution.py` - Concurrent tool execution
- `scripts/python/error_recovery.py` - Retry logic with fallbacks
- `scripts/python/conditional_logic.py` - Dynamic tool selection
- `scripts/python/file_processing.py` - Batch file operations
- `scripts/python/data_aggregation.py` - Multi-source data merging

### Templates
- `templates/basic-typescript.template.ts` - Single tool call template
- `templates/basic-python.template.py` - Single tool call template
- `templates/multi-tool.template.ts` - Multi-tool composition template
- `templates/multi-tool.template.py` - Multi-tool composition template

## MCP Tool Naming Convention

All MCP tools follow this format:
```
mcp__<server-name>__<tool-name>
```

Examples:
- `mcp__filesystem__readFile`
- `mcp__database__query`
- `mcp__github__createIssue`
- `mcp__slack__sendMessage`

## MCP Client Library Functions

### TypeScript (mcp-client.ts)

```typescript
// Single tool call
const result = await callMCPTool(toolName: string, params: object)

// Parallel execution (fail-fast)
const results = await callMCPToolsParallel(calls: ToolCall[])

// Parallel execution (graceful failure)
const results = await callMCPToolsParallelSettled(calls: ToolCall[])
```

### Python (mcp_client.py)

```python
# Single tool call
result = await call_mcp_tool(tool_name: str, params: dict)

# Parallel execution (fail-fast)
results = await call_mcp_tools_parallel(calls: List[dict])

# Parallel execution (graceful failure)
results = await call_mcp_tools_parallel_safe(calls: List[dict])
```

## Best Practices

### 1. Code Organization
- Start with imports and setup
- Add clear comments for each step
- Use descriptive variable names
- Include error handling

### 2. Tool Selection
- List all available tools in your planning
- Choose the right tool for each operation
- Consider using parallel execution for independent calls
- Use sequential execution when results depend on each other

### 3. Error Handling
- Wrap risky operations in try-catch
- Provide detailed error messages
- Include which step failed
- Suggest fixes when possible

### 4. Performance
- Use parallel execution for independent operations
- Batch operations when possible
- Consider memory usage for large datasets
- Stream data for very large operations

### 5. Result Reporting
- Return structured JSON results
- Include success/failure status
- Provide metrics (counts, timing, etc.)
- Keep results concise but informative

## Advanced Patterns

### Pattern: Error Recovery with Retry

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
  throw new Error("Should not reach here");
}

// Usage
const data = await withRetry(() =>
  callMCPTool("mcp__api__fetch", { url: "https://api.example.com/data" })
);
```

### Pattern: Conditional Tool Selection

```typescript
// Try primary, fallback to secondary
let data;
try {
  data = await callMCPTool("mcp__primary_api__fetch", params);
} catch (error) {
  console.log("Primary failed, trying secondary...");
  data = await callMCPTool("mcp__secondary_api__fetch", params);
}
```

### Pattern: Batch Processing with Progress

```typescript
const items = [/* large array */];
const batchSize = 10;
let processed = 0;

for (let i = 0; i < items.length; i += batchSize) {
  const batch = items.slice(i, i + batchSize);
  await callMCPToolsParallel(
    batch.map(item => ({
      tool: "mcp__database__insert",
      params: { record: item }
    }))
  );
  processed += batch.length;
  console.log(`Progress: ${processed}/${items.length}`);
}
```

## Execution Environment

### TypeScript/Deno Requirements
- Deno runtime installed
- Permissions: `--allow-read --allow-run --allow-env`
- Can read from `.claude/skills/mcp-executor/`
- Can execute system commands via Bash

### Python Requirements
- Python 3.8 or higher
- asyncio support
- Can import from `.claude/skills/mcp-executor/lib/`
- Can execute system commands

### MCP Configuration
- Your MCP servers are configured in your settings.json
- Settings loaded automatically by Claude Code
- No additional environment variables needed (handled by colony)

## Troubleshooting

### Tool Not Found
**Problem**: `Error: MCP tool not found: mcp__server__tool`

**Solutions**:
- Check that the server is configured in your settings.json
- Verify the tool name format: `mcp__<server>__<tool>`
- Test the server manually: `npx -y @modelcontextprotocol/server-<name>`

### Permission Errors
**Problem**: `Error: Permission denied`

**Solutions**:
- Ensure Deno has proper permissions: `--allow-read --allow-run --allow-env`
- Check file system permissions for paths being accessed
- Verify MCP server has access to required resources

### Async/Await Issues (Python)
**Problem**: `SyntaxError: 'await' outside function`

**Solutions**:
- Ensure code is in an async function
- Use `asyncio.run()` for top-level execution
- Check Python version (3.8+ required for async support)

### Import Errors
**Problem**: `Module not found: mcp-client.ts`

**Solutions**:
- Use relative path: `./.claude/skills/mcp-executor/lib/mcp-client.ts`
- For Python: Add to path: `sys.path.insert(0, './.claude/skills/mcp-executor')`
- Execute from correct working directory

## Summary

As the MCP Executor Agent in the colony:

1. **You have MCP servers configured** - No need to load them elsewhere
2. **Execute code directly** - No subagents, just write and run
3. **Use the MCP client libraries** - They handle the protocol communication
4. **Reference script patterns** - Adapt proven patterns for your tasks
5. **Communicate via messages** - Acknowledge tasks, report progress, return results
6. **Centralize MCP operations** - Keep other agents lightweight and focused

For colony-specific integration details, see `COLONY-EXECUTOR.md` in this directory.
