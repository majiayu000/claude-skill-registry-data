---
name: risk-register
description: |
  Maintain a centralized living risk register across projects. Use this skill when:
  - You need to create or update a risk register for a project or feature
  - You want to consolidate risks from individual specs into one register
  - You need to review and update risk status, mitigations, and owners
  - You want a cross-project risk view
---

# Risk Register

Centralized risk register that consolidates risks from individual spec sections into one living document.

## Workflow

1. **Determine scope** — Single spec, single project, or cross-project
2. **Read Risks and Assumptions** from relevant specs
3. **If existing register exists**, read and merge (don't duplicate — match by description)
4. **Assess each risk** using the likelihood x impact matrix
5. **Output register**

## Risk Assessment Matrix

**Likelihood:** Low (unlikely) | Medium (possible) | High (probable)
**Impact:** Low (minor inconvenience) | Medium (feature degradation) | High (critical failure/data loss)

| | Low Impact | Medium Impact | High Impact |
|---|-----------|--------------|-------------|
| **High Likelihood** | Medium | High | Critical |
| **Medium Likelihood** | Low | Medium | High |
| **Low Likelihood** | Low | Low | Medium |

## Output Format

```markdown
# Risk Register — {Scope}

**Last Updated:** {DD-MM-YYYY}
**Total Risks:** {n} | Open: {n} | Mitigated: {n} | Closed: {n}

## Risk Summary

| ID | Risk | Source | Likelihood | Impact | Priority | Owner | Mitigation | Status | Last Reviewed |
|----|------|--------|-----------|--------|----------|-------|-----------|--------|--------------|
| R-001 | {desc} | {spec/feature} | H/M/L | H/M/L | Critical/High/Med/Low | {name/role} | {plan} | Open/Mitigated/Closed | {date} |

## Critical Risks
{Filtered view of Critical priority — requires immediate attention}

## Risk Trends
- New risks this period: {n}
- Risks closed this period: {n}
- Overdue reviews: {risks not reviewed in 30+ days}
```

## Rules

- Every risk MUST have an owner (name or role, not "TBD")
- Every risk MUST have a mitigation plan (not empty)
- Review date updates when risk is revisited
- Risk IDs are sequential (R-001, R-002) and never reused
- When merging with existing register, preserve existing IDs
- Separate risks from assumptions — only risks go in the register

## Anti-Patterns

- Don't create a risk without a mitigation plan — "TBD" is not acceptable
- Don't reuse risk IDs — closed risks keep their IDs
- Don't mix risks and assumptions — they're different things

## Quality Checklist

- [ ] Every risk has an owner
- [ ] Every risk has a mitigation plan
- [ ] Likelihood x Impact matrix applied
- [ ] Critical risks highlighted
- [ ] Risk IDs are sequential and unique
