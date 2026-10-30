---
name: z
description: Closed-loop orchestrator for the five-step flow. Senses physical delivery state, advances through steps, and loops until verified complete.
---

# z: closed-loop execution engine

Execute the five-step flow as a continuous state machine.
Do not pause to ask permission. Advance autonomously across all phases until `VERIFIED_COMPLETE`.

## 1. Physical state sensing

Run the physical state validator before taking action:

```bash
ws-delivery-status --json
```

| Physical state | Condition | Mandatory action | Next transition |
|---|---|---|---|
| (Not in worktree) | Primary checkout | Run `init` to claim issue and create isolated worktree | Enter worktree, sense state |
| `UNKNOWN` | `ws-delivery-status` exited 4: git or GitHub could not be read | Fix the cause in `reasons[]`; re-run. Never read it as a pass | Sense state |
| `DRAFT` | Working tree dirty | Implement minimal logic; verify focused tests pass | Run `git commit`, sense state |
| `LOCAL_VERIFIED` | Committed, unmerged | Invoke `auto` to push branch and open pull request | PR opened, sense state |
| `IN_REVIEW` | PR open | Wait for CI events, resolve review feedback, merge PR | PR merged, sense state |
| `CODE_LANDED_STAGE1` | Merged on `main` | Run `ws-delivery-status --assert-complete --reality-probe "<CMD>"` | Probe passes (exit 0) |
| `VERIFIED_COMPLETE` | Merged + reality verified | Run `close` cleanup; advance to next phase or conclude | Next phase or done |

A clean checkout of `main` reports `CODE_LANDED_STAGE1` for prior tasks. The tool has no state for a task that is not begun. Do not probe unbuilt work; run `init` to claim an issue and begin the task.

## 2. State branches

### Branch A: `DRAFT` (Working tree dirty)
1. Apply changes per `ssot`. Do not add failing items to allowlists ("exclusion is not resolution").
2. Run focused tests per `smoke` (`pytest <file>::<test> -x`).
3. Commit with an ASD-STE100 conventional commit message and re-sense state.

### Branch B: `LOCAL_VERIFIED` (Committed, unmerged)
1. Verify HEAD commit is pushable. Open a pull request using `auto` and re-sense state.

### Branch C: `IN_REVIEW` (PR open)
1. Trigger the review and merge gate tool (`ws-pr-gate --merge` or platform equivalent).
2. Bind the PR with `ccd_pr` and wait for `ci-monitor-event`. Hosts without `ccd_pr` run `ws-pr-gate` in the background. Never run a wait loop or a watch command in the foreground.
3. Run long test suites with `run_in_background`. Resolve actionable feedback and re-sense state.

### Branch D: `CODE_LANDED_STAGE1` (Merged on main, reality unverified)
1. Formulate a read-only, non-mutating Business Reality Probe `<CMD>` verifying live behavior.
   Prohibit bare `echo`/`printf`, trivial prints, mutating commands, and active exemptions.
2. Execute gate: `ws-delivery-status --assert-complete --reality-probe "<CMD>"`.
3. If `ws-delivery-status` exits 0 (`VERIFIED_COMPLETE`), proceed to Branch E. If it exits 3, fix the probe and re-run it.

### Branch E: `VERIFIED_COMPLETE` (Physical proof achieved)
1. Invoke `close` to record evidence and clean up.
2. If subsequent phases exist, do not pause or ask permission; begin next phase immediately.

## 3. Loop invariants

1. **Continuous Autonomous Drive (Zero Decision Offloading)**: Never ask permission between phases. The agent owns technical execution end-to-end. Stop only for Stage 3 production deploy.
2. **Multi-Phase Goal Progression**: When goals require multiple phases, chain them sequentially through the state machine until all goals reach `VERIFIED_COMPLETE`.
3. **Zero self-grading**: Completion requires `ws-delivery-status --assert-complete --reality-probe '<cmd>'` to exit 0 (`VERIFIED_COMPLETE`). Without `--assert-complete`, exit 0 means only Stage 1 Landed.
4. **Anti-Exclusion Invariant**: Exclusion is not resolution. Probes with active exemptions fail.
5. **Compaction resilience**: When resuming after disruption, run `ws-delivery-status --json` to recover state without asking the user what to do.
