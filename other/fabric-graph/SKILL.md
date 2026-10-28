---
name: fabric-graph
description: >-
  Use when running the autonomous multi-agent build pipeline after /bdbrainstorm
  or /grill-me, when the user types /fabric-graph or "run a fabric", or
  when a task needs durable state, a review repair loop and an automated
  quality gate. Routes to the fabric-dispatch Dynamic Workflow, which reads
  production_artifacts/state.json and invokes Architect, TechLead, UI/UX,
  Engineering, Media/EventTech, Reviewer, and Shipping in turn per
  .agents/graph.md's edge table — the agents never invoke each other.
category: bdb-core
---

# 🚀 BDB Autonomous Development Cycle (`/fabric-graph`)

**Step 0 — bootstrap the contract into this project, before calling
`Workflow`.** Every agent the dispatcher spawns is told to read/write
`production_artifacts/state.json` "per `.agents/state.schema.json`" — a path
resolved against the CURRENT PROJECT, not globally. If this project has
never run `/fabric-graph` before, that file (and `.agents/graph.md`) won't be
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
bootstrap from, and `/fabric-graph` cannot run correctly until one is
installed. Don't silently proceed.
(`.claude/agents/*.md`, the seven agent persona files, do NOT need this
treatment — Claude Code resolves subagents from the user-level
`~/.claude/agents/` fine without a project-local copy.)

**Action — do this, and nothing else:** call the `Workflow` tool with
`scriptPath` pointing at this repo's dispatcher script — resolve `$HOME`
yourself (e.g. `echo $HOME` or your own environment info) rather than
hardcoding a username, giving
`$HOME/.claude/workflows/fabric-dispatch.mjs` — and `args` set to the
goal text that follows `ARGUMENTS:` below this file's content. Pass the goal
through verbatim, including any `--skill=<name>` flag(s) it contains — the
dispatcher script parses those itself (see below), do not strip or
interpret them yourself. If there is no `ARGUMENTS:` text, pass no `args`
(or `args: undefined`) — the workflow itself asks for a goal in that case
rather than guessing one.

**Injecting a specific skill.** `/fabric-graph --skill=<name> <goal>`
(repeatable, quote a name with spaces) forces that skill into this run as a
hard requirement for the build nodes, validated to exist before anything
else runs — this is how you make the pipeline use your own private skill
that isn't part of `.agents/nodes.json`'s registry.

`<name>` is the **exact skill directory name**, not a description — `senior-frontend`,
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

Use `scriptPath`, not `name: "fabric-dispatch"` — by-name lookup for a
custom (non-built-in) workflow script has been observed to fail with
`Workflow "fabric-dispatch" not found. Available: deep-research`, even
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
file exists only to route the `/fabric-graph` slash command to the real
dispatcher — a Dynamic Workflow script
(`.claude/workflows/fabric-dispatch.mjs`) that holds the actual
node/edge graph, spawns the seven agents, and drives the repair loop. If you
catch yourself about to write a plan file or code directly because of this
skill, stop — that means the `Workflow` tool call was skipped, which is
exactly the failure this file was rewritten to close (see
`SESSION-HANDOVER-v3.13.md` in the source repo for the incident: an earlier
version of this file embedded the full pipeline description in prose, and
the model followed it "in spirit" inline instead of invoking the script —
silently skipping the whole graph, with no `state.json`, no subagents, no
Reviewer, and no quality gate ever running).

## Flags and configuration

Pass these through verbatim in the goal text; the dispatcher parses them itself.

- `--skill=<name>` (repeatable): hard-required skill, see above.
- `--profile=<name>`: select a domain profile from `.agents/profiles/<name>.json` (`copywriter`, `creator`, `kicad`, `touchdesigner`). An unknown or repeated `--profile` escalates before any agent works. Without the flag the dispatcher matches profile triggers against the goal, and falls back to the default software pipeline. See `.agents/graph.md`, "Domain profiles".
- `--workstreams`: let Architect plan dynamic workstreams (1 to 6, `execution_manifest` in `state.json`) instead of the fixed build nodes. See `.agents/graph.md`.
- Teams and roles: `aos-team list|show|new`, resolved Project (`.aos/teams/`, `.aos/roles/`) > User (`~/.aos/`) > shipped defaults.
- `.aos/pipeline.json` (project) or `~/.aos/pipeline.json`: per-role model overrides, see `docs/agent-models.md`.

**Linear run.** `fabric-graph` is the only full pipeline. For a straight-line run with file hand-offs and no `state.json`, follow [`linear.md`](linear.md) instead of calling the dispatcher.

**Existing state files.** `production_artifacts/state.json` keeps its path and schema; a file written by an older dispatcher loads unchanged.

## Live map

When the build phase begins, the dispatcher starts the aos-trail live map
(Trigger B) with the command below; it is safe to run twice, since
`aos-trail` reuses a map already running for this repo:
`aos-trail --ensure`
(it prints a URL, default http://localhost:5330; inside AO, where
`AO_BROWSER_CAPABILITY` is set, also run `ao preview <url>`). If the plan was
opened in plan-canvas (pipeline context), also run
`aos-plan-canvas trail <plan-dir>` first so the map gets the execution plan.
The Architect creates the plan from a template (`aos-plan-canvas new <template-id> production_artifacts/plan`);
before any build node the dispatcher waits for the human verdict via `aos-plan-canvas open <plan> --await`
(`approve` continues, `request-changes` returns to Architect with the feedback; `AOS_PLAN_APPROVAL=auto` is the CI-only skip and prints a visible warning).
Headless runs (`CI` set or stdin not a TTY) wait at most 30 minutes by default and then escalate; `AOS_PLAN_AWAIT_TIMEOUT_MS=<ms>` overrides it (`0` = unbounded). An ended session, timeout or missing `aos-plan-canvas` CLI escalates instead of looping Architect; comment-only feedback is request-changes with all comment texts.
After approval every worker starts with `AOS_TRAIL_NODE`/`AOS_TRAIL_PLAN` (or a `[trail-node:<id>]` brief marker).
Put the live-map link in your reply (the autostart hook also adds it as context when active). Agents follow
the status-mark rules from the `agenttrail` skill: `[~]` before starting,
`[x]` when done, `[!]` when stuck, with `by: <agent>`, saving the plan file
immediately. GO requests surface in the agenttrail hub, where the human
answers them by typing GO.

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

## Teams and roles

`/fabric-graph` resolves roles and teams through the shared registry alongside the default 7-node team:

- **Registry & CLI**: Enumerate available teams with `aos-team list`, inspect a team with `aos-team show <id>`, or scaffold with `aos-team new <id>`. Resolution precedence follows Project (`.aos/teams/`, `.aos/roles/`) > User (`~/.aos/teams/`, `~/.aos/roles/`) > Shipped defaults (`.agents/nodes.json` plus the role and team presets bundled with AOS).
- **Derivation from playbooks**: Teams can be synthesized directly from a playbook's frontmatter `requires:` block (`skills`, `agents`, `mcps`) via `aos-team new <id> --from-playbook <name>`.
- **Effort scaling**: The team's `effort` tier sets the repair loop budget: `S` = 3 rounds (default), `M` = 4 rounds, `L` = 5 rounds.
- **Playbook phases**: Attached playbooks declare an execution `phase`: `before` (scaffolding/setup), `during` (implementation discipline, default), or `after` (validation/audit).
- **Ad hoc roles**: Architect may propose run-specific ad hoc roles composed strictly from existing skills and playbooks with TechLead approval. Such roles introduce no unverified tools/MCPs, live in `state.json` for that run, and are persisted to `.aos/roles/` only if explicitly saved.

## Available tools

Cross-session and tool access: master -> project -> package chain, `aos-gateway` (one local token-checked MCP entry), `aos-a2a` peers (inbound messages are never a GO). Repo docs: https://github.com/hybridlabor-api/aos/tree/main/docs.

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
