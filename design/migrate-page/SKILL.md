---
name: elysium-migrate-page
description: Migrate a Claude Design HTML export into a clean static page following project file structure and conventions.
---

# Elysium Page Migration

Migrate an exported Claude Design HTML file into the project's file structure.

## Prerequisites

- A source HTML file (Claude Design export or offline HTML)
- Target page path confirmed (e.g., `pages/games/valorant.html`)
- Target CSS file confirmed (e.g., `css/valorant.css`)
- Target JS file confirmed (e.g., `js/valorant.js`)
- Target asset directories confirmed

## Migration Steps

1. **Read the source** — Open the exported HTML file. Identify the actual page content vs. export wrapper/boilerplate.
2. **Extract CSS** — Pull all `<style>` blocks into the target page CSS file. Replace hardcoded colors with `global.css` variables where they match.
3. **Extract JS** — Pull all `<script>` blocks into the target page JS file. Remove `console.log` statements.
4. **Extract assets** — Save embedded/base64 images as real files under `assets/`. Convert to WebP for normal images. Keep PNG for transparent icons.
5. **Build the page** — Create the target HTML file with:
   - Proper `<head>` with title, meta description, Google Fonts links
   - Links to `css/global.css`, `css/components.css`, `css/animations.css`, and the page CSS
   - Consistent nav and footer matching other pages
   - All `<img>` tags with `alt` attributes
   - Non-hero images with `loading="lazy"`
   - Scripts loaded with `defer` before `</body>`
   - No inline styles
   - No hardcoded prices
6. **Apply known fixes** — Check CLAUDE.md known fixes list and apply any that are relevant.
7. **Show summary** — List every file created/modified with line counts.
8. **Show diff** — Present the full diff before saving.
9. **Wait for approval** — Do not save until approved.
10. **Do not commit** — Leave committing to the user.

## File Placement Rules

| Content | Destination |
|---------|-------------|
| Page HTML | `pages/games/[game].html` |
| Page CSS | `css/[game].css` |
| Page JS | `js/[game].js` |
| Game icons | `assets/[game]/icons/` |
| Game images | `assets/[game]/images/` |
| Shared images | `assets/images/` |
| Shared icons | `assets/icons/` |

## Do Not

- Modify other game pages during migration
- Place page-specific CSS in `global.css` or `components.css`
- Add new frameworks or libraries
- Hardcode prices in HTML
- Add audio files
- Skip the approval step
