---
name: gortex-application-11-dirs
description: "Work in the application +11 dirs area — 166 symbols across 26 files (63% cohesion)"
---

# application +11 dirs

166 symbols | 26 files | 63% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/application/BinService.ts`
- `src/application/CourseService.ts`
- `src/application/FindingService.ts`
- `src/application/GradeCalculationAppService.ts`
- `src/application/SchoolClassService.ts`
- `src/application/StudentService.ts`
- `src/domain/grade/AssessmentCategory.ts`
- `src/domain/grade/CourseRoster.ts`
- `src/domain/grade/FindingRepository.ts`
- `src/domain/report/CourseReportData.ts`
- `src/infrastructure/persistence/SqliteCourseRepository.ts`
- `src/infrastructure/persistence/SqliteFindingRepository.ts`
- `src/infrastructure/persistence/SqliteGradeRepository.ts`
- `src/infrastructure/persistence/SqliteReportRepository.ts`
- `src/infrastructure/persistence/SqliteStudentPickCountRepository.ts`
- `src/mcp/mcpServer.ts`
- `src/mcp/mcpService.ts`
- `src/renderer/controllers/useSessionGrid.ts`
- `src/renderer/utils/sessionGridModel.ts`
- `tests/integration/application/CourseRosterService.test.ts`
- `tests/integration/application/CourseService.test.ts`
- `tests/integration/application/MitarbeitPickService.test.ts`
- `tests/integration/infrastructure/SqliteSessionRepository.test.ts`
- `tests/unit/domain/grade/CourseRoster.test.ts`
- `tests/unit/renderer/sessionGridMenu.test.ts`

## Key Files

| File | Symbols |
|------|---------|
| `` | sort, map, localeCompare, all, stringify, ... |
| `src/application/BinService.ts` | classes, listAll, courses, students |
| `src/application/CourseService.ts` | courses, list, schoolYearStr, yearResult, courses |
| `src/application/FindingService.ts` | listNotesBySession, note, sessionId, texts |
| `src/application/GradeCalculationAppService.ts` | sessionDates, session, sessionId, calculate, studentId, ... |
| `src/application/SchoolClassService.ts` | list, classes |
| `src/application/StudentService.ts` | schoolClassId, students, list |
| `src/domain/grade/AssessmentCategory.ts` | displayAsGrade |
| `src/domain/grade/CourseRoster.ts` | CourseRoster.of, classStudents, excludedIds |
| `src/domain/grade/FindingRepository.ts` | PerformanceNote |
| `src/domain/report/CourseReportData.ts` | StudentReportEntry, sortStudentsByLastName, PerformanceReportEntry, students |
| `src/infrastructure/persistence/SqliteCourseRepository.ts` | categories, rowToCourse, id, row, compResult, ... |
| `src/infrastructure/persistence/SqliteFindingRepository.ts` | rows, sessionId, findNotesBySession |
| `src/infrastructure/persistence/SqliteGradeRepository.ts` | rows, studentId, findPerformancesByStudent |
| `src/infrastructure/persistence/SqliteReportRepository.ts` | courseId, findCourseReportData, studentEntries, students, courseRow |
| `src/infrastructure/persistence/SqliteStudentPickCountRepository.ts` | findByCourse, rows, courseId |
| `src/mcp/mcpServer.ts` | mcpServer, registerTools |
| `src/mcp/mcpService.ts` | filtered, allPerformances, calculatedGrade, students, sid, ... |
| `src/renderer/controllers/useSessionGrid.ts` | loadPerformances, list, perAssessment |
| `src/renderer/utils/sessionGridModel.ts` | impromptu, sorted, rows, absent, input, ... |
| `tests/integration/application/CourseRosterService.test.ts` | entries, ids |
| `tests/integration/application/CourseService.test.ts` | courseId, excludedOf |
| `tests/integration/application/MitarbeitPickService.test.ts` | impromptus |
| `tests/integration/infrastructure/SqliteSessionRepository.test.ts` | absentRows, sessionId |
| `tests/unit/domain/grade/CourseRoster.test.ts` | ids, students |
| `tests/unit/renderer/sessionGridMenu.test.ts` | entries, summary |

## Entry Points

- `src/mcp/mcpServer.ts::GraderMcpServer.registerTools`
- `src/domain/grade/CourseRoster.ts::CourseRoster.of@8`

## Connected Communities

- **application +10 dirs** (13 cross-edges)
- **application +8 dirs** (8 cross-edges)
- **domain/grade +4 dirs** (8 cross-edges)
- **renderer/utils +2 dirs** (4 cross-edges)
- **domain/student +3 dirs · SchoolYear** (4 cross-edges)
- **domain/grade +1 dirs · rowToPerformance** (2 cross-edges)
- **application +2 dirs · parseCsv** (2 cross-edges)
- **application +6 dirs** (1 cross-edges)
- **domain/report +6 dirs** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-162")
explore(operation:"context", task:"understand application +11 dirs", format:"gcx")
relations(operation:"usages", target:{symbol:"src/mcp/mcpServer.ts::GraderMcpServer.registerTools"}, format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
