---
name: figma-mcp-go-design-automation
description: Automate Figma designs with AI using MCP server - no API limits, full read/write via plugin bridge
triggers:
  - create Figma designs from text descriptions
  - modify Figma components and styles programmatically
  - export Figma designs to code or images
  - automate Figma prototype interactions
  - read Figma design tokens and variables
  - batch update text and styles in Figma
  - generate Figma layouts with auto-layout
  - convert designs to PDFs or screenshots
---

# Figma MCP Go Design Automation

> Skill by [ara.so](https://ara.so) — Design Skills collection

## Overview

`figma-mcp-go` is an MCP (Model Context Protocol) server that provides AI agents with direct read/write access to Figma files through a plugin bridge. Unlike other Figma integrations, it **doesn't use the Figma REST API**, so there are no rate limits or token requirements. This makes it ideal for free Figma users and rapid AI-driven design automation.

**Key capabilities:**
- 73 tools for creating, modifying, and reading Figma designs
- Works via local plugin bridge (no API calls)
- Full access to styles, variables, components, prototypes
- Export to images, PDFs, and design tokens
- Integrated design strategy prompts for best practices

## Installation

The MCP server runs via `npx` with no build step required. You also need to install a Figma plugin to establish the bridge.

### Step 1: Configure MCP Server

**For Claude Code CLI:**
```bash
claude mcp add -s project figma-mcp-go -- npx -y @vkhanhqui/figma-mcp-go@latest
```

**For Cursor / VS Code / GitHub Copilot** (`.vscode/mcp.json`):
```json
{
  "servers": {
    "figma-mcp-go": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@vkhanhqui/figma-mcp-go"]
    }
  }
}
```

**For Claude Desktop** (`.mcp.json`):
```json
{
  "mcpServers": {
    "figma-mcp-go": {
      "command": "npx",
      "args": ["-y", "@vkhanhqui/figma-mcp-go"]
    }
  }
}
```

### Step 2: Install Figma Plugin

1. Download `plugin.zip` from [GitHub releases](https://github.com/vkhanhqui/figma-mcp-go/releases)
2. In Figma Desktop: **Plugins → Development → Import plugin from manifest**
3. Select `manifest.json` from the extracted zip
4. Open any Figma file and run the plugin to activate the bridge

## Core Concepts

### Tool Categories

- **Create**: `create_frame`, `create_rectangle`, `create_text`, `create_component`, etc.
- **Modify**: `set_text`, `set_fills`, `set_auto_layout`, `resize_nodes`, etc.
- **Delete**: `delete_nodes`, `delete_page`, `delete_style`
- **Read**: `get_document`, `get_selection`, `get_styles`, `get_variable_defs`
- **Export**: `get_screenshot`, `save_screenshots`, `export_frames_to_pdf`, `export_tokens`
- **Prototype**: `set_reactions`, `remove_reactions`
- **Variables**: `create_variable_collection`, `bind_variable_to_node`, etc.

### Node IDs

Most tools require node IDs. Get them with:
- `get_selection` - Currently selected nodes
- `get_document` - Full page tree
- `search_nodes` - Find by name/type
- `get_design_context` - Depth-limited tree

## Common Patterns

### Pattern 1: Create a Simple Layout

```typescript
// Get current page context
const context = await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "get_metadata",
  arguments: {}
});

// Create a parent frame
const frame = await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "create_frame",
  arguments: {
    name: "Hero Section",
    x: 100,
    y: 100,
    width: 1200,
    height: 600,
    fills: [{type: "SOLID", color: {r: 0.95, g: 0.95, b: 0.95}}],
    autoLayout: {
      mode: "VERTICAL",
      primaryAxisAlignItems: "CENTER",
      counterAxisAlignItems: "CENTER",
      paddingTop: 40,
      paddingBottom: 40,
      paddingLeft: 60,
      paddingRight: 60,
      itemSpacing: 24
    }
  }
});

// Add text inside
const title = await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "create_text",
  arguments: {
    characters: "Welcome to Our Platform",
    x: 0,
    y: 0,
    parentId: frame.nodeId,
    fontSize: 48,
    fontWeight: "Bold"
  }
});
```

### Pattern 2: Batch Update Text Content

```typescript
// Find all text nodes
const textNodes = await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "scan_text_nodes",
  arguments: {
    rootNodeId: "parentFrameId"
  }
});

// Replace placeholder text
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "find_replace_text",
  arguments: {
    rootNodeId: "parentFrameId",
    findText: "{{product_name}}",
    replaceWith: "Acme Widget Pro",
    useRegex: false,
    caseSensitive: false
  }
});
```

### Pattern 3: Apply Design System Styles

```typescript
// Get available styles
const styles = await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "get_styles",
  arguments: {}
});

// Create a paint style
const primaryColor = await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "create_paint_style",
  arguments: {
    name: "Primary/500",
    color: "#3B82F6"
  }
});

// Apply to nodes
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "apply_style_to_node",
  arguments: {
    nodeId: "buttonNodeId",
    styleId: primaryColor.styleId,
    styleType: "FILL"
  }
});
```

### Pattern 4: Create Variables and Bind Them

```typescript
// Create a variable collection for theming
const collection = await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "create_variable_collection",
  arguments: {
    name: "Theme",
    initialModeName: "Light"
  }
});

// Add Dark mode
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "add_variable_mode",
  arguments: {
    collectionId: collection.collectionId,
    modeName: "Dark"
  }
});

// Create a color variable
const bgColor = await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "create_variable",
  arguments: {
    collectionId: collection.collectionId,
    name: "Background",
    resolvedType: "COLOR"
  }
});

// Set values for both modes
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "set_variable_value",
  arguments: {
    variableId: bgColor.variableId,
    modeId: "Light",
    value: {r: 1, g: 1, b: 1}
  }
});

await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "set_variable_value",
  arguments: {
    variableId: bgColor.variableId,
    modeId: "Dark",
    value: {r: 0.1, g: 0.1, b: 0.1}
  }
});

// Bind to a frame
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "bind_variable_to_node",
  arguments: {
    nodeId: "frameNodeId",
    variableId: bgColor.variableId,
    field: "fillColor"
  }
});
```

### Pattern 5: Export Designs

```typescript
// Export a single frame as screenshot
const screenshot = await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "get_screenshot",
  arguments: {
    nodeId: "frameNodeId",
    format: "PNG",
    scale: 2
  }
});
// Returns base64-encoded image

// Save multiple frames to disk
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "save_screenshots",
  arguments: {
    nodeIds: ["frame1", "frame2", "frame3"],
    format: "PNG",
    scale: 2,
    outputDir: "/path/to/exports"
  }
});

// Export frames as PDF
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "export_frames_to_pdf",
  arguments: {
    frameIds: ["frame1", "frame2"],
    outputPath: "/path/to/design.pdf"
  }
});

// Export design tokens
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "export_tokens",
  arguments: {
    format: "JSON",
    outputPath: "/path/to/tokens.json"
  }
});
```

### Pattern 6: Create Prototype Interactions

```typescript
// Add a click reaction to navigate to another frame
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "set_reactions",
  arguments: {
    nodeId: "buttonNodeId",
    reactions: [{
      trigger: {type: "ON_CLICK"},
      action: {
        type: "NODE",
        destinationId: "targetFrameId",
        navigation: "NAVIGATE",
        transition: {
          type: "DISSOLVE",
          duration: 0.3,
          easing: {type: "EASE_IN_OUT"}
        }
      }
    }],
    mode: "replace"
  }
});

// Get existing reactions
const reactions = await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "get_reactions",
  arguments: {
    nodeId: "buttonNodeId"
  }
});
```

### Pattern 7: Component Management

```typescript
// Convert a frame to a component
const component = await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "create_component",
  arguments: {
    frameNodeId: "frameToConvert"
  }
});

// Get all local components
const components = await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "get_local_components",
  arguments: {}
});

// Swap an instance to use a different component
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "swap_component",
  arguments: {
    instanceNodeId: "instanceId",
    newComponentId: "newComponentId"
  }
});

// Detach instance to plain frame
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "detach_instance",
  arguments: {
    instanceNodeIds: ["instance1", "instance2"]
  }
});
```

## MCP Prompts

The server includes built-in prompts for design strategies. Use them to get AI guidance:

```typescript
// Get best practices for reading designs
const readStrategy = await get_prompt({
  server_name: "figma-mcp-go",
  prompt_name: "read_design_strategy"
});

// Get best practices for creating designs
const designStrategy = await get_prompt({
  server_name: "figma-mcp-go",
  prompt_name: "design_strategy"
});

// Chunked text replacement strategy
const textStrategy = await get_prompt({
  server_name: "figma-mcp-go",
  prompt_name: "text_replacement_strategy"
});
```

## Advanced Techniques

### Auto-Layout with Complex Constraints

```typescript
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "set_auto_layout",
  arguments: {
    nodeId: "frameId",
    mode: "HORIZONTAL",
    primaryAxisAlignItems: "SPACE_BETWEEN",
    counterAxisAlignItems: "CENTER",
    paddingTop: 16,
    paddingBottom: 16,
    paddingLeft: 24,
    paddingRight: 24,
    itemSpacing: 12,
    primaryAxisSizingMode: "AUTO",
    counterAxisSizingMode: "FIXED"
  }
});
```

### Responsive Constraints

```typescript
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "set_constraints",
  arguments: {
    nodeIds: ["childNodeId"],
    constraints: {
      horizontal: "STRETCH",
      vertical: "MIN"
    }
  }
});
```

### Blend Modes and Effects

```typescript
// Set blend mode
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "set_blend_mode",
  arguments: {
    nodeIds: ["overlayNodeId"],
    blendMode: "MULTIPLY"
  }
});

// Add drop shadow
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "set_effects",
  arguments: {
    nodeId: "cardNodeId",
    effects: [{
      type: "DROP_SHADOW",
      color: {r: 0, g: 0, b: 0, a: 0.1},
      offset: {x: 0, y: 4},
      radius: 8,
      visible: true
    }]
  }
});
```

### Batch Operations

```typescript
// Rename multiple nodes with find/replace
await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "batch_rename_nodes",
  arguments: {
    nodeIds: ["node1", "node2", "node3"],
    operation: "findReplace",
    findText: "old",
    replaceWith: "new"
  }
});

// Clone and reposition
const clones = await use_mcp_tool({
  server_name: "figma-mcp-go",
  tool_name: "clone_node",
  arguments: {
    nodeId: "sourceNodeId",
    count: 5,
    offsetX: 20,
    offsetY: 20
  }
});
```

## Troubleshooting

### Plugin Not Connecting

**Symptom:** MCP tools timeout or return "plugin not ready"

**Solutions:**
1. Ensure Figma Desktop (not browser) is running
2. Verify plugin is loaded: **Plugins → Development → figma-mcp-go**
3. Restart both the plugin and your AI tool
4. Check Figma Developer Console for errors (Plugins → Development → Open Console)

### Node ID Not Found

**Symptom:** "Node with ID X not found"

**Solutions:**
1. Use `get_selection` to verify current selection IDs
2. Use `search_nodes` to find nodes by name
3. Ensure you're on the correct page with `navigate_to_page`
4. Check if node was deleted or is on a different page

### Font Not Loading

**Symptom:** Text creation fails with "font not available"

**Solutions:**
1. The plugin auto-loads fonts, but they must be installed on your system
2. Use `get_fonts` to see available fonts in the current file
3. Specify common fonts: `fontFamily: "Inter"` or `"Roboto"`
4. Check Figma's font loading status in the right panel

### Rate Limit Confusion

**Symptom:** Worried about hitting API limits

**Solution:** This tool doesn't use Figma's REST API at all—there are no rate limits. All operations go through the local plugin bridge.

### Export Path Issues

**Symptom:** `save_screenshots` or `export_frames_to_pdf` fails

**Solutions:**
1. Use absolute paths: `/Users/username/exports/` not `~/exports/`
2. Ensure the directory exists (create it first if needed)
3. Check write permissions on the target directory
4. On Windows, use forward slashes: `C:/Users/username/exports/`

### Auto-Layout Not Applied

**Symptom:** `set_auto_layout` succeeds but layout doesn't change

**Solutions:**
1. Ensure the node is a FRAME (not GROUP or other type)
2. Check that child constraints are compatible
3. Verify `mode` is `"HORIZONTAL"` or `"VERTICAL"`
4. Some properties require `primaryAxisSizingMode` to be set

## Best Practices

1. **Always get context first**: Use `get_metadata` or `get_design_context` before making changes
2. **Use search instead of hardcoding IDs**: Node IDs change between sessions—use `search_nodes` or `get_selection`
3. **Leverage MCP prompts**: Call `read_design_strategy` or `design_strategy` for AI-guided best practices
4. **Batch operations**: Group multiple `set_fills`, `resize_nodes`, etc. calls to minimize tool invocations
5. **Export often**: Use `get_screenshot` to verify changes visually during complex operations
6. **Variable-first design**: Prefer `bind_variable_to_node` over direct `set_fills` for themeable designs
7. **Test on a copy**: Clone important frames before applying batch transformations

## Reference: Key Tools by Use Case

| Use Case | Recommended Tools |
|----------|------------------|
| Get started | `get_metadata`, `get_selection`, `get_design_context` |
| Create layouts | `create_frame`, `set_auto_layout`, `create_section` |
| Add content | `create_text`, `create_rectangle`, `import_image` |
| Modify designs | `set_fills`, `resize_nodes`, `set_text`, `move_nodes` |
| Design system | `create_paint_style`, `create_text_style`, `create_variable_collection` |
| Prototyping | `set_reactions`, `remove_reactions`, `get_reactions` |
| Export | `get_screenshot`, `save_screenshots`, `export_tokens`, `export_frames_to_pdf` |
| Search/navigate | `search_nodes`, `navigate_to_page`, `get_pages` |
| Batch edits | `find_replace_text`, `batch_rename_nodes`, `set_fills` (with multiple IDs) |
