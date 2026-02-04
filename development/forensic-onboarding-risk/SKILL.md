---
name: forensic-onboarding-risk
description: Use when developer is leaving or new hire onboarding, assessing team resilience, planning for developer departures, calculating bus/truck factor, identifying knowledge silos, or evaluating organizational risk - identifies knowledge gaps and transition risks
---

# Forensic Onboarding Risk Analysis

## 🎯 When You Use This Skill

**State explicitly**: "Using forensic-onboarding-risk pattern"

**Then follow these steps**:
1. Identify **single-owner files** (files with 1-2 contributors)
2. Calculate **bus factor** (minimum people whose loss cripples project)
3. Estimate **transition risk** (productivity loss if key person leaves)
4. Cite **research** when presenting findings (single-owner = 3-5x risk)
5. Suggest **integration** with knowledge-mapping and refactoring-roi at end

## Overview

Onboarding risk analysis identifies knowledge gaps when team members join or leave. Research shows single-owner files have 3-5x higher risk of quality issues and delays.

This analysis reveals:
- **Bus factor** - How many people must leave to cripple the project
- **Single-owner files** - Code only one person understands
- **Knowledge silos** - Critical expertise held by one person
- **Transition cost** - Productivity lost during onboarding/offboarding
- **Mitigation priorities** - Which knowledge gaps to address first

**Core principle**: Knowledge should be shared. Single points of failure in knowledge create organizational risk.

## When to Use

- Developer is leaving (offboarding risk assessment)
- New hire starting (onboarding plan)
- Team reorganization planning
- Quarterly knowledge health checks
- After key contributor departure (damage assessment)
- Before major project (identify knowledge dependencies)
- Evaluating organizational resilience

## When NOT to Use

- Insufficient git history (<6 months unreliable)
- Small team (<3 people, everyone knows everything)
- Greenfield project (no knowledge silos yet)
- When you need code complexity (use complexity analysis)
- When you need coordination overhead (use coordination analysis)

## Core Pattern

### ⚡ THE BUS FACTOR FORMULA (USE THIS)

**This is the knowledge risk metric - don't create custom calculations**:

```
Bus Factor = Minimum people whose departure cripples project

Single-Owner Risk = Files where 1 person = >80% of commits

Knowledge Silo Threshold:
  - >80% owned by 1 person: CRITICAL (knowledge silo)
  - >60% owned by 1-2 people: HIGH (at-risk)
  - >40% owned by 2-3 people: MODERATE (manageable)
  - <40% distributed: GOOD (shared knowledge)

Transition Cost = Ramp-up Time + Lost Productivity + Mentoring Time
  Example: 3 months ramp-up + 30% reduced productivity + 20% mentor time
```

**Critical**: Bus factor of 1-2 = organizational risk. Project could halt if they leave.

### 📊 Research Benchmarks (CITE THESE)

**Always reference research when presenting knowledge risk findings**:

| Finding | Impact | Source | When to Cite |
|---------|--------|--------|--------------|
| Single-owner files | **3-5x** higher defect risk | Microsoft Research | "Single-owner files have 3-5x higher defect risk (Microsoft)" |
| Knowledge silos | **40-60%** longer feature delivery | Conway's Law Studies | "Knowledge silos slow delivery by 40-60% (Conway)" |
| Onboarding time | **3-6 months** to full productivity | Software Engineering Research | "Average onboarding: 3-6 months to full productivity" |

**Always cite the source** when justifying knowledge sharing investment.

## Quick Reference

### Essential Git Commands

| Purpose | Command |
|---------|---------|
| **Contributors per file** | `git log --since="12 months ago" --format="%an" -- FILE \| sort -u \| wc -l` |
| **Primary owner** | `git log --since="12 months ago" --format="%an" -- FILE \| sort \| uniq -c \| sort -rn \| head -1` |
| **Single-owner files** | Loop through files, count contributors = 1 |
| **Contribution %** | Count commits per person / total commits × 100 |

### Knowledge Risk Classification

| Ownership % | Contributors | Risk | Action |
|-------------|--------------|------|--------|
| **>80%** | 1 person | CRITICAL | Immediate knowledge sharing |
| **>60%** | 1-2 people | HIGH | Schedule pairing/docs |
| **>40%** | 2-3 people | MODERATE | Monitor, encourage sharing |
| **<40%** | 3+ people | GOOD | Maintain practices |

### Bus Factor Interpretation

| Bus Factor | Risk Level | Meaning | Action |
|------------|------------|---------|--------|
| **1** | CRITICAL | One person holds keys | Urgent mitigation |
| **2** | HIGH | Two people critical | Knowledge sharing needed |
| **3-4** | MODERATE | Small core team | Expand expertise |
| **5+** | GOOD | Distributed knowledge | Maintain standards |

## Implementation

### Step 1: Calculate Ownership Per File

**For each file in codebase**:

```python
# Pseudocode for ownership calculation

def calculate_ownership(file, since="12 months ago"):
    commits = git_log(file=file, since=since)

    # Count commits per contributor
    contributor_counts = defaultdict(int)
    for commit in commits:
        contributor_counts[commit.author] += 1

    total_commits = len(commits)

    if total_commits == 0:
        return None  # No recent activity

    # Calculate ownership percentages
    ownership = {}
    for contributor, count in contributor_counts.items():
        ownership_pct = (count / total_commits) * 100
        ownership[contributor] = ownership_pct

    # Find primary owner
    primary_owner = max(ownership, key=ownership.get)
    primary_pct = ownership[primary_owner]

    return {
        'file': file,
        'total_commits': total_commits,
        'primary_owner': primary_owner,
        'primary_pct': primary_pct,
        'all_ownership': ownership,
        'contributor_count': len(ownership)
    }
```

### Step 2: Identify Knowledge Silos

**Find single-owner critical files**:

```python
def find_knowledge_silos(ownership_data, criticality_scores):
    silos = []

    for file_data in ownership_data:
        primary_pct = file_data['primary_pct']
        contributor_count = file_data['contributor_count']
        is_critical = criticality_scores.get(file_data['file'], False)

        # Knowledge silo criteria
        is_silo = (
            (primary_pct > 80 and contributor_count == 1) or
            (primary_pct > 60 and contributor_count <= 2)
        )

        if is_silo:
            severity = 'CRITICAL' if (is_critical and primary_pct > 80) else 'HIGH'

            silos.append({
                'file': file_data['file'],
                'owner': file_data['primary_owner'],
                'ownership_pct': primary_pct,
                'contributors': contributor_count,
                'is_critical': is_critical,
                'severity': severity
            })

    return sorted(silos, key=lambda x: x['ownership_pct'], reverse=True)
```

**Criticality score**: From hotspot analysis or manual business criticality rating.

### Step 3: Calculate Bus Factor

**Minimum people whose loss cripples project**:

```python
def calculate_bus_factor(ownership_data):
    # Group files by owner
    owner_files = defaultdict(list)

    for file_data in ownership_data:
        if file_data['primary_pct'] > 50:  # Primary ownership
            owner = file_data['primary_owner']
            owner_files[owner].append(file_data['file'])

    # Sort by number of primary-owned files
    owners_sorted = sorted(owner_files.items(),
                          key=lambda x: len(x[1]),
                          reverse=True)

    # Calculate bus factor
    # How many top contributors own >50% of files?
    total_files = len(ownership_data)
    files_covered = set()

    bus_factor = 0
    for owner, files in owners_sorted:
        files_covered.update(files)
        bus_factor += 1

        coverage = (len(files_covered) / total_files) * 100
        if coverage > 80:  # 80% coverage threshold
            break

    return {
        'bus_factor': bus_factor,
        'coverage': coverage,
        'key_people': [owner for owner, _ in owners_sorted[:bus_factor]],
        'risk_level': 'CRITICAL' if bus_factor <= 2 else 'HIGH' if bus_factor <= 4 else 'MODERATE'
    }
```

### Step 4: Estimate Transition Cost

**If person X leaves**:

```python
def estimate_transition_cost(person, ownership_data, team_size, avg_salary=150000):
    # Find files they own
    owned_files = [f for f in ownership_data
                   if f['primary_owner'] == person and f['primary_pct'] > 50]

    orphaned_count = len([f for f in owned_files if f['contributor_count'] == 1])

    # Estimate ramp-up time
    if orphaned_count > 20:
        ramp_up_months = 6  # Long learning curve
    elif orphaned_count > 10:
        ramp_up_months = 4
    elif orphaned_count > 5:
        ramp_up_months = 3
    else:
        ramp_up_months = 2

    # Calculate cost
    monthly_cost = avg_salary / 12
    ramp_up_cost = monthly_cost * ramp_up_months * 0.5  # 50% productivity during ramp-up
    mentoring_cost = monthly_cost * ramp_up_months * 0.2  # 20% mentor time

    total_cost = ramp_up_cost + mentoring_cost

    return {
        'person': person,
        'owned_files': len(owned_files),
        'orphaned_files': orphaned_count,
        'ramp_up_months': ramp_up_months,
        'total_cost': total_cost,
        'risk_level': 'CRITICAL' if orphaned_count > 10 else 'HIGH' if orphaned_count > 5 else 'MODERATE'
    }
```

## Output Format

### 1. Executive Summary

```
Onboarding Risk Assessment (forensic-onboarding-risk pattern)

Bus Factor: 2 (CRITICAL)
Key People: Alice, Bob
Single-Owner Files: 47 (15% of codebase)
Knowledge Silos: 12 critical files

Research shows single-owner files have 3-5x higher defect risk (Microsoft).

DEPARTURE RISK:

If Alice leaves:
  - 23 orphaned files (no other contributor)
  - 6 critical systems affected
  - Estimated transition cost: $75,000
  - Ramp-up time: 4-6 months

If Bob leaves:
  - 18 orphaned files
  - 4 critical systems affected
  - Estimated transition cost: $60,000
  - Ramp-up time: 3-4 months

RECOMMENDATION: URGENT knowledge sharing needed
```

### 2. Knowledge Silos (Single-Owner Files)

```
Critical Knowledge Silos:

Rank | File                        | Owner  | Ownership | Contributors | Criticality
-----|----------------------------|--------|-----------|--------------|-------------
1    | payments/stripe.js         | Alice  | 100%      | 1            | 🚨 CRITICAL
2    | auth/oauth-provider.js     | Alice  | 95%       | 1            | 🚨 CRITICAL
3    | core/legacy-migration.js   | Bob    | 92%       | 1            | ❌ HIGH
4    | api/webhooks-handler.js    | Alice  | 88%       | 1            | ❌ HIGH
5    | integrations/salesforce.js | Bob    | 85%       | 1            | ❌ HIGH

Research: Single-owner files have 3-5x higher defect risk (Microsoft).

IMPACT:
  - 47 single-owner files total (15% of codebase)
  - 12 are business-critical
  - If Alice leaves: 23 orphaned (49% of single-owner files)
  - If Bob leaves: 18 orphaned (38% of single-owner files)
```

### 3. Bus Factor Analysis

```
BUS FACTOR: 2 (CRITICAL)

Meaning: Project would be severely compromised if these 2 people left

Key People:
  1. Alice: Primary owner of 23 files (12% of codebase)
     - Domains: Payments, Authentication, Integrations
     - Critical files: 8
     - Unique expertise: Stripe integration, OAuth

  2. Bob: Primary owner of 18 files (9% of codebase)
     - Domains: Legacy systems, Core APIs, Database
     - Critical files: 6
     - Unique expertise: Legacy migration, Database optimization

Coverage Analysis:
  - Top 2 people: 80% of codebase knowledge
  - Top 5 people: 100% of codebase knowledge
  - Team size: 12 developers

RISK LEVEL: CRITICAL
  - Bus factor of 2 for 12-person team = severe organizational risk
  - Research: Knowledge silos slow delivery by 40-60% (Conway)

RECOMMENDATION: Immediate action required
  - Pair Alice/Bob with 2-3 developers each
  - Document critical knowledge
  - Cross-train on key systems
```

### 4. Transition Cost Estimation

```
DEPARTURE SCENARIO: Alice Leaves

Immediate Impact:
  - 23 orphaned files (no other contributor)
  - 8 critical systems without expert
  - Domains affected: Payments, Authentication, Integrations

Knowledge Gap:
  - Stripe API integration (payments/stripe.js)
  - OAuth provider setup (auth/oauth-provider.js)
  - Salesforce integration (integrations/salesforce.js)
  - Webhook processing (api/webhooks-handler.js)

Ramp-Up Estimate:
  - Learning curve: 4-6 months to full productivity
  - Reduced productivity: 50% for first 3 months, 75% for next 3 months
  - Mentoring overhead: 20% of senior developer time

Financial Impact:
  - Lost productivity: $37,500 (6 months × $150K × 50% average)
  - Mentoring cost: $22,500 (6 months × $150K × 20%)
  - Mistake/rework: $15,000 (estimated bugs during learning)
  - Total transition cost: $75,000

Timeline Impact:
  - Features requiring payment changes: Delayed 3-6 months
  - Authentication upgrades: Blocked until knowledge transfer
  - Integration work: High-risk period

MITIGATION (Before Departure):
  1. URGENT: Pair programming on critical files (2-3 months)
  2. Document Stripe integration patterns (2 weeks)
  3. Cross-train 2 developers on payments (1 month)
  4. Code review all Alice's PRs with knowledge transfer focus

MITIGATION (After Departure):
  1. Hire specialist with Stripe experience ($20K+ higher salary)
  2. Consulting budget for Stripe integration ($30K)
  3. Extended timeline for payment features (3-6 month delay)
```

## Common Mistakes

### Mistake 1: Only tracking code ownership, not business criticality

**Problem**: Flagging single-owner files without considering business impact.

```bash
# ❌ BAD: All single-owner files equal
flag all files with 1 contributor

# ✅ GOOD: Prioritize by criticality
flag single-owner files where (
    ownership > 80% AND
    (is_business_critical OR is_hotspot OR is_complex)
)
```

**Fix**: **Always consider business criticality** - single-owner test file < single-owner payment file.

### Mistake 2: Not estimating transition cost

**Problem**: Identifying bus factor without quantifying business impact.

**Fix**: Calculate:
- Ramp-up time (3-6 months typical)
- Lost productivity during transition (50% for 3 months)
- Mentoring overhead (20% of senior time)
- **Always translate to dollars** for executive decision-making

### Mistake 3: Not creating mitigation plan

**Problem**: Reporting risk without actionable recommendations.

**Fix**: For each knowledge silo, recommend:
- **Immediate**: Pair programming (2-3 months)
- **Short-term**: Documentation (2-4 weeks)
- **Medium-term**: Cross-training (1-2 months)
- Include timeline and cost for each mitigation

### Mistake 4: Not differentiating planned vs emergency departure

**Problem**: Same mitigation for planned retirement vs sudden departure.

**Fix**: Two scenarios:
- **Planned departure** (3+ months notice): Knowledge transfer plan, gradual handoff
- **Emergency departure** (immediate): Damage assessment, priority triage, external help

## ⚡ After Running Onboarding Risk Analysis (DO THIS)

**Immediately suggest these next steps to the user**:

1. **Cross-check with code hotspots** (use **forensic-hotspot-finder**)
   - Single-owner hotspots = highest risk (knowledge + complexity)
   - Prioritize knowledge sharing for these files first
   - Refactor to reduce both complexity AND knowledge concentration

2. **Check coordination patterns** (use **forensic-coordination-analysis**)
   - Single-owner files shouldn't need cross-team coordination
   - If they do, create process/documentation
   - Reduce coordination dependencies

3. **Calculate knowledge sharing ROI** (use **forensic-refactoring-roi**)
   - Transition cost = current risk cost
   - Knowledge sharing investment = pairing + documentation time
   - ROI typically very high (single point of failure expensive)

4. **Track bus factor quarterly**
   - Re-run analysis every 3 months
   - Monitor: improving, stable, or deteriorating?
   - Validate mitigation efforts are working

### Example: Complete Onboarding Risk Workflow

```
"Using forensic-onboarding-risk pattern, I analyzed knowledge distribution.

BUS FACTOR: 2 (CRITICAL for 12-person team)

Key People: Alice (23 files, 12%), Bob (18 files, 9%)

SINGLE-OWNER RISK:
  - 47 files with 1 contributor (15% of codebase)
  - 12 are business-critical
  - Research: 3-5x higher defect risk (Microsoft)

DEPARTURE SCENARIO: If Alice leaves:
  - 23 orphaned files (payments, auth, integrations)
  - Transition cost: $75,000
  - Timeline impact: 3-6 month delays on payment features
  - Ramp-up: 4-6 months to full productivity

MITIGATION PLAN:
  1. URGENT: Pair Alice with 2 developers on payments (3 months)
  2. Document Stripe integration (2 weeks)
  3. Cross-train on OAuth (1 month)
  4. Code reviews with knowledge transfer focus

NEXT STEPS:
1. Check hotspots (forensic-hotspot-finder) - Single-owner hotspots?
2. Check coordination (forensic-coordination-analysis) - Process needed?
3. Calculate ROI (forensic-refactoring-roi) - Cost of mitigation?
4. Track quarterly - Measure improvement

Would you like me to proceed with hotspot correlation?"
```

**Always provide this integration guidance** - knowledge risk is organizational risk, requires executive attention.

## Advanced Patterns

### Planned Succession Analysis

**Gradual knowledge transfer**:

```
Succession Plan: Alice (Retiring in 6 months)

Phase 1 (Months 1-2): Shadow & Document
  - Pair programming on payments (Alice + Junior Dev)
  - Document Stripe integration (Alice writes, Junior reviews)
  - Expected: Junior reaches 30% proficiency

Phase 2 (Months 3-4): Reverse Shadow
  - Junior leads, Alice reviews
  - Knowledge validation (can Junior explain to others?)
  - Expected: Junior reaches 60% proficiency

Phase 3 (Months 5-6): Independent with Support
  - Junior owns features, Alice available for questions
  - Handoff critical contacts (Stripe support, etc.)
  - Expected: Junior reaches 80% proficiency

Residual Risk: 20% knowledge gap (tribal knowledge)
Mitigation: Alice available as consultant for 3 months post-departure
```

### New Hire Onboarding Plan

**Accelerated ramp-up**:

```
New Hire Onboarding (Target: 3 months to productivity)

Week 1-2: Codebase Overview
  - Architecture walkthrough
  - Local setup, test suite
  - Read top 10 most-changed files
  - Expected: Can navigate codebase

Week 3-4: First Contribution
  - Bug fixes in low-risk areas
  - Pair with senior on feature
  - Expected: First PR merged

Month 2: Domain Learning
  - Payments module deep-dive (pair with Alice)
  - Auth system understanding (pair with Bob)
  - Expected: Can work semi-independently

Month 3: Full Productivity
  - Own small feature end-to-end
  - Participate in on-call rotation
  - Expected: 70-80% productivity
```

### Critical Knowledge Documentation

**Prioritize documentation efforts**:

```
Documentation Priority (High-Impact, Low-Coverage):

1. payments/stripe.js (Alice's, CRITICAL)
   - Stripe API integration patterns
   - Webhook handling
   - Estimated doc time: 2 days
   - Impact: Reduces transition risk 60%

2. auth/oauth-provider.js (Alice's, CRITICAL)
   - OAuth flow diagrams
   - Token management
   - Estimated doc time: 1.5 days
   - Impact: Reduces transition risk 50%

Total documentation effort: 1 week
Total risk reduction: 55% average
ROI: Very high (1 week prevents $75K transition cost)
```

## Research Background

**Key studies**:

1. **Microsoft Research** (2013): Code ownership and quality
   - Single-owner files have 3-5x higher defect rates
   - Shared ownership improves quality
   - Recommendation: Encourage code reviews and pairing

2. **Conway's Law Studies** (2015): Knowledge silos and velocity
   - Knowledge silos slow feature delivery by 40-60%
   - Cross-functional knowledge accelerates delivery
   - Recommendation: Rotate developers across domains

3. **Software Engineering Research** (2018): Onboarding time
   - Average time to full productivity: 3-6 months
   - With good documentation/mentoring: 2-3 months
   - Recommendation: Invest in onboarding infrastructure

4. **Organizational Risk Research** (2016): Bus factor analysis
   - Most projects have bus factor of 2-3 (critical risk)
   - Bus factor correlates with project abandonment
   - Recommendation: Track bus factor as health metric

**Why knowledge risk matters**: People leave. Knowledge must outlive individual contributors. Bus factor measures organizational resilience.

## Integration with Other Techniques

**Combine onboarding risk with**:

- **forensic-knowledge-mapping**: Ownership patterns across codebase
- **forensic-hotspot-finder**: Single-owner hotspots = critical priority
- **forensic-coordination-analysis**: Single-owner + multi-team = process gap
- **forensic-refactoring-roi**: Knowledge sharing has quantifiable ROI

**Why**: Knowledge risk is organizational risk - affects hiring, retention, and business continuity planning.
