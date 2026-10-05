---
name: execute-plan
description: >-
  Execute an approved plan from thoughts/plans/ to completion — every phase, every check, every
  acceptance criterion — and stop only when DONE or BLOCKED. Use when someone says "execute the plan",
  "implement the plan", "build it" after a plan was approved, "start building", or points at a file in
  thoughts/plans/. Medium/large work without a plan → /dev-skills:write-plan first.
---

# Execute Plan

Carry an approved plan through to working, verified code. The plan is a contract: you either satisfy it or show exactly why it can't be satisfied.

## Input

A plan in `thoughts/plans/` (from `/dev-skills:write-plan`). No plan and the work is medium/large → write one first. No plan and the work is small and clear → state the acceptance criteria in one line each, then run under the same contract.

## The Contract

Approval of the plan is the only gate. From then on you own delivering it, and a run ends in exactly one of two states:

**DONE** — every phase implemented; every phase check green; full test suite, typecheck and lint with no new failures against the baseline you recorded at the start; every acceptance criterion verified with cited evidence. For UI criteria, that means you ran `/dev-skills:qa-test` yourself and it passed.

**BLOCKED** — the contract can't be satisfied without something only the user can provide:
- a permission, credential, or access you don't have (and the plan's pre-flight blockers didn't cover)
- a harness that can't be made runnable by you — a check needs a human step with no bypass
- a plan premise that turns out false, with no resolution that stays within the plan's intent
- a risky or irreversible action that needs explicit confirmation: anything against shared, staging or prod environments, or outward-facing (pushing, opening PRs, deploying, messaging). Local/dev DB migrations, resets and seeds the plan's checks call for are in-contract.
- the same check still failing after 3 genuinely different fix attempts

Before stopping BLOCKED, finish every item that doesn't depend on the blocker.

**Everything else is yours to resolve.** Renamed symbols, moved files, different signatures, a missing import, a choice between two reasonable implementations, a scope-adjacent decision where one option clearly fits the plan's intent — decide, record it under `## Deviations` in the plan file (what the plan said, what you did, why), and keep going.

### How turns end

A message without a tool call ends your turn, and the work stops there. While the contract is open, don't end a turn in any of these ways:

1. A summary of what's done that announces the next step instead of taking it.
2. An offer to continue "unless you'd prefer otherwise".
3. A list of decisions for the user when none of them blocks the remaining work — decide, log under Deviations, continue.
4. Reporting because a phase finished, a milestone landed, or the turn got long.

Status notes are welcome — put them in the same message as your next tool call. Before any message without a tool call, read the plan's checkboxes and your todo list: open items and no stated blocker means keep working. Background work whose result you depend on (test runs, sub-agents) has to finish and be read before you can call the work DONE. Long-running servers are fine — note them or stop them.

## Process

### 1. Load the contract

Read the plan completely, the shape doc it links (acceptance criteria live there), and the files each phase touches. Build a todo list: one item per phase, plus final verification and each acceptance criterion.

Resuming? Existing `[x]` marks in the plan are done — start from the first unchecked item; re-verify earlier work only if something contradicts it.

Verify the plan's **Pre-flight blockers** are cleared (key present, seed runs, auth bypass works) — plus browser MCP reachability if there's a UI layer or UI criterion. Record a baseline of the test suite, typecheck and lint. If a pre-flight item isn't in place, that's BLOCKED before any code — report it now, not after three phases. Pre-existing failures in the baseline are listed in the report, not fixed.

### 2. Execute phase by phase, layer by layer

For each phase:
1. **Implement** the changes, following existing patterns.
2. **Prove** — run the phase checks. They are agent-runnable commands; if one isn't, make it one (a script, a curl, a seeded route) rather than skipping it.
3. **Fix** until green. Don't start a layer until the layer beneath it is proven — a UI bug is never debugged on top of an unproven API.
4. **Record** — check the boxes in the plan file, update todos, log any deviation.

Then move straight to the next phase.

### 3. Final verification

- Full test suite, typecheck, lint.
- Every acceptance criterion from the shape doc, each with evidence: command output, query result, or qa-test finding.
- UI criteria → run `/dev-skills:qa-test` in agent mode. It fixes and re-tests up to its own limit; a criterion it can't get green is a BLOCKED item with its evidence.

### 4. Report

```
Contract: DONE | BLOCKED

Acceptance criteria
1. [criterion] — ✓ [evidence: command/output, qa-test result, row]
2. ...

Deviations
- [plan said X → did Y — why]

Defense deltas
- [decisions made during implementation the developer hasn't seen: a new table, a changed
   failure mode, a different library — in plain words]

(BLOCKED only)
Blocker: [what, with evidence]
Needed from you: [the specific thing]
Already done: [phases/items complete]
```

## Rollout discipline

Check the plan's Rollout & Rollback block before coding:

- **"Direct deploy, no flag"** — don't introduce a flag mid-implementation. If the change turns out riskier than planned (critical path, bigger blast radius), that's a premise change: log it and, if it breaks the plan's intent, BLOCKED.
- **"Flag"** — one named flag for the whole feature, at the user-perceived boundary. No per-phase or per-layer flags.
- **"Expand-contract"** — execute through expand + migrate, then end DONE with "contract phase pending deploy" in the report. The contract phase needs the expand deployed first, so it never runs in the same session; never collapse expand and contract into one PR.
- **"Both"** — flag the consumer, expand-contract the schema/API. Flags wrap code, not storage.

See [write-plan/references/rollout-primitives.md](../write-plan/references/rollout-primitives.md) for the full decision tree.

## Working guidelines

- Read before editing — full files for small ones, targeted sections for large ones.
- Follow the codebase's existing patterns; consult [references/software-design-philosophy.md](references/software-design-philosophy.md) and watch for shallow modules, information leakage, pass-through methods.
- Keep changes inside the plan's scope — no unrelated "improvements".
- Sub-agents for exploration (reading tests and related modules in parallel), not for writing the code.
- Acceptance criteria are the user's: if one looks wrong, verify what's specified and flag it in the report; don't edit it.

## Handoffs

- DONE on customer-facing work → offer `/dev-skills:explain` on the shipped diff, seeded with the Defense deltas, so the developer can explain and defend what shipped.
- BLOCKED because the plan itself is wrong → `/dev-skills:write-plan` with the evidence.
