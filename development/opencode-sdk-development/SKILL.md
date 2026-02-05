---
name: OpenCode SDK Development
description: This skill should be used when the user asks to "create an OpenCode tool", "build an OpenCode plugin", "write a custom tool for OpenCode", "use @opencode-ai/sdk", "use @opencode-ai/plugin", "integrate with OpenCode", "create OpenCode hooks", "define tool schema", "use tool.schema", "work with OpenCode sessions", or needs guidance on OpenCode SDK patterns, plugin development, or custom tool creation.
version: 1.0.0
---

# OpenCode SDK Development

Guide for creating custom tools and plugins using the OpenCode SDK.

## Overview

OpenCode provides two main packages for SDK development:

| Package | Purpose |
|---------|---------|
| `@opencode-ai/sdk` | Client SDK for interacting with OpenCode server (sessions, messages, files) |
| `@opencode-ai/plugin` | Plugin system for creating custom tools with schema validation |

## Quick Start: Custom Tools

Custom tools extend OpenCode's capabilities. Tools are TypeScript/JavaScript files auto-discovered from:
- **Local**: `.opencode/tool/` in project directory
- **Global**: `~/.config/opencode/tool/`

The **filename becomes the tool name**.

### Basic Tool Structure

```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Brief description of what the tool does",
  args: {
    paramName: tool.schema.string().describe("Parameter description")
  },
  async execute(args, context) {
    // context provides: sessionID, messageID, agent, abort
    return "Result string returned to the AI"
  }
})
```

### Schema Definition

Use `tool.schema` (which is Zod) for argument validation:

```typescript
args: {
  // String with description
  query: tool.schema.string().describe("Search query"),

  // Optional string
  path: tool.schema.string().optional().describe("File path"),

  // Number with constraints
  limit: tool.schema.number().min(1).max(100).default(10).describe("Max results"),

  // Enum/literal union
  format: tool.schema.enum(["json", "text"]).describe("Output format"),

  // Boolean
  recursive: tool.schema.boolean().default(false).describe("Search recursively")
}
```

### Tool Context

The execute function receives a context object:

```typescript
type ToolContext = {
  sessionID: string      // Current session ID
  messageID: string      // Current message ID
  agent: string          // Current agent identifier
  abort: AbortSignal     // Signal for cancellation
}
```

### Example: File Search Tool

```typescript
import { tool } from "@opencode-ai/plugin"
import { $ } from "bun"

export default tool({
  description: "Search for files matching a pattern",
  args: {
    pattern: tool.schema.string().describe("Glob pattern to match"),
    directory: tool.schema.string().default(".").describe("Directory to search")
  },
  async execute({ pattern, directory }) {
    const result = await $`find ${directory} -name "${pattern}"`.text()
    return result || "No files found"
  }
})
```

## Plugin Development

Plugins provide more comprehensive integrations with hooks for events, authentication, and tool modification.

### Plugin Structure

```typescript
import type { Plugin } from "@opencode-ai/plugin"

const plugin: Plugin = async (input) => {
  const { client, project, directory, worktree, $ } = input

  return {
    // Custom tools
    tool: {
      myTool: tool({ /* definition */ })
    },

    // Event hooks
    event: async ({ event }) => { /* handle events */ },

    // Configuration hooks
    config: async (config) => { /* modify config */ },

    // Message hooks
    "chat.message": async (input, output) => { /* modify messages */ },

    // Tool execution hooks
    "tool.execute.before": async (input, output) => { /* pre-processing */ },
    "tool.execute.after": async (input, output) => { /* post-processing */ }
  }
}

export default plugin
```

### Available Hooks

| Hook | Purpose |
|------|---------|
| `event` | Handle real-time events from server |
| `config` | Modify configuration on load |
| `tool` | Register custom tools |
| `auth` | Custom authentication providers |
| `chat.message` | Modify messages before sending |
| `chat.params` | Modify LLM parameters (temperature, topP) |
| `permission.ask` | Handle permission requests |
| `tool.execute.before` | Pre-process tool arguments |
| `tool.execute.after` | Post-process tool output |

## SDK Client Usage

The SDK client provides programmatic access to OpenCode functionality.

### Initialization

```typescript
import { createOpencode, createOpencodeClient } from "@opencode-ai/sdk"

// Create both client and server
const { client, server } = await createOpencode({
  hostname: "127.0.0.1",
  port: 4096,
  timeout: 5000
})

// Or just the client
const client = createOpencodeClient({
  baseUrl: "http://127.0.0.1:4096"
})
```

### Client API Categories

| Category | Methods |
|----------|---------|
| `client.session` | list, create, get, delete, prompt, messages, fork, share |
| `client.project` | list, current |
| `client.file` | list, read, status |
| `client.find` | text, files, symbols |
| `client.tool` | ids, list |
| `client.event` | subscribe (SSE streaming) |
| `client.mcp` | status, add |
| `client.tui` | appendPrompt, submitPrompt, showToast |

### Session Management

```typescript
// List sessions
const { data: sessions } = await client.session.list()

// Create session
const { data: session } = await client.session.create()

// Send prompt
const { data: response } = await client.session.prompt({
  path: { id: sessionId },
  body: {
    parts: [{ type: "text", text: "Your message here" }]
  }
})

// Get messages
const { data: messages } = await client.session.messages({
  path: { id: sessionId }
})
```

### Event Streaming

```typescript
const result = await client.event.subscribe()

for await (const event of result.events) {
  console.log("Event:", event.type, event.data)
}
```

## Installation

```bash
# Install SDK
npm install @opencode-ai/sdk

# Install plugin package (for tools)
npm install @opencode-ai/plugin
```

Requires TypeScript >= 4.9.

## Tool File Location

| Location | Scope |
|----------|-------|
| `.opencode/tool/*.ts` | Project-specific tools |
| `~/.config/opencode/tool/*.ts` | Global tools for all projects |

Multiple exports create multiple tools: `filename_exportname`.

## Best Practices

1. **Clear Descriptions**: Write concise, action-oriented descriptions for tools and parameters
2. **Schema Validation**: Use Zod schemas to validate all inputs before processing
3. **Error Handling**: Return meaningful error messages as strings
4. **Abort Signal**: Check `context.abort` for long-running operations
5. **Type Safety**: Use TypeScript for full type inference from schemas
6. **Minimal Dependencies**: Keep tools lightweight and focused

## Common Patterns

### Cross-Language Tool

```typescript
import { tool } from "@opencode-ai/plugin"
import { $ } from "bun"

export default tool({
  description: "Run Python analysis script",
  args: {
    file: tool.schema.string().describe("File to analyze")
  },
  async execute({ file }) {
    return await $`python3 analyze.py ${file}`.text()
  }
})
```

### Tool with Context

```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Get current session info",
  args: {},
  async execute(args, context) {
    return JSON.stringify({
      session: context.sessionID,
      message: context.messageID,
      agent: context.agent
    }, null, 2)
  }
})
```

## Troubleshooting

**Tool not appearing:**
- Verify file is in `.opencode/tool/` or `~/.config/opencode/tool/`
- Check file exports a valid tool definition
- Restart OpenCode to reload tools

**Schema errors:**
- Ensure all required args are provided
- Check type constraints (string vs number)
- Verify optional fields use `.optional()`

**Execution errors:**
- Check `execute` returns a string
- Verify async operations complete
- Handle errors and return error messages as strings

## Additional Resources

### Reference Files

For detailed API documentation:
- **`references/sdk-api.md`** - Complete SDK client API reference
- **`references/plugin-api.md`** - Full plugin hooks and types

### Example Files

Working examples in `examples/`:
- **`examples/basic-tool.ts`** - Simple tool implementation
- **`examples/full-plugin.ts`** - Complete plugin with hooks

### External Documentation

- [OpenCode SDK Docs](https://opencode.ai/docs/sdk/)
- [Custom Tools Guide](https://opencode.ai/docs/custom-tools/)
- [OpenCode GitHub](https://github.com/sst/opencode)
