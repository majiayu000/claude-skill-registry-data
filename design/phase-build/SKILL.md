---
name: phase-build
description: Build one release phase against the specs — plan it on an interactive board (endpoints, components, resources, with what already exists read from the codebase), let the user adjust, then build node by node while the board shows live progress. Use when the user wants to build a phase, implement the phase-1 slice, execute the plan from a story map or spec, or watch a build happen visually.
---

One release phase, built in three passes — API, then UI, then infrastructure — against a plan the
user saw and adjusted first. The board shows three trees (Endpoints · Components · Resources), each
node coloured by what it is: **new** this phase, **changed** (exists, this phase extends it), or
**already built**. Press Start, and the same board becomes the progress view — nodes pulse while
being built and fill in as they land.

```
story map slice + specs + phase screens ──► plan JSON ──► board ──► user adjusts ──► Start
                                                                                         │
        done ◄── infra ◄── ui ◄── api  — one node at a time, each reported to the board ◄┘
```

**`have` is read from the codebase, never from a previous plan.** A plan that colours from last
phase's intentions lies the first time a phase ships partial. Read the actual routes, components,
migrations and infra files; stamp when you read them.

## 1 · Scope the phase

- **Pipeline mode**: phase N is `phase` in `.vstack/pipeline.json`. Its content is the phase-N slice
  of `specs/story-map.json`, the specs in `artifacts.specs[]`, and `design/phase-<n>/` if phase
  wireframes exist. If `"specsOnly": true`, this stage doesn't apply — say so and offer
  `/vstack:start` to add development setup.
- **Standalone**: whatever the user points at — a spec, a story list, "build this". Ask only what
  you can't infer.

## 2 · Read the codebase, then draft the plan

Walk the actual code: API routes and handlers, frontend components/pages, migrations, infra and
deploy files. Then write `.vstack/build/phase-<n>.json`:

```json
{
  "phase": 1,
  "readAt": "2026-07-29 14:05",
  "subjects": {
    "api":   { "mono": true, "root": { "id": "api", "kind": "API", "text": "/v1", "state": "have", "children": [] } },
    "ui":    { "root": { "id": "ui", "kind": "Frontend", "text": "<app>", "state": "have", "children": [] } },
    "infra": { "root": { "id": "in", "kind": "Infra", "text": "<envs>", "state": "have", "children": [] } }
  }
}
```

Node: `{ id, kind, text, state, note?, children[] }` — `state` is `new` | `touch` | `have`; `note`
is the short "what changes" tag on a `touch` node. Ids must be stable and unique across all three
subjects — `patch` finds nodes by id alone. Keep nodes at the granularity you'd build them:
an endpoint, a component, a migration, a queue.

## 3 · Serve the board, let the user adjust

```bash
SKILL=<this skill dir>
LIB="$SKILL/../../lib"
DOC=.vstack/build/phase-<n>.json
node "$LIB/json-bridge.mjs" serve --json "$DOC" --template "$SKILL/assets/build-board.html" --tool phase-build \
  --port 7792 --idle-timeout 0
```

`--idle-timeout 0` because the link must survive the whole build. Start with
**`run_in_background: true`**, hand over the printed URL, then arm the seq waiter:

```bash
node "$LIB/json-bridge.mjs" watch --json .vstack/build/phase-<n>.json --stream --tool phase-build \
  --seq <seq printed when the server started>
```

Start it with the **Monitor tool, `persistent: true`**. How the loop behaves — it never exits, one
event per line, the Linked/Unlinked states, the idle close — is
[`contracts/bridge-loop.md`](../../contracts/bridge-loop.md).

On `SENT`, read the JSON. A plain save is a **plan adjustment** — take it as the new plan and carry on.
A save carrying `"action": "start"` is the user pressing **Start**: remove the `action` key, write
the file back, and begin the build. This is the cheapest moment the user will ever have to move an
endpoint or collapse two components — never start building before they've had it.

## 4 · Build, reporting as you go

Subjects in order **api → ui → infra**; inside a subject, parents before children. Per node whose
`state` isn't `have`:

```bash
node "$LIB/json-bridge.mjs" patch --json "$DOC" --id e4 --set status=building --tool phase-build
# … do the work …
node "$LIB/json-bridge.mjs" patch --json "$DOC" --id e4 --set status=done --tool phase-build
```

- The board updates over SSE on every patch — that's the live build view; keep the reports honest
  and per-node, not batched at the end.
- **Follow the project's own conventions** — the template's `CLAUDE.md` contracts if it's
  template-derived, otherwise whatever the codebase already does. Run the project's own checks
  (tests, lint, typecheck) where they exist, per node or per subject as cost allows.
- A node that fails gets `--set status=failed --set note="why, in a few words"` and you **keep
  going** — a failed node is reported, not silently retried, and never silently skipped.
- Adjustments can still arrive mid-build (the waiter is armed): fold them in before starting the
  next node.

## 5 · Finish

Summarize in chat: what was built, what changed, what failed and why. Stop the bridge (TaskStop).
Leave every node's final `status` in the JSON — it's the build record.

## Notes

- **Never edit `assets/build-board.html` or `lib/json-bridge.mjs`** to fit a project — they're the
  engine; only the plan JSON is yours. The shell chrome is stamped in from `lib/shell/` — see
  `lib/shell/README.md`.
- The bridge binds `127.0.0.1`. Port busy → another board is up; pass `--port`.
- **Works beside any other tooling, in any codebase.** This skill scaffolds nothing, installs
  nothing, adds no hooks or config, and touches only the files its plan nodes call for. It never
  creates vstack or template structure in a project that doesn't have it, and never touches another
  tool's state (`.specify/`, etc.).

## State & handoff

**No `.vstack/pipeline.json`?** You're standalone — everything above still applies, minus this
section. The plan JSON can live wherever the user likes (default `.vstack/build/`).

- **Read** `phase`, `specs/story-map.json`, `artifacts.specs[]`, `design/phase-<n>/`.
- **Write** — **this skill owns the phase counter.** On completing phase N: `phase: N + 1`, or
  `stage: "done"` if N was the last phase in the story map; either way `stage: "phase-build"` in
  history with a note (`"phase 1: 9 built, 1 failed"`). No other stage touches `phase`.
- **Next** — the loop: the next phase starts back at `/vstack:phase-preview` (or straight here if
  phase screens already exist for it). After the last phase, the chain is done — say so plainly.
