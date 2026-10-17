---
name: figma-design-md-generator
description: Generate DESIGN.md and SKILL.md files from Figma design systems for AI-assisted development
triggers:
  - "extract design tokens from Figma"
  - "generate DESIGN.md from Figma file"
  - "create design system documentation"
  - "export Figma styles to markdown"
  - "build SKILL.md for design system"
  - "document Figma design tokens"
  - "extract typography and color tokens"
  - "generate AI-ready design guidelines"
---

# Figma DESIGN.md Generator

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A Figma plugin that extracts local style guidelines, variables, and component families from Figma files and generates `DESIGN.md` and `SKILL.md` files. These outputs provide AI tools (Claude Code, Cursor, Codex) with structured design-system blueprints for building consistent interfaces.

## What It Does

The plugin reads Figma's local styles and variables—colors, typography, spacing, radius, effects, grids, and component sets—and converts them into editable markdown files following the [TypeUI DESIGN.md](https://www.typeui.sh/design-md) format.

**Key capabilities:**
- Auto-extracts color tokens (paint styles + variables)
- Auto-extracts typography tokens (text styles + scales)
- Auto-extracts spacing, radius, motion tokens
- Auto-extracts effect styles (shadows, blur)
- Auto-extracts grid styles and component families
- Generates human-editable `DESIGN.md` (reference documentation)
- Generates AI-optimized `SKILL.md` (agent instructions)

## Installation

### As a Figma Plugin (Development Mode)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bergside/design-md-figma.git
   cd design-md-figma
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Build the plugin:**
   ```bash
   npm run build
   ```

4. **Import into Figma Desktop:**
   - Open Figma Desktop
   - Go to **Plugins → Development → Import plugin from manifest...**
   - Select `manifest.json` from the project directory
   - Run **Design MD Skill Generator** from the plugins menu

### Development Workflow

```bash
# Watch mode for live development
npm run watch

# Type checking
npm run typecheck

# Production build
npm run build
```

## Key Plugin Actions

| Action | Description |
|--------|-------------|
| **Auto-extract** | Reads local styles and variables from active Figma file |
| **Generate DESIGN.md** | Creates design-guideline markdown from extracted signals |
| **Generate SKILL.md** | Creates agent-ready markdown with implementation rules |
| **Toggle view** | Switches between DESIGN.md and SKILL.md in editor |
| **Refresh** | Re-runs extraction for current file state |
| **Download** | Saves generated output as `.md` file |

## Plugin Architecture

### Main Entry Points

**`code.ts`** – Plugin backend (runs in Figma sandbox):

```typescript
figma.showUI(__html__, { width: 800, height: 600 });

// Listen for extraction requests
figma.ui.onmessage = (msg) => {
  if (msg.type === 'extract-styles') {
    const styles = extractLocalStyles();
    const variables = extractVariables();
    const components = extractComponentFamilies();
    
    figma.ui.postMessage({
      type: 'extraction-complete',
      data: { styles, variables, components }
    });
  }
};

function extractLocalStyles() {
  const paintStyles = figma.getLocalPaintStyles();
  const textStyles = figma.getLocalTextStyles();
  const effectStyles = figma.getLocalEffectStyles();
  const gridStyles = figma.getLocalGridStyles();
  
  return {
    colors: paintStyles.map(s => ({
      name: s.name,
      type: s.paints[0]?.type,
      value: paintToHex(s.paints[0])
    })),
    typography: textStyles.map(s => ({
      name: s.name,
      fontFamily: s.fontName.family,
      fontSize: s.fontSize,
      lineHeight: s.lineHeight
    })),
    effects: effectStyles.map(s => ({
      name: s.name,
      effects: s.effects
    })),
    grids: gridStyles.map(s => ({
      name: s.name,
      layoutGrids: s.layoutGrids
    }))
  };
}

function extractVariables() {
  const collections = figma.variables.getLocalVariableCollections();
  
  return collections.map(collection => ({
    name: collection.name,
    modes: collection.modes,
    variables: collection.variableIds.map(id => {
      const variable = figma.variables.getVariableById(id);
      return {
        name: variable?.name,
        resolvedType: variable?.resolvedType,
        valuesByMode: variable?.valuesByMode
      };
    })
  }));
}

function extractComponentFamilies() {
  const components = figma.root.findAll(node => 
    node.type === 'COMPONENT_SET'
  ) as ComponentSetNode[];
  
  return components.map(comp => ({
    name: comp.name,
    variantCount: comp.children.length,
    properties: Object.keys(comp.componentPropertyDefinitions || {})
  }));
}
```

**`ui.html`** – Plugin UI (React-based):

```typescript
// Send extraction request
window.parent.postMessage(
  { pluginMessage: { type: 'extract-styles' } },
  '*'
);

// Receive extraction results
window.onmessage = (event) => {
  const msg = event.data.pluginMessage;
  
  if (msg.type === 'extraction-complete') {
    const designMd = generateDesignMd(msg.data);
    const skillMd = generateSkillMd(msg.data);
    
    setDesignContent(designMd);
    setSkillContent(skillMd);
  }
};
```

## Generated File Structure

### DESIGN.md Format

```markdown
# Design System – [File Name]

## Source
- **File**: [Figma file name]
- **Page**: [Current page]
- **Extracted**: [ISO timestamp]

## Variable Collections
- **Collection Name** (2 modes: Light, Dark)

## Color Tokens
| Token | Value | Type |
|-------|-------|------|
| primary/500 | #3B82F6 | solid |
| neutral/900 | #111827 | solid |

## Typography Tokens
| Token | Font Family | Size | Line Height | Weight |
|-------|-------------|------|-------------|--------|
| heading/xl | Inter | 32px | 1.2 | 700 |
| body/md | Inter | 16px | 1.5 | 400 |

## Spacing Tokens
| Token | Value |
|-------|-------|
| spacing/xs | 4px |
| spacing/md | 16px |

## Component Families
- Button (variants: 8)
- Input (variants: 6)
- Card (variants: 4)
```

### SKILL.md Format

```markdown
# AI Design System Agent – [File Name]

## Mission
Implement UI components that strictly follow the extracted design system from [File Name].

## Brand
- **Product**: [Inferred from file]
- **Audience**: [Inferred context]
- **Surface**: Web/Mobile

## Style Foundations
### Colors
- Primary: #3B82F6
- Semantic: Success (#10B981), Error (#EF4444)

### Typography
- Heading scale: 32/24/20/16px
- Body scale: 16/14/12px
- Font stack: Inter, system-ui, sans-serif

## Accessibility
- WCAG 2.2 AA contrast (4.5:1 text, 3:1 UI)
- Minimum touch target: 44×44px
- Focus indicators required

## Rules: Do
- Use extracted color tokens exactly
- Apply typography tokens for all text
- Respect spacing scale for layout
- Implement all component variants

## Rules: Don't
- Don't invent new colors outside token set
- Don't use arbitrary font sizes
- Don't skip accessibility requirements
```

## Common Usage Patterns

### Extract and Download

```typescript
// In plugin code
async function extractAndGenerate() {
  // Extract all design tokens
  const styles = extractLocalStyles();
  const variables = extractVariables();
  const components = extractComponentFamilies();
  
  // Generate markdown
  const designMd = formatDesignMd({ styles, variables, components });
  const skillMd = formatSkillMd({ styles, variables, components });
  
  // Send to UI for download
  figma.ui.postMessage({
    type: 'download-ready',
    designMd,
    skillMd
  });
}
```

### Convert Paint to Hex

```typescript
function paintToHex(paint: Paint): string {
  if (paint.type === 'SOLID') {
    const r = Math.round(paint.color.r * 255);
    const g = Math.round(paint.color.g * 255);
    const b = Math.round(paint.color.b * 255);
    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`.toUpperCase();
  }
  return 'gradient';
}
```

### Format Typography Token

```typescript
function formatTypographyToken(style: TextStyle) {
  const lineHeight = style.lineHeight.unit === 'PIXELS' 
    ? `${style.lineHeight.value}px`
    : style.lineHeight.value;
    
  return {
    name: style.name,
    fontFamily: style.fontName.family,
    fontSize: `${style.fontSize}px`,
    fontWeight: style.fontWeight,
    lineHeight,
    letterSpacing: style.letterSpacing
  };
}
```

### Extract Component Variants

```typescript
function extractComponentVariants(componentSet: ComponentSetNode) {
  const variants = componentSet.children.map(child => {
    if (child.type === 'COMPONENT') {
      return {
        name: child.name,
        properties: child.variantProperties || {}
      };
    }
  }).filter(Boolean);
  
  return {
    family: componentSet.name,
    count: variants.length,
    variants
  };
}
```

## Using Generated Files with AI Tools

### Claude Code / Cursor

1. Place `DESIGN.md` and `SKILL.md` in project root
2. Reference in agent context:
   ```
   @SKILL.md implement a button component following the design system
   ```

### Prompt Engineering

```
Using the design tokens in DESIGN.md, create a React component 
for [Component Name] that:
- Uses color tokens from primary palette
- Applies typography token heading/md
- Respects spacing/md for padding
- Implements all variants listed in Component Families
```

## Configuration

The plugin reads Figma's native structures—no external configuration required. All extraction is based on:

- Local paint styles
- Local text styles  
- Local effect styles
- Local grid styles
- Variable collections
- Component sets in current file

## Troubleshooting

### No Styles Extracted

**Problem**: Plugin returns empty DESIGN.md

**Solution**: Ensure you have local styles created in Figma. Shared library styles are not extracted—only local file styles.

```typescript
// Check for local styles
const paintStyles = figma.getLocalPaintStyles();
if (paintStyles.length === 0) {
  console.warn('No local paint styles found in this file');
}
```

### Variables Not Showing

**Problem**: Variable collections missing from output

**Solution**: Verify variables are created as local collections, not external libraries.

```typescript
const collections = figma.variables.getLocalVariableCollections();
console.log('Found collections:', collections.length);
```

### Build Errors

**Problem**: TypeScript compilation fails

**Solution**: Ensure Figma plugin types are installed:

```bash
npm install --save-dev @figma/plugin-typings
```

Update `tsconfig.json`:

```json
{
  "compilerOptions": {
    "types": ["@figma/plugin-typings"]
  }
}
```

### Plugin Won't Load

**Problem**: "Failed to load manifest" error

**Solution**: Check `manifest.json` structure:

```json
{
  "name": "Design MD Skill Generator",
  "id": "YOUR_PLUGIN_ID",
  "api": "1.0.0",
  "main": "code.js",
  "ui": "ui.html",
  "editorType": ["figma"]
}
```

## Best Practices

1. **Run extraction on finalized designs** – Ensure your local styles and variables are complete before generating files

2. **Name tokens consistently** – Use `/` separators for token hierarchy (e.g., `color/primary/500`)

3. **Version control generated files** – Commit `DESIGN.md` and `SKILL.md` alongside design system code

4. **Update after design changes** – Re-run extraction when design tokens change

5. **Combine with component library** – Use generated files as source of truth for design token implementation

## Resources

- [TypeUI DESIGN.md format](https://www.typeui.sh/design-md)
- [Curated design skills](https://www.typeui.sh/design-skills)
- [Figma Plugin API](https://www.figma.com/plugin-docs/)
- [Plugin GitHub repository](https://github.com/bergside/design-md-figma)
