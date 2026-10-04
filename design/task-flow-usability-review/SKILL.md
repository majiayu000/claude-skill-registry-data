---
id: frontend.design.task-flow-usability-review
name: Task Flow Usability Review
description: Review user flows for clarity, decision cost, error prevention, recovery, feedback, consistency, and completion confidence.
stack:
  - Frontend
  - UX
  - Product Design
category: usability
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - usability review
  - task flow audit
  - UX friction
  - form flow review
---

# Task Flow Usability Review

## Purpose

Verify that users complete intended work accurately and confidently; visual polish cannot compensate for avoidable flow friction.

## When to Use

- A feature has multiple decisions, steps, forms, dependent states, abandonment, or support evidence.
- Navigation or task order changes in a redesign.

## Do

- Walk the task with realistic content and identify every decision, memory step, context switch, and irreversible action.
- Review validation timing, prevention, recovery, loading, save, partial success, background work, and completion feedback.
- Prefer recognition over recall and progressive disclosure for secondary complexity.

## Do Not

- Do not optimize only happy paths, hide safe validation until submit, or add steps to compensate for unclear copy.

## Review Checklist

- [ ] Users know location, requirements, consequence, and next action.
- [ ] Critical errors are prevented or recoverable and input survives failures.
- [ ] Completion and persistence are unambiguous.

## Expected Output

1. Flow map and severity-ranked friction findings.
2. Sequence, prevention, and recovery recommendations.
3. Keyboard, touch, and assistive-technology validation scope.

## References

- [Design Excellence Guide](../../../../docs/design-excellence-guide.md)
