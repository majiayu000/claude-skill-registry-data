---
name: self-improve
description: Transforms simple user requests into enriched descriptions with traceable findings. Use when interpreting vague user intent, preparing context for agent generation, or synthesizing actionable insights from available project context.
allowed-tools: Read
---

# Self-Improve

Transform user intent into actionable understanding.

## Core Function
```
User Intent + Available Context → Enriched Description
```

## Behavior

- **Specific intent** → focused interpretation, targeted findings
- **Vague intent** → broader scan, note what clarification needed

## Process

### 1. Interpret Intent

Extract from user request:
- **Action:** What to do
- **Subject:** What to affect  
- **Implicit:** What's assumed but not said

### 2. Synthesize Findings

Connect intent with relevant context. Each finding:
```
[Discovery] → [source]
```

Requirements: traceable, relevant, actionable.

### 3. Assess Complexity

| Factor | Question |
|--------|----------|
| Scope | How much affected? |
| Conflicts | Findings contradict? |
| Trade-offs | Significant choices? |

Any factor high → flag for deeper analysis.

## Output
```markdown
## Intent
[Interpreted user intent]

## Findings
1. [Discovery] → [source]
2. [Discovery] → [source]
3. [Discovery] → [source]

## Complexity
[Simple | Needs analysis: scope/conflicts/trade-offs]
```