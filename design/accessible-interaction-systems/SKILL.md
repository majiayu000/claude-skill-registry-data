---
name: accessible-interaction-systems
description: Design or refactor reusable web UI components, design tokens, and interaction states when keyboard, touch, focus, contrast, or reduced-motion behavior is central. Use for navigation, dialogs, tabs, forms, cards, controls, and component showcases; use motion-choreographer for page-wide animation timelines and creative-web-studio for whole-site direction.
---

# Accessible Interaction Systems

Build components that remain understandable before effects load and when input methods change.

## Choose the contract

1. Name the component's job, state, and primary action.
2. List supported inputs: keyboard, pointer, touch, screen reader, and reduced motion. Identify which are essential.
3. Define the visible states: default, hover, focus, pressed/selected, disabled, loading, error, and success where relevant.
4. Reuse the project's color, type, spacing, radius, and motion tokens. Add a token only when it represents a repeated decision.
5. Keep semantic HTML and native behavior where possible. Add ARIA for actual relationships and states, not decoration.

## Implement

- Keep the control and its label in the DOM. Canvas, shader, video, and transition layers are decorative enhancements.
- Make touch targets comfortable and focus indicators distinct from hover styling. Do not require hover to discover a control.
- For dialogs, tabs, menus, and carousels, define keyboard order, escape/return focus, and inactive-content behavior before animating.
- Use transforms and opacity for short state feedback. Reserve spring motion for direct manipulation or spatial continuity; avoid layout reads in input/scroll loops.
- If `document.startViewTransition()` is used for a state change, update state directly when unsupported or reduced motion is requested.
- Let dark/light and mobile variants change composition, not meaning or keyboard order.

## Verify

Use [the component checklist](references/component-checklist.md) for the selected pattern. Exercise a real keyboard and touch-sized viewport. Check computed contrast, visible focus, reduced motion, disabled behavior, and the no-JavaScript or failed-enhancement state where applicable.

Use [worked examples](references/examples.md) for concrete state tables and verification routes. For complex page choreography, hand off animation ownership to `motion-choreographer`; for a full experience concept, use `creative-web-studio`.
