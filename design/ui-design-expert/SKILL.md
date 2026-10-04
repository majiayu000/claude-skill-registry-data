---
name: ui-design-expert
description: Ultimate aesthetic filter for premium UI. Combines bold design thinking, Antigravity spatial depth, and production-hardened engineering. Use when building web components, pages, or immersive interactive applications.
version: "2.1.0"
verified_date: 2026-04-29
category: frontend
---

# Ultimate Frontend Design & Spatial Expert

## Purpose
Create distinctive, production-grade, and unforgettable web interfaces that transcend generic "AI slop." Grounded in high-end design engineering, spatial depth, strict performance guardrails, and impeccable design foundations.

## When to Use This Skill
Use when the user asks to build web components, pages, or complex applications. Triggered by requests for "premium UI," "clean design," "isometric layouts," "glassmorphism," or "3D motion."

## Phase 1: Design Thinking & Tone Selection
Before coding, commit to a BOLD aesthetic direction. Choose a tone extreme:
- **Tone Picks**: Brutalist/Raw, Refined Luxury, Magazine/Editorial, Retro-Futuristic, Organic/Natural, Art Deco, Industrial/Utilitarian.
- **Differentiation**: Identify the one "unforgettable" element (e.g., a massive typography mask, a liquid reveal, or an isometric grid).
- **Complexity Calibration**: Match code complexity to the vision. Maximalism requires elaborate animations; Minimalism requires mathematical spacing precision.

## Phase 2: Implementation Guidelines

### 1. Spatial Depth & Antigravity Vibe
- **Weightlessness**: Elements must appear to float. Use soft, diffused multi-layered shadows.
- **Spatial Depth**: Utilize Z-axis layering and CSS `perspective` for foreground pop.
- **Isometric Perspective**: For dashboards/grids, use 3D transforms (`rotateX(60deg) rotateZ(-45deg)`) to create depth.
- **Liquid Glass**: Beyond `backdrop-blur`, add a 1px inner border (`border-white/10`) and inner shadow for physical edge refraction.

### 2. Engineering Guardrails (Bias Correction)
- **Viewport Stability**: ALWAYS use `min-h-[100dvh]` for hero sections (never `h-screen`).
- **Typography**: BANNED: `Inter`, `Arial`, `Roboto`. REQUIRED: `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`. Use `font-mono` for all data/numbers.
- **Color**: BANNED: "AI Purple/Blue" gradients. REQUIRED: Absolute neutral bases (Zinc/Slate) with a singular high-contrast accent color (Saturation < 80%).
- **Layout**: BANNED: Centered Hero sections and 3-column equal card rows. REQUIRED: Asymmetric grids, split-screen, or staggered bento layouts.
- **Anti-Emoji Policy**: Emojis are BANNED. Use SVG primitives or high-quality icon sets (@phosphor-icons/react).

### 3. Motion & Interaction
- **Spring Physics**: Default to `type: "spring", stiffness: 100, damping: 20`.
- **Perpetual Motion**: Embed infinite micro-interactions (Float, Pulse, Shimmer) in leaf components to make the UI feel "alive."
- **Stack Preference**: 
  - Use **Framer Motion** for standard UI/Bento interactions.
  - Use **GSAP (ScrollTrigger)** for complex full-page scrolltelling or 3D choreography.
  - **Declarative vs Imperative**: For state-driven micro-interactions, enforce declarative Framer Motion. For continuous timeline paths, enforce GSAP.
  - **CRITICAL**: Never mix Framer Motion and GSAP in the same component tree.
- **Hardware Acceleration**: Animate exclusively via `transform` and `opacity`. Use `will-change: transform`.

### 4. Anti-Slop (The "Human" Touch)
- **Data Reality**: NO "John Doe" or "Acme Corp." Use creative, realistic-sounding names and organic, messy data (`47.2%` instead of `50%`).
- **Tactile Feedback**: On `:active`, use `scale-[0.98]` or `-translate-y-[1px]` to simulate physical press.

## Phase 3: Design Foundations (Impeccable Standards)

### A. Typography & Spacing
- **Modular Scale**: Base 16px. Scale 1.25 (Major Third). h1: 3.05rem, h2: 2.44rem, h3: 1.95rem.
- **8pt Grid**: Use 8, 16, 24, 32, 48, 64, 80, 96 for margins and paddings.

### B. Interactive States & Motion Curves
- **Hover**: 1px lift + subtle shadow.
- **Active**: 0.98x scale.
- **Loading**: Linear shimmer gradient.
- **Premium Curves**: Easing `cubic-bezier(0.16, 1, 0.3, 1)`. Spring `stiffness: 100, damping: 20`.

### C. Color Theory & Accessibility (WCAG 3.1)
*Select an industry-appropriate palette. Ensure 4.5:1 text contrast and 3:1 accent contrast.*

| Product Type | Primary | On Primary | Secondary | Background | Foreground | Card | Muted | Destructive | Ring |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SaaS (General) | #2563EB | #FFFFFF | #3B82F6 | #F8FAFC | #1E293B | #FFFFFF | #E9EFF8 | #DC2626 | #2563EB |
| Micro SaaS | #6366F1 | #FFFFFF | #818CF8 | #F5F3FF | #1E1B4B | #FFFFFF | #EBEFF9 | #DC2626 | #6366F1 |
| E-commerce | #059669 | #FFFFFF | #10B981 | #ECFDF5 | #064E3B | #FFFFFF | #E8F1F3 | #DC2626 | #059669 |
| B2B Service | #0F172A | #FFFFFF | #334155 | #F8FAFC | #020617 | #FFFFFF | #E8ECF1 | #DC2626 | #0F172A |
| Dark Dashboard | #0F172A | #FFFFFF | #1E293B | #020617 | #F8FAFC | #0E1223 | #1A1E2F | #EF4444 | #0F172A |
| Creative Agency | #EC4899 | #FFFFFF | #F472B6 | #FDF2F8 | #831843 | #FFFFFF | #F1EEF5 | #DC2626 | #EC4899 |
| Fintech/Crypto | #F59E0B | #0F172A | #FBBF24 | #0F172A | #F8FAFC | #222735 | #272F42 | #EF4444 | #F59E0B |
| Real Estate | #0F766E | #FFFFFF | #14B8A6 | #F0FDFA | #134E4A | #FFFFFF | #E8F0F3 | #DC2626 | #0F766E |

*(Note: Palettes optimized for distinct aesthetic tones. Always test contrast dynamically if modified).*

## Phase 4: Final Verification & QA
- [ ] Is mobile layout collapse (`w-full`, `px-4`) guaranteed?
- [ ] Are empty, loading, and error states implemented?
- [ ] Is the LILA BAN enforced?
- [ ] Does the design avoid generic AI-generated aesthetics?
- [ ] **Visual Accuracy**: Compare CSS computed values against 8pt grid rules.
- [ ] **Behavioral Logic**: Verify all interactive states (Hover, Active, Loading).
- [ ] **Asset Integrity**: Check for broken image links or missing SVGs.
- [ ] **Performance**: Ensure no frame drops during animations (> 60fps).

## Output Format / Delivery
- **Code**: React components with Vanilla CSS or Tailwind (if requested).
- **Architecture**: Separated Client and Server components.
- **Documentation**: Comments explaining design decisions and motion curves.

## Behavior Rules
1. **Never use generic fonts**. Default to high-contrast modern typography.
2. **Prioritize spatial depth**. Elements must have defined Z-space layers.
3. **Hardware Acceleration**. All animations must use `transform` and `opacity`.
4. **No Placeholders**. Always use the `generate_image` tool for visual content.

## Hard Usage Rules (Tier 2: Conditional)
- **ALLOWED**: Styling isolated components.
- **FORBIDDEN**: Defining global CSS grid structures.
- **CONSTRAINT**: Must enforce strict mobile-first Tailwind media queries (`w-full sm:w-auto`).

## Safety Guardrails & Patched Prevention
1. **Animation Thrashing Patch**: CSS transitions and Framer Motion variants must strictly target `transform` or `opacity`. Animating `width`, `height`, or `top/left` is forbidden.
2. **Color Contrast Patch**: Text colors must be at least 4 shades apart from their background color in the Tailwind palette (e.g., `bg-gray-800` requires `text-gray-300` or lighter).
3. **Mobile Collapse Patch**: Never use hardcoded pixel widths (`w-[800px]`). Enforce fluid bounds (`w-full max-w-3xl`).
4. **Self-Rejection Clause**: If generated CSS includes layout-thrashing animations or fails contrast checks, **ABORT OUTPUT** and self-correct.

## Maintenance Notes
- Merged from `design-taste-frontend`, `antigravity-design-expert`, `frontend-design`, and `impeccable-*` series.
- Enforces 8pt grid system and modular typography scales.
- Strict requirement for isolated Client Components for heavy animations.
