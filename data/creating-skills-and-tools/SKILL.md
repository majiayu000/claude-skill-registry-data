---
name: creating-skills-and-tools
description: Guidelines for creating new Agent Skills and MCP tools for this WordPress MCP server. Use when adding new capabilities, creating skills, or registering MCP tools.
---

# Creating Skills and Tools

This skill provides guidelines for extending the WordPress MCP Server with new Agent Skills and MCP tools.

## Core Principle: Minimal Tools, Maximum Flexibility

Before creating anything new, ask yourself:

1. **Can this be done with `wp_cli`?** → If yes, don't create a new tool
2. **Is this WordPress-specific?** → Use WP-CLI commands via `wp_cli`
3. **Is this a reusable workflow?** → Create an Agent Skill, not a tool

## When to Create What

| Need | Solution |
|------|----------|
| Run a WordPress command | Use existing `wp_cli` tool |
| Complex multi-step workflow | Create an Agent Skill |
| Non-WordPress SSH operation | Evaluate if `executeSshCommand` suffices |
| Truly new capability | Create a new MCP tool (rare) |

## Creating Agent Skills

### Skill Structure

```
.github/skills/
└── your-skill-name/
    ├── SKILL.md           # Required: Main instructions
    ├── reference.md       # Optional: Detailed reference
    └── scripts/           # Optional: Utility scripts
        └── helper.py
```

### SKILL.md Template

See [skill-template.md](skill-template.md) for the full template.

Key requirements:
- YAML frontmatter with `name` and `description`
- Name: lowercase, hyphens only, max 64 chars
- Description: What it does AND when to use it

### Progressive Disclosure

Keep SKILL.md lean (<500 lines). Split into separate files:
- Put detailed references in separate `.md` files
- Link with: `See [reference.md](reference.md) for details`
- Claude loads files only when needed

### Best Practices

1. **Be concise**: Claude is smart, don't over-explain
2. **One level deep**: Don't nest references (SKILL.md → file.md, not SKILL.md → a.md → b.md)
3. **Use examples**: Input/output pairs are clearer than descriptions
4. **Forward slashes**: Always use `/` in paths, never `\`

## Creating MCP Tools (Use Sparingly!)

### When to Create a Tool

Only create a new MCP tool when:
1. It cannot be done via `wp_cli` or existing tools
2. It provides significant value that justifies the context cost
3. It's a fundamental capability, not a convenience wrapper

### Tool Registration Pattern

```typescript
server.registerTool(
  "tool_name",
  {
    description: "Clear description of what the tool does",
    inputSchema: {
      param1: z.string().describe("What this parameter is for"),
      param2: z.number().optional().describe("Optional parameter"),
    },
  },
  async ({ param1, param2 }) => {
    // Implementation
    return {
      content: [{ type: "text", text: "Result message" }],
    };
  }
);
```

### Tool Naming

- Use `snake_case` for tool names
- Be descriptive: `test_ssh_connection` not `test_ssh`
- Prefix related tools: `wp_*` for WordPress tools

## Updating the Skills Catalog

After creating a skill, update `.github/copilot-instructions.md`:

```markdown
| Skill Name | Description | Path |
|------------|-------------|------|
| your-skill-name | Brief description | `.github/skills/your-skill-name/SKILL.md` |
```

## Anti-Patterns to Avoid

❌ **Don't create specialized WordPress tools**
```typescript
// BAD - Creates context bloat
server.registerTool("get_plugins", ...)
server.registerTool("activate_plugin", ...)
server.registerTool("update_plugin", ...)
```

✅ **Use the generic wp_cli tool instead**
```typescript
// GOOD - One tool, infinite commands
wp_cli({ domain: "example.com", command: "plugin list" })
wp_cli({ domain: "example.com", command: "plugin activate akismet" })
wp_cli({ domain: "example.com", command: "plugin update --all" })
```

❌ **Don't duplicate WP-CLI documentation**
- Claude already knows WP-CLI
- Link to official docs instead

❌ **Don't create deeply nested skill files**
- Keep references one level deep from SKILL.md

## References

- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Anthropic: Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [WP-CLI Commands](https://developer.wordpress.org/cli/commands/)
