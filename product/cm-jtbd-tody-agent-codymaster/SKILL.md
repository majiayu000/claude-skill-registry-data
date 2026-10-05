---
name: cm-jtbd
description: "Customer discovery framework using Jobs-To-Be-Done theory — uncover the functional, social, and emotional jobs customers hire products to do. Produces JTBD canvases with job statements, outcome metrics, and competing solutions. Use alongside cm-brainstorm-idea for evidence-based product decisions."
---

# Jobs-To-Be-Done — Customer Discovery Framework

> **Understand the job, not the customer.**
> People don't buy products — they hire them to get a job done.

## When to Use

- Before designing a new feature or product
- When existing features aren't converting or being used
- Alongside `cm-brainstorm-idea` for deep customer context
- User mentions: "customer discovery", "JTBD", "what do customers want", "product-market fit", "why are users churning"

## The JTBD Framework

### Job Statement Formula

```
When [SITUATION], I want to [MOTIVATION], so I can [EXPECTED OUTCOME]
```

### Three Job Dimensions

| Dimension | Definition | Example |
|-----------|-----------|---------|
| **Functional** | The core task to accomplish | "Get from A to B quickly" |
| **Social** | How the person wants to be perceived | "Be seen as a reliable professional" |
| **Emotional** | How the person wants to feel | "Feel confident in my decision" |

## Process

### Phase 1: Job Discovery (Interviews)

1. Recruit 5-8 recent customers (ideally within 90 days of purchase)
2. Use the Switch Interview technique — ask about the moment they decided to switch/buy
3. Key questions:
   - "Walk me through the day you decided to [buy/switch/start using X]"
   - "What were you doing before that solution existed?"
   - "What was the first thing you tried? Why didn't that work?"
   - "What almost stopped you from switching?"
4. Record patterns: triggers → anxiety → progress → outcomes

### Phase 2: JTBD Canvas

For each major job discovered, complete the canvas:

```
JOB STATEMENT:
When [situation], I want to [motivation], so I can [outcome]

FUNCTIONAL DIMENSION: [core task]
SOCIAL DIMENSION:     [perception goal]
EMOTIONAL DIMENSION:  [feeling goal]

FORCES PUSHING TO HIRE:
(+) Push: [what makes them switch from current solution]
(+) Pull: [what attracts them to new solution]

FORCES RESISTING HIRE:
(-) Anxiety: [fears about new solution]
(-) Habit: [attachment to old solution]

COMPETING SOLUTIONS CURRENTLY HIRED:
1. [direct competitor or workaround]
2. [indirect solution]
3. [do-nothing option]

OUTCOME METRICS (how customer measures success):
- Speed: [e.g., "get answer in <5 minutes"]
- Accuracy: [e.g., "zero errors in the output"]
- Effort: [e.g., "no manual steps required"]
```

### Phase 3: Opportunity Scoring

Rate each outcome metric:
- **Importance** (1-10): How important is this outcome to the customer?
- **Satisfaction** (1-10): How satisfied are they with current solutions?
- **Opportunity score** = Importance + max(Importance − Satisfaction, 0)

Scores ≥ 15 = underserved outcomes → highest priority to address.

## Output

Save JTBD canvas to `docs/jtbd/jtbd-canvas-[date].md`.

## Integration

| Skill | Relationship |
|-------|-------------|
| `cm-brainstorm-idea` | UPSTREAM: JTBD feeds into strategic analysis |
| `cm-planning` | DOWNSTREAM: Validated jobs inform feature plans |
| `cm-cro-methodology` | COMPLEMENT: JTBD objections → CRO objection handling |
| `cm-dockit` | OUTPUT: JTBD canvases are a document type in DocKit |
