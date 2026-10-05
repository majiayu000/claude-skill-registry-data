---
name: debug
description: "Systematically debugs issues using structured diagnosis — reproduce, isolate, identify root cause, and fix. Use when facing bugs, errors, unexpected behavior, or failing tests."
argument-hint: "[error message, symptom, or file:line]"
allowed-tools: Read, Grep, Glob, Bash, Edit
---

# Structured Debugging

## Recent Changes
!`git log --oneline -10 2>/dev/null`
!`git diff --stat HEAD~3 2>/dev/null`

---

## Debugging Process

### Step 1: Gather Information
1. **What is the symptom?** — Error message, unexpected behavior, crash, performance issue
2. **When did it start?** — Check recent commits: `git log --oneline -20`
3. **Is it reproducible?** — Always, sometimes, only in certain environments?
4. **What changed?** — Recent code changes, dependency updates, config changes

### Step 2: Read the Error
If there's an error message or stack trace:
1. Read the **full** error message — don't skip parts
2. Identify the **origin** — which file and line threw the error?
3. Trace the **call stack** — how did execution reach that point?
4. Check for **root cause vs symptom** — the first error in the chain is usually the cause

### Step 3: Isolate the Problem
Use a binary search strategy:

1. **Narrow the scope**: Is the issue in the frontend, backend, database, or external service?
2. **Check inputs**: Are the inputs to the failing function correct?
3. **Check dependencies**: Are all required services/modules available?
4. **Check state**: Is the application/database in the expected state?
5. **Check environment**: Are env vars, configs, and versions correct?

### Step 4: Common Debugging Patterns

#### "It works on my machine"
- Check environment variables
- Check dependency versions (lock file differences)
- Check OS/runtime version differences
- Check file path separators (Windows vs Unix)
- Check timezone/locale differences

#### "It worked yesterday"
- `git bisect` to find the breaking commit
- Check for dependency updates (lock file changes)
- Check for infrastructure/config changes
- Check for data changes in the database

#### "It works sometimes"
- Race condition — look for shared mutable state
- Timing issue — look for missing awaits, unhandled promises
- Resource exhaustion — connections, file handles, memory
- External dependency flakiness — network, API rate limits

#### "It's slow"
- Profile before guessing — use the project's profiling tools
- Check for N+1 queries
- Check for missing indexes
- Check for synchronous blocking in async code
- Check for unnecessary re-computation

### Step 5: Fix and Verify
1. Implement the minimal fix
2. Verify the fix resolves the original issue
3. Check for regressions — run related tests
4. Add a test that would have caught this bug
5. Document the root cause in the commit message

### Step 6: Prevent Recurrence
- Should there be input validation to catch this earlier?
- Should there be a test for this scenario?
- Should there be monitoring/alerting for this condition?
- Should the error message be improved for faster debugging next time?

---

## Rules
- **Don't guess and check randomly** — use a systematic approach
- **Read the error message** — it usually tells you exactly what's wrong
- **Check the obvious first** — typos, missing imports, wrong file paths
- **One change at a time** — so you know what fixed it
- **Always add a regression test** for the bug you fixed
