---
name: lsp-explore
description: First contact with unfamiliar code via strict LSP symbols, definition, and hover before reading files.
---

# lsp-explore

Resolve what a symbol is before reading around it.

## WHEN

- You need a definition, type/docs, or workspace symbol candidates.
- You want semantic navigation before broader grep/read exploration.

## WHEN NOT

- You already know the file and lines. Use `read`.
- You need all usages. Use `lsp-impact`.
- You only need a file outline. Use `lsp-local-symbols`.

## Workflow

1. `LSP { operation: "workspaceSymbols", query }` to locate candidates.
2. `LSP { operation: "goToDefinition", path, position }` for the jump target.
3. `LSP { operation: "hover", path, position }` for type/docs.
4. `read` the exact target when source text is needed.

## Guardrails

- The model-facing tool name is `LSP`.
- `position` is 0-based in the returned server's negotiated encoding.
- Check the strict envelope `status`; `unavailable` is not a guessed fallback.
- TypeScript sessions are semantic-only: cold starts may be slow or time
  out rather than return fast partial answers. `meta.readiness` is advisory
  progress evidence, never a completeness gate.
- Read-only. No edit/write/patch calls.

## EXAMPLE

```json
{"operation":"goToDefinition","path":"src/auth.ts","position":{"line":41,"character":9}}
```

## Budgets

Use 2-4 LSP calls, then read only the exact source you need.
