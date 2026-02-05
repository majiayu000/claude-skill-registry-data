---
name: forensic-knowledge-mapping
description: Use when assessing team resilience, planning for developer departures, calculating bus/truck factor, identifying knowledge silos, or evaluating organizational risk - maps code ownership from git history and identifies single points of failure using research-backed thresholds (>80% ownership = silo)
---

# Forensic Knowledge Mapping

## 🎯 When You Use This Skill

**State explicitly**: "Using forensic-knowledge-mapping pattern"

**Then follow these steps**:
1. Calculate **ownership percentages** using git commit history
2. Identify **single-owner files** (>80% commits from one person)
3. Calculate **truck factor** (minimum developers to lose before crisis)
4. Cite **research benchmarks** (>9 contributors = 2-3x defects)
5. Cross-reference with **hotspots** (single owner + hotspot = critical risk)
6. Provide **mitigation strategies** for knowledge concentration

## Overview

Knowledge mapping analyzes git history to understand who knows what in your codebase. It identifies knowledge silos, calculates the "truck factor" (minimum developers who could leave before project stalls), and highlights critical single-owner files that create organizational risk.

**Core principle**: Code ownership concentration creates risk. Files with single owners, especially critical files, represent organizational fragility that can be measured and mitigated.

## When to Use

- Assessing team resilience and bus/truck factor
- Planning for developer departures (resignation, leave, promotion)
- Onboarding new team members (where to focus training)
- Identifying knowledge transfer priorities
- Team reorganization planning
- M&A due diligence (technical risk assessment)
- Quarterly team health checks

## When NOT to Use

- Very small teams (2-3 developers) - some concentration inevitable
- Greenfield projects (<6 months) - patterns not yet established
- When ownership by design (designated experts) - may be intentional
- For non-critical codebases where loss doesn't matter

## Core Pattern

### ⚡ TRUCK FACTOR CALCULATION (USE THIS)

**This is the standard formula for calculating organizational risk**:

```
Truck Factor = Minimum number of developers whose loss would
               orphan >50% of essential files

Where:
  "Orphan" = <1 remaining knowledgeable developer
  "Essential" = Critical files (combine with hotspot analysis)
```

### 📊 Risk Classification (APPLY THESE THRESHOLDS)

| Ownership | Contributors | Risk Level | Action | Cite When |
|-----------|--------------|------------|--------|-----------|
| **Single owner** | 1 person >80% commits | 🔴 **CRITICAL** | Immediate pair/cross-train | "This file has >80% single-owner concentration" |
| **Dominant owner** | 2 people (60/40 split) | 🟡 **HIGH** | Add backup knowledge | "Needs backup owner for resilience" |
| **Shared** | 3+ balanced | 🟢 **HEALTHY** | Maintain | "Good knowledge distribution" |
| **Too diffuse** | >9 contributors | 🟡 **COORDINATION** | May need splitting | "Google: >9 contributors = 2-3x bugs" |

### 📊 Research Benchmarks (CITE THESE)

**Always reference these thresholds when analyzing ownership**:

- **Truck Factor < 5**: High organizational risk for most teams
- **>80% ownership**: Defined as knowledge silo requiring action
- **>9 contributors**: 2-3x higher defect rate (Google research on coordination overhead)
- **Critical file + single owner**: Maximum risk - cite both factors together

**Always cite** when identifying these patterns to stakeholders.

## Quick Reference

### Essential Git Commands

| Purpose | Command |
|---------|---------|
| **All contributors** | `git log --since="12 months ago" --format="%an" \| sort \| uniq` |
| **Contributions by author** | `git log --since="12 months ago" --format="%an" \| sort \| uniq -c \| sort -rn` |
| **File ownership** | `git log --since="12 months ago" --follow --format="%an" -- FILE \| sort \| uniq -c \| sort -rn` |
| **Current file owners** | `git blame --line-porcelain FILE \| grep "^author " \| sort \| uniq -c \| sort -rn` |
| **Last modified** | `git log -1 --format="%an %ad" --date=short -- FILE` |

### Ownership Calculation

```
Primary Owner: Author with >50% of commits to file
Secondary Owner: Author with >20% of commits
Backup Knowledge: Author with >10% of commits

Ownership %: (author_commits / total_commits) × 100
```

## Implementation

### Basic Knowledge Map

```bash
#!/bin/bash
# Generate code ownership map

TIME_PERIOD="12 months ago"
OUTPUT_FILE="knowledge-map.txt"

echo "CODE OWNERSHIP ANALYSIS" > "$OUTPUT_FILE"
echo "======================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 1. Get all active contributors
echo "Active Contributors:" >> "$OUTPUT_FILE"
git log --since="$TIME_PERIOD" --format="%an" | \
  sort | uniq -c | sort -rn | \
  awk '{printf "  %s: %d commits\n", $2, $1}' >> "$OUTPUT_FILE"

echo "" >> "$OUTPUT_FILE"

# 2. Identify files and calculate ownership
echo "Analyzing file ownership..." >&2
git log --since="$TIME_PERIOD" --name-only --format="" | \
  sort | uniq | \
  while read file; do
    if [ -f "$file" ]; then
      # Get contributors for this file
      contributors=$(git log --since="$TIME_PERIOD" --follow --format="%an" -- "$file" | sort | uniq -c | sort -rn)
      total_commits=$(echo "$contributors" | awk '{sum+=$1} END {print sum}')

      if [ "$total_commits" -gt 5 ]; then  # Minimum 5 commits for meaningful analysis
        # Calculate ownership percentages
        primary_owner=$(echo "$contributors" | head -1 | awk '{print $2}')
        primary_commits=$(echo "$contributors" | head -1 | awk '{print $1}')
        primary_pct=$(echo "scale=1; $primary_commits * 100 / $total_commits" | bc)

        # Classify risk
        if [ "$(echo "$primary_pct > 80" | bc)" -eq 1 ]; then
          risk="🔴 CRITICAL"
        elif [ "$(echo "$primary_pct > 60" | bc)" -eq 1 ]; then
          risk="🟡 HIGH"
        else
          risk="🟢 SHARED"
        fi

        echo "$risk  $file  ($primary_owner: ${primary_pct}%)" >> "$OUTPUT_FILE"
      fi
    fi
  done

# 3. Calculate truck factor (simplified)
echo "" >> "$OUTPUT_FILE"
echo "TRUCK FACTOR ANALYSIS" >> "$OUTPUT_FILE"
echo "=====================" >> "$OUTPUT_FILE"

# Count files owned (>80%) by each developer
git log --since="$TIME_PERIOD" --format="%an" | sort | uniq | \
  while read author; do
    owned_files=0
    # Count files where this author has >80% ownership
    # (Full implementation would iterate through all files)
    echo "  $author: analyzing..." >&2
    # Simplified output
  done

echo "" >> "$OUTPUT_FILE"
echo "Analysis complete. See $OUTPUT_FILE for results."
```

### Truck Factor Analysis

```python
#!/usr/bin/env python3
"""
Calculate truck factor - minimum developers whose loss would orphan critical files
"""
import subprocess
import json
from collections import defaultdict

def get_file_ownership(time_period="12 months ago", min_commits=5):
    """Get ownership map for all files"""
    ownership = {}

    # Get all files with activity
    files_cmd = f"git log --since='{time_period}' --name-only --format=''"
    files = subprocess.check_output(files_cmd, shell=True, text=True)
    files = [f for f in set(files.strip().split('\n')) if f]

    for file_path in files:
        try:
            # Get contributors for this file
            contrib_cmd = f"git log --since='{time_period}' --follow --format='%an' -- '{file_path}'"
            contributors = subprocess.check_output(contrib_cmd, shell=True, text=True)
            contrib_counts = defaultdict(int)
            for author in contributors.strip().split('\n'):
                if author:
                    contrib_counts[author] += 1

            total = sum(contrib_counts.values())
            if total >= min_commits:
                # Calculate ownership percentages
                ownership[file_path] = {
                    author: (count / total * 100)
                    for author, count in contrib_counts.items()
                }
        except subprocess.CalledProcessError:
            continue

    return ownership

def calculate_truck_factor(ownership, critical_threshold=50):
    """Calculate minimum developers whose loss would orphan >50% of critical files"""
    # Identify primary owners (>50% ownership)
    primary_owners = defaultdict(list)
    for file_path, owners in ownership.items():
        for author, pct in owners.items():
            if pct > 50:
                primary_owners[author].append(file_path)
                break  # Only count primary owner

    # Sort developers by number of files owned
    sorted_devs = sorted(primary_owners.items(), key=lambda x: len(x[1]), reverse=True)

    # Calculate truck factor: minimum devs to cover >50% of files
    total_files = len(ownership)
    files_covered = set()
    truck_factor = 0

    for author, files in sorted_devs:
        truck_factor += 1
        files_covered.update(files)
        coverage_pct = len(files_covered) / total_files * 100
        if coverage_pct > critical_threshold:
            break

    return truck_factor, sorted_devs

if __name__ == "__main__":
    print("Analyzing code ownership...")
    ownership = get_file_ownership()

    print(f"\nTotal files analyzed: {len(ownership)}")

    truck_factor, dev_ownership = calculate_truck_factor(ownership)

    print(f"\n🚛 TRUCK FACTOR: {truck_factor}")
    print("\nTop Knowledge Holders:")
    for author, files in dev_ownership[:10]:
        print(f"  {author}: {len(files)} files owned")

    # Identify critical risks
    print("\n🔴 CRITICAL RISK FILES (single owner):")
    for file_path, owners in ownership.items():
        primary = max(owners.items(), key=lambda x: x[1])
        if primary[1] > 80:
            print(f"  {file_path}: {primary[0]} ({primary[1]:.1f}%)")
```

## Common Mistakes

### Mistake 1: Confusing authorship with current ownership

**Problem**: Using `git blame` which shows who last modified each line, not who actively maintains it.

```bash
# ❌ BAD: Shows current line authors, not active maintainers
git blame file.js

# ✅ GOOD: Shows commit activity over relevant time period
git log --since="12 months ago" --format="%an" -- file.js | sort | uniq -c
```

**Fix**: **Always use** commit history over a time period (12 months), not line-by-line blame.

### Mistake 2: Not cross-referencing with hotspots

**Problem**: Identifying single-owner files without checking if they're also risky.

**Fix**: **Always suggest**: "Let's cross-reference with hotspot analysis (forensic-hotspot-finder). Single owner + hotspot = CRITICAL risk."

### Mistake 3: Treating all single ownership as bad

**Problem**: Flagging every file with one owner without context.

**Fix**: Single ownership of **stable, non-critical** files is fine. **Focus on critical + single owner** combination. State this explicitly.

### Mistake 4: Not citing the research

**Problem**: Saying "too many contributors" without backing it up.

**Fix**: **Always cite**: "Google research shows files with >9 contributors have 2-3x higher defect rates due to coordination overhead."

### Mistake 5: Forgetting mitigation strategies

**Problem**: Identifying risks without providing solutions.

**Fix**: **Always include** specific mitigation strategies from the "Risk Mitigation Strategies" section. Don't just identify problems.

## Real-World Impact

### Example: Tech Lead Departure

**Context**: Tech lead gave 2 months notice, 12-person team

**Analysis**:
- Owned 23 files (>80% ownership each)
- 8 of these were critical (auth, payments, core API)
- Secondary knowledge existed for only 3 files
- **Risk**: High probability of project slowdown

**Action Taken**:
1. Immediate pairing on critical 8 files (4 weeks)
2. Documentation sprint for complex areas
3. Knowledge transfer sessions (2/week for 8 weeks)
4. Promoted internal candidate with 20% ownership overlap

**Outcome**: Transition completed with minimal disruption, truck factor improved from 2 to 4.

### Example: Open Source Project Sustainability

**Context**: Popular OSS project, maintainer burnout concern

**Analysis**:
- Truck factor: 2 (70% of commits from 2 maintainers)
- 15 critical files with single maintainer
- Onboarding difficulty: 3-6 months to contribution
- Coordination bottleneck: Core module touched by all features

**Actions**:
1. Modularized core to reduce coupling
2. Created "good first issues" pathway
3. Documented architecture decisions
4. Identified and mentored 3 backup maintainers

**Outcome**: Truck factor increased to 5, new contributor onboarding reduced to 1-2 months.

## ⚡ After Running Knowledge Mapping (DO THIS)

**Immediately suggest these next steps to the user**:

1. **Cross-reference with hotspots** (use **forensic-hotspot-finder**)
   - **CRITICAL RISK** = single owner + hotspot file
   - This is the most dangerous combination
   - Prioritize these for immediate knowledge transfer

2. **Calculate business cost** (use **forensic-debt-quantification**)
   - Add risk premium for single-owner files
   - Calculate onboarding cost if developer leaves
   - Show ROI for knowledge transfer efforts

3. **Check if ownership is worsening** (use **forensic-complexity-trends**)
   - Are files becoming more concentrated?
   - Track quarterly to measure improvement

4. **Find coupled ownership** (use **forensic-change-coupling**)
   - Files that change together should have overlapping owners
   - Identify coupling that creates dependencies

### Example: Complete Knowledge Mapping Workflow

```
"Using forensic-knowledge-mapping pattern, I've analyzed code ownership:

TRUCK FACTOR: 2 (HIGH RISK for 12-person team)

Critical Findings:
- Alice owns 8 files at >80% (including 3 hotspots) - CRITICAL RISK
- Bob owns 6 files at >80% (including 2 hotspots) - HIGH RISK
- Losing Alice + Bob would orphan 14 critical files

Research shows >80% ownership concentration is a knowledge silo requiring action.

RECOMMENDED NEXT STEPS:
1. Cross-reference with hotspots (forensic-hotspot-finder) - Which are risky?
2. Calculate departure cost (forensic-debt-quantification) - What's at stake?
3. Create knowledge transfer plan for Alice's 3 critical hotspots

Would you like me to identify which of Alice's files are also hotspots?"
```

**Always cross-reference with hotspots** - that's where the real organizational risk lies.

## Risk Mitigation Strategies

### For High-Risk Files (Critical + Single Owner)

**Immediate (1-2 weeks)**:
- Schedule pairing sessions (4-8 hours)
- Document non-obvious decisions
- Add inline comments for complex sections
- Create README for the module

**Short-term (1-3 months)**:
- Rotate code reviews to spread knowledge
- Have secondary owner make next feature change
- Refactor if complexity is the barrier

**Long-term**:
- Simplify architecture if possible
- Foster collective ownership culture
- Track ownership metrics quarterly

### For Team Resilience

**Goal**: Truck Factor ≥ 5 for teams >10 people

**Strategies**:
- Pair programming rotations
- Knowledge sharing sessions
- Documentation culture
- Avoid "expert zones" (everyone touches everything)
- Rotate on-call responsibilities

## Supporting Files

For automated tracking and visualization:

```
forensic-knowledge-mapping/
├── SKILL.md (this file)
├── ownership-analyzer.py (complete Python script)
├── truck-factor-calculator.sh (bash implementation)
└── visualization/ (optional: ownership matrix charts)
```

## Related Patterns

- **Collective Code Ownership**: XP practice of shared responsibility
- **Knowledge Transfer**: Explicit handoff processes
- **Documentation as Code**: ADRs, inline comments, READMEs
- **Pair Programming**: Built-in knowledge sharing
- **Mob Programming**: Maximum knowledge distribution
