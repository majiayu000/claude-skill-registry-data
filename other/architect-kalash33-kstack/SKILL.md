---
name: architect
description: |
  System design, architecture decision records, and trade-off analysis.
  Use when: "design this system", "architecture", "ADR", "trade-offs",
  "how should I structure this", or before building complex systems.
---

# /architect — System Designer

Make the big decisions explicit. Write them down. Justify them.

## When to Use

- Starting a new system or service
- Making a technology choice
- Refactoring a monolith
- When you need to justify a decision to future-you

## Process

### Step 1: Requirements

- What are the functional requirements?
- What are the non-functional requirements? (latency, throughput, availability)
- What are the constraints? (budget, team size, timeline)

### Step 2: Options

Generate at least 3 approaches. For each:
- How it works (diagram or description)
- Pros and cons
- Effort estimate
- Risk assessment

### Step 3: Decision

Pick one. Write an ADR:

```markdown
# ADR-{number}: {title}

## Status: Accepted

## Context
{why we need to decide}

## Decision
{what we chose}

## Consequences
- Good: {benefits}
- Bad: {trade-offs we accept}
- Neutral: {things that don't change}
```

Save to `docs/adr/` in the project.

## Chaining

- **Before**: `/plan` (scope informs architecture)
- **After**: `/review` (validates implementation matches design)
