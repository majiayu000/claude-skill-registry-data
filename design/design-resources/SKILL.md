---
skill_id: design-resources
name: Design Resources
description: "Curated design reference library for Maxim design work — typography scales, color systems, component patterns, spacing and layout references. Consulted by the other design skills rather than invoked directly."
version: 1.0.0
category: design-resources
office: CPO
lead_agent: ui-ux-designer
supporting_agents:
  - ui-designer
  - frontend-developer
  - accessibility-auditor
  - brand-guardian
activation:
  - auto-loaded when any design task activates
  - /mxm-design triggers
  - referenced by design/, brand/, design-system/, ui-styling/, ui-ux-pro-max/ skills
tags:
  - design
  - typography
  - color
  - components
  - animation
  - accessibility
  - critique
  - brand-library
  - design-md
---

# Design Resources — Curated Reference Library

> Practical values, ratios, checklists, and patterns consumed directly by all CPO office design agents.

## Purpose

This skill provides a curated design reference library for all Maxim design agents. It contains typography scales, color systems, component patterns, animation specs, accessibility checklists, critique frameworks, and the 9-section DESIGN.md standard template.

Design agents do not need to memorize design fundamentals. They load the relevant reference from this library and apply it to the task context with Maxim behavioral framing.

## Sub-Resources Routing Table

| Resource | Path | Use When |
|---|---|---|
| DESIGN.md Template | `DESIGN.md` | Starting a new project's design system, defining visual identity |
| Typography | `references/typography.md` | Font selection, type scale, line height, responsive text |
| Color Systems | `references/color-systems.md` | Palette creation, semantic naming, dark mode, contrast |
| Component Patterns | `references/component-patterns.md` | Building UI components, form design, navigation, data display |
| Animation & Motion | `references/animation.md` | Micro-interactions, transitions, loading states, easing |
| Accessibility | `references/accessibility.md` | WCAG compliance, focus management, Maxim roles, screen readers |
| Critique Frameworks | `references/critique-frameworks.md` | Design reviews, heuristic evaluation, anti-pattern detection |
| Brand Design Library | `references/brand-library.md` | Brand-inspired UI, "build like [brand]", match a known brand aesthetic |

## Dispatch Rules

1. **Typography task** — load `references/typography.md` + project DESIGN.md (if exists)
2. **Color task** — load `references/color-systems.md` + project DESIGN.md (if exists)
3. **Component task** — load `references/component-patterns.md` + relevant design-system tokens
4. **Animation task** — load `references/animation.md` + project motion preferences
5. **Accessibility audit** — load `references/accessibility.md` + all relevant component specs
6. **Design review / critique** — load `references/critique-frameworks.md`
7. **New project design setup** — provide `DESIGN.md` template for project customization
8. **Brand-inspired UI** — look up brand in `references/brand-library.md` → load `community-packs/design-templates/design-md/[brand]/README.md` → apply as project DESIGN.md

## Brand Design Library (awesome-design-md)

59 production-grade DESIGN.md files from real brand websites, following the Google Stitch 9-section format. Each captures a brand's complete visual identity: color palette, typography, component styles, layout, elevation, responsive behavior, and agent prompt guide.

**Source:** `community-packs/design-templates/` (VoltAgent/awesome-design-md)
**Catalog:** `references/brand-library.md`

### Task Signals

Activate this resource when the user says any of:
- "Build UI like [brand]" / "design in [brand] style" / "match [brand] aesthetic"
- "Make it look like Stripe/Linear/Vercel/..." (any of the 59 brands)
- "Use the [brand] design system" / "apply [brand] colors and typography"
- "I want a dark premium UI like Superhuman" (aesthetic-based lookup)

### Available Brands (59)

**AI:** Claude, Cohere, ElevenLabs, Minimax, Mistral AI, Ollama, OpenCode AI, Replicate, RunwayML, Together AI, VoltAgent, xAI
**DevTools:** Cursor, Expo, Lovable, Raycast, Superhuman, Vercel, Warp
**Backend/DevOps:** ClickHouse, Composio, HashiCorp, MongoDB, PostHog, Sanity, Sentry, Supabase
**SaaS:** Cal.com, Intercom, Linear, Mintlify, Notion, Resend, Semrush, Zapier
**Design Tools:** Airtable, Clay, Figma, Framer, Miro, Webflow
**Fintech:** Coinbase, Kraken, Revolut, Stripe, Wise
**Consumer:** Airbnb, Apple, IBM, NVIDIA, Pinterest, SpaceX, Spotify, Uber
**Automotive:** BMW, Ferrari, Lamborghini, Renault, Tesla

### Routing

1. Look up brand name in `references/brand-library.md`
2. Load full DESIGN.md from `community-packs/design-templates/design-md/[brand]/README.md`
   - Note: local README.md files link to hosted versions at `https://getdesign.md/[brand]/design-md`
   - For full design tokens, fetch from the getdesign.md URL or use the local file as a pointer
3. Copy the DESIGN.md content into the project's `DESIGN.md` file
4. Use it as the design system source for all UI generation

### Usage Pattern

```
User: "Build me a dashboard that looks like Linear"
Agent:
  1. Load community-packs/design-templates/design-md/linear.app/README.md
  2. Fetch full DESIGN.md from https://getdesign.md/linear.app/design-md
  3. Apply: ultra-minimal, precise, purple accent, dark theme
  4. Generate UI components following Linear's design tokens
```

## Integration with Other Skills

- **design/** — imports typography, color, and component references
- **design-system/** — imports component-patterns and color-systems for token architecture
- **brand/** — imports color-systems and typography for brand identity
- **ui-styling/** — imports all references for implementation guidance
- **ui-ux-pro-max/** — orchestrates all references across parallel design sub-domains
- **accessibility-auditor agent** — primary consumer of accessibility reference
- **brand/** — uses brand-library.md to source brand-inspired design systems
- **awesome-design-md** — external library of 59 brand DESIGN.md files at `community-packs/design-templates/`

## Confidence

- 🟢 HIGH — All references are standards-based (WCAG, Material, type scale mathematics)
- References are universal defaults; project-specific overrides live in the project's own DESIGN.md

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
