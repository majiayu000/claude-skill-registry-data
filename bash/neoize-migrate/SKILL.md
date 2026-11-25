---
name: neoize-migrate
description: Migrate a project's existing written knowledge (a large CLAUDE.md, docs, a notes directory, agent memory) into neoize lessons anchored to topics and operations. Use after neoize-init, when there is a body of hard-won knowledge to move into the graph.
when_to_use: The user has an existing CLAUDE.md or docs full of gotchas and conventions and wants them in the graph, or asks to "migrate the docs", "import our notes", or "turn the CLAUDE.md into lessons".
---

# neoize-migrate

You are moving a project's existing prose knowledge into the graph as authored lessons. The goal is
retrieval by relevance: a maintainer pulls the lessons that touch what they are editing instead of
scrolling one enormous file. Precede this with `neoize-init` so `.neoize/` and the graph exist.

The failure mode to avoid is a migration that produces TWO copies of every fact, the prose and the
lesson, which then drift. So migration ends with the source prose replaced by a short pointer, not left
as a second home for the same fact.

`neoize-init` already set this project's product. Every lesson the loader writes is stamped with it
automatically, so you never put a product into a lesson; these migrated lessons land only in this
product's graph even when the server is shared with others. Most of a project's own docs are exactly that:
project knowledge. But a doc you are migrating may hold a UNIVERSAL rule (how you run git, how a PR is
opened, the writing voice) that is true for every project. Route that one to the **shared** layer, not
here: author it under `~/.neoize/shared/lessons` (or migrate it into the project and `/neoize:promote` it
up). The bar for shared is high, so when a rule is even slightly tied to this product, keep it in the
project.

## Driving neoize: call the tools, not a shell path

Every neoize operation runs as a **plugin MCP tool**, so drive it by calling the tool, with nothing on
PATH and no script for the human to run. The `neoize ...` commands named below are the exact CLI the
tools wrap, kept as an optional terminal fallback. The map:

- `graph_status` / `graph_up` / `graph_down`: is the graph up, start it, stop it.
- `load_lessons`: load the authored lessons (`neoize load-lessons`).
- `load_graph`: load the structural .cypher (`neoize load-graph`).
- `rebuild_structure`: regenerate the structure from the code (runs `.neoize/collect.py`).
- `check_lessons` / `check_graph`: the offline validations (`neoize check` / `neoize check-graph`).
- `read_neo4j_cypher` / `get_neo4j_schema`: query the graph and read its shape.

## Step 1 - inventory the source

Ask the user which files are the knowledge to migrate (commonly `CLAUDE.md`, a `docs/` or `*-toolbox/`
tree, an agent memory directory). Read them. Classify each unit of knowledge into one of:

- **Universal rule or convention** - always applies. This STAYS in `CLAUDE.md` as prose, it is not a
  lesson. Loading it on demand would be wrong, it has to be always-on.
- **Situational gotcha or technical note** anchored to specific code - a symbol, a subsystem, a file,
  a protocol. This becomes a **Lesson anchored to a Topic** (or a structural node, if neoize-init built
  the structural layer).
- **Behavioural trap at a decision point** - a thing that bites when you push, release, close a ticket,
  run a migration. This becomes a **Lesson anchored to an Operation**, plus a row in
  `.neoize/triggers.json` so the hook surfaces it when that operation fires.
- **History** - what shipped when, in which PR. This does NOT belong in the graph. Leave it in a
  changelog or implementation log.

Report the inventory with counts per bucket before writing anything.

## Step 2 - author the lessons

Group lessons into `.neoize/lessons/<theme>.json` files, one file per topic area. Each lesson follows
`${CLAUDE_PLUGIN_ROOT}/templates/lesson.schema.json`:

- `id` - stable kebab-case, because the loader MERGEs on it.
- `title` - the one-line claim.
- `body` - the trap, the mechanism and the fix, enough to act on without re-reading the code. Keep the
  worked example and the date if the source had them; a lesson with its provenance is auditable later.
- `kind` / `scope` / `confidence` / `status` - per the schema.
- `anchors` - at least one. A `Topic` and, where the structural layer exists, the structural node the
  note is really about. For a decision-point trap, an `Operation`.
- `provenance.date` - the date the knowledge was learned, absolute. Convert any relative date.

Validate locally as you go with `neoize check .neoize/lessons`, which flags missing fields, duplicate
ids and dangling supersedes without touching the graph.

## Step 3 - load and prove

Run `neoize load-lessons .neoize/lessons`. Read the denominator: lessons loaded, and anchors resolved
out of anchors checked. An anchor that did not resolve is reported by name; it means a structural node
id is wrong or that node was never extracted. Fix the id, do not leave a lesson anchored to nothing.

Then pull a few lessons back through the MCP server by topic and by operation and confirm the bodies
read correctly. Carry the count.

## Step 4 - replace the prose with a pointer (the first modifying step - CONFIRM FIRST)

Everything up to here was ADDITIVE and reversible: you authored new lesson files under `.neoize/` and
loaded them, and touched none of the user's existing files. This step is the first that MODIFIES the
source. So before editing anything, show the user the planned changes as a list (which prose block in
which file becomes which pointer) and get an explicit confirmation. Do not edit a source file until they
say go. If they decline, stop and leave the authored lessons in place; nothing is lost.

For every block of prose that became a lesson, replace it in the source file with a one-line pointer to
its topic and the query to pull it, the way a migrated section should read:
"X now lives in the graph under Topic `x`; pull it with `MATCH (l:Lesson)-[:ANCHORS_TO]->(:Topic {id:'x'}) RETURN l.title, l.body`."
Leave universal rules as prose. Do NOT leave the full note in both places. Two correct copies is how the
source file acquires its next stale note, because the stale one gets cited with confidence.

## Step 5 - reconcile the project's agent-facing processes (propose, then CONFIRM)

Moving the lessons and the structure is only half of it. A project carries agent-facing PROCESSES that
assume the old world, and a migration that leaves them untouched points the next agent back at what you
just retired. So inventory them and propose an update for each, the same confirm-before-modify discipline
as Step 4: present the proposed edits as a list and apply none until the user approves. This is a
proposal step, never an auto-rewrite of the user's processes.

Inventory the project's slash commands, skills, subagents, hooks and agent instruction files (commonly
`.claude/commands/`, `.claude/skills/`, `.claude/agents/`, `.claude/hooks/`, `CLAUDE.md`, `AGENTS.md`,
`.github/copilot-instructions.md`, a `GEMINI.md`). Read each and classify it against the graph world:

- **A process that tells the agent to grep or read the code for a product fact** should query the graph
  FIRST (the `read_neo4j_cypher` tool, or the saved `.neoize/queries/`), and reach for the code only once
  the graph has come up short. Propose that reordering.
- **A process that names a retired bespoke tool** (an old graph CLI, an old lessons path, an old container
  or MCP tool name) should point at the neoize equivalent: the control tools (`graph_up`, `load_lessons`,
  `load_graph`, `rebuild_structure`, ...), the `.neoize/` paths, and the plugin's MCP server tool names.
  Propose the exact rename or path change.
- **A process that captures end-of-session knowledge** (a wrap or hand-off routine) should route its
  knowledge through `/neoize:wrap`, so a learned fact lands in its one home rather than being pasted back
  into an always-on file. Propose that it call wrap.
- **A reflex or reminder that fired through a now-retired hook** should move to `.neoize/triggers.json`
  plus a lesson anchored to the matching `Operation`, so the neoize hook surfaces it. Propose the trigger
  row and the lesson.

Present the full set of proposed edits (file, the line or block, the change, and why) and apply only the
ones the user approves. Leave a process alone when it does not touch the graph world at all.

## Finish

Report: counts per bucket, lessons authored and loaded with the resolved-anchor denominator, which
source blocks you turned into pointers, which agent-facing processes you proposed to update and which the
user approved, and what you deliberately left as prose (the universal rules) and as history (the
changelog). Name anything you could not classify and left for the user to decide.
