---
name: ctx:architect
description: Systematic architecture analysis following Understand → Research → Specify → Decompose → Plan workflow. Use for system design, solution evaluation, build vs buy decisions, and task decomposition. Activate when users say "design", "architect", "break down", "best approach", or "should I build".
keywords:
  - design
  - architect
  - architecture
  - system design
  - break down
  - best approach
  - should i build
  - build vs buy
  - task decomposition
  - specifications
  - technical design
allowed-tools: []
---

# CTX:Architect - Structured Design Workflow

Senior architect workflow: Understand → Research → Specify → Decompose → Plan

## Core Workflow

### 1. Understand the Problem

**Extract essentials:**
- Core problem (what's the real need?)
- Constraints (time, budget, skills, existing systems)
- Success criteria (what does "done" look like?)
- Assumptions (make implicit explicit)

**If unclear, ask:**
- "What problem does this solve?"
- "What systems must it integrate with?"
- "Expected scale/volume?"
- "Must-haves vs. nice-to-haves?"

### 2. Research Existing Solutions

**Use WebSearch to find:**
- Existing tools/libraries: `"best [tech] for [problem] 2025"`
- Implementation patterns: `"[problem] implementation examples"`
- Known challenges: `"[problem] pitfalls"`
- Comparisons: `"[tool A] vs [tool B]"`

**Evaluate each solution:**
- Maturity (active? community?)
- Fit (solves 80%+?)
- Integration (works with stack?)
- Cost (license, hosting)
- Risk (lock-in, learning curve)

**Output:** Comparison table with pros/cons

### 3. Develop Specifications

**Structure:**
```
## Problem Statement
[1-2 sentences]

## Requirements
- [ ] Functional (High/Med/Low priority)
- [ ] Performance (metrics, scale)
- [ ] Security (requirements)

## Constraints
- Technical: [stack, systems]
- Resources: [time, budget, team]

## Success Criteria
- [Measurable outcomes]
```

**If specs missing, ask:**
- Functional: "What must it do?" "Inputs/outputs?" "Edge cases?"
- Non-functional: "How many users?" "Response time?" "Uptime?"
- Technical: "Current stack?" "Team skills?" "Deployment constraints?"

### 4. Decompose into Tasks

**Process:**
1. Identify major components
2. Break into 1-3 day tasks
3. Classify: Independent | Sequential | Parallel-ready
4. Map dependencies

**Dependency mapping:**
```
Task A (indep) ────┐
Task B (indep) ────┼──> Task D (needs A,B,C)
Task C (indep) ────┘
Task E (needs D) ──> Task F (needs E)
```

**For each task:**
- Prerequisites (what must exist first?)
- Outputs (what does it produce?)
- Downstream (what depends on it?)
- Parallelizable? (can run with others?)

### 5. Create Execution Plan

**Phase structure:**
```
## Phase 1: Foundation (Parallel)
- [ ] Task A - Infrastructure
- [ ] Task B - Data models
- [ ] Task C - CI/CD

## Phase 2: Core (Sequential after Phase 1)
- [ ] Task D - Auth (needs A,B)
- [ ] Task E - API (needs B)

## Phase 3: Features (Mixed)
- [ ] Task F - Feature 1 (needs D,E)
- [ ] Task G - Feature 2 (needs D,E) ← Parallel with F
```

**Per task include:**
- Description (what to build)
- Dependencies (prerequisites)
- Effort (S/M/L)
- Owner (who can execute)
- Done criteria (how to verify)
- Risks (what could fail)

---

## Build vs. Buy Decision

| Factor | Build | Buy |
|--------|-------|-----|
| Uniqueness | Core differentiator | Common problem |
| Fit | Tools don't match | 80%+ match |
| Control | Need full control | Standard OK |
| Timeline | Have time | Need speed |
| Expertise | Team has skills | Steep curve |
| Maintenance | Can maintain | Want support |

**Hybrid:** Buy infrastructure/common features, build differentiation

---

## Critical Success Factors

✅ Research first (don't reinvent)
✅ Make dependencies explicit (enable parallel work)
✅ Ask direct questions (get clarity fast)
✅ Document trade-offs (explain decisions)
✅ Think in phases (iterative delivery)
✅ Consider team (match to capabilities)

---

## Activation Triggers

- "Design a system for..."
- "How should I architect..."
- "Break down this project..."
- "What's the best approach..."
- "Help me plan..."
- "Should I build or buy..."

---

## Integration with Contextune

This skill is invoked automatically when Contextune detects `/ctx:design` command.

**Workflow:**
1. User types: "design a caching system"
2. Contextune detects: `/ctx:design`
3. Hook augments: "You can use your ctx:architect skill..."
4. Claude should ask: "I detected this is a design task. Would you like me to use the ctx:architect skill (structured workflow) or proceed directly?"
5. User chooses, workflow proceeds

**Output:** Structured specifications, researched alternatives, executable plan with dependencies
