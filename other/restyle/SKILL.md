---
name: restyle
description: Rebrand a cloned website with your own identity — swaps colors, fonts, logo, favicons, and rewrites all copy for your brand while keeping the cloned layout, spacing, animations, and interactions pixel-intact. Run after /clone-website. Reads BRAND.md at the repo root. Use when the user wants to "make it mine", rebrand, restyle, or customize the clone.
argument-hint: "[extra instructions, e.g. 'keep their copy, only swap colors']"
user-invocable: true
---

# Restyle

Turn the cloned site into **the user's site**: their brand, their words, their logo — on top of the cloned structure. Layout, spacing, animations, and interactions stay untouched. That separation works because the clone pipeline keeps all content in `src/data/*.ts` and all brand tokens in `globals.css` — you swap those layers only.

$ARGUMENTS

## Step 1 — Read the brand

Read `BRAND.md` at the repo root. If it's missing or has unfilled `TODO` fields, ask the user for what's missing (max 3 questions at a time). Never ask for secrets in chat — anything sensitive belongs in env files, not BRAND.md.

If the user has brand assets (logo files, product screenshots), ask them to drop the files into `public/brand/` and tell you the filenames.

## Step 2 — Take "before" screenshots

```bash
npm run dev   # background
node scripts/extract/screenshot.mjs http://localhost:3000 --name before-restyle
```
These are your regression reference: after restyling, layout must still match them structurally.

## Step 3 — Swap the brand layers (in this order)

1. **Colors** — `src/app/globals.css`: replace the cloned palette in `:root` / `.dark` with the brand colors from BRAND.md. Keep the same token *names* so no component changes. Preserve relative contrast: if the original had a dark section, keep it dark in the new palette.
2. **Fonts** — `src/app/layout.tsx`: swap `next/font` families to the brand fonts. Keep the size/weight structure the clone extracted — only families change.
3. **Logo & icons** — replace `LogoIcon` in `src/components/icons.tsx` (or the logo `<img>` asset) with the brand logo from `public/brand/`. Keep the rendered dimensions of the original logo so the header layout doesn't shift.
4. **Favicons & SEO** — regenerate `public/seo/` (favicon, apple-touch-icon, OG image if provided), update `layout.tsx` metadata: title, description, OG tags — from BRAND.md positioning.
5. **Copy** — rewrite every string in `src/data/*.ts` for the brand: same structure, same approximate length (±20% — long copy breaks cloned layouts), brand voice from BRAND.md. Headlines sell the user's offer, not the original company's. Placeholder patterns like testimonials get realistic brand-appropriate content clearly marked as placeholders unless BRAND.md provides real ones.
6. **Images** — where the clone shows the original company's product shots, swap in files from `public/brand/` if provided; otherwise leave the cloned image and list it in the report as "needs replacement".

## Step 4 — Verify

1. `npm run build` — must pass
2. `node scripts/extract/screenshot.mjs http://localhost:3000 --name after-restyle`
3. Compare before/after at all 3 viewports: layout identical, only brand layers changed. Overflowing text = shorten the copy, never change the layout.
4. Check every page route, not just `/`.

## Report

- What was swapped (colors, fonts, logo, favicon, N copy blocks across M data files)
- Images still showing the original site's content (need user-provided replacements)
- Any copy that had to be shortened/lengthened to fit
- Anything in BRAND.md still marked TODO
