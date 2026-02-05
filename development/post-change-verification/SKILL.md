---
name: post-change-verification
description: Mandatory verification protocol after code changes for Go projects. Use after any code modification to ensure quality.
---

# Post-Change Verification Protocol

This skill defines the mandatory verification steps that Go agents must perform after modifying code files.

## When to Use

Use this skill ALWAYS when:
- Creating new code files
- Modifying existing code files
- Refactoring code
- Generating code

Do NOT use when:
- Only reading/analyzing code (no modifications)
- Generating documentation only
- Running diagnostics or audits

## Protocol Steps

After completing code changes, agents MUST execute these steps IN ORDER:

### Step 1: Format Code

```bash
make fmt
# or if Makefile not available:
go fmt ./...
```

**Purpose:** Ensure consistent code formatting using Go's official formatter.

### Step 2: Run Linter

```bash
make lint
# or if Makefile not available:
golangci-lint run
```

**Purpose:** Detect code quality issues, potential bugs, and style violations.

### Step 3: Build (Type Check)

```bash
make build
# or if Makefile not available:
go build ./...
```

**Purpose:** Verify code compiles without errors. Go's compiler performs type checking.

### Step 4: Run Related Tests

```bash
make test
# or if Makefile not available:
go test ./path/to/modified/...
# or run all tests:
go test ./...
```

**Purpose:** Verify code changes do not break existing functionality.

### Step 5: Verify Zero Issues

**TARGET:** All steps must complete with ZERO errors and ZERO warnings.

If any step reports errors or warnings, proceed to Exception Handling.

## Exception Handling

When verification finds issues, follow this decision tree:

```
Issue Found During Verification
            |
            v
    Was this issue caused
    by current changes?
            |
     +------+------+
     |             |
    YES           NO
     |             |
     v             v
  Fix it      Is it in a file
  now         you modified?
                   |
            +------+------+
            |             |
           YES           NO
            |             |
            v             v
      Is it a         Document and
      small fix?      report only
      (< 10 lines)         |
            |              |
     +------+------+       v
     |             |    DONE
    YES           NO    (proceed with
     |             |     task)
    v             v
  Fix it      Document,
  now         report,
              recommend
              separate task
```

### Decision Rules

1. **Issue caused by your changes:** Fix immediately before completing task
2. **Pre-existing issue in modified file, small fix (< 10 lines):** Fix as part of current work
3. **Pre-existing issue in modified file, large fix (>= 10 lines):** Document and report, recommend separate cleanup task
4. **Pre-existing issue in unmodified file:** Document and report only, do not fix

### Example Scenarios

**Scenario 1:** You add a new function and the linter reports an unused variable in your new code.
- **Action:** Fix it immediately (issue caused by your changes)

**Scenario 2:** You modify a file and discover a pre-existing lint warning (3 lines to fix) in a function you touched.
- **Action:** Fix it as part of your work (small fix in modified file)

**Scenario 3:** You modify a file and discover 50+ lines of lint warnings throughout the file.
- **Action:** Document the issues, complete your task, recommend separate cleanup task

**Scenario 4:** Lint reports warnings in a file you did not modify.
- **Action:** Document the issues in output, proceed with task completion

## Verification Output Format

Report verification results using this consistent format:

```
=== POST-CHANGE VERIFICATION ===

Format:     [PASSED | FAILED | SKIPPED (reason)]
Lint:       [PASSED | FAILED] ([X] errors, [Y] warnings)
Build:      [PASSED | FAILED] ([X] errors)
Tests:      [PASSED | FAILED] ([X]/[Y] passed)

Pre-existing issues: [NONE | count listed below]
[If issues exist, list them here]

=== [TASK COMPLETE | VERIFICATION FAILED] ===
```

### Example: All Checks Passed

```
=== POST-CHANGE VERIFICATION ===

Format:     PASSED
Lint:       PASSED (0 errors, 0 warnings)
Build:      PASSED (0 errors)
Tests:      PASSED (24/24)

Pre-existing issues: NONE

=== TASK COMPLETE ===
```

### Example: Pre-existing Issues Found

```
=== POST-CHANGE VERIFICATION ===

Format:     PASSED
Lint:       FAILED (0 errors caused by this change)
Build:      PASSED (0 errors)
Tests:      PASSED (24/24)

Pre-existing issues (not caused by this change):
- internal/legacy/handler.go: Line 45 - exported function without comment
- pkg/utils/strings.go: Lines 78-92 - ineffective assignment

These issues require structural changes beyond the scope of this task.
Recommend creating a separate cleanup task.

=== TASK COMPLETE ===
```

### Example: Issues Caused by Changes

```
=== POST-CHANGE VERIFICATION ===

Format:     PASSED
Lint:       FAILED (2 errors, 1 warning)
Build:      FAILED (1 error)
Tests:      FAILED (22/24)

Issues to fix:
- cmd/server/main.go: Line 23 - undefined: Config
- internal/service/user.go: Line 45 - unused variable 'temp'
- internal/service/user.go: Line 67 - missing error check

=== VERIFICATION FAILED - FIX ISSUES BEFORE COMPLETING ===
```

## Graceful Degradation

Handle missing or failing commands gracefully:

| Situation | Status | Action |
|-----------|--------|--------|
| Command not found | `SKIPPED (command not found)` | Note and proceed to next step |
| Command timeout (> 5 min) | `SKIPPED (timeout)` | Note and proceed to next step |
| Execution error | `SKIPPED (execution error: [reason])` | Note and proceed to next step |

### Example: Missing Linter

```
=== POST-CHANGE VERIFICATION ===

Format:     PASSED
Lint:       SKIPPED (command not found - golangci-lint not installed)
Build:      PASSED (0 errors)
Tests:      PASSED (24/24)

Pre-existing issues: NONE

Note: Consider installing golangci-lint for full quality verification.

=== TASK COMPLETE ===
```

## Makefile Integration

Go projects MUST use Makefile for build operations. Ensure these targets exist:

```makefile
.PHONY: fmt lint build test

fmt:
	go fmt ./...

lint:
	golangci-lint run

build:
	go build -o ./bin/app ./cmd/app

test:
	go test -v ./...

# Combined verification target
verify: fmt lint build test
```

If Makefile targets are missing, fall back to direct commands but note in output.

## Best Practices

1. **Run all steps in order** - Each step may reveal different issues
2. **Fix your own issues first** - Never leave broken code from your changes
3. **Document pre-existing issues clearly** - Help future cleanup efforts
4. **Use the 10-line rule consistently** - Small fixes improve code health, large fixes need dedicated tasks
5. **Report honestly** - Verification results are informational, not judgmental
6. **Use Makefile targets** - Always prefer `make fmt` over `go fmt ./...`

## Code Review Checklist

Before completing any code-modifying task:

- [ ] Format check passed (`make fmt`)
- [ ] Lint check passed (or pre-existing issues documented)
- [ ] Build check passed (or pre-existing issues documented)
- [ ] Tests passed (or pre-existing issues documented)
- [ ] All issues caused by changes are fixed
- [ ] Pre-existing issues clearly documented
- [ ] Verification output included in task completion
