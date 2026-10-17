---
name: prototype-to-figma-skill
description: Convert Claude Code prototypes into structured Figma design files with component mapping, state flows, and interaction annotations
triggers:
  - "convert this prototype to figma"
  - "explode this into figma frames for review"
  - "create figma specs from my prototype"
  - "put this prototype in figma so the team can review it"
  - "make this reviewable by designers in figma"
  - "generate figma frames from this working prototype"
  - "turn this into a figma file with annotations"
  - "export this prototype to figma with design system components"
---

# Prototype → Figma Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Converts working Claude Code prototypes into structured Figma design files by exploding interaction flows into state-by-state frames, mapping components to your Figma design system, and annotating triggers, transitions, and edge cases natively in Figma.

## What This Skill Does

When a user builds a prototype in Claude Code, this skill:

1. **Analyzes the prototype source** — inventories components, maps interaction flows, identifies all UI states
2. **Maps to design system** — searches linked Figma libraries for matching DS components; flags unmatched elements with "No DS match" badges
3. **Creates one frame per interaction state** — every meaningful step in a user flow becomes a separate Figma frame
4. **Annotates interactions** — adds native Figma Dev Mode annotations with filterable categories (Interaction, Navigation, Validation, Error Handling, etc.)
5. **Adds flow arrows** — visual connectors showing user path through states
6. **Creates overview frame** — table of contents with legend and open questions for reviewers
7. **Optionally links Code Connect** — maps Figma components back to codebase

## Key Capabilities

- **Design system aware** — uses real components from target file's linked libraries
- **Primitive fallback** — builds missing components from Figma primitives (never skips elements)
- **Multi-tier output** — builds directly in Figma on supported clients, generates spec documents on others
- **Code Connect integration** — creates bidirectional links between Figma and code
- **Automatic file creation** — creates new Figma file if no URL provided

## When to Use This Skill

User says things like:
- "Take this prototype and put it in Figma so the team can review it"
- "Explode this into Figma frames for async feedback"
- "Create Figma specs from my prototype for design review"
- "Make this prototype reviewable by the design team"

## Required MCP Tools

This skill requires the Figma MCP server with these tools available:

- `use_figma` — select target file
- `search_design_system` — find matching components
- `get_design_context` — understand file structure
- `get_metadata` — read component details
- `get_screenshot` — verify output
- `get_code_connect_map` — read existing mappings
- `get_context_for_code_connect` — understand component context
- `get_code_connect_suggestions` — get AI suggestions for mappings
- `send_code_connect_mappings` — batch create mappings
- `add_code_connect_map` — create individual mapping
- `whoami` — get user info for file creation
- `create_new_file` — create new Figma file

## Installation Check

Before using this skill, verify Figma MCP is installed:

```bash
# Check Claude Desktop config
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | grep figma

# Or for Claude Code
cat ~/.claude/mcp_config.json | grep figma
```

Expected output should include `@figma/mcp-server` or similar.

## Workflow Steps

### 1. Resolve Target File

If user provides Figma URL:
```typescript
await use_figma({
  url: "https://figma.com/design/abc123/MyFile"
});
```

If no URL provided, create new file:
```typescript
// Get user info
const user = await whoami();

// Create new file
const newFile = await create_new_file({
  name: `${prototypeName} — Prototype Review`,
  team_id: user.team_id // or user.default_team_id
});

await use_figma({ url: newFile.url });
```

### 2. Analyze Prototype Source

Read the prototype files and extract:
- Component inventory (Button, Input, Modal, etc.)
- Interaction flows (user actions → state changes)
- UI states (initial, loading, success, error, etc.)
- Data flows (form submissions, API calls, etc.)

Example analysis structure:
```typescript
interface PrototypeAnalysis {
  components: {
    name: string;        // e.g. "PrimaryButton"
    type: string;        // e.g. "Button"
    props: string[];     // e.g. ["label", "onClick", "disabled"]
    variants: string[];  // e.g. ["default", "hover", "disabled"]
  }[];
  flows: {
    name: string;        // e.g. "Login Flow"
    states: {
      id: string;        // e.g. "login-initial"
      label: string;     // e.g. "Login Form (Empty)"
      components: string[];
      interactions: {
        trigger: string; // e.g. "Click 'Sign In'"
        action: string;  // e.g. "Validate and submit"
        nextState: string; // e.g. "login-loading"
        condition?: string; // e.g. "If fields valid"
      }[];
    }[];
  }[];
}
```

### 3. Map to Design System

For each component in the prototype:

```typescript
// Search for matching DS component
const results = await search_design_system({
  query: componentName,
  component_type: componentType, // "Button", "Input", etc.
  limit: 5
});

// If match found, get metadata
if (results.length > 0) {
  const metadata = await get_metadata({
    node_id: results[0].node_id
  });
  
  // Store mapping
  componentMap.set(componentName, {
    figma_node_id: results[0].node_id,
    figma_name: results[0].name,
    variants: metadata.variants,
    props: metadata.properties
  });
} else {
  // Mark for primitive fallback
  componentMap.set(componentName, {
    needs_primitive_fallback: true,
    primitive_type: componentType
  });
}
```

### 4. Plan Page Structure

Organize frames by flow:

```
Page: "Login Flow"
├─ Overview Frame (legend + TOC)
├─ State 1: Login Form (Empty)
├─ State 2: Login Form (Validation Error)
├─ State 3: Login Form (Loading)
├─ State 4: Login Success
└─ State 5: Login Error (Network)
```

Calculate frame positions:
```typescript
const FRAME_WIDTH = 1440; // desktop, or 390 for mobile
const FRAME_HEIGHT = 900; // desktop, or 844 for mobile
const HORIZONTAL_SPACING = 200;
const VERTICAL_SPACING = 200;

function calculateFramePosition(index: number, perRow: number = 3) {
  const row = Math.floor(index / perRow);
  const col = index % perRow;
  
  return {
    x: col * (FRAME_WIDTH + HORIZONTAL_SPACING),
    y: row * (FRAME_HEIGHT + VERTICAL_SPACING)
  };
}
```

### 5. Build Frames in Figma

**CRITICAL**: Never call `createComponent()` — always use `createInstance()` for DS components or primitives for fallbacks.

For matched DS components:
```typescript
// Create instance of DS component
const buttonInstance = await figma.createInstance({
  component_id: componentMap.get("PrimaryButton").figma_node_id,
  parent_id: frameId,
  x: 100,
  y: 200,
  properties: {
    variant: "default",
    label: "Sign In"
  }
});
```

For components needing primitive fallback:
```typescript
// Build from primitives (example: Button)
const buttonGroup = await figma.createFrame({
  name: "Button (No DS match)",
  parent_id: frameId,
  x: 100,
  y: 200,
  width: 120,
  height: 40,
  fills: [{ type: "SOLID", color: { r: 0.2, g: 0.4, b: 1 } }],
  cornerRadius: 8
});

const buttonLabel = await figma.createText({
  parent_id: buttonGroup.id,
  characters: "Sign In",
  fontSize: 16,
  fills: [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }]
});

// Add "No DS match" badge
const badge = await figma.createFrame({
  name: "⚠️ No DS match",
  parent_id: buttonGroup.id,
  x: -10,
  y: -10,
  width: 100,
  height: 20,
  fills: [{ type: "SOLID", color: { r: 1, g: 0.8, b: 0 } }]
});
```

### 6. Add Annotations

Use native Figma Dev Mode annotations with categories:

```typescript
await figma.addAnnotation({
  node_id: buttonInstance.id,
  category: "Interaction",
  text: "Trigger: Click\nAction: Validate form fields\nNext: → Login Form (Loading) if valid, → Login Form (Error) if invalid"
});

await figma.addAnnotation({
  node_id: emailInput.id,
  category: "Validation",
  text: "Required field\nValidation: Must be valid email format\nError message: 'Please enter a valid email'"
});

await figma.addAnnotation({
  node_id: errorBanner.id,
  category: "Error Handling",
  text: "Shown when: Network request fails\nDuration: Persistent until dismissed\nDismiss: Click X icon or retry"
});
```

Categories to use:
- `Interaction` — clicks, hovers, focus
- `Navigation` — route changes, deep links
- `Validation` — input rules, error states
- `Error Handling` — error scenarios, recovery
- `Data Flow` — API calls, state updates
- `Edge Cases` — empty states, loading, timeouts

### 7. Add Flow Arrows

Create connector arrows between frames:

```typescript
await figma.createConnector({
  start_node_id: state1Frame.id,
  end_node_id: state2Frame.id,
  stroke_weight: 2,
  stroke_color: { r: 0.5, g: 0.5, b: 0.5 },
  label: "Click 'Sign In'"
});
```

### 8. Create Overview Frame

First frame in each flow page:

```typescript
const overviewFrame = await figma.createFrame({
  name: "📋 Overview",
  width: FRAME_WIDTH,
  height: FRAME_HEIGHT,
  fills: [{ type: "SOLID", color: { r: 0.98, g: 0.98, b: 0.98 } }]
});

// Add title
await figma.createText({
  parent_id: overviewFrame.id,
  characters: "Login Flow — Prototype Review",
  fontSize: 32,
  fontWeight: 700,
  y: 40
});

// Add legend
await figma.createText({
  parent_id: overviewFrame.id,
  characters: `Legend:
• 🟦 Frame = One UI state
• ➡️  Arrow = User action / transition
• 📝 Annotation = Interaction detail
• ⚠️  Badge = No design system match (built from primitives)`,
  fontSize: 16,
  y: 120
});

// Add TOC
await figma.createText({
  parent_id: overviewFrame.id,
  characters: `States in this flow:
1. Login Form (Empty)
2. Login Form (Validation Error)
3. Login Form (Loading)
4. Login Success
5. Login Error (Network)`,
  fontSize: 16,
  y: 250
});

// Add open questions
await figma.createText({
  parent_id: overviewFrame.id,
  characters: `Open questions for reviewers:
• Should "Forgot Password" link to modal or new page?
• Do we show loading spinner in button or overlay entire form?
• How long should success message persist?`,
  fontSize: 16,
  y: 450,
  fills: [{ type: "SOLID", color: { r: 0.8, g: 0.4, b: 0 } }]
});
```

### 9. Create Code Connect Mappings (Optional)

If user wants Code Connect integration:

```typescript
// Get existing mappings
const existingMaps = await get_code_connect_map({
  file_key: fileKey
});

// Get suggestions for unmapped components
const suggestions = await get_code_connect_suggestions({
  component_id: buttonComponentId,
  code_snippet: `<Button variant="primary" onClick={handleClick}>Sign In</Button>`
});

// Create mappings
const mappings = componentMap.entries().map(([codeName, figmaInfo]) => ({
  figma_node_id: figmaInfo.figma_node_id,
  code_location: `src/components/${codeName}.tsx`,
  code_snippet: getComponentSnippet(codeName),
  framework: "react" // or "vue", "svelte", etc.
}));

await send_code_connect_mappings({
  mappings: mappings
});
```

### 10. Verify and Present

```typescript
// Take screenshot of output
const screenshot = await get_screenshot({
  node_id: pageId,
  scale: 0.5 // overview scale
});

// Present to user
return `✅ Prototype converted to Figma!

File: ${figmaFileUrl}

Created:
• ${flowCount} flows
• ${frameCount} state frames
• ${annotationCount} interaction annotations
• ${componentMatchCount} design system components used
• ${primitiveFallbackCount} components built from primitives (flagged with ⚠️)

${codeConnectEnabled ? `Code Connect: ${mappingCount} mappings created` : ''}

Open questions for reviewers:
${openQuestions.join('\n')}

[Screenshot attached]`;
```

## Common Patterns

### Pattern: Detecting Prototype Framework

```typescript
function detectFramework(prototypeFiles: string[]): string {
  const hasReact = prototypeFiles.some(f => 
    f.includes('import React') || f.includes('from "react"')
  );
  const hasVue = prototypeFiles.some(f => 
    f.includes('<template>') || f.includes('from "vue"')
  );
  const hasSvelte = prototypeFiles.some(f => 
    f.includes('<script>') && f.endsWith('.svelte')
  );
  
  if (hasReact) return 'react';
  if (hasVue) return 'vue';
  if (hasSvelte) return 'svelte';
  return 'html'; // vanilla
}
```

### Pattern: Grouping Micro-Interactions

Group very small interactions (hover, focus) into a single frame with annotations:

```typescript
function shouldGroupInteractions(interactions: Interaction[]): boolean {
  // If all interactions are micro-interactions (hover, focus, blur)
  const microTypes = ['hover', 'focus', 'blur', 'mouseover', 'mouseout'];
  return interactions.every(i => microTypes.includes(i.type));
}

// Instead of 5 frames for hover states, create 1 frame with annotations:
await figma.addAnnotation({
  node_id: button.id,
  category: "Interaction",
  text: `Hover: Background darkens to #1a3d8f
Focus: 2px blue outline appears
Click: Ripple animation, navigate to /dashboard`
});
```

### Pattern: Handling Responsive Variants

```typescript
function explodeResponsiveStates(state: UIState): UIState[] {
  if (!state.hasResponsiveVariants) return [state];
  
  return [
    { ...state, viewport: 'mobile', frameWidth: 390, frameHeight: 844 },
    { ...state, viewport: 'tablet', frameWidth: 768, frameHeight: 1024 },
    { ...state, viewport: 'desktop', frameWidth: 1440, frameHeight: 900 }
  ];
}
```

### Pattern: Primitive Button Fallback

```typescript
async function createPrimitiveButton(
  parent_id: string,
  x: number,
  y: number,
  label: string,
  variant: 'primary' | 'secondary' = 'primary'
) {
  const colors = {
    primary: { bg: { r: 0.2, g: 0.4, b: 1 }, fg: { r: 1, g: 1, b: 1 } },
    secondary: { bg: { r: 0.95, g: 0.95, b: 0.95 }, fg: { r: 0.2, g: 0.2, b: 0.2 } }
  };
  
  const group = await figma.createFrame({
    name: `Button: ${label} (No DS match)`,
    parent_id,
    x,
    y,
    width: Math.max(120, label.length * 10),
    height: 40,
    fills: [{ type: "SOLID", color: colors[variant].bg }],
    cornerRadius: 8,
    paddingLeft: 16,
    paddingRight: 16
  });
  
  await figma.createText({
    parent_id: group.id,
    characters: label,
    fontSize: 16,
    fontWeight: 500,
    fills: [{ type: "SOLID", color: colors[variant].fg }],
    textAlignHorizontal: "CENTER",
    textAlignVertical: "CENTER"
  });
  
  // Add badge
  await figma.createFrame({
    name: "⚠️ No DS match",
    parent_id: group.id,
    x: -12,
    y: -12,
    width: 110,
    height: 24,
    fills: [{ type: "SOLID", color: { r: 1, g: 0.8, b: 0 } }],
    cornerRadius: 4
  });
  
  return group;
}
```

## Troubleshooting

### "No Figma MCP tools available"

**Cause**: Figma MCP server not installed or not running.

**Solution**:
```bash
# Install Figma MCP
npx @figma/mcp-server init

# Or check Claude Desktop config
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### "Cannot create component"

**Cause**: Skill is calling `createComponent()` instead of using instances or primitives.

**Solution**: NEVER call `createComponent()`. Always:
- Use `createInstance()` for DS components
- Build from primitives (`createFrame`, `createText`, etc.) for fallbacks

### "Design system search returns no results"

**Cause**: Target file has no linked libraries, or component naming mismatch.

**Solution**:
- Verify linked libraries in Figma file settings
- Try fuzzy search: `search_design_system({ query: "btn primary" })` instead of exact "PrimaryButton"
- Fall back to primitives if no match after 2-3 search attempts

### "Too many frames created"

**Cause**: Exploding every micro-interaction into separate frames.

**Solution**: Group hover/focus/blur into single frame with annotations (see pattern above).

### "Annotations not visible"

**Cause**: User not in Dev Mode, or annotations have no category.

**Solution**: Always specify category. Remind user to switch to Dev Mode in Figma.

### "Code Connect mappings fail"

**Cause**: Invalid code snippet format, or component not in file.

**Solution**:
```typescript
// Get context first
const context = await get_context_for_code_connect({
  component_id: nodeId
});

// Then create mapping with valid snippet
await add_code_connect_map({
  figma_node_id: nodeId,
  code_location: "src/components/Button.tsx",
  code_snippet: `import { Button } from "./Button";\n\n<Button variant="primary">Click me</Button>`,
  framework: "react"
});
```

## Output Tier Compatibility

This skill produces different outputs based on client capabilities:

**Tier 1** (Full build in Figma): Claude Code, Claude Desktop, Cursor, VS Code, Copilot CLI, Augment Code, Factory, Firebender, Codex
- Builds frames directly in Figma
- Creates Code Connect mappings
- Adds native annotations

**Tier 2** (Spec document): Android Studio, Gemini CLI, Kiro, Amazon Q, Openhands
- Generates markdown spec document
- Includes frame-by-frame descriptions
- No direct Figma manipulation

**Tier 3** (Build only): Replit
- Builds frames in Figma
- No Code Connect support

Check available tools at runtime:
```typescript
const hasCodeConnect = tools.includes('get_code_connect_suggestions');
const canBuildInFigma = tools.includes('use_figma');
```

## Environment Variables

This skill does not require API keys — it uses Figma MCP tools which handle authentication via OAuth.

Users must have Figma account connected to their Claude client.

## Best Practices

1. **Always verify file access** — call `use_figma()` before any other Figma operations
2. **Never skip elements** — if no DS match, build from primitives and flag with badge
3. **Group micro-interactions** — don't create 10 frames for hover states
4. **Organize by flow** — one page per user flow, not one giant page
5. **Use consistent naming** — "State 1: [Description]" format for frame names
6. **Add legend on every page** — overview frame explaining notation
7. **Flag open questions** — surface design decisions that need input
8. **Take screenshots** — verify output before presenting to user
9. **Provide file URL** — always share direct link to Figma file in response

## Example Full Workflow

```typescript
// User: "Put this login prototype in Figma"

// 1. Create new file (no URL provided)
const user = await whoami();
const file = await create_new_file({
  name: "Login Prototype — Review",
  team_id: user.team_id
});
await use_figma({ url: file.url });

// 2. Analyze prototype
const analysis = analyzePrototype(prototypeFiles);
// → { flows: [{ name: "Login Flow", states: [...] }], components: [...] }

// 3. Map components
for (const comp of analysis.components) {
  const results = await search_design_system({
    query: comp.name,
    component_type: comp.type
  });
  if (results.length > 0) {
    componentMap.set(comp.name, results[0]);
  } else {
    componentMap.set(comp.name, { primitive: true, type: comp.type });
  }
}

// 4. Create page
const page = await figma.createPage({ name: "Login Flow" });

// 5. Create overview frame
const overview = await createOverviewFrame(page.id, analysis.flows[0]);

// 6. Create state frames
for (let i = 0; i < analysis.flows[0].states.length; i++) {
  const state = analysis.flows[0].states[i];
  const pos = calculateFramePosition(i + 1); // +1 to skip overview
  
  const frame = await figma.createFrame({
    name: `State ${i + 1}: ${state.label}`,
    parent_id: page.id,
    x: pos.x,
    y: pos.y,
    width: 1440,
    height: 900
  });
  
  // Build components
  for (const compName of state.components) {
    const mapping = componentMap.get(compName);
    if (mapping.primitive) {
      await createPrimitiveButton(frame.id, 100, 100, compName);
    } else {
      await figma.createInstance({
        component_id: mapping.figma_node_id,
        parent_id: frame.id
      });
    }
  }
  
  // Add annotations
  for (const interaction of state.interactions) {
    await figma.addAnnotation({
      node_id: frame.id,
      category: "Interaction",
      text: `${interaction.trigger} → ${interaction.action}`
    });
  }
  
  // Add flow arrow to next state
  if (i < analysis.flows[0].states.length - 1) {
    await figma.createConnector({
      start_node_id: frame.id,
      end_node_id: nextFrameId
    });
  }
}

// 7. Screenshot and present
const screenshot = await get_screenshot({ node_id: page.id });
return `✅ Prototype in Figma: ${file.url}`;
```

---

This skill is part of the **Design Skills** collection at [ara.so](https://ara.so). For issues or contributions, see the [GitHub repo](https://github.com/alima-max/prototype-to-figma-skill).
