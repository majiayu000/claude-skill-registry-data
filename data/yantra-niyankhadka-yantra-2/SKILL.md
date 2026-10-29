---
name: yantra
description: "Make interactive, step-by-step diagrams and one-page answers with Yantra, written as Yantra JSON that the user opens in the Yantra playground or builds into one offline HTML file: architecture and system diagrams, request and data flows, pipelines, sequence diagrams for APIs, auth and payment flows, ERD / database schema and class diagrams, state machines and lifecycles, org charts, decision trees, mind maps, and explainer pages, comparisons or decision records. Use when the user asks to diagram, visualise or visualize something, draw an architecture or a flow, explain how a system or process works step by step, or wants a one-page answer to share."
---

# Yantra (chat edition)

Yantra turns a JSON payload into an interactive diagram (with a walkthrough) or a one-page
answer, as one offline HTML file. Layout, edge routing and label placement are automatic.
This edition is for chats without a shell: you write the JSON, the user views and downloads
it. (In a coding agent, the `yantra` skill shipped in the npm package runs the CLI instead.)

## How to answer

1. One or two sentences on what you made, then ONE ```json code block holding the whole
   payload: valid JSON, no comments, no trailing commas, nothing else in the block.
2. After the block, list the walkthrough steps (diagram) or repeat the headline (page), and
   tell the user how to see it:
   - paste the JSON into the playground, https://yantra.nbk.com.np/playground/ (checks it,
     shows the result, downloads HTML, SVG, PNG or Markdown; nothing leaves the browser), or
   - save it as `file.json` and run `npx -y @niyankhadka/yantra build file.json`.
3. If a code execution tool with npm access is available, you may run
   `npx -y @niyankhadka/yantra validate file.json` and `build` yourself and offer the HTML.
   Otherwise never claim the JSON was validated: check it against the rules below instead.
4. If the user pastes validation findings back (codes such as `ref/edge-unknown-target`),
   fix exactly those and send the full corrected JSON again.

The schemas are in `reference/` (`yantra-payload.schema.json` for diagrams,
`yantra-page.schema.json` for pages) and complete examples in `examples/`:
`oauth-login.json` (sequence), `aws-serverless.json` (groups), `ticket-lifecycle.json`
(state machine), `ecommerce-schema.json` (ERD), `org-chart.json` (tree) and
`answer-checkout-saga.json` (answer page). Read the closest one before a large payload.

## Pick the output

| The user wants... | Make |
|---|---|
| how parts connect, how a request or pipeline flows | diagram (flow view) |
| who calls whom, in order (API call, auth, payment, webhook, handshake) | diagram with `meta.view: "sequence"` |
| the states something goes through | diagram with `shape: "state"` / `"initial"` / `"final"` / `"choice"` nodes |
| a hierarchy: org chart, decision tree, breakdown, mind map | diagram with `meta.layout.algorithm: "tree"` or `"mindmap"` |
| tables and relations (ERD), classes | diagram with node `data.fields` / `data.methods` |
| an answer, explanation, comparison or decision | answer page (`"kind": "page"`) |

For "explain how X works" with both a picture and an argument, make an answer page with a
`diagram` block holding the diagram inline (`{ "type": "diagram", "diagram": { ... } }`).

## Diagram shape

```
{ "meta": { "title", "description", "layout"?: { "direction": "LR"|"TB", "algorithm"?: "layered"|"tree"|"mindmap" },
            "view"?: "flow"|"sequence", "summary"?: ["3-5 key points"], "lang"?: "BCP 47 tag" },
  "roles": { "<type>": { "label", "color": blue|teal|green|amber|rose|violet|orange|slate, "icon"? } },
  "nodes": [ { "id", "type": "<role key>", "shape"?: card|state|initial|final|choice|fork|chart,
               "data": { "title", "subtitle"?, "tech"?, "badge"?, "icon"?, "description"?, "metadata"?: { "Owner": "..." },
                         "url"?, "fields"?: [{ "name", "type", "pk"?, "fk"? }], "methods"?: [{ "name", "params"?, "type"? }] } } ],
  "edges": [ { "id", "source": "<node id>", "target": "<node id>", "label"?, "type"?: sync|async|event|stream|data,
               "arrow"?: forward|both|none, "relation"?: inheritance|realization|composition|aggregation|association|dependency,
               "sourceEnd"?/"targetEnd"?: one|zero-or-one|many|one-or-many|zero-or-many } ],
  "groups"?: [ { "id", "title", "nodes": ["<node id>"], "parent"?: "<group id>" } ],
  "scenarios": [ { "id", "name", "steps": [ { "id", "title", "description"?, "highlightNodes"?: [ids], "highlightEdges"?: [ids] } ] } ] }
```

Icons: cpu server database layers shield key globe zap credit-card user users building truck
warehouse package book-open graduation-cap award activity heart file-text crosshair
check-circle flag mail cloud monitor settings.

## Diagram rules

1. **Story first**: the question the diagram answers and 3-6 walkthrough steps. The first
   step is an overview (highlights nothing); each focused step lists the nodes **and** the
   edges involved, and every highlighted edge has both endpoints highlighted.
2. **Budgets**: at most 14 cards (aim for 6-10), 20 edges, 3-5 `roles` (one colour each),
   titles up to 42 characters, edge labels 1-3 words (up to 28 characters), 2-5 `groups`
   for boundaries that matter (VPC, trust zone, team); a node sits only in its innermost group.
3. **No coordinates**: never write `x`/`y`; point edges along the main flow (user ->
   service -> store) and keep return edges (refund, retry) as they are.
4. **Ids**: short, unique, kebab-case; every edge `source` / `target` and every highlighted
   id must exist. Copy ids, do not retype them.
5. Cards show `title`, `subtitle` (its job, a few words) and `tech`; longer text goes in
   `description`, facts in `metadata`.
6. Edge labels name what flows (`JWT`, `Order event`, `SQL write`); in a state machine, the
   event. `type: "async"` or `"event"` for asynchronous flows.
7. **Sequences** (`meta.view: "sequence"`): one step per message, in order; each step's
   `highlightEdges` become its arrows.
8. **Trees** (`"layout": { "algorithm": "tree", "direction": "TB" }`, or `"mindmap"`): edges
   parent -> child, one parent per node, no groups; label decision branches `Yes` / `No`.
9. **Data models**: cards with `data.fields` (`{ name, type, pk, fk, unique, nullable, ref }`,
   at most 12 rows, key columns first); ER edges with `sourceEnd` / `targetEnd` and a verb
   label; class diagrams use `data.methods` and edge `relation` (parent -> child).
10. **Charts on cards**: `data.chart` draws a mini chart (`kind` `line`, `area`, `column`,
   `bar`, `donut`, `ring`, `bullet`; `values` or `data: [{ label, value }]`). Limits on a
   card: `bar` 8 rows, `donut` 6 slices, `column` 16, `line` / `area` 48 points. More bars:
   a chart card (`"shape": "chart"`, same `data`, up to 12). At most 12 mini charts and 6
   chart cards.
11. Content not in English: set `meta.lang` and write all text in that language.

## Answer page shape

```
{ "kind": "page",
  "meta": { "title", "question"?, "kicker"?: "Explainer|Decision|How-to|Incident review|...", "author"?, "date"? },
  "answer": { "headline": "the conclusion in 1-2 sentences (under 220 characters)", "text"?, "points"?: ["3-5 facts"] },
  "blocks": [ ... 3-8 blocks ... ] }
```

Blocks (`"type"`, then fields): `points` items[{title,text?,tone?}] - `steps` items[{title,text?}] -
`metrics` items[{label,value,note?,trend?:[numbers]}] - `chart` kind bar|column|line|area|pie|donut,
data[{label,value}] or categories[] + series[{name,values[]}], unit?, prefix? - `compare`
options[{name,summary?,pros?[],cons?[],verdict?,recommended?}] - `table` columns[], rows[[cells]] -
`timeline` items[{date,title,text?}] - `faq` items[{q,a}] - `checklist` items[{text,done?}] -
`callout` body, tone info|good|warn|bad - `text` body - `code` code, language? - `sources`
items[{title,url?}] - `kv` items[{k,v}] - `quote` text, by? - `gantt` items[{title,start?,days?,after?,milestone?}] -
`matrix` items[{label,x,y}], x, y, quadrants? - `diagram` diagram:{...a diagram payload...}, caption?.

## Answer page rules

1. `answer.headline` first: the conclusion in 1-2 sentences, not a teaser; then
   `answer.text` and 3-5 `answer.points`.
2. 3-8 blocks chosen by content; any block takes `title`, `span: "half"` pairs two blocks
   side by side, `span: "third"` puts three in a row, and a `section` (`title`, `intro?`,
   `blocks`) groups blocks under a heading, one level deep. At most 2 diagram blocks with
   `interactive: true`. `meta.reading`: `scroll` (default), `book` or `present`.
3. Numbers need units and context (`unit`, `prefix`, `note`). Dates as `DD/MM/YYYY` or
   `YYYY-MM-DD`. Prefer a `compare` with a `recommended` option over "it depends".
4. Do not state uncertain facts as certain: flag them in a `callout` and cite `sources`.
5. **Books**: when one page is not enough (onboarding, a system part by part), write
   `{ "kind": "book", "meta": { "title", "description"? }, "summary"?, "chapters": [...] }`
   with 2-12 answer pages (no `kind`) as chapters, one question each. It reads like an
   e-reader, one screen at a time.

## Check before sending

- The block parses as JSON (quotes, commas, brackets).
- Every edge endpoint and highlighted id is a real node or edge id; ids are unique.
- Every highlighted edge has both of its nodes highlighted in that step.
- No `x` / `y`; titles and labels within budget; 3-6 steps, the first an overview.
- Pages: `kind`, `meta.title` and `answer.headline` are present; every block has a known `type`.

## Smallest valid diagram

```json
{
  "meta": { "title": "Checkout", "description": "How an order is paid and stored." },
  "roles": {
    "client": { "label": "Client", "color": "amber" },
    "service": { "label": "Service", "color": "blue" },
    "data": { "label": "Data", "color": "violet" }
  },
  "nodes": [
    { "id": "web", "type": "client", "data": { "title": "Web app", "subtitle": "Customer checkout", "icon": "monitor" } },
    { "id": "api", "type": "service", "data": { "title": "Orders API", "subtitle": "Validates and charges", "tech": "Go" } },
    { "id": "db", "type": "data", "data": { "title": "Orders DB", "subtitle": "Source of truth", "tech": "PostgreSQL", "icon": "database" } }
  ],
  "edges": [
    { "id": "web-api", "source": "web", "target": "api", "label": "POST /orders" },
    { "id": "api-db", "source": "api", "target": "db", "label": "INSERT order" }
  ],
  "scenarios": [
    {
      "id": "main",
      "name": "Place an order",
      "steps": [
        { "id": "s1", "title": "Overview", "description": "Three parts: client, API, database." },
        { "id": "s2", "title": "Submit", "description": "The browser posts the cart.", "highlightNodes": ["web", "api"], "highlightEdges": ["web-api"] },
        { "id": "s3", "title": "Persist", "description": "The API stores the order.", "highlightNodes": ["api", "db"], "highlightEdges": ["api-db"] }
      ]
    }
  ]
}
```

## A short sequence diagram

```json
{
  "meta": { "title": "Password reset", "description": "How a reset link is requested and used.", "view": "sequence" },
  "roles": {
    "person": { "label": "Person", "color": "amber", "icon": "user" },
    "service": { "label": "Service", "color": "blue" },
    "external": { "label": "External", "color": "slate", "icon": "mail" }
  },
  "nodes": [
    { "id": "user", "type": "person", "data": { "title": "User", "subtitle": "Forgot the password" } },
    { "id": "web", "type": "service", "data": { "title": "Reset page", "subtitle": "Takes the new password" } },
    { "id": "auth", "type": "service", "data": { "title": "Auth service", "subtitle": "Issues reset tokens" } },
    { "id": "mail", "type": "external", "data": { "title": "Email provider", "subtitle": "Delivers the link" } }
  ],
  "edges": [
    { "id": "ask", "source": "user", "target": "auth", "label": "Reset request" },
    { "id": "send", "source": "auth", "target": "mail", "label": "Send link", "type": "async" },
    { "id": "deliver", "source": "mail", "target": "user", "label": "Email" },
    { "id": "open", "source": "user", "target": "web", "label": "Open link" },
    { "id": "set", "source": "web", "target": "auth", "label": "New password" }
  ],
  "scenarios": [
    {
      "id": "reset",
      "name": "Reset a password",
      "steps": [
        { "id": "s1", "title": "Overview", "description": "The user, the reset page, the auth service and the email provider." },
        { "id": "s2", "title": "Request", "description": "The user asks for a reset.", "highlightNodes": ["user", "auth"], "highlightEdges": ["ask"] },
        { "id": "s3", "title": "Send", "description": "A single-use link goes out by email.", "highlightNodes": ["auth", "mail", "user"], "highlightEdges": ["send", "deliver"] },
        { "id": "s4", "title": "Reset", "description": "The link opens a page that sets the new password.", "highlightNodes": ["user", "web", "auth"], "highlightEdges": ["open", "set"] }
      ]
    }
  ]
}
```

## Smallest valid answer page

```json
{
  "kind": "page",
  "meta": { "title": "Queue or direct call?", "question": "Should checkout call the email service directly?", "kicker": "Decision" },
  "answer": {
    "headline": "Put a queue between checkout and email: a slow email provider must never block a payment.",
    "points": ["Checkout stays fast when email is slow.", "Failed sends retry on their own.", "Adds one component to run."]
  },
  "blocks": [
    { "type": "compare", "title": "Options", "options": [
      { "name": "Queue", "pros": ["Isolates failures", "Retries"], "cons": ["One more service"], "recommended": true },
      { "name": "Direct call", "pros": ["Simplest"], "cons": ["Email outages fail checkout"] }
    ] },
    { "type": "callout", "tone": "warn", "body": "Send the order email only after the payment is confirmed." }
  ]
}
```
