---
name: timeboxed-execution
description: Run deadline-bound or scope-sensitive agent tasks with explicit done conditions, protected verification time, evidence gates, and safe-stop rules. Use for rapid implementation, debugging, integration, delegated work, feasibility gates, or tasks where scope drift, false completion, repeated failure, or deadline overruns are material risks.
license: MIT
compatibility: Tool-agnostic. Designed for agent runtimes including Hermes and Codex on Linux, macOS, and Windows.
metadata:
  author: "WENJI"
  version: "1.4.1"
  tags: "timebox,execution,verification,scope-control,delegation"
---

# Timeboxed Execution

Use timeboxes to make agent work **bounded, visible, and verifiable**. The goal is not to make the agent rush. The goal is to stop scope drift and repeated failure early while preserving enough budget to prove that the result works.

The governing contract is:

```text
bounded goal + explicit done condition + evidence gate + deadline + stop rule
```

A partial result remains partial. A passed test is evidence for what it tested, not proof that the whole task is complete.

## When to Use

Use this skill when:

- a user gives a deadline or asks for a rapid result;
- a task can expand into research, implementation, integration, or debugging;
- earlier attempts became slow, opaque, repetitive, or over-designed;
- several agents or tools must finish before one parent agent can accept the work;
- a risky project should pass a prerequisite or feasibility gate before implementation.

Do not add process to a genuinely simple task. For a small lookup, edit, or check, use:

```text
one goal → shortest verified path → one check → stop
```

## Core Principles

1. **Define done before work.** Describe the observable result and its acceptance evidence, not a list of activities.
2. **Budget verification first.** Reserve roughly 25–35% of total effort for tests, readback, live probes, and reporting; this work may begin before final acceptance.
3. **Front-load the decisive unknown.** Check permissions, availability, entry points, and other Go/No-Go prerequisites before building around them.
4. **Freeze scope before the deadline.** At about 70% of the budget, reject optional additions. At about 80–85%, stop implementation and enter final acceptance.
5. **Stop truthfully.** At the deadline, unverified work is unfinished. Report it; do not silently continue or relabel it.
6. **Use time saved, not scope invented.** Early completion creates verification margin or returns time to the parent plan. It does not authorize new features.
7. **Optimize outcomes, not visible busyness.** Tool calls, delegation, and long reports are costs unless they reduce uncertainty or produce acceptance evidence.

Percentages are defaults, not laws. The invariant is that acceptance receives protected time.

## Completion States

Use explicit states so speed cannot hide an incomplete result:

- **`verified_complete`** — every declared exit condition passed with claim-matched evidence.
- **`partial_verified`** — some bounded outcomes passed, but the main goal or a material risk remains open.
- **`blocked`** — a named prerequisite or external decision prevents further valid progress.
- **`failed`** — the attempted result was checked and did not satisfy the declared exit condition.
- **`stopped_unverified`** — the deadline arrived before the result could be accepted; no success may be inferred.

“Implemented,” “tests passed,” “UI updated,” and “works in the current runtime” are separate claims. Promote the task to `verified_complete` only when the evidence required by the original done condition exists.

When states overlap, classify the main declared goal first. Use `verified_complete` only when every exit condition passes; use `partial_verified` when at least one bounded outcome is accepted but the main goal remains incomplete, and name any blocker, failed check, or deadline separately. Use `blocked`, `failed`, or `stopped_unverified` when no bounded outcome has been accepted and that condition best explains why the goal did not complete.

## Procedure

### 1. Write the execution contract

Before acting, state or internally record:

- **Goal:** one bounded outcome.
- **Done:** what must be observably true.
- **Evidence:** the test, readback, probe, diff, or source that proves it.
- **Budget:** total time and the portion protected for acceptance.
- **Deadline:** a real clock time or a clearly defined elapsed-time limit.
- **Stop rule:** what happens when the phase or project expires.
- **Out of scope:** tempting adjacent work that must not enter this run.

**Completion criterion:** another agent could later classify an observed outcome as `verified_complete`, `partial_verified`, `blocked`, `failed`, or `stopped_unverified` using the contract and obtained evidence.

### 2. Test prerequisites before implementation

Resolve the smallest fact that can invalidate the whole plan:

- required permission or account capability;
- correct repository, branch, file, endpoint, or process;
- reproducibility of the reported failure;
- availability of the official or already-verified path;
- whether a simpler existing solution already satisfies the goal.

If the prerequisite fails, stop at the gate. Do not compensate by building an unofficial detour unless that detour is separately approved.

**Completion criterion:** the prerequisite gate is explicitly Go or No-Go with evidence; any resulting task blocker is recorded separately. Go and No-Go are gate outcomes, not Completion States.

### 3. Split only when a phase has an independent exit

Create phases only for work that cannot safely fit one short loop. Each phase must leave a result that can be judged even if the project stops immediately afterward.

Good phase exits:

- a boundary rule passes named tests;
- a selected account is proven to handle the next real request;
- a UI action is read back from the backend state it claims to change;
- a permission gate is confirmed before any code is written.

Bad phase labels:

- inspect code;
- research options;
- implement feature;
- run tests.

These describe activity, not an accepted state.

**Completion criterion:** every phase has one outcome, one evidence gate, and one local deadline.

### 4. Execute the shortest dependency path

Work on the critical path only:

1. reproduce or inspect;
2. isolate one root cause or decisive unknown;
3. make the smallest justified change;
4. run the narrowest meaningful check;
5. broaden verification only when the narrow check passes.

When a path fails and its prerequisites have not changed, do not repeat it. Record the blocker and switch strategy or stop.

Do not run a sleeping timer process and repeatedly poll it. Record the start and deadline once, work continuously, and check the clock at necessary phase boundaries or acceptance without polling.

**Completion criterion:** every action either reduces a named uncertainty or advances the defined artifact toward acceptance.

### 5. Delegate inside the parent budget

Delegation does not suspend the deadline.

- Give each worker a smaller internal deadline than the parent phase.
- Reserve enough parent time to read the worker's diff or evidence and rerun critical checks.
- Give workers isolated write scopes when concurrent edits could conflict.
- While workers run, do independent acceptance work instead of polling.
- Treat worker summaries as claims until the parent verifies the artifact or external state.

A practical split for a 10-minute implementation phase is about 6 minutes for worker execution and 4 minutes for parent review, correction, and evidence. Adjust to task risk.

**Completion criterion:** the parent can still accept or reject the result before its own deadline.

### 6. Freeze, verify, and report

At scope freeze:

- reject optional refactors, UI polish, extra APIs, and unrelated cleanup;
- keep only work required by the done condition.

At acceptance mode:

- stop adding behavior;
- read the diff or output;
- run tests or live probes;
- verify the exact target after external writes;
- check that exclusions and safety boundaries still hold.

Report five items:

```text
State: applicable Completion State
Completed: outcomes that satisfy the contract
Evidence: exact tests, probes, readbacks, or source checks
Blocked/unfinished: what is not accepted and why
Remaining: bounded next step and realistic time needed
```

**Completion criterion:** the report distinguishes verified completion from implementation progress.

### 7. Stop or request a bounded extension

At the hard deadline, stop all new implementation, retries, exploration, and non-safety external mutations. Perform only the bounded actions necessary to pause safely, make the state observable, and preserve handoff evidence.

Safe-stop actions may include:

- stopping temporary services, tunnels, or tracked child processes when they must not remain active;
- saving or reverting only edits made by this task, and only when the contract explicitly permits that action;
- recording modified files, uncommitted state, and residual processes;
- preserving logs or evidence needed for handoff;
- stating which verification was not run.

Do not use safe-stop as hidden overtime for feature work or optional testing.

Request an extension only when:

- the remaining items are named and small;
- the uncertainty that caused the miss is explained;
- the current artifact is safe to pause;
- the extension includes protected acceptance time;
- work does not resume until approval when approval is required.

Any extension must be explicit before the current hard deadline, approved where required, and establish a new hard deadline. Otherwise, apply safe-stop.

Use this format:

```text
Current accepted state:
Remaining items:
Why the estimate was short:
Extension requested:
Acceptance reserved:
Risk if denied:
```

If the contract says a phase timeout stops the whole project, do not borrow later-phase time. If unused time may roll forward, do so only under the original project rule.

**Completion criterion:** work is stopped or resumed only under an explicit, bounded, and correctly approved rule.

## Evidence Gates

Choose evidence that matches the claim:

| Claim | Minimum useful evidence |
|---|---|
| A bug is fixed | failing reproduction before, passing regression after |
| Declared code change satisfies its done condition | diff readback plus tests or probes that cover the declared done condition |
| Integration works | real boundary call and readback of the target state |
| UI changed backend state | real UI action plus backend or target readback |
| A setting affects the current runtime | one real subsequent operation through that runtime |
| A setting persists | restart or fresh-session readback when persistence is part of the claim |
| Performance improved | same-path before/after under materially comparable conditions; repeat or report variability when magnitude matters |
| Permission exists | current live capability check, not historical state |
| External write succeeded | read back the exact record or remote object |
| Research conclusion is current | authoritative source or sources appropriate to the claim, checked during the task |

Never use activity counts as a substitute for these gates.

## Quality and Efficiency Measures

Evaluate the workflow over several real tasks, not one successful run.

Track:

- accepted outcomes per task;
- user corrections after delivery;
- time to first verified useful result;
- percentage of budget protected for acceptance;
- scope additions after work began;
- repeated attempts with unchanged prerequisites;
- false-completion claims caught during acceptance;
- tasks stopped safely at a failed prerequisite;
- extensions requested, approved, and actually sufficient.

A good timebox may produce an honest No-Go or partial result. That is a quality improvement when it prevents unsafe changes, false claims, or hours of uncontrolled work.

For anonymized validation examples and a small replay rubric, read `references/validated-patterns.md`.

## Pitfalls

1. **Rushing instead of bounding.** A deadline never lowers the acceptance standard.
2. **Process heavier than the task.** Simple tasks need no phase plan, timer process, fan-out, or status ceremony.
3. **Activity-based phases.** “Investigated” and “implemented” are not accepted outcomes.
4. **Acceptance squeezed to zero.** Stop implementation early rather than report unverified work.
5. **Silent overtime.** A near-finished task still requires an explicit bounded extension when the contract requires approval.
6. **Scope reward for speed.** Finishing early does not justify extra features.
7. **Delegation without parent review time.** A worker finishing at the parent deadline is functionally late.
8. **Historical evidence presented as current.** Recheck live prerequisites when they decide Go/No-Go.
9. **Repeating a failed path.** Retry only after a relevant precondition changes or a new testable hypothesis exists.
10. **Tool-count optimization.** Fewer calls are good only when correctness and evidence remain intact.

## Verification Checklist

- [ ] Goal, done condition, evidence, deadline, and stop rule were defined.
- [ ] The decisive prerequisite was checked before expensive work.
- [ ] The task used the simple fast path or independently acceptable phases.
- [ ] Verification time was protected rather than consumed by implementation.
- [ ] Scope froze before acceptance began.
- [ ] Delegated work left parent review time.
- [ ] Failed paths were not repeated without changed prerequisites.
- [ ] Final claims match the evidence actually obtained.
- [ ] Partial, blocked, failed, and No-Go states are labeled honestly.
- [ ] A stopped task left no unexplained service, process, external exposure, or unsafe partial state.
- [ ] Any extension is bounded, justified, and approval-gated when required.
