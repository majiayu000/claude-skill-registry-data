---
name: gortex-application-8-dirs
description: "Work in the application +8 dirs area — 158 symbols across 20 files (69% cohesion)"
---

# application +8 dirs

158 symbols | 20 files | 69% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/application/AssessmentCategoryService.ts`
- `src/application/AssessmentService.ts`
- `src/application/CourseRosterService.ts`
- `src/application/CourseService.ts`
- `src/application/GradingService.ts`
- `src/application/SessionService.ts`
- `src/application/StudentPickerService.ts`
- `src/domain/grade/Assessment.ts`
- `src/domain/grade/Course.ts`
- `src/domain/grade/GradedAssessment.ts`
- `src/domain/grade/Session.ts`
- `src/infrastructure/persistence/SqliteAssessmentRepository.ts`
- `src/infrastructure/persistence/SqliteCourseRosterRepository.ts`
- `src/renderer/components/course/GradingTab.vue`
- `src/renderer/components/course/SessionsTab.vue`
- `src/renderer/components/courses/CourseCloneDialog.vue`
- `src/renderer/views/CoursesView.vue`
- `src/shared/errors.ts`
- `tests/unit/renderer/sessionGridModel.test.ts`

## Key Files

| File | Symbols |
|------|---------|
| `` | toLowerCase |
| `src/application/AssessmentCategoryService.ts` | course, listByCourse, courseId |
| `src/application/AssessmentService.ts` | create, delete, sessionId, AssessmentDto, result, ... |
| `src/application/CourseRosterService.ts` | course, classStudents, rosterOfCourse, excluded, rosterOf, ... |
| `src/application/CourseService.ts` | id, compositions, id, updated, cloned, ... |
| `src/application/GradingService.ts` | session, sidResult, student, SaveGradeInput, loadSessionDate, ... |
| `src/application/SessionService.ts` | courseId, sessions, update, session, text, ... |
| `src/application/StudentPickerService.ts` | reset, course, courseId |
| `src/domain/grade/Assessment.ts` | isImpromptu |
| `src/domain/grade/Course.ts` | assessmentCategories, gradeCompositions |
| `src/domain/grade/GradedAssessment.ts` | maxPoints |
| `src/domain/grade/Session.ts` | updateNotes, notes, markPresent, studentId |
| `src/infrastructure/persistence/SqliteAssessmentRepository.ts` | save, catId, assessment, maxPoints |
| `src/infrastructure/persistence/SqliteCourseRosterRepository.ts` | courseId, findExcludedIds, rows |
| `src/renderer/components/course/GradingTab.vue` | members, courseAssessmentIds, loadData, sessions, studentId, ... |
| `src/renderer/components/course/SessionsTab.vue` | startEdit, session |
| `src/renderer/components/courses/CourseCloneDialog.vue` | handleClone, result |
| `src/renderer/views/CoursesView.vue` | ListEntry |
| `src/shared/errors.ts` | constructor, NotFoundError, id, entity |
| `tests/unit/renderer/sessionGridModel.test.ts` | o, numeric, anAssessment |

## Entry Points

- `src/application/CourseService.ts::CourseService.update`
- `src/renderer/components/course/GradingTab.vue#script:268::loadData`
- `src/application/SessionService.ts::SessionService.update`

## Connected Communities

- **application +11 dirs** (13 cross-edges)
- **application +10 dirs** (6 cross-edges)
- **application +6 dirs** (3 cross-edges)
- **domain/grade +3 dirs · hardDeleteStudent** (3 cross-edges)
- **infrastructure/persistence +3 dirs** (1 cross-edges)
- **domain/student +3 dirs · SchoolYear** (1 cross-edges)
- **domain/grade +3 dirs · Session** (1 cross-edges)
- **application +1 dirs · list** (1 cross-edges)
- **application +2 dirs · parseCsv** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-8")
explore(operation:"context", task:"understand application +8 dirs", format:"gcx")
relations(operation:"usages", target:{symbol:"src/application/CourseService.ts::CourseService.update"}, format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
