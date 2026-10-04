---
name: site-edit
description: Make a change to the Attoset marketing website — edit copy, tweak a section, add a page, adjust layout/visuals, fix responsiveness. Use for any request to change, update, add, remove, restyle or fix something on the site. Routes the request to the right file, applies the house rules, and verifies with build + screenshots.
---

# Attoset site — change workflow

The app is `attoset-web/` (Next.js 16 · App Router · Tailwind v4 · framer-motion · lucide-react).
Run every command from `attoset-web/`.

Load the **`attoset-brand`** skill alongside this one whenever the change is visual,
new UI, or user-facing copy. This skill says *where* and *how*; that one says *what it should look like*.

## 1. Locate

Find the file before editing. Routing shortcuts:

| The request is about… | Go to |
|---|---|
| Wording, headings, lists, feature/FAQ/pricing/testimonial data, nav links, CTA link | `src/lib/content.ts` — **all copy lives here**, not in components |
| A whole band on a page (hero, security, pricing, FAQ…) | `src/components/sections/<name>.tsx` |
| A product visual (table, kanban, gantt, Atto chat, agents, building blocks) | `src/components/mockups/<name>.tsx` — built in code, never an image |
| Buttons, badges, eyebrows, container, section heading, reveal | `src/components/ui/` |
| Navbar, footer, logo | `src/components/layout/` |
| Which sections appear on a page, and in what order | `src/app/<page>/page.tsx` |
| Colors, fonts, radii, keyframes, `.reveal` classes | `src/app/globals.css` (`@theme` block) |
| Page title/description/OG, canonical | `src/lib/seo.ts` + the page's `metadata` export |
| Sitemap, robots, manifest, structured data | `src/app/sitemap.ts`, `robots.ts`, `manifest.ts`, `src/lib/schema.ts` |

Full section→page map: `references/file-map.md`.
When unsure which section renders a phrase: `grep -rn "the phrase" src/`.

## 2. Edit — house rules

Non-negotiable; breaking one is a regression, not a style choice.

- **Brand is "Attoset"** — capital A only. Never "AttoSet". Never mention Smartsheet anywhere.
- **Light mode only.** No `prefers-color-scheme: dark` default. Dark panels are deliberate design accents.
- **No raw hex outside `globals.css`.** Use tokens: `text-ink`, `bg-warm`, `text-orange`, `border-line`, `bg-peach`…
- **Orange is surgical** — CTAs, Atto/AI moments, one key highlight per band. Not large fills.
- **Animation: import `m`, never `motion`.** The app is wrapped in `LazyMotion … strict`, so `motion.*` throws at runtime. Animated components need `"use client"`.
- **`Reveal` is CSS-only** (IntersectionObserver + classes in `globals.css`). Don't rewrite it with framer-motion — it's used ~80×.
- **Don't opacity-gate anything above the fold with JS.** The hero `<h1>` and hero image use `anim-rise-solid` (translate only) to protect LCP. The hero stays a server component.
- **Fonts are Inter (body) + Plus Jakarta Sans (display).** Not Space Grotesk (rejected), not mono eyebrows (rejected) — `Eyebrow` is the orange accent pill, sentence case.
- Server Components by default; `"use client"` only for interactivity/animation.
- Icons: `lucide-react`, stroke `1.5–1.75`. Note lucide v1 dropped brand icons — social marks are inline SVGs in `src/components/ui/social-icons.tsx`.
- Next.js **16** — if an API is unfamiliar, read `node_modules/next/dist/docs/` rather than guessing from memory.

Adding a new section: create `src/components/sections/<name>.tsx`, put its copy in `content.ts`,
wrap blocks in `<Reveal>`, use `<Container>` + `<SectionHeading>` + `<Eyebrow>`, alternate
`bg-bg` / `bg-warm` against its neighbours, then import it into the page.

## 3. Verify — always

```bash
npm run lint && npx tsc --noEmit     # cheap, run on every change
npm run build                        # run before saying it's done
```

Visual check for anything that changes layout or visuals:

```bash
npm run dev                                              # background; note the port it prints
node scripts/shot.mjs --page home --w 1440,390           # one page, desktop + mobile
node scripts/shot.mjs --page features --sel "#security"  # one section only
node scripts/shot.mjs --w 360,768,1440 --overflow        # every page + overflow report
```

Pages are slugs: `home features pricing about contact` (comma-separate for several).
Add `--port <n>` if the dev server picked a port other than 3000.

Screenshots land in `screenshots/latest/` (override with `--out`). **Read the PNGs** —
don't claim a visual change works without looking. `--overflow` reports `docOverflow`
and offending elements; both must be 0 / empty at 360px.

Perf-sensitive changes (hero, fonts, images, anything newly client-side): confirm the hero
headline still paints immediately and no new heavy client component landed above the fold.
Baseline is ~92 mobile Lighthouse — don't regress it.

## 4. Report

Say which files changed, what was verified (lint / types / build / screenshots at which widths),
and anything intentionally left out. Don't commit or push here — when the change is approved,
the **`publish`** skill puts it live.
