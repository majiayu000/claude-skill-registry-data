---
name: agent-orchestration
description: Coordinate superRA agents and handoffs. Requires superRA:using-superra. Use to dispatch roles, run parallel agents, choose reviewers, or preserve workflow state.
---

# Agent Orchestration

Delegate tasks to specialized agents with isolated context. Parallel-dispatch independent tasks/reviews; serialize iterative loops.

## Workload Balancing

Every dispatch costs a spawn — skill-load, context hydration, per-turn overhead. Match the tier to the work:

### Tier 1 — Small: main implementer seat

Use the small-task structure in §Seat Assignment.

### Tier 2 — Slightly involved: bundle and delegate

One dispatch carrying several small-to-medium tasks that share context — same stage, same domain, same parent, shared files or references — done by one agent in a single turn.

- Three edits in the same skill file.
- A reviewer sweep over two sibling agent files.
- A template plus its one consumer.

Bundling is spawn-cost amortization only: each bundled task keeps its own contract, status, results section, and review verdict.

### Tier 3 — Complicated: one dedicated agent per task

One agent owns one task. Use when the task needs deep context — cross-file grep, multi-step refactor, full skill-load chain — or its deliverable will be reviewed in isolation.

- A refactor touching >5 files across skills + agents + tests.
- A new feature requiring full domain-skill engagement.
- Bundle-context that would exceed ~150k tokens.

### Model Tier Selection

Default to medium — Sonnet in Claude Code, medium thinking in Codex. Step up to Opus / deep thinking when:

- the spec emerges mid-task rather than from the objective;
- silent-error risk is high — results-bearing code where a wrong output ships without obvious failure;
- the dispatch is a thorough-tier first-pass review (lower tiers over-comply); a narrow re-review of a cited fix stays medium;
- heavy context synthesis reconciles many files/skills in one head.

Fable is reserved for the most challenging, expensive tasks. Defaults, not rules — an explicit user preference wins.

**No agent type:** call `Agent(model: <concrete Claude model>, prompt: <dispatch prompt>)`.

## Parallelization and Worktree Isolation

**Load `references/parallel-dispatch.md` before dispatching agents in parallel or isolating an agent in its own worktree** — parallel agents require per-agent worktrees, and the seeding and harvest rules live there.

## Dispatch Templates

**Implementer:**
```
Prompt:
  Load `using-superra` and `implement-task` skill.

  Stage: <stage-name>
  Task(s): <task path — e.g., "data-preparation/merge">
  Worktree: <absolute path>   # optional — parallel-dispatch only

  Additionally: <optional steering — focus area, prior-round adjudication notes, warnings>
```

**Reviewer:**
```
Prompt:
  Load `using-superra` and `superRA:review-task` skill.

  Stage: <stage-name>
  Task: <task path — e.g., "data-preparation/merge">
  Git range: <BASE_SHA>..<HEAD_SHA>
  Tier: quick | thorough      # optional — defaults to quick
  Focus: <dimensions>         # optional — defaults to correctness
  Worktree: <absolute path>   # optional — parallel-reviewer pattern only

  Additionally: <optional steering — focus area, prior-round adjudication notes, warnings>
```

`Additionally:` is steering only — omit it when there is none, never restate role protocol, manifest loads, or task content.

Bundle only same-stage, same-domain, same-parent frontier leaves that share context and are simple enough for one agent. Keep dependent siblings out unless the upstream task is already `approved` or deferred (§Handling Reviewer Feedback).

Parent objectives are inherited shared context at the dispatch boundary; sibling results are not. A downstream task consuming an upstream result: the steering or the downstream objective names the approved dependency `## Results` to read.

## Seat Assignment

In **autonomous** mode (`using-superra/references/main-agent.md` §Execution Modes) each task has an implementer seat, and a reviewer seat when a review is triggered; each is filled by the main agent or a dispatched subagent:

| Implementer | Reviewer | Choose when |
|---|---|---|
| subagent | subagent | Default for large or routine work. |
| subagent | main | Small or high-stakes work where the main context should carry the review. |
| main | subagent | Small or context-heavy implementation that still needs independent review. |

Main agent filling a seat: load that seat's role skill — `superRA:implement-task` or `superRA:review-task` — plus its stage and domain loads, and execute directly. A main reviewer gets the same `Git range:` a dispatched one would; a main implementer hands its commits to the dispatched reviewer.

## Orchestrator Duties

Done by the orchestrator alone, at every workflow stage:

- **Task sequencing and dispatch inside the selected frontier.** The main agent picks the frontier; this skill sizes, bundles, and dispatches inside it.
- **Adjudicate reviewer feedback in place** (§Handling Reviewer Feedback).
- **Handle implementer status returns.** Re-dispatch on missing context; escalate researcher-owned blockers through the active workflow's pause rules.
- **Escalate via `AskUserQuestion`** (plain text if unavailable) when stuck — hard blocker, research-related decision, override of a blocking finding. Fold the decision into the task objective by rewriting it fully; add `## Revision Notes` when the change is non-obvious.

## Handling Reviewer Feedback

Adjudicate every finding — REVISE (`[BLOCKING]`) or APPROVE (`[ADVISORY]`) — before moving on; read cited code or task context only when needed to decide. Per finding:

**Approval gate.** `[BLOCKING]` in `## Review Notes` keeps the task out of `approved`.

- **Accept** real issues.
- **Reject** false positives, removing them from `## Review Notes`.
- **Escalate** findings that would materially change the direction of the task.

**Schedule accepted fixes against the whole workflow**

- **Fix now** when the issue significantly affects downstream tasks:
  1. **Implementer:** choose a dispatched or main seat; execute it per §Seat Assignment.
  2. **Reviewer:** choose a dispatched or main seat; execute it per §Seat Assignment. Iterate to APPROVE before advancing the frontier.
  Small fix/re-review with warm agents: steer each existing seat rather than spawning replacements (in Claude Code, `SendMessage` to its id/name; a new `Agent` call always starts cold).
- **Defer** when the open items do not affect downstream work, defer the fix and proceed for now. Fix them later in bundles (see §Workload Balancing) and re-review before the workflow's completion gate.
