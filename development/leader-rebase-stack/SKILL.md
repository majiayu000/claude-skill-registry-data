---
name: leader-rebase-stack
description: >-
  Maintain your contributions to a moving-leader leaderboard as an ordered stack of
  idempotent patches (stack/NN-slug/) that rebase onto whatever submission currently
  leads, with a background leader watcher, a restack that scores the leader first,
  and a submission gate tied to the live board (submit only when the stack beats the
  leader by a written margin at submission time). Use on any benchmark where rivals
  keep landing rows while you build.
whenToUse: Running or auditing a multi-day campaign on a contested leaderboard; deciding when a stack is worth submitting; rebuilding your work after a rival lands a new leader
---

# Huckepack (leader-rebase-stack)

Distilled from jackylee0424's public shor-ecdlp-contest lab (MIT, commit 15db543):
his patches survive leader changes because they were never attached to a checkout —
only to the *idea* of the current leader.

## Each contribution is a patch, not a checkout

```
stack/<NN>-<slug>/
  apply.sh    # idempotent; edits only the bench's editable paths; no prior state
  check.sh    # optional fast assertion that the patch is present after apply
  src/        # sources/templates the apply script installs into tracked files
  PATCH.md    # what it changes, expected Δ, proof anchors, owner brief, last leader it applied to
  ENABLED     # present = included in restacks; delete to park
```

- `apply.sh` exit codes: **0 = applied, 3 = absorbed/superseded by the leader (skip),
  anything else = broken (stop the restack)**. When a patch exits 3, update its
  PATCH.md and the lever ledger — the leader ate your lever, which is also a win.
- Package only into files the leader already tracks; new untracked files fail source
  gates that scan the whole filesystem.
- One builder agent per checkout (`bench`, `bench-m`, `bench-c`…) so parallel work
  never fights over one working tree.

## Restack on every leader change

1. A background watcher polls the board and exits on change
   (`watch-leader.sh <known-best>` every ~15 min; on change it prints the new best
   and its source commit).
2. `restack.sh <leader-commit>`: reset a dedicated restack checkout to the leader,
   **build and score the untouched leader first** (you need its real number, not its
   README number), then apply each ENABLED patch in NN order, run the boundary and
   axiom gates, score, and write a timestamped report with the % cut.
3. Parked and absorbed patches are recorded in the report, not silently dropped.

## The submission gate is tied to the live board

Submit only when the stacked score beats the current leader by a **written margin
(his: >10%) measured at submission time** — not the margin you had when the build
started. A board that moved while you built is a reason to restack, not to submit.
