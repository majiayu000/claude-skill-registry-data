---
name: verification-gate
description: Hidden quality gate that runs before showing "Done!" to user - ensures all tests pass, build succeeds, and requirements met before claiming completion
---

# Verification Gate

## Overview

Part of the hidden validation layer. User never sees this running, but it prevents false "Done!" claims.

**Core principle:** Never show success to user without evidence.

## When This Runs (Automatically)

- Before displaying "✅ Done!"
- Before showing preview URL
- Before `/mvp:deploy`
- After any `/mvp:add` feature

## The Gate Checklist

```
BEFORE showing success to user:

[ ] Tests pass (run full suite, not partial)
[ ] Build succeeds (no compilation errors)
[ ] No TypeScript/linting errors
[ ] Feature actually works (manual smoke test)
[ ] Security checks pass (from security-check skill)
[ ] Code review clean (from code-review-auto skill)

ALL must pass. ANY failure = fix silently, don't show error to user.
```

## User Experience

**What user sees:**
```
Adding login feature...
✅ Done! Check your preview.
```

**What happens behind the scenes:**
```
1. Generate login code
2. Run tests → 2 failures
3. Fix failures automatically
4. Run tests → pass
5. Run build → pass
6. Security check → pass
7. Code review → 1 minor issue
8. Fix issue automatically
9. All gates pass → show "Done!"
```

## Failure Handling

**If gate fails and can auto-fix:**
- Fix silently
- Re-run verification
- User never knows

**If gate fails and cannot auto-fix:**
- Ask simple question (no technical jargon)
- Example: "Should login require email confirmation?"
- NOT: "The auth middleware threw ValidationError"

## Automation Script

Run all checks programmatically:

```bash
python scripts/verify.py --path /project/path --language rust
python scripts/verify.py --path /project/path --json  # JSON output
```

The script auto-detects language and runs appropriate checks.

## Integration

**Called by:**
- `/mvp:build` - Before showing preview
- `/mvp:add` - Before confirming feature added
- `/mvp:deploy` - Before deployment

**Uses:**
- **auto-testing** - Run test suite
- **security-check** - Security validation
- **code-review-auto** - Code quality check
- **scripts/verify.py** - Deterministic verification

## Philosophy

User paid for "vibe coding" - they describe what they want, we handle how.

Showing them test failures or build errors breaks the magic.

Fix it. Don't explain it.
