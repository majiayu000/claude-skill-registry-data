---
name: mcp-integration
description: Manage MCP (Model Context Protocol) servers - discover, analyze, execute tools. Use for external service integrations, browser automation, documentation lookup, AI image/video generation, database connections, and any MCP server management.
---

# MCP Integration

## Overview

MCP (Model Context Protocol) enables Claude to connect with external tools and services through standardized server interfaces.

**Key Benefits:**
- Connect to external APIs and services
- Browser automation (Playwright)
- Documentation lookup (context7)
- Design file editing (pencil)
- AI multimodal (Gemini for images/videos)
- Database connections
- Custom integrations

## Available MCP Servers

### Built-in Servers

| Server | Purpose | Example Tools |
|--------|---------|---------------|
| `context7` | Documentation lookup | `resolve-library-id`, `query-docs` |
| `playwright` | Browser automation | `browser_navigate`, `browser_click`, `browser_snapshot` |
| `pencil` | Design file editing | `batch_get`, `batch_design`, `get_screenshot` |

### Check Available Servers

```bash
# List configured MCP servers
claude mcp list

# Or check settings
cat ~/.claude/settings.json | grep -A 20 "mcpServers"
```

## Tool Naming Convention

```
mcp__{server}__{tool}
```

**Examples:**
```
mcp__context7__resolve-library-id
mcp__context7__query-docs
mcp__playwright__browser_navigate
mcp__playwright__browser_snapshot
mcp__pencil__batch_get
```

## Common Use Cases

### 1. Documentation Lookup (context7)

When implementing unfamiliar library/framework:

```typescript
// Step 1: Resolve library ID
mcp__context7__resolve-library-id("react-query")
// Returns: "/tanstack/query"

// Step 2: Query specific topic
mcp__context7__query-docs({
  libraryId: "/tanstack/query",
  topic: "useQuery hooks"
})
// Returns: Latest documentation
```

**When to use:**
- Implementing new library
- Checking latest API changes
- Finding best practices

### 2. Browser Automation (playwright)

For E2E testing and web automation:

```typescript
// Navigate to page
mcp__playwright__browser_navigate({ url: "http://localhost:3000" })

// Take snapshot of current state
mcp__playwright__browser_snapshot()

// Click element
mcp__playwright__browser_click({ selector: "button#submit" })

// Fill form
mcp__playwright__browser_fill_form({
  selector: "form#login",
  values: { email: "test@test.com", password: "password" }
})

// Take screenshot
mcp__playwright__browser_take_screenshot({ path: "screenshot.png" })

// Close browser
mcp__playwright__browser_close()
```

**When to use:**
- E2E testing
- Visual verification
- Form automation
- Screenshot capture

### 3. Design Files (pencil)

For working with .pen design files:

```typescript
// Get current editor state
mcp__pencil__get_editor_state()

// Read nodes from design
mcp__pencil__batch_get({ patterns: ["**/Button*"] })

// Modify design
mcp__pencil__batch_design({
  operations: [
    'newButton=I("parent-id", { type: "button", text: "Click me" })'
  ]
})

// Get screenshot
mcp__pencil__get_screenshot({ nodeId: "some-node-id" })
```

**When to use:**
- UI/UX design work
- Component design
- Visual prototyping

## Integration in Super Agent

### For PM

When assigning tasks that need external services:

```markdown
## Task 3.5: Implement Payment Integration

**MCP Required:** Yes
**Server:** stripe (if configured)

Instructions:
1. Use context7 to lookup Stripe SDK docs
2. Implement payment flow
3. Use playwright for E2E testing
```

### For Specialists

Before using MCP tools:

```bash
# 1. Check if MCP server is available
claude mcp list

# 2. Check tool schema
# Tools are available as mcp__{server}__{tool}

# 3. Execute tool
# Use directly in Claude conversation
```

### For DevOps/QA

Automated testing with playwright:

```typescript
// Test flow example
async function testLoginFlow() {
  // Navigate
  await mcp__playwright__browser_navigate({ url: "http://localhost:3000/login" })

  // Fill form
  await mcp__playwright__browser_fill_form({
    selector: "form",
    values: { email: "test@test.com", password: "password" }
  })

  // Click submit
  await mcp__playwright__browser_click({ selector: "button[type=submit]" })

  // Verify redirect
  const snapshot = await mcp__playwright__browser_snapshot()
  // Check snapshot for dashboard content
}
```

## Configuration

### Adding MCP Servers

Edit `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@anthropic/context7-mcp"]
    },
    "playwright": {
      "command": "npx",
      "args": ["@anthropic/playwright-mcp"]
    },
    "custom-server": {
      "command": "node",
      "args": ["/path/to/your/mcp-server.js"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

### Project-Specific Configuration

Add to `.claude/settings.json` in project root:

```json
{
  "mcpServers": {
    "project-db": {
      "command": "npx",
      "args": ["@prisma/mcp-server"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Server not found` | MCP server not configured | Add to settings.json |
| `Tool not found` | Wrong tool name | Check available tools |
| `Connection failed` | Server crashed | Restart Claude Code |
| `Permission denied` | Missing env vars | Set required env variables |

## Best Practices

1. **Check availability first** - Verify MCP server is configured
2. **Handle errors gracefully** - Services may be unavailable
3. **Use appropriate server** - Match tool to task
4. **Document MCP usage** - Note in task logs for knowledge base
5. **Don't expose secrets** - Use env vars for API keys

## Quick Reference

| Task | Server | Tool |
|------|--------|------|
| Lookup docs | context7 | `query-docs` |
| Navigate browser | playwright | `browser_navigate` |
| Click element | playwright | `browser_click` |
| Take screenshot | playwright | `browser_take_screenshot` |
| Fill form | playwright | `browser_fill_form` |
| Get browser state | playwright | `browser_snapshot` |
| Read design | pencil | `batch_get` |
| Edit design | pencil | `batch_design` |

## Integration with Other Skills

- Use with `test-driven-development` for E2E test implementation
- Use with `systematic-debugging` for browser-based debugging
- Use with `visual-preview` for design documentation
- Use with `qa-testing` for automated test suites
