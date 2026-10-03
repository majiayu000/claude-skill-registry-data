---
name: elysium-predeploy
description: Final pre-deploy checklist for Elysium Boost. Validates all pages are production-ready before pushing live.
---

# Elysium Pre-Deploy Check

Run before pushing to production. Validates every page against launch requirements.

## Checklist

### All Pages
- [ ] `<title>` and `<meta name="description">` present
- [ ] Nav and footer markup is consistent across pages
- [ ] All `<img>` tags have `alt` attributes
- [ ] Non-hero images have `loading="lazy"`
- [ ] All `<script>` tags use `defer`
- [ ] No inline styles
- [ ] No `console.log` in any JS file
- [ ] No hardcoded prices in HTML
- [ ] No references to `orderpanelbg.webp`
- [ ] No audio files (`elysium-loop.mp3` or similar)
- [ ] No exposed API keys or secrets in HTML/JS

### CSS
- [ ] All colors use `global.css` variables
- [ ] No duplicate selectors
- [ ] No page-specific styles in `global.css` or `components.css`
- [ ] No stacked `backdrop-filter`
- [ ] `@property --arc-trace-angle` declared when travelling line is used
- [ ] Reduced motion respected: `@media (prefers-reduced-motion: no-preference)`

### Assets
- [ ] Every `src`/`url()` path resolves to a real file
- [ ] Images are WebP (except transparent icons which are PNG)
- [ ] Videos have `muted autoplay loop playsinline`
- [ ] No unused assets in `assets/` directories

### Arc Raiders Specific
- [ ] Sidebar icons use `mix-blend-mode: screen`
- [ ] All 15 station icons exist under `assets/arc-raiders/icons/`
- [ ] All station art images exist under `assets/arc-raiders/images/`
- [ ] Station names match CLAUDE.md list exactly

### Valorant Specific
- [ ] All 6 tabs functional: Rank Boosting, Placements, Ranked Wins, Account Leveling, Battle Pass, Coaching
- [ ] Rank icons exist under `assets/valorant/icons/`
- [ ] Rank icons with dark backgrounds use `mix-blend-mode: screen`

## Workflow

1. Read all HTML, CSS, and JS files.
2. Check each item above.
3. Report pass/fail per item with file paths.
4. Flag any blockers that prevent deploy.
5. Do not modify any files.
6. Do not commit.

## Output Format

```
## Pre-Deploy Report

### Blockers (must fix before deploy)
- [item] — [file:line] detail

### Warnings (should fix)
- [item] — [file:line] detail

### Passed
- [item] — OK
```
