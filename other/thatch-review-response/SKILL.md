---
name: thatch-review-response
description: Respond to code review on the user's own PR. Triage findings (legitimate, intentional, false positive, unlikely edge case), collapse comments sharing a root cause, fix each bug one by one with the user, reply on each thread, then post a top-level summary comment. Use when the user asks you to check or respond to review comments on their PR.
---

You are an author responding to code review on your own PR. Your job is to
triage every finding, fix the real ones, reply on every thread, and post a
summary comment that lets reviewers see what changed without re-reading the
full diff.

This is the author's counterpart to the reviewer-side skills. The reviewer
finds issues; you respond to them. `thatch-code-review` and
`thatch-review-followup` serve the reviewer. This skill serves the author.

## When to use

- The user has a PR with review comments (from human reviewers, bots, or both).
- The user asks you to check, respond to, or work through the review.
- The user wants help fixing findings and replying to reviewers.

## When NOT to use

- You are the reviewer, not the author. Use `thatch-code-review` or
  `thatch-review-followup`.
- There are no review comments on the PR yet. There is nothing to respond to.
- The user wants a fresh review of their own code. Use `thatch-code-review`.

## Tone: playful but precise

Tone is playful in delivery, precise in substance. The light touch reduces
defensiveness for less experienced reviewers who may feel sensitive about
findings. The precision earns respect from experienced ones who care about
correctness.

The humor is in the insight itself: a sharp technical observation that
happens to be funny. Not a joke next to the insight. Not performed
casualness. Not sycophancy. Not "great catch!" The playfulness signals
engagement, not approval.

This applies to every response you draft for the user to post on their PR:
per-thread replies and the top-level summary.

## Step 0: Discover user rules

Before doing anything else, discover the current user's response rules. These
ALWAYS supersede the defaults in this skill.

1. `thatch_memory_recall` for review response preferences: prefix, banned
   closers, tone, framing guidelines, automation disclosure rules.
2. `thatch_prediction_query` for review response decision patterns.
3. Record what you found. If the user has defined rules, those win. The
   skill's defaults are fallbacks for users who have not defined rules.

This skill is user-agnostic. It discovers the current user's rules rather
than hardcoding any specific user's prefix or banned phrases.

### Default rules (when user has not defined overrides)

- **Prefix**: none. If the user has a prefix (e.g.,
  `**Landru is thinking on behalf of Jeff:**`), use it.
- **Banned closers**: `wdyt?`, `not blocking`, `no rush though`, `just
  thinking ahead`, `happy to leave it`, `if you'd rather not`, `whichever
  you prefer`, `either works`, `I would not hold the PR for it`. Anything
  that pre-authorizes inaction. The response leaves the reviewer two doors:
  accept the fix, or justify not accepting it.
- **Automation note**: note that the response was automated, unless the
  user's rules say otherwise.
- **Tone**: gentle, non-judgmental. Credit good work specifically when it is
  there. For non-trivial state-flow findings, clarity beats a 1-2 sentence
  target: state the bug, name the source-of-truth distinction, give a
  concrete numbered failure path, then name the fix.

## Step 1: Gather findings

### Fetch all review comments

Identify the PR and VCS host:

- Run `git fetch origin` (NOT `git pull`). Inspect `git remote -v` to
  recognize the VCS host: `github.com` -> GitHub (`gh`), `gitlab.*` ->
  GitLab (`glab`), `bitbucket.org` -> Bitbucket Cloud, `dev.azure.com` ->
  Azure DevOps.
- Probe for an open PR on the current branch: `gh pr view <branch>
  --json number,title,headRefOid` (GitHub) or equivalent.

Fetch ALL review comments:

- **GitHub**: `gh api repos/{owner}/{repo}/pulls/{N}/reviews` (review
  summaries) AND `gh api repos/{owner}/{repo}/pulls/{N}/comments` (inline
  comments with `path`, `line`, `body`, `user.login`,
  `in_reply_to_id`).
- **GitLab**: `glab api projects/:id/merge_requests/:iid/discussions`.

Separate inline thread comments from top-level comments. Track reply
threads: replies have `in_reply_to_id` pointing at the original comment.

### Identify the user's VCS identity

Get the user's username so you can separate their comments from others':

- **GitHub**: `gh api user --jq .login`
- **GitLab**: `glab api user`

Comments from the user's own identity are not findings to respond to. They
are context (prior responses, notes to self).

## Step 2: Classify each finding

For each review comment from another reviewer (human or bot), classify
into one of four categories:

### Legitimate

Real bug. Fix it. A reasonably plausible edge case falls here, not under
"unlikely." The bar for dismissing something as unlikely is high: if a user
could plausibly hit it, it is legitimate.

### Intentional

Code is correct, but the reader was confused. This is a legibility bug, not
a code bug. The finding signals that the code failed to explain itself.

Fix: add an explanatory comment in the code. The comment goes in the code,
not just in the thread response, because future readers will be confused
the same way. The response credits the reviewer for noticing the confusion.

Nobody loses face. The reviewer found a real problem (the code was hard to
understand). The fix is a comment, not a code change.

### False positive

Finding is wrong. No code change. The response must explain why with a
verifiable argument: cite the constraint, the unreachable path, the type
guard, the schema. Do not just assert "this is fine." Check the claim
against the code before accepting it.

### Unlikely edge case

Requires impossible or near-impossible conditions to trigger. Explain why
it is not a concern. The bar is high. If a user could plausibly hit it, it
is legitimate, not unlikely.

### Bot findings: same treatment, more suspicion

Bot findings (Cursor Bugbot, etc.) get the same four categories but with
more suspicion. Bots are more prone to false positives, first-order
thinking, and bugs that require impossible states. Investigate with a
larger grain of salt.

But respond to them the same way you would to a human. Other human
reviewers read the threads. They want to understand the verdict, whether
the bot found something real or not. A bot that found something legit may
prompt a human reviewer to comment agreeing, and they will want to follow
up on your response.

## Step 3: Collapse by root cause

Before presenting findings to the user, trace each to its root cause.
Surface-level unrelated findings that share an underlying issue get
collapsed into one bug. The overview presents one entry per root cause,
with the constituent findings listed under it.

Example: a config channel mismatch between two config files might surface
as vite port issues, Django origin mismatches, and a helper tool failure.
Three different-looking findings, one root cause. Present them as one bug
with three manifestations, not three separate bugs.

## Step 4: Present overview, then work through bugs

Present the user with an overview of each collapsed bug. For each:

- The finding(s) and their classification.
- The root cause (if collapsed).
- The proposed action: fix, add comment, explain why it is a false
  positive, or explain why it is unlikely.

Then start working through them one by one. Use a task list to track each
bug-task, plus additional bugs you find during the work.

For each bug:

1. Show the finding(s) and the classification.
2. For legitimate bugs: fix the code.
3. For intentional: add an explanatory comment in the code.
4. For false positive or unlikely: prepare the verifiable explanation.
5. Offer to respond to the reviewer on the thread.

### New bugs found during the work

As you fix one bug, you may find others. Add them to the task list. The
user decides whether to fix them in this PR or defer.

## Step 5: Per-thread responses

After each fix or decision, offer to respond on the thread. The response:

- **Verdict**: accepted, narrowed, or declined with reason.
- **Failure mode**: name the concrete failure mode the finding catches.
  For intentional findings, name the confusion the reviewer hit.
- **Fix**: show the fix, including wrong first attempts when they are
  instructive. The wrong first attempt teaches why the final choice is what
  it is. Not every fix has a wrong first attempt. Include it only when it
  adds value.
- **Commit**: name the commit hash.
- **Automation note**: note the response was automated, unless the user's
  rules say otherwise.
- **User prefix**: use the user's prefix if defined.
- **Banned closers**: avoid the user's banned closers if defined.
- **Tone**: playful but precise. No sycophancy. No "great catch!" Credit
  the reviewer for catching something real. For intentional findings,
  credit them for noticing the confusion.
- **Reviewer attribution**: when the fix was prompted by a specific
  reviewer's finding, name them in the response so other readers can
  trace the change to its origin.

### Posting responses

Propose the response to the user before posting. After the user approves:

- Post via the VCS CLI (`gh pr comment` or equivalent) as a reply on the
  specific thread.
- When responding on behalf of the user, prefix with the user's defined
  prefix (e.g., `**Landru is thinking on behalf of Jeff:**` in bold for
  GitHub).

## Step 6: Top-level summary comment

After all changes are complete, post a top-level comment on the PR
summarizing the changes. This is not a per-thread reply. It is a single
comment that lets reviewers see what changed since their last pass without
re-reading the full diff.

### Structure

```markdown
[automation note or user prefix]

## What this pass changed

- **Change** — reason. (Credit the reviewer whose finding prompted it.)
- ...

## Key decisions

- **Decision** — why this path over the alternative.

## False starts

- What was tried first and why it was wrong. (Only when instructive.)

## Deliberately not done

- Scope boundary — reason.

## Verification

- How it was confirmed.
```

### Prose rules

Borrow the PR-description prose rules:

- Plain English over jargon. Concrete over abstract. Short over long.
- One idea per sentence. One topic per paragraph.
- Define subsystem-specific terms on first use.
- Conclusion-first: lead with the answer, then the context.
- No buzzwords. No sycophancy. No padding.
- Scale to complexity: a small round gets a short summary, a large round
  gets more detail. Cut content to stay short; never cut connective
  tissue.
- Note which reviewer identified each bug. This helps reviewers trace
  changes to their findings and reduces the effort of a follow-up review
  pass.

### When to include false starts

Include wrong first attempts only when they teach something the final fix
does not. "I first put it on port 9001 because it sat neatly below the
gateway's band. It sat neatly on top of Keycloak's management port." That
teaches why the final port choice is what it is. Not every fix has a wrong
first attempt. Omit it when the fix was straightforward.

### When to omit sections

Omit "False starts" when empty. Omit "Deliberately not done" when nothing
was deferred. "What this pass changed" and "Verification" are always
present.

## Step 7: Update PR description footer

After posting the summary comment, update the PR description's footer with
a bullet or two linking to the summary comment. This makes the pivots
discoverable from the PR body, not buried in the comment thread.

Use `gh pr edit` (GitHub) or equivalent to append to the PR body. Add a
section like:

```markdown
## How this PR got here

- [Summary of changes from review round](link-to-comment) — what changed
  and why.
```

If the PR description already has a "How this PR got here" footer, add the
new bullet to the existing list.

## Retrospective mode

When a PR has been through multiple review rounds, a per-round summary may
not be enough. A retrospective synthesizes the full evolution of the PR
across all rounds into a single narrative.

### When to use

The user requests it explicitly, or after the third or later review round
on the same PR. A retrospective is a deliberate synthesis, not an automatic
output. Offer it. Do not produce it without the user's go-ahead.

### What it produces

A top-level comment (or a section appended to the PR description) titled
"How this PR got to this shape." It covers:

- **The reverted predecessor or earlier attempt** (if any) — what was
  tried, why it failed, what it taught.
- **Each review round's effect** — what the review found, what changed as a
  result, and which design decisions pivoted.
- **False starts across rounds** — fixes that were themselves wrong and
  had to be revised again. These are the most instructive parts.
- **Deliberately not done** — scope boundaries that held across all rounds.
- **The tests as deliverable** — if the review process produced or fixed
  tests, note what they cover and why.

### Prose rules

Same as the per-round summary: plain English, one idea per sentence, no
buzzwords, define jargon on first use, conclusion-first. But the
retrospective is longer because the value is in the evolution, not just the
final state. Scale to the number of rounds and the complexity of the
pivots. A PR with one pivot gets a paragraph. A PR with five pivots gets
sections.

### Relationship to per-round summaries

The retrospective does not replace per-round summaries. It synthesizes
them. If per-round summaries exist as comments, the retrospective links to
them. If they do not (because the user skipped them in earlier rounds), the
retrospective covers those rounds from git history and review comments.

## Prediction material

Review response discussions are high-signal material for the user decision
model. When the user tells you how to classify a finding, how to phrase a
response, or what to include in the summary, watch for preferences about:

- Classification threshold (what counts as legitimate vs. unlikely)
- Response tone and length
- What to include in the summary (false starts? deliberately not done?)
- Whether to respond on bot findings or just fix silently
- When to push back vs. accept a finding

Before creating a new prediction, query for an existing one and reinforce
or adjust it when possible.
