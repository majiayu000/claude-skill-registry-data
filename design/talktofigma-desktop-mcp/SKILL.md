---
name: talktofigma-desktop-mcp
description: Bridge Figma designs with AI assistants using TalkToFigma Desktop via Model Context Protocol
triggers:
  - connect to figma designs
  - read figma file layers
  - modify figma components
  - extract design tokens from figma
  - sync figma with ai tools
  - access figma via mcp
  - talk to figma desktop
  - integrate figma with cursor
---

# TalkToFigma Desktop MCP

> Skill by [ara.so](https://ara.so) — Design Skills collection.

TalkToFigma Desktop is a cross-platform desktop application that bridges Figma and AI coding assistants through the Model Context Protocol (MCP). It provides 50+ MCP tools for reading and manipulating Figma designs, enabling AI agents to directly interact with design files through a WebSocket server and stdio-based MCP servers.

## Architecture Overview

```
MCP Client (Cursor/Claude Code) → stdio MCP Server → WebSocket (port 3055) → Desktop App → Figma Plugin
```

The desktop app manages:
- **WebSocket server** on port 3055 for real-time communication
- **stdio MCP servers** spawned independently by each AI client
- **Channel-based routing** for multi-client support
- **System tray interface** for server management

## Installation

### 1. Install Desktop Application

Download from [GitHub Releases](https://github.com/grab/TalkToFigmaDesktop/releases):
- **macOS**: `TalkToFigma-v*.*.*.zip` (Universal binary)
- **Windows**: `TalkToFigma-v*.*.*.exe`

**First run on macOS**: Right-click app → "Open" → "Open" (bypass Gatekeeper)

**First run on Windows**: SmartScreen → "More info" → "Run anyway"

### 2. Install Figma Plugin

Install the [Talk to Figma MCP Plugin](https://www.figma.com/community/plugin/1485687494525374295/talk-to-figma-mcp-plugin) from Figma Community.

### 3. Configure MCP Client

**For Cursor, Claude Code, or VS Code with Cline:**

1. Launch TalkToFigma Desktop
2. Right-click tray icon → "Settings"
3. Copy the MCP configuration path shown
4. Add to your MCP client config:

**macOS** (`~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`):
```json
{
  "mcpServers": {
    "TalkToFigmaDesktop": {
      "command": "node",
      "args": [
        "/Users/yourname/Library/Application Support/TalkToFigma/mcp-server.cjs"
      ]
    }
  }
}
```

**Windows Direct Install** (`%APPDATA%\Cursor\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`):
```json
{
  "mcpServers": {
    "TalkToFigmaDesktop": {
      "command": "node",
      "args": [
        "%APPDATA%\\TalkToFigma\\mcp-server.cjs"
      ]
    }
  }
}
```

**Windows Store/MSIX**: Use the exact path from Settings page (usually under `%LOCALAPPDATA%\Packages\...\LocalCache\Roaming\TalkToFigma\mcp-server.cjs`)

## Starting the Server

1. **Launch TalkToFigma Desktop** from Applications/Start Menu
2. **Start WebSocket server**: Right-click tray icon → "Start Server"
3. **Verify status**: Tray icon should show green (🟢 Active)
4. **Open Figma**: Run the Talk to Figma MCP plugin
5. **Connect**: Plugin should show "Connected" status

## MCP Tools Reference

### Core Connection Tools

#### `join_channel`
Join a Figma file channel to start interacting with it.

**Parameters:**
- `channel` (string): Format `{file_key}:{page_id}:{view_id}`

**Usage:**
```typescript
// Extract from Figma URL: https://www.figma.com/design/ABC123/Project?node-id=1-2&t=xyz
// Format: ABC123:1:2
await use_mcp_tool("TalkToFigmaDesktop", "join_channel", {
  channel: "ABC123:1:2"
});
```

#### `leave_channel`
Leave the current Figma file channel.

```typescript
await use_mcp_tool("TalkToFigmaDesktop", "leave_channel", {});
```

### Reading Design Data

#### `get_current_page`
Get the currently active page in Figma.

```typescript
const page = await use_mcp_tool("TalkToFigmaDesktop", "get_current_page", {});
// Returns: { id: "1:2", name: "Page 1", type: "PAGE" }
```

#### `get_node_by_id`
Retrieve a specific node by its ID.

```typescript
const node = await use_mcp_tool("TalkToFigmaDesktop", "get_node_by_id", {
  nodeId: "123:456"
});
// Returns complete node data including children, properties, styles
```

#### `get_all_nodes`
Get all nodes in the current page with optional filtering.

```typescript
const allFrames = await use_mcp_tool("TalkToFigmaDesktop", "get_all_nodes", {
  type: "FRAME"
});

const allComponents = await use_mcp_tool("TalkToFigmaDesktop", "get_all_nodes", {
  type: "COMPONENT"
});
```

#### `search_nodes`
Search for nodes by name or type.

```typescript
const buttons = await use_mcp_tool("TalkToFigmaDesktop", "search_nodes", {
  query: "Button",
  type: "COMPONENT"
});
```

#### `get_selection`
Get currently selected nodes in Figma.

```typescript
const selection = await use_mcp_tool("TalkToFigmaDesktop", "get_selection", {});
// Returns: [{ id: "123:456", name: "Selected Frame", type: "FRAME" }]
```

### Creating and Modifying Nodes

#### `create_rectangle`
Create a rectangle node.

```typescript
await use_mcp_tool("TalkToFigmaDesktop", "create_rectangle", {
  name: "Background",
  x: 0,
  y: 0,
  width: 375,
  height: 812,
  fills: JSON.stringify([{
    type: "SOLID",
    color: { r: 0.95, g: 0.95, b: 0.95 }
  }])
});
```

#### `create_frame`
Create a frame container.

```typescript
await use_mcp_tool("TalkToFigmaDesktop", "create_frame", {
  name: "Mobile Screen",
  x: 100,
  y: 100,
  width: 375,
  height: 812
});
```

#### `create_text`
Create a text node.

```typescript
await use_mcp_tool("TalkToFigmaDesktop", "create_text", {
  name: "Heading",
  characters: "Welcome to TalkToFigma",
  x: 20,
  y: 40,
  fontSize: 24,
  fontName: JSON.stringify({ family: "Inter", style: "Bold" })
});
```

#### `create_component`
Create a reusable component.

```typescript
await use_mcp_tool("TalkToFigmaDesktop", "create_component", {
  name: "Button/Primary",
  x: 0,
  y: 0,
  width: 120,
  height: 44
});
```

#### `set_properties`
Modify properties of existing nodes.

```typescript
await use_mcp_tool("TalkToFigmaDesktop", "set_properties", {
  nodeId: "123:456",
  properties: JSON.stringify({
    name: "Updated Button",
    x: 50,
    y: 50,
    fills: [{
      type: "SOLID",
      color: { r: 0.2, g: 0.4, b: 0.8 }
    }]
  })
});
```

#### `delete_node`
Delete a node by ID.

```typescript
await use_mcp_tool("TalkToFigmaDesktop", "delete_node", {
  nodeId: "123:456"
});
```

### Layout and Positioning

#### `set_auto_layout`
Apply auto layout to a frame.

```typescript
await use_mcp_tool("TalkToFigmaDesktop", "set_auto_layout", {
  nodeId: "123:456",
  mode: "VERTICAL",
  padding: 16,
  spacing: 12,
  primaryAxisAlignItems: "MIN",
  counterAxisAlignItems: "CENTER"
});
```

#### `group_nodes`
Group multiple nodes together.

```typescript
await use_mcp_tool("TalkToFigmaDesktop", "group_nodes", {
  nodeIds: JSON.stringify(["123:456", "123:457", "123:458"]),
  name: "Button Group"
});
```

### Styles and Design Tokens

#### `get_local_paint_styles`
Get all local color styles.

```typescript
const colors = await use_mcp_tool("TalkToFigmaDesktop", "get_local_paint_styles", {});
// Returns: [{ id: "S:...", name: "Primary/Blue", paints: [...] }]
```

#### `get_local_text_styles`
Get all local text styles.

```typescript
const textStyles = await use_mcp_tool("TalkToFigmaDesktop", "get_local_text_styles", {});
// Returns: [{ id: "S:...", name: "Heading/H1", fontSize: 32, ... }]
```

#### `create_paint_style`
Create a new color style.

```typescript
await use_mcp_tool("TalkToFigmaDesktop", "create_paint_style", {
  name: "Brand/Primary",
  paints: JSON.stringify([{
    type: "SOLID",
    color: { r: 0.2, g: 0.4, b: 0.8 }
  }])
});
```

#### `apply_paint_style`
Apply a color style to a node.

```typescript
await use_mcp_tool("TalkToFigmaDesktop", "apply_paint_style", {
  nodeId: "123:456",
  styleId: "S:abc123..."
});
```

### Export and Assets

#### `export_node`
Export a node as an image.

```typescript
const imageData = await use_mcp_tool("TalkToFigmaDesktop", "export_node", {
  nodeId: "123:456",
  format: "PNG",
  scale: 2
});
// Returns base64-encoded image data
```

#### `get_image_fills`
Get image fill data from nodes.

```typescript
const images = await use_mcp_tool("TalkToFigmaDesktop", "get_image_fills", {
  nodeId: "123:456"
});
```

## Common Workflows

### Extract Design Tokens

```typescript
// 1. Join the Figma file
await use_mcp_tool("TalkToFigmaDesktop", "join_channel", {
  channel: "FILE_KEY:PAGE_ID:VIEW_ID"
});

// 2. Get all color styles
const colors = await use_mcp_tool("TalkToFigmaDesktop", "get_local_paint_styles", {});

// 3. Get all text styles
const typography = await use_mcp_tool("TalkToFigmaDesktop", "get_local_text_styles", {});

// 4. Convert to design tokens
const tokens = {
  colors: colors.map(style => ({
    name: style.name.replace(/\//g, '-'),
    value: rgbToHex(style.paints[0].color)
  })),
  typography: typography.map(style => ({
    name: style.name.replace(/\//g, '-'),
    fontSize: style.fontSize,
    fontFamily: style.fontName.family,
    fontWeight: style.fontName.style
  }))
};
```

### Build Component Library

```typescript
// 1. Search for all components
const components = await use_mcp_tool("TalkToFigmaDesktop", "get_all_nodes", {
  type: "COMPONENT"
});

// 2. For each component, get detailed properties
for (const comp of components) {
  const details = await use_mcp_tool("TalkToFigmaDesktop", "get_node_by_id", {
    nodeId: comp.id
  });
  
  // 3. Generate React component code
  const componentCode = generateReactComponent(details);
  // Write to file system...
}
```

### Sync Design Changes to Code

```typescript
// 1. Get current selection in Figma
const selection = await use_mcp_tool("TalkToFigmaDesktop", "get_selection", {});

// 2. For each selected node
for (const node of selection) {
  const nodeData = await use_mcp_tool("TalkToFigmaDesktop", "get_node_by_id", {
    nodeId: node.id
  });
  
  // 3. Update corresponding code file
  const cssProperties = {
    width: `${nodeData.width}px`,
    height: `${nodeData.height}px`,
    backgroundColor: rgbToHex(nodeData.fills[0].color),
    borderRadius: `${nodeData.cornerRadius}px`
  };
  
  // Update CSS/styled-components...
}
```

### Create UI from Specification

```typescript
// 1. Join channel
await use_mcp_tool("TalkToFigmaDesktop", "join_channel", {
  channel: "FILE_KEY:PAGE_ID:VIEW_ID"
});

// 2. Create mobile frame
await use_mcp_tool("TalkToFigmaDesktop", "create_frame", {
  name: "Mobile/Login",
  x: 0,
  y: 0,
  width: 375,
  height: 812
});

// 3. Get the created frame
const frames = await use_mcp_tool("TalkToFigmaDesktop", "search_nodes", {
  query: "Mobile/Login",
  type: "FRAME"
});
const frameId = frames[0].id;

// 4. Set auto layout
await use_mcp_tool("TalkToFigmaDesktop", "set_auto_layout", {
  nodeId: frameId,
  mode: "VERTICAL",
  padding: 24,
  spacing: 16
});

// 5. Add heading
await use_mcp_tool("TalkToFigmaDesktop", "create_text", {
  name: "Title",
  characters: "Welcome Back",
  fontSize: 28,
  fontName: JSON.stringify({ family: "Inter", style: "Bold" })
});

// 6. Add input fields, buttons, etc.
```

## Configuration

### Environment Variables

TalkToFigma Desktop doesn't require API keys, but the stdio server path varies by platform:

```bash
# macOS
TALKTOFIGMA_STDIO_PATH="$HOME/Library/Application Support/TalkToFigma/mcp-server.cjs"

# Windows (Direct Install)
TALKTOFIGMA_STDIO_PATH="%APPDATA%\TalkToFigma\mcp-server.cjs"

# Windows (Store/MSIX)
# Check Settings page for exact path under LocalCache
```

### WebSocket Port

Default port: `3055`

To verify the server is running:
```bash
# macOS/Linux
lsof -i :3055

# Windows
netstat -ano | findstr :3055
```

### Multi-Client Setup

Each AI client spawns its own stdio server process. All connect to the same WebSocket server (port 3055).

**Cursor config** (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "TalkToFigmaDesktop": {
      "command": "node",
      "args": ["/path/to/mcp-server.cjs"]
    }
  }
}
```

**Claude Code config** (`~/.claude/mcp.json`):
```json
{
  "mcpServers": {
    "TalkToFigmaDesktop": {
      "command": "node",
      "args": ["/path/to/mcp-server.cjs"]
    }
  }
}
```

## Troubleshooting

### Server Won't Start

**Check logs:**
1. Right-click tray icon → "Terminal"
2. Look for error messages

**Common issues:**
- Port 3055 already in use: Kill conflicting process or restart
- Firewall blocking: Allow TalkToFigma through firewall

**macOS port check:**
```bash
lsof -i :3055
kill -9 <PID>
```

**Windows port check:**
```powershell
netstat -ano | findstr :3055
taskkill /PID <PID> /F
```

### Plugin Can't Connect

**Verify:**
1. Desktop app is running (tray icon visible)
2. WebSocket server is active (green icon 🟢)
3. Figma plugin is running in the same file

**Reset connection:**
1. Right-click tray → "Stop Server"
2. Wait 5 seconds
3. Right-click tray → "Start Server"
4. Restart Figma plugin

### MCP Client Can't Find Server

**Check stdio path:**

**macOS:**
```bash
ls -la ~/Library/Application\ Support/TalkToFigma/mcp-server.cjs
```

**Windows:**
```powershell
dir "%APPDATA%\TalkToFigma\mcp-server.cjs"
```

**If missing:**
1. Restart TalkToFigma Desktop (installs stdio server on launch)
2. Check Settings page for correct path
3. Manually verify file exists

### Channel Not Joined Error

Always call `join_channel` before any other operations:

```typescript
// Extract channel from Figma URL
// https://www.figma.com/design/ABC123/Project?node-id=1-2
const channel = "ABC123:1:2";

await use_mcp_tool("TalkToFigmaDesktop", "join_channel", { channel });

// Now other operations work
const page = await use_mcp_tool("TalkToFigmaDesktop", "get_current_page", {});
```

### Node ID Format Issues

Figma node IDs use format `123:456`. Extract from:
- Plugin selection: `figma.currentPage.selection[0].id`
- URL parameters: `node-id=123-456` → convert to `123:456`

```typescript
// Convert URL format to ID format
const nodeId = urlNodeId.replace(/-/g, ':'); // "123-456" → "123:456"
```

## Building from Source

```bash
# Clone repository
git clone https://github.com/grab/TalkToFigmaDesktop.git
cd TalkToFigmaDesktop

# Install dependencies
npm install

# Development mode
npm start

# Build package
npm run package

# Create installer
npm run make
```

**Output locations:**
- Development: Electron starts with hot reload
- Package: `out/TalkToFigma-{platform}-{arch}/`
- Installers: `out/make/`

## API Reference Summary

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `join_channel` | Connect to Figma file | `channel` |
| `get_current_page` | Get active page | - |
| `get_node_by_id` | Fetch node details | `nodeId` |
| `get_all_nodes` | List all nodes | `type` (optional) |
| `search_nodes` | Search by name/type | `query`, `type` |
| `get_selection` | Get selected nodes | - |
| `create_rectangle` | Create rectangle | `x`, `y`, `width`, `height` |
| `create_frame` | Create frame | `x`, `y`, `width`, `height` |
| `create_text` | Create text | `characters`, `fontSize` |
| `create_component` | Create component | `name`, `width`, `height` |
| `set_properties` | Update node | `nodeId`, `properties` |
| `delete_node` | Remove node | `nodeId` |
| `set_auto_layout` | Apply auto layout | `nodeId`, `mode`, `padding` |
| `get_local_paint_styles` | Get color styles | - |
| `get_local_text_styles` | Get text styles | - |
| `export_node` | Export as image | `nodeId`, `format`, `scale` |

Full tool list available in desktop app Terminal logs on startup.
