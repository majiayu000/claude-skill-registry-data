---
name: brand-assets
description: Generate a product's full brand-asset set at finishing time — two logo concepts to choose from, then the square app icon, favicon set, horizontal lockup, and a separate square auth-provider logo. One SVG source of truth, rendered with rsvg-convert. Every product needs all of these before launch.
---

# brand-assets

> **The atom trap + the tiny-circle trap.** Crossing orbit ellipses read as an *atom*, not a
> cosmos — for "many things" use scattered dots with NO connecting orbit lines. And an
> auth-provider logo (Google consent) is shown tiny inside a circle, so it must be a
> **text-free square** — a wordmark is illegible there. Learned shipping ThousandWorlds
> Explorer (2026-06-28): the first orbital mark read as an atom; replaced with a
> magnifier-over-scattered-worlds. Operator also wants this baked in because *every* product
> needs the full set at the end.

## When you activate

At finishing / pre-launch, or any time a product still ships a default favicon and an
unbranded auth screen. Make the whole set one deliberate step — not a scramble the night
before launch.

## Core principles

- **One SVG is the source of truth.** Design the mark once as `docs/logo.svg`; the app,
  README, email, and favicon all reference that single file (import it — never copy it).
- **Design in SVG, rasterize with `rsvg-convert`** (`brew install librsvg`):
  `rsvg-convert -w 512 -h 512 docs/logo.svg -o docs/logo.png`.
- **Two concepts, operator picks.** Offer two distinct directions, render both at large AND
  favicon size, and let the operator choose before you generate the rest.
- **Legible at 26px.** The silhouette must read at favicon size — verify by rendering small.
- **Echo the product.** Pull the palette from what the app already shows (a chart's colours,
  the hero) so the icon and the product visually rhyme.

## Pipeline

1. **Brief** — product name, one-line essence, 2–4 brand colours (lift them from the app).
2. **Concept** — author two distinct logo SVGs (240×240, rounded-square icon). Avoid generic
   or ambiguous reads (see the atom trap). Show both at ~96px and ~26px; operator picks one.
3. **Finalize** — the chosen SVG becomes canonical `docs/logo.svg`; retire the rejects.
4. **Generate the set** (all from `docs/logo.svg` via rsvg-convert):
   - `docs/logo.png` — 512px square app icon.
   - `public/favicon.svg` + `public/favicon-32.png` + `public/apple-touch-icon.png` (180px).
   - `docs/logo-lockup.{svg,png}` — horizontal: icon + wordmark, for header / email.
   - `docs/logo-<provider>-auth.png` — the **square, text-free** mark for Google/etc. consent.
5. **Wire** — favicon `<link>`s in `index.html`; the icon beside the wordmark in the header;
   import the one SVG everywhere (no duplicate files).
6. **Verify** — renders in the browser, legible small, and the production build bundles the
   assets (`dist/assets/*.svg`, `dist/favicon.svg`). Then hand the operator the exact file to
   upload to each auth provider's branding screen.

## Artifacts (persist per product)

`docs/logo.svg` · `docs/logo.png` · `docs/logo-lockup.{svg,png}` ·
`docs/logo-<provider>-auth.png` · `public/favicon.svg` · `public/favicon-32.png` ·
`public/apple-touch-icon.png` — plus the `index.html` + header wiring.

## Output

The full set above, wired and verified, and a one-line "upload `docs/logo-google-auth.png`
to Google → Branding" hand-off. Note: the auth-screen *domain* line (e.g. the
`…supabase.co` text on Google's account chooser) is an auth/go-live concern, not an asset —
that needs a custom auth domain + OAuth verification, so point the operator to `/go-live`.
