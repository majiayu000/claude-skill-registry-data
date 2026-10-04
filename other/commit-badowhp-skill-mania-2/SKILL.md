---
name: commit
description: "Create focused local Git commits from an existing worktree. Use when asked to inspect changes, stage selected files or hunks, verify the staged diff, or make a local commit; do not use for pushing, rebasing, branch management, or pull-request workflows."
---
# Commit

Create reviewable local commits without sweeping unrelated work into the index.

## Core Rules

1. Read repository guidance before staging. Preserve worktree changes that the user did not put in scope.
2. Inspect `git status --short`, the unstaged diff, and the staged diff before deciding what belongs together.
3. Never use `git add .`, `git add -A`, or another repository-wide staging shortcut.
4. Stage explicit paths or deliberate hunks. Keep unrelated, generated, secret-bearing, and temporary files out of the commit.
5. Verify the exact staged patch before committing. Do not infer that a clean test run makes an unreviewed staged diff safe.
6. Do not amend, reset, rebase, cherry-pick, push, force-push, change branches, or open a pull request unless the user separately and explicitly authorizes that operation.

## Workflow

1. Establish scope:
   - identify the requested outcome and current branch
   - inventory staged, unstaged, untracked, conflicted, generated, and ignored files
   - separate pre-existing user work from changes created for the current task
2. Review changes:
   - inspect relevant unstaged and staged diffs
   - check new files before staging them
   - stop on unresolved conflicts, suspected credentials, unexpected binaries, or unclear ownership
3. Form one semantic change set. If the work contains independent concerns, commit only the requested group or explain the proposed split.
4. Run the smallest relevant validation required by repository guidance. Treat a failing required check as a blocker unless the user explicitly accepts the known failure.
5. Stage only the chosen paths or hunks.
6. Verify with the equivalent of:
   - `git diff --cached --check`
   - `git diff --cached --stat`
   - `git diff --cached`
7. Write a concise imperative commit message that describes the behavior or repository outcome. Add a body only when the reason, compatibility impact, or validation context would otherwise be lost.
8. Create the local commit, then inspect the resulting commit summary and `git status --short`.
9. Report the commit identifier, message, validation performed, and any intentionally uncommitted changes. Do not push automatically.

## Commit Boundaries

- Keep code, tests, generated package copies, and directly related documentation together when they implement one behavior.
- Split unrelated refactors, formatting churn, dependency changes, and opportunistic cleanup.
- Include generated files only when repository guidance requires them and the canonical source change is in the same commit.
- Do not stage a file merely because it is modified. Inclusion requires a clear relationship to the commit's purpose.
- Prefer leaving an ambiguous file unstaged and naming it over guessing ownership.

## Tool Output

- Use RTK when available for verbose, non-destructive Git inspection such as `rtk git status` or `rtk git diff`.
- Inspect raw Git output before making staging, secret-exposure, conflict, or commit-boundary decisions when filtered output omits material detail.

## Honest Opinion
Use `honest opinion:` when it adds decision value: reviews, audits, recommendations, plans, tradeoffs, or implementation close-outs with a material risk or gap. Be brutally honest and evidence-based. Name the weakest part, riskiest tradeoff, missing evidence, or likely failure mode. Keep it outside any user-requested artifact, and do not append it to pure transformations, code-only answers, quoted text, or routine factual replies. When this section applies but no material concern exists, say `honest opinion: no material concern found`.

## Output Shape

After a commit, report:

1. commit identifier and message
2. staged scope included in the commit
3. validation performed and result
4. intentionally uncommitted or unresolved changes
5. confirmation that no push occurred
