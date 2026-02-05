---
name: enter-merge-queue
description: Guarantee a PR merges by repeatedly rebasing from the base branch, fixing CI, addressing Gemini review feedback, enabling auto-merge, and waiting until the PR is merged. Use when you are asked to babysit a PR through the merge queue, resolve CI failures, handle Gemini review threads, or keep a branch up to date until merge.
---

# Enter Merge Queue

Ensure a PR merges by looping through base updates, review handling, CI monitoring, and auto-merge until the PR is actually merged.

## Setup

Determine the repository for all `gh` commands:

```bash
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
```

Always pass `-R "$REPO"` to `gh` commands.

Track these state flags:

- `has_bumped_version`: Boolean, starts `false`. Set to `true` after version bump is applied.
- `has_waited_for_gemini`: Boolean, starts `false`. Set to `true` after waiting once for Gemini.
- `gemini_can_review`: Boolean, starts `true`. Set to `false` if PR contains only non-code files.
- `associated_issue_number`: Number or null. Track the issue to mark `needs-qa` after merge.

Use polling jitter with ±20% randomization:

```text
actual_wait = base_wait × (0.8 + random() × 0.4)
```

## Workflow

1. Verify the PR exists and collect metadata.

   ```bash
   gh pr view --json number,title,headRefName,baseRefName,url,state,labels,files,body -R "$REPO"
   ```

   - Store `baseRefName` for rebase.
   - Detect `high-priority` label.
   - If all files are non-code types, set `gemini_can_review = false`:
     - Config: `.json`, `.yaml`, `.yml`, `.toml`, `.ini`, `.env*`
     - Docs: `.md`, `.txt`, `.rst`
     - Assets: `.png`, `.jpg`, `.svg`, `.ico`, `.gif`
     - Build/CI: `Dockerfile`, `.dockerignore`, `.gitignore`

   Handle issue tracking:

   - Remove auto-close language from PR body (`Closes #`, `Fixes #`, `Resolves #`).
   - If no issue is referenced, search for an open issue referencing the PR number; create one if missing.
   - When creating the issue, describe the work from the PR and add the `needs-qa` label immediately.
   - Store the issue number as `associated_issue_number`.

2. Ensure you are on the PR head branch, not `main`.

3. Mark as queued in the UI and move the tmux window to the front:

   ```bash
   setQueued.sh "(queued) #<pr-number> - <branch>"
   ```

4. Main loop until PR is merged:

   4a. Yield to high-priority PRs unless the current PR has `high-priority`.

   - List high-priority PRs and check their `mergeStateStatus`.
   - Yield if any high-priority PR is `CLEAN`, `BLOCKED`, `BEHIND`, `UNKNOWN`, `UNSTABLE`, or `HAS_HOOKS`.
   - Skip yielding if all high-priority PRs are `DIRTY`.

   4b. Check merge status:

   ```bash
   gh pr view --json state,mergeStateStatus,mergeable -R "$REPO"
   ```

   - `MERGED`: exit loop.
   - `BEHIND`: update from base (4c).
   - `BLOCKED` or `UNKNOWN`: handle Gemini feedback while waiting for CI (4d/4e).
   - `CLEAN`: enable auto-merge (4f).
   - **Note**: You can merge your own PRs once the branch is up to date, all required checks pass, and Gemini feedback is fully addressed. If blocked, confirm those three conditions before waiting longer.

   4c. Rebase on base and bump version once:

   ```bash
   git fetch origin <baseRefName> >/dev/null
   git rebase -X theirs origin/<baseRefName> >/dev/null
   ```

   If rebase conflicts:
   - Prefer upstream changes and attempt an automatic resolution:
     - List conflicts: `git diff --name-only --diff-filter=U`
     - For each conflicted file, checkout upstream: `git checkout --theirs <file>`
     - Stage all resolved files: `git add <file>`
     - Continue: `git rebase --continue`
   - If conflicts persist after preferring upstream:
     - Run `git rebase --abort` to restore the branch
     - List the remaining conflicting files
     - Clear the queued status with `clearQueued.sh`
     - Stop and ask the user for help.

   If `has_bumped_version` is `false`, run `bumpVersion.sh`, stage the version files, amend the last commit with a GPG-signed message, and set `has_bumped_version = true`. Force push after rebase:

   ```bash
   git push --force-with-lease >/dev/null
   ```

   4d. Address Gemini feedback (parallel with CI):

   **IMPORTANT**: Do NOT wait for CI to complete before addressing Gemini feedback. Handle Gemini feedback while CI is running to maximize efficiency.

   **Initial Gemini check** (if `has_waited_for_gemini` is `false`):

   ```bash
   gh pr view <pr-number> --json reviews -R "$REPO"
   ```

   Poll every 30 seconds (with jitter) for up to 5 minutes for `gemini-code-assist`. Set `has_waited_for_gemini = true` after first review is found.

   If Gemini reports unsupported file types, set `gemini_can_review = false` and continue to CI.

   **Address feedback while CI runs**:

   - Use `/address-gemini-feedback` and `/follow-up-with-gemini`.
   - Reply in-thread:
     - List review comments: `gh api /repos/$REPO/pulls/<pr-number>/comments`
     - Reply in-thread: `gh api -X POST /repos/$REPO/pulls/<pr-number>/comments -F in_reply_to=<comment_id> -f body="...@gemini-code-assist ..."`
     - List general PR comments (issue comments): `gh api /repos/$REPO/issues/<pr-number>/comments`
     - Reply to general PR comments: `gh api -X POST /repos/$REPO/issues/<pr-number>/comments -f body="...@gemini-code-assist ..."`
   - **Push commits before tagging Gemini with a hash** so the hash links on GitHub and is reviewable.
   - When replying that a fix is complete, **include the commit hash (not just the message) and explicitly ask if the change addresses the issue** (e.g., "Commit <hash> ... does this address the issue?").
   - Analyze Gemini's sentiment in follow-up replies:
     - If Gemini confirms/approves and does not request more changes, resolve the thread.
     - If Gemini is uncertain or requests more work, keep the thread open and iterate.
   - Never use `gh pr review` or GraphQL review comment mutations to reply (they create pending reviews).
   - Include relevant commit hashes in replies (not just titles).
   - **Do NOT wait for all threads to be resolved before proceeding to CI monitoring** - continue to step 4e and handle remaining Gemini feedback in parallel.

   4e. Wait for CI with adaptive polling and branch freshness checks:

   ```bash
   git rev-parse HEAD
   gh run list --commit <commit-sha> --limit 1 --json status,conclusion,databaseId -R "$REPO"
   ```

   Poll cadence (with jitter):
   - 0-5 min: every 1 min
   - 5-15 min: every 2 min
   - 15+ min: every 3 min

   At each poll, check if the branch is behind:

   ```bash
   gh pr view --json mergeStateStatus -R "$REPO"
   ```

   If `BEHIND`, return to 4c immediately.

   When CI completes:
   - Pass: continue to 4f.
   - Cancelled: rerun with `gh run rerun <run-id> -R "$REPO"`.
   - Failed: run `/fix-tests`, add tests for coverage failures, and re-run coverage locally.

   4f. Enable auto-merge and wait:

   If `has_bumped_version` is still `false`, perform the bump, amend, force push, and return to 4e.

   ```bash
   gh pr merge --auto --merge -R "$REPO"
   gh pr view --json state,mergeStateStatus -R "$REPO"
   ```

   - Only enable auto-merge after:
     - All required status checks pass
     - Branch is up to date with `main` (not `BEHIND`)
     - Gemini feedback is fully addressed (per sentiment analysis)
   - If auto-merge is unavailable, try a direct merge (same conditions) and continue polling.

   Poll until `MERGED`. If `BEHIND`, return to 4c.

5. Refresh workspace after merge:

   ```bash
   refresh.sh
   ```

   Post-merge QA handling for `associated_issue_number`:
   - Reopen the issue if closed.
   - Ensure the `needs-qa` label is applied.
   - Prefer updating the issue body with merge status.

6. Report success with PR URL, a short description of the merged changes, and the associated issue status.

## Keeping PR Description Updated

As you iterate, update the PR body with `gh pr edit --body`. Always remove auto-close language (`Closes/Fixes/Resolves #...`) and track the issue separately - all issues are marked `needs-qa` after merge. Always preserve the Claude-style format:

```text
## Summary
- <verb-led, concrete change>

## Testing
- <command run or "not run (reason)">

## Issue
- #<issue-number>

Agent: <agent-id>
```

If there is no associated issue, use `## Related` instead of `## Issue`.

When updating the body, recompute the agent id and ensure the PR body ends with the evaluated value:

```bash
AGENT_ID=$(basename "$(git rev-parse --show-toplevel)")
```

Then ensure the PR body ends with `Agent: ${AGENT_ID}`. Add bullets for significant changes (CI fixes, Gemini feedback addressed).

## Token Efficiency

Suppress stdout on git commands:

```bash
git push --force-with-lease >/dev/null
git push >/dev/null
git commit -S -m "message" >/dev/null
git fetch origin <baseRefName> >/dev/null
git rebase origin/<baseRefName> >/dev/null
```

Always use minimal `--json` fields and avoid redundant fetches.
