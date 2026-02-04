---
name: forensic-organizational-alignment
description: Use when team reorganization planning, identifying coordination inefficiencies, validating Conway's Law, assessing team-architecture fit, or planning service splits - analyzes alignment between code module boundaries and team structures revealing organizational bottlenecks
---

# Forensic Organizational Alignment Analysis

## 🎯 When You Use This Skill

**State explicitly**: "Using forensic-organizational-alignment pattern"

**Then follow these steps**:
1. Map **teams to modules** (which teams work on which code)
2. Calculate **alignment score** (single-team modules = good, multi-team = misalignment)
3. Identify **Conway's Law violations** (architecture doesn't match org structure)
4. Cite **research** when presenting findings (Conway's Law empirically validated)
5. Suggest **integration** with coordination-analysis and change-coupling at end

## Overview

Organizational alignment analysis examines whether code architecture matches team structure. Based on Conway's Law: "Organizations design systems that mirror their communication structures."

This analysis reveals:
- **Well-aligned modules** - Single team ownership, clear boundaries
- **Misaligned modules** - Multiple teams editing same code (coordination overhead)
- **Orphaned modules** - No clear team ownership
- **Overloaded teams** - Spread across too many modules
- **Conway's Law violations** - Architecture and organization conflict

**Core principle**: Architecture should match team boundaries. Misalignment causes coordination overhead, slow velocity, and unclear ownership.

## When to Use

- Planning team reorganizations or splits
- Before microservices extraction (which team owns which service?)
- Investigating slow cross-team velocity
- Diagnosing coordination overhead sources
- Quarterly organizational health checks
- After team changes (did architecture adapt?)
- Validating team autonomy

## When NOT to Use

- Insufficient git history (<6 months unreliable)
- Small team (<3 people, structure irrelevant)
- No clear team boundaries (everyone works on everything)
- Early-stage projects (structure still forming)
- When you need defect prediction (use coordination-analysis instead)

## Core Pattern

### ⚡ THE ALIGNMENT FORMULA (USE THIS)

**This is Conway's Law-based alignment measurement - don't create custom metrics**:

```
Module Alignment Score:
  - Single team (>80% contribution):    GOOD (10 points)
  - Two teams (50-80% primary):         MODERATE (5 points)
  - Multi-team (<50% each):             POOR (0 points)
  - Orphaned (no team >50%):            CRITICAL (-5 points)

Team Focus Score:
  - Focused (1-2 modules owned):        GOOD (5 points)
  - Spread (3-5 modules):               MODERATE (0 points)
  - Overloaded (6+ modules):            POOR (-5 points)

Cross-Team Coupling Penalty:
  - Low (<10% cross-team commits):      GOOD (5 points)
  - Medium (10-30%):                    MODERATE (0 points)
  - High (>30%):                        POOR (-5 points)

Overall Alignment = (sum of points / max possible) × 100
```

**Thresholds**: >75 = good alignment, 50-75 = moderate, <50 = poor (needs action)

**Critical**: Single-team modules with <10% cross-team involvement = ideal state.

### 📊 Research Benchmarks (CITE THESE)

**Always reference Conway's Law research when presenting findings**:

| Finding | Impact | Source | When to Cite |
|---------|--------|--------|--------------|
| Conway's Law | Architecture mirrors org structure | Herbsleb & Mockus (2003) | "Conway's Law shows architecture mirrors communication structure (Herbsleb)" |
| Multi-team modules | **40-60%** slower velocity | Microsoft DevOps | "Multi-team modules reduce velocity by 40-60% (Microsoft)" |
| Reverse Conway | Org structure can drive architecture | Inverse Conway | "You can reorganize teams to drive architectural change (Inverse Conway)" |

**Always cite Conway's Law** when recommending organizational or architectural changes.

## Quick Reference

### Essential Git Commands

| Purpose | Command |
|---------|---------|
| **Contributors by module** | `git log --since="12 months ago" --format="%an" -- MODULE/ \| sort \| uniq -c \| sort -rn` |
| **Cross-module commits** | `git log --since="12 months ago" --name-only --format="COMMIT:%H\|%an"` |
| **Team inference (email)** | `git log --since="12 months ago" --format="%an\|%ae" \| sort -u` |
| **Contribution matrix** | `git log --since="12 months ago" --numstat --format="%H\|%an" -- MODULE/` |

### Alignment Classification

| Module State | Primary Team % | Secondary Teams | Alignment | Action |
|--------------|----------------|-----------------|-----------|--------|
| **Single-team** | >80% | None | GOOD | Maintain boundaries |
| **Shared** | 50-80% | 1 team | MODERATE | Clarify ownership |
| **Multi-team** | <50% each | 2+ teams | POOR | Refactor or reassign |
| **Orphaned** | <50% | Many | CRITICAL | Assign owner or deprecate |

### Misalignment Patterns

| Pattern | Indicator | Risk | Fix |
|---------|-----------|------|-----|
| **Multi-team module** | >2 teams contribute significantly | HIGH | Assign primary owner, create interfaces |
| **Cross-boundary coupling** | High co-change across teams | HIGH | API contracts, versioning |
| **Orphaned code** | No team >50% ownership | CRITICAL | Assign ownership or delete |
| **Overloaded team** | Team owns 6+ modules | MEDIUM | Split team or consolidate modules |

## Implementation

### Step 1: Identify Team Structure

**If not provided, infer from git data**:

```python
# Pseudocode for team inference

def infer_teams(contributors):
    # Method 1: Email domains
    teams_by_domain = defaultdict(list)
    for name, email in contributors:
        domain = email.split('@')[1]
        teams_by_domain[domain].append(name)

    # Method 2: Co-commit patterns (proxy for communication)
    teams_by_cocommit = cluster_by_cocommit_frequency(contributors)

    # Method 3: Module ownership patterns
    teams_by_module = cluster_by_shared_modules(contributors)

    # Combine methods for best inference
    return merge_team_inferences([teams_by_domain, teams_by_cocommit, teams_by_module])
```

**Ask user for validation**: Inferred teams may be wrong - always confirm.

### Step 2: Map Teams to Modules

**Calculate contribution percentage**:

```python
def map_teams_to_modules(modules, contributors, team_mapping):
    module_ownership = {}

    for module in modules:
        # Get all commits to this module
        commits_by_team = defaultdict(int)

        for commit in get_commits_to_module(module, since="12 months ago"):
            author = commit.author
            team = team_mapping.get(author, "Unknown")
            commits_by_team[team] += 1

        # Calculate percentages
        total_commits = sum(commits_by_team.values())
        ownership_pct = {
            team: (count / total_commits * 100)
            for team, count in commits_by_team.items()
        }

        # Find primary owner
        primary_team = max(ownership_pct, key=ownership_pct.get)
        primary_pct = ownership_pct[primary_team]

        module_ownership[module] = {
            'primary_team': primary_team,
            'primary_pct': primary_pct,
            'all_teams': ownership_pct
        }

    return module_ownership
```

### Step 3: Calculate Alignment Score

**Apply scoring formula**:

```python
def calculate_alignment_score(module_ownership, team_focus):
    score = 0
    max_score = 0

    # Module alignment scoring
    for module, ownership in module_ownership.items():
        max_score += 10
        primary_pct = ownership['primary_pct']
        team_count = len([p for p in ownership['all_teams'].values() if p > 5])

        if primary_pct > 80 and team_count == 1:
            score += 10  # Single-team (ideal)
        elif primary_pct > 50:
            score += 5   # Shared but clear primary
        elif primary_pct < 50:
            score += 0   # Multi-team (poor)

        # Orphaned modules
        if primary_pct < 50 and team_count > 3:
            score -= 5   # Orphaned (critical)

    # Team focus scoring
    for team, modules_owned in team_focus.items():
        max_score += 5
        if len(modules_owned) <= 2:
            score += 5   # Focused (good)
        elif len(modules_owned) <= 5:
            score += 0   # Spread (moderate)
        else:
            score -= 5   # Overloaded (poor)

    # Overall alignment percentage
    alignment_pct = (score / max_score) * 100 if max_score > 0 else 0
    return max(0, min(100, alignment_pct))  # Clamp to 0-100
```

### Step 4: Identify Misalignments

**Detect specific patterns**:

```python
def identify_misalignments(module_ownership, cross_team_coupling):
    misalignments = []

    for module, ownership in module_ownership.items():
        primary_pct = ownership['primary_pct']
        team_count = len(ownership['all_teams'])

        # Pattern 1: Multi-team module
        if team_count >= 3 and primary_pct < 60:
            misalignments.append({
                'type': 'MULTI_TEAM_MODULE',
                'module': module,
                'severity': 'HIGH',
                'teams': ownership['all_teams'],
                'recommendation': 'Assign primary owner, create interface layer'
            })

        # Pattern 2: Orphaned module
        if primary_pct < 50:
            misalignments.append({
                'type': 'ORPHANED_MODULE',
                'module': module,
                'severity': 'CRITICAL',
                'recommendation': 'Assign ownership or deprecate'
            })

        # Pattern 3: High cross-team coupling
        if module in cross_team_coupling and cross_team_coupling[module] > 30:
            misalignments.append({
                'type': 'CROSS_BOUNDARY_COUPLING',
                'module': module,
                'severity': 'HIGH',
                'recommendation': 'Create API contract, reduce coupling'
            })

    return misalignments
```

## Output Format

### 1. Executive Summary

```
Organizational Alignment Analysis (forensic-organizational-alignment pattern)

Teams: 4 (Frontend, Backend, Platform, QA)
Modules: 12
Alignment Score: 68/100 (MODERATE)
Critical Misalignments: 2
Multi-Team Modules: 5

Conway's Law shows architecture mirrors communication structure (Herbsleb).
```

### 2. Team-Module Ownership Matrix

```
Team              | Primary Modules          | Secondary Modules        | Focus Score
------------------|--------------------------|--------------------------|-------------
Frontend Team     | frontend/, ui/           | api/ (15%)               | GOOD (2)
Backend Team      | backend/*, api/          | infrastructure/ (20%)    | MODERATE (4)
Platform Team     | infrastructure/, db/     | backend/ (25%)           | GOOD (2)
QA Team           | tests/                   | (contributes to all)     | FOCUSED (1)
```

### 3. Module Alignment Status

```
Module               | Primary Team  | Primary % | Other Teams          | Status
---------------------|---------------|-----------|----------------------|----------
frontend/            | Frontend      | 95%       | -                    | ✅ GOOD
backend/auth/        | Backend       | 75%       | Platform (20%)       | ⚠️  MODERATE
backend/api/         | Backend       | 55%       | Frontend (30%), QA   | ❌ POOR
infrastructure/      | Platform      | 70%       | Backend (25%)        | ⚠️  MODERATE
legacy/old-api/      | (multiple)    | 35%       | All teams            | 🚨 ORPHANED
```

### 4. Detected Misalignments

```
CRITICAL MISALIGNMENT #1: Orphaned Module

Module: legacy/old-api/
Status: No clear ownership (highest contributor: 35%)
Teams: Backend (35%), Frontend (30%), Platform (20%), QA (15%)
Impact: Nobody maintains, unclear responsibility, technical debt accumulates

Conway's Law: Module structure doesn't reflect any team's communication pattern

RECOMMENDATION:
1. IMMEDIATE: Assign Backend team as owner (highest contribution)
2. SHORT-TERM: Document current state, freeze new features
3. MEDIUM-TERM: Plan migration or deprecation
```

```
HIGH MISALIGNMENT #2: Multi-Team Module

Module: backend/api/
Primary Team: Backend (55%)
Secondary Teams: Frontend (30%), QA (15%)
Impact: 40-60% slower velocity (Microsoft Research)

Issue: All teams editing API layer = coordination bottleneck

RECOMMENDATION:
1. Establish Backend team as sole owner
2. Create clear API contract (OpenAPI spec)
3. Cross-team changes go through PR review process
4. Consider API versioning strategy
```

### 5. Conway's Law Violations

```
VIOLATION: Monolithic Module, Distributed Teams

Module: core/
Contributing Teams: All 4 teams (no primary >40%)
Pattern: Everyone needs core utilities, no clear boundaries

Conway's Law Violation: Architecture (monolithic) conflicts with organization (4 teams)

RECOMMENDATION (choose one):
  A) REFACTOR: Split core/ into team-aligned modules
     - core-frontend/, core-backend/, etc.
     - Teams maintain their own utilities

  B) ORGANIZE: Create dedicated "Platform" ownership
     - Assign Platform team as core/ owner
     - Other teams submit PRs for changes

  C) EXTRACT: Create shared library with versioning
     - Extract to separate repo
     - Semantic versioning, formal releases
```

## Common Mistakes

### Mistake 1: Not validating inferred teams

**Problem**: Auto-detecting teams from email/commits without user confirmation.

```bash
# ❌ BAD: Use inferred teams directly
teams = infer_teams_from_email_domains()
proceed_with_analysis(teams)

# ✅ GOOD: Validate with user
inferred_teams = infer_teams_from_email_domains()
print("Inferred teams:", inferred_teams)
confirmed_teams = ask_user_to_validate(inferred_teams)
proceed_with_analysis(confirmed_teams)
```

**Fix**: **Always validate inferred teams** - automated inference may group incorrectly.

### Mistake 2: Treating all multi-team modules as bad

**Problem**: Flagging every module with >1 team without considering context.

```bash
# ❌ BAD: All multi-team = misalignment
if team_count > 1:
    flag_as_misaligned()

# ✅ GOOD: Consider primary ownership and purpose
if team_count > 2 AND primary_pct < 60:
    flag_as_misaligned()
# Shared modules (60-80% primary) may be acceptable
```

**Fix**: **Moderate sharing is acceptable** - focus on modules with <60% primary ownership or >3 teams.

### Mistake 3: Not considering module purpose

**Problem**: Applying same standards to all modules regardless of their role.

**Fix**: Different standards for different module types:
- **Domain modules** (auth/, payments/): Should be single-team
- **Infrastructure** (db/, logging/): May legitimately be multi-team
- **Tests**: Expected to be edited by all teams
- **Shared utilities**: Consider extracting to library

### Mistake 4: Ignoring Inverse Conway Maneuver

**Problem**: Only suggesting architectural changes, not considering organizational changes.

**Fix**: Conway's Law works both ways:
- Architecture → Organization: Refactor code to match teams
- Organization → Architecture: Reorganize teams to match desired architecture
- **Always present both options** and let user choose

## ⚡ After Running Alignment Analysis (DO THIS)

**Immediately suggest these next steps to the user**:

1. **Check coordination overhead** (use **forensic-coordination-analysis**)
   - Misaligned modules likely have high contributor counts
   - Validate that >9 contributors correlate with poor alignment
   - Coordination + misalignment = severe velocity problem

2. **Find cross-team couplings** (use **forensic-change-coupling**)
   - Multi-team modules may have high coupling patterns
   - Coupling across team boundaries = architectural debt
   - Prioritize decoupling efforts

3. **Calculate reorganization ROI** (use **forensic-refactoring-roi**)
   - Misalignment = coordination cost
   - Refactoring to align = velocity improvement
   - Translate to business value (40-60% velocity gain)

4. **Track alignment trends** (re-run quarterly)
   - Is alignment improving or degrading?
   - Did team changes improve architecture fit?
   - Early warning for emerging misalignments

### Example: Complete Alignment Analysis Workflow

```
"Using forensic-organizational-alignment pattern, I analyzed team-module fit.

ALIGNMENT SCORE: 68/100 (MODERATE)

Teams: 4 (Frontend, Backend, Platform, QA)
Modules: 12 analyzed

CRITICAL MISALIGNMENT:

legacy/old-api/:
  - Orphaned (no team >40% ownership)
  - 4 teams editing (Backend 35%, Frontend 30%, Platform 20%, QA 15%)
  - Conway's Law violation: No communication structure owns this

backend/api/:
  - Multi-team (Backend 55%, Frontend 30%, QA 15%)
  - Impact: 40-60% slower velocity (Microsoft Research)

RECOMMENDATIONS:

Option A (Architectural):
  1. Assign clear owners (Backend for both modules)
  2. Refactor to reduce cross-team coupling
  3. Create API contracts for cross-team changes

Option B (Organizational):
  1. Create dedicated API team
  2. Deprecate legacy/old-api/
  3. Realign teams around module boundaries

NEXT STEPS:
1. Check coordination (forensic-coordination-analysis) - Validate >9 contributors?
2. Find couplings (forensic-change-coupling) - Which files cross teams?
3. Calculate ROI (forensic-refactoring-roi) - Cost of misalignment?
4. Track quarterly - Monitor alignment trends

Would you like me to proceed with coordination analysis?"
```

**Always provide this integration guidance** - alignment issues connect to coordination overhead and architectural coupling.

## Advanced Patterns

### Inverse Conway Maneuver

**Use organizational changes to drive architecture**:

```
CURRENT STATE:
  Teams: Monolithic (one team, all code)
  Architecture: Monolithic (one codebase)

DESIRED STATE:
  Architecture: Microservices (separate deployable units)

INVERSE CONWAY:
  1. Split team into service-aligned teams FIRST
  2. Assign each team a future service boundary
  3. Teams will naturally refactor toward separation
  4. Architecture follows organizational change

Result: Team structure drives architectural evolution
```

### Alignment Over Time

**Track evolution**:

```
Quarterly Alignment Scores:

Q1 2024: 45/100 (POOR) - 3 teams, monolithic codebase
Q2 2024: 58/100 (MODERATE) - Started module boundaries
Q3 2024: 72/100 (GOOD) - Clear ownership established
Q4 2024: 68/100 (MODERATE) - New team added, realignment needed

Insight: Team changes require architectural adaptation
Action: Review module boundaries after team structure changes
```

### Cross-Team Communication Network

**Map actual vs desired communication**:

```
Actual Communication (from co-commits):
  Frontend ↔ Backend: 45 interactions (HIGH)
  Backend ↔ Platform: 32 interactions (HIGH)
  Frontend ↔ Platform: 8 interactions (LOW)

Module Coupling:
  frontend/ ↔ backend/: Strong coupling
  backend/ ↔ infrastructure/: Strong coupling
  frontend/ ↔ infrastructure/: Weak coupling

VALIDATION: ✅ Conway's Law confirmed
  Communication patterns match coupling patterns
```

## Research Background

**Key studies**:

1. **Herbsleb & Mockus** (2003): Conway's Law empirical validation
   - Architecture mirrors organizational communication structure
   - Coordination distance predicts defects better than code complexity
   - Recommendation: Align architecture with team boundaries

2. **Microsoft DevOps Research** (2016): Multi-team module impact
   - 40-60% slower velocity for modules with >2 teams
   - Clear ownership improves velocity and quality
   - Recommendation: Minimize cross-team module editing

3. **Inverse Conway Maneuver** (ThoughtWorks, 2015): Organizational architecture
   - Team structure can drive architectural change
   - Reorganizing teams before refactoring accelerates change
   - Recommendation: Consider both architectural AND organizational options

4. **MacCormack et al** (2012): Architectural coupling and team structure
   - Misalignment correlates with technical debt accumulation
   - Well-aligned organizations ship faster
   - Recommendation: Regular alignment audits (quarterly)

**Why alignment matters**: Conway's Law is empirically validated - fighting it causes coordination overhead, slow velocity, and organizational friction.

## Integration with Other Techniques

**Combine alignment analysis with**:

- **forensic-coordination-analysis**: Misalignment → high contributor counts → coordination overhead
- **forensic-change-coupling**: Cross-team couplings reveal alignment violations
- **forensic-refactoring-roi**: Misalignment cost = coordination overhead cost
- **forensic-knowledge-mapping**: Single-team modules should have clear ownership

**Why**: Organizational alignment affects all other forensic metrics - fixing alignment improves everything else.
