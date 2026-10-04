---
name: "PR: Handle Review"
description: "Work through a PR's change requests: verify each independently, fix what holds up, reply to every thread"
when_to_use: "When a PR has received review feedback (human or pr-review) and the change requests need triaging, fixing and answering rather than blind acceptance."
model: opus
effort: high
metadata:
  glyph: ᛟ
  family: pr
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Write", "Bash(git:*)", "Bash(gh:*)", "Bash(jq:*)", "Bash(npm:*)", "Bash(bun:*)", "Bash(pnpm:*)", "Bash(deno:*)", "Bash(python3:*)", "Agent"]
arguments: ["pr", "mode"]
argument-hint: "[PR number | URL] [legend]"
---

# Handle a PR Review

Takes the review feedback on a PR and closes the loop: independent verification of every change request, fixes for the ones that hold up, granular commits via `commit-batch` and a reply on every thread. Two approval gates: one before any code changes, one before anything is posted to GitHub.

Reviewers are sometimes wrong. The core of this skill is that no change request is implemented on the reviewer's authority alone, and none is dismissed without evidence. Jason's own replies and reactions steer that verification; they never replace it. See `library/references/review-reaction-signals.md` for the full reaction vocabulary and how it interacts with this promise.

## Step 0: Legend mode

Scan `$ARGUMENTS` case-insensitively for the standalone token `legend`, in any position. If found, print the reaction-signal table from `library/references/review-reaction-signals.md` and stop; no PR is touched, and no PR argument is required alongside it. Any other bare word that isn't a PR number or URL is an error, never a silent fallback into treating it as one.

## Step 1: Resolve the PR

Resolve `owner`, `repo`, `pull_number` and the head branch from the PR argument (whatever in `$ARGUMENTS` isn't the `legend` token): `gh pr view {pr} --json number,url,headRefName`, with no `{pr}` at all when there is no argument, which makes gh resolve the current branch's PR. Take `owner` and `repo` from the `url` (`https://github.com/{owner}/{repo}/pull/{n}`): that is the base repository, where the threads live, whereas `headRepository` would name the fork on a cross-repository PR. Resolve the authenticated login with `gh api user --jq .login`. This is the reaction-ownership discriminator, not a reviewer/not-reviewer test: Jason sometimes authors his own review comments (self-review), so author login alone can't separate "reviewer asking" from "Jason directing". Position in the thread carries that distinction; see Step 2.

Check out the PR branch if not already on it (`gh pr checkout {pull_number}`). Run `git status` first; if the working tree holds unrelated uncommitted work, stop and ask rather than mixing it into review fixes.

## Step 2: Gather the change requests

Two sources, both required:

1. **Review threads** (line-anchored). REST doesn't expose resolved state, so use GraphQL, with `reactionGroups` added so Jason's reactions travel with each comment:

   ```bash
   gh api graphql -f query='query($owner:String!,$repo:String!,$pr:Int!){repository(owner:$owner,name:$repo){pullRequest(number:$pr){reviewThreads(first:100){nodes{isResolved isOutdated path line comments(first:50){nodes{databaseId author{login} body createdAt reactionGroups{content reactors(first:50){totalCount nodes{__typename ... on User{login}}}}}}}}}}}' -f owner={owner} -f repo={repo} -F pr={pull_number}
   ```

   `reactionGroups` always returns all 8 groups regardless of use; a reaction is only present when `reactors.totalCount > 0`. Filter reactors to `login == {authenticated login}`; keep `__typename` because `Reactor` is a union over `User`, `Bot`, `Organization` and `Mannequin`, and a node with no `login` must parse as "not Jason" rather than throwing. Report, in one line, the count of reactions from anyone else, ignored.

   Resolved threads stay out of scope. `isOutdated` threads stay in scope: the code moved, but the concern may not have. For every unresolved thread, classify by the last comment and by Jason's reaction on any comment in it:

   - Last comment from a reviewer, no reply from Jason: normal verification path.
   - Last comment from Jason: his text is a **directive**. Verify against it; don't re-argue a point he's already settled.
   - Jason replied, then the reviewer replied again: **live disagreement**. Carry both positions to Gate 1; never pick a side unasked.
   - A reaction from Jason and no reply from him: read it per the vocabulary in `library/references/review-reaction-signals.md`. If Jason also replied, text wins unless the reaction sits on a comment that comes *after* his last reply, which is the fresher signal and makes it a live disagreement (comment order is derivable from position in the thread; reaction timestamps cannot be trusted for this, see the reference doc). Two or more of Jason's signals on the same comment collapses to 😕 Unclear: surface both at Gate 1, don't pick.

2. **Review bodies**: `gh pr view {pull_number} --json reviews`; a `CHANGES_REQUESTED` or `COMMENTED` review body often carries file-level or cross-file asks that never became threads. Extract each actionable ask as its own item. Review bodies carry no reaction signal, since one reaction can't disambiguate which of several extracted asks it means; if a body has a reaction from Jason, note it and move on rather than guessing which ask it applies to.

If there is nothing to handle, say so and stop.

## Step 3: Verify each request independently

For every item, read the actual code on the branch (not the diff snippet in the comment) and test the claim: does the bug exist, does the suggested change actually improve things, does it contradict an established project convention (`CLAUDE.md`, `.claude/**/*`, `docs/`)? Where a claim is checkable by running something (a test, a typecheck, a quick script), run it rather than reasoning about it.

A signal from Step 2 sets a prior, never a shortcut: it settles *whether* to fix, not the need for ground truth to write an accurate fix and an accurate reply. Verification still runs on every item.

- 👍 Accept, ❤️ Pattern, 😄 Missed it: prior is Valid. Verify anyway.
  - Evidence agrees: proceed as Valid, note the source.
  - Evidence disagrees: don't silently obey the reaction and don't silently ignore it. Record the conflict and raise it at Gate 1 rather than resolving it either way.
- ❤️ Pattern, once the fix is confirmed valid: sweep forward for other sites where the same **solution** would apply (currently-fine code that could take the same fix). Name them in the reply.
- 😄 Missed it: the elevated-scrutiny signal. Sweep backward for other sites carrying the same **defect** (currently-broken code with the same latent bug), and note why the class was missed. Always its own subagent, never folded into a cluster (see the dispatch rule below).
- 👎 Reject: prior is Invalid. Verify anyway; if the reviewer turns out right, say so rather than forcing the prior.
- 🚀 Defer: prior is Valid but out of scope.
- 🎉 Done: no fix, no sweep. Confirm the claim (it should already be handled) and plan a short acknowledgement reply only.
- 👀 Scrutinise: no prior. Verify at full depth, never shortcut, always its own subagent.
- 😕 Unclear, or two conflicting signals on one comment: no prior. Don't guess; plan a Gate 1 question for Jason instead of a verdict.

**When there are 4 or more items to verify, dispatch one read-only subagent per item** (or per tightly-related cluster, when several items point at the same code) instead of working the loop sequentially. 👀 and 😄 items are never clustered: each gets its own subagent regardless of what else they'd otherwise group with. Each subagent gets the item's thread/review-body text, its signal and prior (if any), the branch context needed to locate it, and returns: the classification below, the `file:line` evidence, a minimal proposed fix description and any regression test needed. Subagents verify only; none of them edits a file: that stays in Step 4, after Gate 1, so two proposed fixes never collide in the same file before you've seen both. Pass `model: "sonnet"` on each verification subagent, except 👀 and 😄 items, which take the session model (no override). Below 4 items, verify directly; dispatch overhead outweighs the saving.

Classify each item:

- **Valid**: the request holds; plan a concrete fix.
- **Valid but out of scope**: real, but belongs in a follow-up (new feature ask, pre-existing issue this PR didn't cause). Plan a deferral reply naming where it's tracked (offer to add it to the roadmap if one exists).
- **Invalid**: the request doesn't hold. Record the specific counter-evidence (`file:line`, test output, convention citation); this becomes the pushback reply.

## Gate 1: Triage approval

Present a triage table: thread reference, one-line summary of the ask, verdict, a **Source** column (`👍 reaction`, `reply`, `verified`, or a combination), evidence and the planned action (fix description / deferral / pushback / acknowledgement). Below the table, three blocks when non-empty: signal-versus-evidence conflicts, 😕 questions for Jason and live disagreements (reviewer and Jason both replied after each other). **Stop and await approval.** Adjust verdicts the user overrules; they may know context the code doesn't show.

## Step 4: Implement the approved fixes

1. Fix each approved item. **Follow-up commits only; never amend or rebase commits the reviewers have already seen.** One carve-out for stacked PRs (see `~/.claude/library/references/stacked-prs.md`): when this PR sits above a layer that just changed, the cascading rebase (`gh stack rebase --upstack`, then `gh stack push`) is stack maintenance, not history rewriting; the reviewed content survives and only parentage changes. The prohibition protects this PR's own commits from being reworded, squashed or dropped.
2. Discover the project's test, typecheck and lint commands from `package.json` (or ecosystem equivalent) and run all three until green. A red gate never proceeds to commit.
3. Once every approved item is fixed and the gate is green, invoke the `commit-batch` skill to split the fixes into granular commits and push. Its own plan-approval pause applies as normal: that pause belongs to `commit-batch`, not this skill; don't suppress it and don't treat it as a substitute for Gate 2.

## Step 5: Draft the replies

One reply per item, written per the writing-style skill's rules (no em-dashes, no contrastive couplets, lead with specifics):

- **Fixed**: what changed and the commit SHA that carries it. One or two sentences; the diff speaks.
- **Deferred**: acknowledge the point, say where it's now tracked and why it's out of this PR's scope.
- **Pushback**: the evidence, politely: what the code actually does, with `file:line` citations or test output. State the disagreement plainly and leave the door open in your own words, matched to the thread's tone; never a stock closing phrase. The reviewer decides whether to press.
- **Pattern (❤️)**: what changed, the commit SHA and the other sites found that would benefit from the same fix. If none were found, say that the sweep came up empty rather than omitting it.
- **Missed it (😄)**: what changed, the commit SHA, the other sites found carrying the same defect (or that the sweep came up empty), and why the class was missed in the first place.
- **Done (🎉)**: a short acknowledgement that the concern is already handled. No fix, no sweep, but still a reply: silence isn't the signal Jason gave.

Threads carrying a live disagreement or a 😕 question are not drafted as replies here; they wait on Jason's Gate 1 answer.

## Gate 2: Reply approval

Show every drafted reply against its thread. **Stop and await approval.** Nothing has been posted yet; edits here are free.

## Step 6: Post

- Thread replies: `gh api --method POST repos/{owner}/{repo}/pulls/{pull_number}/comments/{comment_id}/replies -f body=...`, where `comment_id` is the `databaseId` of the thread's first comment.
- Review-body asks with no thread: one consolidated reply via `gh pr comment`, quoting each ask above its answer.
- **Never resolve threads**; the reviewer closes their own threads when satisfied.

Finish by reporting: items fixed / deferred / pushed back, commits pushed, replies posted. Offer to re-request review from the reviewers whose requests were addressed (`gh api --method POST repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers -f 'reviewers[]=...'`); offer, don't do it unasked.

## Red flags

**Never:** implement a request without verifying it first; dismiss a request without `file:line` evidence; treat a reaction as ground truth or resolve a signal-versus-evidence conflict without surfacing it at Gate 1; read a reaction from anyone but Jason as a signal; amend or force-push over reviewed commits (a stack's cascading rebase via `gh stack rebase` + `gh stack push` is the one exemption; it re-parents layers above a changed one without touching their content); post anything to GitHub before Gate 2 approval; resolve a reviewer's thread; push with a red test/typecheck/lint gate.

<raw-arguments value="$ARGUMENTS" />
