---
name: react-bits
description: "Catalog + task router for React Bits — 130 open-source animated, interactive, fully customizable React components (DavidHDev/react-bits, 38k★). Use when user wants animated React UI: animated text (blur, shiny, decrypt, split, scroll-reveal), interactive animations (cursor effects, click spark, magnet, splash), shader/canvas backgrounds (aurora, galaxy, particles, liquid chrome, prism), or polished components (dock, card swap, magic bento, tilted card, glass surface). Maps design briefs to the right component + shadcn/jsrepo install command + required deps."
---

# React Bits — Animated Component Catalog

## What it is

**React Bits** (github.com/DavidHDev/react-bits, 38k★, MIT + Commons Clause, reactbits.dev) — 130 animated, interactive, fully customizable React components for building memorable websites. Four source variants per component: **JS-CSS, JS-TW, TS-CSS, TS-TW**.

Not a runtime npm dependency — components are copied into the user's project via shadcn-style CLI (like shadcn/ui, magicui, aceternity-ui). Each component owns its imports.

## Install pattern

```bash
# Primary: shadcn CLI (preferred)
npx shadcn@latest add @react-bits/<ComponentName>-<VARIANT>

# Variants:
#   -JS-CSS     → plain CSS, JavaScript
#   -JS-TW      → Tailwind CSS, JavaScript
#   -TS-CSS     → plain CSS, TypeScript
#   -TS-TW      → Tailwind CSS, TypeScript  (recommended for modern projects)

# Examples:
npx shadcn@latest add @react-bits/BlurText-TS-TW
npx shadcn@latest add @react-bits/Galaxy-TS-TW
npx shadcn@latest add @react-bits/Dock-TS-TW

# Alternate: jsrepo
# Alternate: copy source manually from reactbits.dev/<category>/<Component>
```

Pick `TS-TW` unless the user's project is JS-only or CSS-first. After install, check component's import block for required peer deps.

## Dependency map (install only what each component needs)

| Dep family | Required for | npm install |
|------------|-------------|-------------|
| `motion` (Framer Motion v12) | Most text + ui animations | `npm i motion` |
| `gsap` + `@gsap/react` | Scroll-based text effects (ScrollFloat, ScrollVelocity, SplitText variants) | `npm i gsap @gsap/react` |
| `three` + `@react-three/fiber` + `@react-three/drei` + `@react-three/postprocessing` | 3D scenes (Ballpit, ModelViewer, FluidGlass, Galaxy, Prism, PrismaticBurst) | `npm i three @react-three/fiber @react-three/drei @react-three/postprocessing` |
| `@react-three/rapier` | Physics 3D (Ballpit, Antigravity) | `npm i @react-three/rapier` |
| `ogl` | Lightweight WebGL backgrounds (Balatro, Beams, Dither, DotField, many others) | `npm i ogl` |
| `matter-js` | 2D physics (FallingText) | `npm i matter-js` |
| `meshline` | Line-based 3D (Threads, Ribbons) | `npm i meshline` |
| `lenis` | Smooth scroll integrations | `npm i lenis` |
| `postprocessing` | Shader bloom/glow (some backgrounds) | `npm i postprocessing` |
| `@use-gesture/react` | Gesture-driven interactions (TiltedCard, Carousel) | `npm i @use-gesture/react` |
| `react-confetti` | Confetti overlays | `npm i react-confetti` |

Default stack for 80% of cases: `motion` + `gsap` + Tailwind. Add three/ogl/rapier per-component when a 3D/shader background is used.

## Full catalog (130 components)

### Text Animations (23) — `reactbits.dev/text-animations/<Name>`

`ASCIIText`, `BlurText`, `CircularText`, `CountUp`, `CurvedLoop`, `DecryptedText`, `FallingText`, `FuzzyText`, `GlitchText`, `GradientText`, `RotatingText`, `ScrambledText`, `ScrollFloat`, `ScrollReveal`, `ScrollVelocity`, `ShinyText`, `Shuffle`, `SplitText`, `TextCursor`, `TextPressure`, `TextType`, `TrueFocus`, `VariableProximity`

### Animations (29) — `reactbits.dev/animations/<Name>`

`AnimatedContent`, `Antigravity`, `BlobCursor`, `ClickSpark`, `Crosshair`, `Cubes`, `ElectricBorder`, `FadeContent`, `GhostCursor`, `GlareHover`, `GradualBlur`, `ImageTrail`, `LaserFlow`, `LogoLoop`, `MagicRings`, `Magnet`, `MagnetLines`, `MetaBalls`, `MetallicPaint`, `Noise`, `OrbitImages`, `PixelTrail`, `PixelTransition`, `Ribbons`, `ShapeBlur`, `SplashCursor`, `StarBorder`, `StickerPeel`, `TargetCursor`

### Backgrounds (42) — `reactbits.dev/backgrounds/<Name>`

`Aurora`, `Balatro`, `Ballpit`, `Beams`, `ColorBends`, `DarkVeil`, `Dither`, `DotField`, `DotGrid`, `EvilEye`, `FaultyTerminal`, `FloatingLines`, `Galaxy`, `GradientBlinds`, `Grainient`, `GridDistortion`, `GridMotion`, `GridScan`, `Hyperspeed`, `Iridescence`, `LetterGlitch`, `Lightning`, `LightPillar`, `LightRays`, `LineWaves`, `LiquidChrome`, `LiquidEther`, `Orb`, `Particles`, `PixelBlast`, `PixelSnow`, `Plasma`, `PlasmaWave`, `Prism`, `PrismaticBurst`, `Radar`, `RippleGrid`, `ShapeGrid`, `Silk`, `SoftAurora`, `Threads`, `Waves`

### Components (36) — `reactbits.dev/components/<Name>`

`AnimatedList`, `BorderGlow`, `BounceCards`, `BubbleMenu`, `CardNav`, `CardSwap`, `Carousel`, `ChromaGrid`, `CircularGallery`, `Counter`, `DecayCard`, `Dock`, `DomeGallery`, `ElasticSlider`, `FlowingMenu`, `FluidGlass`, `FlyingPosters`, `Folder`, `GlassIcons`, `GlassSurface`, `GooeyNav`, `InfiniteMenu`, `Lanyard`, `MagicBento`, `Masonry`, `ModelViewer`, `PillNav`, `PixelCard`, `ProfileCard`, `ReflectiveCard`, `ScrollStack`, `SpotlightCard`, `Stack`, `StaggeredMenu`, `Stepper`, `TiltedCard`

## Design brief → component routing

Match the user's ask to the minimum component set. Don't spray — pick ONE per role (one hero background, one headline text animation, one primary CTA treatment).

### Hero-section patterns

| Intent | Background | Headline | Supporting |
|--------|------------|----------|------------|
| AI / dev tool, luminous | `Aurora`, `Galaxy`, `Silk`, `Plasma` | `BlurText`, `ShinyText`, `GradientText` | `SplashCursor`, `ClickSpark` |
| SaaS analytics, architectural | `Beams`, `DotField`, `DotGrid`, `Dither` | `SplitText`, `TextType`, `ScrollReveal` | `GradualBlur` frame |
| Editorial / typographic hero | no bg / `SoftAurora` / `Grainient` | `TextPressure`, `VariableProximity`, `ScrambledText` | minimal |
| Consumer / energetic | `Balatro`, `Iridescence`, `PrismaticBurst`, `LiquidChrome` | `GlitchText`, `RotatingText`, `TextType` | `ImageTrail`, `PixelTrail` |
| Developer CLI / brutalist | `FaultyTerminal`, `LetterGlitch`, `GridScan`, `Hyperspeed` | `DecryptedText`, `ScrambledText`, `ASCIIText` | `Crosshair` cursor |
| 3D product showcase | `Particles`, `Ballpit`, `Prism` | `BlurText`, `ShinyText` | `ModelViewer`, `FluidGlass` |

### UI element patterns

| Need | Component |
|------|-----------|
| macOS-style launcher dock | `Dock` |
| Portfolio card stack / deck | `CardSwap`, `Stack`, `BounceCards`, `FlyingPosters` |
| Feature grid w/ glow | `MagicBento`, `SpotlightCard`, `BorderGlow` |
| 3D-feeling hover card | `TiltedCard`, `DecayCard`, `ReflectiveCard` |
| Image gallery (circular) | `CircularGallery`, `DomeGallery`, `InfiniteMenu` |
| Masonry / pinterest grid | `Masonry` |
| Pricing tier picker | `ElasticSlider`, `Stepper` |
| Multi-step onboarding | `Stepper`, `AnimatedList` |
| Navigation | `CardNav`, `PillNav`, `StaggeredMenu`, `BubbleMenu`, `FlowingMenu`, `GooeyNav` |
| Team / profile | `ProfileCard`, `GlassIcons`, `GlassSurface` |
| Number counter (KPI) | `CountUp`, `Counter` |
| Scroll-linked timeline | `ScrollStack`, `ScrollFloat`, `ScrollReveal`, `ScrollVelocity` |
| Marquee / logo strip | `LogoLoop` |
| Cursor (custom) | `SplashCursor`, `TargetCursor`, `GhostCursor`, `BlobCursor`, `TextCursor`, `Crosshair` |

### When NOT to use react-bits

- **Design systems for enterprise dashboards** → use the `interface-design` skill + plain Tailwind primitives; animations should be restrained.
- **Brand-first design language (tokens, palette, typography scales)** → use `hue` first to generate the design system, then layer react-bits components INTO it.
- **Accessibility-critical flows** — several components use canvas/WebGL and lack ARIA semantics. For forms, tables, a11y-required UI, stick to shadcn/ui primitives and only sprinkle react-bits for hero/marketing surfaces.
- **SSR-sensitive pages** — some three.js / OGL / face-api components need client-only rendering. Wrap in `'use client'` (Next.js App Router) or lazy-import with `ssr: false`.

## Integration checklist

When the user adds a react-bits component:

1. **Pick the right variant**: `TS-TW` for modern stacks; `JS-CSS` only if the project is JS + CSS modules.
2. **Run `npx shadcn@latest add @react-bits/<Component>-<VARIANT>`** — the CLI writes source into the project's components dir.
3. **Check the component's import block** and install the listed peer deps (see dependency map above).
4. **For three.js / OGL / face-api components** in Next.js: mark the parent as `'use client'` or lazy-load with `next/dynamic({ ssr: false })`.
5. **Respect `prefers-reduced-motion`** — most components animate by default; add a wrapper that disables motion for a11y-sensitive users.
6. **Performance-test 3D/shader components** on target devices. Stack 2+ canvas backgrounds at your own risk — each one costs GPU.

## Relationship to other skills

- `hue` — generates brand-specific design language (tokens, hero-stage presets). Run `hue` FIRST for a new brand, then pick react-bits components that fit the brand's declared hero preset.
- `impeccable-design` / `impeccable-audit` / `impeccable-polish` — craft layer for UI. Use react-bits components as primitives; impeccable-* for spacing/typography/polish.
- `interface-design` — dashboards, admin panels. React-bits is generally NOT the right choice here; the interface-design skill steers toward restrained Tailwind primitives.
- `frontend-design`, `aidesigner-frontend` — generative UI. Can reference react-bits components in their output.
- `baseline-ui` — animation-duration and a11y sanity checks. Run AFTER adding a react-bits component.
- `fixing-motion-performance` — when the canvas backgrounds tank Lighthouse.

## Rules for Claude

1. When the user describes a visual brief, propose the **minimum** set of components from the tables above. Don't stack 3 animated backgrounds.
2. Always cite the exact component name and the `npx shadcn@latest add @react-bits/<Name>-TS-TW` command.
3. Flag required peer deps so the user doesn't hit an install and then immediately hit a missing-module error.
4. For Next.js projects, always mention the `'use client'` / `ssr: false` caveat for three/OGL/face-api components.
5. When a brand-first design is in progress (user is running `hue` or an `interface-design` flow), let that skill lead; react-bits is a component source, not a design authority.
6. Link to `reactbits.dev/<category>/<Component>` for live previews — always more useful than a text description.

## Source

- Repo: https://github.com/DavidHDev/react-bits
- Docs / live previews: https://reactbits.dev
- Vue port: https://vue-bits.dev
- License: MIT + Commons Clause (free for personal and commercial use)
- Last catalog sync: 2026-04-16 (130 components enumerated from `src/content/{TextAnimations,Animations,Backgrounds,Components}/`)
