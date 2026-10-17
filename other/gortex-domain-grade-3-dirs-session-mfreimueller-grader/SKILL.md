---
name: gortex-domain-grade-3-dirs-session
description: "Work in the domain/grade +3 dirs · Session area — 50 symbols across 5 files (69% cohesion)"
---

# domain/grade +3 dirs · Session

50 symbols | 5 files | 69% cohesion

## When to Use

Use this skill when working on files in:
- `src/application/SessionService.ts`
- `src/domain/grade/Session.ts`
- `src/domain/grade/SessionRepository.ts`
- `src/shared/types.ts`
- `tests/unit/domain/grade/Session.test.ts`

## Key Files

| File | Symbols |
|------|---------|
| `src/application/SessionService.ts` | UpdateSessionInput |
| `src/domain/grade/Session.ts` | assessments, course, date, _course, students, ... |
| `src/domain/grade/SessionRepository.ts` | SessionRepository |
| `src/shared/types.ts` | UpdateSessionInput |
| `tests/unit/domain/grade/Session.test.ts` | aSession, aSession |

## Connected Communities

- **application +11 dirs** (2 cross-edges)
- **application +6 dirs** (1 cross-edges)

## How to Explore

```
analyze(operation:"communities", id:"community-30")
explore(operation:"context", task:"understand domain/grade +3 dirs · Session", format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
