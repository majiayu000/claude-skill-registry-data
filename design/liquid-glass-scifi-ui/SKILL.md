---
name: liquid-glass-scifi-ui
description: Transform any frontend project (HTML/CSS/JS, React, Vue, Next.js, Tailwind, 3D WebGL/Cesium/Three.js workbenches, or dashboards) into an authentic Apple Liquid Glass + Sci-Fi high-tech interface. Use when the user asks to apply liquid glass, Apple glassmorphism, futuristic sci-fi HUD styling, optical SVG refraction (feDisplacementMap), cursor-tracking border glow, or Uiverse tactile switches and lens buttons to a web app.
---

# Liquid Glass + Sci-Fi UI Transformation Workflow

A complete, stack-agnostic workflow and toolkit that enables an agent to transform any existing web interface into an **authentic Apple Liquid Glass (SDF optical refraction + opposing meniscus specular bevels) + Sci-Fi High-Tech UI** without breaking existing DOM contracts, layout geometry, or business logic.

## When to Use

- The user wants to redesign, restyle, or upgrade a frontend project into **Apple Liquid Glass (液态玻璃)**, **Sci-Fi HUD / Digital Twin workbench (科幻/数字孪生工作台)**, or **high-translucency crystal UI**.
- An existing glassmorphism UI looks **chalky/milky white (发白/起雾)**, **overly dark/muddy (死黑不通透)**, or has **inconsistent internal controls (控件风格割裂)**.
- The user wants tactile micro-interactions inspired by **Uiverse** (squish-and-stretch droplet switches, 45-degree specular shimmer lens buttons, cursor-tracking masked border spotlights) and sci-fi telemetry feedback.

## Bundled Resources

Load these resources from this skill package and copy or adapt them into the target project:

- `assets/design-tokens.json` - Optical parameters, 4-tier glass color/alpha matrices, meniscus shadow recipes, and unified control metrics.
- `assets/component-mapping-matrix.json` - Rules for mapping any project's existing UI components (navbars, drawers, cards, inputs, selects, tables, charts, 3D canvas overlays) to the Liquid Glass hierarchy.
- `assets/liquid-glass-core.css` - Drop-in stylesheet providing CSS variables, 6-layer opposing meniscus bevels, `-webkit-mask-composite: xor` cursor border spotlights, Uiverse droplet switches, and unified 34px form controls.
- `scripts/liquid-glass-engine.js` - Zero-dependency runtime that generates real-time Signed Distance Field (`roundedRectSDF` + `smoothStep`) RGBA displacement maps on an offscreen `<canvas>`, mounts `<svg><filter><feDisplacementMap>` defs, tracks cursor proximity (`--mx`, `--my`), and provides optional Web Audio sci-fi micro-sound synthesis.
- `scripts/audit-liquid-glass.js` - Automated static and optical QA script that detects milky white fills, excessive Gaussian blur, control height mismatches, and fixed-element collisions.

## Why Standard CSS Glassmorphism Fails (Core Optical Principles)

Before writing any CSS, internalize these three optical rules proven in production:

1. **Never use heavy Gaussian blur (`blur(16px-30px)`) as the primary glass effect**:
   - Heavy blur destroys background edges and turns maps, 3D scenes, or wallpapers into a flat, muddy soup.
   - Authentic Liquid Glass pairs **real SVG pixel displacement (`url(#vge-lg-...)`)** with a **low crystal blur (`blur(2px)` to `blur(4px)`)** plus `contrast(1.18) brightness(0.92) saturate(1.28)`. Low blur preserves recognizable background edges so the curved glass bezel visibly bends and refracts them, while `contrast(1.18) brightness(0.92)` crushes milky midtone haze.
2. **Ban diffuse white fills (`rgba(255, 255, 255, 0.08+)` is the enemy)**:
   - Filling panels, cards, or secondary buttons with semi-transparent white over bright or midtone backgrounds acts like white chalk paint, making the entire UI look foggy and washed out.
   - Use **zero-white dark crystal tints (`rgba(4, 12, 24, 0.28-0.44)`)** for the body, and concentrate 100% of the white/cyan brilliance into **opposing diagonal `inset` meniscus rim shadows**.
3. **Strict Control Unification**:
   - Every text input, number input, and custom dropdown trigger in a panel must share the exact same height (`34px`), border radius (`8px`), and dark optical recess fill (`rgba(2, 8, 18, 0.42)`).
   - Limit buttons to **two clean optical tiers**: **Primary Sapphire-Cyan Lens** and **Secondary Smoked-Crystal Lens** (destructive buttons remain neutral crystal at rest and reveal coral-rose glow only on `:hover`).

## Step-by-Step Adaptation Workflow

### Phase 1: Project Reconnaissance & Background Luminance Tuning

1. **Inventory the target project**:
   - Identify the stack (Vanilla HTML/CSS/JS, React/Vue/Svelte, Tailwind, or 3D Canvas like CesiumJS/Three.js/Mapbox).
   - Record all automated test selectors or required DOM `id` attributes so zero functional bindings are broken.
2. **Diagnose and tune the background layer**:
   - Liquid Glass requires background contrast and color to refract.
   - **For 3D / GIS / Map / Video backgrounds**: Remove heavy dark vignette overlays or top black gradients covering the canvas. Tune imagery/canvas brightness to `0.80-0.88`, saturation to `0.85-0.92`, and contrast to `1.10-1.15`. Keep any outer boundary mask alpha at `<= 0.10`.
   - **For flat SaaS / Dashboard backgrounds**: If the page background is a flat solid color (where refraction would be invisible), inject a subtle ambient background mesh or 2-3 slow-drifting radial cyan/indigo glow orbs behind the glass containers so `<feDisplacementMap>` has gradients and grid lines to bend.

### Phase 2: Mount the SDF Optical Refraction Engine

1. Copy `scripts/liquid-glass-engine.js` into the project (or import its `initLiquidGlassEngine()` function into the app entry point).
2. The engine automatically:
   - Computes pixel-accurate Signed Distance Fields (`roundedRectSDF`) and `smoothStep` lens profiles for 6 aspect-ratio presets (`#vge-lg-drawer`, `#vge-lg-topbar`, `#vge-lg-rail`, `#vge-lg-pill`, `#vge-lg-card`, `#vge-lg-btn`).
   - Encodes inward normal pull vectors into RGBA channels (`R` = X shift, `G` = Y shift, `128` = zero distortion at the flat center) and injects hidden `<svg>` `<feDisplacementMap>` filters into `document.body`.
   - Tracks pointer movement within a `180px` proximity halo around glass panels and cards, updating `--mx` and `--my` CSS custom properties in real time.

### Phase 3: Apply the 4-Tier Optical Hierarchy & Unified Controls

Consult `assets/component-mapping-matrix.json` and import or adapt `assets/liquid-glass-core.css`:

1. **Tier 1 - Primary Floating Containers (Topbar, Navigation Rail, Main Drawer/Sidebar, Bottom Dock, Modals)**:
   - Bind the matching aspect-ratio SVG filter: `backdrop-filter: url(#vge-lg-drawer) blur(4px) contrast(1.18) brightness(0.92) saturate(1.28)`.
   - Apply the 6-layer opposing meniscus `box-shadow`:
     - Top-left specular glint: `inset 2px 2px 1.5px -0.5px rgba(255, 255, 255, 0.82)`
     - Bottom-right cyan caustic: `inset -2px -2px 1.5px -0.5px rgba(56, 189, 248, 0.48)`
     - Inner bevel depth: `inset 5px 5px 4px -5px rgba(255, 255, 255, 0.42), inset -5px -5px 4px -5px rgba(125, 211, 252, 0.35)`
     - Core vignette & elevation shadow: `inset 0 0 18px 2px rgba(2, 6, 14, 0.42), 0 20px 48px rgba(0, 4, 12, 0.55)`
2. **Tier 2 - Sub-Cards, Telemetry Blocks, List Rows, Accordions**:
   - Use zero-white smoked crystal fill (`linear-gradient(155deg, rgba(4, 12, 24, 0.28) 0%, rgba(2, 8, 18, 0.36) 100%)`) with `backdrop-filter: url(#vge-lg-card) blur(2px) contrast(1.12)`.
   - Attach the `::after` masked border spotlight (`padding: 1.5px; -webkit-mask-composite: xor; mask-composite: exclude;`) so a `170px` pure-white/cyan light beam travels along the card's `1.5px` rim following `--mx` and `--my`.
3. **Tier 3 - Unified Form Controls, Uiverse Droplet Switches & Shimmer Buttons**:
   - Unify all `<input>`, `<textarea>`, and custom `<select>` triggers to `height: 34px`, `border-radius: 8px`, `background: rgba(2, 8, 18, 0.42)`, and `box-shadow: inset 0 1.5px 4px rgba(0,0,0,0.48), inset 0 -1px 0.5px rgba(255,255,255,0.34)`.
   - Style toggle switches (`.lg-switch-track`) with a 3D convex crystal droplet thumb that stretches horizontally (`width: 18px -> 23px`) on `:active` press.
   - Add the `::before` 45-degree skewed specular shimmer sweep and `:active { transform: scale(0.96); }` spring physics to all primary and secondary lens buttons.
4. **Tier 4 - Hero / Context Banner**:
   - Style top context headers as borderless right-dissolving holographic banners using `-webkit-mask-image: linear-gradient(90deg, #000 64%, transparent 100%)` and `border-left: 3px solid #38bdf8`.

### Phase 4: Adaptive Sci-Fi Domain Enhancements

Select the enhancements that fit the target application's domain:

- **For 3D / Geospatial / Robotics / Autonomous Systems**:
  - **Airway / Trajectory Ribbon & Flow Pulse**: Pair primary paths with a wide translucent safety ribbon (`width: 16px`, alpha `0.26`) and an animated high-intensity energy packet streaming along the path at `50-60 m/s`.
  - **Vehicle / Agent Sensor Cone & Halo**: Render a glowing perimeter halo ring, a forward-sweeping radar cone (`±20°` fan with oscillating scan ray), a vertical ground laser altimeter line, and an expanding ground sonar ring.
  - **Viewport-Centered Airborne HUD**: Mount a pill-shaped telemetry HUD (`HDG`, `AGL`, `GS`, `ATT`) above the bottom dock. **Critical layout rule**: Always compute horizontal centering relative to the active canvas viewport (`left: calc(var(--sidebar-offset) + (100vw - var(--sidebar-offset)) / 2)`) and place `bottom` at least `12px` above the top edge of any bottom dock (`calc(var(--dock-bottom) + var(--dock-height) + 12px)`) to guarantee zero overlap.
- **For SaaS / AI / Analytics Dashboards**:
  - Enable cursor-tracking rim glow on KPI bento cards and data tables.
  - Apply SVG `<linearGradient>` glow fills under sparklines/area charts and liquid droplet thumbs on range sliders.
  - Enable subtle Web Audio API harmonic micro-tones (`playCyberTone`) on primary workflow actions.

### Phase 5: Verification & Optical QA

1. Run `node scripts/audit-liquid-glass.js <path-to-css-or-dir>` to verify:
   - Zero chalky white surface fills (`rgba(255, 255, 255, alpha > 0.06)` on container backgrounds).
   - Zero over-blurred containers (`blur > 8px` on primary refractive glass).
   - Unified `34px` input/select control heights.
2. Visually inspect the rendered UI in a live browser (at `1366x768` and `1920x1080`) to confirm zero horizontal drawer overflow and zero HUD/dock overlap.

## Gotchas

- **Cross-Browser Fallback**: Chromium browsers (Chrome, Edge, Brave, Electron) natively render `backdrop-filter: url(#svg-filter)`. For Safari/Firefox where SVG `backdrop-filter` is ignored, always include a clean CSS fallback property immediately before the SVG rule (`backdrop-filter: blur(6px) saturate(160%) contrast(1.12);`).
- **Legacy Pseudo-Element Conflicts**: When upgrading existing toggle switches to the Liquid Glass droplet thumb (`::before`), explicitly set `.switch-track::after { display: none !important; }` if the legacy stylesheet used `::after` for its thumb.
- **Dynamic Viewport Alignment**: Never hardcode `left: 50%` on floating HUDs if the app has a collapsible left/right drawer; bind the HUD's `left` coordinate to the same CSS variable (`--map-left` or `--sidebar-width`) used by the main viewport.
