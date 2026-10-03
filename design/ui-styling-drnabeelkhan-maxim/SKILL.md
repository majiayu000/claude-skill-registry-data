---
name: maxim:ui-styling
description: Maxim UI Styling Intelligence — shadcn/ui components, Tailwind CSS, CSS architecture, responsive design, dark mode, accessibility-compliant styling (WCAG 2.1 AA), animation and motion design, theming systems. Activate for component building, layout implementation, theme customization, dark mode, CSS architecture decisions, UI polish. Powered by Maxim behavioral science + Fitts' Law + Color Psychology.
argument-hint: "[component|layout|theme|dark-mode|animate|audit] [args]"
confidence: 🟢 HIGH
---

# Maxim UI Styling Intelligence

> Maxim behavioral layer active. Behavioral science applied to every output.
> External reference: `community-packs/ui-ux-pro-max/.claude/skills/ui-styling/`

## Agents in This Skill

### 1. component-builder
Builds accessible, composable UI components using shadcn/ui + Tailwind.
- Primary stack: shadcn/ui (Radix UI primitives) + Tailwind CSS utility-first
- Applies Fitts' Law: interactive targets minimum 44×44px, CTA targets ≥48×48px on touch
- Applies Proximity (Gestalt): related elements grouped with consistent spacing tokens
- Enforces WCAG 2.1 AA: 4.5:1 contrast ratio for body text, 3:1 for large text and UI components
- Absorbs external component catalog: `community-packs/ui-ux-pro-max/.claude/skills/ui-styling/references/shadcn-components.md`
- Installation automation: `scripts/shadcn_add.py` (component + dependency handling)
- Output: TypeScript React component + Tailwind classes + accessibility attributes + usage example

### 2. layout-architect
Owns responsive layout systems from mobile-first to desktop.
- Enforces mobile-first methodology: base styles → sm → md → lg → xl → 2xl
- Applies Gestalt Laws to layout: Proximity (grouping), Similarity (visual rhythm), Continuation (flow)
- Applies Cognitive Load Theory: max 5±2 visual elements per viewport region before chunking
- Absorbs responsive patterns: `community-packs/ui-ux-pro-max/.claude/skills/ui-styling/references/tailwind-responsive.md`
- Output: Complete responsive layout spec + Tailwind class map + breakpoint decision rationale

### 3. theme-engineer
Owns dark mode, theming, and token-to-Tailwind integration.
- Implements CSS variable system: semantic layer enables light/dark swap without component changes
- Implements next-themes integration for React (no flash, SSR-safe)
- Applies Color Psychology: primary (trust/action), secondary (support), destructive (danger/urgency)
- Generates Tailwind config extension from design tokens: `scripts/tailwind_config_gen.py`
- Absorbs theming reference: `community-packs/ui-ux-pro-max/.claude/skills/ui-styling/references/shadcn-theming.md`
- Proactively loops: `design-system` skill to confirm token-Tailwind parity
- Output: Complete Tailwind config extension + CSS variable declarations + dark mode implementation

### 4. motion-designer
Owns animation, transition, and micro-interaction design.
- Applies Material Design Motion Principles: duration (100–500ms), easing (ease-out for exits, ease-in-out for transitions)
- Applies Perceived Performance psychology: skeleton loaders and optimistic UI reduce perceived latency by 40%
- Enforces: `prefers-reduced-motion` media query on ALL animations — accessibility non-negotiable
- Applies Feedback Loop theory: every user action must have visual acknowledgment within 100ms
- Absorbs canvas animation patterns: `community-packs/ui-ux-pro-max/.claude/skills/ui-styling/references/canvas-design-system.md`
- Output: Animation spec (property + duration + easing + trigger) + Tailwind animation classes + CSS keyframes

### 5. accessibility-auditor
Audits and enforces accessibility compliance across all UI styling.
- WCAG 2.1 AA as minimum (AAA for healthcare and government projects)
- Audits: contrast ratios, focus indicators, keyboard navigation order, Maxim labels, screen reader announcements
- Absorbs patterns: `community-packs/ui-ux-pro-max/.claude/skills/ui-styling/references/shadcn-accessibility.md`
- Proactively loops: `compliance` skill for regulated-industry projects
- Output: Accessibility audit report (PASS/FAIL per criterion) + remediation spec

## Maxim Behavioral Framing

**Core Principle:** UI styling is an applied behavioral science. Every visual decision — color, spacing, size, motion — is a behavioral trigger that shapes user action. The best-styled interface is invisible: users achieve their goals without thinking about the interface.

**Framework Selection by Task:**

| Task | Framework |
|---|---|
| Interactive element sizing | Fitts' Law |
| Layout grouping | Gestalt Laws (Proximity, Similarity, Continuation) |
| Cognitive load management | Miller's Law + Cognitive Load Theory |
| Color decisions | Color Psychology + WCAG contrast requirements |
| Animation design | Material Motion + Perceived Performance |
| Accessibility audit | WCAG 2.1 AA + Maxim Authoring Practices Guide |

## Dispatch

| Argument | Agent | External Reference |
|---|---|---|
| `component` | component-builder | `references/shadcn-components.md` |
| `layout` | layout-architect | `references/tailwind-responsive.md` + `references/tailwind-utilities.md` |
| `theme` | theme-engineer | `references/shadcn-theming.md` + `references/tailwind-customization.md` |
| `dark-mode` | theme-engineer | `references/shadcn-theming.md` |
| `animate` | motion-designer | `references/canvas-design-system.md` |
| `audit` | accessibility-auditor | `references/shadcn-accessibility.md` |

## Proactive Agent Loops

- **Always** loop `design-system` skill — Tailwind config must align with token architecture
- Loop `design` skill for visual hierarchy and Gestalt validation
- Loop `engineering` skill for implementation review and performance audit
- Loop `compliance` skill for regulated-industry projects (healthcare, finance, government)

## Confidence Tagging

🟢 HIGH — design tokens exist, framework specified (React/Next.js/Vite), Maxim behavioral layer fully applied
🟡 MEDIUM — no design tokens yet or framework unspecified
🔴 LOW — no design system context (flag: run `design-system create` first)

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
