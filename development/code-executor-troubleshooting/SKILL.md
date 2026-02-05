---
name: code-executor-troubleshooting
description: Troubleshooting guide for Code Executor MCP issues - diagnose hanging, import errors, and connection problems
tags:
  - mcp
  - troubleshooting
  - debugging
  - code-executor
---

# Code Executor Troubleshooting Guide

This skill helps you diagnose and fix common issues when using Code Executor MCP.

## Quick Diagnostic Workflow

When `execute_code` fails or hangs, follow these steps in order:

### Step 1: Check Server Availability

```
Tool: list_available_servers
```

Look for your server's status:
- **"ready"** → Server wrapper exists, proceed to Step 2
- **"disabled"** → Enable in mcp.json (`"enabled": true`)
- **"no-wrapper"** → Run `pnpm run gen` to generate wrappers

### Step 2: Verify Tool Exists

```
Tool: list_server_tools
Args: { "server": "your-server-name" }
```

**Important**: Copy the exact import statement from the output! Don't guess.

### Step 3: Test Server Connection

```
Tool: test_server_connection
Args: { "server": "your-server-name" }
```

If this fails, the MCP server is not responding. Check:
- Is the server command installed?
- Are there dependency issues?
- Check stderr with `get_server_stderr`

### Step 4: Check Server Health

```
Tool: check_server_health
Args: { "server": "your-server-name" }
```

Shows detailed diagnostics including:
- Command path and arguments
- Timeout settings
- Connection status
- Error suggestions

### Step 5: Get Server Stderr

```
Tool: get_server_stderr
Args: { "server": "your-server-name" }
```

Shows any error output from the server process startup.

---

## Common Error Patterns

### Import Errors

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `Cannot find module '../servers/X'` | Missing `/index.js` | Add `/index.js` to path |
| `Cannot find module '../servers/X/index'` | Missing `.js` extension | Add `.js` extension |
| `ERR_MODULE_NOT_FOUND` | Wrong path format | Use exact path from `list_server_tools` |
| `X is not exported from module` | Wrong export name | Use camelCase name from `list_server_tools` |
| `does not provide an export named` | Using wrong export | Check available exports with `list_server_tools` |

**Correct Import Examples:**
```typescript
// ✅ Correct - full path with .js
import { resolveLibraryId } from '../servers/context7/index.js';

// ✅ Correct - direct file import
import * as tool from '../servers/context7/resolve-library-id.js';

// ❌ Wrong - missing /index.js
import { resolveLibraryId } from '../servers/context7';

// ❌ Wrong - missing .js extension
import { resolveLibraryId } from '../servers/context7/index';
```

### Function Call Errors

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `X is not a function` | Wrong call pattern | Use `tool({ args })` or `tool.call({ args })` |
| `call is not a function` | Imported wrong thing | Check import statement matches `list_server_tools` output |

**Correct Call Patterns:**
```typescript
// ✅ Both patterns work
const result = await resolveLibraryId({ libraryName: "react" });
const result = await resolveLibraryId.call({ libraryName: "react" });

// ❌ Wrong - double call
const result = await resolveLibraryId.call.call({ ... });
```

### Execution Hangs

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| No output at all | Server not responding | Use `debug: true` and check connection |
| First console.log appears, then hangs | Tool call hanging | Use `debug: true` to see where it stalls |
| Hangs at "Connecting..." | Server startup slow/failed | Use `test_server_connection` to diagnose |
| Hangs at "Calling..." | Tool execution slow | Increase timeout or check tool parameters |

**Debugging Hanging Execution:**
```
execute_code({
  code: "...",
  debug: true  // ← Shows connection/call progress
})
```

Debug output progression:
1. `[server] Connecting...` - Starting connection to MCP server
2. `[server] Calling toolName...` - Connection succeeded, making tool call
3. `[server] Call completed.` - Tool returned successfully

If it hangs at step 1: Server is not starting properly
If it hangs at step 2: Tool execution is slow or stuck

### Server Connection Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Server "X" not found in config` | Wrong server name | Check `list_available_servers` for correct name |
| `Server "X" is disabled` | Server disabled in config | Set `"enabled": true` in mcp.json |
| `Command not found` | Server not installed | Install the MCP server package |
| `Connection timed out` | Server too slow to start | Increase `timeout` in mcp.json |

### Parameter Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Required parameter missing` | Missing required param | Use `get_tool_schema` to see requirements |
| `Invalid enum value` | Wrong enum value | Use `get_tool_schema` to see valid values |
| `Type error` | Wrong parameter type | Check parameter types in schema |

---

## Timeout Configuration

If operations are too slow, configure timeouts in `mcp.json`:

```json
{
  "servers": {
    "your-server": {
      "command": "npx",
      "args": ["your-mcp-server"],
      "timeout": 120000,      // Connection timeout (ms)
      "callTimeout": 60000,   // Tool call timeout (ms)
      "retries": 3,           // Connection retry count
      "retryDelay": 1000      // Delay between retries (ms)
    }
  }
}
```

Or use per-call timeout:
```typescript
const result = await tool.call({ args }, { timeout: 60000 });
```

---

## Server-Specific Issues

### Context7 Server
- Requires valid library names
- Use `resolveLibraryId` first to get the correct ID
- Then use that ID with `getLibraryDocs`

### Sequential Thinking Server
- Requires specific stage values
- Use `get_tool_schema` to see valid stage enum values
- Must call `clear-history` before starting new session

---

## Recovery Steps

If you've tried everything and it still doesn't work:

1. **Regenerate wrappers**: `pnpm run gen`
2. **Clear cached config**: Restart the MCP server
3. **Check server logs**: `get_server_stderr`
4. **Test manually**: Run the server command directly in terminal
5. **Check dependencies**: Ensure all npm packages are installed

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│  CODE EXECUTOR TROUBLESHOOTING QUICK REFERENCE     │
├─────────────────────────────────────────────────────┤
│  1. list_available_servers    → See ready servers   │
│  2. list_server_tools         → Get import paths    │
│  3. execute_code {debug:true} → See where it hangs  │
│  4. test_server_connection    → Test connectivity   │
│  5. check_server_health       → Detailed diagnostics│
│  6. get_server_stderr         → Error output        │
├─────────────────────────────────────────────────────┤
│  IMPORT PATTERN:                                    │
│  import { X } from '../servers/NAME/index.js';      │
│                          ↑            ↑             │
│                     server name    MUST have .js    │
├─────────────────────────────────────────────────────┤
│  CALL PATTERN:                                      │
│  await tool({ param: "value" });                    │
│  await tool.call({ param: "value" });               │
└─────────────────────────────────────────────────────┘