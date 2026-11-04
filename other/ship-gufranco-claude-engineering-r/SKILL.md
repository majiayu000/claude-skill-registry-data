---
name: ship
description: Ship code through the full delivery pipeline, with subcommands commit, pr, release, checks, and worktree. Handles semantic commits, pull requests with CI monitoring, tagged releases, pipeline diagnosis, and parallel worktree management. Use when user says "commit", "create a PR", "push", "release", "check CI", "pipeline status", "worktree", or wants to move code from working directory to production. For code review, use /review; for running tests, use /test; for planning, use /plan.
argument-hint: "/ship commit | /ship pr | /ship release | /ship checks | /ship worktree <new|list|prune>"
allowed-tools: "Read, Edit, Bash, Grep, Glob, AskUserQuestion"
sensitive: true
---

## Overview

Unified delivery skill for getting code from working directory to production.

## When to Use

- The user says "commit", "create a PR", "push", "release", "check CI", "pipeline status", or "worktree".
- Finished work needs semantic commits, a pull request, a tagged release, or a CI diagnosis.
- Several tasks need parallel worktrees, or a worktree's task is ready to deliver.

For reviewing a change, use `/review`; for running the suite, use `/test`; for human review comments on your own PR, use `/respond`; for merging and deploying, use `/deploy`.

## Process

| Invocation | Action |
|-----------|--------|
| `/ship` or `/ship commit` | Create semantic commits (default) |
| `/ship pr` | Create or update a pull request |
| `/ship release` | Create a tagged release with changelog |
| `/ship checks` | Monitor CI/CD pipeline and diagnose failures |
| `/ship worktree` | Manage git worktrees for parallel development |

If no subcommand is given, default to `commit`.

---

## commit

Analyze all uncommitted changes and create semantic commits following the conventional commit format.

### When to use

- After completing a task and ready to save progress.
- When multiple unrelated changes need separate commits.
- Before creating a PR, to ensure clean commit history.

### Arguments

- No arguments: commit and ask whether to push.
- `--push`: commit and push automatically.
- `--pipeline`: commit, push, ensure a PR exists, open one if missing, and stay in a monitoring loop until **CI is 100% green AND there are zero open AI-tool review threads**. Implies push. If no PR exists on the current branch, runs the `pr` flow, with `--no-pipeline` to avoid recursion before entering Pipeline Monitoring. On CI failure, diagnoses, fixes, and re-pushes. On open AI-tool comments, CodeRabbit, Copilot, Greptile, Sourcery, etc., addresses every actionable finding, pushes the fix, and resolves the thread. The loop only exits when both conditions hold simultaneously on the latest SHA.

### Steps

1. Run **in parallel**: `git status`, `git diff`, `git diff --cached`, `git log --oneline -10`.
2. Group related changes into logical units. Each group becomes one commit:
   - Same feature/module together.
   - Unrelated changes in separate commits.
   - Tests go with the code they test.
3. For each group: stage specific files, `git add <file>`, never `-A` or `.`, commit with format below.
4. Run **in parallel**: `git status`, `git log --oneline` to verify.
5. Push logic:
   - `--push`: push immediately.
   - `--pipeline` without `--push`: ask "Push to remote and monitor pipeline?"
   - No flags: ask "Want me to push to remote?"
   - Check upstream: `git rev-parse --abbrev-ref @{upstream}`. Use `-u origin <branch>` if none.
6. If `--pipeline`:
   - Check if a PR exists for the current branch via `GH_TOKEN=$(gh auth token --user <account>) gh pr view` or `glab mr view`.
   - If none exists, invoke the `pr` flow with `--no-pipeline` to create the PR, skipping its own monitoring loop, then continue.
   - Enter the Pipeline Monitoring loop (see below).

### Commit Message Format

Follow [`rules/git-workflow.md`](../../rules/git-workflow.md). Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. Subject: imperative mood, no caps, no period, max 50 chars. Body: wrap at 72, explain WHAT and WHY. Footer: `BREAKING CHANGE:`, `Fixes #`, `Closes #`, `Refs #`.

---

## pr

Create or update a pull request with a structured description. Supports GitHub and GitLab.

### When to use

- After committing to a feature branch and ready for review.
- When updating an existing PR description.
- When creating a draft PR for early feedback.

### Arguments

- No arguments: create a new PR.
- `--draft`: create as draft.
- `--base <branch>`: target specific base branch.
- `--reviewer <user>`: request review, repeatable.
- `--assignee <user>`: assign PR; defaults to `@me`.
- `--label <name>`: add label, repeatable.
- `--no-pipeline`: skip CI monitoring after creation.
- `--docs`: automatically update stale documentation without asking.
- `update` or a PR number: update existing PR.

### Steps

1. **Gather context** in parallel: `git status --porcelain`, `git remote get-url origin`, `git branch --show-current`. Stop if uncommitted changes or on main. Detect CLI tool, either `gh` or `glab`. **Resolve account** per [`standards/multi-account-cli.md`](../../standards/multi-account-cli.md): map the owner in the remote URL to an account and prefix every `gh` call with `GH_TOKEN=$(gh auth token --user <account>)`, never switching the global active account.
2. **Check existing PR and base branch**, parallel: look up existing PR, detect base branch, unless `--base`. If PR exists and no `update` flag, show URL and ask. One task gets one PR per repository: when this task already has an open PR in the repository on another branch, cherry-pick these commits onto that branch and update its title and body to name every tracker key, instead of opening a second PR. A second PR opened by mistake is closed without a comment. [`hooks/pr-comment-discipline.py`](../../hooks/pr-comment-discipline.py) asks before a second `gh pr create` in one repository and session.
3. `git fetch origin`, `git log --oneline origin/<base>..HEAD`. Stop if no commits.
4. **Run quality gate** per [`rules/git-workflow.md`](../../rules/git-workflow.md), in order: format check, lint, type check, full test suite, build. Stop if any fails.
5. **Update from base**: when the branch has never been pushed, `git rebase origin/<base>`; if it conflicts, `git rebase --abort` and stop. When the branch is already on the remote, never rewrite it: merge `origin/<base>` only if it conflicts, per Conflict Resolution in [`standards/git-workflow.md`](../../standards/git-workflow.md).
6. **Check PR size**, parallel: `git diff origin/<base>...HEAD --stat` and full diff. Warn at 400+ lines, confirm at 1000+.
7. **Self-review**: scan for debug statements, TODO/FIXME, accidentally committed files, binaries.
8. **Extract context and capture visual evidence**: check branch and commits for ticket patterns. When the diff touches a web, mobile, desktop, or terminal surface, capture `Before` from the base commit in a `git worktree` and `After` from the branch, same data, viewport, theme, and locale, at device scale 2 or more with the longer side at least 1600 px. Capture the full page, unclipping an inner scroll container with `height: auto` first, never `overflow: visible`; scale every image in the set to one pixel width, never pad; group desktop and mobile under their own headings, with alt text naming device and viewport, such as `After: Mobile 320 px, default queue`. A new page states it has no Before. Recipes per surface: "Visual Evidence In Published Text" in [`standards/frontend-render-gate.md`](../../standards/frontend-render-gate.md). This step is never skipped; [`hooks/frontend-render-gate.py`](../../hooks/frontend-render-gate.py) blocks the PR without the images.
9. **Push**: re-read the pull request first, `gh pr view --json state,mergedAt,headRefOid`, because a teammate can merge it while the gate runs. When it is `MERGED` or `CLOSED`, stop and report who merged it and when. Use `-u` if no upstream. Never force push; a pushed branch was never rewritten, so a plain push always applies.
10. **Build title and description**: detect PR template at `.github/PULL_REQUEST_TEMPLATE.md` or the GitLab equivalent. Use the What, How, Evidence, and Merge Danger structure in [PR Description](#pr-description). Scale to PR size.
11. **Create/update**: write body to temp file. `GH_TOKEN=$(gh auth token --user <account>) gh pr create --body-file <file> --attach 'before.png#Before: Desktop 1440 px, <screen>' --attach 'after.png#After: Desktop 1440 px, <screen>'` or `glab mr create --description-file`, with GitLab images uploaded first and embedded. Self-assign by default. Clean up temp file. AI reviews are requested by [`hooks/ai-review-request.py`](../../hooks/ai-review-request.py) after `gh pr create`, `gh pr ready` and `git push`; read its `ai-review:` line and report it with the PR URL.
12. Show PR URL. The PR is reported done only with the counted done state from "The Done State" in [`standards/pr-comment-discipline.md`](../../standards/pr-comment-discipline.md): 0 unresolved threads and 0 unminimized bot review bodies.
13. **Documentation staleness check.** Read project documentation files such as README.md, CONTRIBUTING.md, and the docs/ directory, then cross-reference against the diff:
    - New features without corresponding documentation.
    - Removed features still documented.
    - Changed APIs with stale examples.
    - New environment variables not in `.env.example`.
    - New CLI commands or scripts not documented.
    - A `specs/current/` living spec that no longer matches the change. If the plan folder carries a spec delta, remind the user to run `/plan archive` once the PR merges, to fold the delta into the living spec. See [`rules/living-specs.md`](../../rules/living-specs.md).
    If stale documentation is found, list the gaps and offer to update. If `--docs` flag is passed, update automatically without asking.
14. Enter Pipeline Monitoring loop unless `--no-pipeline`. The loop monitors both CI checks AND AI-tool review threads, and only exits when both are clean.

### PR Title

Conventional commit style when it fits. Max 70 chars. Prefix ticket ID if available.

### PR Description

- **Small PR**: one paragraph, no headers, plus the Merge Danger and Evidence lines.
- **Standard PR**: What, How, Evidence, Merge Danger sections. Add Breaking Changes only if applicable.
- **Evidence** is a before and after: the exact test that failed and now passes, or the output that changed. "Tests are green" alone is a claim, not evidence. A visible change carries high-resolution screenshots labeled `Before:` and `After:`, attached in step 11.
- **Merge Danger** states the **Door** and the **Blast Radius**. A two-way door is cheap to reverse; a one-way door is not. Always one-way: a migration that drops or rewrites data, an outbound send to users or partners, a deletion, and a public API removal. Blast radius names what breaks if the change is wrong, such as API consumers, layout on mobile, or a scheduled job. Be most suspicious of your own "two-way, small" call: a revert does not unsend an email, and a flagged rollout stays two-way only until the first write lands in the new format.
- Concise, direct. No filler. Open questions go to the chat, never the PR body.
- Do not hard-wrap the body. The platform renders single newlines as line breaks, so write each paragraph as one long line. The 72-column wrap is for commit bodies only. See [`standards/git-workflow.md`](../../standards/git-workflow.md) "PR/MR Creation".

---

## release

Create a tagged release whose notes are written for users per [`standards/changelog.md`](../../standards/changelog.md). Conventional commits pick the version bump and locate what changed; they never become the notes verbatim.

### When to use

- After merging all planned changes to main and ready to release.
- With `--dry-run` to preview before creating.

### Arguments

- No arguments: auto-detect next version from commit types.
- A version (e.g. `1.2.0`): use that exact version.
- `--dry-run`: show what would be released without creating anything.

### Steps

1. **Gather context**, parallel: `git remote get-url origin`, `git describe --tags --abbrev=0`, `git status --porcelain`. Detect CLI tool. **Resolve account** as in `pr` step 1. Stop if dirty.
2. `git log --oneline <last-tag>..HEAD`. Stop if no commits.
3. Determine version: parse last tag as semver. `BREAKING CHANGE`/`!` = major, `feat` = minor, `fix`/`perf`/`refactor` = patch. Only `chore`/`docs`/`style`/`test`/`build`/`ci` = no bump.
4. Build the release notes per [`standards/changelog.md`](../../standards/changelog.md) Release Notes:
   - When the project keeps a changelog file with an Unreleased section, the notes are those entries. Move them under the new version heading, in the heading format the file already uses, as part of the release.
   - Never regenerate or rewrite existing entries in a hand-written changelog; only move its Unreleased entries.
   - Otherwise draft from the commits in the range: one user-facing entry per change a user would notice, related commits grouped into a single entry, sections What's New, Improvements, Fixes, Breaking Changes, Deprecated, and Internal. A list of commit subjects is never release notes.
5. If `--dry-run`, show and stop.
6. **Run quality gate**, in order: format check, lint, type check, full test suite, build. Stop if any fails.
7. Present the version and the release notes for approval.
8. After approval: `git tag -a v<version> -m "v<version>"`, `git push origin v<version>`, `GH_TOKEN=$(gh auth token --user <account>) gh release create` or `glab release create` with notes-file. Clean up temp file.
9. Show release URL.

---

## checks

Monitor CI/CD pipeline checks and diagnose failures. Diagnosis only, no auto-fix.

### When to use

- After pushing or creating a PR.
- When a pipeline fails and you need diagnosis.

### Arguments

- No arguments: check current branch.
- A PR number: check that specific PR.

### Steps

1. **Gather context**, parallel: `git remote get-url origin`, `git branch --show-current`. Detect CLI tool. **Resolve account** as in `pr` step 1.
2. Check for PR, or use provided number. Fall back to branch pipelines.
3. Check status: `GH_TOKEN=$(gh auth token --user <account>) gh pr checks` or `glab ci status`.
4. If passing, report and stop.
5. If running, poll a one-shot `GH_TOKEN=$(gh auth token --user <account>) gh run view <id> --json status,conclusion` every 60 seconds, at most 20 times, and every 3 minutes while the run is `queued`; GitLab: `glab ci status -F json` on the same schedule. Report and stop when the poll budget runs out.
6. If failed: fetch logs, parallel with `GH_TOKEN=$(gh auth token --user <account>) gh run view <id> --log-failed` or `glab ci trace <job-id>`. Search for existing fixes first.
7. Present diagnosis per failure: check name, URL, error, log excerpt.
8. Suggest next steps but do not auto-fix.

---

## worktree

Manage git worktrees for parallel development.

### Subcommands

| Invocation | Action |
|-----------|--------|
| `/ship worktree init <task1> \| <task2>` | Create worktrees from pipe-separated tasks |
| `/ship worktree deliver` | Commit, push, and create PR from worktree |
| `/ship worktree check` | Show status of all worktrees |
| `/ship worktree cleanup` | Remove worktrees for merged branches |

### init

1. Verify: git repo, not inside worktree, get repo root and branch.
2. Parse tasks on `|`. Each segment becomes a worktree.
3. For each: branch `wt/<kebab-case>`, path `<root>/.worktrees/<name>`, `git worktree add -b <branch> <path>`. Write `.worktree-task.md`. Ask about package install.
4. Present table: path, branch, task.

### deliver

1. Verify inside a worktree.
2. Gather state, parallel: status, commits, task file, remote, branch. **Resolve account** as in `pr` step 1.
3. Stage and commit, worktrees are task-scoped. Remove `.worktree-task.md` from staging.
4. Push with `-u`.
5. Create PR using task description. Follow PR conventions.
6. Show PR URL.

### check

1. `git worktree list --porcelain`.
2. For each, parallel: branch, commit count, uncommitted changes, task file.
3. Present as table.

### cleanup

- Default: remove worktrees whose branch is merged.
- `--all`: all `wt/*` worktrees, warn about unmerged work.
- `--branch <name>`: specific worktree.
- `--dry-run`: show what would be removed.
- Remove the worktree with `git worktree remove <path>`, delete the local branch with `git branch -d <branch>`, and, after asking, delete the remote branch with `git push origin --delete <branch>`. Run `git worktree prune`.

---

## Pipeline Monitoring (shared by commit and pr)

The monitoring loop has **two parallel exit conditions that must BOTH hold on the latest pushed SHA**:

1. Every functional CI check is green, manual gates like `lead-approval` are excluded.
2. Every actionable AI-tool comment is closed, across all four comment channels, for every bot in the 6a list.

Condition 2 spans every channel in [`../../standards/pr-comment-channels.md`](../../standards/pr-comment-channels.md), not just inline review threads. A bot summary posted as a review body or a PR-level comment holds the loop open exactly like an inline thread does.

Do not declare the loop complete while either condition is open. If a fix is pushed for one condition, both conditions must be re-verified on the new SHA before exiting.

**Human-authored comments are out of scope of this loop.** They require judgment per comment and are handled by `/respond`, which owns the only reply surface. When a human reviewer comments during pipeline monitoring, this loop ignores it; the author runs `/respond` separately to triage and reply. The loop still reports the count of open human comments per channel on exit, so a human concern is never silently buried by a green pipeline.

### Step 1: Detect platform and locate checks

Run **in parallel**: `git remote get-url origin`, `git branch --show-current`. Detect CLI tool. **Resolve account** as in `pr` step 1. Check if PR exists.

If no PR exists and the caller invoked `--pipeline`, fall through to the `pr` flow with `--no-pipeline`, steps 1-13, to open one, then re-evaluate. Many CI configs only fire on `pull_request` events; without a PR there is nothing to monitor.

### Step 2: Wait for CI checks

- With PR: read the run IDs from `GH_TOKEN=$(gh auth token --user <account>) gh pr checks`, then poll a one-shot `GH_TOKEN=$(gh auth token --user <account>) gh run view <id> --json status,conclusion` every 60 seconds, at most 20 times, and every 3 minutes while the run is `queued`; GitLab: `glab ci status -F json` on the same schedule.
- Without PR, only when CI fires on push, e.g. branch protections or scheduled workflows: the same bounded poll on the run ID from `GH_TOKEN=$(gh auth token --user <account>) gh run list --branch <branch> --limit 1`.
- When the poll budget runs out, report and stop. Schedule a wakeup and re-poll if the loop is still active.

### Step 3: Evaluate CI

- All functional checks pass: proceed to Step 6, AI comment sweep. Do NOT exit yet.
- Any functional check fails: proceed to Step 4.

### Step 4: Diagnose CI failure

Fetch failed logs, parallel. Search for existing fixes first. Present diagnosis per failure.

### Step 5: Fix CI failure

- Apply fix, stage specific files, commit, its own commit, conventional format, push.
- Return to Step 2 on the new SHA.
- Stop only on user request or after the guardrail cycle limit.

### Step 6: AI-tool comment sweep

Fetch every open comment authored by AI bots, across every channel, and close them all. This step is mandatory in `--pipeline` mode and runs every time CI is green, including after a CI fix push.

**Optional delegation to `/respond`.** When the environment variable `RESPOND_DRIVES_PIPELINE=1` is set, this step delegates to `/respond --auto --include-bots` instead of running the inline sweep below. The delegated workflow gives unified vocabulary and unified bot triage with the human-thread flow, and routes through the same hooks. To take effect, the user must also set `RESPOND_AUTO_ACK=1` since `/respond --auto` requires the second lock. The default behavior, when the env var is unset, is the inline sweep documented in 6a through 6e.

The delegation is opt-in to preserve backward compatibility. Existing `--pipeline` invocations continue to work without changes.

#### 6a: Fetch open AI-tool comments across every channel

Read [`../../standards/pr-comment-channels.md`](../../standards/pr-comment-channels.md) and use its canonical fetch. Inline review threads are one channel of four. AI reviewers post their summary and often their highest-severity findings as a review body or a PR-level conversation comment, neither of which appears in `reviewThreads`. Sweeping only inline threads lets a bot's blocking finding through while the loop reports the PR as clean.

The four GitHub channels are `reviewThreads`, `reviews`, `comments`, and `timelineItems` filtered to `PULL_REQUEST_COMMIT_COMMENT_THREAD`. The standard carries the exact query. Do not hand-roll a narrower one.

Filter the result to comments that are non-terminal per the standard's Terminal States table, then keep those whose author login matches the AI-bot list. The match is a case-insensitive substring match on the login, with or without a `[bot]` suffix, since the GraphQL API omits it, and includes, non-exhaustive: `coderabbit`, `copilot`, `greptile`, `sourcery`, `korbit`, `bito`, `qodo`, `codium`, `cursor`, `tabnine`, `gemini-code-assist`, `chatgpt-codex-connector`, `claude`. A login outside the list that still looks automated is reported, never treated as human by default.

Two filters that look right and are not: `isResolved == false` alone misses the three channels that have no `isResolved` field, and `isOutdated == true` is not a terminal state.

#### 6b: Triage each finding

For every open item, read the full comment body for the unabridged text, then classify. Inline thread comments come from `GH_TOKEN=$(gh auth token --user <account>) gh api repos/<owner>/<repo>/pulls/comments/<databaseId> --jq '.body'`. Review bodies, PR-level comments, and commit comments already arrive in full from the canonical fetch.

| Classification | Action |
|---------------|--------|
| Actionable + valid | Apply the fix. Each fix becomes its own commit. |
| Already resolved by prior code | Verify the current code resolves the issue, then close the thread. |
| False positive | Close the thread. |
| Out of scope | Fix it anyway when it is small, then close the thread. When it is genuinely blocked outside this change, close the thread and name the blocker in the pull-request description. |

This loop handles bot findings, and a bot thread receives no reply, per [`../../rules/pr-comment-discipline.md`](../../rules/pr-comment-discipline.md). Close it by resolving where the channel allows and by minimizing where it does not. Never close a thread without either fixing the issue or verifying that the finding does not hold.

#### 6c: Apply fixes

Group related fixes per file when possible. Run formatter, linter, typechecker, tests, and build locally before committing. Push once per logical fix group.

#### 6d: Close each item

After the fix is verified and pushed, or after the finding has been checked and does not hold, close the item. How to close depends on the channel, per the standard's "Answering Each Channel" table.

Inline review threads resolve through GraphQL:

```bash
GH_TOKEN=$(gh auth token --user <account>) gh api graphql -f query='mutation($threadId: ID!) {
  resolveReviewThread(input: { threadId: $threadId }) {
    thread { id isResolved }
  }
}' -F threadId=<thread-node-id>
```

Review bodies, PR-level comments, and commit comments have no resolve action, and a bot receives no reply, so minimizing is the close action:

```bash
GH_TOKEN=$(gh auth token --user <account>) gh api graphql -f query='mutation($id: ID!) {
  minimizeComment(input: { subjectId: $id, classifier: RESOLVED }) {
    minimizedComment { isMinimized minimizedReason }
  }
}' -F id=<comment-node-id>
```

The evidence a finding was considered is the commit that answers it, or the absence of one plus a minimized thread. Both are visible on the pull request and both outlast a comment. When the account lacks permission to minimize, leave the item open and report it rather than posting a comment to mark it handled.

GitLab uses `glab api` with the discussion resolve endpoint. Bitbucket Cloud resolves via `POST .../comments/<cid>/resolve`.

#### 6e: Loop back

After every push triggered by Step 6, return to Step 2. New AI tools often re-review the new SHA and may post fresh threads. The loop is not complete until a full pass finds zero open AI threads AND CI is green on the same SHA.

### Step 7: Final verification and exit

Only when **both** conditions hold on the latest SHA:

- `GH_TOKEN=$(gh auth token --user <account>) gh pr checks <pr>` shows every functional check as `pass`, manual gates excluded.
- The canonical four-channel fetch returns zero non-terminal AI-bot comments, across `reviewThreads`, `reviews`, `comments`, and commit-comment threads.

Run the Completeness Cross-Check from [`../../standards/pr-comment-channels.md`](../../standards/pr-comment-channels.md) before exiting.

Report per-channel counts, never a single total. A bare "0 open threads" cannot distinguish "all four channels are clean" from "only one channel was queried", which is the ambiguity that let a blocking comment through in the first place.

```
PR #1234  SHA a1b2c3d
CI: 12/12 functional checks passed
AI comments closed:  inline 3 resolved | review bodies 1 minimized | PR-level 2 minimized | commit 0
Human comments open: inline 0 | review bodies 0 | PR-level 1 | commit 0  -> run /respond
```

### Guardrails

- Max 5 fix-and-retry cycles per loop run. Above the limit, stop and ask the user how to proceed.
- Only fix what you can confidently fix. When a finding does not survive the failure-scenario gate, close it without writing anything; when you cannot tell, leave it open and report it.
- Each fix is its own commit with a conventional-commit message.
- Never skip hooks. `--no-verify`.
- Never close an item without verifying the fix is on the pushed SHA.
- Never close comments authored by humans automatically, Step 6 covers AI bots only.
- Never scope the sweep to inline review threads. All four channels in [`../../standards/pr-comment-channels.md`](../../standards/pr-comment-channels.md) are in scope every pass.
- Use `ScheduleWakeup`, or equivalent when waiting on CI or AI re-review to avoid burning context on tight polling loops.

---

## Rules

- Never combine unrelated changes in one commit.
- Never use `git add -A` or `git add .`.
- Never include files with secrets.
- Always detect git platform from remote URL. Never assume GitHub or GitLab.
- Always detect base branch dynamically.
- Always check for uncommitted changes before PR operations.
- Always write body to temp file for shell safety.
- Never force push. Rebase only a branch that has never been pushed; resolve conflicts on a pushed branch with a merge.
- Never merge PRs. Only create or update.
- Never auto-approve Terraform applies or releases without user approval.
- Prefix every `gh` call with an inline `GH_TOKEN` for the account matched from the remote, per [`standards/multi-account-cli.md`](../../standards/multi-account-cli.md). Never switch the global active account.
- `--pipeline` and any `pr` flow that opens a PR must run the full Pipeline Monitoring loop. The loop only exits when CI is 100% green AND every AI-tool comment across all four channels is closed on the latest pushed SHA. Resolving partial state, CI green but comments open, or comments closed but CI red is not "done".

## Common Rationalizations

- "The checks rollup is green, so the loop is done": a green rollup can mean CI never ran on the head SHA. Confirm the functional checks ran on the latest pushed SHA, then sweep all four comment channels.
- "No open review threads, so no bot comments": inline threads are one channel of four. Bots post blocking findings as review bodies and PR-level comments too.
- "The changes are small, so one commit is fine": unrelated changes go in separate commits whatever their size.
- "A reply tells the bot the finding was handled": a bot thread gets no reply. The fix commit, or a resolved or minimized thread, is the record.
- "The rebase was clean, so a force push is safe": a pushed branch is never rebased, so no push of it ever needs force. Merge the base instead.

## Red Flags

- Stop and ask the user how to proceed when the loop reaches its fifth fix-and-retry cycle.
- Stop and stage file by file when the next command is `git add -A` or `git add .`.
- Stop and abort the rebase when `git rebase origin/<base>` hits conflicts, then report them.
- Stop and leave the item open, then report it, when the account lacks permission to resolve or minimize a bot comment.
- Stop and re-verify both exit conditions when a fix lands on a new SHA after one condition was already clean.

## Verification

- `git status` shows no staged leftovers, and each commit subject matches `<type>(<scope>): <subject>` within 50 characters.
- The final report prints per-channel counts for AI and human comments on the latest SHA, never a single total.
- `GH_TOKEN=$(gh auth token --user <account>) gh pr checks <pr>` shows every functional check as `pass` on that same SHA.
- Every `gh` call in the run carried an inline `GH_TOKEN`, and the global active account never changed.
- Temp files for PR bodies and release notes are deleted.

## Related skills

- `/review` -- Review code before or after creating a PR.
- `/respond` -- Address incoming human review comments on a PR you authored. Complements this skill's AI-bot loop with a workflow for the human-thread side.
- `/test` -- Run tests before shipping.
- `/infra` -- Manage Docker/DB before shipping.
- `/deploy` -- Merge and deploy after the PR is approved.
