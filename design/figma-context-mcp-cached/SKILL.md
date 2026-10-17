---
name: figma-context-mcp-cached
description: Cache-enabled Figma Context MCP server for AI agents to fetch and analyze Figma designs with persistent disk caching
triggers:
  - fetch figma design data
  - get figma file contents
  - download figma images
  - analyze figma components
  - extract figma styles
  - cache figma file
  - refresh figma cache
  - prepare figma file for analysis
---

# Figma Context MCP Cached

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## Overview

Figma-Context-MCP-Cached is an MCP (Model Context Protocol) server that provides AI agents access to Figma design files with intelligent disk caching. It reduces API rate limits by caching Figma file data locally, making it ideal for AI coding agents that need to frequently access design specifications.

**Key Features:**
- Persistent disk caching with configurable TTL
- Smart file preparation with node validation
- Force refresh capability for latest design data
- Image download support (SVG/PNG)
- Automatic system downloads folder detection
- Three core MCP tools: `figma_prepare_file`, `get_figma_data`, `download_figma_images`

## Installation

### For MCP Clients (Claude Desktop, Cursor, etc.)

Add to your MCP settings configuration:

```json
{
  "mcpServers": {
    "figma-context-mcp-cached": {
      "command": "npx",
      "args": [
        "-y",
        "@pactortester/figma-mcp-cached",
        "--stdio",
        "--figma-api-key=${FIGMA_API_KEY}",
        "--figma-caching={\"ttl\":{\"value\":30,\"unit\":\"d\"},\"cacheDir\":\"~/.cache/figma-mcp\"}"
      ]
    }
  }
}
```

### Environment Variables

```bash
# Required
export FIGMA_API_KEY="your-figma-api-key"

# Optional - if not using command-line args
export FIGMA_CACHING='{"ttl":{"value":30,"unit":"d"},"cacheDir":"~/.cache/figma-mcp"}'
```

## Configuration

### Cache TTL Units

- `ms` - milliseconds
- `s` - seconds
- `m` - minutes
- `h` - hours
- `d` - days

### Cache Directory

Default locations by platform:
- **Linux**: `~/.cache/figma-mcp`
- **macOS**: `~/Library/Caches/FigmaMcp`
- **Windows**: `%LOCALAPPDATA%/FigmaMcpCache`

Custom directory (relative or absolute):
```json
{
  "cacheDir": "~/my-custom-cache"
}
```

## MCP Tools Usage

### 1. `figma_prepare_file` - Prepare Figma File

**Always call this first** before fetching Figma data. It checks cache validity and optionally forces refresh.

```typescript
// Tool call structure
{
  "name": "figma_prepare_file",
  "arguments": {
    "figmaUrl": "https://www.figma.com/design/QlQwKAl9abcdhvlfvpM5K/MyDesign?node-id=2777-9428",
    "forceRefresh": false  // Set to true to get latest data
  }
}
```

**When to use `forceRefresh: true`:**
- User says "get the latest design"
- User mentions design was just updated
- User says "refresh the figma file"
- Cache is stale but not yet expired

**Response indicates:**
- Cache hit (file ready to use)
- Cache miss (file downloaded and cached)
- Node validation result (if nodeId in URL)
- Whether file was refreshed

### 2. `get_figma_data` - Fetch Design Data

Retrieves the actual Figma file structure, styles, and component data.

```typescript
// Tool call structure
{
  "name": "get_figma_data",
  "arguments": {
    "fileKey": "QlQwKAl9abcdhvlfvpM5K",
    "nodeId": "2777-9428",  // Optional: specific node to fetch
    "depth": 5  // Optional: tree traversal depth (omit unless user requests)
  }
}
```

**Extracting fileKey and nodeId from URL:**
```
https://www.figma.com/design/{fileKey}/Title?node-id={nodeId}
Example: https://www.figma.com/design/QlQwKAl9abcdhvlfvpM5K/MyDesign?node-id=2777-9428

fileKey = "QlQwKAl9abcdhvlfvpM5K"
nodeId = "2777-9428"
```

**Response structure:**
```typescript
{
  "metadata": {
    "name": "Design System",
    "lastModified": "2026-05-15T10:32:24Z"
  },
  "nodes": [
    {
      "id": "2777:9428",
      "name": "Hero Section",
      "type": "FRAME",
      "children": [...],
      "absoluteBoundingBox": {
        "x": 0,
        "y": 0,
        "width": 1440,
        "height": 800
      },
      "fills": [...],
      "strokes": [...]
    }
  ],
  "globalVars": {
    "colors": {...},
    "typography": {...}
  },
  "components": {...},
  "componentSets": {...}
}
```

### 3. `download_figma_images` - Export Images

Downloads PNG or SVG assets from Figma nodes.

```typescript
// Tool call structure
{
  "name": "download_figma_images",
  "arguments": {
    "fileKey": "QlQwKAl9abcdhvlfvpM5K",
    "nodes": [
      {
        "nodeId": "2777-9428",
        "fileName": "hero-image.png"
      },
      {
        "nodeId": "2777-9430",
        "fileName": "icon-star.svg"
      }
    ],
    "localPath": "/absolute/path/to/save",  // Optional: defaults to system Downloads
    "pngScale": 2  // Optional: 1x, 2x, 3x for PNG export
  }
}
```

**Advanced image download with cropping:**
```typescript
{
  "name": "download_figma_images",
  "arguments": {
    "fileKey": "QlQwKAl9abcdhvlfvpM5K",
    "nodes": [
      {
        "nodeId": "2777-9428",
        "fileName": "cropped-image.png",
        "imageRef": "abc123def456",  // Required for image fills
        "needsCropping": true,
        "cropTransform": [[1, 0, 0], [0, 1, 0]],  // Figma transform matrix
        "requiresImageDimensions": true  // Returns width/height for CSS
      }
    ],
    "pngScale": 3
  }
}
```

## Common Workflows

### Workflow 1: Analyze a Figma Design

```typescript
// Step 1: Prepare the file (checks cache, validates nodes)
{
  "name": "figma_prepare_file",
  "arguments": {
    "figmaUrl": "https://www.figma.com/design/QlQwKAl9abcdhvlfvpM5K/Dashboard?node-id=2777-9428"
  }
}

// Step 2: Fetch the design data
{
  "name": "get_figma_data",
  "arguments": {
    "fileKey": "QlQwKAl9abcdhvlfvpM5K",
    "nodeId": "2777-9428"
  }
}

// Step 3: Analyze the response
// - Extract layout structure from nodes
// - Get color palette from globalVars.colors
// - Identify reusable components
// - Generate CSS/Tailwind from styles
```

### Workflow 2: Export Design Assets

```typescript
// Step 1: Prepare file
{
  "name": "figma_prepare_file",
  "arguments": {
    "figmaUrl": "https://www.figma.com/design/QlQwKAl9abcdhvlfvpM5K/Assets"
  }
}

// Step 2: Get file data to identify exportable nodes
{
  "name": "get_figma_data",
  "arguments": {
    "fileKey": "QlQwKAl9abcdhvlfvpM5K"
  }
}

// Step 3: Download images
{
  "name": "download_figma_images",
  "arguments": {
    "fileKey": "QlQwKAl9abcdhvlfvpM5K",
    "nodes": [
      {"nodeId": "123-456", "fileName": "logo.svg"},
      {"nodeId": "789-012", "fileName": "hero@2x.png"}
    ],
    "pngScale": 2
  }
}
```

### Workflow 3: Force Refresh After Design Update

```typescript
// When user says "the design just changed, get the latest"
{
  "name": "figma_prepare_file",
  "arguments": {
    "figmaUrl": "https://www.figma.com/design/QlQwKAl9abcdhvlfvpM5K/Dashboard",
    "forceRefresh": true  // Bypasses cache, fetches fresh data
  }
}

// Then fetch data normally
{
  "name": "get_figma_data",
  "arguments": {
    "fileKey": "QlQwKAl9abcdhvlfvpM5K"
  }
}
```

## Parsing Figma Node Data

### Extract Layout Information

```typescript
function extractLayout(node: any) {
  const { absoluteBoundingBox, layoutMode, layoutAlign } = node;
  
  return {
    position: {
      x: absoluteBoundingBox.x,
      y: absoluteBoundingBox.y
    },
    size: {
      width: absoluteBoundingBox.width,
      height: absoluteBoundingBox.height
    },
    layout: layoutMode, // 'HORIZONTAL', 'VERTICAL', 'NONE'
    alignment: layoutAlign // 'MIN', 'CENTER', 'MAX', 'STRETCH'
  };
}
```

### Extract Color Styles

```typescript
function extractColors(node: any) {
  const fills = node.fills || [];
  
  return fills
    .filter(fill => fill.type === 'SOLID')
    .map(fill => {
      const { r, g, b, a } = fill.color;
      return `rgba(${Math.round(r*255)}, ${Math.round(g*255)}, ${Math.round(b*255)}, ${a})`;
    });
}
```

### Extract Typography

```typescript
function extractTypography(node: any) {
  if (node.type !== 'TEXT') return null;
  
  const { style } = node;
  return {
    fontFamily: style.fontFamily,
    fontSize: style.fontSize,
    fontWeight: style.fontWeight,
    lineHeight: style.lineHeightPx || style.lineHeightPercentFontSize,
    letterSpacing: style.letterSpacing,
    textAlign: style.textAlignHorizontal
  };
}
```

### Generate CSS from Figma Node

```typescript
function generateCSS(node: any): string {
  const layout = extractLayout(node);
  const colors = extractColors(node);
  const typography = node.type === 'TEXT' ? extractTypography(node) : null;
  
  let css = `.${node.name.toLowerCase().replace(/\s+/g, '-')} {\n`;
  
  // Layout
  css += `  width: ${layout.size.width}px;\n`;
  css += `  height: ${layout.size.height}px;\n`;
  
  // Colors
  if (colors[0]) {
    css += `  background-color: ${colors[0]};\n`;
  }
  
  // Typography
  if (typography) {
    css += `  font-family: '${typography.fontFamily}';\n`;
    css += `  font-size: ${typography.fontSize}px;\n`;
    css += `  font-weight: ${typography.fontWeight};\n`;
  }
  
  css += `}\n`;
  return css;
}
```

## Cache Management

### Check Cache Status

The cache is transparent, but you can infer status from `figma_prepare_file` response:

- `"File is already cached and valid"` → Cache hit
- `"Successfully cached file"` → Cache miss, file downloaded
- `"Cache refreshed"` → Force refresh executed

### Manual Cache Clearing

Cache files are stored as JSON in the configured directory:

```bash
# Linux/macOS
rm -rf ~/.cache/figma-mcp/*

# Windows (PowerShell)
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\FigmaMcpCache\*"
```

### Cache Naming Convention

Files are cached as: `{fileKey}.json`

Example: `QlQwKAl9abcdhvlfvpM5K.json`

## Troubleshooting

### Cache Not Working

**Symptom:** Every request hits Figma API

**Check:**
1. Verify `FIGMA_CACHING` is set in config
2. Ensure cache directory is writable
3. Check TTL is reasonable (not 0 or negative)

```json
// Valid caching config
{
  "ttl": {"value": 30, "unit": "d"},
  "cacheDir": "~/.cache/figma-mcp"
}
```

### Node Not Found Error

**Symptom:** `figma_prepare_file` reports node doesn't exist

**Solution:**
1. Verify nodeId format: `1234-5678` or `1234:5678`
2. Use `forceRefresh: true` to update cache
3. Check if node was deleted in Figma

### Rate Limit Errors

**Symptom:** 429 Too Many Requests from Figma API

**Solution:**
1. Increase cache TTL (e.g., from 1 day to 30 days)
2. Use `figma_prepare_file` to check cache before fetching
3. Avoid calling `get_figma_data` with `forceRefresh` repeatedly

### Stale Cache Data

**Symptom:** Design changes not reflected in results

**Solution:**
1. Use `forceRefresh: true` in `figma_prepare_file`
2. Reduce cache TTL for frequently updated files
3. Clear cache manually during active design iterations

### Permission Errors

**Symptom:** Cannot write to cache directory

**Solution:**
```bash
# Linux/macOS
chmod 755 ~/.cache/figma-mcp

# Or set custom directory in user space
{
  "cacheDir": "~/my-figma-cache"
}
```

## Best Practices

1. **Always call `figma_prepare_file` first** before `get_figma_data`
2. **Use longer cache TTL** (7-30 days) for stable design systems
3. **Use shorter cache TTL** (1-6 hours) for active design work
4. **Use `forceRefresh`** when user explicitly requests latest data
5. **Don't specify `depth`** parameter unless user has specific need
6. **Parse globalVars** for reusable design tokens (colors, fonts, spacing)
7. **Batch image downloads** in single `download_figma_images` call
8. **Use SVG for icons**, PNG for photos/raster images

## Integration Examples

### Generate Tailwind Config from Figma

```typescript
async function generateTailwindConfig(fileKey: string) {
  // Prepare and fetch file
  await callTool('figma_prepare_file', { 
    figmaUrl: `https://www.figma.com/design/${fileKey}/DesignSystem` 
  });
  
  const data = await callTool('get_figma_data', { fileKey });
  
  // Extract colors from globalVars
  const colors = {};
  for (const [name, value] of Object.entries(data.globalVars.colors)) {
    colors[name] = value; // Already in hex/rgba format
  }
  
  // Generate Tailwind config
  return {
    theme: {
      extend: {
        colors,
        fontFamily: data.globalVars.typography || {}
      }
    }
  };
}
```

### Export Component Library

```typescript
async function exportComponents(fileKey: string, outputDir: string) {
  const data = await callTool('get_figma_data', { fileKey });
  
  // Find all component instances
  const components = Object.entries(data.components).map(([id, comp]) => ({
    id,
    name: comp.name,
    nodeId: id.replace(':', '-')
  }));
  
  // Download each component as SVG
  const nodes = components.map(c => ({
    nodeId: c.nodeId,
    fileName: `${c.name.toLowerCase().replace(/\s+/g, '-')}.svg`
  }));
  
  await callTool('download_figma_images', {
    fileKey,
    nodes,
    localPath: outputDir
  });
}
```
