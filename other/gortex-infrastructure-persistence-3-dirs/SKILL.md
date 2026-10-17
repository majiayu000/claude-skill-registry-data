---
name: gortex-infrastructure-persistence-3-dirs
description: "Work in the infrastructure/persistence +3 dirs area — 114 symbols across 19 files (82% cohesion)"
---

# infrastructure/persistence +3 dirs

114 symbols | 19 files | 82% cohesion

## When to Use

Use this skill when working on files in:
- `src/domain/grade/CourseRosterRepository.ts`
- `src/domain/shared/UnitOfWork.ts`
- `src/infrastructure/persistence/SqliteAssessmentRepository.ts`
- `src/infrastructure/persistence/SqliteCourseRepository.ts`
- `src/infrastructure/persistence/SqliteCourseRosterRepository.ts`
- `src/infrastructure/persistence/SqliteFindingRepository.ts`
- `src/infrastructure/persistence/SqliteGradeRepository.ts`
- `src/infrastructure/persistence/SqliteSchoolClassRepository.ts`
- `src/infrastructure/persistence/SqliteSessionRepository.ts`
- `src/infrastructure/persistence/SqliteStudentPickCountRepository.ts`
- `src/infrastructure/persistence/SqliteStudentRepository.ts`
- `src/infrastructure/persistence/SqliteUnitOfWork.ts`
- `src/infrastructure/persistence/db.ts`
- `tests/integration/infrastructure/DataExportService.test.ts`
- `tests/integration/infrastructure/PdfReportGenerator.test.ts`
- `tests/integration/infrastructure/SqliteAssessmentRepository.test.ts`
- `tests/integration/infrastructure/SqliteGradeRepository.test.ts`
- `tests/integration/infrastructure/SqliteStudentRepository.test.ts`
- `tests/integration/infrastructure/dbFileValidation.test.ts`

## Key Files

| File | Symbols |
|------|---------|
| `src/domain/grade/CourseRosterRepository.ts` | CourseRosterRepository |
| `src/domain/shared/UnitOfWork.ts` | UnitOfWork |
| `src/infrastructure/persistence/SqliteAssessmentRepository.ts` | id, delete |
| `src/infrastructure/persistence/SqliteCourseRepository.ts` | db, id, deleteCategory, refCount, constructor, ... |
| `src/infrastructure/persistence/SqliteCourseRosterRepository.ts` | constructor, studentIds, SqliteCourseRosterRepository, setExcluded, db, ... |
| `src/infrastructure/persistence/SqliteFindingRepository.ts` | delete, id |
| `src/infrastructure/persistence/SqliteGradeRepository.ts` | savePerformance, id, deletePerformance, delete, performance, ... |
| `src/infrastructure/persistence/SqliteSchoolClassRepository.ts` | softDeleteWithDependents, id, restore, row, id, ... |
| `src/infrastructure/persistence/SqliteSessionRepository.ts` | assessment, student, insertNote, delete, note, ... |
| `src/infrastructure/persistence/SqliteStudentPickCountRepository.ts` | courseId, reset |
| `src/infrastructure/persistence/SqliteStudentRepository.ts` | delete, insertInfo, student, schoolClass, restore, ... |
| `src/infrastructure/persistence/SqliteUnitOfWork.ts` | constructor, work, error, result, db, ... |
| `src/infrastructure/persistence/db.ts` | db, migration, Db, runMigrations, filePath, ... |
| `tests/integration/infrastructure/DataExportService.test.ts` | seedData |
| `tests/integration/infrastructure/PdfReportGenerator.test.ts` | seedReportData |
| `tests/integration/infrastructure/SqliteAssessmentRepository.test.ts` | seedSession |
| `tests/integration/infrastructure/SqliteGradeRepository.test.ts` | assessmentId, name, maxPoints, id, year, ... |
| `tests/integration/infrastructure/SqliteStudentRepository.test.ts` | year, seedSchoolClass, insertStudent |
| `tests/integration/infrastructure/dbFileValidation.test.ts` | createGraderDb, path, db, name |

## Entry Points

- `src/infrastructure/persistence/SqliteCourseRepository.ts::SqliteCourseRepository.hardDelete`
- `src/infrastructure/persistence/SqliteStudentRepository.ts::SqliteStudentRepository.hardDelete`
- `tests/integration/infrastructure/PdfReportGenerator.test.ts::seedReportData`
- `src/infrastructure/persistence/SqliteCourseRepository.ts::SqliteCourseRepository.deleteCategory`
- `tests/integration/infrastructure/DataExportService.test.ts::seedData`

## Connected Communities

- **application +6 dirs** (4 cross-edges)
- **domain/grade +4 dirs** (3 cross-edges)
- **domain/student +3 dirs · SchoolYear** (2 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-50")
explore(operation:"context", task:"understand infrastructure/persistence +3 dirs", format:"gcx")
relations(operation:"usages", target:{symbol:"src/infrastructure/persistence/SqliteCourseRepository.ts::SqliteCourseRepository.hardDelete"}, format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
