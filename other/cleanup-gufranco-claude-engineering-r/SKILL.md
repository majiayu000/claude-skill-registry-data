---
name: cleanup
description: List stale branches, long-open PRs, merged branches, and orphaned worktrees, then close or delete each one with confirmation.
disable-model-invocation: true
argument-hint: "/cleanup [branches|prs|worktrees] [--dry-run|--apply]"
allowed-tools: "Bash, Read, AskUserQuestion"
sensitive: true
---

## Overview

Repository hygiene tool that finds stale branches, lingering PRs, merged branches not yet deleted, and orphaned worktrees. Presents everything in a table, asks for confirmation per item, and cleans up what you approve.

## When to use

- When the repository has accumulated many old branches.
- When you want to prune merged branches that were never deleted after merge.
- When open PRs have gone stale and need to be closed or re-evaluated.
- When worktrees from previous tasks were left behind.
- Before a release to reduce clutter.

## When NOT to use

- For refactoring or cleaning up code. Use `/review` or a manual refactor instead.
- For dependency updates or vulnerability scanning. Use `/audit` instead.
- For git commit, push, or PR creation. Use `/ship` instead.

## Arguments

This skill accepts optional arguments after `/cleanup`:

- No arguments: full scan covering branches, PRs, and worktrees. **Default mode is dry-run.** No mutation happens without `--apply`.
- `branches`: scan branches only.
- `prs`: scan PRs only.
- `worktrees`: scan worktrees only.
- `--dry-run`: explicit dry-run flag. Same as the default. Kept for clarity.
- `--apply`: perform the cleanup. Required for any mutation. Without this flag, the skill prints the report and exits.

Examples: `/cleanup branches`, dry-run, `/cleanup prs --apply`, `/cleanup --apply`.

The two-phase flow exists because cleanup is destructive: read the report, decide, then re-run with `--apply`.

## Steps

1. **Detect the platform and account.** Read `git remote get-url origin` to determine GitHub or GitLab. Identify the correct account token per the github-accounts or gitlab-accounts rules.

2. **Find merged branches.** Run `git branch --merged origin/HEAD 2>/dev/null` to list local branches whose HEAD is reachable from the default branch. If `origin/HEAD` is not set, try `origin/main`, then `origin/master`. Exclude protected branches: `main`, `master`, `develop`, `staging`, `production`, and any branch matching `release/*`. These can be safely deleted with `git branch -d`.

3. **Find stale branches.** For each local and remote branch not in the merged list and not protected, check the date of the last commit: `git log -1 --format="%ci" <branch>`. Flag branches with no commits in the last 30 days as stale. Record the branch name, last commit date, last commit message, and author.

4. **Find stale PRs.** Query the platform for open PRs in the current repo.
   - GitHub: `GH_TOKEN=$(gh auth token --user <account>) gh pr list --state open --json number,title,author,createdAt,updatedAt,isDraft,url`
   - GitLab: `GITLAB_TOKEN=<token> GITLAB_HOST=<host> glab mr list -F json`, which lists open MRs by default
   - Flag PRs open for more than 14 days with no activity in the last 7 days as stale.
   - Flag draft PRs open for more than 7 days separately.

5. **Find orphaned worktrees.** Run `git worktree list --porcelain`. For each worktree, check if its branch still exists and is not merged. A worktree whose branch was deleted or merged is orphaned.

6. **Present findings.** Display a table grouped by category:

   ```
   ## Cleanup Report

   ### Merged branches (safe to delete)

   | Branch | Merged into | Last commit |
   |--------|------------|-------------|
   | feature/auth-v2 | main | 12 days ago |
   | bugfix/null-check | main | 3 weeks ago |

   ### Stale branches (no commits in 30+ days)

   | Branch | Last commit | Author | Last message |
   |--------|------------|--------|-------------|
   | feature/old-idea | 45 days ago | alice | WIP: initial attempt |

   ### Stale PRs (open 14+ days, no recent activity)

   | PR | Title | Author | Age | Last activity |
   |----|-------|--------|-----|--------------|
   | #42 | Add caching layer | bob | 21 days | 18 days ago |

   ### Draft PRs (open 7+ days)

   | PR | Title | Author | Age |
   |----|-------|--------|-----|
   | #55 | WIP: new layout | carol | 10 days |

   ### Orphaned worktrees

   | Path | Branch | Reason |
   |------|--------|--------|
   | /tmp/repo-auth | feature/auth | branch deleted |
   ```

7. **If `--apply` was NOT passed, stop here.** Default mode is dry-run. Print the report, remind the user to re-run with `--apply` to mutate, and exit.

8. **Confirm and act.** Only when `--apply` was passed. For each category, ask the user which items to clean up. Accept "all", a comma-separated list of names or numbers, or "skip".

   - Merged branches: `git branch -d <branch>`.
   - Stale branches: `git branch -D <branch>` with a warning that this force-deletes an unmerged branch.
   - Stale PRs: close without a comment, per [`../../rules/pr-comment-discipline.md`](../../rules/pr-comment-discipline.md). The terminal report names each closed PR and its idle time, so the user can tell the author directly.
     - GitHub: `GH_TOKEN=$(gh auth token --user <account>) gh pr close <number>`
     - GitLab: `GITLAB_TOKEN=<token> GITLAB_HOST=<host> glab mr close <number>`
   - Draft PRs: same as stale PRs.
   - Orphaned worktrees: `git worktree remove <path>`.

9. **Prune remote tracking branches.** Run `git remote prune origin` to clean up references to deleted remote branches.

10. **Print summary.**

    ```
    ### Cleanup complete

    - N merged branches deleted
    - N stale branches deleted
    - N PRs closed
    - N worktrees removed
    - Remote tracking branches pruned
    ```

## Rules

- Never delete protected branches: `main`, `master`, `develop`, `staging`, `production`, or branches matching `release/*`.
- Always confirm before force-deleting unmerged branches. Make the warning visible.
- Never close PRs that have activity in the last 7 days, even if they are older than the stale threshold.
- Always prefix `gh` commands with `GH_TOKEN` per the github-accounts rule.
- Always prefix `glab` commands with `GITLAB_TOKEN` and `GITLAB_HOST` per the gitlab-accounts rule.
- Close a PR with no comment. The reason goes in the terminal report, where the user decides how to tell the author.
- In `--dry-run` mode, do not modify any state. Report only.
- When a branch exists both locally and on the remote, delete both if approved. Delete local first with `git branch -d <branch>`, or `-D` after the force-delete warning, then remote with `git push origin --delete <branch>`.
- Show age and last activity in relative format.

## Common Rationalizations

- "The user asked for cleanup, so `--apply` is implied": the default is a dry run. Print the report and wait for a re-run with `--apply`.
- "The branch is stale, so `-D` is fine": a stale branch can hold the only copy of unmerged work. Show the force-delete warning and get a per-item answer.
- "`origin/HEAD` is missing, so skip the merged scan": fall back to `origin/main`, then `origin/master`.
- "The PR is 20 days old, close it": age alone is not staleness. Activity in the last 7 days keeps it open.
- "The default token works for `gh`": the wrong account sees the wrong PRs or none. Prefix `GH_TOKEN` for the account read from the remote.

## Red Flags

- Stop and drop the item when a candidate branch is `main`, `master`, `develop`, `staging`, `production`, or matches `release/*`.
- Stop after the report when the invocation lacks `--apply`.
- Stop and ask again when the user's selection names an item absent from the report.
- Stop and keep the worktree when `git worktree list --porcelain` shows uncommitted changes in it.

## Verification

- The report lists every category the invocation scanned, with relative ages.
- In dry-run mode, `git branch -a`, `git worktree list`, and the open PR list are unchanged after the run.
- With `--apply`, each approved branch is absent from `git branch -a` and each approved worktree from `git worktree list`.
- Each closed PR shows the state `CLOSED` in `GH_TOKEN=$(gh auth token --user <account>) gh pr view <number> --json state`, or `glab mr view` on GitLab.
- The summary counts match the items the user approved.

## Related skills

- `/ship` - Commit, push, and create PRs.
- [`/morning`](../morning/SKILL.md) - Cross-account sweep of open PRs, reviews, and issues. This skill covers one repository; that one covers every account.
