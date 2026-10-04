---
name: premium-website-design
description: Design distinctive, production-grade personal websites, portfolios, and landing pages end-to-end. Use when the user asks to build, redesign, or review a personal site, portfolio, landing page, or any visually-led marketing page, including brief inference, design direction, tokens, typography, tactile interactions, generative artwork (free watermark-free image generation + vision review), icon sourcing and verification, privacy-first content handling, light/dark themes, QA verification, and deploy readiness.
---

# Premium Website Design

Fused from taste-skill, high-end-visual-design, frontend-design, frontend-skill, hallmark, algorithmic-art, and webapp-testing. Ships personal sites that do not look templated.

## Workflow

Run these in order. Do not skip the design read or the verification gate.

1. **Design Read** - brief inference and dials
2. **Direction** - one committed aesthetic
3. **Tokens & skeleton** - palette, type, layout
4. **Interactions** - tactile motion layer
5. **Artwork** - imagery and privacy
6. **Verification & deploy** - evidence gate

---

## 1. Design Read

Declare one line before coding: "Reading this as: `<page kind>` for `<audience>`, with a `<vibe>` language, leaning toward `<aesthetic family>`."

Set three dials explicitly:

- `DESIGN_VARIANCE: 8` (1 = symmetry, 10 = artsy chaos)
- `MOTION_INTENSITY: 6` (1 = static, 10 = cinematic)
- `VISUAL_DENSITY: 4` (1 = gallery, 10 = cockpit)

Defaults for portfolios: 8 / 6 / 4. Calm editorial briefs: 5-6 / 3-4 / 2-3. Wild agency briefs: 9-10 / 8-10 / 3-4.

Redesign rules:
- Preserve IA, anchor slugs, nav labels, and analytics events.
- Audit brand tokens before touching them.
- Modernisation order: type refresh, spacing, color, motion, hero recomposition.

If the brief is ambiguous on one axis only, ask exactly one question; otherwise proceed with the read.

## 2. Direction

Pick ONE vibe and ONE layout archetype. Examples that work:

- **Editorial ink** (dark-first portfolio): deep blue-black surfaces, one electric accent, variable sans + mono labels, bento grid, generous whitespace.
- **Premium consumer**: cool paper neutrals with a single saturated pop; never default to beige + brass + espresso.
- **Kinetic poster** (launch/manifesto): centered manifesto type, one dominant visual, scroll-linked depth.

Rules:
- Max one primary accent. A second "signal" color is allowed only for semantic status, used sparingly.
- Shape system lock: cards 20px, pills 999px, inputs 12px (or one documented alternative).
- Theme lock: dark-first with `[data-theme="light"]` overrides; respect `prefers-reduced-motion`.
- Type: avoid Inter by default. Prefer a variable sans (e.g., Plus Jakarta Sans) paired with a mono for labels. Chinese text needs positive letter-spacing (0.01-0.06em); Latin display can go tighter.
- No AI tells: no purple gradients, no neon glows, no em-dash, no centered-hero-over-mesh default, no three equal feature cards, no decorative dots, no version labels.

## 3. Tokens & skeleton

Start from `assets/tokens.css` (dark-first OKLCH system with light overrides). Keep CSS variables for every color, shadow, radius, and type token.

Default page skeleton for a personal site:

```
hero (split: copy + layered portrait)
skills marquee (one marquee max)
bento grid (about, stats, capabilities, flagship)
work rows (period + title + KPIs)
timeline rail
education
contact (email + socials)
footer
```

Content hygiene:
- No phone numbers or private identifiers on public pages unless explicitly requested.
- Use year-only date ranges, not months.
- Put deployable files in a `public/` directory; keep README, logs, and private originals out of it.
- Real photo should be a generated avatar when privacy matters; keep the original locally, never in the public repo.

## 4. Interactions

Ship 2-3 intentional motions minimum: one entrance, one scroll-linked effect, one hover/feedback state. Implement the recipes in `references/interactions.md`.

Hard rules:
- Animate only `transform` and `opacity`.
- No `window.addEventListener("scroll")`. Use IntersectionObserver, CSS scroll-driven animations, or pointer events with rAF.
- Gate pointer-driven effects behind `(pointer: fine)` and `prefers-reduced-motion`.
- Every animation must justify itself: hierarchy, storytelling, feedback, or state transition.
- Buttons keep press feedback (`:active` down + edge shadow); magnetic pull must not break clickability (small offsets or a fixed wrapper).

## 5. Artwork

Prefer real imagery with a job: hero anchor, flagship proof, contact atmosphere.

- **Free API pipeline (recommended)**: SiliconFlow Kolors for watermark-free image generation + Zhipu GLM-4V-Flash for free visual review; keys come from environment variables only, never hardcoded. Details in `references/art-pipeline.md`.
- **No API key**: use the algorithmic-art pipeline (flow field / particles) in `references/art-pipeline.md`; export transparent WebP and blend with `screen` on dark, `multiply` on light.
- **Paid quota available**: generate a stylized avatar (e.g., Seedream image-to-image) from a reference photo; keep the likeness, then remove the real photo from the public repo.
- **Icons**: use `references/icons.md`. Prefer Iconify API or Simple Icons (official brand glyphs) over scraping; inline SVG with `fill: currentColor`, never external CSS masks.
- Optimize: crop to rendered aspect, resize to 2x display size, WebP q80+, lazy-load below-fold art, `fetchpriority="high"` only for LCP.
- Add `_headers`: long cache only for images/fonts; keep CSS/JS revalidating; version CSS/JS URLs on change.

## 6. Verification & deploy

Run the preflight checklist in `references/preflight.md`, then the QA script:

```bash
python scripts/qa_site.py --url http://localhost:8080
```

QA must cover: overflow at 1440/390/320, console errors, failed requests, font/image loading, both themes, reduced motion, mobile menu, counters, anchor navigation, and contrast (WCAG AA) on both themes.

Deploy readiness (static site on Cloudflare Pages):
- Framework preset: None
- Build command: `exit 0`
- Build output directory: `public`
- Production branch: main
- Result URL: `<project>.pages.dev`; verify the live site after deploy.

## References

- `references/preflight.md` - release gate checklist
- `references/interactions.md` - motion recipes with code
- `references/art-pipeline.md` - generative art + avatar + privacy
- `references/icons.md` - icon sourcing (Iconify / Simple Icons / iconfont) + verification
- `assets/tokens.css` - starter token system (dark-first + light)
- `scripts/qa_site.py` - generic Playwright verification
