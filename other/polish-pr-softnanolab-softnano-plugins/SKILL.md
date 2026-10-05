---
name: polish-pr
description: Address Codex review comments on an open PR, re-run thermo-nuclear-code-quality-review, sync with the base branch, and push the updates. Use after a Codex (or human) review has landed on a PR you opened — the skill resolves each comment in code, marks the GitHub review thread resolved, then rebases/merges any new base-branch commits before pushing.
argument-hint: "[pr-number (default: PR for current branch)] [--base <branch>] [--no-rebase]"
allowed-tools: Bash, Read, Grep, Glob, Agent, Write, Edit
---

# Polish PR

End-to-end follow-up pass for a PR that has accumulated review feedback. Pulls open Codex review threads, fixes each one in code, marks the thread resolved on GitHub, re-runs the thermo-nuclear review, syncs with the base branch, and pushes.

## Input

<args>
$ARGUMENTS
</args>

Parse `$ARGUMENTS`:
- Optional PR number. If absent, resolve the PR for the current branch with `gh pr view --json number,baseRefName,headRefName,url`.
- `--base <branch>` overrides the detected base branch.
- `--no-rebase` skips Step 4 (sync with base) — use only if the user explicitly asks.

## Step 0: Pre-flight

Run in parallel:

```bash
git rev-parse --is-inside-work-tree
git rev-parse --abbrev-ref HEAD
git status --porcelain
gh auth status
gh pr view <pr> --json number,url,headRefName,baseRefName,state,isDraft,mergeable
```

Create a writable job directory for downloaded review metadata:

```bash
JOB_DIR="${CLAUDE_JOB_DIR:-$(mktemp -d -t softnano-polish-pr.XXXXXX)}"
```

Hard stops:

- Not a git repo / `gh` not authenticated.
- PR is `CLOSED` or `MERGED`.
- Uncommitted changes — ask whether to commit, stash, or abort. Polishing on a dirty tree leads to mixed-up commits.
- Local branch ≠ PR head branch — checkout the PR head first (`gh pr checkout <pr>`) and confirm with the user before continuing.

Save `PR_NUMBER`, `BASE`, `HEAD`, and `REPO` (`gh repo view --json nameWithOwner -q .nameWithOwner`) for later steps.

## Step 1: Fetch open review threads (Codex + humans)

GitHub exposes review threads only via GraphQL — REST gives you comments but not the `isResolved` flag, so you cannot tell which threads still need work from REST alone. Use GraphQL:

```bash
gh api graphql -f query='
  query($owner:String!, $repo:String!, $pr:Int!) {
    repository(owner:$owner, name:$repo) {
      pullRequest(number:$pr) {
        reviewThreads(first:100) {
          nodes {
            id
            isResolved
            isOutdated
            path
            line
            comments(first:20) {
              nodes { databaseId author { login } body createdAt url }
            }
          }
        }
      }
    }
  }' -F owner=<owner> -F repo=<repo> -F pr=<pr> \
  > "$JOB_DIR/threads.json"
```

Also pull general PR conversation comments (Codex sometimes posts a top-level summary review):

```bash
gh pr view <pr> --json reviews,comments > "$JOB_DIR/pr_meta.json"
```

Filter `threads.json` to threads where `isResolved == false`. Bucket them:

- **Codex threads** — author login is `chatgpt-codex-connector[bot]`, `codex[bot]`, or any login containing `codex`. These are the primary target.
- **Human threads** — everything else still unresolved. Surface these to the user but do not auto-resolve unless the user opts in.
- **Outdated threads** (`isOutdated: true`) — the line they reference no longer exists. Read the original comment, judge whether the concern is already addressed in the current code; if yes, just resolve the thread; if no, treat like an active thread.

If there are no unresolved Codex threads **and** the user did not pass `--force`, skip Step 2 and go straight to Step 3 — there is nothing review-driven to address.

## Step 2: Address each Codex thread

For each unresolved thread, in source order (group by file, then by line):

1. Read the comment body and the surrounding code (the file at `path` around `line`, plus any references the comment names).
2. Decide: **fix in code**, **reply and resolve** (the comment is wrong or already addressed), or **escalate to user** (judgment call, ambiguous, or out of scope).
3. If fixing: edit the file. Keep the fix minimal and scoped to what the comment asked for — do not bundle unrelated cleanup. If the fix touches code outside the review's stated scope, stop and confirm with the user.
4. After the fix lands (or if you decided "already addressed"), resolve the thread:

   ```bash
   gh api graphql -f query='
     mutation($id:ID!) {
       resolveReviewThread(input:{threadId:$id}) {
         thread { id isResolved }
       }
     }' -F id=<thread-id>
   ```

5. Reply to the thread with a one-line note before resolving, so the trail on GitHub is legible:

   ```bash
   gh api "repos/<owner>/<repo>/pulls/<pr>/comments/<comment-id>/replies" \
     -f body="Addressed in <short-sha>: <one-line description>."
   ```

   Use the first comment's `databaseId` from the thread as `<comment-id>`. Omit this if the thread had no fix (e.g. you concluded it was already addressed — say so in the reply).

**Do not resolve threads you did not actually act on.** If you skip one (escalated to user, or unclear), leave it unresolved and list it in the final report.

Commit the fixes in logical groups — one commit per concern is fine, but bundle obvious siblings (e.g. the same typo across three files). Commit messages: `address review: <short summary>`. Reference thread URLs in the body if helpful.

## Step 3: Re-run thermo-nuclear-code-quality-review

Invoke the `thermo-nuclear-code-quality-review` skill against the current diff (`$BASE..HEAD`). Treat its findings the same way as Codex threads:

- **Blocker / should-fix** findings — address in code (another commit), then continue.
- **Nit** findings — list them in the final report; let the user decide.

If thermo-nuclear flags something that contradicts a Codex resolution from Step 2, stop and surface the conflict to the user — do not silently revert either side.

## Step 4: Sync with the base branch

Skip if `--no-rebase` was passed.

```bash
git fetch origin <base> --prune
NEW=$(git rev-list --count HEAD..origin/<base>)
echo "new commits on $base since branch point: $NEW"
```

If `NEW == 0`, nothing to do — skip the rest of this step.

Otherwise, prefer **rebase** unless the PR already has review commits the user wants preserved as merge history (ask if unsure):

```bash
git rebase origin/<base>
```

On conflict: do **not** auto-resolve. Surface the conflicted files and stop. The user resolves, then re-runs the skill (which will pick up at Step 5).

If the user explicitly prefers merge, use `git merge origin/<base> --no-ff -m "Merge <base> into <head>"` instead.

## Step 5: Push and report

If Step 2/3 made commits or Step 4 rewrote history:

```bash
# Rebase rewrites history, so a force-push is required — but only with-lease,
# never plain --force. With-lease aborts if the remote moved (someone else
# pushed in the meantime); plain --force would silently overwrite their work.
if <step 4 rebased>; then
  git push --force-with-lease
else
  git push
fi
```

If nothing changed (no unresolved threads, no thermo-nuclear findings, no base drift): say so plainly and stop — do not push an empty update.

Final report to the user:

```markdown
## Polish summary for PR #<n>

### Codex threads
- Resolved: <count>
  - <file:line> — <one-line of what was fixed>
- Skipped / escalated: <count>
  - <file:line> — <why>

### Thermo-nuclear pass
- <verbatim summary or "no new findings">

### Base sync
- <"up to date" | "rebased onto <N> new commits on <base>" | "skipped per --no-rebase">

### Pushed
- <"yes — <sha>" | "no changes to push">

PR: <url>
```

## Notes

- **Never** resolve a human reviewer's thread without their explicit OK — only Codex threads are auto-resolvable. Humans expect to click the button themselves.
- **Never** force-push without `--force-with-lease`. Never force-push if the user said `--no-rebase` and no rebase happened.
- If the PR is a draft and all review threads close cleanly, ask whether to mark it ready (`gh pr ready <pr>`) — don't do it unprompted.
- Codex sometimes posts the same concern as both a top-level review comment (in `pr_meta.json`) and an inline thread. Address it once; resolve the inline thread; the top-level review will auto-stale.
- If `gh pr checkout <pr>` is needed in Step 0, run it before any edits — editing the wrong branch and force-pushing is the worst possible failure mode for this skill.
