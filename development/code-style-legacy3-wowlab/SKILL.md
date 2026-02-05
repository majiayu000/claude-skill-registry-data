---
name: code-style
description: Enforce code style and formatting preferences. Use when writing or reviewing code to ensure consistent style.
---

# Code Style

Project code style and formatting rules.

## Control Flow

**Always use brackets** for control flow statements. Never single-line without braces.

### Wrong

```ts
if (condition) return early;

if (x) doSomething();
else doOther();

for (const item of items) process(item);
```

### Right

```ts
if (condition) {
  return early;
}

if (x) {
  doSomething();
} else {
  doOther();
}

for (const item of items) {
  process(item);
}
```

## DRY - Don't Repeat Yourself

**Always check for existing utilities before creating new ones.**

### Before Writing New Code

1. Search `hooks/` for existing React hooks
2. Search `utils/` for utility functions
3. Search `atoms/utils/` for Jotai helpers
4. Check if a service already provides the functionality
5. Look for similar patterns in the codebase

### If Similar Code Exists

- Extend the existing utility
- Extract common logic into shared function
- Don't duplicate - refactor

## No Backwards Compatibility

**Prefer breaking and remaking over maintaining legacy support.**

### Do

- Delete obsolete code entirely
- Rename things to be correct, update all usages
- Remove deprecated APIs immediately
- Refactor aggressively when improving

### Don't

- Keep old function signatures "for compatibility"
- Add `// @deprecated` and leave code around
- Maintain multiple ways to do the same thing
- Add shims or adapters for old patterns
- Comment out code "in case we need it"

## No Legacy Code

**Remove, don't preserve.**

### Signs of Legacy Code to Remove

- Commented-out code blocks
- Functions with `_old`, `_legacy`, `_deprecated` suffixes
- `// TODO: remove after migration`
- Unused exports
- Dead code paths
- Backwards-compat shims

### When Refactoring

1. Delete the old implementation
2. Write the new implementation
3. Update all call sites
4. Don't provide migration period

## Code Cleanup Rules

- Delete unused imports immediately
- Remove empty files
- Delete unused variables (not just prefix with `_`)
- Remove console.log statements
- Clean up TODO comments by doing them or removing them

## Formatting - Use Utilities

**Always use `@/lib/format` instead of manual formatting.**

### Wrong

```tsx
{
  value.toLocaleString();
}
{
  new Date(date).toLocaleDateString();
}
{
  `${duration}ms`;
}
{
  (percent * 100).toFixed(1) + "%";
}
```

### Right

```tsx
import {
  formatInt,
  formatRelativeToNow,
  formatDurationMs,
  formatPercent,
} from "@/lib/format";

{
  formatInt(value);
}
{
  formatRelativeToNow(date);
}
{
  formatDurationMs(duration);
}
{
  formatPercent(percent);
}
```

### Available Formatters

| Function                | Use For                    |
| ----------------------- | -------------------------- |
| `formatInt`             | Large integers with commas |
| `formatCompact`         | Abbreviated numbers (1.2M) |
| `formatPercent`         | Percentages                |
| `formatNumber`          | Spell description numbers  |
| `formatRelativeToNow`   | Relative time ("2h ago")   |
| `formatDate`            | Formatted dates            |
| `formatDurationMs`      | Millisecond durations      |
| `formatDurationSeconds` | Second durations           |

## Instructions

When writing or reviewing code:

1. Check control flow has brackets
2. Search for existing utilities before creating new ones
3. Delete obsolete code, don't deprecate
4. Remove legacy patterns, don't maintain them
5. Keep codebase lean - when in doubt, delete
6. Use `@/lib/format` for all number/date/duration formatting
