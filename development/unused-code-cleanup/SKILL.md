---
name: unused-code-cleanup
description: Systematically identify and remove unused imports, variables, and dead code from TypeScript/React projects using --noUnusedLocals and --noUnusedParameters compiler flags
allowed-tools: Read, Edit, Bash, Grep
---

# Unused Code Cleanup

Identify and remove unused imports/variables/dead code from TypeScript/React projects.

## When to Use

- TypeScript projects with unused code warnings
- After major refactoring or feature removal
- Pre-production cleanup for bundle size optimization
- Code quality improvement initiatives

## Detection

| Task | Command |
|------|---------|
| **Detect** | `npx tsc --noEmit --noUnusedLocals --noUnusedParameters 2>&1 \| grep "error TS6133"` |
| **Count** | `... \| wc -l` |
| **High-impact files** | `... \| sed 's/([0-9]*,[0-9]*).*//' \| sort \| uniq -c \| sort -rn \| head -15` |

## Common Patterns

| Pattern | Cause | Impact | Difficulty |
|---------|-------|--------|-----------|
| **Unused imports** | Icon libraries, API types | Smaller bundle | Easy |
| **Dead feature** | Feature removed, code remains | Reveals subsystems | Complex |
| **Unused parameters** | React Query error callbacks | Clean conventions | Easy |
| **Debug snapshots** | Debugging code left in | Runtime performance | Easy |
| **Unused props** | Component refactoring | Interface clarity | Medium |
| **Unused hooks** | Removed functionality | Prevent unnecessary renders | Easy |

## Cleanup Strategy

1. **Prioritize high-impact** → Files with 10+ warnings first
2. **Identify patterns** → Imports (quick wins), state (dead features), parameters (callbacks), variables (debug)
3. **Verify each file** → `npm run build && npx tsc --noEmit`
4. **Track progress** → Start count → Current count

## Key Insights

**Cascading dependencies**: Unused state → unused setters → unused conversion functions → entire dead feature subsystems

**Performance**:
- Removing unused `getQueryData()` improves runtime
- Smaller bundle from unused import removal
- Faster TypeScript compilation

**Debug archaeology**: `beforeCache`/`afterCache` variables reveal debugging history (often paired with removed console.log)

## Common Mistakes

| Mistake | Issue | Solution |
|---------|-------|----------|
| **Remove used destructured** | `error` might be used later | Check all references |
| **Miss dynamic calls** | String references to functions | Search for function name |
| **No build verification** | Reflection/dynamic imports break | Run build after each file |
| **Remove API-required params** | Breaking callback signature | Use `_` for unused params |

## Session Metrics (Example: 2025-11-08)

| Metric | Value |
|--------|-------|
| Warnings | 148 → 101 (32% reduction) |
| Files cleaned | 6 |
| Items removed | 47 |
| Build time | 15.30s |

**Files**:
| File | Warnings | Items |
|------|----------|-------|
| BranchContextDialog.tsx | 22 | Icons, parsing functions, state |
| useRealtimeSync.ts | 12 | Debug snapshot variables |
| useSubtasks.ts | 4 | Unused onError parameters |
| useTasks.ts | 2 | Unused onError parameters |
| api-lazy.ts | 4 | Unused type/API imports |
| LazySubtaskList/* | 5 | queryClient, props, parameters |

## Automation

### ESLint
```json
{
  "rules": {
    "@typescript-eslint/no-unused-vars": ["error", {
      "argsIgnorePattern": "^_",
      "varsIgnorePattern": "^_"
    }]
  }
}
```

### Pre-commit Hook
```bash
#!/bin/bash
unused=$(npx tsc --noEmit --noUnusedLocals --noUnusedParameters 2>&1 | grep "error TS6133" | wc -l)
[ $unused -gt 0 ] && echo "⚠️ $unused unused code warnings"
```

## Quick Reference

| Task | Command |
|------|---------|
| Detect | `npx tsc --noEmit --noUnusedLocals --noUnusedParameters` |
| Count | `... \| grep "error TS6133" \| wc -l` |
| High-impact | `... \| sed 's/([0-9]*,[0-9]*).*//' \| sort \| uniq -c \| sort -rn` |
| Build | `npm run build` |
| TypeScript | `npx tsc --noEmit` |

## Supporting Files

- **[EXAMPLES.md](EXAMPLES.md)** - 9 patterns with before/after code, session example (148→101), cascading dependencies, performance impact
- **[TEMPLATES.md](TEMPLATES.md)** - Detection commands, cleanup workflows, 9 pattern templates, progress tracking
- **[VALIDATION.md](VALIDATION.md)** - Pre/during/post checklists, validation commands, quality checks by pattern, metrics collection
