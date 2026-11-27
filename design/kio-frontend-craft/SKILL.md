---
name: kio-frontend-craft
description: "Kio Frontend, UI/UX & Motion hub. Use for any UI work: designing or reviewing pages, landing pages, dashboards, components; picking a style, palette, font pairing or icons (79 searchable styles, 192 palettes, 74 pairings, 1,934 Google Fonts, 22 stacks); de-slopping AI-looking UIs (9-pass /unslop); accessibility, spacing and responsive fixes; Lenis smooth scroll and GSAP motion; Core Web Vitals / PageSpeed 95-100 (LCP, CLS, INP); React 19 and Next.js App Router performance (64 rules: waterfalls, bundle size, RSC, re-renders); React Native / Expo / SwiftUI mobile; PDF or mockup to responsive HTML; free stock photos (Unsplash, Pexels, Openverse) with credits."
license: MIT
metadata:
  author: Kio System / Toan Pham
  version: 3.0.0
---

# 🎨 Kio Frontend, UI/UX & Motion (`kio-frontend-craft`)

The router for Kio's interface work. Knowledge lives in `references/`, design data lives in `assets/data/` and is queried with `scripts/search.py`. This file only points the way and holds the mandatory rules.

`KIO_FE_ROOT` = this skill's install directory (e.g. `~/.claude/skills/kio-frontend-craft`). All commands below use `${KIO_FE_ROOT:-skills/kio-frontend-craft}`.

## ⚙️ How to work

1. **New UI → pick a design system first, never improvise.**
   ```bash
   python3 "${KIO_FE_ROOT:-skills/kio-frontend-craft}/scripts/search.py" "<product type + mood>" --design-system [--stack nextjs]
   ```
   It returns a page pattern, style, palette, font pairing, effects and anti-patterns. Record them and apply them consistently.
2. **Pick exactly one primary reference** from the [routing table](#-routing-table). For overlaps use the [selection rules](#-selection-rules-for-overlaps).
3. **Look details up by domain/stack** instead of guessing: `--domain style|color|typography|icons|landing|product|ux|chart|gsap|react|web|google-fonts`, `--stack <framework>`.
4. **Before delivery** always run the checklist in `references/ui-ux/pro-rules.md` (*Pre-Delivery Checklist*), check at 375 px, 768 px and 1440 px, and run `scripts/layout-check.js` (no edge spill, no misaligned rows, no wrapped buttons).
5. **MANDATORY reads (open the file first):** performance or PageSpeed work → `references/web-performance.md`; React / Next.js code → `references/react/README.md`; motion or smooth scroll → `references/motion-lenis.md`; "looks AI-generated" → `references/unslop-9-pass.md`; mobile apps → `references/mobile/README.md`. In the answer, name the reference you followed.

## 🧭 Routing table

| Task | Open | Notes |
|---|---|---|
| Choose style, colours, fonts, icons, landing pattern | `scripts/search.py` (`--design-system`, `--domain`) | Data: `assets/data/*.csv`, 192 reasoning profiles in `assets/data/ui-reasoning.csv` |
| Full UI/UX rules in 10 groups (accessibility, touch, layout, forms, navigation, charts…) | `references/ui-ux/quick-reference.md` | CRITICAL → LOW priority |
| Professional rules + pre-delivery checklist | `references/ui-ux/pro-rules.md` | The single, mandatory checklist |
| UI "looks AI-generated" and needs a redo | `references/unslop-9-pass.md` | 9 passes, in order |
| 3-layer design tokens | `assets/templates/design-tokens-starter.json` | Primitive → semantic → component |
| Lenis smooth scroll, GSAP ScrollTrigger | `references/motion-lenis.md` | `data-lenis-prevent`, reduced motion |
| Core Web Vitals, PageSpeed 95–100, page performance audit | `references/web-performance.md` | LCP, CLS, INP, 5-phase audit |
| React / Next.js performance (waterfalls, bundle, RSC, re-renders) | `references/react/README.md` → `references/react/rules/<rule>.md` | 64 rules, 8 groups; full compiled guide: `references/react/AGENTS.md` |
| Framework rules (Vue, Svelte, Astro, shadcn, Flutter, WPF…) | `search.py --stack <name>` | 22 stacks, 1,271 rules |
| React Native / Expo / SwiftUI apps | `references/mobile/README.md` → `references/mobile/react-native-expo.md`, `references/mobile/swiftui-ios.md`, `references/mobile/performance-and-offline.md` | |
| PDF / mockup → responsive HTML | `references/pdf-to-html.md` | Scripts `scripts/convert.sh`, `scripts/extract_sections.py` |
| Images for a page when the user has no real photos | `references/stock-images.md` | `scripts/stock_images.py`: Unsplash / Pexels (key) or Openverse (no key); emits `<img>` tags and credits |

## 🔀 Selection rules for overlaps

| Need | Start at | Switch when |
|---|---|---|
| Slow page | `web-performance.md` (measure first) | The cause is in React/Next.js code → `react/rules/` by group `async-`, `bundle-`, `server-`, `rerender-` |
| React component review | `react/README.md` | The issue is visual/accessibility → `ui-ux/quick-reference.md` |
| Beautify an old UI | `unslop-9-pass.md` | Only small fixes needed → `ui-ux/pro-rules.md` |
| Mobile | `mobile/README.md` | Need detailed stack rules → `search.py --stack react-native` / `swiftui` / `flutter` |
| Motion | `motion-lenis.md` | Need motion presets → `search.py "<mood>" --domain gsap` |

## 🧩 Workflows

| Job | Order |
|---|---|
| New landing page | `search.py --design-system` → tokens → `stock-images.md` (one image per slot when there are no real photos) → `ui-ux/quick-reference.md` → `motion-lenis.md` (if needed) → `web-performance.md` → `ui-ux/pro-rules.md` checklist |
| Redo an AI-looking UI | Screenshot current state → `search.py --design-system` → `unslop-9-pass.md` → checklist |
| Slow Next.js app | `web-performance.md` (Lighthouse mobile + desktop) → `react/rules/` by cause → measure again |
| PDF → website | `pdf-to-html.md` → tokens → `ui-ux/quick-reference.md` (responsive) → `web-performance.md` |
| New mobile app | `mobile/README.md` → `search.py --stack react-native` → `mobile/performance-and-offline.md` |

APIs, databases and payments belong to `kio-backend-cloud`; Playwright UI testing to `kio-qa-security`; marketing copy and CRO to `kio-growth-marketing`.

## 🛡️ Mandatory rules

1. **No edge bleed (defensive spacing).**
   - Every section sits in `max-w-7xl mx-auto px-4 sm:px-6 md:px-8 lg:px-12`; no text, card or form touches the screen edge at 375 px.
   - Offset fixed headers with `pt-20 sm:pt-28`; leave `pb-20 sm:pb-32` before the footer.
   - Inputs at least `py-3 px-4`, 44 px tall, ≥ 16 px text (no iOS auto-zoom); buttons at least `py-2.5 px-5`.
   - Multi-column grids/flex rows declare the mobile layout explicitly: `grid grid-cols-1 lg:grid-cols-12` (never a bare `grid`), every child column gets `min-w-0`, SVGs/images/tables get `max-w-full` or `w-full`. Without them a column grows to its widest content and spills off the screen.
   - Never hide overflow on sections or `body` (`overflow-hidden`, `overflow-x-hidden`) to mask spills; reserve it for image frames or carousels of known size.
   - Check at 375 px before delivery: run `scripts/layout-check.js` in the console (see rule 10); its `overflow` list must be empty.
2. **No generic AI look.** No decorative neon purple gradients, identical 3-column bento grids, emoji as icons, or buzzword copy.
3. **Accessibility is a delivery requirement.** Text contrast ≥ 4.5:1 (large text and controls ≥ 3:1) in light and dark; visible focus; fully keyboard operable; images have `alt`.
4. **Performance is a delivery requirement.** LCP < 2.5 s, CLS < 0.1 (target 0), INP < 200 ms on mobile; images carry dimensions and `aspect-ratio`.
   - **Target Lighthouse 100 / 100 / 100 / 100** (Performance, Accessibility, Best Practices, SEO) on mobile and desktop.
   - **Google Fonts must not block rendering:** load them with `<link rel="preload" as="style" href="…" onload="this.onload=null;this.rel='stylesheet'">` plus `<noscript><link rel="stylesheet" href="…"></noscript>`, `preconnect` to `fonts.googleapis.com` and `fonts.gstatic.com`, `display=swap`; at most 2 families × 3 weights (or system fonts when no web font is needed).
   - **Always ship a favicon** (`<link rel="icon" …>`, an inline `data:` SVG is fine); without it the browser logs a 404 and Best Practices drops.
   - Only the hero image gets `fetchpriority="high"`; correct `srcset`/`sizes` so phones do not download a larger image than needed.
   - **Mobile LCP image ≤ ~80 KB** with 480 / 768 px steps in `srcset`: a 380 px slot on a 1.75–2× screen needs ~700 px, and without a 768 step the browser downloads the 1024 file. `stock_images.py` already writes these steps and compresses the `--eager` image harder. Image-heavy pages: only the hero loads eagerly, everything else `loading="lazy"`.
5. **React 19 / Next.js:** Server Components by default, Client Components at the leaves; no sequential `await` waterfalls when work can run in parallel.
6. **Motion respects `prefers-reduced-motion`** and animates only `transform`/`opacity`.
7. **Language:** answer in the language of the user's request (an English prompt gets an English answer), even when skill documents are written in another language.
8. **Images:** without real photos, fetch stock photos with `scripts/stock_images.py` (see `references/stock-images.md`), with `alt`, dimensions and credits; never paste image URLs found on the web; label them as illustrative when the page presents a real business.
9. **No HTML entities.** Write real characters in text and attributes: `Nail & Spa`, `©`, `–`, `→`, accented letters, `&` inside URLs. Never `&amp;`, `&nbsp;`, `&copy;`, `&ndash;`, `&#...;`… (the file declares `<meta charset="utf-8">`). The only exception is a literal `<` shown as text. Content inserted from JavaScript uses `textContent`, not `innerHTML`. Check before delivery — this must print nothing:
   ```bash
   grep -nE '&[a-zA-Z]+;|&#[0-9]+;' index.html
   ```
10. **Rows stay aligned and balanced — no wrapped text throwing the layout off.** Items in one row (stats, cards, buttons, footer columns) keep their matching parts at the same height, at 375 px and at 1440 px.
   - **Stat rows (number + label):** put the **number on top and the label below** (`flex flex-col-reverse` or `<dd>` first) so a wrapping label never pushes its number down. Keep labels to 2–3 words ("Stores", "Since", "From"); move details into a note underneath. If three columns do not fit at 375 px, use `grid-cols-1 sm:grid-cols-3` instead of squeezing.
   - **Cards in a row:** `grid ... items-stretch`; each card `h-full flex flex-col`; price / meta / button at the end uses `mt-auto` so it sits on the bottom; card titles `line-clamp-2` with a two-line minimum height (e.g. `min-h-[3.5rem]`) so descriptions start on one line.
   - **Buttons:** labels never wrap (`whitespace-nowrap`, ≤ 3–4 words on mobile); button groups stack full-width on mobile `flex flex-col sm:flex-row`; side-by-side buttons share one height.
   - **Numbers and prices in columns:** `tabular-nums`, right-aligned or on one axis.
   - **Check before delivery:** run `scripts/layout-check.js` in the console at 375 px and 1440 px; its `overflow`, `misaligned` and `wrappedButtons` lists must all be empty.

## 📦 What's included

- `assets/data/` — styles, colours, typography, icons, landing, products, UX, charts, motion, React performance, 22 stacks; `catalog-summary.json` (counts), `data-provenance.json` (sources and review dates).
- `scripts/` — `layout-check.js` (console check for edge spill / misaligned rows / wrapped buttons), `stock_images.py` (stock photos), `search.py` (BM25 search + design systems), `validate_data.py`, `convert.sh`, `extract_sections.py`; tests: `python3 -m pytest scripts/tests`.
- `references/` — the documents in the table above. `assets/templates/` — design tokens.
- `THIRD_PARTY_NOTICES.md` — credits and licenses for the open-source sources Kio uses; keep it when redistributing.
