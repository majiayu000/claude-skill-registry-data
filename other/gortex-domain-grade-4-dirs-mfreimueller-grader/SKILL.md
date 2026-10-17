---
name: gortex-domain-grade-4-dirs
description: "Work in the domain/grade +4 dirs area — 110 symbols across 16 files (73% cohesion)"
---

# domain/grade +4 dirs

110 symbols | 16 files | 73% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/domain/grade/GradeCalculationService.ts`
- `src/domain/grade/Session.ts`
- `src/domain/grade/StudentPicker.ts`
- `src/domain/grade/categoryWeightedMean.ts`
- `src/domain/grade/computeFinalGrade.ts`
- `src/infrastructure/persistence/SqliteCourseRosterRepository.ts`
- `src/infrastructure/persistence/SqliteSchoolClassRepository.ts`
- `tests/integration/application/BinService.test.ts`
- `tests/integration/application/DigigradeImportService.test.ts`
- `tests/integration/application/MitarbeitPickService.test.ts`
- `tests/integration/application/SchoolClassService.test.ts`
- `tests/integration/application/SchoolYearRolloverService.test.ts`
- `tests/integration/infrastructure/SqliteCourseRosterRepository.test.ts`
- `tests/integration/infrastructure/SqliteSchoolClassRepository.test.ts`
- `tests/integration/infrastructure/SqliteUnitOfWork.test.ts`

## Key Files

| File | Symbols |
|------|---------|
| `` | reduce, get |
| `src/domain/grade/GradeCalculationService.ts` | GradeCategoryGradeResult, compositions, perf, result, sessionDates, ... |
| `src/domain/grade/Session.ts` | studentNoteOf, studentId |
| `src/domain/grade/StudentPicker.ts` | counts, counts, winner, countOf, min, ... |
| `src/domain/grade/categoryWeightedMean.ts` | totalWeightedSum, compositions, categoryWeightedMean, mean, categoryId, ... |
| `src/domain/grade/computeFinalGrade.ts` | sum, mean, computeFinalGrade, totalWeight, i, ... |
| `src/infrastructure/persistence/SqliteCourseRosterRepository.ts` | grades, countEntries, studentId, courseId, performances |
| `src/infrastructure/persistence/SqliteSchoolClassRepository.ts` | id, courseCount, studentCount, hardDelete, courses, ... |
| `tests/integration/application/BinService.test.ts` | count, table |
| `tests/integration/application/DigigradeImportService.test.ts` | count, snapshot, where, table |
| `tests/integration/application/MitarbeitPickService.test.ts` | count, table |
| `tests/integration/application/SchoolClassService.test.ts` | table, live |
| `tests/integration/application/SchoolYearRolloverService.test.ts` | table, row, id |
| `tests/integration/infrastructure/SqliteCourseRosterRepository.test.ts` | table, count |
| `tests/integration/infrastructure/SqliteSchoolClassRepository.test.ts` | id, table, deletedAt |
| `tests/integration/infrastructure/SqliteUnitOfWork.test.ts` | classCount |

## Entry Points

- `src/domain/grade/StudentPicker.ts::StudentPicker.pickRandom@18`

## Connected Communities

- **application +10 dirs** (7 cross-edges)
- **application +11 dirs** (7 cross-edges)
- **application +6 dirs** (2 cross-edges)
- **infrastructure/persistence +3 dirs** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-46")
explore(operation:"context", task:"understand domain/grade +4 dirs", format:"gcx")
relations(operation:"usages", target:{symbol:"src/domain/grade/StudentPicker.ts::StudentPicker.pickRandom@18"}, format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
