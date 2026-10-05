---
name: implementation-plan
description: Apply when planning before writing code, defining scope, or producing an implementation plan for a feature or change.
license: MIT
version: 1.0.0
tokens_target: 1300
triggers:
  - implementation plan
  - planning before code
  - scope definition
loads_after: []
supersedes: []
---

# Sub-Skill: Implementation Plan

**Purpose:** Ensure every non-trivial change is planned before execution, reducing rework, missed files, and undetected regressions.

---

## Rules

### Scope & Files

1. **List affected files first.** Always list all files that will be modified before beginning implementation. Reference: ERR-2026-029
2. **Define scope boundaries.** Before writing code, explicitly state what is in scope and what is out of scope to prevent scope creep.
3. **Map dependencies.** Always identify which modules, services, or packages depend on the code being changed before touching it.

### Ordering & Safety

4. **Order migrations before rollouts.** Always sequence database migrations before application deployments in the plan; never assume they run together.
5. **Write the rollback story.** Before starting, define the rollback procedure: which commands revert the change and restore the previous state.
6. **Identify stop-the-line criteria.** Always define explicit conditions that would cause you to halt implementation and reassess (e.g., test failure rate, latency spike).

### Testing & Quality

7. **Include a test plan.** Always specify which tests will be added or modified and what scenarios they cover before writing implementation code.
8. **Assess risk per change.** For each file in the touch list, note the risk level (low/medium/high) based on blast radius and test coverage.

### Communication & Completion

9. **Estimate time per step.** Always provide a rough time estimate for each implementation step so stakeholders can track progress.
10. **Define done explicitly.** Always write a definition of done (DoD) that includes passing tests, updated docs, and any required approvals before starting.
11. **Communicate blockers immediately.** After discovering a blocker during implementation, surface it immediately rather than working around it silently.
12. **Verify the plan against the codebase.** Before executing, confirm each file in the touch list exists and the planned change is compatible with its current state.

---

## See also

- `skills/review-deployment/SKILL.md`
- `skills/error-log/SKILL.md`
