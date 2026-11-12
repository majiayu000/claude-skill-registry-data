---
name: lsp-fix
description: Turn strict LSP diagnostics into server-backed code-action proposals without mutating files.
---

# lsp-fix

From diagnostic to validated proposal, with SmartEdit owning the write.

## WHEN

- A compiler or language-server diagnostic identifies a failing range.
- You want quick fixes grounded in the server's current document state.

## WHEN NOT

- There is no diagnostic. Use `lsp-explore` or `grep` first.
- You need a non-diagnostic refactor. Use `lsp-safe-refactor`.
- You are checking an already-applied fix. Use `lsp-verify`.

## Workflow

1. `diagnostics` for the file.
2. Choose the exact diagnostic range.
3. Optionally `hover` at the range start for type context.
4. `codeActions` for that range, passing diagnostic context when useful.
5. Return the selected action/proposal. SmartEdit applies it.

## Guardrails

- Do not silently broaden the diagnostic range.
- Check strict envelope status and freshness.
- Code actions are proposals; SmartRead does not apply them.
- Positions and ranges are 0-based in negotiated encoding.

## EXAMPLE

```json
{"operation":"diagnostics","path":"src/auth.ts"}
```

## Budgets

Diagnostics plus one code-action request is the default; add hover only when it resolves ambiguity.
