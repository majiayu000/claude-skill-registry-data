---
name: code-review
description: Use when reviewing a diff before merges or pushes — checking correctness, readability, test adequacy, security, and scope.
---

# Code Review

## Priority order

Review in this order, and don't let later items distract from earlier ones:

1. **Correctness** — does the change do what it claims, including edge cases?
2. **Readability & naming** — can a future reader understand it without asking
   the author?
3. **Test adequacy** — are the changed behaviors actually covered?
4. **Security** — any of the concerns in `nextjs-security`/input handling/auth?
5. **Scope** — is the diff tightly focused on its stated purpose?

## Scope discipline

- Reject or split out unrelated refactoring bundled into a feature/fix diff.
  Unrelated changes make the diff harder to review and harder to revert safely.

## Reviewer behavior

- Leave actionable comments — say what to change, not just that something is
  wrong.
- **Verify claims rather than trusting them.** If the author says "tests pass"
  or "this handles X," check it — run the tests, read the code path.
- Mark every comment explicitly as **blocking** or **non-blocking** so the
  author knows what must be fixed before merge vs. what's a suggestion.
- Approve only once all blocking issues are resolved.

---
Source: blog.palantir.com/code-review-best-practices
