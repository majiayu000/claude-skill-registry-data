---
name: figma-ui-mcp-bridge
description: Bridge AI assistants to Figma Desktop via MCP — draw UI with JavaScript, read designs as structured data, extract screenshots and tokens
triggers:
  - "connect to Figma and draw a UI"
  - "create a design in Figma using AI"
  - "read the selected Figma frame"
  - "extract design tokens from Figma"
  - "take a screenshot of the Figma canvas"
  - "generate a design system rule sheet"
  - "draw a mobile app screen in Figma"
  - "get component instances from Figma"
---

# Figma UI MCP Bridge

> Skill by [ara.so](https://ara.so) — Design Skills collection

Bidirectional MCP bridge between AI assistants and Figma Desktop. Let Claude Code, Cursor, Windsurf, VS Code Copilot, or any MCP-compatible IDE draw UI directly on Figma canvas via JavaScript and read existing designs back as structured data, screenshots, or code-ready tokens. Works entirely over localhost — no Figma API key required.

**Requires Figma Desktop** (web app cannot access localhost).

## Architecture

```
AI Agent ─figma_write─▶ MCP Server ─HTTP (localhost:38451)─▶ Figma Plugin ─▶ Figma Document
AI Agent ◀figma_read──── MCP Server ◀HTTP (localhost:38451)─ Figma Plugin ◀─ Figma Document
```

The MCP server starts an HTTP server on `localhost:38451`. The Figma plugin uses long polling (8s hold, <100ms latency). Multi-instance support — multiple Figma files can connect simultaneously via `sessionId`.

## Installation

### Step 1: Add MCP Server

**Claude Code (CLI):**
```bash
# Project scope
claude mcp add figma-ui-mcp -- npx figma-ui-mcp

# Global scope
claude mcp add --scope user figma-ui-mcp -- npx figma-ui-mcp
```

**Claude Desktop:**
Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):
```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "figma-ui-mcp"]
    }
  }
}
```

**Cursor:**
Edit `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global):
```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "figma-ui-mcp"]
    }
  }
}
```

**VS Code / Copilot:**
Edit `.vscode/mcp.json`:
```json
{
  "mcp": {
    "servers": {
      "figma": {
        "command": "npx",
        "args": ["-y", "figma-ui-mcp"]
      }
    }
  }
}
```

**Windsurf:**
Edit `~/.codeium/windsurf/mcp_config.json`:
```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "figma-ui-mcp"]
    }
  }
}
```

**⚠️ MUST restart IDE/AI client after adding MCP server** (quit and reopen — saving config is not enough).

### Step 2: Install Figma Plugin

1. Download `plugin.zip` from https://github.com/TranHoaiHung/figma-ui-mcp/raw/main/plugin.zip
2. Unzip anywhere on your machine
3. Open **Figma Desktop** (required)
4. **Plugins → Development → Import plugin from manifest...**
5. Select `manifest.json` from unzipped folder
6. Run **Plugins → Development → Figma UI MCP Bridge**

Green dot = connected. Orange = server not reachable.

### Step 3: Verify Connection

```javascript
// AI will call this automatically when you say "connect to Figma"
figma_status()
// Returns: { status: "ok", fileName, pageName, pluginVersion, sessions: [...] }
```

## Core MCP Tools

### `figma_status`

Check connection status and list active sessions.

```javascript
figma_status()
// Response:
// {
//   status: "ok",
//   fileName: "My Project",
//   pageName: "Page 1",
//   pluginVersion: "2.5.12",
//   sessions: [
//     { sessionId: "abc123", fileName: "My Project", pageName: "Page 1" }
//   ]
// }
```

### `figma_docs`

Get full API reference and examples. Call once at session start to load capabilities.

```javascript
figma_docs()
// Returns: markdown reference with all operations, params, examples
```

### `figma_rules`

Generate design system rule sheet — color tokens, typography styles, variables (all modes), component catalog. Equivalent to official Figma MCP's `create_design_system_rules`. Call once per file.

```javascript
figma_rules({ sessionId: "abc123" }) // optional sessionId
// Returns: markdown rule sheet with all design tokens
```

### `figma_write`

Execute JavaScript operations on Figma canvas. Takes `operation` (string) and `params` (object).

**Single operation:**
```javascript
figma_write({
  operation: "create",
  params: {
    type: "FRAME",
    name: "Login Screen",
    width: 390,
    height: 844,
    fill: "#FFFFFF",
    children: [
      {
        type: "TEXT",
        name: "Title",
        characters: "Welcome Back",
        fontSize: 32,
        fontFamily: "Inter",
        fontWeight: 700,
        fill: "#000000",
        x: 40,
        y: 100
      }
    ]
  }
})
```

**Batch operations:**
```javascript
figma_write({
  operations: [
    {
      operation: "create",
      params: { type: "FRAME", name: "Container", width: 800, height: 600 }
    },
    {
      operation: "modify",
      params: { id: "result[0]", fill: "#F5F5F5" }
    }
  ]
})
```

Use `result[0]`, `result[1]` to reference previous operation results.

### `figma_read`

Read data from Figma. Takes `operation` and `params`.

**Get page structure:**
```javascript
figma_read({
  operation: "get_page_nodes",
  params: {}
})
// Returns: { nodes: [...], totalNodes: 42 }
```

**Get selection:**
```javascript
figma_read({
  operation: "get_selection",
  params: {}
})
// Returns: [{ id, name, type, x, y, width, height, ... }]
```

**Take screenshot:**
```javascript
figma_read({
  operation: "screenshot",
  params: { nodeId: "123:456", scale: 2 }
})
// Returns: { base64: "data:image/png;base64,..." }
```

**Get design context (AI-optimized):**
```javascript
figma_read({
  operation: "get_design_context",
  params: { nodeId: "123:456" }
})
// Returns: flex layout, token-resolved colors, typography with style names,
// component instances with variant properties — best for code generation
```

**Get component map:**
```javascript
figma_read({
  operation: "get_component_map",
  params: { frameId: "123:456" }
})
// Returns: { instances: [{ componentSetName, variantLabel, properties, suggestedImport }] }
```

**Get CSS:**
```javascript
figma_read({
  operation: "get_css",
  params: { nodeId: "123:456" }
})
// Returns: { css: "display: flex; flex-direction: column; ..." }
```

## Common Operations

### Create Nodes

**Frame with auto-layout:**
```javascript
figma_write({
  operation: "create",
  params: {
    type: "FRAME",
    name: "Card",
    width: 320,
    height: 240,
    fill: "#FFFFFF",
    cornerRadius: 16,
    layoutMode: "VERTICAL",
    paddingTop: 24,
    paddingRight: 24,
    paddingBottom: 24,
    paddingLeft: 24,
    itemSpacing: 16,
    effects: [
      {
        type: "DROP_SHADOW",
        color: "rgba(0,0,0,0.1)",
        offsetX: 0,
        offsetY: 4,
        blur: 12
      }
    ]
  }
})
```

**Text with typography:**
```javascript
figma_write({
  operation: "create",
  params: {
    type: "TEXT",
    name: "Heading",
    characters: "Design System",
    fontSize: 48,
    fontFamily: "Inter",
    fontWeight: 700,
    lineHeight: { value: 120, unit: "PERCENT" },
    letterSpacing: { value: -2, unit: "PERCENT" },
    fill: "#1A1A1A"
  }
})
```

**Rectangle with gradient:**
```javascript
figma_write({
  operation: "create",
  params: {
    type: "RECTANGLE",
    name: "Gradient BG",
    width: 800,
    height: 600,
    fill: {
      type: "LINEAR_GRADIENT",
      angle: 135,
      stops: [
        { position: 0, color: "#667EEA" },
        { position: 1, color: "#764BA2" }
      ]
    }
  }
})
```

**Icon from library:**
```javascript
figma_write({
  operation: "createIcon",
  params: {
    name: "home",
    library: "ionicons", // ionicons | fluent | bootstrap | phosphor | tabler-filled | tabler-outline | lucide
    size: 24,
    fill: "#000000",
    x: 100,
    y: 100
  }
})
```

**Component instance with overrides:**
```javascript
figma_write({
  operation: "instantiate",
  params: {
    componentKey: "abc123",
    overrides: {
      "ButtonLabel": { text: "Submit", fill: "#FFFFFF" },
      "Icon": { visible: false }
    }
  }
})
```

### Modify Nodes

**Change properties:**
```javascript
figma_write({
  operation: "modify",
  params: {
    id: "123:456",
    fill: "#FF5733",
    width: 400,
    opacity: 0.8
  }
})
```

**Apply design tokens:**
```javascript
figma_write({
  operation: "applyVariable",
  params: {
    nodeId: "123:456",
    field: "fills", // fills | strokes | width | height | cornerRadius | paddingTop | etc.
    variableName: "color/primary"
  }
})
```

**Apply text style:**
```javascript
figma_write({
  operation: "applyTextStyle",
  params: {
    nodeId: "123:456",
    styleName: "Heading/H1"
  }
})
```

### Setup Design Tokens

**Color tokens (all modes):**
```javascript
figma_write({
  operation: "setupDesignTokens",
  params: {
    colors: {
      "color/primary": {
        Light: "#667EEA",
        Dark: "#A5B4FC"
      },
      "color/background": {
        Light: "#FFFFFF",
        Dark: "#1A1A1A"
      }
    }
  }
})
```

**Typography tokens:**
```javascript
figma_write({
  operation: "setupDesignTokens",
  params: {
    fontSizes: {
      "size/xs": { Compact: 12, Comfortable: 14, Large: 16 },
      "size/sm": { Compact: 14, Comfortable: 16, Large: 18 },
      "size/md": { Compact: 16, Comfortable: 18, Large: 20 }
    },
    fonts: {
      "font/primary": { Compact: "Inter", Comfortable: "Inter", Large: "SF Pro" }
    },
    textStyles: [
      {
        name: "Heading/H1",
        fontFamily: "font/primary",
        fontSize: "size/md",
        fontWeight: 700,
        lineHeightPercent: 120
      }
    ]
  }
})
```

### Prototyping

**Add click interaction:**
```javascript
figma_write({
  operation: "setReactions",
  params: {
    nodeId: "123:456",
    reactions: [
      {
        trigger: "ON_CLICK", // ON_CLICK | ON_HOVER | ON_PRESS | ON_DRAG
        action: "NAVIGATE", // NAVIGATE | OVERLAY | SWAP | SCROLL_TO | CLOSE
        destinationId: "789:012",
        transition: "SMART_ANIMATE", // SMART_ANIMATE | DISSOLVE | SLIDE_IN | PUSH | etc.
        duration: 300,
        easing: "EASE_OUT"
      }
    ]
  }
})
```

**Set scroll behavior:**
```javascript
figma_write({
  operation: "setScrollBehavior",
  params: {
    nodeId: "123:456",
    overflow: "VERTICAL" // HORIZONTAL | VERTICAL | BOTH | NONE
  }
})
```

### Component Variants

**Set variant properties:**
```javascript
figma_write({
  operation: "setComponentProperties",
  params: {
    instanceId: "123:456",
    properties: {
      "State": "Primary",
      "Size": "Large"
    }
  }
})
```

**Swap component:**
```javascript
figma_write({
  operation: "swapComponent",
  params: {
    instanceId: "123:456",
    newComponentKey: "def789"
  }
})
```

## Read Operations Reference

| Operation | Purpose | Key Params |
|-----------|---------|------------|
| `get_page_nodes` | List all top-level nodes | `{ maxDepth }` |
| `get_selection` | Get selected nodes | `{}` |
| `get_node_detail` | Full node data with resolved variables/styles | `{ nodeId }` |
| `get_design_context` | AI-optimized payload for code generation | `{ nodeId }` |
| `get_component_map` | List component instances with variants | `{ frameId }` |
| `get_unmapped_components` | Find components missing code mapping | `{ frameId }` |
| `get_css` | Generate CSS from node | `{ nodeId }` |
| `screenshot` | Capture PNG | `{ nodeId, scale }` |
| `get_variables` | All variables (all modes) | `{}` |
| `get_styles` | All color/text/effect styles | `{}` |

## Multi-Instance Sessions

When multiple Figma files are open, each plugin instance has a unique `sessionId`. Target specific files:

```javascript
// List all sessions
figma_status()
// { sessions: [{ sessionId: "abc123", fileName: "App Design" }, ...] }

// Write to specific session
figma_write({
  operation: "create",
  params: { type: "FRAME", name: "Test" },
  sessionId: "abc123"
})

// Read from specific session
figma_read({
  operation: "get_page_nodes",
  params: {},
  sessionId: "abc123"
})
```

Omit `sessionId` to use the first connected session.

## Common Patterns

### Design System Bootstrap

```javascript
// Step 1: Generate rule sheet
figma_rules()

// Step 2: Setup color tokens
figma_write({
  operation: "setupDesignTokens",
  params: {
    colors: {
      "color/primary": { Light: "#667EEA", Dark: "#A5B4FC" },
      "color/text": { Light: "#1A1A1A", Dark: "#F5F5F5" }
    }
  }
})

// Step 3: Setup typography
figma_write({
  operation: "setupDesignTokens",
  params: {
    fontSizes: {
      "size/h1": { Compact: 32, Comfortable: 40, Large: 48 }
    },
    textStyles: [
      {
        name: "Heading/H1",
        fontSize: "size/h1",
        fontWeight: 700
      }
    ]
  }
})
```

### Design-to-Code Workflow

```javascript
// Step 1: Get design context
const context = await figma_read({
  operation: "get_design_context",
  params: { nodeId: "123:456" }
})
// Returns: flex layout, resolved color tokens, typography with style names

// Step 2: Get component map
const components = await figma_read({
  operation: "get_component_map",
  params: { frameId: "123:456" }
})
// Returns: { instances: [{ componentSetName: "Button", variantLabel: "State=Primary", suggestedImport: "@/components/Button" }] }

// Step 3: Get CSS
const css = await figma_read({
  operation: "get_css",
  params: { nodeId: "123:456" }
})
// Returns: { css: "display: flex; ..." }
```

### Batch Create + Reference

```javascript
figma_write({
  operations: [
    // Create container
    {
      operation: "create",
      params: {
        type: "FRAME",
        name: "Container",
        width: 800,
        height: 600,
        layoutMode: "VERTICAL",
        itemSpacing: 24
      }
    },
    // Create child, insert into container
    {
      operation: "create",
      params: {
        type: "RECTANGLE",
        name: "Header",
        width: 800,
        height: 80,
        fill: "#667EEA",
        parentId: "result[0]" // Reference first operation's result
      }
    }
  ]
})
```

## Troubleshooting

### Plugin shows orange dot
- **Cause:** MCP server not running or wrong port
- **Fix:** Restart IDE/AI client (MCP server loads on startup). Check server logs for port conflicts.

### "Plugin not connected" error
- **Cause:** Plugin not running in Figma Desktop
- **Fix:** Figma Desktop → Plugins → Development → Figma UI MCP Bridge. Must be Figma Desktop (web app cannot access localhost).

### Operations fail silently
- **Cause:** Invalid node ID or operation params
- **Fix:** Call `figma_read get_page_nodes` first to get valid node IDs. Check `figma_docs` for param schema.

### Font not found
- **Cause:** Font not installed on system
- **Fix:** Use `fontFamily: "Inter"` (ships with Figma) or install custom fonts locally.

### Multi-instance targeting wrong file
- **Cause:** No `sessionId` specified with multiple files open
- **Fix:** Call `figma_status` to list sessions, then pass `sessionId` to `figma_write`/`figma_read`.

### Variable binding fails
- **Cause:** Variable doesn't exist or wrong type
- **Fix:** Call `figma_read get_variables` first. Ensure `FLOAT` variables for dimensions, `COLOR` for fills.

## Best Practices

1. **Always call `figma_docs` at session start** to load API reference into AI context
2. **Call `figma_rules` once per file** to get design system tokens before generating code
3. **Use `get_design_context` for code generation** — single call returns all layout/color/typography data
4. **Use `get_component_map` for import statements** — returns `suggestedImport` paths
5. **Batch operations when possible** — reduces round-trips (single `figma_write` with `operations` array)
6. **Reference previous results** with `result[0]`, `result[1]` in batch operations
7. **Use design tokens** (`applyVariable`) instead of hardcoded colors for maintainability
8. **Check `figma_status` first** to verify connection and list sessions
9. **Use `sessionId`** when multiple Figma files are open to avoid ambiguity
10. **Take screenshots** to verify AI-generated designs match intent

## Version Updates

```bash
# Get latest version + plugin path
npx figma-ui-mcp@latest --version

# Re-link Figma plugin (manual step required)
# Figma Desktop → Plugins → Development → Manage plugins in development
# Remove old → Import from manifest → Select new plugin path
```

Plugin does **not** auto-update — must re-link after npm update.
