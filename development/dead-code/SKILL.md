---
name: dead-code
description: Find and remove unused code added in the current branch. Use when asked to find dead code, remove unused functions, clean up unreferenced code, or check for orphaned controllers/services/SDK functions. Triggers on phrases like "find dead code", "remove unused code", "check for orphaned functions", or "clean up unreferenced exports".
---

# Dead Code Removal

Find and remove code added in the current branch that is never actually used.

## Workflow

1. Get the diff: `git diff master...HEAD --name-only` to find changed files
2. For each changed file, identify newly added exports:
   - Functions, classes, constants, types
   - Controllers, services, SDK functions, API endpoints
   - React components, hooks, utilities
3. Search the codebase for references to each new export
4. Flag exports with zero references (excluding their own definition and re-exports)
5. Remove confirmed dead code or report findings

## What to Look For

**Backend dead code**
- Controllers with no routes pointing to them
- Service methods never called by controllers or other services
- SDK/API client functions never imported in frontend
- Middleware not registered in any route
- Database models with no queries

**Frontend dead code**
- Components never rendered or imported
- Hooks never called
- Utility functions never imported
- Context providers never used
- Redux actions/selectors with no dispatch/useSelector calls

**Shared dead code**
- Types/interfaces never referenced
- Constants never imported
- Exported functions only used internally (should not be exported)

## Search Strategy

For each new export `ExportName`:
1. Grep for import statements: `import.*ExportName` or `require.*ExportName`
2. Grep for direct usage: `ExportName(` or `<ExportName` or `.ExportName`
3. Check barrel files (index.ts) for re-exports
4. Exclude the file where it's defined from results

An export is dead if:
- Zero imports outside its own file
- Zero usages outside its own file
- Not re-exported from a public API barrel

## Guidelines

- Only analyze code added in the current branch (not pre-existing code)
- Be careful with dynamically referenced code (string-based imports, reflection)
- Check for indirect usage through barrel files and re-exports
- When uncertain, report as "potentially unused" rather than auto-deleting
- Preserve code that's part of a public API even if unused internally
- Report a summary: number of dead exports found, files affected, bytes removed
