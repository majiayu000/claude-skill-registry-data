---
name: baseline-check
description: Autonomously run quality checks (RuboCop, RSpec) to establish baseline or detect regressions. Triggers before starting development work, after completing changes, when checking code quality, or when explicitly requested. Compares current metrics against previous baseline to identify improvements or regressions in code quality and test coverage.
allowed-tools: Bash, Read, Write, Glob
---

# Baseline Check Skill

## Purpose

This skill maintains code quality throughout development by:
- Establishing baseline quality metrics before development
- Detecting regressions after code changes
- Tracking quality trends over time
- Providing clear feedback on code health

## When to Use

Invoke this skill:

1. **Before starting development work** - Establish current baseline
2. **After completing changes** - Check for regressions
3. **After GREEN phase** - Verify tests exist and pass
4. **After REFACTOR phase** - Verify tests still pass after refactoring
5. **Before committing code** - Verify quality standards
6. **When explicitly requested** - User asks for quality check, baseline, or regression analysis
7. **During code review** - Validate changes meet quality bar

## How to Execute

### Step 1: Run the Baseline Check

Execute the wrapper script (from project root):

```bash
./.claude/skills/baseline-check/baseline-check.sh
```

The script will:
- Run RuboCop (if available)
- Run RSpec (if available)
- Generate a timestamped JSON report
- Output the filepath to the generated report

**Expected output:**
```
Running baseline checks...
✓ RuboCop check completed
✓ RSpec check completed
Baseline saved to: .claude/baseline/main-20251117-084523.json
```

**Error handling:**
- If script fails, report the error to user
- If tools are unavailable, the JSON will reflect `"available": false`
- Empty test suite is acceptable (allows pre-implementation baselines)

### Step 2: Read the Results

Parse the generated JSON file to extract metrics:

```json
{
  "timestamp": "2025-11-17T08:45:23Z",
  "branch": "main",
  "commit": "168d4ea",
  "checks": {
    "rubocop": {
      "available": true,
      "status": "passed",
      "files_inspected": 15,
      "offenses": 3,
      "offenses_by_severity": {
        "convention": 2,
        "warning": 1,
        "error": 0,
        "fatal": 0
      },
      "execution_time": 1.45
    },
    "rspec": {
      "available": true,
      "status": "passed",
      "examples": 42,
      "failures": 0,
      "pending": 2,
      "execution_time": 3.21
    }
  },
  "overall_status": "passed",
  "summary": "All checks passed"
}
```

### Step 3: Find Previous Baseline (If Any)

Search for previous baselines on the current branch:

```bash
ls -t .claude/baseline/{current-branch}-*.json 2>/dev/null | head -2
```

This returns the two most recent baseline files (including the one just created).

**Scenarios:**
- **One file returned**: This is the first baseline (nothing to compare)
- **Two files returned**: Compare the newest against the previous
- **Zero files returned**: This should not happen if Step 1 succeeded

### Step 4: Compare Baselines

If a previous baseline exists, compare key metrics:

#### RuboCop Comparison

| Metric | Check |
|--------|-------|
| Total offenses | `current.offenses` vs `previous.offenses` |
| Convention offenses | `current.offenses_by_severity.convention` vs `previous` |
| Warning offenses | `current.offenses_by_severity.warning` vs `previous` |
| Error offenses | `current.offenses_by_severity.error` vs `previous` |
| Fatal offenses | `current.offenses_by_severity.fatal` vs `previous` |
| Files inspected | `current.files_inspected` vs `previous.files_inspected` |

**Classifications:**
- **Improvement**: Offenses decreased, files inspected increased
- **Regression**: Offenses increased (especially errors/fatals)
- **Stable**: No change in offense counts

#### RSpec Comparison

| Metric | Check |
|--------|-------|
| Test count | `current.examples` vs `previous.examples` |
| Failures | `current.failures` vs `previous.failures` |
| Pending tests | `current.pending` vs `previous.pending` |

**Classifications:**
- **Improvement**: More tests, fewer failures, fewer pending
- **Regression**: New failures introduced, test count decreased
- **Stable**: Metrics unchanged or expected changes (e.g., pending tests fixed)

### Step 5: Report Findings

Provide a clear, actionable summary.

#### Report Format: First Baseline

When no previous baseline exists:

```
Baseline Quality Check - Initial Assessment
==========================================

Branch: main
Commit: 168d4ea
Timestamp: 2025-11-17T08:45:23Z

RuboCop Analysis:
  Status: passed
  Files Inspected: 15
  Total Offenses: 3
    - Convention: 2
    - Warning: 1
    - Error: 0
    - Fatal: 0

RSpec Analysis:
  Status: passed
  Examples: 42
  Failures: 0
  Pending: 2

Overall Status: PASSED ✓

This is the first baseline for this branch. Future checks will compare against these metrics.

Baseline file: .claude/baseline/main-20251117-084523.json
```

#### Report Format: Comparison with Previous Baseline

When comparing against previous baseline:

```
Baseline Quality Check - Regression Analysis
============================================

Branch: feat/ssh-integration
Commit: abc123d
Timestamp: 2025-11-17T09:15:42Z
Previous: 2025-11-17T08:45:23Z

RuboCop Changes:
  Status: passed → passed
  Files Inspected: 15 → 18 (+3)
  Total Offenses: 3 → 5 (+2) ⚠️ REGRESSION
    - Convention: 2 → 3 (+1)
    - Warning: 1 → 2 (+1)
    - Error: 0 → 0 (stable)
    - Fatal: 0 → 0 (stable)

RSpec Changes:
  Status: passed → passed
  Examples: 42 → 48 (+6) ✓ IMPROVEMENT
  Failures: 0 → 0 (stable)
  Pending: 2 → 1 (-1) ✓ IMPROVEMENT

Overall Status: PASSED (with quality regressions)

FINDINGS:
⚠️  2 new RuboCop offenses introduced
✓  6 new tests added
✓  1 pending test resolved

RECOMMENDATION:
Address the new RuboCop offenses before committing. Run 'bundle exec rubocop' for details.

Baseline file: .claude/baseline/feat-ssh-integration-20251117-091542.json
Previous baseline: .claude/baseline/feat-ssh-integration-20251117-084523.json
```

#### Report Format: Critical Regression

When significant regressions occur:

```
Baseline Quality Check - CRITICAL REGRESSIONS DETECTED
======================================================

Branch: feat/provider-class
Commit: def456e
Timestamp: 2025-11-17T10:30:15Z

⚠️  CRITICAL ISSUES DETECTED ⚠️

RuboCop Changes:
  Status: passed → FAILED ❌
  Total Offenses: 3 → 12 (+9) ❌ CRITICAL REGRESSION
    - Error: 0 → 2 (+2) ❌ NEW ERRORS
    - Fatal: 0 → 1 (+1) ❌ NEW FATAL

RSpec Changes:
  Status: passed → FAILED ❌
  Examples: 42 → 42 (stable)
  Failures: 0 → 3 (+3) ❌ NEW FAILURES

Overall Status: FAILED ❌

CRITICAL FINDINGS:
❌ 1 fatal RuboCop offense (code will not run correctly)
❌ 2 error-level RuboCop offenses (serious code issues)
❌ 3 failing tests (broken functionality)

REQUIRED ACTIONS:
1. Run 'bundle exec rubocop' to see fatal/error details
2. Run 'bundle exec rspec' to see test failures
3. Fix all critical issues before proceeding
4. Re-run baseline check to verify fixes

DO NOT COMMIT until these critical issues are resolved.

Baseline file: .claude/baseline/feat-provider-class-20251117-103015.json
```

## Interpretation Guidelines

### Status Indicators

Use these indicators in reports:
- ✓ `IMPROVEMENT` - Metrics got better
- ⚠️ `REGRESSION` - Metrics got worse (non-critical)
- ❌ `CRITICAL REGRESSION` - Serious issues (errors, fatals, test failures)
- `(stable)` - No change
- `PASSED` - All checks passed
- `FAILED` - One or more checks failed

### Severity Assessment

**Critical (❌):**
- RuboCop fatal offenses
- RuboCop error offenses
- RSpec test failures
- Overall status changed to "failed"

**Warning (⚠️):**
- Increased convention offenses
- Increased warning offenses
- Decreased test count
- Increased pending tests

**Positive (✓):**
- Decreased offenses
- Increased test count
- Decreased pending tests
- Resolved failures

### Recommendations

Based on findings, provide actionable guidance:

**No regressions:**
- "Quality baseline looks good. Proceed with confidence."

**Minor regressions:**
- "Consider addressing new offenses before committing."
- "Run 'bundle exec rubocop -a' to auto-fix some issues."

**Critical regressions:**
- "DO NOT COMMIT until critical issues are resolved."
- "Run diagnostic commands to investigate failures."
- "Re-run baseline check after fixes to verify."

## Edge Cases

### No Tools Available

If both RuboCop and RSpec are unavailable:

```
Baseline Quality Check - Tools Not Available
============================================

Neither RuboCop nor RSpec are available in this environment.

To enable quality checks:
1. Run 'bundle install' to install dependencies
2. Ensure RuboCop and RSpec gems are in Gemfile
3. Re-run this baseline check

Baseline file: .claude/baseline/main-20251117-084523.json
```

### Empty Test Suite

If no tests exist yet (pre-implementation):

```
Baseline Quality Check - Pre-Implementation
===========================================

RuboCop: passed (3 files inspected, 0 offenses)
RSpec: No tests exist yet

This appears to be a pre-implementation baseline. As you add tests,
future checks will track test coverage growth.

Baseline file: .claude/baseline/feat-new-feature-20251117-084523.json
```

### Branch Comparison

If comparing across branches (e.g., feature branch vs main):

```
Note: Previous baseline is from a different branch or significantly
older commit. Comparison may include expected differences from other work.
```

## TDD Integration

baseline-check plays a critical role in TDD workflow:

**During GREEN Phase**:
- Verify tests exist for new implementation
- Confirm tests are passing
- Measure test coverage increase
- Flag if implementation has no corresponding tests

**During REFACTOR Phase**:
- Confirm all tests still pass after refactoring
- Verify no test coverage regression
- Compare before/after refactor metrics

**Quality Gate**:
- No implementation accepted without tests
- Test count should increase with new features
- Test pass rate should remain 100%

## Best Practices

1. **Run before starting work** - Establishes clean baseline
2. **Run after each significant change** - Catches issues early
3. **Run after GREEN phase** - Verify tests exist and pass
4. **Run after REFACTOR phase** - Confirm tests still pass
5. **Don't ignore warnings** - Small regressions accumulate
6. **Celebrate improvements** - Acknowledge quality improvements
7. **Block on critical issues** - Never commit with fatals/errors/failures

## Technical Notes

- Baseline files are timestamped: `{branch}-{YYYYMMDD-HHMMSS}.json`
- Files are stored in `.claude/baseline/` (gitignored)
- Script exits 0 even if checks fail (allows baseline capture)
- Execution times are informational only (don't compare)
- Branch name is sanitized (slashes replaced with dashes)

## Example Workflow

**Starting new feature:**
```
1. User: "I want to add SSH support"
2. Claude: Runs baseline-check skill → establishes baseline
3. Claude: Reports current state (e.g., "15 files, 0 offenses, 42 passing tests")
4. Claude: Proceeds with implementation
5. Claude: After implementation, runs baseline-check again
6. Claude: Compares results, reports findings
7. Claude: If regressions, recommends fixes before commit
```

## Output Files

The skill reads but does not create files (wrapper script creates them):
- Input: `.claude/baseline/{branch}-{timestamp}.json`
- Format: See Step 2 for JSON structure

## Success Criteria

The skill succeeds when it:
- Executes the wrapper script without errors
- Reads and parses the JSON results
- Compares against previous baseline (if available)
- Provides clear, actionable report
- Highlights any regressions prominently
- Guides next steps based on findings

The skill fails when:
- Wrapper script cannot be executed
- JSON file cannot be read or parsed
- Report is unclear or incomplete
