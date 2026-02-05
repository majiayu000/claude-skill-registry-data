---
name: adr
description: Create TCC Architecture Decision Records (ADRs) in docs/ADRs for architecture, data, API, security, infra, or compliance decisions. Use when making or changing significant system behavior, contracts, tenancy/RLS, evidence/audit posture, data retention, or integrations.
---

# ADR

## Workflow

1) Find the next ADR number

```bash
ls docs/ADRs/*.md 2>/dev/null | sort -V | tail -5
```

- If none exist, start at 0001.

2) Create the ADR file

`docs/ADRs/NNNN-<kebab-case>.md`

3) Fill the template

```markdown
# NNNN - <Decision Title>

## Context
- What problem or constraint is driving this decision now?
- What options were considered?

## Decision
- What will we do?
- What will we explicitly not do?

## Consequences
- Positive outcomes
- Negative tradeoffs
- Follow-up work (if any)

## Decision Linkback
- Related ADRs
- Related specs/plans (e.g., ENGINEERING_SPEC.md, IMPLEMENTATION_PLAN.md)

## Behavior Delta
- What changes in system behavior, contracts, or operations?
```

## Checklist

- Title is the decision (not the problem)
- Context explains why now and key constraints
- Decision is specific and testable
- Consequences include positives and negatives
- Linkback references relevant ADRs/specs
- Behavior Delta is explicit
