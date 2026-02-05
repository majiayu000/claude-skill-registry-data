---
name: review-gates
description: Quality gates and review processes
---

# Review Gates

## Overview

Review gates are checkpoints between phases that ensure quality and alignment before proceeding.

## Gate Philosophy

### Never Skip Gates
Gates exist to catch issues early when they're cheap to fix.

### Gate ≠ Bureaucracy
Gates should be lightweight verification, not lengthy approval processes.

### Document Decisions
Record gate decisions for future reference.

## Gate Checklist by Phase

### Discovery → Definition Gate

**Required**:
- [ ] Problem statement documented
- [ ] User need validated (interviews, data, or support)
- [ ] Aligned with product strategy
- [ ] Stakeholder acknowledgment

**Questions to Answer**:
- Is this problem worth solving?
- Do we understand who has this problem?
- Does solving this align with our goals?

---

### Definition → Design Gate

**Required**:
- [ ] Requirements documented and complete
- [ ] Experience spec (UX flows) created
- [ ] Success metrics defined
- [ ] Dependencies identified
- [ ] PM and Designer sign-off

**Questions to Answer**:
- Do we know what "done" looks like?
- Have we thought through the user experience?
- How will we measure success?

---

### Design → Development Gate

**Required**:
- [ ] Architecture spec complete
- [ ] Technical risks documented with mitigations
- [ ] Implementation plan created
- [ ] API contracts defined (if applicable)
- [ ] Architect and Tech Lead sign-off

**Questions to Answer**:
- Is the technical approach sound?
- Have we identified the hard parts?
- Do we have a plan to build this?

---

### Development → Documentation Gate

**Required**:
- [ ] Code complete and merged
- [ ] All tests passing
- [ ] Code review approved
- [ ] QA sign-off
- [ ] No critical bugs

**Questions to Answer**:
- Does it work as specified?
- Is the code quality acceptable?
- Has QA validated the implementation?

---

### Documentation → Delivery Gate

**Required**:
- [ ] User documentation complete
- [ ] API documentation complete (if applicable)
- [ ] Support team enabled
- [ ] Runbooks created/updated
- [ ] Docs reviewed

**Questions to Answer**:
- Can users figure out how to use this?
- Can support help users who have problems?
- Can ops respond to incidents?

---

### Delivery → Data Gate

**Required**:
- [ ] Feature deployed to production
- [ ] Monitoring in place
- [ ] Rollback plan tested
- [ ] No critical issues in first 24-48 hours
- [ ] Users informed (if needed)

**Questions to Answer**:
- Is the feature working in production?
- Can we detect problems?
- Can we roll back if needed?

---

### Data → Debrief Gate

**Required**:
- [ ] Metrics collected (per success criteria)
- [ ] Data analysis complete
- [ ] Results documented
- [ ] Stakeholders informed

**Questions to Answer**:
- Did we achieve our success metrics?
- What do the numbers tell us?
- Are there surprises to investigate?

---

### Debrief → Deprecation Gate (when applicable)

**Required**:
- [ ] Deprecation justified (low usage, better alternative, etc.)
- [ ] Migration path defined
- [ ] Timeline communicated
- [ ] Stakeholder approval

**Questions to Answer**:
- Is it time to retire this?
- How will affected users transition?
- Have we communicated clearly?

## Gate Decision Template

```markdown
## Gate Review: [Phase] → [Phase]

**Feature**: [Name]
**Date**: [Date]
**Reviewer(s)**: [Names]

### Checklist
- [x] Item 1
- [x] Item 2
- [ ] Item 3 (waived - reason)

### Decision
[ ] Pass - Proceed to next phase
[ ] Pass with conditions - Proceed but address [items]
[ ] Fail - Return to [phase] to address [issues]

### Notes
[Any additional context or decisions]
```

## Escalation

### When to Escalate
- Gate criteria cannot be met
- Disagreement on pass/fail
- Need to waive critical requirement
- External dependencies blocking

### How to Escalate
1. Document the issue clearly
2. Propose options with trade-offs
3. Bring to appropriate decision maker
4. Document the decision
