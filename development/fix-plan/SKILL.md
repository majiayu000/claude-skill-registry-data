---
name: fix-plan
description: Create a remediation/fix plan from code review findings in REVIEW.md (especially outputs from the code-review skill).
---

# Fix Plan

## Workflow

1. Read `.skill-output/REVIEW.md`. If missing or empty, ask the user for the review results or request that code review be run first.
2. Extract each finding and keep its severity (`Must`/`Should`/`May`), location, and suggested fix.
3. Convert findings into an actionable plan ordered by severity and dependency (Must -> Should -> May).
4. Write the plan to `.skill-output/FIX-PLAN.md` (or the path specified by the user). Overwrite the file unless the user asks to append.

## Output Format

Use Japanese headings and concise bullets. Keep steps actionable and include target files.

```markdown
# 修正計画

## 目的
- ...

## 優先順位と対応方針
- Must を最優先で修正し、次に Should、最後に May を対応する
- ...

## 作業ステップ
1. ...
   - 対象: `path/to/file`
   - 対応: ...
2. ...

## 完了条件
- ...
```

## Notes

- If tests are mentioned in the review, add a step for test additions and specify where.
- Keep the plan aligned with the review wording; do not invent new issues.
