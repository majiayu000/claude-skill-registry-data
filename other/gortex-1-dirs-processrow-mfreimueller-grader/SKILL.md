---
name: gortex-1-dirs-processrow
description: "Work in the . +1 dirs · processRow area — 43 symbols across 2 files (70% cohesion)"
---

# . +1 dirs · processRow

43 symbols | 2 files | 70% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/application/CsvImportService.ts`

## Key Files

| File | Symbols |
|------|---------|
| `` | entries |
| `src/application/CsvImportService.ts` | rows, classRepo, student, findOrCreateClass, processRow, ... |

## Entry Points

- `src/application/CsvImportService.ts::CsvImportService.handleExistingStudent`
- `src/application/CsvImportService.ts::CsvImportService.importCsv`

## Connected Communities

- **application +10 dirs** (8 cross-edges)
- **application +6 dirs** (2 cross-edges)
- **domain/student +3 dirs · SchoolYear** (1 cross-edges)
- **application +4 dirs · create** (1 cross-edges)
- **application +2 dirs · parseCsv** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-9")
explore(operation:"context", task:"understand . +1 dirs · processRow", format:"gcx")
relations(operation:"usages", target:{symbol:"src/application/CsvImportService.ts::CsvImportService.handleExistingStudent"}, format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
