---
name: dsn-handoff
version: 1.0.0
description: Turn a finished design into a developer-ready handoff spec - tokens, every interactive state, responsive breakpoints, and the edge cases mockups never show.
author: matrixx0070
tags: [design, handoff, tokens, states, engineering, responsive]
capabilities: []
---

# Developer Handoff

## When to use
Use this the moment a design is approved and about to be built, or when engineers keep asking "what happens when...". A good handoff kills the back-and-forth by answering the questions before they are asked.

**Not for:** unapproved or still-changing designs (you will spec churn), design-system authoring itself (use dsn-design-system), or accessibility sign-off (use dsn-accessibility-review — though note a11y requirements inline).

## Method
1. **Inventory components.** List each component and variant. *Decision:* map each to an existing design-system component where one exists; only flag as NEW when nothing covers the need — reuse beats invention.
2. **Tokens, not pixels.** Specify color, type, spacing, radius, elevation, motion as named tokens (`color.text.secondary`, `space.4`). Give raw values only where no token exists, and call that gap out explicitly.
3. **Every state.** For each interactive element document default, hover, focus, active, disabled, loading, error, empty, selected. A state you skip is a state that ships broken.
4. **Responsive behavior.** Define breakpoints and what reflows, stacks, hides, or truncates at each. State min/max widths and how text wraps.
5. **Edge cases and data.** Longest/shortest text, zero and overflow counts, missing images, slow network, permission-denied, and RTL if supported.
6. **Interaction and validation.** Trigger, transition, timing, and exact validation copy. *Decision:* if a value is genuinely undecided, list it under Open questions rather than inventing one.

## Example
Handoff for a "Notifications" badge. **Component:** Badge → DS: existing. **Tokens:** bg `color.bg.danger`, text `color.text.inverse`, `space.1` padding. **States:** default (count), empty (hidden at 0), overflow (`99+` above 99). **Edge:** count 1000 → still `99+`. **Open question for eng:** does count poll live or on route change?

## Pitfalls
- Handing off pixel values instead of tokens — the build drifts from the system on day one.
- Documenting only the default state; hover/disabled/loading/error are where bugs live.
- Ignoring content extremes — the design breaks on the longest name and the empty list.
- Silently guessing an undecided value instead of flagging it as an open question.

## Output format
```
# Handoff: <feature>
**Components:** <name> → DS: <existing | NEW>
**Tokens:** element — token/value
**States:** element — default / hover / focus / disabled / loading / error / empty
**Breakpoints:** <bp> — behavior
**Edge cases:** condition — expected behavior
**Interactions:** trigger — result — timing
**Open questions for eng:** ...
```
Leave nothing to guesswork; if a value is undecided, say so explicitly.
