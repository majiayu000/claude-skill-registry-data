---
name: pr-review-rubric
description: Staff-level PR review rubric — correctness, contract, clarity, tests, blast radius. Use when reviewing code (yours or others') before merge.
---

# PR review rubric

What a staff-plus engineer looks at when reviewing.

## 1. Understand before commenting

- Read the PR description. If there isn't one, that's the first problem.
- Skim commits. A clean story of atomic commits tells you what the author was thinking.
- Read the tests first — they describe the contract.
- Now read the code.

If you can't state what this PR does in one sentence in your own words, you can't review it yet.

## 2. Correctness

- Does the happy path do what the description claims?
- What are the boundary inputs? (empty, huge, zero, negative, unicode, null, undefined, missing)
- What about concurrency? Two callers at once. Retries. Cancellation.
- Error paths — is every `throw` handled, and is the handler the right place?
- Off-by-one, inclusive/exclusive range, integer overflow on counters.

## 3. Contract

- Public API change? Add-only? Breaking?
- Response shape change — who depends on the old shape?
- Database schema change — is the migration safe under traffic?
- Removed a function — who called it? `git grep` before approving the delete.

## 4. Clarity

- Names convey intent. `getUser` returns a user. `getUserOrDefault` returns a user or a default. `resolve` explains nothing.
- Control flow reads top-to-bottom with minimal branching surprise.
- The obvious case isn't buried under the edge case.
- Comments explain *why*, not *what*. If there's a non-obvious constraint, it's documented.

## 5. Tests

- Do they assert behavior the user cares about, or implementation detail?
- Would they catch the next regression of this code?
- Are the failing messages useful, or "expected true got false"?
- Are there tests for every new branch?
- Do the tests actually run? (Yes, this gets missed.)

## 6. Blast radius

- What else does this code touch or get touched by?
- Are those callers tested, or are we relying on this PR's tests alone?
- Is there a way to stage the rollout?

## 7. Security

- Only flag real risks. "You could add validation here" is noise unless there's an exploitable surface.
- If this touches authn/authz, data egress, or user-controlled strings → apply the security checklist.

## 8. Perf

- Loops inside loops on user data. Queries inside loops. New deps that balloon the bundle.
- Do not optimize on feel. If you flag perf, propose a measurement.

## Severity

Every comment has a severity:

- **Blocker** — must fix before merge
- **Important** — should fix, call out if intentional
- **Nit** — optional polish
- **Question** — explain the choice

Pick the right severity. "Blocker" for whitespace is how people learn to ignore you.

## Respect the author

- Point at the problem. Let them choose the fix.
- Don't rewrite the PR in the comments.
- Ask before assuming incompetence — sometimes there's context you don't have.
- Approve with nits is a valid verdict. Don't chain-block on trivia.
