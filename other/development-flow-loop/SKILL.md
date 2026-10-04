---
name: development-flow-loop
description: "Structured software delivery lifecycle for coding tasks that should move from planning to production with repeated quality gates. Use when building features, refactors, integrations, automations, or systems work where the expected flow is Plan, Architect, Evaluate, Implement, Test, Fix, Test, Improve, Test, Fix or Launch, Launch."
---

# Development Flow Loop

## Overview

Follow this exact execution loop for development work.
Advance only when each stage gate is satisfied.

## Lifecycle

1. Plan
- Define objective, constraints, dependencies, risks, and success criteria.
- Output: concise plan with explicit deliverables.

2. Architect
- Choose structure, interfaces, data flow, and failure boundaries.
- Output: implementation shape and file ownership.

3. Evaluate
- Critique the design before coding: complexity, maintainability, testability, cost, and safety.
- Output: go/no-go with concrete adjustments.

4. Implement
- Ship the minimum correct version first.
- Keep changes scoped; avoid unrelated edits.

5. Test
- Run targeted tests first, then broader checks if needed.
- Output: pass/fail evidence.

6. Fix
- Resolve failures from step 5 with minimal blast radius.

7. Test
- Re-run relevant tests until stable.

8. Improve
- Upgrade quality after stability: readability, performance, docs, ergonomics, observability.

9. Test
- Validate improvements did not regress behavior.

10. Fix or Launch Decision
- If red or risky: fix and return to Test.
- If green and acceptable risk: prepare launch.

11. Launch
- Publish/deploy/release with verification and rollback awareness.
- Output: release confirmation and post-launch check result.

## Operating Rules

- Prefer small increments and frequent validation over large untested changes.
- Keep a clear audit trail: what changed, why, what proved it works.
- If blocked, reroute quickly, then merge best parts back into one path.
- Treat this flow as iterative: repeat `Fix -> Test -> Improve -> Test` as needed.
