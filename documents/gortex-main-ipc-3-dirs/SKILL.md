---
name: gortex-main-ipc-3-dirs
description: "Work in the main/ipc +3 dirs area — 42 symbols across 12 files (76% cohesion)"
---

# main/ipc +3 dirs

42 symbols | 12 files | 76% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/application/AssessmentCategoryService.ts`
- `src/application/GradingService.ts`
- `src/application/ImpromptuAssessmentService.ts`
- `src/application/MitarbeitPickService.ts`
- `src/main/ipc/course.ipc.ts`
- `src/main/ipc/grade.ipc.ts`
- `src/main/ipc/picker.ipc.ts`
- `src/main/ipc/roster.ipc.ts`
- `src/main/ipc/session.ipc.ts`
- `src/main/ipc/student.ipc.ts`
- `tests/unit/main/digigrade-export.schema.test.ts`

## Key Files

| File | Symbols |
|------|---------|
| `` | parse |
| `src/application/AssessmentCategoryService.ts` | courseRepo, constructor, AssessmentCategoryService |
| `src/application/GradingService.ts` | performanceId, deletePerformance |
| `src/application/ImpromptuAssessmentService.ts` | ImpromptuAssessmentService, gradingService, assessmentService, constructor |
| `src/application/MitarbeitPickService.ts` | courseRepo, impromptuService, studentRepo, rosterService, constructor, ... |
| `src/main/ipc/course.ipc.ts` | registerCourseHandlers, classService, categoryService, courseService |
| `src/main/ipc/grade.ipc.ts` | gradeImportService, impromptuService, gradingService, calcService, findingService, ... |
| `src/main/ipc/picker.ipc.ts` | mitarbeitPickService, registerPickerHandlers, pickerService |
| `src/main/ipc/roster.ipc.ts` | registerRosterHandlers, service |
| `src/main/ipc/session.ipc.ts` | registerSessionHandlers, service |
| `src/main/ipc/student.ipc.ts` | registerStudentHandlers, csvImportService, service |
| `tests/unit/main/digigrade-export.schema.test.ts` | doc, withChange, change, fixture |

## Entry Points

- `src/main/ipc/grade.ipc.ts::registerGradeHandlers`
- `src/main/ipc/course.ipc.ts::registerCourseHandlers`
- `src/main/ipc/student.ipc.ts::registerStudentHandlers`
- `src/main/ipc/session.ipc.ts::registerSessionHandlers`
- `src/main/ipc/picker.ipc.ts::registerPickerHandlers`

## Connected Communities

- **application +8 dirs** (6 cross-edges)
- **application +2 dirs · toDto** (5 cross-edges)
- **application +6 dirs** (4 cross-edges)
- **application +2 dirs · pickRandom** (3 cross-edges)
- **application +11 dirs** (2 cross-edges)
- **application +1 dirs · toPerfDtos** (2 cross-edges)
- **application +2 dirs · findById** (1 cross-edges)
- **application** (1 cross-edges)
- **domain/grade +2 dirs** (1 cross-edges)
- **application +1 dirs · list** (1 cross-edges)
- **application +4 dirs · create** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-53")
explore(operation:"context", task:"understand main/ipc +3 dirs", format:"gcx")
relations(operation:"usages", target:{symbol:"src/main/ipc/grade.ipc.ts::registerGradeHandlers"}, format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
