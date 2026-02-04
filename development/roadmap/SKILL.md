---
name: roadmap
description: View and update the development roadmap. Use at the start of each session to understand current progress and next priorities.
---

# GATE 4: PLANNING — PLANNER PROTOCOL

> **Agent**: PLANNER
> **Gate**: 4 of 6
> **Prerequisite**: Gate 3 (Test Design) COMPLETE
> **Output**: docs/planning/ROADMAP.md with traced tasks

---

## GATE 4 ENTRY CHECKLIST

Before proceeding, verify:

- [ ] .fortress/gates/GATE_3_TEST_DESIGN.md exists
- [ ] All test stubs exist in tests/
- [ ] TEST_MATRIX.md is complete
- [ ] `pytest --collect-only` succeeds

**If any checkbox fails**: STOP. Complete Gate 3 first.

---

## PLANNER PROTOCOL

### Core Principle: TASKS TRACE TO SPECS

```
❌ FORBIDDEN: "Implement feature X"
✅ REQUIRED: "Implement S001 - Package validation"
             TRACES: S001, INV001, INV002
             TESTS: T001.1-T001.10
```

Every task MUST link to:
1. SPEC_ID(s) it implements
2. INV_ID(s) it enforces
3. TEST_ID(s) it must pass

---

### Step 1: Define Task Size Limits

| Rule | Limit | Reason |
|:-----|:------|:-------|
| Max task size | 8 hours | Smaller = better estimates |
| Estimation multiplier | 2.5x | Always over-estimate |
| Buffer per week | 20% | Unexpected issues |

---

### Step 2: Create Task Breakdown

For each SPEC_ID, create implementation tasks:

```markdown
## TASK: W1.1 — Implement Core Types

### Traces
- SPEC: S001, S002
- INVARIANTS: INV001, INV002
- TESTS: T001.1-T001.5

### Definition
Implement the core data types for PackageRisk, Signals, and Recommendation.

### Acceptance Criteria
- [ ] T001.1 passes (valid package structure)
- [ ] T001.2 passes (empty input handling)
- [ ] INV001 enforced (risk_score bounds)
- [ ] INV002 enforced (signals not None)
- [ ] mypy passes with no errors
- [ ] 100% coverage on new code

### Estimated Effort
- Optimistic: 2 hours
- Likely: 4 hours
- Pessimistic: 8 hours
- **Planned**: 4 hours × 2.5 = 10 hours

### Dependencies
- None (first task)

### Pre-Conditions
- Test stubs T001.1-T001.5 exist (GATE 3)
- Types defined in architecture (GATE 1)

### Post-Conditions
- Tests T001.1-T001.5 pass (not skipped)
- src/phantom_guard/core/types.py exists
- Code has IMPLEMENTS: S001 comments
```

---

### Step 3: Create Week Plans

Group tasks into weeks:

```markdown
# docs/planning/ROADMAP.md

## Week 1: Core Types & Detection Engine

### Goals
- Implement S001-S005 (Core detection)
- All T001.* tests passing
- 90% coverage on core module

### Tasks

| Task | SPEC | Hours | Status |
|:-----|:-----|:------|:-------|
| W1.1 | S001 | 10 | PENDING |
| W1.2 | S002 | 8 | PENDING |
| W1.3 | S003 | 6 | PENDING |
| W1.4 | S004 | 8 | PENDING |
| W1.5 | S005 | 8 | PENDING |
| **Buffer** | - | 10 | - |
| **Total** | - | 50 | - |

### Exit Criteria
- [ ] All W1.* tasks complete
- [ ] T001-T005 tests passing
- [ ] Coverage ≥90% on core/
- [ ] Hostile review passed

---

## Week 2: Registry Clients

### Goals
- Implement S030-S055 (All registry clients)
- All T030-T055 tests passing
- Integration tests with live APIs

### Tasks

| Task | SPEC | Hours | Status |
|:-----|:-----|:------|:-------|
| W2.1 | S030-S035 | 12 | PENDING |
| W2.2 | S040-S045 | 12 | PENDING |
| W2.3 | S050-S055 | 12 | PENDING |
| W2.4 | Cache integration | 6 | PENDING |
| **Buffer** | - | 8 | - |
| **Total** | - | 50 | - |

### Exit Criteria
- [ ] All W2.* tasks complete
- [ ] T030-T055 tests passing
- [ ] Live API tests work
- [ ] Hostile review passed
```

---

### Step 4: Create Dependency Graph

```markdown
## DEPENDENCY GRAPH

```
W1.1 (Core Types)
  │
  ├── W1.2 (Risk Scoring) ──┐
  │                         │
  ├── W1.3 (Signal Detection)──┤
  │                         │
  └── W1.4 (Pattern Matching)──┘
                            │
                            ▼
                    W1.5 (Detector Integration)
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
         ▼                  ▼                  ▼
    W2.1 (PyPI)       W2.2 (npm)       W2.3 (crates)
         │                  │                  │
         └──────────────────┼──────────────────┘
                            │
                            ▼
                    W2.4 (Cache Integration)
                            │
                            ▼
                    W3.1 (CLI Interface)
```

### Critical Path
W1.1 → W1.5 → W2.1 → W2.4 → W3.1 → W4.1 (Release)
```

---

### Step 5: Risk Assessment

```markdown
## RISK ASSESSMENT

| Task | Risk Level | Risk Factor | Mitigation |
|:-----|:-----------|:------------|:-----------|
| W1.1 | LOW | Well-defined types | N/A |
| W1.2 | MEDIUM | Algorithm complexity | Property tests |
| W2.1 | HIGH | External API | Mocking, retries |
| W2.2 | HIGH | External API | Mocking, retries |
| W3.1 | LOW | Standard CLI patterns | typer framework |

### Contingency Plans

**If PyPI API changes:**
1. Switch to cached-only mode
2. Document regression
3. Implement new parser

**If rate limiting hit:**
1. Implement backoff
2. Add queue mechanism
3. Consider API key
```

---

## ROADMAP DOCUMENT TEMPLATE

```markdown
# Phantom Guard — Development Roadmap

> **Version**: 0.1.0
> **Created**: YYYY-MM-DD
> **Last Updated**: YYYY-MM-DD
> **Status**: ACTIVE

---

## Overview

### MVP Target
- Date: YYYY-MM-DD
- Scope: Core detection + CLI + 3 registries

### Total Effort
- Planned: X weeks
- Buffer: Y% contingency

---

## Phase 1: Core Engine (Weeks 1-2)

[Detailed week plans with tasks]

## Phase 2: Integrations (Weeks 3-4)

[Detailed week plans with tasks]

## Phase 3: CLI & Hooks (Weeks 5-6)

[Detailed week plans with tasks]

## Phase 4: Polish & Release (Weeks 7-8)

[Release preparation tasks]

---

## Task Registry

| Task ID | SPEC | Description | Hours | Status | Week |
|:--------|:-----|:------------|:------|:-------|:-----|
| W1.1 | S001 | Core types | 10 | PENDING | 1 |
| W1.2 | S002 | Risk scoring | 8 | PENDING | 1 |
| ... | ... | ... | ... | ... | ... |

---

## Progress Tracking

### Week 1
- [ ] W1.1 Complete
- [ ] W1.2 Complete
- [ ] Week 1 hostile review

### Week 2
...

---

## Trace Matrix

| Task | SPEC_IDs | INV_IDs | TEST_IDs |
|:-----|:---------|:--------|:---------|
| W1.1 | S001 | INV001, INV002 | T001.1-T001.5 |
| ... | ... | ... | ... |
```

---

## GATE 4 EXIT CHECKLIST

Before Gate 4 is complete:

- [ ] docs/planning/ROADMAP.md exists
- [ ] Every task has SPEC trace
- [ ] Every task has TEST trace
- [ ] Every task < 8 hours
- [ ] 20% buffer per week
- [ ] Dependency graph defined
- [ ] Risk assessment complete
- [ ] HOSTILE_PLANNER review passed

**If any checkbox fails**: DO NOT PROCEED TO IMPLEMENTATION.

---

## HOSTILE_PLANNER REVIEW

After completing roadmap:

```
/hostile-review planning
```

The reviewer checks:
- Are estimates realistic?
- Are dependencies correct?
- Are traces complete?
- Are risks identified?
- Is critical path clear?

---

## RECORDING GATE COMPLETION

```markdown
# .fortress/gates/GATE_4_PLANNING.md

## Gate 4: Planning — COMPLETE

**Date**: YYYY-MM-DD
**Approver**: HOSTILE_PLANNER
**Output**: docs/planning/ROADMAP.md

### Summary
- X tasks defined
- Y weeks planned
- Z hours total (with buffer)

### Schedule
| Phase | Weeks | Hours |
|:------|:------|:------|
| Core | 1-2 | X |
| Integrations | 3-4 | Y |
| CLI | 5-6 | Z |
| Release | 7-8 | W |

### Next Step
Begin implementation with /implement W1.1
```

---

## IMPLEMENTATION WORKFLOW

After Gate 4, use `/implement` for each task:

```
/implement W1.1
```

This triggers:
1. Load task definition
2. Verify pre-conditions
3. TDD implementation cycle
4. Verify post-conditions
5. Mark task complete

---

## PROTOCOL VIOLATIONS

| Violation | Response |
|:----------|:---------|
| Task without SPEC trace | Add trace |
| Task > 8 hours | Split task |
| No buffer in week | Add 20% buffer |
| Skipped HOSTILE review | Run review |
| Starting implementation without Gate 4 | BLOCKED |

---

*Gate 4 is about PLANNING what to build. Gate 5 is about VALIDATING what was built.*
