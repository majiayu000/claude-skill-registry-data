---
name: motion-behavior-planner
description: Plans purposeful UI motion behavior before implementation, including motion intent, triggers, duration and easing relationships, interruption rules, reduced-motion alternatives, and performance boundaries. Use when a user asks to define animations, transitions, microinteractions, page or component motion, interaction feedback, or motion guidelines without immediately writing animation code.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: planner
  audience: frontend-designers-and-developers
  tags:
    - motion-design
    - animation
    - interaction-design
    - reduced-motion
    - performance
  status: draft
  side_effects: none
---

# Motion Behavior Planner

## Purpose

Plan UI motion as a functional behavior system, not decorative animation. Use this skill to define why motion exists, when it starts, how long related motions take, how motion responds to interruption, how reduced-motion users are served, and which performance boundaries implementation must respect.

## When to use this skill

Use this skill when:

- The user asks for an animation, transition, motion system, microinteraction, or interaction feedback plan.
- A feature needs motion decisions before CSS, JavaScript, timeline, or library implementation.
- Existing motion feels inconsistent, slow, distracting, inaccessible, or performance-heavy and needs a behavioral plan.
- A UI flow needs page transitions, component entrance or exit motion, loading feedback, drag or gesture feedback, hover or press feedback, disclosure motion, or status-change motion.

Do not use this skill when:

- The user only needs finished animation code and already supplied complete motion specs.
- The task is a visual style review without interaction or temporal behavior.
- The primary problem is layout responsiveness rather than temporal behavior.
- Motion would hide a usability, accessibility, or information-architecture problem that should be solved directly.

## Inputs to inspect

Inspect relevant context such as:

- User goals, product tone, brand constraints, and target platform.
- The affected user flow, component, page, state diagram, or storyboard.
- Existing design files, prototypes, screenshots, videos, or implementation files.
- Current CSS transitions, animation keyframes, JavaScript animation code, motion libraries, or design tokens.
- Accessibility requirements, especially reduced-motion expectations and focus or keyboard behavior.
- Performance constraints such as low-end devices, animation frequency, list sizes, viewport changes, and expected rendering load.

## Workflow

1. Identify the motion scope: list the screens, components, states, and user actions affected by the plan.
2. Define the motion purpose for each moment: orientation, continuity, causality, feedback, hierarchy, delight, status communication, or error prevention.
3. Remove unjustified motion: mark any motion that lacks a user-facing purpose as optional or avoid.
4. Map triggers and preconditions: specify whether motion starts from user input, state change, navigation, data loading, validation, system event, viewport change, or time-based sequencing.
5. Define start and end states: describe position, scale, opacity, elevation, blur, color, content, focus, and layout changes only as needed for implementation clarity.
6. Plan duration relationships: assign relative timing tiers such as instant, quick feedback, standard transition, complex spatial transition, or background ambient motion; ensure nested and dependent motions feel related.
7. Choose easing intent: describe whether motion should feel responsive, physical, calm, sharp, elastic, or restrained; avoid naming exact curves unless the project already has tokens.
8. Specify sequencing: decide what runs together, what waits, what must complete before user comprehension, and what should never block interaction.
9. Define interruption behavior: specify what happens when the user reverses, repeats, navigates away, scrolls, changes focus, resizes, or triggers another action mid-motion.
10. Define reduced-motion behavior: preserve meaning while reducing or replacing movement with opacity, instant state changes, static affordances, shorter durations, or non-motion feedback.
11. Set performance boundaries: prefer compositor-friendly properties where possible, avoid layout-thrashing animation, cap concurrent animations, avoid heavy effects on large surfaces, and define graceful degradation.
12. Identify implementation handoff details: name motion tokens, affected components, states, events, test scenarios, and any decisions still needing design or engineering confirmation.
13. Validate the plan against accessibility, responsiveness, latency, and usability expectations before recommending implementation.

## Output format

Return the result using this structure:

```md
## Summary

Briefly state the intended motion direction and the highest-risk decisions.

## Motion inventory

| Element or flow | Motion purpose | Trigger | Start state | End state |
|---|---|---|---|---|

## Timing relationships

| Motion | Duration tier | Easing intent | Sequencing relationship |
|---|---|---|---|

## Interruption rules

- ...

## Reduced-motion plan

- ...

## Performance boundaries

- ...

## Implementation handoff

- Components or files likely affected:
- Tokens or constants to define:
- Tests or checks to run:
- Open decisions:
```

If reviewing existing motion, add:

```md
## Findings

| Priority | Issue | Evidence | Recommendation |
|---|---|---|---|
```

## Quality bar

The task is complete only when:

- Every proposed motion has a clear user-facing purpose.
- Triggers, start states, end states, and completion states are explicit enough for implementation.
- Duration tiers and sequencing relationships are consistent across related motions.
- Interruption and repeated-trigger behavior is defined.
- Reduced-motion behavior preserves meaning without relying on large movement.
- Performance boundaries identify risky properties, surfaces, frequency, or concurrency.
- The plan separates must-have functional motion from optional polish.

## Edge cases

- If motion communicates critical state, provide a non-motion cue as well.
- If the component can appear in dense lists, tables, or repeated cards, define stricter performance and concurrency limits.
- If the user can trigger the motion rapidly, define debouncing, reversing, cancellation, or state snapping behavior.
- If the flow includes keyboard or assistive technology users, ensure focus order and announcements do not depend on animation timing.
- If network latency affects the experience, distinguish loading feedback from transition polish.
- If the project already has motion tokens, align to them instead of inventing new timing values.

## Related skills

- `interface-state-coverage-review`
- `responsive-behavior-planner`
- `ui-design-direction-builder`
