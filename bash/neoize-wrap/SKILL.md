---
name: neoize-wrap
description: End-of-session capture. Decide what this session learned, route each fact to its one home (a lesson in the graph, where an always-on rule is a scope:always lesson materialised into the rules file, the changelog, or agent memory), author and load the new lessons, and reconcile any that went stale. Use at the end of a working session, or when asked to "wrap", "write up what we learned", or "capture this before I close".
when_to_use: The user is ending a session and wants the knowledge captured, or asks to wrap, record lessons, or save what was learned. Run it after the work is done and verified, not mid-task.
---

# neoize-wrap

You are capturing what this session learned so the next session starts ahead of it. The one rule that
governs everything here: **each fact lives in exactly one home.** A fact written in two places drifts,
and the stale copy gets cited with confidence. So routing is the whole job, and the graph is only one of
the homes.

Run this after the work is done and verified. Capturing an unverified claim as a lesson launders a guess
into the record, so only write down what you actually confirmed, and say what you did not.

A lesson has one more routing axis than its theme: which **space** it belongs to. Two spaces exist; a
lesson lives in exactly one.

- **shared** - knowledge that holds for ALL work with Claude on this machine, independent of any one
  codebase: how you run git, the PR flow, verification discipline, how articles are written, how agents
  are orchestrated. It is read by every session on top of its own project, so it is the baseline. Its home
  is the universal store under `neoize shared dir`, at `~/.neoize/shared/lessons`, loaded into product=shared.
- **project** - anything that names this product's code, tools, domain or infra. Its home is
  `.neoize/lessons/`, loaded into this project's product.

The bar for shared is HIGH: a wrong shared lesson pollutes every future session, so when a fact is even
slightly tied to this product, keep it in the project. Default to project. A lesson already in the project
that turns out to be universal is moved up with `promote` (the `/neoize:promote` skill), never copied, so
it never lives in both and shows up twice in the union read.

## Driving neoize: call the tools, not a shell path

Every neoize operation runs as a **plugin MCP tool**, so drive it by calling the tool, with nothing on
PATH and no script for the human to run. The `neoize ...` commands named below are the exact CLI the
tools wrap, kept as an optional terminal fallback. The map:

- `graph_status` / `graph_up` / `graph_down`: is the graph up, start it, stop it.
- `load_lessons`: load the authored lessons (`neoize load-lessons`).
- `load_graph`: load the structural .cypher (`neoize load-graph`).
- `rebuild_structure`: regenerate the structure from the code (runs `.neoize/collect.py`).
- `check_lessons` / `check_graph`: the offline validations (`neoize check` / `neoize check-graph`).
- `load_shared`: load the universal store into product=shared (`neoize shared load`).
- `apply`: end of work, apply structure, symbols, lessons and shared to the graph in one pass (`neoize apply`).
- `promote_lessons`: move a project lesson up into the shared space (`neoize promote`).
- `read_neo4j_cypher` / `get_neo4j_schema`: query the graph and read its shape. A read scopes to the
  shared+project union with `WHERE n.product IN $products` (pre-bound); the tool refuses a
  Lesson/Topic/Operation read that is not scoped.

## Step 1 - read the project's routing config

The non-graph homes are project-specific, so read `.neoize/wrap.md` for where the changelog and the
agent-memory location live. If it is absent, scaffold it from
`${CLAUDE_PLUGIN_ROOT}/templates/wrap.template.md`, ask the user to confirm the targets, and proceed.
The always-on rules file is no longer a hand-authored home: it is where `neoize apply` writes the
generated `scope: always` block, at the path in project.json `rules_file` (default `CLAUDE.md`). Never
guess a store's path into a write.

## Step 2 - enumerate what was learned, then route each fact

List the candidate facts from this session before writing any of them. Everything the graph holds is a
Lesson, placed by two independent choices: its SPACE (shared or project, which is its reach across
products) and its `scope` (always or situational, which is how it is retrieved). Route each fact to its
ONE home:

- **An always-applies discipline** (a rule or convention that must be in view every session, not tied to
  one piece of code: git flow, PR discipline, verification, writing voice, orchestration) -> a **Lesson
  with `scope: always`**. Author it once as a lesson; `neoize apply` materialises it into the rules file
  block, so you do not hand-write it into `CLAUDE.md`. Put it in the **shared** space when it holds for
  every codebase, the **project** space when it is about this product.
- **A situational note anchored to specific code** (a symbol, a subsystem, a file, a domain entity) -> a
  **Lesson with `scope: situational`**, anchored to that node (or a Topic). It surfaces only when you touch
  what it concerns. Shared when the practice is universal, project when it names your code.
- **A trap at a decision point** (bites when you push, release, migrate, close a ticket) -> a **Lesson
  anchored to an Operation**, plus a row in `.neoize/triggers.json` so the hook surfaces it when that
  operation fires. Use `scope: always` when it must always be in view, `scope: situational` when the
  trigger is enough. Shared for a universal push rule, project for THIS product's release.
- **History** (what shipped, when, in which PR) -> the changelog named in `wrap.md`. Not the graph.
- **Session state** (what to pick up next, what is still unverified, open threads) -> agent memory.

Report the routing (fact -> home; for a lesson, its space and its scope) before writing. A fact you
cannot place is one to raise with the user, not to file twice. Hold a high bar for the shared space and
for `scope: always`; when in doubt, file it project and situational.

## Step 3 - author the new lessons

For each fact routed to the graph, write it into its space's store: a project lesson into
`.neoize/lessons/<theme>.json`, a universal one into `$(neoize shared dir)/lessons/<theme>.json`, which is
`~/.neoize/shared/lessons/<theme>.json`. Both follow
`${CLAUDE_PLUGIN_ROOT}/templates/lesson.schema.json`: a stable `id`, the one-line `title`, a `body` that
carries the trap, the mechanism and the fix (plus the worked example and date if there is one), the
`kind`/`scope`/`confidence`/`status`, at least one `anchor`, and `provenance.date` as an absolute date.
Set `confidence: measured` only for a fact you demonstrated with a control; otherwise `observed` or
`inferred`, honestly. Validate as you go with `neoize check .neoize/lessons` (and
`neoize check "$(neoize shared dir)/lessons"` if you wrote a shared one).

## Step 4 - reconcile what went stale

A fix made this session may have falsified an existing lesson. A lesson stating a now-fixed mechanism in
the present tense reads as current and gets cited, so reconcile it rather than leaving it:

- Pull candidates that name what you changed (scoped to the union you read):
  `MATCH (l:Lesson) WHERE l.product IN $products AND l.body CONTAINS '<ticket-or-symbol>' RETURN l.product, l.id, l.title, l.prov_date`.
- Read each (the citation is only an upper bound, this is a judgement). Correct it with a new lesson
  carrying `supersedes: ["<old-id>"]`, mark it `status: historical` if it is worth keeping as a
  postmortem, or `status: retired` to tombstone it. A lesson citing the change as the ORIGIN of current
  behaviour is fine and stays.

Never auto-retire on the citation alone, and carry the denominator (how many cited, how many actually
reconciled).

## Step 5 - apply everything to the graph (saving the JSON is not the end)

Authoring a lesson writes a JSON file; it is not in the graph until it is loaded, and a lesson that is
only on disk is not retrievable. End the session by applying the whole of what you wrote, in one pass:

- Run `apply` (`neoize apply`). It regenerates and loads the structural layer, runs the project's
  symbol-layer refresh if it has one, loads this project's lessons, loads the shared layer, then
  regenerates the `scope: always` block in the rules file. Both lesson layers are pruned against their
  store, so a retired or moved lesson leaves the graph too, not only the new ones land. It is the one
  action that takes everything you saved this session, structure and symbols and project and shared
  lessons, into the live graph together, in the right order so the anchors resolve.
- If a session authored its first `scope: always` lesson and the rules file has no block yet, `apply`
  points that out rather than editing the file unasked. Run `neoize always-on --write` once to add the
  block, and every later `apply` keeps it current.
- Read the resolved-anchor denominator `apply` prints from the lesson load: an anchor that did not resolve
  is reported by name, so fix the id, never leave a lesson anchored to nothing. If `apply` stops on a step,
  fix that step rather than loading the rest by hand.
- If you only authored lessons and touched no code or symbols, `apply` still does the right thing (it skips
  the structure and symbol steps), so it is always the safe end-of-work action. For the individual pieces
  (just reload lessons, just rebuild structure) defer to the `neoize-refresh` routine.

## Step 6 - keep one home per fact

When you authored a `scope: always` lesson and the same rule was also sitting hand-written in the rules
file or in a scratch note, delete the hand-written copy. The generated block is now the one home for an
always-on rule, so a hand-written duplicate is just the project's next stale note waiting to happen. Grep
for an older copy of anything you just wrote and collapse it to one.

## Finish

Report: the routing table (fact -> home), the lessons authored and loaded with the resolved-anchor
denominator, anything reconciled with the reason, and what you deferred or could not verify. A bare
"wrapped" is not a report; show the counts.
