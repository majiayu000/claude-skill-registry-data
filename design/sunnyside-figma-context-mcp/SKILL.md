---
name: sunnyside-figma-context-mcp
description: Extract pixel-perfect code, design tokens, and component structures from Figma designs via MCP tools for AI-driven development workflows
triggers:
  - "extract code from this Figma design"
  - "generate React component from Figma selection"
  - "get design tokens from Figma file"
  - "convert Figma frame to Tailwind component"
  - "analyze design system health in Figma"
  - "extract CSS from Figma layers"
  - "simulate design token changes"
  - "download assets from Figma design"
---

# Sunnyside Figma Context MCP

> Skill by [ara.so](https://ara.so) — Design Skills collection

A Model Context Protocol (MCP) server providing 27 specialized tools to bridge Figma designs with AI development workflows. Supports two data paths: **Figma Plugin** (highest fidelity, works on any plan including Drafts) and **Figma REST API** (headless, requires team/project files).

## Installation

**Prerequisites:**
- Node.js 18+
- Figma Personal Access Token ([create here](https://www.figma.com/developers/api#access-tokens))

```bash
git clone https://github.com/tercumantanumut/sunnysideFigma-Context-MCP
cd sunnysideFigma-Context-MCP
npm install
npm run build
```

**Environment configuration** (`.env`):
```env
FIGMA_API_KEY=figd_your_token_here
PORT=3333
OUTPUT_FORMAT=json
```

**Start the server:**
```bash
npm start
# Server runs on http://localhost:3333
# SSE endpoint: /sse
# HTTP endpoint: /mcp
```

## MCP Client Configuration

### SSE Transport (Recommended for Plugin Use)

Use when you need the Figma plugin and MCP tools to share extraction state:

```json
{
  "mcpServers": {
    "sunnyside-figma": {
      "type": "sse",
      "url": "http://localhost:3333/sse"
    }
  }
}
```

### stdio Transport

For headless use without plugin integration:

```json
{
  "mcpServers": {
    "sunnyside-figma": {
      "type": "stdio",
      "command": "node",
      "args": [
        "/absolute/path/to/sunnysideFigma-Context-MCP/dist/cli.js",
        "--stdio"
      ],
      "env": {
        "FIGMA_API_KEY": "figd_your_token_here"
      }
    }
  }
}
```

### HTTP Transport

```json
{
  "mcpServers": {
    "sunnyside-figma": {
      "type": "http",
      "url": "http://localhost:3333/mcp"
    }
  }
}
```

## Figma Plugin Setup

1. Open Figma Desktop → **Plugins → Development → Import plugin from manifest…**
2. Navigate to `figma-dev-plugin/manifest.json` in the cloned repo
3. Run the plugin on any file
4. Select a frame → click **Extract Dev Code**

The plugin sends extraction data to `http://localhost:3333/plugin/*` endpoints.

## Core Tool Categories

### Plugin-Bridge Tools (Highest Fidelity)

These tools read data extracted by the Figma plugin. **No API limits, works on Drafts.**

**`get_JSON`** — Primary extraction tool, returns comprehensive structured data:
```typescript
// Returns:
{
  id: string,
  name: string,
  type: string,
  layoutMode?: string,
  primaryAxisAlignItems?: string,
  counterAxisAlignItems?: string,
  paddingLeft?: number,
  // ... full layout properties
  fills: Array<{type: string, color: {r, g, b, a}, opacity?: number}>,
  strokes: Array<any>,
  effects: Array<any>,
  variables: {[key: string]: {resolvedType: string, value: any}},
  designTokens: {[category: string]: {[token: string]: any}},
  allLayersCSS: {[layerId: string]: string}  // CSS for every layer
}
```

**`get_figma_dev_history`** — List all past extractions:
```typescript
// Returns array of:
{
  id: string,
  name: string,
  timestamp: string,
  type?: string,
  layoutMode?: string
}
```

**`get_Basic_CSS`** — Root-level CSS only:
```typescript
// Arguments: { extractionId?: string }
// Returns: CSS string from getCSSAsync()
```

**`get_All_Layers_CSS`** — CSS for every layer in selection:
```typescript
// Arguments: { extractionId?: string }
// Returns: { [layerId: string]: string }
```

### Code Generation Tools

**`get_react_component`** — TypeScript React + CSS module:
```typescript
// Arguments: { extractionId?: string }
// Returns:
{
  component: string,  // .tsx file
  styles: string      // .module.css file
}
```

**`get_tailwind_component`** — React with Tailwind classes:
```typescript
// Arguments: { extractionId?: string }
// Returns: Single-file React component with inline Tailwind classes
```

**`get_styled_component`** — React + styled-components:
```typescript
// Arguments: { extractionId?: string }
// Returns: React component with styled-components CSS-in-JS
```

### Design Token Lifecycle

**`extract_design_tokens`** — Build token catalog from selection:
```typescript
// Arguments: { extractionId?: string }
// Returns:
{
  colors: {[name: string]: {value: string, type: string}},
  spacing: {[name: string]: {value: string, type: string}},
  typography: {[name: string]: {value: string, type: string}},
  // ... other categories
}
```

**`simulate_token_change`** — Dry-run a token modification:
```typescript
// Arguments:
{
  tokenPath: string,      // e.g., "colors.primary.500"
  newValue: any,
  reason?: string
}
// Returns: { simulationId: string, affected: string[] }
```

**`analyze_token_change_impact`** — Blast-radius analysis:
```typescript
// Arguments: { simulationId: string }
// Returns:
{
  affectedNodes: Array<{id, name, currentValue, newValue}>,
  breakingChanges: Array<{issue, severity}>,
  recommendations: string[]
}
```

**`apply_token_change`** — Commit a simulated change:
```typescript
// Arguments: { simulationId: string }
// Returns: { success: boolean, appliedChanges: number }
```

**`rollback_token_change`** — Revert an applied change:
```typescript
// Arguments: { simulationId: string }
// Returns: { success: boolean, rolledBackChanges: number }
```

**`generate_migration_code`** — Produce codemod output:
```typescript
// Arguments: { simulationId: string, format?: 'js' | 'ts' | 'css' }
// Returns: { code: string, instructions: string }
```

**`track_design_system_health`** — Coverage & conflict report:
```typescript
// Returns:
{
  tokenCoverage: number,  // percentage
  conflicts: Array<{token, instances, values}>,
  orphanedTokens: string[],
  recommendations: string[]
}
```

### Figma REST API Tools

Require `FIGMA_API_KEY` and file access (team/project). **Do not work on Drafts.**

**`get_figma_data`** — Raw file or node JSON:
```typescript
// Arguments:
{
  fileKey: string,      // From Figma URL
  nodeId?: string       // Optional: specific node
}
// Returns: Full Figma API response
```

**`get_figma_page_structure`** — Page-level tree:
```typescript
// Arguments: { fileKey: string }
// Returns:
{
  pages: Array<{
    id: string,
    name: string,
    children: Array<{id, name, type}>
  }>
}
```

**`download_figma_images`** — Batch export assets:
```typescript
// Arguments:
{
  fileKey: string,
  nodeIds: string[],
  format: 'svg' | 'png' | 'jpg',
  scale?: number,
  outputDir?: string
}
// Returns: { downloads: Array<{nodeId, path}> }
```

**`analyze_figma_components`** — Component detection:
```typescript
// Arguments: { fileKey: string }
// Returns:
{
  components: Array<{
    id: string,
    name: string,
    description?: string,
    instances: number
  }>
}
```

### Figma Dev Mode Tools (Professional Plan Only)

Bridge to Figma's official Dev Mode MCP Server (`localhost:3845`).

**`check_figma_dev_connection`** — Test Dev Mode server:
```typescript
// No arguments
// Returns: { connected: boolean, error?: string }
```

**`get_figma_dev_mode_code`** — Official React + Tailwind generator:
```typescript
// Arguments: { fileKey: string, nodeId: string }
// Returns: { code: string, format: string }
```

## Common Usage Patterns

### Pattern 1: Extract and Generate Component

```typescript
// User selects a frame in Figma and runs the plugin.
// Agent workflow:

// 1. Check extraction history
const history = await use_mcp_tool("sunnyside-figma", "get_figma_dev_history", {});
const latestExtraction = history[0];

// 2. Get full structured data
const data = await use_mcp_tool("sunnyside-figma", "get_JSON", {
  extractionId: latestExtraction.id
});

// 3. Generate Tailwind component
const component = await use_mcp_tool("sunnyside-figma", "get_tailwind_component", {
  extractionId: latestExtraction.id
});

// Write component to file
await writeFile("./components/HeroSection.tsx", component);
```

### Pattern 2: Design System Audit

```typescript
// User clicks "Scan Entire Project" in plugin

// 1. Get project overview
const overview = await use_mcp_tool("sunnyside-figma", "get_plugin_project_overview", {});

// 2. Extract design tokens
const tokens = await use_mcp_tool("sunnyside-figma", "extract_design_tokens", {});

// 3. Check health metrics
const health = await use_mcp_tool("sunnyside-figma", "track_design_system_health", {});

// 4. Report conflicts
if (health.conflicts.length > 0) {
  console.log("Token conflicts detected:");
  health.conflicts.forEach(conflict => {
    console.log(`- ${conflict.token}: ${conflict.instances} instances with different values`);
  });
}
```

### Pattern 3: Safe Token Migration

```typescript
// User wants to rename "primary-500" to "brand-primary"

// 1. Simulate the change
const simulation = await use_mcp_tool("sunnyside-figma", "simulate_token_change", {
  tokenPath: "colors.primary.500",
  newValue: "brand-primary",
  reason: "Align with new brand guidelines"
});

// 2. Analyze impact
const impact = await use_mcp_tool("sunnyside-figma", "analyze_token_change_impact", {
  simulationId: simulation.simulationId
});

console.log(`Affects ${impact.affectedNodes.length} nodes`);
console.log(`Breaking changes: ${impact.breakingChanges.length}`);

// 3. Generate migration code
const migration = await use_mcp_tool("sunnyside-figma", "generate_migration_code", {
  simulationId: simulation.simulationId,
  format: "ts"
});

await writeFile("./migrations/rename-primary-token.ts", migration.code);

// 4. If safe, apply
if (impact.breakingChanges.length === 0) {
  await use_mcp_tool("sunnyside-figma", "apply_token_change", {
    simulationId: simulation.simulationId
  });
}
```

### Pattern 4: Headless Asset Export from URL

```typescript
// User provides Figma URL: https://www.figma.com/file/ABC123/Design?node-id=10%3A52

// 1. Parse URL
const fileKey = "ABC123";
const nodeId = "10:52";

// 2. Get node data
const nodeData = await use_mcp_tool("sunnyside-figma", "get_figma_data", {
  fileKey,
  nodeId
});

// 3. Export as SVG
const exports = await use_mcp_tool("sunnyside-figma", "download_figma_images", {
  fileKey,
  nodeIds: [nodeId],
  format: "svg",
  outputDir: "./assets"
});

console.log(`Exported to: ${exports.downloads[0].path}`);
```

### Pattern 5: Multi-Layer CSS Extraction

```typescript
// User selects complex component with nested layers

// 1. Get latest extraction
const history = await use_mcp_tool("sunnyside-figma", "get_figma_dev_history", {});
const extractionId = history[0].id;

// 2. Get CSS for all layers
const allCSS = await use_mcp_tool("sunnyside-figma", "get_All_Layers_CSS", {
  extractionId
});

// 3. Get structured data for layer names
const data = await use_mcp_tool("sunnyside-figma", "get_JSON", {
  extractionId
});

// 4. Build CSS module with named classes
let cssModule = "";
Object.entries(allCSS).forEach(([layerId, css]) => {
  const layerName = findLayerName(data, layerId);
  cssModule += `.${toClassName(layerName)} {\n${css}\n}\n\n`;
});

await writeFile("./styles/component.module.css", cssModule);
```

## Troubleshooting

### "No extracted data available"

**Cause:** Plugin hasn't sent data or client is using stdio (separate process).

**Solution:**
1. Re-open Figma plugin and click **Extract Dev Code**
2. If using stdio transport, switch to SSE to share state with the HTTP server:
   ```json
   {
     "mcpServers": {
       "sunnyside-figma": {
         "type": "sse",
         "url": "http://localhost:3333/sse"
       }
     }
   }
   ```

### Figma REST API 404 / Timeout

**Cause:** File is in Drafts or token lacks access.

**Solution:**
- Move file from Drafts to a team/project
- Verify `FIGMA_API_KEY` has correct permissions
- Fallback to plugin-bridge tools (work on Drafts)

### `check_figma_dev_connection` Fails

**Cause:** Figma Dev Mode MCP Server not enabled or Free plan.

**Solution:**
- Requires Figma Professional plan
- Enable in Figma Desktop: **Preferences → Enable local MCP Server**
- Dev Mode server must be running on `localhost:3845`
- Free plan users: use plugin-bridge tools instead

### Server Won't Start on Port 3333

**Cause:** Port already in use.

**Solution:**
```env
# Change in .env
PORT=3334
```
Update MCP client URL: `http://localhost:3334/sse`

### Token Simulation Not Showing Changes

**Cause:** Simulation not applied or extraction is stale.

**Solution:**
1. Check simulation list:
   ```typescript
   await use_mcp_tool("sunnyside-figma", "list_token_simulations", {});
   ```
2. Apply simulation:
   ```typescript
   await use_mcp_tool("sunnyside-figma", "apply_token_change", {
     simulationId: "sim-123"
   });
   ```
3. Re-extract from Figma plugin to see changes

### Plugin Shows "Failed to Send Data"

**Cause:** MCP server not running or wrong port.

**Solution:**
1. Verify server is running: `npm start`
2. Check console for `Server running on port 3333`
3. Plugin sends to hardcoded `localhost:3333` — if using different port, update plugin code:
   ```typescript
   // figma-dev-plugin/code.ts
   const response = await fetch('http://localhost:YOUR_PORT/plugin/extract', {
     method: 'POST',
     // ...
   });
   ```

## Key Configuration Options

**Environment Variables:**
```env
# Required
FIGMA_API_KEY=figd_your_token_here

# Optional
PORT=3333                    # HTTP server port
OUTPUT_FORMAT=json           # Response format (json | text)
FIGMA_DEV_MODE_URL=http://localhost:3845  # Official Dev Mode server
```

**Plugin Configuration:**

Edit `figma-dev-plugin/manifest.json` to adjust plugin metadata:
```json
{
  "name": "Sunnyside Dev Extractor",
  "id": "your-plugin-id",
  "api": "1.0.0",
  "main": "code.js",
  "ui": "ui.html",
  "editorType": ["figma"]
}
```

## Development Commands

```bash
npm run dev          # Watch mode build (tsup)
npm run dev:cli      # stdio development loop
npm run type-check   # TypeScript validation
npm run lint         # ESLint
npm test             # Jest test suite
npm run inspect      # Open MCP inspector UI
npm run build        # Production build
```

## Tool Selection Guide

| Goal | Use Tool | Why |
|------|----------|-----|
| Get comprehensive layer data | `get_JSON` | Single call returns layout, fills, variables, tokens, and CSS for all layers |
| Generate production component | `get_tailwind_component` or `get_react_component` | Ready-to-use code with styling |
| Audit design system | `get_plugin_project_overview` + `track_design_system_health` | Full project scan with token coverage |
| Plan token refactor | `simulate_token_change` → `analyze_token_change_impact` | Safe what-if analysis |
| Export assets headlessly | `download_figma_images` | Batch SVG/PNG export from file key |
| Use official Figma codegen | `get_figma_dev_mode_code` | Requires Pro plan, uses Figma's generator |

**Plugin vs. REST API decision tree:**
- **Need Drafts support?** → Plugin tools
- **Headless automation?** → REST API tools
- **Highest CSS fidelity?** → Plugin (uses native `getCSSAsync()`)
- **Batch export many files?** → REST API tools

## Advanced: Token Registry Architecture

The token lifecycle tools maintain an in-memory registry:

```typescript
// Internal structure (reference only)
interface TokenRegistry {
  tokens: Map<string, {
    value: any,
    type: string,
    path: string[]
  }>,
  dependencies: Map<string, Set<string>>,  // token -> nodeIds
  simulations: Map<string, {
    changes: Array<{tokenPath, oldValue, newValue}>,
    applied: boolean
  }>
}
```

**Query registry state:**
```typescript
const registry = await use_mcp_tool("sunnyside-figma", "debug_token_registry", {});
```

**Build dependency graph:**
```typescript
const graph = await use_mcp_tool("sunnyside-figma", "build_dependency_graph", {
  extractionId: "latest"
});
// Returns: { tokens: {...}, edges: [...] }
```

This enables surgical updates: when a token changes, only affected components need regeneration.
