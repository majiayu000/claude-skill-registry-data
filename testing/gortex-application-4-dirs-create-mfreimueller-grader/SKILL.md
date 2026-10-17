---
name: gortex-application-4-dirs-create
description: "Work in the application +4 dirs · create area — 60 symbols across 7 files (68% cohesion)"
---

# application +4 dirs · create

60 symbols | 7 files | 68% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/application/CourseService.ts`
- `src/application/StudentService.ts`
- `src/domain/student/AdditionalInformation.ts`
- `src/domain/student/Student.ts`
- `src/renderer/controllers/useSessionGrid.ts`
- `tests/integration/application/StudentService.test.ts`

## Key Files

| File | Symbols |
|------|---------|
| `` | error |
| `src/application/CourseService.ts` | SchoolClassRefDto |
| `src/application/StudentService.ts` | sidResult, id, updated, AdditionalInfoEntry, student, ... |
| `src/domain/student/AdditionalInformation.ts` | key |
| `src/domain/student/Student.ts` | existingIndex, changeColor, equals, other, info, ... |
| `src/renderer/controllers/useSessionGrid.ts` | studentId, absent, result, setAbsence |
| `tests/integration/application/StudentService.test.ts` | createStudent, created |

## Connected Communities

- **application +10 dirs** (2 cross-edges)
- **renderer/controllers +2 dirs** (1 cross-edges)
- **application +11 dirs** (1 cross-edges)
- **domain/student +3 dirs · SchoolYear** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-19")
explore(operation:"context", task:"understand application +4 dirs · create", format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
