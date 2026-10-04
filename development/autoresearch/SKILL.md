---
name: autoresearch
description: Autonomous goal-directed iteration. Define a goal with a measurable metric, then modify-measure-keep/discard-repeat until the goal is met.
---

# Autoresearch — Autonomous Optimization

Inspired by iterative research methodology. Apply to ANY task with a measurable metric.

## Core Loop

```
1. Define GOAL (what you want to achieve)
2. Define METRIC (how you measure success)
3. Define DIRECTION (higher is better / lower is better)
4. Define VERIFY (how to check the metric)

REPEAT:
  a. Make ONE modification
  b. Measure the metric
  c. If improved: KEEP the change
  d. If worsened: DISCARD (revert)
  e. Log the attempt and result
  f. Choose next modification
UNTIL: goal is met OR no more improvements found
```

## Example Applications

### Performance optimization
- Goal: Page load under 2 seconds
- Metric: Lighthouse performance score
- Direction: Higher is better
- Verify: Run Lighthouse audit

### Bundle size reduction
- Goal: Main bundle under 200KB
- Metric: Bundle size in KB
- Direction: Lower is better
- Verify: Run build and check output

### Test coverage
- Goal: 80%+ code coverage
- Metric: Coverage percentage
- Direction: Higher is better
- Verify: Run test suite with coverage

### SEO score
- Goal: All pages score 90+
- Metric: SEO audit score
- Direction: Higher is better
- Verify: Run SEO analysis tool

## Rules
- ONE change per iteration (isolate variables)
- ALWAYS measure before and after
- ALWAYS revert failed attempts (no accumulating debt)
- LOG every attempt for learning
- STOP when goal is met or 3 consecutive iterations show no improvement
