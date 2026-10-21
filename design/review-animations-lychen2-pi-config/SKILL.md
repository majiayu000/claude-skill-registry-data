---
name: review-animations
description: Audit an existing interface's animation purpose, timing, interruption, accessibility, and rendering. Invoke explicitly with a component, page, or recording.
disable-model-invocation: true
license: MIT; see LICENSE
---

# Review animations

Run this workflow when the user explicitly requests an animation audit.
Loading another design skill does not start this audit.
Treat the review as read-only unless the user also authorizes repairs.

1. Identify the target and requested behavior from the active task.
2. Read project motion tokens, component primitives, relevant code, and dependencies.
3. Observe the actual interaction in the browser or the supplied recording when available.
4. Review the points below against the product's purpose and project conventions.
5. Return actionable findings ordered by user impact, with file locations and verification evidence.

## Review points

- Purpose: Does motion explain state, acknowledge input, or preserve spatial continuity?
- Frequency: Do repeated actions remain fast and usable?
- Timing: Do duration and easing fit the distance, scale, and existing motion language?
- Continuity: Do origin, enter and exit direction, and overlapping states make sense?
- Interruption: Do reversal, repeated activation, and cancellation preserve the right state?
- Gestures: Are capture, momentum, boundaries, and alternate inputs handled?
- Accessibility: Do keyboard, focus, touch, and reduced-motion behavior remain usable?
- Rendering: Is there observed jank, excessive layout or paint, or unnecessary main-thread work?

Use project-specific values. Evaluate spring and easing choices in the actual interaction.
Verify library and browser behavior before claiming hardware acceleration or a performance regression.
When only code is available, identify runtime questions that need browser checks.
For implementation patterns, discover and load emil-design-eng as needed.

## Findings

For each issue, give location, observed behavior, user impact, and the smallest useful correction.
Use a Before / After / Why table when several concrete changes benefit from comparison.
Separate observed defects from code-based questions that need runtime confirmation.
If repair is authorized, apply the corrections and repeat the affected interactions.
