---
name: pull-request
description: >-
  Load this skill when a branch is heading into main: open a PR, "merge it", "land this", or before
  you run `gh pr create` or `gh pr merge` yourself. Covers the PR body, pre-merge gate, merge, and
  cleanup. Not for shipping a version (use ceh-git-workflow:release).
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires the git CLI on PATH and a git working tree. Opening or merging a PR additionally
  requires the GitHub CLI (`gh`) authenticated via `gh auth login`, a GitHub remote, push
  permission, and network access. The local no-PR merge needs git alone.
license: Apache-2.0
---

# Pull request

Gets a branch into `main` through a merge commit: open the PR once the definition of done holds,
merge only on a green gate, then clean up and report whether the remote branch survived.

## Procedure

Pick the path from the request, then run only that path:

| Request                                       | Path                                |
| --------------------------------------------- | ----------------------------------- |
| "open a PR", "push this for review"           | [Open](#open)                       |
| "merge it", "land PR #N", "merge this branch" | [Merge](#merge)                     |
| "commit, PR and merge", "wrap up this branch" | [Land the branch](#land-the-branch) |

### Open

1. Check the [definition of done](#definition-of-done) for the change type and the
   [author self-review](#author-self-review).
2. Write the body to a temp file using the [template](#pr-title-and-description), then:

   ```bash
   git push -u origin <branch-name>
   gh pr create --title "<type>(<scope>): <short summary>" --body-file body.md
   rm body.md
   if [ "$(gh api repos/{owner}/{repo} --jq .allow_auto_merge)" = "true" ]; then
     gh pr merge --merge --auto   # queues; lands when CI + approvals go green
   fi
   gh api repos/{owner}/{repo} --jq .delete_branch_on_merge   # false: the branch survives
   ```

3. **Record the PR in its build plan.** When the branch changes a plan in `product/plans/`
   (`git diff --name-only origin/main...HEAD -- product/plans/`), append
   `- YYYY-MM-DD PR: #<n> <url>` to the `## Record` section at the end of that plan, then commit and
   push it to the same branch. The plan then traces its change to the review that landed it. With
   no plan in the diff, skip this step.
4. Open as a **draft** while CI runs or the work is still settling, and mark it ready only once the
   self-review passes. A draft is safe to queue: auto-merge waits until the PR is marked ready.
   Request the reviewers the [approval rules](#approvals-and-merge-strategy) require.

### Merge

1. Check the [pre-merge gate](#pre-merge-gate). If the branch won't merge cleanly,
   [resolve conflicts](#resolving-conflicts) first.
2. Merge with the [merge commit message](#merge-commit-message):

   ```bash
   if [ "$(gh api repos/{owner}/{repo} --jq .allow_auto_merge)" = "true" ]; then
     gh pr merge <N> --merge --auto --subject "..." --body-file merge-body.txt
   else
     gh pr merge <N> --merge --subject "..." --body-file merge-body.txt   # gate must be green
   fi
   ```

   With no PR (solo repo, low-risk work), merge locally. Still `--no-ff`, never fast-forward, so
   the branch still lands as one merge commit that reverts as a unit:

   ```bash
   git checkout <branch-name> && git fetch origin && git rebase origin/main
   git checkout main && git pull origin main
   git merge --no-ff <branch-name>
   git push origin main
   ```

   In a worktree (`git rev-parse --git-dir` differs from `git rev-parse --git-common-dir`),
   `git checkout main` fails because the main checkout holds `main`. Build the merge on a detached
   `HEAD` instead:

   ```bash
   git fetch origin && git rebase origin/main
   git checkout --detach origin/main
   git merge --no-ff <branch-name>
   git push origin HEAD:main
   ```

3. Clean up once merged. In a worktree, skip this block: run only `git fetch --prune`, and tell
   the user to pick remove at Claude Code's exit prompt. A branch that survives it, or a raw
   `git worktree add` worktree, is cleaned up by this block run later from the main checkout.
   Otherwise:

   ```bash
   git checkout main && git pull origin main
   git worktree list                          # a worktree on the branch blocks `branch -d`
   git branch -d <branch-name>                # lowercase: refuses an unmerged branch
   git fetch --prune
   git worktree prune                         # drops records of worktrees already deleted
   ```

   Remove a worktree on the merged branch with `git worktree remove <path>` before `branch -d`.
   Remove one this session created without asking. For any other, list it with its branch and
   last commit and ask first: it may hold uncommitted work.

4. [Report the remote branch](#reporting-the-remote-branch).

### Land the branch

Changelog → README → commit → open → merge, on the branch you are already on. Each step gates
the next.

1. **On `main`?** Create a branch first with `git checkout -b`, which carries uncommitted work over.
   **Behind `main`?** Rebase before opening, so the gate measures the right tree.
2. Log the change under `## [Unreleased]`: invoke the Skill tool with
   skill="ceh-git-workflow:update-changelog" in **Unreleased mode**. A genuinely invisible change
   (typo, test-only tweak) is the one exception; record the skip.
3. Refresh the README per `ceh-git-workflow:update-readme` if the change is user-facing, or record
   "no update needed".
4. Commit the work and docs following `ceh-git-workflow:commit`. Tree clean before the next step.
5. Run [Open](#open), then [Merge](#merge). If Open queued auto-merge, Merge only waits for it to
   land and cleans up. Wait on CI with `gh run watch`, never by polling by hand.

## Rules

### PR title and description

The title is a Conventional Commits subject (imperative, lowercase, no trailing period, ≤ 72
chars). It seeds the merge commit subject.

```markdown
## What

<One sentence: the change as an outcome for the reader, not a list of files.>

<The smallest before and after that shows it: command output, a screenshot, or a few diff lines.
Skip when there is nothing to show.>

## Why

<The problem or request that motivated it. Link the issue: Closes #NNN.>

## How

<Only the non-obvious decisions and the alternatives rejected. Skip if the diff explains itself.>

## Risk

<Two-way door (reverting the merge commit undoes it) or one-way (a migration, a published API,
rewritten or deleted data). Then the blast radius: what breaks, and for whom, if this is wrong.>

## Testing

<What you actually ran and added, so a reviewer can reproduce it. Never imply coverage you
didn't add.>

## Checklist

- [ ] All CI checks pass
- [ ] Tests added or updated for new behavior
- [ ] No new lint or type-check suppressions introduced
- [ ] No secrets or credentials in code
- [ ] Migrations (if any) are backward-compatible
- [ ] Decision record updated (if a durable decision was made)
- [ ] Attribution included if AI tooling assisted
```

Attribution: append the `attribution.pr` line the session's Git instructions supply, verbatim, as
the last line of the body. Never substitute a literal from this skill or from memory. If settings
supply none, omit it and check the box.

Write the body to a temp file and pass `--body-file`, for `gh pr create` and `gh pr edit` alike.
Never inline it with a shell heredoc or a PowerShell here-string: the temp file avoids all quoting
and behaves the same in both shells.

### Definition of done

| Change type | Bar                                                                                                                               |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Bug fix     | Root cause stated in the PR. A failing test reproduces the bug and now passes. Full suite green. Lint and type checks pass        |
| Feature     | Unit tests for new logic, integration tests for new API surface. Lint and type checks pass. No new suppressions                   |
| Refactor    | No behavior change, proven by existing tests passing unchanged. No tests deleted to make it pass. PR names the structural problem |

Meet the repo's own coverage and type-check bars. Never lower strictness to pass them; fix the
code.

### Author self-review

- Read the full diff (`git diff main...HEAD`) before requesting review.
- Every file in the diff serves the PR's What. Anything else moves to its own PR or gets named in
  the body.
- No commented-out code, debug logs, or `TODO` without a linked issue.
- Rebased on latest `main`, scoped to one concern.

### Size

| PR type      | Recommended                                               | Max     |
| ------------ | --------------------------------------------------------- | ------- |
| Bug fix      | ≤ 200 LOC                                                 | 300 LOC |
| New feature  | ≤ 400 LOC                                                 | 600 LOC |
| Refactor     | ≤ 500 LOC                                                 | 800 LOC |
| DB migration | Migration file only; split app changes into a separate PR |         |

Over the guideline, split by layer (schema → service → API). Review quality falls with diff size:
past these sizes a reviewer skims instead of verifying. A migration ships alone because the schema
has to deploy and roll back independently of the app code.

### Approvals and merge strategy

- Approvals: 1 for bug fixes and small features, 2 for new API surfaces, schema, or security
  changes, 1 minimum for an urgent fix. Those three are the hardest to undo once shipped, so they
  get a second reviewer. Never bypass CI.
- **Merge commit only.** Never squash, never rebase-merge. Commits land on `main` as written, and
  the per-PR history is kept on purpose: each PR stays one revertable unit on `main`, and its
  commits stay available to bisect. Keep each commit Conventional Commits format and clean the
  branch as you go.
- **Never pass `--delete-branch`.** Claude Code's permission classifier reads it as destructive
  and blocks the whole command, so the merge fails. Remote cleanup is left to the repo's
  "Automatically delete head branches" setting.

### Pre-merge gate

Do not merge until all hold: CI green, required approvals met, rebased on latest `main`, history
clean (fixup/WIP/debug commits squashed or dropped). With no PR, the gate is whatever signals
exist: rebased, clean history, local checks green.

A rebase or conflict fix after review can change what was reviewed without touching a check. When
a review or local test run finishes, record the change's patch id, and compare it again right
before merging:

```bash
git diff origin/main...HEAD | git patch-id --stable   # first field is the id
```

The same id means the reviewed change is what lands, whatever the commit SHAs. A different id
means the content moved: re-request review, or re-read the diff and rerun the local checks with no
reviewer.

Read CI with `gh run`, anchored to the commit, never the branch:

```bash
gh run watch "$(gh run list -c "$(git rev-parse HEAD)" -L1 --json databaseId -q '.[0].databaseId')" --exit-status
gh run view <run-id> --log-failed   # why it went red
```

Three traps make a red build look green or a green one look broken:

- `gh pr checks` and `--json statusCheckRollup` return HTTP 403 with a fine-grained PAT lacking
  `checks=read`. That is a permissions error, not a red gate. Use `gh run` instead.
- `gh api .../commits/<sha>/status` returns 200 but is the legacy Statuses API, which Actions
  never writes to: `pending`, `total_count: 0`, forever. Never gate on it.
- `gh run` sees only this repo's Actions. Third-party checks (Codecov, Sonar, GitHub Apps) need
  the rollup or a manual check.

`gh pr view <N> --json mergeStateStatus` works without `checks=read` and is a valid gate, but
`UNSTABLE` cannot tell a pending optional check from a failing one. Use it to gate, `gh run` to
diagnose.

### Resolving conflicts

Rebase on `main` and resolve there, never inside the merge commit, where the resolution escapes
review and CI:

```bash
git fetch origin && git rebase origin/main
git add <file> && git rebase --continue   # per resolved file
git push --force-with-lease               # your own branch only
```

The gate applies to the rebased state: let CI re-run before merging.

## Output

### Merge commit message

The merge commit reads on its own in `git log main`, never GitHub's default:

```
Merge pull request #<N>: <PR title>

<one or two lines: what it delivers and why it is landing, plus anything a bisect would want>
```

A local merge uses the same shape with the branch's Conventional Commits subject.

### Reporting the remote branch

Never claim the remote branch was deleted without checking
`gh api repos/{owner}/{repo} --jq .delete_branch_on_merge`:

- `true`: the PR merged and GitHub deleted the remote branch.
- `false`: the PR merged and **the remote branch still exists**. Give the command that removes it:
  `git push origin --delete <branch-name>`.

Report the same when auto-merge is only queued: the branch outlives the queue either way.

## Stop conditions

- CI red or approvals missing → surface the failing run and wait. Never merge around it.
- The branch needs a version bump or tag → stop and switch to `ceh-git-workflow:release`.

## Hands off to

- Invoke the Skill tool with skill="ceh-git-workflow:update-changelog" in Unreleased mode at step 2
  of [Land the branch](#land-the-branch).
