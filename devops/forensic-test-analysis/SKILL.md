---
name: forensic-test-analysis
description: Use when investigating test suite issues, reducing CI/CD time, identifying brittle tests, finding test duplication, or analyzing test maintenance burden - reveals test code quality problems through git history analysis
---

# Forensic Test Analysis

## 🎯 When You Use This Skill

**State explicitly**: "Using forensic-test-analysis pattern"

**Then follow these steps**:
1. Calculate **test change frequency** vs production code changes
2. Identify **brittle tests** (coupling ratio >2x = test changes more than prod)
3. Find **large test files** (>500 LOC = maintenance burden)
4. Cite **research** when presenting findings (brittle tests = 2-3x maintenance cost)
5. Suggest **integration** with hotspot-finder and complexity-trends at end

## Overview

Test analysis examines test code quality through git forensics. Unlike static test coverage tools, this reveals:
- **Brittle tests** - Change more frequently than production code
- **Over-coupled tests** - Break with every production change
- **Test hotspots** - High-churn test files requiring constant fixes
- **Duplicate test logic** - Copy-paste test code (maintenance burden)
- **Large test files** - Unmaintainable test suites
- **Slow tests** - Impact CI/CD cycle time

**Core principle**: Good tests are stable. If tests change more than production code (ratio >2x), they're brittle and expensive.

## When to Use

- Investigating slow or flaky CI/CD pipelines
- Reducing test maintenance burden
- Before refactoring test suites
- Diagnosing "broken tests" tickets frequency
- Quarterly test health checks
- After major refactoring (did tests improve?)
- Justifying test refactoring investment

## When NOT to Use

- Insufficient git history (<6 months unreliable)
- No test files (obviously)
- Greenfield projects (no patterns yet)
- When you need test coverage metrics (use coverage tools)
- When you need defect correlation (use hotspot analysis)

## Core Pattern

### ⚡ THE TEST BRITTLENESS FORMULA (USE THIS)

**This is the test health metric - don't create custom ratios**:

```
Test Brittleness Ratio = test_changes / production_changes

Interpretation:
  - >2.0:  BRITTLE (test changes more than prod - expensive)
  - 1.0-2.0: NORMAL (tests evolve with production)
  - 0.5-1.0: GOOD (stable tests, well-designed)
  - <0.5:  UNDER-TESTED or integration tests (fewer changes expected)

Test File Size Risk:
  - >500 LOC:  CRITICAL (unmaintainable)
  - 300-500 LOC: HIGH (should split)
  - 150-300 LOC: MODERATE (monitor)
  - <150 LOC:  GOOD (focused tests)

Test Hotspot = Brittle (>2x) + High Changes (>20 commits/year)
```

**Critical**: Ratio >2x indicates tests are MORE expensive to maintain than production code.

### 📊 Research Benchmarks (CITE THESE)

**Always reference research when presenting test findings**:

| Finding | Impact | Source | When to Cite |
|---------|--------|--------|--------------|
| Brittle tests | **2-3x** maintenance cost | Google Testing Blog | "Brittle tests cost 2-3x more to maintain (Google)" |
| Test duplication | **40-60%** wasted effort | Microsoft DevOps | "Test duplication wastes 40-60% of test effort (Microsoft)" |
| Slow tests | **20-30 min** daily waste per dev | Continuous Delivery | "Slow tests waste 20-30 min/developer/day (CD research)" |

**Always cite the source** when justifying test refactoring investment.

## Quick Reference

### Essential Git Commands

| Purpose | Command |
|---------|---------|
| **Test change frequency** | `git log --since="12 months ago" --name-only --format="" -- "*test*" "*spec*" \| sort \| uniq -c \| sort -rn` |
| **Production changes** | `git log --since="12 months ago" --name-only --format="" -- "src/**/*.js" \| grep -v test \| sort \| uniq -c` |
| **Test-only commits** | `git log --since="12 months ago" --name-only --format="COMMIT:%H\|%s" \| awk '/test.*fix\|flaky/'` |
| **Test file sizes** | `find . -name "*.test.*" -o -name "*spec.*" \| xargs wc -l \| sort -rn` |

### Test Health Classification

| Brittleness Ratio | File Size | Change Frequency | Classification | Action |
|-------------------|-----------|------------------|----------------|--------|
| **>2.0** | >500 LOC | >20/year | CRITICAL | Urgent refactoring |
| **1.5-2.0** | 300-500 | 15-20 | HIGH | Schedule refactoring |
| **1.0-1.5** | 150-300 | 10-15 | MODERATE | Monitor trends |
| **<1.0** | <150 | <10 | GOOD | Maintain standards |

### Common Test Anti-Patterns

| Pattern | Indicator | Fix |
|---------|-----------|-----|
| **Brittle snapshots** | "update snapshots" commits | Use semantic assertions |
| **Test-only commits** | "fix failing test" commits | Decouple from implementation |
| **Large test files** | >500 LOC | Split by feature/scenario |
| **Duplicate setup** | Repeated beforeEach code | Extract test helpers |

## Implementation

### Step 1: Identify Test Files

**Gather test file list**:

```bash
# Find all test files (adapt patterns to your project)
test_files=$(find . -type f \
  -name "*.test.js" -o \
  -name "*.test.ts" -o \
  -name "*.spec.js" -o \
  -name "*_test.py" -o \
  -name "*Test.java")

# Get corresponding production files
# (remove .test/.spec from filename)
```

### Step 2: Calculate Brittleness Ratio

**For each test file**:

```python
# Pseudocode for brittleness calculation

def calculate_brittleness(test_file, production_file):
    # Count test file changes
    test_changes = git_log_count(test_file, since="12 months ago")

    # Count production file changes
    prod_changes = git_log_count(production_file, since="12 months ago")

    if prod_changes == 0:
        return None  # No production changes to compare

    # Calculate ratio
    brittleness_ratio = test_changes / prod_changes

    # Classify
    if brittleness_ratio > 2.0:
        classification = "BRITTLE"
        severity = "CRITICAL"
    elif brittleness_ratio > 1.5:
        classification = "BRITTLE"
        severity = "HIGH"
    elif brittleness_ratio > 1.0:
        classification = "MODERATE"
        severity = "MEDIUM"
    else:
        classification = "GOOD"
        severity = "LOW"

    return {
        'test_changes': test_changes,
        'prod_changes': prod_changes,
        'ratio': brittleness_ratio,
        'classification': classification,
        'severity': severity
    }
```

### Step 3: Detect Test-Only Commits

**Identify pure test maintenance**:

```python
def find_test_only_commits(since="12 months ago"):
    # Get all commits
    commits = git_log(since=since, name_only=True)

    test_only_commits = []
    for commit in commits:
        changed_files = commit.files

        # Check if only test files changed
        all_tests = all(is_test_file(f) for f in changed_files)

        # Check for brittle test keywords
        brittle_keywords = ['fix failing test', 'update snapshot',
                           'fix flaky', 'fix test', 'test fix']
        is_brittle = any(kw in commit.message.lower() for kw in brittle_keywords)

        if all_tests and is_brittle:
            test_only_commits.append({
                'hash': commit.hash,
                'message': commit.message,
                'files': changed_files,
                'category': 'BRITTLE_TEST_MAINTENANCE'
            })

    return test_only_commits
```

**High count of test-only commits = brittle test suite**

### Step 4: Analyze Test File Size

**Flag large test files**:

```python
def analyze_test_sizes():
    large_tests = []

    for test_file in find_test_files():
        loc = count_lines(test_file)

        if loc > 500:
            severity = "CRITICAL"
        elif loc > 300:
            severity = "HIGH"
        elif loc > 150:
            severity = "MODERATE"
        else:
            severity = "LOW"

        if severity in ["CRITICAL", "HIGH"]:
            large_tests.append({
                'file': test_file,
                'loc': loc,
                'severity': severity,
                'recommendation': 'Split into smaller test files'
            })

    return large_tests
```

## Output Format

### 1. Executive Summary

```
Test Suite Health Assessment (forensic-test-analysis pattern)

Test Files: 247
Production Files: 312
Test-to-Production Ratio: 0.79:1

KEY FINDINGS:

Brittle Tests (>2x changes): 18 files (7%)
Large Test Files (>500 LOC): 12 files
Test-Only Commits: 89 commits (23% of test commits)
Test Hotspots (brittle + high-churn): 8 files

Research shows brittle tests cost 2-3x more to maintain (Google).

Estimated Annual Test Maintenance Cost: $45,000
  - Brittle test fixes: $28,000
  - Large file maintenance: $12,000
  - Duplicate code: $5,000
```

### 2. Test Hotspots (Brittle + High-Churn)

```
Rank | Test File                | Test Chg | Prod Chg | Ratio | LOC | Status
-----|--------------------------|----------|----------|-------|-----|----------
1    | auth/login.test.js      | 42       | 15       | 2.8x  | 687 | 🚨 CRITICAL
2    | api/users.spec.js       | 35       | 18       | 1.9x  | 523 | ❌ HIGH
3    | checkout.test.ts        | 48       | 22       | 2.2x  | 445 | ❌ HIGH
4    | Form.test.tsx           | 38       | 14       | 2.7x  | 392 | ❌ HIGH
```

### 3. Detailed Test Analysis

```
=== TEST HOTSPOT #1: auth/login.test.js ===

Brittleness Metrics:
  Test Changes (12mo): 42 commits
  Production Changes: 15 commits (login.js)
  Brittleness Ratio: 2.8x (CRITICAL - tests change faster than prod)
  Lines of Code: 687 (CRITICAL - unmaintainable size)

Research: Brittle tests cost 2-3x more to maintain (Google).

Change Pattern Analysis:
  - 14 commits: "fix failing test" (33% - pure maintenance)
  - 11 commits: "update snapshots" (26% - brittle snapshots)
  - 10 commits: aligned with production (24% - expected)
  - 7 commits: "refactor tests" (17%)

Issues Identified:
  ⚠️  Brittle: 2.8x change ratio (expected ~1.0x)
  ⚠️  Large: 687 LOC (expected <300 LOC)
  ⚠️  Snapshot-heavy: 26% of changes are snapshot updates
  ⚠️  Maintenance burden: 33% pure test fixes

RECOMMENDATIONS:
1. IMMEDIATE: Replace snapshots with semantic assertions
2. SHORT-TERM: Split into 3 smaller test files (~200 LOC each)
3. MEDIUM-TERM: Decouple tests from implementation details
4. PROCESS: Add test brittleness check to CI

Expected Impact: -60% maintenance cost, -70% brittleness ratio
```

### 4. Test-Only Commit Analysis

```
Brittle Test Maintenance (Test-Only Commits):

Total Test Commits: 387
Test-Only Commits: 89 (23% - maintenance overhead)

Top Brittle Tests (by fix commits):
  1. auth/login.test.js: 14 "fix" commits
  2. api/users.spec.js: 11 "fix" commits
  3. checkout.test.ts: 9 "fix" commits

Pattern: 23% of test effort is pure maintenance (not new tests)
Impact: Wasted effort, developer frustration

Research: Brittle tests cost 2-3x more to maintain (Google).
```

## Common Mistakes

### Mistake 1: Ignoring brittleness ratio

**Problem**: Only looking at test change count, not comparing to production.

```bash
# ❌ BAD: Just count test changes
high_churn_tests = tests with >20 changes

# ✅ GOOD: Calculate brittleness ratio
brittle_tests = tests where (test_changes / prod_changes) > 2.0
```

**Fix**: **Always calculate ratio** - 30 test changes with 30 prod changes is normal, not brittle.

### Mistake 2: Treating all snapshot commits as bad

**Problem**: Flagging legitimate snapshot updates as brittle.

**Fix**: Distinguish between:
- **Legitimate**: Snapshot updates with corresponding UI changes
- **Brittle**: Frequent snapshot updates without meaningful prod changes (>5 per year)
- **Always check**: If "update snapshots" commit has NO production changes = brittle

### Mistake 3: Not checking test file size

**Problem**: Focusing only on change frequency, missing unmaintainable large files.

```bash
# ❌ BAD: Only brittleness
flag tests with ratio > 2.0

# ✅ GOOD: Combine brittleness + size
flag tests where (ratio > 2.0 OR size > 500)
```

**Fix**: **Always check file size** - large files (>500 LOC) are maintenance burdens even if stable.

### Mistake 4: Not estimating test maintenance cost

**Problem**: Identifying brittle tests without quantifying business impact.

**Fix**: Calculate cost:
- Average commit time: 30 minutes
- Brittle test commits: 89 per year
- Cost: 89 × 0.5 hours × $100/hour = $4,450/year per brittle test file
- **Always translate to dollars** for executive justification

## ⚡ After Running Test Analysis (DO THIS)

**Immediately suggest these next steps to the user**:

1. **Correlate with production hotspots** (use **forensic-hotspot-finder**)
   - Are brittle tests testing hotspot code?
   - Hotspot + brittle test = double maintenance burden
   - Prioritize refactoring both together

2. **Check test complexity trends** (use **forensic-complexity-trends**)
   - Are test files growing in complexity?
   - Track whether test refactoring is working
   - Set up monitoring for test file sizes

3. **Calculate refactoring ROI** (use **forensic-refactoring-roi**)
   - Test maintenance cost = annual waste
   - Test refactoring investment = effort estimation
   - ROI typically very high (brittle tests are expensive)

4. **Track test health monthly**
   - Re-run test analysis quarterly
   - Monitor brittleness ratio trends
   - Early warning for emerging brittle tests

### Example: Complete Test Analysis Workflow

```
"Using forensic-test-analysis pattern, I analyzed 247 test files.

TEST HEALTH ASSESSMENT:

Brittle Tests: 18 files (7% of test suite)
  - Brittleness ratio >2.0x (tests change faster than production)
  - Research shows 2-3x higher maintenance cost (Google)

TOP BRITTLE TEST:

auth/login.test.js:
  - Ratio: 2.8x (42 test changes vs 15 prod changes)
  - Size: 687 LOC (CRITICAL)
  - Pattern: 33% "fix failing test" commits
  - Cost: ~$8,400/year in maintenance

ESTIMATED ANNUAL COST: $45,000 in brittle test maintenance

RECOMMENDATIONS:
1. Replace snapshot tests with semantic assertions
2. Split large test files (>500 LOC)
3. Decouple tests from implementation details

NEXT STEPS:
1. Check production hotspots (forensic-hotspot-finder) - Testing hotspot code?
2. Track complexity trends (forensic-complexity-trends) - Are tests growing?
3. Calculate ROI (forensic-refactoring-roi) - Business case for cleanup

Would you like me to proceed with hotspot correlation?"
```

**Always provide this integration guidance** - test issues often indicate production code quality problems.

## Advanced Patterns

### Test-Production Co-Change Analysis

**Find which tests always change with production**:

```
Co-Change Pattern:

login.test.js ↔ login.js:
  - 15 commits changed both together (expected)
  - 27 commits changed ONLY login.test.js (brittle!)

Ratio Analysis:
  - Expected: 1:1 co-change
  - Actual: 1:2.8 (test changes 2.8x more)

Conclusion: Tests over-coupled to implementation details
```

### Test Refactoring Impact Validation

**Measure before/after**:

```
Before Refactoring (auth/login.test.js):
  - Brittleness: 2.8x
  - Size: 687 LOC
  - Maintenance commits: 14/year

After Refactoring (Q2 2024):
  - Brittleness: 1.1x (-61%)
  - Size: 245 LOC (-64%)
  - Maintenance commits: 2/year (-86%)

VALIDATION: ✅ Refactoring successful
Annual savings: $7,200 (from $8,400 to $1,200)
```

### Flaky Test Detection

**If test execution data available**:

```
Flaky Tests (intermittent failures):

checkout.test.ts:
  - 12 "fix flaky test" commits
  - Pattern: Failures on CI but pass locally
  - Root cause: Race conditions, timing dependencies

Impact: Developer context switching, CI/CD unreliability
Fix: Condition-based waiting, not arbitrary timeouts
```

## Research Background

**Key studies**:

1. **Google Testing Blog** (2017): Test brittleness cost
   - Brittle tests cost 2-3x more to maintain than stable tests
   - Snapshot tests are particularly brittle
   - Recommendation: Use semantic assertions, not snapshots

2. **Microsoft DevOps** (2019): Test duplication impact
   - 40-60% of test effort wasted on duplicate test logic
   - Copy-paste tests create maintenance burden
   - Recommendation: Extract test helpers, reduce duplication

3. **Continuous Delivery** (Humble & Farley): Slow test impact
   - Slow tests waste 20-30 minutes per developer per day
   - Developers skip running tests if they're too slow
   - Recommendation: Optimize test execution, parallelize

4. **Test Maintenance Research** (Garousi et al, 2013): Test code quality
   - Test code quality predicts test effectiveness
   - Large test files correlate with defects
   - Recommendation: Apply same quality standards to test code

**Why test quality matters**: Poor test quality wastes developer time, reduces confidence, and creates maintenance burden exceeding test value.

## Integration with Other Techniques

**Combine test analysis with**:

- **forensic-hotspot-finder**: Brittle tests on hotspot code = double maintenance burden
- **forensic-complexity-trends**: Track test complexity over time
- **forensic-refactoring-roi**: Test refactoring typically has very high ROI
- **forensic-debt-quantification**: Test maintenance is quantifiable technical debt

**Why**: Test quality affects developer productivity - poor tests slow everyone down.
