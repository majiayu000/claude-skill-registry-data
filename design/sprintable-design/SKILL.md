---
name: sprintable-design
description: Use this skill to generate well-branded interfaces and assets for Sprintable, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Quick orientation

- `colors_and_type.css` — all tokens (color, type, spacing, radii, shadows). Link it from any HTML artifact and use CSS variables (`var(--fg-1)`, `var(--brand-primary)`, etc).
- `assets/` — logos (`sprintable-logo-full.png`, `sprintable-logo-square.png`). Never redraw.
- `preview/` — small specimen cards for each token group; useful references.
- `ui_kits/web/` and `ui_kits/app/` — working React (JSX + Babel) components demonstrating the marketing site and the workspace. Copy individual components out as starting points.

## Non-negotiables

- Dark-mode-native. Canvas is `#08090a`.
- Inter Variable with `font-feature-settings: "cv01", "ss03"` globally. Without these features, it is not Sprintable's Inter.
- Signature weight **510**. Three-tier system: 400 / 510 / 590. Never 700.
- Primary text is `#f7f8f8`, never pure white.
- Brand blue (`#3385f8`) is the only chromatic color — reserved for CTAs, links, active states, the logo mark. Never decorative.
- Borders are always semi-transparent white (`rgba(255,255,255,0.05–0.08)`) on dark.
- Display text uses aggressive negative letter-spacing: -1.584px @ 72, -1.056px @ 48, -0.704px @ 32.
- No emoji in UI. No gradients on backgrounds. No bouncy/spring animations.
