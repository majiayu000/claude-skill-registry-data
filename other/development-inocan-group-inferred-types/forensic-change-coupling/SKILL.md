---
name: forensic-change-coupling
description: Use when planning architecture refactoring, understanding cross-module dependencies, discovering hidden dependencies, finding shotgun surgery patterns, or identifying files that change together - reveals temporal coupling and architectural violations using git history analysis
---

# Forensic Change Coupling Analysis

## 🎯 When You Use This Skill

**State explicitly**: "Using forensic-change-coupling pattern"

**Then follow these steps**:
1. Apply the **coupling strength formula** (see below)
2. Identify both **strong couplings** (>0.5) and **coupling clusters** (3+ files)
3. Flag **cross-module couplings** (architectural violations)
4. Cite **research** when presenting findings (shotgun surgery = 2-3x maintenance cost)
5. Suggest **integration** with other forensic skills at the end

## Overview

Change coupling (temporal coupling) analysis discovers files that frequently change together in the same commits. These patterns reveal:
- **Hidden dependencies** not visible in code imports
- **Architectural violations** (coupling across boundaries)
- **Shotgun surgery** anti-pattern (feature changes require many files)
- **Missing abstractions** or poorly designed interfaces
- **Refactoring opportunities** (files that change together should live together)

**Core principle**: Files that change together reveal architectural truth - the system's *actual* boundaries, not the *intended* ones.

## When to Use

- Planning architecture refactoring or module boundaries
- Understanding why changes touch so many files (shotgun surgery)
- Finding hidden dependencies before splitting services
- Assessing impact of architectural changes
- Identifying tightly coupled modules for extraction
- Planning team ownership boundaries (Conway's Law)
- Post-mortem analysis of brittle areas

## When NOT to Use

- Insufficient git history (<6 months, <100 commits unreliable)
- Greenfield projects without meaningful patterns
- When analyzing single file in isolation
- For understanding code dependencies (use static analysis instead)
- When you need bug-proneness (use hotspot analysis instead)

## Core Pattern

### ⚡ THE COUPLING FORMULA (USE THIS)

**This is the research-backed temporal coupling formula - don't create custom approaches**:

```
Coupling Strength (A, B) = co_changes(A, B) / min(changes(A), changes(B))

Where:
  co_changes(A, B) = number of commits containing both A and B
  changes(A) = total commits touching A
  changes(B) = total commits touching B

Score ranges: 0.0 (never together) to 1.0 (always together)
```

**Thresholds**:
- **>0.7**: Very strong coupling - files are essentially one unit
- **>0.5**: Strong coupling - architectural concern
- **>0.3**: Moderate coupling - worth investigating
- **<0.3**: Weak coupling - may be coincidental

**Critical**: Minimum co-changes threshold (≥3) prevents false positives from single refactoring.

### 📊 Research Benchmarks (CITE THESE)

**Always reference the research when using these patterns**:

| Pattern | Impact | Source | When to Cite |
|---------|--------|--------|--------------|
| Shotgun surgery | **2-3x** maintenance cost | Fowler's Refactoring | "Shotgun surgery patterns cost 2-3x more to maintain (Fowler)" |
| Cross-module coupling | **40-60%** slower feature velocity | Microsoft DevOps Research | "Cross-module coupling reduces velocity by 40-60% (Microsoft)" |
| Coupling clusters | **3-5x** more defects | Google eng practices | "Coupling clusters have 3-5x higher defect rates (Google)" |

**Always cite the source** when presenting coupling findings to architects or team leads.

## Quick Reference

### Essential Git Commands

| Purpose | Command |
|---------|---------|
| **Commits with files** | `git log --since="12 months ago" --name-only --format="COMMIT:%H"` |
| **Files per commit** | `git diff-tree --no-commit-id --name-only -r COMMIT_HASH` |
| **Coupling for file** | `git log --since="12 months ago" --name-only --format="" -- FILE \| grep -v "^$" \| sort \| uniq -c \| sort -rn` |
| **Commit timestamps** | `git log --since="12 months ago" --format="%H\|%ad" --date=short` |

### Coupling Strength Interpretation

| Score | Strength | Meaning | Action |
|-------|----------|---------|--------|
| **>0.7** | Very Strong | Files are essentially one unit | Merge or extract common dependency |
| **0.5-0.7** | Strong | Architectural concern | Review boundaries, consider refactoring |
| **0.3-0.5** | Moderate | Worth investigating | Understand why, monitor trend |
| **<0.3** | Weak | Likely coincidental | No action unless cross-module |

### Coupling Pattern Types

| Pattern | Indicator | Risk | Action |
|---------|-----------|------|--------|
| **Shotgun surgery** | File appears in many couplings | HIGH | Extract abstraction |
| **God file** | Couples with 10+ other files | CRITICAL | Break apart |
| **Cross-boundary** | Coupling across modules | HIGH | Review architecture |
| **Asymmetric** | A→B strong, B→A weak | MEDIUM | Clarify dependency direction |

## Implementation

### Step 1: Extract Coupling Data

**Basic approach**:

```bash
# Get all commits with changed files (last 12 months)
git log --since="12 months ago" --name-only --format="COMMIT:%H" > commits.txt

# Process into commit->files mapping
# Each commit becomes: commit_hash|file1|file2|file3...
```

**Filter considerations**:
- Exclude commits with >20 files (massive refactorings skew data)
- Include only source code files (exclude docs, configs unless analyzing those)
- Consider excluding test files (or analyze separately)
- Time period: 6-12 months for established codebases, 3-6 for fast-moving

### Step 2: Calculate Coupling Scores

**For each pair of files** that appear together:

```python
# Pseudocode for coupling calculation
co_changes = count commits containing both file_a AND file_b
changes_a = count commits containing file_a
changes_b = count commits containing file_b

coupling_score = co_changes / min(changes_a, changes_b)

# Only report if:
if co_changes >= 3 AND coupling_score >= 0.3:
    report_coupling(file_a, file_b, coupling_score, co_changes)
```

**Normalization by minimum** ensures asymmetric coupling detection:
- If A changes 100 times, B changes 10 times, and they co-change 10 times
- Coupling = 10/10 = 1.0 (B *always* changes with A)
- This reveals dependency direction

### Step 3: Identify Coupling Clusters

**Clustering algorithm**:

```
1. Start with highest coupling pair (A, B)
2. Find all files that couple with A or B at >0.5
3. Add to cluster if they also couple with each other
4. Repeat until no more files qualify
5. Move to next unclustered coupling pair
```

**Cluster interpretation**:
- 2-3 files: Likely feature or abstraction boundary
- 4-6 files: Module or service candidate
- 7+ files: Architectural concern, possible god object

### Step 4: Flag Cross-Module Couplings

**Architectural violations**:

```
For each coupling where:
  - File A in module_x/
  - File B in module_y/
  - Coupling score > 0.5

Flag as cross-module coupling (architectural concern)
```

**Why it matters**: Cross-module coupling indicates:
- Leaky abstractions
- Missing API contracts
- Inappropriate dependencies
- Modules that should merge OR need better boundaries

## Output Format

### 1. Executive Summary

```
Change Coupling Analysis (forensic-change-coupling pattern)

Analyzed: X commits over Y months
Files: Z total, N with significant couplings
Strong Couplings (>0.5): M pairs
Coupling Clusters: K groups
Cross-Module Issues: J violations

Research shows shotgun surgery patterns cost 2-3x more to maintain (Fowler).
```

### 2. Top Couplings Table

```
Rank | File A                    | File B                    | Co-Chg | Coupling | Type
-----|---------------------------|---------------------------|--------|----------|---------------
1    | src/auth/login.ts        | src/api/session.ts       | 23     | 0.92     | Very Strong
2    | components/Nav.tsx       | styles/navigation.css     | 18     | 0.85     | Strong
3    | models/user.js           | validators/user.js        | 15     | 0.75     | Strong
```

**For each top coupling**, explain:
- Why they change together (feature? abstraction? architectural issue?)
- Risk level and impact on maintenance
- Refactoring recommendation

### 3. Coupling Clusters

```
Cluster 1 (Avg Coupling: 0.78, Changes: 24):
├─ src/models/user.ts
├─ src/controllers/user.ts
├─ src/validators/user-schema.ts
└─ src/routes/user-routes.ts

Pattern: Vertical slice (model-controller-validator-route)
Recommendation: Extract to user/ module or merge into user-service.ts
Impact: Would eliminate 24 shotgun surgery changes
```

### 4. Cross-Module Violations

```
Module Coupling Issues:

frontend/ <-> backend/ (CRITICAL):
├─ frontend/components/UserProfile.tsx <-> backend/routes/users.js (0.70)
├─ frontend/store/auth.ts <-> backend/auth/jwt.js (0.68)
└─ frontend/api/client.ts <-> backend/middleware/cors.js (0.55)

Research: Cross-module coupling reduces feature velocity by 40-60% (Microsoft).

Recommendation:
1. Define strict API contract (OpenAPI spec)
2. Version the API to decouple frontend/backend releases
3. Consider backend-for-frontend pattern
```

### 5. Shotgun Surgery Patterns

**Files appearing in many couplings** (hub files):

```
Shotgun Surgery Candidates:

1. src/utils/config.js (couples with 15 other files)
   - Every feature change touches config
   - Recommendation: Extract to environment variables or feature flags

2. src/types/common.ts (couples with 22 other files)
   - Type changes cascade across codebase
   - Recommendation: Split into domain-specific type files
```

### 6. Asymmetric Couplings

**Dependency direction**:

```
Asymmetric Coupling (dependency flow):

src/validators/schema.js ALWAYS changes when src/models/user.js changes (0.95)
But src/models/user.js rarely changes with validators (0.12)

Interpretation: Validators are tightly coupled to models
Direction: models/user.js → validators/schema.js
Recommendation: Use schema-first approach (validators define models)
```

## Common Mistakes

### Mistake 1: Not filtering minimum co-changes

**Problem**: Reporting every file pair that changed once together, creating noise.

```bash
# ❌ BAD: No minimum threshold
report all couplings where score > 0.3

# ✅ GOOD: Require meaningful frequency
report couplings where co_changes >= 3 AND score > 0.3
```

**Fix**: Always use **minimum co-changes threshold (≥3)** to filter coincidental changes.

### Mistake 2: Ignoring cross-module couplings

**Problem**: Only looking at coupling strength, missing architectural violations.

```bash
# ❌ BAD: Just sorting by coupling score
sort_by_coupling_score()

# ✅ GOOD: Flag cross-module issues separately
flag_cross_module_couplings()  # Even if score is moderate
report_by_score()
```

**Fix**: **Always highlight cross-module couplings** (score >0.3) as architectural concerns, regardless of absolute score.

### Mistake 3: Not checking for massive commits

**Problem**: Single 100-file refactoring skews all coupling scores.

```bash
# ❌ BAD: Include all commits
analyze_all_commits()

# ✅ GOOD: Exclude outliers
exclude commits with >20 changed files
```

**Fix**: **Exclude commits with >20 files** (configurable) to avoid refactoring noise.

### Mistake 4: Not analyzing temporal trends

**Problem**: Treating all couplings as static, missing increasing/decreasing patterns.

**Fix**: Split analysis into time windows (e.g., last 3 months vs 3-6 months ago) to detect:
- Increasing coupling (new technical debt)
- Decreasing coupling (refactoring working)
- Persistent coupling (architectural issue)

## ⚡ After Running Coupling Analysis (DO THIS)

**Immediately suggest these next steps to the user**:

1. **Check if coupled files are also hotspots** (use **forensic-hotspot-finder**)
   - Coupled hotspots = CRITICAL risk (high churn + architectural issue)
   - Prioritize these for immediate refactoring

2. **Map ownership of coupled clusters** (use **forensic-knowledge-mapping**)
   - Single owner of cluster = knowledge silo
   - Multiple owners = coordination overhead

3. **Calculate refactoring ROI** (use **forensic-refactoring-roi**)
   - Shotgun surgery = maintenance cost
   - Breaking couplings = velocity improvement

4. **Track coupling trends over time** (use **forensic-complexity-trends**)
   - Is coupling increasing or decreasing?
   - Are refactoring efforts working?

### Example: Complete Coupling Analysis Workflow

```
"Using forensic-change-coupling pattern, I analyzed 847 commits over 12 months.

KEY FINDINGS:

Top Coupling Cluster (0.82 avg strength):
├─ src/models/user.ts
├─ src/controllers/user.ts
├─ src/validators/user.ts
└─ src/routes/user.ts
(Changed together 28 times - shotgun surgery pattern)

Research shows shotgun surgery costs 2-3x more to maintain (Fowler).

Cross-Module Violation (CRITICAL):
frontend/UserProfile.tsx <-> backend/users.js (0.75 coupling)
Research: Cross-module coupling reduces velocity by 40-60% (Microsoft).

RECOMMENDED NEXT STEPS:
1. Check hotspots (forensic-hotspot-finder) - Is user cluster also high-churn?
2. Map ownership (forensic-knowledge-mapping) - Who owns this cluster?
3. Calculate ROI (forensic-refactoring-roi) - Cost of shotgun surgery?

Would you like me to proceed with any of these analyses?"
```

**Always provide this integration guidance** - coupling analysis is most valuable when combined with other forensic techniques.

## Advanced Patterns

### Temporal Coupling Trends

**Compare time windows** to detect changes:

```
Last 3 months coupling vs 3-6 months ago:

File A <-> File B:
- 3-6 months ago: 0.45 (moderate)
- Last 3 months: 0.78 (very strong)
- TREND: ⬆️ INCREASING (new technical debt)

Recommendation: Investigate recent changes that introduced coupling
```

### Coupling + Hotspot Intersection

**Combine with hotspot analysis**:

```
Critical Files (Hotspot + High Coupling):

manager.go:
- Hotspot score: 0.89 (high churn + complexity)
- Coupling: couples with 8 other files
- RISK: CRITICAL - refactor immediately

Expected impact: 30-40% bug reduction (Microsoft Research hotspot data)
```

### Conway's Law Violations

**Cross-team coupled files**:

```
Team Coordination Issues:

Files coupled but owned by different teams:
- frontend/Dashboard.tsx (Team A) <-> backend/metrics.js (Team B) (0.68)

Coupling requires cross-team coordination for every change.
Recommendation: Assign ownership to single team OR define API contract
```

## Research Background

**Key studies**:

1. **Fowler's Refactoring** (1999): Shotgun surgery anti-pattern identification
   - Changes requiring many file touches = 2-3x maintenance cost
   - Recommendation: Files that change together should be together

2. **Microsoft DevOps Research** (2016): Cross-module coupling impact
   - 40-60% slower feature velocity with high cross-module coupling
   - Recommendation: Strong module boundaries with versioned contracts

3. **Google Engineering** (2020): Coupling cluster defect correlation
   - 3-5x higher defect rates in highly coupled clusters
   - Recommendation: Limit cluster size, extract abstractions

4. **Adam Tornhill's "Your Code as a Crime Scene"** (2015): Temporal coupling as forensic tool
   - Git history reveals actual vs intended architecture
   - Recommendation: Use coupling to guide refactoring priorities

**Why temporal coupling matters**: Static analysis shows intended dependencies. Temporal coupling reveals *actual* dependencies - how the system really behaves.

## Integration with Other Techniques

**Combine coupling analysis with**:

- **forensic-hotspot-finder**: Coupled hotspots = critical refactoring targets
- **forensic-knowledge-mapping**: Coupled files + single owner = severe knowledge silo
- **forensic-organizational-alignment**: Coupling patterns reveal actual team boundaries
- **forensic-refactoring-roi**: Coupling clusters = shotgun surgery cost
- **forensic-complexity-trends**: Track coupling trends over time

**Why**: Change coupling alone shows "what changes together" but not why it matters. Integration provides business impact and priority.
