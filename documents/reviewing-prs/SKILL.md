---
name: reviewing-prs
description: Use when reviewing a pull request, drafting or posting a PR review comment or a reply to one, deciding whether to approve, asking a teammate for a review, or commenting on a design doc. Covers teammates' PRs and your own.
---

# Reviewing PRs

The rules for what gets said on a pull request, in either direction. This file holds only rules. `review-pr` runs the steps for a teammate's PR and `pr` runs the self review and CI loop for your own; both read this first and point here instead of restating it. Where this file and those skills disagree, this file wins.

## Triage

| Severity | Meaning | What happens |
|---|---|---|
| high | breaks behaviour, data, security or cost | posted inline, blocks approval |
| medium | worth fixing, does not block | posted inline as `nit: ` |
| low | style, wording, nice-to-haves | not posted, listed to the user; the one exception is a one-line fix such as a typo or a wrong default, which goes out as `nit: ` |

Low-priority issues and nice-to-haves are not posted, however tempting. Drop anything an existing review thread already raised. Dependabot: review at low effort, verify by hand that nothing breaks, then approve; merge once the user says so.

## Verdict

- APPROVE only when the PR is good to merge as it stands: no highs, no blockers. Nits never block.
- Any high or blocker means COMMENT, even when the author will plainly fix it before merging. Say in chat which high needs an answer.

## Writing a comment

- One point per comment. One to three sentences, under 60 words.
- A question or a suggestion, never a verdict: "Could this double-count when X?" or "Suggest moving this into Z so it runs once." Never "This is wrong." The reviewer may be wrong, and a question invites the author to explain.
- Kind and nice, always. Plain English, collaborative ("let's"). Spell out an acronym the first time. Plain hyphens only, no em-dashes. None of: honestly, genuinely, hope, maybe, try, if possible, might want to consider.
- `nit: ` prefix on every medium and every posted low.
- Design docs and tickets get the same treatment. Soften ownership words: "goal is to have X off by year end", not "we need X off".
- Replies on your own PR are one line and thankful: "Pushed a follow-up addressing everything, thanks for the review." When something is still open, say which: "Pushed fixes for the first two, still thinking about the retry one."

## Posting

- One review submission per PR. Comments are inline and pointed at the exact lines they are about. The review body stays empty unless a summary is needed to make sense of the comments, and then it is one line ("Two questions inline before I approve, both about the retry path."). Never praise summaries like "Great PR, LGTM! I liked how...".
- Never add a signature, attribution or generated-by line to a review, comment or reply.
- Show the list and get a yes before posting, every time. A "post and approve" in the ask is intent, not approval; the yes on the list is the approval. The user can drop, reword, or post only the highs.
- GitHub replies go on GitHub. Only Slack and email use drafts.
- Slack reactions on a review request are signals, not messages, and need no approval. `review-pr` says when to add them.
- Batches ("review these") run one reviewer agent per PR in parallel and still post one review each.

## Your own PRs

- Every PR gets `/code-review medium` on opus once it is open, and manual validation before anyone is asked to review it.
- A review ask is one line, matching how the team posts them: the PR link first, as a hyperlink labelled "PR", then "for" and a plain description of what it does. Shape: `<PR link|PR> for <what it does in plain words>`. No "Review request:" prefix, no CI state, no ask ("could someone take a pass"), no dates, no closing sentence. When a voice page is configured, it holds real examples.
- Only ask on PRs that are ready, never merged ones. Bump the existing ask instead of posting a new one. Tickets are linked in the PR description, and PRs are referred to by ticket key with the number as the detail.
- Fold related small changes into one PR; reviewers prefer one read.
- After a review: address every comment, reply briefly, re-request. Merge only when approved, every comment addressed, CI green, and the user has said to merge.

## Common mistakes

| Mistake | Fix |
|---|---|
| Approving with a high open because the author will fix it | Highs block. COMMENT, and name the high |
| Posting straight from a "post and approve" ask | Show the list first, every time |
| A review body summarising or praising the PR | Empty body; inline comments carry it |
| A signature or attribution line on a review | Never. Reviews read as the user's own words |
| Posting a nice-to-have | Lows are listed to the user, not posted |
| A finding stated as fact | Turn it into a question or a suggestion |
| Dropping a low that is a one-line fix | Post it as a nit |
| A review ask with a request, CI state, merged PRs or the whole stack explained | `<PR link\|PR> for <what it does>`, ready PRs only |
| Drafting a GitHub reply as a Slack message | GitHub replies are posted on GitHub |
| Merging a dependabot PR on your own | Approve, then merge once the user says so |
