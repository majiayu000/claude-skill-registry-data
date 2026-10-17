---
name: gortex-domain-grade-3-dirs-assessmentcategory
description: "Work in the domain/grade +3 dirs · AssessmentCategory area — 46 symbols across 6 files (66% cohesion)"
---

# domain/grade +3 dirs · AssessmentCategory

46 symbols | 6 files | 66% cohesion

## When to Use

Use this skill when working on files in:
- `src/domain/grade/Assessment.ts`
- `src/domain/grade/AssessmentCategory.ts`
- `src/domain/grade/GradingType.ts`
- `src/shared/types.ts`
- `tests/unit/domain/grade/StudentPerformance.test.ts`
- `tests/unit/renderer/pendingDelete.test.ts`

## Key Files

| File | Symbols |
|------|---------|
| `src/domain/grade/Assessment.ts` | _title, title, category, _sessionId, _isImpromptu, ... |
| `src/domain/grade/AssessmentCategory.ts` | constructor, gradingType, id, _gradingType, type, ... |
| `src/domain/grade/GradingType.ts` | NUMERIC, TERTIARY, GradingType |
| `src/shared/types.ts` | UpdateAssessmentCategoryInput |
| `tests/unit/domain/grade/StudentPerformance.test.ts` | TestPerformance, id, student, score, assessment, ... |
| `tests/unit/renderer/pendingDelete.test.ts` | Item |

## How to Explore

```
analyze(operation:"communities", id:"community-20")
explore(operation:"context", task:"understand domain/grade +3 dirs · AssessmentCategory", format:"gcx")
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
