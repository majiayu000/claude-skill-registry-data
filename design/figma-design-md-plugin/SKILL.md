---
name: figma-design-md-plugin
description: Figma plugin that extracts local styles and generates DESIGN.md and SKILL.md files for AI-driven design system implementation
triggers:
  - "extract design tokens from Figma"
  - "generate DESIGN.md from Figma file"
  - "create design system documentation from Figma"
  - "build SKILL.md for AI coding agents"
  - "export Figma styles to markdown"
  - "convert Figma variables to design tokens"
  - "setup TypeUI design guidelines"
  - "auto-generate design system blueprint"
---

# Figma Design.md Plugin Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## Overview

The **design-md-figma** plugin extracts local styles, variables, and component families from Figma files and generates standardized `DESIGN.md` and `SKILL.md` files. These outputs provide AI coding agents with design-system blueprints for building consistent interfaces.

The plugin reads:
- Local color/typography/spacing/radius/motion styles
- Figma variable collections
- Effect styles (shadows, blur)
- Grid styles
- Component families

It generates TypeUI-format markdown that AI agents can use to implement design-consistent code.

## Installation & Setup

### Development Setup

```bash
# Clone the repository
git clone https://github.com/bergside/design-md-figma.git
cd design-md-figma

# Install dependencies
npm install

# Build the plugin
npm run build
```

### Load in Figma Desktop

1. Open Figma Desktop
2. Navigate to **Plugins → Development → Import plugin from manifest...**
3. Select the `manifest.json` file from your cloned directory
4. The plugin appears in **Plugins → Development → Design MD Skill Generator**

### Watch Mode for Development

```bash
# Auto-rebuild on file changes
npm run watch
```

## Plugin Architecture

### File Structure

```
design-md-figma/
├── src/
│   ├── code.ts          # Main plugin logic (runs in Figma sandbox)
│   ├── ui.html          # Plugin UI (runs in iframe)
│   └── types.ts         # TypeScript type definitions
├── manifest.json        # Figma plugin configuration
└── package.json
```

### Key TypeScript Interfaces

```typescript
interface ExtractedData {
  source: {
    fileName: string;
    pageNames: string[];
    timestamp: string;
  };
  variableCollections: VariableCollection[];
  colorTokens: ColorToken[];
  typographyTokens: TypographyToken[];
  spacingTokens: SpacingToken[];
  radiusTokens: RadiusToken[];
  effectStyles: EffectStyle[];
  gridStyles: GridStyle[];
  componentFamilies: string[];
}

interface ColorToken {
  name: string;
  value: string; // hex, rgb(), or variable reference
  type: 'paint-style' | 'color-variable';
}

interface TypographyToken {
  name: string;
  fontFamily: string;
  fontSize: number;
  fontWeight: number;
  lineHeight: string;
  letterSpacing: string;
}
```

## Core Plugin Functions

### Extracting Design Tokens

The plugin automatically extracts tokens when run:

```typescript
// Main extraction flow (src/code.ts)
async function extractDesignTokens(): Promise<ExtractedData> {
  const data: ExtractedData = {
    source: {
      fileName: figma.root.name,
      pageNames: figma.root.children.map(page => page.name),
      timestamp: new Date().toISOString()
    },
    variableCollections: [],
    colorTokens: [],
    typographyTokens: [],
    spacingTokens: [],
    radiusTokens: [],
    effectStyles: [],
    gridStyles: [],
    componentFamilies: []
  };

  // Extract local paint styles
  const paintStyles = figma.getLocalPaintStyles();
  paintStyles.forEach(style => {
    const paint = style.paints[0];
    if (paint.type === 'SOLID') {
      data.colorTokens.push({
        name: style.name,
        value: rgbToHex(paint.color),
        type: 'paint-style'
      });
    }
  });

  // Extract local text styles
  const textStyles = figma.getLocalTextStyles();
  textStyles.forEach(style => {
    data.typographyTokens.push({
      name: style.name,
      fontFamily: style.fontName.family,
      fontSize: style.fontSize,
      fontWeight: style.fontName.style,
      lineHeight: formatLineHeight(style.lineHeight),
      letterSpacing: formatLetterSpacing(style.letterSpacing)
    });
  });

  // Extract variable collections
  const collections = figma.variables.getLocalVariableCollections();
  collections.forEach(collection => {
    data.variableCollections.push({
      id: collection.id,
      name: collection.name,
      modes: collection.modes.map(m => m.name)
    });
  });

  return data;
}
```

### Generating DESIGN.md

```typescript
function generateDesignMD(data: ExtractedData): string {
  let markdown = `# DESIGN.md\n\n`;
  
  markdown += `## Source\n\n`;
  markdown += `- **File**: ${data.source.fileName}\n`;
  markdown += `- **Pages**: ${data.source.pageNames.join(', ')}\n`;
  markdown += `- **Extracted**: ${data.source.timestamp}\n\n`;

  markdown += `## Color Tokens\n\n`;
  markdown += `| Name | Value | Type |\n`;
  markdown += `| --- | --- | --- |\n`;
  data.colorTokens.forEach(token => {
    markdown += `| ${token.name} | ${token.value} | ${token.type} |\n`;
  });
  markdown += `\n`;

  markdown += `## Typography Tokens\n\n`;
  markdown += `| Name | Family | Size | Weight | Line Height | Letter Spacing |\n`;
  markdown += `| --- | --- | --- | --- | --- | --- |\n`;
  data.typographyTokens.forEach(token => {
    markdown += `| ${token.name} | ${token.fontFamily} | ${token.fontSize}px | ${token.fontWeight} | ${token.lineHeight} | ${token.letterSpacing} |\n`;
  });

  return markdown;
}
```

### Generating SKILL.md

```typescript
function generateSkillMD(data: ExtractedData): string {
  let markdown = `# SKILL.md\n\n`;
  
  markdown += `## Mission\n\n`;
  markdown += `Build interfaces that strictly adhere to the design system extracted from **${data.source.fileName}**.\n\n`;

  markdown += `## Style Foundations\n\n`;
  markdown += `### Colors\n\n`;
  data.colorTokens.forEach(token => {
    markdown += `- **${token.name}**: \`${token.value}\`\n`;
  });
  markdown += `\n`;

  markdown += `### Typography\n\n`;
  data.typographyTokens.forEach(token => {
    markdown += `- **${token.name}**: ${token.fontFamily} ${token.fontSize}px/${token.lineHeight}, weight ${token.fontWeight}\n`;
  });

  markdown += `\n## Rules: Do\n\n`;
  markdown += `- Use extracted color tokens exactly as defined\n`;
  markdown += `- Apply typography scales from text styles\n`;
  markdown += `- Reference component families for consistency\n`;
  markdown += `- Follow spacing/radius token values\n\n`;

  markdown += `## Rules: Don't\n\n`;
  markdown += `- Never hardcode colors outside extracted palette\n`;
  markdown += `- Don't create arbitrary font sizes\n`;
  markdown += `- Avoid inconsistent spacing values\n`;

  return markdown;
}
```

## Message Passing (UI ↔ Plugin)

The plugin uses Figma's message API:

```typescript
// In code.ts (plugin sandbox)
figma.ui.onmessage = async (msg) => {
  if (msg.type === 'extract') {
    const data = await extractDesignTokens();
    figma.ui.postMessage({
      type: 'extraction-complete',
      data
    });
  }
  
  if (msg.type === 'generate-design-md') {
    const markdown = generateDesignMD(msg.data);
    figma.ui.postMessage({
      type: 'markdown-ready',
      markdown,
      fileType: 'DESIGN.md'
    });
  }
};

// In ui.html (iframe)
window.onmessage = (event) => {
  const msg = event.data.pluginMessage;
  if (msg.type === 'extraction-complete') {
    displayExtractedData(msg.data);
  }
  if (msg.type === 'markdown-ready') {
    updateEditor(msg.markdown);
    enableDownload(msg.markdown, msg.fileType);
  }
};
```

## Common Usage Patterns

### Extract and Download DESIGN.md

```typescript
// User opens plugin in Figma
// Plugin auto-extracts on load
figma.showUI(__html__, { width: 600, height: 800 });

const data = await extractDesignTokens();
figma.ui.postMessage({ type: 'extraction-complete', data });

// User clicks "Generate DESIGN.md"
// UI sends message to plugin
parent.postMessage({
  pluginMessage: { type: 'generate-design-md', data }
}, '*');

// Plugin generates markdown and sends back
const markdown = generateDesignMD(data);
figma.ui.postMessage({ 
  type: 'markdown-ready', 
  markdown, 
  fileType: 'DESIGN.md' 
});

// UI enables download button
function downloadFile(content: string, filename: string) {
  const blob = new Blob([content], { type: 'text/markdown' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
}
```

### Refresh Token Extraction

```typescript
// User modifies Figma file (adds new color style)
// User clicks "Refresh" in plugin UI
parent.postMessage({
  pluginMessage: { type: 'refresh' }
}, '*');

// Plugin re-runs extraction
const updatedData = await extractDesignTokens();
figma.ui.postMessage({ 
  type: 'extraction-complete', 
  data: updatedData 
});
```

### Toggle Between DESIGN.md and SKILL.md

```typescript
// UI state management
let currentView: 'design' | 'skill' = 'design';

function toggleView() {
  currentView = currentView === 'design' ? 'skill' : 'design';
  
  parent.postMessage({
    pluginMessage: { 
      type: currentView === 'design' ? 'generate-design-md' : 'generate-skill-md',
      data: extractedData
    }
  }, '*');
}
```

## Configuration

### manifest.json

```json
{
  "name": "Design MD Skill Generator",
  "id": "1612814320994608244",
  "api": "1.0.0",
  "main": "dist/code.js",
  "ui": "dist/ui.html",
  "editorType": ["figma"],
  "networkAccess": {
    "allowedDomains": ["none"]
  }
}
```

### TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ES6",
    "module": "commonjs",
    "lib": ["ES2015"],
    "outDir": "./dist",
    "strict": true,
    "typeRoots": ["./node_modules/@types", "./node_modules/@figma"]
  }
}
```

## Helper Utilities

### Color Conversion

```typescript
function rgbToHex(color: RGB): string {
  const r = Math.round(color.r * 255).toString(16).padStart(2, '0');
  const g = Math.round(color.g * 255).toString(16).padStart(2, '0');
  const b = Math.round(color.b * 255).toString(16).padStart(2, '0');
  return `#${r}${g}${b}`;
}

function rgbaToString(color: RGBA): string {
  const r = Math.round(color.r * 255);
  const g = Math.round(color.g * 255);
  const b = Math.round(color.b * 255);
  return `rgba(${r}, ${g}, ${b}, ${color.a})`;
}
```

### Typography Formatting

```typescript
function formatLineHeight(lineHeight: LineHeight): string {
  if (lineHeight.unit === 'PIXELS') {
    return `${lineHeight.value}px`;
  }
  if (lineHeight.unit === 'PERCENT') {
    return `${lineHeight.value}%`;
  }
  return 'auto';
}

function formatLetterSpacing(spacing: LetterSpacing): string {
  if (spacing.unit === 'PIXELS') {
    return `${spacing.value}px`;
  }
  if (spacing.unit === 'PERCENT') {
    return `${spacing.value}%`;
  }
  return 'normal';
}
```

### Component Family Detection

```typescript
function extractComponentFamilies(): string[] {
  const families = new Set<string>();
  
  const components = figma.root.findAll(node => 
    node.type === 'COMPONENT_SET'
  ) as ComponentSetNode[];
  
  components.forEach(componentSet => {
    // Component set name format: "Button"
    families.add(componentSet.name);
  });
  
  return Array.from(families).sort();
}
```

## Troubleshooting

### Plugin Won't Load

**Issue**: Plugin doesn't appear in Figma menu

**Solution**:
```bash
# Ensure build completed successfully
npm run build

# Check dist/ folder exists with code.js and ui.html
ls -la dist/

# Verify manifest.json points to correct paths
cat manifest.json
```

### No Styles Extracted

**Issue**: Generated markdown shows empty token lists

**Solution**:
- Ensure file has **local styles** (not from external libraries)
- Check Figma file has published color/text styles
- Run **Refresh** after adding new styles

```typescript
// Debug: Log style counts
console.log('Paint styles:', figma.getLocalPaintStyles().length);
console.log('Text styles:', figma.getLocalTextStyles().length);
console.log('Effect styles:', figma.getLocalEffectStyles().length);
```

### Variable Collections Not Found

**Issue**: Variable collections section empty in DESIGN.md

**Solution**:
```typescript
// Ensure using Figma API 1.0.0+ (supports variables)
const collections = figma.variables.getLocalVariableCollections();
if (collections.length === 0) {
  console.warn('No local variable collections found');
}

// Check file actually has variables defined
// Variables → View local variables in Figma
```

### TypeScript Errors

**Issue**: Build fails with type errors

**Solution**:
```bash
# Install Figma type definitions
npm install --save-dev @figma/plugin-typings

# Run type check separately
npm run typecheck

# Common fix: ensure tsconfig includes Figma types
# tsconfig.json
{
  "compilerOptions": {
    "typeRoots": ["./node_modules/@types", "./node_modules/@figma"]
  }
}
```

### Download Not Working

**Issue**: Download button doesn't trigger file save

**Solution**:
```typescript
// Ensure blob creation and download logic is correct
function downloadMarkdown(content: string, filename: string) {
  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link); // Required for Firefox
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url); // Clean up
}
```

## Integration with AI Agents

### Using Generated DESIGN.md with Claude Code

```bash
# Add to project root
cp ~/Downloads/DESIGN.md ./DESIGN.md

# Reference in .claude/instructions
echo "Follow design tokens and guidelines in DESIGN.md" >> .claude/instructions
```

### Using SKILL.md with Cursor

```bash
# Add to .cursor/ directory
mkdir -p .cursor
cp ~/Downloads/SKILL.md .cursor/design-system.md

# Cursor automatically reads skills from .cursor/
```

### Programmatic Usage

```typescript
import fs from 'fs';

// Read generated DESIGN.md
const designMD = fs.readFileSync('./DESIGN.md', 'utf-8');

// Parse color tokens (example)
const colorSection = designMD.match(/## Color Tokens\n\n([\s\S]*?)\n\n##/);
if (colorSection) {
  const rows = colorSection[1].split('\n').slice(2); // Skip header
  const colors = rows.map(row => {
    const [name, value, type] = row.split('|').map(s => s.trim());
    return { name, value, type };
  });
  console.log(colors);
}
```

## Best Practices

1. **Run extraction on design-complete files** — Extract after design system is stable
2. **Use local styles, not library styles** — Plugin only reads local file styles
3. **Name styles consistently** — Use hierarchical naming: `color/primary/500`, `text/heading/h1`
4. **Leverage variable collections** — Map design tokens to Figma variables for better extraction
5. **Refresh after changes** — Re-run extraction when styles/variables updated
6. **Commit generated files to repo** — Keep DESIGN.md and SKILL.md in version control alongside code

## TypeUI Format Compliance

Generated files follow [TypeUI DESIGN.md specification](https://www.typeui.sh/design-md):

- Structured sections (Source, Tokens, Styles, Components)
- Markdown tables for token lists
- ISO 8601 timestamps
- Hex color format for paint styles
- Pixel-based sizing units
- Component family enumeration

## Resources

- **Plugin homepage**: https://www.figma.com/community/plugin/1612814320994608244/design-md-skills
- **TypeUI DESIGN.md format**: https://www.typeui.sh/design-md
- **Curated design skills**: https://www.typeui.sh/design-skills
- **Figma Plugin API**: https://www.figma.com/plugin-docs/api/api-overview/
