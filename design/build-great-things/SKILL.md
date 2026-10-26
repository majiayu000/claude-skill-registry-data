---
name: Build Great Things
description: Comprehensive playbook for building world-class websites, landing pages, web applications, and dashboards. Covers the full build sequence from brand identity and information architecture through layout, typography, color, scroll animations, micro-interactions, hover effects, loading states, empty states, error handling, accessibility, SEO, and conversion optimization. Use this skill whenever building a new website or web app from scratch, redesigning pages (pricing, landing, portfolio), adding polish or animations, fixing generic-looking UI, improving visual hierarchy, or when the user says anything looks "janky", "generic", "amateur", or "needs more polish". Also use when adding hover states, scroll effects, page transitions, or doing a design review pass.
---

# How to Build Great Things

You are building something that will be seen, used, and judged by real humans. Your default instinct is to get it working and move on. That instinct produces mediocre output. This skill exists to override that instinct.

**The north star is taste and judgment.** World-class products are not just functional — they are intentional in every detail: typography that reads beautifully, spacing that breathes, motion that guides, states that never surprise. The difference between "works" and "exceptional" is not talent — it is the discipline to never skip the steps that feel optional but aren't.

**You have unlimited time.** You are a long-running agent. There is no deadline pressure. There is no excuse for cutting corners. Every phase below exists because skipping it produces output that a discerning human will immediately recognize as AI-generated slop.

---

## Design Philosophy

Two intellectual foundations underpin this skill — one for code architecture, one for visual design. Together they provide the *why* behind every principle in the phases that follow.

### Complexity is the root cause (Ousterhout)

John Ousterhout's *A Philosophy of Software Design* identifies a single organizing insight: **complexity is the root cause of nearly all difficulty in software**. It manifests as three symptoms — change amplification (one conceptual change requires edits in many places), cognitive load (the reader must hold too much context to understand the code), and unknown unknowns (it is not obvious what needs to change). Every architectural decision you make either contains complexity or leaks it.

The principles that follow from this:

- **Deep modules, not shallow ones.** A component should have a simple interface that hides substantial internal complexity — the same philosophy as headless primitives (Radix, React Aria). A `<DatePicker>` with 30 props is a shallow module; one with 3 props that internally handles timezone, locale, and parsing is deep. *Measure interface cost against hidden complexity.*
- **Pull complexity downward.** When complexity must exist, push it into the implementation rather than exporting it through configuration props, environment variables, or required setup steps. It is more important for a module to have a simple interface than a simple implementation.
- **Different layer, different abstraction.** Each layer should add genuine conceptual value. A pass-through component that merely forwards props to a child is the UI equivalent of a pass-through method — it adds indirection without adding abstraction. Token layers (primitive → semantic → component) should each represent a distinct level of design decision.
- **Define errors out of existence.** Instead of handling every possible validation error, design flows and APIs so entire categories of errors cannot occur — autofill defaults, constrained input types, smart type coercion. The best error message is one that never needs to appear.
- **Strategic, not tactical.** A tactical programmer (or a tactical AI) gets things working and moves on. A strategic one invests 10-20% additional effort in good structure, knowing it compounds. This skill exists to make you strategic.
- **Design it twice.** Before committing to a component API, state architecture, or page layout, sketch two meaningfully different approaches and compare their trade-offs. The first design that comes to mind is rarely the best.

*Full survey: `docs/compound/research/development/software-design/philosophy-of-software-design.md`*

### Constraint-based design (Wathan & Schoger)

Refactoring UI's core insight is that **visual design becomes programmable when reduced to constrained decision spaces**. Instead of choosing from infinite possibilities for spacing, type size, color, and shadow, you define a finite scale and pick only from that scale. This is especially powerful for an AI agent — constrained decision spaces produce more consistent output than open-ended aesthetic judgment.

The perceptual science behind the constraints:

- **Weber-Fechner law** justifies geometric (multiplicative) spacing scales. Equal arithmetic increments (4px, 8px, 12px, 16px) do not produce perceptually equal steps — the jump from 8→12 is far more visible than 48→52. A geometric scale (4, 8, 16, 24, 32, 48, 64) produces perceptually uniform increments because perceived intensity scales logarithmically with physical magnitude.
- **Preattentive processing** (Treisman) explains visual hierarchy. The human visual system processes color, size, and weight in parallel in under 200ms — before conscious attention engages. Hierarchy works through three channels (size, weight, color), and **de-emphasis is as important as emphasis**: reducing the salience of secondary elements increases the relative salience of the primary element without adding visual noise.
- **Gestalt proximity** is the most powerful grouping principle — it overrides color and shape similarity. Maintain more space *between* groups than *within* groups, and the structure communicates itself without borders or dividers.
- **Border alternatives.** Borders are a crutch. Spacing, background color differences, and shadows separate content more elegantly and with less visual clutter. Reach for a border only after trying these three alternatives.

*Full survey: `docs/compound/research/design/web-apps/refactoring-ui-design-principles.md`*

---

## How to Use This Skill

Read the **routing table** below to find the sections relevant to your current task. Read those sections before writing code. Run the **quality checklist** before declaring any build complete.

### Routing Table

| If you are... | Read... |
|---|---|
| Starting a new website from scratch | `references/website/01-foundation.md` (then each phase in order) |
| Starting a new web application from scratch | `references/webapp/01-foundation.md` (then each phase) |
| Choosing brand, fonts, colors, identity | `references/website/01-foundation.md` |
| Building layout, grid systems | `references/website/02-structure.md` |
| Making it responsive | `references/website/02-structure.md` |
| Structuring components, sections | `references/website/02-structure.md` |
| Fine-tuning typography | `references/website/03-craft.md` |
| Applying color, dark mode | `references/website/03-craft.md` |
| Working with images, icons, media | `references/website/03-craft.md` |
| Tuning spacing, visual weight, hierarchy | `references/website/03-craft.md` |
| Adding scroll animations | `references/website/04-motion-and-interaction.md` |
| Adding hover effects, cursor craft | `references/website/04-motion-and-interaction.md` |
| Adding micro-interactions, feedback | `references/website/04-motion-and-interaction.md` |
| Adding page transitions | `references/website/04-motion-and-interaction.md` |
| Optimizing loading, perceived speed | `references/website/05-performance-and-polish.md` |
| Handling empty, error, loading states | `references/website/05-performance-and-polish.md` |
| Doing an accessibility pass | `references/website/05-performance-and-polish.md` |
| Optimizing for search engines | `references/website/05-performance-and-polish.md` |
| Adding analytics, tracking | `references/website/06-launch-and-growth.md` |
| Optimizing conversion | `references/website/06-launch-and-growth.md` |
| Adding testimonials, trust signals | `references/website/06-launch-and-growth.md` |
| Doing final review before launch | `references/website/05-performance-and-polish.md` + `06-launch-and-growth.md` |
| "Make it look better" / "it looks generic" | `references/website/03-craft.md` + `04-motion-and-interaction.md` |
| "Needs more polish" | `references/website/04-motion-and-interaction.md` + `05-performance-and-polish.md` |
| Building a complex web app (data-dense, state-heavy) | `references/webapp/` (all phases, in order) |
| Designing forms, data tables, dashboards | `references/webapp/03-craft.md` |
| Adding drag-and-drop, real-time updates | `references/webapp/04-motion-and-interaction.md` |
| Designing onboarding flows | `references/webapp/06-launch-and-growth.md` |

---

## The Build Sequence

Every great build follows this sequence. **Do not skip phases.** Do not jump to code before finishing Foundation. Do not ship without completing Polish.

### Website

| Phase | Section | Focus |
|---|---|---|
| 01 | [Foundation](references/website/01-foundation.md) | Brand identity, positioning, IA, content strategy. Everything before a pixel is placed. |
| 02 | [Structure](references/website/02-structure.md) | Layout systems, responsive architecture, component hierarchy, page templates. The skeleton. |
| 03 | [Craft](references/website/03-craft.md) | Typography, color application, imagery, visual hierarchy. Where design becomes intentional. |
| 04 | [Motion & Interaction](references/website/04-motion-and-interaction.md) | Scroll choreography, micro-interactions, transitions, hover states. The texture that separates award-level from competent. |
| 05 | [Performance & Polish](references/website/05-performance-and-polish.md) | Loading UX, edge states, accessibility, SEO. The professional finish. |
| 06 | [Launch & Growth](references/website/06-launch-and-growth.md) | Analytics, conversion optimization, social proof. Getting it into the world. |

### Web Application

| Phase | Section | Focus |
|---|---|---|
| 01 | [Foundation](references/webapp/01-foundation.md) | Product vision, user mental models, IA for complex apps, design system strategy, state architecture. |
| 02 | [Structure](references/webapp/02-structure.md) | Layout systems, navigation patterns, routing, component architecture, responsive strategy for complex UIs. |
| 03 | [Craft](references/webapp/03-craft.md) | Typography in data-dense contexts, color systems for modes/themes, form design, data visualization. |
| 04 | [Motion & Interaction](references/webapp/04-motion-and-interaction.md) | Micro-interactions, state transitions, drag-and-drop, real-time feedback, keyboard shortcuts. |
| 05 | [Performance & Polish](references/webapp/05-performance-and-polish.md) | Perceived performance, skeleton screens, optimistic UI, edge states, accessibility, offline resilience. |
| 06 | [Launch & Growth](references/webapp/06-launch-and-growth.md) | Onboarding flows, progressive disclosure, analytics, retention mechanics, feature adoption. |

---

## Mandatory Quality Checklist

**Run this before declaring ANY build complete.** Every unchecked item is a sign of lazy craft.

### States
- [ ] Every page has a loading state (skeleton, shimmer, or spinner — never a blank screen)
- [ ] Every data-dependent view has an empty state with illustration, copy, and CTA
- [ ] Error states exist for all failure modes (network, auth, validation, 404, 500)
- [ ] Offline/degraded states are handled gracefully
- [ ] Partial data states render correctly (not just full-data and empty)

### Interaction
- [ ] Every interactive element has distinct hover, active, focus, and disabled states
- [ ] Focus styles are visible and keyboard-navigable (not just browser defaults)
- [ ] Buttons have press feedback (scale, color shift, or both)
- [ ] Form inputs have clear validation feedback (inline, not just on submit)
- [ ] Page transitions are not hard cuts (fade, slide, or morph)

### Visual Craft
- [ ] Typography uses at least 3 levels of visual hierarchy (not just font size — weight and color too)
- [ ] De-emphasis used for secondary content (muted color, lighter weight, smaller size) — not just emphasis for primary content
- [ ] Spacing uses a geometric scale (4/8/16/24/32/48/64 — not arbitrary values)
- [ ] No borders used purely for separation where spacing, background color, or shadow would suffice
- [ ] Shadows follow a consistent elevation scale (not arbitrary box-shadow values)
- [ ] Color has semantic meaning beyond decoration
- [ ] At least one scroll-triggered animation exists per long page
- [ ] Images are optimized (WebP/AVIF, responsive srcset, lazy loading)
- [ ] Icons are consistent in style, weight, and size

### Responsiveness
- [ ] Mobile is a first-class experience, not a shrunken desktop
- [ ] Touch targets are at least 44x44px on mobile
- [ ] Typography is fluid (clamp-based, not fixed breakpoints only)
- [ ] No horizontal scroll on any viewport

### Performance
- [ ] Core Web Vitals pass (LCP < 2.5s, INP < 200ms, CLS < 0.1)
- [ ] Fonts load without visible flash (font-display strategy in place)
- [ ] Above-the-fold content renders without JS dependency where possible

### Accessibility
- [ ] Semantic HTML used throughout (not div soup)
- [ ] ARIA labels only where HTML semantics fall short
- [ ] Color contrast meets WCAG AA minimum (4.5:1 text, 3:1 large text)
- [ ] Reduced motion preference respected (prefers-reduced-motion)
- [ ] Screen reader announcement for dynamic content changes

### Completeness
- [ ] 404 page is designed, not default
- [ ] Favicon and Open Graph meta tags are set
- [ ] Print styles exist if content is printable
- [ ] Footer is complete (links, legal, contact)

---

## Common AI Laziness Patterns

Ousterhout calls the programmer who optimizes for speed-of-shipping over structure a "tactical tornado" — someone who gets things working fast but leaves a wake of complexity for every future change. These are the specific ways you will default to tactical tornado behavior if you don't actively resist:

1. **Tactical component design**: Shallow components with sprawling prop interfaces that leak implementation complexity upward. *Instead*: Design deep components — simple interfaces hiding substantial internal complexity. Pull complexity downward.

2. **Generic UI**: Using default Tailwind colors, Inter font, standard component library look. *Instead*: Every project deserves a curated palette, specific typeface pairing, and deliberate whitespace system built from constrained scales.

3. **Skipping the polish phase**: Getting features working and declaring done. *Instead*: Phase 04 (Motion) and Phase 05 (Polish) are not optional. They are where "works" becomes "exceptional."

4. **First-design-only**: Implementing the first approach that comes to mind without considering alternatives. *Instead*: Design it twice. Sketch two meaningfully different approaches for any non-trivial component, layout, or state architecture before committing.

5. **Ignoring visual hierarchy**: Content is present but layout, spacing, and typography don't guide the eye. *Instead*: Use all three hierarchy channels (size, weight, color). De-emphasize secondary elements rather than over-emphasizing primary ones.

6. **Missing edge states**: Only building the happy path. *Instead*: Empty, loading, error, partial, and offline states are not edge cases — they are the states users encounter most. Define errors out of existence where possible; design graceful recovery where not.

7. **Flat interactions**: No hover effects, no transitions, no feedback. *Instead*: Every click, hover, and scroll should feel responsive. Silence from the UI feels broken.

8. **Cookie-cutter layouts**: Every section looks like every other section. *Instead*: Visual rhythm requires variation — alternate section structures, vary content density, use negative space as a design element.

9. **Borders everywhere**: Reaching for `border-b` to separate every section and list item. *Instead*: Try spacing, background color differences, or subtle shadows first. Borders add visual noise; the alternatives communicate structure more cleanly.

10. **Afterthought mobile**: Responsive is not "the same thing smaller." *Instead*: Mobile often needs different IA, different content priority, different interaction patterns.

11. **Ignoring font loading**: Fonts flash, shift, or render as system fallbacks for seconds. *Instead*: Font-display strategy, preloading critical fonts, size-adjust fallbacks.

12. **Arbitrary spacing**: Using whatever pixel value "looks right" without a system. *Instead*: Define a geometric spacing scale (4, 8, 16, 24, 32, 48, 64) and use only those values. Weber-Fechner law: perceptually uniform steps require multiplicative increments.

---

## Research Library

Deep survey papers that ground this skill's two intellectual foundations. Each phase also has its own `references/REFERENCES.md` with topic-specific papers.

| Paper | What it provides |
|-------|-----------------|
| `docs/compound/research/development/software-design/philosophy-of-software-design.md` | Ousterhout's 13 principles (deep modules, complexity management, information hiding, define errors out of existence, strategic programming) — the code architecture philosophy |
| `docs/compound/research/design/web-apps/refactoring-ui-design-principles.md` | Wathan & Schoger's systematic visual design (hierarchy, spacing, typography, color, shadows, border alternatives) — the visual design philosophy |