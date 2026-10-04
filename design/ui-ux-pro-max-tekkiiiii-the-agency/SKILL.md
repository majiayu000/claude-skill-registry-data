---
name: ui-ux-pro-max
description: >
  Design-system-first UI/UX skill for generating professional interfaces across
  React, Next.js, Vue, Nuxt, Svelte, SwiftUI, Flutter, and React Native.
  Trigger for UI work: landing pages, dashboards, components, UX improvements,
  visual redesigns, and design-system requests. Balances modern copy-paste ecosystems
  (shadcn/ui, Magic UI-style motion patterns) with equal framework parity and
  accessibility-first implementation.
  Purpose: Generates a complete, implementation-ready design system before UI code
  is written — tokens, component primitives, interaction states, motion, and full
  framework mapping. When to trigger: (1) Building a landing page, dashboard, app UI,
  or component. (2) Improving UX, refreshing visual design, or increasing conversion
  clarity. (3) Building animated UI while preserving accessibility. (4) Design
  system work: tokens, component libraries, design-to-code handoff. (5) Visual
  redesign of an existing interface. (6) Cross-platform work needing parity across
  web and mobile. Key capabilities: Equal-depth mapping for React, Vue, Svelte,
  SwiftUI, Flutter, React Native. WCAG AA accessibility gate with focus visibility
  and reduced-motion fallbacks. Three-tier motion system (minimal/moderate/expressive)
  with fallbacks. Industry guidance for B2B SaaS, fintech, healthcare, e-commerce,
  and AI products. Also for: Design consultation, accessibility audits, design
  token setup. Ideal for: Developers who need quality UI without a dedicated designer,
  or designers wanting a structured hand-off spec.
---

# UI UX Pro Max

Generate a complete, implementation-ready design system before writing UI.

## When Invoked

Use for requests like:
- Build/design a landing page, dashboard, app UI, component system
- Improve UX, refresh visual design, increase conversion clarity
- Build modern animated UI while preserving accessibility

---

## Core Principle: Framework Parity, Not Framework Bias

Use modern React ecosystem patterns as reference material, but always output equally strong guidance for the target stack.

Reference ecosystems:
- **Foundation patterns**: shadcn/ui-style composable primitives
- **Motion pattern references**: Magic UI / Eldora / Kokonut style interactions
- **Inspiration-only sources**: Aceternity/CuiCui visual motifs (verify licensing and implementation independently)

Never output guidance that only works for React when user requests Vue/Svelte/mobile.

---

## Required Workflow (Always)

1. **Classify product context** (industry + user intent + platform)
2. **Pick design direction** (style, motion intensity, information density)
3. **Generate design system spec** (tokens, layout, components, interactions, states)
4. **Map to target framework** (equal-depth implementation notes)
5. **Run UX + accessibility gate** before final delivery

---

## Design System Output Format (Mandatory)

```markdown
PATTERN:
- Page/app structure and section order
- Primary user flow

STYLE:
- Chosen style family
- Why this style matches audience + product
- Accessibility impact of style choice

TOKENS:
- Colors: primary, secondary, accent/CTA, bg, text, muted, semantic (success/warn/error)
- Typography: heading/body/mono pairings + fallback stack
- Spacing scale + radius scale + shadow/elevation scale
- Motion scale: duration/easing/intensity presets

COMPONENT SYSTEM:
- Core primitives
- Composite blocks
- Empty/loading/error states
- Interaction states (default/hover/focus/active/disabled)

MOTION & INTERACTION:
- Motion tier (minimal / moderate / expressive)
- Enter/exit/hover/scroll behaviors
- Reduced-motion fallback behavior

FRAMEWORK MAPPING:
- React/Next
- Vue/Nuxt
- Svelte/SvelteKit
- SwiftUI
- Flutter
- React Native
(Each with concrete equivalent implementation pattern)

AVOID:
- Industry anti-patterns
- Accessibility or performance pitfalls

PRE-DELIVERY CHECKLIST:
- UX, accessibility, responsiveness, and consistency checks
```

---

## Industry Guidance (Representative Categories)

Use these as decision anchors:

| Category | Recommended Traits | Avoid |
|---|---|---|
| B2B SaaS / DevTools | High clarity, structured density, low-noise motion | Decorative-only motion, weak hierarchy |
| Fintech / Banking | Trust palette, explicit feedback states, conservative motion | Playful color chaos, ambiguous CTA hierarchy |
| Healthcare | Calm contrast-safe colors, readability-first layouts | Dense clutter, neon-heavy palettes |
| E-commerce | Strong product hierarchy, conversion CTAs, social proof cadence | Over-animated checkout path |
| Legal / Enterprise | Formal typography, predictable IA, low-variance UI | Trend-chasing visuals over trust |
| Creative / Agency | Expressive visuals with guarded performance budgets | Unbounded animation without fallbacks |
| AI products | Conversation-first IA, transparent system status | Generic templates with no product voice |

---

## Style Families

Use these families and state why selected:
- Minimal / Swiss
- Glass / Frosted layers
- Bento modular
- Editorial typography-led
- Motion-forward storytelling
- Data-dense operational
- Inclusive utility-first

Always tie style to user goals, not aesthetics alone.

---

## Motion System (Cross-Framework)

Define one tier and implement consistently:

### Tier A — Minimal
- 120–180ms transitions, subtle hover/focus
- Best for enterprise, finance, healthcare

### Tier B — Moderate
- 180–280ms, contextual entrance and micro-interactions
- Best for SaaS, dashboards, product marketing

### Tier C — Expressive
- 280–450ms, layered transforms/scroll choreography
- Best for campaigns, portfolios, storytelling surfaces only

Rules:
- Respect `prefers-reduced-motion` (web) and platform motion settings (mobile)
- Motion must communicate hierarchy/state, not decoration
- Cap concurrent animated elements in viewport to preserve performance

---

## Framework Mapping Matrix (Equal Priority)

### React / Next.js
- Component architecture: composable primitives
- Styling: Tailwind + tokenized theme
- Accessibility: Radix/headless primitives where useful
- Motion: Framer Motion or Motion

### Vue / Nuxt
- Component architecture: slots/composables-first patterns
- Styling: Tailwind + design tokens
- Accessibility: headless or native semantic patterns
- Motion: Vue transitions / motion composables

### Svelte / SvelteKit
- Component architecture: lean composable stores + actions
- Styling: Tailwind or scoped styles with tokens
- Accessibility: semantic-first + keyboard flow checks
- Motion: Svelte transitions/animate APIs

### SwiftUI
- Component architecture: reusable Views + modifiers
- Styling: semantic color/text styles + dynamic type
- Accessibility: VoiceOver labels/traits, contrast, hit targets
- Motion: withAnimation + matchedGeometryEffect with reduced motion handling

### Flutter
- Component architecture: composable widgets + theme extension tokens
- Styling: Material 3 token overrides mapped to brand
- Accessibility: semantics tree, text scale, contrast
- Motion: implicit/explicit animations with duration tiers

### React Native
- Component architecture: shared design tokens + platform variants
- Styling: utility/native style system consistency
- Accessibility: TalkBack/VoiceOver labels, role/state hints
- Motion: Reanimated/native animations with reduced motion support

---

## Accessibility & UX Gate (Hard Requirements)

Before final output, verify:
- [ ] Text contrast meets WCAG AA (4.5:1 body, 3:1 large text/UI)
- [ ] Focus visibility and keyboard navigation are complete
- [ ] Tap/click targets meet platform guidance (mobile minimums)
- [ ] Forms include clear validation timing + error recovery
- [ ] Loading/empty/error/success states are explicitly designed
- [ ] Motion has reduced-motion alternatives
- [ ] Responsive behavior validated at key breakpoints/platform classes

---

## Performance Guardrails

- Prefer transform/opacity animations over layout-thrashing properties
- Avoid heavy blur/shadow stacks on low-power/mobile targets
- Use progressive disclosure for dense dashboards
- Keep visual complexity proportional to task criticality

---

## Component Source Policy

When suggesting third-party component patterns:
1. Identify source type: open-source, paid, inspiration-only
2. State integration model: copy-paste vs package
3. Mention dependency implications (animation, icons, primitives)
4. Avoid implying official support outside documented scope

---

## Output Quality Bar

Every response from this skill must include:
1. A clear design rationale linked to user goals
2. A full token + component + interaction spec
3. Equal-depth mapping for the requested framework/platform
4. Accessibility and performance checks passed
5. Concrete next implementation steps
