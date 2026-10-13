---
name: prc
description: "Land the current work and merge it: self-heals the branch state (commits and pushes uncommitted work via /co push, pushes a new branch, opens the PR via /pr if none exists), then monitors CI checks and merges when ready. Use when: (1) User says 'complete pr', 'merge pr', or 'finish pr', (2) PR is reviewed and ready but CI may still be running, (3) User wants to wait for CI and auto-merge, (4) User wants their current branch committed, PR'd, and merged in one go. Missing PR, missing upstream, uncommitted changes, and a missing linked issue for -c are all normal states to fix silently — never preconditions to stop and report."
argument-hint: "[-c/--close] [-k/--keep-issue] [-w/--watch-ci] [-now/--no-wait]"
---

# PR Complete

This PR is checked, reviewed, and no other tasks are left. Complete the following:

> **On Claude Code on the web** (`$CLAUDE_CODE_REMOTE=true`): follow [`web/web-mode.md`](../../web/web-mode.md). Check CI, merge the PR, and close the linked issue via the GitHub MCP (`pull_request_read` / `get_check_runs`, `merge_pull_request`, `issue_write`), not `gh`. **CI-watch + merge run in-turn on web — see web-mode.md §8:** web has no background-task wakeup, so do **NOT** "watch CI in the background" and end the turn (Step 1.4's background path and "do NOT block the conversation with polling" are terminal-only). Instead poll the PR's checks via MCP in a loop and merge in the **same run** the moment they're green — under `-m`/`-c` the merge is already authorized; never end the turn at "CI running, I'll check back." **Branch deletion — see web-mode.md §5:** when the PR's head is the `claude/*` session branch (the common web case — head=`$WEB_BASE`, base=`$WEB_PARENT`), merge via MCP `merge_pull_request` **WITHOUT any branch-delete** (no `delete_branch:true`). The web platform owns the session branch — never delete it. Deleting a `claude/agent-fix-*` fix branch is fine; deleting the session branch is not. Translate the `--delete-branch` in Step 1 / `--no-wait` accordingly: on web, drop the delete for the session branch.

## Step 0: Pre-flight — get to a pushed PR, then continue

`/prc` means **"take my current work, land it, and merge it."** The user does not always invoke it from a tidy state — often there is no PR yet, no upstream, or uncommitted work sitting in the tree. **These are normal, not errors.** Bring the branch up to a mergeable PR yourself and keep going. Do NOT stop and ask the user to run `/co push` or `/pr` first, and do NOT narrate a list of preconditions before starting — just fix the state and proceed.

Gather the state in one pass:

```bash
git status --porcelain
git branch --show-current
git rev-parse --abbrev-ref @{upstream} 2>/dev/null || echo "NO_UPSTREAM"
gh pr view --json number,state,url 2>/dev/null || echo "NO_PR"
```

Then heal in this order:

1. **Uncommitted changes** (`git status --porcelain` non-empty) → invoke `/co push`. This commits and pushes, and creates the upstream for a new branch. Only stop to ask if the changes are genuinely ambiguous (clearly unrelated files, experimental leftovers) — work that matches the branch topic is committed without asking.
2. **No upstream** and nothing left to commit → `git push -u origin $(git branch --show-current)`.
3. **No PR for this branch** → invoke `/pr`, which auto-detects the base branch. Take the PR number from its result.
4. **PR exists but is a draft** → mark it ready: `gh pr ready <number>`.

Then continue to step 1 with the PR that now exists.

**The one case that must stop:** the current branch is the repo default (`main`/`master`). There is nothing to open a PR from, so healing is impossible. Say so in one line and stop.

**Reporting:** mention healing steps only as part of the final result ("committed and pushed 2 files, opened PR #41, merged"). Do not preface the run with a warning about what is missing.

## Step 1: Check PR status

1. Check the current PR status and CI checks using `gh pr view` and `gh pr checks`
2. If `--no-wait` / `-now` was passed → skip the CI wait and merge immediately (see "`--no-wait` (`-now`) option" below)
3. If all CI checks have already passed and the PR is approved → proceed to step 4
4. If CI checks are still in progress:
- Invoke `/watch-ci` to monitor CI in the background
- Tell the user: "CI is still running. Watching in background via /watch-ci"
- do NOT block the conversation with polling
- **On web (web-mode.md §8): do the opposite — block in-turn.** There is no background-task wakeup on web, so a background watch + turn-end leaves the PR unmerged. Poll the checks via MCP (`pull_request_read` / `get_check_runs`) in a loop (~30–60 s between polls) until terminal, then merge in the same run (step 5) the moment they're green. Do not end the turn at "watching in background."
5. Once all CI checks are green and the PR is approved:
- Merge the PR using `gh pr merge --merge --delete-branch` (**on web (web-mode.md §5): MCP `merge_pull_request` with NO branch-delete when the head is the `claude/*` session branch — the web owns it; only `claude/agent-fix-*` heads may be deleted**)
- Confirm the operation completed successfully

**Important:** Before merging, verify:

- All CI checks have passed (if still in progress, use `/watch-ci` and stop), unless `--no-wait` was passed
- The PR has been approved
- You are on the correct branch

If any CI checks fail, report the failure and do not merge (unless `--no-wait` was explicitly passed — see below).

## `--no-wait` (`-now`) option

If `--no-wait` or `-now` is passed, skip the CI watch entirely and merge the PR immediately, regardless of check status:

1. Do NOT invoke `/watch-ci`
2. Do NOT block on or wait for CI checks to complete
3. Run `gh pr merge --merge --delete-branch` straight away
- If GitHub rejects the merge because branch protection requires passing checks, report the error to the user and stop. Do not retry, do not bypass with admin merge unless the user explicitly asks
4. Then proceed to the post-merge steps (`--close` / `--keep-issue` / `--watch-ci`) as normal

**When to use:** the user has already verified locally that the changes are good (or doesn't care about CI for this merge) and wants the PR merged now without waiting on the pipeline. This is an explicit opt-in — never assume `--no-wait` from context.

**Note:** `--no-wait` only skips waiting for CI checks. The `--watch-ci` (`-w`) option, which watches **post-merge** CI on the target branch, is independent and still works alongside `-now`.

## `--close` (`-c`) option

If `--close` or `-c` is passed, after the PR is successfully merged:

1. Find the parent issue linked to this PR
- Check PR body for "Closes #N", "Fixes #N", "Resolves #N" patterns
- Also check `gh pr view --json closingIssuesReferences`

**If no linked issue is found, `-c` is a no-op.** Merge as normal and add at most `no issue to close` to the final report. Do NOT explain what `-c` stands for, do NOT list it as a problem, and above all do NOT raise it *before* doing the work — a missing issue never blocks or delays the merge. This is a normal outcome, not a warning.

2. If a linked issue is found and the PR was merged successfully:
- Check if it is an **epic issue** (one that holds sub-issues):

     a. Fetch the issue body: `gh issue view <number> --json body`
     b. Look for task list entries referencing issues in the body:

  - Patterns: `- [ ] #N`, `- [x] #N`, `- [ ] owner/repo#N`, `- [x] owner/repo#N`

     c. Also try the GitHub sub-issues API: `gh api repos/{owner}/{repo}/issues/<number>/sub_issues`
        (this returns a list if the newer GitHub sub-issues feature is in use)

- If sub-issues are found (either from the body task list or the API):
  - For each sub-issue:
    - Confirm it is still open: `gh issue view <sub-issue-number> --json state`
    - If open, close it: `gh issue close <sub-issue-number>`
    - Report each closure
  - After all sub-issues are closed, close the epic issue itself:
    - `gh issue close <number>`
    - Report that the epic issue was closed
- If no sub-issues are found (regular issue):
  - `gh issue close <number>`
  - Report which issue was closed

## `--keep-issue` (`-k`) option

If `--keep-issue` or `-k` is passed, after the PR is successfully merged:

1. Find the parent issue linked to this PR (same lookup as `--close`)
2. Instead of closing the issue, prepend `[PR-Merged][Confirm] ` to the issue title:
- `gh issue edit <number> --title "[PR-Merged][Confirm] <original title>"`
- This signals that the PR was merged but the issue needs user confirmation before closing
3. Report which issue was updated

**Note:** `--keep-issue` and `--close` are mutually exclusive. If both are passed, `--keep-issue` takes precedence.

## `--watch-ci` (`-w`) option

If `--watch-ci` or `-w` is passed, after the PR is successfully merged:

1. Determine the merge target branch (the base branch of the PR)
2. Invoke `/watch-ci` to monitor the merge target branch CI. `/watch-ci` already handles

   merged PRs (its Step 2b): it detects the merged state and itself applies the
   push-trigger-check determination — [`skills/watch-ci/references/push-trigger-check.md`](../watch-ci/references/push-trigger-check.md)
   is the single source of truth for that classification; do not restate the recipe
   here. Do not run a separate preliminary `gh run list` check before calling `/watch-ci`
   — that duplicate check is exactly what silently swallowed the missing-run condition
   before.

3. Report whatever `/watch-ci` returns, without softening it:
- a **pass** only for `RESULT: PASSED`
- a **failure** for `RESULT: FAILED`, or for an `EXPECTED_RUN_MISSING` push-trigger-check

  verdict — name the likely cause `/watch-ci` reports (a skip marker in the merge commit
  message, or a merge performed by Actions using `GITHUB_TOKEN`)

- **unresolved, never a pass**, for `RESULT: INCONCLUSIVE`, `RESULT: TIMEOUT` (the watch

  gave up before CI reached a terminal state — say what was still unfinished), or an
  `INCONCLUSIVE` push-trigger-check verdict

- **benign, with the stated reason**, only for a `BENIGN_NO_TRIGGER` verdict — this is

  the only case that may say "no CI detected", and the reason `/watch-ci` gave (no
  matching trigger, excluded by a `branches`/`paths` filter, disabled workflow, Actions
  disabled repo-wide) must be repeated, not dropped

**On web (web-mode.md §8): the post-merge watch is also in-turn — do NOT background `/watch-ci`.** Web has no background-task wakeup, so a backgrounded post-merge watch would leave this step hanging exactly like the pre-merge case. Poll the target-branch CI via MCP (`pull_request_read` / `actions_*` per github-ops.md) in a loop (~30–60 s between polls) until terminal, then report. If it goes red, fix via a `claude/agent-fix-*` PR (web-mode.md §5) and re-poll until green. Stay in the turn — never end at "watching in background, I'll check back."

**This option is only activated when explicitly passed.** Without `-w`, prc does not watch post-merge CI.
