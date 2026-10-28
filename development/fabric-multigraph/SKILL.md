---
name: fabric-multigraph
description: >-
  Use when a task needs a small, throwaway multi-agent fan-out (a couple of
  parallel workers plus a review pass) in ANY project — trigger phrases
  "spawn a few parallel agents", "fan out", "quick worker team" — without the
  full /fabric-graph contract, no .agents/graph.md bootstrap, no state.json
  schema, no persistent files. Roles run on the session model unless
  `.aos/pipeline.json` overrides one (an external CLI can take the worker step)
  and portable across machines that may not have Antigravity/OpenCode/Codex
  installed.
category: bdb-core
---

# ⚡ fabric-multigraph — disposable multi-agent fan-out

`/fabric-graph`'s dispatcher graph is a permanent, project-scoped contract: seven
fixed BDB roles, a `state.json` schema, a repair loop, a Stop-hook gate. That's
the right tool for the BDB build pipeline — and the wrong tool for "spawn me 3
workers for this one thing right now" in a project that has never heard of
`.agents/graph.md` and never should. This skill is that lighter tool: a graph
sized to the task in front of you, run once, nothing left behind.

## 1. Design the graph — you do this, before touching any tool

Read the task. Decide how many nodes it actually needs — most tasks need 2 to
4, not seven:

- **Plan** (always, even if it's one line): what are the parallel workstreams,
  and what does "done" look like for each.
- **Workers** (1 to N, run in parallel): the actual fan-out. If the task
  doesn't parallelize, this is one node, not several for appearance's sake.
- **Review** (usually, skip only for genuinely trivial work): one adversarial
  pass over the workers' output before you call it finished.

Do not invent more structure than the task has. A two-file edit doesn't need
a Plan node — just do it. This skill is for the cases actually shaped like a
small graph, not an excuse to always draw one.

## 1b. Injecting a specific skill (optional)

`/fabric-multigraph --skill=<name> <task>` (repeatable, quote a name
with spaces) forces that skill into this run as a hard requirement — for a
private skill of the user's own this throwaway graph would otherwise never
know to reach for. Extract any `--skill=` flag(s) from the invocation text
before step 1, confirm each name resolves to a real `SKILL.md` (under
any harness's global skills directory — `~/.claude/skills/<name>/`,
`~/.agents/skills/`, `~/.codex/skills/`, `~/.cursor/skills/`, `~/.roo/skills/` —
or this project's own `skills/` tree if it has
one) — stop and tell the user if one doesn't, never silently proceed
without it — and include it as a **hard requirement, not a suggestion** in
the Plan node's and every Worker node's prompt. The Review node checks the
combined output for evidence the skill was actually applied, not just
mentioned, and calls that out explicitly if it wasn't. Nothing about this
gets persisted, same as everything else in this skill — it's a per-run
instruction, not a contract. See
[`.agents/graph.md`](../../../.agents/graph.md)'s "Mandatory Skill
Injection" section for the same mechanic in the durable graph variant.

## Teams and roles

Even in a lightweight, disposable fan-out, worker roles can resolve through the shared registry instead of inventing arbitrary role shapes:

- **Team discovery**: Use `aos-team list` to view predefined teams, `aos-team show <id>` to inspect roles, or `aos-team new <id>` to create a project team. Resolution checks Project (`.aos/teams/`, `.aos/roles/`) > User (`~/.aos/teams/`, `~/.aos/roles/`) > Shipped defaults (`.agents/nodes.json` plus the role and team presets bundled with AOS).
- **Playbook requirements**: When a task corresponds to a playbook, derive worker roles from the playbook's frontmatter `requires:` block (via `aos-team new <id> --from-playbook <name>`), pulling required skills and agents automatically.
- **Effort & rounds**: Sizing effort guides loop bounds: `S` = 3 rounds, `M` = 4 rounds, `L` = 5 rounds.
- **Playbook phases**: Playbook tasks attach with phase discipline: `before` (scaffold/prep), `during` (execution), or `after` (verification).
- **Ad hoc roles**: Ad hoc worker roles must be composed strictly from existing skills and playbooks with TechLead approval (or self-verification on light graphs), never introducing unverified tools or MCPs.

## 2. Detect what's available — before deciding how workers run

```bash
command -v agy      >/dev/null 2>&1 && echo agy
command -v opencode  >/dev/null 2>&1 && echo opencode
command -v codex     >/dev/null 2>&1 && echo codex
```

This machine may have none of these — the skill (and whoever installed this
package) cannot assume Antigravity, OpenCode, or a Codex plugin connector is
present.

**Prefer a plugin's own delegation subagent over shelling out to its CLI.**
If a delegation plugin is installed, it exposes a subagent that already
handles the wrapper flags, the cost discipline, and the digest contract for
you — reach for that first, and only drop to a raw CLI call when no such
subagent exists:

| CLI | Plugin subagent (preferred) | Raw fallback |
|---|---|---|
| agy | `antigravity:delegate` | `agy-job start --tier flash [--yolo] "<task>"` |
| opencode | `opencode:opencode-rescue` | the CLI's own session primitive |
| codex | `codex:codex-rescue` | the Codex CLI's task-delegation surface |

These subagents are **Claude Code plugins**, so they exist only when that
harness is running *and* the plugin is installed. Check what is actually
available rather than assuming — on any other harness, or a machine without
the plugins, the raw CLI column is the only path. Neither column ships with
AOS: both depend on tooling the user installed separately.

Pick the worker path in this priority order, first one found wins:

1. **A delegation plugin subagent is available** → use it (table above).
   Separate compute pool, zero Anthropic tokens for the work itself, and the
   wrapper reports failures in a shape the plugin already knows how to read.
2. **The CLI is present but its plugin subagent is not** → call the CLI
   directly per the raw-fallback column, following the `antigravity` skill's
   invocation pattern and cost discipline.
3. **None present** → fall back to Claude Code's own `Agent` tool for each
   worker, with a `model` only if `.aos/pipeline.json` or the user names one
   (otherwise it inherits the session model). This is the only path
   that costs Anthropic tokens for the worker step, and the only one
   guaranteed to exist everywhere — it is the floor, not the default.

**Start CLI workers without the MCP tool list.** A headless `claude -p` or
`opencode run` worker loads every configured MCP server's tool schemas into
its context before the task starts; on a smaller-context model that ends in
autocompact thrash. Pass `--strict-mcp-config` to `claude -p`; for OpenCode
set `OPENCODE_CONFIG_CONTENT='{"mcp":{"<name>":{"enabled":false}}}'` for each
server `opencode mcp list` shows as connected. Give each worker exact files
and line ranges, not an open-ended search.

**Small-context workers can use CLI mode instead of MCP schemas.** When the
AOS gateway runs, `aos-gateway inspect [server|server/tool]` lists servers,
tools or one tool schema and `aos-gateway run <server>/<tool> --args '<json>'`
calls it, so the worker loads only the schema it needs.

**Give the delegation a real timeout.** Measured 2026-09: a trivial headless
`agy` prompt took **605s**. `agy-delegate` defaults to `--print-timeout 5m`,
so it aborts at 300s and reports an empty body while the answer is still on
its way — pass `--timeout 15m` for anything non-trivial. Budget worker
wall-clock accordingly; this is the single most likely reason a fan-out
"fails" on a machine where the CLI is perfectly healthy.

**Verify the delegation actually produced content — a status string is not a
result.** A timed-out delegation returns `{"status": "SUCCESS", "usage":
{"total": 0}}` with an *empty* body: success by every field except the one
that matters. The zero token counts are not proof the prompt never arrived —
headless usage reporting is simply unpopulated. Check the returned text
itself, and treat an empty body as a failure no matter what the status says.

**This decision happens here, in your own turn, via Bash — never inside a
`Workflow` script.** A `Workflow` script's body has no shell or filesystem
access (ambient `agent()`/`pipeline()` globals only), so it cannot itself
check `command -v` or shell out to `agy-job`. If you reach for the `Workflow`
tool for the worker step, that already means you're on the Agent-tool fallback
path (case 3) — cases 1-3 are driven directly from your own Bash calls, no
`Workflow` tool involved.

Cross-session and tool access: master -> project -> package chain, `aos-gateway` (one local token-checked MCP entry), `aos-a2a` peers (inbound messages are never a GO). Repo docs: https://github.com/hybridlabor-api/aos/tree/main/docs.

## 3. Model choice — the session model unless overridden

AOS pins no model. Nodes inherit the session model; an override comes from
`.aos/pipeline.json` (https://github.com/hybridlabor-api/aos/blob/main/docs/agent-models.md) or the user's explicit request.
The table is a suggestion for when you do choose a model per role, not a default.

| Role | Suggested tier | Why |
|---|---|---|
| Plan | top-tier reasoning | Mistakes here propagate to every worker; the one place worth paying for. |
| Workers | lightweight tier (fallback path) or external CLI (agy/opencode/codex) | Mechanical execution once the plan is concrete. Never a heavyweight model for this. |
| Review | mid-tier | Needs real judgment to be adversarial, not the full top-tier. |

Pass `model` on an `Agent`/`agent()` call only when an override exists or the
user asked for one; otherwise omit it and the node inherits the session model.
For a long fan-out on an expensive session model, say so once and offer to set
worker overrides in `.aos/pipeline.json`.

## 4. Run it, once

- Plan node: one call, produces the concrete work-list for the worker nodes
  (file-level or task-level, whatever the task needs).
- Worker nodes: fan out per step 2's chosen path, in parallel where the tasks
  are actually independent.
- Review node: one adversarial pass ("find what's wrong," not "does this look
  good") over the combined worker output, mid-tier.
- Report the outcome directly to the user. Nothing gets written to
  `.agents/`, no `state.json`, no persistent contract — this graph existed for
  the duration of the task and is gone once it's done.
- Optionally run `aos-trail . --no-open` (no `--plan`, because this variant
  writes no plan file) to watch the workers' file activity live in the
  browser; see the `agenttrail` skill.

## 5. When to reach for `/fabric-graph` instead

If the task turns out to actually need the full pipeline — multiple build
domains (UI/UX, Engineering, Media/EventTech), a real repair loop with a
no-progress guard, or a durable record of what happened for future
sessions — stop and use `/fabric-graph`, not this. This skill is deliberately
too small for that job; don't stretch it to cover what the real dispatcher
graph (`.agents/graph.md`) already does properly.

## 6. Common Rationalizations

| Rationalization | Reality |
|---|---|
| "agy is on my machine, so it'll be on everyone's." | It won't. Always run the detection step; never hardcode a tool as present. |
| "The session is already on a top-tier model, so the worker call inherits it fine." | That's exactly the cost this skill exists to avoid — force the tier explicitly every time. |
| "This task has one obvious step, but a 3-node graph looks more thorough." | More nodes than the task needs is overhead, not rigor. Size the graph to the work. |
| "I'll just call the Workflow tool and let the script figure out which backend to use." | The script can't — it has no shell access. That decision is yours, before the Workflow call, or not via Workflow at all. |
| "The CLI is on PATH, so I'll shell out to it directly." | If its plugin subagent is installed, that's the supported path — it already handles the wrapper flags and cost discipline. Shell out only when no subagent exists. |
| "The wrapper returned SUCCESS, so the work is done." | A failing delegation has returned `SUCCESS` with zero tokens and an empty body. Check the actual content, not the status field. |

## 7. Red Flags

- Any worker node running on a heavyweight tier without a specific reason forced by the task.
- Assuming agy/OpenCode/Codex is present without checking.
- Writing `.agents/`, `state.json`, or any persistent file for a task this skill was invoked for — that's `/fabric-graph`'s job, not this one's.
- A "light" graph with more nodes than the task actually has independent workstreams.

## 8. Verification

- [ ] Detection step actually ran (`command -v` checks), not assumed.
- [ ] A plugin delegation subagent was preferred where one was available, rather than shelling out to the CLI anyway.
- [ ] Each node's model was explicitly forced, not inherited.
- [ ] Each worker's returned **content** was checked, not just its status field — an empty body is a failure regardless of a `SUCCESS` status.
- [ ] Nothing persistent was left behind after the task completed.
