---
name: bug-investigation
description: Systematic bug investigation and root cause analysis
phases: [E, V]
---

# Bug Investigation

## When to Use
Use this skill when investigating bugs or unexpected behavior.

## Investigation Process

### 1. Reproduce
- Get exact steps to reproduce
- Identify environment (OS, version, config)
- Create minimal reproduction case

### 2. Isolate
- Binary search through code/commits
- Disable features to narrow scope
- Check if issue exists in isolation

### 3. Understand
- Read the relevant code carefully
- Check recent changes (git log, blame)
- Review related tests

### 4. Hypothesize
- Form theories about root cause
- Rank by likelihood
- Design tests for each hypothesis

### 5. Verify
- Add logging/debugging
- Write failing test
- Confirm fix addresses root cause

## Debugging Checklist
- [ ] Can I reproduce consistently?
- [ ] When did it start? (git bisect)
- [ ] What changed recently?
- [ ] Are there related error logs?
- [ ] Does it happen in all environments?
- [ ] Is it data-dependent?

## Root Cause Categories
- Logic error
- Race condition
- Resource leak
- Configuration issue
- Dependency problem
- Data corruption

## Report Format
```markdown
## Bug: [Title]

### Symptoms
[What the user sees]

### Root Cause
[Technical explanation]

### Fix
[What was changed and why]

### Prevention
[How to prevent similar bugs]
```