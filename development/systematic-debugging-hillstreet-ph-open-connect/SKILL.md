---
name: systematic-debugging
description: Systematic root-cause debugging with structured triage. Use when tests fail, builds break, behavior doesn't match expectations, or you encounter any unexpected error. Find root cause before fixing - never guess.
license: MIT
---

# Systematic Debugging

Systematic debugging with structured triage. When something breaks, stop adding features, preserve evidence, and follow a structured process to find and fix the root cause. Guessing wastes time.

## When to Use This Skill

**Trigger conditions:**
- Tests fail after a code change
- The build breaks
- Runtime behavior doesn't match expectations
- A bug report arrives
- An error appears in logs or console
- Something worked before and stopped working

## The Stop-the-Line Rule

When anything unexpected happens:
```
1. STOP adding features or making changes
2. PRESERVE evidence (error output, logs, repro steps)
3. DIAGNOSE using the triage checklist
4. FIX the root cause
5. GUARD against recurrence
6. RESUME only after verification passes
```

**Don't push past a failing test or broken build to work on the next feature.** Errors compound.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## The Triage Checklist

Work through these steps in order. Do not skip steps.

### Step 1: Reproduce

Make the failure happen reliably. If you can't reproduce it, you can't fix it with confidence.

```
Can you reproduce the failure?
├── YES → Proceed to Step 2
└── NO
├── Gather more context (logs, environment details)
├── Try reproducing in a minimal environment
└── If truly non-reproducible, document conditions and monitor
```

### Step 2: Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

### Step 3: Check Recent Changes

- What changed recently?
- Git log, file modifications
- Dependencies updates
- Environment changes

### Step 4: Isolate the Problem

- Can you create a minimal reproduction?
- Remove unrelated code
- Find the smallest test case

### Step 5: Trace the Root Cause

**Question:** What's actually causing this?

- Look at where the error manifests
- Trace back through call stack
- Find the original trigger
- Fix at source, not symptom

### Step 6: Verify End-to-End

After fixing, verify:
```bash
# Run the specific test
npm test -- --grep "specific test"
# Run the full test suite
npm test
# Build the project
npm run build
```

## The Four Phases

### Phase 1: Root Cause Investigation

BEFORE attempting ANY fix:
1. Read error messages carefully
2. Reproduce consistently
3. Check recent changes
4. Trace the root cause

### Phase 2: Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

### Phase 3: Verify Fix

- Test passes now?
- No other tests broken?
- Issue actually resolved?

### Phase 4: Guard Against Recurrence

- Add proper test case
- Add validation at multiple layers
- Add monitoring/logging

## Anti-Patterns to Avoid

- Guessing at solutions
- Applying fixes without understanding root cause
- Skipping the reproduction step
- Making multiple changes at once
- Not adding tests after fixing

## Supporting Techniques

See `references/` for additional techniques:
- **root-cause-tracing.md** - Trace bugs backward through call stack
- **defense-in-depth.md** - Add validation at multiple layers
- **condition-based-waiting.md** - Replace arbitrary timeouts

## Error-Specific Patterns

### Test Failure
```
Test fails after code change:
├── Did you change code the test covers?
│ └── YES → Check if the test or the code is wrong
│    ├── Test is outdated → Update the test
│    └── Code has a bug → Fix the code
```

### Build Failure
```
Build breaks:
├── Check error message (often contains solution)
├── Check recent changes
├── Check dependencies
└── Isolate and reproduce
```

### Runtime Bug
```
Unexpected behavior:
├── Reproduce consistently
├── Trace data flow
├── Find where value becomes wrong
└── Fix at source