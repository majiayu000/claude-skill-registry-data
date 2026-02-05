---
name: design-validation
description: Cross-check design artifacts for consistency and completeness. Use before implementation.
---

# Design Validation

Verify that all design documents are consistent and complete before implementation begins.

## Process

1. Check spec → architecture coverage
2. Check architecture → API consistency
3. Verify test plan covers all requirements
4. Confirm security requirements addressed
5. Identify gaps or contradictions

## Output

Create `design-validation.md` using the template in `templates/design-validation.md`.

## Tips

- Every requirement should trace to architecture
- Every API should trace to architecture components
- Test plan should cover all acceptance criteria
- Flag ambiguities, don't assume
- Severity: Critical > Major > Minor
