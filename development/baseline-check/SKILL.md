---
name: baseline-check
description: Autonomously run quality checks (detekt, Gradle tests) to establish baseline or detect regressions. Supports three modes (capture, compare, auto) for comprehensive regression detection. Triggers before starting development work, after completing changes, when checking code quality, or when explicitly requested. Compares current metrics against previous baseline to identify improvements or regressions in code quality and test coverage.
allowed-tools: Bash, Read, Write, Glob
---

# Baseline Check Skill

## Purpose

This skill maintains code quality throughout development by:
- Establishing baseline quality metrics before development
- Detecting regressions after code changes with automated delta analysis
- Tracking quality trends over time
- Providing clear, actionable feedback on code health with visual indicators

## When to Use

Invoke this skill:

1. **Before starting development work** - Establish current baseline (capture mode)
2. **After completing changes** - Check for regressions (compare or auto mode)
3. **After GREEN phase** - Verify tests exist and pass
4. **After REFACTOR phase** - Verify tests still pass after refactoring
5. **Before committing code** - Verify quality standards (compare mode)
6. **When explicitly requested** - User asks for quality check, baseline, or regression analysis
7. **During code review** - Validate changes meet quality bar

## Execution Modes

The skill supports three execution modes for different scenarios:

### Mode 1: Capture (Default)
**Purpose**: Establish a quality baseline

**When to use:**
- Starting new development work
- After syncing with main branch
- Before making changes
- Creating a reference point for later comparison

**Command:**
```bash
./.claude/skills/baseline-check/baseline-check.sh --capture [--issue SPI-XXX]
```

**What it does:**
- Runs `./gradlew clean check --rerun-tasks` (comprehensive, cache-proof execution)
- Captures test metrics (total, passed, failed, skipped)
- Captures detekt metrics (offenses by severity)
- Stores JSON + log file in `.claude/baseline/`
- Creates latest symlink for easy access

**Output:**
- JSON file: `.claude/baseline/{branch}-{timestamp}.json`
- Log file: `.claude/baseline/{branch}-{timestamp}.log`
- Symlink: `.claude/baseline/latest-{branch}.json`

### Mode 2: Compare
**Purpose**: Compare current state against a specific baseline

**When to use:**
- After completing implementation
- Before creating a pull request
- Verifying no regressions introduced
- Explicit regression check requested

**Command:**
```bash
# Auto-detect latest baseline for current branch
./.claude/skills/baseline-check/baseline-check.sh --compare

# Compare against specific baseline file
./.claude/skills/baseline-check/baseline-check.sh --compare .claude/baseline/main-20241120-100000.json
```

**What it does:**
- Runs comprehensive tests (fresh execution)
- Auto-detects latest baseline if not specified
- Calculates deltas (total, passed, failed, skipped)
- Classifies changes (new tests, fixed tests, regressions)
- Generates visual comparison report with interpretation
- Returns exit code 1 if regressions detected

**Output:**
```
═══════════════════════════════════════════════════════════
  BASELINE vs CURRENT COMPARISON
═══════════════════════════════════════════════════════════

BASELINE:
  • Total: 861 | Passed: 861 | Failed: 0 | Skipped: 0

CURRENT:
  • Total: 873 | Passed: 868 | Failed: 5 | Skipped: 0

DELTA (Current - Baseline):
  • Total: +12 | Passed: +7 | Failed: +5 | Skipped: 0

───────────────────────────────────────────────────────────
  INTERPRETATION
───────────────────────────────────────────────────────────
  ✅ 12 new tests added
  ❌ 5 NEW test failures introduced
     📋 Analyze if failures are:
        - Expected (testing edge cases, deprecated endpoints)
        - Bugs requiring fixes
        - Pre-existing issues incorrectly attributed

═══════════════════════════════════════════════════════════
```

### Mode 3: Auto (Autonomous)
**Purpose**: Capture baseline and automatically compare if previous exists

**When to use:**
- Continuous quality monitoring
- Agent-driven autonomous checks
- When unsure if baseline exists
- Workflow automation

**Command:**
```bash
./.claude/skills/baseline-check/baseline-check.sh --auto [--issue SPI-XXX]
```

**What it does:**
1. Captures current baseline (same as capture mode)
2. Checks if previous baseline exists for this branch
3. If found, automatically performs comparison
4. Reports both baseline capture and comparison results
5. Returns exit code 1 if regressions detected

**Decision logic:**
- **First run on branch**: Only captures baseline, no comparison
- **Subsequent runs**: Captures baseline AND compares against previous

## Command-Line Reference

```bash
# Capture baseline (default mode)
./.claude/skills/baseline-check/baseline-check.sh
./.claude/skills/baseline-check/baseline-check.sh --capture
./.claude/skills/baseline-check/baseline-check.sh --capture --issue SPI-866

# Compare against baseline
./.claude/skills/baseline-check/baseline-check.sh --compare
./.claude/skills/baseline-check/baseline-check.sh --compare .claude/baseline/main-20241120-100000.json

# Autonomous mode (capture + optional compare)
./.claude/skills/baseline-check/baseline-check.sh --auto
./.claude/skills/baseline-check/baseline-check.sh --auto --issue SPI-866

# Adjust timeout (default: 300 seconds)
./.claude/skills/baseline-check/baseline-check.sh --capture --timeout 600

# Show help
./.claude/skills/baseline-check/baseline-check.sh --help
```

## JSON Output Format

The skill generates structured JSON for programmatic access:

```json
{
  "timestamp": "2025-11-20T14:30:22Z",
  "branch": "feat/spi-866-baseline-enhancement",
  "commit": "abc123d",
  "issue_id": "SPI-866",
  "checks": {
    "detekt": {
      "available": true,
      "status": "passed",
      "total_offenses": 5,
      "offenses_by_severity": {
        "convention": 2,
        "warning": 3,
        "error": 0
      },
      "execution_time": 8
    },
    "tests": {
      "available": true,
      "status": "passed",
      "total": 873,
      "passed": 873,
      "failures": 0,
      "skipped": 0,
      "execution_time": 145
    }
  },
  "overall_status": "passed",
  "summary": "All quality checks passed"
}
```

## File Storage Structure

```
.claude/baseline/
├── main-20241120-100000.json          # Metrics JSON
├── main-20241120-100000.log           # Full console log
├── main-20241120-110000.json          # Later baseline
├── main-20241120-110000.log           # Later log
├── latest-main.json -> main-20241120-110000.json  # Symlink to latest
├── feat-spi-866-20241120-120000.json  # Feature branch baseline
├── feat-spi-866-20241120-120000.log   # Feature branch log
└── latest-feat-spi-866.json           # Feature branch latest symlink
```

**Key features:**
- **Dual storage**: JSON (metrics) + log (full output)
- **Timestamped**: Sortable, preserves history
- **Issue-based naming**: Optional `--issue` flag for Linear integration
- **Latest symlinks**: Easy access to most recent baseline per branch

## Interpretation Guidelines

### Visual Indicators

The skill uses these indicators in comparison reports:

- ✅ **Improvements** - Metrics got better (tests fixed, offenses reduced)
- ⚠️ **Changes** - Neutral changes (tests removed, skipped tests changed)
- ❌ **Regressions** - Serious issues (new failures, error offenses)
- **Stable** - No change in metrics

### Delta Classifications

**New Tests Added** (Positive):
- `Delta Total > 0` indicates new test coverage

**Tests Fixed** (Positive):
- `Delta Failures < 0` indicates previously failing tests now pass

**Regressions** (Critical):
- `Delta Failures > 0` indicates NEW test failures introduced
- Script exits with code 1 (blocks commit)

**Tests Removed** (Warning):
- `Delta Total < 0` may indicate deleted tests (review needed)

### Regression Analysis

When regressions are detected, the report provides:

1. **Clear identification**: "❌ 5 NEW test failures introduced"
2. **Classification guidance**: Expected vs bugs vs misattribution
3. **Actionable next steps**: Review logs, fix failures, re-run check
4. **Exit code 1**: Signals failure for CI/CD integration

## Workflow Examples

### Example 1: Starting New Feature (Capture Mode)

```bash
# Agent invokes before starting work
./.claude/skills/baseline-check/baseline-check.sh --capture --issue SPI-866

# Output shows baseline established
# Agent proceeds with implementation
# After implementation, agent runs compare mode
```

**Agent prompt:**
```
Before starting SPI-866, I'll establish a quality baseline to track regressions.

Running baseline check...

✓ Baseline captured: 861/861 tests passing, 5 detekt offenses
✓ Saved to: .claude/baseline/main-20241120-140000.json

Proceeding with implementation...
```

### Example 2: Post-Implementation Check (Compare Mode)

```bash
# Agent invokes after completing work
./.claude/skills/baseline-check/baseline-check.sh --compare

# Output shows delta analysis
# Agent reports findings to user
```

**Agent prompt:**
```
Implementation complete. Running regression check against baseline...

═══════════════════════════════════════════════════════════
  BASELINE vs CURRENT COMPARISON
═══════════════════════════════════════════════════════════

BASELINE:
  • Total: 861 | Passed: 861 | Failed: 0 | Skipped: 0

CURRENT:
  • Total: 873 | Passed: 873 | Failed: 0 | Skipped: 0

DELTA (Current - Baseline):
  • Total: +12 | Passed: +12 | Failed: 0 | Skipped: 0

───────────────────────────────────────────────────────────
  INTERPRETATION
───────────────────────────────────────────────────────────
  ✅ 12 new tests added

═══════════════════════════════════════════════════════════

✓ No regressions detected
✓ Quality improved: 12 new tests for new functionality
✓ Ready for code review
```

### Example 3: Autonomous Monitoring (Auto Mode)

```bash
# Agent uses auto mode for continuous monitoring
./.claude/skills/baseline-check/baseline-check.sh --auto

# First run: only captures
# Subsequent runs: captures + compares
```

**Agent prompt (first run):**
```
Running autonomous quality check...

✓ Baseline captured: 861/861 tests passing
ℹ️  No previous baseline for comparison (first run on this branch)

Baseline established for future comparisons.
```

**Agent prompt (subsequent run):**
```
Running autonomous quality check...

✓ Current: 873/873 tests passing
✓ Previous baseline detected, performing comparison...

  ✅ 12 new tests added
  ✅ No regressions detected

Quality maintained!
```

### Example 4: Regression Detected (Compare Mode)

```bash
# After changes, comparison detects regressions
./.claude/skills/baseline-check/baseline-check.sh --compare
```

**Agent prompt:**
```
Running regression check...

═══════════════════════════════════════════════════════════
  BASELINE vs CURRENT COMPARISON
═══════════════════════════════════════════════════════════

BASELINE:
  • Total: 873 | Passed: 873 | Failed: 0 | Skipped: 0

CURRENT:
  • Total: 885 | Passed: 880 | Failed: 5 | Skipped: 0

DELTA (Current - Baseline):
  • Total: +12 | Passed: +7 | Failed: +5 | Skipped: 0

───────────────────────────────────────────────────────────
  INTERPRETATION
───────────────────────────────────────────────────────────
  ✅ 12 new tests added
  ❌ 5 NEW test failures introduced
     📋 Analyze if failures are:
        - Expected (testing edge cases, deprecated endpoints)
        - Bugs requiring fixes
        - Pre-existing issues incorrectly attributed

═══════════════════════════════════════════════════════════

⚠️  REGRESSIONS DETECTED

I've detected 5 new test failures. Let me analyze the failure logs...

[Agent reviews .claude/baseline/*.log file]

The failures are in SessionManagerTest. These appear to be legitimate bugs
introduced by the recent changes. I recommend:

1. Review the failing tests in the log file
2. Fix the SessionManager implementation
3. Re-run baseline check to verify fixes

Should I help investigate the failures?
```

## TDD Integration

baseline-check plays a critical role in TDD workflow:

**During GREEN Phase:**
- Verify tests exist for new implementation
- Confirm tests are passing
- Measure test coverage increase
- Flag if implementation has no corresponding tests

**During REFACTOR Phase:**
- Confirm all tests still pass after refactoring
- Verify no test coverage regression
- Compare before/after refactor metrics

**Quality Gate:**
- No implementation accepted without tests
- Test count should increase with new features
- Test pass rate should remain 100%
- No detekt errors allowed

## Best Practices

1. **Always capture before starting work** - Clean baseline prevents confusion
2. **Use auto mode for continuous monitoring** - Simplifies workflow
3. **Compare before creating PRs** - Catch regressions early
4. **Review logs when failures occur** - Full console output preserved
5. **Use issue-based naming for Linear integration** - `--issue SPI-XXX`
6. **Don't ignore regressions** - Exit code 1 should block commits
7. **Leverage symlinks for quick access** - `latest-{branch}.json`

## Technical Notes

- **Comprehensive execution**: Uses `./gradlew clean check --rerun-tasks`
- **Cache-proof**: `--rerun-tasks` forces fresh execution, no FROM-CACHE false positives
- **Cross-platform**: Works on macOS and Linux
- **Dual parsing**: Console output (primary) + XML (fallback)
- **Timeout support**: Default 300s, adjustable with `--timeout`
- **Exit codes**: 0 = success, 1 = failures/regressions, 2 = script error
- **Storage**: `.claude/baseline/` (should be in `.gitignore`)

## Success Criteria

The skill succeeds when it:
- Executes in the appropriate mode (capture/compare/auto)
- Runs comprehensive tests with forced fresh execution
- Captures metrics in structured JSON format
- Compares against baseline with delta calculation (compare/auto modes)
- Provides clear, actionable reports with visual indicators
- Returns appropriate exit codes for automation

The skill fails when:
- Script cannot be executed
- Tests time out or fail to run
- JSON cannot be generated or parsed
- Comparison logic fails
- Report is unclear or incomplete

## Troubleshooting

### "No baseline found for branch"
**Cause**: Running `--compare` without a previous baseline

**Solution**: Run `--capture` first, or use `--auto` mode

### "timeout: command not found"
**Cause**: `timeout` command not available on macOS

**Solution**: Install coreutils (`brew install coreutils`) or script falls back to no timeout

### "Console parsing returned 0 tests"
**Cause**: Gradle output format changed or tests didn't run

**Solution**: Script automatically falls back to XML parsing

### "Regressions detected but expected"
**Cause**: Intentional breaking changes or deprecated endpoint tests

**Solution**: Document expectations in PR, consider test-specific skips if appropriate
