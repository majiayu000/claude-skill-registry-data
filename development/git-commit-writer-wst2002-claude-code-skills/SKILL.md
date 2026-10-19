---
name: git-commit-writer
description: Use when writing a git commit message, committing staged changes, following Conventional Commits, cleaning up a vague commit message, or splitting a large mixed change into separate commits.
---

# Git Commit Writer

## Overview

A commit message tells a future reader why the change was made. Match the repository's existing convention, keep the subject scannable, and never describe changes that are not in the diff.

## Method

1. **Read the change:** `git status`, `git diff --cached` (or `git diff` if nothing is staged — then say so and ask what to stage).
2. **Detect the convention:** `git log --oneline -20`.
   - Most subjects look like `feat(x): ...` → Conventional Commits.
   - Ticket prefixes (`ABC-123: ...`) → keep that pattern.
   - Otherwise → plain imperative subjects.
3. **Check for mixed concerns.** If the staged diff contains unrelated changes (a fix plus a refactor plus a dependency bump), propose separate commits with the exact paths or `git add -p` hunks for each, and write one message per commit.
4. **Write the message** with the format below.
5. **Output the message.** Only run `git commit` when the user asked you to commit.

## Format

```
<type>(<scope>): <subject>

<body: why the change was needed and what it does, wrapped at 72>

<footer: BREAKING CHANGE: ..., Refs #123>
```

| Part | Rule |
|---|---|
| Subject | Imperative ("Add", "Fix", not "Added"), ≤ 72 characters, no trailing period, specific ("Fix rounding of order totals", not "Fix bug") |
| Type | `feat` new behavior, `fix` bug fix, `refactor` no behavior change, `perf`, `docs`, `test`, `build`, `ci`, `chore` |
| Scope | The area touched, taken from folder or module names; omit if unclear |
| Body | Why first, then what at a high level. Skip it for trivial one-line changes |
| Breaking change | `!` after type/scope and a `BREAKING CHANGE:` footer describing the migration |
| References | Issue or ticket IDs only if they appear in the branch name, diff or conversation |

## Example

```
fix(cart): keep discounts when quantity changes

Updating an item's quantity rebuilt the cart from the catalog price and
dropped any applied coupon, so customers were charged full price.
Recalculate totals from the existing line items instead.

Refs #482
```

## Common mistakes

- Describing every file ("update a.ts, update b.ts") instead of the purpose.
- Inventing motivation or ticket numbers not present in the context.
- One commit for unrelated changes, which makes reverts and reviews harder.
- Adding attribution or co-author trailers the user did not ask for.
- Committing when the user only asked for a message.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
