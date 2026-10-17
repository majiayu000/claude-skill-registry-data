---
name: figma-console-mcp-skills
description: Use powerful Figma Console MCP capabilities as Markdown skills for design tokens, variables, components, WCAG lint, a11y audits, version history, FigJam & Slides
triggers:
  - export figma design tokens to code
  - audit figma file accessibility
  - generate component documentation from figma
  - import tokens into figma variables
  - analyze figma component variants
  - create figma version changelog
  - lint figma design for wcag compliance
  - manage figma variables programmatically
---

# Figma Console MCP Skills

> Skill by [ara.so](https://ara.so) — Design Skills collection.

A comprehensive collection of 22 self-contained skills that extend the native Figma MCP server with design-systems workflows: design token export/import (DTCG, CSS, Tailwind), variable management, component analysis, WCAG linting, accessibility audits, version history, and FigJam/Slides authoring. Each skill is a Markdown playbook with ready-to-paste JavaScript for the `use_figma` tool.

## Installation

**Prerequisites:**
- Native Figma MCP server configured with OAuth
- The official `figma-use` skill (provides Figma Plugin API reference)
- For 4 REST skills only: Figma personal access token in `$FIGMA_TOKEN`

**Option 1: Clone all skills**
```bash
git clone https://github.com/PercentProduction/figma-console-mcp-skills-347.git
cd figma-console-mcp-skills-347
npm install
npm start
```

**Option 2: Copy individual skills**
```bash
# Each skill folder is self-contained
cp -R figma-console-mcp-skills-347/figma-export-tokens ~/.claude/skills/
cp -R figma-console-mcp-skills-347/figma-lint-design ~/.claude/skills/
```

**Option 3: Claude Desktop/Web (no terminal)**
- Compress individual skill folders (e.g., `figma-export-tokens.zip`)
- Upload via **Create / upload a skill** in Claude
- Toggle skill on

## Core Concepts

### Skill Structure
Each skill is a folder containing:
- `SKILL.md` — playbook with YAML frontmatter
- `scripts/*.js` — ready-to-paste snippets for `use_figma`
- `scripts/*.mjs` / `*.sh` — Node/bash for REST skills
- `references/` — skill-specific documentation (self-contained)

### use_figma Conventions
Scripts follow these patterns:
```javascript
// Top-level await supported
const nodes = await figma.currentPage.findAll(n => n.type === 'FRAME');

// Inline inputs (no external deps)
const collectionName = "Brand Tokens";

// Return for output
return {
  nodeCount: nodes.length,
  data: nodes.map(n => ({ id: n.id, name: n.name }))
};
```

## Key Skills Overview

### 🎨 Tokens & Variables

#### figma-export-tokens
Export Figma variables to code-ready formats (DTCG, CSS, Tailwind, SCSS, TypeScript).

**Use case:** Export design tokens for consumption in code

**Example: Export to DTCG JSON**
```javascript
// In use_figma tool
const collections = await figma.variables.getLocalVariableCollectionsAsync();
const collection = collections.find(c => c.name === "Semantic Tokens");

const modes = collection.modes;
const variables = await Promise.all(
  collection.variableIds.map(id => figma.variables.getVariableByIdAsync(id))
);

// Resolve aliases recursively
async function resolveValue(value) {
  if (value.type === 'VARIABLE_ALIAS') {
    const aliasVar = await figma.variables.getVariableByIdAsync(value.id);
    return resolveValue(aliasVar.valuesByMode[Object.keys(aliasVar.valuesByMode)[0]]);
  }
  return value;
}

const dtcg = {};
for (const variable of variables) {
  for (const mode of modes) {
    const rawValue = variable.valuesByMode[mode.modeId];
    const resolved = await resolveValue(rawValue);
    
    dtcg[variable.name] = {
      $type: variable.resolvedType.toLowerCase(),
      $value: resolved,
      $description: variable.description || undefined
    };
  }
}

return JSON.stringify(dtcg, null, 2);
```

**Example: Export to CSS Custom Properties**
```javascript
const collections = await figma.variables.getLocalVariableCollectionsAsync();
const vars = [];

for (const collection of collections) {
  const variables = await Promise.all(
    collection.variableIds.map(id => figma.variables.getVariableByIdAsync(id))
  );
  
  for (const variable of variables) {
    const value = variable.valuesByMode[Object.keys(variable.valuesByMode)[0]];
    const cssName = `--${variable.name.toLowerCase().replace(/\s+/g, '-')}`;
    
    if (typeof value === 'object' && value.r !== undefined) {
      // Color
      const r = Math.round(value.r * 255);
      const g = Math.round(value.g * 255);
      const b = Math.round(value.b * 255);
      vars.push(`${cssName}: rgb(${r}, ${g}, ${b});`);
    } else if (typeof value === 'number') {
      vars.push(`${cssName}: ${value}px;`);
    } else {
      vars.push(`${cssName}: ${value};`);
    }
  }
}

return `:root {\n  ${vars.join('\n  ')}\n}`;
```

#### figma-import-tokens
Push tokens (DTCG/JSON) into Figma as variables.

**Use case:** Sync tokens from code back into Figma

**Example: Import DTCG JSON**
```javascript
// Input: dtcgJson (string)
const tokens = JSON.parse(dtcgJson);
let collection = await figma.variables.getLocalVariableCollectionsAsync()
  .then(cols => cols.find(c => c.name === "Imported Tokens"));

if (!collection) {
  collection = figma.variables.createVariableCollection("Imported Tokens");
}

for (const [name, token] of Object.entries(tokens)) {
  const existing = await figma.variables.getLocalVariablesAsync()
    .then(vars => vars.find(v => v.name === name));
  
  let variable;
  if (existing) {
    variable = existing;
  } else {
    const resolvedType = token.$type === 'color' ? 'COLOR' : 'FLOAT';
    variable = figma.variables.createVariable(name, collection.id, resolvedType);
  }
  
  const modeId = collection.modes[0].modeId;
  
  if (token.$type === 'color') {
    const hex = token.$value;
    const r = parseInt(hex.slice(1, 3), 16) / 255;
    const g = parseInt(hex.slice(3, 5), 16) / 255;
    const b = parseInt(hex.slice(5, 7), 16) / 255;
    variable.setValueForMode(modeId, { r, g, b });
  } else {
    variable.setValueForMode(modeId, parseFloat(token.$value));
  }
  
  if (token.$description) {
    variable.description = token.$description;
  }
}

return { imported: Object.keys(tokens).length };
```

#### figma-manage-variables
CRUD operations for variables: create, update, delete, batch operations, scopes.

**Example: Batch create variables**
```javascript
const specs = [
  { name: "spacing/sm", value: 8, type: "FLOAT" },
  { name: "spacing/md", value: 16, type: "FLOAT" },
  { name: "spacing/lg", value: 24, type: "FLOAT" }
];

const collection = figma.variables.createVariableCollection("Spacing");
const modeId = collection.modes[0].modeId;

for (const spec of specs) {
  const variable = figma.variables.createVariable(spec.name, collection.id, spec.type);
  variable.setValueForMode(modeId, spec.value);
  variable.scopes = ['ALL_SCOPES'];
}

return { created: specs.length, collectionId: collection.id };
```

### 🧩 Components & Design System

#### figma-analyze-component-set
Extract variant state machine, CSS pseudo-class mappings, visual diffs.

**Example: Extract variant states**
```javascript
const componentSet = figma.currentPage.selection[0];
if (componentSet.type !== 'COMPONENT_SET') {
  throw new Error('Select a component set');
}

const variants = componentSet.children.filter(c => c.type === 'COMPONENT');
const properties = {};

for (const variant of variants) {
  const props = variant.name.split(', ').reduce((acc, pair) => {
    const [key, value] = pair.split('=');
    acc[key.trim()] = value.trim();
    return acc;
  }, {});
  
  for (const [key, value] of Object.entries(props)) {
    if (!properties[key]) properties[key] = new Set();
    properties[key].add(value);
  }
}

// Convert Sets to arrays
const stateMachine = Object.fromEntries(
  Object.entries(properties).map(([k, v]) => [k, Array.from(v)])
);

// Map to CSS pseudo-classes
const cssPseudoMap = {};
if (stateMachine.State) {
  cssPseudoMap.State = {
    'Hover': ':hover',
    'Active': ':active',
    'Focus': ':focus',
    'Disabled': ':disabled'
  };
}

return { stateMachine, cssPseudoMap, variantCount: variants.length };
```

#### figma-deep-component
Unlimited-depth component tree with resolved tokens and mainComponent refs.

**Example: Deep traverse component**
```javascript
async function deepTraverse(node, depth = 0) {
  const result = {
    id: node.id,
    name: node.name,
    type: node.type,
    depth
  };
  
  if (node.type === 'INSTANCE') {
    result.mainComponent = {
      id: node.mainComponent.id,
      name: node.mainComponent.name,
      key: node.mainComponent.key
    };
  }
  
  // Resolve bound variables
  if (node.boundVariables) {
    result.boundVariables = {};
    for (const [field, binding] of Object.entries(node.boundVariables)) {
      if (binding.type === 'VARIABLE_ALIAS') {
        const variable = await figma.variables.getVariableByIdAsync(binding.id);
        result.boundVariables[field] = {
          name: variable.name,
          value: variable.valuesByMode[Object.keys(variable.valuesByMode)[0]]
        };
      }
    }
  }
  
  if ('children' in node) {
    result.children = await Promise.all(
      node.children.map(child => deepTraverse(child, depth + 1))
    );
  }
  
  return result;
}

const selected = figma.currentPage.selection[0];
return await deepTraverse(selected);
```

### ♿ Quality & Accessibility

#### figma-lint-design
WCAG 2.2 + design-system quality lint over node tree.

**Example: Color contrast check**
```javascript
function getContrast(fg, bg) {
  const luminance = (c) => {
    const val = c / 255;
    return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
  };
  
  const l1 = 0.2126 * luminance(fg.r * 255) + 0.7152 * luminance(fg.g * 255) + 0.0722 * luminance(fg.b * 255);
  const l2 = 0.2126 * luminance(bg.r * 255) + 0.7152 * luminance(bg.g * 255) + 0.0722 * luminance(bg.b * 255);
  
  return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
}

const issues = [];
const textNodes = figma.currentPage.findAll(n => n.type === 'TEXT');

for (const node of textNodes) {
  const fontSize = node.fontSize;
  const fills = node.fills;
  
  if (fills.length > 0 && fills[0].type === 'SOLID') {
    const parent = node.parent;
    let bgColor = { r: 1, g: 1, b: 1 }; // default white
    
    if (parent.fills && parent.fills.length > 0 && parent.fills[0].type === 'SOLID') {
      bgColor = parent.fills[0].color;
    }
    
    const contrast = getContrast(fills[0].color, bgColor);
    const minContrast = fontSize >= 18 ? 3 : 4.5; // WCAG AA
    
    if (contrast < minContrast) {
      issues.push({
        nodeId: node.id,
        nodeName: node.name,
        issue: `Insufficient contrast: ${contrast.toFixed(2)}:1 (needs ${minContrast}:1)`,
        wcag: 'WCAG 2.2 Level AA - 1.4.3 Contrast (Minimum)'
      });
    }
  }
}

return { totalIssues: issues.length, issues };
```

#### figma-audit-accessibility
Per-component a11y scorecard: state coverage, focus, target size.

**Example: Check touch target size**
```javascript
const MIN_TOUCH_TARGET = 44; // WCAG 2.2 AAA

const interactiveNodes = figma.currentPage.findAll(n => 
  n.type === 'INSTANCE' && 
  (n.name.includes('Button') || n.name.includes('Input'))
);

const violations = [];

for (const node of interactiveNodes) {
  if (node.width < MIN_TOUCH_TARGET || node.height < MIN_TOUCH_TARGET) {
    violations.push({
      nodeId: node.id,
      nodeName: node.name,
      size: { width: node.width, height: node.height },
      issue: `Touch target too small (minimum ${MIN_TOUCH_TARGET}x${MIN_TOUCH_TARGET}px)`,
      wcag: 'WCAG 2.2 Level AAA - 2.5.5 Target Size'
    });
  }
}

return { 
  totalChecked: interactiveNodes.length, 
  violations: violations.length,
  details: violations 
};
```

### 🕓 Versioning & Collaboration (REST API)

**Setup required:**
```bash
export FIGMA_TOKEN="figd_your_token_here"
```

#### figma-version-history
List versions, snapshot a version, diff two versions.

**Example: List recent versions (Node.js)**
```javascript
// scripts/list-versions.mjs
const fileKey = process.argv[2];
const token = process.env.FIGMA_TOKEN;

const response = await fetch(
  `https://api.figma.com/v1/files/${fileKey}/versions`,
  { headers: { 'X-Figma-Token': token } }
);

const data = await response.json();
console.log(JSON.stringify(data.versions.slice(0, 10), null, 2));
```

#### figma-generate-changelog
Human-readable markdown changelog between versions.

**Example: Generate changelog**
```javascript
// scripts/changelog.mjs
const fileKey = process.argv[2];
const fromVersion = process.argv[3];
const toVersion = process.argv[4];
const token = process.env.FIGMA_TOKEN;

// Fetch both versions
const [v1, v2] = await Promise.all([
  fetch(`https://api.figma.com/v1/files/${fileKey}?version=${fromVersion}`, {
    headers: { 'X-Figma-Token': token }
  }).then(r => r.json()),
  fetch(`https://api.figma.com/v1/files/${fileKey}?version=${toVersion}`, {
    headers: { 'X-Figma-Token': token }
  }).then(r => r.json())
]);

// Compare node counts
const changes = [];
const v1Nodes = new Set(Object.keys(v1.document));
const v2Nodes = new Set(Object.keys(v2.document));

const added = [...v2Nodes].filter(id => !v1Nodes.has(id));
const removed = [...v1Nodes].filter(id => !v2Nodes.has(id));

console.log(`# Changelog\n\n## Added (${added.length})\n`);
console.log(`## Removed (${removed.length})\n`);
```

#### figma-comments
Read / post / reply / delete file comments.

**Example: List comments**
```javascript
// scripts/list-comments.mjs
const fileKey = process.argv[2];
const token = process.env.FIGMA_TOKEN;

const response = await fetch(
  `https://api.figma.com/v1/files/${fileKey}/comments`,
  { headers: { 'X-Figma-Token': token } }
);

const data = await response.json();
for (const comment of data.comments) {
  console.log(`${comment.user.handle}: ${comment.message}`);
  console.log(`  Created: ${new Date(comment.created_at).toLocaleString()}`);
  if (comment.client_meta?.node_id) {
    console.log(`  Node: ${comment.client_meta.node_id}`);
  }
}
```

**Example: Post comment**
```javascript
// scripts/post-comment.mjs
const fileKey = process.argv[2];
const message = process.argv[3];
const nodeId = process.argv[4]; // optional
const token = process.env.FIGMA_TOKEN;

const body = {
  message,
  ...(nodeId && { client_meta: { node_id: [nodeId] } })
};

await fetch(`https://api.figma.com/v1/files/${fileKey}/comments`, {
  method: 'POST',
  headers: {
    'X-Figma-Token': token,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(body)
});
```

### 📝 Documentation & Annotations

#### figma-generate-component-doc
Generate complete component documentation markdown.

**Example: Document component**
```javascript
const component = figma.currentPage.selection[0];
if (component.type !== 'COMPONENT') {
  throw new Error('Select a component');
}

const doc = [`# ${component.name}\n`];
doc.push(`**Description:** ${component.description || 'No description'}\n`);

// Properties
if (component.componentPropertyDefinitions) {
  doc.push(`## Properties\n`);
  for (const [name, def] of Object.entries(component.componentPropertyDefinitions)) {
    doc.push(`- **${name}** (${def.type})`);
    if (def.type === 'VARIANT' && def.variantOptions) {
      doc.push(`  - Options: ${def.variantOptions.join(', ')}`);
    }
    if (def.defaultValue !== undefined) {
      doc.push(`  - Default: ${def.defaultValue}`);
    }
  }
  doc.push('');
}

// Bound variables
const boundVars = [];
function findBoundVariables(node) {
  if (node.boundVariables) {
    for (const [field, binding] of Object.entries(node.boundVariables)) {
      if (binding.type === 'VARIABLE_ALIAS') {
        boundVars.push({ nodeId: node.id, field, varId: binding.id });
      }
    }
  }
  if ('children' in node) {
    node.children.forEach(findBoundVariables);
  }
}
findBoundVariables(component);

if (boundVars.length > 0) {
  doc.push(`## Design Tokens (${boundVars.length})\n`);
  for (const { field, varId } of boundVars) {
    const variable = await figma.variables.getVariableByIdAsync(varId);
    doc.push(`- **${field}**: \`${variable.name}\``);
  }
}

return doc.join('\n');
```

### 🎯 FigJam & Slides

#### figjam-create-content
Author FigJam: stickies, connectors, shapes, tables.

**Example: Create sticky note**
```javascript
// Must be in a FigJam file
const sticky = figma.createSticky();
sticky.x = 100;
sticky.y = 100;
sticky.resize(200, 200);

await figma.loadFontAsync({ family: "Inter", style: "Regular" });
sticky.text.characters = "TODO: Design tokens export";
sticky.fills = [{ type: 'SOLID', color: { r: 1, g: 0.9, b: 0.2 } }];

return { id: sticky.id, name: sticky.name };
```

**Example: Create connector**
```javascript
const nodes = figma.currentPage.selection;
if (nodes.length < 2) throw new Error('Select 2+ nodes');

const connector = figma.createConnector();
connector.connectorStart = {
  endpointNodeId: nodes[0].id,
  magnet: 'AUTO'
};
connector.connectorEnd = {
  endpointNodeId: nodes[1].id,
  magnet: 'AUTO'
};

return { id: connector.id };
```

#### figma-slides
Author Figma Slides: create/reorder slides, text/shapes.

**Example: Create slide with title**
```javascript
// Must be in a Figma Slides file
const slide = figma.createSlide();
slide.name = "Design System Overview";

await figma.loadFontAsync({ family: "Inter", style: "Bold" });
const title = figma.createText();
title.characters = "Design System Overview";
title.fontSize = 48;
title.x = 100;
title.y = 100;

slide.appendChild(title);

return { slideId: slide.id, titleId: title.id };
```

## Common Patterns

### Error Handling
```javascript
try {
  const result = await someOperation();
  return { success: true, data: result };
} catch (error) {
  return { success: false, error: error.message };
}
```

### Loading Fonts
```javascript
// Always load fonts before creating text
await figma.loadFontAsync({ family: "Inter", style: "Regular" });
const text = figma.createText();
text.characters = "Hello";
```

### Async Variable Resolution
```javascript
// Variables require async access
const collections = await figma.variables.getLocalVariableCollectionsAsync();
const variables = await Promise.all(
  collections[0].variableIds.map(id => figma.variables.getVariableByIdAsync(id))
);
```

### Finding Nodes
```javascript
// Find all text nodes
const textNodes = figma.currentPage.findAll(node => node.type === 'TEXT');

// Find specific component
const button = figma.currentPage.findOne(
  node => node.type === 'COMPONENT' && node.name.includes('Button')
);
```

## Troubleshooting

**"Script failed on first use_figma call"**
- Scripts are atomic — nothing applied if it errors
- Check error message for specific API issue
- Verify you're in the correct file type (Design vs FigJam vs Slides)

**"Cannot read property of undefined"**
- Ensure node selection is correct type
- Use type guards: `if (node.type !== 'COMPONENT') throw new Error(...)`

**"Font not found"**
- Always call `figma.loadFontAsync()` before creating/editing text
- Check font name and style match exactly

**"Variable not found"**
- Variables require async: `await figma.variables.getVariableByIdAsync(id)`
- Check variable exists in current file

**"REST skills not working"**
- Verify `$FIGMA_TOKEN` environment variable is set
- Confirm token has required scopes (file:read, file:write)
- REST skills only work in terminal-capable agents

**"Skill not loading"**
- Ensure `SKILL.md` is at root of skill folder
- For zips: compress the folder contents, not the folder itself
- Verify YAML frontmatter is valid

## Configuration

**Enable REST Skills:**
```bash
# Create personal access token at figma.com/settings
# Required scopes: file:read, file:write (for comments)
export FIGMA_TOKEN="figd_your_token_here"

# Persist in shell profile
echo 'export FIGMA_TOKEN="figd_your_token_here"' >> ~/.zshrc
```

**Figma MCP OAuth:**
- Configured once when adding Figma connector
- No token management needed for `use_figma` skills
- OAuth session automatically used by native tools

## Best Practices

1. **Always load `figma-use` skill first** — provides Plugin API reference
2. **Batch operations** — minimize async calls in loops
3. **Validate inputs** — check node types before operations
4. **Self-contained skills** — each skill folder has everything it needs
5. **Environment variables** — never hardcode tokens/secrets
6. **Error messages** — return structured error objects for debugging
7. **Type safety** — use TypeScript hints in comments for clarity

## Skill Invocation

**Implicit:** Natural language triggers skill matching
```
"Export my figma design tokens to CSS variables"
→ loads figma-export-tokens
```

**Explicit:** Direct skill invocation
```
/figma-lint-design
/figma-export-tokens
```

## Further Resources

- [Official Figma Plugin API](https://www.figma.com/plugin-docs/)
- [Figma REST API](https://www.figma.com/developers/api)
- [DTCG Specification](https://design-tokens.github.io/community-group/format/)
- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)
