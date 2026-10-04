---
name: pr-address-review
description: >
  Answer human review feedback on your own PR end to end: find the latest
  comments left by real people (bots filtered out), validate each claim against
  the code, fix the valid ones, resolve merge conflicts with the base, draft
  replies in the user's voice, then commit, push, post the replies paced, and
  watch CI until it is green. Use when the user says "address the review",
  "answer the reviewer's comments", "reply to the reviewers", "handle the new
  comments on my PR", "/pr-address-review", or asks to fix and respond to what
  a teammate said on their PR. Works on any GitHub repo with gh auth. Bot
  comments (Copilot, code-quality) are out of scope; reviewing someone else's
  PR belongs to pr-review, re-checking it afterwards to pr-verify-review.
---

# Address Human Review

The PR is the user's. A teammate commented. The job: work out which comments are
right, fix those, answer every one in the user's voice, ship it, keep CI green.

Pairs with `pr-post-comments` (voice rules and the paced posting driver) and
`pr-verify-review` (the same loop from the reviewer's side). Uses a personal
voice skill for every reply when one is installed, and hands off to a
`pr-babysit` skill for CI and bot comments when one is installed.

```bash
POST=~/.claude/skills/pr-post-comments/scripts/post_pr_comments.py  # adjust if installed elsewhere
```

## Hard stops

- NEVER merge. NEVER approve or request changes. Green + answered = report and stop.
- NEVER resolve a human's thread. The reviewer closes their own. Reply, leave open.
- NEVER post without one explicit go on the exact drafts (Step 6). That single go
  covers push and posting; nothing after it needs re-confirmation unless the
  drafts change.
- Every reply goes through `$POST` in the background. Nothing else creates
  comments: no direct `gh api` calls, no `gh pr comment`, no loop.
- No attribution, no AI or tool mention in commits, replies, or PR body.
- Commits carry only the fix. No CLAUDE.md, agent configs, planning files.

## Step 0 - Pin the PR and the account

```bash
gh pr view ${PR:-} --json number,url,headRefName,headRefOid,baseRefName,author,state
```

No number given: use the PR for the current branch. `OWNER/REPO` from the URL.

- Account: `ME` is `gh api user --jq .login`. If the repo needs a different
  account than the active one, switch (`gh auth switch`) or set `GH_TOKEN` first,
  then re-check the login.
- The PR author must be `ME`. If not, stop - this is someone else's PR, use
  pr-review (first pass) or pr-verify-review (after your review).
- The checkout must be the head branch, tree clean, up to date with the remote
  (`git status -sb`, `git fetch && git status`). In a multi-worktree repo, find the
  worktree that holds the branch (`git worktree list`) and work there. Never switch
  branches in the main worktree with uncommitted work in it.

## Step 0.5 - Merge conflicts

Check before touching review feedback. Fixes written on a branch that
conflicts with its base get rewritten twice.

```bash
gh pr view $PR --json mergeable,mergeStateStatus
```

`mergeable` can read `UNKNOWN` for a few seconds after a push while GitHub
computes it; re-query until it's `MERGEABLE` or `CONFLICTING`. Also check
locally, which catches a base that moved since GitHub last looked:

```bash
git fetch origin <base>
git merge --no-commit --no-ff origin/<base>; git merge --abort
```

Conflicting: merge the base into the branch. Don't rebase - a rebase needs a
force-push, which strands the reviewer's inline threads on dead commits and
rewrites history they already read.

```bash
git merge origin/<base>
```

Resolve each conflicted file by understanding both sides, not by picking one:

- Read what the base changed (`git log -p origin/<base> -- <file>` since the
  merge base) and why. The resolution has to keep the base's intent and the
  PR's intent. Taking `--ours` or `--theirs` wholesale is only right when one
  side's change is fully superseded, and that needs saying.
- Lockfiles and generated files (lockfiles, codegen output, schemas, snapshots):
  take the base's version, then regenerate with the repo's own command. Never
  hand-merge them.
- Migrations: two heads after the merge means the PR's migration gets
  re-parented onto the base's latest one. Check the chain is linear.
- Code that merged cleanly can still be wrong. A renamed function on base that
  the PR still calls by the old name is a conflict git won't show. Run types,
  lint, and the affected tests after every merge, not just for conflicted files.
- A conflict where the two intents genuinely clash (base removed what the PR
  builds on, both sides redesigned the same thing): stop and ask the user.

Commit with git's default merge message, no trailers. Record which files
conflicted and how each was resolved - it goes into the Step 6 summary. The
merge commit stays local until Step 7 like everything else.

## Step 1 - Collect what the humans said

Three places people leave feedback. Fetch all three once, into the scratchpad.

```bash
gh api graphql -F owner=$OWNER -F repo=$REPO -F pr=$PR -f query='
query($owner:String!,$repo:String!,$pr:Int!){repository(owner:$owner,name:$repo){pullRequest(number:$pr){
  reviewThreads(first:100){nodes{id isResolved isOutdated path line originalLine
    comments(last:30){nodes{databaseId createdAt body url author{__typename login}}}}}
  reviews(last:50){nodes{databaseId state body createdAt url author{__typename login}}}
  comments(last:100){nodes{databaseId body createdAt url author{__typename login}}}
}}}' > $S/feedback.json
```

A person is `author.__typename == "User"`, login not ending in `[bot]`, login not
`ME`. Everything else is a bot and is out of scope here.

What counts as open, per source:

- **Review thread**: unresolved, a human wrote in it, and the last comment is not
  `ME`'s. A thread where `ME` already answered and the reviewer hasn't come back
  is waiting on them - skip it.
- **Review body** (`COMMENTED` / `CHANGES_REQUESTED` with text): newer than
  `ME`'s last PR-level comment or push, whichever is later.
- **Conversation comment**: same cutoff as review bodies.

`--since <ISO>` from the user overrides the cutoff. Print the list as a table
(source, reviewer, path:line, first 100 chars) before doing anything else. Zero
open items: say so, go to Step 8, done.

## Step 2 - Validate every comment

Reviewers are often right and sometimes wrong. Neither is assumed. For each item:

1. Read the code it points at **at the current head**, plus callers and tests.
   Outdated threads: find where that code moved to, or confirm it's gone.
2. Reproduce the claim. A bug claim gets a failing test or a concrete input. A
   design claim gets traced through every caller. A "why" question gets the
   actual reason from code, git log, or the linked issue.
3. Assign one verdict:

| Verdict | Meaning | Action |
|---|---|---|
| FIX | claim holds | change the code, reply saying what changed |
| PARTIAL | right problem, wrong remedy or too broad | fix the real part, reply explaining the narrower fix |
| ANSWER | question, no change needed | reply with the answer |
| DISAGREE | claim is wrong | no change; reply with the evidence (file:line, test, input) |
| DONE | already fixed at head | reply pointing at the commit |
| DEFER | real, but outside this PR's scope | only if the user agrees; open an issue, reply with the link |

DISAGREE needs proof you could paste into the reply. "I think it's fine" is not a
verdict - that's FIX by default. When a human reviewer and a bot contradict each
other, the human wins; the bot thread stays open.

Two reviewers asking for opposite things: stop and ask the user which way to go.

## Step 3 - Fix

- Follow the repo's own rules first (AGENTS.md / CLAUDE.md: impact analysis,
  test commands, lint config).
- Behaviour change: failing test first, then the fix. A fix without a test that
  would have caught the original problem is half a fix.
- Keep each fix to what the comment asked. Opportunistic refactors start new
  review threads.
- Run lint, types, and the affected tests locally. Red stays red until fixed.
- Commit per concern, conventional message (`fix: ...`, `test: ...`), no
  trailers. Grouping every reviewer fix into one "address review" commit is fine
  when they're small. Record the short SHA per thread - replies cite it.

Commit locally now. Do not push yet.

## Step 4 - Draft the replies

Load the user's voice skill first if one is installed (for example
`Skill("voice-of-er")`). The voice rules in pr-post-comments Step 3 apply either way.

One reply per item. Review threads get `{"in_reply_to": <databaseId>, "body": ...}`
on the thread's first comment id. Review bodies and conversation comments get one
PR-level `{"body": ...}`; if several reviewers, one each, opening with their
`@login`.

What a good reply looks like:

- Lead with what happened. "moved the retry into the client, abc1234" beats
  "Great catch! I've addressed this by...".
- Cite the SHA for FIX/PARTIAL/DONE. Cite file:line or the test name for DISAGREE.
- DISAGREE stays warm and specific. The reviewer should be able to check the
  claim in ten seconds.
- No "thanks for the review" on every reply. Maybe once, if it's natural.
- Length follows the item. A rename gets one line.
- No tags here - `[r]/[o]/[f]/[c]` are for reviewing, not answering.
- No process narration ("checked the code", "I looked into it"), no em dashes,
  no So/Okay/Well/Yeah openers.

Write the JSON list to `$S/replies.json` (python or `jq -n --arg` so quoting
survives), then lint:

```bash
python3 "$POST" $OWNER/$REPO $PR $S/replies.json --check
```

Fix any flagged body, re-check until clean.

## Step 5 - Self-review the diff

Before showing anything, read `git diff origin/<head>..HEAD` as a hostile reviewer:
does each hunk trace back to a comment? Anything unrelated leaked in? Did a
DISAGREE item accidentally get a code change? Does a reply promise something the
diff doesn't do?

## Step 6 - The one approval gate

Show the user:

1. The item table: reviewer, location, verdict, commit SHA, one-line reason.
2. The diff summary (`git diff --stat` plus anything non-obvious), and if Step
   0.5 merged the base: each conflicted file and how it was resolved.
3. Every reply body, bare text, not in a blockquote.

Wait for an explicit go ("post", "ship it", "go"). Edits to a body: apply, re-run
`--check`, show just the changed ones. A DEFER item needs the user's yes before
anything is filed.

## Step 7 - Push, then post

Order matters: the fix has to be on the PR before the reply that says it is.

0. `git fetch origin <base>` once more. If the base moved since Step 0.5 and
   conflicts again, redo Step 0.5 and show the user the new resolutions before
   pushing.
1. Pre-push gate: the repo's lint, type check and affected tests, green. If a
   repo-specific gate skill or hook exists, it runs here instead.
2. `git push`. Never force-push unless the branch was already rewritten and the
   user said so.
3. Post in the background:

```bash
python3 "$POST" $OWNER/$REPO $PR $S/replies.json
```

with `run_in_background: true`. It paces each reply by its length and keeps
the clock across runs. Do not wait on it - move on to Step 8.

## Step 8 - Watch CI

With a `pr-babysit` skill installed, hand off to it on the new head (CI watch,
bot sweep, re-arm after each push). Without one:

```bash
gh pr checks $PR --watch --fail-fast
```

A red check: read the failing job's log, fix it if it's this PR's (it isn't if
the same check is red on base), commit, pre-push gate, push, watch again. Green
is not proof on its own - skim the test job for 0 collected or skipped suites.

What carries over from this skill while watching:

- A **new human comment** that lands while watching re-enters this skill at Step 1.
  Its drafts go through Step 6 again - the earlier go doesn't cover new text.
- The PR turns `CONFLICTING` (base moved meanwhile): run Step 0.5, then the
  pre-push gate, push, re-arm. A clean mechanical merge doesn't need a new go;
  a resolution that changed behaviour on either side does.
- A bot comment that contradicts a human reviewer's request is left open, not
  fixed, not resolved.

## Step 9 - Report

When the posting log shows every `html_url` and CI is green:

- Table: reviewer, location, verdict, SHA, reply link.
- CI state, head SHA, threads still open (human ones are expected to be open -
  they're the reviewer's to close).
- Anything posted partially or failed, by number.

Then stop. No merge.
