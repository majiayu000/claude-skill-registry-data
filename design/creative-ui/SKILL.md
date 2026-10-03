---
name: creative-ui
description: Produce distinctive, accessible UI that belongs to the existing design system — not generic AI output. Use whenever building or restyling any visible component, page, or layout. Reads the existing component system and design tokens first so new UI integrates seamlessly.
---

# Creative UI

Read `learnings.md` beside this file before starting; append an entry when a design intent line or token decision proved notably right or wrong.

## Governing Principle

> **Intentional restraint over decorative excess.** Every visual choice serves the product's character. Typography carries the hierarchy, whitespace creates breathing room, motion is earned — never applied for its own sake. The result should feel like a considered design, not a template.

## Procedure

1. **Discover** the existing design system before touching any styles:
   - Read the project's CSS tokens / theme file (the source of spacing, color, and typography scales).
   - Read the shared primitive components directory (Button, Card, Input, Modal, Spinner, etc.).
   - Read the two closest sibling components to where you're working.
   - New UI must look like it was always part of the application.

2. **Articulate** the design intent in one line before writing code (e.g., "reading a considered post, not scrolling a slot machine"). If you can't state the feeling, the output will be generic.

3. **Scaffold** the component using discovered primitives and tokens. If a primitive is missing (e.g., Modal, Toast), propose adding it to the shared primitives directory — never inline a one-off.

## Constraints (non-negotiable)

- **Tokens over arbitrary values.** Spacing, radius, and color come from the existing scale. A hardcoded pixel value or hex color requires a written justification.
- **Avoid the AI-generated look:** no gradient-hero-on-white, no emoji as section markers, no identical rounded-shadow cards everywhere, no centered-everything-with-no-hierarchy.
- **Typography carries the design.** Set a real scale (size + weight + line-height per level) and stay on it; body text ~65ch max-width; headings with balanced text-wrap.
- **Motion is earned.** One deliberate transition per surface beats scattered hover effects. Respect `prefers-reduced-motion`. Nothing loops forever.
- **Both themes are first-class.** Every new color decision is made as a token pair, verified on both light and dark backgrounds.
- **Accessibility is part of the look:** real `<button>`/`<a>` elements, visible focus states (never bare `outline-none`), labeled inputs, meaningful `alt` text, 4.5:1 contrast ratio minimum.
- **Media discipline:** images reserve aspect-ratio space before load (no layout shift); multi-image layouts handle 1–n images gracefully; text over images gets a scrim.
- **Conditional classes** via the project's utility function — never template-string class concatenation.

## Definition of Done

- [ ] Uses/extends shared primitive components
- [ ] All four states designed (loading skeleton, empty, error, content — per `/web-design-patterns`)
- [ ] Holds at 360px width and at desktop
- [ ] Keyboard path works; focus visible
- [ ] Both themes checked
- [ ] No arbitrary values without justification

## Handoffs

- Behavior/data questions while styling → `/web-design-patterns`.
- The surface needs a new server capability → stop, run `/system-design` first.
- Finished → `/full-review` (ui-reviewer + ux-reviewer agents check this skill's rules).
- Don't understand why a rule exists → `/teach <the rule>`.
