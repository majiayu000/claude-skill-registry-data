---
name: elysium-audit
description: Audit HTML/CSS/JS files for code quality violations per CLAUDE.md rules. Reports issues grouped by file without auto-fixing.
---

# Elysium Audit

Run a read-only code quality audit on the specified page(s). Report findings only — do not auto-fix.

## Scope

Audit one or more of: `index.html`, `pages/games/arc-raiders.html`, `pages/games/valorant.html`, and their associated CSS/JS files.

## What to Check

### HTML
- Inline styles (`style="..."` attributes)
- Images missing `alt` attribute
- Non-hero images missing `loading="lazy"`
- Scripts missing `defer`
- Hardcoded prices in HTML
- Missing `<title>` or `<meta name="description">`
- Inconsistent nav/footer across pages

### CSS
- Hardcoded hex/rgb values not using `global.css` variables
- Duplicate selectors within the same file
- Page-specific styles placed in `global.css` or `components.css`
- Stacked `backdrop-filter` layers
- Missing `@property --arc-trace-angle` when travelling line is used

### JavaScript
- `console.log` statements
- Page-specific logic in `main.js` or shared logic in page JS
- Global variable pollution (non-const top-level declarations)
- Page JS files exceeding ~300 lines

### Assets
- Broken `src` paths (referenced files that don't exist)
- Non-WebP images that should be WebP
- Non-PNG icons that need transparency
- Audio files present (none should exist)
- References to `orderpanelbg.webp` (removed permanently)

## Workflow

1. List all HTML, CSS, and JS files to confirm scope.
2. Read each file in scope.
3. Check against every rule above.
4. Report findings grouped by file.
5. Separate **critical** (broken paths, missing assets, inline styles) from **polish** (missing lazy, missing alt on decorative images).
6. Do not modify any files.
7. Do not commit.

## Output Format

```
## Audit Results — [page name]

### Critical
- [file:line] description

### Polish
- [file:line] description

### Clean
- [rule] — no issues found
```
