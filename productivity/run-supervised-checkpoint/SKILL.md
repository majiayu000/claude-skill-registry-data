---
name: run-supervised-checkpoint
description: Approve, execute, verify, repair, continue, independently review, preview, or explicitly finalize the current CEWP supervised checkpoint through Core gates. Use when the user asks to run or continue an already proposed CEWP checkpoint.
---

# Run A Supervised Checkpoint

Use canonical JSON from `cewp supervise`; generated Markdown is a view, not mutable state. Keep the ChatGPT/Codex host in the operator role while CEWP owns the isolated child worktree.

1. Run `cewp supervise status [run-id] --json` and state the current run/checkpoint status, plan revision, owner/backend, latest evidence, budget consumption, warnings, blocker, and next safe action.
2. Perform no more than one CEWP-controlled model operation per invocation. Local verification commands do not count as model operations, but their approved limits still apply.
3. Follow only the transition matching canonical state:
   - `proposed`: show the plan and run `cewp supervise approve <run-id> --yes --json` only after explicit approval. Stop before dispatch.
   - `approved/ready`: if the operator explicitly requested a Codex task class, model, or effort, record it first with `cewp supervise effort <run-id> --operation implementation --task-class <class> [--model <model>] [--effort <effort>] --yes --json`. Never infer model or effort from the class. Then run `cewp supervise execute <run-id> --yes --json` only after explicit execution approval. If dispatch reaches `verifying`, run `cewp supervise verify <run-id> --json`; then stop at the verified, repair, paused, or blocked result.
   - `needs-repair/repair-ready`: explain the failure signature and remaining repair allocation. Record any explicitly requested repair-specific Codex selection through `cewp supervise effort ... --operation repair ... --yes --json`; do not reuse or change implementation settings implicitly. Run `cewp supervise retry <run-id> --yes --json` only when the user explicitly chooses retry, then run local verification and stop.
   - `checkpoint-complete/verified`: offer final review or a safe pause for one manually bounded next checkpoint. For final review, record any explicitly requested independent-review Codex selection through `cewp supervise effort ... --operation reviewer ... --yes --json`, record `cewp supervise continue <run-id> --json`, run `cewp supervise review <run-id> --yes --json`, and stop at the reviewer decision. For more work, hand off to the resume workflow without dispatching another model operation.
   - `review-passed`: run `cewp supervise receipt <run-id> --json` to preview the receipt. Do not finalize in the same step unless the user already gave explicit finalize intent after seeing equivalent receipt facts.
   - `ready-to-finalize`: run `cewp supervise finalize <run-id> --yes --json` only after explicit finalization approval.
   - any `paused-*` or `blocked`: do not dispatch. Present Core recovery actions and hand off to the resume workflow.
4. Treat any nonzero command, scope warning, failed verification, missing reviewer decision, `REQUEST_CHANGES`, `BLOCK`, exhausted allocation, host limit, or ownership mismatch as a closed gate.
5. Report the resulting canonical status and exact next safe command. Never label dispatch completion, partial files, or a reviewer request as checkpoint success.

Do not edit the managed worktree from the host task, bypass `--yes`, borrow protected allocations, automatically add budget, switch backend/provider, merge, push, publish, tag, or release.
