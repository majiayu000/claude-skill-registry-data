---
name: site-updater
description: Update videos, modules, or styling on the Alpha AI Learning site. Use when adding/replacing videos, updating module content, changing week descriptions, or modifying site styling.
---

# Alpha AI Site Updater

## Site Structure

- `index.html` - Homepage with week cards
- `docs/learning-plan.html` - 4-week curriculum with modules
- `docs/quick-reference.html` - Quick reference page
- `assets/css/custom.css` - Styling (fraternity colors: #CFB53B gold)
- `README.md` - Documentation

## How to Update Videos

### In learning-plan.html
Find the module and update the `href` attribute:
```html
<a href="https://youtu.be/YOUR-VIDEO-ID" target="_blank" rel="noopener noreferrer" class="btn btn-sm mt-2">
    Watch Video
</a>
```

Also update:
- `<span class="module-title">` - Video title
- `<span class="module-duration">` - Duration
- `<p class="module-description">` - Description

### In index.html
Update the corresponding week card to match.

## How to Add a New Module

1. Copy an existing module block in learning-plan.html
2. Update `data-module-id` to be unique (e.g., `week2-module2`)
3. Update the `id` and `for` attributes to match
4. Update the progress counter: `0 of X modules complete`

## Week Structure

- Week 1: Understand the Power (~35 min) - 2 modules
- Week 2: Understanding AI Workflows (~17 min) - 1 module + reference table
- Week 3: Using AI for Productivity (~30 min) - 1 module + 6 skills list
- Week 4: Make It Your Own (~1 hour) - 1 action module

## Styling

Fraternity colors:
- Gold: #CFB53B
- Black: #000000
- Accent red (labels): #B22222

## After Making Changes

Always update both:
1. `docs/learning-plan.html` - The detailed curriculum
2. `index.html` - The homepage week cards (keep them in sync)
