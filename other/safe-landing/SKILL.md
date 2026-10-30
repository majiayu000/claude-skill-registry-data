---
name: safe-landing
description: Appa's safe landing for shipping a green stack. Appa never sets down until he has seen the ground is solid. Use for "land it", "ship the stack", "merge when ready", "merge it", or landing PRs after `long-flight` reports merge-ready. Verifies each PR independently, lands only the contiguous verified run from the root bottom-up under a head guard, and reads back every landing. Needs the user's landing authority.
---

# Appa's safe landing

Appa does not land on ice he has not tested, because the whole team is riding. Green CI is not solid ground. You own what lands. Verify each PR independently, land only the verified run from the root, then keep your hands off the stack. Landing needs the user's landing authority, and you confirm each landing before the next starts.

On Codex, read [avatar-mode/references/codex.md](../avatar-mode/references/codex.md) for tool equivalents.

Read [references/merge-safety.md](references/merge-safety.md) before you merge, arm, rebase, or retarget anything. The `ship-pr` and `watch-pr` commands below live at `../../tools/watch-pr/` in this plugin. Both carry a `bun` shebang, so run them directly by full path when they are not on PATH.

## Steps

1. **Resolve the forge, then verify each PR independently before it lands.** GitHub CLI (`gh`) is the default. If `command -v origin` succeeds and Origin can resolve the repository, use `origin pr` for every PR operation. Otherwise stay on `gh` and record the fallback. Never require Graphite (`gt`).

   Capture the affected chain bottom to top. Record each head branch and SHA, each base branch and SHA, and the intended destination repository and branch. Leave unrelated PRs alone. Inspect pending merge requests on entry. Cancel and read back any that lack the verification gates in step 4 before a lengthy review.

   Dispatch one verifier per PR, each in its own worktree. Send Katara on Suki's model from the avatar-setup sheet, as `avatar-mode` sets for every verifier, never the character who wrote the code. The verifier runs the change the way a user would, parent against head, through the project's driver (its own verify skill when it has one, made with `vital-signs`, otherwise Claude Code's `run`). It posts `PASS`, `PASS+NOTES`, or `FAIL` on that PR. Only a verdict from an agent that did not write the code counts, because an author checks what it meant to build. Green CI and an approving bot review are not verdicts, because neither runs the change as a user would. Record each verdict's head SHA, base SHA, base branch, and the stable `git patch-id` of the base-to-head diff.

   When you run as a dispatched character, you cannot dispatch verifiers. Record `BLOCKED: independent review` in the todolist, keep landing closed, and report to your caller which verdicts exist and which are missing. Never count your own check as the verdict.
2. **Land only the contiguous verified run rooted at the bottom.** Walk up from the lowest unmerged PR and stop at the first one without `PASS` or `PASS+NOTES`. The PRs below it are the run, and the top one is the ceiling. A verified PR above an unverified one waits, because it cannot land without the code below it. A PR whose branch neither holds nor needs that code can move onto trunk and land on its own. It needs a fresh verdict first, because its old verdict ran with that code beneath it and trunk does not have it.
3. **Re-check that the verdicts still describe the code.** A verdict covers a patch, and a chain rebase moves every PR above it to a new SHA without failing any check. Compare `git patch-id` at the verdict SHA with the current head before you trust an older verdict.
   - When the patches differ only in tests, docs, or lint config, a lane's result stands if what it ran builds the same at both SHAs apart from noise. Noise is a difference that also shows up between two builds of the verdict SHA, or an embedded commit SHA. Report each kind of noise with its files, so a reader can check the call. The change itself still gets fresh checks and a review, because the old verdict never saw it.
   - A lane with no build output, such as a dev server, cannot show this, so rerun it. Re-verify anything else that drifted.
   - A matching patch-id keeps a review only after you check that it applies to the new destination and dependencies. Re-verify changed behavior or uncertain applicability. Rerun checks and mergeability after every rewrite or retarget.
4. **Land bottom-up, one PR at a time.** Always merge the run's lowest unmerged PR under a service-enforced head condition, because a last-second read without one leaves a race.
   - On GitHub, use `gh pr merge <pr> --repo <owner/repo> --squash --match-head-commit <verified-head>`. Confirm the destination right before the request, since the head guard does not guard the base.
   - Use `origin pr merge <pr>` only once Origin's CLI proves an equivalent server-side head condition. Otherwise stop at merge-ready and report the limitation. On Origin the plain command also merges every PR below the one you name.
   - On GitHub, a PR whose base is still its parent's branch merges into that branch, not trunk.

   Read the PR back for the result (`origin pr view <pr>` or `gh pr view <pr> --json state,mergedAt,baseRefName`). A merge command can report success when a merge queue only queued the PR, and a requested auto-merge is not a merge. A landed PR reads merged with trunk as its base, not its parent's branch. Then fetch the destination and confirm the merge commit is in its history. Stop the chain if anything contradicts the verified landing.

   Arm `--auto` (Origin merge-when-ready or GitHub auto-merge) only on a PR whose verdict covers its current head, because it lands whatever head is ready. Arm it only behind repository rules that enforce the verdict and required CI on the revision that will land. A queue-required branch can turn a plain merge into queue admission, so it takes the same rules. Never change protection settings or use `--admin` to get there.

   Before any push, rebase, or base edit, run `ship-pr inspect` and `ship-pr cancel-pending` from the safety reference for every PR the change can affect, and require a `cancelled` result. If cancellation fails, state is unavailable, or a PR merges meanwhile, stop and reconcile actual state first.

   After a merge lands, retarget the PR whose base was the merged branch to trunk (`origin pr edit <pr> --base <trunk>` or `gh pr edit <pr> --base <trunk>`). Replay only its own commits onto the merge result from the recorded old parent boundary, as in the safety reference, and push with a lease on the remote SHA captured before the rewrite. The verdict covers the patch, not its commits, so step 3's patch-id rule decides whether the verdict survives. Merge it once its checks pass and its verdict survives.
5. **Leave the stack alone while it lands.** Step 4's move of the next PR is the only change to a branch or base, because a merge lands whatever its branch and base hold at that moment, verdict or not.
   - On GitHub, watch the run with the queued watcher from `long-flight` (`watch-pr --queued-stack --stack-prs <bottom-to-top>`). On Claude Code run it under `/loop` in dynamic mode until it reports `COMPLETE` at the ceiling. On Codex, call it in the turn and let it block.
   - On Origin, re-read the current PR with `origin pr view <pr> --checks` each time `origin pr checks <pr> --watch` returns, until the ceiling reads merged.

   A base that moves to trunk when its parent merges is expected, not damage to repair. If a merge stalls, find out why before you change anything. At each wakeup, compare the landing revision, including the base OID, with the approved record through `ship-pr inspect`. Cancel a pending request whose evidence no longer applies.

   The watcher owns GitHub blocker classification. Preserve its `BLOCKER` reasons and route them through `long-flight`. Conflicts and `behind-base` go to the topology owner, threads and CI to the PR owner, and human approval gates to a wait. Do not rearm an unchanged blocker. `WAITING`, including `merge-queue`, is non-terminal. Pending checks are neither failure nor completion. Diagnose `TIMEOUT` and `status-query` blockers, since unknown state never permits a merge.
6. **Stop at the ceiling.** Extending the run takes new verdicts, so it is a new pass through step 1.

## Rules

- Merging is irreversible. Land only on the user's explicit request to merge, land, ship, or "merge when ready". Babysitting never grants it.
- Never use `--admin`, change branch protection, or bypass a required queue.
- Never treat a merge command's exit code as the landing. The readback is the landing.

## Reply

The verified run and its ceiling. Each PR's verdict and who produced it. What was armed or cancelled, and how you read it back. What landed and how you confirmed it. Any unresolved state or service limit, and what the next gap needs.
