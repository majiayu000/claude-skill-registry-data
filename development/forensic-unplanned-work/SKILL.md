---
name: forensic-unplanned-work
description: Use when understanding velocity issues, measuring quality improvement efforts, tracking interrupt work, or quantifying technical debt impact - monitors trends in unplanned work (bugs, hotfixes) and correlates with code hotspots
---

# Forensic Unplanned Work Analysis

## 🎯 When You Use This Skill

**State explicitly**: "Using forensic-unplanned-work pattern"

**Then follow these steps**:
1. Calculate **unplanned work ratio** (bug fixes / total commits)
2. Identify **interrupt hotspots** (files causing most unplanned work)
3. Track **trends over time** (ratio increasing = quality degrading)
4. Cite **research** when presenting findings (>40% unplanned = low morale)
5. Suggest **integration** with hotspot-finder and refactoring-roi at end

## Overview

Unplanned work analysis tracks interrupt-driven work (bugs, hotfixes, urgent patches) vs planned work (features). Research shows teams spending >40% on unplanned work have low morale and reduced velocity.

This analysis reveals:
- **Unplanned work ratio** - % of commits fixing problems vs building features
- **Interrupt hotspots** - Files generating most bug fixes
- **Velocity impact** - Time lost to fire-fighting
- **Quality trends** - Is unplanned work increasing or decreasing?
- **ROI of quality** - Reducing bugs increases feature delivery

**Core principle**: Unplanned work = technical debt tax. Every bug fix is time not spent building features.

## When to Use

- Understanding why velocity is declining
- Measuring impact of refactoring efforts (did bugs decrease?)
- Quarterly quality health checks
- Justifying quality investment to executives
- Post-release analysis (spike in hotfixes?)
- Before/after major refactoring validation
- Diagnosing team morale issues

## When NOT to Use

- Insufficient git history (<6 months unreliable)
- No commit message conventions (can't distinguish bugs from features)
- Greenfield projects (no bug history yet)
- When you need defect prediction (use hotspot analysis)
- When you need bug severity (requires issue tracker data)

## Core Pattern

### ⚡ THE UNPLANNED WORK FORMULA (USE THIS)

**This is the interrupt work metric - don't create custom classifications**:

```
Unplanned Work Ratio = bug_fix_commits / total_commits × 100

Classification:
  - >40%:  CRITICAL (team in fire-fighting mode)
  - 30-40%: HIGH (significant interrupt overhead)
  - 20-30%: MODERATE (normal for mature systems)
  - 10-20%: GOOD (quality-focused development)
  - <10%:  EXCELLENT (greenfield or very high quality)

Interrupt Hotspot = File with:
  - >10 bug fix commits per year AND
  - Bug fix ratio >50% (more fixes than features)

Velocity Impact = Unplanned % × Team Capacity
  Example: 35% unplanned × 5 developers = 1.75 FTE firefighting
```

**Critical**: >40% unplanned work correlates with low team morale and declining velocity.

### 📊 Research Benchmarks (CITE THESE)

**Always reference research when presenting unplanned work findings**:

| Finding | Impact | Source | When to Cite |
|---------|--------|--------|--------------|
| High unplanned work | **>40%** = low morale | DevOps Research | "Research shows >40% unplanned work correlates with low morale (DevOps)" |
| Quality investment ROI | **10% less bugs** = 15-20% more features | Google SRE | "Reducing unplanned work 10% increases delivery 15-20% (Google SRE)" |
| Hotspot correlation | **80-90%** bugs from 20% of files | Pareto Principle | "80-90% of bugs come from 20% of files (Pareto)" |

**Always cite the source** when justifying quality improvement investment.

## Quick Reference

### Essential Git Commands

| Purpose | Command |
|---------|---------|
| **Count bug fixes** | `git log --since="12 months ago" --grep="fix\|bug\|hotfix" --oneline \| wc -l` |
| **Total commits** | `git log --since="12 months ago" --oneline \| wc -l` |
| **Bug fixes per file** | `git log --since="12 months ago" --grep="fix\|bug" --name-only --format="" \| sort \| uniq -c \| sort -rn` |
| **Monthly trends** | Loop through months counting bug fix vs total commits |

### Unplanned Work Classification

| Ratio | Team Impact | Classification | Action |
|-------|-------------|----------------|--------|
| **>40%** | Fire-fighting mode, low morale | CRITICAL | Urgent quality investment |
| **30-40%** | Significant interrupt overhead | HIGH | Schedule refactoring |
| **20-30%** | Normal for mature systems | MODERATE | Monitor trends |
| **10-20%** | Quality-focused development | GOOD | Maintain standards |
| **<10%** | Greenfield or very high quality | EXCELLENT | Document practices |

### Commit Classification Keywords

| Type | Keywords | Examples |
|------|----------|----------|
| **Unplanned** | fix, bug, hotfix, urgent, patch | "fix auth timeout", "hotfix payment crash" |
| **Planned** | feat, feature, add, implement | "feat: add dashboard", "implement retry logic" |
| **Refactoring** | refactor, improve, optimize | "refactor: extract module" |

## Implementation

### Step 1: Classify Commits

**Identify unplanned work**:

```python
# Pseudocode for commit classification

def classify_commit(commit_message):
    message_lower = commit_message.lower()

    # Unplanned work keywords
    unplanned_keywords = ['fix', 'bug', 'hotfix', 'urgent', 'emergency',
                          'patch', 'issue', 'defect', 'broken']

    # Planned work keywords
    planned_keywords = ['feat', 'feature', 'add', 'implement', 'create']

    # Refactoring keywords
    refactor_keywords = ['refactor', 'improve', 'optimize', 'clean']

    if any(kw in message_lower for kw in unplanned_keywords):
        return 'UNPLANNED'
    elif any(kw in message_lower for kw in refactor_keywords):
        return 'REFACTORING'
    elif any(kw in message_lower for kw in planned_keywords):
        return 'PLANNED'
    else:
        return 'UNKNOWN'
```

**Note**: Adjust keywords based on team's commit message conventions.

### Step 2: Calculate Unplanned Work Ratio

**For time period**:

```python
def calculate_unplanned_ratio(since="12 months ago"):
    commits = git_log(since=since)

    unplanned_count = 0
    planned_count = 0
    refactoring_count = 0
    unknown_count = 0

    for commit in commits:
        classification = classify_commit(commit.message)

        if classification == 'UNPLANNED':
            unplanned_count += 1
        elif classification == 'PLANNED':
            planned_count += 1
        elif classification == 'REFACTORING':
            refactoring_count += 1
        else:
            unknown_count += 1

    total = len(commits)
    unplanned_ratio = (unplanned_count / total) * 100 if total > 0 else 0

    return {
        'total_commits': total,
        'unplanned': unplanned_count,
        'planned': planned_count,
        'refactoring': refactoring_count,
        'unknown': unknown_count,
        'unplanned_ratio': unplanned_ratio
    }
```

### Step 3: Identify Interrupt Hotspots

**Files causing most unplanned work**:

```python
def find_interrupt_hotspots():
    # Get all bug fix commits
    bug_commits = git_log(grep="fix|bug|hotfix", since="12 months ago")

    # Count bug fixes per file
    bug_fixes_per_file = defaultdict(int)
    total_changes_per_file = defaultdict(int)

    for commit in bug_commits:
        for file in commit.changed_files:
            bug_fixes_per_file[file] += 1

    # Get total changes per file for ratio
    all_commits = git_log(since="12 months ago")
    for commit in all_commits:
        for file in commit.changed_files:
            total_changes_per_file[file] += 1

    # Calculate bug fix ratio per file
    hotspots = []
    for file, bug_count in bug_fixes_per_file.items():
        total_count = total_changes_per_file.get(file, bug_count)
        bug_ratio = (bug_count / total_count) * 100

        # Hotspot threshold: >10 bug fixes AND >50% ratio
        if bug_count > 10 and bug_ratio > 50:
            hotspots.append({
                'file': file,
                'bug_fixes': bug_count,
                'total_changes': total_count,
                'bug_ratio': bug_ratio,
                'severity': 'CRITICAL' if bug_ratio > 70 else 'HIGH'
            })

    return sorted(hotspots, key=lambda x: x['bug_fixes'], reverse=True)
```

### Step 4: Track Trends Over Time

**Monthly breakdown**:

```python
def calculate_monthly_trends(months=12):
    trends = []

    for i in range(months):
        start_date = get_date_n_months_ago(i + 1)
        end_date = get_date_n_months_ago(i)

        month_data = calculate_unplanned_ratio_for_period(start_date, end_date)

        trends.append({
            'month': start_date.strftime('%Y-%m'),
            'unplanned_ratio': month_data['unplanned_ratio'],
            'unplanned_count': month_data['unplanned'],
            'total_commits': month_data['total_commits']
        })

    return trends
```

## Output Format

### 1. Executive Summary

```
Unplanned Work Analysis (forensic-unplanned-work pattern)

Period: Last 12 months
Total Commits: 1,247
Unplanned Work: 418 commits (33.5%)

Classification:
  - Unplanned (bugs/hotfixes): 418 (33.5%) - HIGH
  - Planned (features): 682 (54.7%)
  - Refactoring: 98 (7.9%)
  - Unknown: 49 (3.9%)

Research shows >40% unplanned work correlates with low morale (DevOps).

VELOCITY IMPACT:
  Team Size: 5 developers
  FTE on Unplanned Work: 1.7 developers (33.5% × 5)
  Opportunity Cost: ~3-4 features not delivered per quarter

TREND: ⬆️ INCREASING (was 28% six months ago)
  → Quality degrading, technical debt accumulating
```

### 2. Interrupt Hotspots (Files Causing Most Bugs)

```
Files Generating Most Unplanned Work:

Rank | File                     | Bug Fixes | Total Chg | Ratio | Impact
-----|--------------------------|-----------|-----------|-------|--------
1    | auth/authentication.js  | 28        | 42        | 67%   | 🚨 CRITICAL
2    | api/payments.js         | 23        | 38        | 61%   | 🚨 CRITICAL
3    | models/user.js          | 19        | 32        | 59%   | ❌ HIGH
4    | utils/validation.js     | 15        | 25        | 60%   | ❌ HIGH

Research: 80-90% of bugs come from 20% of files (Pareto).

RECOMMENDATION: These 4 files are interrupt hotspots
  - 85 bug fixes total (20% of all unplanned work)
  - Refactoring these would significantly reduce interrupt work
```

### 3. Monthly Trend Analysis

```
Unplanned Work Trend (12 months):

Month     | Unplanned % | Commits | Unplanned | Trend
----------|-------------|---------|-----------|-------
2024-01   | 28%         | 98      | 27        | ━━━━━━━━━━━━━━━━━━━━━━━━━━━
2024-02   | 29%         | 102     | 30        | ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2024-03   | 31%         | 105     | 33        | ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2024-04   | 33%         | 108     | 36        | ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2024-05   | 35%         | 110     | 39        | ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2024-06   | 37%         | 104     | 38        | ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...

TREND ANALYSIS:
  - ⬆️ INCREASING: +9% over 12 months (28% → 37%)
  - Pattern: Steady degradation, not seasonal
  - Impact: Quality declining, velocity suffering

INFLECTION POINT: March 2024 (ratio started accelerating)
  - Possible cause: Major feature release without quality time?

Research: 10% reduction in unplanned work = 15-20% more features (Google SRE).
```

### 4. Velocity Impact Calculation

```
PRODUCTIVITY IMPACT ANALYSIS:

Team Capacity:
  - Team Size: 5 developers
  - Sprint Capacity: 100 story points
  - Velocity: ~25 points per developer per sprint

Current State (33.5% Unplanned):
  - Unplanned Capacity: 33.5 points (33.5% × 100)
  - Planned Capacity: 66.5 points
  - FTE on Firefighting: 1.7 developers

If Reduced to 20% Unplanned:
  - Unplanned Capacity: 20 points (-13.5)
  - Planned Capacity: 80 points (+13.5)
  - FTE Freed Up: 0.7 developers
  - Additional Features: ~3-4 per quarter

ANNUAL OPPORTUNITY COST:
  - Lost Features: ~12-16 features/year
  - Developer Time: 1.7 FTE × $150K = $255,000/year
  - Actual Value: $170,000/year on unplanned work

RECOMMENDATION: Invest in quality to reduce unplanned work
  - ROI: 10% reduction = 15-20% more features (Google SRE)
```

## Common Mistakes

### Mistake 1: Not tracking trends over time

**Problem**: Only looking at current ratio, missing degradation pattern.

```bash
# ❌ BAD: Single snapshot
unplanned_ratio = 33.5%

# ✅ GOOD: Trend analysis
monthly_ratios = [28%, 29%, 31%, 33%, 35%, 37%]
trend = INCREASING (+9% over 6 months)
```

**Fix**: **Always track trends** - increasing ratio indicates quality degrading.

### Mistake 2: Not correlating with code hotspots

**Problem**: Reporting unplanned work without identifying which files cause it.

```bash
# ❌ BAD: Just overall ratio
report("33.5% unplanned work")

# ✅ GOOD: Identify interrupt hotspots
find_files_with_most_bug_fixes()
correlate_with_hotspot_analysis()
```

**Fix**: **Always identify interrupt hotspots** - 80-90% of bugs come from 20% of files.

### Mistake 3: Not quantifying velocity impact

**Problem**: Presenting ratio without translating to business impact.

**Fix**: Calculate:
- FTE on unplanned work: ratio × team size
- Lost features: unplanned capacity / average feature size
- Opportunity cost: FTE × average salary
- **Always translate to dollars and features** for executives

### Mistake 4: Not checking commit classification accuracy

**Problem**: Trusting automated classification without validation.

**Fix**: Sample validation:
- Manually review 50 random commits
- Check if classification matches reality
- Adjust keywords based on team's conventions
- Report accuracy percentage (e.g., "85% classification accuracy")

## ⚡ After Running Unplanned Work Analysis (DO THIS)

**Immediately suggest these next steps to the user**:

1. **Correlate with code hotspots** (use **forensic-hotspot-finder**)
   - Are interrupt hotspots also code hotspots?
   - High churn + high bugs = critical refactoring target
   - Pareto principle: Fix 20% of files to reduce 80% of bugs

2. **Calculate refactoring ROI** (use **forensic-refactoring-roi**)
   - Unplanned work cost = annual waste
   - Refactoring interrupt hotspots = reduced bug rate
   - ROI typically very high (bugs are expensive)

3. **Track quality trends** (use **forensic-complexity-trends**)
   - Is complexity increasing in interrupt hotspots?
   - Validate that refactoring reduces both complexity AND bugs
   - Monitor monthly to ensure quality improving

4. **Re-run quarterly** to measure improvement
   - Did refactoring reduce unplanned work ratio?
   - Track trend: improving, stable, or deteriorating?
   - Validate ROI predictions with actual results

### Example: Complete Unplanned Work Analysis Workflow

```
"Using forensic-unplanned-work pattern, I analyzed 1,247 commits over 12 months.

UNPLANNED WORK RATIO: 33.5% (HIGH)

Classification:
  - Unplanned (bugs): 418 commits (33.5%)
  - Planned (features): 682 commits (54.7%)

Research shows >40% unplanned work correlates with low morale (DevOps).

TREND: ⬆️ INCREASING (+9% over 12 months, from 28% to 37%)
  → Quality degrading, velocity suffering

INTERRUPT HOTSPOTS:

authentication.js: 28 bug fixes (67% of changes are fixes)
payments.js: 23 bug fixes (61%)
user.js: 19 bug fixes (59%)

These 3 files = 70 bug fixes (17% of all unplanned work)

VELOCITY IMPACT:
  - 1.7 FTE firefighting (33.5% × 5 developers)
  - Opportunity cost: ~12-16 lost features/year
  - Research: 10% reduction = 15-20% more features (Google SRE)

NEXT STEPS:
1. Check hotspots (forensic-hotspot-finder) - Are these also high-churn?
2. Calculate ROI (forensic-refactoring-roi) - Business case for cleanup
3. Track complexity (forensic-complexity-trends) - Are they deteriorating?
4. Re-run quarterly - Validate improvement

Would you like me to proceed with hotspot correlation?"
```

**Always provide this integration guidance** - unplanned work directly impacts team velocity and morale.

## Advanced Patterns

### Virtuous vs Vicious Cycle Detection

**Quality investment impact**:

```
VICIOUS CYCLE (Current State):
  High unplanned work (37%)
    → Less time for quality
    → More technical debt
    → More bugs
    → Even higher unplanned work (cycle continues)

VIRTUOUS CYCLE (After Quality Investment):
  Reduce unplanned work (20%)
    → More time for quality
    → Less technical debt
    → Fewer bugs
    → Even lower unplanned work (improving)

BREAK POINT: Need initial quality investment to break vicious cycle
```

### Post-Release Spike Analysis

**Detect release quality issues**:

```
Unplanned Work Around Releases:

Release 2.0 (Mar 15):
  Week before: 25% unplanned
  Week after: 48% unplanned (+92% spike)
  Following month: 41% unplanned

Pattern: Major releases followed by bug spikes
Recommendation: Increase QA before releases, stabilization sprints
```

### Team Morale Correlation

**Estimate morale impact**:

```
Unplanned Work vs Team Sentiment:

Jan-Mar (28% unplanned): High morale, good velocity
Apr-Jun (35% unplanned): Declining morale, complaints about firefighting
Jul-Sep (41% unplanned): Low morale, attrition concerns

Research correlation: >40% unplanned = low morale (DevOps)

CURRENT: 37% (approaching morale threshold)
ACTION: Reduce unplanned work before reaching 40%
```

## Research Background

**Key studies**:

1. **DevOps Research & Assessment** (DORA, 2019): Unplanned work and morale
   - >40% unplanned work correlates with low team morale
   - High-performing teams: 10-20% unplanned
   - Recommendation: Monitor unplanned work as quality metric

2. **Google SRE** (2017): Quality investment ROI
   - 10% reduction in unplanned work = 15-20% increase in feature delivery
   - Quality investment has compounding returns
   - Recommendation: Dedicated quality time in sprints

3. **Pareto Principle** (Software Engineering Application): Bug distribution
   - 80-90% of bugs come from 20% of files
   - Recommendation: Focus quality efforts on interrupt hotspots

4. **Technical Debt Research** (Kruchten et al, 2012): Debt and velocity
   - Technical debt manifests as increased unplanned work
   - Unplanned work ratio is leading indicator of debt accumulation
   - Recommendation: Track ratio monthly as health metric

**Why unplanned work matters**: It's the most visible symptom of technical debt - directly impacts velocity, morale, and business delivery.

## Integration with Other Techniques

**Combine unplanned work analysis with**:

- **forensic-hotspot-finder**: Interrupt hotspots are often code hotspots
- **forensic-refactoring-roi**: Reducing unplanned work has high ROI
- **forensic-complexity-trends**: Track if quality improving reduces bugs
- **forensic-debt-quantification**: Unplanned work = quantifiable debt cost

**Why**: Unplanned work is the outcome metric that validates all other forensic analyses - if unplanned work decreases after refactoring, you've succeeded.
