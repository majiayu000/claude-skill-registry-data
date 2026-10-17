---
name: gortex-application-10-dirs
description: "Work in the application +10 dirs area — 176 symbols across 13 files (75% cohesion)"
---

# application +10 dirs

176 symbols | 13 files | 75% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `scripts/seed.ts`
- `src/application/DigigradeExport.ts`
- `src/application/DigigradeImportService.ts`
- `src/domain/grade/Course.ts`
- `src/domain/grade/Session.ts`
- `src/domain/shared/IdGenerator.ts`
- `src/domain/student/Student.ts`
- `src/infrastructure/asciidoc/AsciidocReportGenerator.ts`
- `src/infrastructure/fs/DataExportService.ts`
- `src/main/menu.ts`
- `src/renderer/utils/sessionGridLabels.ts`
- `tests/integration/application/DigigradeImportService.test.ts`

## Key Files

| File | Symbols |
|------|---------|
| `` | push, substring, values, filter, isNaN, ... |
| `scripts/seed.ts` | key, courseId, normalized, categoryId, studentId, ... |
| `src/application/DigigradeExport.ts` | DigigradeStudent, DigigradeCategory, DigigradePerformance, DigigradeSession, DigigradeAssessment, ... |
| `src/application/DigigradeImportService.ts` | students, a, composition, existing, created, ... |
| `src/domain/grade/Course.ts` | composition, removeGradeComposition, addGradeComposition, addAssessmentCategory, categoryId, ... |
| `src/domain/grade/Session.ts` | studentId, removeStudent |
| `src/domain/shared/IdGenerator.ts` | random, timestamp, generateId |
| `src/domain/student/Student.ts` | key, removeInformation |
| `src/infrastructure/asciidoc/AsciidocReportGenerator.ts` | gradeToWritten, p, maxStr, data, generate, ... |
| `src/infrastructure/fs/DataExportService.ts` | courseId, data, rows, cells, exportCourseReportCsv, ... |
| `src/main/menu.ts` | menu, win, digigradeImportService, template, createAppMenu, ... |
| `src/renderer/utils/sessionGridLabels.ts` | cellAriaLabel, studentName, cell, parts |
| `tests/integration/application/DigigradeImportService.test.ts` | fixture |

## Entry Points

- `src/application/DigigradeImportService.ts::DigigradeImportService.mergeCourse`
- `src/application/DigigradeImportService.ts::DigigradeImportService.mergeSession`
- `src/application/DigigradeImportService.ts::DigigradeImportService.mergeStudents`

## Connected Communities

- **domain/grade +4 dirs** (9 cross-edges)
- **application +11 dirs** (3 cross-edges)
- **application +6 dirs** (2 cross-edges)
- **domain/student +3 dirs · SchoolYear** (2 cross-edges)
- **domain/grade +1 dirs · rowToPerformance** (1 cross-edges)
- **main/ipc +3 dirs** (1 cross-edges)
- **. +1 dirs · create** (1 cross-edges)
- **domain/report +6 dirs** (1 cross-edges)
- **renderer/utils · symbolName** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-37")
explore(operation:"context", task:"understand application +10 dirs", format:"gcx")
relations(operation:"usages", target:{symbol:"src/application/DigigradeImportService.ts::DigigradeImportService.mergeCourse"}, format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
