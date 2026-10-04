---
name: sflow-cancel
description: Cancel an active governed Story, preserve all generated artifacts and approvals, record the human reason and identity, commit and push the decision, and move the Story to Archived.
disable-model-invocation: true
argument-hint: "[WORK-ID] --reason 'explanation'"
---
# Cancel and archive governed work

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

This is an explicit human lifecycle decision, not an artifact-generation task.

1. Run `singularity-flow status [WORK-ID]` and show the current phase, generated artifacts, approvals, branch, and publication state.
2. Require the human to provide a non-empty cancellation reason. Never invent or infer the reason.
3. Explain that cancellation stops the lifecycle but preserves the Story branch, state, artifacts, approvals, telemetry, and Git history. It does not claim successful completion and does not delete files.
4. Ask the human for explicit confirmation of the exact Work ID.
5. Run `singularity-flow cancel <WORK-ID> --fetch --reason "<exact reason>" --confirm <WORK-ID>`.
6. Stop on a stale/diverged branch, pending publication, closed Story, already-cancelled Story, or confirmation mismatch. Never reset, rebase, force-push, or delete the branch.
7. If cancellation reports remaining uncommitted paths, explain that a new Story will remain blocked until they are preserved. Run `singularity-flow cancel <WORK-ID> --release --json` to preview the exact paths, stash consequence, and recorded base branch. Ask separately whether to apply that release; never infer this authority from the cancellation confirmation.
8. Only after explicit release approval, run `singularity-flow cancel <WORK-ID> --release --apply --confirm <WORK-ID> --json`. Report the durable stash SHA and recovery command exactly. The archived branch and governed history remain intact.
9. Report the cancellation reason, human Git identity, governed agent audit context, phase, commit, push, and that the Story is now visible under **Archived** in VS Code.
