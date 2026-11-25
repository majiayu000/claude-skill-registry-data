---
name: c4-repo-doc
description: >
  Generates a detailed C4-model architecture document for the current repository:
  System Context, Container, Component, and Code (function/method) levels, plus a
  full call graph. Outputs Markdown, self-contained interactive HTML (force-directed
  SVG call graph, anchor links), and PDF. Use when user says "C4", "generate C4 docs",
  "document this repo", "architecture document", "call graph of this repo", or
  invokes /c4.
---

# C4 Repo Documentation Skill

Produce a maximum-detail C4 model of the current repo. C4 = 4 nested levels
(Simon Brown): **System Context → Container → Component → Code**. This skill adds
a generated function/method-level call graph as the Code level. Levels 1–3 are
prose + diagrams you write from reading the repo; Level 4 is extracted
deterministically by a script, then enriched by you.

## Output contract

All artifacts go in `<repo_root>/.gbencke/c4/`, basename:

```
<UTC timestamp>.diagram.<ext>     e.g. 2025-06-08T14-30-00Z.diagram.md
```

(ISO-8601 with `:` and `:` replaced by `-` — colons are hostile in filenames.)

Generate **three files sharing one basename**: `.md`, `.html`, `.pdf`, plus
`graph.json` (raw extraction, keep it — it's the data source).

## Workflow

### 1. Setup

```bash
TS=$(date -u +%Y-%m-%dT%H-%M-%SZ)
OUT="<repo_root>/.gbencke/c4"; mkdir -p "$OUT"
BASE="$OUT/$TS.diagram"
```

### 2. Extract the call graph (deterministic half)

```bash
python3 <skill_dir>/scripts/extract_calls.py <repo_root> --out "$OUT/graph.json"
```

- Requires `ast-grep`/`sg` on PATH. If missing: tell the user, fall back to
  manual extraction via the `lsp_symbols` tool + reading code, and say so in
  the output's Methodology section.
- Covers Python, JS/TS/TSX, Go, Rust, Java, C/C++, Ruby.
- Output: `defs` (every function/method/class with file + line range) and
  `edges` (caller → callee, resolved to def ids where possible).
- **Verify before trusting**: spot-check 3–5 edges against the real code.
  Name-matching can fan out on overloaded/common names (`init`, `run`,
  `render`); prune wrong targets in your narrative and note it. If the repo
  uses a language with poor yield, extend `DEF_KINDS`/`NAME_RES` in the script
  or extract that language by hand.

### 3. Survey the repo (semantic half)

Read, in order: README/docs, manifests (`package.json`, `pyproject.toml`,
`go.mod`, …), entry points (`main`, CLI, server bootstrap), config, docker/
deploy files, top-level directory layout. Identify:

- **Persons**: who uses this (roles, not individuals).
- **External systems**: APIs, databases, queues, SaaS it talks to.
- **Containers** (C4 sense — deployable/runnable units): apps, services, DBs,
  workers. NOT Docker necessarily.
- **Components**: the major modules/packages inside each container.

### 4. Write the Markdown (`$BASE.md`)

This is the single source of truth; the HTML is a rendering of it. Structure:

1. **Title block**: repo name, timestamp, commit hash (`git rev-parse --short HEAD`).
2. **Methodology**: one short paragraph — how the doc was generated, script
   version caveats, confidence notes.
3. **Level 1 — System Context**: the system as one box; persons and external
   systems around it; every relationship labelled with an active verb
   ("Reads trades from", not "is connected to"). Mermaid diagram + table.
4. **Level 2 — Containers**: zoom into the system. One subsection per
   container: purpose, technology, runtime, what it talks to. Mermaid diagram.
5. **Level 3 — Components**: one section per container, decomposed. Every
   component: responsibility, key files, dependencies. Mermaid diagram per
   container (skip trivial ones).
6. **Level 4 — Code (function/method level)**: the bulk. Per component, per
   file:
   - **Symbol inventory table**: name, kind, lines, one-line purpose (write
     the purpose from reading the code — do not copy docstrings blindly).
   - **Call tables**: for every function/method, `Calls:` list and
     `Called by:` list, built from `graph.json` edges, formatted as
     `` `name` (file:line) `` links to anchors in HTML.
   - Entry points and hot paths (most-called functions — compute fan-in from
     `graph.json`) get a paragraph each, not just a row.
7. **Appendix**: top-20 functions by fan-in, top-20 by fan-out, orphan
   functions (no callers, excluding entry points — candidate dead code).

C4 rules to respect: one abstraction level per diagram; active verbs on every
relationship; every element has a name + short description; no deployment
detail in logical diagrams.

### 5. Write the HTML (`$BASE.html`)

Self-contained single file. **No CDN, no external requests** — must work
offline. Requirements:

- Inline CSS, clean readable layout, sticky table of contents with anchor
  links to every section/function.
- Every function/method heading gets `id="fn-<sanitized-file--name--line>"`
  so call tables and the graph link to it (`<a href="#fn-...">`).
- Levels 1–3: hand-authored inline SVG (boxes + labelled arrows are enough —
  few nodes, keep layout manual and tidy).
- **Level 4 interactive call graph**: inline `<svg class="cg" data-graph="main">`
  + `<script>window.GRAPHS = {...}</script>` + the contents of
  `<skill_dir>/assets/callgraph.js` inlined verbatim. Build the `"main"` graph
  from `graph.json`: nodes = defs (`id`, `label`=name, `kind`,
  `anchor`=matching heading id), edges = resolved caller→target pairs.
  If defs > ~400, default the graph to a filtered view (e.g. one component or
  top-100 by fan-in) and say so — a hairball helps no one.
- **Per-component code diagrams**: one `<svg class="cg" data-graph="<comp>">`
  per Level-3/4 component. Nodes = the component's symbols (cap ~40 by
  connectivity, but never cap away inheritance pairs), edges = internal calls
  plus `kind:"inherits"` edges from class bases (extract with `ast`). All go
  in `window.GRAPHS` keyed by component path.
- `callgraph.js` drives every `svg.cg` on the page: class-box nodes colored
  by kind, per-diagram filter box (matches + 1-hop neighbours), drag nodes,
  drag-background pan, wheel/button zoom, reset. Don't rewrite it.
- **Left sidebar navbar**: fixed `nav#TOC` (h2–h4 links, ellipsis overflow),
  content wrapped in a `.content` div with `margin-left`; collapse to static
  under 900px; hide in print.
- Print CSS (`@media print`): hide `.cg-controls` and the sidebar,
  page-break before each Level section.

### 6. Generate the PDF (`$BASE.pdf`)

Chrome headless, with a virtual-time budget so the JS/SVG renders first:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=15000 \
  --print-to-pdf="$BASE.pdf" "file://$BASE.html"
```

Fallbacks if Chrome is absent: `weasyprint "$BASE.html" "$BASE.pdf"`, then
`pandoc "$BASE.md" -o "$BASE.pdf"`. Use whichever exists, note which in the
final report. The PDF is static by nature — that's fine, the HTML is the
interactive artifact.

### 7. Verify and report

- Re-open the HTML: check the TOC anchors resolve and `window.GRAPH` parses
  (headless `--dump-dom` and grep for `circle` works).
- Check the PDF exists and is non-trivial in size.
- Report to the user: the three paths, def/edge counts, languages covered,
  and any extraction gaps you had to fill by hand.

## Tone

Maximum detail, minimum filler. Every sentence in the doc must carry
information a reader can't get from the filename. No "this module contains
various utilities" — say what it does.
