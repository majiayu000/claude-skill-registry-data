---
name: lsp-verify
description: Verify an applied change with fresh strict LSP diagnostics, definition, and references.
---

# lsp-verify

Re-check semantics after SmartEdit changes the files.

## WHEN

- SmartEdit applied a rename, refactor, or fix.
- You need fresh diagnostics or semantic navigation on the changed state.

## WHEN NOT

- No edit happened.
- You are still scoping a future change. Use `lsp-impact`, `lsp-rename`, or `lsp-fix`.

## Workflow

1. `diagnostics` on each touched file.
2. Re-run `goToDefinition` at the new anchor when resolution matters.
3. Re-run `findReferences` when scope/count matters.
4. Report the strict statuses and any new diagnostics. Do not silently retry mutation.

## Guardrails

- Verification is read-only even when it fails.
- Require fresh results when judging the post-edit state. Freshness means
  synchronized content; `meta.readiness` is advisory progress evidence,
  not a substitute for freshness and not a completeness gate.
- Positions are 0-based in negotiated encoding.
- One failed verification returns evidence to the mutation owner.

## EXAMPLE

```json
{"operation":"diagnostics","path":"src/auth.ts","timeoutMs":5000}
```

## Budgets

One diagnostic pass plus only the semantic checks needed for the edit's acceptance criteria.
