---
name: feature-prioritizer
description: Evaluate and prioritize product features using RICE, ICE, and Value vs Effort frameworks with visual matrices
---

# Feature Prioritizer

## Overview

The Feature Prioritizer skill helps AI Product Managers make data-driven decisions about what to build next. It applies multiple prioritization frameworks (RICE, ICE, Value vs. Effort), generates comparison matrices, and provides strategic recommendations for feature roadmapping.

## When to Use This Skill

- Planning quarterly or annual roadmaps
- Evaluating a large feature backlog
- Making build vs. buy vs. partner decisions
- Responding to stakeholder feature requests
- Resolving conflicts about priorities
- Communicating trade-offs to leadership
- Balancing technical debt vs. new features
- Comparing AI/ML investment opportunities

## PM Frameworks Applied

- **RICE Scoring**: Reach × Impact × Confidence / Effort
- **ICE Scoring**: (Impact + Confidence + Ease) / 3
- **Value vs. Effort Matrix**: 2x2 matrix for visual prioritization
- **Weighted Scoring**: Custom weights for company priorities
- **Strategic Alignment**: Fit with company OKRs and vision
- **Dependency Mapping**: Understanding feature relationships
- **Risk-Adjusted Scoring**: Accounting for uncertainty

## Inputs Required

```json
{
  "features": [
    {
      "name": "string",
      "description": "string",
      "reach": "number (users affected per quarter)",
      "impact": "number (0.25-3.0 scale)",
      "confidence": "number (0.0-1.0 scale)",
      "effort": "number (person-months)",
      "strategic_alignment": "number (1-5 scale, optional)",
      "dependencies": ["list of feature names, optional"],
      "risk_level": "string (low/medium/high, optional)"
    }
  ],
  "company_priorities": {
    "growth_weight": "number (0.0-1.0, optional)",
    "retention_weight": "number (0.0-1.0, optional)",
    "monetization_weight": "number (0.0-1.0, optional)"
  },
  "constraints": {
    "max_effort_per_quarter": "number (optional)",
    "required_features": ["list, optional"]
  }
}
```

## Outputs Produced

1. **Prioritized Feature List** - Features ranked by RICE and ICE scores
2. **Value vs. Effort Matrix** - Visual 2x2 matrix in ASCII or data format
3. **Strategic Recommendations** - Which features to build, defer, or cut
4. **Roadmap Scenarios** - Different options based on resource availability
5. **Risk Analysis** - Highlighting high-risk features
6. **Dependency Map** - Features that should be built together
7. **Trade-off Analysis** - What you're giving up by choosing certain features

## Usage Instructions

### Basic Invocation

```
Prioritize these features using RICE: [list 3-5 features with reach, impact, confidence, effort]
```

### Detailed Invocation

```
I need to prioritize my feature backlog for Q1 planning. Here are the features:

1. AI-powered search - 50K users, high impact (2.0), 80% confidence, 4 months effort
2. Mobile app dark mode - 100K users, low impact (0.5), 95% confidence, 1 month effort
3. Advanced analytics dashboard - 10K users, massive impact (3.0), 60% confidence, 6 months effort
4. Social sharing - 75K users, medium impact (1.0), 70% confidence, 2 months effort

Company priorities: 60% growth, 30% retention, 10% monetization
Constraint: Maximum 8 person-months available

Generate RICE scores, ICE scores, value vs. effort matrix, and recommend Q1 roadmap.
```

## Best Practices

- **Use consistent units** - Always measure reach in same timeframe (e.g., quarterly)
- **Calibrate impact scale** - 0.25=minimal, 0.5=low, 1.0=medium, 2.0=high, 3.0=massive
- **Be honest about confidence** - Low confidence should penalize risky bets
- **Include all effort** - Design, engineering, testing, documentation
- **Consider dependencies** - Some features unlock others
- **Validate with stakeholders** - Scoring is subjective, get alignment
- **Revisit regularly** - Priorities change, update scores quarterly
- **Balance frameworks** - No single framework is perfect
- **Account for strategic value** - Some features are strategic bets

## Composition with Other Skills

### Recommended Workflow

1. **Before Prioritization**:
   - `user-research-analyzer` → Understand user needs
   - `competitive-analyzer` → Know market dynamics
   - `metrics-dashboard-builder` → Define success metrics

2. **During Prioritization**:
   - Use this skill (`feature-prioritizer`) → Score and rank features
   - Iterate on assumptions with team

3. **After Prioritization**:
   - `prd-generator` → Create PRDs for top features
   - `roadmap-planner` → Build visual roadmap
   - `stakeholder-communicator` → Explain priorities and trade-offs

## Common Pitfalls to Avoid

- **Optimism bias** - Overestimating impact, underestimating effort
- **Recency bias** - Overweighting recently requested features
- **HiPPO effect** - Letting highest paid person's opinion dominate
- **Analysis paralysis** - Over-analyzing instead of deciding
- **Ignoring technical debt** - Only prioritizing new features
- **Missing dependencies** - Building features in wrong order
- **Forgetting maintenance** - Not accounting for support burden
- **Local optimization** - Optimizing for team vs. company goals

## Prioritization Framework Details

### RICE Scoring

**Formula**: (Reach × Impact × Confidence) / Effort

**When to use**: 
- Large feature sets (10+ features)
- Need quantitative justification
- Want to compare very different features

**Strengths**:
- Comprehensive and objective
- Forces thinking about all dimensions
- Easy to communicate to stakeholders

**Limitations**:
- Requires good data/estimates
- Doesn't capture strategic value well
- Can be gamed if not careful

### ICE Scoring

**Formula**: (Impact + Confidence + Ease) / 3

**When to use**:
- Quick prioritization needed
- Early-stage features with limited data
- Evaluating experiments or bets

**Strengths**:
- Simple and fast
- Good for experiments
- Less data-intensive than RICE

**Limitations**:
- Doesn't account for reach
- All factors weighted equally
- More subjective

### Value vs. Effort Matrix

**Quadrants**:
- **Quick Wins** (High Value, Low Effort) → Build first
- **Big Bets** (High Value, High Effort) → Plan carefully
- **Fill Ins** (Low Value, Low Effort) → Build if capacity
- **Time Sinks** (Low Value, High Effort) → Avoid

**When to use**:
- Visual communication to executives
- Simplifying complex decisions
- First-pass filtering of backlog

## Python Functions

### `calculate_rice(reach: int, impact: float, confidence: float, effort: float) -> float`
Calculates RICE prioritization score.

### `calculate_ice(impact: float, confidence: float, ease: float) -> float`
Calculates ICE prioritization score.

### `generate_value_effort_matrix(features: list) -> dict`
Creates 2x2 matrix categorizing features into quadrants.

### `apply_strategic_weights(features: list, weights: dict) -> list`
Adjusts scores based on company strategic priorities.

### `identify_dependencies(features: list) -> dict`
Maps feature dependencies and suggests build order.

### `generate_roadmap_scenarios(features: list, constraints: dict) -> list`
Creates different roadmap options based on resource constraints.

### `assess_portfolio_balance(features: list) -> dict`
Analyzes if feature mix balances growth, retention, technical debt, etc.

## Output Format Example

```markdown
## Feature Prioritization Results

### RICE Scores (Ranked)

| Rank | Feature | Reach | Impact | Confidence | Effort | RICE Score |
|------|---------|-------|--------|------------|--------|------------|
| 1 | Feature A | 50,000 | 2.0 | 80% | 4 | 20.0 |
| 2 | Feature B | 100,000 | 0.5 | 95% | 1 | 47.5 |

### Value vs. Effort Matrix

```
     │
High │  [Big Bets]        [Quick Wins]
     │  Feature A         Feature B
VALUE│
     │  [Time Sinks]      [Fill Ins]
Low  │  Feature C         Feature D
     │
     └─────────────────────────────
        High              Low
              EFFORT
```

### Strategic Recommendations

**Build Now (Q1)**:
1. Feature B - Quick win with massive reach
2. Feature A - Strategic bet, high impact

**Defer to Q2**:
- Feature D - Low value, wait for capacity

**Cut from Roadmap**:
- Feature C - Time sink, recommend alternative approach
```

## Related Documentation

- See `prd-generator` for creating specs for prioritized features
- See `roadmap-planner` for visual roadmap creation
- See `user-research-analyzer` for validating impact assumptions
- See `stakeholder-communicator` for explaining priority decisions

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Skill Type**: Analytical (with Python)  
**Complexity**: Intermediate
