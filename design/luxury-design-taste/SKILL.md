---
name: luxury-design-taste
description: Luxury streetwear design taste for SkyyRose surfaces — visual hierarchy, restraint, materials, motion, and imagery treatment. Use when doing any visual design, design review, or elevation work on skyyrose.co or the DevSkyy dashboard (mockups, theme CSS, hero sections, collection pages, motion passes). Do NOT use for generic non-SkyyRose UI work (use frontend-design) or native iOS glass surfaces (use liquid-glass-design). Replaces the lost high-end-visual-design / design-taste-frontend / image-taste-frontend skills.
---

# Luxury Design Taste — SkyyRose

Brand truth: "Luxury Grows from Concrete." Oakland-rooted luxury streetwear — NOT European maison minimalism. Canonical references: Kith, Oaklandish, Culture Kings, Fear of God, Palm Angels. Never Chanel/Dior/Celine lineage.

## When to use

- A surface on skyyrose.co (theme templates, collection pages, PDP, hero sections) or the devskyy.app dashboard is being designed, restyled, reviewed, or "elevated".
- A mockup or design reference HTML is being graded against brand canon.
- A motion/animation pass is being added to any SkyyRose surface.
- Another design skill (impeccable, ui-ux-pro-max, frontend-design) produced output that must be filtered through SkyyRose canon before shipping.

**When NOT to use:** generic frontend work with no SkyyRose brand surface (frontend-design owns that); native iOS SwiftUI/UIKit (liquid-glass-design); 3D scene architecture (immersive-interactive-architect / skyyrose-3d-web-os); product-copy or SEO work (skyyrose-market plugins).

## Inputs

Required before any taste judgment. **If any is absent, stop and obtain it — never proceed on memory.**

| Input | Canonical location | If absent |
|---|---|---|
| Brand tokens + fonts | `CLAUDE.md` §6 Brand; `wordpress-theme/skyyrose-flagship/theme.json`; `data/brand/typography.json` | Stop — read them; memory rots, tokens do not |
| Per-collection identity | `wordpress-theme/skyyrose-flagship/data/logo-registry.json` → `collections.<slug>` | Stop — this is the SOT (see `docs/CLAUDE.md`); never invent a palette |
| Visual reference canon | `docs/brand/visual-references.md` (The Five) | Stop — read it; proposing European-maison references is a canon violation |
| Product imagery, if any product appears | `data/sot-images.json` via `skyyrose.core.sot_images` | Stop — filenames are not identity; SOT-resolve or do not show the product |
| The surface under review | the actual file(s), or a live URL | Stop — taste review of an unread surface is a guess |

## The garment is the protagonist

Every surface serves the product photography. Copy, chrome, and motion are supporting cast.
- Imagery: on-model shots outrank ghost mannequins outrank flat lays. Full-bleed where possible.
- NEVER: urgency timers, countdown clocks, related-products/"wears with" cross-sell (retired canon), fake scarcity, discount-brand energy.
- Hero titles = brand-script lockup IMAGES (`assets/images/hero-overlays/` for BR/LH/SIG, `assets/images/logos/` for Kids), never type-rendered. Fonts are for interior text only.

## Restraint rules (what separates luxury from template)

- One accent per collection surface: Signature `#D4AF37`, Black Rose `#C0C0C0`, Love Hurts `#DC143C`, Kids Capsule `#B76E79`, on dark `#0A0A0A`. Two accents on one screen = flea market.
- Whitespace is the luxury signal. If a section feels empty, that's usually correct. Density is for dashboards, not storefronts.
- Type scale: big display moments (Archivo, expanded via `font-variation-settings: 'wdth' 125`) + tiny wide-tracked utility labels (Anton, 10-13px, 4-8px letter-spacing). The MIDDLE sizes are where generic creeps in — avoid 16-20px workhorse type on marketing surfaces.
- Materials: glass (rgba white 0.04-0.08 + blur), hairline borders (1px, low-alpha white), metallic gradients ONLY on brand-token hues. No drop shadows heavier than `0 24px 80px rgba(0,0,0,.4)` on dark.
- Contrast is a brand constraint: crimson `#DC143C` on `#0A0A0A` measures below WCAG AA for body text (see Verification) — fills/borders/glows only; de-emphasised text uses `--color-text-muted` (`#B3B3B3`, 9.44:1), never low-alpha white guessed by eye.

## Motion taste

- Ease: `cubic-bezier(.16,1,.3,1)` (the house curve, `--ease-luxury`). Duration 0.6-1.2s for reveals; nothing snaps.
- Motion must have narrative purpose: reveal on scroll, parallax depth, slow zoom (`heroZoom`-style 20-30s ambient). Decorative twitching = slop.
- Everything animated pauses under `@media (prefers-reduced-motion: reduce)` and stays legible when frozen.
- Auto-scrolling media (marquees, strips) must remain background texture: opacity ≤ 0.25 behind content, masked edges, and never compete with the lockup.

## Imagery treatment

- Product pixels are identity — verify garment matches SKU (eyes-on, reading pixels) before any imagery ships. Wrong-garment is the #1 recurring defect (lh-005 fanny-pack hallucination).
- Editorial treatment for background/ambient use: desaturate 30-40%, brightness 0.7-0.8, contrast +5%, vignette-mask edges. Full color is reserved for the product being sold.
- Aspect discipline: portrait 3:4/2:3 for garments, wide only for scenes. Never stretch, never letterbox with visible bars.

## Slop detectors (instant fail)

Centered-everything symmetric layouts; gradient text on headings; emoji in UI; 12-col bootstrap rhythm; uniform border-radius 8px everywhere; stock-photo energy (non-brand models, generic city b-roll); grey-on-white "SaaS clean" palettes; identical card grids without one broken/featured element for rhythm.

## Procedure

1. Load inputs (table above). Read the surface's actual CSS/HTML/template files — never review from a description.
2. Identify the collection register from the registry's `collections.<slug>` entry for the surface; note its single permitted accent hex.
3. Grade against each section above in order: protagonist → restraint → motion → imagery → slop detectors. Record each violation as `file:line` + the rule it breaks.
4. For every proposed change, state which rule it serves in one line. A change serving no rule is scope creep — drop it.
5. If the surface is theme CSS/JS, every edit requires `cd wordpress-theme && npm run build` — production serves `.min` (see skyyrose-design:theme-min-build).
6. Run Verification below before reporting the pass/fail verdict.

## Verification

Taste is judged; these floors are measured. A surface that fails a floor fails the review regardless of how it "feels".

1. Contrast floor — measure, never eyeball:

```bash
python3 -c "
def lum(h):
    r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    r,g,b=f(r),f(g),f(b); return 0.2126*r+0.7152*g+0.0722*b
fg,bg='DC143C','0A0A0A'
l1,l2=sorted((lum(fg),lum(bg)),reverse=True)
print(f'{(l1+0.05)/(l2+0.05):.2f}:1')
"
```

   **PASS:** every body-text fg/bg pair ≥ 4.5:1, large-display pairs ≥ 3:1. `[repro]`
   Observed 2026-07-28: `#DC143C` on `#0A0A0A` → `3.97:1` — below AA, which is WHY crimson is fills/borders/glows only.

2. Cut-font guard — the four retired fonts never return as declarations:

```bash
grep -rniE "font-family[^;]*(playfair|cormorant|bebas|yellowtail)" \
  wordpress-theme/skyyrose-flagship/assets/css wordpress-theme/skyyrose-flagship/theme.json
```

   **PASS:** exits 1, prints nothing. `[repo]` (Observed 2026-07-28: clean. A bare name-grep false-positives on the `fonts.css:13` changelog comment — scope to `font-family` declarations as above.)

3. Accent-discipline census — the palette in use must be the brand palette:

```bash
grep -rhoE '#[0-9a-fA-F]{6}\b' wordpress-theme/skyyrose-flagship/assets/css/*.css \
  | grep -v '.min.css' | tr 'A-F' 'a-f' | sort | uniq -c | sort -rn | head -8
```

   **PASS:** top counts are brand tokens (`#b76e79 #0a0a0a #d4af37 #dc143c #c0c0c0`) + neutrals; a non-token hue appearing in the top ranks is a drift finding. `[repo]`

4. Eyes-on render (mobile 390px + desktop) via Playwright/Chrome DevTools is a BROWSER aspect this skill cannot self-execute headlessly. **A SKIP is not a PASS** — flag it explicitly for the caller or run `verify:theme` aspect `responsive` in a browser-capable session. Severity claims about the live site require that `[live]` probe.

Rule inherited from `docs/skill-authoring-standard.md`: if any check above errors or times out, its empty output is an artifact, not a pass — re-run by hand. Before attributing a census/grep finding to your change, run the same command against a pristine tree (`git archive HEAD wordpress-theme | tar -x -C <scratch>`), never `git stash`.

## Worked example

Real session, 2026-07-28, this repo. Grading the theme's token discipline before a design pass:

```bash
$ grep -rhoE '#[0-9a-fA-F]{6}\b' wordpress-theme/skyyrose-flagship/assets/css/*.css \
    | grep -v '.min.css' | tr 'A-F' 'a-f' | sort | uniq -c | sort -rn | head -8
 478 #b76e79
 146 #0a0a0a
 103 #d4af37
  49 #050505
  48 #ffffff
  46 #dc143c
  31 #c0c0c0
  14 #2a2a2a
```

Verdict: top 8 are all brand tokens or neutrals (`#050505`/`#2a2a2a` are dark-surface steps) — no palette drift `[repo]`. The contrast probe on the same session returned `3.97:1` for crimson-on-dark `[repro]`, confirming the fills/borders/glows-only rule is load-bearing, not stylistic.

## Failure modes

- **Wrong-garment imagery ships** — the #1 recurring defect (lh-005; bug-096 ×30 hallucinated brand canon on 30 SKUs). Cause: trusting filenames/manifests instead of reading pixels. Fix: SOT-resolve + eyes-on before anything ships.
- **"Looks like a plausible BR/LH look" passes QC** — lenient-QC defect (bug-276 class); cost 16cr of bad hero clips. QC only against the canonical reference asset, side-by-side.
- **Crimson used for body text** — reads fine to the eye on a bright monitor, fails AA at 3.97:1. Always measure (Verification #1).
- **Cut fonts reintroduced** via a well-meaning "elegant serif" suggestion (ui-ux-pro-max recommends Cormorant for luxury queries — observed 2026-07-28). Filter every external recommendation through Verification #2.
- **Second accent creeps in** when composing sections from different collections onto one surface. One accent per surface, always.
- **Stale `.min` shipped** — source CSS edited, `.min` not rebuilt; production serves `.min` (bug-287 adjacent). `npm run build` + `verify:theme --only min-sync` closes it.

## Precedence

When design sources disagree: project `.impeccable.md` > this skill > impeccable > ui-ux-pro-max tables > interactive-web-development examples. ui-ux-pro-max's html-tailwind default and Liquid Glass recommendation are overridden for this project (vanilla CSS; glassmorphism banned outside `product-card-holo`). impeccable's reflex-font rejection does not apply to locked brand fonts (Archivo, Hanken Grotesk, Anton, Cinzel, Inter, plus the per-collection name-scripts: SkyyRose Black Rose Script, SkyyRose Love Hurts Graffiti, Pinyon Script, Grand Hotel — lockup images only, never interior).
