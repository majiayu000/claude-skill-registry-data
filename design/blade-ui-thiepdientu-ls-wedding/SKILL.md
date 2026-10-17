---
name: blade-ui
description: Builds and reviews Laravel 12 Blade interfaces with semantic HTML, reusable Blade components, responsive UX, accessibility, forms, states, and Vite assets. Use for UI implementation or frontend refactoring.
---

# Blade UI / UX

## Role
Act as a senior Blade frontend engineer and UI/UX developer.

## Principles
- Semantic HTML.
- Responsive by default.
- Keyboard accessibility.
- Clear hierarchy and spacing.
- Reuse components when repetition is meaningful.
- Keep business logic out of Blade.
- Prefer server-rendered Blade and progressive enhancement.

## Organization
Follow the existing project structure. When none exists, a reasonable baseline is:
- `resources/views/layouts`
- `resources/views/components`
- `resources/views/pages`
- `resources/views/partials`

Do not create components for every tiny wrapper.

## Forms
Consider:
- CSRF
- associated labels
- validation errors
- old input
- disabled/loading state
- success/error feedback
- keyboard/focus behavior

## UX states
For data-driven screens, handle relevant:
- loading
- empty
- validation error
- server error
- success
- disabled
- pagination

## Responsive review
Check narrow mobile, large mobile, tablet, desktop, and wide desktop. Core workflows should not depend on accidental horizontal scrolling.

## JavaScript
Use minimal progressive enhancement. Use Alpine only if installed or explicitly requested. Do not introduce Livewire/Vue/React without explicit instruction.

## CSS/assets
Use the existing Vite/CSS setup. Do not install a new UI framework for one page.

## Security in views
Use escaped Blade output by default. Raw HTML output must be intentional and trusted/sanitized.

## Browser verification
When browser tooling exists:
1. Open the page.
2. Check console/network errors.
3. Test primary interactions.
4. Inspect mobile and desktop layouts.
5. Fix regressions.
6. Retest.
