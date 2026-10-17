---
name: figma-bridge-html-export
description: Transform Figma designs into LLM-friendly HTML/CSS for AI-assisted development
triggers:
  - convert figma design to html
  - export figma to semantic html css
  - generate code from figma design
  - setup figma bridge server
  - preview figma design in browser
  - extract design tokens from figma
  - create html from figma component
  - parse figma layout to css
---

# Figma Bridge HTML Export

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## Overview

Figma Bridge is a Figma-to-code conversion tool that parses Figma designs into clean, semantic HTML/CSS optimized for Large Language Models. It enables AI to accurately understand design intent and achieve pixel-perfect implementation. The tool includes a Figma plugin, local server with live preview, and a standalone conversion pipeline.

## Installation

```bash
# Clone the repository
git clone https://github.com/kingkongshot/Figma-Bridge.git
cd Figma-Bridge

# Install dependencies
npm install

# Start the development server
npm run dev
```

The server starts at `http://localhost:7788` by default.

## Figma Plugin Setup

1. Open Figma and navigate to any canvas
2. Right-click on a blank area
3. Select **Plugins → Development → Import plugin from manifest**
4. Select the `manifest.json` file from the project root
5. Open the plugin via **Plugins → Development → Bridge**
6. Click any component in Figma to see the preview in your browser

## Key Components

### Server & Preview

The local server provides real-time preview with visual debugging overlays:

```bash
# Start server (default port 7788)
npm run dev

# Custom port via environment variable
PORT=8080 npm run dev
```

Access the preview interface at `http://localhost:7788` (or your custom port).

### Bridge Pipeline

The core conversion package is available at `packages/bridge-pipeline/`:

```typescript
import { convertFigmaNode } from './packages/bridge-pipeline';

// Convert a Figma node to HTML/CSS
const result = convertFigmaNode(figmaNodeData, {
  enableFontMatching: true,
  preserveLayout: true
});

console.log(result.html);
console.log(result.css);
```

### Output Files

Generated files are saved to `output/`:

```
output/
├── index.html          # Main HTML file
├── styles.css          # Generated CSS
└── assets/             # Extracted images/fonts
```

## Configuration

### Debug Mode

Enable detailed logging and intermediate output:

```bash
# Enable debug mode
BRIDGE_DEBUG=1 npm run dev
```

Debug files are saved to `debug/` directory with timestamped conversion steps.

### Font Handling

Figma Bridge automatically matches fonts with Google Fonts:

```typescript
// Font matching is enabled by default
const config = {
  enableFontMatching: true,
  fallbackFonts: ['Arial', 'sans-serif']
};
```

## Code Examples

### Basic Figma Node Processing

```typescript
// In your Figma plugin code (code.js)
figma.on('selectionchange', () => {
  const selection = figma.currentPage.selection;
  
  if (selection.length > 0) {
    const node = selection[0];
    
    // Extract node data
    const nodeData = {
      id: node.id,
      name: node.name,
      type: node.type,
      x: node.x,
      y: node.y,
      width: node.width,
      height: node.height,
      fills: node.fills,
      strokes: node.strokes,
      children: node.children?.map(child => processChild(child))
    };
    
    // Send to server for processing
    fetch('http://localhost:7788/convert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(nodeData)
    });
  }
});
```

### Server-Side Conversion

```typescript
// src/server.ts example
import express from 'express';
import { convertToHTML } from './converter';

const app = express();
app.use(express.json());

app.post('/convert', async (req, res) => {
  try {
    const figmaData = req.body;
    
    // Convert Figma data to HTML/CSS
    const result = await convertToHTML(figmaData, {
      outputDir: './output',
      includeDebugOverlay: true
    });
    
    res.json({
      success: true,
      html: result.html,
      css: result.css,
      preview: `http://localhost:7788/preview/${result.id}`
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 7788;
app.listen(PORT, () => {
  console.log(`Figma Bridge server running on http://localhost:${PORT}`);
});
```

### Custom Style Processing

```typescript
// Processing Figma fills to CSS
function processFills(fills: Paint[]): string {
  if (!fills || fills.length === 0) return 'transparent';
  
  const fill = fills[0];
  
  if (fill.type === 'SOLID') {
    const { r, g, b } = fill.color;
    const a = fill.opacity ?? 1;
    return `rgba(${Math.round(r * 255)}, ${Math.round(g * 255)}, ${Math.round(b * 255)}, ${a})`;
  }
  
  if (fill.type === 'GRADIENT_LINEAR') {
    const stops = fill.gradientStops.map(stop => {
      const { r, g, b } = stop.color;
      return `rgba(${Math.round(r * 255)}, ${Math.round(g * 255)}, ${Math.round(b * 255)}, ${stop.alpha})`;
    }).join(', ');
    
    return `linear-gradient(${stops})`;
  }
  
  return 'transparent';
}
```

### Layout Extraction

```typescript
// Extract layout properties
function extractLayout(node: SceneNode): CSSProperties {
  return {
    position: 'absolute',
    left: `${node.x}px`,
    top: `${node.y}px`,
    width: `${node.width}px`,
    height: `${node.height}px`,
    
    // Auto-layout (Flexbox)
    ...(node.layoutMode !== 'NONE' && {
      display: 'flex',
      flexDirection: node.layoutMode === 'HORIZONTAL' ? 'row' : 'column',
      gap: `${node.itemSpacing}px`,
      padding: `${node.paddingTop}px ${node.paddingRight}px ${node.paddingBottom}px ${node.paddingLeft}px`
    }),
    
    // Border radius
    ...(node.cornerRadius && {
      borderRadius: `${node.cornerRadius}px`
    })
  };
}
```

## Common Patterns

### AI-Assisted Workflow

```typescript
// 1. Export design from Figma Bridge
const designData = await fetchFromFigmaBridge('http://localhost:7788/latest');

// 2. Pass to LLM with context
const prompt = `
Convert this Figma design to React components:
${JSON.stringify(designData.html)}
${JSON.stringify(designData.css)}

Requirements:
- Use Tailwind CSS
- Make it responsive
- Add proper TypeScript types
`;

// 3. LLM generates production code with full design context
```

### Batch Processing

```typescript
// Process multiple Figma components
const components = figma.currentPage.findAll(node => 
  node.type === 'COMPONENT'
);

for (const component of components) {
  const result = await convertToHTML(component, {
    outputFile: `output/${component.name}.html`
  });
  
  console.log(`Converted: ${component.name}`);
}
```

### Custom Preview Templates

```html
<!-- public/preview-template.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Figma Bridge Preview</title>
  <link rel="stylesheet" href="/styles.css">
  <style>
    body { margin: 0; padding: 20px; }
    .debug-overlay { border: 1px dashed red; }
  </style>
</head>
<body>
  <div id="root">
    <!-- Generated HTML inserted here -->
  </div>
</body>
</html>
```

## Troubleshooting

### Plugin Not Loading

```bash
# Ensure manifest.json is valid
cat manifest.json

# Check Figma plugin console for errors
# In Figma: Plugins → Development → Open Console
```

### Server Connection Issues

```bash
# Check if port is available
lsof -i :7788

# Kill existing process if needed
kill -9 <PID>

# Restart with different port
PORT=8080 npm run dev
```

### Font Matching Failures

```typescript
// Add custom font fallbacks
const config = {
  enableFontMatching: true,
  customFonts: {
    'SF Pro': 'system-ui',
    'Inter': 'Inter, sans-serif'
  },
  googleFontsAPI: process.env.GOOGLE_FONTS_API_KEY
};
```

### CSS Not Applied Correctly

```bash
# Enable debug mode to see generated CSS
BRIDGE_DEBUG=1 npm run dev

# Check debug/latest.css for issues
cat debug/latest.css

# Verify output/styles.css is linked correctly
grep -r "styles.css" output/
```

### Large File Performance

```typescript
// Optimize large Figma files
const config = {
  maxDepth: 10,           // Limit nesting depth
  skipHiddenLayers: true, // Ignore hidden layers
  minSize: 1,             // Skip very small elements
  imageOptimization: {
    maxWidth: 2048,
    quality: 0.85
  }
};
```

### Memory Issues

```bash
# Increase Node.js memory limit
NODE_OPTIONS="--max-old-space-size=4096" npm run dev
```

## API Reference

### Core Functions

```typescript
// Main conversion function
convertFigmaNode(node: FigmaNode, options?: ConversionOptions): ConversionResult

// Options
interface ConversionOptions {
  enableFontMatching?: boolean;
  preserveLayout?: boolean;
  outputDir?: string;
  includeDebugOverlay?: boolean;
  customFonts?: Record<string, string>;
}

// Result
interface ConversionResult {
  html: string;
  css: string;
  assets: string[];
  metadata: {
    nodeId: string;
    timestamp: number;
    fonts: string[];
  };
}
```

## Project Structure

```
Figma-Bridge/
├── packages/bridge-pipeline/  # Core conversion logic
├── src/                       # Server & CLI
├── public/                    # Preview interface
├── code.js                    # Figma plugin
├── ui.html                    # Plugin UI
├── output/                    # Generated files
└── debug/                     # Debug output
```
