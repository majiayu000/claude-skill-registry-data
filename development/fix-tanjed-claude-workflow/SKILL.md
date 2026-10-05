---
name: fix
description: >
  Diagnose and fix a bug, error, or failing test. Auto-invoke when the user
  shares an error message, stack trace, failing test output, or says "this is
  broken", "fix this bug", "why is this failing", "debug this".
allowed-tools: Read, Write, Bash, Glob, Grep
argument-hint: <error message, file path, or description of the bug>
---
 
# Fix Skill
 
Diagnose and fix: `$ARGUMENTS`
 
## Step 1 — Reproduce and Understand the Failure
 
### If an error message or stack trace is provided:
- Read it fully — identify the exact file, line, and error type
- Trace the call stack from the bottom up — where did it actually originate?
 
### If a failing test is provided:
```bash
# Run just the failing test to get full output
npx jest --testNamePattern="<test name>" --verbose 2>&1
go test ./... -run "TestName" -v 2>&1
./vendor/bin/pest --filter="test name" 2>&1
```
 
### If a vague description ("it's broken", "it returns wrong data"):
- Ask ONE question to get a reproducible case before proceeding
- Never guess at a fix without understanding the failure
 
## Step 2 — Trace the Root Cause
 
Do NOT fix the symptom. Find the root cause.
 
Checklist:
- Is this a **type mismatch**? (null where value expected, wrong shape)
- Is this a **missing guard**? (no null check, no error handling)
- Is this a **wrong layer**? (business logic leaking into wrong place)
- Is this a **dependency wiring** issue? (wrong implementation injected, service not registered)
- Is this a **data problem**? (bad migration, wrong column type, missing index causing wrong query result)
- Is this a **race condition or async issue**? (missing await, shared mutable state)
- Is this a **contract mismatch**? (interface not matching implementation, DTO missing a field)
 
Read all files involved in the call chain — not just the file where the error appears.
 
```bash
# Trace what calls what
grep -r "methodName\|ClassName" src/ --include="*.ts" -n 2>/dev/null
grep -r "FuncName\|StructName" internal/ --include="*.go" -n 2>/dev/null
grep -r "methodName\|ClassName" app/ --include="*.php" -n 2>/dev/null
```
 
## Step 3 — State the Diagnosis Before Fixing
Output this before touching any code:
 
```
Root cause: <precise explanation of WHY it fails, not just what error appears>
Location:   <file:line>
Fix:        <what will be changed and why this solves the root cause>
Risk:       <any side effects or related areas that might be affected>
```
 
If the fix is more than 10 lines or touches more than 2 files — wait for approval.
Simple, obvious fixes can proceed immediately.
 
## Step 4 — Apply the Fix
 
Rules:
- Fix only what is broken — no unrelated refactoring in the same change
- If the root cause reveals a design problem (e.g. missing interface, wrong layer), fix the immediate bug first, then flag the design issue separately
- After fixing, verify the fix doesn't break adjacent behaviour
 
```bash
# Verify: run tests related to the changed files
npx jest --collectCoverageFrom="<changed-file>" 2>&1
go test ./... -run ".*" 2>&1
./vendor/bin/pest 2>&1
```
 
## Step 5 — Prevent Recurrence
 
After fixing, answer:
- Does this need a new test case that would have caught this? Write it.
- Is this a class of bug (missing null check everywhere, no error handling on a pattern) that exists elsewhere? Grep for it and report.
- Was this caused by a missing abstraction or a layer violation? Flag it for a follow-up `/refactor` or `/design-review`.
 
## Output
- Show the exact diff of what changed
- Confirm the fix with test output
- Note any follow-up work (design issues, missing test coverage, similar bugs elsewhere)

