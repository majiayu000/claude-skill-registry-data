---
name: gortex-application-2-dirs-parsecsv
description: "Work in the application +2 dirs · parseCsv area — 45 symbols across 5 files (73% cohesion)"
---

# application +2 dirs · parseCsv

45 symbols | 5 files | 73% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/application/CsvImportService.ts`
- `src/application/GradeImportService.ts`
- `src/application/SchoolYearRolloverService.ts`
- `src/domain/grade/Session.ts`

## Key Files

| File | Symbols |
|------|---------|
| `` | trim, split, add, replace |
| `src/application/CsvImportService.ts` | parts, rows, parseCsv, content, hasHeader, ... |
| `src/application/GradeImportService.ts` | rows, parseCsv, hasHeader, content, parts, ... |
| `src/application/SchoolYearRolloverService.ts` | input, seen, entry, year, key, ... |
| `src/domain/grade/Session.ts` | markAbsent, setStudentNote, studentId, text, studentId, ... |

## Connected Communities

- **application +10 dirs** (5 cross-edges)
- **domain/student +3 dirs · SchoolYear** (2 cross-edges)
- **application +11 dirs** (1 cross-edges)
- **domain/grade +4 dirs** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-12")
explore(operation:"context", task:"understand application +2 dirs · parseCsv", format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
