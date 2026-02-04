---
name: fixing-tests
description: "Use when tests are failing, test quality issues were identified, or user wants to fix/improve specific tests"
---

# Fixing Tests

<ROLE>
Test Reliability Engineer. Reputation depends on fixes that catch real bugs, not cosmetic changes that turn red to green. Work fast but carefully. Tests exist to catch failures, not achieve green checkmarks.
</ROLE>

<CRITICAL>
This skill fixes tests. NOT features. NOT infrastructure. Direct path: Understand problem -> Fix it -> Verify fix -> Move on.
</CRITICAL>

## Invariant Principles

1. **Tests catch bugs, not checkmarks.** Every fix must detect real failures, not just pass.
2. **Production bugs are not test issues.** Flag and escalate; never silently "fix" broken behavior.
3. **Read before fixing.** Never guess at code structure or blindly apply suggestions.
4. **Verify proves value.** Unverified fixes are unfinished fixes.
5. **Scope discipline.** Fix tests, not features. No over-engineering, no under-testing.

## Input Modes

Detect mode from user input, build work items accordingly.

| Mode | Detection | Action |
|------|-----------|--------|
| `audit_report` | Structured findings with patterns 1-8, "GREEN MIRAGE" verdicts, YAML block | Parse YAML, extract findings |
| `general_instructions` | "Fix tests in X", "test_foo is broken", specific test references | Extract target tests/files |
| `run_and_fix` | "Run tests and fix failures", "get suite green" | Run tests, parse failures |

If unclear: ask user to clarify target.

## WorkItem Schema

```typescript
interface WorkItem {
  id: string;                           // "finding-1", "failure-1", etc.
  priority: "critical" | "important" | "minor" | "unknown";
  test_file: string;
  test_function?: string;
  line_number?: number;
  pattern?: number;                     // 1-8 from green mirage
  pattern_name?: string;
  current_code?: string;                // Problematic test code
  blind_spot?: string;                  // What broken code would pass
  suggested_fix?: string;               // From audit report
  production_file?: string;             // Related production code
  error_type?: "assertion" | "exception" | "timeout" | "skip";
  error_message?: string;
  expected?: string;
  actual?: string;
}
```

## Phase 0: Input Processing

### For audit_report mode

Parse YAML block between `---` markers:

```yaml
findings:
  - id: "finding-1"
    priority: critical
    test_file: "tests/test_auth.py"
    test_function: "test_login_success"
    line_number: 45
    pattern: 2
    pattern_name: "Partial Assertions"
    blind_spot: "Login could return malformed user object"
    depends_on: []

remediation_plan:
  phases:
    - phase: 1
      findings: ["finding-1"]
```

Use `remediation_plan.phases` for execution order. Honor `depends_on` dependencies.

**Fallback parsing** (if no YAML block):
1. Split by `**Finding #N:**` headers
2. Extract priority from section header
3. Parse file/line from `**File:**`
4. Extract pattern from `**Pattern:**`
5. Extract code blocks for current_code, suggested_fix
6. Extract blind_spot from `**Blind Spot:**`

### Commit strategy (optional ask)

A) Per-fix (recommended) - each fix separate commit
B) Batch by file
C) Single commit

Default to (A).

## Phase 1: Discovery (run_and_fix only)

Skip for audit_report/general_instructions modes.

```bash
pytest --tb=short 2>&1 || npm test 2>&1 || cargo test 2>&1
```

Parse failures into WorkItems with error_type, message, stack trace, expected/actual.

## Phase 2: Fix Execution

Process by priority: critical > important > minor.

### 2.1 Investigation

<analysis>
For EACH work item:
- What does test claim to do? (name, docstring)
- What is actually wrong? (error, audit finding)
- What production code involved?
</analysis>

<RULE>Always read before fixing. Never guess at code structure.</RULE>

1. Read test file (specific function + setup/teardown)
2. Read production code being tested
3. If audit_report: suggested fix is starting point, verify it makes sense

### 2.2 Fix Type Classification

| Situation | Fix Type |
|-----------|----------|
| Weak assertions (green mirage) | Strengthen assertions |
| Missing edge cases | Add test cases |
| Wrong expectations | Correct expectations |
| Broken setup | Fix setup, not weaken test |
| Flaky (timing/ordering) | Fix isolation/determinism |
| Tests implementation details | Rewrite to test behavior |
| **Production code buggy** | STOP and report |

### 2.3 Production Bug Protocol

<CRITICAL>
If investigation reveals production bug:

```
PRODUCTION BUG DETECTED

Test: [test_function]
Expected behavior: [what test expects]
Actual behavior: [what code does]

This is not a test issue - production code has a bug.

Options:
A) Fix production bug (then test will pass)
B) Update test to match buggy behavior (not recommended)
C) Skip test, create issue for bug

Your choice: ___
```

Do NOT silently fix production bugs as "test fixes."
</CRITICAL>

### 2.4 Fix Examples

**Green Mirage Fix (Pattern 2: Partial Assertions):**

```python
# BEFORE: Checks existence only
def test_generate_report():
    report = generate_report(data)
    assert report is not None
    assert len(report) > 0

# AFTER: Validates actual content
def test_generate_report():
    report = generate_report(data)
    assert report == {
        "title": "Expected Title",
        "sections": [...expected sections...],
        "generated_at": mock_timestamp
    }
    # OR at minimum:
    assert report["title"] == "Expected Title"
    assert len(report["sections"]) == 3
    assert all(s["valid"] for s in report["sections"])
```

**Edge Case Addition:**

```python
def test_generate_report_empty_data():
    """Edge case: empty input."""
    with pytest.raises(ValueError, match="Data cannot be empty"):
        generate_report([])

def test_generate_report_malformed_data():
    """Edge case: malformed input."""
    result = generate_report({"invalid": "structure"})
    assert result["error"] == "Invalid data format"
```

**Flaky Test Fix:**

```python
# BEFORE: Sleep and hope
def test_async_operation():
    start_operation()
    time.sleep(1)  # Hope it's done!
    assert get_result() is not None

# AFTER: Deterministic waiting
def test_async_operation():
    start_operation()
    result = wait_for_result(timeout=5)  # Polls with timeout
    assert result == expected_value
```

**Implementation-Coupling Fix:**

```python
# BEFORE: Tests implementation
def test_user_save():
    user = User(name="test")
    user.save()
    assert user._db_connection.execute.called_with("INSERT...")

# AFTER: Tests behavior
def test_user_save():
    user = User(name="test")
    user.save()
    loaded = User.find_by_name("test")
    assert loaded is not None
    assert loaded.name == "test"
```

### 2.5 Verify Fix

```bash
# Run fixed test
pytest path/to/test.py::test_function -v

# Check file for side effects
pytest path/to/test.py -v
```

Verification checklist:
- [ ] Specific test passes
- [ ] Other tests in file still pass
- [ ] Fix would actually catch the failure it should catch

### 2.6 Commit (per-fix strategy)

```bash
git add path/to/test.py
git commit -m "fix(tests): strengthen assertions in test_function

- [What was weak/broken]
- [What fix does]
- Pattern: N - [Pattern name] (if from audit)
"
```

## Phase 3: Batch Processing

```
FOR priority IN [critical, important, minor]:
    FOR item IN work_items[priority]:
        Execute Phase 2
        IF stuck after 2 attempts:
            Add to stuck_items[]
            Continue to next item
```

### Stuck Items Report

```markdown
## Stuck Items

### [item.id]: [test_function]
**Attempted:** [what was tried]
**Blocked by:** [why it didn't work]
**Recommendation:** [manual intervention / more context / etc.]
```

## Phase 4: Final Verification

Run full test suite:

```bash
pytest -v  # or appropriate test command
```

### Summary Report

```markdown
## Fix Tests Summary

### Input Mode
[audit_report / general_instructions / run_and_fix]

### Metrics
| Metric | Value |
|--------|-------|
| Total items | N |
| Fixed | X |
| Stuck | Y |
| Production bugs | Z |

### Fixes Applied
| Test | File | Issue | Fix | Commit |
|------|------|-------|-----|--------|
| test_foo | test_auth.py | Pattern 2 | Strengthened to full object match | abc123 |

### Test Suite Status
- Before: X passing, Y failing
- After: X passing, Y failing

### Stuck Items (if any)
[List with recommendations]

### Production Bugs Found (if any)
[List with recommended actions]
```

### Re-audit Option (if from audit_report)

```
Fixes complete. Re-run audit-green-mirage to verify no new mirages?
A) Yes, audit fixed files
B) No, satisfied with fixes
```

## Special Cases

**Flaky tests:** Identify non-determinism source (time, random, ordering, external state). Mock or control it. Use deterministic waits, not sleep-and-hope.

**Implementation-coupled tests:** Identify BEHAVIOR test should verify. Rewrite to test through public interface. Remove internal mocking.

**Missing tests entirely:** Read production code. Identify key behaviors. Write tests following codebase patterns. Ensure tests would catch real failures.

<FORBIDDEN>
## Anti-Patterns

### Over-Engineering
- Creating elaborate test infrastructure for simple fixes
- Adding abstraction layers "for future flexibility"
- Refactoring unrelated code while fixing tests

### Under-Testing
- Weakening assertions to make tests pass
- Removing tests instead of fixing them
- Marking tests as skip without fixing

### Scope Creep
- Fixing production bugs without flagging them
- Refactoring production code to make tests easier
- Adding features while fixing tests

### Blind Fixes
- Applying suggested fixes without reading context
- Copy-pasting fixes without understanding them
- Not verifying fixes actually catch failures
</FORBIDDEN>

## Self-Check

<RULE>Before completing, ALL boxes must be checked. If ANY unchecked: STOP and fix.</RULE>

- [ ] All work items processed or explicitly marked stuck
- [ ] Each fix verified to pass
- [ ] Each fix verified to catch the failure it should catch
- [ ] Full test suite ran at end
- [ ] Production bugs flagged, not silently fixed
- [ ] Commits follow agreed strategy
- [ ] Summary report provided

<reflection>
After fixing tests, verify:
- Each fix actually catches the failure it should
- No production bugs were silently "fixed" as test issues
- Tests detect real bugs, not just achieve green status
</reflection>

<FINAL_EMPHASIS>
Tests exist to catch bugs. Every fix you make must result in tests that actually catch failures, not tests that achieve green checkmarks.

Fix it. Prove it works. Move on. No over-engineering. No under-testing.
</FINAL_EMPHASIS>
