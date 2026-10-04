---
name: retriggering-ai-reviews
description: >-
  Use when a pull request has no CodeRabbit, cubic, or Qodo review after a push, a bot replies that
  the review was rate limited, that the review limit was reached, that the review was skipped
  because the diff exceeds 100 files, or that reviews are paused; when several PRs need AI review in
  one session; or when a CodeRabbit approval is required before merge. Names the mention commands
  each bot accepts and the reviewers no mention can reach.
---

# Retriggering AI reviews

## Profile keys consumed

- `review.coderabbit`
- `make.pr_comments`
- `ci.required_checks`

`review.coderabbit` says whether a CodeRabbit review is expected at all — when it is disabled,
record the CodeRabbit steps SKIPPED and fall back to the reviewers that do run. Thread listing goes
through the target mapped by `make.pr_comments`; skip that step with a recorded note when it maps to
`null` and list threads with the GitHub CLI instead. `ci.required_checks` is the check set that must
have registered before a review is requested.

## Overview

Frontend repositories in this plugin's scope rely on bot reviewers that do not always run on their
own: CodeRabbit auto-review is often paused at the organization level and refuses oversized or
rate-limited PRs, cubic runs only when asked, and Qodo stops entirely when its subscription lapses.
The remedy is a mention comment on a PR that is already in its final shape — plus knowing which
reviewers no mention can reach.

## When to use

- A PR has CI running but no review from `coderabbitai`, `cubic-dev-ai`, or `qodo-code-review`.
- CodeRabbit replied `Review rate limited.`, `Review limit reached`, or
  `Review skipped: N files exceed the limit of 100`.
- Qodo posted that reviews are paused because the subscription is no longer active.
- Several PRs are being landed in one session and each needs a fresh AI review.
- A branch-protection rule wants a CodeRabbit approval and none has been posted.
- Not for: qlty and SonarCloud. Both post their own summary comment automatically and have no
  mention command; they only re-run on a new push.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — CodeRabbit, cubic, Qodo, and qlty all comment; the target mapped by
  `make.pr_comments` lists threads.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — the same four bots; the
  target mapped by `make.pr_comments` lists threads.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — the same
  four plus SonarCloud; there is no mapped `make.pr_comments` target, so list threads with
  `gh api graphql` directly.

## Quick reference

| Reviewer   | Trigger comment             | Notes                                        |
| ---------- | --------------------------- | -------------------------------------------- |
| CodeRabbit | `@coderabbitai review`      | incremental; about one per hour per repo     |
| CodeRabbit | `@coderabbitai full review` | re-reviews already-reviewed commits          |
| CodeRabbit | `@coderabbitai approve`     | resolves threads and approves; no merge      |
| cubic      | `@cubic-dev-ai review`      | replies "I have started the AI code review"  |
| cubic      | `@cubic-dev-ai approve`     | blocked while cubic threads stay unresolved  |
| Qodo       | none while paused           | lapsed subscription; report and skip         |
| qlty       | none                        | auto-comments a summary; re-run by pushing   |
| SonarCloud | none                        | component-library shape; comment per push    |

Start the comment with the mention — text before it can stop the bot parsing it, while trailing
words on the same line are fine (`@cubic-dev-ai review this PR` starts a review).
`@coderabbitai review` skips commits it has already reviewed, so reach for
`@coderabbitai full review` after a long gap or a dismissed review.

## Procedure

1. Pre-flight the PR before asking, so the bot reviews the final diff:
   - not a draft (CodeRabbit auto-review skips drafts);
   - at or under 100 changed files — above that CodeRabbit answers `Review skipped` and no mention
     helps; split the PR or change its base branch;
   - `mergeable` is true (`gh pr view <n> --json mergeable`);
   - earlier threads answered — CodeRabbit will not approve while threads are open;
   - the full check set named by `ci.required_checks` has registered (30-plus checks in the React
     SPA and Next.js shapes) with no failure; pending is fine.
2. Post the mention as its own comment:

   ```bash
   gh pr comment <n> --body '@coderabbitai review'
   gh pr comment <n> --body '@cubic-dev-ai review'
   ```

3. Wait for the bot's acknowledgement, then poll for the review (two to five minutes). Address
   findings, push, and re-request only after the push.
4. For several PRs, space CodeRabbit requests about an hour apart. When it answers
   `Review limit reached` it names the wait itself (`Next review available in: 20 minutes`) and that
   figure beats the hourly rule of thumb. cubic has no such limit. Keep a
   `PR / checks passing / reviewer state` table and update it after each bot response.
5. When findings are addressed and CI is green, post `@coderabbitai approve` if the repository
   requires its approval. It resolves the threads and records an approving review; the squash merge
   stays a separate step.
6. When a reviewer cannot run (Qodo subscription lapsed, cubic refusing a bot-authored PR on the
   free plan, CodeRabbit out of credits), say so in the PR summary and fall back to the reviewers
   that did run plus a local review. Never treat a missing review as an implicit pass.

## Common mistakes

- Requesting before CI has registered — the bot reviews a diff that then changes; wait for checks.
- Firing `@coderabbitai review` on every PR at once — requests queue silently; space them an hour.
- Putting the mention mid-sentence — the bot ignores it; start the comment with it.
- Re-mentioning after `Review skipped: N files exceed the limit of 100` — no mention lifts that;
  reduce the PR to 100 files or fewer.
- Retriggering Qodo while it reports a lapsed subscription — nothing happens; report and move on.
- Waiting for a mention-driven reply from qlty or SonarCloud — read the summary comment they already
  posted and their check details instead.
- Treating `@coderabbitai approve` as a merge command — it records an approval; merge with squash as
  the repository requires.
