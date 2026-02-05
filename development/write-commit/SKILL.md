---
name: write-commit
description: Write well-structured commit messages.
---

# Write Commit

## Conventions

- Check repo's existing commits first (`git log --oneline -20`)
- Subject: imperative mood, 50 chars max, capitalized, no period
- Body: wrap at 72 chars, explain what and why (not how)
- Skip body for trivial/self-explanatory changes (renames, typos, simple fixes)
- Use conventional prefixes (`feat:`, `fix:`, `docs:`) only if repo uses them

## Format

```
<Subject - imperative, 50 chars max>

<Body - wrap at 72 chars>

Explain motivation: what problem does this solve?
Why this approach over alternatives?

- Bullet points for multiple changes
- Keep each point concise

Fixes #123
```

## Examples

Subject-only (trivial changes):

```
Fix typo in README
```

```
Rename auth module to authentication
```

```
Add input validation for email field
```

With body (complex changes):

```
Refactor authentication to use JWT

Session-based auth required sticky sessions, complicating
horizontal scaling. JWT tokens are stateless and verifiable
by any server instance.

Trade-off: tokens cannot be invalidated before expiry.
Added a token blacklist for logout and password changes.
```

```
Fix race condition in queue processor

Multiple workers could claim the same job when polling
simultaneously. Added row-level locking.

Fixes #847
```

## Avoid

- `Fix stuff`, `WIP`, `Update file.js` (too vague)
- Past tense (`Fixed` instead of `Fix`)
- Mixing unrelated changes
