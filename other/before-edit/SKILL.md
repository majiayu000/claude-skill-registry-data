---
name: before-edit
description: Run before modifying a function — impact + test-map + explain in one pass, presented as a modification checklist.
argument-hint: "<function_name>"
---

# Before Edit

Run before modifying any function. Shows what breaks, what tests cover it, and what to check.

## Arguments

- `<function_name>` — the function you're about to edit

## Process

1. Run `cqs impact <function_name> --json` via Bash
2. Run `cqs test-map <function_name> --json` via Bash
3. Run `cqs explain <function_name> --json` via Bash
4. Present results as a checklist

## Output Format

Present this to the user (fill in from the JSON results):

```
## Impact Analysis: <function_name>

**Signature:** <from explain>
**File:** <from explain>
**Callers (<count>):** <list top 10 caller names with files>
**Tests (<count>):** <list test names>
**Risk:** <High if >10 callers, Medium if 3-10, Low if 0-2>

### Before you edit:
- [ ] Understand what callers expect (check the top callers above)
- [ ] Note the existing tests — run them after your change
- [ ] If changing the signature or return type, update all callers

### After you edit:
- [ ] Run: `cargo test --features cuda-index -- <test_names>`
- [ ] If tests fail, check whether your change broke the caller contract
- [ ] If no tests cover the changed behavior, write one
```

## Rules

- If `cqs impact` returns empty results, the function may be dead code or a leaf node — note this
- If `cqs test-map` returns empty, flag as "NO TESTS — write tests before and after editing"
- If `cqs explain` fails (function not indexed), fall back to `cqs "<function_name>" --name-only --json`
- Always run all 3 commands before presenting — don't skip based on partial results
