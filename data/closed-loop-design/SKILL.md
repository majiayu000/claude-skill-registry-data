---
name: closed-loop-design
description: Design closed-loop prompts with Request-Validate-Resolve structure for reliable agentic workflows. Use when creating self-validating agents, adding feedback loops, or improving agent reliability through verification.
allowed-tools: Read, Grep, Glob
---

# Closed Loop Design Skill

Guide for designing closed-loop prompts that ensure agent reliability through feedback loops.

## When to Use

- Designing new agentic workflows
- Adding validation to existing processes
- Creating self-correcting agent pipelines
- Building automated test-fix cycles

## Core Concept

Every agentic operation should follow the Request-Validate-Resolve pattern:

```text
REQUEST → VALIDATE → RESOLVE
    ↑                    ↓
    └────────────────────┘
```

## Design Workflow

### Step 1: Identify the Operation

What task needs to be validated?

- Code changes (feature, bug fix, refactor)
- File operations (create, modify, delete)
- External interactions (API calls, database queries)
- Build/deploy operations

### Step 2: Define Validation Mechanism

How do we know if it succeeded?

| Operation Type | Validation Mechanism |
| --- | --- |
| Code changes | Run tests, type check, lint |
| File operations | Verify file exists, check content |
| API interactions | Check response status, validate data |
| Build operations | Build succeeds, no errors |

### Step 3: Design the Resolve Path

What happens on failure?

1. **Analyze**: Parse error output to understand failure
2. **Fix**: Make minimal, targeted corrections
3. **Re-validate**: Run validation again
4. **Limit retries**: Set maximum attempts (typically 3-5)

### Step 4: Create the Prompt Structure

Template:

```markdown
## Closed Loop: [Operation Name]

### Request
[Clear task description with success criteria]

### Validate
- Command: `[validation command]`
- Success: [what success looks like]
- Failure: [what failure looks like]

### Resolve (if validation fails)
1. Analyze the failure output
2. Identify root cause
3. Apply minimal fix
4. Return to Validate step
5. Maximum 3 retry attempts
```

## Example: Test-Fix Loop

```markdown
## Closed Loop: Implement Feature

### Request
Implement the user login feature according to spec.

### Validate
- Command: `pytest tests/test_auth.py -v`
- Success: All tests pass (exit code 0)
- Failure: One or more tests fail

### Resolve
1. Read failing test output
2. Identify which test failed and why
3. Fix the implementation (not the test)
4. Re-run pytest
5. Maximum 3 retry attempts
```

## Common Closed Loop Patterns

### Code Quality Loop

```text
REQUEST: Write/modify code
VALIDATE: Lint + Type check + Tests
RESOLVE: Fix errors iteratively
```

### Build Verification Loop

```text
REQUEST: Make changes
VALIDATE: Full build succeeds
RESOLVE: Fix build errors
```

### E2E Validation Loop

```text
REQUEST: Implement user flow
VALIDATE: E2E test passes
RESOLVE: Fix failing steps
```

## Best Practices

1. **Start with tests**: If tests do not exist, consider adding them first
2. **Fast validation first**: Run quick checks before slow ones
3. **Structured output**: Use JSON for machine-parseable results
4. **Clear failure messages**: Include context for resolution
5. **Bounded retries**: Prevent infinite loops

## Memory References

- @closed-loop-anatomy.md - Full pattern documentation
- @test-leverage-point.md - Why tests are ideal validators
- @validation-commands.md - Validation command patterns

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
