---
name: resume-supervised-run
description: Inspect and recover the latest or selected CEWP supervised run, including generated progress, pauses, blockers, budgets, ownership, and safe resume actions without losing trusted evidence. Use when the user asks for status, interruption recovery, budget recovery, rollback, cancellation, or what to do next.
---

# Resume A Supervised Run

Read CEWP Core state before suggesting an action. This workflow may perform an explicitly requested non-model control, but it does not silently restart model work.

1. If setup or capability readiness is in question, run `cewp doctor --json` and present actionable remediation.
2. Run `cewp supervise status [run-id] --json`. Omitting the id selects the latest supervised run. This command regenerates `progress.md` from canonical state.
3. Summarize:
   - run and checkpoint status;
   - plan revision and source identity;
   - completed evidence and attempts;
   - latest targeted/full verification and failure classification;
   - execution/worktree owner and backend;
   - consumed and remaining allocations, protected reserve, thresholds, and absolute ceiling;
   - managed usage as observed, estimated range with basis, and unavailable host usage as unknown;
   - pause reason, blocker, and exact next safe action.
4. For `paused-budget-safe`, `paused-budget-unverified`, or `paused-host-limit`, explain the trusted checkpoint and any partial isolated work separately. Never infer that the host limit cleared.
5. Apply a recovery control only with explicit user intent:
   - resume: `cewp supervise resume <run-id> --yes --json`;
   - add approved operations: `cewp supervise add-budget <run-id> --operations <count> --allocation <implementation|repair|reviewer|finalization> --yes --json`;
   - revise an unstarted checkpoint: `cewp supervise revise <run-id> <changed fields> --json`, then require fresh approval;
   - after a verified `budget-safe` pause, propose exactly one next bounded checkpoint with `--goal`, `--scope`, `--verify`, and `--stop`; CEWP seals prior evidence, and `resume` returns to fresh proposal approval;
   - rollback isolated work: `cewp supervise rollback <run-id> --yes --json`;
   - cancel or abandon: `cewp supervise cancel <run-id> --yes --json` or `cewp supervise abandon <run-id> --yes --json`;
   - record a blocker: `cewp supervise block <run-id> --reason "<reason>" --json`.
6. After a non-model control, run status again and stop before the next model operation. Direct the user to the checkpoint workflow when they choose to execute, retry, or review.

Do not rewrite `progress.md`, delete evidence, claim hidden token/credit data, clear a host limit without explicit resume, mutate the source repo, or bypass policy, scope, verification, reviewer PASS, or finalization gates.
