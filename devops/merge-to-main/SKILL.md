---
name: merge-to-main
description: Review and merge a delivery branch directly into the main branch with local quality gates, native harness reviews, exact-SHA protection, and safe Git completion. Use when the user wants a locally reviewed dev-to-main or branch-to-main merge without a pull request, remote CI wait, deployment monitoring, health polling, or release tagging.
---

# Merge to Main

Run one locally reviewed direct merge. Keep the workflow semantics here and use the active
harness's native shell, review, delegation, confirmation, and notification capabilities.

Do not build a scheduler, sandbox runtime, report protocol, or subprocess-based agent adapter for
this workflow. Native reviews may run concurrently when the harness supports it; otherwise run the
same independent review lenses sequentially.

## Preserve the contract

- Default to `dev` as the source branch, `main` as the target, and `origin` as the remote. Accept
  explicit overrides when the repository uses different names.
- Treat `--dry-run`, `--effort <low|medium|high|max>`, `--discard-state`, and
  `--skip-deploy-health` as portable intent even when the harness exposes arguments differently.
- Merge without a pull request. Stop after the target branch is pushed. Do not wait for remote CI,
  monitor the deployment created by the push, run a post-merge health loop, or create a release tag.
- Pin the source SHA before review and merge that exact SHA. Never merge a source ref that advanced
  after review.
- Never force-push, resolve merge conflicts on the target branch, or leave the session checked out
  on a different branch than it started from.
- Report completion only after the remote target contains the merge and the starting branch is
  restored.

Read [the portability map](references/portability-map.md) when authoring or changing a harness
binding. Read [recovery](references/recovery.md) when a phase fails or a resumed run may be stale.

## 1. Resolve and preflight

1. Read repository instructions and determine the repository root, starting branch, source branch,
   target branch, and remote.
2. Require a clean working tree. Do not absorb, stash, or commit unrelated changes as part of the
   merge workflow.
3. Fetch the remote and resolve immutable source and target SHAs.
4. Require the local source to match the remote source unless the user explicitly selected another
   reviewed ref.
5. Require at least one commit in `target..source` and check mergeability without mutating the
   target branch.
6. Capture the starting branch so it can be restored on every exit path.

For a dry run, stop after printing the source and target SHAs, commit and diff summaries, detected
quality gates, review lenses, confirmation policy, and planned merge command.

## 2. Summarize the release

Build a concise summary from `target..source`: commit count, changed files, churn, notable features,
fixes, infrastructure changes, and archived feature/spec identifiers when the repository records
them. This summary informs review scope, the merge gate, the merge message, and the final report; it
is not a second workflow ledger.

## 3. Check current health

Before expensive validation, perform only cheap checks that the repository already supports:

- Read the last known deployment state once. Halt only on a definitive unhealthy result. Unknown,
  unavailable, or unconfigured deployment state is non-blocking.
- Run the repository's existing smoke command when one is declared.
- `--skip-deploy-health` bypasses only a definitive unhealthy-deployment halt. It never bypasses
  smoke tests, local quality gates, review, or SHA protection.

Skip capabilities that the repository does not define. Do not invent a deploy detector or poll a
deployment service.

## 4. Run local quality gates

Use the repository's existing gate command or documented validation sequence. Prefer one canonical
gate entrypoint when present. At minimum, honor the repository's lint, typecheck, build, and test
contract. Halt on failure and include the failing command and useful output; do not review broken
code as merge-ready.

## 5. Review the pinned diff

Review `target...PINNED_SOURCE_SHA`, not a moving branch name.

1. Run a correctness lens over the complete diff. For large changes, partition by coherent path or
   subsystem so every changed file remains covered.
2. Run one architecture lens over the complete diff.
3. Classify findings as `blocking` only for concrete correctness, security, data-loss, compatibility,
   or architectural failures that make the merge unsafe. Classify cleanup and optional simplification
   as `advisory`.
4. For each proposed blocker, perform a focused independent re-check against the cited code and
   surrounding behavior. Keep only confirmed blockers. A missing or inconclusive re-check does not
   clear a blocker.
5. Halt when confirmed blockers remain. Report file, location, impact, and the evidence needed to
   resume. Otherwise carry advisory findings into the final report.

Use the harness's native review or subagent primitive. Structured output is helpful but no
cross-harness JSON schema or temporary-file protocol is required.

## 6. Apply the merge gate

After gates and review pass, show the source, target, commit count, feature/spec count, and advisory
count. Auto-proceed only for a small batch of at most 10 commits unless repository policy is
stricter. For a larger batch, use the harness's native user-confirmation primitive and require an
explicit merge decision.

The user's original invocation authorizes the documented small-batch auto-proceed behavior. A
large-batch confirmation is a risk gate, not a request to redesign the workflow.

## 7. Merge the reviewed SHA

1. Serialize target-branch mutation with the repository's existing merge lock or lease when one is
   available. Do not create a new global lock service. Without a repository lock, keep this phase
   synchronous and revalidate immediately before mutation.
2. Fetch again and require the live remote source SHA to equal `PINNED_SOURCE_SHA`.
3. Check out the target branch and update it from the remote without creating an unreviewed merge.
4. Merge `PINNED_SOURCE_SHA` with `--no-ff` and a concise message containing the release summary and
   review counts.
5. On conflict, abort the merge, restore the starting branch, release any lock, and halt. Resolve
   conflicts on the source branch before retrying.
6. Push the target branch normally, verify the remote target contains the resulting merge commit,
   release any lock, and restore the starting branch.

## 8. Complete and report

Report the source and target, pinned reviewed SHA, merge SHA, gate commands and outcomes, review
counts, shipped summary, push verification, and restored branch. State explicitly that no pull
request, remote CI wait, post-merge deploy monitoring, health polling, or tag was performed.

Resume only from evidence bound to the same repository and exact source/target SHAs. Harness-native
checkpoints may cache completed phases; otherwise safely rerun read-only phases. Never let cached
state bypass SHA validation, quality gates after changed code, confirmation, or remote push proof.
