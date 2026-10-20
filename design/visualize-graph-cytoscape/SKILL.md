---
name: visualize-graph-cytoscape
description: >-
  Load this skill when building an interactive node-and-edge graph UI with Cytoscape.js: a network,
  dependency map, knowledge graph, or org chart. Trigger on "visualize this graph", "draw a
  network", or any mention of cytoscape. Not for a fixed diagram (use Mermaid).
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires the `cytoscape` package installed from npm (via `bun add`, npm, or a CDN script tag)
  and a browser to render the graph. The bundled `scripts/to-elements.js` is dependency-free but
  needs Node.js 18+ when required server-side; loaded via a script tag it needs only the browser.
  Layout extensions (`cytoscape-dagre`, `-fcose`) are separate npm packages.
license: Apache-2.0
---

# Visualize a Graph with Cytoscape.js

Cytoscape.js is a canvas-rendering graph theory library. It is a building block, not an
app: it gives you a graph model, a stylesheet, layouts, algorithms, and an event system.
Everything else — panels, search boxes, legends, detail views — is your own code.

The examples pin Cytoscape.js 3.34.2.

Done when the graph renders with readable labels and passes `references/checklist.md`.

## Procedure

Follow these steps in order. Do not skip step 1: picking the wrong layout is the difference between
a legible diagram and a hairball.

### 0. Rule zero: the ten failures that break most builds

Most broken Cytoscape.js builds fail for one of ten reasons. Check every one of these
before you consider a visualizer finished. They are listed in the order they usually bite.

1. **The container must have a non-zero height before `cytoscape()` is called.**
   A bare `<div id="cy">` is 0px tall and the graph renders invisibly, or every node
   stacks at one point. Set an explicit `height` (px, vh, or a flexed parent with a
   definite size) in CSS that is parsed _before_ init. The official docs are explicit:
   put stylesheets in `<head>` before any Cytoscape-related code, or dimensions get
   reported incorrectly.

2. **Arrows do not render on the default edge style.** `curve-style` defaults to
   `haystack`, and haystack edges do not support endpoint arrows, loops, or compound
   nodes. If your graph is directed, you must set `'curve-style': 'bezier'` (or
   `straight`, `taxi`, `segments`) in the edge selector. This is the single most common
   "why are my arrows missing" bug.

3. **The stylesheet is not CSS.** It is a JSON array of `{ selector, style }` blocks
   using Cytoscape's own property names (`background-color`, `line-color`, `label`).
   CSS variables, `rgb(var(--x))`, `class` attributes from your HTML, Tailwind classes,
   and `!important` do nothing. Resolve theme colors to concrete strings in JS before
   passing them in. See `references/theming.md`.

4. **Every element needs a unique string `id`, and every edge's `source`/`target` must
   name a node that exists.** A dangling edge throws on init. Validate the data first —
   there is a ready-made guard in `references/integration.md`.

5. **`cy` is an imperative instance, never React state.** Hold it in a ref, create it
   once, and call `cy.destroy()` in cleanup. Putting it in `useState` causes infinite
   re-render loops and leaked canvases.

6. **Call `cy.resize()` when the container changes size for any reason other than a
   window resize.** Cytoscape hooks `window.resize` only; it cannot observe arbitrary
   DOM elements. A sidebar opening, a tab switching, or a flex reflow will leave the
   canvas mis-sized and taps offset from where you clicked. Use a `ResizeObserver`.

7. **Layout is asynchronous for force-directed algorithms.** `cy.layout(...).run()`
   returns immediately. If you need to act on final positions (fit, screenshot, measure),
   listen for `layoutstop` or await `layout.promiseOn('layoutstop')`.
   **A layout passed as the `layout:` constructor option cannot be listened to this way.**
   It runs during `cytoscape()`, before your code has an instance to bind a handler to, so
   a `cy.on('layoutstop')` or `cy.one('layoutstop')` registered on the next line never
   fires and every check you hung off it silently does not run. Two ways out, and you must
   pick one deliberately: keep `layout:` in the constructor and use `cy.ready(fn)`, which
   fires after that initial layout; or omit `layout:`, then `const l = cy.layout(opts);
l.one('layoutstop', fn); l.run();`. Use the second whenever the handler must also run on
   later re-layouts. `layoutstop` also lands well after `animationDuration` on an animated
   layout — a 300ms animation on 150 nodes took over 1.6s — so never verify it with a short
   fixed sleep and conclude it never fires.

8. **The container div must be empty and owned by Cytoscape.** Do not render your own
   children into it. If taps land at the wrong offset, this or a missing `cy.resize()`
   is why.

9. **`cy.fit()` on a large graph can leave every label unreadable.** When `zoom × font-size`
   falls under `min-zoomed-font-size`, Cytoscape draws no labels at all. Gate on that pixel
   size, never a zoom constant. See "Sizing and readable defaults" below.

10. **On live or polling data, never `remove()` then `add()`.** It silently resets the
    user's zoom, pan, and selection on every refresh. Diff into the existing instance
    with `syncGraph` (`references/integration.md`) and re-run the layout only when the
    topology actually changed.

### 1. Classify the graph, then pick the layout

| Graph shape                         | Layout                                 | Notes                                                 |
| ----------------------------------- | -------------------------------------- | ----------------------------------------------------- |
| Tree / forest / clear roots         | `breadthfirst`                         | Built in. Set `roots` and `direction`.                |
| DAG, pipeline, flowchart            | `dagre` (extension)                    | Proper layered ranking. Best for left→right flows.    |
| DAG needing orthogonal routing      | `elk` (extension), `layered` algorithm | Heavier, best-in-class edge routing.                  |
| General network, no hierarchy       | `fcose` (extension)                    | Use this, not `cose`. Faster and much better quality. |
| Network with compound/grouped nodes | `fcose` or `cola`                      | Both handle compound parents well.                    |
| Clustered / community structure     | `cise` (extension)                     | Places clusters in circles.                           |
| Small graph, categorical ordering   | `circle`, `concentric`, `grid`         | Deterministic, instant, no jitter.                    |
| Positions supplied by your data     | `preset`                               | Reads `position: {x, y}` from each node.              |

Built-in layouts only: `null`, `random`, `preset`, `grid`, `circle`, `concentric`,
`breadthfirst`, `cose`. Everything else is an extension you must load and register.
Lifecycle, re-running, and the extension layouts are in `references/layouts.md`. Full option
lists are in the Cytoscape.js docs.

Rule of thumb: if the user's graph is hierarchical, do not use a force layout. Force
layouts on trees look like accidents.

### 2. Shape the data

Real inputs are almost never already in elements JSON. They arrive in one of four shapes,
and converting them is where dangling edges and duplicate ids get introduced. Use the
bundled helper rather than writing the conversion by hand each time:

```js
// scripts/to-elements.js — works in Node and the browser
const {
  fromParentPointer,
  fromDependsOn,
  fromEdgeList,
  fromAdjacency,
  sanitize,
} = require("./scripts/to-elements.js");
```

| Input shape                                               | Example                     | Use                                                                           |
| --------------------------------------------------------- | --------------------------- | ----------------------------------------------------------------------------- |
| Parent pointer (org charts, file trees, category trees)   | `{id, name, manager_email}` | `fromParentPointer(rows, {id:'email', parent:'manager_email', label:'name'})` |
| Dependency arrays (Terraform, package manifests, imports) | `{id, depends_on:[...]}`    | `fromDependsOn(rows, {id:'id', deps:'depends_on'})`                           |
| Edge list plus optional node list                         | `[{from, to, weight}]`      | `fromEdgeList(edges, nodes, {source:'from', target:'to'})`                    |
| Adjacency matrix                                          | `[[0,1],[1,0]]` + labels    | `fromAdjacency(matrix, labels)`                                               |

Every one of these routes through `sanitize()`, which drops duplicate ids and edges
pointing at nodes that do not exist, and returns the dropped ones as `warnings`.
**Surface those warnings in the UI.** In real exports, edges pointing outside the dataset
are common — a `manager_email` for someone who left, a `depends_on` on a module in
another state file. Silently dropping them makes the graph quietly wrong; showing "3
relationships referenced records not in this file" makes it honest.

The resulting shape:

```js
const elements = [
  { data: { id: "a", label: "Auth service", type: "service" } },
  { data: { id: "b", label: "Postgres", type: "datastore" } },
  { data: { id: "a->b", source: "a", target: "b", kind: "reads" } },
];
```

Put everything you will style or query into `data`. Style with `data(...)` and
`mapData(...)` mappers or with selectors on data fields — not with per-element `style`
overrides, which bypass the stylesheet and are hard to undo.

Use `classes` for _state_ that changes at runtime (`highlighted`, `dimmed`, `faded`) and
`data` for _facts_ about the entity. This split keeps interaction code to
`addClass` / `removeClass`.

Ids from real data often contain characters the `#id` selector grammar cannot carry:
`@`, `$`, `/`, `:` and spaces all fail, and they fail **silently** — `cy.$('#ceo@corp.com')`
returns an empty collection rather than throwing, so the bug surfaces as a button that
does nothing. (`.` and `-` do parse: `cy.$('#aws_vpc.main')` matches by id even when a
class named `main` exists. Do not rely on it — the next id in the same dataset will have
an `@` in it.) Use `cy.$id('aws_vpc.main')`, which takes the id as a plain string with no
parsing and no escaping, or pass collections directly to options like `roots` — never
hand-escape into a selector string.

### 3. Write the stylesheet

Start from the base stylesheet in `assets/template.html`, then adjust. Every visualizer
needs at minimum: node body, node label, edge line, edge arrow, selected state, and the
dim/highlight pair used by interactions. Look up any other property in the Cytoscape.js style
docs.

### 4. Wire the interactions

Tap-to-highlight-neighborhood is the baseline expectation for any explorer. Search,
filter, expand/collapse, and detail panels build on the same collection primitives.
Copy-paste-ready implementations are in `references/recipes.md`.

### 5. Verify

Run through `references/checklist.md` before declaring done. It is short and catches the
failures that only appear at runtime.

### Minimal working skeleton

This runs as-is. Use it as the starting point rather than writing init from memory.

```html
<style>
  #cy {
    width: 100%;
    height: 600px;
    display: block;
  }
</style>
<div id="cy"></div>
<script src="https://cdn.jsdelivr.net/npm/cytoscape@3.34.2/dist/cytoscape.min.js"></script>
<script>
  const cy = cytoscape({
    container: document.getElementById("cy"),
    elements: [
      { data: { id: "a", label: "A" } },
      { data: { id: "b", label: "B" } },
      { data: { id: "ab", source: "a", target: "b" } },
    ],
    style: [
      {
        selector: "node",
        style: {
          "background-color": "#7F77DD",
          label: "data(label)",
          "font-size": 11,
          color: "#26215C",
          "text-valign": "bottom",
          "text-margin-y": 4,
          width: 32,
          height: 32,
        },
      },
      {
        selector: "edge",
        style: {
          "curve-style": "bezier",
          width: 1.5,
          "line-color": "#B4B2A9",
          "target-arrow-shape": "triangle",
          "target-arrow-color": "#B4B2A9",
          "arrow-scale": 0.9,
        },
      },
      { selector: ".dimmed", style: { opacity: 0.15 } },
      {
        selector: ".highlighted",
        style: { "border-width": 3, "border-color": "#D85A30" },
      },
    ],
    layout: {
      name: "breadthfirst",
      directed: true,
      padding: 30,
      spacingFactor: 1.2,
    },
    minZoom: 7 / 11, // min-zoomed-font-size / font-size — below this, no labels
    maxZoom: 3,
    wheelSensitivity: 0.3,
  });

  cy.on("tap", "node", (evt) => {
    const hood = evt.target.closedNeighborhood();
    cy.elements().addClass("dimmed").removeClass("highlighted");
    hood.removeClass("dimmed").addClass("highlighted");
  });

  cy.on("tap", (evt) => {
    if (evt.target === cy) cy.elements().removeClass("dimmed highlighted");
  });
</script>
```

### Loading the library

- **npm**: `npm install cytoscape`, then `import cytoscape from 'cytoscape'`.
  `import * as cytoscape from 'cytoscape'` does **not** work — the default export is
  required.
- **CDN**: cdnjs, jsDelivr, or unpkg. Pin the version. `dist/cytoscape.min.js` is UMD
  and exposes a `cytoscape` global; `dist/cytoscape.esm.min.mjs` is the ES module build.
- **Extensions**: register once, before creating any instance:
  ```js
  import cytoscape from "cytoscape";
  import fcose from "cytoscape-fcose";
  cytoscape.use(fcose);
  ```

#### Extensions from a CDN

Guessing the UMD global name is the usual failure here, and a wrong guess fails silently
until layout time. You do not have to guess: **the global is the package name in
camelCase** — `cytoscape-fcose` exposes `cytoscapeFcose`, `cytoscape-cose-bilkent`
exposes `cytoscapeCoseBilkent`. That rule covers every extension, including ones not
listed below. What you cannot derive is the load order, which is what the table carries.

Pin the core exactly. Pin extensions to a
major range: their patch releases are not tracked here, and a stale exact pin is worse
than a range.

```html
<script src="https://cdn.jsdelivr.net/npm/cytoscape@3.34.2/dist/cytoscape.min.js"></script>

<!-- fcose: needs layout-base then cose-base first -->
<script src="https://cdn.jsdelivr.net/npm/layout-base@2/layout-base.js"></script>
<script src="https://cdn.jsdelivr.net/npm/cose-base@2/cose-base.js"></script>
<script src="https://cdn.jsdelivr.net/npm/cytoscape-fcose@2/cytoscape-fcose.js"></script>

<!-- dagre: needs dagre first -->
<script src="https://cdn.jsdelivr.net/npm/dagre@0.8/dist/dagre.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/cytoscape-dagre@2/cytoscape-dagre.js"></script>

<script>
  // Never call cytoscape.use(window.X) unguarded: if the script tag failed, X is
  // undefined and the page dies at layout time with nothing on screen. Degrade instead.
  let layoutName = "cose"; // built-in, always available
  if (window.cytoscapeFcose) {
    cytoscape.use(window.cytoscapeFcose);
    layoutName = "fcose";
  } else {
    setStatus("fcose did not load — using the built-in cose layout.");
  }
</script>
```

| Extension                | UMD global             | Must load first            |
| ------------------------ | ---------------------- | -------------------------- |
| `cytoscape-fcose`        | `cytoscapeFcose`       | `layout-base`, `cose-base` |
| `cytoscape-cose-bilkent` | `cytoscapeCoseBilkent` | `layout-base`, `cose-base` |
| `cytoscape-dagre`        | `cytoscapeDagre`       | `dagre`                    |
| `cytoscape-klay`         | `cytoscapeKlay`        | `klayjs`                   |
| `cytoscape-cola`         | `cytoscapeCola`        | `webcola`                  |
| `cytoscape-popper`       | `cytoscapePopper`      | `@popperjs/core`           |
| `cytoscape-edgehandles`  | `cytoscapeEdgehandles` | —                          |
| `cytoscape-cxtmenu`      | `cytoscapeCxtmenu`     | —                          |

Guard every extension this way, not just the layout ones — `edgehandles` and `cxtmenu`
fail the same silent way. **Fall back to a built-in layout rather than shipping a page
that throws**: `breadthfirst` for hierarchies and `cose` for networks are always
available with zero extra script tags, and a working graph with a slightly worse layout
beats a blank canvas.

Published npm versions are immutable, so a pinned jsDelivr URL keeps resolving — the pin
goes stale, it does not break. Do not spend effort verifying the URLs; spend it on the
guard above, which is what actually catches a script tag that did not load.

## Rules

### Sizing and readable defaults

The most common way a technically-correct graph fails its user is being rendered at a
zoom nobody can read. Work out the zoom _before_ deciding to fit.

**A bare zoom threshold is the wrong test.** What decides legibility is the label's
rendered size — `zoom × font-size`, in CSS pixels — and a gate written as a constant like
`fitZoom >= 0.35` passes graphs whose labels Cytoscape then refuses to draw at all.
Measured on a 116-node org chart, `font-size: 10`, `min-zoomed-font-size: 7`, viewport
1828×559:

| Layout                                              | Bounding box | Aspect   | Fit zoom | Label at that zoom | Result                            |
| --------------------------------------------------- | ------------ | -------- | -------- | ------------------ | --------------------------------- |
| `breadthfirst` downward, `spacingFactor: 1.15`      | 4268 × 393   | 10.9 : 1 | 0.47     | 4.6px              | labels hidden — grey confetti     |
| `breadthfirst` `circle: true`, `spacingFactor: 1.0` | 1142 × 1115  | 1.02 : 1 | 0.50     | 5.0px              | labels hidden; structure readable |

Both clear 0.35 comfortably and both are unusable. `circle: true` fixes the aspect ratio —
the hierarchy is legible as _shape_ — but it does not fix label size, so it is a framing
fix, not a readability fix. Trees also get wider with depth, so a tree that fits
comfortably at 30 nodes will not at 150, and the failure never shows up in a small test
fixture.

Gate on the pixel size instead:

```js
const MIN_LABEL_PX = 7; // keep equal to your min-zoomed-font-size
const FONT_PX = 10; // the node font-size in your stylesheet

// Constructor layout? use cy.ready(...) instead — see rule 7.
const layout = cy.layout(opts);
layout.one("layoutstop", () => {
  const bb = cy.elements().boundingBox();
  const fitZoom = Math.min(cy.width() / bb.w, cy.height() / bb.h);

  if (fitZoom * FONT_PX >= MIN_LABEL_PX) {
    cy.fit(30); // labels survive the fit
  } else {
    cy.zoom(MIN_LABEL_PX / FONT_PX); // smallest zoom that still renders labels
    cy.center(cy.nodes().roots()); // start somewhere meaningful
    setStatus("Large graph — drag to pan, or search to jump to a node.");
  }
});
layout.run();
```

With those numbers the real gate is `fitZoom >= 0.7`, twice what a 0.35 constant allows.
Raising the font size lowers the gate proportionally; it does not remove it.

When fitting is not viable, give the user a way in: search-and-zoom-to-node, collapse to
the top two levels with expand on demand, or `circle: true` plus a starting zoom for
trees. Any of these is better than a fitted view of unreadable specks. Set `minZoom` to
`MIN_LABEL_PX / FONT_PX` too, so users cannot hand-zoom into that state either.

### Reference files (`${CLAUDE_SKILL_DIR}`)

Load these as needed; do not read all of them upfront.

- `references/layouts.md` — layout lifecycle, re-running without losing the user's place, which
  extension to pick
- `references/integration.md` — React, Vue, Svelte, bundlers, SSR, data validation
- `references/theming.md` — dark mode, design tokens, resolving CSS variables to canvas
- `references/recipes.md` — highlight, search, filter, expand/collapse, tooltips, export, context menus
- `references/performance.md` — scaling to thousands of elements, and when to stop
- `references/checklist.md` — pre-delivery verification
- `assets/template.html` — a complete, working, themeable single-file visualizer
- `scripts/to-elements.js` — data-shape converters and the `sanitize()` guard; require it
  rather than rewriting the conversion, and surface its `warnings`

## Stop conditions

Cytoscape.js is the wrong tool in the cases below. Say so rather than forcing it.

- **Above ~5,000 elements** interaction gets sluggish even tuned; above ~10,000 it is the
  wrong library. Reach for Sigma.js, regl-based renderers, or server-side layout with a
  rendered tile/image.
- **Purely hierarchical data with no cross-links** — a tree component or a D3 tidy tree
  is simpler and looks better.
- **Statistical relationships** (correlation, flows by volume) — a heatmap, chord
  diagram, or Sankey communicates better than a node-link diagram.
- **A single fixed diagram that never changes** — hand-authored SVG or Mermaid is less
  machinery.
