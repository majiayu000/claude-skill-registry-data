---
name: verify
description: Use when a plan's tasks are landed and its branch needs the gate before a pull request, the scripted checks, the branch review and repairing what it finds. Not for landing a task, which build owns, or a decided change with no plan.
argument-hint: "[plan path]"
effort: high
---

# Verifying a branch

## The loop

1. **Run the gate.** Run `node "${CLAUDE_SKILL_DIR}/scripts/verify.mjs" --plan <plan path> --root <checkout> --base <base>`.
   - It runs each landed task's own Proof command, except one equal to the gate command, or running the test suite (`npm test`, `node --test`) under the default `npm run check` gate.
   - It then runs the gate once: the first backticked command of the plan's `Success criterion`, else its `Land gate:`, else `npm run check`.
   - `Land gate: none` prints `UNRUN success-criterion`, not `PASS`.
   - It runs the stray-path check against `base`.
   - It prints one `REVIEWER: review-branch` or `REVIEWER: review-branch-deep` line, then one `DONE` or `OPEN` line per task and one `MANUAL` line per `## Manual checks` bullet.
   - A `FAIL` or `STRAY` line ends the turn with the script's own report, and nothing here reruns its checks.
2. **Review the branch.** Dispatch the `exo:review-branch` agent, or `exo:review-branch-deep` when the `REVIEWER:` line prints that name, with no model override.
   - Pass the plan path, branch, checkout and base.
   - Pass the code standard path from `CLAUDE.md` or `AGENTS.md`, else `${CLAUDE_SKILL_DIR}/../route-skills/references/code-standard.md`.
   - Pass `<checkout>/.exo/` as the implementer report directory and `<checkout>/.exo/branch-review.md` as the findings path.
   - `BLOCKED` ends the turn with its report.
3. **Repair the findings.** A `FINDINGS` verdict with `fix=1` or more goes to the `exo:fix-review` agent, with no model override, with the text of `../build/review-fixer-prompt.md` and the report path.
   - At `fix=0` make no `exo:fix-review` dispatch, no rerun and no fix commit; list the report findings in the turn's report and go to step 4.
   - Then rerun step 1's `verify.mjs` command.
   - After that rerun, a `FAIL` or `STRAY` line ends the turn with its report and the fixes uncommitted.
   - Only then run `node "${CLAUDE_SKILL_DIR}/../build/scripts/land-task.mjs" --fix "fix(<scope>): address the branch review" --plan <plan path> --root <checkout>` to commit every changed path.
4. **Offer the finish.** End on `ship`.

## References

| File | Read it when |
|---|---|

Report: `ship`'s overview as this turn's one report, ending with every task as done or open and the plan's `MANUAL` checks, listed once.
