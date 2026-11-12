---
name: lsp-cross-root
description: Route strict LSP requests across multiple workspaces with explicit workspace and exact server selection.
---

# lsp-cross-root

Make routing explicit when one task spans multiple roots.

## WHEN

- Files belong to different project roots.
- Multiple same-language servers make routing ambiguous.
- You need deterministic per-root provenance.

## WHEN NOT

- One workspace and one routable server are sufficient.
- The question is path authorization. SmartRead does not invent that policy.

## Workflow

1. Identify the owning workspace for each target file.
2. Pass `workspace` explicitly on cross-root requests.
3. Pass exact `server` descriptor id when multiple candidates exist.
4. Run each root's request independently and retain envelope provenance.
5. Merge results only after preserving workspace/server labels.

## Guardrails

- The strict field is `workspace`, not legacy `root`.
- `server` is exact descriptor-id routing; there is no fuzzy match.
- An ambiguous/unavailable envelope is a routing result, not permission denial.
- Read-only. Cross-root read permission remains external to SmartRead.

## EXAMPLE

```json
{"operation":"goToDefinition","workspace":"/repo/app-a","server":"typescript","path":"/repo/app-a/src/auth.ts","position":{"line":9,"character":4}}
```

## Budgets

One scoped call chain per workspace; avoid broad duplicate searches across every root.
