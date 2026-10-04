---
name: spec-to-done
description: Route a piece of work through the full long-horizon loop — specify, plan, execute, replan, report — by deciding whether the work warrants the loop, detecting which stage it is already in, and handing off to the right skill. Use this skill whenever the user asks to take something from idea to done, to handle a goal end to end, to run the full workflow, to work on something properly with a plan and evidence, or to resume, continue, or check where a previous run of this workflow stopped.
metadata:
  author: "Giuliano Lemes <giuice@gmail.com>"
---

# Spec to Done

Route work through `SPECIFY → PLAN → EXECUTE ↔ REPLAN → REPORT`.

This skill decides and hands off. It holds **no** planning, execution, or reporting rules — those live in the skills it routes to, and duplicating them here would create a second source of truth that drifts. If you catch yourself explaining how to write a task or a report, stop and hand off instead.

## Step 1 — Locate the work first

Derive a slug from the goal — short kebab-case — and look at `spec-interview/<slug>/`. If the user is resuming and the slug is unknown, list the folders and ask which one.

**Match on the goal, not on the slug.** If a folder already exists, compare its stored goal to what the user is asking for now — the `Goal:` line in `PLAN.md` or `SPEC.md` (older SPECs may only have a Summary — use it); failing that, the scope restatement that opens `state.md`. If none of these exists yet, ask the user whether the folder is the same work before touching it. Different work can produce the same slug — two "export" features, two "cleanup" tasks. When the stored goal is not this goal, do not resume it: pick a distinguishing slug and start fresh. Silently continuing an unrelated run corrupts both records.

Locating comes before deciding, because the gate below must never fire on work that already exists.

## Step 2 — Does *new* work need the loop?

Only for work with no folder yet. **An existing run is never subject to this gate** — it already has a contract and a ledger, and finishing it outside them would strand the record it was keeping.

Most new work does not need the loop. It costs a requirements interview, a plan file, a verification and a ledger entry per task, and a replan checkpoint after each one. That overhead buys traceability and resilience over a long horizon; on a small change it buys nothing.

Run the loop when **at least two** of these hold:

- the work is more than a handful of tasks;
- it will not finish in one sitting, or will outlive one context window;
- getting the requirements wrong is expensive to undo;
- execution is likely to discover things that change the approach;
- someone needs to audit afterwards what was done and on what evidence;
- the work will be handed between people, sessions, or agents.

Otherwise just do the work. Say in one line that you are skipping the loop and why — do not run a ceremony to look thorough.

Between the extremes, offer the middle: `plan-from-spec` and `execute-plan` on a stated goal, skipping the SPEC interview.

## Step 3 — Route on what exists

**First matching row wins.**

| State of `spec-interview/<slug>/` | Hand off to |
|---|---|
| `REPORT.md` exists and no other artifact in the folder changed after it — compare file modification times | Nothing — state the outcome and ask what is next; if the user reports a blocker resolved, see "Reopening after `replan exhausted`" |
| The last ledger entry says `Gate: replan required` | `execute-plan` — resuming, it invokes the replanner and closes the `Gate:` |
| `PLAN.md` has `Status: no-op` and no tasks | `completion-report` |
| Every task is `done` or `no_op` | `completion-report` |
| Some task has no ledger entry | `execute-plan` |
| Every task has an entry and at least one is not `done`/`no_op` | See "Interrupted mid-loop" below |
| `SPEC.md` exists, no `PLAN.md` | `plan-from-spec`, initial mode |
| Interview artifacts exist (`round-*.html`, `state.md`), no `SPEC.md` | `spec-from-scratch`, resuming the interview |
| Nothing yet, and the goal is already clear | `plan-from-spec` — state the goal directly, no SPEC |
| Nothing yet, product work with unclear requirements | `spec-from-scratch` |
| Nothing yet, non-product work with unclear requirements | Clarify here first — see below |

Replanning is never a direct route from here. `execute-plan` owns its replan gate, calls `plan-from-spec` itself, and closes the `Gate:` line afterwards — only it writes the ledger. Do not intercept that loop.

### Interrupted mid-loop

Every task has an entry, but the run is not finished. Read the **last** entry's `Gate:` line:

| `Gate:` | Meaning | Hand off to |
|---|---|---|
| `replan required` | The gate fired and the replan never finished | `execute-plan` — it replans and closes the `Gate:` |
| missing | The run died before reaching its gate | `execute-plan` — it runs the gate it never reached |
| `replan exhausted`, `PLAN.md` version equals the entry's | Replanning concluded no valid plan exists | `completion-report` |
| `replan exhausted`, `PLAN.md` version is higher | The run was reopened and the replan finished; only the `Gate:` was left open | `execute-plan` — it closes the `Gate:` and continues |
| `replan done (plan version N)` or `replan reopened (plan version N)`, N is the current plan version, still nothing dispatchable | Replanning already tried and could not route around the blocker | `completion-report` |

This is why `execute-plan` closes every entry with `Gate:`. Without it, an interrupted run and a terminally blocked one look identical from the folder.

### Reopening after `replan exhausted`

`replan exhausted` means no valid plan existed under the conditions of that moment — not that the goal is dead. When the user returns saying the blocker is resolved — access granted, decision made, dependency available — do not start a new run and do not re-gate the work. Hand off to `execute-plan` with the user's report: it owns the replan loop, so it confirms the resolution — observably when a check exists, by the user's explicit confirmation (`attested`) otherwise — and then invokes `plan-from-spec` in replan mode itself, with the resolution as the trigger. Routing straight to the planner from here would bypass the owner of the gate and the ledger. The exhausted entry's `Gate:` becomes `replan reopened (plan version N)`, so the stop and the restart both survive in the ledger even after later replans replace the plan text.

### Non-product work with unclear requirements

Do not send this to `spec-from-scratch` — its interview and output are shaped for product work, and it would force user journeys and launch criteria onto research, operations, or physical-world goals.

Clarify it here instead, in as few questions as it takes: what does done look like, what must not happen, and what constrains the approach. As soon as you can name at least one checkable outcome condition, hand to `plan-from-spec` with the goal stated directly. If the goal resists that after a couple of rounds, say so — a goal with no checkable outcome cannot be planned, only discussed.

## Step 4 — Hand off cleanly

One stage at a time. Name the skill you are invoking and why, then let it own its own contract, gates, and output. Do not pre-chew its work, and do not second-guess its gates from here — a readiness gate that fails means another round in that stage, not an override from this one.

When a stage escalates to the user — an unreachable acceptance criterion, a destructive action, a missing credential — surface it and stop. Escalations are the user's decision, and routing around one defeats the point of having it.

## Resuming

When the user asks where things stand, read the folder and state it plainly before routing:

```
Goal:        <from PLAN.md, SPEC.md, or state.md>
Plan:        version <N>, <M> tasks
Progress:    <k> done, <k> unresolved
Last entry:  <task id, status, and its Gate line>
Blockers:    <from the ledger, or none>
Next:        <the row that matched in step 3>
```

The ledger is the source of truth for progress, not memory of the conversation.

## When the user wants one stage only

Honor it. "Just write me a plan" ends at `plan-from-spec`. "Just tell me what happened" is `completion-report` alone. Do not drag someone through the whole loop because they touched one part of it.
