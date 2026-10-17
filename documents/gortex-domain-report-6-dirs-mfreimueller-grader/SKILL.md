---
name: gortex-domain-report-6-dirs
description: "Work in the domain/report +6 dirs area — 48 symbols across 9 files (80% cohesion)"
---

# domain/report +6 dirs

48 symbols | 9 files | 80% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/application/ReportService.ts`
- `src/domain/report/CourseReportData.ts`
- `src/domain/report/ReportGenerator.ts`
- `src/domain/report/ReportRepository.ts`
- `src/infrastructure/asciidoc/AsciidocReportGenerator.ts`
- `src/infrastructure/fs/DataExportService.ts`
- `src/infrastructure/pdf/PdfReportGenerator.ts`
- `src/infrastructure/persistence/SqliteReportRepository.ts`

## Key Files

| File | Symbols |
|------|---------|
| `` | from |
| `src/application/ReportService.ts` | pdfGenerator, gradeCalc, reportRepo, constructor, adocGenerator |
| `src/domain/report/CourseReportData.ts` | CategoryGradeReportEntry, CourseReportData |
| `src/domain/report/ReportGenerator.ts` | ReportGenerator |
| `src/domain/report/ReportRepository.ts` | ReportRepository |
| `src/infrastructure/asciidoc/AsciidocReportGenerator.ts` | AsciidocReportGenerator |
| `src/infrastructure/fs/DataExportService.ts` | constructor, DataExportService, reportRepo |
| `src/infrastructure/pdf/PdfReportGenerator.ts` | isDetailed, catCols, gradeCol, doc, mode, ... |
| `src/infrastructure/persistence/SqliteReportRepository.ts` | constructor, db, SqliteReportRepository |

## Connected Communities

- **application +11 dirs** (2 cross-edges)
- **. +1 dirs · renderTable** (1 cross-edges)
- **application +2 dirs · parseCsv** (1 cross-edges)
- **main +3 dirs** (1 cross-edges)
- **application +10 dirs** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-38")
explore(operation:"context", task:"understand domain/report +6 dirs", format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
