---
name: forensic-complexity-trends
description: Use when monitoring code quality over time, measuring refactoring impact, tracking if complexity is improving or worsening, or validating technical debt work - tracks complexity metrics across git history identifying improving, stable, or deteriorating files
---

# Forensic Complexity Trends Analysis

## 🎯 When You Use This Skill

**State explicitly**: "Using forensic-complexity-trends pattern"

**Then follow these steps**:
1. Sample **time-series data** at regular intervals (monthly for 12 months)
2. Calculate **complexity change percentage** (comparing first vs last sample)
3. Classify trends: **improving** (<-20%), **stable** (±10%), **deteriorating** (>+20%)
4. Cite **research** when presenting trends (complexity growth = 2x defect rate)
5. Suggest **integration** with hotspot/refactoring analysis at the end

## Overview

Complexity trends analysis tracks how code complexity changes over time by sampling git history at regular intervals. Unlike static analysis (which shows current state), trend analysis reveals:
- **Deteriorating files** - Complexity increasing, technical debt accumulating
- **Improving files** - Refactoring working, complexity decreasing
- **Stable files** - Complexity controlled, good maintenance practices
- **Volatile files** - Complexity oscillating, inconsistent quality practices

**Core principle**: Trend direction matters more than absolute complexity. A simple file becoming complex signals emerging problems. A complex file becoming simpler validates refactoring ROI.

## When to Use

- Monitoring code quality over time (quarterly health checks)
- Measuring impact of refactoring efforts (before/after validation)
- Tracking if technical debt is improving or worsening
- Justifying continued refactoring investment to stakeholders
- Identifying files where quality is deteriorating (early warning)
- Validating that coding standards are being followed
- Pre-release quality assessment (trending toward stability?)

## When NOT to Use

- Insufficient git history (<6 months, trends unreliable)
- Greenfield projects (no baseline to compare against)
- When you need current complexity (use static analysis)
- When you need bug-proneness (use hotspot analysis)
- Single-commit analysis (trends require time series)

## Core Pattern

### ⚡ THE TREND CLASSIFICATION FORMULA (USE THIS)

**This is the research-backed approach - don't create custom classifications**:

```
Complexity Change (%) = ((complexity_now - complexity_baseline) / complexity_baseline) × 100

Trend Classification:
  - IMPROVING:       < -20% (complexity decreasing significantly)
  - STABLE:          -10% to +10% (controlled complexity)
  - DETERIORATING:   > +20% (complexity increasing significantly)
  - VOLATILE:        Oscillates >15% between samples

Where complexity_score = weighted combination:
  - LOC (lines of code): 40%
  - Indentation depth: 30%
  - Function count: 20%
  - Long functions (>50 LOC): 10%
```

**Sampling frequency**: Monthly for last 12 months (established codebases), weekly for last 6 months (fast-moving projects)

**Critical**: Must track BOTH trend direction (improving/deteriorating) AND correlation with change frequency.

### 📊 Research Benchmarks (CITE THESE)

**Always reference the research when presenting trend findings**:

| Finding | Impact | Source | When to Cite |
|---------|--------|--------|--------------|
| Increasing complexity | **2x** higher defect rate | Software Engineering Research | "Research shows increasing complexity correlates with 2x higher defects" |
| Complexity volatility | **3x** higher maintenance cost | Microsoft DevOps | "Volatile complexity costs 3x more to maintain (Microsoft)" |
| Refactoring validation | **30-40%** bug reduction | Google eng practices | "Successful complexity reduction typically yields 30-40% fewer bugs (Google)" |

**Always cite the source** when presenting trends to justify technical debt work or refactoring investment.

## Quick Reference

### Essential Git Commands

| Purpose | Command |
|---------|---------|
| **Monthly snapshots** | `git rev-list -1 --before="YYYY-MM-DD" HEAD` |
| **File at commit** | `git show COMMIT_HASH:path/to/file` |
| **Commit history** | `git log --since="12 months ago" --follow --oneline -- FILE` |
| **Date ranges** | `git log --since="YYYY-MM-DD" --until="YYYY-MM-DD" -- FILE` |

### Trend Classification

| Change % | Classification | Risk | Action |
|----------|----------------|------|--------|
| **< -20%** | IMPROVING | LOW | Document practices, apply elsewhere |
| **-10% to +10%** | STABLE | VARIES | Monitor, maintain standards |
| **+10% to +20%** | WARNING | MEDIUM | Investigate causes, plan cleanup |
| **> +20%** | DETERIORATING | HIGH | Urgent refactoring needed |

### Complexity Metrics Quick Check

| Metric | Calculation | Threshold |
|--------|-------------|-----------|
| **LOC growth** | `(current_LOC - baseline_LOC) / baseline_LOC × 100` | >30% = concern |
| **Indentation depth** | Average leading whitespace per line | >3 levels = high |
| **Long functions** | Count functions >50 lines | >20% of functions = high |
| **Function density** | LOC / function count | <20 or >100 = concern |

## Implementation

### Step 1: Define Sampling Points

**Time series approach**:

```bash
# Last 12 months, monthly samples
# Start with current (month 0) back to month 11

for month in {0..11}; do
  # Calculate date for this sample point
  sample_date=$(date -d "$month months ago" +%Y-%m-01)

  # Get commit hash closest to this date
  commit_hash=$(git rev-list -1 --before="$sample_date" HEAD)

  # Extract file at this commit for analysis
  git show $commit_hash:path/to/file > /tmp/sample_${month}.txt

  # Analyze this version (next step)
done
```

**Sampling strategy**:
- **12 months**: Monthly samples (12 data points)
- **6 months**: Bi-weekly samples (13 data points)
- **2 years**: Quarterly samples (8 data points)

### Step 2: Calculate Complexity for Each Sample

**For each file snapshot**:

```python
# Pseudocode for complexity calculation

def calculate_complexity(file_content):
    lines = file_content.split('\n')

    # Basic metrics
    loc = count_non_blank_non_comment_lines(lines)
    avg_indentation = average_leading_whitespace(lines)
    function_count = count_functions(lines)  # Language-specific
    long_functions = count_functions_over_n_lines(lines, 50)

    # Weighted complexity score
    complexity = (
        loc * 0.4 +
        avg_indentation * 30 * 0.3 +  # Scale to LOC range
        function_count * 10 * 0.2 +
        long_functions * 50 * 0.1
    )

    return {
        'complexity': complexity,
        'loc': loc,
        'avg_depth': avg_indentation,
        'functions': function_count,
        'long_functions': long_functions
    }
```

**Complexity indicators** (language-agnostic proxies):
- High indentation = nested control flow
- Many functions = potential fragmentation
- Long functions = poor separation of concerns
- High LOC = more to maintain

### Step 3: Analyze Trend

**Calculate trend metrics**:

```python
# Comparing first sample (baseline) to last sample (current)

baseline = samples[0]  # 12 months ago
current = samples[-1]  # Now

change_pct = ((current.complexity - baseline.complexity) / baseline.complexity) * 100

# Classify
if change_pct < -20:
    trend = "IMPROVING"
elif change_pct > 20:
    trend = "DETERIORATING"
elif -10 <= change_pct <= 10:
    trend = "STABLE"
else:
    trend = "WARNING"  # Between 10-20%

# Check for volatility
volatility = calculate_standard_deviation(samples)
if volatility > 15:
    trend += " (VOLATILE)"
```

**Inflection point detection**:
- Find month where trend direction changed
- Correlate with specific commits or events
- Identify what caused the change

### Step 4: Correlate with Change Frequency

**Critical insight**: Complexity trend + change frequency = risk

```python
# Get commit count for time period
change_frequency = count_commits_touching_file(last_12_months)

# Risk matrix
if trend == "DETERIORATING" and change_frequency > 20:
    risk = "CRITICAL"  # Worsening AND active development
elif trend == "DETERIORATING":
    risk = "HIGH"
elif trend == "STABLE" and change_frequency > 20:
    risk = "MEDIUM"  # Active but controlled
else:
    risk = "LOW"
```

## Output Format

### 1. Executive Summary

```
Complexity Trends Analysis (forensic-complexity-trends pattern)

File: src/services/user-manager.ts
Period: Oct 2023 - Oct 2024 (12 months, monthly samples)
Overall Trend: DETERIORATING (+34%)
Risk Level: CRITICAL

Research shows increasing complexity correlates with 2x higher defects.
```

### 2. Trend Metrics Table

```
Metric              | Baseline (12mo ago) | Current | Change  | Trend
--------------------|---------------------|---------|---------|-------
LOC                 | 456                 | 687     | +51%    | ↑
Avg Indentation     | 2.1                 | 3.4     | +62%    | ↑↑
Function Count      | 18                  | 24      | +33%    | ↑
Long Functions (>50)| 2                   | 6       | +200%   | ↑↑↑
Weighted Complexity | 342                 | 458     | +34%    | ↑↑
```

### 3. Time-Series Chart (ASCII)

```
Complexity Trend (12 months):

500 |                                            ●
450 |                                    ●    ●
400 |                          ●    ●
350 |              ●      ●                   ← Inflection (Jun)
300 |     ●    ●
250 |  ●
    +------------------------------------------------
      Oct  Nov  Dec  Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct

Legend: ● = Monthly sample
Inflection point (Jun 2024): Complexity increase accelerated
```

### 4. Detailed Analysis

**For each significant change**:

```
Period: Apr-Jun 2024 (Inflection Point)
Complexity: +18% in 2 months
Commits: 15 changes
Key Contributors: Alice (9), Bob (6)

Analysis:
- Feature: "Advanced user permissions" added (May 15)
- Commits show nested if-else statements increased from 12 to 28
- No corresponding refactoring to extract complexity
- Long function count doubled (2→4)

Recommendation: Extract permission logic to dedicated service class
Expected impact: -25% complexity (based on similar refactorings)
```

### 5. Risk Assessment

```
RISK LEVEL: CRITICAL

Why:
1. Complexity increased 34% over 12 months (DETERIORATING)
2. File has 47 commits in same period (HIGH CHURN)
3. Complexity + churn = hotspot with worsening quality
4. Recent trend shows acceleration (18% in last 2 months)

Research: Deteriorating complexity with high churn has 4-9x defect rate (Microsoft).

Urgency: Address within current sprint
Priority: P0 (before next release)
```

### 6. Recommendations

```
IMMEDIATE ACTIONS:

1. Refactor extracted: user-permissions-service.ts
   - Move permission logic to separate class
   - Expected: -30% complexity, -50% long functions
   - Effort: 2-3 days

2. Add complexity gates to CI
   - Block PRs that increase indentation depth >3
   - Limit function length to 50 LOC
   - Prevent further deterioration

3. Schedule complexity review
   - Monthly trend check for this file
   - Validate refactoring impact next month
```

## Common Mistakes

### Mistake 1: Only checking current complexity

**Problem**: Analyzing current state without tracking how you got there.

```bash
# ❌ BAD: Static analysis only
analyze_current_complexity(file)

# ✅ GOOD: Trend analysis over time
analyze_complexity_trends(file, last_12_months)
compare_baseline_to_current()
```

**Fix**: **Always track trends** - a simple file becoming complex is a warning signal that static analysis misses.

### Mistake 2: Not correlating with change frequency

**Problem**: Treating complexity in isolation without considering how often file changes.

```bash
# ❌ BAD: Just complexity trend
if complexity_increasing:
    flag_as_deteriorating()

# ✅ GOOD: Complexity + churn = risk
if complexity_increasing AND high_change_frequency:
    flag_as_critical_hotspot()
```

**Fix**: **Always combine** complexity trends with change frequency from git history. Deteriorating + active = critical.

### Mistake 3: Using too few samples

**Problem**: Drawing conclusions from 2-3 data points instead of time series.

```bash
# ❌ BAD: Before/after only
compare(current, one_year_ago)

# ✅ GOOD: Time series with monthly samples
analyze_monthly_samples(last_12_months)
detect_inflection_points()
```

**Fix**: **Minimum 8-12 samples** for reliable trend detection. Monthly sampling for 12 months is ideal.

### Mistake 4: Not validating refactoring impact

**Problem**: Refactoring files without measuring if complexity actually decreased.

**Fix**: Run trend analysis AFTER refactoring to validate:
- Did complexity decrease as expected?
- Is the trend now stable or improving?
- Document successful patterns for future refactoring

## ⚡ After Running Trend Analysis (DO THIS)

**Immediately suggest these next steps to the user**:

1. **Correlate deteriorating files with hotspots** (use **forensic-hotspot-finder**)
   - Deteriorating complexity + high churn = critical priority
   - Focus refactoring on these overlaps first

2. **Check ownership of deteriorating files** (use **forensic-knowledge-mapping**)
   - Single owner + deteriorating = knowledge silo forming
   - Multiple owners + deteriorating = coordination issue

3. **Calculate ROI for stabilizing trends** (use **forensic-refactoring-roi**)
   - Complexity reduction = defect reduction
   - Translate trend data to business value

4. **Track refactoring validation** (re-run **forensic-complexity-trends**)
   - Did refactoring work? (expect -20 to -40% complexity)
   - Set up monthly monitoring to ensure trend stays stable

### Example: Complete Trend Analysis Workflow

```
"Using forensic-complexity-trends pattern, I analyzed user-manager.ts over 12 months.

TREND CLASSIFICATION: DETERIORATING (+34% complexity)

Time Series:
- Oct 2023 (baseline): 342 complexity score
- Oct 2024 (current): 458 complexity score
- Inflection point: Jun 2024 (complexity accelerated)

Research shows increasing complexity correlates with 2x higher defects.

KEY FINDING: Deteriorating trend + 47 commits = CRITICAL RISK
This file is both worsening in quality AND actively developed.

RECOMMENDED NEXT STEPS:
1. Check hotspots (forensic-hotspot-finder) - Is this also high-churn?
2. Map ownership (forensic-knowledge-mapping) - Knowledge silo forming?
3. Calculate ROI (forensic-refactoring-roi) - Business case for cleanup?
4. After refactoring: Re-run trends to validate improvement

Would you like me to proceed with the hotspot cross-check?"
```

**Always provide this integration guidance** - trend analysis is most actionable when combined with hotspot and ownership data.

## Advanced Patterns

### Refactoring Impact Validation

**Measure before/after** refactoring efforts:

```
Pre-Refactoring (Mar 2024):
- Complexity: 458
- Long functions: 6
- Avg depth: 3.4

Post-Refactoring (Apr 2024):
- Complexity: 312 (-32%)
- Long functions: 2 (-67%)
- Avg depth: 2.1 (-38%)

VALIDATION: ✅ Refactoring successful
Expected: 30-40% bug reduction (Google research)
Recommendation: Apply same pattern to other deteriorating files
```

### Team/Developer Correlation

**Find patterns in who introduces complexity**:

```
Complexity Increases by Contributor (last 6 months):

Alice: +12% (3 commits) - Features adding business logic
Bob: +8% (5 commits) - Bug fixes increasing conditionals
Carol: -4% (2 commits) - Refactoring efforts

Insight: Feature development correlates with complexity growth
Recommendation: Add complexity review to feature PR checklist
```

### Multi-File Dashboard

**Aggregate trends across module**:

```
Module: src/services/ (12 files)

IMPROVING (3 files):
├─ auth-service.ts (-28%)
├─ cache-manager.ts (-15%)
└─ logger.ts (-22%)

STABLE (6 files): ...

DETERIORATING (3 files):
├─ user-manager.ts (+34%) ← CRITICAL (47 commits)
├─ permissions.ts (+28%) ← HIGH (32 commits)
└─ session-handler.ts (+21%) ← HIGH (29 commits)

Recommendation: Focus refactoring budget on deteriorating files first
```

## Research Background

**Key studies**:

1. **Microsoft Research** (2016): Complexity and defect correlation
   - 2x higher defect rates in files with increasing complexity
   - Recommendation: Track trends to predict problem areas early

2. **Google Engineering** (2018): Refactoring impact measurement
   - 30-40% bug reduction typical after successful complexity reduction
   - Recommendation: Validate refactoring with before/after measurement

3. **IBM Software Engineering** (2012): Volatility impact
   - 3x higher maintenance cost for files with volatile complexity
   - Recommendation: Stabilize complexity through coding standards

4. **Code Forensics Literature** (Tornhill, 2015): Trend analysis value
   - Historical patterns better predictor than static metrics
   - Recommendation: Always analyze trends, not just snapshots

**Why trends matter more than absolutes**: A complex but stable file (old, proven code) is less risky than a simple but deteriorating file (emerging problem).

## Integration with Other Techniques

**Combine complexity trends with**:

- **forensic-hotspot-finder**: Deteriorating + high churn = critical hotspot
- **forensic-refactoring-roi**: Complexity reduction = quantifiable value
- **forensic-knowledge-mapping**: Deteriorating + single owner = severe risk
- **forensic-change-coupling**: Coupled files deteriorating together = architectural issue

**Why**: Complexity trends alone show "what's getting worse" but not impact. Integration provides business justification and priority.
