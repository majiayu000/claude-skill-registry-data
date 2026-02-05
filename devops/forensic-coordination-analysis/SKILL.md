---
name: forensic-coordination-analysis
description: Use when investigating merge conflicts, reducing communication overhead, detecting modules with high coordination complexity, or identifying files edited by many contributors and cross-team - reveals coordination bottlenecks and team communication issues
---

# Forensic Coordination Analysis

## 🎯 When You Use This Skill

**State explicitly**: "Using forensic-coordination-analysis pattern"

**Then follow these steps**:
1. Count **unique contributors** per file (threshold: >9 = high risk)
2. Identify **cross-team hotspots** (files edited by multiple teams)
3. Detect **concurrent edit patterns** (multiple developers within 1 week)
4. Cite **research** when presenting findings (>9 contributors = 2-3x defect rate)
5. Suggest **integration** with knowledge-mapping and organizational-alignment at end

## Overview

Coordination analysis identifies files and modules requiring high levels of team coordination. Research shows coordination issues predict defects better than code complexity alone. This analysis reveals:
- **High-contributor files** - Too many people editing the same code
- **Cross-team coordination** - Files edited by multiple teams
- **Concurrent edits** - Overlapping work causing merge conflicts
- **Contributor churn** - High turnover indicating instability
- **Communication bottlenecks** - Where team coordination breaks down

**Core principle**: More contributors = more coordination overhead = higher defect risk. Files with >9 contributors have 2-3x higher bug rates.

## When to Use

- Investigating frequent merge conflicts in specific areas
- Reducing team communication overhead
- Planning team reorganizations (Conway's Law)
- Identifying files needing clear ownership
- Post-mortem analysis of coordination failures
- Quarterly health checks on team collaboration
- Before splitting teams or services

## When NOT to Use

- Insufficient git history (<6 months unreliable)
- Small team (<3 people, coordination not an issue)
- Greenfield projects (no patterns yet)
- When you need bug prediction (use hotspot analysis instead)
- For understanding code dependencies (use coupling analysis)

## Core Pattern

### ⚡ THE COORDINATION THRESHOLD (USE THIS)

**This is the research-backed contributor threshold - don't use arbitrary numbers**:

```
Coordination Risk = Unique Contributors (12 months)

Risk Thresholds:
  - >9 contributors:  CRITICAL (2-3x higher defect rate - Google Research)
  - 6-9 contributors: HIGH (elevated coordination overhead)
  - 3-5 contributors: MODERATE (manageable with communication)
  - 1-2 contributors: LOW (minimal coordination needed)

Concurrent Edit Risk = Developers editing within 7-day window

Cross-Team Risk = Number of different teams contributing
  - 3+ teams: HIGH (requires formal coordination)
  - 2 teams:  MODERATE (requires communication)
  - 1 team:   LOW (internal team coordination)
```

**Critical**: Always check for BOTH high contributors AND cross-team involvement for maximum risk.

### 📊 Research Benchmarks (CITE THESE)

**Always reference the research when presenting coordination findings**:

| Finding | Impact | Source | When to Cite |
|---------|--------|--------|--------------|
| High contributors | **2-3x** higher defect rate | Google Research | "Research shows >9 contributors correlates with 2-3x defect rate (Google)" |
| Cross-team changes | **40-60%** slower velocity | Microsoft DevOps | "Cross-team coordination reduces velocity by 40-60% (Microsoft)" |
| Contributor churn | **35-50%** higher bugs | Software Engineering Studies | "High contributor turnover increases bugs by 35-50%" |

**Always cite the source** when presenting coordination hotspots to justify process or organizational changes.

## Quick Reference

### Essential Git Commands

| Purpose | Command |
|---------|---------|
| **Count contributors** | `git log --since="12 months ago" --format="%an" -- FILE \| sort -u \| wc -l` |
| **List contributors** | `git log --since="12 months ago" --format="%an" -- FILE \| sort \| uniq -c \| sort -rn` |
| **Find high-contributor files** | `for f in $(git ls-files); do echo "$(git log --since="12 months ago" --format="%an" -- "$f" \| sort -u \| wc -l)\|$f"; done \| sort -rn \| head -20` |
| **Concurrent edits** | `git log --since="12 months ago" --format="%ad\|%an" --date=short -- FILE` |

### Risk Classification

| Contributors | Team Count | Concurrent Edits | Risk | Action |
|--------------|------------|------------------|------|--------|
| **>9** | 3+ | High | CRITICAL | Urgent: Assign ownership, refactor |
| **6-9** | 2-3 | Medium | HIGH | Establish ownership, improve docs |
| **3-5** | 1-2 | Low | MODERATE | Monitor, maintain communication |
| **1-2** | 1 | None | LOW | Normal maintenance |

### Coordination Complexity Score

| Score | Level | Meaning | Action |
|-------|-------|---------|--------|
| **9-10** | CRITICAL | Severe coordination overhead | Immediate restructuring |
| **7-8** | HIGH | Significant coordination needs | Establish protocols |
| **4-6** | MODERATE | Manageable coordination | Monitor trends |
| **0-3** | LOW | Minimal coordination | Normal state |

## Implementation

### Step 1: Identify High-Contributor Files

**For each file in codebase**:

```bash
# Find files with >9 contributors (last 12 months)
for file in $(git ls-files "*.js" "*.ts" "*.py" "*.go"); do
  contributor_count=$(git log --since="12 months ago" --format="%an" -- "$file" | sort -u | wc -l)

  if [ $contributor_count -gt 9 ]; then
    echo "CRITICAL: $file - $contributor_count contributors"
  elif [ $contributor_count -gt 6 ]; then
    echo "HIGH: $file - $contributor_count contributors"
  fi
done | sort -rn
```

**Priority**: Files with >9 contributors are CRITICAL (research-backed threshold).

### Step 2: Detect Cross-Team Coordination

**If team mapping available**:

```python
# Pseudocode for cross-team detection

# Map contributors to teams
team_mapping = {
    "Alice": "Backend",
    "Bob": "Frontend",
    "Carol": "Platform",
    # ...
}

def analyze_cross_team_coordination(file):
    contributors = git_log_contributors(file, since="12 months ago")

    teams = set()
    for contributor in contributors:
        team = team_mapping.get(contributor, "Unknown")
        teams.add(team)

    if len(teams) >= 3:
        return "CRITICAL - Cross-team coordination bottleneck"
    elif len(teams) == 2:
        return "HIGH - Requires cross-team communication"
    else:
        return "LOW - Single team ownership"
```

**Why it matters**: Cross-team coordination requires formal communication, slowing velocity by 40-60%.

### Step 3: Find Concurrent Edit Patterns

**Identify merge conflict risk**:

```python
# Detect multiple developers editing within 7-day window

def find_concurrent_edits(file, window_days=7):
    commits = git_log_with_dates(file, since="12 months ago")

    # Group by week
    weeks = defaultdict(list)
    for commit in commits:
        week_key = commit.date.strftime("%Y-W%U")
        weeks[week_key].append(commit.author)

    # Find weeks with multiple authors
    concurrent_weeks = []
    for week, authors in weeks.items():
        unique_authors = set(authors)
        if len(unique_authors) > 2:
            concurrent_weeks.append({
                'week': week,
                'authors': unique_authors,
                'commit_count': len(authors),
                'risk': 'HIGH' if len(unique_authors) > 3 else 'MODERATE'
            })

    return concurrent_weeks
```

**Interpretation**: >3 developers in same week = high merge conflict risk.

### Step 4: Calculate Coordination Complexity Score

**Weighted formula**:

```python
def calculate_coordination_score(file_metrics):
    # Weights based on impact
    contributor_weight = 0.40  # 40% - primary factor
    team_diversity_weight = 0.30  # 30% - cross-team overhead
    concurrent_edits_weight = 0.20  # 20% - conflict risk
    churn_weight = 0.10  # 10% - instability

    # Normalize each factor to 0-10 scale
    contributor_score = min(file_metrics.contributor_count / 10, 1.0) * 10
    team_score = min(file_metrics.team_count / 4, 1.0) * 10
    concurrent_score = min(file_metrics.concurrent_events / 5, 1.0) * 10
    churn_score = file_metrics.contributor_churn_rate * 10

    # Weighted sum
    coordination_score = (
        contributor_score * contributor_weight +
        team_score * team_diversity_weight +
        concurrent_score * concurrent_edits_weight +
        churn_score * churn_weight
    )

    return coordination_score  # 0-10 range
```

**Thresholds**: >9 = CRITICAL, 7-8 = HIGH, 4-6 = MODERATE, 0-3 = LOW

## Output Format

### 1. Executive Summary

```
Coordination Analysis (forensic-coordination-analysis pattern)

Files Analyzed: 487
Coordination Hotspots: 23 (5% of codebase)
Critical (>9 contributors): 5 files
High (6-9 contributors): 12 files
Cross-Team Hotspots: 8 files

Research shows >9 contributors correlates with 2-3x defect rate (Google).
```

### 2. Top Coordination Hotspots Table

```
Rank | File                  | Contributors | Teams | Concurrent | Churn  | Risk
-----|----------------------|--------------|-------|------------|--------|----------
1    | core/config.js       | 14           | 4     | 8 events   | HIGH   | CRITICAL
2    | api/v1/users.js      | 11           | 3     | 5 events   | MED    | CRITICAL
3    | models/user.js       | 9            | 2     | 12 events  | HIGH   | HIGH
4    | utils/validation.js  | 8            | 3     | 3 events   | LOW    | HIGH
```

### 3. Detailed Hotspot Analysis

```
=== HOTSPOT #1: core/config.js ===

Coordination Metrics:
  Contributors (12mo): 14 (CRITICAL - exceeds threshold of 9)
  Teams Involved: 4 (Backend, Frontend, Platform, QA)
  Total Commits: 67
  Concurrent Edit Events: 8 (multiple developers within 1 week)
  Contributor Churn: HIGH (7 new contributors in 6 months)
  Coordination Score: 8.5/10 (HIGH)

Research: >9 contributors correlates with 2-3x defect rate (Google).

Top Contributors:
  1. Alice (Backend):  25 commits (37%)
  2. Bob (Frontend):   18 commits (27%)
  3. Carol (Platform): 12 commits (18%)
  4. +11 other contributors (18%)

Risk Factors:
  ⚠️  Too many contributors (14 vs threshold 9)
  ⚠️  Multiple teams editing same file
  ⚠️  High concurrent edit frequency
  ⚠️  No clear ownership (largest share: 37%)

Recent Concurrent Edit (Oct 2024):
  - Oct 1: Alice added config key
  - Oct 2: Bob refactored structure
  - Oct 3: Carol added validation
  → Likely merge conflicts or coordination needed

RECOMMENDATIONS:
  1. IMMEDIATE: Assign Backend team as primary owner
  2. SHORT-TERM: Implement config schema validation
  3. MEDIUM-TERM: Split into domain-specific modules
  4. PROCESS: Require cross-team review for changes
  5. COMMUNICATION: Create #config-changes channel
```

### 4. Cross-Team Coordination Matrix

```
Files with Multi-Team Involvement:

File                | Team A    | Team B   | Team C   | Velocity Impact
--------------------|-----------|----------|----------|------------------
api/users.js        | Frontend  | Backend  | Mobile   | -60% (Microsoft)
models/user.js      | Backend   | Platform | -        | -40%
core/config.js      | All teams | -        | -        | -60% (CRITICAL)

Research: Cross-team coordination reduces velocity by 40-60% (Microsoft).
```

## Common Mistakes

### Mistake 1: Not checking contributor threshold

**Problem**: Flagging all files with >3 contributors without using research-backed threshold.

```bash
# ❌ BAD: Arbitrary threshold
flag all files with >3 contributors

# ✅ GOOD: Research-backed threshold
flag files with >9 contributors (CRITICAL)
flag files with 6-9 contributors (HIGH)
```

**Fix**: **Always use >9 contributor threshold** from Google Research showing 2-3x defect correlation.

### Mistake 2: Ignoring cross-team coordination

**Problem**: Only counting total contributors, missing cross-team overhead.

```bash
# ❌ BAD: Just contributor count
if contributors > 9:
    flag_as_hotspot()

# ✅ GOOD: Check cross-team involvement
if contributors > 9 OR team_count >= 3:
    flag_as_coordination_hotspot()
    check_velocity_impact()  # 40-60% reduction
```

**Fix**: **Always flag cross-team files** (3+ teams) even if contributor count is moderate.

### Mistake 3: Not tracking concurrent edits

**Problem**: Missing merge conflict patterns from temporal analysis.

```bash
# ❌ BAD: Only historical count
count_total_contributors()

# ✅ GOOD: Detect concurrent patterns
find_weeks_with_multiple_authors()
flag_concurrent_edit_risk()
```

**Fix**: **Always analyze temporal patterns** - concurrent edits within 7 days = merge conflict risk.

### Mistake 4: Not suggesting ownership changes

**Problem**: Identifying hotspots without recommending who should own the code.

**Fix**: For every coordination hotspot, recommend:
- Primary team owner (based on largest contribution %)
- Cross-team review process if multi-team
- Refactoring to reduce coordination needs

## ⚡ After Running Coordination Analysis (DO THIS)

**Immediately suggest these next steps to the user**:

1. **Map ownership patterns** (use **forensic-knowledge-mapping**)
   - High coordination + single owner leaving = disaster scenario
   - Identify which hotspots are also knowledge silos
   - Calculate truck factor for coordination hotspots

2. **Check organizational alignment** (use **forensic-organizational-alignment**)
   - Coordination hotspots = Conway's Law violations
   - Architecture may not match team structure
   - Suggest team/architecture realignment

3. **Correlate with defect data** (if available)
   - Validate 2-3x defect rate prediction
   - Prioritize hotspots with actual bug history
   - Use for executive justification

4. **Track coordination trends** (re-run monthly)
   - Is coordination increasing or decreasing?
   - Are process changes working?
   - Early warning system for emerging hotspots

### Example: Complete Coordination Analysis Workflow

```
"Using forensic-coordination-analysis pattern, I analyzed 487 files.

COORDINATION HOTSPOTS FOUND:

CRITICAL: core/config.js
  Contributors: 14 (exceeds threshold of 9)
  Teams: 4 (Backend, Frontend, Platform, QA)
  Concurrent Edits: 8 events in 12 months
  Coordination Score: 8.5/10

Research shows >9 contributors correlates with 2-3x defect rate (Google).

Cross-Team Impact: 4 teams editing = 60% velocity reduction (Microsoft).

RECOMMENDATIONS:
1. Assign Backend team as primary owner (currently 37% Alice)
2. Establish cross-team review process
3. Split into domain-specific config modules

NEXT STEPS:
1. Map ownership (forensic-knowledge-mapping) - Is Alice the only expert?
2. Check team alignment (forensic-organizational-alignment) - Conway's Law violation?
3. Correlate with bugs - Validate 2-3x defect prediction
4. Track monthly - Set up coordination monitoring

Would you like me to proceed with the ownership mapping?"
```

**Always provide this integration guidance** - coordination issues often indicate deeper organizational or architectural problems.

## Advanced Patterns

### Contributor Churn Analysis

**Track stability over time**:

```
File: legacy/payment.js

Q1 2024: Alice, Bob (stable)
Q2 2024: Carol, Dave (Alice/Bob left) ← CHURN EVENT
Q3 2024: Eve, Frank (Carol left) ← INSTABILITY
Q4 2024: Grace, Henry (Dave left) ← CRITICAL

Pattern: High turnover, no stable ownership
Impact: 35-50% higher bugs (research)
Recommendation: Establish stable ownership or deprecate
```

### Coordination + Hotspot Intersection

**Most critical combination**:

```
CRITICAL INTERSECTION:

core/config.js:
  - Coordination: 14 contributors (CRITICAL)
  - Hotspot: 67 commits, high complexity
  - Cross-team: 4 teams involved

Combined Risk: EXTREME
  - 2-3x defects from coordination (Google)
  - 4-9x defects from hotspot (Microsoft)
  - Estimated: 8-27x normal defect rate

URGENT ACTION REQUIRED
```

### Team Handoff Patterns

**Detect when teams stop/start editing**:

```
File: api/v1/users.js

Jan-Jun: Backend team (35 commits)
Jul-Dec: Frontend team took over (28 commits)

Pattern: Team handoff occurred (July)
Risk: Knowledge transfer gap
Recommendation: Ensure handoff documentation
```

## Research Background

**Key studies**:

1. **Google Research** (2011): Organizational metrics as defect predictors
   - >9 contributors = 2-3x higher defect rate
   - More predictive than code complexity
   - Recommendation: Use 9 as critical threshold

2. **Microsoft DevOps Research** (2016): Cross-team coordination cost
   - 40-60% slower velocity with cross-team changes
   - Formal communication overhead
   - Recommendation: Minimize cross-team dependencies

3. **Herbsleb & Mockus** (2003): Conway's Law empirical validation
   - Architecture mirrors organization structure
   - Coordination issues = architectural misalignment
   - Recommendation: Align teams with module boundaries

4. **Nagappan et al** (2008): Organizational complexity metrics
   - Number of developers > code complexity for defect prediction
   - Contributor churn increases bugs 35-50%
   - Recommendation: Track organizational metrics alongside code metrics

**Why coordination matters more than code**: Social factors (communication, coordination) predict bugs better than technical factors (complexity, LOC).

## Integration with Other Techniques

**Combine coordination analysis with**:

- **forensic-knowledge-mapping**: Coordination + single owner = critical knowledge silo
- **forensic-organizational-alignment**: Coordination hotspots reveal Conway's Law violations
- **forensic-hotspot-finder**: Coordination + change frequency = highest defect risk
- **forensic-refactoring-roi**: Coordination overhead = quantifiable velocity cost

**Why**: Coordination issues are organizational problems, not just technical problems. Integration reveals whether to fix with process, architecture, or team changes.
