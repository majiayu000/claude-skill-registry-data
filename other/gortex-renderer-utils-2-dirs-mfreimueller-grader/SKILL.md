---
name: gortex-renderer-utils-2-dirs
description: "Work in the renderer/utils +2 dirs area — 56 symbols across 4 files (80% cohesion)"
---

# renderer/utils +2 dirs

56 symbols | 4 files | 80% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/renderer/controllers/useSessionGrid.ts`
- `src/renderer/utils/pendingDelete.ts`
- `src/renderer/utils/sessionGridModel.ts`

## Key Files

| File | Symbols |
|------|---------|
| `` | keys, includes |
| `src/renderer/controllers/useSessionGrid.ts` | pendingCount, categories, sortAscending, students, errorMessage, ... |
| `src/renderer/utils/pendingDelete.ts` | id, options, PendingDeleteOptions, entry, has, ... |
| `src/renderer/utils/sessionGridModel.ts` | a, noteText, student, cellFor, points, ... |

## Entry Points

- `src/renderer/controllers/useSessionGrid.ts::useSessionGrid`

## Connected Communities

- **domain/grade +4 dirs** (3 cross-edges)
- **application +11 dirs** (3 cross-edges)
- **application +10 dirs** (2 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-158")
explore(operation:"context", task:"understand renderer/utils +2 dirs", format:"gcx")
relations(operation:"usages", target:{symbol:"src/renderer/controllers/useSessionGrid.ts::useSessionGrid"}, format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
