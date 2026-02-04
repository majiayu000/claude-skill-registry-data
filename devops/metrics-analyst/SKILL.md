---
name: Metrics Analyst
description: Collects, analyzes, and reports software metrics for data-driven decision making and continuous improvement
when_to_use: when establishing metrics, measuring quality, tracking performance, or driving process improvements
version: 1.0.0
swecom_area: "12. Software Measurement"
---

# Metrics Analyst

## Overview

The Metrics Analyst establishes measurement processes to enable data-driven decisions and continuous improvement. This skill implements the Goal-Question-Metric (GQM) approach and provides practical metrics for code quality, team performance, and process effectiveness.

## When to Use This Skill

- Establishing metrics for a project
- Measuring code quality
- Tracking team performance
- Identifying process improvements
- Preparing retrospectives with data
- Setting improvement goals

## Critical Rules

1. **Measure what matters** - Don't track metrics just because you can
2. **Avoid metric gaming** - Metrics should inform, not control behavior
3. **Context is critical** - Same metric means different things in different contexts
4. **Review regularly** - Metrics should evolve with the team

## Goal-Question-Metric (GQM) Approach

### The GQM Method

**Structure**:
```
Goal → Questions → Metrics
```

**Example**:
```
Goal: Improve code quality
  ↓
Questions:
  - How complex is our code?
  - How well is code tested?
  - How much duplication exists?
  ↓
Metrics:
  - Cyclomatic complexity
  - Code coverage
  - Code duplication percentage
```

### Defining Good Goals

**Template**:
```
Analyze [object] for the purpose of [purpose]
with respect to [quality focus]
from the viewpoint of [stakeholder]
in the context of [environment]
```

**Examples**:

1. **Quality Goal**:
   "Analyze the codebase for the purpose of improvement with respect to maintainability from the viewpoint of the development team in the context of long-term product evolution"

2. **Performance Goal**:
   "Analyze the CI/CD pipeline for the purpose of optimization with respect to deployment speed from the viewpoint of DevOps team in the context of frequent releases"

3. **Team Goal**:
   "Analyze the development process for the purpose of understanding with respect to team velocity from the viewpoint of product management in the context of sprint planning"

## Metric Categories

### 1. Code Quality Metrics

#### Cyclomatic Complexity
**Definition**: Number of linearly independent paths through code

**How to Measure**:
```bash
# JavaScript/TypeScript (using plato)
plato -r -d reports src/

# Python (using radon)
radon cc -a src/
```

**Interpretation**:
| Complexity | Risk | Action |
|------------|------|--------|
| 1-10 | Low | No action needed |
| 11-20 | Moderate | Monitor |
| 21-50 | High | Refactor |
| 50+ | Critical | Refactor immediately |

**Target**: Average <10, max <20

#### Code Coverage
**Definition**: Percentage of code executed by tests

**How to Measure**:
```bash
# Jest (JavaScript/TypeScript)
npm test -- --coverage

# pytest (Python)
pytest --cov=src tests/
```

**Interpretation**:
- <60%: Insufficient
- 60-80%: Adequate
- 80-90%: Good
- \>90%: Excellent

**Caution**: High coverage doesn't guarantee good tests
**Target**: >80% with meaningful assertions

#### Code Duplication
**Definition**: Percentage of duplicated code blocks

**How to Measure**:
```bash
# jscpd (JavaScript/TypeScript)
jscpd src/

# CPD (any language via PMD)
pmd cpd --minimum-tokens 50 --files src/
```

**Interpretation**:
- <3%: Excellent
- 3-5%: Good
- 5-10%: Moderate (needs attention)
- \>10%: Poor (refactor)

**Target**: <3%

#### Technical Debt Ratio
**Definition**: Cost to fix code issues / Development cost

**How to Measure**:
```bash
# SonarQube
sonar-scanner

# CodeClimate
codeclimate analyze
```

**Interpretation**:
- <5%: Low debt
- 5-10%: Moderate debt
- 10-20%: High debt
- \>20%: Critical debt

**Target**: <5%, trending down

#### Maintainability Index
**Definition**: Composite metric (0-100) based on complexity, LOC, volume

**Formula**:
```
MI = 171 - 5.2 * ln(HV) - 0.23 * CC - 16.2 * ln(LOC)

Where:
  HV = Halstead Volume
  CC = Cyclomatic Complexity
  LOC = Lines of Code
```

**Interpretation**:
- 0-9: Unmaintainable
- 10-19: Difficult
- 20-100: Maintainable

**Target**: >65

### 2. Process Metrics

#### Lead Time
**Definition**: Time from work started to deployed

**How to Measure**:
```sql
-- From issue tracking
SELECT
  AVG(TIMESTAMPDIFF(DAY, started_at, deployed_at)) as avg_lead_time
FROM issues
WHERE deployed_at > NOW() - INTERVAL 30 DAY;
```

**Interpretation**:
- <1 day: Excellent
- 1-3 days: Good
- 3-7 days: Moderate
- \>7 days: Slow

**Target**: Minimize while maintaining quality

#### Cycle Time
**Definition**: Time from commit to deploy

**How to Measure**:
```bash
# GitHub Actions
gh run list --limit 100 --json createdAt,updatedAt
```

**Interpretation**:
- <10 min: Excellent
- 10-30 min: Good
- 30-60 min: Moderate
- \>60 min: Slow

**Target**: <30 minutes

#### Deployment Frequency
**Definition**: How often code is deployed to production

**How to Measure**:
```sql
SELECT
  COUNT(*) / 30 as deploys_per_day
FROM deployments
WHERE deployed_at > NOW() - INTERVAL 30 DAY;
```

**DORA Levels**:
- Elite: Multiple per day
- High: Once per day to once per week
- Medium: Once per week to once per month
- Low: Less than once per month

**Target**: At least daily

#### Change Failure Rate
**Definition**: Percentage of deployments causing failures

**How to Measure**:
```sql
SELECT
  (SUM(CASE WHEN rollback = true THEN 1 ELSE 0 END) / COUNT(*)) * 100 as failure_rate
FROM deployments
WHERE deployed_at > NOW() - INTERVAL 30 DAY;
```

**DORA Levels**:
- Elite: 0-15%
- High: 16-30%
- Medium: 31-45%
- Low: >45%

**Target**: <15%

#### Mean Time to Recovery (MTTR)
**Definition**: Average time to recover from failure

**How to Measure**:
```sql
SELECT
  AVG(TIMESTAMPDIFF(MINUTE, incident_start, incident_resolved)) as mttr_minutes
FROM incidents
WHERE incident_resolved > NOW() - INTERVAL 30 DAY;
```

**DORA Levels**:
- Elite: <1 hour
- High: <1 day
- Medium: 1 day to 1 week
- Low: >1 week

**Target**: <1 hour

### 3. Team Metrics

#### Velocity
**Definition**: Story points completed per sprint

**How to Measure**:
```sql
SELECT
  sprint_number,
  SUM(story_points) as velocity
FROM completed_stories
GROUP BY sprint_number
ORDER BY sprint_number DESC
LIMIT 6;  -- Last 6 sprints
```

**Use**:
- Sprint planning
- Capacity forecasting
- Identifying trends

**Caution**: Don't compare velocity across teams

#### Pull Request Size
**Definition**: Lines changed per PR

**How to Measure**:
```bash
# GitHub CLI
gh pr list --state merged --limit 100 --json additions,deletions
```

**Interpretation**:
- <100 LOC: Small (easy to review)
- 100-500 LOC: Medium
- 500-1000 LOC: Large (hard to review)
- \>1000 LOC: Too large (split)

**Target**: <500 LOC per PR

#### Code Review Time
**Definition**: Time from PR creation to approval

**How to Measure**:
```bash
# GitHub CLI
gh pr list --state merged --limit 100 --json createdAt,mergedAt
```

**Interpretation**:
- <4 hours: Excellent
- 4-24 hours: Good
- 1-3 days: Slow
- \>3 days: Too slow

**Target**: <24 hours

#### WIP (Work in Progress)
**Definition**: Number of items being worked on simultaneously

**How to Measure**:
```sql
SELECT COUNT(*)
FROM issues
WHERE status = 'In Progress';
```

**Little's Law**: `Lead Time = WIP / Throughput`

**Target**: Minimize WIP to reduce lead time

### 4. Quality Metrics

#### Defect Density
**Definition**: Bugs per 1000 lines of code

**How to Measure**:
```sql
SELECT
  (COUNT(*) / (SELECT SUM(lines_of_code) FROM modules) * 1000) as defect_density
FROM bugs
WHERE found_in_production = true
  AND created_at > NOW() - INTERVAL 90 DAY;
```

**Interpretation**:
- <1: Excellent
- 1-5: Good
- 5-10: Moderate
- \>10: Poor

**Target**: <3 per 1000 LOC

#### Escaped Defects
**Definition**: Bugs found in production (not caught in testing)

**How to Measure**:
```sql
SELECT
  COUNT(*) as escaped_defects
FROM bugs
WHERE found_in_production = true
  AND created_at > NOW() - INTERVAL 30 DAY;
```

**Interpretation**:
- 0: Perfect (rare)
- 1-5: Excellent
- 6-15: Good
- \>15: Poor

**Target**: <5 per month

#### Test Execution Time
**Definition**: Time to run full test suite

**How to Measure**:
```bash
# Jest
npm test -- --coverage --json --outputFile=test-results.json
```

**Interpretation**:
- <5 min: Fast (run locally)
- 5-15 min: Moderate (CI only)
- 15-30 min: Slow (optimize)
- \>30 min: Too slow (parallelize)

**Target**: <10 minutes

## Metrics Dashboard Design

### Essential Dashboards

#### 1. Code Quality Dashboard
```
┌─────────────────────────────────────────┐
│  Code Quality Overview                  │
├─────────────────────────────────────────┤
│  Complexity: 12 (↓2 from last week)     │
│  Coverage: 84% (↑3% from last week)     │
│  Duplication: 2.1% (↓0.5% from last week)│
│  Tech Debt: 6% (→ unchanged)            │
│                                         │
│  [Complexity Trend Chart]               │
│  [Coverage Over Time Chart]             │
└─────────────────────────────────────────┘
```

#### 2. DORA Metrics Dashboard
```
┌─────────────────────────────────────────┐
│  DevOps Performance (DORA)              │
├─────────────────────────────────────────┤
│  Deployment Frequency: 3.2/day (Elite)  │
│  Lead Time: 2.3 hours (Elite)          │
│  MTTR: 45 min (Elite)                  │
│  Change Failure Rate: 8% (Elite)        │
│                                         │
│  [30-day trend charts for each]         │
└─────────────────────────────────────────┘
```

#### 3. Sprint Health Dashboard
```
┌─────────────────────────────────────────┐
│  Sprint 47 Health                       │
├─────────────────────────────────────────┤
│  Velocity: 42 points (on track)         │
│  Completed: 32 / 42 points              │
│  WIP: 5 items                           │
│  Blocked: 1 item                        │
│                                         │
│  [Burndown Chart]                       │
│  [Velocity Trend (6 sprints)]           │
└─────────────────────────────────────────┘
```

## Metrics Collection Process

### Step 1: Define Goals

**Template**:
```markdown
## Measurement Goal

**Objective**: [What are we trying to achieve?]
**Stakeholder**: [Who needs this information?]
**Context**: [What situation are we in?]

### Questions to Answer:
1. [Key question 1]
2. [Key question 2]
3. [Key question 3]

### Proposed Metrics:
- [Metric 1]: [How it answers question]
- [Metric 2]: [How it answers question]
```

### Step 2: Establish Baselines

**For each metric**:
1. Collect current value
2. Document context (team size, project phase)
3. Set realistic target
4. Define measurement frequency

**Example**:
```markdown
## Baseline: Code Coverage

**Current**: 68%
**Context**: 3-person team, legacy codebase (5 years old)
**Target**: 80% in 3 months
**Frequency**: Daily (automated)
**Trend**: +2% per month
```

### Step 3: Automate Collection

**Tools by Metric Type**:

**Code Quality**:
```yaml
# .github/workflows/metrics.yml
name: Code Metrics
on: [push]
jobs:
  metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run coverage
        run: npm test -- --coverage
      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@master
      - name: Upload to Codecov
        uses: codecov/codecov-action@v2
```

**DORA Metrics**:
```python
# collect_dora_metrics.py
import requests
from datetime import datetime, timedelta

def get_deployment_frequency():
    # Query CI/CD API
    response = requests.get(f"{CI_API}/deployments")
    deployments = response.json()
    return len([d for d in deployments if d['target'] == 'production'])

def get_lead_time():
    # Query issue tracker
    response = requests.get(f"{JIRA_API}/issues")
    issues = response.json()
    times = [(i['resolved'] - i['started']) for i in issues]
    return sum(times) / len(times)
```

### Step 4: Visualize and Report

**Weekly Report Template**:
```markdown
# Engineering Metrics - Week of [Date]

## Summary
- ✅ Code coverage increased to 84% (target: 80%)
- ⚠️ Lead time increased to 3.2 days (target: <3 days)
- ✅ Deployment frequency: 12 deploys (target: 10+)
- ❌ Change failure rate: 18% (target: <15%)

## Code Quality
| Metric | Current | Last Week | Target | Status |
|--------|---------|-----------|--------|--------|
| Coverage | 84% | 81% | 80% | ✅ |
| Complexity | 12 | 14 | <10 | ⚠️ |
| Duplication | 2.1% | 2.6% | <3% | ✅ |

## DORA Metrics
[Charts showing trends]

## Actions Required
1. Investigate lead time increase (check WIP limits)
2. Review last 3 failed deployments (root cause)
3. Continue complexity reduction (2 high-complexity files remain)

## Wins This Week
- Test coverage milestone achieved (80%+)
- Zero escaped defects for 3 weeks straight
- Average PR review time down to 8 hours
```

## Anti-Patterns to Avoid

### 1. Vanity Metrics
**Problem**: Metrics that look good but don't drive action

**Examples**:
- Total lines of code (more isn't better)
- Number of commits (activity ≠ productivity)
- Number of tests (without coverage/quality)

**Solution**: Focus on actionable metrics

### 2. Metric Gaming
**Problem**: Optimizing for the metric instead of the goal

**Examples**:
- Writing tests just for coverage (not quality)
- Splitting PRs artificially to reduce size
- Deploying trivial changes to increase frequency

**Solution**:
- Use multiple complementary metrics
- Review qualitatively
- Make gaming counterproductive

### 3. Analysis Paralysis
**Problem**: Too many metrics, can't decide what to do

**Solution**:
- Start with 5-7 key metrics
- Add more only if needed
- Retire metrics that don't drive action

### 4. Lack of Context
**Problem**: Comparing metrics without considering differences

**Examples**:
- Comparing velocity across teams
- Comparing coverage on legacy vs new code
- Comparing complexity across languages

**Solution**: Always provide context and trends

## Output Format

After establishing metrics:

```markdown
# Metrics Report: [Project/Team Name]

## Measurement Goals

### Goal 1: Improve Code Quality
**Stakeholder**: Engineering Team
**Context**: Preparing for scale (10x traffic expected)

**Questions**:
1. Is our code maintainable?
2. Are we introducing new technical debt?
3. Is test coverage adequate?

**Metrics**:
- Cyclomatic Complexity: 12 (target <10)
- Code Duplication: 2.1% (target <3%) ✅
- Code Coverage: 84% (target >80%) ✅
- Maintainability Index: 68 (target >65) ✅

**Status**: 3/4 targets met, complexity improving

---

## Dashboards Configured

### 1. Code Quality Dashboard
**URL**: https://sonarqube.example.com/dashboard?id=myproject
**Update Frequency**: Every commit
**Viewers**: All engineers

### 2. DORA Metrics Dashboard
**URL**: https://grafana.example.com/d/dora-metrics
**Update Frequency**: Real-time
**Viewers**: Engineering leadership, DevOps

### 3. Sprint Health Dashboard
**URL**: https://jira.example.com/dashboards/sprint-health
**Update Frequency**: Daily
**Viewers**: Product team, Scrum Master

---

## Automation Setup

### CI/CD Integration
```yaml
# Runs on every push
- Code coverage → Codecov
- Complexity analysis → SonarQube
- Security scan → Snyk
- Bundle size → BundleWatch
```

### Scheduled Reports
- **Daily**: DORA metrics to #engineering Slack
- **Weekly**: Code quality report to engineering@
- **Sprint End**: Velocity and sprint metrics to team

---

## Baseline & Targets

| Metric | Baseline | Target (3 mo) | Current | Progress |
|--------|----------|---------------|---------|----------|
| Code Coverage | 68% | 80% | 84% | ✅ Achieved |
| Complexity | 18 | 10 | 12 | ⚠️ 60% there |
| Lead Time | 5.2 days | 3 days | 3.2 days | ⚠️ Close |
| Deploy Freq | 2/week | 1/day | 1.7/day | ✅ Achieved |
| MTTR | 3 hours | 1 hour | 45 min | ✅ Achieved |

---

## Action Items

### Immediate (This Week)
- [ ] Refactor 2 high-complexity modules (target <20 complexity)
- [ ] Investigate lead time outliers (3 items >7 days)
- [ ] Add complexity gates to CI (fail if new code >20)

### Short-Term (This Month)
- [ ] Achieve <10 avg complexity
- [ ] Reduce lead time to <3 days consistently
- [ ] Document metrics playbook for new team members

### Long-Term (This Quarter)
- [ ] Establish defect prediction models
- [ ] Implement automated complexity refactoring suggestions
- [ ] Achieve Elite DORA performer status (all 4 metrics)
```

## Boundaries

**This skill does NOT**:
- Implement improvements (that's execution)
- Make decisions (metrics inform, humans decide)
- Replace qualitative assessment (complement, don't replace)

**This skill DOES**:
- Define measurement goals (GQM)
- Collect and analyze metrics
- Visualize trends
- Identify improvement opportunities
- Track progress toward goals

## Related Skills

- Code Quality Engineer (`~/.claude/skills/lifecycle/construction/code_quality/SKILL.md`) - Uses metrics to guide refactoring
- QAS Agent (`~/.claude/skills/lifecycle/testing/acceptance_testing/SKILL.md`) - Provides test metrics
- RTE Agent (`~/.claude/skills/crosscutting/configuration/release_management/SKILL.md`) - Uses DORA metrics

## Resources

### Books
- **How to Measure Anything in Software** - Douglas Hubbard
- **Accelerate** - Nicole Forsgren, Jez Humble, Gene Kim (DORA metrics)
- **Software Metrics** - Norman Fenton, James Bieman

### Tools
- SonarQube - Code quality
- Codecov - Test coverage
- Grafana - Dashboards
- Sleuth - DORA metrics
- LinearB - Engineering metrics

### Frameworks
- DORA - DevOps performance
- SPACE - Developer productivity
- GQM - Goal-Question-Metric

## Version History
- 1.0.0 (2025-10-17): Initial skill creation (SWECOM gap fill)
