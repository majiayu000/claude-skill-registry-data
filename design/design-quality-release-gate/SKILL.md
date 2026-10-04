---
id: frontend.design.design-quality-release-gate
name: Design Quality Release Gate
description: Score product intent, visual identity, usability, components, accessibility, responsiveness, states, motion, and validation with blocker overrides.
stack:
  - Frontend
  - UX
  - Design Systems
  - Testing
category: quality
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - design release gate
  - frontend quality score
  - design QA
  - approve UI release
---

# Design Quality Release Gate

## Purpose

Provide measurable closure for design work: blockers override score, while evidence prevents subjective iteration from continuing indefinitely.

## When to Use

- A feature, page, component family, or multi-agent design pass is ready for release decision.
- Teams need shared design definition of done.

## Do

- Score product intent and task success (20), visual identity (15), hierarchy (10), component API/reuse (15), accessibility (15), responsiveness (10), states/feedback (10), and motion/performance/regression validation (5).
- Attach implementation, task, screenshot, and test evidence; classify remaining work by severity, owner, and date.
- Pass at 85 or above with no blocker; conditionally approve at 70-84 only with owned remediation; fail below 70 or on any blocker.

## Do Not

- Do not average away critical blockers, inflate score through low-value polish, or use a rubric instead of product judgment.

## Review Checklist

- [ ] Score has evidence for every category.
- [ ] User-task and accessibility blockers are resolved or decision is fail.
- [ ] Accepted debt has owner and date.

## Expected Output

1. 100-point scorecard and evidence.
2. Blocker list and approval status.
3. Owned remediation and accepted-debt record.

## References

- [Design Excellence Guide](../../../../docs/design-excellence-guide.md)
