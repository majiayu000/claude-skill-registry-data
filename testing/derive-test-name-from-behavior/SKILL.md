---
name: derive-test-name-from-behavior
description: Produce a single test name in "should <observable behavior>" form from a goal statement. Use when starting the red phase of a TDD cycle and you need a precise, testable name.
---

# Derive a test name from a behavior

Given a behavior description, produce **one** test name that asserts a single observable outcome.

## Rules

1. Start with `should`.
2. Describe the observable outcome, not the implementation. `should reject empty username` is observable; `should call validateUsername` is implementation-detail leakage.
3. Be specific about input shape and expected output. `should return ValidationError when username is empty` beats `should validate username`.
4. One test = one assertion target. If you find yourself joining clauses with `and`, split into two tests.

## Examples

- Behavior: "username validation"
  - Bad: `should validate username`
  - Better: `should reject empty username`
  - Better still: `should reject empty username with a ValidationError`

- Behavior: "OAuth flow"
  - Bad: `should handle OAuth`
  - Better: `should redirect to provider when no token is present`
  - Better still: `should redirect to /oauth/authorize with the configured client_id`

## Reusable outside TDD

Coverage-gap workflows use this when proposing tests for uncovered branches.
