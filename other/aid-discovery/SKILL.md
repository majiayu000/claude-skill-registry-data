---
name: aid-discovery
description: AID Phase 0 - Research & discovery. Use for validating problem spaces, identifying stakeholders, defining success metrics, deciding whether to proceed.
---

# aid-discovery - AID Phase 0

Purpose: Validate problem space before committing to solution.
Entry: Initial idea/request exists, stakeholders available.
Exit: Problem validated, stakeholders identified, success metrics defined, go/no-go decision.

## Deliverables

1. Problem Statement (SCQ format) - Validated, no solution assumptions
2. Stakeholder Map - All affected parties identified
3. Success Metrics - Quantified, measurable outcomes

## Discovery Questions

Ask these:

- Problem: What problem are we solving? Who has this problem? How painful? (Quantify) What if we don't solve it?
- Stakeholders: Who are end users? Who owns data/process? Who makes decisions? Who else touches this?
- Success: What does success look like? How will we measure? What's minimum viable outcome?
- Technical feasibility: Is this feasible? Major technical risks? Required skills? Infrastructure needs?

## Problem Statement Template (SCQ)

```markdown
## Problem Statement

### Situation
[Current state]

### Complication
[What's wrong]

### Question
[What solving this answers]

### Impact
- [Quantified impact]

### Success Metrics
| Metric | Current | Target |
|--------|---------|--------|
| [Metric] | [Now] | [Goal] |
```

## Stakeholder Map Template

```markdown
### Decision Makers
- [Name/Role]: [Responsibility]

### Data/System Owners
- [Name/Role]: [What they own]

### End Users
- [Type]: [How affected]

### Integrations
- [System]: [Relationship]
```

## Common Pitfalls

|Pitfall|Fix|
|---|---|
|Solution-first|Start with "what problem?"|
|Missing stakeholders|Ask "who else touches this?"|
|Vague problems|If can't measure, not defined|
|Assumption blindness|Make assumptions explicit|

## Phase Gate Checklist

- [ ] Problem statement validated
- [ ] All stakeholders identified
- [ ] Success metrics specific
- [ ] Technical feasibility assessed
- [ ] Proceed/not-proceed decision clear
- [ ] Scope boundaries established

## Handoff to PRD

- Validated problem statement
- Stakeholder map
- Success metrics
- Constraints identified
- Scope boundaries
