---
name: postmortem-writing
description: Document root cause analysis for team learning. Blameless, actionable, preventive.
---

# Postmortem Writing

## Purpose

- Share learnings across team
- Prevent recurrence
- Build institutional knowledge
- Blameless culture

## Template

```markdown
# Postmortem: [Incident Title]

**Date:** YYYY-MM-DD
**Duration:** X hours
**Severity:** P1/P2/P3
**Author:** [Name]

## Summary

One paragraph describing what happened and impact.

## Timeline

- HH:MM - Event
- HH:MM - Detection
- HH:MM - Response started
- HH:MM - Mitigation
- HH:MM - Resolution

## Root Cause

Technical explanation of why this happened.
Use 5 Whys technique if helpful.

## Impact

- Users affected: X
- Revenue impact: $Y
- Data loss: None/Partial/Full

## What Went Well

- Detection was fast
- Team responded quickly
- Communication was clear

## What Went Wrong

- Monitoring gap
- Missing validation
- Unclear runbook

## Action Items

| Action | Owner | Due Date |
|--------|-------|----------|
| Add monitoring for X | @person | YYYY-MM-DD |
| Implement validation | @person | YYYY-MM-DD |
| Update runbook | @person | YYYY-MM-DD |

## Lessons Learned

Key takeaways for the team.
```

## Principles

### Blameless

- Focus on systems, not people
- "The system allowed X" not "Person did X"
- Assume good intentions

### Actionable

- Every finding has an action item
- Actions have owners and dates
- Follow up on completion

### Honest

- Don't minimize impact
- Include what went wrong
- Acknowledge gaps

## 5 Whys Example

1. Why did the query fail? → Null user_id
2. Why was user_id null? → Auth didn't set it
3. Why didn't auth set it? → Token was expired
4. Why wasn't expiry handled? → Missing check
5. Why was check missing? → No test coverage

**Root cause:** Missing test for token expiry path
