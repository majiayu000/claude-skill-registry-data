---
name: interactive-system-docs
description: >-
  Build a self-contained interactive HTML visualization that explains how a
  complex system works — architecture, data flows, state machines, processing
  pipelines, and search patterns — with D3.js graphs where every node is
  clickable, all rendered from a single file with no build step. Use when the
  user wants a "how it works" page, an architecture explainer, an interactive
  spec, or a visual reference doc for a technical system. Based on the memtree
  how-it-works.html approach.
metadata:
  last_updated: "2026-05-26"
---

# Interactive System Docs

Build one self-contained `docs/how-it-works.html` (or similar) that makes a complex system immediately legible to anyone — developer, operator, or curious outsider. No build step, no framework, no server. Open the file in a browser and everything works.

## Workflow

### Phase 1 — Deep system understanding first

Do not start writing HTML until you fully understand the system. Read source before docs.

**Read in this order:**
1. Hook files, middleware, interceptors — anything that fires automatically
2. Core source files for each major tool or subsystem
3. Config files and schemas
4. Specs and design docs last (they describe intent; source describes reality)

**Build a mental map of:**
- All entity types (nodes in your graph): What are the "things" in this system?
- All relationship types (edges): How do entities connect, derive from, trigger, contain each other?
- All flows: What sequences happen for each major operation?
- All states: What lifecycle do entities go through?

Don't guess. If you're unsure what a hook does, read it. If you're unsure what a field means, trace it to where it's written.

### Phase 2 — Narrative structure before visuals

Plan sections top to bottom. Each section = one concept. Order: why → what → how → reference → install.

**Standard section sequence for a tool/system:**
1. **Hero** — Problem / Solution / Payoff (3 cards) + spec link
2. **Architecture** — The property graph / data model with full node+edge legend
3. **Per-operation sections** — One per major tool or flow (Read, Grep, WebFetch…)
4. **Cross-cutting concerns** — Prompts, conversation tree, agent subgraphs
5. **Infrastructure sections** — Hooks pipeline, processing pipeline
6. **Reference sections** — Hook reference table, search visualizations, state machine
7. **Install** — Practical setup with exact commands

For each operation section, show a specific non-trivial example — not a toy. Real URIs, real properties, real edge types.

### Phase 3 — Build the HTML

Single file. Inline all CSS and JS. Use D3.js v7 from CDN.

```html
<script src="https://d3js.org/d3.v7.min.js"></script>
```

#### CSS architecture

Use CSS custom properties for the dark theme. Define all colors at `:root`:

```css
:root {
  --bg:#080e1a; --bg1:#0f1a2e; --bg2:#162032; --bg3:#1c2940;
  --border:#1e3452; --borderhi:#2d4d7a;
  --text:#dde6f0; --muted:#7a9ab8; --dim:#3d5a78;
  --sky:#38bdf8; --green:#4ade80; --orange:#fb923c;
  --purple:#c084fc; --pink:#f472b6; --red:#f87171; --indigo:#818cf8;
  --mono:'SF Mono','JetBrains Mono','Fira Code',Consolas,monospace;
}
```

Organize CSS by component — nav, hero, sections, graphs, property panel, tabs, etc. Never inline colors; always reference variables.

#### Type system — define this first, everything else uses it

```js
const NK = { /* node kind → hex color */
  session:'#334155', turn:'#6d28d9', tool_call:'#c2410c',
  file:'#0369a1', file_chunk:'#0ea5e9', web_content:'#16a34a',
  // ... one entry per node type
};
const NI = { /* node kind → icon character (monospace, 1 char) */
  session:'⬡', turn:'◎', tool_call:'⚡', file:'▤', file_chunk:'{}',
  // ...
};
const EK = { /* edge kind → { color, dash } */
  contains:   { color:'#475569', dash:'' },
  references: { color:'#0ea5e9', dash:'' },
  triggers:   { color:'#f472b6', dash:'5,3' },
  // ...
};
```

Every node type gets a **different color AND a different icon**. No two types share either. Icons must be readable at 9–12px in a monospace font.

#### Property panel — always present, always on the right

Fixed panel, slides in from the right on any node click. Shows: kind badge with color, URI, all properties as a key/value table. Special renderers for structured values (a11y trees, chunk lists).

```js
function openPropPanel(datum) {
  // set kind badge color from NK[datum.kind]
  // render all datum props as rows
  // special-case: a11y_tree array → render as indented accessibility tree
  // special-case: chunks array → render as scrollable chunk list
  document.getElementById('prop-panel').classList.add('open');
  document.getElementById('prop-overlay').classList.add('open');
}
```

The overlay click closes the panel. Escape key closes it too.

#### Node rendering pattern

Every node = two circles (glow effect) + icon text + label below:

```js
function drawNode(g, id, node, opts={}) {
  const color = NK[node.kind] ?? '#475569';
  const icon  = NI[node.kind] ?? '◉';
  const ng = g.append('g').attr('transform', `translate(${node.x},${node.y})`);
  // glow: larger, same color, 0.18 opacity
  ng.append('circle').attr('r', node.r + 7).attr('fill', color).attr('opacity', 0.18);
  // main circle
  ng.append('circle').attr('r', node.r).attr('fill', color);
  // icon
  ng.append('text').attr('text-anchor','middle').attr('dy','0.35em')
    .attr('fill','#fff').attr('font-size', Math.max(9, node.r * 0.7))
    .attr('font-family','monospace').text(icon);
  // label
  ng.append('text').attr('y', node.r + 13).attr('text-anchor','middle')
    .attr('fill','#7a9ab8').attr('font-size',9).text(node.label);
  // hover: expand radius
  ng.on('mouseover', () => ng.select('circle:nth-child(2)').attr('r', node.r + 4));
  ng.on('mouseout',  () => ng.select('circle:nth-child(2)').attr('r', node.r));
  // click: property panel
  ng.on('click', () => openPropPanel(node));
}
```

#### Edge rendering pattern

Curved bezier paths with optional dash animation and hover tooltip:

```js
function drawEdge(g, id, link, nodeMap, opts={}) {
  const ek = EK[link.kind] ?? { color:'#475569', dash:'' };
  const src = nodeMap[link.source], tgt = nodeMap[link.target];
  const mx = (src.x + tgt.x) / 2, my = (src.y + tgt.y) / 2 - 30; // curve up
  const path = `M${src.x},${src.y} Q${mx},${my} ${tgt.x},${tgt.y}`;
  g.append('path').attr('d', path)
    .attr('fill','none').attr('stroke', ek.color).attr('stroke-width', 1.5)
    .attr('stroke-dasharray', ek.dash || null)
    .attr('marker-end', 'url(#arrow)');
  // label on midpoint, hover tooltip
}
```

Add arrow marker defs once per SVG:

```js
svg.append('defs').append('marker')
  .attr('id','arrow').attr('markerWidth',8).attr('markerHeight',8)
  .attr('refX',6).attr('refY',3).attr('orient','auto')
  .append('path').attr('d','M0,0 L0,6 L8,3 Z').attr('fill','#475569');
```

### Phase 4 — Choose visualization type per section

| What you're showing | Use |
|---------------------|-----|
| A specific operation flow (Read, Grep, etc.) | **Fixed-position scenario graph** — lay nodes out by hand, no simulation |
| The full conversation / session tree | **D3 force-directed** — nodes push apart, links pull together, drag+zoom |
| A time-ordered process (hooks firing) | **Swimlane diagram** — horizontal lanes, sequential animation |
| A pipeline (walker → chunker → embedder) | **Horizontal pipeline** — boxes with arrows, staggered CSS animation |
| A state machine | **Fixed state graph** — states as rounded rects, transitions as labeled arcs |
| Multiple query types | **Tabbed pane** — one tab per query type, result rows with score badges |
| Hook/API reference | **Card list** — one card per hook, header = event+file+trigger, body = what/result |
| Install steps | **Numbered steps** — step-num circle + title + description + code block |

### Phase 5 — Specific section patterns

#### Hero section

```html
<div class="hero-badge">🌳 tagline · tagline · tagline</div>
<h1>One punchy line.<br>Second line with the core claim.</h1>
<p class="hero-sub">One paragraph. What it intercepts, what it produces, the key number.</p>
<div class="why-grid">
  <!-- 3 cards: The Problem · The Solution · The Payoff -->
</div>
<a href="spec-url" class="spec-link" target="_blank">📄 Read the spec →</a>
```

The 3 cards follow this formula exactly:
- **Problem card**: Name a specific failure mode. Quantify it (tokens, time, sessions).
- **Solution card**: Name the mechanism. One sentence on what it does to each operation.
- **Payoff card**: Name the outcome. End with the aspiration ("Context rot disappears.").

#### Scenario graph (per-tool section)

Each tool section gets:
- A before/after comparison (raw output vs. memtree reference)
- A graph showing: session → turn → tool_call → result nodes → child nodes
- Play button triggers an edge-by-edge reveal animation
- All nodes clickable with realistic property data

Node data structure for scenarios:

```js
const nodes = [
  { id:'sess', kind:'session', label:'session://abc', x:80,  y:180,  r:18,
    props:{ session_id:'abc123', started_at:'2026-05-26T10:00Z', project:'/myproject' }},
  { id:'tc',   kind:'tool_call', label:'memtree_read', x:260, y:180, r:14,
    props:{ tool:'memtree_read', file_path:'src/server.ts', status:'ok', tokens_saved:4140 }},
  // ...
];
```

Always include realistic-looking values in `props`. These are what the property panel shows.

#### Force-directed conversation tree

For the "full conversation" section — use D3 force simulation:

```js
const simulation = d3.forceSimulation(nodes)
  .force('link', d3.forceLink(edges).id(d=>d.id).distance(80))
  .force('charge', d3.forceManyBody().strength(-300))
  .force('center', d3.forceCenter(W/2, H/2));
```

Add drag behavior and zoom. Store the simulation globally so a "Fit" button can restart it.

#### Swimlane (hooks pipeline)

```
Lanes: [Claude] [Hook System] [memtree] [Native Tool]
Each lane = a vertical strip, nodes placed in lane by actor.
Animation: edges appear one by one with 600ms delay.
```

#### State machine

Fixed-position state nodes as rounded rects (`rx:8`). Transition arrows are bezier paths with `marker-end`. Include a running animation that cycles through the lifecycle on an interval, highlighting the active state.

#### Hook reference card list

One card per hook. Header row: event badge + filename + tool tag. Body: two columns — "When it fires" (trigger conditions) + "What it does" (exact behavior + result badge).

Result badges: `✕ deny`, `✦ inject`, `◉ silent`, `→ passthrough`.

### Phase 6 — Mini version + README

After the full document:
1. Create `docs/mini.html` — same dark theme, no D3, pure CSS — token comparison bars, hook flow, tool grid, install steps. One prominent "Full visualization →" button.
2. Rewrite README.md with: problem/solution narrative, token savings table, install commands, tool table, hook table, built-on attribution, coming-soon section. Run `bunx markdownlint-cli2 --fix README.md` after writing.

## Reference implementation — memtree how-it-works.html

The canonical example of this skill in action is:

**File:** `/Users/joe/github/joeblackwaslike/memtree/docs/how-it-works.html`
**GitHub:** `https://github.com/joeblackwaslike/memtree/blob/main/docs/how-it-works.html`
**Mini version:** `/Users/joe/github/joeblackwaslike/memtree/docs/mini.html`

### What it covers

The memtree doc is ~2600 lines of self-contained HTML. It visualizes a Claude Code plugin that intercepts tool calls and routes them through a SQLite property graph. Sections and what each one demonstrates:

| Section | ID | Demonstrates |
|---------|-----|-------------|
| Hero | `#top` | why-grid (problem/solution/payoff), spec link button, token comparison bars |
| Property Graph | `#arch` | Flow diagram, full node-type legend (20+ types), edge-type legend — the type system at a glance |
| Read | `#read` | session→turn→tool_call→file→[chunk stream] with `next` edges; chunk nodes have source_uri, content, size, lang |
| Grep | `#grep` | File nodes that **expand inline** when clicked to reveal their semantic chunk stream — dynamic SVG injection |
| WebFetch | `#webfetch` | `web_content` node with accessibility tree rendered in the property panel (`a11y_tree` array) |
| Monitor | `#monitor` | Read-only (output_chunk stream) and read-write (bidirectional with input_chunk + `sends` edges) |
| WebSearch | `#websearch` | `web_result` nodes with status/etag/title; failed fetches rendered red (`web_result_err` kind) |
| Agent | `#agent` | Subgraph box (dashed rect) containing its own session/turns/tool_calls; collapses to summary node |
| Skill | `#skill` | Skill node as its own graph: SKILL.md + step chunks + mermaid diagram nodes + plugin edge |
| MCP | `#mcp` | MCP server → MCP tool → result; shows that ALL MCP calls are intercepted, not just native tools |
| Prompt | `#prompt` | Observation → thinking → response → tool_call → question → choice nodes; selected choice in green |
| Conversation | `#convo` | D3 force-directed tree of a full non-trivial conversation, 25+ nodes, drag+zoom+fit |
| Hooks | `#hooks` | Swimlane animation: Claude → Hook System → memtree → Native Tool, sequential edge reveal |
| Hook Ref | `#hookref` | Card-per-hook reference: event badge, filename, trigger conditions, what it does, result badge |
| Pipeline | `#pipeline` | Walker → Chunker → Embedder → Indexer → Summarizer → Dedupe → Indexed, animated |
| Search | `#search` | 8 tabbed search types: semantic, hybrid, compose, JSONPath, metadata, neighbors, path-to-root, recent |
| States | `#states` | State machine: raw→processing→indexed→stale→superseded/redacted→pruned, animated lifecycle |
| Install | `#install` | 4-step install guide, requirements, links to GitHub and marketplace |

### Key implementation details from this example

**Inline chunk expansion (Grep section):** File nodes override the default click handler. Clicking toggles `expandedState[node.id]`. On expand: dynamically appends chunk nodes and `next` edges directly to the SVG, with a `contains` edge from the file. On collapse: removes all `.expand-{nodeId}` elements. No re-render.

**Subgraph box (Agent section):** Drawn as a `rect` with `stroke-dasharray:'6,3'` and red stroke before any nodes. Nodes that belong to the subgraph are positioned inside its bounds. The box label is a `text` element above the rect.

**Accessibility tree in property panel (WebFetch):** When `node.a11y_tree` is an array, the property panel renders each entry as a `.a11y-item` with role badge, name, `[ref=eN]` indicator, and optional meta (level, type). Each item is clickable for future interaction.

**State machine animation:** `setInterval` cycles through `['raw','processing','indexed','stale','pruned']` every 1.2s. Each step highlights the active state card with a CSS class and draws the active transition arrow in a bright color. Play/Reset buttons control the interval.

**Force-directed conversation graph:** The simulation is stored in a module-level variable so the "Fit" button can call `simulation.alpha(0.3).restart()`. Drag behavior is wired via `d3.drag()` on each node group. Zoom is a `d3.zoom()` transform on the outer SVG `<g>`.

**Global type system:** `NK`, `NI`, and `EK` are defined at module scope before any rendering functions. Every `drawNode` and `drawEdge` call references them. Adding a new node type = one line in each object.

## Design rules

- **One file**. Inline all CSS and JS. No imports, no build, no CDN except D3.
- **Every node type = unique color + unique icon**. No exceptions.
- **Every node is clickable**. The property panel must show all meaningful properties.
- **Non-trivial examples**. Real URIs, real filenames, realistic token counts, realistic timestamps.
- **Play/Reset on every animation**. Never auto-play. Let the user control pacing.
- **Dark theme only**. Use the CSS variable palette above verbatim.
- **Sticky nav** with section anchors. Every section has a nav link.
- **Write the file in one pass** when possible. Consistency across 5000 lines is hard to retrofit.

## Red flags — stop and re-read the source

- You're guessing what a hook does → read the hook file
- You're inventing node properties → read the schema or source
- A section feels thin → add a before/after comparison
- A graph has fewer than 4 node types → you're not showing enough of the system
- The property panel would show nothing interesting → add richer props to the node data

## Rationalization table

| Thought | Reality |
|---------|---------|
| "I'll use a diagram tool instead." | No interactivity, no property panel, can't show all types. Single HTML wins. |
| "D3 is overkill for this." | Fixed-position graphs need no simulation. D3 is just SVG helpers. |
| "I'll add the property panel later." | Write it first. Every node needs click behavior from the start. |
| "This section can be a bullet list." | If there are relationships, draw them. Lists hide structure. |
| "The example can be simple." | Simple examples teach nothing. Use real-looking data. |
