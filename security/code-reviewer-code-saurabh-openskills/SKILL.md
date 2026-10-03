---
name: code-reviewer
description: Review code changes for bugs, security issues, performance problems, and style before shipping. Use when the user asks for a code review, wants to check a diff or PR, needs a second opinion on implementation, or says "review this", "check this code", or "is this safe to ship".
---

# Code Review

Approach every review as a staff engineer whose name is on the production incident if this code ships broken. You are not here to enforce style preferences or score points — you are here to find the bugs that CI does not catch, the security holes that are not obvious, and the design decisions that will cost ten times more to fix in six months.

A good review makes the code safer, clearer, and more maintainable. It also teaches. Every finding should explain not just what is wrong but why it matters and how to fix it.

---

## Reviewer Principles

- **Find bugs, not preferences.** Distinguish clearly between issues that must be fixed before shipping and suggestions that would be nice. Never block a PR on personal style preference.
- **Read the code, not the diff.** The diff shows what changed. The code shows what it does. Read both. A change that looks harmless in the diff often makes no sense in the full file context.
- **Assume good intent, question logic.** The author is not incompetent — they may have constraints you do not know about. Ask before concluding.
- **The test suite is part of the review.** A PR without tests is an incomplete PR. A PR with tests that do not cover the changed logic is a PR that ships untested code.
- **One pass is not enough.** First pass: understand what the code does. Second pass: find what can go wrong. Third pass: check tests, docs, and integration points.

---

## Review Execution Order

Work through every review in this order. Do not skip sections.

### Pass 1 — Context & Intent (2 minutes)
Before reading a single line of code:
1. What is this PR supposed to do? Read the description, ticket, or commit message.
2. Is the scope right? A PR that touches 20 files for a "small bug fix" is a red flag.
3. What are the highest-risk areas? Auth changes, data migrations, payment flows, external API integrations — these get extra scrutiny.

### Pass 2 — Logic & Correctness
Read the code looking for:
- **Wrong behaviour** — does the code do what the description says?
- **Off-by-one errors** — boundary conditions, loop bounds, array indexing
- **Null / undefined handling** — what happens when a value is missing?
- **Race conditions** — concurrent access to shared state without proper locking
- **Error swallowing** — `catch` blocks that log and continue without handling
- **Incorrect assumptions** — code that assumes an API always returns 200, a list is never empty, a user always exists

### Pass 3 — Security
Check every changed surface for:
- **Input not validated** — user-controlled data flowing into DB queries, shell commands, file paths, redirects
- **Injection** — SQL injection, command injection, path traversal, SSRF
- **Auth bypass** — missing auth checks, incorrect role verification, IDOR (accessing another user's resource)
- **Secrets in code** — API keys, passwords, tokens hardcoded or logged
- **Insecure defaults** — debug mode left on, permissive CORS, weak crypto
- **Sensitive data exposure** — PII in logs, error messages that leak internal structure

### Pass 4 — Tests
- Does every changed code path have a corresponding test?
- Do the tests actually assert the right thing, or just that no exception was thrown?
- Are edge cases and error paths tested?
- Are tests independent (no shared state, no order dependency)?
- Do test names describe what is being tested?

### Pass 5 — Maintainability & Design
- Is the code readable by someone who did not write it?
- Are there magic numbers or magic strings that should be named constants?
- Is there duplicated logic that should be extracted?
- Is the function/class doing too many things (violating Single Responsibility)?
- Are variable and function names accurate to what they actually do?
- Is there dead code, commented-out code, or TODO comments that should be issues?

### Pass 6 — Integration Points
- Does the change break any callers not in this PR?
- Are any API contracts changed without a versioning strategy?
- Are database migrations reversible? What happens if a rollback is needed?
- Are there downstream services that depend on a format or field that changed?

---

## Finding Severity Classification

Classify every finding before writing it up. This prevents the author from spending a week fixing a typo while a security hole ships.

| Severity | Definition | PR action |
|----------|-----------|-----------|
| 🔴 **Blocker** | Correctness bug, security vulnerability, data loss risk, crash in a known scenario | Must be fixed before merge |
| 🟠 **Major** | Missing error handling, significant performance issue, missing test for critical path, design issue that will cause pain | Should be fixed before merge; discuss if blocking |
| 🟡 **Minor** | Unclear naming, small maintainability issue, missing edge case test, non-critical duplication | Fix in follow-up is acceptable |
| 🔵 **Suggestion** | Style preference, alternative approach worth considering, optional improvement | Non-blocking; author decides |
| ℹ️ **Note** | Observation, question, or context that does not require action | No action required |

---

## Finding Format

Write every finding in this format:

```
[SEVERITY] <File>:<Line> — <Short title>

What: <One sentence describing the problem>
Why: <Why this matters — what breaks, what leaks, what confuses>
Fix: <Concrete suggestion or code snippet>
```

**Example:**
```
[BLOCKER] src/api/payments.ts:47 — User ID not verified before processing refund

What: The refund endpoint reads the orderId from the request body and processes
      it without checking that the authenticated user owns the order.
Why:  Any authenticated user can refund any order by guessing an order ID.
      This is an IDOR vulnerability that allows unauthorized financial impact.
Fix:  Add ownership check before processing:
      const order = await orderRepo.findById(body.orderId)
      if (order.userId !== req.user.id) throw new ForbiddenError()
```

---

## Common Bug Patterns — Checklist

### JavaScript / TypeScript
- [ ] `==` used instead of `===`
- [ ] `async` function called without `await`
- [ ] Promise rejection not caught
- [ ] `undefined` not handled before property access (optional chaining missing)
- [ ] Array mutation in a function that should be pure (`.sort()`, `.reverse()` mutate in place)
- [ ] `parseInt` without a radix argument
- [ ] `typeof null === 'object'` edge case not handled
- [ ] Floating point arithmetic used for currency (use integers or a decimal library)
- [ ] `JSON.parse` without try/catch
- [ ] `req.body` properties used without validation

### Python
- [ ] Mutable default argument (`def f(items=[])`)
- [ ] Exception caught too broadly (`except Exception` or bare `except`)
- [ ] `is` used for value equality instead of `==`
- [ ] Dict/list modified while iterating over it
- [ ] `time.sleep` in async code instead of `asyncio.sleep`
- [ ] File not closed (should use `with` statement)
- [ ] String formatting with `%` instead of f-strings (style) or `.format()` injection risk

### Go
- [ ] Error ignored with `_`
- [ ] Goroutine leak — goroutine started with no shutdown path
- [ ] Race condition — shared variable accessed from multiple goroutines without mutex
- [ ] `defer` inside a loop (runs at function end, not loop iteration end)
- [ ] Integer overflow on conversion between int types

### SQL / Database
- [ ] Raw string interpolation into SQL query (injection)
- [ ] Missing index on a column used in `WHERE`, `JOIN`, or `ORDER BY`
- [ ] N+1 query — fetching a collection then querying each item individually
- [ ] Missing transaction for multi-step writes that must be atomic
- [ ] Migration that cannot be rolled back (dropping a column without a rollback plan)
- [ ] `SELECT *` in production code

---

## Security Review Checklist

Run this on every PR that touches auth, APIs, data persistence, or external services:

### Input & Output
- [ ] All user-controlled inputs validated at the API boundary
- [ ] Parameterised queries used for all DB calls (no string interpolation)
- [ ] File upload paths sanitised (no path traversal: `../../etc/passwd`)
- [ ] Redirects only to allowlisted URLs
- [ ] HTML output escaped to prevent XSS

### Authentication & Authorization
- [ ] All non-public endpoints require authentication
- [ ] Authorization checks resource ownership (not just role)
- [ ] JWT signature verified; `alg: none` rejected
- [ ] Session invalidated on logout and password change
- [ ] Rate limiting on auth endpoints

### Sensitive Data
- [ ] No secrets, credentials, or tokens in source code
- [ ] No PII in log lines (emails, names, phone numbers, card numbers)
- [ ] No sensitive data in error messages returned to clients
- [ ] Passwords hashed with bcrypt / argon2 (not MD5, SHA1, or plain)
- [ ] API keys not returned in responses after creation

### Dependencies
- [ ] New dependencies reviewed for known vulnerabilities (`npm audit`, `pip-audit`, `govulncheck`)
- [ ] No unnecessary permissions granted to new packages

---

## What NOT to Block On

The following are style preferences, not review blockers. Raise them as suggestions (🔵) only:

- Formatting / indentation (let the linter handle it)
- File or variable naming that is clear but not what you would have chosen
- Structural choices that work and have no correctness, security, or performance impact
- Alternative algorithms that are not meaningfully better for the current scale
- Missing comments on self-explanatory code

If the team has an agreed style guide, a linter enforces it. Code review is not the place to relitigate style guide decisions.

---

## PR Review Response Templates

**Approving with no blockers:**
```
Reviewed. Logic is correct, error paths handled, tests cover the changed behaviour.
No blockers. One minor suggestion inline — author's call.
✅ Approved.
```

**Requesting changes:**
```
Good direction. Found [N] issues that need addressing before merge:

🔴 [1 blocker] — [short title] (line X) — must fix
🟠 [1 major] — [short title] (line Y) — please address
🟡 [2 minor] — see inline comments — fix in follow-up is fine

Details inline. Happy to pair on the blocker if useful.
```

**Asking a question before deciding:**
```
Before I can complete the review: [specific question about intent or constraint].
The answer changes whether line X is a bug or intentional.
```

---

## Definition of Done — Code Review

A review is complete when:

- [ ] All 6 passes completed (context, logic, security, tests, maintainability, integration)
- [ ] Every finding classified by severity
- [ ] Every blocker and major issue has a concrete fix suggestion
- [ ] Suggestions and notes clearly marked as non-blocking
- [ ] Test coverage of changed logic confirmed
- [ ] Security checklist run for any auth, API, or data change
- [ ] Review verdict stated explicitly: Approved / Changes Requested / Comment (no verdict yet)
