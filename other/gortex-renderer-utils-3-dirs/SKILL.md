---
name: gortex-renderer-utils-3-dirs
description: "Work in the renderer/utils +3 dirs area — 117 symbols across 12 files (86% cohesion)"
---

# renderer/utils +3 dirs

117 symbols | 12 files | 86% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/renderer/controllers/useGridFocus.ts`
- `src/renderer/controllers/useSessionGrid.ts`
- `src/renderer/controllers/useSessionGridInteractions.ts`
- `src/renderer/utils/panelAnchor.ts`
- `src/renderer/utils/sessionGridInput.ts`
- `src/renderer/utils/sessionGridLabels.ts`
- `src/renderer/utils/sessionGridModel.ts`
- `src/renderer/utils/sessionGridNavigation.ts`
- `tests/unit/renderer/sessionGridLabels.test.ts`
- `tests/unit/renderer/sessionGridMenu.test.ts`
- `tests/unit/renderer/sessionGridNavigation.test.ts`

## Key Files

| File | Symbols |
|------|---------|
| `` | focus, querySelector |
| `src/renderer/controllers/useGridFocus.ts` | focusPosition, anchorOfPosition, el, key, row, ... |
| `src/renderer/controllers/useSessionGrid.ts` | assessmentId, cell, undoDelete, scheduleImpromptuDelete |
| `src/renderer/controllers/useSessionGridInteractions.ts` | selectCellAction, el, direction, studentId, studentId, ... |
| `src/renderer/utils/panelAnchor.ts` | PanelAnchor |
| `src/renderer/utils/sessionGridInput.ts` | key, symbolForKey, resolveSymbolPick, current, picked |
| `src/renderer/utils/sessionGridLabels.ts` | base, column, columnAriaLabel |
| `src/renderer/utils/sessionGridModel.ts` | GridRow, GridGradingType, GridColumn, GridSymbol, GridCellKind, ... |
| `src/renderer/utils/sessionGridNavigation.ts` | col, column, sharedCount, position, NavigationTarget, ... |
| `tests/unit/renderer/sessionGridLabels.test.ts` | aCell, column, o, o |
| `tests/unit/renderer/sessionGridMenu.test.ts` | o, aCell |
| `tests/unit/renderer/sessionGridNavigation.test.ts` | column, impromptu, row, studentId, studentId, ... |

## Entry Points

- `src/renderer/controllers/useSessionGridInteractions.ts::onKeydown`
- `src/renderer/controllers/useSessionGridInteractions.ts::selectCellAction`
- `src/renderer/controllers/useSessionGridInteractions.ts::commitEdit`

## Connected Communities

- **renderer/controllers · attempt** (5 cross-edges)
- **application +6 dirs** (3 cross-edges)
- **renderer/utils +2 dirs** (3 cross-edges)
- **application +10 dirs** (1 cross-edges)
- **. +2 dirs · parsePoints** (1 cross-edges)
- **renderer/utils +1 dirs · navigate** (1 cross-edges)
- **domain/grade +4 dirs** (1 cross-edges)
- **application +11 dirs** (1 cross-edges)
- **renderer/controllers +2 dirs** (1 cross-edges)
- **application +8 dirs** (1 cross-edges)
- **renderer/utils · entry** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-155")
explore(operation:"context", task:"understand renderer/utils +3 dirs", format:"gcx")
relations(operation:"usages", target:{symbol:"src/renderer/controllers/useSessionGridInteractions.ts::onKeydown"}, format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
