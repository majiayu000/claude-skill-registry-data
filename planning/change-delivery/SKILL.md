---
name: change-delivery
description: Use to deliver approved repository changes from a saved Issue plan through branch preparation, PR, review, CI, merge, and post-integration main verification. Do not use for planning alone or read-only review alone.
---

# Deliver approved changes to main

Inherit execution approval and the saved, retrieved, and verified Issue plan. An Issue alone is not execution approval. Do not recreate, resave, or reapprove the same approved purpose and success conditions. `docs/` refers to the working repository.

## Scope and plan

- Treat a clear change request, including an instruction to implement an agreed plan, as execution approval. For consultation or planning alone, stop at the requested deliverable. Honor explicit endpoints such as “through PR.”
- Before editing, inspect target instructions and relevant files, dependencies, existing checks, and other sessions' work. Search existing Issues and PRs. If no Issue covers the change, save a plan stating purpose, success conditions, affected scope, order, validation, and completion conditions. Assign the confirmed requester and choose labels from their actual descriptions.
- Follow [Record content](references/repository-adoption.md#record-content) and [Publish and verify records](references/repository-adoption.md#publish-and-verify-records). Retrieve the saved plan, verify body agreement and rendering, and present its URL and content before implementation. Unconfirmed saving is incomplete; resume from verified state without duplicate records.
- Continue adjustments to files, procedures, decomposition, or order within the approved purpose and success conditions. Record and present concrete proposals before changing purpose, outcomes, acceptance conditions, external impact, or authority; obtain the necessary confirmation before affected work. Reducing agreed outcomes also requires confirmation.
- Preserve authorization across continuation. Plans, proposals, and silence alone do not authorize execution. Confirm permission before publishing unpublished information outside an already approved draft and destination. Do not extend approval to unrelated work, extra permissions, costs, or global settings; hold only affected operations when required access is unavailable.

## Material to read at each stage

Do not repeat completed stages; read material needed for the current stage. Resolve bundled links relative to the referring file.

| Stage or condition | Material |
| --- | --- |
| Work protection and branch preparation before editing, execution of approved decomposition | [Branches and integration units](references/branches.md) |
| Drafting commit messages, staging, committing | [Commit messages](references/conventional-commits.md) |
| Start of repository change work; local change-record gaps or adoption requests | [Repository adoption](references/repository-adoption.md) |
| Writing Issue/PR descriptions and checking publication | [Record content](references/repository-adoption.md#record-content), [Publish and verify records](references/repository-adoption.md#publish-and-verify-records) |
| PR, review, CI, merge, main verification and cleanup, recovery after failure | [Review and merge](references/review-and-merge.md) |
| Issue plans, execution approval, or changes to the agreed scope | [Scope and plan](#scope-and-plan) |

## Continuation and completion

- For planning-only requests, stop after saving, verifying, and presenting the requested plan; do not proceed to branches, edits, or PRs before approval. Apply [Scope and plan](#scope-and-plan) to explicit stop conditions and changes needing confirmation.
- With execution approval and confirmed saving, check branches, diffs, worktrees, other sessions' responsibilities, and required public-main checks before preparing a branch. Do not ignore conflicts, inability to verify, or failing main; protect and recover work.
- Within the approved scope, proceed through implementation, validation, commits, push, Draft PR, required CI, conflict resolution, ordinary review of a stable latest HEAD, and squash or merge-commit merging as permitted by the target repository. Do not use rebase merging. If findings or other changes update HEAD, check required CI and conflicts on the new HEAD before re-review. Do not reinterpret pair checks as ordinary PR review. Keep code, tests, and documents consistent with the approved behavior and target conventions; read-only review alone does not authorize fixes or delivery.
- When evaluating changed skill judgments, use reproducible inputs and expected judgments. If independent simulated execution is selected or separately required, compare before/after with the same inputs and criteria, honoring repository-specific exclusions. Format checks or keyword matches alone do not prove judgment quality.
- Report actual validation status; choose whether and how to execute checks unless independently required, without making every planned check a gate. Compare the final diff with the request, related functionality, documents, paths, and commands. Commit in small verifiable units, and push after a small completed change and commit. Use TDD cycles when selected; do not imply unperformed validation succeeded.
- During long work, share findings, remaining issues, and next work. Investigate failure causes and evidence-based alternatives; do not repeat the same operation without reason. State reasons and targets when user decisions or additional permissions are needed.
- Do not finish at PR-side success; confirm required validation and distribution at the actual public-main SHA, and own synchronization and branch cleanup. Do not treat failures or unverified results as success; prioritize recovery before resuming subsequent work.
- Report the Issue and PR, outcomes, validation and review, merge, main verification, synchronization, branch cleanup, and remaining issues. Do not treat unexecuted or unobtainable results as success; distinguish incomplete scope from conditions for resumption.

Record observed improvement opportunities and small proposed experiments in existing or follow-up Issues only within publication approval, preserving evidence, scope, and how to check the next relevant task. Search prior records, distinguish implementation from observed improvement, and retain follow-up tracking when results remain unverified. Do not leave current delivery incomplete waiting for subsequent improvements, or begin separate changes based solely on improvement proposals.
