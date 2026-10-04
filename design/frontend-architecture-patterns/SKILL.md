---
name: frontend-architecture-patterns
description: Advanced structural patterns for Landing Pages, SaaS apps, and Data Visualization. Use when determining the macro-level layout, conversion flows, and ergonomic hierarchy of a new frontend project.
version: "1.0.0"
verified_date: 2026-04-29
category: frontend
---

# Frontend Architecture & Interface Patterns

## Purpose
Provide strict structural and ergonomic rules for assembling high-conversion landing pages, complex SaaS shells, and dense data visualizations. This bridges the gap between atomic UI design and full-page composition.

## When to Use This Skill
Use when structuring a new frontend project, deciding on the layout of a landing page or SaaS dashboard, optimizing conversion funnels, or building complex data charts.

## Phase 1: Macro-Architecture Selection
Identify the target product type to enforce the correct UI shell:

### A. Landing Page Architecture (Conversion Optimized)
Select the correct sequence based on the product:
1. **Classic SaaS**: Hero -> Value Prop -> Key Features -> Social Proof -> Pricing -> CTA
2. **Product-Led Growth**: Hero (Interactive Demo) -> Social Proof -> Features -> Interactive Pricing -> CTA
3. **Enterprise**: Hero (Video) -> Client Logos -> Solutions by Industry -> Security/Compliance -> Contact Sales
4. **Developer Tool**: Hero (Code snippet/Terminal) -> Quick Start -> Technical Features -> Documentation link -> Github CTA

### B. SaaS / App Interface Shells
1. **Sidebar Navigation**: Width 64px (collapsed) / 240px (expanded). Main content area scrollable independently.
2. **Top Bar**: Reserved for global search, profile management, and notification centers. Sticky blur.
3. **Bento Grid Dashboards**: Asymmetric tile layouts prioritizing the highest-value data metric in the top left.

## Phase 2: Micro-Architecture & Ergonomics
- **Fitts's Law**: Make primary CTAs large and easy to click. Minimum touch target: `44x44px`. Place crucial actions at screen edges (bottom right floating action button).
- **Hick's Law**: Minimize choices. Never show more than 3 primary pricing tiers or 5 main navigation links.
- **Contrast**: Maintain strict 4.5:1 text-to-background contrast ratio (WCAG AA). 

## Phase 3: Data Visualization Patterns
- **Fonts**: All numerical data and tabular data must use monospace fonts (`font-mono`) to prevent layout shifting.
- **Legends**: Bottom-aligned or right-aligned. Use distinct shape markers (dots/squares) to aid colorblind users.
- **Interactivity**: Charts must feature tooltips on hover. Empty states must be designed ("No data available").

## Output Format / Delivery
- A complete layout specification or skeleton code (e.g., Next.js layout.tsx).
- Component architecture mapped to the chosen conversion pattern.

## Behavior Rules
1. **Structure first, style second**: Do not apply colors or animations until the structural sequence (Hero -> Features -> CTA) is locked.
2. **Adhere to standard shells**: Do not reinvent navigation unless the product specifically demands experimental interaction.
3. **Data density**: SaaS dashboards must optimize for data density without clutter; use spacing over borders to separate elements.
4. **State Management Boundaries**: Explicitly decide state managers. Use local state for atomic components, `Zustand` or `Jotai` for lightweight global state, and React Context only for dependency injection, avoiding prop-drilling in complex SaaS shells.

## Hard Usage Rules (Tier 2: Conditional)
- **ALLOWED**: Initializing App Router files (`layout.tsx`, `page.tsx`).
- **FORBIDDEN**: Writing complex reactive state logic.
- **CONSTRAINT**: Every file generated must contain an explicit `"use client"` or a comment explaining why it is a Server Component.

## Safety Guardrails & Patched Prevention
1. **Client/Server Bleed Patch**: If `useState`, `useEffect`, or any event listener (`onClick`) is present, the file MUST start with `"use client"`.
2. **Prop Drilling Patch**: If a prop is passed more than two component levels deep, halt generation and implement Context or Zustand.
3. **Layout Shift Patch**: All `<Suspense>` boundaries must have a `<Skeleton>` fallback with deterministic height and width.
4. **Self-Rejection Clause**: If the output violates boundary validation or generates uncapped prop chains, **ABORT OUTPUT** and self-correct.

## Maintenance Notes
- Merged from legacy `pro-max-landing-page-architecture`, `pro-max-app-interface-patterns`, `pro-max-ux-guidelines`, and `pro-max-data-visualization`.
