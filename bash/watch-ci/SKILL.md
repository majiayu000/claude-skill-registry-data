---
name: watch-ci
description: "Watch GitHub PR CI checks in the background and notify on completion. Use when: (1) User wants to monitor CI/CD status, (2) User says 'watch CI', 'check CI', 'monitor checks', or 'wait for CI', (3) User wants to know when checks pass or fail. Runs a background gh polling shell loop (NOT a subagent — near-zero token cost), sends macOS notification on completion. Also handles merged PRs by watching the target branch CI."
---

# Watch CI

Monitor GitHub PR CI checks in the background, notify on completion via macOS system notification.
Also supports watching CI on the merge target branch when a PR is already merged.

The polling itself is a pure shell loop (`gh` CLI + `jq`) launched via `Bash` with `run_in_background: true`. No subagent is spawned — token cost is paid only at launch and at completion, not on every poll cycle.

> **On Claude Code on the web** (`$CLAUDE_CODE_REMOTE=true`): follow [`web/web-mode.md`](../../web/web-mode.md). `gh` is unavailable, so the `gh`-based poll scripts won't run — poll CI through the GitHub MCP instead (`pull_request_read` with `get_check_runs`, or `actions_*` / `get_job_logs`), or the `Monitor` tool. There is no macOS notifier on web; just report status when checks finish. **When this watch is part of a `-m` merge flow** (`/prc -c -w`, or the Merge Mode of `/x-as-pr` / `/x-wt-teams`), follow **web-mode.md §8: poll in-turn and block** until the checks are terminal — Step 3's "launch a background poll and end the turn" model is **terminal-only**, because web has no background-task wakeup, so a background watch + turn-end would leave the merge unfired. Stay in the turn until terminal, then let the caller merge in the same run.

## Scripts

- `scripts/notify.sh` — macOS notification helper
- `scripts/poll-pr-checks.sh <pr-number> [max-min]` — poll an open PR's checks until terminal, then notify
- `scripts/poll-runs.sh <branch> <commit-sha> [max-min]` — poll workflow runs on a branch+commit until terminal, then notify

All scripts default to a 60-minute cap and a 30-second poll interval.

### False-pass guards — do NOT "simplify" these away

A green report from this skill is often what authorizes a merge, so a false pass is the
expensive failure mode. Both poll scripts carry three guards, added after a real incident
where a PR was reported **"All CI passed" while its actual workflow had not started**:

1. **A skipped check is not a passing check.** The original arithmetic was

   `passed = total - pending - failed`, which folded skips into the pass count. A single
   third-party `skipping` check therefore read as "1/1 ok". Both scripts now count the
   `pass` / `success` state explicitly and report skips as their own number.

2. **Checks that GitHub has not registered yet are invisible.** `gh pr checks` lists only

   registered checks, so a queued workflow (or one waiting on a concurrency group) does not
   appear at all — leaving one unrelated check to stand in for the whole PR.
   `poll-pr-checks.sh` therefore cross-checks `gh run list` for the head SHA and refuses to
   conclude while any run for that commit is not `completed`. Related: the server-side
   `gh run list --commit <sha>` filter has been observed to **omit queued runs** that
   `--branch` returns, so both scripts list by branch and match the SHA in `jq`.

3. **A terminal-looking state must hold for 2 consecutive polls** before it is believed,

   since both the check list and the run list lag a push by seconds.

**Exit codes:** `0` passed · `1` failed · `2` timeout · **`3` inconclusive** · `64` bad args.

**Exit 3 (`RESULT: INCONCLUSIVE`)** means checks reached a terminal state but *nothing
produced a result* — only skips, or no real checks. That is legitimate for a fully
path-filtered PR, but it is **not** a pass and must never be reported as one: the caller
decides what it means. Treat it the same as a red result for any merge decision.

**When reporting a pass to the user, sanity-check the job count.** If a repo normally runs
N workflows and the result names fewer, say so rather than reporting green — that mismatch
is exactly how the original bug surfaced.

## Workflow

### Step 1: Identify the PR

Determine which PR to watch:

```bash
# If user provides a PR number or URL, use it directly
# Otherwise, detect from current branch
gh pr view --json number,title,url,headRefName,baseRefName,state,mergeCommit --jq '{number,title,url,headRefName,baseRefName,state,mergeCommit}'
```

If no PR is found for the current branch, inform the user and stop.

**Check the PR state:**

- If `state` is `"OPEN"` → proceed to Step 2 (normal PR watch)
- If `state` is `"MERGED"` → proceed to Step 2b (merged PR: watch target branch CI)
- If `state` is `"CLOSED"` (not merged) → inform the user the PR was closed without merging and stop

### Step 2: Show Initial Status (Open PR)

Show the current state:

```bash
gh pr checks <PR_NUMBER> --json name,state,bucket,workflow
```

Report to the user: PR number/title, total checks, current status breakdown (passed/pending/failed).

If checks have already **failed**, skip to Step 5. If they *look* all-green, go to Step 4 — but
read its two confirmations first: an initial snapshot cannot distinguish "everything passed"
from "the real workflow has not registered yet", and taking the fast path on that snapshot is
the documented false-pass bug. Otherwise proceed to **Step 3**.

### Step 2b: Merged PR — Switch to Target Branch CI

When the PR is already merged:

1. Get the base branch and merge commit SHA from Step 1 output
2. Inform the user: "PR #123 is already merged into `main`. Watching CI on `main` for merge commit `abc1234`..."
3. Show initial status, filtered by the merge commit SHA:

   ```bash
   # Filter on headSha CLIENT-side. Server-side `--commit <sha>` has been observed to OMIT
   # queued runs that `--branch` does return (poll-runs.sh guard 2) — using it here would
   # make a still-queued workflow invisible and push this step into the missing-run branch
   # below for a run that is simply not started yet.
   gh run list --branch <base-branch> --limit 40 --json databaseId,name,headSha,status,conclusion \
     | jq --arg sha '<merge-commit-sha>' '[.[] | select(.headSha | startswith($sha))]'
   ```

   Runs take a few seconds to register after a merge. If none are found, **retry this
   same SHA-filtered query** 2-3 more times with a short delay (~10s) before concluding
   anything. Do **not** fall back to an unfiltered `gh run list --branch <base-branch>`
   as the result path — a run belonging to an unrelated commit can surface there and get
   misreported as this merge's outcome. A broader, unfiltered listing may still be shown
   alongside the determination below for context, but never in place of it.

4. If the SHA-filtered query still returns nothing after retrying, do **not** report "no

   CI detected" from that alone. Run the **push-trigger-check determination** — see
   [`references/push-trigger-check.md`](references/push-trigger-check.md), the single
   source of truth for this classification — and report one of its three outcomes:

- `EXPECTED_RUN_MISSING` → report a **failure**. A workflow should have run for this

     merge commit and did not; name the likely cause per the reference (a skip marker in
     the merge commit message, or a merge performed by Actions using `GITHUB_TOKEN`).

- `BENIGN_NO_TRIGGER` → report "no CI expected" **and name the specific reason** (no

     matching `push` trigger, excluded by a `branches`/`paths` filter, a disabled
     workflow, or Actions disabled repo-wide). Never report bare "no CI detected" without
     the reason.

- `INCONCLUSIVE` → surface it as unresolved — never as a pass, never as benign. State

     what could not be determined and why (unparseable workflow YAML, an API error, a
     truncated changed-file list).

   **One escape hatch back to Step 3:** the reference's Step 5 may find a run for this SHA
   that this step's listing missed and whose `status` is not yet `completed` (`queued`,
   `in_progress`, `waiting`, `requested`). That is "not yet", not a verdict — do **not**
   classify it into any of the three outcomes. Go to **Step 3** and poll it instead.
   Otherwise do not proceed to Step 3 in this branch — there is nothing to poll.

5. If runs were found (on the initial query or a retry), proceed to **Step 3** to poll

   them to a terminal state.

### Step 3: Launch Background Poll (CLI-only, no subagent)

**Do NOT launch a subagent.** Use the Bash tool with `run_in_background: true` to run the polling shell script. The script polls `gh` directly, exits when checks reach a terminal state, fires a macOS notification, and prints a final `RESULT:` line.

For an open PR:

```
bash $HOME/.claude/skills/watch-ci/scripts/poll-pr-checks.sh <PR_NUMBER>
```

For a merged PR:

```
bash $HOME/.claude/skills/watch-ci/scripts/poll-runs.sh <BASE_BRANCH> <MERGE_SHA>
```

Behaviour:

- Polls every 30 seconds (open PR: `gh pr checks`; merged PR: `gh run list --branch ...` with the SHA matched client-side in `jq` — **not** `--commit`, which can hide queued runs)
- On **success**: `notify.sh success` (Glass sound) + `RESULT: PASSED` to stdout, exit 0
- On **failure**: `notify.sh error` (Basso sound) with failed check names + `RESULT: FAILED (<names>)`, exit 1
- On **timeout** (default 60 min): `notify.sh warning` (Purr sound) + `RESULT: TIMEOUT`, exit 2
- On **inconclusive** (runs completed but none produced a `success`, only skips): `notify.sh warning` + `RESULT: INCONCLUSIVE (...)`, exit 3 — this is `poll-runs.sh`'s own guard against reporting a fluke pass (see the false-pass guards above); it is **not** a pass

After launching, tell the user: "Watching CI in background. You'll be notified when it completes."

When the background task completes you'll be notified automatically. Read its output file to see the `RESULT:` line, report to the user, and — if `FAILED` **or** `INCONCLUSIVE` — treat it as a problem, not a green light: for `FAILED`, proceed to Step 5's investigation steps; for `INCONCLUSIVE`, report it as unresolved and do not authorize a merge on it (same handling as the `INCONCLUSIVE` push-trigger-check outcome in Step 2b).

### Step 4: All Checks Passed (Foreground Fast Path)

**This fast path is where the false-pass bug bites hardest**, because it skips the polling
loop that carries the guards. An initial `gh pr checks` snapshot showing "everything green"
is exactly what an un-started workflow looks like. So before taking it:

1. **Confirm nothing is still queued for the head commit** — a run that is `queued` /

   `in_progress` means CI has not finished, whatever the check list says:

   ```bash
   SHA=$(gh pr view <PR_NUMBER> --json headRefOid -q .headRefOid)
   BR=$(gh pr view <PR_NUMBER> --json headRefName -q .headRefName)
   gh run list --branch "$BR" --limit 40 --json headSha,name,status,conclusion \
     | jq --arg sha "$SHA" '[.[] | select(.headSha == $sha)]'
   ```

2. **Confirm at least one check actually passed** — not merely "none failed". A list of

   only `skipping` buckets is `RESULT: INCONCLUSIVE`, not a pass.

If either confirmation fails, **do not use this fast path** — fall through to Step 3 and let
the poll script settle it.

Once both hold:

1. Send notification:

   ```bash
   bash $HOME/.claude/skills/watch-ci/scripts/notify.sh success "All CI checks passed! PR #<number>"
   ```

2. Report the final status summary, naming the jobs that passed and any that were skipped.

### Step 5: CI Check Failed (Foreground Fast Path)

If checks already failed at Step 2/2b:

1. Send notification:

   ```bash
   bash $HOME/.claude/skills/watch-ci/scripts/notify.sh error "CI check failed: <check-name>. PR #<number>"
   ```

2. Investigate the failure:

   ```bash
   gh pr checks <PR_NUMBER> --json name,state,bucket,link --jq '[.[] | select(.bucket == "fail" or .bucket == "cancel")]'
   gh run list --branch <branch> --status failure --limit 5 --json databaseId,name,conclusion
   gh run view <run-id> --log-failed
   ```

3. Analyze and report. For open PRs: offer to fix. For merged PRs: report only, do NOT auto-fix on the target branch.

## Notes

- Polling is a pure shell loop run via `Bash run_in_background: true` — no subagent, no per-cycle token cost. The main conversation only pays at launch and at completion.
- System notifications use macOS `osascript` via `notify.sh`
- The `gh` CLI must be authenticated and have access to the repository
- 30-second polling interval balances responsiveness with API rate limits
- Default cap 60 minutes; override with the optional `[max-min]` arg to either script
- For merged PRs, watches workflow runs on the target branch filtered by merge commit SHA
- The script's stdout (progress lines + final `RESULT:` line) is captured by the background task — read the output file when you get the completion notification
- Each progress line reports `pass / fail / skip / pending` separately rather than a single

  `N/M ok` ratio, so a run carrying skipped checks is legible at a glance instead of being
  rounded up into the pass count

- **`RESULT: PASSED` is the only line that authorizes a merge.** `RESULT: INCONCLUSIVE`

  (exit 3) means nothing actually ran — treat it as not-green and investigate

- On web, where these `gh` scripts can't run, the MCP polling that replaces them needs the

  same three guards — skips aren't passes, queued runs block the verdict, and let the state
  settle before believing it
