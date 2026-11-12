---
name: lsp-safe-refactor
description: Triage strict LSP code actions and refactor proposals while leaving all file mutation to SmartEdit.
---

# lsp-safe-refactor

Ask the language server what refactors it can prove.

## WHEN

- You want server-offered refactors or source actions for a known range.
- You may need to resolve a deferred code action before handing it to SmartEdit.

## WHEN NOT

- It is a simple rename. Use `lsp-rename`.
- A diagnostic is driving the fix. Use `lsp-fix`.
- The server offers no relevant action. Do not invent one.

## Workflow

1. Build the exact 0-based `range` to refactor.
2. `codeActions` with `path`, `range`, and optional `context`.
3. If an action is deferred, call `resolveCodeAction` with the exact returned action.
4. Return the selected proposal and provenance to SmartEdit.

## Guardrails

- `codeActions` requires a range; legacy line/character-only calls are invalid.
- Returned edits are proposals only.
- Require `status: "ok"` and fresh proposal metadata before handoff.
- No edit/write/patch calls from SmartRead.

## EXAMPLE

```json
{"operation":"codeActions","path":"src/auth.ts","range":{"start":{"line":41,"character":0},"end":{"line":44,"character":1}},"context":{"only":["refactor"]}}
```

## Budgets

One code-action request, plus at most one resolve and one impact check.
