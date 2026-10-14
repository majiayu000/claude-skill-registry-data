---
name: java-exception-robustness
description: "Trigger: Java exceptions, error handling, try-with-resources, resource cleanup, checked exceptions, robustness. Design Java failure handling safely."
license: MIT
metadata:
  author: andresnator
  status: testing
  version: "1.0.4"
---

# Skill: java-exception-robustness

## Activation Contract

Use this skill when reviewing or designing Java exception handling, resource cleanup, checked/unchecked exception choices, failure boundaries, retry/fallback policy, and robust service behavior.

Do **not** use this skill for logging-only changes, security-only auditing, non-Java error models, or framework-specific exception mapping with no Java design question.

## Responsibility

This skill teaches Java failure-handling design. It does not call other skills, hide failures by default, or invent business recovery policies.

## Required Context

- Operation being protected.
- Who can recover from failures.
- Resource ownership and cleanup needs.
- Whether this is library, application, batch, or long-running service code.
- Sensitive-data constraints in messages/logs.

## Context Budget

- Keep this `SKILL.md` focused on error boundaries.
- Use `references/java-exception-guidance.md` for detailed choices.

## Hard Rules

- Do not swallow exceptions silently.
- Release resources deterministically with try-with-resources or `finally`.
- Catch exceptions only where you can add context, recover, translate boundary errors, or enforce cleanup.
- Preserve stack traces when wrapping unless there is a deliberate boundary sanitization.
- Do not expose sensitive internal data in exception messages returned to users.
- Define boundary policy for long-running services: discard unit of work, log safely, cleanup, and continue or stop.

## Decision Gates

| Condition | Action |
|---|---|
| Resource acquired | Use try-with-resources or explicit finally cleanup. |
| Caller can recover | Use checked exception or documented recoverable result. |
| Caller cannot recover | Use unchecked exception or boundary translation. |
| Exception crosses trust/user boundary | Sanitize message and preserve internal diagnostics safely. |
| Broad catch appears | Allow only at orchestration boundary with clear policy. |

## Execution Steps

1. Identify failure sources and recovery owner.
2. Map resource acquisition and release.
3. Choose catch/propagate/wrap/translate behavior.
4. Check message sensitivity and logging policy.
5. Return a robust failure-handling plan or code shape.

## Output Contract

Return:

- Failure boundary verdict.
- Exception strategy and recovery owner.
- Resource cleanup requirements.
- Message/logging sensitivity notes.
- Example handling shape when useful.

## References

- `references/java-exception-guidance.md` — Exception choices, cleanup, and boundary policy.

## Assets

- None.
