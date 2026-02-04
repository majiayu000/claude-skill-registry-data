---
name: mindmap-skill
description: Maintain and evolve interactive mind maps generated from OPML outlines and XML palettes.
license: MIT
---

# ⚠️ CODE COPYING RULE ⚠️

**YOU MUST COPY THE EXACT CODE FROM `index.jsx` - DO NOT WRITE YOUR OWN CODE**

When creating inline previews:
1. Read `/mnt/skills/user/mindmap-skill/index.jsx`
2. Copy the ENTIRE component code exactly as written
3. Only modify: the embedded data objects (OPML structure and color palette)
4. Everything else stays identical - all logic, state management, event handlers, styling

If you write your own implementation of ANY feature, you have failed. The code in `index.jsx` is the only correct implementation.

# Overview

Use this skill when someone needs to review, adjust, or create an interactive mind map. The instructions apply to any subject matter. Ensure the content and layout reflect the topic the requester provides.

# Guardrails

**CRITICAL: NEVER REWRITE THE CODE**
- DO NOT rewrite, refactor, or modify ANY of the code logic from `index.jsx`
- DO NOT change function names, state management, event handlers, or component structure
- DO NOT add your own implementation of zoom, pan, drag, expand/collapse, or any other features
- ONLY action allowed: Copy the exact code from `index.jsx` and embed data into it
- The code in `index.jsx` is the ONLY correct implementation - use it verbatim
- If you find yourself writing code logic instead of copying it, STOP immediately

**What you ARE allowed to do:**
- Embed the mindmap data (OPML structure) as JavaScript objects
- Embed the color palette as JavaScript objects
- Change the content of the data (node labels, descriptions, children)
- Use Tailwind classes for styling in place of the CSS file

**What you are NOT allowed to do:**
- Rewrite any of the React component logic
- Create your own implementation of any feature
- Change how state is managed
- Modify event handlers or interaction logic
- Refactor the code structure

# When to Respond

- The requester wants to add, edit, or remove nodes in the mind map outline.
- A new mind map topic must be set up.
- The preview fails to render correctly and needs debugging.
- The requester explicitly asks to modify colors, typography, or spacing.

# Preview Modes

**Inline Preview (default)**: Create a single `.jsx` React artifact that embeds all mindmap data inline for immediate preview in the chat interface. Parse the OPML structure and color palette into JavaScript objects within the component. This mode is ideal for quick iteration and sharing.

**Multi-file Setup**: When the user specifically requests downloadable files, mentions "local server", or asks for files they can host, create the traditional multi-file structure with separate `mindmap.opml`, `palette.xml`, `index.html`, `index.jsx`, and `styles.css` files.

# Standard Workflow

1. **Determine preview mode**
   - Default to inline preview (React artifact) unless the user requests downloadable files
   - For inline preview, create a single `.jsx` artifact with embedded data
   - For multi-file, follow the traditional multi-file workflow

2. **Clarify the intent**
   - Confirm the mind map topic and the exact hierarchy or copy edits
   - Gather the precise text for new or updated nodes, including detailed notes
   - Only ask about visual preferences if the user explicitly mentions wanting to change colors or styling

3. **Update data structure**
   - Use `mindmap.opml` as the source of truth; translate its hierarchy directly unless the requester provides new or updated nodes
   - Create the hierarchical structure with roughly 5-8 main branches and 3-6 children each
   - Keep node labels short (1-3 words) and use detailed notes for extended descriptions
   - Maintain balanced depth across branches

4. **Apply color palette**
   - Use the existing color palette from `palette.xml` unless the user explicitly requests color changes
   - Colors are already optimized for technical content and should not be modified without explicit user request
   - If color changes are requested, ensure hex values remain unique and visually distinct

5. **Create preview**
   - For inline preview: Generate a complete React component with all data embedded
   - For multi-file: Create separate OPML, palette, HTML, and CSS files

6. **Report back**
   - Summarize the structure created and any assumptions made
   - Provide preview instructions if using multi-file mode

# Inline Preview Implementation

When creating inline previews:

- Read `mindmap.opml` and `palette.xml` from the repository first. Parse both files and embed their contents as JavaScript data so the preview matches the source of truth.
- Convert OPML hierarchy into nested JavaScript objects with structure:
  ```javascript
  {
    text: "Node Label",
    note: "Detailed description for this node",
    children: [/* nested nodes */]
  }
  ```

- Embed color palette as an array:
  ```javascript
  const colors = [
    { name: 'Color-1', rgb: 'RRGGBB', r: R, g: G, b: B },
    // ... more colors
  ]
  ```

- Include all React logic, styling, and data in a single `.jsx` file
- Mirror the component structure and state handling from `index.jsx` so that interactions remain identical.
- Use Tailwind utility classes for styling
- Ensure the component has no required props and uses a default export
- Create radial layout with main topic at center and branches radiating outward
- **DO NOT include any title or description text overlays** - the mindmap should be clean with only nodes visible

## Default Node State

IMPORTANT: All child nodes should be COLLAPSED by default when the mindmap first loads.
- Only the center node and main branches (level 1) are visible initially
- Child nodes (level 2+) are hidden until user clicks the + button
- This creates a clean, uncluttered initial view
- Prevents overwhelming viewers with too much information at once
- Users progressively reveal details as they explore

Set initial state: `const [expandedNodes, setExpandedNodes] = useState({});` (empty object = all collapsed)

**CRITICAL: Initialize hiddenNodes after building the node tree:**
```javascript
// After setNodes(newNodes) and setConnections(newConnections):
const initialHidden = {};
Object.values(newNodes).forEach(node => {
  if (node.level >= 2) {
    initialHidden[node.id] = true;
  }
});
setHiddenNodes(initialHidden);
```

## Required Interactive Features

CRITICAL: All inline previews MUST include these features. Do not omit any:

1. **Zoom Controls**
   - Mouse wheel scroll to zoom in/out
   - Maintain zoom state with useState
   - Apply zoom via CSS transform on the canvas
   - Typical range: 0.5x to 2x

2. **Pan/Drag Canvas**
   - Click and drag background to pan the entire view
   - Track pan offset with useState
   - Change cursor to 'grab' when hovering, 'grabbing' when dragging
   - Apply pan via CSS transform: `translate(${pan.x}px, ${pan.y}px)`

3. **Node Expansion/Collapse**
   - Display +/- button on hover for nodes with children
   - Clicking + expands to show child nodes
   - Clicking - collapses to hide child nodes
   - Track expanded state with useState object keyed by node ID
   - Button should appear styled with node's color

4. **Reset Hidden Children**
   - Display reset button (↻) for expanded nodes that have hidden children
   - Clicking reset unhides all collapsed child nodes
   - Only show when node is expanded AND has hidden children

5. **Node Dragging**
   - Click and drag individual nodes to reposition them
   - Drag should move node and all its descendants together
   - Update node positions in state
   - Prevent click event from firing if user dragged (hasDragged flag)

6. **Detail Popovers**
   - Click node to show detailed popover with description
   - Display node label, description, and list of children
   - Position popover intelligently based on node position (avoid edges)
   - Click same node again to close popover
   - Style popover border with node's color

7. **Visual Feedback**
   - Hover effects: scale node slightly (1.05-1.1x)
   - Selected node: larger scale (1.15x) with colored glow
   - Smooth transitions on all interactions
   - Connection lines from center to branch nodes

8. **State Management**
   - selectedNode: currently clicked node ID
   - hoveredNode: currently hovered node ID
   - zoom: current zoom level
   - pan: { x, y } for canvas position
   - expandedNodes: object mapping node IDs to boolean
   - hiddenNodes: object tracking collapsed children
   - draggingNode: ID of node being dragged
   - dragOffset: { x, y } offset during drag

Reference the original `index.jsx` file for implementation details if needed.

## Typography

**For inline React artifacts:**
- Use system font stack: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif`
- Inline artifacts cannot load custom fonts, so rely on clean system fonts

**For multi-file setups:**
- Always load Hubot Sans via Google Fonts in `index.html` (mirror the link/preconnect tags in the repository). System fonts serve only as safety fallbacks.
- Font stack: `'Hubot Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`

**Font sizing:**
- Center node: 1.25rem, weight 700
- Branch nodes: 0.95rem, weight 600
- Popover title: 1.125rem, weight 700
- Popover description: 0.95rem
- Child labels: 0.9rem, weight 600
- Child details: 0.75rem

# Multi-file Structure

When users request downloadable files:

- `mindmap.opml` — Hierarchical outline; each `<outline>` element becomes a node. `text` holds the label, `_note` holds extended details
- `palette.xml` — Defines branch colors. Each `<color>` entry needs a unique `name`, six-character `rgb` value (without `#`), and matching `r`, `g`, `b` integers
- `index.html` — Minimal loader that pulls in React/Babel and mounts the mind map
- `index.jsx` — React-based viewer that fetches the OPML and palette, lays out the mind map, and wires up interactions
- `styles.css` — Visual design for nodes, popovers, background, typography

Package all files into a ZIP archive and provide server instructions:
1. Extract the ZIP file
2. Open terminal in the extracted folder
3. Run: `python3 -m http.server 3000`
4. Open browser to `http://localhost:3000/index.html`

# Quality Checklist

- **All child nodes collapsed by default** - only center + main branches visible on load
- Node labels stay short (1-3 words); detailed notes capture descriptive text
- Hierarchical structure is balanced and logical
- Colors are not modified unless explicitly requested by the user
- Layout keeps the map readable with proper spacing
- All content is accurate and relevant to the requested topic
- **ALL interactive features are implemented:**
  - ✓ Scroll to zoom (wheel events)
  - ✓ Click and drag to pan canvas
  - ✓ Click and drag individual nodes
  - ✓ Hover to show +/- buttons (for nodes with children)
  - ✓ Click +/- to expand/collapse children
  - ✓ Reset button (↻) to unhide children
  - ✓ Click nodes to show/hide detail popovers
  - ✓ Hover effects with smooth transitions
  - ✓ Visual feedback (scale, glow, cursor changes)

# Color Palette Protection

The color palette in `palette.xml` is optimized and should not be changed unless the user explicitly requests it. Do not offer to change colors, do not ask about color preferences, and do not modify the palette as part of normal workflow. Only change colors when the user specifically says they want different colors.

# Troubleshooting Tips

- **Blank Preview** — Check that data structure is valid JavaScript/XML
- **Overlapping Nodes** — Reduce node counts per branch or adjust spacing
- **Missing Interactions** — Verify event handlers are properly bound
- **Layout Issues** — Ensure container dimensions and SVG viewBox are correctly set
- **Missing Features** — If zoom, pan, drag, or expand/collapse don't work, refer to the Required Interactive Features section and cross-check with the original `index.jsx` implementation. Every feature must be included.
