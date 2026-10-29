---
name: yantra
description: "Make interactive, step-by-step diagrams and one-page answers as single offline HTML files with Yantra: architecture and system diagrams, request and data flows, pipelines, sequence diagrams for APIs, auth and payment flows, ERD / data model / database schema diagrams, class diagrams, state machines and lifecycles, org charts, decision trees, mind maps, and explainer pages, comparisons or decision records. Use when the user asks to diagram, visualise or visualize something, draw the architecture or a flow, explain how a system, codebase or process works step by step, wants a one-page answer to share, or wants to import or convert a Mermaid, PlantUML, draw.io or Visio diagram."
---

# Yantra

Yantra turns a JSON payload into an interactive diagram (with a walkthrough) or a one-page
answer, as one offline HTML file. Layout, edge routing and label placement are automatic;
the validator checks the rendered geometry.

## Tools

Use the MCP tools when the `yantra` server is connected; otherwise run the CLI. With the
package installed (`npm i -D @niyankhadka/yantra` or `-g`), `yantra <cmd>` works; otherwise
use `npx -y @niyankhadka/yantra <cmd>`.

| Action | MCP tool | CLI |
|---|---|---|
| Schema and authoring rules | `yantra_get_schema` (`kind: "page"` for pages) | `yantra schema [diagram\|page]`, `yantra docs authoring\|pages\|mermaid\|import` |
| Reference examples | `yantra_list_examples`, `yantra_get_example` | `yantra examples`, `yantra examples <name> -o ref.json` |
| Starter file | - | `yantra new file.json [--page]` |
| Import Mermaid, PlantUML, draw.io, Visio | `yantra_import` | `yantra import sketch.mmd -o file.json` |
| Validate | `yantra_validate` | `yantra validate file.json` |
| Build HTML | `yantra_build` | `yantra build file.json -o file.html` |
| Look at it | `yantra_screenshot` | `yantra screenshot file.json [--step n] [--view sequence] [--theme dark]` |
| SVG or Markdown | `yantra_export` | `yantra export file.json -f svg\|md` |

Read the schema and rules once before writing the first payload of a session, and open the
closest example: `oauth-login` (sequence), `cloud-architecture`, `aws-serverless` (groups),
`platform-overview` (overview with drill-down), `ecommerce-schema` (ERD),
`payment-classes` (class diagram), `ticket-lifecycle` (state machine), `org-chart`,
`incident-triage-decision-tree`, `study-plan-mindmap` (trees), `answer-checkout-saga`
(answer page), `chart-sales-dashboard` (charts). The MCP server reads and writes only inside
the folder it runs in (the project), so keep files there.

## Pick the output

| The user wants... | Make |
|---|---|
| how parts connect, how a request or pipeline flows | diagram (flow view) |
| who calls whom, in order (API call, auth, payment, webhook, handshake) | diagram with `meta.view: "sequence"` |
| the states something goes through | diagram with `shape: "state"` / `"initial"` / `"final"` / `"choice"` nodes |
| a hierarchy: org chart, decision tree, breakdown, mind map | diagram with `meta.layout.algorithm: "tree"` or `"mindmap"` |
| tables and relations (ERD), classes | diagram with node `data.fields` / `data.methods` |
| an answer, explanation, comparison or decision | answer page (`"kind": "page"`) |
| their Mermaid, PlantUML, draw.io or Visio diagram | `import`, then review the warnings |

For "explain how X works", make the diagram first, then a page around it
(`{ "type": "diagram", "src": "flow.json" }`).

## Diagram rules

1. **Story first**: the question the diagram answers and 3-8 walkthrough steps. The first
   step is an overview (highlights nothing); each focused step lists the nodes **and** the
   edges involved, and every highlighted edge has both endpoints highlighted.
2. **Budgets**: at most 14 cards as it opens (aim for 6-10), 20 edges, 3-5 `roles` (one
   colour each), titles up to 42 characters, edge labels 1-3 words (up to 28 characters),
   2-5 `groups` for boundaries that matter (VPC, trust zone, team). Bigger systems: an
   overview whose cards drill into detail diagrams (`data.drill: "<id>"` plus
   `diagrams.<id>`, or `{ "$ref": "./detail.json" }`), or fold groups.
3. **No coordinates**: never write `x`/`y`; point edges along the main flow.
4. Cards show `title`, `subtitle` (its job, a few words) and `tech`; longer text goes in
   `description`, facts in `metadata`, the code location in `sourceFile`.
5. Edge labels name what flows (`JWT`, `Order event`, `SQL write`); in a state machine, the
   event. `type: "async"` or `"event"` for asynchronous flows.
6. **Walkthrough**: `meta.story` `"collapsed"` opens it as one slim bar, `"off"` shows the
   diagram as a picture (readers can still switch with W).
7. **Charts on cards**: `data.chart` draws a mini chart (`line`, `area`, `column`, `bar`,
   `donut`, `ring`, `bullet`). Card limits: `bar` 8 rows, `donut` 6 slices, `column` 16,
   `line` / `area` 48 points. More bars: a chart card (`"shape": "chart"`, same `data`, up
   to 12). At most 12 mini charts and 6 chart cards.

## Diagrams from a codebase

1. **Read before drawing**: entry points and routes, services and their clients, queues and
   jobs, config and infrastructure files, the schema or migrations. Draw what the code does,
   not what names suggest, and cite files in `data.sourceFile` (`src/api/orders.ts`).
2. **Architecture**: one overview of the main components (clients, services, stores,
   external APIs) with a walkthrough of the main request; for large systems, one detail
   diagram per subsystem linked by `data.drill` rather than one crowded picture.
3. **Data model (ERD)**: one card per table from the schema, ORM models or migrations;
   `data.fields` rows (`{ name, type, pk, fk, unique, nullable, ref }`, at most 12 per card,
   key columns first); edges with `sourceEnd` / `targetEnd` (`one`, `many`, `zero-or-many`,
   ...) and `sourceField` / `targetField` so each edge joins the FK row to the PK row.
4. **Auth, payment, webhook and other request/response flows**: a sequence diagram
   (`meta.view: "sequence"`), one step per message, in order, with the request and
   response named on the edges; put example payloads in `step.payload`.
5. **Lifecycles** (order status, subscription, ticket): a state machine from the enum and
   the code that changes it; edge labels are the events.
6. **Where files go**: keep sources and outputs together, for example
   `docs/diagrams/<name>.json` and `docs/diagrams/<name>.html`, unless the project already
   has a place for diagrams. Link the HTML from the README or docs if asked.

## Answer page rules

1. `answer.headline` first: the conclusion in 1-2 sentences; then `answer.text` and 3-5
   `answer.points`.
2. 3-8 blocks chosen by content (`points`, `steps`, `metrics`, `chart`, `compare`, `table`,
   `timeline`, `faq`, `checklist`, `callout`, `code`, `sources`, `diagram`, `gantt`,
   `matrix`, ...). At most 2 diagrams with `interactive: true` per page. `span: "half"` or
   `"third"` puts blocks side by side; a `section` groups blocks under a heading.
3. Do not state uncertain facts as certain: flag them in a `callout` and cite `sources`.
4. **Books**: when one page is not enough, a `{ "kind": "book" }` holds 2-12 answer pages as
   `chapters` (inline, or `{ "$ref": "chapter.json" }`) and reads like an e-reader. See
   `docs/books.md` (`yantra docs books`).

## Finish every output

1. **Validate** and fix errors in this order: `schema/*`, `ref/*`, `page/*`, `layout/*`,
   `geometry/*`, then warnings. At most two repair rounds; if geometry still fails, remove
   cards or split the diagram.
2. **Build** the HTML.
3. **Look**: take a screenshot (also a focused `--step`, `--view sequence` for sequences,
   `--theme dark`) and view the PNG. Do not say it looks right without viewing it.
4. **Report** the HTML path and the walkthrough steps (or the page headline), plus any
   warnings you kept.

`meta.watermark: false` hides the "Made with Yantra" badge. Content not in English: set
`meta.lang` and write all text in that language.
