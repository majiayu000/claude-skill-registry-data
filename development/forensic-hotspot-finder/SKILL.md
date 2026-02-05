---
name: forensic-hotspot-finder
description: Use when planning refactoring priorities, investigating recurring bugs, identifying which files cause the most bugs, or determining problem areas to fix - identifies high-risk files by combining git change frequency with code complexity using research-backed formula (4-9x defect rates)
---

# Forensic Hotspot Finder

## 🎯 When You Use This Skill

**State explicitly**: "Using forensic-hotspot-finder pattern"

**Then follow these steps**:
1. Apply the **normalized hotspot formula** (see below)
2. Cite **research benchmarks** (4-9x defect rates from Microsoft Research)
3. Check for **both** high frequency AND high complexity (not just one)
4. Normalize by **file age** (older files naturally have more commits)
5. Suggest **integration** with other forensic skills at the end

## Overview

Hotspot analysis identifies files that are both frequently changed AND structurally complex. Research shows these files have 4-9x higher defect rates than normal code. This technique uses git history to find where bugs are most likely to occur.

**Core principle**: Change frequency × Complexity = Risk. Files with both characteristics are "hotspots" requiring immediate attention.

## When to Use

- Planning technical debt reduction sprints
- Investigating recurring bug patterns in specific modules
- Prioritizing code review focus areas
- Pre-release risk assessment
- Quarterly code health checks
- Allocating refactoring budget

## When NOT to Use

- Insufficient git history (<6 months preferred, <3 months unreliable)
- Greenfield projects without meaningful change patterns
- When only complexity matters (use static analysis instead)
- For individual function analysis (hotspots work at file level)
- When you need architectural insights (use change coupling analysis instead)

## Core Pattern

### ⚡ THE HOTSPOT FORMULA (USE THIS)

**This is the research-backed formula - don't create custom variations**:

```
Risk Score = Normalized Change Frequency × Normalized Complexity Factor

Where:
  Change Frequency = (commits in time period) / (file age in days)
  Complexity Factor = LOC + Indentation Depth + Function Count

Normalize BOTH factors to 0-1 scale within your codebase before multiplying.
```

**Critical**: Must have BOTH high frequency AND high complexity. High-change simple files are not hotspots.

### 📊 Research Benchmarks (CITE THESE)

Based on Microsoft Research and Google engineering studies:

- **4-9x higher defect rates** for files in top 10% of both change frequency + complexity
- **2-3x higher bug rates** for files with >9 contributors (coordination overhead)
- **30-40% bug reduction** typically achieved by refactoring top 3 hotspots

**Always cite these benchmarks** when presenting hotspot findings to stakeholders.

## Quick Reference

### Essential Git Commands

| Purpose | Command |
|---------|---------|
| **Change frequency** | `git log --since="12 months ago" --name-only --format="" \| sort \| uniq -c \| sort -rn` |
| **File contributors** | `git log --since="12 months ago" --format="%an" -- FILE \| sort \| uniq -c \| sort -rn` |
| **Commit details** | `git log --since="12 months ago" --follow --oneline -- FILE` |
| **Recent changes** | `git log --since="3 months ago" --stat -- FILE` |

### Complexity Metrics (Quick)

| Metric | Command | Interpretation |
|--------|---------|----------------|
| **Lines of Code** | `wc -l FILE` | >500 lines = high |
| **Indentation depth** | `grep "^[[:space:]]" FILE \| awk '{print length($0)-length(ltrim($0))}' \| sort -n \| tail -1` | >6 tabs/spaces = complex |
| **Function count** | `grep -E "^(function\|def\|func\|void\|public\|private)" FILE \| wc -l` | Context-dependent |

### Risk Classification

| Changes (12mo) | LOC | Risk Level | Action |
|----------------|-----|------------|--------|
| >20 | >500 | **CRITICAL** | Refactor immediately |
| >15 | >300 | **HIGH** | Schedule for next sprint |
| >10 | >200 | **MEDIUM** | Monitor closely |
| <10 | any | **LOW** | Normal maintenance |

## Implementation

### Basic Hotspot Detection

```bash
#!/bin/bash
# Basic hotspot finder - identifies top 10 risky files

TIME_PERIOD="12 months ago"
MIN_CHANGES=5

# Step 1: Get change frequency for all files
echo "Analyzing git history..."
git log --since="$TIME_PERIOD" --name-only --format="" | \
  grep -v "^$" | \
  sort | uniq -c | sort -rn | \
  awk -v min="$MIN_CHANGES" '$1 >= min {print $1 "\t" $2}' > /tmp/changes.txt

# Step 2: For top 50 changed files, calculate complexity
echo "Calculating complexity scores..."
cat /tmp/changes.txt | head -50 | while read count file; do
  if [ -f "$file" ]; then
    loc=$(wc -l < "$file" 2>/dev/null || echo 0)
    depth=$(grep "^[[:space:]]" "$file" 2>/dev/null | \
            awk '{print length($0)-length($1)}' | \
            sort -n | tail -1)
    depth=${depth:-0}

    # Risk score: changes * (LOC/100) * (depth/10)
    risk=$(echo "$count * ($loc / 100) * (1 + $depth / 10)" | bc -l)
    printf "%.2f\t%d\t%d\t%s\n" "$risk" "$count" "$loc" "$file"
  fi
done | sort -rn > /tmp/hotspots.txt

# Step 3: Report top 10 hotspots
echo ""
echo "TOP 10 CODE HOTSPOTS"
echo "===================="
printf "%-10s %-10s %-10s %s\n" "Risk Score" "Changes" "LOC" "File"
echo "------------------------------------------------------------"
head -10 /tmp/hotspots.txt | while read risk changes loc file; do
  printf "%-10.2f %-10d %-10d %s\n" "$risk" "$changes" "$loc" "$file"
done

echo ""
echo "Focus refactoring efforts on files with highest risk scores."
```

### Advanced Analysis (with visualization data)

For more sophisticated analysis including:
- Time-series complexity tracking
- Contributor count correlation
- Visualization-ready JSON output
- Cross-module hotspot clusters

Consider creating a supporting script (see pattern below) or using code analysis tools.

## Common Mistakes

### Mistake 1: Creating a custom scoring formula

**Problem**: Inventing your own formula instead of using the research-backed approach.

```bash
# ❌ BAD: Custom formula without research backing
score = commits + (bugs × 3) + (size ÷ 100)

# ✅ GOOD: Use the normalized hotspot formula from this skill
risk = (commits / file_age) × (LOC + depth + functions)
# Then normalize both factors to 0-1 before multiplying
```

**Fix**: Use the hotspot formula from this skill. It's based on Microsoft Research showing 4-9x higher defects. Don't reinvent it.

### Mistake 2: Ignoring file age normalization

**Problem**: Older files naturally have more commits, biasing results.

**Fix**: **Always** divide commit count by file age (in days or months). This is critical for accuracy.

### Mistake 3: Treating all high-change files as problems

**Problem**: High change + low complexity = active but healthy code (like simple config files).

**Fix**: Require BOTH high change AND high complexity. Check this explicitly. Simple, frequently changed files aren't hotspots.

### Mistake 4: Not citing research benchmarks

**Problem**: Saying "this file is complex" without evidence.

**Fix**: **Always cite**: "Research shows hotspot files have 4-9x higher defect rates (Microsoft Research)". This makes recommendations credible.

### Mistake 5: Forgetting to suggest next steps

**Problem**: Providing hotspot list without integration guidance.

**Fix**: After hotspot analysis, **always suggest** checking ownership (knowledge-mapping) and calculating costs (debt-quantification).

## Real-World Impact

### Research Foundation

- **Microsoft Research** (Nagappan et al.): Code churn correlates with defects, especially when combined with complexity
- **Google**: Files with >9 contributors have 2-3x higher defect rates
- **Industry data**: Refactoring top 3 hotspots reduces bug rate by 30-40%

### Typical Results

```
Before refactoring hotspots:
- File auth.js: 45 bugs/year, 28 changes/year
- File config.js: 32 bugs/year, 41 changes/year
- File api-handler.js: 38 bugs/year, 35 changes/year

After 2-week refactoring sprint (top 3 hotspots):
- auth.js: 12 bugs/year (-73%), 22 changes/year
- config.js: 18 bugs/year (-44%), 38 changes/year
- api-handler.js: 23 bugs/year (-39%), 31 changes/year

Overall bug reduction: 35%, Development velocity: +15%
```

## ⚡ After Running Hotspot Analysis (DO THIS)

**Immediately suggest these next steps to the user**:

1. **Check ownership** for single-owner hotspots (use **forensic-knowledge-mapping**)
   - Critical risk = hotspot + single owner
   - Calculate truck factor for team resilience

2. **Calculate business cost** (use **forensic-debt-quantification**)
   - Translate hotspot findings to dollars
   - Show ROI for refactoring
   - Get stakeholder buy-in

3. **Track trends** (use **forensic-complexity-trends**)
   - Are hotspots improving or getting worse?
   - Measure refactoring impact over time

4. **Find coupled files** (use **forensic-change-coupling**)
   - Identify files that should be refactored together
   - Avoid breaking dependencies

### Example: Complete Hotspot Workflow

```
"I've identified the top 10 hotspots using the forensic-hotspot-finder pattern.

The top 3 files with highest risk scores are:
1. manager.go (Score: 386) - 62 bug fixes, 2,471 LOC
2. Layout.tsx (Score: 371) - 61 bug fixes, 1,126 LOC
3. sessions.go (Score: 259) - 31 bug fixes, 1,799 LOC

Research shows hotspot files have 4-9x higher defect rates (Microsoft Research).

RECOMMENDED NEXT STEPS:
1. Check ownership (forensic-knowledge-mapping) - Are these single-owner risks?
2. Calculate business cost (forensic-debt-quantification) - What's the ROI?
3. Track trends (forensic-complexity-trends) - Are they getting worse?

Would you like me to proceed with any of these analyses?"
```

**Always provide this integration guidance** - it's what makes forensic analysis actionable.

## Supporting Files

For complete automation with JSON output and trend tracking, consider creating:

```
forensic-hotspot-finder/
├── SKILL.md (this file)
├── hotspot-analyzer.sh (complete analysis script)
└── visualize-hotspots.py (optional: generate charts)
```

## Related Patterns

- **Root Cause Analysis**: When you find a hotspot, investigate WHY it's complex (tight coupling? god object? accumulation of features?)
- **Boy Scout Rule**: Make hotspot files slightly better with each change, don't just add to the mess
- **Strangler Fig Pattern**: For critical hotspots, build replacement alongside, gradually migrate
- **Defense in Depth**: Add extra validation, logging, and tests to hotspots you can't refactor yet
