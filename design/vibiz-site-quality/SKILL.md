---
name: vibiz-site-quality
description: Use when building or improving customer-facing landing pages, websites, dashboards, forms, content sections, brand adaptation, or visual polish.
compatibility: opencode
---

# Vibiz Site Quality

The output should feel like a tailored, working customer site, not a generic SaaS starter. Optimize for first-run success: fewer retries, fewer broken CTAs, stronger brand fit, and a page that survives real viewport sizes.

Before editing broad UI, read:

- `template.config.ts`
- `src/app/page.tsx`
- `src/components/landing/*`
- `src/components/ui/*`
- `src/app/globals.css`

Quality rules:

- Build the actual requested page or site as the first screen. Do not add how-to text or internal implementation notes to the UI.
- Replace generic placeholder copy when the prompt gives business, audience, offer, or brand details.
- Keep visual hierarchy tight: clear hero, credible proof, specific features, pricing/offer path, FAQ or objection handling, and final CTA when relevant.
- Buttons and links should do something honest. Use existing `Button` and UI components where possible.
- Maintain mobile and desktop responsiveness. Watch for long words, price text, cards, nav, and CTA overflow.
- Do not rely on one-note color palettes or generic purple SaaS styling if user brand context suggests otherwise.
- Avoid nested cards and decorative clutter. Prefer clear layout, strong spacing, and concrete content.
- Use Tailwind v4-compatible CSS. Do not add top-level `@apply` without the right reference context.

Verification:

- Run `npm run build` for structural UI changes.
- If the dev server is available, inspect the page at mobile and desktop widths.
- Check that key CTAs, navigation anchors, and pricing/offers still work after visual changes.
