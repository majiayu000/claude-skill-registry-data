---
name: refactor
description: Refactor implemented product code in bounded increments while preserving observable behavior and compatibility. Use when existing code has a concrete structural problem; use implement for new behavior and bug fixes.
---

# Refactor

Apply the [core](../../README.md#loading-rules); read linked procedures only when their operation applies.
Persona: maintenance engineer, focused on simpler structure with stable observable behavior.
Work on existing implementation.

Retain the agreement, planning, and refactoring evidence in the owning record under
[retention](../../references/retention.md), which states when a spec is required; other direct
work without a spec may use [notes](../../templates/notes.md). At entry, and again when scope
grows, decide whether the refactor requires independent review under
[Review and communication](../../README.md#review-and-communication). If creating a spec, use relevant sections of
[the change record](../../templates/spec.md) under [naming](../../references/naming.md).
Use existing execution records in place. Do not create a product-wide cleanup backlog from
incidental findings.

- Inspect the working tree, relevant implementation, callers, and tests. Identify a concrete
  structural problem and its consequence, such as duplicated business rules or dependencies
  that prevent testing a boundary. Name the bounded target, intended structural result, and
  observable behavior and interfaces that must remain stable.
- Distinguish refactoring from defect correction or new behavior. If the requested outcome
  changes behavior, route that part to [implement](../implement/SKILL.md),
  or [specify](../specify/SKILL.md) if scope is unsettled. Do not silently
  fix discovered bugs or expand into adjacent modules. No change is valid when the proposed
  abstraction or rewrite has no demonstrated benefit.
- Use reversible increments with focused regression checks; record sequencing only when useful.
  Prefer a local change over a speculative framework or rewrite.
- Apply the [TDD rules](../../references/tdd.md) for behavior-preserving restructuring.
  A separately authorized behavior change follows the test-first sequence in
  [implement](../implement/SKILL.md).
- Establish the relevant baseline before edits. Report pre-existing failures and distinguish
  them from regressions; resolve failures that prevent verifying the affected behavior before
  proceeding with dependent changes. With TDD `none`, verification remains required.
- When using or creating a spec, apply the [queue rules](../../references/queue.md) for its
  row and lifecycle state.
- Run regression checks at boundaries where failures can be attributed. Independent assignments
  may run in parallel; dependent work waits for verified prerequisites. Preserve public contracts,
  persisted formats, and user-visible behavior.
- Inspect the final diff for unintended behavior changes and unnecessary abstractions. Run
  agreed and required checks. Record the structural result, baseline and final evidence, and
  limitations in the owning record.

## Commit verified increments

Establish and preserve the passing baseline, satisfy the selected coverage policy, and run
required regression checks, then apply the [commit procedure](../../references/commits.md).

## Next action

Continue the next authorized increment while the structural objective remains unmet; resolve
a failed or missing check before dependent edits. At the authorized boundary, name required
review, acceptance, or delivery with its diff scope and preservation constraints.
