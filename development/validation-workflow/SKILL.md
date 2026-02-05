---
name: validation-workflow
description: Use this skill to validate code changes pass all checks (format, lint, build, tests). Runs validation script and iteratively fixes failures. Invoke before finalizing PRs or after making code changes.
---

# Validation Workflow

This skill provides a structured process for validating code changes and fixing any failures.

## When to Use

- After implementing features or fixes
- After addressing code review feedback
- When `/fly` or `/refuel` reaches the validation phase
- When explicitly asked to verify the build passes

## Phase 1: Run Validation

**Send notification:** Run `${CLAUDE_PLUGIN_ROOT}/scripts/notify.sh testing "Running validation"`

Execute the validation script:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/run-validation.sh
```

Parse the JSON results to determine status of each check:
- Format check
- Lint check
- Build
- Tests

## Phase 2: Handle Results

### If All Checks Pass

Report success:
```
Validation Status:
- Format check: ✅ pass
- Lint check: ✅ pass
- Build: ✅ pass
- Tests: ✅ pass (X passed)
```

Proceed to next workflow phase.

### If Any Check Failed

1. **Send notification:** Run `${CLAUDE_PLUGIN_ROOT}/scripts/notify.sh error "Validation failed"`

2. **Parse error output** from failed checks

3. **Create TODO list** of failures

4. **Fix failures in priority order:**
   - Compilation errors (highest priority)
   - Linting errors
   - Test failures
   - Formatting issues (lowest priority)

5. **Fix ALL failures** - even if unrelated to current changes

## Phase 3: Fix Failures

### For Compilation/Lint Errors

Address each error directly based on the error message. Common fixes:
- Missing imports
- Type mismatches
- Unused variables
- Clippy warnings

### For Test Failures

Spawn subagents for each failing test:

```
Fix failing test: [test name]
Error: [error output]
File: [location]

Investigate whether it's a test bug or implementation bug.
Fix the actual issue - do NOT weaken assertions.
```

### For Formatting Issues

```bash
cargo fmt --all
```

## Phase 4: Iterate

After fixing issues:

1. **Re-run validation:**
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/run-validation.sh
   ```

2. **Check results**

3. **If still failing:** Return to Phase 3

4. **Maximum iterations:** 5 attempts before reporting blockers

## Phase 5: Commit Fixes

If any changes were made to fix validation issues:

```bash
git add -A
git commit -m "fix: resolve validation failures

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

## Output

After completing validation, report:

```markdown
## Validation Status

- Format check: ✅/❌ pass/fail
- Lint check: ✅/❌ pass/fail
- Build: ✅/❌ pass/fail
- Tests: ✅/❌ pass/fail (X passed, Y failed)

### Issues Fixed
- [List of issues that were fixed during validation]

### Remaining Blockers (if any)
- [List of issues that could not be resolved after 5 iterations]
```
