---
description: Propagate reviewed changes down an existing PR stack, keeping every PR mergeable
model: sonnet
---

# Goal

- Given the current PR is one branch in a stack of sequential PRs, propagate
  changes reviewed in an earlier PR into every PR stacked on top of it
- Preserve full history: merge forward and commit. Never rebase or force-push
- End with every PR in the stack mergeable, with CI green

# When to Use This Skill

- Use after a PR in the middle or bottom of a stack was reviewed and changed,
  and the branches stacked on top of it need those changes
- Do not use this to build a new stack. Use
  `/auto_task.execute_with_stacked_prs` instead
- Follow `.claude/skills/auto_task.rules.md` section "Ask for Clarification
  Before Executing an Unclear Plan" when a PR's description is unclear. Do not
  guess and merge blind

# Workflow

## Discover the Full Stack

- Get the current PR:
  ```bash
  > gh pr view --json number,title,baseRefName,headRefName,url
  ```
- Walk up from the current PR's `baseRefName`, following each branch's own PR
  (`gh pr list --head <base> --state all`), until reaching the default branch
  (`master`). This is the bottom of the stack
- Walk down from the current PR's `headRefName`, finding the open PR whose
  `baseRefName` equals the previous PR's `headRefName`
  (`gh pr list --base <branch> --state open`). This is the top
- Order the PRs from bottom (based on `master`) to top
- Check whether the bottom PR is behind the default branch:
  ```bash
  > gh pr view <bottom PR> --json mergeable,mergeStateStatus
  ```
  If `mergeable` is `CONFLICTING` (or the branch is just behind), treat the
  default branch as an implicit `PR_0` at the bottom. It needs the same
  merge-forward treatment as every other pair

## Print the Stack

- Print one table with columns `#`, `Branch`, `PR` (`#<NUM> — <title>`), `Base`,
  e.g.:
  ```
  +---+--------------------+-----------------------------------------------+--------+
  | # | Branch             | PR                                             | Base   |
  +---+--------------------+-----------------------------------------------+--------+
  | 1 | ..._invoke_tasks   | #1423 -- auto-pick suffix in git_branch_create | master |
  | 2 | ..._invoke_tasks_2 | #1424 -- unit tests for git_*/gh_* tasks       | #1423  |
  +---+--------------------+-----------------------------------------------+--------+
  ```

## Create and Confirm the Propagation Plan

- Create `plan-auto_task.restack.md` listing, for every consecutive pair
  `(PR_i, PR_i+1)`, including `(master, PR_1)` when the bottom PR is behind the
  default branch:
  - What `PR_i` changed, from its GH description and
    `git diff <base_i>...<head_i>`
  - What must merge into `PR_i+1`, and which files are likely to conflict
    (touched by both)
- Wait for the user to confirm this plan before touching any branch

## Propagate Changes Down the Stack

- Process pairs bottom-up, one at a time, so each merge includes everything
  propagated so far. Start with `(master, PR_1)` when it is in the plan
- For each pair `(PR_i, PR_i+1)` or `(master, PR_1)`:
  - Read `PR_i`'s description (`gh pr view <PR_i> --json body,title`) to resolve
    conflicts by its intent, not blindly
  - Right before merging, `git fetch` and confirm the local branch tip matches
    `origin/<branch_i+1>`. Another process or session can push mid-stack, and
    merging on a stale copy silently drops those commits
    ```bash
    > git fetch origin <branch_i> <branch_i+1>
    > git checkout <branch_i+1>
    > git reset --hard origin/<branch_i+1>
    > git merge origin/<branch_i>
    ```
  - Resolve conflicts by hand, favoring the intent of `PR_i`'s change. Do not use
    `git rebase` or force-push
  - Follow `.claude/skills/coding.rules.md` and `.claude/skills/testing.rules.md`
    while resolving conflicts in code and tests
  - Commit the merge and run `git push`. If the push is rejected because
    `origin/<branch_i+1>` moved, re-fetch and redo the merge. Do not force-push
    over it
- Repeat up to the top of the stack

## Make Every PR Mergeable

- For every PR in the stack, in order, run `/github.get_pr_ready_to_merge` to get
  its CI green
- After propagation, confirm mergeability:
  ```bash
  > gh pr view <NUM> --json mergeable,mergeStateStatus
  ```

## Report Only Failures

- Do not comment on a PR that merged cleanly and passed CI
- If a PR hits an unresolved conflict or a CI failure needing human input, post
  one comment explaining the problem:
  ```bash
  > gh pr comment <NUM> --body "<what failed and why>"
  ```
- Also describe the problem to the user directly. Do not leave it only in a PR
  comment

# Conventions

- Follow `.claude/skills/auto_task.rules.md` for clarification conventions
- Follow `.claude/skills/github.get_pr_ready_to_merge/SKILL.md` to get each PR's
  CI green

# Constraints

- Never rebase or force-push a branch in the stack. Propagate with merge commits
  only, to preserve review history
- Never merge any PR. Merging is the user's decision
- Never skip a PR or reorder the propagation. Always go strictly bottom-up
- Never guess the intent of an unclear PR when resolving a conflict. Stop and ask
- Never merge or build on a local branch copy without re-fetching first. A
  concurrent session or auto-commit/auto-push process can move a branch in the
  stack while this skill runs

# Verification

- [ ] The full stack was discovered from `master` up through the top PR, matching
      GitHub's actual base chain, and the bottom PR's mergeability against
      `master` was checked
- [ ] `plan-auto_task.restack.md` lists every consecutive pair and was confirmed
      by the user before any branch was touched
- [ ] Every merge between stacked branches is a merge commit, not a rebase. No
      branch was force-pushed
- [ ] `gh pr view <NUM> --json mergeable` reports `MERGEABLE` for every PR in the
      stack
- [ ] `/github.get_pr_ready_to_merge` ran on every PR and its CI is green
- [ ] A PR comment exists only for PRs that hit a conflict or CI failure needing
      human input
