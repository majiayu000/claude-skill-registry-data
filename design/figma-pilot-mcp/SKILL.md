---
name: figma-pilot-mcp
description: Control Figma through code execution with MCP - create, modify, and query design elements programmatically via AI agents
triggers:
  - "create a figma design"
  - "modify figma elements"
  - "query figma components"
  - "generate figma design system"
  - "check figma accessibility"
  - "export figma assets"
  - "create figma components"
  - "batch update figma layers"
---

# Figma Pilot MCP Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## Overview

Figma Pilot is an MCP (Model Context Protocol) server that enables AI agents to control Figma through code execution. Instead of exposing dozens of individual tools, it provides only 3 MCP tools with full Figma API access through JavaScript code execution.

**Key advantages:**
- 90%+ fewer tokens in tool definitions
- Batch operations (modify 100 elements in one call)
- Data filtering before returning to context
- Complex workflows with loops, conditionals, error handling

## Installation

### 1. Install MCP Server

```bash
# For Claude Code
claude mcp add figma-pilot -- npx @youware-labs/figma-pilot-mcp

# For other MCP clients, add to config:
```

**Claude Desktop** (`~/.config/claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "figma-pilot": {
      "command": "npx",
      "args": ["@youware-labs/figma-pilot-mcp"]
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "figma-pilot": {
      "command": "npx",
      "args": ["@youware-labs/figma-pilot-mcp"]
    }
  }
}
```

### 2. Install Figma Plugin

1. Download `figma-pilot-plugin-vX.X.X.zip` from [GitHub Releases](https://github.com/youware-labs/figma-pilot/releases)
2. Unzip the file
3. In Figma: **Plugins > Development > Import plugin from manifest...**
4. Select `manifest.json` from unzipped folder
5. Run: **Plugins > Development > figma-pilot**

### 3. Verify Connection

```
Check the Figma connection status
```

The plugin should show "Connected" in Figma.

## MCP Tools

| Tool | Purpose |
|------|---------|
| `figma_status` | Check if plugin is connected |
| `figma_execute` | Execute JavaScript code with Figma API |
| `figma_get_api_docs` | Get API documentation for reference |

## Core API Reference

### Query Operations

```javascript
// Query selected elements
const { nodes } = await figma.query({ target: 'selection' });

// Query by node ID
const { nodes } = await figma.query({ target: 'nodeId:123:456' });

// Query current page
const { nodes } = await figma.query({ target: 'page' });

// Query entire document
const { nodes } = await figma.query({ target: 'document' });
```

### Create Operations

```javascript
// Create a rectangle
await figma.create({
  type: 'rectangle',
  name: 'My Rectangle',
  width: 200,
  height: 100,
  fill: '#FF6B6B',
  cornerRadius: 8
});

// Create text
await figma.create({
  type: 'text',
  content: 'Hello World',
  fontSize: 24,
  fontWeight: 600,
  fill: '#333333'
});

// Create frame with children
await figma.create({
  type: 'frame',
  name: 'Card',
  width: 300,
  height: 200,
  children: [
    {
      type: 'text',
      content: 'Title',
      fontSize: 18,
      fontWeight: 600
    },
    {
      type: 'text',
      content: 'Description text',
      fontSize: 14,
      fill: '#666666'
    }
  ]
});

// Create auto layout frame
await figma.create({
  type: 'frame',
  name: 'Button',
  layoutMode: 'horizontal',
  primaryAxisAlignItems: 'center',
  counterAxisAlignItems: 'center',
  paddingLeft: 16,
  paddingRight: 16,
  paddingTop: 8,
  paddingBottom: 8,
  itemSpacing: 8,
  fill: '#0066FF',
  cornerRadius: 6,
  children: [
    {
      type: 'text',
      content: 'Click me',
      fontSize: 14,
      fill: '#FFFFFF'
    }
  ]
});
```

### Modify Operations

```javascript
// Modify by selection
await figma.modify({
  target: 'selection',
  fill: '#4CAF50',
  cornerRadius: 12,
  opacity: 0.9
});

// Modify by node ID
await figma.modify({
  target: 'nodeId:123:456',
  width: 300,
  height: 150
});

// Modify text content
await figma.modify({
  target: 'selection',
  content: 'Updated text',
  fontSize: 16,
  fontWeight: 700
});
```

### Delete Operations

```javascript
// Delete selected elements
await figma.delete({ target: 'selection' });

// Delete by node ID
await figma.delete({ target: 'nodeId:123:456' });
```

### Append Operations

```javascript
// Move selected element into a parent frame
await figma.append({
  target: 'selection',
  parent: 'nodeId:789:012'
});
```

## Component Operations

### List Components

```javascript
// List all components in document
const { components } = await figma.listComponents();

// components = [
//   { id: '123:456', name: 'Button/Primary', key: 'abc123...' },
//   { id: '123:457', name: 'Button/Secondary', key: 'def456...' }
// ]
```

### Create Component Instance

```javascript
// Create instance from component key
await figma.instantiate({
  component: 'abc123componentkey',
  name: 'Button Instance'
});

// Create instance and position it
await figma.instantiate({
  component: 'abc123componentkey',
  x: 100,
  y: 200
});
```

### Convert to Component

```javascript
// Convert selected element to component
await figma.toComponent({
  target: 'selection',
  name: 'My Component'
});
```

### Create Variants

```javascript
// Create component variants
await figma.createVariants({
  name: 'Button',
  variants: [
    {
      properties: { size: 'small', state: 'default' },
      node: 'nodeId:123:456'
    },
    {
      properties: { size: 'small', state: 'hover' },
      node: 'nodeId:123:457'
    },
    {
      properties: { size: 'large', state: 'default' },
      node: 'nodeId:123:458'
    }
  ]
});
```

## Design Tokens

### Create Token

```javascript
// Create color token
await figma.createToken({
  name: 'colors/primary',
  value: '#0066FF',
  type: 'color',
  description: 'Primary brand color'
});

// Create spacing token
await figma.createToken({
  name: 'spacing/md',
  value: 16,
  type: 'number',
  description: 'Medium spacing'
});
```

### Bind Token to Element

```javascript
// Bind color token to fill
await figma.bindToken({
  target: 'selection',
  property: 'fill',
  token: 'colors/primary'
});

// Bind spacing token to padding
await figma.bindToken({
  target: 'selection',
  property: 'paddingLeft',
  token: 'spacing/md'
});
```

## Accessibility Operations

```javascript
// Check accessibility issues
const result = await figma.accessibility({
  target: 'page',
  level: 'AA' // or 'AAA'
});

// result = {
//   issues: [
//     { type: 'contrast', severity: 'error', node: '123:456', message: '...' }
//   ],
//   totalIssues: 1
// }

// Check and auto-fix issues
const result = await figma.accessibility({
  target: 'selection',
  level: 'AA',
  autoFix: true
});

// result.fixedCount contains number of issues fixed
```

## Export Operations

```javascript
// Export as PNG
const { data } = await figma.export({
  target: 'selection',
  format: 'png',
  scale: 2
});

// Export as SVG
const { data } = await figma.export({
  target: 'nodeId:123:456',
  format: 'svg'
});

// Export as JPG
const { data } = await figma.export({
  target: 'selection',
  format: 'jpg',
  quality: 0.9
});

// data is base64 encoded image data
```

## Common Patterns

### Batch Modify Elements

```javascript
// Get all rectangles in selection and change their color
const { nodes } = await figma.query({ target: 'selection' });
const rectangles = nodes.filter(n => n.type === 'RECTANGLE');

for (const rect of rectangles) {
  await figma.modify({
    target: `nodeId:${rect.id}`,
    fill: '#FF6B6B',
    cornerRadius: 8
  });
}

console.log(`Modified ${rectangles.length} rectangles`);
```

### Create Design System Components

```javascript
// Create button variants
const sizes = ['small', 'medium', 'large'];
const variants = [];

for (const size of sizes) {
  const buttonNode = await figma.create({
    type: 'frame',
    name: `Button/${size}`,
    layoutMode: 'horizontal',
    primaryAxisAlignItems: 'center',
    counterAxisAlignItems: 'center',
    paddingLeft: size === 'small' ? 12 : size === 'medium' ? 16 : 20,
    paddingRight: size === 'small' ? 12 : size === 'medium' ? 16 : 20,
    paddingTop: size === 'small' ? 6 : size === 'medium' ? 8 : 10,
    paddingBottom: size === 'small' ? 6 : size === 'medium' ? 8 : 10,
    fill: '#0066FF',
    cornerRadius: 6,
    children: [{
      type: 'text',
      content: 'Button',
      fontSize: size === 'small' ? 12 : size === 'medium' ? 14 : 16,
      fill: '#FFFFFF'
    }]
  });
  
  variants.push({
    properties: { size },
    node: buttonNode.id
  });
}

await figma.createVariants({
  name: 'Button',
  variants
});
```

### Generate Card Layout

```javascript
// Create a card with image, title, description, and action
await figma.create({
  type: 'frame',
  name: 'Card',
  width: 320,
  height: 400,
  layoutMode: 'vertical',
  primaryAxisAlignItems: 'min',
  counterAxisAlignItems: 'min',
  paddingLeft: 0,
  paddingRight: 0,
  paddingTop: 0,
  paddingBottom: 0,
  itemSpacing: 0,
  fill: '#FFFFFF',
  cornerRadius: 12,
  effects: [{
    type: 'DROP_SHADOW',
    color: { r: 0, g: 0, b: 0, a: 0.1 },
    offset: { x: 0, y: 2 },
    radius: 8,
    visible: true
  }],
  children: [
    {
      type: 'rectangle',
      name: 'Image',
      width: 320,
      height: 180,
      fill: '#E0E0E0'
    },
    {
      type: 'frame',
      name: 'Content',
      layoutMode: 'vertical',
      primaryAxisAlignItems: 'min',
      counterAxisAlignItems: 'stretch',
      paddingLeft: 20,
      paddingRight: 20,
      paddingTop: 20,
      paddingBottom: 20,
      itemSpacing: 12,
      children: [
        {
          type: 'text',
          content: 'Card Title',
          fontSize: 20,
          fontWeight: 600,
          fill: '#1A1A1A'
        },
        {
          type: 'text',
          content: 'This is a description of the card content. It provides more details about what this card represents.',
          fontSize: 14,
          fill: '#666666',
          lineHeight: { value: 150, unit: 'PERCENT' }
        },
        {
          type: 'frame',
          name: 'Action',
          layoutMode: 'horizontal',
          primaryAxisAlignItems: 'center',
          counterAxisAlignItems: 'center',
          paddingLeft: 16,
          paddingRight: 16,
          paddingTop: 8,
          paddingBottom: 8,
          fill: '#0066FF',
          cornerRadius: 6,
          children: [{
            type: 'text',
            content: 'Learn More',
            fontSize: 14,
            fill: '#FFFFFF'
          }]
        }
      ]
    }
  ]
});
```

### Filter and Process Elements

```javascript
// Find all text layers with specific content
const { nodes } = await figma.query({ target: 'page' });
const headings = nodes.filter(n => 
  n.type === 'TEXT' && 
  n.fontSize >= 24 &&
  n.fontWeight >= 600
);

// Update all headings
for (const heading of headings) {
  await figma.modify({
    target: `nodeId:${heading.id}`,
    fill: '#1A1A1A',
    fontFamily: 'Inter',
    fontWeight: 700
  });
}

console.log(`Updated ${headings.length} headings`);
```

### Create Responsive Grid

```javascript
// Create a 3-column grid
await figma.create({
  type: 'frame',
  name: 'Grid',
  width: 1200,
  layoutMode: 'horizontal',
  primaryAxisAlignItems: 'min',
  counterAxisAlignItems: 'stretch',
  itemSpacing: 24,
  paddingLeft: 24,
  paddingRight: 24,
  paddingTop: 24,
  paddingBottom: 24,
  children: Array(3).fill(null).map((_, i) => ({
    type: 'frame',
    name: `Column ${i + 1}`,
    layoutMode: 'vertical',
    primaryAxisSizingMode: 'FIXED',
    counterAxisSizingMode: 'FIXED',
    width: 376,
    primaryAxisAlignItems: 'min',
    counterAxisAlignItems: 'stretch',
    itemSpacing: 16,
    fill: '#F5F5F5',
    cornerRadius: 8,
    paddingLeft: 16,
    paddingRight: 16,
    paddingTop: 16,
    paddingBottom: 16,
    children: [
      {
        type: 'text',
        content: `Column ${i + 1}`,
        fontSize: 18,
        fontWeight: 600
      }
    ]
  }))
});
```

## Troubleshooting

### Plugin Not Connecting

1. Check MCP server status in your AI client
2. Verify plugin shows "Connected" in Figma
3. Ensure port 38451 is not blocked
4. Try reopening the plugin

```bash
# Check if port is in use
lsof -i :38451

# Kill process if needed
kill <PID>
```

### Code Execution Errors

If you get errors like "Cannot read property 'type' of undefined":

```javascript
// Always check if query returned results
const { nodes } = await figma.query({ target: 'selection' });
if (!nodes || nodes.length === 0) {
  console.log('No elements selected');
  return;
}

// Process nodes safely
for (const node of nodes) {
  if (node.type === 'RECTANGLE') {
    await figma.modify({
      target: `nodeId:${node.id}`,
      fill: '#FF0000'
    });
  }
}
```

### Font Loading Issues

Some fonts may not be available. Use safe defaults:

```javascript
try {
  await figma.create({
    type: 'text',
    content: 'Hello',
    fontFamily: 'Inter', // Safe default
    fontSize: 16
  });
} catch (error) {
  console.error('Font not available:', error.message);
  // Fallback to system font
  await figma.create({
    type: 'text',
    content: 'Hello',
    fontSize: 16
  });
}
```

### Performance with Large Documents

When working with large documents, filter data before returning:

```javascript
// Bad: Returns all nodes
const { nodes } = await figma.query({ target: 'document' });

// Good: Filter specific types
const { nodes } = await figma.query({ target: 'document' });
const buttons = nodes.filter(n => 
  n.name.includes('Button') && 
  n.type === 'FRAME'
).slice(0, 10); // Limit results

// Return only needed data
console.log(buttons.map(b => ({ id: b.id, name: b.name })));
```

## Best Practices

1. **Always validate query results** before processing
2. **Use batch operations** instead of multiple individual calls
3. **Filter data** before returning to reduce context window usage
4. **Log meaningful messages** to help track progress
5. **Handle errors gracefully** with try/catch blocks
6. **Use design tokens** for consistent styling
7. **Create components** for reusable elements
8. **Check accessibility** regularly with WCAG checks

## Architecture

```
┌─────────────┐     stdio      ┌─────────────────┐     HTTP      ┌──────────────┐
│ MCP Client  │ <------------> │  MCP Server     │ <-----------> │ Figma Plugin │
│             │                │  (with bridge)  │   port 38451  │              │
└─────────────┘                └─────────────────┘               └──────────────┘
```

The MCP server acts as a bridge between the AI client and the Figma plugin, enabling code execution with full Figma API access.
