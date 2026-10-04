---
name: audit-tokens
description: Find hardcoded hex/rgb/hsl colors in frontend files that should be using CSS variable tokens (bg-background, text-foreground, etc.). Use after UI changes and during design-system audits.
---

# audit-tokens

Per ADR 003, all colors come from CSS variable tokens defined in `apps/web/src/index.css` (HSL emerald hue 160). Hardcoded colors break dark mode and theme consistency.

## What to look for

- Hex codes: `#fff`, `#10b981`, `#22c55e`, etc.
- `rgb(...)`, `rgba(...)`, `hsl(...)` literals
- Tailwind palette classes: `bg-emerald-500`, `text-red-600`, `border-gray-300`, etc.
- Inline `style={{ color: '...' }}`

## What's allowed

- CSS variable references: `bg-background`, `text-foreground`, `text-muted-foreground`, `bg-card`, `bg-primary`, `text-primary-foreground`, `border-border`, `bg-destructive`, `text-destructive`, `bg-warning`, etc.
- Arbitrary values referencing variables: `bg-[hsl(var(--warning)/0.3)]`
- Anything in `apps/web/src/index.css` (the source of truth)

## Steps

1. **Grep** for hex patterns: `#[0-9a-fA-F]{3,8}` in `apps/web/src/**/*.{tsx,ts,css}`
2. **Grep** for `rgb(`, `rgba(`, `hsl(` literals (excluding `var(--...)` references)
3. **Grep** for Tailwind palette classes: `(bg|text|border|ring|fill|stroke)-(red|green|blue|yellow|emerald|amber|gray|slate|...)-\d+`
4. **Filter** allowed exceptions:
   - `index.css` itself
   - Storybook / dev-only files
   - Files in `tests/` (test fixtures may use hardcoded values)
5. **Group by file** with proposed token replacements:
   - `bg-emerald-500` → `bg-primary`
   - `text-red-600` → `text-destructive`
   - `bg-gray-50` → `bg-muted`
   - `border-gray-200` → `border-border`
6. **Report** the violations and ask before fixing.

## Verification

- [ ] All frontend files scanned
- [ ] `index.css` excluded
- [ ] Replacements suggested per match
- [ ] User asked before bulk-replacing

## Notes

- The project's destructive token uses `hsl(0 72% 51%)` (softened from default 84% saturation)
- See [[Architecture/Frontend Structure]] in the vault for the full token list
