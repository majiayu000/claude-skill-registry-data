---
name: idea-evaluation
description: Assess solution ideas on impact and feasibility to prioritize prototyping. Use during Ideate phase when deciding which ideas to pursue.
---

# Idea Evaluation

## Overview
Systematically assess solution ideas to prioritize which ones to pursue through prototyping.

## When to Use
- During Ideate phase after generating multiple ideas
- When deciding which ideas to prototype
- When stakeholders or leadership ask for prioritization
- Before committing resources to development

## How to Apply

### 1. Grade on Two Dimensions

**IMPACT** — How much value would this create?
- **High**: Solves major pain point, affects many users, strategic value
- **Medium**: Improves experience, helps some users, supports goals
- **Low**: Nice improvement, limited scope, minor benefit

**FEASIBILITY** — How realistic is this to build/implement?
- **High**: Clear path, existing tech, reasonable timeline/resources
- **Medium**: Some unknowns, might need new tech, moderate complexity
- **Low**: Major technical challenges, unclear if possible, high cost

### 2. Plot on Impact/Feasibility Matrix

```
       FEASIBILITY
       Low    Med    High
    ┌─────────────────────┐
H   │       │  B  │  A   │
I   │       │     │      │
M   ├───────┼─────┼──────┤
P   │       │  C  │  B   │
A   │       │     │      │
C   ├───────┼─────┼──────┤
T   │   D   │  D  │  C   │
    └─────────────────────┘
```

**A tier**: High impact, High feasibility → Prioritize
**B tier**: High impact, Med feasibility OR Med impact, High feasibility → Consider
**C tier**: Med impact, Med feasibility OR Low impact, High feasibility → Maybe later
**D tier**: Low feasibility or Low impact → Park or discard

### 3. Consider Additional Factors

Beyond impact/feasibility:
- **Stakeholder priority**: What do users care about most?
- **Strategic fit**: Aligns with business goals?
- **Dependencies**: Blocks or enables other ideas?
- **Learning value**: Will prototyping teach us something important?
- **Risk**: What happens if we're wrong?

### 4. Make Recommendations

For each tier:

**A tier**: "Prototype immediately. This addresses [key insight] with clear path forward."

**B tier**: "Strong candidate. Needs [feasibility spike / user validation / resource check] before committing."

**C tier**: "Interesting but not priority. Revisit if A/B tier ideas fail or after launch."

**D tier**: "Park for now. [Technical barriers / unclear value / other ideas are stronger]."

### 5. Document in currentstate.json

```json
{
  "id": "idea1",
  "title": "Offline data capture",
  "description": "Allow field techs to log data without connection, sync when back online",
  "impact": "high",
  "feasibility": "high",
  "status": "ideated",
  "idea_doc_link": "ideas/offline_capture.md"
}
```

## Evaluation Example

**Idea**: "AI-powered predictive maintenance alerts"
- **Impact**: High — Prevents costly downtime, major pain point
- **Feasibility**: Low — Need ML expertise, training data, unclear accuracy
- **Grade**: B tier
- **Recommendation**: Validate predictive value with simple rule-based alerts first, then explore AI if rules prove useful

**Idea**: "Quick-capture field form"
- **Impact**: High — Addresses #1 user frustration with current 10-step process
- **Feasibility**: High — Straightforward UI work, existing tech
- **Grade**: A tier
- **Recommendation**: Prototype immediately, test with 5 field techs

## Tips
- Involve the whole DesignTeam
- Get stakeholder input on impact
- Validate feasibility with technical experts
- Don't over-engineer low-hanging fruit
- High impact + Low feasibility may need research spike first
- Re-evaluate as you learn more
- Document reasoning, not just grades
