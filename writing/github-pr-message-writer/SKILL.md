---
name: github-pr-message-writer
description: Draft GitHub pull request titles, bodies, issue-closing footers, and maintainer ping comments. Use when the user wants a PR message, PR description, review request comment, or commitlint-safe/conventional-commit-friendly PR text based on a concrete bug fix or feature change.
---

# GitHub PR Message Writer

Use this skill to generate PR-facing text that is ready to paste into GitHub with minimal cleanup.

Default outputs:

1. Suggested PR title
2. PR body
3. Optional maintainer ping comment if the user asks

## Core Goals

- Make the PR easy for maintainers to review quickly.
- Preserve the real bug / change scope.
- Avoid boilerplate status noise unless the user explicitly wants it.
- Keep the text compatible with repo-specific PR title or commitlint checks when possible.

## First Checks

If the target repo exists locally, inspect these before drafting:

- `.github/workflows/` for PR title / semantic PR / commitlint checks
- `.commitlintrc*` or equivalent lint config
- contributing docs if they define PR title conventions

If the repo lints PR title + body as a merge commit message:

- output a Conventional Commits style title
- do not use a plain prose title
- put `Fixes #123` or similar issue-closing footer at the end of the PR body
- ensure there is a blank line before the footer

## Writing Rules

1. Lead with the actual problem solved.
2. Explain root cause only as far as needed for review.
3. Summarize what changed in a few bullets.
4. Omit routine workflow narration such as rebasing, formatting, or CI basics unless the user asks.
5. Do not inflate the PR body into a deep-dive article unless the user explicitly wants that.
6. If the user has a public write-up or blog post, link it as optional background instead of duplicating everything.
7. If the user asks to mention production impact or deployment evidence, include it briefly near the end.
8. If the user asks to mention AI assistance, keep it short and place it near the end, before any issue-closing footer.

## Default Structure

Use this structure unless the user requests a different format:

### Suggested PR title

- One line only
- Prefer `fix(scope): subject` / `feat(scope): subject` when repo conventions suggest it

### PR body

Use short sections:

1. `Summary`
2. `Root cause`
3. `What changed`
4. `Additional context` only if it adds value
5. Final short note if requested
6. Blank line
7. `Fixes #123`

## What To Avoid

- Long code indexes in PR bodies
- File-by-file changelogs unless specifically requested
- Test / rebase / formatting narration as filler
- Marketing language
- Hiding the actual problem behind generic phrases like "improves stability"

## Reviewer Ping Comments

When the user asks for a maintainer ping / review request comment:

- keep it under 6 lines
- be polite and direct
- mention concrete impact
- say why the review matters now
- include a background link only if it truly helps

Template:

```md
@maintainer could you take a look at this PR when you have a chance?

This issue is currently affecting my normal use of X in production, so I would really appreciate a review when convenient.

Thanks.
```

## Conventional-Commit-Friendly Pattern

If commitlint or semantic PR checks are present, default to:

Title:

```text
fix(scope): concise subject
```

Body pattern:

```md
## Summary

Short problem statement.

## Root cause

Short explanation.

## What changed

- change 1
- change 2

## Additional context

- optional link

Requested final note if any.

Fixes #123
```

Important:

- `Fixes #123` belongs at the bottom, not the top
- leave a blank line before the footer
- do not reuse a prose heading as the PR title if the repo expects conventional commits

## Output Style

When generating the result, prefer:

- one fenced block for `Suggested PR title`
- one fenced block for `PR body`
- one fenced block for `Review request comment` if requested

Keep each block ready to paste without further explanation unless the user asks for alternatives.
