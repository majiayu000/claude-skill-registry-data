---
name: pr-babysit
description: >
  Babysit a GitHub PR to completion: pre-push quality gate, CI watch,
  Copilot/reviewer comment sweep (fix, reply, resolve threads, re-arm until
  zero), paced inline comment posting, and post-merge cleanup. Use when user
  says "babysit the PR", "watch the PR", "fix the copilot comments", "monitor
  checks and fix comments", "post the review comments", "/pr-babysit", or asks
  to keep a PR green until reviewers have nothing left to say. Works on any
  repo with gh auth.
---

Drive a PR until CI is green and every review thread is addressed. The end
state the user expects: "Copilot has nothing to say."

Pairs with `pr-post-comments` (voice rules and the paced posting driver) and
`pr-address-review` (the human-feedback side of the same loop).

```bash
POST=~/.claude/skills/pr-post-comments/scripts/post_pr_comments.py  # adjust if installed elsewhere
```

## Hard stops (non-negotiable)

- NEVER merge the PR. Green + zero comments = report and stop. Merge only on
  an explicit "merge it" in the current conversation.
- NEVER remove, dismiss, or disable the Copilot reviewer. The goal is a PR so
  clean it has nothing to flag, not silencing it.
- Show comment/reply drafts before anything is posted. Once the user says
  "post", the approved drafts go out without re-confirmation.
- Only `$POST` creates comments. No `gh api .../replies`, no `gh pr comment`,
  no loop.
- No attribution anywhere (commit messages, PR body, replies).

Resolve OWNER/REPO from `gh repo view --json nameWithOwner` once; export
`PR=<number>`.

## Phase 0 - Pre-push gate (make Copilot mute before it speaks)

Run before every push, lint FIRST (a lint failure at the end of a chain
wastes the whole test run). If a repo-specific gate skill or hook exists, it
runs here instead.

1. Format + lint: `ruff check && ruff format --check` / `npx eslint` /
   `npx prettier --check` - whatever the touched services use.
2. Types: `mypy` / `tsc --noEmit`.
3. Tests for touched code, then the full affected suite.
4. Self-review the diff as Copilot would. Recurring flags to kill in advance:
   unused imports/vars, missing error handling on new I/O, magic numbers,
   missing docstrings on new public functions, untested branches, leftover
   debug prints, secrets.
5. Scope check: diff contains ONLY the task's files - no CLAUDE.md, agent
   configs, PRDs, planning artifacts. Docs-only branches stay docs-only.

## Phase 1 - CI watch

Background task (Bash `run_in_background: true`). Bare `sleep N; check` is
blocked by the harness - use a bounded until-loop:

```bash
i=0
until [ "$(gh pr checks $PR --json bucket --jq '[.[] | select(.bucket=="pending")] | length' 2>/dev/null)" = "0" ]; do
  i=$((i+1)); [ $i -gt 45 ] && { echo TIMEOUT; break; }
  sleep 30
done
gh pr checks $PR 2>&1 | grep -vE 'skipping|pass'
```

Red check: pull the failing job log
(`job_id=$(gh pr checks $PR | grep '<job>' | grep -o 'job/[0-9]*' | cut -d/ -f2); gh run view --job $job_id --log`),
fix, commit, push, re-arm this phase.

## Phase 2 - Comment sweep loop

Repeat until exit condition; re-arm after every push.

1. Snapshot HEAD: `gh pr view $PR --json headRefOid --jq .headRefOid`.
2. Wait for Copilot's pass on that commit (it reviews each push). Poll with
   the until-loop pattern, ~10 min budget; filter by
   `created_at > <push time>`:
   `gh api "repos/$OWNER/$REPO/pulls/$PR/comments?per_page=100" --paginate -q '.[] | select(.created_at > "<ISO>") | "[\(.id)] \(.user.login) \(.path):\(.line // .original_line) \(.body)"'`
   Copilot posts as `copilot-pull-request-reviewer[bot]`. Also check review
   bodies: `gh api repos/$OWNER/$REPO/pulls/$PR/reviews -q '.[] | "\(.user.login): \(.state)"'`.
3. List unresolved threads:

```bash
gh api graphql -f query='{repository(owner:"'$OWNER'",name:"'$REPO'"){pullRequest(number:'$PR'){reviewThreads(first:100){nodes{id isResolved isOutdated path line comments(first:1){nodes{databaseId author{login} body}}}}}}}' \
  --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved==false)'
```

4. Triage every unresolved thread - none skipped, none half-done. The rule
   is permanent and has no exceptions:
   - **Copilot / bot thread: fix it in code, then resolve it. Never reply.**
     No rebuttal, no "pre-existing", no "follow-up". If the fix collides with
     a teammate's contract, fix it anyway and tell the user who must adapt.
     A thread whose flagged code is already gone is resolved as fixed.
   - **Human thread: fix it in code, then reply. Never resolve it**; the
     reviewer closes their own thread.
   - Replies go through `$POST`. Load the user's voice skill first if one is
     installed (for example `Skill("voice-of-er")`); the voice rules in
     pr-post-comments Step 3 apply either way. Write
     `[{"in_reply_to": <databaseId>, "body": "..."}]`, dry-run
     `python3 "$POST" $OWNER/$REPO $PR replies.json --check`,
     then the same command without `--check` with `run_in_background: true`.
5. Resolve each fixed bot thread (never a human's):

```bash
gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -f id=$tid --jq '.data.resolveReviewThread.thread.isResolved'
```

6. Pushed fixes? Go to Phase 1. Copilot re-reviews the new commit -
   re-enter this phase for it.

Exit: CI green AND unresolved threads = 0 AND one full poll cycle with no
new comments. Report a table: thread -> fixed (sha).

Recount threads after EVERY push - "I see more comments unsolved" means this
loop exited early. Never claim done while any thread is unresolved.

## Phase 3 - Paced inline posting (for reviews the user wrote, e.g. pr-review output)

After the user approves the drafts:

- Everything goes through `$POST`. Follow pr-post-comments Steps 5-6: a JSON
  list of `{"path", "line", "body"}` entries (`start_line` for a span),
  `--commit $HEAD_SHA`, `--check` first, then the real run with
  `run_in_background: true`. It paces each post by its length on its own.
- Line numbers are NEW-file (right side) numbers.
- The driver prints each `html_url`; report posted/total at the end.

## Phase 4 - After the human merges

Only when the PR is actually merged (by the user):

```bash
git checkout main 2>/dev/null || git checkout master
git pull
git branch -d <branch>
```

Report: merged sha, branch deleted, working tree clean.
