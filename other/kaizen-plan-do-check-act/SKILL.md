---
name: kaizen-plan-do-check-act
description: PDCA experimentation cycle.
argument-hint: improvement goal or problem
---

# Plan-Do-Check-Act (PDCA)

Apply PDCA cycle for continuous improvement through iterative problem-solving and process optimization.

## Description

Four-phase iterative cycle: Plan (identify and analyze), Do (implement changes), Check (measure results), Act (standardize or adjust). Enables systematic experimentation and improvement.

## Steps

### Phase 1: PLAN

1. Define the problem or improvement goal
2. Analyze current state (baseline metrics)
3. Identify root causes (Five Whys or Fishbone → `kaizen-analyse-problem/root-cause-methods.md`)
4. Develop hypothesis: "If we change X, Y will improve"
5. Design experiment: what to change, how to measure success
6. Set success criteria (measurable targets)

### Phase 2: DO

1. Implement the planned change (small scale first)
2. Document what was actually done
3. Record any deviations from plan
4. Collect data throughout implementation
5. Note unexpected observations

### Phase 3: CHECK

1. Measure results against success criteria
2. Compare to baseline (before vs. after)
3. Analyze data: did hypothesis hold?
4. Identify what worked and what didn't
5. Document learnings and insights

### Phase 4: ACT

1. **If successful**: Standardize the change
   - Update documentation
   - Train team
   - Create checklist/automation
   - Monitor for regression
2. **If unsuccessful**: Learn and adjust
   - Understand why it failed
   - Refine hypothesis
   - Start new PDCA cycle with adjusted plan
3. **If partially successful**:
   - Standardize what worked
   - Plan next cycle for remaining issues

## Examples

### Example 1: Reducing Build Time

```
CYCLE 1
───────
PLAN:
  Problem: Docker build takes 45 minutes
  Current State: Full rebuild every time, no layer caching
  Root Cause: Package manager cache not preserved between builds
  Hypothesis: Caching dependencies will reduce build to <10 minutes
  Change: Add layer caching for package.json + node_modules
  Success Criteria: Build time <10 minutes on unchanged dependencies

DO:
  - Restructured Dockerfile: COPY package*.json before src files
  - Added .dockerignore for node_modules
  - Configured CI cache for Docker layers
  - Tested on 3 builds

CHECK:
  Results:
    - Unchanged dependencies: 8 minutes ✓ (was 45)
    - Changed dependencies: 12 minutes (was 45)
    - Fresh builds: 45 minutes (same, expected)
  Analysis: 82% reduction on cached builds, hypothesis confirmed

ACT:
  Standardize:
    ✓ Merged Dockerfile changes
    ✓ Updated CI pipeline config
    ✓ Documented in README
    ✓ Added build time monitoring
  
  New Problem: 12 minutes still slow when deps change
  → Start CYCLE 2


CYCLE 2
───────
PLAN:
  Problem: Build still 12 min when dependencies change
  Current State: npm install rebuilds all packages
  Root Cause: Some packages compile from source
  Hypothesis: Pre-built binaries will reduce to <5 minutes
  Change: Use npm ci instead of install, configure binary mirrors
  Success Criteria: Build <5 minutes on dependency changes

DO:
  - Changed to npm ci (uses package-lock.json)
  - Added .npmrc with binary mirror configs
  - Tested across 5 dependency updates

CHECK:
  Results:
    - Dependency changes: 4.5 minutes ✓ (was 12)
    - Compilation errors reduced to 0 (was 3)
  Analysis: npm ci faster + more reliable, hypothesis confirmed

ACT:
  Standardize:
    ✓ Use npm ci everywhere (local + CI)
    ✓ Committed .npmrc
    ✓ Updated developer onboarding docs
  
  Total improvement: 45min → 4.5min (90% reduction)
  ✓ PDCA complete, monitor for 2 weeks
```

