---
name: motion-design
description: "Animation that explains state changes, never decorates."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, motion]
    category: web
    related_skills: [web-design, micro-interactions]
    web_designer_stages: [components, build]
---

# Motion Design Principles Skill

Use animation only where it communicates: feedback, orientation, attention and continuity. This skill covers timing, easing, which properties to animate, and reduced-motion behaviour. It does not cover micro-interactions in detail — those have their own skill — and it does not cover video or decorative animation, which this skill excludes. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- For state changes, page and modal transitions and scroll reveals.
- When an element appears, disappears or moves and the visitor needs to see where it came from and where it went.
- When motion must be checked against prefers-reduced-motion.
- When an action needs confirmation that the visitor can feel as well as see.
- When a transition must show the relationship between two states, not just swap them.
- Never as decoration that delays the task, and never to animate a change the visitor does not need to follow.
- Not for a static page with no state changes: no motion is the right amount of motion there.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage or stages.
- Tokens are defined, so durations and easings are token values rather than one-off numbers in components.
- The component inventory is known, so the skill can see every state change that needs motion.
- The reduced-motion behaviour is decided as a token-level rule, not per component.

## How to Run

1. For each state change, name one of the four legitimate reasons: feedback, orientation, attention or continuity. If none applies, use no motion.
   - Feedback confirms an action the visitor just took.
   - Orientation shows where an element came from and where it went.
   - Attention draws the eye to a change that matters.
   - Continuity connects two states so the visitor follows the change.
2. Pick the duration from the timing ladder by the size of the change: small feedback, medium change, large or page transition.
   - Small feedback runs 100–200ms.
   - A medium change runs 200–300ms.
   - A large change or page transition runs 300–500ms.
   - Nothing runs longer than 500ms.
3. Pick the easing by direction: ease-out for entering, ease-in for leaving, ease-in-out between states.
   - An entering element decelerates into place.
   - A leaving element accelerates away.
   - An element moving between states eases both ways.
4. Animate transform and opacity only; never animate layout properties.
   - Width, height, top and left force layout work on every frame.
   - Transform and opacity run on the compositor and stay smooth.
5. Respect prefers-reduced-motion: disable or reduce non-essential motion for users who ask for it.
   - Under reduced motion, state changes happen without the animation, and nothing essential is lost.
6. Record the durations, easings and reduced-motion behaviour in the stage record.
   - Record the reason for each animation beside its duration and easing.
7. Re-check after any fix, and record what changed.
   - A changed duration, easing or reason is re-checked against the ladder before the stage closes.
   - The motion recorded is the motion in the final build, not an earlier draft.

## Quick Reference

- Timing by size: 100–200ms small feedback; 200–300ms medium; 300–500ms large and page transitions.
- Maximum: nothing takes more than 500ms.
- Easing: ease-out for entering, ease-in for leaving, ease-in-out between states.
- Properties: transform and opacity only, for performance.
- Reduced motion: always respect prefers-reduced-motion.
- Four legitimate reasons (Material Design): feedback, orientation, attention, continuity.
- Implementation: CSS transitions and keyframes with the duration ladder above.

## Procedure

### 1. What it is

Purposeful animation that communicates: feedback, orientation, attention and continuity (Material Design). Timing by size — 100-200ms small feedback, 200-300ms medium, 300-500ms large/page transitions; ease-out for entering, ease-in for leaving, ease-in-out between states; transform/opacity only for performance; always respect prefers-reduced-motion.

### 2. How Hermes applies it

Hermes animates only for one of the four legitimate reasons, uses CSS transitions/keyframes with the duration ladder above, avoids layout-property animation, and disables/non-essential motion under prefers-reduced-motion.

### 3. What it returns to the stage

- `components` stage record: `inventory` carries the motion for each component — the reason, duration and easing per state change, and the reduced-motion behaviour.
- `build` stage record: `files` carries the CSS transitions and keyframes; `build_log` notes the motion tokens used; `token_drift` must be empty — durations and easings come from tokens.

### 4. Good looks like

Motion is barely noticed consciously; actions feel confirmed, origins/destinations are clear, and nothing takes >500ms.

## Pitfalls

- Motion with no reason: decoration that delays the task and teaches visitors to ignore animation.
- A duration over 500ms: the interface feels slow, and the visitor waits on the animation instead of the result.
- The wrong easing: an entering element that decelerates into place the wrong way, or a leaving element that lingers.
- Animating width, height, top or left: layout work on every frame, jank on modest devices, and layout shift as a side effect.
- Ignoring prefers-reduced-motion: motion that some visitors experience as discomfort or worse, with no way to opt out.
- Motion that hides the origin or destination: the visitor loses track of where an element went, which is the opposite of orientation.
- A scroll reveal on every element: the page animates as the visitor reads, and the reading itself is interrupted.
- Motion that delays the result: an animation that must finish before the visitor can act again.
- Two animations fighting over one element: the state change is unclear because the motion contradicts itself.

## Verification

- Every animation names one of the four legitimate reasons; no animation exists for decoration alone.
- Every duration sits on the ladder (100–200ms, 200–300ms, 300–500ms) and nothing takes more than 500ms.
- Easing matches direction: ease-out entering, ease-in leaving, ease-in-out between states.
- Only transform and opacity are animated; no layout property is animated.
- Non-essential motion is disabled or reduced under prefers-reduced-motion.
- Origins and destinations are clear for every animated change.
- No animation blocks the visitor from acting until it finishes.
- Every animation is recorded with its reason, duration and easing in the component inventory.
- Durations and easings come from tokens; token drift is empty.
- No scroll reveal interrupts reading; no animation runs on a static page with no state change.
- State changes under reduced motion lose nothing essential.
- The build log records the motion tokens used.
- The stage record carries the final transitions and keyframes, not earlier drafts.
- The visual judger checks motion timing and continuity; the a11y judger checks reduced-motion behaviour. The skill does the work and the judgers check it; the skill never grades its own output.

## Coordinator wiring

Loaded by stages: components, build. Returns: `components.inventory` (motion per component: reason, duration, easing, reduced-motion behaviour); `build.files` (transitions and keyframes); `build.build_log` (motion tokens used). Judger boundary: visual judger checks timing and continuity; a11y judger checks prefers-reduced-motion behaviour.
