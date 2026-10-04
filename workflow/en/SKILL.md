---
name: decide
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "Structured decision making: Pro/Con matrix, weighted scoring, decision tree, scenario analysis, and Eisenhower matrix."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [decision, evaluation, prioritization, framework]
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/decide.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="decide banner">

> **English** — Official English version of `decide`.


# Decide — Structured Decision Making

> Rational decisions through structured frameworks and evaluation methods

---

## When to Use?

- Choosing between options
- Need a pro/con list
- Multi-criteria decision
- Uncertain about important decisions

**Trigger words:** decide, choose, compare, evaluate, weigh

---

## Frameworks

### 1. Pro/Con Matrix (Simple)

Quick decisions between 2 options.

```
PRO A:                    CON A:
- Advantage 1             - Disadvantage 1
- Advantage 2             - Disadvantage 2

PRO B:                    CON B:
- Advantage 1             - Disadvantage 1
- Advantage 2             - Disadvantage 2

Recommendation: [A/B] because [reasoning]
```

---

### 2. Weighted Scoring (Complex)

Multi-criteria decisions with weighting.

| Criterion | Weight | Option A | Score A | Option B | Score B |
|-----------|--------|----------|---------|----------|---------|
| Criterion 1 | 30% | 8 | 2.4 | 6 | 1.8 |
| Criterion 2 | 25% | 7 | 1.75 | 9 | 2.25 |
| TOTAL | 100% | - | X.XX | - | X.XX |

**Process:**
1. Collect criteria
2. Assign weights (sum = 100%)
3. Rate options (1-10 scale)
4. Calculate scores (rating x weight)
5. Compare and recommend

---

### 3. Decision Tree (Sequential)

Decisions with clear if-then paths:
1. Define starting question
2. First branch (most important criterion)
3. Next level (second most important)
4. Down to final option

---

### 4. Scenario Analysis (Uncertainty)

```
Best Case (X% probability):
  Outcome: +Y points -> Expected value: +Z

Realistic Case (X%):
  Outcome: +Y -> Expected value: +Z

Worst Case (X%):
  Outcome: -Y -> Expected value: -Z

Total expected value: [Sum]
```

---

### 5. Eisenhower Matrix (Prioritization)

```
              URGENT          NOT URGENT
IMPORTANT     1. DO           2. PLAN
NOT IMPORTANT 3. DELEGATE     4. ELIMINATE
```

---

## Quality Checklist

Check before final recommendation:
- [ ] All relevant criteria identified?
- [ ] User values considered?
- [ ] Long-term effects considered?
- [ ] Risks identified and evaluated?
- [ ] Bias check performed?
- [ ] Reversibility assessed?

---

## Best Practices

### Defining Criteria
- Specific and measurable
- Not too many (3-7 ideal)
- Independent of each other

### Weighting
- Sum = 100%
- Most important criterion >= 25%
- No weights < 5%

### Recommendation
- Clear and reasoned
- Mention alternatives
- Name risks
- Consider reversibility

---

## Workflow & Procedure

```
1. User request
2. Understand decision
3. Identify options (2-5)
4. Choose framework
5. Collect criteria
6. Apply framework
7. Bias check (optional)
8. Make recommendation
9. Document reasoning
```

---

## Changelog

### 1.0.0 (2026-03-15)
- Ported from BACH v3.8.0

---

*Ported from BACH v3.8.0 | Standalone Version*
