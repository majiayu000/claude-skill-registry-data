---
name: review
description: Review code, a diff, a branch or a pull request for correctness, security, performance, maintainability and test coverage, producing severity-ranked findings with concrete fixes. USE WHEN the user asks to "review", "check my code", "look over", "audit", "any issues with", "before I merge", or wants a second opinion on changes.
---

# Review

Goal: findings a reviewer would actually block on, ranked, each with file:line and a concrete fix — not a style lecture.

## 1. Scope the change
- Diff first: `run_command` `git diff` (unstaged), `git diff --cached`, or `git diff main...HEAD` / the PR's base. No diff? Review the files the user named, or the recently changed ones (`git log --name-only -5`).
- Read the surrounding code for every hunk — a hunk is only right in context. Use `find_references` on changed signatures to check all callers were updated.
- Understand the intent (commit messages, linked spec/design docs, PR description) so you review against what was meant, not what you'd have built.

## 2. Check, in this order
1. **Correctness** — logic errors, off-by-one, null/undefined, wrong types at boundaries, unhandled promise/async paths, error handling that swallows failures, race conditions, broken invariants, missed edge cases (empty, max, unicode, concurrency).
2. **Security** (OWASP Top 10) — injection (SQL/shell/HTML/path), auth/authz gaps, secrets in code or logs, unsafe deserialization, SSRF, insecure defaults, missing input validation at system boundaries, dependency risk.
3. **Data & compatibility** — schema/migration safety, backward compatibility of APIs and stored data, feature-flag behaviour, i18n/timezone.
4. **Performance** — N+1 queries, work inside hot loops, unbounded memory, missing pagination/limits, blocking I/O on the main thread, redundant re-renders.
5. **Tests** — are new behaviours and bug fixes covered? Do tests assert behaviour (not implementation)? Any weakened/deleted assertions?
6. **Maintainability** — naming, duplication, dead code, misleading comments, inconsistency with the codebase's own conventions. Mention only when it hurts understanding.
Run what you can: `get_diagnostics`, the lint/typecheck/test commands. Real failures beat opinions.

## 3. Write the review
```markdown
## Summary
One paragraph: what the change does and overall verdict (approve / approve with nits / request changes).

## Findings
### 🔴 Must fix
- `src/x.ts:42` — <problem>. <why it matters>. Fix: <concrete change or snippet>.
### 🟠 Should fix
### 🟡 Consider
### ✅ Good
Call out things done well (1–3 bullets) so they are kept.

## Tests & verification
What was run and the result; gaps.
```
- Every finding: location, problem, impact, fix. No vague "consider refactoring".
- Don't restate the diff; don't nitpick formatting a linter would catch.
- If asked to fix as well, apply the Must/Should fixes with the `implement` workflow and re-verify.
