---
name: gortex-application-2-dirs-pickrandom
description: "Work in the application +2 dirs · pickRandom area — 52 symbols across 3 files (80% cohesion)"
---

# application +2 dirs · pickRandom

52 symbols | 3 files | 80% cohesion

## When to Use

Use this skill when working on files in:
- `src/application/StudentPickerService.ts`
- `src/domain/grade/StudentPickCountRepository.ts`
- `src/infrastructure/persistence/SqliteStudentPickCountRepository.ts`

## Key Files

| File | Symbols |
|------|---------|
| `src/application/StudentPickerService.ts` | courseId, courseId, pickRepo, roster, student, ... |
| `src/domain/grade/StudentPickCountRepository.ts` | StudentPickCountRepository |
| `src/infrastructure/persistence/SqliteStudentPickCountRepository.ts` | courseId, count, increment, courseId, studentId, ... |

## Connected Communities

- **application +11 dirs** (3 cross-edges)
- **domain/grade +4 dirs** (2 cross-edges)
- **application +6 dirs** (2 cross-edges)
- **application +8 dirs** (1 cross-edges)
- **infrastructure/persistence +3 dirs** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-18")
explore(operation:"context", task:"understand application +2 dirs · pickRandom", format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
