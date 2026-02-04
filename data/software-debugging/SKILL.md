---
name: software-debugging
description: Find and fix bugs systematically. Use when encountering errors, test failures, or unexpected behavior. Hypothesis-driven debugging to locate root causes and implement minimal fixes.
---

# Software Debugging

You find and fix bugs systematically.

## Method

Hypothesis-driven debugging. Test hypotheses. Find root cause. Fix minimally.

## Process

### 1. Reproduce

- Isolate minimal steps
- Verify consistent reproduction
- Document exact conditions
- Note environment factors

### 2. Gather Evidence

```
Error: [Exact message]
Stack: [Key frames]
When: [Conditions]
Changed: [Recent changes]

Hypotheses:
1. [Most likely]
2. [Second possibility]
3. [Edge case]
```

### 3. Test Hypotheses

For each:
- Test: [How to verify]
- Expected: [What should happen]
- Actual: [What happened]
- Result: Confirmed/Rejected

### 4. Root Cause

```
Cause: [Actual problem]
Not: [What seemed wrong but wasn't]
Why missed: [Testing gap]
```

### 5. Fix

- Implement minimal fix
- Verify resolution
- Check side effects
- Add regression test

## Investigation Pattern

**Narrow down:**
- Binary search through code paths
- Add strategic logging
- Isolate failing component
- Identify exact failure point

**Fix:**
- Minimal change only
- Root cause, not symptoms
- Preserve existing behavior
- Keep changes traceable

**Verify:**
```bash
just test        # Regression test passes
just check-all   # No side effects
```

## Common Bug Types

**Type bugs:**
- None/null handling
- Type mismatches
- Undefined variables

**State bugs:**
- Race conditions
- Stale data
- Initialization order

**Logic bugs:**
- Off-by-one
- Boundary conditions
- Wrong assumptions

**Integration bugs:**
- API contract violations
- Version incompatibilities
- Configuration issues

## Logging Strategy

Strategic points only:

```python
logger.debug(f"Entering {fn} with {args}")
logger.debug(f"State before: {state}")
logger.debug(f"Decision: {condition} = {value}")
logger.error(f"Expected {expected}, got {actual}")
```

## Fix Principles

**Minimal:**
- Fix root cause only
- Don't refactor while fixing
- One change at a time

**Defensive:**
- Add appropriate guards
- Validate inputs
- Handle edge cases
- Fail gracefully

**Tested:**
- Add test for bug
- Test boundary conditions
- Verify error handling

## Output Format

```markdown
## Bug: [Description]

### Reproduction
Steps: [Minimal]
Frequency: [Always/Sometimes/Rare]

### Root Cause
Problem: [Exact issue]
Location: file.py:123
Why: [Explanation]

### Fix
# Before
[problematic code]

# After
[fixed code]

### Verification
- [ ] Original issue resolved
- [ ] No side effects
- [ ] Regression test added
```

## Prevention

After fixing, suggest:
1. Code improvements to prevent similar bugs
2. Testing gaps to fill
3. Documentation that would help
4. Monitoring to catch earlier

## Red Flags

- Fixing symptoms, not root cause
- Refactoring during bug fix
- No regression test added
- Side effects not checked
- Changes too broad

Fix the root cause. Add a test. Move on.
