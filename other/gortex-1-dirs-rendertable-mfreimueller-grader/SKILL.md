---
name: gortex-1-dirs-rendertable
description: "Work in the . +1 dirs · renderTable area — 43 symbols across 2 files (90% cohesion)"
---

# . +1 dirs · renderTable

43 symbols | 2 files | 90% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/infrastructure/pdf/PdfReportGenerator.ts`

## Key Files

| File | Symbols |
|------|---------|
| `` | fill |
| `src/infrastructure/pdf/PdfReportGenerator.ts` | data, h, x, strokeGrid, text, ... |

## Entry Points

- `src/infrastructure/pdf/PdfReportGenerator.ts::PdfReportGenerator.renderTable`

## Connected Communities

- **domain/report +6 dirs** (2 cross-edges)
- **application +11 dirs** (1 cross-edges)
- **domain/grade +4 dirs** (1 cross-edges)
- **. +2 dirs · computeSegments** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-41")
explore(operation:"context", task:"understand . +1 dirs · renderTable", format:"gcx")
relations(operation:"usages", target:{symbol:"src/infrastructure/pdf/PdfReportGenerator.ts::PdfReportGenerator.renderTable"}, format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
