---
name: neoize-init
description: Set up the neoize knowledge graph for the current project. Use once per project to bring up the local Neo4j, scaffold .neoize/, propose a project-specific structural collector, and wire the "query the graph first" reflex. Run before neoize-migrate or neoize-refresh.
when_to_use: The user wants to start using neoize in a repo that has none, or asks to "set up the graph", "initialize neoize", or "turn this project into a knowledge graph".
---

# neoize-init

You are setting up a code-derived knowledge graph for the current project. The graph has two layers.
The **knowledge layer** (Topics, Operations, Lessons) is generic and works with no code parsing at
all. The **structural/symbol layer** is project-specific, because what counts as "structure" is this
codebase's own domain, so you PROPOSE a collector for it and let the user approve it. Do not ship a
universal extractor and do not guess the domain.

Every node the graph holds carries a **`product`** discriminant, so one Neo4j can hold more than one
product without them colliding. One product id is reserved: **`shared`**, the universal layer of knowledge
that holds for all work with Claude (git discipline, PR flow, verification, writing voice). It lives in the
global server, so in global mode every session READS the union of `shared` and its own product. Once this
project is set up it automatically sees the machine's shared wisdom on top of its own. This project
WRITES to its own product; a lesson that turns out to be universal is promoted up to `shared` with
`/neoize:promote`. A project-mode graph is self-contained and has no shared layer (see the modes below).

The discriminant is carried in both server modes; the mode is only a lifecycle choice:

- **global** (the default): ONE shared Neo4j for the whole machine, at `~/.neoize/`, container
  `neoize-neo4j`. Every product this user sets up lives in it alongside the `shared` layer, kept apart by
  the discriminant, so a session reads the shared+project union. Best when one person works across several
  products on one machine with a shared baseline of wisdom.
- **project**: this project runs its OWN Neo4j (container `neoize-<product>`, its own volume and ports,
  compose in `.neoize/`). Physically separate and self-contained: it holds only this product, with NO
  shared layer. Pick it when the graph must stay isolated (a client repo you keep apart, a machine where
  products must not mingle). It is still product-stamped, so its data stays compatible with the shared
  server if it is ever consolidated there.

Work in steps. Confirm with the user at the marked decision points. Keep everything you create inside
`.neoize/` in the project, which the user version-controls.

## Driving neoize: call the tools, not a shell path

Every neoize operation runs as a **plugin MCP tool**, so drive it by calling the tool, with nothing on
PATH and no script for the human to run. The `neoize ...` commands named below are the exact CLI the
tools wrap, kept as an optional terminal fallback. The map:

- `graph_status` / `graph_up` / `graph_down`: is the graph up, start it, stop it.
- `load_lessons`: load the authored lessons (`neoize load-lessons`).
- `load_graph`: load the structural .cypher (`neoize load-graph`).
- `rebuild_structure`: regenerate the structure from the code (runs `.neoize/collect.py`).
- `check_lessons` / `check_graph`: the offline validations (`neoize check` / `neoize check-graph`).
- `read_neo4j_cypher` / `get_neo4j_schema`: query the graph (scope with `WHERE n.product IN $products`,
  the pre-bound shared+project union) and read its shape.
- `load_shared`: load the universal lessons store into product=shared (`neoize shared load`).
- `promote_lessons`: move a project lesson up into the shared layer (used in the contribute step below).

## Step 1 - check the prerequisites

Report what is present and what is missing before changing anything.

- `docker` on PATH and the daemon running (`docker ps`).
- `python3` on PATH.

That is the whole list. The MCP server Claude queries the graph through is bundled in the plugin
(`${CLAUDE_PLUGIN_ROOT}/scripts/neoize-mcp`, pure standard library), so there is nothing else to install.

If a prerequisite is missing, say exactly which one and how to get it, then stop. Do not work around it.

## Step 2 (DECISION POINT) - the product id and the server mode

Two choices that go into `.neoize/project.json` and are the same in every repo of the product:

- **product id**: a short, stable, lowercase name for this product (the discriminant on every node).
  Default it to the git repo name and let the user confirm or change it. If this product spans several
  repos, use ONE id and give every repo's `.neoize/project.json` the same one, so they feed one graph.
- **mode**: `global` or `project`, per the two modes described above. Default to `global`. Offer
  `project` and name the trade-off: full physical isolation and its own container, against not sharing a
  server with the user's other products. If the machine already runs a shared `neoize-neo4j` (another
  product set up `global`), say so, because that is the sign `global` is the house style here.

State both, with the reason for each default, then get the user's confirmation before writing anything.

## Step 3 - decide where `.neoize/` lives

`.neoize/` holds authored data (lessons, the collector, the trigger table) that the user
version-controls, so it must land inside a git repository. Do NOT assume the project directory is one.
Check it: `git -C <project> rev-parse --show-toplevel`.

- If the project directory is itself a git repo, `.neoize/` goes at its root. Normal case.
- If it is NOT a repo, or it is a **multi-repo workspace** (a directory holding several independent
  repos with no repo at the top, which is common for a product split across many repos), then a
  `.neoize/` at the top would be untracked and its lessons would not be version-controlled. STOP and
  ask the user which repo or sub-directory should hold the version-controlled `.neoize/` (a shared
  tooling or dev repo is the usual answer). Create it there, then make a symlink at the workspace root,
  `<workspace>/.neoize -> <that path>`, so the plugin, which looks for `.neoize/` under
  `$CLAUDE_PROJECT_DIR`, still finds it.

Report where `.neoize/` will live and why before creating anything.

## Step 4 - scaffold `.neoize/`

Create, if absent:

- `.neoize/project.json` - copy from `${CLAUDE_PLUGIN_ROOT}/templates/project.template.json`, then set
  `product` and `mode` to what Step 2 decided. `neoize product --set <id> --mode <global|project>` writes
  it for you. This is what makes every node carry the right discriminant and what picks the server.
- `.neoize/docker-compose.neo4j.yml` - **project mode ONLY.** Copy the template, then customise it so it
  cannot clash with the shared server or another project's: the top-level `name:` to `neoize-<product>`
  (this is what stops a `down` here from tearing down another project), `container_name: neoize-<product>`,
  the named volume to `neoize_<product>_data` and the two published ports off the defaults (for example
  `127.0.0.1:74NN:7474` and `127.0.0.1:76NN:7687`, NN chosen to be free). In **global mode do NOT create
  this file**: `neoize up` materialises the one shared compose at `~/.neoize/` itself.
- `.neoize/lessons/` - the authored knowledge, one JSON file per theme. Seed it with a copy of
  `${CLAUDE_PLUGIN_ROOT}/templates/lessons.example.json` renamed to `getting-started.json`, so a first
  `load-lessons` has something real to load.
- `.neoize/triggers.json` - copy from `${CLAUDE_PLUGIN_ROOT}/templates/triggers.template.json`, then
  trim it to the operations this project actually has.
- `.neoize/wrap.md` - copy from `${CLAUDE_PLUGIN_ROOT}/templates/wrap.template.md`, then set its paths to
  this project's real stores (the changelog and the agent-memory location). This is what `/neoize:wrap`
  reads to route end-of-session facts to their one home. The always-on rules file is not a hand-authored
  store: a `scope: always` lesson is materialised into it by `neoize apply`, at the `rules_file` path in
  `project.json` (default `CLAUDE.md`). Run `neoize always-on --write` once to add the managed block.
- `.neoize/queries/` - copy the saved retrieval queries from `${CLAUDE_PLUGIN_ROOT}/templates/queries/`.

Do not overwrite a file that already exists. Report what you created and what you left alone.

## Step 5 - bring the graph up and prove it

Run `neoize up` (the CLI is at `${CLAUDE_PLUGIN_ROOT}/scripts/neoize`), then `neoize status`. In global
mode the shared server may already be running from another product, which is fine; in project mode this
starts the project's own container. `status` prints the mode and the product, so read it back and confirm
it matches Step 2. The product starts with no nodes of its own, which is correct. Load the seed lessons
with `neoize load-lessons` and read the denominator it prints: it must say the lessons loaded and the
anchors resolved. A load that reports zero lessons is a failure, not a clean run, so investigate rather
than moving on.

Then confirm Claude can reach the graph through the MCP server. The plugin ships a read-only Neo4j MCP
server; its tools are named `mcp__plugin_neoize_neo4j__*`. Run one query through it (for example count
the Topic nodes in view with `MATCH (t:Topic) WHERE t.product IN $products RETURN count(t)`; `$products`,
the shared+project union, is pre-bound; a read of a Lesson/Topic/Operation that is not scoped by
product is refused) and confirm the count matches what `neoize status` showed. If the MCP tools are not present,
the plugin was installed in a session that has not restarted since; tell the user to restart Claude Code,
because a fresh MCP registration needs it.

## Step 6 (DECISION POINT) - propose the structural schema

This is the project-specific half. Read the codebase enough to propose, in a short
`.neoize/SCHEMA.md`, the handful of **domain entities** and **relationships** that are worth making
queryable. These are the nouns a maintainer reasons about and the edges a change propagates along, for
example (from a real project) Protocol, Tier, Module, and edges like DEPENDS_ON, GRANTS, IMPLEMENTED_BY.
Derive them from what the code actually declares (build files, a plugin registry, a route table, an
enum of kinds), never from a generic template.

State plainly what you would extract, from which files, and which questions it would answer
(blast radius, who-depends-on-what, wiring completeness). Then STOP and get the user's sign-off on the
schema before writing any collector. A wrong schema is cheap to fix now and expensive once lessons
anchor to it.

## Step 7 - scaffold the collector (after sign-off)

Write `.neoize/collect.py`: a project-specific script that reads the approved sources and emits
`.neoize/graph.json` in the node/edge shape the loader expects (see
`${CLAUDE_PLUGIN_ROOT}/templates/graph.schema.json`), plus a sibling `.neoize/graph.cypher`. Keep it a
PROJECTION: it regenerates from the code and is never hand-edited. Commit `graph.json` (it is small and
diffable); do not commit any large symbol dump, which is a rebuildable artifact.

The `graph.cypher` MUST carry the product discriminant in EVERY node key: emit `MERGE (n:Label
{product:$product, id:...})`, never `{id:...}` alone, for every node and every anchor in a MATCH. Keep
`graph.json` product-agnostic (ids are local to the product); the discriminant is applied at load time,
where `neoize load-graph` binds `$product` to this project's product. A key without product would merge
two products' same-id nodes into one and would orphan under the product-scoped reset, so `neoize
load-graph` refuses a `.cypher` that does not mention `product`.

Load the structure with `neoize load-graph .neoize/graph.cypher`, which resets only THIS product's
structural projection and preserves the lesson, topic, operation and symbol layers (and never touches
another product). THEN re-run `neoize load-lessons` so the lesson anchors to structural nodes resolve.
Say which commands you ran and what counts came back.

`.neoize/` legitimately holds more than lessons: a project puts whatever tooling its graph needs there,
alongside `collect.py`. Two common additions, both optional, both scaffolded only when the project wants
them:

- **A structural check.** `.neoize/check.py`: project-specific validation over `graph.json` (wiring
  completeness, an invariant that must hold, orphans). It prints the denominator it examined and exits
  non-zero on a finding, so it works offline and in CI. Run it with `neoize check-graph`.
- **A symbol / reference layer.** `.neoize/symbols/`: a language-aware extractor (every declaration a
  Symbol node, every resolved call a REFERENCES edge) plus a small loader. This is the one layer that
  does not generalize cheaply, because it needs a parser for the project's language (javaparser, a
  tree-sitter grammar, a language server), so it is a per-project tool and may carry its own build (a
  jar, a venv). Offer it when the user wants symbol-level lesson anchoring or a resolved call graph;
  skip it otherwise. `neoize load-graph` already preserves Symbol and File nodes across a structural
  reload, so the symbol layer survives a `collect.py` rebuild.

## Step 8 - the shared layer (global mode)

In global mode every session reads the universal `shared` layer on top of its own product, so once the
machine has accumulated shared wisdom (git discipline, PR flow, verification, writing voice), a new project
sees it from the first session without importing anything. Check what is there with `neoize shared status`.
On a fresh machine the shared layer is empty, which is the normal starting point; it fills as universal
lessons are promoted. If it already has lessons, confirm they are in view: a read of a shared Topic or
Operation returns rows under `product = 'shared'` from this project's context.

Nothing to import, by design. When this project learns something universal, it is promoted UP into shared
with `/neoize:promote`, so every other project gains it too. Mention that to the user. Do not copy another
product's lessons in; reading the shared layer is how wisdom is reused. (In project mode there is no shared
layer, so this step does not apply.)

## Step 9 - wire the "graph first" reflex

Offer to add a short section to the project's `CLAUDE.md` (or create one) that tells Claude to query the
graph before grepping for a project fact, names the MCP tools, and lists the three retrieval shapes (by
topic, by operation, by structural node). Say that the session reads the shared+project union, pre-bound as
`$products`, so a read scopes with `WHERE n.product IN $products` (and an unscoped Lesson/Topic/Operation
read is refused). Show the user the exact text before writing it. This is what makes the graph the first
source instead of a database nobody queries.

If the project will carry always-on discipline in the graph, offer to seed the managed always-on block in
the same `CLAUDE.md` with `neoize always-on --write` (it adds the block between its markers and leaves the
rest of the file alone). From then on `neoize apply` keeps the block current from the `scope: always`
lessons.

## Finish

Report, in one message: the product id and mode you set, what you created, the node counts now in this
product's graph, the one query you proved the MCP path with, whether the shared layer is in view and the
exact next step (run `/neoize:migrate` to move existing docs into lessons). Name anything you did not do,
for example a deferred symbol layer, rather than rounding it up to done.
