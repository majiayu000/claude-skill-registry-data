---
name: debug-session
description: Start a structured debugging session for an error or unexpected behavior. Use when encountering bugs or test failures.
---

# Debug Session

Structured debugging workflow for: $ARGUMENTS

## Process

1. **Reproduce** — get a minimal reproduction
2. **Isolate** — binary search to find the smallest failing case
3. **Hypothesize** — form 2-3 hypotheses about root cause
4. **Test** each hypothesis with targeted logging/reading
5. **Fix** the root cause, not symptoms
6. **Verify** fix doesn't break other tests
7. **Document** what was found in a comment or ADR

See [debugging-patterns.md](./debugging-patterns.md) for common patterns.
