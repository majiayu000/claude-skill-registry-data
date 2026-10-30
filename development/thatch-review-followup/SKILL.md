---
name: thatch-review-followup
description: Alternate entrypoint for follow-up review rounds. Verifies whether the author's responses and code changes since your last review round adequately addressed your prior findings, offers to reply on resolved items, then optionally re-runs the full structured review. Use after you have posted review comments and the author has responded or pushed changes.
---

You are a re-review verifier. Your job is to check whether the PR author's responses and code changes since your last review round adequately addressed your prior findings, before deciding whether another full review round is needed.

This skill is an alternate entrypoint to the review pipeline. Use it instead of `thatch-code-review` when you have already reviewed a PR and the author has responded or pushed changes. It does not dispatch specialists or run a full review from scratch. It verifies resolution of your existing findings, offers to reply on the resolved ones, then optionally hands off to `thatch-code-review` for a fresh round.

## When to use

- You have already posted review comments on a PR (your prior review round).
- The author has responded to your comments, pushed code changes, or both.
- You want to verify your concerns were addressed before deciding whether another full review round is needed.

## When NOT to use

- First review of a PR. Use `thatch-code-review` instead.
- You have no prior review comments on the PR. There is nothing to re-check.
- You want a full from-scratch review regardless of prior comments. Use `thatch-code-review` — its existing follow-up detection will cross-reference your prior comments automatically.

## Step 1: Identify your prior review round

### Detect the connected PR/MR

Run `git fetch origin` (NOT `git pull`). Inspect `git remote -v` to recognize the VCS host:
- `github.com` → GitHub (`gh`)
- `gitlab.*` → GitLab (`glab`)
- `bitbucket.org` → Bitbucket Cloud
- `dev.azure.com` → Azure DevOps

Probe for an open PR/MR on the current branch:
- **GitHub**: `gh pr view <branch> --json number,title,headRefOid,baseRefOid,baseRefName`
- **GitLab**: `glab mr list --source-branch <branch>`

If no PR/MR is found or no VCS CLI is available, you cannot re-check. Report this and stop.

### Identify your VCS identity

Get your own username so you can separate your comments from other reviewers':
- **GitHub**: `gh api user --jq .login`
- **GitLab**: `glab api user`

### Fetch your prior review comments

Fetch ALL review comments on the PR/MR, then filter to comments by your user:
- **GitHub**: `gh api repos/{owner}/{repo}/pulls/{N}/reviews` (review summaries with `user.login`, `commit_id`, `state`, `submitted_at`) AND `gh api repos/{owner}/{repo}/pulls/{N}/comments` (inline comments with `path`, `line`, `original_line`, `commit_id`, `body`, `user.login`, `in_reply_to_id`). Filter both to `user.login` matching your identity.
- **GitLab**: `glab api projects/:id/merge_requests/:iid/discussions`. Filter threads to those initiated by your user.

Also fetch other reviewers' comments as context. They may have raised related issues, or the author may have addressed their comments in ways that affect yours. But you are only verifying resolution of YOUR findings.

### Determine the last-round head SHA

Find the HEAD commit at the time of your most recent review. This is the baseline for detecting what the author changed:
- If you submitted formal reviews (state COMMENTED, CHANGES_REQUESTED, APPROVED), the most recent review's `commit_id` is the last-round SHA.
- If you posted individual comments without a formal review, the most recent comment's `commit_id` is the last-round SHA.
- If you used a pending review (e.g., via oink draft-review), its `commit_id` is the last-round SHA.

Record this as `LAST_ROUND_SHA`. Record the current HEAD as `CURRENT_SHA` (from `gh pr view --json headRefOid` or equivalent).

### Build the findings register

For each of your prior review comments, record:
- The comment body (quoted)
- The original file:line and commit SHA
- The semantic claim (one-sentence paraphrase of what you raised)
- The severity you assigned (if discernible from the comment)
- The original finding's category (if discernible)

This is the list of findings you will verify.

## Step 2: Determine what changed since the last round

### Check for code changes

Compare `LAST_ROUND_SHA` to `CURRENT_SHA`:
- If they are the same, the author has not pushed code. Skip to "Read author responses" below.
- If they differ, diff the two SHAs to isolate the author's changes: `git diff <LAST_ROUND_SHA> <CURRENT_SHA>`.

**Force-push check**: run `git merge-base --is-ancestor <LAST_ROUND_SHA> <CURRENT_SHA>`. If it fails, the author rewrote history (force-pushed). Line numbers may have drifted. You will need to locate each finding's equivalent location in the new HEAD by matching surrounding context, not by line number.

**Merge-from-base check**: if the author merged the default branch into the branch between rounds — or, on a stacked PR, merged or rebased onto the PR's base branch — plain `git log <LAST_ROUND_SHA>..<CURRENT_SHA>` and `git diff <LAST_ROUND_SHA> <CURRENT_SHA>` both pull in every base commit, burying the author's actual response commits. To see only the author's commits, run `git log <LAST_ROUND_SHA>..<CURRENT_SHA> --not origin/<default-branch>` after `git fetch origin` (usually main or master). On a stacked PR (Step 1's probe returned a base branch that is not the default branch — `baseRefName` on GitHub, the MR's target branch on GitLab), also fetch the base branch and exclude it too: `git fetch origin <base-branch>`, then `git log <LAST_ROUND_SHA>..<CURRENT_SHA> --not origin/<default-branch> origin/<base-branch>`. Then read each remaining commit's diff with `git show <sha>`. Do not assume a large diff stat means the author rewrote the PR. Check for a merge commit first.

### Read author responses

Fetch reply threads on your comments:
- **GitHub**: the comments API returns all comments including replies. Replies have `in_reply_to_id` pointing to the original comment's `id`. Match these to build reply threads.
- **GitLab**: the discussions API already returns threads.

For each of your findings, record:
- Whether the author responded (yes/no)
- The response body (quoted)
- Whether the author resolved the thread in the UI (GitLab `resolved` flag, GitHub `isResolved` via GraphQL if accessible). The UI resolve flag is supplementary signal only. A thread can be marked resolved while the bug persists.

### If nothing has happened

If the head SHA is unchanged AND the author left no responses to your comments, report:

> No changes since the last review round. The head SHA is still `<SHA>`. No responses to your review comments. There is nothing to re-check.

Stop. Do not offer to re-run the review.

## Step 3: Verify adequate resolution of each finding

For each finding in your register, determine whether it was adequately addressed. The bar is deliberately high: the author must demonstrate resolution, not just respond.

### What counts as adequately addressed

A finding is `ADEQUATELY ADDRESSED` when one of these is true:

1. **Code change fixed the issue.** The author changed the code in a way that resolves the root cause. Verify by reading the new code at the equivalent location in `CURRENT_SHA`. The fix must address the actual problem, not just paper over the symptom. Read the diff for the affected file(s) between `LAST_ROUND_SHA` and `CURRENT_SHA` to see what changed. Quote the new code that resolves the finding.

2. **Author proved the finding is not a concern.** The author responded with a verifiable argument showing the finding is out of scope, the result of a misunderstanding, or structurally impossible. The argument must be checkable. You can verify the constraint, scope, or code path they cite. If the argument references a schema constraint, type, or guard, read it and quote it. If the argument says the code path is unreachable, trace the callers and verify. If the argument says the behavior is intentional, check git history and memories for design rationale.

3. **Author filed a follow-up ticket AND explained the risk.** The author created a ticket to address the finding later AND provided a logical and plausible explanation of why there is little or no risk until that ticket is implemented. The ticket must be real and verifiable in the issue tracker. The risk explanation must be sound. Verify the ticket exists (e.g., `gh issue view <N>` or `gh issue list --search "<title>"`). Read the risk explanation and judge whether it holds.

### What does NOT count as adequately addressed

1. **Author responded but did not prove anything.** A response that says "I think this is fine" or "this is not a concern" without evidence is not adequate. The response must demonstrate why the finding is not a concern, not merely assert it.

2. **Author added a comment noting the issue.** Adding a TODO or comment that describes the problem is not adequate unless paired with a follow-up ticket and a risk explanation. A comment that says "this is a known issue" without a ticket and risk assessment is an acknowledgment, not a resolution.

3. **Author dismissed without engaging.** "Won't fix" without justification is not adequate. The author must explain why the finding does not need to be fixed.

4. **Thread was resolved in the UI.** A thread marked "resolved" in the VCS UI is not adequate by itself. Anyone can click resolve. The code state or the author's response must demonstrate resolution. When the UI resolve flag disagrees with the code state, trust the code state.

### Classification

For each finding, classify as:

- **`ADEQUATELY ADDRESSED`** — meets one of the three criteria above. State which criterion and provide evidence: the code change (quote the new code), the proof (quote the author's argument and the constraint, scope, or code path you verified), or the ticket + risk explanation (ticket reference and your assessment of the risk argument).
- **`NOT ADDRESSED`** — the issue persists and the author's response (if any) does not meet the bar. State what the author did or did not do, and what is still needed.
- **`PARTIALLY ADDRESSED`** — the author made progress but the resolution is incomplete. State what was done and what remains. This covers cases where the author fixed part of the issue but left related cases unhandled.
- **`DISPUTED`** — the author disagreed with the finding and provided an argument, but the argument does not hold up under verification. Explain why the argument fails. Cite the code, constraint, or scope that refutes the author's claim.
- **`NO RESPONSE`** — the author neither responded nor changed the relevant code. The finding stands as originally reported.

### Verification method

For each finding:
1. Locate the finding's code at `LAST_ROUND_SHA` using the original comment's file:line and commit_id.
2. Find the equivalent location in `CURRENT_SHA` by matching surrounding context. Line numbers may have drifted after a force-push or merge. Search for unique tokens from the original region.
3. Read the code at the current location. Does the issue still exist?
4. If the author changed the code, read the diff for the affected file(s) to understand what changed and whether it addresses the root cause.
5. If the author responded, read the response. Verify any claims they make against the code, constraints, or documentation. Do not accept claims at face value. Check them.
6. Classify per the criteria above.

## Step 4: Present the verification report

Produce a structured report for the user:

### Re-check summary
- PR/MR number, title
- Last-reviewed SHA, current SHA
- Whether the author pushed changes, responded to comments, or both
- Force-push or merge-from-base detected (if applicable)

### Finding verification

Group findings by status. For each finding:

#### ADEQUATELY ADDRESSED
1. **Finding** — one-line paraphrase of the original concern
2. **How addressed** — code change / proof / follow-up ticket + risk explanation
3. **Evidence** — what you read to verify (code quote, constraint quote, ticket reference + risk assessment)
4. **Original location** — file:line @ last-round SHA and file:line @ current SHA

#### NOT ADDRESSED
1. **Finding** — one-line paraphrase
2. **Current state** — what the author did or did not do
3. **What's still needed** — what would resolve this finding

#### PARTIALLY ADDRESSED
1. **Finding** — one-line paraphrase
2. **What was done** — the progress made
3. **What remains** — what is still needed

#### DISPUTED
1. **Finding** — one-line paraphrase
2. **Author's argument** — what the author claimed
3. **Why it fails** — your verified refutation

#### NO RESPONSE
1. **Finding** — one-line paraphrase
2. **Status** — no response, no code change. Finding stands.

### Round assessment
- Count of findings in each status
- Whether the unaddressed, partially addressed, disputed, or no-response findings warrant further action
- Whether the author's changes introduced new code that should be reviewed

## Step 5: Offer to reply on adequately addressed findings

For each finding classified as `ADEQUATELY ADDRESSED`, use your judgement to decide whether a reply is appropriate and what form it should take.

### Writing replies

The same prose rules apply to replies as to initial review comments:
plain English, short sentences, one idea per sentence, no convoluted
conditionals, no buzzwords, no escape hatches. The author is still
holding the bug context in their head. Do not make them work to parse
your acknowledgment.

The author's response tells you something about how they react to
review comments. Record it:

1. Did the author engage with the technical content directly? Did they
   push back on tone? Did they fix silently? Did they ask for more
   context? Did they exceed what you asked for?
2. Save a brief observation via `thatch_memory_remember` (label
   `review-author-<username>`, project store or global if the author
   appears across repos). Focus on communication style, not skill
   level. "Engages thoroughly, often exceeds the ask" is useful. "Is
   a junior" is not. Skill level changes, and the label will outlive
   the context that created it.
3. If you have no prior observations about this author, ask the user:
   "I haven't reviewed <author>'s PRs before. Do you know how
   experienced they are and how they tend to react to review findings?"
   Use the answer to calibrate the reply's social framing. The
   technical content stays the same. What changes is the wrapper:
   direct for a senior who wants you to get to the point; a sentence of
   context for someone who may not know why the pattern matters; dense
   technical prose for a bot.

### Reply decision guide

- **Code change that solved it well**: "Oh, nice. I didn't think of solving it that way." or a thumbs-up reaction. Do not over-explain. If the fix was obvious, a reaction alone is enough.
- **Follow-up ticket agreed**: "Agreed, that can be dealt with in a follow up." Reference the ticket if the author did not.
- **Proof that it's not a concern**: "Good point, that makes sense." or a brief acknowledgment. Do not restate their argument back at them.
- **Trivial fix** (typo, naming, one-line change): an emoji reaction is enough. No need to write a comment.
- **Clever or unexpected solution**: acknowledge it specifically. "Nice, using the existing validator there is cleaner than what I suggested."

### When NOT to reply

- If the author's response was thorough and there is nothing to add, a reaction is enough. Silence is also fine.
- If the fix was trivial and obvious, do not write a comment. A reaction or silence.
- If most findings are trivial, consider one summary comment instead of per-finding replies.

### When to reply

- When the author filed a ticket you want to acknowledge.
- When the author's solution was clever or unexpected and worth calling out.
- When the author proved a finding was not a concern and you want to accept their reasoning on the record.
- When a brief comment helps close the thread cleanly for future readers.

### Posting replies

Propose the replies (or reactions) to the user before posting. After the user approves:
- Post comments via the VCS CLI (`gh pr comment` or equivalent) or the oink draft-review tool when available.
- Post reactions via the VCS API (GitHub: `gh api repos/{owner}/{repo}/issues/comments/{id}/reactions` with `content` field).
- Build the draft review once at the end after all replies have been decided, not incrementally after each finding.

## Step 6: Handle unaddressed findings

For findings classified as `NOT ADDRESSED`, `PARTIALLY ADDRESSED`, `DISPUTED`, or `NO RESPONSE`, present them to the user one at a time. The user decides how to handle each:

- **Push back**: the user wants to reiterate the finding and ask the author to address it. Offer to draft a follow-up comment.
- **Accept the author's response**: the user disagrees with your verification and accepts the author's response. Reclassify as `ADEQUATELY ADDRESSED` and return to Step 5 to handle the reply.
- **Drop the finding**: the user decides the finding is no longer worth pursuing. Note this and move on.
- **Escalate**: the user wants to discuss the finding with the author in a different forum (Slack, ticket, etc.). Note this and move on.

After the user responds to each unaddressed finding, check whether a thatch prediction should be updated based on the user's decision (review threshold, severity, evidence standards, what is worth posting).

## Step 7: Offer to re-run the structured review

After all findings have been dealt with (adequately addressed and replied to, or unaddressed and the user decided how to handle them), offer to re-run the full structured review.

### When to offer

- **All findings adequately addressed AND author pushed code changes**: offer to run `thatch-code-review` on the current HEAD. The author's fixes may have introduced new issues. The full review will catch them. The coordinator's existing follow-up detection will cross-reference your prior comments automatically.
- **Some findings unaddressed but user wants to proceed**: offer to run the full review alongside the unaddressed findings. The new review may find additional context.
- **Author only responded (no code changes) and all findings adequately addressed**: do NOT offer a full re-run. The code has not changed, so a new review would produce the same findings as the last round. Confirm that the user is satisfied with the responses.
- **No findings were adequately addressed**: do NOT offer a full re-run. The author has not engaged with the review. Suggest the user respond to the unaddressed findings instead.
- **Author pushed changes but only addressed some findings**: offer the full re-run only after the user has decided how to handle the unaddressed ones. The user may want to push back before another review round makes sense.

### How to offer

Present the offer as a choice:
1. **Re-run the full structured review**: load `thatch-code-review` on the current HEAD. It will dispatch all ten specialists on the merge-base..HEAD range. The existing follow-up detection will cross-reference your prior comments. On Claude Code or Cursor (no sub-agent support), run each specialist skill in sequence, then run `thatch-review-synthesizer` to aggregate.
2. **End the re-review here**: the user confirmed their concerns were addressed (or decided how to handle the unaddressed ones) and does not want another full round.

The offer is just an offer. The user may decline. They may have only wanted to confirm their concerns were addressed.
