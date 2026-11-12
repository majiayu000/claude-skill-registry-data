---
name: lsp-rename
description: Scope and request a strict LSP rename proposal; only applyProposal applies it, through SmartEdit.
---

# lsp-rename

Propose a semantic rename without writing files.

## WHEN

- A code symbol needs a semantic rename.
- You need renameability, usage scope, and a server-produced WorkspaceEdit proposal.

## WHEN NOT

- It is a text-only rename across non-code files. Use `grep`.
- You only need usage scope. Use `lsp-impact`.
- The rename has already been applied. Use `lsp-verify`.

## Workflow

1. `prepareRename` on the anchor.
2. `findReferences` to inspect scope.
3. `rename` with `newName` to obtain a proposal.
4. Hand the proposal and provenance to SmartEdit, or apply it with applyProposal. Do not write files directly.

## Guardrails

- `rename` is proposal-only and never auto-retries after a server crash.
- Use only an `ok` envelope with `meta.freshness.state === "fresh"`.
- Positions are 0-based in `server.positionEncoding`.
- Only applyProposal mutates, through SmartEdit's evidence-checked edit path.

## EXAMPLE

```json
{"operation":"rename","path":"src/auth.ts","position":{"line":41,"character":9},"newName":"authorizeRequest"}
```

## Budgets

Usually 2-3 LSP calls: prepare, references, proposal.
