---
name: forge-team-orchestration
description: "Use when splitting a job over 2+ parallel Bosses or lanes (werk verdelen)."
# W2-BUDGET original description (listing budget): "Use when splitting one job over 2+ parallel Bosses or Workflow lanes (werk verdelen, lanes verdelen, team samenstellen): cards, file ownership, waves, one integrator."
---

# forge-team-orchestration: running Bosses as a team

A parallel run only helps when its output can be merged. This skill turns a job into **cards** with an owner, a disjoint
file scope, a state, evidence and a merge gate, then puts the cards into **waves**. It runs them with Workflow
`parallel()` / `pipeline()` or Agent-tool dispatch, and leaves **one integrator** (the Lead) to merge and verify the
assembled result.

## When to use / when not
- Use when two or more Bosses or lanes would write the same repo in one run, when a work package has two or more natural
  parts (contract, core code, tests, docs, data, UI), or when earlier fan-out produced output that does not merge.
- Do not use it for a one or two file change, or for work tightly coupled inside one file. Keep that package whole and say so
  in one line.
- Read-only work (audits, reviews, measuring, drafts) never collides, so it can run beside the writers. It still gets a card
  so its output has an owner and a place to land.

**Siblings, which this skill does not replace:** `dispatching-parallel-agents` (is this work independent at all?),
`forge-worktrees` (isolation mechanics), `forge-agent-report` (the report each card returns), `forge-router` Step 4 (the
hotspot lock protocol), `forge-heartbeat` (silent agents). This skill is the team doctrine that ties them together.

## 1. The card contract (every parallel part gets one)
A card is a work package, logged as an `agent_work_package_created` event before the work starts (mission ledger rule in
`CLAUDE.md`). Each card states:

| Field | Meaning |
|---|---|
| `owner` | Exactly one Boss (or GOAT agent) accountable for the card. |
| `route` | GOAT route + model + effort (`build` = opus/medium and so on). An unrouted card is not dispatchable. |
| `owns` | Project-relative paths this card may write. No wildcards, no overlap with any other card in the same wave. |
| `reads` | Shared files it may read but never edit (types, contracts, config). |
| `forbidden` | Hotspots and areas it must not touch (registries, sync manifests, doctor, settings). |
| `interface` | What it exports to and imports from other cards: names, shapes, file paths. |
| `acceptance` | Verifiable criteria: a command, an output, a screenshot. Never "looks good". |
| `out_of_scope` | Work that is explicitly not this card's job. |
| `state` | One of the states below. |
| `evidence` | Real command output, file paths, screenshots, review notes. |
| `merge_gate` | The exact condition that lets the Lead integrate it. |

Full card shape, the six-part brief every dispatched agent receives, and a worked example: `references/card-and-brief.md`.

**Card states:**

| State | Exit criteria |
|---|---|
| backlog | Acceptance criteria written. |
| ready | Owner, route, `owns` and wave assigned; no overlap with another card in that wave. |
| running | The agent returned a forge-report and its changed-file list. |
| review | Verify Boss re-ran the checks; every changed file lies inside `owns`. |
| blocked | The blocker has an owner and a next action (owner-gated items go to the owner queue at the end). |
| merged | The Lead integrated it and the integration check on the assembled tree passed. |
| archived | No longer relevant; the reason is recorded. |

"Done" means `merged`. A card in `running` that says it is finished is a claim, not proof.

## 2. Decompose by file ownership
You may think in layers (UI, API, data, tests), components (auth, profile, billing) or concerns (security, performance,
architecture). **Before dispatch, always reduce the split to file ownership**: each card gets a disjoint `owns` list.
- A shared file (types, an interface, a config) has exactly **one** owner. That can be a contract card in an earlier wave or the
  integrator itself. Everyone else gets it under `reads`.
- Hotspots (build or sync manifests, event registries, doctor, dashboards, settings, a project's core files) have one writer per
  run. When a hotspot is not worth a worktree, wrap its writer with `node .claude/forge-bin/forge-lock-guard.cjs acquire <hotspot>
  --run <run_id> --owner "<Boss>"`, keep the `token=` it prints, and release it on the card's terminal event
  with `release <hotspot> --run <run_id> --token <token>` (only the exact acquirer can release). Exit 3 means another run holds the hotspot:
  serialize the card or isolate it.
- Cap: **4 parts per package**. The number of lanes running at once comes from the lane budget
  (`node .claude/forge-bin/forge-lane-budget.cjs`), never from a guess.
- An edit an agent needs outside its `owns` goes into its report (`outOfScopeNeeds` in `forge-build`), never into the tree.

## 3. Dependency graph and waves
- Prefer a wide, shallow graph. The longest chain (the critical path) sets the minimum run time.
- Add an edge only when a card really consumes another card's output. Remove edges that are only habit.
- A cycle is a deadlock. Extract the shared piece into its own earlier card.
- Standard wave order for a package: **contract or design → builders in parallel → tests against the real code → Verify Boss
  on the assembled result**.

Patterns (independent, diamond, fork-join, two chains), their trade-offs, the anti-patterns and worked splits:
`references/graphs-and-teams.md`.

## 4. Running the waves
- **Workflow (preferred, ultracode on).** One wave = one `parallel([...])` of routed `agent()` calls. A serial chain of waves
  is a `pipeline()` or consecutive awaits. Every `agent()` carries `agentType` (a Boss whose frontmatter fixes model and effort)
  or explicit `model` + `effort` opts. Label each one `'<Boss Name> · <card id>'`. For a single package with up to 4 disjoint
  parts, use the bundled runner instead of writing a new one: `Workflow({ name: "forge-build", args: { task, projectRoot,
  parts: [{ id, task, owns: [...] }] } })`. It rejects overlapping `owns`, routes every worker, runs Verify Boss with a scope
  check, and allows at most one escalation.
- **Agent tool (fallback).** One `Agent` call per card, all in one message for a wave, with `subagent_type` = the Boss,
  `model` = the route model, and `effort` when the route differs from the Boss default.
- **Isolation.** Each parallel writer works in its own worktree and branch (`forge-worktrees`) unless the `owns` lists are
  disjoint *and* the workers do not commit (the `forge-build` contract). Read-only cards need no worktree.
- **Brief cold.** A dispatched agent starts with no memory of this chat. Its prompt holds the whole card: objective, owned
  files, requirements, interface, acceptance, out of scope, route, run id, and the name of the next Boss for a SendMessage
  hand-off.
- **Tool fit.** Before each dispatch: `node .claude/forge-bin/forge-dispatch-fit.cjs check --agent <boss> --needs <tools the brief uses>`; exit 1 = pick another Boss (`suggest`).
- **Watch.** From the second lane on, arm the watchdog (`lane-watchdog.cjs` for Agent-tool lanes, `wf-watchdog.cjs` for
  Workflow runs; global HARD MUST). Act on STALLED, HUNG-TOOL and NO-WORK flags at once. When a lane finishes, refill the slot
  from the backlog with the next card that does not collide.

## 5. One integrator: the Lead
Only the Lead merges. No Boss merges its own branch while other parallel work is in flight.
1. **Fail closed on scope.** For each card compare `git diff --name-only` (or `git status --porcelain`) with `owns`. A file
   outside it rejects the card, however good the rest is. Send it back once with the violation named.
2. **Merge in wave order**, resolving conflicts yourself (`resolving-merge-conflicts`). Never use a destructive reset or force
   on the integration branch.
3. **Verify the whole, not the parts.** Run the real build, tests and integration check on the assembled tree. Green parts with a
   red whole are a FAIL.
4. **One rework round.** Following GOAT, a failed card gets at most one escalation (more effort first, then a bigger model).
   A second FAIL goes to the owner as a blocker, not into a repair loop.
5. Update the card states and the ledger, then clean up: remove merged clean worktrees and let the scratch cleanup clear their
   folders (temp HARD MUST).

## 6. Team size
Start with the smallest team that covers every needed dimension. Each extra member adds coordination cost. Two to four
members is the usual best size. Above that, merge roles: one agent covering two dimensions beats two agents finding the same
issues. A read-only Boss (Verify Boss, Test Boss in verifier mode, codex-reviewer) never gets a write card. Preset teams
mapped to the Forge Bosses: `references/graphs-and-teams.md`.

Claude-flow swarm and SPARC ideas on Forge's execution layer: `references/swarm-patterns.md`. The multi-plan, multi-execute, multi-backend, multi-frontend and multi-workflow intents as Workflow fan-outs: `references/multi-commands.md`.

## 7. Failure modes to catch
- **Agent soup:** many agents running, none with an owner or a merge gate.
- **Invisible work:** useful output exists only in a transcript. Every card ends in files plus a forge-report.
- **Board theater:** cards exist but have no acceptance criteria or evidence.
- **Overlapping writes:** two cards with overlapping `owns`, or a hotspot without its lock. This is the 2026-07-22 incident class.
- **No product:** the run produced plans and notes but nothing runnable or reviewable.
- **Fake done:** a card reported done that Verify Boss has not re-run, or a claimed commit that does not exist.
- **Idle lanes:** fewer lanes than the budget allows while independent cards wait. Name the blocking file or lock once.
- **Unrouted agent:** an `agent()` without a route inherits the session model. The workflow guard denies it, so fix the call.
- **Imbalance:** one lane holds three times the work of the others, or every card is blocked on one slow card. Split that
  card or shorten the critical path.

## 8. End of each orchestration pass
Report: the card states (what is merged, in review, blocked), the branches and worktrees still open, the commands and real
results of the integration check, blockers with owner and next action, and any card pattern that repeated and could become a
shared skill.

## Provenance
- **affaan-m/everything-claude-code (ECC)**, `skills/team-agent-orchestration/SKILL.md`, pinned local catalog commit
  `e2b8a51cea2228e515e1c3653effbeb62a2800fa`, MIT (Copyright (c) 2026 Affaan Mustafa). Taken and rewritten: the
  owner/scope/state/evidence/merge-gate card contract, the Kanban states with exit criteria, "one integrator", review in sequence,
  and the failure modes (agent soup, invisible work, board theater, overlapping writes, no product artifact). Excluded: the
  dmux/tmux/Zellij/desktop-orchestrator execution modes, the "dynamic workflow mode" harness section, and the control-pane UI.
- **wshobson/agents**, `plugins/agent-teams/skills/task-coordination-strategies/SKILL.md` plus its task-decomposition and
  dependency-graphs reference files, commit `7e2fb559cf4b824b27f1fec49fe88f7511066d26`, MIT (Copyright (c) 2024 Seth Hobson). Taken and rewritten: the
  decomposition strategies (layer, component, concern, file ownership), the dependency-graph principles and patterns with their
  anti-patterns, the six-part task description, and the workload-imbalance signals. Excluded: every `TaskCreate`, `TaskUpdate`,
  `TaskList` and `blockedBy` API call.
- **wshobson/agents**, `plugins/agent-teams/skills/team-composition-patterns/SKILL.md` plus its agent-type-selection and
  preset-teams reference files, same commit, MIT, read in full. Taken and rewritten: the team-sizing heuristics, the preset
  team shapes (review, debug, feature, fullstack, research, security, migration), "never give a write task to a read-only agent",
  and the custom-team guidelines. Excluded: the `/team-spawn` commands, the `agent-teams:*` subagent types, and the
  `teammateMode` / tmux / iTerm2 display settings (a Claude Code settings write).
- Adopted as markdown only. No scripts, hooks, commands, binaries or install steps were copied or run. MIT notice: "Permission is
  hereby granted, free of charge, to any person obtaining a copy of this software ... The above copyright notice and this
  permission notice shall be included in all copies or substantial portions of the Software."
