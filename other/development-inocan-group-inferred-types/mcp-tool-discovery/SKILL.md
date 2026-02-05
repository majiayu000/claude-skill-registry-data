---
name: mcp-tool-discovery
description: Use this skill when you need to discover MCP tool parameters, understand naming conventions, or debug tool call errors
---

# MCP Tool Discovery Guide

## Overview

This skill helps you discover and correctly use MCP tools exposed through the Code Executor MCP server.

## Naming Conventions

MCP tools use different naming conventions at different levels:

| Level | Convention | Example |
|-------|------------|---------|
| Original MCP tool | kebab-case | `resolve-library-id` |
| TypeScript export (primary) | camelCase | `resolveLibraryId` |
| TypeScript export (alias) | snake_case | `resolve_library_id` |

All three are valid for imports. Use whichever you prefer.

## The .call() Pattern

All tool exports are objects with a `.call()` method, not direct functions:

```typescript
// CORRECT
import * as context7 from "../servers/context7/index.js";
await context7.resolveLibraryId.call({ libraryName: "react" });

// INCORRECT - This won't work
await context7.resolveLibraryId({ libraryName: "react" });
```

## Discovering Parameters

### Method 1: Check SCHEMA Export

Every tool exports its JSON Schema:

```typescript
import { resolveLibraryId } from "../servers/context7/index.js";
console.log(resolveLibraryId.SCHEMA);
// Shows: { type: "object", properties: {...}, required: [...] }
```

### Method 2: Use list_server_tools

```typescript
// Via MCP tool
{ "tool": "list_server_tools", "server": "context7" }
```

### Method 3: Check Generated .d.ts Files

Look in `servers/<server>/<tool>.d.ts` for TypeScript definitions.

## Common Errors and Solutions

### "required property missing"

**Cause:** A required parameter was not provided.

**Solution:** Check SCHEMA.required array for required parameters.

### "invalid enum value"

**Cause:** Parameter value not in allowed list.

**Solution:** Check SCHEMA.properties.<param>.enum for valid values.

### "Server not connected"

**Cause:** Server connection not established.

**Solution:** The wrapper auto-connects, but if you see this error:
1. Check server is configured in mcp.json
2. Check server is enabled (enabled: true)
3. Use check_server_health tool to diagnose

## Quick Reference

```typescript
// Import a server's tools
import * as serverName from "../servers/<server>/index.js";

// Check available exports
console.log(Object.keys(serverName));

// Check a tool's schema
console.log(serverName.toolName.SCHEMA);

// Check original tool name
console.log(serverName.toolName.TOOL_NAME);

// Call the tool
const result = await serverName.toolName.call({ param: "value" });
```

## Config Loading (Important for Scripts)

When writing scripts that use custom config paths, you must set environment variables BEFORE importing the mcp module:

```typescript
// CORRECT - Set env before dynamic import
process.env.CODE_EXECUTOR_MCP_CONFIG = "path/to/mcp.json";
const { checkServerHealth } = await import("../src/mcp.js");

// WRONG - Import before setting env (ES modules evaluate immediately)
import { checkServerHealth } from "../src/mcp.js";
process.env.CODE_EXECUTOR_MCP_CONFIG = "path/to/mcp.json"; // Too late!
```

This is because ES modules are evaluated at import time, and the config is loaded when the module initializes. Setting environment variables after the import has no effect.

### Alternative: Use CLI Arguments

If you're running the server directly, use CLI arguments instead:

```bash
node build/server.js --mcp-config /path/to/mcp.json --skills-config /path/to/skills.json
```

## Scripts

This skill includes utility scripts in the `scripts/` folder:

### discover-tools.ts

Discover all available MCP servers and their tools programmatically:

```typescript
import { discoverAllServers, discoverServerTools } from './scripts/discover-tools.js';

// Discover all servers
const servers = await discoverAllServers();
console.log(servers);

// Discover tools for a specific server
const context7 = await discoverServerTools('context7');
console.log(context7.tools);
```

Or run directly to print a summary:

```typescript
import './scripts/discover-tools.js';
```

### test-tool-call.ts

Reference script showing the correct pattern for calling MCP tools. Use as a template for testing tool calls.