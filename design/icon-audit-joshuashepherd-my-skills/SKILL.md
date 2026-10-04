---
name: icon-audit
description: Audit and fix icon usage for movemental — mixed libraries, wrong sizes, hardcoded colors, missing accessibility, and illustration anti-patterns. Enforces lucide-react as the single icon library.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit
---

Audit and fix icon anti-patterns across the movemental codebase.

Target: $ARGUMENTS

If no target is provided, scan `src/components/` and `src/app/(site)/`.

## Before Starting

1. Read `docs/design/DESIGN.md` — icon conventions.
2. Grep for icon imports to understand current usage patterns.

## Icon Standard

**Single library: `lucide-react`** — no other icon libraries allowed.

### Size Scale
| Context | Size | Tailwind |
|---------|------|----------|
| Inline with text | 16px | `size-4` |
| Standard UI | 20px | `size-5` |
| Feature cards | 20-24px | `size-5` or `size-6` |
| Hero features | 24px | `size-6` |

### Color
- Icons inherit `currentColor` by default
- Use semantic tokens via parent: `text-primary`, `text-muted-foreground`, etc.
- **Never** hardcode icon colors (`text-blue-600`, `fill="#000"`)

### Accessibility
- Decorative icons: `aria-hidden` attribute
- Meaningful icons (no adjacent label): wrap with `<span className="sr-only">Label</span>`
- Icon-only buttons: must have `aria-label`

## Audit Checklist

### 1. WRONG LIBRARY (Critical)
Search for non-lucide icon imports:
- `@heroicons/react` → replace with lucide equivalent
- `react-icons` → replace with lucide equivalent
- `@radix-ui/react-icons` → replace with lucide equivalent
- Material Symbols (`material-symbols-outlined`) → replace with lucide
- Inline SVGs that duplicate a lucide icon → use the lucide component

### 2. SIZE INCONSISTENCY (High)
- Mixed icon sizes in the same context (e.g., `size-4` and `size-6` in the same card grid)
- Icons not using the Tailwind `size-*` utility (using `w-5 h-5` instead of `size-5`)
- Icons larger than `size-6` (24px) in non-hero contexts

### 3. COLOR VIOLATIONS (High)
- Hardcoded colors: `text-blue-600`, `fill="#0053db"`, `stroke="black"`
- Should use parent's semantic color or explicit token: `text-primary`, `text-muted-foreground`

### 4. ACCESSIBILITY (Medium)
- Decorative icons missing `aria-hidden`
- Icon-only buttons without `aria-label`
- Icons conveying meaning without text alternative

### 5. FLEX COMPRESSION (Medium)
- Icons inside flex containers without `shrink-0` (can get squished)
- Fix: add `shrink-0` to icons in flex layouts

## Output Format

```
## Icon Audit Report

### Summary
- Files scanned: X
- Icons found: X
- Violations: X

### Issues
| # | Severity | File:Line | Issue | Fix |
|---|----------|-----------|-------|-----|

### Fixes Applied
- file.tsx — description of change
```

## Rules

- Lucide is the ONLY icon library. No exceptions.
- Icons use `size-*` utility, not `w-*/h-*` pairs.
- All decorative icons get `aria-hidden`.
- Never modify `src/components/ui/*` — only domain components and pages.
