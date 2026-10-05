---
name: babysit
description: |
  Babysit a GitHub PR to a green review approval, looping until the GOAL (fresh APPROVED +
  CI green + mergeable) is reached. Each pass verifies every review finding, fixes the
  valid ones, pushes back with evidence on the invalid, and replies on every thread. Use
  when the user says "babysit", "babysit the PR", "watch the PR", or "drive the PR to
  green". Never merges — a human does that.
license: MIT
metadata:
  author: Nicholas Sollazzo
  version: "3.0.0"
argument-hint: "<PR number> [owner/repo]"
---

# Drive a PR to green — goal loop

**Arguments:** the **PR number** (first argument) and optionally `owner/repo` (second). If
the repo is omitted, default to the current repo
(`gh repo view --json nameWithOwner -q .nameWithOwner`).

**GOAL:** the PR reaches `reviewDecision == APPROVED` — a *fresh* approval on the current
head commit — with **all CI checks green** and `mergeable == MERGEABLE`. Loop until then.
**A human still does the merge; you never merge.**

**You are the loop — do not delegate it away.** Run pass after pass *yourself* until the
GOAL is met. One pass = the full procedure below (observe → React protocol on any new
finding → evaluate the GOAL), **not** a bare status check. Between passes you only need to *wait* for
CI/review to land; use your harness's wait/recurring primitive for that (see the table
below), then run the next pass. The primitive controls **how you wait**, never **whether
you loop**. For a one-shot status check, run a single pass.

### Waiting between passes (per harness)

The loop is always yours; this is only how to *wait* between passes (and re-enter for the
long, blocked-on-a-human waits without holding a session open):

| Harness | Wait / re-enter primitive |
|---------|---------------------------|
| Claude Code | the `loop` skill (recurring; self-paces between passes), `schedule` (cron, for long/over-session waits), or a background `gh` poll that wakes you to run the next full pass |
| Nous Hermes | `cronjob` / `blueprint` |
| Grok Build | wait in-session — no interval scheduler; `/goal` mode natively iterates until verified (fits babysit's GOAL) |
| OpenAI Codex | wait in-session — no native scheduler; use `codex exec` under external cron for unattended recurrence |
| Any other / none | wait in-session (short sleep while CI/review run), then run the next pass |

## Operating principles (non-negotiable)

- **Never substitute a hand-rolled CI poll for this skill.** Watching `gh pr checks` /
  `gh pr view` in a background loop is **not** babysitting — it skips the React protocol
  (verify every finding, reply on every thread, resolve), which is the whole point. The
  `gh` snippet below is the *observe* step of a pass, not a standalone watcher to lift out.
  Each cycle is a full pass of *this* procedure.
- **Verify every finding against the code — do not capitulate.** Open the file, run the
  check, read the diff. A reviewer (review bot or human) can be wrong. Fix what's real;
  push back with evidence on what isn't. The code, the tests, and the runtime behavior are
  the authorities — not "the reviewer said so."
- **Always answer every review comment** with what you did — the fix + commit SHA, or the
  evidence-based reason you didn't change anything. Never leave one unanswered.
- **Never merge.** Drive to approval only.
- **Never mutate external state to force a gate green.** If a check is red because of live
  infrastructure state (a deploy gate, a shared CI resource, server state another job
  owns), you may diagnose it read-only but do NOT delete or modify shared resources to make
  the check pass — they may be another job's live workload. Report the cause and owner,
  notify the user, and keep looping at a slower pace (~20–30 min) until the state clears or
  the user intervenes.
- **Surgical fixes** — minimal, match surrounding style, conventional-commit messages with
  a `Co-Authored-By` trailer.

## Each pass (one iteration of the loop)

These commands are only the pass's **observe** step; work through the steps below to finish
the pass.

> In the snippets below, substitute the PR number and repo you were invoked with
> **literally**.

```bash
PR=<pr-number>
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)   # or the 2nd arg, if given
ME=$(gh api user --jq .login)
gh pr view "$PR" --repo "$REPO" --json reviewDecision,mergeable,state,headRefName
gh pr checks "$PR" --repo "$REPO"
# latest review from a non-self author (your own reply-comments surface as reviews — exclude them):
# NOTE: gh's --jq takes a single filter string and has no --arg; interpolate $ME via the shell instead.
gh api "repos/$REPO/pulls/$PR/reviews" --jq "[.[]|select(.user.login!=\"$ME\")]|max_by(.id)|{id,user:.user.login,state}"
```

1. **Is there a new review or unaddressed finding** since your last pass (a non-self review
   with id greater than the last you handled, or any open 🔴/🟡 thread)? If yes → run the
   **React protocol** below. If no → just re-evaluate the goal.
2. **Evaluate the GOAL:**
   - **Met** — `reviewDecision == APPROVED` (fresh, i.e. a non-self APPROVED review id newer
     than your last push) **and** every CI check passes **and** `mergeable == MERGEABLE`:
     report the green light, notify the user, remind them a human still merges, and **END
     the loop** (don't run another pass).
   - **Not met** — state what's outstanding and **continue the loop**. Pace the next check
     to when progress is expected: a re-review lands shortly after a push, so a short wait
     is right while CI/review run; use a longer wait if you're blocked on a *human* reviewer.
3. **Guard the green light:** know your repo's review policy. If pushing dismisses stale
   approvals (branch protection `dismiss_stale_reviews` on), avoid any push once approved.
   Even when it doesn't, every push re-triggers CI + a fresh review that can flip the
   verdict — so fix blocking findings, but leave 🟢 nice-to-haves for a moment you're
   re-opening the PR anyway (e.g. an update-with-base).

## React protocol (per review)

1. **Fetch** the review body + its unresolved inline comments:
   ```bash
   gh api "repos/$REPO/pulls/$PR/reviews/<REVIEW_ID>" --jq '.body'
   gh api graphql -f query='query($o:String!,$r:String!,$p:Int!){repository(owner:$o,name:$r){pullRequest(number:$p){reviewThreads(first:100){nodes{id isResolved comments(first:1){nodes{databaseId path line body}}}}}}}' -f o="${REPO%/*}" -f r="${REPO#*/}" -F p="$PR" \
     --jq '.data.repository.pullRequest.reviewThreads.nodes[]|select(.isResolved==false)|"thread=\(.id) cmt=\(.comments.nodes[0].databaseId) \(.comments.nodes[0].path):\(.comments.nodes[0].line)\n\(.comments.nodes[0].body)"'
   ```
2. **Verify each finding** by reading the actual code at the cited file:line — real bug, or
   false positive? **When a review carries several findings, verify them in parallel
   sub-agents** (Claude Code `Agent`/Task, Codex `worker`, Grok parallel sub-agents, Hermes
   `delegate_task`, OpenClaw `sessions_spawn`) — one finding per sub-agent, each returning
   real/not-real plus the `file:line` evidence. No sub-agents on your harness? Verify them
   sequentially. Either way, every finding is checked against the code before you act.
3. **Real** → minimal fix, `git commit` (conventional + `Co-Authored-By`), **reply** on the
   thread (fix + SHA), **resolve** the thread.
4. **False positive** → **reply** on the thread with the evidence (file:line, command
   output) for why it doesn't hold; don't change code; resolve only if genuinely
   refuted/addressed.
5. **Push** the fixes (batched) — re-triggers CI + a fresh review, which the next loop pass
   will pick up.

### Reply + resolve mechanics
```bash
gh api "repos/$REPO/pulls/$PR/comments/<COMMENT_DB_ID>/replies" --method POST -f body="✅ Fixed in <sha>. <what changed>"   # or pushback reasoning
gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -f id="<THREAD_NODE_ID>"
```

## Guardrails / gotchas

- **A red status posted by a review bot is its NO-GO verdict, not a CI failure.**
  Distinguish a bot-posted commit status (the bot's approve/reject signal) from the real CI
  checks (build / test / lint). They go red for different reasons and need different fixes.
- **`gh ... --jq` is gojq** (not local jq) — validate emoji / `test()` filters with real
  `gh` when unsure.
- **A review bot can post COMMENT-not-approved if it reviewed mid-CI** (a race); a clean
  re-review on stable green will approve. If it's genuinely stuck clean-but-unapproved,
  trigger a fresh review (a no-op push or a re-run) — don't spin silently.
- **PR title may need to pass a conventional-commit gate.** If a `pr-title`-style check
  fails, fix the title to match the changed files' type.
- **A `gh run rerun` re-evaluates live gates against current external state** — a rerun can
  go red on infra drift unrelated to your diff, and a red caused by transient state can pass
  on a later rerun with no code change. Check WHAT failed before assuming your diff caused it.
- **Intermittent `gh` HTTP 401s** on GraphQL / write endpoints are usually transient
  (re-check `gh auth status` — it stays clean). Retry once; if it persists on a write, fall
  back to the REST equivalent.

## Done

Goal met → report it, notify the user, remind them a human still merges, and stop looping
(don't run another pass).
