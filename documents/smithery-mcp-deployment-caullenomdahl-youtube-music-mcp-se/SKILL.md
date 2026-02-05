---
name: smithery-mcp-deployment
description: |
  Best practices for creating, optimizing, and deploying MCP servers to Smithery. Use this skill when:
  (1) Creating new MCP servers for Smithery deployment
  (2) Optimizing quality scores (achieving 90/100)
  (3) Troubleshooting deployment issues (0/0 tools, missing annotations, low scores)
  (4) Migrating existing MCP servers to Smithery format
  (5) Understanding Smithery's schema format requirements
  (6) Adding workflow prompts, tool annotations, or documentation resources
  (7) Configuring smithery.yaml and package.json for deployment
---

# Smithery MCP Deployment Best Practices

## Documentation Resources

Before implementing MCP features or troubleshooting issues, consult the official MCP specification:

**Use the context7 tool** to look up current MCP documentation:
- Primary resource: `https://context7.com/websites/modelcontextprotocol_io_specification`
- This provides the authoritative MCP specification for tools, prompts, resources, and protocol details

## Critical: Schema Format (Most Common Issue)

The #1 cause of deployment failures is incorrect schema format. Smithery expects **plain objects with Zod properties**, NOT `z.object()` wrappers.

```typescript
// WRONG - Results in "0/0 tools"
inputSchema: z.object({
  param: z.string()
}).strict()

// CORRECT - Tools will be detected
inputSchema: {
  param: z.string()
}
```

This applies to:
- `inputSchema` in tools
- `outputSchema` in tools
- `argsSchema` in prompts

## Quality Scoring (90/100 Optimal)

| Feature | Points | How to Achieve |
|---------|--------|----------------|
| Tools with descriptions | 25 | Detailed 2-4 sentence descriptions |
| Tool annotations | 20 | Add inside config object (not 4th param) |
| Optional config | 15 | All fields optional or with defaults |
| Workflow prompts | 15 | Create 3-5 workflow prompts |
| Icon | 10 | Add icon.svg to repository root |
| Documentation | 5 | Comprehensive README |

**Note**: "Optional Config" (15pts) and "Config Schema" (10pts) are mutually exclusive. Optional is better UX and higher points.

## Tool Registration Template

```typescript
server.registerTool(
  'tool_name',
  {
    title: 'Action-Oriented Title',
    description: 'Clear 2-4 sentence description. Start with action verb. ' +
                 'Explain behavior (async/blocking). Mention related tools.',
    inputSchema: {
      param: z.string()
        .describe('Specific description with examples (e.g., foo, bar)')
    },
    outputSchema: {
      result: z.string()
    },
    annotations: {              // Inside config object!
      readOnlyHint: true,       // Only reads data?
      destructiveHint: false,   // Deletes/destroys data?
      idempotentHint: true,     // Same input = same result?
      openWorldHint: false      // Deterministic results?
    }
  },
  async (args) => {
    // Args passed directly (not request.params.arguments)
    return {
      content: [{
        type: 'text',
        text: JSON.stringify(result, null, 2)
      }]
    };
  }
);
```

## Workflow Prompt Template

```typescript
server.registerPrompt(
  'workflow-name',
  {
    title: 'Workflow Title',
    description: 'End-to-end workflow description',
    argsSchema: {              // Plain object, not z.object()!
      // IMPORTANT: Only z.string() types supported
      param: z.string().describe('Parameter description').optional()
    }
  },
  async (args) => ({
    messages: [{
      role: 'user',
      content: {
        type: 'text',
        text: `Multi-step workflow instructions...`
      }
    }]
  })
);
```

## Configuration Setup

**src/types.ts:**
```typescript
export const configSchema = z.object({
  apiToken: z.string().optional()
    .describe("Token (or use API_TOKEN env var)"),
  format: z.enum(["json", "markdown"]).default("markdown")
});

export type Config = z.infer<typeof configSchema>;
```

**src/index.ts:**
```typescript
export { configSchema };  // Must export!

export default function createServer(config?: Config) {
  const server = new McpServer({ name: 'your-server', version: '1.0.0' });
  return server;
}
```

**smithery.yaml (TypeScript runtime):**
```yaml
runtime: "typescript"
# Do NOT include configSchema - auto-detected from TypeScript export
```

## Project Structure

```
your-mcp-server/
├── icon.svg              <- REQUIRED for 10 points!
├── package.json
├── smithery.yaml
├── tsconfig.json
├── src/
│   ├── index.ts         <- Export createServer & configSchema
│   ├── types.ts         <- Define configSchema
│   ├── tools/           <- Tool implementations
│   ├── prompts/         <- Workflow prompts
│   └── resources/       <- Documentation resources
```

## Testing Before Deployment

```bash
# 1. Lint TypeScript
npx tsc --noEmit

# 2. Build with Smithery
npm run build
# Look for: "Config schema: N fields (M required)"

# 3. Test with MCP Inspector
npx @modelcontextprotocol/inspector dist/index.js

# 4. Verify in Inspector:
#    - tools/list shows all tools with annotations
#    - prompts/list shows all prompts
#    - Try calling each tool
```

## Common Issues Quick Reference

| Symptom | Cause | Fix |
|---------|-------|-----|
| "0/0 tools" | Using `z.object()` | Use plain objects for schemas |
| "9/16 parameters" | `.optional()`/`.default()` on schema | Remove modifiers, handle in handler |
| No annotations | Wrong placement | Put inside config object, not 4th param |
| Score stuck at 43 | Schema + annotations | Fix both issues |
| Icon not showing | Wrong location | Place icon.svg in repo root |
| TS error: `request.params` | Old handler pattern | Use `async (args) =>` not `async (request) =>` |
| TS error: prompt argsSchema | Non-string types | Use only `z.string().optional()` |
| Deployment fails | configSchema in yaml | Remove from yaml for TypeScript runtime |

## Detailed Documentation

For comprehensive guides, see:
- **Schema Format Details**: [references/schema-format.md](references/schema-format.md)
- **Quality Scoring Guide**: [references/quality-scoring.md](references/quality-scoring.md)
- **Troubleshooting**: [references/troubleshooting.md](references/troubleshooting.md)
- **Complete Examples**: [references/examples.md](references/examples.md)
- **Migration Guide**: [references/migration.md](references/migration.md)

## Path to 90/100 Checklist

1. Use plain object schemas (not `z.object()`)
2. Remove `.optional()`/`.default()` from schemas (handle in handler)
3. Add comprehensive tool descriptions (2-4 sentences)
4. Include annotations in all tools (inside config object)
5. Create 3-5 workflow prompts (use `z.string().optional()` for args)
6. Add icon.svg to repository root
7. Make all config optional or with defaults
8. Export configSchema from index.ts
9. Remove configSchema from smithery.yaml (for TypeScript)
10. Lint with `npx tsc --noEmit` before building
11. Test locally with MCP Inspector
