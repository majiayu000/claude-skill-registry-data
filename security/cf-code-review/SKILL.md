---
name: code-review
description: When the user asks to review code, review a diff, check changes before pushing, or wants a second opinion on their work — activate this skill for structured code review
---

# Code Review Skill

## Goal

Find issues that matter — bugs, security holes, and maintainability problems — in changed code. Skip style nitpicking. Every finding must be actionable.

## Constraints

- Only flag real issues. If there's nothing significant, say so. Don't invent problems.
- Read the full file for context, not just the diff lines.
- Group by severity: **Critical** (bugs, security, data loss) > **Warning** (code smells) > **Suggestion** (readability).
- Every finding needs: file:line, what's wrong, why it matters, suggested fix.

## Review Priorities

1. **Correctness** — logic errors, edge cases, race conditions, resource leaks
2. **Security** — injection, auth bypass, leaked secrets, OWASP top-10
3. **Maintainability** — unclear naming, SRP violations, dead code
4. **Performance** — N+1 queries, unnecessary allocations, missing indexes

## Output

End with a verdict: **Ship it** / **Needs changes** / **Needs discussion**, plus the top 1-3 items to fix first.

## Gotchas

- Don't review generated files (lock files, build output, vendor dirs) unless the user specifically asks.
- When reviewing a large diff (50+ files), prioritize files with logic changes over config/docs changes.
- Watch for "fix one thing, break another" — check that the fix doesn't introduce a regression in the same file.
- If a test file changed but the source didn't (or vice versa), flag the mismatch.
