---
name: find-callers
description: Find every page, component, hook, or route that imports or uses a given symbol — function, type, component. Use before refactoring, deleting, or renaming anything to know the blast radius.
---

# find-callers

Pre-refactor reconnaissance. Always run this before changing a public symbol's signature.

## Inputs to gather

- **Symbol name** (function, component, type, hook, constant)
- **Source file** where it's defined (helps disambiguate common names like `Button`)
- **Refactor intent** — rename / signature change / delete / move

## Steps

1. **Confirm the definition exists** — read the source file to see the exact export.
2. **Grep for imports** in `apps/web/src/` and `apps/api/`:
   - `from "@/path/to/file"` style
   - `from "./relative"` style
3. **Grep for usage** of the symbol name itself (filtering matches inside the source file).
4. **Group results** by directory: pages, components, hooks, routes, tests.
5. **Report** as a table: `File:line | Usage type (import / call / type ref)`
6. **Estimate blast radius**: 0-3 callers = small refactor, 4-15 = medium, 16+ = needs planning.
7. **For type changes**, also check for downstream type errors with `/typecheck` after a trial edit.

## Verification

- [ ] Both apps scanned (or scoped if symbol is one-app-only)
- [ ] Tests included in scan
- [ ] Results grouped by directory
- [ ] Blast radius estimate provided

## Notes

- For shadcn/ui primitives (`Button`, `Card`, etc.), filter to project source — node_modules will swamp the results
- For very common names (`use`, `render`), include the source path in the grep to disambiguate
