---
name: open-design-craft
description: |
  Open Design's brand-agnostic craft rulebooks — typography, color, motion,
  accessibility, anti-AI-slop, RTL/bidi (Arabic), state coverage, form
  validation and laws of UX. Use when building, reviewing or polishing any web
  page or UI, especially Arabic/RTL pages, to apply the rules a professional
  designer applies on top of any brand or design system.
---

# Open Design craft rules

Universal UI craft knowledge from [Open Design](https://github.com/nexu-io/open-design)
(`craft/`). A design system says *which* colors and fonts a brand uses; these
files say the rules a competent designer applies regardless of brand
(e.g. ALL CAPS always needs ≥0.06em tracking).

## How to use

Read only the reference files relevant to the task, then apply their rules
while building or reviewing. Don't load all of them by default.

| Reference | Read when |
|---|---|
| [references/anti-ai-slop.md](references/anti-ai-slop.md) | Any new page or redesign — removes the generic "AI-made" look |
| [references/typography.md](references/typography.md) | Choosing fonts, sizes, tracking, line-height |
| [references/typography-hierarchy.md](references/typography-hierarchy.md) | Setting up a type scale and heading hierarchy |
| [references/typography-hierarchy-editorial.md](references/typography-hierarchy-editorial.md) | Long-form reading pages, articles, editorial layouts |
| [references/color.md](references/color.md) | Palette roles, accent usage, light/dark tokens |
| [references/rtl-and-bidi.md](references/rtl-and-bidi.md) | Arabic, Urdu, Hebrew or mixed-direction content |
| [references/accessibility-baseline.md](references/accessibility-baseline.md) | Every page — contrast, focus, semantics, reduced motion |
| [references/animation-discipline.md](references/animation-discipline.md) | Adding or reviewing transitions and motion |
| [references/state-coverage.md](references/state-coverage.md) | Interactive components — empty, loading, error, disabled states |
| [references/form-validation.md](references/form-validation.md) | Forms and input validation |
| [references/laws-of-ux.md](references/laws-of-ux.md) | Layout and interaction decisions (Fitts, Hick, etc.) |

## Pairings

- Build: `design-taste-frontend`, `high-end-visual-design`, `minimalist-ui`, `industrial-brutalist-ui`
- Improve an existing page: `redesign-existing-projects`, then `impeccable-design-polish`
- Review: `web-design-guidelines`, `review-animations`
- Direction from references: `reference-design-contract`

Source: nexu-io/open-design, Apache-2.0 (see `../OPEN_DESIGN_LICENSE`).
