---
name: web-development
description: "Web apps: HTML, CSS, JS, TS, React, Next.js, shadcn/ui, accessibility, forms, motion, responsive, performance, react-doctor."
---

# Web Development

## Workflow
- Classify request first: UI/design, component implementation, React app work, motion, forms/accessibility, or performance/verification.
- Open most relevant nested guide first, pull deeper references from there as needed.
- Keep design guidance framework-agnostic unless request clearly React-specific.
- Prefer existing design systems, platform APIs, framework features, browser-native behavior over custom wrappers.
- Keep behavior stable unless user asked for behavior change.

## Core Rules
- Reuse existing tokens, components, primitives before inventing new ones.
- Accessibility by default: semantic HTML, keyboard navigation, focus states, reduced motion, appropriate touch targets.
- Prefer fast, purposeful UI over decorative motion in product surfaces.
- Fix root cause, not visual band-aids.
- React-specific diagnostics only when stack is React.
- This parent skill is the only live trigger. Nested guides are documentation, not standalone skills.

## Guide Index
- `design-engineering/guide.md` -> language-agnostic UI design engineering, polish, forms, accessibility, touch, marketing, performance guidance.
- `design-engineering/animations.md` -> motion rules, easing, timing, spring guidance, performance, reduced-motion guidance.
- `design-engineering/PRACTICAL-TIPS.md` -> concrete animation implementation patterns and fixes.
- `react/guide.md` -> React and Next.js implementation and review guidance.
- `react/react-doctor.md` -> when/how to run `react-doctor`, plus interpreting findings.
- `shadcn/guide.md` -> shadcn/ui install/configuration, component docs, theming, registries, framework-specific setup references.

## Common Stacks
- UI polish: `design-engineering/guide.md`
- Motion work: `design-engineering/animations.md` + `design-engineering/PRACTICAL-TIPS.md`
- Forms/accessibility/mobile: `design-engineering/forms-controls.md` + `design-engineering/touch-accessibility.md`
- Marketing pages: `design-engineering/marketing.md` + `design-engineering/aesthetic-direction.md`
- React feature or bug work: `react/guide.md`
- React verification pass: `react/guide.md` + `react/react-doctor.md`
- shadcn/ui setup or component work: `shadcn/guide.md`
