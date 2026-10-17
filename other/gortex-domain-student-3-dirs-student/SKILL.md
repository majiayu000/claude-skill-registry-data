---
name: gortex-domain-student-3-dirs-student
description: "Work in the domain/student +3 dirs · Student area — 57 symbols across 8 files (63% cohesion)"
---

# domain/student +3 dirs · Student

57 symbols | 8 files | 63% cohesion

## When to Use

Use this skill when working on files in:
- `src/domain/student/Color.ts`
- `src/domain/student/Student.ts`
- `src/domain/student/StudentId.ts`
- `src/domain/student/StudentRepository.ts`
- `tests/integration/infrastructure/SqliteStudentRepository.test.ts`
- `tests/unit/domain/grade/CourseRoster.test.ts`
- `tests/unit/domain/student/Student.test.ts`
- `tests/unit/domain/student/StudentRepository.test.ts`

## Key Files

| File | Symbols |
|------|---------|
| `src/domain/student/Color.ts` | value, raw, value, Color, constructor, ... |
| `src/domain/student/Student.ts` | deletedAt, schoolClass, id, _color, name, ... |
| `src/domain/student/StudentId.ts` | value, StudentId, value, raw, constructor, ... |
| `src/domain/student/StudentRepository.ts` | StudentRepository |
| `tests/integration/infrastructure/SqliteStudentRepository.test.ts` | color, aStudent, name, id |
| `tests/unit/domain/grade/CourseRoster.test.ts` | sid, lastName, id, deletedAt, aStudent, ... |
| `tests/unit/domain/student/Student.test.ts` | aColor, raw, color |
| `tests/unit/domain/student/StudentRepository.test.ts` | _id, repo.restore, repo.hardDelete, _id |

## Connected Communities

- **application +2 dirs · parseCsv** (1 cross-edges)
- **application +8 dirs** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-36")
explore(operation:"context", task:"understand domain/student +3 dirs · Student", format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
