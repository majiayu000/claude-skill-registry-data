---
name: lsp-impact
description: Measure change blast radius with strict LSP references, implementation lookup, and call hierarchy.
---

# lsp-impact

Map semantic dependents before changing shared code.

## WHEN

- A function, class, interface, or method signature may change.
- You need references, implementations, or caller/callee chains.

## WHEN NOT

- The change is file-local and already understood.
- You only need a definition. Use `lsp-explore`.
- You are verifying an edit that already landed. Use `lsp-verify`.

## Workflow

1. `findReferences` on the anchor.
2. `goToImplementation` when interface/abstract dispatch matters.
3. `prepareCallHierarchy` on the anchor.
4. Pass the returned hierarchy `item` to `incomingCalls` or `outgoingCalls`.
5. Summarize touched files and semantic edges before mutation.

## Guardrails

- Use `LSP` strict operations, not legacy `lsp.foo(...)` syntax.
- Positions are 0-based in negotiated encoding.
- `incomingCalls`/`outgoingCalls` require an `item`, not path+position.
- Read-only. SmartEdit owns any mutation.

## EXAMPLE

```json
{"operation":"findReferences","path":"src/auth.ts","position":{"line":41,"character":9},"includeDeclaration":true}
```

## Budgets

Start with references plus one hierarchy direction. Expand only when the first hop shows meaningful fan-out.
