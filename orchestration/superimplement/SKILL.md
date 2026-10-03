---
name: superimplement
description: "Run a superRA task tree autonomously through dispatched implementer and reviewer seats. Requires superRA:using-superra. Use when the researcher asks for autonomous execution or accepts a recommendation for it, and to resume mixed task statuses or verify code-complete work."
---

# superimplement — autonomous IMPLEMENT execution

Owns per-task dispatch, the implementer-reviewer loop with orchestrator-discipline filtering, and the phase-exit gate in `references/completion.md`.

**Announce at start:** "I'm using the superimplement skill to run the task tree autonomously."

## Execution Modes

Entering this skill *is* autonomous mode. Interactive main-agent execution is the default on a built tree — you are here because the researcher asked for autonomous execution or accepted your recommendation of it (`using-superra/references/main-agent.md` §Execution Modes). Researcher asks to steer closely mid-flight: hand the frontier back to `using-superra/references/interactive-mode.md`.

## The Process

**Load `superRA:agent-orchestration` before selecting seats or writing any dispatch prompt.**

1. Complete Step 1.
2. Execute frontier tasks through Step 2 until none require implementation, review, or fixes.
3. Close the phase through `references/completion.md`.

### Step 1: Load

1. Run `superra task tree` for the full tree with statuses.
2. **Confirm there is implementation work.** Continue here when the frontier has tasks to implement, review, or fix, or reproducibility or the completion disposition is pending. All tasks already `approved`: skip dispatch, go to `references/completion.md`.
3. **Load the active domain skill(s) following the manifest**, plus any task-specific helper skills named in the active task or its ancestor chain.

### Step 2: Execute Tasks

**Compute the frontier with `superra task frontier`.** Execute frontier tasks singly or as same-parent bundles; use a parallel Agent-tool batch when multiple selected seats are dispatched and independent (subject to `agent-orchestration` §Workload Balancing). Serialize only when no parallel batch is available. Re-compute the frontier after each completed task or bundle.

#### Task Execution Steps

1. Select the per-task seat structure through `superRA:agent-orchestration`.
2. Execute the implementer seat. `Task:` carries one task path (e.g. `Task: data-preparation/merge`); `Tasks:` lists a bundle.
3. **NEEDS_CONTEXT or BLOCKED:** provide context and rerun the implementer seat (`agent-orchestration` §Orchestrator Duties).
4. **DONE or DONE_WITH_CONCERNS:** decide per assigned task whether an independent pass runs, per `using-superra/references/main-agent.md` §Deciding on Review. Review runs: execute the reviewer seat, naming the tier and focuses; on REVISE, adjudicate and schedule fixes per §Handling Reviewer Feedback — fix now and iterate to APPROVE, or defer and advance. No review: that section's no-review branch.
5. **Approved:** in a bundle, verify every assigned task has its own `status: approved` — an aggregate approval is invalid. A child major result worth surfacing: one-line entry in the immediate parent's `## Results` linking to the child, not restating its numbers. Findings that change upcoming tasks: update those objectives and commit. Re-compute the frontier.

A downstream task about to inherit a structurally messy or notation-incoherent derivation from a just-approved task: dispatch `Stage: integration` against that single task before advancing.

#### Handling Reviewer Feedback (Orchestrator Discipline)

See `superRA:agent-orchestration` §Handling Reviewer Feedback (Orchestrator Discipline).

### Step 3: Close the Phase

Follow `references/completion.md` — reproducibility verification, then the 4-option completion menu.

## Orchestrator Discipline

Cross-stage orchestrator behavior: `superRA:agent-orchestration`.

**Review scope at interim checkpoints:** task-local correctness under `superRA:review-task` §Review Protocol. Codebase integration review defers to `superintegrate`. **When** a review runs at all: `using-superra/references/main-agent.md` §Deciding on Review, applied per Step 2.4 above.

## Autonomy and Stop Points

Pausing is a main-agent decision — dispatched implementer/reviewer subagents never ask the researcher directly; they return `NEEDS_CONTEXT` / `BLOCKED` and the orchestrator applies `using-superra/references/main-agent.md` §Proceeding and Pausing. Its two pause situations map onto superimplement work as:

- **Pre-set workflow gate** — the completion menu (`references/completion.md`).
- **A decision that materially changes a task objective** — a domain hard blocker (bad input quality, a merge that shifts row counts, a validation failure, a missing pipeline file or required input, critical gaps in the tree) or a methodology/authority call (disagreement with a reviewer, overriding a blocking finding, repeated reviewer disagreement on the same point, a scope/definition call with no obvious answer). A **researcher-initiated scope change** mid-execution — new task, removed task, methodology pivot, sample redefinition — routes through `superplan §User Feedback and Changing the Task Tree` instead.

Blocking reviewer findings are not a stop point — adjudicate and fix through the REVISE loop without asking the user.

## Agent Loads

Both roles run the `implementation` Stage (`superRA:using-superra` §Skill-Load Manifest).
