---
name: result-protection
description: Protect key research results with permanent documentation, drift tests, or artifact-appropriate checks. Use when selecting protection, creating or reviewing tests, or guarding important outputs through integration.
---

# Result Protection

Protect key results from unintended changes. Permanent results documentation suffices when the researcher chooses it; drift tests and other checks add automated protection where useful.

## References

Load only the reference for the protection mechanism in use:

| Reference | Load when |
|---|---|
| `references/drift-test-quality.md` | Writing, refreshing, or reviewing drift/regression tests for selected results. |

Load any domain-specific drift-test reference per the active domain skill's stage-load table at the `protection` stage.

## Scope Gate

- `[BLOCKING]` Protect researcher-confirmed key results, not every intermediate number.
- `[BLOCKING]` Record a protection mechanism and durable home for every researcher-confirmed kept result.
- `[BLOCKING]` A protection update that changes expected results requires the same escalation as a meaningful result change.
