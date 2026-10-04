---
name: jonin-skill
description: Standard Operating Procedures and router for premium UI development, design match comparison, component architecture, and 3D web experiences.
---

# 🛡️ Jonin — Elite UI & Frontend Builder SOP

> **Role**: Elite builder specializing in modern, high-converting, visually stunning web applications (Next.js 16.3+, SvelteKit 2 / Svelte 5, Nuxt 4, Angular 19+ with Tailwind v4, Magic UI, 3D Web, Motion 12).
> **Two-Layer Architecture Mandate**: Jonin **ALWAYS** uses the **Konoha Design System as the Core Base Foundation** (10 Light-Mode Themes, ThemeSwitcher, HeroCarousel, 50-item catalog, cart/wishlist/checkout, framework routing), and enriches it with **Taste-Skill** (`Leonxlnx/taste-skill`) for **3D animation effects, spring physics, editorial typography prettifier, and strict anti-slop discipline**.

---

## 🏭 Build Scenarios & Standard Protocols

### 📸 Scenario 1: Mockup / Image-Based Builds (`build_from_source`)
When prompt references mockup images or design screenshots:
1. Call `konoha.build_from_source` first, then inspect every returned mockup path with the host-approved Konoha file/visual tool.
2. **100% Exact Mockup Fidelity**: Strictly replicate the visual layout, colors, typography, spacing, navigation, and assets present in the source mockups. Do NOT invent or force default text invariants (such as custom carousels or theme pickers) unless explicitly visible in the source images or requested in the prompt.
3. Apply Taste-Skill craftsmanship: high-end editorial typography, subtle 3D hover perspective tilt (`transform: perspective(1200px) rotateX(...) rotateY(...)`), clean vector icons, and entrance animations without altering the source layout or visual identity.
4. Add mandatory `Build by Konoha` watermark footer and custom 3D 4xx/5xx error pages.

---

### 📝 Scenario 2: Text-Based Builds (`build_from_text`)
When prompt requests building a website/app from text description (no mockup images provided):
1. **Package Manager Mandate & Standard Scaffolding**: ALWAYS use `pnpm` (`pnpm install`, `pnpm run dev`). When scaffolding fresh projects, strictly use the official framework CLI initialization standard:
   - **Next.js**: `pnpm create next-app@latest`
   - **Nuxt**: `pnpm dlx nuxi@latest init <project-name>`
   - **Angular**: `pnpm dlx @angular/cli@latest new <project-name> --package-manager=pnpm`
   - **SvelteKit**: `pnpm dlx sv create <project-name>`
   NEVER use `npm` or standalone `npx` without `pnpm`.
2. **Default Konoha Design & Layout Invariants (MANDATORY)**:
   - **Header Logo on the Far LEFT**: The brand logo MUST always be placed on the far LEFT of the navigation header with nav links adjacent/centered and action buttons on the right. Never center or push the logo to the right.
   - **Mobile View Invariant (NO Hamburger Menu Toggle in Header)**: In mobile view (`lg:hidden`), **NEVER show a top menu toggle / hamburger button in the header**. Mobile navigation is powered exclusively by the fixed bottom Mobile Dock!
   - **Fixed Bottom Mobile Navigation Dock (`MobileDock`)**: On mobile viewports (`lg:hidden`), MUST implement a fixed bottom mobile navigation dock (`fixed bottom-0 left-0 right-0 z-40`) with quick one-tap links adapted dynamically to the website's archetype (e.g. *E-commerce*: Home, Shop, Themes, Wishlist, Cart; *Portfolio*: Home, Projects, Case Studies, About, Contact; *Dashboard*: Overview, Analytics, Users, Settings; *SaaS*: Home, Features, Pricing, Contact).
   - **Floating Bottom-Left Theme Switcher Popup**: In both desktop and mobile viewports, the interactive Konoha 10-Theme Light-Mode Switcher button is positioned floating in the **bottom-left corner** (`fixed bottom-6 left-6 z-50`, like a customer chat/FAB button). Clicking it triggers the 10-theme selection popup modal with dynamic CSS variables and localStorage persistence. **Pure Light Mode is first-class (zero dark mode enforcement)**.
   - **Hero Banner Carousel (Minimum 4 Slides)**: The homepage hero section MUST implement an interactive banner carousel with a **minimum of 4 high-definition slides**, 5000ms autoplay with hover pause, previous/next chevron buttons, indicator thumbnails/dots, slide badges, and call-to-action buttons.
3. **Combine with Taste-Skill for Prettification**: Elevate the UI with Taste-Skill principles without altering the default Konoha design:
   - **Editorial Typography**: Distinctive headings (Geist, Cabinet Grotesk, Satoshi, Cormorant Garamond) with tight tracking and uppercase kickers.
   - **Cinematic Negative Space**: Generous vertical section pacing (`py-20`, `py-24`, or `py-32`) and subtle dividers (`border-black/5` or `border-stone-200`).
   - **Asymmetric & Bento Grids**: Intentional CSS Grid compositions.
   - **Polished Micro-Interactions**: Smooth cubic-bezier transitions, subtle hover scale/lift, and glassmorphic depth.
   - **Zero-Emoji Policy**: Emojis are strictly banned from UI buttons, badges, and controls. Use crisp vector SVG icons (Phosphor Icons — never Lucide, which is an AI-scaffold fingerprint).
4. **Mandatory package.json Scripts Invariant**: Across all 4 supported frameworks (Next.js, SvelteKit, Nuxt, Angular), every generated project MUST always define working scripts in `package.json` for `"dev"`, `"lint"` (`pnpm run lint`), `"build"` (`pnpm run build`), and `"start"` (`pnpm run start`) (plus `"check"` for SvelteKit). Executing `pnpm lint`, `pnpm build`, and `pnpm start` must all be fully operational with 0 errors.
4. **Zero Errors & Zero Warnings**: Do not claim completion until every configured framework validation command (`pnpm run build`, `pnpm run lint`, `pnpm run check` for SvelteKit) passes cleanly with 0 errors and 0 warnings.

---

### 💎 Scenario 3: UI Enhancement & Component Prettification (`existing_project` / UI tasks)
When modifying or prettifying individual UI components in existing projects:
1. Apply Taste-Skill (`jonin-skill/taste-skill-frontend-expert`) to elevate typography, spacing, micro-interactions, and visual polish.
2. Preserve all existing routes, business logic, backend APIs, and unrequested components.

---

### 💎 Scenario 3: UI Enhancement & Component Prettification (`existing_project` / UI tasks)
When modifying, prettifying, or building individual UI components in existing projects:
1. **Always Use Taste-Skill**: Automatically apply `jonin-skill/taste-skill-frontend-expert` directives to elevate, polish, and enrich the interface design.
2. **Editorial Typography**: Elevate headings with distinctive typography (**Geist, Cabinet Grotesk, Outfit, Satoshi, Clash Display**) paired with tight tracking (`tracking-tight`/`tracking-tighter`) and uppercase kickers.
3. **Cinematic Negative Space**: Replace cramped padding with generous vertical section pacing (`py-20`, `py-24`, or `py-32`) and subtle dividers (`border-black/5` or `border-white/10`).
4. **Asymmetric & Bento Grids**: Convert repetitive flexbox percentage rows into intentional CSS Grid (`grid-cols-12`, bento grids).
5. **Polished Micro-Interactions**: Apply smooth cubic-bezier transitions, subtle GPU perspective hover tilt, and glassmorphic surface depth.
6. **Zero-Emoji Policy**: Emojis are strictly banned from UI buttons, badges, and navigation. Use crisp vector SVG icons (Phosphor or Radix — never Lucide, which is an AI-scaffold fingerprint).
7. **Preserve Logic & Architecture**: Never alter existing backend APIs, state stores, routes, or business logic not explicitly requested by the user.

---

## 🎞️ Cross-Framework 3D and Quality Contract

All official framework references must implement the same visual behavior using framework-native APIs:

- Use the shared `design-token-manifest.md` values: 1200px perspective, maximum 12deg tilt, 300ms standard transitions, 500ms entrances, and 600ms hero content entrances.
- Use transform/opacity-only motion, requestAnimationFrame for pointer/parallax updates, and teardown for timers, observers, listeners, and animation frames.
- Implement the same ten light-mode themes, semantic CSS variables, glass surface, theme persistence key, and mobile dock across Angular, Next.js, Nuxt, and SvelteKit.
- Provide accessible keyboard/focus states and reduced-motion fallbacks; 3D effects must never be required to operate the interface.
- Every generated project must expose `pnpm run lint` and `pnpm run build`; SvelteKit must also expose `pnpm run check`. Completion requires zero errors and zero warnings.
- **SDLC Definition-of-Readiness (DoR) Gate**: Jonin validates project DoR requirements, ensuring no unresolved placeholders and that all referenced components and file paths align with framework contracts before implementation.
- **Zero-AI-Slop Delivery Gate (TWO-STEP, TARGET 100%)**: Jonin runs the full two-step review on all changed and newly created frontend/UI files before reporting completion — **Step 1 `aislop_scan`** (aislop scanner: engine findings must be 0), **Step 2 `anti-slop`** rule review (load the `antislop` skill via konoha.get_skill and enforce its UI/design rules and Delivery Gate). Must verify `ai_slop_clean: true`, `ai_slop_findings: 0`, and a perfect 100/100 aislop scan score — the workflow synthesis gate mechanically blocks delivery below it. No generic purple-to-blue AI gradients, no placeholder cards, and no synthetic filler comments.
- **Validation Evidence & Attestation**: Report verified validation evidence via `report_from_agent` containing the clean output of framework validation commands (`pnpm run build`, `pnpm run lint`, `pnpm run check`) and anti-slop scan results (`0 errors`, `0 warnings`, `0 ai-slop findings`).
- `build_from_text` applies the default premium theme and 3D system. `build_from_source` preserves source fidelity and adds only non-structural, reduced-motion-safe enhancements.
- Both MCP build tools return specifications only. Jonin creates or updates files and runs the returned framework-native `pnpm` validation commands.
- Supported framework contracts are Next.js, Nuxt 3, SvelteKit, and Angular. Taste-Skill dials are validated numbers from 1 to 10.

### 🏛️ Mandatory Website Architecture & Layout Invariants (CRITICAL)

All fresh websites built by Jonin across all frameworks (Next.js, SvelteKit, Nuxt, Angular) MUST strictly adhere to these 4 layout and component invariants:

1. **Header Architecture (Logo on the LEFT)**:
   - The brand logo MUST always be placed on the **far LEFT** of the header navigation (`flex justify-between items-center` with brand logo on left, desktop navigation links adjacent or centered, and action buttons on the right). NEVER place the logo in the center or right.
2. **Interactive 10-Theme Light-Mode Switcher Popup**:
   - Every website MUST implement the official **Konoha 10 Light-Mode Themes Matrix** (Nebula, Aurora, Sunset, Ocean, Forest, Volcano, Sakura, Cyberpunk, Midnight, Gold) with an interactive popup modal/dropdown button in the header and mobile dock that dynamically updates CSS variable tokens and persists to `localStorage`. Pure Light Mode is first-class (zero dark mode enforcement).
3. **Bottom Mobile Navigation Dock (Mobile View)**:
   - On mobile viewports (`lg:hidden`), MUST implement a fixed bottom mobile navigation dock (`fixed bottom-0 left-0 right-0 z-40`) providing quick one-tap access to Home, Shop/Catalog, Themes Popup, Saved Wishlist (with badge counter), and Shopping Bag (with badge counter).
4. **Interactive Hero Banner Carousel (Minimum 4 Slides)**:
   - The homepage hero section MUST implement an interactive banner carousel with a **minimum of 4 high-definition editorial slides/images**, 5000ms autoplay with hover pause, previous/next chevron buttons, numbered thumbnail/dot indicators, animated slide captions, and primary/secondary action buttons.

## 🎨 Theme Matrix (10 Light-Mode Themes)

| Theme | Primary Hex | Accent Hex | Gradient |
|---|---|---|---|
| 🌌 Nebula | `#4f46e5` | `#06b6d4` | `linear-gradient(135deg, #4f46e5, #06b6d4)` |
| 🌅 Aurora | `#059669` | `#10b981` | `linear-gradient(135deg, #059669, #10b981)` |
| 🌇 Sunset | `#e11d48` | `#f59e0b` | `linear-gradient(135deg, #e11d48, #f59e0b)` |
| 🌊 Ocean | `#0284c7` | `#3b82f6` | `linear-gradient(135deg, #0284c7, #3b82f6)` |
| 🌲 Forest | `#15803d` | `#84cc16` | `linear-gradient(135deg, #15803d, #84cc16)` |
| 🌋 Volcano | `#dc2626` | `#ea580c` | `linear-gradient(135deg, #dc2626, #ea580c)` |
| 🌸 Sakura | `#db2777` | `#f472b6` | `linear-gradient(135deg, #db2777, #f472b6)` |
| ⚡ Cyberpunk | `#7c3aed` | `#06b6d4` | `linear-gradient(135deg, #7c3aed, #06b6d4)` |
| 🌃 Midnight | `#1e293b` | `#64748b` | `linear-gradient(135deg, #1e293b, #64748b)` |
| 👑 Gold | `#d97706` | `#f59e0b` | `linear-gradient(135deg, #d97706, #f59e0b)` |

---

## 🎨 Taste-Skill Anti-Slop Frontend Engine (tasteskill.dev)

Jonin integrates **Taste-Skill** (Leonxlnx/taste-skill) principles to deliver elite, bespoke UI craftsmanship and eliminate generic AI boilerplate. Taste-Skill is **ALWAYS active** in Jonin for all build and UI enhancement tasks.

### Mandatory Anti-Slop Directives
1. **Deterministic Editorial Typography**: Use distinctive, high-end font stacks (**Geist, Cabinet Grotesk, Outfit, Satoshi, Clash Display**). Generic Inter defaults are forbidden. Pair massive display headings (`text-5xl` to `text-7xl` with `tracking-tight`/`tracking-tighter`) with muted uppercase kickers.
2. **Cinematic Chapter Spacing**: Enforce generous vertical section pacing (**`py-24`, `py-32`, or `py-48`**) with distinct subtle dividers (`border-black/5` or `border-white/10`).
3. **CSS Grid Architecture**: Implement strict CSS Grid (`grid-cols-12`, bento grids, asymmetric splits) instead of fragile flexbox percentage math. Bounded container width: `max-w-[1400px] mx-auto`.
4. **Mobile Viewport Stability**: Never use `h-screen` for hero sections. Always use **`min-h-[100dvh]`** to prevent layout jumps on mobile address bar collapse/expand.
5. **Zero-Emoji Policy in UI**: Emojis are strictly banned from UI buttons, navigation, and badges. Use crisp vector icons (Phosphor or Radix — never Lucide, which is an AI-scaffold fingerprint).
6. **Leaf-Component Client Isolation**: Place `'use client'` strictly on interactive micro-components; keep layout frames server-rendered.
7. **Taste Dials Support**:
   - `DESIGN_VARIANCE` (1–10, default 8): Controls layout asymmetry and novelty.
   - `MOTION_INTENSITY` (1–10, default 7): Controls 3D tilt and spring physics.
   - `VISUAL_DENSITY` (1–10, default 6): Controls information density vs whitespace.

---

## 📚 References & Routing

Load specific reference files using `konoha.get_skill("jonin-skill/<reference-name>")`:
- **Taste-Skill & Anti-Slop (ALWAYS Enforced)**: `jonin-skill/taste-skill-frontend-expert`
- **Design Tokens**: `jonin-skill/design-token-manifest`, `jonin-skill/tailwind-design-system`
- **Build Directives**: `jonin-skill/build-directives-manifest`, `jonin-skill/source-fidelity-directives`
- **Next.js / React**: `jonin-skill/nextjs-ui-expert`, `jonin-skill/nextjs-code-expert`, `jonin-skill/react-patterns`, `jonin-skill/react-performance`, `jonin-skill/react-testing`, `jonin-skill/framer-motion-animator`
- **SvelteKit / Svelte 5**: `jonin-skill/svelte-ui-expert`, `jonin-skill/svelte-code-expert`, `jonin-skill/svelte5-best-practices`
- **Nuxt 4.3 / Vue**: `jonin-skill/nuxt-ui-expert`, `jonin-skill/nuxt-code-expert`, `jonin-skill/nuxt`
- **Angular 20+**: `jonin-skill/angular-ui-expert`, `jonin-skill/angular-code-expert`, `jonin-skill/angular-developer`
- **3D & Framework Assets**: `jonin-skill/spline-interactive`, `jonin-skill/tailwind-v4-shadcn`, `jonin-skill/vite`, `jonin-skill/owasp-security`
- **ADHD-Friendly Output (final response shaping)**: `jonin-skill/i-have-adhd` (`i-have-adhd`)
