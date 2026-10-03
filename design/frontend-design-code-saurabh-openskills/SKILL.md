---
name: frontend-design
description: Design and implement distinctive, production-ready web interfaces. Use when creating or substantially redesigning a page, component, dashboard, marketing site, or product UI; when choosing visual direction, typography, layout, responsive behavior, states, or accessibility; or when an existing interface feels generic, inconsistent, or poorly structured.
---

# Frontend Design

Create an interface with a clear point of view that serves its users and works in the existing product. Do not default to fashionable AI-generated aesthetics, decorative effects, or a familiar component-library layout when they are not justified by the brief.

## 1. Establish the brief

Before changing code, identify or explicitly state:

- **Subject:** What is being designed?
- **Audience:** Who uses it and what do they need to understand or do?
- **Primary job:** What is the one most important outcome for this page or flow?
- **Context:** Is this a new surface, an extension of an established product, or a redesign?
- **Constraints:** Existing design system, brand rules, framework, content, assets, browser support, and deadline.

For an existing product, inspect the relevant routes, components, styles, tokens, assets, and UI conventions first. Preserve purposeful conventions; do not introduce a parallel design system merely to make the page look new.

If a decision is genuinely blocked by missing product information, ask one focused question. Otherwise, make a stated, reversible assumption and proceed.

## 2. Set a deliberate visual direction

Write a compact design plan before implementation. Include:

- **Concept:** One sentence that ties the design to the subject, not a visual trend.
- **Hierarchy:** What a person sees first, second, and next.
- **Tokens:** A restrained palette (4–6 named colors), type roles, spacing rhythm, radii, borders, and shadows.
- **Layout:** Content regions, reading order, breakpoints, and an ASCII wireframe when the page is structurally complex.
- **Signature:** One memorable but useful element—such as a data treatment, interaction, visual metaphor, or editorial composition.
- **Motion:** The few interactions or transitions that clarify state or add atmosphere. Respect `prefers-reduced-motion`.

Choose typography for role and readability. Pair display, body, and utility styles intentionally; establish a type scale and use it consistently. Use familiar defaults only when they suit the product and audience, not because they are easy.

Avoid making every brief converge on cream-and-serif editorial layouts, dark pages with neon accents, gradients, floating glass cards, excessive rounded rectangles, or generic hero-stat layouts. Use any of these only when the content and brand support the choice.

## 3. Design the complete experience

Model the real content and task flow before polishing the happy path.

- Put the primary action where it is expected and describe it with a specific verb.
- Use labels and headings that reflect user language, not implementation language.
- Make structure carry meaning: use groups, dividers, labels, tabs, timelines, and numbered steps only when they represent real relationships.
- Define loading, empty, success, error, disabled, hover, focus, selected, and overflow states where they apply.
- Keep copy concise and operational. A button should describe its outcome; an error should say what happened and what to do next.
- Spend visual boldness in one place. Let surrounding areas remain disciplined enough for content and actions to be clear.

## 4. Implement with the product, not beside it

Build semantic HTML and accessible controls. Reuse existing components and tokens when they fit; extend them deliberately when they do not. Keep styling maintainable by avoiding conflicting selectors, magic-number positioning, and one-off overrides that fight the cascade.

Design responsive behavior intentionally rather than shrinking desktop layouts. At narrow widths, reconsider information order, interaction density, labels, and touch targets. Do not hide essential actions without a clear alternative.

Use motion sparingly and only when it improves orientation, feedback, or comprehension. Do not rely on motion, color, or hover alone to convey meaning.

## 5. Validate before handoff

Render the interface and inspect it at representative viewport sizes. Use screenshots or browser inspection when available. Fix observed issues rather than claiming visual quality from the source alone.

Check keyboard navigation, visible focus, contrast, heading order, form labels, image alternatives, zoom/reflow, and reduced-motion behavior. Test the most important user path and relevant non-happy-path states.

## Definition of Done

Before considering the design complete, verify:

- [ ] The page has a clearly stated user, purpose, and primary action.
- [ ] The visual direction is tied to the subject and does not rely on unexplained default aesthetics.
- [ ] Hierarchy makes the primary content and action easy to find.
- [ ] Typography, colors, spacing, and component treatments follow a coherent token system.
- [ ] The interface uses real or representative content, not filler that hides layout problems.
- [ ] Loading, empty, error, success, disabled, and overflow states are handled where relevant.
- [ ] The layout works at mobile, tablet, and desktop widths without clipped content or lost actions.
- [ ] All controls work with keyboard navigation and have visible focus states.
- [ ] Contrast, labels, semantics, and non-color cues support accessible use.
- [ ] Motion is purposeful and reduced-motion preferences are respected.
- [ ] The implementation reuses or carefully extends the existing design system and does not add avoidable CSS conflicts.
- [ ] The implemented result has been visually inspected and the primary flow has been tested.

## Handoff

Summarize the design direction, key implementation decisions, assumptions, responsive behavior, and any remaining trade-offs. Include screenshots or a short validation note when available.
