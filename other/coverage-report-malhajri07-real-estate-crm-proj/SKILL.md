---
name: coverage-report
description: Report TSDoc/JSDoc coverage across the codebase — what % of exported symbols have documentation blocks, and which files have the worst coverage. Use after /comment-batch sessions and as the C20 verification step.
---

# coverage-report

A simple, dependency-free way to measure how much of the codebase has TSDoc. Don't wait for full TypeDoc tooling — this skill works today.

## Inputs

- **Scope** (optional) — `web` | `api` | `schema` | `all` (default `all`)
- **Format** (optional) — `summary` (default) | `detailed`

## Steps

1. **Find all source files**:
   - Web: `apps/web/src/**/*.{ts,tsx}` excluding `*.test.*`, `*.spec.*`, `node_modules`, `dist`
   - API: `apps/api/{routes,middleware,lib}/**/*.ts`
   - Schema: `data/schema/prisma/schema.prisma` (special handling — `///` triple-slash, not `/**`)
2. **For each file**, count:
   - **Exports**: lines matching `^export (async )?(function|class|const|default function|default class)` or `^export default function`
   - **React components**: lines matching `^export (default )?function [A-Z]` (PascalCase)
   - **TSDoc blocks**: count of `^/\*\*` immediately preceded by an export within 10 lines
3. **Compute** coverage = (documented exports / total exports) × 100, per file and overall.
4. **Format** output:

   **Summary mode:**
   ```
   Coverage report
   ───────────────
   apps/web:    234/812 (29%)  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ░░░░░░░░░░░░░░
   apps/api:    87/192  (45%)  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ░░░
   schema:      12/78   (15%)  ━━━━━━━━━━━━━━━━━━━━━━━░░░░░░░░░░░░░░░░░░░░░░
   ───────────────
   Overall:     333/1082 (31%)

   Worst-covered files:
   - apps/web/src/pages/admin/system-settings.tsx (0/14)
   - apps/web/src/components/admin/data-display/AdminTable.tsx (0/9)
   - apps/api/routes/promotions.ts (1/12)
   ```

   **Detailed mode:** also list every file with `< 50%` coverage and show file:line for each undocumented export.
5. **Compare to last run** if a previous report exists at `Aqarkom_Knowledge/Engineering/Coverage Report.md`.
6. **Save the result** to `Aqarkom_Knowledge/Engineering/Coverage Report.md` with a timestamp so future runs can show deltas.
7. **Recommend next session** — find the C session in [[Sessions/Comment Plan C1-C20]] that targets the worst-covered files and link to it.

## Verification

- [ ] All scope files counted
- [ ] Numbers add up (documented + undocumented = total)
- [ ] Output saved to vault
- [ ] Next-session recommendation included

## Notes

- This is a heuristic, not a perfect parser — it can miss exotic export styles. If a file looks suspiciously low-coverage, eyeball it manually.
- For more rigorous analysis later, we'll add `typedoc --validation.notDocumented` in C1's tooling step. Until then, this skill is "good enough".
- Don't penalize shadcn re-exports or generated files — exclude them from the count.

## Exclusions

Always exclude:
- `node_modules/`
- `dist/`, `build/`
- `*.test.ts`, `*.spec.ts`, `tests/`
- `.next/`, `.vite/`
- Files inside `apps/web/src/components/ui/` that are pure shadcn re-exports (no project logic)
- Generated files (Prisma client, GraphQL codegen)
