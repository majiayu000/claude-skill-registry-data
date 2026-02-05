---
name: mcp-figma-desktop
description: Extract UI code, design tokens, and screenshots from Figma designs via desktop app. Use when implementing designs, building component libraries, or documenting design systems.
---

# Figma Desktop Skill

Interact with Figma designs directly through the Figma desktop app. Extract UI code (React, Vue, SwiftUI, etc.), design tokens (colors, spacing, typography), screenshots, and metadata from design files. Perfect for implementing design specs, creating component libraries, and maintaining design-code consistency.

## Prerequisites

- Figma desktop app installed and running
- mcp2rest running on http://localhost:28888
- figma-desktop server loaded in mcp2rest (http://127.0.0.1:3845/mcp)
- Node.js 18+ installed

**Verify connection:**
```bash
curl http://localhost:28888/health
curl http://localhost:28888/servers | grep figma-desktop
```

## Quick Start

Most tools work with either:
- **Currently selected node** in Figma (no parameters)
- **Specific node ID** (via `--nodeId` parameter)
- **Figma URL** (automatically extracts node ID)

**Example: Get code for selected component**
```bash
cd .claude/skills/mcp-figma-desktop/scripts

# 1. Select a component in Figma desktop app
# 2. Run this to get React code:
node get_design_context.js --clientFrameworks react

# Output: React component code with props, styling, and structure
```

**Example: Get code from Figma URL**
```bash
# Extract node 123-456 from URL: https://figma.com/design/abc/MyFile?node-id=123-456
node get_design_context.js --nodeId "123:456" --clientFrameworks react,typescript
```

## Available Tools

### Design Code Generation

**get_design_context.js** - Generate production-ready UI code
- **Use for:** Converting designs to React/Vue/SwiftUI/etc components
- **Parameters:**
  - `--nodeId` (optional) - Node ID like "123:456", or omit to use selected node
  - `--clientLanguages` (optional) - Language preferences (e.g., typescript, swift)
  - `--clientFrameworks` (optional) - Framework preferences (e.g., react, vue, swiftui)
  - `--forceCode` (optional) - Force code generation even if not recommended

**get_figjam.js** - Generate code from FigJam boards
- **Use for:** Extracting content from FigJam files (NOT regular Figma files)
- **Parameters:**
  - `--nodeId` (optional) - FigJam node ID or omit for selected node
  - `--clientLanguages` (optional) - Language preferences
  - `--clientFrameworks` (optional) - Framework preferences
  - `--includeImagesOfNodes` (optional) - Include embedded images

**Important:** FigJam URLs use `/board/` instead of `/design/`:
- FigJam: `https://figma.com/board/:fileKey/:fileName?node-id=1-2` → nodeId: "1:2"
- Figma: `https://figma.com/design/:fileKey/:fileName?node-id=1-2` → nodeId: "1:2"

### Design Tokens & Variables

**get_variable_defs.js** - Extract design system variables
- **Use for:** Getting reusable design tokens (colors, spacing, typography)
- **Parameters:**
  - `--nodeId` (optional) - Node ID or omit for selected node
  - `--clientLanguages` (optional) - Output format preferences
  - `--clientFrameworks` (optional) - Framework-specific token formats

**Output example:**
```json
{
  "icon/default/secondary": "#949494",
  "spacing/base": "8px",
  "font/heading/large": "32px"
}
```

### Visual Assets

**get_screenshot.js** - Generate high-quality screenshots
- **Use for:** Creating visual documentation, design reviews, presentations
- **Parameters:**
  - `--nodeId` (optional) - Node to screenshot, or omit for selected
  - `--clientLanguages` (optional) - Format preferences
  - `--clientFrameworks` (optional) - Context for screenshot generation

### Structure & Metadata

**get_metadata.js** - Extract structural information
- **Use for:** Understanding design hierarchy before detailed extraction
- **Returns:** XML with node IDs, types, names, positions, sizes
- **Note:** Prefer `get_design_context` for most use cases
- **Parameters:**
  - `--nodeId` (optional) - Node or page ID (e.g., "0:1" for whole page)
  - `--clientLanguages` (optional)
  - `--clientFrameworks` (optional)

**When to use metadata:**
1. Get overview of large page structure
2. Find specific node IDs for detailed extraction
3. Understand design organization before processing

### Design System

**create_design_system_rules.js** - Generate design system documentation
- **Use for:** Creating design system rules for your codebase
- **Returns:** Prompt/template for documenting design patterns
- **Parameters:**
  - `--clientLanguages` (optional) - Language context
  - `--clientFrameworks` (optional) - Framework context

## Common Workflows

### Workflow 1: Implement Component from Design

**Scenario:** Designer shares Figma link, you need to build the component

**Checklist:**
- [ ] Copy Figma URL from designer (e.g., `https://figma.com/design/abc/Button?node-id=12-34`)
- [ ] Extract node ID from URL: `12-34` becomes `12:34`
- [ ] Get component code: `node get_design_context.js --nodeId "12:34" --clientFrameworks react,typescript`
- [ ] Review generated code and component props
- [ ] Extract design tokens: `node get_variable_defs.js --nodeId "12:34"`
- [ ] Create screenshot for documentation: `node get_screenshot.js --nodeId "12:34"`
- [ ] Implement component using generated code as reference
- [ ] Verify design tokens match

**Example:**
```bash
cd .claude/skills/mcp-figma-desktop/scripts

# 1. Get React + TypeScript code
node get_design_context.js --nodeId "12:34" --clientFrameworks react,typescript

# 2. Get design variables
node get_variable_defs.js --nodeId "12:34"

# 3. Take screenshot for docs
node get_screenshot.js --nodeId "12:34"
```

**Expected output:**
- TypeScript React component with props interface
- Design tokens (colors, spacing, typography)
- High-quality PNG screenshot

### Workflow 2: Build Component Library

**Scenario:** Create reusable component library from design system

**Checklist:**
- [ ] Open design system file in Figma desktop
- [ ] Get page structure: `node get_metadata.js --nodeId "0:1"` (page root)
- [ ] Identify component node IDs from metadata XML
- [ ] For each component:
  - [ ] Extract code: `node get_design_context.js --nodeId "{id}" --clientFrameworks react`
  - [ ] Extract tokens: `node get_variable_defs.js --nodeId "{id}"`
  - [ ] Generate screenshot: `node get_screenshot.js --nodeId "{id}"`
- [ ] Create design system rules: `node create_design_system_rules.js`
- [ ] Organize components into library structure
- [ ] Document usage patterns

**Example: Button component extraction**
```bash
# 1. Get page structure to find button variants
node get_metadata.js --nodeId "0:1" > structure.xml

# From XML, identify button node IDs: 45:12, 45:13, 45:14

# 2. Extract primary button
node get_design_context.js --nodeId "45:12" --clientFrameworks react,typescript > Button.tsx
node get_variable_defs.js --nodeId "45:12" > button-tokens.json
node get_screenshot.js --nodeId "45:12" > button-primary.png

# 3. Repeat for secondary, tertiary variants
```

### Workflow 3: Design-to-Code for FigJam Wireframes

**Scenario:** Convert FigJam wireframes into initial code structure

**Important:** Use `get_figjam.js` for FigJam files, NOT `get_design_context.js`

**Checklist:**
- [ ] Open FigJam board in Figma desktop
- [ ] Select wireframe frame/section
- [ ] Extract structure: `node get_figjam.js --includeImagesOfNodes true`
- [ ] Review generated code skeleton
- [ ] Refine with actual design components

**Example:**
```bash
cd .claude/skills/mcp-figma-desktop/scripts

# From FigJam URL: https://figma.com/board/xyz/Wireframes?node-id=5-10
# Extract node "5:10"

node get_figjam.js --nodeId "5:10" --clientFrameworks react --includeImagesOfNodes true
```

**Expected output:**
- Basic component structure matching wireframe layout
- Placeholder content from FigJam sticky notes/text
- Embedded images if present

### Workflow 4: Extract Design Tokens for Theme

**Scenario:** Create theme configuration from design variables

**Checklist:**
- [ ] Select root design system frame in Figma
- [ ] Extract all variables: `node get_variable_defs.js`
- [ ] Parse output into theme format (CSS custom properties, JS theme object, etc.)
- [ ] Validate variable naming conventions
- [ ] Generate theme documentation

**Example:**
```bash
# 1. Get all design tokens from selected design system root
node get_variable_defs.js > design-tokens.json

# Output will include:
# {
#   "color/primary/500": "#3B82F6",
#   "color/primary/600": "#2563EB",
#   "spacing/xs": "4px",
#   "spacing/sm": "8px",
#   "typography/heading/h1": "32px"
# }

# 2. Convert to CSS variables or theme object in your build process
```

## Node ID Format

Figma uses colon-separated node IDs internally:

**From Figma URLs:**
- URL: `...?node-id=123-456` → Node ID: `"123:456"` (replace hyphen with colon)
- Always use quotes: `--nodeId "123:456"`

**From metadata:**
- XML includes actual node IDs: `id="123:456"`
- Copy directly into commands

**Page IDs:**
- Pages typically start with `0:` (e.g., `0:1`, `0:2`)
- Use for getting entire page structure

## State Persistence

The figma-desktop server maintains state between calls:
- Selected node in Figma remains consistent across commands
- Can run multiple extractions without re-selecting
- Server state persists until Figma desktop app is closed

**Best practice:** For batch operations, keep Figma desktop app open and navigate to each node before running scripts.

## Troubleshooting

### Connection Issues

**Error: Cannot connect to mcp2rest**
```bash
# 1. Check mcp2rest is running
curl http://localhost:28888/health

# 2. Verify figma-desktop server is loaded
curl http://localhost:28888/servers

# 3. Look for figma-desktop in output with "connected" status
```

**Error: figma-desktop server not found**
- Ensure Figma desktop app is running
- Restart mcp2rest: `mcp2rest restart`
- Check server URL matches: `http://127.0.0.1:3845/mcp`

### Tool-Specific Issues

**No output or empty response**
- Ensure a node is selected in Figma desktop app
- Try providing explicit `--nodeId` parameter
- Verify node ID format uses colon: `"123:456"` not `"123-456"`

**Wrong framework/language output**
- Use `--clientFrameworks` to specify: `react`, `vue`, `swiftui`, etc.
- Use `--clientLanguages` to specify: `typescript`, `javascript`, `swift`
- Combine multiple: `--clientFrameworks react,typescript`

**FigJam extraction fails**
- Ensure using `get_figjam.js` for FigJam files (not `get_design_context.js`)
- Check URL contains `/board/` (FigJam) not `/design/` (Figma)
- FigJam requires `--includeImagesOfNodes` for embedded images

### Getting Help

```bash
# View help for any script
node scripts/get_design_context.js --help
node scripts/get_variable_defs.js --help
node scripts/get_screenshot.js --help
```

## Advanced Usage

### Custom Language/Framework Output

Most tools support `--clientLanguages` and `--clientFrameworks` for customization:

```bash
# React with TypeScript
node get_design_context.js --nodeId "12:34" --clientFrameworks react,typescript

# Vue with Composition API
node get_design_context.js --nodeId "12:34" --clientFrameworks vue,composition-api

# SwiftUI
node get_design_context.js --nodeId "12:34" --clientFrameworks swiftui --clientLanguages swift

# Multiple frameworks for comparison
node get_design_context.js --nodeId "12:34" --clientFrameworks react,vue,svelte
```

### Batch Processing

Process multiple nodes in sequence:

```bash
# Save node IDs to file
echo "12:34" > nodes.txt
echo "45:67" >> nodes.txt
echo "89:01" >> nodes.txt

# Process each node
while read nodeId; do
  echo "Processing $nodeId..."
  node get_design_context.js --nodeId "$nodeId" --clientFrameworks react > "component_${nodeId//:/_}.tsx"
  node get_screenshot.js --nodeId "$nodeId" > "screenshot_${nodeId//:/_}.png"
done < nodes.txt
```

### Integration with Build Tools

Example: Extract design tokens during build:

```json
{
  "scripts": {
    "extract-tokens": "cd .claude/skills/mcp-figma-desktop/scripts && node get_variable_defs.js > ../../src/theme/tokens.json",
    "prebuild": "npm run extract-tokens"
  }
}
```

## Tips for Best Results

1. **Use specific frameworks:** `--clientFrameworks react` gives better output than generic
2. **Select precise nodes:** Select the exact component/frame in Figma for accurate extraction
3. **Verify metadata first:** Use `get_metadata.js` to explore structure before detailed extraction
4. **Consistent naming:** Use Figma naming conventions that match your code (e.g., `Button/Primary`, `Icon/Close`)
5. **Design tokens:** Set up variables in Figma for automatic token extraction
6. **Batch operations:** Keep Figma desktop open and process multiple nodes in sequence for efficiency

## Related Resources

- [Figma Desktop Plugin MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/figma-desktop)
- [mcp2rest Documentation](https://github.com/ulasbilgen/mcp2skill-tools/tree/main/packages/mcp2rest)
- [Figma Variables Guide](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)
