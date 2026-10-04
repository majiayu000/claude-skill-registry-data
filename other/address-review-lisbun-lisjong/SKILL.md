---
name: address-review
description: Resolve blocking review findings on an existing PR without broadening its scope.
argument-hint: "[pr-number]"
disable-model-invocation: true
---

Address unresolved review findings for PR $0.

1. Read `AGENTS.md`, the PR, its Issue, current diff, and review comments.
2. Identify unresolved blocking findings and verify each one independently.
3. Make the minimum change required to resolve valid blocking findings.
4. Do not implement unrelated non-blocking suggestions.
5. Add or update focused regression tests where the fix changes behavior.
6. Run focused tests and deterministic checks required by `AGENTS.md`.
7. Re-review the changed area and its direct regression boundary.
8. Commit and push the fix. Do not merge.

Report each original blocking finding as `resolved`, `not reproduced`, or `still unresolved`.
