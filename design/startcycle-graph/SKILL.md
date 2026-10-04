---
name: startcycle-graph
description: Use when running the autonomous multi-agent build pipeline after /bdbrainstorm or /grill-me. Routes to the startcycle-dispatch Dynamic Workflow, which reads production_artifacts/state.json and invokes Architect, TechLead, UI/UX, Engineering, Media/EventTech, Reviewer, and Shipping in turn per .agents/graph.md's edge table — the agents never invoke each other.
category: bdb-core
---

# 🚀 BDB Autonomous Development Cycle (`/startcycle-graph`)

**Step 0 — bootstrap the contract into this project, before calling
`Workflow`.** Every agent the dispatcher spawns is told to read/write
`production_artifacts/state.json` "per `.agents/state.schema.json`" — a path
resolved against the CURRENT PROJECT, not globally. If this project has
never run `/startcycle-graph` before, that file (and `.agents/graph.md`) won't be
here yet, and every agent will freelance the state shape instead of
conforming to the schema (observed for real: a run's `state.json` was
missing `run_id`/`max_iterations`/`gate`/`findings`/`approvals` and had
several fields the schema doesn't define at all). Fix it first:

```bash
mkdir -p .agents
[ -f .agents/graph.md ] || cp "$HOME/.agents/graph.md" .agents/graph.md
[ -f .agents/state.schema.json ] || cp "$HOME/.agents/state.schema.json" .agents/state.schema.json
[ -f .agents/nodes.json ] || cp "$HOME/.agents/nodes.json" .agents/nodes.json
```

`nodes.json` is not optional and is the one that fails loudest: it is the
node registry the dispatcher loads as its very first step, and without it
the run escalates immediately with *"`.agents/nodes.json` failed to load, or
is missing required node id(s)"* — before Architect or any other agent has
run. (Found exactly that way: a first run in a project that had followed
this bootstrap step as it was previously written, which copied only the
other two files.)

If any of the three doesn't exist under `$HOME/.agents/` either, stop and
tell the user: this machine has no canonical copy of the graph contract to
bootstrap from, and `/startcycle-graph` cannot run correctly until one is
installed. Don't silently proceed.
(`.claude/agents/*.md`, the seven agent persona files, do NOT need this
treatment — Claude Code resolves subagents from the user-level
`~/.claude/agents/` fine without a project-local copy.)

**Action — do this, and nothing else:** call the `Workflow` tool with
`scriptPath` pointing at this repo's dispatcher script — resolve `$HOME`
yourself (e.g. `echo $HOME` or your own environment info) rather than
hardcoding a username, giving
`$HOME/.claude/workflows/startcycle-dispatch.mjs` — and `args` set to the
goal text that follows `ARGUMENTS:` below this file's content. Pass the goal
through verbatim, including any `--skill=<name>` flag(s) it contains — the
dispatcher script parses those itself (see below), do not strip or
interpret them yourself. If there is no `ARGUMENTS:` text, pass no `args`
(or `args: undefined`) — the workflow itself asks for a goal in that case
rather than guessing one.

**Injecting a specific skill.** `/startcycle-graph --skill=<name> <goal>`
(repeatable, quote a name with spaces) forces that skill into this run as a
hard requirement for the build nodes, validated to exist before anything
else runs — this is how you make the pipeline use your own private skill
that isn't part of `.agents/nodes.json`'s registry.

`<name>` is the **exact skill directory name**, not a description — `ui-component`,
not "the UI one". Two ways to find it without leaving the terminal:

- `/ask-tim` — the routing skill; start there when you know the *job* but not the name
- list the installed skills directly, if you half-remember the spelling. The installer
  syncs the same set to every harness it detects, so use whichever path is yours:
  `~/.claude/skills`, `~/.agents/skills`, `~/.codex/skills`, `~/.cursor/skills`, or
  `~/.roo/skills`. `ls ~/.agents/skills` is the safest guess on an unknown machine —
  that one is written on every install regardless of harness.

A name that does not resolve halts the run before any agent works, and the
error now lists installed near-misses rather than only saying "not found".
That is deliberate: silently running without a skill you explicitly demanded
is worse than stopping.

See [`.agents/graph.md`](../../../.agents/graph.md)'s "Mandatory Skill
Injection" section for the full mechanics; nothing about it needs handling
in this router file, since `args` is passed through as raw text either way.

Use `scriptPath`, not `name: "startcycle-dispatch"` — by-name lookup for a
custom (non-built-in) workflow script has been observed to fail with
`Workflow "startcycle-dispatch" not found. Available: deep-research`, even
when the script exists at the expected path and is correctly named inside
its own `meta.name`. `scriptPath` pointing directly at the file works
reliably; `name` apparently requires a separate registration step (the
`/workflows` monitor's `s save` action looked like a candidate, but that's
an interactive step a slash command can't trigger on its own, so don't rely
on it).

Then wait for the `Workflow` tool call to finish and report its result
(including `phase`, any `reason`, and — at `ready_to_ship` — the instruction
to reply `GO`) back to the user. Do not summarize or reinterpret it; relay it.

**Do NOT decompose the task, write anything under `production_artifacts/`, or
implement any part of the goal yourself in response to this skill.** This
file exists only to route the `/startcycle-graph` slash command to the real
dispatcher — a Dynamic Workflow script
(`.claude/workflows/startcycle-dispatch.mjs`) that holds the actual
node/edge graph, spawns the seven agents, and drives the repair loop. If you
catch yourself about to write a plan file or code directly because of this
skill, stop — that means the `Workflow` tool call was skipped, which is
exactly the failure this file was rewritten to close (see
`SESSION-HANDOVER-v3.13.md` in the source repo for the incident: an earlier
version of this file embedded the full pipeline description in prose, and
the model followed it "in spirit" inline instead of invoking the script —
silently skipping the whole graph, with no `state.json`, no subagents, no
Reviewer, and no quality gate ever running).

## Live map

When the build phase begins, the dispatcher starts the aos-trail live map
(Trigger B) with the command below; it is safe to run twice, since
`aos-trail` reuses a map already running for this repo:
`aos-trail --ensure`
(it prints a URL, default http://localhost:5330; inside AO, where
`AO_BROWSER_CAPABILITY` is set, also run `ao preview <url>`). Put the live-map link in your reply (the autostart hook also adds it as context when active). Agents follow
the status-mark rules from the `agenttrail` skill: `[~]` before starting,
`[x]` when done, `[!]` when stuck, with `by: <agent>`, saving the plan file
immediately.

## Architecture diagram (Archify, native)

Architect authors `production_artifacts/00_architecture.json` (editable truth)
and delivers `production_artifacts/00_architecture.html` (read-only) via
`aos-archify validate` / `aos-archify deliver` with `--quality showcase --json`
at the Architect→TechLead boundary; only a passing showcase receipt (9/9
checks, 0 errors) sets `state.artifacts.architecture`, and a failed
validate/deliver preserves the previous HTML and escalates instead of
proceeding silently. The plan links the diagram with a
`url: production_artifacts/00_architecture.html` line so the live map opens it
from the card. Review the HTML in plan-canvas alongside the plan:
`aos-plan-canvas open production_artifacts/00_architecture.html`.

## Why this file is a thin router, not a spec

The full contract — state schema, node/edge table, the Stop-hook
loop-keeper, the no-progress guard — lives in
[`.agents/graph.md`](../../../.agents/graph.md) and
[`.agents/state.schema.json`](../../../.agents/state.schema.json). Those are
read by the dispatcher script itself and by the agents it invokes, not
duplicated here — so there is nothing here to follow "in spirit" instead of
actually running.

## If the `Workflow` tool is unavailable

Some harnesses (or Claude Code with Dynamic Workflows toggled off in
`/config`) have no `Workflow` tool at all. Only in that case, fall back to
manually driving `.agents/graph.md`'s node/edge table yourself as the
dispatcher: read `production_artifacts/state.json`, decide the next node
per the edge predicates, invoke exactly that one agent, and repeat. Never
let one agent's output instruct another agent directly — that hand-off
pattern is the thing `.agents/graph.md` (F-17) rules out.
