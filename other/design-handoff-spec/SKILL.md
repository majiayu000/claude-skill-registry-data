---
name: design-handoff-spec
description: Use when handing a design over to developers, writing a design spec, handoff document, redlines or annotations for a screen, component or flow, or listing the states, edge cases, responsive behaviour and interactions developers need from a Figma file or mockup.
---

# Design Handoff Spec

## Overview

Developers build what is specified and guess the rest. A handoff spec removes the guessing: every state, edge case, breakpoint and interaction is written down, with exact values or design tokens, and anything not yet decided is listed as an open question instead of being invented.

## Inputs

- The design: Figma frames (via the Figma MCP server if connected), exported screens, or a description.
- The design system or token names, if any (colours, type styles, spacing scale, components).
- Platform and breakpoints (web, iOS, Android; for example 360, 768, 1280).

## Method

1. **Inventory.** List the screens in the flow and, per screen, the components in reading order. Note which are existing design-system components and which are new.
2. **Layout and values.** For each component: size behaviour (fixed, hug, fill), spacing, alignment, type style, colour. Use token names when they exist; use raw values only when there is no token, and mark them `(no token)`.
3. **States.** For every interactive or data-driven component, fill in the states table below. A state that is not designed is an open question.
4. **Content rules.** Minimum and maximum length, what happens to long text (wrap, truncate with ellipsis, tooltip), number and date formats, images that fail to load.
5. **Responsive behaviour.** What changes at each breakpoint: stacking, hiding, column count, font size, navigation pattern.
6. **Interactions and motion.** Trigger, result, duration and easing; what happens on slow network; where focus goes.
7. **Accessibility.** Focus order, keyboard behaviour, accessible names for icon buttons, what screen readers announce on errors and updates, reduced-motion behaviour.
8. **Edge cases** from the checklist below.
9. **Acceptance criteria** that a tester can check, and **open questions** with an owner.

## States checklist

| Component type | States to specify |
|---|---|
| Buttons, links, chips | default, hover, focus, pressed, disabled, loading |
| Inputs | empty, placeholder, filled, focus, error with message, disabled, read-only |
| Lists, tables, feeds | loading, empty (first use and no results), one item, many items, error, partial load |
| Pages and sections | loading, success, error, no permission, offline |
| Overlays (modal, sheet, toast) | open, close, scroll when content is long, what closes it |

## Edge cases checklist

- Very long and very short text: names, titles, translations (German is about 30% longer).
- 0, 1 and many items; the largest realistic number.
- Missing data: no avatar, no image, optional fields empty.
- Slow network and failures: what shows while waiting, retry.
- Permissions: what a user without access sees.
- Small screens, large text settings and zoom to 200%.
- Right-to-left languages, if supported.

## Output

```
# Handoff: <feature or screen>

**Platforms and breakpoints:** <…>
**Design file:** <link and frame names>

## Screens and components
### <Screen name>
| Component | Design system? | Layout | Type | Colour | Spacing |
|---|---|---|---|---|---|

#### States
| Component | State | Looks like | Behaviour |
|---|---|---|---|

#### Content rules
#### Responsive
| Breakpoint | Change |
|---|---|

#### Interactions
| Trigger | Result | Motion |
|---|---|---|

#### Accessibility

## Edge cases
## Acceptance criteria
- [ ] Given <…>, when <…>, then <…>

## Open questions
| Question | Owner | Needed by |
|---|---|---|
```

## Rules

- Never invent a value, colour, copy or state. If the design does not show it, it goes in Open questions.
- Prefer design tokens and existing components over raw values; flag every new component.
- Write behaviour, not implementation: "the list keeps its scroll position when returning from details", not code.
- One spec per flow; keep values in tables so they are easy to scan and check.
- If an input is a screenshot only, say which values are measured from pixels and may be off by a pixel or two.

## Common mistakes

- Specifying only the happy path at one screen width.
- Copying every pixel value when a token exists, so the build drifts from the design system.
- "Loading state: TBD" left with no owner.
- Error states with no error message text.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
