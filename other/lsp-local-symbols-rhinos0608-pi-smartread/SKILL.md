---
name: lsp-local-symbols
description: Outline a file with strict LSP document symbols so reads can target exact source slices.
---

# lsp-local-symbols

Outline first, read slices second.

## WHEN

- A file is large or has many members.
- You need symbol ranges before selecting a `read` slice.

## WHEN NOT

- The file is small enough for a normal read.
- You need cross-file symbols. Use `lsp-explore`.
- You need usage scope. Use `lsp-impact`.

## Workflow

1. `LSP { operation: "documentSymbols", path }`.
2. Pick the relevant returned symbol/range.
3. Convert the 0-based LSP range to the 1-based `read { offset, limit }` line convention.
4. Read only the required slice.

## Guardrails

- LSP positions/ranges are 0-based; `read.offset` is 1-based.
- Keep the strict envelope provenance if server choice matters.
- Read-only. No mutation calls.

## EXAMPLE

```json
{"operation":"documentSymbols","path":"src/auth.ts","limit":100}
```

## Budgets

One LSP outline call plus one or two targeted reads.
