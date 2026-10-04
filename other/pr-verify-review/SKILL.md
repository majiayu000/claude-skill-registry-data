---
name: pr-verify-review
description: >
  Re-check someone else's PR after you reviewed it: find every comment you left,
  verify each one is actually solved in the code (not just replied to or
  resolved), judge the author's pushback on its merits, scan everything that
  changed since your review for new regressions, then draft follow-up replies
  and new findings in the user's voice, post them paced on your go, and resolve
  your own threads that are genuinely fixed. Use when the user says "check if
  my comments were addressed", "verify the fixes on PR 123", "did they fix my
  review", "re-review round 2", "/pr-verify-review", or asks whether a
  teammate's PR is ready after their review. Works on any GitHub repo with gh
  auth. No babysitting, no pushing, no merging.
---

# Verify Review Fixes

The PR is someone else's. The user reviewed it. The author pushed changes and
probably replied "done". The job: prove each "done" is real, catch anything the
fixes broke, and tell the author what's still open - in the user's voice.

Pairs with `pr-review` (the original review and its checklist),
`pr-post-comments` (tags, voice rules, and the paced posting driver) and
`pr-address-review` (the same loop from the author's side). Uses a personal
voice skill for every body when one is installed.

```bash
POST=~/.claude/skills/pr-post-comments/scripts/post_pr_comments.py  # adjust if installed elsewhere
```

## Hard stops

- Read-only on their code. No commits, no pushes to their branch, no suggested
  changes applied. Local checkouts live in a scratch worktree, never the user's.
- NEVER merge. NEVER approve or request changes unless the user asks for it
  in this conversation - report a recommendation instead.
- NEVER post or resolve without one explicit go on the exact drafts (Step 6).
- Every comment and reply goes through `$POST` in the background. Nothing else
  creates comments: no direct `gh api` calls, no `gh pr comment`, no loop.
- A reply or a resolve click is not a fix. Only the code at head counts.
- No babysitting. One pass, report, done.

## Step 0 - Pin the PR, the account, and past rounds

```bash
gh pr view $PR --json number,url,author,headRefName,headRefOid,baseRefName,state,mergeable,commits
```

- Account: `ME` is `gh api user --jq .login`. If the repo needs a different
  account than the active one, switch (`gh auth switch`) or set `GH_TOKEN` first,
  then re-check the login.
- The PR author must NOT be `ME`. Own PR: use pr-address-review.
- Closed or merged: say so. Still verify if the user wants it, but nothing gets
  posted on a merged PR without asking.
- Past rounds: look in the project memory for a note on this PR
  (`project_pr<N>_*`). It has the round history, what was tagged `[r]`, and
  what the author pushed back on. Read it before reading the thread.

Check out the head in a scratch worktree for running tests:

```bash
git fetch origin pull/$PR/head:pr-$PR-verify
git worktree add $S/pr-$PR pr-$PR-verify
```

## Step 1 - Collect your comments and what happened to them

```bash
gh api graphql -F owner=$OWNER -F repo=$REPO -F pr=$PR -f query='
query($owner:String!,$repo:String!,$pr:Int!){repository(owner:$owner,name:$repo){pullRequest(number:$pr){
  reviewThreads(first:100){nodes{id isResolved isOutdated path line originalLine
    comments(first:50){nodes{databaseId createdAt body url author{login}
      originalCommit{oid} commit{oid}}}}}
  reviews(last:50){nodes{databaseId state body createdAt commit{oid} author{login}}}
  comments(last:100){nodes{databaseId body createdAt url author{login}}}
}}}' > $S/threads.json
```

Keep every thread `ME` started or commented in, plus `ME`'s review bodies and
PR-level comments that asked for something. For each, record:

- the tag (`[r]`/`[o]`/`[f]`/`[c]`) and the ask, in one line
- the commit it was made on (`originalCommit.oid`) - the reviewed SHA
- resolved / outdated state, and who resolved it
- every reply after `ME`'s last word, and any SHA the author cited

Skip threads `ME` already closed out in an earlier round unless the code under
them changed since.

Reviewed SHA gone (the author force-pushed): `git fetch origin <sha>` usually
still works, GitHub keeps review commits. If not, use `git range-diff` against
the old and new commit lists from the PR timeline, or fall back to the base
and say the delta is approximate.

## Step 2 - Verify each comment against head

For every item, read the code at head where the comment pointed - or where
that code moved to - plus its callers and tests. Then assign one verdict:

| Verdict | Meaning |
|---|---|
| SOLVED | the code at head does what was asked, and a test would catch a regression |
| SOLVED-UNTESTED | behaviour fixed, but nothing fails if it's reverted |
| PARTIAL | part of the ask landed, or the fix covers one path and misses a sibling |
| NOT SOLVED | the thread says done, the code says otherwise; or no change and no reply |
| ANSWERED | a `[c]` question with a reply that actually answers it |
| DEFERRED | author moved it to a follow-up - verify the issue exists and says the right thing |
| DISPUTED | author disagrees - see below |

How to prove it, not assume it:

- "Fixed in abc1234": confirm abc1234 is an ancestor of head and actually
  touches the thing. Cited SHAs that point at unrelated diffs happen.
- A fix is only as good as its test. For a bug fix, mentally revert the fix
  hunk: does the new test fail? If it wouldn't, it's SOLVED-UNTESTED. Run the
  test in the scratch worktree when it's cheap.
- Check siblings. A fix applied to one of three copies of the same pattern is
  PARTIAL, and it's the most common way a "done" is wrong.
- Outdated thread: GitHub marks it outdated when the line moved, not when it's
  fixed. Outdated says nothing about solved.
- Resolved by the author: still verify. Resolving isn't fixing.

DISPUTED gets judged honestly. Re-read the original comment as if a stranger
wrote it. If the author's argument holds (they found a constraint the review
missed, the risk is narrower than claimed), the verdict is CONCEDE and the
reply says so plainly. If it doesn't, the reply carries the evidence - file:line,
an input, a failing case - not a restatement of the original point.

## Step 3 - Regression scan on the delta

Everything that changed since the reviewed SHA is unreviewed code. Split it:

```bash
git log --no-merges --oneline <reviewed>..head      # the author's new work
git log --merges --oneline <reviewed>..head         # base merges
git diff <reviewed>..head -- . ':!<lockfiles>'       # full delta
```

- Author's new commits: review them the way the original review would have,
  with the same checklist (pr-review's T, S and D tables), applied to this
  delta only. At minimum: correctness,
  error paths, tests for new branches, no scope creep.
- Merge commits: `git show --remerge-diff <merge>` shows exactly how conflicts
  were resolved. A bad resolution is the classic hidden regression - base
  changes silently dropped, or the PR's own fix reverted.
- Fix side effects: a fix for comment A that changed a signature, a default,
  or a shared helper - trace every caller, not just the one the comment was about.
- Tests deleted, skipped, loosened (exact assertion turned into `in`, a
  `pytest.skip`, a widened tolerance) in the delta: always a finding.
- CI: `gh pr checks $PR`. Green is not proof - open the test job logs and look
  for 0 collected, skipped suites, `continue-on-error`. A red check is only
  the author's if it isn't also red on base.

Every regression is a new finding, tagged per pr-post-comments
(`[r]` blocks merge, `[o]`, `[f]`, `[c]`). Don't re-raise anything a bot
already flagged at the same spot, and don't invent findings to fill a round.

## Step 4 - Draft

Load the user's voice skill first if one is installed (for example
`Skill("voice-of-er")`). The voice rules in pr-post-comments apply either way.

Per verdict:

| Verdict | Action |
|---|---|
| SOLVED | resolve the thread, no reply - unless the author asked something |
| SOLVED-UNTESTED | reply asking for the test that would catch it; leave open |
| PARTIAL / NOT SOLVED | reply naming exactly what's missing (the sibling, the path, the line); leave open |
| ANSWERED / DEFERRED (issue ok) | resolve; reply only if something in the answer needs a word |
| DISPUTED - CONCEDE | short reply agreeing, then resolve |
| DISPUTED - HOLD | reply with the evidence; leave open |

Replies are `{"in_reply_to": <root databaseId>, "body": ...}`. New regression
findings are inline `{"path", "line", "body"}` on head, with a tag, line numbers
verified against `git show head:<path>` (pr-post-comments Step 4).

Voice rules on top of pr-post-comments Step 3:

- Point at the code, never the person. "the retry in _fetch still swallows
  the timeout" beats "you missed the timeout".
- A follow-up reply doesn't repeat the original comment. The author can scroll up.
- Short. A PARTIAL is usually two lines.
- No tag on thread replies, a tag on every new inline finding.
- No process narration, no em dashes, no So/Okay/Well/Yeah openers.

Write `$S/followup.json` (replies first, then new findings, in file order) and
lint it:

```bash
python3 "$POST" $OWNER/$REPO $PR $S/followup.json --commit <head> --check
```

## Step 5 - Recommendation

Give one line the user can act on:

- **Ready**: every `[r]` SOLVED or conceded, no new `[r]`, CI green for real.
- **One more round**: any `[r]` PARTIAL / NOT SOLVED / SOLVED-UNTESTED, or a new `[r]`.
- **Blocked on a decision**: a DISPUTED `[r]` where both sides have a case -
  the user decides, not this skill.

`[o]` items left open don't block. Say which ones the author skipped, that's all.

## Step 6 - The one approval gate

Show the user:

1. Table: original comment (tag + one line), verdict, evidence (SHA, file:line,
   test name), action (resolve / reply / leave).
2. New findings from Step 3, tagged.
3. Every body, bare text, not in a blockquote.
4. The recommendation.

Wait for an explicit go. Edits: apply, re-run `--check`, show only what changed.

## Step 7 - Post and resolve

Post in the background (`run_in_background: true`):

```bash
python3 "$POST" $OWNER/$REPO $PR $S/followup.json --commit <head>
```

Resolve the approved threads - only threads `ME` started:

```bash
gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -f id=$TID --jq '.data.resolveReviewThread.thread.isResolved'
```

## Step 8 - Report and clean up

- Posted count vs planned, with links from the driver log. Failed posts by number.
- Threads resolved, threads left open and why.
- The recommendation again.
- `git worktree remove $S/pr-$PR && git branch -D pr-$PR-verify`.
- Update (or create) the project memory note for this PR: round number, what's
  solved, what's still open, what was conceded. The next round starts there.

Then stop. No watching, no re-polling.
