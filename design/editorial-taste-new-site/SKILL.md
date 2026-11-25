---
name: editorial-taste-new-site
description: Editorial Taste — create a brand-new website or landing page from scratch in a monochrome, editorial, photography-led style (Geist + Geist Mono, #151515 / #EDEDED alpha ramps, 5px spacing rhythm, glass blur instead of shadows, full-bleed photos with vignettes, a word-by-word statement section). Asks which stack to use (Astro, Next.js/React, plain HTML, Vue, Svelte), then covers intake, page structure, editorial copy, a fresh layout composed per site from 8 hero variants and section patterns (never a copy of the starter template), buttery motion (Lenis smooth scroll, masked text reveals, image unmasks, count-up, parallax), isometric hairline illustrations, states, and a ship checklist. Use when the user asks to build, create, scaffold, or design a new site, landing page, homepage, or marketing page with Editorial Taste, an editorial / minimal / monochrome / premium look, or "in our style", in code or in Figma. Not for restyling an existing site; use editorial-taste-redesign for that.
---

# Editorial Taste: New site

Builds a new site in the Editorial Taste style. It's **monochrome, editorial, and photography-led**: the UI is achromatic, color comes only from photography, and the words carry the page. The **system is fixed** (tokens, type, spacing, radii, glass, motion). The **layout is composed fresh for every site** from `references/layouts.md`. The bundled template is a tested reference implementation of the system: reuse its CSS, motion, and components, but never its page composition as is.

Work through **Part A (what the page says)** before **Part B (how it looks)**.

## Non-negotiable rules

1. **No accent colors.** Use only the neutral ramp, `--light-*` (#EDEDED alpha), `--dark-*` (#151515 alpha), and semantic tokens. Express hierarchy with alpha steps. The single exception is `--signal`, one dot per isometric illustration.
2. **Two type voices.** Geist Medium for headings, Geist Regular for body. **Geist Mono only** for buttons, nav, labels, tags, and eyebrows. No bold headings and no italics. **Type roles are fixed**: the hero headline (`h1`) is always `.h2`, `.h0` belongs only to the statement, section titles are `.h3`, stat values and prices `.h1`.
3. **5px rhythm.** Spacing and radii come from the 5-step scale through the `--space-*` tokens (the compact-scale exceptions are 8, 12, 32, 56, and 96). Never reference a token that `styles.css` doesn't define. Nested radii: `inner = outer − gap`.
4. **Glass, not shadow.** No `box-shadow`. For depth, use translucent fills plus `backdrop-filter: blur(16px)`. The only gradients allowed are black vignettes over photos.
5. **Text on photos always sits on a vignette.** Use a white logo on photos and a dark logo on light surfaces.
6. **Radii:** buttons 8 · cards 10 · case cards 20 · chips and pills full. **20 is for case cards only**: photos, frames, mosaics, panels, and forms use 10. Don't mix radii within a row.
7. **Motion is buttery and restrained**: expo-out (`--ease-out`), 200/450/800/1200ms, compositor-only properties, one hero sequence, reveals that play once, and full reduced-motion and no-JS fallbacks (`references/motion.md`).
8. **One statement per page, never directly under the hero.** At least one section sits between them.
9. **Every site gets its own layout.** Choose the hero, signature moves, surface rhythm, and section patterns per site (`references/layouts.md`). Shipping the template's composition with new copy is a failure, not a starting point. Layouts vary, the rules above never do (`references/layouts.md` §2).
10. **Never invent facts** for a real business. Missing prices, stats, testimonials, and logos stay as marked `{{placeholders}}`.

---

# Part A: Strategy and content

## A1. Intake: ask once, in one batch
Collect what's missing in **a single message**, never one question at a time.

**Always ask which stack to build in**, unless the user already named one or the repo already uses one (check `package.json`, `astro.config.*`, `next.config.*`, `vite.config.*`, `nuxt.config.*`, `svelte.config.*`). If a question tool is available (e.g. `AskUserQuestion`), use it with these options:
| Option | Best for |
|---|---|
| **Astro** (recommended) | Marketing sites and landing pages: static, fast, minimal JS, content collections |
| **Next.js (React)** | Sites that will grow into an app, or React teams |
| **React + Vite** | A single-page React site without a server |
| **Plain HTML/CSS/JS** | The simplest handoff, no build step, any host |
| Other (Vue/Nuxt, SvelteKit, …) | Match the team's stack |

Also ask about the following (in the same message):
- **Brand**: name, what it does, for whom, and the one thing that makes it different.
- **Goal**: the one primary action (book, buy, contact, join a waitlist) and what counts as a conversion.
- **Audience**: who they are, what they already know when they land, and their top 2–3 objections.
- **Proof**: real numbers, clients, case studies, testimonials, press.
- **Assets**: logo SVG, photography (the style depends on it; without it, photos come from Unsplash in B3, so ask for an Unsplash Access Key if none is set), existing copy.
- **Constraints**: pages beyond the homepage, deadline, whether it's indexed or campaign-only.
- **Illustrations**: which ideas (a system, process, platform, modules) should be explained with isometric hairline drawings rather than photos.

If the user doesn't answer or says "just build it", make reasonable assumptions, state each in one line, and continue. Don't stall the build. For the stack, Astro is the default if nothing is said.

## A2. Choose the page type, and say why
| Type | Use when | Jobs the page must do |
|---|---|---|
| **Editorial homepage** | A brand with several products or audiences | Hook, proof, offers, work, story, journal, objections, action |
| **Product landing** | One offer, one audience, one action | Hook, proof, how it works, offer or pricing, objections, action |
| **Long-form story** | The audience needs educating or convincing | Hook, statement, a sequence of explanations, proof, objections, action |
| **Minimal conversion** | High-intent traffic: waitlist, download, event | Hook with the form, one proof, objections, footer |

The page type sets the jobs, not the blocks. Pick a pattern for each job from `references/layouts.md`.

**One primary action per page.** The hero gets one light button plus at most one glass button.

## A3. Plan before code
Before writing code, post a short plan (don't wait for approval unless the user asked to review first):
1. Page type and why
2. **Layout signature** (`references/layouts.md` §1): hero variant, two signature moves, surface rhythm, image density, grid rhythm. If another site already exists in the repo or conversation, say how this one differs
3. Section outline in order, naming the pattern used for each section
4. Hero copy: headline, paragraph, CTAs, and a proof line or stats
5. Statement line (2–4 lines)
6. FAQ: 6–10 real questions
7. Assumptions and missing assets (become `{{placeholders}}`)
8. SEO: index or noindex, plus title and meta description

## A4. Copy
Follow `references/copy.md`: declarative headlines ending in a period, sentence case, numbered mono eyebrows, CTAs built from a verb and an object, concrete numbers, no filler words, and calm, specific system messages.

---

# Part B: Build

## B1. Set up the chosen stack
Follow the matching section of `references/frameworks.md`:
- **Plain HTML** → copy `styles.css`, `motion.js`, `404.html`, and `favicon.svg`; write a new `index.html` for the planned layout.
- **Astro** → scaffold, then split the template into `.astro` components with a `Base` layout. Lenis and `motion.js` load in the layout.
- **Next.js / React + Vite** → components in `.tsx`, `ReactLenis` plus Framer Motion variants from `references/motion.md`.
- **Vue/Nuxt, SvelteKit** → SFCs or Svelte components, with `motion.js` loaded once on mount.
- **Tailwind** in any of these → map the tokens in the theme, keeping `tokens.css` as the source of truth.
- **Figma** → follow `references/figma.md`.

Keep the template's class names for the components you reuse, so the CSS, motion, and illustration styles work unchanged. New patterns get their own BEM classes.

## B2. Take the system from the template, not the layout
From `templates/`, copy `styles.css` (tokens, base, every component), `motion.js`, `404.html`, and `favicon.svg`. Read `index.html` as a component reference only: copy the nav, drawer, and footer markup and any component you need, then compose the page from your layout signature. Add CSS for new patterns in a separate block of `styles.css` (recipes in `references/layouts.md` §6) and delete CSS for components the page doesn't use. The reference `index.html` demonstrates:

Nav (glass over the hero, solid on scroll, hides on scroll down, mobile drawer with staggered links) → Hero (choreographed intro) → Highlight numbers (count-up) → **Statement** (word-by-word reveal) → Product cards → Case cards (expandable) → Split cards (image unmask) → **How it works** (isometric illustration that builds in) → Journal → **FAQ** → CTA band (parallax) with an email form → Footer, plus Lenis smooth scroll, page transitions, meta and OG tags, a skip link, and full reduced-motion and no-JS fallbacks.

## B3. Photography (Unsplash by default)
Every page ships with real photos. If the user supplied photos, use those. Otherwise, pull photos from **Unsplash** for every image slot before building the sections:
```bash
export UNSPLASH_ACCESS_KEY=...                                # free key: unsplash.com/developers → New Application
python3 <skill-dir>/scripts/images.py --spec > images.json    # one slot per <img>: name, query, w, h, alt
python3 <skill-dir>/scripts/images.py images.json --out <project-dir>
```
- The script searches the Unsplash API per slot, triggers Unsplash's download tracking for each photo it picks, and writes `unsplash.json` (for each slot: `src`, `srcset`, `color`, photographer and photo links), `credits.html`, and `review/contact-sheet.jpg`.
- If `UNSPLASH_ACCESS_KEY` is missing, ask the user for it in the intake batch. If they can't provide one, run with `--placeholders` (neutral local blocks), keep building, and report every slot as a missing photo in B9.
- Write queries the way a photo editor would brief: 3 to 6 concrete words for the subject, material, place, and light (`oak kitchen lime plaster daylight`, not `modern home`). Size each slot to its use: hero 2400×1500, product cards 1200×900, case cards 1000×1250, splits 1600×1000, CTA band 2400×1200.
- **Look at the contact sheet.** Reject anything off-subject, low quality, with visible logos or text, with people at laptops, or with a colour cast that fights the monochrome UI. Rerun with a sharper query, or set `"offset": n` on that slot to take the next result. Delete `review/` when done.
- Give every `<img>` a `data-slot="<name>"` matching its slot, then fill them all with `python3 <skill-dir>/scripts/images.py --apply <project-dir>/unsplash.json <project-dir>/index.html`. A site built with `--placeholders` switches to Unsplash later by running the fetch and `--apply` again.
- Use the URLs exactly as returned: `<img src="{src}" srcset="{srcset}" sizes="…" width="{w}" height="{h}" alt="…">`, and set the media wrapper's background to `{color}` so the frame isn't empty while the photo loads. Unsplash's API guidelines require hotlinking from `images.unsplash.com`, so don't download or re-host these files. Every other image is a local file.
- Write the final `alt` text from what the chosen photo actually shows, not from the query.
- Credit every Unsplash photo ("Photo by {name} on Unsplash", with the links from `unsplash.json`). Link `credits.html` from the footer's legal row as "Photo credits".

## B4. Build section by section
Build in the order of your planned outline, hero first, then 404. For each section:
- Replace its `{{placeholders}}` with the planned copy, and point images at the photos fetched in B3. The user's own photos always win over fetched ones.
- **Use the planned pattern**, from `references/layouts.md` or built from the system. Leave out sections the content doesn't support. Keep the fixed rules in `references/layouts.md` §2 and follow the variation rules in §3: adjacent sections differ in grid and surface, and at least half the sections use patterns the template doesn't show.
- Swap the `#logo` symbol for the client's SVG logo (keep `fill="currentColor"`), and update the favicon letter.
- Keep diffs per section. Don't regenerate the whole page on every iteration.

## B5. Motion
Keep the template's motion system (`references/motion.md`): Lenis smooth scroll, the hero intro sequence, `.reveal` plus `data-stagger` on every content block, `data-reveal="text"` on section titles, `data-reveal="image"` on standalone images, `data-count` on numeric stats, and `data-words` on the statement. Use the motion tokens (`--ease-out`, 200/450/800/1200ms) for anything new. Animate only transforms, opacity, and clip-path. Never add bounce, scroll-jacking, custom cursors, or more than one hero sequence.

## B6. Illustrations
For the 1–3 ideas that photos can't show (a system, platform layers, a process, modules), generate an isometric hairline illustration and place it in an Illustration split section (`references/illustrations.md`):
```bash
python3 <skill-dir>/scripts/iso.py --list
python3 <skill-dir>/scripts/iso.py --preset stack --spec > iso-platform.json   # edit labels and blocks
python3 <skill-dir>/scripts/iso.py iso-platform.json > iso-platform.svg
```
Inline the SVG inside `<figure class="illo" data-reveal="iso">` so it builds in on scroll. Use labels that match the section's numbered steps, one active block, and at most one `--signal` dot.

## B7. States and details
Every interactive element has hover, pressed, focus-visible, and disabled states. Forms validate inline. Data areas get loading, empty, and error states. Mark the current nav item with `aria-current="page"`. No dead `href="#"` links. Specs are in `references/components.md` under States and Forms.

## B8. Verify
1. `python3 <skill-dir>/scripts/lint.py <project-dir>`: fix every ERROR and review the WARNs.
2. `python3 <skill-dir>/scripts/lint.py --strict index.html`: catches leftover `{{placeholders}}`.
   Check that every `<img>` loads, that Unsplash photos use the returned `images.unsplash.com` URLs, that `credits.html` is linked from the footer, and that `review/` is gone.
3. Compare the section sequence and hero against the template and any other site in the repo. If they match, recompose before polishing.
4. Open the page at 1440, 768, and 390px widths. Check the hero intro plays once, scrolling is smooth, the nav switches state and hides or returns, the drawer opens and pauses scrolling, headings rise word by word, the statement lights up, stats count, the illustration builds in, FAQ items toggle, nothing scrolls horizontally, and every photo with text has its vignette.
5. Check again with reduced motion turned on, and with JavaScript disabled: everything should be visible.
6. Work through `references/ship-checklist.md`.

## B9. Report
Summarize the page type, the sections built, the assumptions made, any remaining `{{placeholders}}` (real facts the user must supply), the Unsplash photos used (suggest replacing them with the brand's own photography), and the missing assets (logo, legal pages, any placeholder photos).

---

## Quick token reference (web desktop)

| Need | Token |
|---|---|
| Page background | `--bg-base` #EDEDED (white for card-heavy pages) |
| Hover fill / raised surface | `--bg-lift` #D9D9D9 |
| Primary text, primary button | `--tone-strong` #151515 |
| Secondary text | `--text-muted` #737373 (`--neutral-600` on gray surfaces) |
| Hairlines, chip fill, disabled | `--border-subtle` / `--tone-faint` |
| Glass on a photo | `--light-16` + `--blur-glass` |
| Container / margin / gutter | 1280 / 40 / 20 (mobile: fluid / 20 / 12) |
| Section padding / title→content | 96 / 32 (mobile 64 / 24) |
| Motion | `--ease-out`, `--dur-fast` .2s, `--dur-base` .45s, `--dur-slow` .8s, `--dur-xslow` 1.2s |

| Role | Style |
|---|---|
| Statement | `.h0` 72/68 |
| Hero headline | `.h2` 40/44 |
| Section title | `.h3` 32/36 |
| Card title | `.h4` 24/28 (case card `.h5` 20/24) |
| Stat value | `.h1` 48/48 |
| Paragraph | `.body-md` 15/22 |
| Eyebrow / tag | `.eyebrow` / `.label-lg` 11/14 mono uppercase |

## Reference files
- `templates/`: `index.html`, `styles.css`, `motion.js`, `404.html`, `favicon.svg` (system reference, not a layout)
- `references/layouts.md`: layout signature, variation rules, 8 hero variants, section patterns by job, recipes, example compositions
- `references/motion.md`: motion principles, tokens, every animation, HTML API, framework recipes
- `references/illustrations.md`: isometric hairline illustration rules, generator spec, compositions
- `scripts/iso.py`: isometric illustration generator (presets: modules, stack, flow, single)
- `scripts/images.py`: pulls photos from Unsplash per image slot, writes URLs and credits
- `references/foundations.md`: color, type, spacing, radius, grid, effects, motion, icons, contrast
- `references/components.md`: anatomy of every component and block, forms, states, layout variety
- `references/copy.md`: voice, headline formulas, CTAs, content realism, banned words
- `references/ship-checklist.md`: final QA, SEO, and ship requirements
- `references/frameworks.md`: Next.js, Tailwind v3/v4, shadcn/MUI
- `references/figma.md`: building in Figma
- `references/pitfalls.md`: common mistakes and generic patterns to avoid
- `references/tokens.css`: the token set on its own
- `scripts/lint.py`: rule checker (`--strict` for delivery)
