---
name: code-executor
description: Efficiently compose multiple MCP tool operations by launching a subagent that writes and executes TypeScript or Python code. Use when you need to compose 3+ MCP tool calls, process their results together, implement complex logic, or avoid token overhead from loading many MCP tool schemas into main context. The subagent has MCP servers configured and writes code that calls tools dynamically.
---

# Code Executor Skill

## Overview

This skill teaches you (Main Claude Code) how to efficiently handle multi-tool MCP workflows by launching a subagent that writes and executes code to compose MCP tool calls.

### Architecture

```
Main Context (YOU - no MCP servers configured)
    ↓
    Recognize multi-tool MCP workflow needed
    ↓
    Launch subagent via Task tool
    ↓
Subagent Context (has MCP servers configured)
    ↓
    Write TypeScript/Python code
    ↓
    Execute code via Bash (deno/python)
    ↓
    Code calls multiple MCP tools via local MCP client
    ↓
    Return results to YOU (main context)
```

### Why This Architecture?

**Problem**: Loading all MCP tool schemas into your main context causes token bloat (141k tokens for 47 tools).

**Solution**:
- YOU (main) have NO MCP servers → no token bloat
- Subagent has MCP servers → isolated context
- Subagent writes code that calls multiple tools
- Results return to you

**Benefits**:
- ✅ 98% token reduction in main context
- ✅ Multi-tool composition in single execution
- ✅ Complex logic, loops, data transformations
- ✅ Subagent context disposed after task

## When to Use This Pattern

### ✅ Launch Subagent With This Skill When:

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

### ❌ Don't Use This Pattern When:

1. **Single simple MCP tool call** - Just call the tool directly
2. **No MCP tools needed** - Use regular task planning
3. **UI/user interaction required** - Use slash commands
4. **Simple sequential operations** - Regular tool calls are clearer

## How to Launch a Subagent

When you identify a multi-tool MCP workflow, use the Task tool to launch a subagent:

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `You have access to MCP servers with the following tools:
  - mcp__filesystem__readFile, writeFile, listDirectory
  - mcp__database__query, insert, update
  - [list the relevant tools for this task]

  Task: [Describe the multi-tool workflow clearly]

  Instructions:
  1. Reference the cached script pattern from scripts/[relevant-script].ts
  2. Write TypeScript code that:
     - Imports: import { callMCPTool } from '../../lib/mcp-client.ts';
     - Calls MCP tools using callMCPTool('mcp__server__tool', params)
     - Processes and transforms data as needed
     - Returns summary of results
  3. Execute the code via Bash with MCP_CONFIG_PATH set:
     MCP_CONFIG_PATH=~/.claude/subagent-mcp.json deno run --allow-read --allow-run --allow-env /tmp/script.ts
  4. Return the execution results

  Use the pattern from: [specify cached script that matches]
  - scripts/typescript/multi-tool-workflow.ts (sequential pipeline)
  - scripts/typescript/parallel-execution.ts (concurrent operations)
  - scripts/typescript/error-recovery.ts (retry logic)
  - scripts/typescript/file-processing.ts (batch file ops)
  - scripts/typescript/conditional-logic.ts (dynamic tool selection)
  - scripts/typescript/data-aggregation.ts (multi-source merging)

  Expected output: [What you need back from the subagent]`
})
```

## Cached Script Patterns

The skill includes 12 proven script patterns (6 TypeScript + 6 Python) in the `scripts/` directory. **Always reference these** when launching subagents:

### TypeScript Patterns

1. **`scripts/typescript/multi-tool-workflow.ts`**
   - Sequential 5-step pipeline: Fetch → Transform → Validate → Store → Report
   - Use for: Data processing pipelines where each step depends on previous

2. **`scripts/typescript/parallel-execution.ts`**
   - Concurrent operations with Promise.all and Promise.allSettled
   - Use for: Fetching from multiple sources simultaneously

3. **`scripts/typescript/error-recovery.ts`**
   - Retry logic with exponential backoff, fallback strategies
   - Use for: Unreliable APIs, failover patterns

4. **`scripts/typescript/file-processing.ts`**
   - Batch file operations: list → filter → process → aggregate
   - Use for: Processing multiple files, generating reports

5. **`scripts/typescript/conditional-logic.ts`**
   - Dynamic tool selection based on runtime data
   - Use for: Routing, adaptive workflows, decision trees

6. **`scripts/typescript/data-aggregation.ts`**
   - Fetch from multiple sources, transform to common format, merge
   - Use for: Combining data from multiple databases/APIs

### Python Patterns

Same patterns available in `scripts/python/`:
- `multi_tool_workflow.py`
- `parallel_execution.py`
- `error_recovery.py`
- `file_processing.py`
- `conditional_logic.py`
- `data_aggregation.py`

## Subagent Task Prompt Template

Use this template when launching subagents:

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `You are a subagent with access to MCP servers. Write code to complete this task.

  ## Available MCP Tools
  [List the MCP servers/tools available - you should know these from your configuration]
  - mcp__filesystem__readFile, writeFile, listDirectory
  - mcp__database__query, insert
  - [etc...]

  ## Task
  [Clear description of what needs to be done]

  ## Instructions

  1. **Reference Cached Pattern**
     Use the pattern from: scripts/typescript/[most-similar-script].ts
     - This script shows: [what pattern it demonstrates]
     - Adapt it for: [how to modify for this task]

  2. **Write TypeScript Code**
     \`\`\`typescript
     import { callMCPTool } from '../../lib/mcp-client.ts';

     // [Step-by-step comments of what the code should do]
     \`\`\`

  3. **Tool Call Format**
     - Format: callMCPTool('mcp__<server>__<tool>', { params })
     - Example: callMCPTool('mcp__filesystem__readFile', { path: '/data/file.json' })

  4. **Execute Code**
     Run via Bash with MCP_CONFIG_PATH set:
     \`\`\`bash
     MCP_CONFIG_PATH=~/.claude/subagent-mcp.json deno run --allow-read --allow-run --allow-env /tmp/your-script.ts
     \`\`\`

  5. **Return Results**
     Provide summary of:
     - What was accomplished
     - Number of records/files processed
     - Any errors or warnings
     - Final output data

  ## Expected Output
  [Specify exactly what data/summary you need back]

  ## Error Handling
  - Wrap all MCP calls in try/catch
  - Log errors clearly
  - [Any specific error handling needed]
  `
})
```

## Example: Complete Workflow

### User Request
"Read all JSON files in /tmp/data, aggregate the data, and store in database"

### Your Response (Main Claude Code)

You recognize this needs:
- Multiple filesystem operations (list, read multiple files)
- Data processing (parse JSON, aggregate)
- Database operation (insert)

**You launch subagent:**

```typescript
Task({
  subagent_type: "general-purpose",
  prompt: `You have access to MCP servers with these tools:
  - mcp__filesystem__listDirectory
  - mcp__filesystem__readFile
  - mcp__database__insert

  Task: Read all JSON files in /tmp/data, parse them, aggregate the data, and store in database table 'aggregated_data'.

  Instructions:
  1. Use the pattern from scripts/typescript/file-processing.ts
     - It shows: batch file operations with filtering and aggregation
     - Adapt it to: read JSON files specifically and store results in DB

  2. Write TypeScript code that:
     - Lists files in /tmp/data
     - Filters for .json extension
     - Reads each JSON file
     - Parses and aggregates the data
     - Stores aggregated results in database

  3. Import the MCP client:
     import { callMCPTool } from '../../lib/mcp-client.ts';

  4. Execute via:
     MCP_CONFIG_PATH=~/.claude/subagent-mcp.json deno run --allow-read --allow-run --allow-env /tmp/aggregate-files.ts

  5. Return: Number of files processed and records stored

  Expected output: "Processed X files, stored Y records in database"`
})
```

### Subagent Executes

1. Reads cached pattern from `scripts/typescript/file-processing.ts`
2. Writes adapted code:

```typescript
import { callMCPTool } from '../../lib/mcp-client.ts';

const files = await callMCPTool('mcp__filesystem__listDirectory', {
  path: '/tmp/data'
});

const jsonFiles = files.filter(f => f.name.endsWith('.json'));
const allData = [];

for (const file of jsonFiles) {
  const content = await callMCPTool('mcp__filesystem__readFile', {
    path: file.path
  });
  allData.push(...JSON.parse(content));
}

const aggregated = {
  total_records: allData.length,
  data: allData,
  timestamp: new Date().toISOString()
};

await callMCPTool('mcp__database__insert', {
  table: 'aggregated_data',
  record: aggregated
});

console.log(`Processed ${jsonFiles.length} files, ${allData.length} records`);
```

3. Executes code via Bash
4. Returns: "Processed 15 files, 1,247 records stored in database"

### You Receive Results

You report to user:
"✓ Successfully processed 15 JSON files from /tmp/data and stored 1,247 aggregated records in the database."

## Tool Naming Convention

**Format**: `mcp__<server>__<tool>`

**Examples**:
- `mcp__filesystem__readFile`
- `mcp__database__query`
- `mcp__github__createPullRequest`
- `mcp__postgres__insert`

The `<server>` name comes from the subagent's MCP configuration file (`.mcp.json` or `~/.claude/subagent-mcp.json`).

## Choosing TypeScript vs Python

**TypeScript (Deno)**:
- ✅ Strong typing with interfaces
- ✅ Better for complex data transformations
- ✅ Native async/await, Promise.all
- ✅ Faster execution
- ❌ Requires Deno installed

**Python**:
- ✅ More familiar to some developers
- ✅ Better for data science/ML tasks
- ✅ Rich standard library
- ✅ Type hints with TypedDict
- ❌ Slightly slower

**Default recommendation**: Use TypeScript unless subagent explicitly needs Python libraries.

## MCP Client Library

The subagent uses a local MCP client library to call tools:

**TypeScript**: `lib/mcp-client.ts`
```typescript
import { callMCPTool, callMCPToolsParallel } from '../../lib/mcp-client.ts';

// Single tool call
const result = await callMCPTool('mcp__filesystem__readFile', {
  path: '/data/file.json'
});

// Parallel calls
const [file1, file2, file3] = await callMCPToolsParallel([
  { tool: 'mcp__filesystem__readFile', parameters: { path: '/data/1.json' } },
  { tool: 'mcp__filesystem__readFile', parameters: { path: '/data/2.json' } },
  { tool: 'mcp__filesystem__readFile', parameters: { path: '/data/3.json' } }
]);
```

**Python**: `lib/mcp_client.py`
```python
from lib.mcp_client import call_mcp_tool, call_mcp_tools_parallel

# Single tool call
result = await call_mcp_tool('mcp__filesystem__readFile', {
    'path': '/data/file.json'
})

# Parallel calls
results = await call_mcp_tools_parallel([
    {'tool': 'mcp__filesystem__readFile', 'parameters': {'path': '/data/1.json'}},
    {'tool': 'mcp__filesystem__readFile', 'parameters': {'path': '/data/2.json'}},
    {'tool': 'mcp__filesystem__readFile', 'parameters': {'path': '/data/3.json'}}
])
```

## Templates

For simpler tasks, reference the templates in `templates/`:

- `basic-typescript.template.ts` - Single tool call skeleton
- `basic-python.template.py` - Single tool call skeleton
- `multi-tool.template.ts` - Multiple tool composition
- `multi-tool.template.py` - Multiple tool composition

Tell the subagent: "Use the pattern from templates/basic-typescript.template.ts"

## Error Handling

Always instruct subagents to include error handling:

```typescript
try {
  const result = await callMCPTool('mcp__database__query', {
    query: 'SELECT * FROM users'
  });
  return { success: true, data: result };
} catch (error) {
  console.error('Database query failed:', error.message);
  return { success: false, error: error.message };
}
```

## Best Practices

### When Launching Subagents

1. **Be specific about tools available**
   - List the exact MCP tools the subagent has access to
   - Don't assume subagent knows your MCP configuration

2. **Reference cached patterns**
   - Always point to the most similar cached script
   - Explain how to adapt it for the current task

3. **Specify execution command**
   - CRITICAL: Set `MCP_CONFIG_PATH=~/.claude/subagent-mcp.json` before command
   - Include the full `deno run` or `python` command
   - Include required permissions: `--allow-read --allow-run --allow-env`
   - Example: `MCP_CONFIG_PATH=~/.claude/subagent-mcp.json deno run --allow-read --allow-run --allow-env script.ts`

4. **Define expected output clearly**
   - What data you need back
   - What format (summary, full data, counts, etc.)

5. **Include error handling instructions**
   - How to handle failures
   - Whether to fail-fast or continue on errors

### When Subagent Writes Code

(These are instructions for the subagent, but you should know them to guide effectively)

1. **Always import MCP client first**
   ```typescript
   import { callMCPTool } from '../../lib/mcp-client.ts';
   ```

2. **Use proper tool name format**
   - Format: `mcp__<server>__<tool>`
   - Match exactly to MCP configuration

3. **Handle errors gracefully**
   - Try/catch around all MCP calls
   - Log errors clearly
   - Return error status

4. **Process data efficiently**
   - Use parallel calls when possible (Promise.all, asyncio.gather)
   - Stream large datasets
   - Aggregate early to reduce memory

5. **Return useful summaries**
   - Include counts, timestamps
   - Report errors/warnings
   - Provide actionable results

## Debugging

If subagent task fails:

1. **Check MCP configuration**
   - Is the tool available in subagent's `.mcp.json`?
   - Is the server running?

2. **Verify tool name format**
   - Correct format: `mcp__server__tool`
   - Match to actual server name in config

3. **Check MCP_CONFIG_PATH is set**
   - CRITICAL: Bash execution must set `MCP_CONFIG_PATH=~/.claude/subagent-mcp.json`
   - Without this, MCP client won't find server configuration
   - Verify config file exists: `ls -la ~/.claude/subagent-mcp.json`

4. **Check permissions**
   - Deno needs: `--allow-read --allow-run --allow-env`
   - MCP servers may have restricted access

5. **Review generated code**
   - Did subagent import MCP client correctly?
   - Are tool names formatted properly?
   - Is error handling present?

6. **Check execution output**
   - Look at stdout/stderr from Bash execution
   - MCP errors appear in output

## Security Considerations

1. **Subagent has code execution** - Review generated code before execution in sensitive contexts
2. **MCP servers access resources** - Configure MCP with least privilege
3. **Filesystem access** - Limit allowed paths in MCP server configuration
4. **Database access** - Use read-only connections where possible
5. **Network access** - MCP servers can make network requests

## Documentation References

- **Setup**: See [SUBAGENT_SETUP.md](./SUBAGENT_SETUP.md) for configuration
- **TypeScript**: See [TYPESCRIPT_GUIDE.md](./TYPESCRIPT_GUIDE.md) for patterns
- **Python**: See [PYTHON_GUIDE.md](./PYTHON_GUIDE.md) for patterns
- **Examples**: See [EXAMPLES.md](./EXAMPLES.md) for complete use cases
- **API Reference**: See [REFERENCE.md](./REFERENCE.md) for MCP client API

## Summary

**You are Main Claude Code**. When you encounter a multi-tool MCP workflow:

1. ✅ **Recognize the pattern** - Multiple MCP tools needed, complex logic
2. ✅ **Launch subagent** - Use Task tool with clear instructions
3. ✅ **Reference cached scripts** - Point to most similar pattern
4. ✅ **Specify tools available** - List MCP servers/tools explicitly
5. ✅ **Define expected output** - What you need back from subagent
6. ✅ **Receive results** - Subagent executes code and returns summary
7. ✅ **Report to user** - Present results clearly

**Key principle**: You orchestrate, subagent executes. Keep your main context clean, let subagents handle the heavy MCP lifting.
