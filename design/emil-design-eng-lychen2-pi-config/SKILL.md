---
name: emil-design-eng
description: Polish UI components and purposeful motion using Emil Kowalski's design engineering principles. Use for feedback, transitions, popovers, tooltips, and gestures.
license: MIT; see LICENSE
---

# Design engineering

Start with the active UI task and the project's design system, components, and dependencies.
Continue that task after loading this skill. If no target is available, request the component or interaction to examine.

## Decide what motion contributes

Identify the state change, user input, expected feedback, and frequency of repetition.
Use motion to explain state, preserve spatial continuity, or acknowledge an action.
Keep frequent keyboard actions immediate. Reduce repeated decorative entrances.
Match the interface's existing duration and easing tokens before introducing new values.
Use short feedback for controls; give larger transitions enough time to remain understandable.
Choose timings from the actual distance, content, and interaction, then inspect them in the browser.

Read [Component and motion patterns](references/patterns.md) before implementing the affected pattern.
Use the relevant sections for buttons, popovers, tooltips, entry and exit, or gestures.

## Choose implementation from the requirement

Prefer CSS transitions for ordinary state changes that may reverse.
Use keyframes for a defined sequence when restart behavior is appropriate.
Reuse existing Motion, GSAP, or native animation APIs when their capabilities solve the task.
For springs, evaluate settling, interruption, and bounce with the actual interaction.
Prefer transform and opacity where they express the intended effect.
Measure layout, paint, compositing, and main-thread work when performance is a concern.
Library version, animation properties, and browser support determine acceleration behavior.

## Review and verify

Inspect the real rendered interaction and exercise repeated activation or reversal.
Check keyboard operation, focus, touch, and reduced motion.
Use slower playback to inspect origins, timing drift, and overlapping states when needed.
For performance findings, cite observed behavior or a trace from the affected browser.
Report each actionable issue with its location, observed behavior, proposed change, and reason.
A short Before / After / Why table works when comparing several concrete changes.
Use /skill:review-animations for a user-requested animation audit.
