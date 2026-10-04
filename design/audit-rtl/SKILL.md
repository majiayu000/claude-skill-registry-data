---
name: audit-rtl
description: Find LTR-only Tailwind classes (ml-, mr-, pl-, pr-, left-, right-, text-left, text-right) in JSX files. These break the Arabic-first layout. Use after editing pages and before /complete-session.
---

# audit-rtl

The app is RTL-first. Any directional class that uses `left`/`right` instead of logical `start`/`end` will visually break for Arabic users.

## Forbidden patterns

| Use this | Not this |
|---|---|
| `ms-2` | `ml-2` |
| `me-4` | `mr-4` |
| `ps-3` | `pl-3` |
| `pe-6` | `pr-6` |
| `start-0` | `left-0` |
| `end-2` | `right-2` |
| `text-start` | `text-left` |
| `text-end` | `text-right` |
| `border-s` | `border-l` |
| `border-e` | `border-r` |
| `rounded-s-md` | `rounded-l-md` |
| `rounded-e-md` | `rounded-r-md` |

## Steps

1. **Grep** `apps/web/src/` for each forbidden pattern in `.tsx` and `.ts` files. Use a single combined regex if possible.
2. **Filter out** false positives:
   - Inside `// rtl-ok` comment annotations (rare opt-out)
   - Inside CSS variables / arbitrary values that don't refer to direction
   - Inside imported third-party components we can't change
3. **Group by file** with line numbers.
4. **Report** as a table — file, line, current class, suggested replacement.
5. **Offer to fix** — apply replacements one file at a time, asking the user to approve the first one as a sanity check, then batch the rest.

## Verification

- [ ] All `.tsx` files scanned
- [ ] False positives filtered
- [ ] Replacements proposed (not applied without permission)

## Anti-patterns

- Don't blindly replace all occurrences — `text-right` inside a `dir="ltr"` block (e.g. an English-only admin panel) is intentional
- Don't replace classes inside `node_modules`
- Don't change `right` / `left` in inline JS logic (those are computed values, not Tailwind classes)
