---
name: 9designer
description: "Codex-native image-to-website pipeline. Give any reference image and 9designer writes a complete structured blueprint (brand, colors, fonts, grid, full design toolkit selection, every section spec, every asset slot), renders that blueprint as an imagegen visual for confirmation, then builds the full working Next.js website from the blueprint -- every page, every component, every Motion for React / Framer Motion animation -- then deploys it live to Vercel. Nothing is guessed. The blueprint drives everything."
---

# 9Designer

Give any image. 9Designer writes a precise blueprint. Selects the full design toolkit. Renders it as a visual. You confirm. It builds the complete working website -- every page, every component, every Motion for React / Framer Motion animation -- exactly to spec. Then deploys it live.

The blueprint is the contract. The imagegen is the preview. The code is the output.
Nothing is guessed. Nothing is improvised.

!! IMAGEGEN IS THE HIGHEST PRIORITY CAPABILITY IN THIS SKILL !!

Every visual asset -- hero images, section illustrations, product shots, background
scenes, gallery images, team photos, feature graphics -- MUST be generated using
imagegen. There are NO exceptions. Do not substitute SVG drawings, CSS gradients,
placeholder divs, or stock-photo URLs for imagegen assets. If imagegen has not
been called for an asset slot, that slot is NOT done.

The ONLY files that are hand-crafted (not imagegen) are:
  - logo-main.svg (SVG wordmark, drawn to match the brand mark)
  - favicon.svg or favicon.png (simplified version of logo mark)
  - Lucide/Phosphor icon components (UI icons only, not decorative art)

Everything else is imagegen. Always. No exceptions.

---

## The Architecture

```
[USER] gives any reference image
       |
[STEP 1] ANALYZE
         Read the image. Extract design intent:
         brand direction, category, tone, color palette,
         layout style, imagery type, section patterns.
         (30 seconds. No output yet.)
       |
[STEP 2] WRITE THE BLUEPRINT
         Produce the complete structured specification document.
         Every value locked before imagegen runs:
         - Brand identity (name, tagline, category)
         - Exact color tokens (hex codes + roles)
         - Exact typography (font names, weights, sizes per breakpoint)
         - Grid system (columns, gaps, container width)
         - Layout variant (nav style, hero style, scroll, motion, mood)
         - Design toolkit (animation lib, components, icons, effects)
         - Every section with layout spec, content, dimensions
         - Every asset slot (type, ratio, position, imagegen prompt)
         - Every interactive element (behavior, animation pattern)
         - All pages to be built
       |
[STEP 3] GENERATE IMAGEGEN FROM BLUEPRINT
         Translate the blueprint into one imagegen prompt.
         Nothing added, nothing invented -- every element was
         already defined in the blueprint.
       |
[PAUSE] PRESENT TO USER
        Show: imagegen visual + blueprint summary card.
        "Here is [BRAND]. Blueprint is locked. Say GO to build."
       |
[USER] says: go / yes / build / next / looks good / proceed
       |
[STEP 4] GENERATE ALL ASSETS FROM BLUEPRINT
         Use asset slots defined in blueprint. Each imagegen call
         uses the exact prompt, ratio, and style from the blueprint.
       |
[STEP 5] BUILD ALL PAGES FROM BLUEPRINT
         Next.js 14 App Router + TypeScript + Tailwind + chosen toolkit.
         Every section specced. Every asset named and positioned.
         Code is a direct translation of blueprint to components.
         No decisions made during build -- all decisions already made.
       |
[STEP 6] FIDELITY VERIFICATION
         Compare each built page against its imagegen visual.
         Fix every gap before moving to next page.
       |
[STEP 7] DEPLOY TO VERCEL
         `vercel --prod` from project root.
         Live at https://[brand-slug].vercel.app
       |
[DONE] Live website delivered.
```

---

## Step 1 -- Analyze

**First: check for user-specified category or intent.**

If the user said anything like "make it a SaaS", "turn this into a bakery",
"I want a gaming site", "design it as a portfolio" -- that instruction overrides
everything the image suggests. The image becomes visual inspiration only
(color energy, aesthetic mood, imagery style). Brand name, sections, content
structure, and nav/layout decisions all follow the specified category.

If no category was specified -- read the image and infer it.

Read the reference image silently. Extract:

- Category: use user override if given, otherwise infer from image
  (SaaS / gaming / fashion / food / agency / portfolio / tech / finance /
   health / beauty / bakery / real estate / music / sports / other)
- Dominant tone (aggressive / minimal / luxury / editorial / playful / technical / warm / bold)
- Color temperature (dark / light / colorful / monochrome / gradient-heavy)
- Layout energy (structured / editorial / chaotic / minimal / dense / airy)
- Imagery style (photography / illustration / 3D / abstract / gradient / mixed / typographic)
- Implied site scale (single long-scroll / multi-page standard / large multi-section)

Do not output anything yet. Carry this into Step 2.

---

## Step 2 -- Write the Blueprint

This is the most important step. Write the complete blueprint document before anything else.
Every value is decided here. Nothing gets decided during build.

Output the blueprint in this exact format:

```
========================================
BLUEPRINT: [BRAND NAME]
========================================

BRAND
  name:      [invented brand name fitting the aesthetic]
  tagline:   [1-line brand tagline]
  category:  [SaaS / gaming / clothing / food / agency / etc.]
  tone:      [one word: aggressive / minimal / luxury / editorial / technical / warm / bold]
  domain:    [brand-name.com]
  slug:      [brand-name] (lowercase, hyphens -- used for project folder + Vercel URL)

----------------------------------------
COLORS
----------------------------------------
  --clr-primary:     #[hex]   [role: main brand color]
  --clr-accent:      #[hex]   [role: highlight, CTAs]
  --clr-bg:          #[hex]   [role: page background]
  --clr-surface:     #[hex]   [role: cards, panels]
  --clr-surface-2:   #[hex]   [role: elevated surface, borders]
  --clr-text:        #[hex]   [role: primary text]
  --clr-text-muted:  #[hex]   [role: secondary text, captions]
  --clr-border:      #[hex]   [role: dividers, outlines]

----------------------------------------
TYPOGRAPHY
----------------------------------------
  display-font:  [Font Name], [weight], [style]  -- Google Fonts
  heading-font:  [Font Name], [weight]            -- Google Fonts
  body-font:     [Font Name], [weight]            -- Google Fonts
  mono-font:     [Font Name], [weight]            -- Google Fonts (if numbers/code used)

  Desktop scale (Perfect Fourth 1.333 ratio):
    hero-text:    [px] / line-height [1.05-1.15] / letter-spacing [-0.02em to -0.04em]
    h1:           [px] / line-height [1.1-1.2]
    h2:           [px] / line-height [1.2-1.3]
    h3:           [px] / line-height [1.3]
    body:         [px] / line-height [1.6-1.75] / max-width 65ch
    small:        [px]
    label:        [px] / letter-spacing [0.1-0.15em] / uppercase yes

  Mobile scale (375px):
    hero-text:    [px]
    h1:           [px]
    h2:           [px]
    h3:           [px]
    body:         [px] (min 16px)

----------------------------------------
GRID
----------------------------------------
  container:      max-width [px], px-4 mobile / px-8 desktop
  columns:        [12 / 6 / custom]
  column-gap:     [px] (multiple of 8)
  row-gap:        [px] (multiple of 8)
  section-padding: [px] vertical desktop / [px] vertical mobile (min 80px / 48px)

----------------------------------------
LAYOUT VARIANT
----------------------------------------
  Choose one from each row. Pick based on the reference image energy,
  the category, and the tone. Vary every time -- do not default to same choices.

  nav-style:
    top-transparent-blur  | top-solid       | left-sidebar
    right-sidebar         | bottom-bar      | floating-pill
    hamburger-only        | mega-menu

  hero-style:
    banner-short          | half-viewport   | full-viewport
    super-tall            | typographic-only| split-50-50
    split-asymmetric      | full-bleed-overlay | product-dominant
    editorial-diagonal    | centered-radial | video-bg

  scroll-behavior:
    standard-vertical     | snap-sections   | horizontal-sections
    parallax              | sticky-text     | cinematic

  motion-level:
    static                | subtle          | moderate
    rich                  | cinematic

  layout-mood:
    minimal               | editorial       | dense
    bold-maximalist       | brutalist       | playful
    luxury                | technical

  code-stack:
    nextjs-ts-tailwind    | react-ts-tailwind | html-css-js   | html-gsap

  site-scale:
    micro                 | standard        | large

  SELECTED:
    nav-style:       [chosen]
    hero-style:      [chosen]
    scroll-behavior: [chosen]
    motion-level:    [chosen]
    layout-mood:     [chosen]
    code-stack:      [chosen]
    site-scale:      [chosen]

  RATIONALE: [1 sentence explaining why these choices fit this image + category]

  Nav position implementation:
    left-sidebar:   fixed left, 240px wide, content ml-60
    right-sidebar:  fixed right, 240px wide, content mr-60
    bottom-bar:     fixed bottom, full width, flex row icon+label tabs, pb-safe
    floating-pill:  fixed top-5, centered, max-w-xl, backdrop-blur glassmorphism
    hamburger-only: no visible links, trigger button top-right, fullscreen overlay

  Hero height implementation:
    banner-short:     h-[clamp(120px,20vh,200px)]
    half-viewport:    h-[50vh] min-h-[400px]
    full-viewport:    h-screen min-h-[600px]
    super-tall:       h-[180vh] (parallax layers scroll through)
    typographic-only: min-h-screen, no images, type fills space

  Scroll implementation:
    snap-sections:       scroll-snap-type y mandatory, each section scroll-snap-align start
    horizontal-sections: flex overflow-x-scroll scroll-snap-type x mandatory, w-screen per section
    sticky-text:         sticky top-0 h-screen on text col, image col scrolls behind

  Motion implementation (Motion for React, formerly Framer Motion, default; GSAP for cinematic):
    static:   no motion calls, instant render, no transition classes
    subtle:   whileInView opacity 0->1, 0.3s ease
    moderate: whileInView opacity+y(24->0), 0.5s, staggerChildren 0.1s
    rich:     parallax hero, counters, stagger 0.15s, hover scale/lift
    cinematic: GSAP ScrollTrigger, timeline per section, scrub, pinning

  Code stack implementation:
    nextjs-ts-tailwind: Next.js 14 App Router + TypeScript + Tailwind + Motion for React
                        Full project: app/, components/, lib/, public/
                        Fonts via next/font/google. Images via next/image.
                        Deploy with `vercel --prod`. Default for all projects.
    react-ts-tailwind:  React 18 + TypeScript via babel CDN + Tailwind CDN
                        Single index.html, no build step required
    html-css-js:        Standalone .html files + tokens.css + vanilla JS
    html-gsap:          GSAP 3 CDN + ScrollTrigger, timeline animations, no framework

----------------------------------------
DESIGN TOOLKIT
----------------------------------------
  Decide which libraries and tools this project needs BEFORE building.
  All tools listed are free and open-source. Select based on motion-level,
  layout-mood, and design complexity. Only include what will actually be used.

  Animation library (pick primary -- must match motion-level):
    motion-react       -- Motion for React, formerly Framer Motion.
                         Install package: `motion`; import from `motion/react`.
                         React declarative, spring physics, layout animations, whileInView,
                         AnimatePresence, gestures, layoutId shared transitions.
                         REQUIRED default for nextjs-ts-tailwind subtle/moderate/rich motion.
    gsap               -- Pro timeline, ScrollTrigger, SplitText, scrub, pinning, morphSVG
                         Best for: cinematic motion level, complex scroll sequences
    motion-one         -- Web Animations API, 3kb, zero dependencies
                         Best for: static or subtle motion on simple sites
    anime-js           -- keyframe timeline, SVG stroke draw, CSS property animation
                         Best for: playful or bold-maximalist mood, icon animations
    auto-animate       -- zero-config layout/list transitions (1 line: useAutoAnimate)
                         Best for: interactive lists, filtering, adding/removing items
    react-spring       -- spring physics, works with 3D (R3F), imperative + declarative
                         Best for: 3D scenes, physics-based UI interactions

  3D library (include only if blueprint has a 3D section or 3D hero):
    react-three-fiber  -- Three.js React renderer, hooks-based, composable
    drei               -- R3F helpers: models, environment, camera, text, effects, MeshReflector
    spline-viewer      -- embed Spline scenes as web component, no Three.js needed
    babylon-js         -- full 3D engine, physics, inspector, GUI, shaders

  Component system (pick one):
    shadcn-ui          -- Radix UI + Tailwind, copy-paste components, WCAG accessible
                         Includes: Button, Card, Badge, Dialog, Tabs, Accordion, Sheet,
                         Dropdown, Tooltip, Popover, Select, Slider, Toggle, Switch
    radix-ui           -- headless primitives only, bring your own styles
    headless-ui        -- Tailwind Labs headless: Listbox, Combobox, Disclosure, Menu
    daisyui            -- Tailwind plugin, semantic components with theme system

  Icon pack (pick 1-2 max):
    lucide-react       -- 1000+ consistent outline icons, tree-shakable, React/Next
    phosphor-icons     -- 6 weights (thin/light/regular/bold/fill/duotone), 1200+ icons
    heroicons          -- Tailwind team, 292 icons, outline + solid variants, React
    tabler-icons       -- 4200+ icons, outline, React + SVG sprite

  Typography effects (pick only if blueprint has text animation):
    splitting-js       -- split text into chars/words/lines for GSAP/Framer targets
    typed-js           -- typewriter effect, multiple strings, loop, cursor
    countup-js         -- animated number counter, easing, prefix/suffix
    react-wrap-balancer -- prevent orphan words in headlines (1-line fix)

  Scroll library:
    lenis              -- smooth inertia scroll, replaces browser scroll, GSAP compatible
                         Use when: motion-level >= moderate
    react-intersection-observer -- IntersectionObserver hook, scroll-triggered React state

  Visual effects (pick only if blueprint calls for them):
    tsparticles        -- configurable particles: snow, bubbles, confetti, network
    canvas-confetti    -- celebration burst, works with any framework
    vanta-js           -- animated 3D backgrounds: waves, birds, net, fog, dots
    react-parallax     -- parallax scrolling component, overlay text, children offset
    three-globe        -- interactive 3D globe, arc animations, hex bin map
    aceternity-ui      -- advanced motion components: moving cards, beam, spotlight

  Carousel and slider:
    embla-carousel     -- minimal, accessible, plugins: autoplay, fade, wheel
    swiper-js          -- feature-rich: coverflow, cube, creative effects, virtual
    keen-slider        -- performant, native-feel, drag, React hooks

  Form handling:
    react-hook-form    -- performant, uncontrolled, minimal re-renders
    zod                -- TypeScript schema validation, paired with RHF

  Data visualization (only for data-heavy or dashboard designs):
    recharts           -- React SVG charts: line, bar, area, pie, radar, scatter
    nivo               -- data viz: bar, line, heatmap, network, sankey, chord
    chart-js           -- canvas-based: 8 chart types, lightweight

  Image handling (built into Next.js):
    next-image         -- automatic optimization, lazy loading, blur placeholder, AVIF/WebP
    react-zoom-pan-pinch -- pinch-to-zoom and pan for galleries/portfolios

  Color and gradient effects:
    chroma-js          -- color manipulation, scales, contrast ratio checks
    CSS mesh-gradient: background: radial-gradient(ellipse at [pos], [hex], transparent)
                       Layered multiple radial-gradients for mesh effect
    CSS animated gradient: @keyframes gradient-shift + background-size: 200% 200%
    tailwind-animate   -- Tailwind plugin: animate-in, fade-in, zoom-in, slide-in-from-*

  Glassmorphism:
    backdrop-filter: blur(12px) saturate(180%); background: rgba([hex], 0.7)
    @supports (backdrop-filter: blur(1px)) -- progressive enhancement

  SELECTED FOR THIS PROJECT:
    animation:    [chosen library]
    components:   [chosen component system]
    icons:        [chosen icon pack(s)]
    scroll:       [lenis / react-intersection-observer / both / none]
    3d:           [chosen 3D library / none]
    effects:      [chosen visual effects / none]
    typography:   [splitting-js / typed-js / react-wrap-balancer / none]
    forms:        [react-hook-form+zod / none]
    extras:       [any additional libraries this specific design needs]

  RATIONALE: [1 sentence: why these tools match the motion-level, layout-mood, and complexity]

  INSTALL COMMAND:
    [exact npm install command listing all selected packages]
    [npx shadcn@latest init  -- if shadcn-ui selected]
    [npx shadcn@latest add button card badge tabs dialog sheet accordion  -- as needed]

----------------------------------------
SECTIONS
----------------------------------------

[1] NAV
  layout:         horizontal, space-between, sticky top
  height:         [px]
  bg:             [color / transparent with backdrop-blur on scroll]
  logo:           left, height [px], [SVG wordmark / icon + text]
  links:          center / right, [N] items, [font], [size]px, color [hex]
  cta-button:     [label], [filled/outlined], bg [hex], text [hex], h [px], px [px], radius [px]
  mobile:         hamburger below [px]px, menu: [slide-in / fullscreen overlay]

[2] HERO
  layout:         [split [%/% left/right] / centered / full-bleed]
  height:         [100vh / [px]px / auto]
  bg:             [color / gradient from [hex] to [hex] [angle]deg / image full-bleed]
  content-col:    [% width if split]
  image-col:      [% width if split]

  headline:
    text:         "[HEADLINE TEXT]"
    font:         [display-font], [weight], [size]px desktop / [size]px mobile
    color:        [hex]
    position:     [left-aligned / centered / bottom-left overlay]
    transform:    [uppercase / none]
    max-width:    [px]
    animation:    [Framer variant / GSAP from spec / none]

  subtext:
    text:         "[SUBTEXT]"
    font:         [body-font], [weight], [size]px, max-width [ch]
    color:        [hex]
    margin-top:   [px]

  cta-primary:
    label:        "[ACTION VERB + NOUN]"
    bg:           [hex], hover: [10% darker]
    text:         [hex]
    height:       [px]
    padding:      [px] [px]
    border-radius:[px]
    margin-top:   [px]

  cta-secondary:
    label:        "[LABEL]"
    style:        [outlined / ghost / text-link with arrow]
    margin-left:  [px]

  hero-asset:
    slot-name:    [hero-illustration / hero-bg / hero-photo / hero-3d]
    type:         [illustration / photograph / 3D render / abstract / particle-bg]
    placement:    [right-column / full-bleed-bg / absolute-right / bottom-center]
    aspect-ratio: [16/9 / 4/3 / 1/1 / 3/4]
    width:        [% or px]
    imagegen-description: "[exact visual description for asset generation]"

[3] [SECTION NAME]
  label:          "[SECTION LABEL]" (uppercase eyebrow tag, 12px, letter-spacing 0.1em)
  layout:         [full-width / 2-col [%/%] / 3-col equal / 4-col / grid [cols x rows] / centered]
  bg:             [hex / --clr-surface / --clr-bg]
  padding:        [px] vertical (multiple of 8)
  headline:       "[TEXT]", [font], [size]px, [color]
  body:           "[TEXT]", [font], [size]px, max-width [ch], [color]
  animation:      [stagger cards / fade-up section / slide-in / none]

  [For each card/component:]
  card:
    width:        [px or 1/N]
    bg:           [hex]
    radius:       [px]
    padding:      [px]
    border:       [px solid hex / none]
    shadow:       [none / sm / md]
    icon:         [Lucide icon name / Phosphor name / custom SVG slot]
    headline:     [size]px, [font], [weight]
    body:         [size]px, [color]
    hover:        [scale(1.02) / translateY(-4px) / border-color change]
    cta:          [label / none]

[4...N] [repeat for every section -- be specific, never vague]

[N] FOOTER
  layout:         full-width, [N]-column grid
  bg:             [hex]
  padding:        [px] top / [px] bottom
  logo:           left column, height [px]
  tagline:        [size]px below logo, [color]
  columns:        [N] link groups, each: [label], [N] links
  social-icons:   [platform list], size [px], color [hex]
  legal:          copyright, [size]px, [color]
  border-top:     [px solid hex / none]

----------------------------------------
ASSET LIST
----------------------------------------
  RULE: Every asset marked [IMAGEGEN] MUST be generated with imagegen before code is
  written. Do NOT substitute SVG drawings, CSS shapes, or placeholder images.
  If imagegen has not been called for that slot, the asset does not exist yet.

  Asset types:
    [IMAGEGEN] -- must be generated via imagegen call, no substitute allowed
    [SVG-HAND] -- hand-crafted SVG (logo and favicon only)
    [ICON]     -- Lucide/Phosphor component name, no image file needed

  Format: slot-name | [IMAGEGEN / SVG-HAND / ICON] | ratio | dimensions | position | prompt

  logo-main | [SVG-HAND] | 4/1 | 160x40px | nav + footer |
    "Draw SVG: [mark description, letterforms, colors, transparent bg]"

  favicon | [SVG-HAND] | 1/1 | 32x32px | browser tab |
    "Simplified logo mark only, square, bold, readable at 16px"

  hero-illustration | [IMAGEGEN] | 4/3 | 600x450px | right column |
    "[Detailed scene: style, subject, colors, mood, no text in image, transparent bg if illustration]"

  [section-img-1] | [IMAGEGEN] | [ratio] | [dimensions] | [position] |
    "[Detailed imagegen prompt -- specific, visual, descriptive. Never vague.]"

  [gallery-1] | [IMAGEGEN] | [ratio] | [dimensions] | gallery grid cell 1 |
    "[imagegen prompt -- consistent style with other gallery images]"

  [repeat for every image asset. Every [IMAGEGEN] slot must have a distinct, detailed prompt.]

  ICON list (not imagegen -- Lucide/Phosphor component names):
    [section] -- [icon-name]: [what it represents]

----------------------------------------
INTERACTIVE ELEMENTS
----------------------------------------
  hamburger-menu:  below [px]px, Motion for React AnimatePresence slide-in,
                   aria-expanded state, body scroll lock when open
  scroll-reveal:   Motion for React whileInView, threshold 0.15, once: true
  pricing-toggle:  monthly/yearly, React useState, swap price values
  dark-mode:       [yes / no], next-themes or CSS class "dark" on html
  smooth-scroll:   Lenis if motion-level >= moderate, else CSS scroll-behavior: smooth
  form:            [page], react-hook-form + zod, loading spinner, success state
  counters:        [section], countup-js or custom useCountUp, trigger on scroll
  carousel:        [section], embla-carousel, touch, [autoplay yes/no]
  accordion:       [section], Radix UI Accordion or shadcn Accordion
  tabs:            [section], Radix UI Tabs or shadcn Tabs
  [other elements specific to this design]

  Animation spec per element (Motion for React / Framer Motion):
    hero-headline:  initial { opacity: 0, y: 60 } animate { opacity: 1, y: 0 }
                    transition { duration: 0.8, ease: [0.16, 1, 0.3, 1] }
    hero-subtext:   delay 0.15s, same pattern
    hero-cta:       delay 0.3s, same pattern
    section-cards:  staggerChildren 0.1s, each card fadeUp
    [add specific animation spec for every animated element]

----------------------------------------
PAGES TO BUILD
----------------------------------------
  / (index)         -- landing page (this blueprint)
  /features         -- [brief purpose]
  /pricing          -- [brief purpose]
  /about            -- [brief purpose]
  /contact          -- [brief purpose]
  not-found         -- on-brand 404 page

========================================
BLUEPRINT COMPLETE
========================================
```

This document is the single source of truth. Every decision is made here. Nothing changes during build.

---

## Step 2b -- Blueprint Summary Card

After writing the full blueprint, output this short card BEFORE generating the imagegen.

```
+------------------------------------------------------------------+
|  BLUEPRINT PREVIEW -- [BRAND NAME]                               |
+------------------------------------------------------------------+
|  "[TAGLINE]"                                                     |
|                                                                  |
|  Category:  [CATEGORY]             Tone:    [TONE]               |
|  Nav:       [NAV STYLE]                                          |
|  Hero:      [HERO STYLE]                                         |
|  Scroll:    [SCROLL BEHAVIOR]      Motion:  [MOTION LEVEL]       |
|  Mood:      [LAYOUT MOOD]          Stack:   [CODE STACK]         |
|                                                                  |
|  Colors:    [PRIMARY] [ACCENT] [BG] [TEXT]                       |
|  Fonts:     [DISPLAY FONT] + [BODY FONT]                         |
|  Toolkit:   [animation] + [components] + [icon pack]             |
|  Effects:   [effects / none]                                     |
|                                                                  |
|  Sections:  [N] -- [comma list of section names]                 |
|  Pages:     [comma list of routes]                               |
|  Assets:    [N] images to generate + [N] icons                   |
|  Deploy:    https://[brand-slug].vercel.app                      |
+------------------------------------------------------------------+
|  Generating landing page visual now...                           |
+------------------------------------------------------------------+
```

Immediately after printing this card, generate the imagegen visual.
Do not wait for user input between the card and the imagegen call.
The user sees both at the same time and confirms both together.

---

## Step 3 -- Generate Imagegen Visual FROM Blueprint

Translate the blueprint into one imagegen prompt. Every element in the visual
was already defined in the blueprint. Nothing is added or invented here.

Build the prompt by reading the blueprint top to bottom:

```
A full-length [CATEGORY] website for "[BRAND NAME]". "[TAGLINE]"

Layout: [NAV STYLE] navigation, [HERO STYLE] hero section, [LAYOUT MOOD] aesthetic mood.

[NAV STYLE NOTE:
  left-sidebar: vertical sidebar panel fixed to left, content pushed right
  bottom-bar: icon tabs fixed at bottom, no top nav visible
  floating-pill: centered capsule nav floating at top with blur background
  hamburger-only: minimal top corner trigger button, no visible links
  top-transparent-blur: full horizontal nav, transparent, no background color]

Full vertical layout top to bottom:

[1] NAV: [exact description from blueprint nav section]
[2] HERO: [describe hero-style exactly -- height, layout, headline position,
     hero asset position, CTA buttons, background. Reference hero-style.]
[3] [SECTION NAME]: [describe layout, bg color, content, card style, asset placement]
[4] [SECTION]: [...]
... [every section in order]
[N] FOOTER: [columns, logo, social links, legal]

Brand colors: [PRIMARY hex], [ACCENT hex], [BG hex], [SURFACE hex], [TEXT hex].
Display font [DISPLAY FONT], [weight], [size]px for headlines.
Body font [BODY FONT] for paragraph text.
Imagery: [imagery style from blueprint].
Mood: [LAYOUT MOOD description -- e.g. editorial large asymmetric type / bold maximalist
      oversized elements / minimal generous whitespace / brutalist exposed grid].
[If motion-level is rich or cinematic: describe UI mid-animation --
 hero headline rising in, cards in stagger offset, parallax layers displaced.]

Website design mockup, full vertical page, all sections visible,
high detail, sharp edges, production-ready UI.
```

Generate the image. Do not proceed to PAUSE until the image is generated.

---

## Step 4 -- PAUSE POINT

Present the visual and a compressed summary:

```
+----------------------------------------------------------+
|  BLUEPRINT LOCKED -- VISUAL READY FOR REVIEW             |
+----------------------------------------------------------+
|  Brand:    [NAME] -- [TAGLINE]                           |
|  Category: [CATEGORY]   |   Tone: [TONE]                 |
|  Colors:   [PRIMARY] [ACCENT] [BG] [TEXT]                |
|  Fonts:    [DISPLAY FONT] + [BODY FONT]                  |
|  Toolkit:  [animation] + [components] + [icons]          |
|  Sections: [N] -- [list names]                           |
|  Pages:    [list all routes]                             |
|  Deploy:   https://[brand-slug].vercel.app               |
+----------------------------------------------------------+
|  Blueprint is locked. Visual is built from it.           |
|  Say GO to generate all assets and build the website.    |
|  Tell me what to change if anything looks off.           |
+----------------------------------------------------------+
```

Wait for the user. Do not generate assets or write code before confirmation.

Valid signals: go / yes / build / next / looks good / perfect / do it / proceed

If the user requests a change -- update the blueprint first, then re-generate the imagegen.
Never re-generate the visual without updating the blueprint first. They must stay in sync.

---

## Step 5 -- Generate All Assets FROM Blueprint

!! THIS STEP IS MANDATORY. DO NOT SKIP. DO NOT SUBSTITUTE. !!

Every [IMAGEGEN] asset in the ASSET LIST must be generated NOW using imagegen,
before a single line of HTML, TSX, or CSS is written.

If you write code before generating imagegen assets, you are violating the core
contract of this skill. The imagegen visual is the source of truth. The code
translates it. Code written without the imagegen is guesswork.

NEVER substitute:
  - Hand-drawn SVG paths for a hero illustration
  - CSS gradient boxes for section images
  - Placeholder divs for product shots
  - Emoji or icon components for decorative art
  - Downloaded stock photo URLs for generated assets

These substitutions are wrong every time, without exception.

**Execution order:**

1. logo-main [SVG-HAND] -- Draw SVG by hand. Mark recognizable at 40px height.
2. favicon [SVG-HAND] -- Simplified mark, 32x32.
3. hero asset [IMAGEGEN] -- Call imagegen now. Use exact prompt from blueprint.
4. [section-img-1] [IMAGEGEN] -- Call imagegen. Use exact prompt.
5. [section-img-2] [IMAGEGEN] -- Call imagegen. Use exact prompt.
6. ... continue for every [IMAGEGEN] slot in the ASSET LIST in order ...
7. [gallery-1] [IMAGEGEN] -- Call imagegen. Same style as other gallery images.
8. [gallery-N] [IMAGEGEN] -- Call imagegen. Consistent with gallery-1.

For each [IMAGEGEN] call:
  - Use the exact prompt from the blueprint ASSET LIST -- do not paraphrase
  - If the result does not match the expected ratio or style, call imagegen again
  - Save the result as /public/assets/[slot-name].[ext]

**Asset checklist (every box must be checked before writing any code):**

```
[ ] logo-main.svg: drawn, mark recognizable at h-10 (40px), transparent bg
[ ] favicon.svg: drawn, reads at 16px
[ ] hero asset: imagegen called, result saved, ratio matches blueprint
[ ] [section-img-1]: imagegen called, result saved
[ ] [section-img-2]: imagegen called, result saved
[ ] [all section images]: imagegen called for every [IMAGEGEN] slot
[ ] [gallery images]: imagegen called for every gallery slot, consistent style
[ ] Total [IMAGEGEN] count called = total [IMAGEGEN] count in ASSET LIST
[ ] All assets visually belong to the same brand system
```

Do not write any code until every box above is checked.

---

## Step 6 -- Build All Pages FROM Blueprint

Default stack: **nextjs-ts-tailwind** unless blueprint specifies otherwise.
For html-css-js or html-gsap stacks: use standalone .html + tokens.css + chosen CDN libraries.
Every decision comes from the blueprint. Nothing invented during build.

---

### 6a -- Scaffold and Install

```bash
npx create-next-app@latest [brand-slug] \
  --typescript --tailwind --eslint --app \
  --src-dir=false --import-alias "@/*"

cd [brand-slug]
```

Install toolkit from the blueprint DESIGN TOOLKIT INSTALL COMMAND:

```bash
# Animation (always for nextjs-ts-tailwind)
# Motion for React is the current package for Framer Motion-style React animations.
npm install motion

# Smooth scroll (if motion-level >= moderate)
npm install lenis

# Icons (from blueprint)
npm install lucide-react
# or: npm install @phosphor-icons/react @tabler-icons/react

# Components (if shadcn-ui selected)
npx shadcn@latest init
npx shadcn@latest add button card badge tabs dialog sheet accordion dropdown-menu tooltip

# GSAP (if motion-level = cinematic)
npm install gsap

# 3D (if blueprint has 3D section)
npm install @react-three/fiber @react-three/drei three

# Visual effects (from blueprint)
# npm install @tsparticles/react @tsparticles/slim
# npm install vanta

# Forms (if blueprint has form)
npm install react-hook-form zod @hookform/resolvers

# Typography effects (if blueprint uses them)
# npm install typed.js react-wrap-balancer

# Tailwind animation plugin
npm install tailwindcss-animate
```

---

### 6b -- Project File Structure

```
[brand-slug]/
  app/
    layout.tsx          -- root layout: fonts, metadata, Nav, Footer, SmoothScroll
    page.tsx            -- homepage: imports all section components in blueprint order
    features/
      page.tsx
    pricing/
      page.tsx
    about/
      page.tsx
    contact/
      page.tsx
    not-found.tsx       -- 404 page, centered, brand-styled
    globals.css         -- design tokens as CSS custom properties + Tailwind base
  components/
    layout/
      Nav.tsx           -- matches nav-style from blueprint exactly
      Footer.tsx        -- matches footer spec from blueprint
      SmoothScroll.tsx  -- Lenis wrapper (client component, no UI)
    sections/
      Hero.tsx          -- matches hero-style from blueprint exactly
      [SectionName].tsx -- one file per section (Features.tsx, Pricing.tsx, etc.)
    ui/                 -- shadcn/ui components (copy-pasted by shadcn CLI)
    effects/
      ParticleBackground.tsx  -- if tsparticles in toolkit
      VantaBackground.tsx     -- if vanta in toolkit
      TypedText.tsx           -- if typed.js in toolkit
  lib/
    tokens.ts           -- design tokens as TypeScript constants
    utils.ts            -- cn() from shadcn (clsx + tailwind-merge)
    animations.ts       -- shared Motion for React variants
  public/
    assets/             -- all generated images, named by slot-name from blueprint
    icons/              -- custom SVG icons not covered by icon pack
  next.config.ts
  tailwind.config.ts
  package.json
  .gitignore
```

---

### 6c -- Design Tokens

**app/globals.css** -- all values from blueprint, zero invented:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --clr-primary:    [hex from blueprint];
  --clr-accent:     [hex from blueprint];
  --clr-bg:         [hex from blueprint];
  --clr-surface:    [hex from blueprint];
  --clr-surface-2:  [hex from blueprint];
  --clr-text:       [hex from blueprint];
  --clr-text-muted: [hex from blueprint];
  --clr-border:     [hex from blueprint];

  --text-hero:  [px from blueprint];
  --text-h1:    [px from blueprint];
  --text-h2:    [px from blueprint];
  --text-h3:    [px from blueprint];
  --text-body:  [px from blueprint];
  --text-sm:    [px from blueprint];
  --text-label: [px from blueprint];

  --container:     [px from blueprint];
  --section-pad-v: [px from blueprint];
  --col-gap:       [px from blueprint];

  --sp-1: 8px;  --sp-2: 16px; --sp-3: 24px; --sp-4: 32px;
  --sp-6: 48px; --sp-8: 64px; --sp-12: 96px; --sp-16: 128px;

  --radius-sm: 4px; --radius-md: 8px;
  --radius-lg: 16px; --radius-full: 9999px;
}

@media (max-width: 767px) {
  :root {
    --text-hero: [mobile px from blueprint];
    --text-h1:   [mobile px from blueprint];
    --text-h2:   [mobile px from blueprint];
    --text-h3:   [mobile px from blueprint];
  }
}

html { background: var(--clr-bg); color: var(--clr-text); }
*, *::before, *::after { box-sizing: border-box; }
```

**lib/tokens.ts** -- same values for TypeScript/Tailwind:

```typescript
export const tokens = {
  colors: {
    primary:   '[hex]',
    accent:    '[hex]',
    bg:        '[hex]',
    surface:   '[hex]',
    surface2:  '[hex]',
    text:      '[hex]',
    textMuted: '[hex]',
    border:    '[hex]',
  },
  fonts: {
    display: '[display-font name]',
    body:    '[body-font name]',
  },
  spacing: {
    container:  '[px]',
    sectionPad: '[px]',
  },
} as const;
```

**tailwind.config.ts** -- extend with blueprint tokens:

```typescript
import type { Config } from 'tailwindcss';
import { tokens } from './lib/tokens';
import animate from 'tailwindcss-animate';

export default {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary:     tokens.colors.primary,
        accent:      tokens.colors.accent,
        bg:          tokens.colors.bg,
        surface:     tokens.colors.surface,
        'surface-2': tokens.colors.surface2,
        'text-main': tokens.colors.text,
        'text-muted':tokens.colors.textMuted,
        border:      tokens.colors.border,
      },
      fontFamily: {
        display: [tokens.fonts.display, 'serif'],
        body:    [tokens.fonts.body,    'sans-serif'],
      },
      maxWidth: { container: tokens.spacing.container },
    },
  },
  plugins: [animate],
} satisfies Config;
```

**app/layout.tsx** -- fonts via next/font, no external stylesheet:

```typescript
import { [DisplayFont], [BodyFont] } from 'next/font/google';
import type { Metadata } from 'next';
import Nav from '@/components/layout/Nav';
import Footer from '@/components/layout/Footer';
import SmoothScroll from '@/components/layout/SmoothScroll';
import './globals.css';

const displayFont = [DisplayFont]({
  subsets: ['latin'],
  weight: ['400', '700'],
  variable: '--font-display',
});
const bodyFont = [BodyFont]({
  subsets: ['latin'],
  weight: ['400', '500', '600'],
  variable: '--font-body',
});

export const metadata: Metadata = {
  title: '[Brand Name] -- [Tagline from blueprint]',
  description: '[Brand description, max 160 chars]',
  openGraph: {
    title: '[Brand Name]',
    description: '[Description]',
    url: 'https://[brand-slug].vercel.app',
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${displayFont.variable} ${bodyFont.variable}`}>
      <body className="bg-bg text-text-main font-body antialiased">
        <a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 z-50">
          Skip to content
        </a>
        <SmoothScroll />
        <Nav />
        <main id="main">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
```

---

### 6d -- Shared Animation Variants (lib/animations.ts)

Write once. Import in every section that animates.

```typescript
import type { Variants } from 'motion/react';

export const fadeUp: Variants = {
  hidden: { opacity: 0, y: 24 },
  show:   { opacity: 1, y: 0, transition: { duration: 0.5, ease: 'easeOut' } },
};

export const fadeIn: Variants = {
  hidden: { opacity: 0 },
  show:   { opacity: 1, transition: { duration: 0.4 } },
};

export const slideLeft: Variants = {
  hidden: { opacity: 0, x: 48 },
  show:   { opacity: 1, x: 0, transition: { duration: 0.6, ease: 'easeOut' } },
};

export const slideRight: Variants = {
  hidden: { opacity: 0, x: -48 },
  show:   { opacity: 1, x: 0, transition: { duration: 0.6, ease: 'easeOut' } },
};

export const scaleIn: Variants = {
  hidden: { opacity: 0, scale: 0.9 },
  show:   { opacity: 1, scale: 1, transition: { duration: 0.4 } },
};

export const stagger: Variants = {
  hidden: {},
  show:   { transition: { staggerChildren: 0.1, delayChildren: 0.05 } },
};

export const staggerSlow: Variants = {
  hidden: {},
  show:   { transition: { staggerChildren: 0.15, delayChildren: 0.1 } },
};

// Standard viewport trigger: 15% visible, animate only once
export const viewport = { once: true, amount: 0.15 } as const;
```

---

### 6e -- Component Patterns

**Smooth scroll (components/layout/SmoothScroll.tsx):**
```typescript
'use client';
import { useEffect } from 'react';
import Lenis from 'lenis';

export default function SmoothScroll() {
  useEffect(() => {
    const lenis = new Lenis({ lerp: 0.1, wheelMultiplier: 0.8 });
    function raf(time: number) { lenis.raf(time); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
    return () => lenis.destroy();
  }, []);
  return null;
}
```

**Animated section (wrap any section component in this):**
```typescript
'use client';
import { motion } from 'motion/react';
import { fadeUp, viewport } from '@/lib/animations';

export function FadeSection({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <motion.section
      initial="hidden"
      whileInView="show"
      viewport={viewport}
      variants={fadeUp}
      className={className}
    >
      {children}
    </motion.section>
  );
}
```

**Staggered card grid:**
```typescript
'use client';
import { motion } from 'motion/react';
import { stagger, fadeUp, viewport } from '@/lib/animations';

export function CardGrid<T>({ items, renderCard }: { items: T[]; renderCard: (item: T) => React.ReactNode }) {
  return (
    <motion.div
      variants={stagger}
      initial="hidden"
      whileInView="show"
      viewport={viewport}
      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      {items.map((item, i) => (
        <motion.div key={i} variants={fadeUp}>
          {renderCard(item)}
        </motion.div>
      ))}
    </motion.div>
  );
}
```

**GSAP ScrollTrigger (cinematic motion-level only):**
```typescript
'use client';
import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

export function CinematicSection({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLElement>(null);
  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo('.reveal-gsap',
        { opacity: 0, y: 80 },
        {
          opacity: 1, y: 0, duration: 1, ease: 'power3.out',
          stagger: 0.12,
          scrollTrigger: { trigger: ref.current, start: 'top 80%' },
        }
      );
    }, ref);
    return () => ctx.revert();
  }, []);
  return <section ref={ref}>{children}</section>;
}
```

**Hamburger nav (Motion for React AnimatePresence):**
```typescript
'use client';
import { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import Link from 'next/link';

const links = ['Features', 'Pricing', 'About', 'Contact'];

export default function Nav() {
  const [open, setOpen] = useState(false);
  return (
    <nav className="fixed top-0 inset-x-0 z-50 h-16 flex items-center px-6
                    backdrop-blur-md bg-bg/80 border-b border-border">
      <Link href="/" className="mr-auto">
        <img src="/assets/logo.svg" alt="[Brand] logo" className="h-10 w-auto" />
      </Link>
      <ul className="hidden md:flex gap-8 text-sm font-medium">
        {links.map(l => (
          <li key={l}><Link href={`/${l.toLowerCase()}`} className="hover:text-accent transition-colors">{l}</Link></li>
        ))}
      </ul>
      <Link href="#cta" className="hidden md:inline-flex ml-8 h-10 px-5 rounded-full
                                   bg-accent text-bg text-sm font-semibold items-center
                                   hover:bg-accent/90 transition-colors">
        [CTA Label]
      </Link>
      <button
        className="md:hidden ml-auto"
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        aria-label="Toggle menu"
      >
        {/* burger icon from Lucide */}
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            className="fixed inset-0 top-16 bg-bg z-40 flex flex-col items-center justify-center gap-8"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.25 }}
          >
            {links.map(l => (
              <Link key={l} href={`/${l.toLowerCase()}`}
                className="text-2xl font-display font-bold hover:text-accent transition-colors"
                onClick={() => setOpen(false)}
              >
                {l}
              </Link>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}
```

**Number counter (stats sections):**
```typescript
'use client';
import { useState, useEffect, useRef } from 'react';

export function CountUp({ end, suffix = '', duration = 2000 }: { end: number; suffix?: string; duration?: number }) {
  const [count, setCount] = useState(0);
  const observed = useRef(false);
  const ref = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting || observed.current) return;
      observed.current = true;
      const start = Date.now();
      const tick = () => {
        const p = Math.min((Date.now() - start) / duration, 1);
        const ease = 1 - Math.pow(1 - p, 3);
        setCount(Math.round(ease * end));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [end, duration]);
  return <span ref={ref}>{count}{suffix}</span>;
}
```

**Typewriter effect (if typed-js in toolkit):**
```typescript
'use client';
import { useEffect, useRef } from 'react';
import Typed from 'typed.js';

export function TypedText({ strings }: { strings: string[] }) {
  const el = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    const typed = new Typed(el.current!, {
      strings,
      typeSpeed: 60,
      backSpeed: 40,
      backDelay: 2000,
      loop: true,
    });
    return () => typed.destroy();
  }, [strings]);
  return <span ref={el} aria-label={strings[0]} />;
}
```

**Particle background (if tsparticles in toolkit):**
```typescript
'use client';
import { useEffect } from 'react';
import { tsParticles } from '@tsparticles/engine';
import { loadSlim } from '@tsparticles/slim';

export function ParticleBackground() {
  useEffect(() => {
    loadSlim(tsParticles).then(() =>
      tsParticles.load({
        id: 'particles',
        options: {
          particles: {
            number: { value: 60 },
            color: { value: '[--clr-accent hex]' },
            opacity: { value: 0.3 },
            size: { value: 2 },
            move: { enable: true, speed: 0.8 },
          },
          interactivity: { events: { onHover: { enable: true, mode: 'repulse' } } },
        },
      })
    );
    return () => { tsParticles.dom().forEach(c => c.destroy()); };
  }, []);
  return <div id="particles" className="absolute inset-0 -z-10 pointer-events-none" />;
}
```

**React Hook Form + Zod (contact/newsletter forms):**
```typescript
'use client';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  name:    z.string().min(2, 'Name required'),
  email:   z.string().email('Valid email required'),
  message: z.string().min(10, 'Message too short'),
});
type Fields = z.infer<typeof schema>;

export function ContactForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting, isSubmitSuccessful } } = useForm<Fields>({
    resolver: zodResolver(schema),
  });
  async function onSubmit(data: Fields) {
    await new Promise(r => setTimeout(r, 1200));
    console.log(data);
  }
  if (isSubmitSuccessful) return (
    <p className="text-accent text-lg font-semibold">You are in. Check your inbox.</p>
  );
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium mb-1">Name</label>
        <input id="name" {...register('name')} className="w-full rounded-lg border border-border bg-surface px-4 py-2" />
        {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name.message}</p>}
      </div>
      <div>
        <label htmlFor="email" className="block text-sm font-medium mb-1">Email</label>
        <input id="email" type="email" {...register('email')} className="w-full rounded-lg border border-border bg-surface px-4 py-2" />
        {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>}
      </div>
      <div>
        <label htmlFor="message" className="block text-sm font-medium mb-1">Message</label>
        <textarea id="message" rows={4} {...register('message')} className="w-full rounded-lg border border-border bg-surface px-4 py-2" />
        {errors.message && <p className="text-red-500 text-sm mt-1">{errors.message.message}</p>}
      </div>
      <button type="submit" disabled={isSubmitting}
        className="h-11 px-6 rounded-full bg-accent text-bg font-semibold hover:bg-accent/90 transition-colors disabled:opacity-60">
        {isSubmitting ? 'Sending...' : 'Send Message'}
      </button>
    </form>
  );
}
```

**All images -- use next/image with blueprint dimensions:**
```typescript
import Image from 'next/image';

// Hero image (above fold -- priority=true)
<Image
  src="/assets/hero-illustration.png"
  alt="[Descriptive text matching imagegen-description from blueprint]"
  width={600}
  height={450}
  priority
  className="object-contain w-full h-auto"
/>

// All other images (lazy by default)
<Image
  src="/assets/[slot-name].png"
  alt="[Descriptive text]"
  width={[width from blueprint]}
  height={[height from blueprint]}
  className="object-cover w-full h-full"
/>
```

---

### 6f -- UI/UX Design Principles (Applied Silently During Every Build)

These are applied automatically to every component. Never mentioned unless user asks.

**Visual hierarchy:**
- One dominant element per section -- size OR color, never both simultaneously
- Hero headline: largest text on the page, display-font, tight line-height 1.05-1.15
- CTAs: highest contrast element in their section, never compete with headline
- Weight 400 for body, 600 for labels, 700+ for headings -- weight creates hierarchy

**Typographic scale (Perfect Fourth 1.333x ratio):**
- hero: 72px -> h1: 54px -> h2: 40px -> h3: 30px -> body: 18px -> small: 14px
- Adjust for brand tone: luxury gets tighter scale, bold-maximalist gets wider
- Headings: letter-spacing -0.02em to -0.04em (tighter = more editorial)
- Labels: uppercase, letter-spacing 0.1-0.15em, weight 600, size 11-12px
- Body text: line-height 1.65-1.75, max-width 65ch, never below 16px on mobile

**8px spacing grid (all values must be multiples of 8):**
- Section vertical padding: 96-128px desktop / 64-80px mobile
- Card inner padding: 24px or 32px
- Grid gap between cards: 24px or 32px
- Stack spacing (label -> headline -> subtext -> cta): 8px / 16px / 32px

**60/30/10 color rule:**
- 60% background (--clr-bg) fills most of the page
- 30% surface (--clr-surface) for cards, sidebars, subtle sections
- 10% accent (--clr-accent) for CTAs, highlights, hover states, key stats
- WCAG AA contrast: body text >= 4.5:1 on its background
- WCAG AA contrast: large text (18px+ bold or 24px+) >= 3:1
- Hover states: 10% shade/tint of current color, never a completely different hue
- Never use color alone to convey meaning -- always add shape/text/icon change

**Composition and layout:**
- F-pattern (info-dense): critical info top-left, subtext below, features down left side
- Z-pattern (minimal): logo top-left, nav top-right, CTA bottom-right diagonal
- Asymmetric layouts: dominant side 65-70%, supporting side 30-35%
- Cards in a grid: identical height, identical radius, identical shadow level
- Whitespace is emphasis -- more space around a CTA makes it more prominent
- Section alternation: vary bg between --clr-bg and --clr-surface to create rhythm

**Conversion-optimized patterns:**
- Primary CTA visible above the fold without scrolling (always in hero)
- Repeat CTA at the end of every major content section
- Social proof (logos, counts, testimonials) placed directly before or after primary CTA
- Button labels: action verb + object ("Start building", "Get early access", "See all plans")
- Lead capture: name + email is enough, never add fields users will resent
- Friction reducers: "No credit card required" / "Cancel anytime" below paid CTAs
- Trust signals: company logos, review counts, certifications near signup

**Accessibility (WCAG 2.1 AA -- non-negotiable):**
- Skip link first in body: `<a href="#main" class="sr-only focus:not-sr-only">`
- All visible images: descriptive alt text (describe what the image shows, not "image of")
- Icon-only buttons: aria-label describing the action
- Toggles (hamburger, pricing, dark mode): aria-expanded={open}
- Focus rings: visible on all interactive elements -- `outline: 2px solid var(--clr-accent); outline-offset: 2px`
- Form inputs: always a visible `<label>`, not just placeholder text
- Tab order: logical document order, no positive tabindex

**Next.js performance:**
- Hero image: `priority` prop (loads immediately, never lazy)
- All other images: next/image default (lazy loaded automatically)
- Fonts: `next/font/google` only -- no `<link>` to fonts.googleapis.com
- Third-party scripts: `<Script strategy="lazyOnload">` via next/script
- Avoid `'use client'` on layout.tsx and page.tsx -- use it only on interactive leaf components
- Dynamic imports for heavy effects: `dynamic(() => import('./effects/Particles'), { ssr: false })`

---

### 6g -- Build Checklist (Per Page, Mandatory Before Moving to Next)

```
IMAGEGEN VERIFICATION (check first, before anything else):
  [ ] Every [IMAGEGEN] slot in ASSET LIST has a generated image saved in /public/assets/
  [ ] Hero image is a generated imagegen asset (NOT an SVG drawing or CSS gradient)
  [ ] All section images are generated imagegen assets (NOT SVG, NOT placeholder)
  [ ] All gallery images are generated imagegen assets
  [ ] The only SVG files are logo-main.svg and favicon.svg
  [ ] No <div> with a background-color is standing in for an image
  [ ] No <img src="placeholder..."> or external stock URL in place of imagegen asset
  [ ] Count of next/image calls in code = count of [IMAGEGEN] slots in blueprint

STRUCTURE:
  [ ] All sections present in exact blueprint order
  [ ] All asset slots filled with their generated imagegen image (no placeholder divs)
  [ ] No hardcoded hex -- all colors via Tailwind classes or CSS custom properties
  [ ] Fonts loaded via next/font/google in layout.tsx

COMPONENTS:
  [ ] Nav: all links, CTA button, hamburger trigger, correct nav-style
  [ ] Hamburger: AnimatePresence, aria-expanded, body scroll lock
  [ ] All CTA buttons: valid href, correct style from blueprint
  [ ] Pricing toggle: React state swap (if in blueprint)
  [ ] Dark mode: next-themes or class toggle (if in blueprint)
  [ ] Forms: react-hook-form + zod + loading state + success state (if in blueprint)
  [ ] Accordions: Radix Accordion or shadcn, one open at a time (if in blueprint)
  [ ] Carousels: embla-carousel, touch-enabled (if in blueprint)

IMAGES:
  [ ] All images: next/image with width + height from blueprint
  [ ] All alt attributes: descriptive text, never empty
  [ ] Hero image: priority prop set
  [ ] All images below fold: default lazy loading

ANIMATION:
  [ ] Shared variants imported from lib/animations.ts
  [ ] whileInView + viewport once on all section components
  [ ] Stagger applied to all card/list grids
  [ ] Hover effects on all interactive cards and buttons
  [ ] Motion removed entirely for static motion-level

ACCESSIBILITY:
  [ ] Skip link in layout.tsx
  [ ] All icon-only buttons have aria-label
  [ ] All toggles have aria-expanded
  [ ] Focus rings visible in tab order
  [ ] Form inputs have visible <label>

SEO:
  [ ] metadata export in layout.tsx or page.tsx: title, description, openGraph
  [ ] canonical URL included
  [ ] Viewport meta present (auto in Next.js App Router)

RESPONSIVE:
  375px mobile:
    [ ] Hamburger visible (block md:hidden), desktop nav hidden (hidden md:flex)
    [ ] Hero: single column, font >= mobile scale from blueprint
    [ ] All grids: grid-cols-1 on mobile
    [ ] No horizontal overflow (body overflow-x-hidden)
    [ ] Tap targets: min h-11 (44px) on all buttons and links
    [ ] No font-size below 14px

  768px tablet:
    [ ] Nav compact or hamburger (md: breakpoint)
    [ ] 2-col grids active (md:grid-cols-2)
    [ ] Hero: image visible alongside text

  1024px laptop:
    [ ] Full nav visible (md:flex)
    [ ] 3-col grids active (lg:grid-cols-3)
    [ ] max-w-container enforced on all sections (mx-auto max-w-container)

  1440px desktop:
    [ ] Container max-width from blueprint enforced
    [ ] No content beyond container
    [ ] Layout matches blueprint section specs exactly
```

---

### 6h -- Inner Pages (Same Blueprint-First Process)

For each route in the blueprint PAGES list:

**1. Write the inner page section spec (extend the main blueprint):**

/features page spec:
```
PAGE: /features
Sections:
  PAGE-HERO:  headline "[Features headline]", subtext, bg --clr-surface
  FEATURES-ALTERNATING: rows alternating dark/light, image + text pairs
    each row: slot-name | ratio | imagegen-prompt
  COMPARISON-TABLE: [Brand] vs [Comp A] vs [Comp B], feature rows, Lucide Check/X
  DEMO-PREVIEW: full-width next/image, caption, rounded-xl overflow-hidden
  PAGE-CTA: same CTA section as landing page (reuse component)
```

/pricing page spec:
```
PAGE: /pricing
Sections:
  PAGE-HERO: "Choose Your Plan", shadcn Tabs for monthly/yearly
  PRICING-CARDS: 3-col grid, shadcn Card
    tier-1: [name], $[price]/mo, [N] features, [CTA], bg surface
    tier-2: [name FEATURED], $[price]/mo, [N] features, [CTA], bg primary, ring accent
    tier-3: [name], $[price]/mo, [N] features, [CTA], bg surface
  FAQ: shadcn Accordion, [N] questions, one open at a time
  PAGE-CTA: same CTA section (reuse component)
```

/about page spec:
```
PAGE: /about
Sections:
  PAGE-HERO: mission headline, full-bleed or muted bg
  STORY: 2-col 50/50, text left, next/image right, slot: about-photo | 4/3
  VALUES: 3-col cards, icon-name from blueprint + headline + body
  TEAM: grid [N]-col, card: next/image (slot: team-N | 1/1, rounded-full) + name + role
  TIMELINE: horizontal or vertical, [N] milestones, line connector
```

/contact page spec:
```
PAGE: /contact
Sections:
  PAGE-HERO: minimal "Get in Touch" headline, muted bg
  CONTACT-SPLIT: 2-col 55/45
    left: ContactForm component (react-hook-form + zod)
    right: address, email, hours, social icon links
  MAP: 400px height, bg --clr-surface, centered location icon (or MapLibre embed)
```

not-found.tsx spec:
```
PAGE: not-found (Next.js not-found.tsx, auto-rendered on 404)
  min-h-screen flex flex-col items-center justify-center
  "404" -- font-display text-[180px] leading-none text-primary
  headline: "Page not found."
  subtext: "[brand-voice friendly message]"
  cta: <Link href="/">Back to Home</Link> -- bg-accent text-bg button
  bg: bg-bg
```

**2. Generate imagegen visual for that page FROM its spec.**
**3. Build the page.tsx or not-found.tsx from the spec.**
**4. Run the full build checklist and responsive checklist.**

---

## Step 7 -- File Delivery

Final project structure:

```
[brand-slug]/
  app/
    layout.tsx
    page.tsx              -- homepage
    globals.css
    features/page.tsx
    pricing/page.tsx
    about/page.tsx
    contact/page.tsx
    not-found.tsx
  components/
    layout/
      Nav.tsx
      Footer.tsx
      SmoothScroll.tsx
    sections/
      Hero.tsx
      [SectionName].tsx   -- one file per section
    effects/              -- particle, vanta, typed (if in toolkit)
    ui/                   -- shadcn components
  lib/
    tokens.ts
    utils.ts
    animations.ts
  public/
    assets/
      logo.svg
      logo.png
      favicon.png
      hero.[ext]
      [all slot-name images from blueprint]
    icons/                -- custom SVG icons
  next.config.ts
  tailwind.config.ts
  package.json
  .gitignore
```

---

## Step 8 -- Fidelity Verification (per page, mandatory)

After building each page, compare the output against the imagegen visual.
Not optional. Every gap found must be fixed before moving to the next page.

**Section-by-section fidelity check:**

```
NAV:
  [ ] Logo mark matches imagegen at nav size (40px height)?
      -- If SVG looks like a blob: redraw paths to match the imagegen mark
      -- Common fix: icon not recognizable, text too large for viewBox
  [ ] Logo stacking correct (side-by-side vs stacked)?
  [ ] Nav link count and labels match?
  [ ] CTA button style (filled/outlined/color/radius) matches?
  [ ] Nav position correct (top/left/bottom/floating)?

HERO:
  [ ] Hero height matches (banner/half/full/super-tall)?
  [ ] Content position matches (bottom-left/centered/split)?
  [ ] Headline text size proportional to imagegen?
  [ ] Hero image/illustration in correct slot?
  [ ] CTA buttons positioned correctly below headline?
  [ ] Eyebrow label present and styled?
  [ ] LEFT MARGIN: content has proper mx-auto max-w-container, not flush to edge?
      -- Fix: ensure hero section uses `<div class="mx-auto max-w-container px-4">`
      --      not a raw div with no container constraint

EACH SECTION:
  [ ] Background color matches imagegen (bg-surface vs bg-bg)?
  [ ] Layout matches (2-col / 3-col / centered / grid)?
  [ ] Section images in correct position with correct aspect ratio?
  [ ] Card style (border / no border / dark / light / radius) matches?
  [ ] Icons match chosen icon pack names visible in imagegen?
  [ ] Typography weight and size proportionally correct?

FOOTER:
  [ ] Column count matches imagegen?
  [ ] Logo at correct size in footer?
  [ ] Social icons match platforms shown?
```

**Common gaps and fixes:**

| Gap | Cause | Fix |
|---|---|---|
| Hero text flush to edge | Missing container wrapper | Add mx-auto max-w-container px-4 div |
| Logo wrong shape | SVG paths are blobs | Redraw SVG paths to match imagegen mark |
| Logo too wide in nav | viewBox too landscape | Tighten viewBox, reduce mark canvas |
| Wrong section bg | Wrong Tailwind class | Check bg-surface vs bg-bg vs bg-surface-2 |
| Card borders missing | border class missing | Add border border-border class to card |
| Image wrong ratio | Missing aspect class | Add aspect-video or aspect-[4/3] class |
| Font not rendering | Variable class missing | Ensure font-display or font-body class on element |
| Section extra content | Content invented during build | Strip back to exactly what imagegen shows |

**Logo SVG fidelity:**
- Must be recognizable at height:40px
- Render the SVG in isolation at h-10 -- is the mark clear?
- Organic mark (animal, object): smooth bezier curves, not spiky straight lines
- viewBox aspect ratio should match intended render (roughly 3:1 for icon+text logo)
- Letter-spacing must not push text outside the viewBox -- always verify

Fix gaps immediately. Do not move to next page with known issues.

---

## Step 9 -- Deploy to Vercel

After all pages pass fidelity verification, deploy.

The brand-slug is from the blueprint BRAND slug field.
Example: "Volt Claw" -> slug "volt-claw" -> https://volt-claw.vercel.app

```bash
cd [brand-slug]

# Install CLI if not present
npm install -g vercel
vercel login

# Deploy to production
vercel --prod
```

Vercel CLI prompts:
- Set up and deploy: Y
- Which scope: (select user account)
- Link to existing project: N (first deploy)
- Project name: [brand-slug]
- Directory: ./
- Override settings: N (Next.js auto-detected)

No vercel.json needed for standard Next.js projects.

After deploy succeeds, print:

```
+------------------------------------------------------------------+
|  [BRAND NAME] IS LIVE                                            |
+------------------------------------------------------------------+
|  URL:     https://[brand-slug].vercel.app                        |
|  Stack:   [code-stack from blueprint]                            |
|  Pages:   [N] pages deployed                                     |
|  Assets:  [N] images generated                                   |
|  Toolkit: [animation] + [components] + [icons]                   |
+------------------------------------------------------------------+
|  Website is live. Redeploy anytime with: vercel --prod           |
|  Add env vars at: vercel.com/[account]/[brand-slug]/settings     |
+------------------------------------------------------------------+
```

---

## Rules That Cannot Be Broken

1. Blueprint is written BEFORE imagegen is called. No exceptions.
2. Imagegen is called BEFORE any code is written. No exceptions.
3. All code values come from the blueprint. If a value is not in the blueprint, add it to the blueprint first, then use it.
4. No hardcoded hex in any file -- all colors via Tailwind config extending blueprint tokens or CSS custom properties.
5. No placeholder divs -- every image slot is filled with a generated asset via next/image.
6. No blank alt attributes on any visible image. Alt text describes what the image shows.
7. No emoji or decorative characters used as icons -- Lucide, Phosphor, Heroicons, Tabler, or generated SVG only.
8. Every interactive element in the blueprint must be functionally implemented -- not mocked or faked.
9. Every inner page gets its own imagegen visual generated FROM its blueprint spec before any code is written.
10. Blueprint and imagegen visual must always be in sync -- if the visual changes, the blueprint changes first.
11. Default stack is Next.js 14 App Router + TypeScript + Tailwind + Motion for React (formerly Framer Motion). Only switch stacks if the blueprint explicitly calls for it based on project type.
12. Every project deploys to Vercel at https://[brand-slug].vercel.app as the mandatory final step.
13. Every [IMAGEGEN] asset in the ASSET LIST MUST be generated via imagegen before any code is written. SVG drawings, CSS shapes, placeholder divs, and external stock URLs are NEVER acceptable substitutes. The only hand-crafted files are logo-main.svg and favicon.svg.
14. The total count of imagegen calls made MUST equal the total count of [IMAGEGEN] slots in the blueprint ASSET LIST. If they do not match, assets are missing and build must not proceed.
