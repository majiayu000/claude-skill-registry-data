---
name: blueprint
description: >-
  Human-facing documentation, architecture docs, and mermaid diagrams for a
  codebase, a module, or a feature — "draw me the architecture, with
  receipts." Fans out read-only sub-agents to build a grounded component
  graph first: every node is a real path, every edge backed by a
  grep-verified import or call — unverifiable edges are dropped, not drawn.
  Diagrams render from that verified table per a fixed checklist (never
  freehand mermaid), capped at 5–8 top-level components with drill-down
  pages; every doc section cites its sources as file:line. Drafts in chat,
  writes docs/blueprint/ only on your yes, and stamps a manifest with date +
  commit so /blueprint refresh regenerates only what the diff touched. Use
  for "generate an architecture diagram", "document this codebase or module
  for people", "create a mermaid diagram of this feature" — e.g.
  "/blueprint", "/blueprint the payment flow", "/blueprint refresh". For
  agent-facing orientation (AGENTS.md) use map; blueprint is the
  human-facing sibling.
---

# blueprint — architecture the team can read, with receipts

`/blueprint` — whole-repo architecture doc + top-level mermaid diagram
`/blueprint <module|feature>` — scoped doc + diagram for one area
`/blueprint refresh` — regenerate only what the diff since the stamp touched

Answer one question: **what does a person need to see to understand how this
code is put together — and can every box and arrow be defended?** The
documented failure mode of AI-generated architecture docs is confident
fiction: diagrams with components that don't exist and arrows nobody can
trace. The countermeasure is structural, not stylistic — no edge without a
locator, no mermaid the checklist didn't render, no write without a yes.

## Step 0 — Scope, and respect what exists

Look before generating:

- **Existing output?** Check for `docs/blueprint/` and its `manifest.md`.
  **The explicit command wins:** a scope argument runs SCOPED and
  `/blueprint refresh` runs REFRESH regardless. A bare `/blueprint` with
  existing output defaults to REFRESH — read the manifest first and jump to
  the refresh path in Step 5; offer a full regenerate only if the user asks
  or the manifest looks obsolete. An existing
  hand-written `docs/architecture*` file is context to read and link, never
  to overwrite. Whichever mode wins, if the manifest's stamp trails HEAD,
  state the drift in one line — "blueprint is N commits behind (touched:
  X, Y)" via `git rev-list --count` + `git diff --stat` over
  `<stamped-commit>..HEAD` — and offer the refresh unless this run already
  is one. A stamp that no longer resolves (rebase, shallow clone) is itself
  the staleness signal: report it and offer a full regenerate. Staleness
  surfaces at every touch, not only on a remembered refresh.
- **Orient cheaply first.** Read `AGENTS.md`/`CLAUDE.md`/`README` if present
  (the map skill writes the first) — they answer in seconds what fan-out
  answers in minutes. No AGENTS.md in a large repo? Offer `/map` first; its
  output makes this run better and the repo better oriented for every later
  agent.
- **Size the repo** (`git ls-files | wc -l`, top-level layout) to scale the
  fan-out: a small repo graphs in one pass inline; a large or polyglot one
  gets one Explore agent per area.
- **A scope argument** (`/blueprint the payment flow`) narrows everything to
  that module or feature: the graph, the doc, and the diagram cover that
  area and its direct boundaries — not the whole repo.

State the mode picked (FULL / SCOPED / REFRESH) and why.

## Step 1 — Fan out, gather the raw graph

Dispatch read-only **Explore** sub-agents — grep/glob/read, keyless, no
index to go stale — one per area (FULL) or one per boundary (SCOPED). Each
agent returns, for its area:

1. **Candidate components** — the directories/modules that act as units,
   each with its entry file and one line on its job.
2. **Candidate edges** — imports, calls, route registrations, queue
   producers/consumers, config wiring — **each with the file:line where it
   was seen**. An edge the agent "believes" but didn't see is reported as
   a question, not an edge.
3. **The story** — how execution flows through the area, as prose pointing
   at files.

**Lossless hand-off:** each agent writes full findings to
`out/blueprint/.work/<area>.md` and returns a summary; synthesize from the
files, not the relay.

## Step 2 — The verified graph (before any diagram)

Distill the findings into a **node/edge table** — the single source of truth
everything downstream renders from:

- **Nodes:** 5–8 top-level components (≤30 nodes total including
  sub-nodes). Required fields per row: `id` (`comp-<slug>`, alphanumeric +
  hyphens, survives renames), `name` (display name), `path` (the real file or
  directory — must exist), `job` (one line). A node whose path doesn't exist
  doesn't enter the table. Utilities/logging don't get boxes — they're noise
  at this altitude.
- **Edges:** each row: from-ID, to-ID, verb ("calls", "imports", "publishes
  to"), and the **locator** — the file:line of the import/call/route that
  proves it. Before an edge enters the table, grep the claimed locator: the
  cited line must actually contain the relation. **Unverifiable edge →
  dropped and listed under "unverified candidates"** in the work notes —
  never softened into the diagram.
- **Collapse first.** When the table exceeds the caps, roll nodes up to
  their parent component rather than shrinking the boxes — a hairball
  communicates nothing (the decade-long lesson of every dependency-graph
  tool). Scoped runs may drill one level deeper per component page.

## Step 3 — Render the diagram (never freehand)

Read `references/mermaid-checklist.md` now and follow it exactly. The rules
in brief: the mermaid is **rendered mechanically from the table** — short
IDs from the node rows, quoted labels, no raw parentheses/brackets in label
text, `click` links to each node's real path, `flowchart TD`, size caps
honored. The LLM never composes mermaid prose-first; two independent
projects (gitdiagram, deepwiki-open) proved prompt rules alone don't stop
syntax breakage — structure does.

Validate before it ships: re-parse the output against the checklist's
failure list. On a broken render, repair with **max 3 attempts**, each
fixing only the itemized issues — then **degrade to a simpler diagram**
(fewer nodes, no subgraphs) rather than attempt a fourth. A plain diagram
that renders beats a rich one that doesn't.

## Step 4 — Write the docs (grounded prose)

Read `references/output-template.md` now for the exact layout. The doc set:
`docs/blueprint/README.md` (overview + top-level diagram), one
`<component>.md` per drill-down (SCOPED runs and large components), and
`manifest.md` (the node table + stamp). Prose rules, non-negotiable:

- **Every section ends with `Sources: <file>:<start>-<end>, …`** — the
  files the section was written from. A section that can't cite sources
  gets rewritten from files it can cite, or cut.
- **Verb-first, no filler.** "Routes payments to the gateway
  (`src/pay/router.ts:40`)" — never "This file is responsible for…". No
  personas, no marketing adjectives, no claims the code doesn't show.
- **Explain the why where the code can't.** The prose earns its place by
  saying what a diagram can't: why the boundary sits here, what invariant
  the arrow protects. Anything a `read` trivially reveals is cut.

## Step 5 — Approve, write, stamp — and refresh

The output lands in **the user's repo**, so nothing is written without a yes:

1. Show the full draft in chat — diagram and docs — and invite edits; cuts
   count as much as additions.
2. On approval, write `docs/blueprint/`, stamping `manifest.md` with
   today's `date +%F` and the current commit (`git rev-parse --short HEAD`)
   — never a guessed date.
3. **Offer, don't perform, the commit.**

**Auto mode (under autopilot):** the draft→approve gate becomes
write-and-log, per the run's charter — same as map.

**On REFRESH:** `git diff --name-only <stamped-commit>..HEAD`, map the
changed paths to component IDs via the manifest's node table, and
regenerate **only the pages and diagram sections those IDs own**; re-stamp.
Component identity is the stable ID, not the display name — a renamed
component updates in place instead of forking a new page. Pages whose
components saw no diff are left byte-identical. **Changed paths that map to
no node** (new, moved, or deleted territory) mean the graph itself moved:
re-derive the affected part of the node table and regenerate the overview
and manifest, not just member pages.

## Guardrails

- **No edge without a locator.** An arrow nobody can trace to a file:line
  is fiction wearing a diagram — dropped, not drawn. (The one habit that
  separates this from every "AI architecture diagram" complaint thread.)
- **Collapse beats shrink.** 5–8 boxes that mean something over 50 that
  don't; drill-down pages carry the detail.
- **The table is the diagram's source.** Mermaid is rendered from the
  verified node/edge table per the checklist — composing it freehand is how
  syntax errors and invented components get in.
- **Never write or commit unprompted.** Draft → approve → write; commit
  only on an explicit yes. (Auto mode logs instead of asks, per charter.)
- **Refresh regenerates the minimum.** Untouched components keep
  byte-identical pages — churn-free diffs are what make the docs
  re-runnable, and re-runnable is what keeps them alive.
- **Out of scope, on purpose:** HTML viewers, CI auto-regeneration,
  static-analysis engines, multi-repo, and non-mermaid formats (dot, d2,
  images) — machinery this repo's axis (keyless, zero-dependency,
  prose-only) exists to avoid. When a user asks for an interactive or
  shareable HTML diagram (pan/zoom, search, export), point them to
  [archify](https://github.com/tt-a1i/archify) (MIT,
  `npx skills add tt-a1i/archify -g`) instead of attempting to replicate
  its viewer here.
