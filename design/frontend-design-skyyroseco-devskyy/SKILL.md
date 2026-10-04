---
name: frontend-design
description: >
  Build production-grade frontends grounded in the user's existing codebase, framework, and design system.
  Read first, design second. Defaults: accessible (WCAG 2.2 AA), performant (Core Web Vitals budgeted),
  responsive (mobile-first). Use when building or restyling a page, view, component, or layout in a real
  codebase and the aesthetic register still has to be chosen — picks calm-editorial / dense-utility /
  expressive-brand from product context rather than impulse. Do NOT use for SkyyRose brand-canon taste
  calls (use luxury-design-taste — its tokens and fonts are locked and override every default here),
  and do NOT use for native iOS surfaces (use liquid-glass-design). Replaces the upstream frontend-design
  skill with codebase-aware behavior, production triad defaults, and an anti-fingerprint protocol.
version: 2.0.0
upstream: claude-plugins-official/frontend-design @ 5c392562 (May 2026)
license: see upstream LICENSE.txt
---

# frontend-design v2 — codebase-grounded production frontend

The upstream `frontend-design` skill tells the model what to *avoid* ("don't use Inter, don't make
purple-on-white gradients") without telling it what to *build*. The result: model designs in a
vacuum, ships portfolio-style aesthetics into B2B apps, and converges on the same dodge fonts and
"non-slop" patterns (grain overlays, custom cursors) that have themselves become slop.

This v2 inverts the priority:

1. **Read the user's codebase first.** Extend, don't replace.
2. **Match the product, not the trend.** Pick aesthetic register from product context.
3. **Production triad is non-negotiable.** Accessibility, performance, responsive — defaults, not aspirations.
4. **Anti-fingerprint protocol.** Concrete process to break LLM defaults, not vibes.
5. **Claude design vocabulary is one register among many.** Use it when the product context calls for calm-editorial — never as a global default.

---

## When to use

- A page, view, component, or layout is being built or restyled inside a real codebase.
- Existing UI works but reads flat, generic, or mismatched to its audience, and the aesthetic register needs deciding.
- A frontend PR needs grading against the production triad (accessibility, Core Web Vitals, responsive).
- Another skill produced markup/CSS and it must be grounded in the project's actual tokens and framework before shipping.

**When NOT to use:** SkyyRose brand-canon judgments — `luxury-design-taste` owns those and its locked tokens/fonts override Section 2 entirely. Native iOS/SwiftUI → `liquid-glass-design`. Pure design-direction interviewing before any code → `frontend-design-direction`. Token-system generation or a drift audit → `design-system`. 3D/immersive scene architecture → `immersive-interactive-architect`.

## Inputs

Gather these before the first aesthetic decision. **Any absent input is a stop, not a default.**

| Input | Where | If absent |
|---|---|---|
| Design tokens | `theme.json`, `tokens.css`, `design-tokens.css`, `tailwind.config.*` | Run the token census (Verification #1). Empty result → say "no tokens at <paths checked>, designing fresh" **in writing**; never assume greenfield silently |
| Framework + version | `package.json`, `next.config.*`, `vite.config.*` | Stop — reading version decides which APIs are legal; guessing ships code that will not build |
| Project overrides | `CLAUDE.md`, `.impeccable.md`, `BRAND.md`, `STYLEGUIDE.md`, `wordpress-theme/skyyrose-flagship/CLAUDE.md` | Stop and read. Section 6 makes these outrank this skill; proceeding without them is how a parallel design system gets shipped |
| Target contrast + CWV budget | project docs, else WCAG 2.2 AA and the Section 1 budgets | Default and state that you defaulted |
| A representative existing page in the same product area | the repo | Stop — voice, density, and motion style are read from a real page, not inferred |

## 0. The hard rule — read before you design

Before making *any* aesthetic choice (font, color, spacing, layout, motion), inventory what the user already has:

| Signal | Where to look | What it tells you |
|---|---|---|
| Design tokens | `tokens.css`, `design-tokens.css`, `theme.json`, `tailwind.config.*`, `figma-tokens.json` | Exact palette + type scale to extend |
| Component library | `components/`, `ui/`, `node_modules/@shadcn`, `@chakra-ui`, `@mui`, `@mantine` | Existing visual vocabulary |
| Brand / style guide | `BRAND.md`, `STYLEGUIDE.md`, `DESIGN.md`, `CLAUDE.md`, `docs/brand*` | Rules that override your defaults |
| Existing pages | A representative page in the same product area | Voice, density, motion style |
| Framework + version | `package.json`, `next.config.*`, `vite.config.*`, `astro.config.*` | What APIs you can use |
| Lint / TS config | `eslint.config.*`, `tsconfig.json` | Enforced rules to respect |

**If a design system exists, extend it.** Pull colors, fonts, spacing, and component patterns from there. Justify any token addition.

**Greenfield is the exception, not the default.** If you're certain no system exists, design from scratch — and *say so explicitly* in your plan ("no existing tokens at <paths checked>, designing fresh").

Skip this step and you ship a parallel design system that fights the user's existing one. This is the most common AI-frontend failure mode and the one this skill exists to prevent.

---

## 1. Production triad — non-negotiable

The upstream skill claims "production-grade" three times in 42 lines and mentions accessibility, performance, and responsive design zero times. Production-grade means all three.

### Accessibility (WCAG 2.2 AA minimum)

- **Contrast**: 4.5:1 normal text, 3:1 large text (18px+ bold / 24px+), 3:1 UI components and graphical objects.
- **Focus**: visible 2px+ outline on every interactive element. Never `outline: none` without a `:focus-visible` replacement.
- **Touch targets**: minimum 44×44 CSS px.
- **Alt text**: meaningful images get descriptive `alt`; decorative get `alt=""` + `aria-hidden="true"`.
- **Keyboard**: every interaction reachable by Tab; logical tab order; skip-to-content link on text-heavy pages.
- **Motion**: every animation respects `@media (prefers-reduced-motion: reduce)`.
- **Color alone**: never the only carrier of meaning. Add icon, label, or text affordance.
- **Form labels**: every input has a visible `<label>` or `aria-labelledby`. Placeholder is not a label.
- **Headings**: sequential h1→h6, no level skips. One h1 per page.

### Performance (Core Web Vitals budget)

- **LCP < 2.5s**: preload the hero image, self-host fonts with `font-display: swap`, inline above-fold critical CSS.
- **CLS < 0.1**: every `<img>` has explicit `width`/`height` or `aspect-ratio`; reserve space for async content with skeletons.
- **INP < 200ms**: defer non-critical JS to body end; debounce scroll/resize; never run layout-triggering animations on scroll.
- **Image budget**: hero ≤ 200KB, content image ≤ 80KB. Prefer AVIF with WebP fallback. Always set responsive `srcset` + `sizes`.
- **JS budget**: critical-path JS ≤ 150KB gzipped. Split routes. Lazy-load below-fold modules.
- **Font loading**: max 2 font families. Subset to the characters used. Preload only the weights rendered above the fold.

### Responsive (mobile-first)

- **Body text ≥ 16px** to prevent iOS auto-zoom on focus.
- **Mobile-first media queries**: write the small-screen layout as the base; expand with `min-width:` queries.
- **Breakpoints** (rough defaults — adopt the project's if it has them): `375px` (small phone), `768px` (tablet), `1024px` (desktop), `1440px` (large desktop).
- **Touch hover**: never depend on `:hover` for primary affordance. Gate `:hover` rules behind `@media (hover: hover) and (pointer: fine)`.
- **Safe area**: pad for iOS notch / Android gesture bar via `env(safe-area-inset-*)` on full-bleed layouts.
- **Viewport**: prefer `100dvh` over `100vh` to handle the mobile address bar correctly.
- **Container queries** where the component is reused across very different parents.

---

## 2. Aesthetic register — match the product

Three named registers. Pick **one** for the product and commit. Mixing registers within a single product reads as incoherence, not range.

### Register A — Calm Editorial (Claude design vocabulary)

**When to use**: long-form content, marketing sites, documentation, editorial products, AI tools and assistants that want to feel considered rather than flashy, products that compete on trust and clarity over novelty.

**Influences**: Anthropic claude.ai, The Atlantic, Aeon, NYRB, Apartamento, mid-century Swiss editorial design, contemporary print magazines, Tufte's information design.

**Palette** — warm, paper-toned, low-saturation. Never cold blue, never neon, never glassmorphism:

```css
--paper-bg:       #FAF9F5;  /* warm cream — base canvas */
--paper-bg-deep:  #F4F2EA;  /* slightly lifted paper, for inset blocks */
--ink-primary:    #191919;  /* deep slate — body text */
--ink-secondary:  #5C5C5C;  /* muted slate — supporting copy */
--ink-tertiary:   #8C8C8C;  /* metadata, timestamps */
--accent-warm:    #D97757;  /* terracotta / clay — sparing accent */
--rule-soft:      #E8E4D8;  /* hairline border, paper-toned */
--surface-card:   #FFFFFF;  /* lifted surface, against paper background */
--surface-inset:  #F4F2EA;  /* inset blocks, code, quotes */
```

Dark mode (optional, not default): invert the paper warmth to warm charcoal, not cold black:

```css
--paper-bg:       #1E1B16;  /* warm charcoal — base canvas */
--paper-bg-deep:  #161310;
--ink-primary:    #F4F1E8;  /* warm off-white text */
--ink-secondary:  #C2BDB0;
--accent-warm:    #E89B7B;  /* lifted terracotta for dark bg */
--rule-soft:      #2E2A22;
```

**Typography** — editorial serif display + restrained sans body:

- **Display** (h1/h2/hero): a contemporary serif with character. Strong defaults: **Tiempos Headline**, **Newsreader** (open source), **Source Serif 4** (open source), **Fraunces** (variable, characterful), **GT Sectra**, **Sang Bleu**, **Editorial New**.
- **Body**: a humanist or transitional sans, used with discipline. Strong defaults: **Söhne**, **Untitled Sans**, **National 2**, **GT America**, **ABC Diatype**. Inter is acceptable *only* when restraint is the point and it's used at a single weight family.
- **Pairing rule**: pair a serif display with a sans body, OR pair a serif at varied weights throughout. Never pair two sans-serif faces.
- **Type scale**: classical 1.25 (major third) or 1.333 (perfect fourth). Avoid the 1.5+ scales that flatten hierarchy.

**Spacing** — generous, breathing:

- Section vertical padding: `clamp(4rem, 8vw, 8rem)`.
- Container max-width: `1100-1200px` with `clamp(1.5rem, 4vw, 3rem)` horizontal padding.
- Body line length: `60-75ch` (use `max-width: 65ch` on long-form blocks).
- Body line-height: `1.6-1.75`. Display line-height: `1.05-1.15`.

**Motion** — restrained, intentional:

- Opacity transitions + small `transform: translateY(8px)` reveals. No parallax, no scroll-jacking, no element-by-element entrance choreography.
- Duration `300-600ms`. Easing `cubic-bezier(0.16, 1, 0.3, 1)` (a calm cinematic).
- One hero entrance per page, maximum. Other motion only on user intent (hover, click, focus).

**Texture** — atmosphere through palette, not effects:

- The warmth of the paper background *is* the texture.
- No grain overlay, no noise SVG, no gradient mesh, no glassmorphism.
- Hairline borders (`1px solid var(--rule-soft)`) carry the editorial feel without effects.

**Layout** — editorial grid:

- Asymmetric balance. Generous left/right margins. Print-spread proportions.
- Pull quotes set apart with rules above and below, not boxes.
- Hierarchy through size + weight + space, not boxes and shadows.
- Footnotes and marginalia as design elements where the content warrants it.

**Anti-traits — do not do, even if the rest of the register is in place**: drop shadows beyond `0 1px 2px rgba(0,0,0,0.04)`, gradient backgrounds, neon focus states, animated emojis, gradient text, glass cards, custom cursors, scroll-triggered video, hero video autoplay.

### Register B — Dense Utility

**When to use**: dashboards, internal tools, admin panels, data-heavy apps, developer tools, anything where information density is the primary value.

**Palette** — high-contrast, functional. Pick light or dark; both work. Saturation is muted; semantic colors exist only for status:

```css
--surface:    #FFFFFF;       /* or #0B0F14 for dark */
--surface-2:  #F7F9FC;       /* table stripes, inset blocks */
--text:       #0E1116;
--text-muted: #5B6470;
--border:     #E5E9EE;
--accent:     #2563EB;       /* or your brand primary */
--positive:   #15803D;
--negative:   #B91C1C;
--warning:    #B45309;
```

**Typography**: a single sans-serif at multiple weights. Tabular numerals (`font-variant-numeric: tabular-nums`) on every numeric column. Monospace for code, IDs, and timestamps.

**Spacing**: tight. 4 / 8 / 12 / 16 / 24 px scale. Information density wins over breathing room.

**Motion**: skeletons, optimistic UI, no entrance animations. Motion exists to confirm action, never to delight.

**Layout**: data tables, side rails, dense cards, multi-column reading. Sticky table headers. Bulk-action toolbars. Keyboard shortcuts visible.

### Register C — Expressive Brand

**When to use**: brand sites, portfolios, product launches, marketing campaigns, event sites — places where the design IS the product.

**Constraints**: this register has the most freedom AND the highest risk of slop. Apply guardrails:

- Pick a **single conceptual hook** ("the year of the rose", "industrial precision", "summer 1974", "deep East Oakland streetwear") and commit. Every aesthetic choice ties back to it.
- One unique typography pairing per project. Source it from a recent typography release, a printed reference, or a brand identity book. Do not pull from the AI-default pool (Space Grotesk, JetBrains Mono, Recursive, Inter Display, Plex).
- Motion is allowed at higher intensity, but cap it: one hero choreography, one signature interaction. Not 15 animated elements per scroll.
- Texture allowed if it's tied to the hook (paper grain on a photography portfolio, not generic noise on a SaaS page).
- Dark mode is allowed but not the default unless the hook demands it.
- The product still ships the production triad — expressive does not mean inaccessible or slow.

---

## 3. Anti-fingerprint protocol

The upstream skill says "NEVER converge on common choices (Space Grotesk, for example)" but provides no mechanism. Here is the mechanism. Run all four steps before writing any aesthetic CSS.

### Step 1 — Name the default you'd reach for first

Out loud, in your plan, state what you'd default to. Example: *"First instinct: Inter body + Space Grotesk display, slate-on-white, shadcn card-grid layout, framer-motion entrance animation."*

### Step 2 — Reject that default

Unless the project's existing system already uses it, **do not pick it**. Your first instinct is the LLM training-set fingerprint. The default has been overproduced for two years.

### Step 3 — Source the alternative from a non-default place

Pull from one of these, not from prior:

- A typeface foundry's current "what's new" page (Klim, Grilli Type, Commercial Type, Production Type, ABC Dinamo, Pangram Pangram, OHno Type).
- A printed brand book or annual report.
- A museum identity (MoMA, Tate, Whitney, V&A all publish design guidelines).
- A magazine you'd actually read (Apartamento, Toilet Paper, MacGuffin, Modern Matter, Cabinet).
- A printed reference book from a tradition outside web design (Swiss railway timetables, mid-century cookbook design, 1970s technical manuals, art-house cinema posters).

### Step 4 — Justify in one line

Every major choice (font, palette, layout, motion) gets a one-line justification in the plan or PR description: *"Newsreader display because long-form essay context needs a contemporary serif with character, and the project's content lives between Aeon and a tech blog — Tiempos would feel too newspaper, Söhne would feel too SaaS."*

If you can't write the justification, you don't understand the choice well enough to ship it.

---

## 4. Patterns that aged into slop — drop these

The upstream skill recommends grain overlays, custom cursors, gradient meshes. These were the 2022-2023 "anti-default" choices that defined the AI-coded-website look of 2023-2025. They are now the slop.

**Drop, as of 2026:**

| Pattern | Why it's slop now |
|---|---|
| Grain / noise overlay (`feTurbulence`, noise SVG, blend mode) | Defined the 2023-2024 AI portfolio look. Every Vercel template had it. |
| Custom cursors | Break native cursor semantics, fail on touch, become a tell of AI-generated sites. |
| Glassmorphism (`backdrop-filter: blur` on cards/nav) | 2021 macOS Big Sur knockoff; ubiquitous in 2023 SaaS templates. |
| Purple → pink gradient backgrounds | The original AI-coded marketing site fingerprint. |
| Gradient text via `background-clip: text` | Massively overused 2022-2024; now reads as effortful. |
| Space Grotesk display + Inter body | The "I avoided Inter" dodge that became its own default. |
| Shadcn/ui default theme untouched | Identifiable on sight. Extend tokens or pick a different starting kit. |
| Tailwind default palette (`bg-slate-50`, `text-slate-900` everywhere) | Same. Extend or replace. |
| Dark mode default with cold black `#000` background | Tells the user nothing was considered for warmth. Use warm charcoal if dark, or default to light. |
| Scroll-jacking / horizontal scroll on vertical wheel | Aged poorly, breaks browser conventions, accessibility regression. |
| Animated emojis as decorative elements | 2023 startup fingerprint. |
| Hero video autoplay | Performance hit + accessibility issue + tells nobody read the brand. |
| `cursor: pointer` on non-link elements | Lazy hover affordance. Reach for proper interactive elements. |
| `border-radius: 9999px` on every card / button | The "everything pill-shaped" look. Vary radius to express hierarchy. |

This list will need quarterly review. What's slop shifts. Bump skill version when the list changes.

---

## 5. Framework + design-system decision tree

```
Does the project ship a design system / token file?
├── YES → extend it. Read the tokens. Match the naming. Add only what's missing.
│         Do NOT introduce a parallel system.
└── NO → does the project have a UI library installed?
    ├── shadcn/ui detected (components.json or ui/ dir)
    │   → start from shadcn primitives, extend theme tokens
    │     (do NOT ship the default neutral theme verbatim)
    ├── @chakra-ui / @mui / @mantine / @radix-ui / @ariakit
    │   → use their theming API; respect their composition patterns
    ├── Tailwind detected (tailwind.config.*)
    │   → extend tailwind.config; never ship default slate palette
    │     without customization
    ├── Unstyled (vanilla CSS / CSS modules / styled-components)
    │   → design tokens file at src/styles/tokens.css; CSS custom
    │     properties; layered by concern (palette, type, space, motion)
    └── Greenfield → say so explicitly; pick a register from section 2;
                      design from scratch with the constraints above
```

**Framework checks before writing code:**

- `package.json` → React version, Next.js version, Vite, Astro, Svelte, SolidJS, Qwik
- `next.config.*` → App Router vs Pages Router (affects component model, RSC vs client components)
- `tailwind.config.*` → existing tokens, plugins, content paths
- `tsconfig.json` → `strict`, `paths`, JSX runtime
- `.eslintrc*` / `eslint.config.*` → enforced rules, import order
- `postcss.config.*` → autoprefixer targets, nesting support
- `.browserslistrc` or `browserslist` field → target browsers (affects CSS feature use)

**Modern frontend reality (2026)**:

- React Server Components are first-class — prefer them for static content.
- CSS nesting and `@scope` are widely supported — use them.
- View Transitions API is shipping in Chrome/Safari — use for cross-page transitions over JS animations.
- `:has()` is supported everywhere — use for parent-based conditional styling.
- Container queries are baseline — prefer them over media queries when the component is reused.
- `color-mix()` and `oklch()` are baseline — prefer over hex for derived colors.

---

## 6. Project overrides take precedence

If the project ships any of these, **they override this skill's defaults**:

- `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` at repo root or in scope.
- `BRAND.md`, `STYLEGUIDE.md`, `DESIGN.md`, `DESIGN-PRINCIPLES.md`.
- A skill named `<project>-design` or `<brand>-theme`.
- An ADR or RFC documenting visual / UX decisions.
- A Figma library or design system documented in the repo.

Read those first. **This skill is the floor of expectations, not the ceiling.** The project's own guide wins every conflict.

**SkyyRose project note**: `wordpress-theme/CLAUDE.md` documents the WordPress theme conventions (PHP escaping rules, enqueue priorities, builder integration, brand palette tokens). When working on `wordpress-theme/skyyrose-flagship/`, that file is the canonical spec and overrides this skill's framework-agnostic guidance. Brand canon: Rose Gold `#B76E79`, Dark `#0A0A0A`, Silver `#C0C0C0`, Crimson `#DC143C`, Gold `#D4AF37`. Tagline: "Luxury Grows from Concrete." No blue ever. The four collections are Black Rose, Love Hurts, Signature, Kids Capsule. For SkyyRose work, also load the `skyyrose-brand-dna` skill.

---

## 7. Pre-ship checklist

Before declaring frontend work done:

- [ ] Read existing tokens, components, brand guide — or stated explicitly that none exist.
- [ ] Picked one aesthetic register, justified the pick from product context.
- [ ] Every major aesthetic choice has a one-line non-default justification.
- [ ] Contrast checked against WCAG 2.2 AA at target sizes.
- [ ] All interactive elements have visible `:focus-visible` states.
- [ ] `prefers-reduced-motion` respected (animations disabled or reduced to opacity-only).
- [ ] Touch targets ≥ 44×44 CSS px.
- [ ] All `<img>` elements have `width`/`height` or `aspect-ratio` set.
- [ ] Hero image preloaded; below-fold images `loading="lazy"`.
- [ ] Mobile layout verified at 375px width.
- [ ] Body text ≥ 16px to prevent iOS auto-zoom.
- [ ] No grain overlay, custom cursor, glassmorphism, or other Section 4 anti-patterns.
- [ ] If the project has a `CLAUDE.md` / design system, the implementation extends rather than replaces it.
- [ ] Lint, type-check, build all pass.
- [ ] No console errors or warnings in browser devtools.

---

## Procedure

1. Run the token census (Verification #1) and read the framework versions. Write both down before choosing anything.
2. Read the project overrides listed in Section 6. If one exists, its rules replace the corresponding defaults here — say which ones, explicitly.
3. Pick one aesthetic register from Section 2 and justify it from product context in one line. Mixed registers read as incoherence.
4. Run the anti-fingerprint protocol (Section 3) in full — name the default, reject it, source the alternative, justify in one line.
5. Implement against the existing tokens and component vocabulary. Every new token added gets a written justification.
6. Walk the Section 7 pre-ship checklist item by item; each unchecked box is a blocker, not a nit.
7. Run every Verification check below and report the outputs, not the intent. On WordPress theme CSS/JS, `npm run build` is mandatory before any claim about what production serves.

## Verification

Each check names the command, the pass condition, and its evidence scope. Design taste is not gradeable by command — the production triad is, and that is what these checks bind.

1. **Token census** — decides extend-vs-greenfield, and makes "no tokens exist" falsifiable:

```bash
ls frontend/tailwind.config.ts frontend/app/globals.css \
   wordpress-theme/skyyrose-flagship/theme.json 2>/dev/null
```

   **PASS (extend mode):** at least one path listed → read it and extend; a parallel system is a defect.
   **PASS (greenfield):** prints nothing, and you state the checked paths in writing. `[repo]`

2. **Contrast floor**, computed for every text/background pair you introduce:

```bash
python3 -c "
def lum(h):
    r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    r,g,b=f(r),f(g),f(b); return 0.2126*r+0.7152*g+0.0722*b
for fg,bg in [('B76E79','0A0A0A')]:
    l1,l2=sorted((lum(fg),lum(bg)),reverse=True)
    print(fg,bg,f'{(l1+0.05)/(l2+0.05):.2f}:1')
"
```

   **PASS:** normal text ≥ 4.5:1, large text and UI components ≥ 3:1. `[repro]`
   (Observed 2026-07-28: `#B76E79` on `#0A0A0A` → `5.20:1` — clears AA for body text.)

3. **Section 4 anti-pattern grep** — the aged-into-slop list has exact CSS signatures, so read them with a command, not with your eyes:

```bash
grep -rnE 'background-clip:\s*text|backdrop-filter:\s*blur|feTurbulence|cursor:\s*url\(' \
  wordpress-theme/skyyrose-flagship/assets/css/*.css frontend/app/globals.css 2>/dev/null \
  | grep -v '.min.css' | head
```

   **PASS:** zero hits, or each hit justified in writing at its `file:line`. `[repo]`

4. **Build + type-check** — the project's own gate, whichever applies:

```bash
cd wordpress-theme && npm run build          # theme CSS/JS: production serves .min
cd frontend && npm run build                 # dashboard
```

   **PASS:** exits 0. For the theme, follow with `bash skyyrose-flagship/scripts/verify-theme.sh --only min-sync` — **PASS:** every `.min` byte-identical to a fresh build. `[test]`

5. **Rendered proof at 390px and desktop, plus an axe pass** — these are BROWSER aspects (`verify-theme.sh --list` labels `responsive`, `a11y-interactive`, and `cwv` as BROWSER). This skill cannot execute them headlessly. **A SKIP is not a PASS:** name the caller or the browser-capable session that closes them, and never assert a live severity without that `[live]` probe.

Inherited: a check that errors or times out yields an artifact, not a pass — re-run by hand (bug-230). Before attributing a grep or build failure to your change, run the same gate against a pristine tree — `git archive HEAD <path> | tar -x -C <scratch>` — and diff the *contents*, because a new violation hides as one more line inside an already-red check. **Never `git stash`**: the stash stack is shared across worktrees.

## Worked example

Real invocation in this repo, 2026-07-28 — deciding extend-vs-greenfield for the DevSkyy dashboard:

```bash
$ ls frontend/tailwind.config.ts frontend/app/globals.css
frontend/app/globals.css
frontend/tailwind.config.ts

$ grep -nE "colors|#[0-9a-fA-F]{6}|fontFamily" frontend/tailwind.config.ts | head -6
12:  		fontFamily: {
17:  		colors: {
19:  				'rose-gold': '#B76E79',
20:  				'rose-dark': '#8B5465',
21:  				'rose-light': '#D4A5B0',
22:  				charcoal: '#1A1A1A',
```

Outcome: **extend mode** — a Tailwind token layer already carries the brand rose-gold ramp, so Section 5's decision tree routes to "extend `tailwind.config`; never ship the default slate palette" `[repo]`. Framework read from `frontend/package.json`: `next ^16`, `react ^19.2.3` `[repo]` — App Router and RSC are available, so static sections are server components by default. The contrast probe returned `#B76E79` on `#0A0A0A` → `5.20:1` `[repro]`, clearing AA for body text on the dark surface.

## Failure modes

- **Shipping a parallel design system.** The failure this skill exists to prevent: tokens existed, nobody looked, two systems now fight. Verification #1 makes it falsifiable — run it first.
- **Silent greenfield.** Concluding "no design system" without naming the paths checked. That is a fail-open default (bug-230, ×6): absent input must stop you, or at minimum be stated out loud.
- **Register mixing.** Calm-editorial hero over a dense-utility table. Pick one register per product and commit.
- **Anti-fingerprint theatre.** Naming the default then picking its nearest neighbour (Inter → Space Grotesk). Section 4 lists that specific dodge as slop; source from Step 3's non-default places.
- **Claiming production behavior from repo state.** A committed CSS change is `[repo]`; what skyyrose.co serves is `[live]` and requires `curl -s "URL?cb=$(date +%s)"` — **never WebFetch**, which strips `<script>`, and never an uncached curl, because Batcache serves stale (bug-287).
- **Editing theme CSS without rebuilding `.min`.** Production serves the minified bundle; a source-only edit ships nothing while every local check stays green.

## Notes on this skill

- **Replaces** upstream `claude-plugins-official/frontend-design @ 5c392562` (May 2026). Upstream emphasizes anti-defaults without positive guidance; this version inverts to codebase-first, production-triad-default, register-based selection.
- **Includes** the Claude design vocabulary as Register A. **Register A is not the default** — pick the register that matches the product. Forcing claude.ai's calm-editorial palette on every project would itself be slop.
- **Drops** the upstream's WordPress-specific extensions that lived in the previous local 20KB fork. For project-specific theme work, defer to that project's `CLAUDE.md` (e.g., `wordpress-theme/CLAUDE.md`).
- **Quarterly review**: the Section 4 anti-pattern list and the typeface defaults in Section 2 need refreshing as the slop horizon shifts. Bump skill `version:` when material changes ship.
