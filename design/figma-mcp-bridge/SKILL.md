---
name: figma-mcp-bridge
description: Stream live Figma document data to AI tools via MCP server, bypassing API rate limits for free users
triggers:
  - connect to figma and get design data
  - extract components from my figma file
  - analyze figma design structure
  - get styles and variables from figma
  - screenshot figma nodes
  - work with multiple figma files simultaneously
  - bypass figma api rate limits
  - build ui from figma designs
---

# Figma MCP Bridge

> Skill by [ara.so](https://ara.so) — Design Skills collection

Figma MCP Bridge is a plugin + MCP server that streams live Figma document data to AI tools without hitting Figma API rate limits. It supports multiple Figma files connected simultaneously, allowing AI agents to query design data, extract components, get styles, and export screenshots.

## Installation

### 1. Add MCP Server to AI Tool

Add to your MCP configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` for Claude Desktop, or similar for Cursor/Windsurf):

```json
{
  "mcpServers": {
    "figma-bridge": {
      "command": "npx",
      "args": ["-y", "@gethopp/figma-mcp-bridge"]
    }
  }
}
```

### 2. Install Figma Plugin

Download the plugin from the [latest release](https://github.com/gethopp/figma-mcp-bridge/releases), then in Figma:
1. Go to `Plugins > Development > Import plugin from manifest`
2. Select the `manifest.json` file from the `plugin/` folder

### 3. Usage

1. Open your Figma file
2. Run the "Figma MCP Bridge" plugin
3. The plugin shows "Connected" when the MCP server is active
4. Start prompting your AI tool

For multiple files, open the plugin in each Figma file — all connections stay active.

## Available Tools

### `list_files`

List all connected Figma files (useful for multi-file workflows).

```typescript
// Agent will call this to discover available files
{
  "files": [
    {
      "fileKey": "abc123def456",
      "name": "Design System",
      "connected": true
    },
    {
      "fileKey": "xyz789uvw012",
      "name": "Mobile App",
      "connected": true
    }
  ]
}
```

### `get_document`

Get the complete Figma page document tree.

```typescript
// Single file (auto-detected)
get_document()

// Multi-file (specify fileKey)
get_document({ fileKey: "abc123def456" })

// Response includes full node tree
{
  "id": "0:1",
  "type": "PAGE",
  "name": "Homepage",
  "children": [
    {
      "id": "4029:12345",
      "type": "FRAME",
      "name": "Hero Section",
      "children": [...]
    }
  ]
}
```

### `get_selection`

Get currently selected nodes in Figma.

```typescript
get_selection({ fileKey: "abc123def456" })

// Returns array of selected nodes
{
  "selection": [
    {
      "id": "4029:12345",
      "type": "FRAME",
      "name": "Button",
      "absoluteBoundingBox": {
        "x": 100,
        "y": 200,
        "width": 120,
        "height": 40
      }
    }
  ]
}
```

### `get_node`

Get a specific node by ID (colon format required).

```typescript
get_node({ 
  nodeId: "4029:12345",
  fileKey: "abc123def456" // optional
})

// Returns detailed node data
{
  "id": "4029:12345",
  "type": "FRAME",
  "name": "Button",
  "backgroundColor": { "r": 0.2, "g": 0.5, "b": 1, "a": 1 },
  "children": [...],
  "layoutMode": "HORIZONTAL",
  "paddingLeft": 16,
  "paddingRight": 16
}
```

### `get_styles`

Get all local paint, text, effect, and grid styles.

```typescript
get_styles({ fileKey: "abc123def456" })

// Returns style definitions
{
  "paintStyles": {
    "primary-blue": {
      "id": "S:abc123",
      "name": "Primary/Blue",
      "type": "SOLID",
      "color": { "r": 0.2, "g": 0.5, "b": 1 }
    }
  },
  "textStyles": {
    "heading-1": {
      "id": "S:def456",
      "name": "Heading/H1",
      "fontSize": 32,
      "fontFamily": "Inter",
      "fontWeight": 700
    }
  }
}
```

### `get_metadata`

Get file name, pages list, and current page info.

```typescript
get_metadata({ fileKey: "abc123def456" })

// Returns file metadata
{
  "fileName": "Design System",
  "pages": [
    { "id": "0:1", "name": "Homepage" },
    { "id": "0:2", "name": "Components" }
  ],
  "currentPage": {
    "id": "0:1",
    "name": "Homepage"
  }
}
```

### `get_design_context`

Get a depth-limited tree optimized for understanding design context (faster than full document).

```typescript
get_design_context({ 
  maxDepth: 3,
  fileKey: "abc123def456" 
})

// Returns simplified tree
{
  "id": "0:1",
  "type": "PAGE",
  "name": "Homepage",
  "children": [
    {
      "id": "4029:1",
      "type": "FRAME",
      "name": "Hero Section",
      "children": "..." // Truncated at maxDepth
    }
  ]
}
```

### `get_variable_defs`

Get all variable collections, modes, and values (design tokens).

```typescript
get_variable_defs({ fileKey: "abc123def456" })

// Returns design tokens
{
  "collections": [
    {
      "id": "VariableCollectionId:1",
      "name": "Colors",
      "modes": [
        { "modeId": "1:0", "name": "Light" },
        { "modeId": "1:1", "name": "Dark" }
      ],
      "variables": [
        {
          "id": "VariableID:2",
          "name": "color/primary",
          "resolvedType": "COLOR",
          "valuesByMode": {
            "1:0": { "r": 0.2, "g": 0.5, "b": 1, "a": 1 },
            "1:1": { "r": 0.4, "g": 0.7, "b": 1, "a": 1 }
          }
        }
      ]
    }
  ]
}
```

### `get_screenshot`

Export nodes as PNG/SVG/JPG/PDF (base64-encoded).

```typescript
get_screenshot({
  nodeIds: ["4029:12345", "4029:67890"],
  format: "PNG", // PNG | SVG | JPG | PDF
  scale: 2, // optional, default 1
  fileKey: "abc123def456" // optional
})

// Returns base64-encoded images
{
  "screenshots": [
    {
      "nodeId": "4029:12345",
      "format": "PNG",
      "data": "iVBORw0KGgoAAAANSUhEUgAA..." // base64
    }
  ]
}
```

### `save_screenshots`

Export and save screenshots directly to local filesystem.

```typescript
save_screenshots({
  nodeIds: ["4029:12345"],
  format: "PNG",
  outputDir: "/path/to/output",
  fileKey: "abc123def456"
})

// Saves files and returns paths
{
  "savedFiles": [
    {
      "nodeId": "4029:12345",
      "path": "/path/to/output/Button_4029-12345.png"
    }
  ]
}
```

## Common Patterns

### Building UI from Figma Components

```typescript
// 1. Get the component you want to implement
const node = await get_node({ nodeId: "4029:12345" });

// 2. Extract styles and properties
const styles = await get_styles();

// 3. Get design tokens if using variables
const variables = await get_variable_defs();

// 4. Screenshot for visual reference
const screenshot = await get_screenshot({ 
  nodeIds: ["4029:12345"],
  format: "PNG",
  scale: 2
});

// 5. Build the component using extracted data
// Agent will generate React/Vue/etc. code based on:
// - node.layoutMode (HORIZONTAL/VERTICAL)
// - node.padding*, node.itemSpacing
// - node.fills, node.strokes
// - node.children structure
```

### Extracting Design System

```typescript
// Get all styles
const styles = await get_styles();

// Get all variables (design tokens)
const variables = await get_variable_defs();

// Get component library structure
const context = await get_design_context({ maxDepth: 2 });

// Generate CSS/Tailwind/styled-components config
// Agent creates design token files from this data
```

### Multi-File Workflow

```typescript
// List all connected files
const files = await list_files();

// Work with specific files
const designSystemStyles = await get_styles({ 
  fileKey: files[0].fileKey 
});

const appComponents = await get_document({ 
  fileKey: files[1].fileKey 
});

// Cross-reference components across files
```

### Component Analysis

```typescript
// Get current selection
const selection = await get_selection();

// Analyze each selected component
for (const node of selection.selection) {
  // Get detailed data
  const details = await get_node({ nodeId: node.id });
  
  // Check for auto-layout
  if (details.layoutMode) {
    console.log(`Uses auto-layout: ${details.layoutMode}`);
    console.log(`Gap: ${details.itemSpacing}px`);
  }
  
  // Extract text styles
  if (details.type === "TEXT") {
    console.log(`Font: ${details.fontFamily} ${details.fontSize}px`);
  }
}
```

## Configuration

### Local Development Setup

```bash
# Clone repository
git clone git@github.com:gethopp/figma-mcp-bridge.git
cd figma-mcp-bridge

# Build server
cd server
npm install
npm run build

# Build plugin
cd ../plugin
bun install
bun run build
```

### MCP Config for Local Development

```json
{
  "mcpServers": {
    "figma-bridge": {
      "command": "node",
      "args": ["/absolute/path/to/figma-mcp-bridge/server/dist/index.js"]
    }
  }
}
```

## Architecture

The bridge uses a leader-follower architecture to support multiple AI tool instances:

- **Leader**: Maintains WebSocket connection to Figma plugin on port 1994
- **Followers**: Proxy requests to leader via HTTP
- **Election**: Automatic leader election if primary instance dies
- **Multi-file**: Registry keyed by `fileKey` for simultaneous file connections

WebSocket endpoint: `ws://localhost:1994/ws`  
Health check: `http://localhost:1994/ping`  
RPC endpoint: `http://localhost:1994/rpc`

## Troubleshooting

### Plugin Not Connecting

1. Verify plugin is running in Figma (should show "Connected")
2. Check MCP server is running (look for port 1994)
3. Restart your AI tool to reload MCP configuration
4. Check browser console in Figma for WebSocket errors

### "No Figma file connected" Error

1. Open the Figma MCP Bridge plugin in your Figma file
2. Wait for "Connected" status
3. Try the command again
4. For multi-file: ensure you're using correct `fileKey` from `list_files`

### Tools Not Appearing

1. Verify MCP configuration JSON is valid
2. Restart AI tool completely
3. Check AI tool's MCP logs (Claude: `~/Library/Logs/Claude/`)
4. Ensure `npx` is in PATH

### Node ID Format Errors

Node IDs must use colon format: `"4029:12345"` not `"4029-12345"`

### Screenshot Export Fails

1. Ensure nodes are visible in viewport
2. Try reducing scale parameter
3. For large exports, use `save_screenshots` instead of `get_screenshot`
4. Check node IDs are correct (use `get_selection` to verify)

### Multiple AI Tools Conflict

Only one leader at a time. Others become followers automatically. If issues:
1. Close all AI tool instances
2. Kill any orphaned Node processes on port 1994
3. Restart one AI tool at a time

### Rate Limit Workarounds

This tool bypasses Figma API limits, but note:
- Large documents may take time to serialize
- Use `get_design_context` with `maxDepth` for faster queries
- Cache results in your prompts when possible
- For repeated screenshot exports, batch node IDs
