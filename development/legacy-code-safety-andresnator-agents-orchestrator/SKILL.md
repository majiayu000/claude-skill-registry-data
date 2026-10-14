---
name: legacy-code-safety
description: "Trigger: legacy code safety, safe refactor. Make untested code safe to change."
license: Apache-2.0
metadata:
  author: gentle-ai
  adapted_by: andresnator
  source: gentle-ai/plan-refactor
  version: "1.1.1"
  status: testing
---

# Legacy Code Safety
Legacy code is code without a sufficient test safety net. The goal is not to make it beautiful first; the goal is to make it safe to change.

## Principles

- Capture current behavior before refactoring.
- Treat current observable behavior as the contract until explicitly changed.
- Search for seams before structural changes.
- Break dependencies minimally to enable characterization tests.
- Refactor incrementally in small, reversible steps.
- Separate behavior-preserving refactor from functional change.
- Validate after every step.
- Protect public contracts.
- Document rollback before implementation begins.

## Legacy Code Change Algorithm

Every safe change to legacy code follows the same pipeline: (1) identify change points, (2) find test points, (3) break dependencies, (4) write characterization tests, (5) change and refactor. Plans over legacy code should make these five steps recognizable in their task ordering.

## Cover & Modify

Cover & Modify, never Edit & Pray: no plan step modifies code that is not covered by tests (the "software vise"). If coverage is not affordable, the step shrinks until it is, or it moves behind a hardening task.

## Cheap impact mapping

Lean on the compiler: in statically typed code, deliberately changing a signature or type makes the compiler enumerate every use site — a free impact map when call hierarchies are unclear.

## Sprout and Wrap (routing note)

Sprout Method/Class (grow new, tested code called from the untested flow) and Wrap Method/Class (add behavior before or after the untested code) are mitigation routes for delivering NEW logic when putting the class under test is not affordable yet. They add behavior, so they never appear as tasks in a behavior-preserving refactor group. Record them as separate behavior-changing work for Orchestraitor. Use sprout for new logic inside the flow and wrap for behavior before or after it; escalate to the class variant when the original cannot be instantiated.
