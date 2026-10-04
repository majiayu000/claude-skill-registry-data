---
name: stitch-ux-design
description: Apply this repository's exported Google Stitch UX design system. Use when changing Angular frontend UI, navigation, layouts, screens, components, CSS, visual states, responsive behavior, or user-facing workflows so changes follow the Stitch export and Indigo Utility guidelines.
---

# Stitch UX Design

Use this skill for UI implementation and review work in `projects/frontend`.

Required reading:

- `docs/guidelines/stitch-ux-design.md`
- `docs/adr/20260613-1009-implement-stitch-ux-design-system.md`

When implementing or reviewing a specific screen, also inspect the matching files inside `docs/guidelines/stitch_color_toggle_gym_tracker.zip`:

- Sign-in: `sign_in_color_toggle_app/code.html` and `screen.png`
- Buttons desktop: `your_color_buttons/code.html` and `screen.png`
- Buttons mobile: `buttons_mobile_view/code.html` and `screen.png`
- Map desktop: `gym_map/code.html` and `screen.png`
- Map mobile: `gym_map_mobile_view/code.html` and `screen.png`
- Defenders desktop: `defenders_management/code.html` and `screen.png`
- Defenders mobile: `defenders_mobile_view/code.html` and `screen.png`
- Design tokens: `indigo_utility/DESIGN.md`

Implementation approach:

1. Preserve existing Angular behavior, services, routes, Signals, repositories, auth, storage, geolocation, and Leaflet map lifecycle.
2. Translate the Stitch design into Angular templates, component CSS, and shared style tokens.
3. Migrate incrementally by screen rather than rebuilding from static exported HTML.
4. Preserve loading, saving, refreshing, empty, validation, and error states.
5. Verify affected layouts on mobile and desktop.

Guardrails:

- Keep the first signed-in screen usable; do not add a marketing landing page.
- Keep the Buttons screen pessimistic: tile state changes only after persistence succeeds.
- Keep map workflows intact: crosshair, current-location control, save/edit panels, and marker click editing.
- Keep Defenders workflows intact: Defending/Nearby tabs, quick defend, inline edit, delete confirmation, refresh, and empty states.
- Use Indigo Utility styling rather than default Bootstrap visual chrome.
