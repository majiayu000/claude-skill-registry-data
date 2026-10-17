---
name: gortex-application-6-dirs
description: "Work in the application +6 dirs area — 119 symbols across 13 files (64% cohesion)"
---

# application +6 dirs

119 symbols | 13 files | 64% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/application/AssessmentCategoryService.ts`
- `src/application/GradeImportService.ts`
- `src/application/GradingService.ts`
- `src/application/ImpromptuAssessmentService.ts`
- `src/application/MitarbeitPickService.ts`
- `src/domain/grade/Course.ts`
- `src/domain/grade/performanceNormalization.ts`
- `src/infrastructure/persistence/SqliteGradeRepository.ts`
- `src/infrastructure/persistence/SqliteSessionRepository.ts`
- `src/main/config.ts`
- `src/shared/types.ts`
- `tests/integration/application/SessionService.test.ts`

## Key Files

| File | Symbols |
|------|---------|
| `` | log, slice, find |
| `src/application/AssessmentCategoryService.ts` | input, CreateAssessmentCategoryInput, create, reconstituted, category, ... |
| `src/application/GradeImportService.ts` | reconstituted, maxPoints, index, created, student, ... |
| `src/application/GradingService.ts` | sessionDate, assessment, recordPerformance, sidResult, perfResult, ... |
| `src/application/ImpromptuAssessmentService.ts` | common, CreateImpromptuInput, ImpromptuResultDto, input, assessed, ... |
| `src/application/MitarbeitPickService.ts` | category, MitarbeitPickDto, studentId, course, RecordMitarbeitPickInput, ... |
| `src/domain/grade/Course.ts` | getMitarbeitCategory |
| `src/domain/grade/performanceNormalization.ts` | value, normalized, gradedAssessment, performance, performanceToValue, ... |
| `src/infrastructure/persistence/SqliteGradeRepository.ts` | rows, assessmentId, findPerformancesByAssessment |
| `src/infrastructure/persistence/SqliteSessionRepository.ts` | findByCourse, rows, courseId |
| `src/main/config.ts` | defaultPath, envPath, resolveDbPath, settings, cliPath, ... |
| `src/shared/types.ts` | GradeImportResultDto |
| `tests/integration/application/SessionService.test.ts` | created, createSession, createSession, created |

## Entry Points

- `src/application/GradeImportService.ts::GradeImportService.processRow`
- `src/application/AssessmentCategoryService.ts::AssessmentCategoryService.create`

## Connected Communities

- **application +10 dirs** (18 cross-edges)
- **application +8 dirs** (13 cross-edges)
- **application +11 dirs** (4 cross-edges)
- **application +2 dirs · parseCsv** (3 cross-edges)
- **domain/grade +1 dirs · rowToPerformance** (2 cross-edges)
- **domain/grade +3 dirs · hardDeleteStudent** (2 cross-edges)
- **infrastructure/persistence · rowToSession** (1 cross-edges)
- **main +3 dirs** (1 cross-edges)
- **main/ipc +3 dirs** (1 cross-edges)
- **. +2 dirs · parsePoints** (1 cross-edges)
- **. +1 dirs · processRow** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-13")
explore(operation:"context", task:"understand application +6 dirs", format:"gcx")
relations(operation:"usages", target:{symbol:"src/application/GradeImportService.ts::GradeImportService.processRow"}, format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
