---
name: yantra
description: Create interactive, step-by-step diagrams (architecture, request flows, pipelines, business or clinical processes) and one-page answers (explainers, comparisons, decision records) as single offline HTML files with automatic layout, routed edges, summary cards and a validator. Use when the user wants to visualise how a system or process works, explain a flow step by step, turn a description, codebase or Mermaid, draw.io or PlantUML sketch into a shareable diagram, or asks a question whose answer should be a page to read, print or share.
---

# Yantra

Every output is a single offline HTML file. Pick one:

| The user wants… | Make | Guide |
|---|---|---|
| to see how parts connect or how a flow runs | **diagram** | `docs/authoring.md`, `schemas/yantra-payload.schema.json` |
| who calls whom, in order (protocol, API call, handshake) | **diagram** with `meta.view: "sequence"` | `docs/authoring.md` (Sequence view) |
| the states something goes through (lifecycle, state machine) | **diagram** with `shape: "state"` / `"initial"` / `"final"` / `"choice"` nodes | `docs/authoring.md` (State machines) |
| a hierarchy: org chart, decision tree, breakdown, taxonomy, mind map | **diagram** with `meta.layout.algorithm: "tree"` or `"mindmap"` | `docs/authoring.md` (Trees, org charts and mind maps) |
| a database schema (ERD) or class diagram | **diagram** with node `fields` / `methods`, edge `sourceEnd` / `targetEnd` or `relation` | `docs/authoring.md` (Data models) |
| an answer, explanation, comparison or decision on one page | **answer page** (`"kind": "page"`) | `docs/pages.md`, `schemas/yantra-page.schema.json` |
| their Mermaid flowchart / sequence / state / ER / class diagram, mind map or journey as Yantra (a gantt, pie, timeline or quadrantChart becomes an answer page) | `node bin/yantra.js import sketch.mmd` then review | `docs/mermaid.md` |
| their draw.io (`.drawio`, `.drawio.png`), Visio (`.vsdx`) or PlantUML (`.puml`, `@startgantt` → page) diagram as Yantra | `node bin/yantra.js import file.drawio` (`--page n`) then review | `docs/import.md` |

For "explain how X works", make the diagram first, then the page around it
(`{ "type": "diagram", "src": "flow.json" }`). References: `examples/*.json`
(`answer-*.json` are pages and `chart-*.json` are dashboard pages: sales, budget, survey, SLA; `oauth-login.json` is a sequence; `aws-serverless.json` has groups;
`platform-overview.json` drills into detail diagrams; `ticket-lifecycle.json` is a state machine;
`ecommerce-schema.json` is an ERD; `payment-classes.json` is a class diagram;
`org-chart.json`, `incident-triage-decision-tree.json` and `study-plan-mindmap.json` are trees).

## Diagram

1. **Plan the story**: the question it answers and 3-6 walkthrough steps. More than ~12
   nodes → an overview plus detail diagrams: give the subsystem card `data.drill: "<id>"`
   and put the detail diagram (its own nodes, edges, steps) under `diagrams.<id>`, or
   `{ "$ref": "./detail.json" }` for a file next to it. Up to 8 levels (deep breadcrumbs
   fold their middle into a menu); see Drill-down in `docs/authoring.md`. A card can open
   another level per mode: `data.modes.<id>.drill`.
2. **Write the payload** (`meta`, `roles`, `nodes`, `edges`, `scenarios`) in one pass.
   - Do **not** write `x`/`y`. Point edges along the main flow; layout and routing are automatic.
   - Group node `type`s into 3-5 `roles` with one colour each; specific label in `data.badge`.
   - Cards show `title`, `subtitle`, `tech`; details go in `description`, `metadata`, `sourceFile`.
   - Edge labels: 1-3 words naming what flows (in a state machine: the event).
   - `edge.arrow`: `"both"` for one two-way edge, `"none"` for an undirected link. An edge
     whose `source` is its `target` draws a self-loop (retry, edit, poll); keep it.
   - Boundaries that matter to the explanation (VPC, trust zone, team, phase) → `groups`:
     2-5 of them, each node in its innermost group only.
   - Deep hierarchies (city > district > service > system > site > sensors, trust > hospital
     > ward > bay > bed) nest groups with `parent`, up to 6 levels and 24 groups in one frame;
     a group may hold only child groups (`"nodes": []`). Open with inner boxes folded
     (`meta.layout.collapsed`, list inner ids too) and let steps open them with
     `focusGroup: "<group id>"`. When a level needs its own story or the cards would pass ~14,
     drill down instead, or both. See Deep hierarchies in `docs/authoring.md`.
   - Hierarchies → `meta.layout.algorithm: "tree"` (`direction: "TB"` for org charts and
     decision trees, `"LR"` for deep breakdowns) or `"mindmap"`. Edges go parent → child, one
     parent per node; hierarchy edges need no label (label decision branches `Yes` / `No`).
     Up to ~40 cards; for bigger trees fold branches with `meta.layout.collapsed`. Wide org
     charts stack leaf teams in a column by themselves (`meta.layout.compact`, default
     `"auto"`); mark an assistant or chief of staff `data.assistant: true` to sit beside
     the manager. Groups are not drawn in trees: fold a subtree instead.
   - Steps: an overview first, then focused steps listing the nodes **and** edges involved.
     In the sequence view each step's `highlightEdges` become its arrows, in order.
   - Inspector tabs come from content, so include only what was asked for: `meta.summary`
     → **Summary**; step `payload`s → **Step**; node `description`/`metadata`/`tech` →
     **Details**; anything else (risks, costs, glossary) → a `panels` entry built from page
     blocks. Set `meta.inspector.onNodeClick` (a panel id, or `"stay"`) only when needed.
   - For code-backed diagrams, read the code first and cite it in `data.sourceFile`.
   - Tables and classes: `data.fields` (`{ name, type, pk, fk, unique, nullable, ref }`) and
     `data.methods` (`{ name, params, type, visibility }`), at most 12 rows per card;
     `data.stereotype: "interface"`. ER edges: `sourceEnd` / `targetEnd` (`one`, `zero-or-one`,
     `many`, `one-or-many`, `zero-or-many`) plus a verb label. UML edges: `relation`
     (`inheritance`, `realization`, `composition`, `aggregation`, `association`, `dependency`)
     pointing parent → child and whole → part; structural relations need no label.
     `sourceField` / `targetField` attach an edge at a field row (FK → PK); `sourceLabel` /
     `targetLabel` add multiplicities (`"1"`, `"0..*"`) beside the ends.
   - State machines: `shape: "fork"` is a fork / join bar; concurrent regions are child groups
     with `"kind": "region"` under the composite state's group.
     A diagram of only table / class cards has no sequence view; `meta.views: ["flow"]` hides
     the Flow / Sequence toggle on any other diagram whose steps are not messages.
   - Numbers that belong to a component (latency, uptime, conversion, a reading) →
     `data.chart` draws a mini chart on its card: `{ "kind": "line", "label": "p95 latency",
     "values": [..], "target": 160, "unit": " ms" }`; kinds `line`, `area`, `column`, `bar`
     (`data`, up to 8), `donut` (up to 6), `ring` (`value` of `max`), `bullet` (`value` against `target`).
     A dashboard number the diagram is about → a chart card: `"shape": "chart"` with a page
     chart block in `data.chart` (column, bar, line, area, pie, donut); it takes the same
     `data` list, so more bars than a card fits → add `"shape": "chart"`. At most 6 chart cards
     and 12 mini charts; see Charts in diagrams in `docs/authoring.md`.
   - Runbooks, dashboards, specs: `url` on a node (`data.url`), edge or step (http, https or
     mailto only); the inspector opens them in a new tab.
   - A diagram read mostly as a picture: `meta.story: "collapsed"` (one slim walkthrough bar)
     or `"off"` (no walkthrough, nothing dimmed; readers can switch it on with W).

## Answer page

1. Write `answer.headline` first: the conclusion in 1-2 sentences. Then `answer.text` and
   3-5 `answer.points`.
2. Add 3-8 blocks chosen by content: `points`, `steps`, `metrics`, `chart`, `compare`,
   `table`, `timeline`, `faq`, `checklist`, `quote`, `image`, `kv`, `callout`, `text`,
   `code`, `sources`, `diagram`, `gantt`, `matrix`. See the table in `docs/pages.md`.
   Numbers: `chart` with `kind` bar (default), column, line, area (trends; dates allowed),
   pie or donut (parts of a whole, ≤ 8 slices); several series via `categories` + `series`
   (≤ 6, `stacked: true` to stack); `trend: [..]` on a metric adds a sparkline. Plans:
   `gantt` (tasks with `start`/`days`/`after`, `milestone`, `group`, `today`; `workdays: true`
   counts working days, `holidays: [dates]`). Priorities
   and risks: `matrix` (2x2 with `quadrants`, or `grid: 5` heat map).
3. Diagrams are static figures; `interactive: true` embeds the live viewer - at most 2 per page.
4. Do not state uncertain facts as certain: flag them in a `callout`, cite `sources`.
5. Layout: `span: "half"` pairs blocks, `span: "third"` puts three in a row; a `section`
   (`title`, `intro?`, `blocks`) groups blocks under a heading, one level deep.
   `meta.reading` opens the page in `scroll` (default), `book` or `present` mode.
6. **Books** (`"kind": "book"`, `docs/books.md`): 2-12 answer pages as `chapters`, inline or
   `{ "$ref": "chapter.json" }`, with a `summary` on the cover. Use one when a single page is
   not enough (onboarding, a system part by part); each chapter keeps the page rules.
   `node bin/yantra.js new guide.json --book` writes a starter.
7. **Detail pages** (`docs/pages.md`): when a block needs depth only some readers want, put
   the deeper answer page in a top-level `details` map (`{ "id": page }` or `{ "$ref": … }`)
   and add `"detail": "id"` to the block; details can link to other details of the same
   map. Keep the page itself short; every detail must be linked from somewhere.

## Then, for every output

1. **Validate**: `node bin/yantra.js validate file.json`. Fix errors in this order:
   `schema/*` → `ref/*` → `page/*` → `layout/*` → `geometry/*`, then warnings. At most two
   repair rounds; if geometry still fails, remove nodes or split the diagram.
2. **Build**: `node bin/yantra.js build file.json -o file.html`
3. **Look**: `node bin/yantra.js screenshot file.json` (diagrams: `--step 2`, sequence:
   `--view sequence`; detail diagrams: `--level <id>`; pages: `--height 3200` if long,
   `--width 390` for phones; also `--theme dark`) and view the PNG.
   Do not say it looks right without viewing it.
4. **Report** the HTML path and, in chat, the answer headline or the walkthrough steps,
   plus any warnings you chose to keep. `export -f md` gives a Markdown copy to paste.

With the MCP server connected the same actions are tools: `yantra_get_schema` (pass
`kind: "page"` for pages), `yantra_get_example`, `yantra_import` (Mermaid, draw.io, PlantUML, Visio),
`yantra_import_mermaid`, `yantra_validate`,
`yantra_build`, `yantra_export`, `yantra_screenshot`.

## Other outputs

- Static SVG: `node bin/yantra.js export diagram.json -f svg [--theme dark] [--view sequence]`
- Markdown: `node bin/yantra.js export file.json -f md` (`--all-levels` adds every detail diagram)
- `meta.watermark: false` hides the "Made with Yantra" badge; a string replaces its text.
- Content not in English: set `meta.lang` (BCP 47; built in: en es fr de pt it hi bn ne zh zh-Hant ja ko id
  ar he fa ur; zh-TW/zh-HK use zh-Hant) and
  write all payload text in that language. Labels, number formats and `<html lang>` follow it;
  ar/he/fa/ur (or `meta.dir: "rtl"`) mirror the chrome while the diagram keeps its layout.
  `meta.strings` overrides a label by key. Screenshot both themes to check the script renders.
  Title/label budgets count CJK characters as 2 (about 21 for a title). `yantra validate --lang auto`
  gives the common messages in the payload language.
  See `docs/authoring.md` (Languages and right to left).
- Exact hand layout (rare): `meta.layout.mode: "manual"` plus `x`/`y` on the 10px grid.
