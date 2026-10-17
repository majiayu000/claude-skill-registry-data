---
name: apply-kinetic-continuity-motion
description: Applies the Kinetic Continuity motion language when planning, building, or reviewing a GSAP demo or interface that needs natural, smooth editorial spatial motion. Use for image fields, galleries, carousels, contact-sheet transitions, anchored previews, path-based sequences, or restrained kinetic typography; do not use for unrelated animation tasks with no continuity or spatial-state problem.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: refactor
  audience: frontend-developers-and-creative-technologists
  tags:
    - motion-design
    - gsap
    - interaction-design
    - spatial-continuity
    - reduced-motion
    - performance
  status: draft
  side_effects: file-write
---

# Apply Kinetic Continuity Motion

## Purpose

Apply a restrained motion language that gives a layout physical memory: elements remain identifiable, respond to the user's energy, and settle where the next decision can be made.

Treat supplied reference videos as evidence for a design language, not as templates to reproduce. Preserve the user's requested concept, technology, scope, and authorization boundary. Apply file changes only when the user asks for implementation; for planning or review requests, return guidance without editing files.

## When to use this skill

Use this skill when:

- A GSAP demo or web interface needs continuity across spatial or layout states.
- The task involves an image field, gallery, carousel, contact sheet, anchored preview, path-based sequence, routed group, or restrained kinetic typography.
- Existing motion feels disconnected, stale under rapid input, overly decorative, or unclear about object identity.
- The user wants to translate supplied motion references into an original, accessible, and implementable interaction language.

Do not use this skill when:

- A simple hover, focus, press, or opacity change can be handled with an ordinary CSS transition.
- The request is an unrelated animation task with no continuity or spatial-state problem.
- The task concerns film, video editing, or character animation rather than interface behavior.
- The user needs a comprehensive accessibility audit rather than motion-specific planning, implementation, or review.

## Inputs to inspect

Inspect the smallest relevant set of available inputs:

- The requested user task, trigger, subject, start state, and target state.
- Relevant components, templates, styles, motion utilities, tests, demos, and documentation.
- Existing animation dependencies, especially GSAP plugins already in use.
- User-supplied videos, prototypes, screenshots, storyboards, or motion-analysis notes.
- Responsive behavior, pointer and touch behavior, keyboard paths, focus behavior, and reduced-motion requirements.
- Performance constraints such as repeated items, image weight, geometry measurement, and high-frequency input.

Do not assume reference media, GSAP plugins, or project conventions exist when they are not present.

## Reference routing

Read [references/pattern-catalog.md](references/pattern-catalog.md) when selecting a motion primitive, tuning timing and easing, defining reduced-motion behavior, or reviewing naturalness.

The catalog is self-contained. If a task requires per-video provenance or comparison with a named clip, inspect the reference media or motion-analysis document supplied in that task's workspace rather than assuming details from this skill.

## Core motion contract

- Preserve object identity through position, scale, and layout changes.
- Give each motion beat one dominant direction.
- Make neighboring elements respond as one spatial field, with related velocity and distance-based stagger.
- Respond to direct input on the next painted frame. Apply easing to the settle, not the grab point.
- Accelerate briefly and spend more of the duration decelerating.
- Overlap outgoing and incoming states enough to avoid a dead frame.
- Use scale consistently to communicate focus, depth, or priority.
- Resolve active passages into stable, readable rest states.
- Keep expressive distortion brief, local, reversible, and non-essential.

Prefer continuity over spectacle. Remove motion that does not explain state, hierarchy, orientation, or feedback.

## Select one primary primitive

Choose the primitive that best explains the state change. Do not combine several simply to increase visual novelty.

- **Inertial field:** a pannable or drifting constellation that moves as one system.
- **Parallel rails:** repeated media tracks with restrained speed variation.
- **Routed groups:** clusters moving between visible lanes or categories.
- **Anchored preview exchange:** a stable index controls a bounded preview region.
- **Curved procession:** cards derive position, scale, and stacking from one path-progress value.
- **Converging chain:** an overview bends and scales into a focused composition.
- **Contact-sheet resolve:** retained items bridge dense and curated layouts.
- **Bounded text disruption:** display text briefly offsets and then cleanly reconstructs.

Use ordinary CSS transitions when the interaction needs only a simple hover, focus, press, or opacity change.

## Workflow

1. Confirm whether the request is planning, implementation, or review, and preserve that boundary.
2. Identify the trigger, subject, start state, target state, and user task.
3. Write a one-sentence motion thesis that explains why motion exists.
4. Choose one primary primitive and define its stable start and end compositions.
5. Define the reduced-motion state before adding full choreography.
6. Establish micro, meso, and macro hierarchy. Not every element needs motion at every layer.
7. Implement or specify direct response, coordinated travel, and a quiet settle.
8. Make rapid input retarget the current rendered state instead of queuing animations.
9. Verify pointer, touch, keyboard, focus, reduced motion, interruption, and failure paths.
10. Review at normal speed and frame-step or `0.25x` speed to find discontinuities and stacking errors.
11. When implementation was requested, run the repository's relevant tests or checks and report manual validation that remains.

## Timing signature

Use the reference tokens as starting points, then adjust modestly for travel distance and interaction frequency:

- Immediate acknowledgement: about `90ms`.
- Hover or focus: about `180ms`.
- Compact state change: about `320ms`.
- Layout reconfiguration: about `520ms`.
- Large spatial scene: about `780ms`, normally capped below `1000ms`.
- Spatial stagger: `35–60ms`, ordered by distance from the motion source.

Prefer `power3.out` for standard settling, `power4.out` for a stronger editorial entrance, and `power2.inOut` for known-state reconfiguration. Use linear motion only when progress follows scroll, drag, or another continuous input.

Do not make elastic or back easing the system signature. If a release snap needs overshoot, keep it below roughly `3%`.

## Implementation invariants

- Use CSS for simple state transitions and GSAP timelines for coordinated sequences.
- Use GSAP Flip for real layout changes when shared-element continuity is valuable.
- Use Draggable only when drag is a real interaction and equivalent visible controls exist.
- Use ScrollTrigger only for a genuine scroll narrative; do not introduce scroll-jacking.
- Derive curved motion properties from one normalized progress value so `x`, `y`, scale, opacity, and stacking do not drift apart.
- Use `overwrite: "auto"`, `quickTo()`, or one progress-driven timeline for interruptible motion.
- Animate `transform` and `opacity` first.
- Batch DOM reads, cache geometry, and avoid measurement inside high-frequency updates.
- Apply `will-change` only during active motion and remove it after large one-off sequences where practical.
- Keep final content available if JavaScript fails. Do not require an entrance timeline to reveal essential content.

Follow the repository's existing HTML, CSS, JavaScript, asset, and demo-documentation conventions. Do not add or replace an animation dependency without user authorization.

## Interaction and accessibility invariants

- Match hover with focus and click or tap behavior.
- Keep focus styling visible and at least as clear as hover.
- Preserve semantic source order when visual items become spatial.
- Keep one intact readable text source for split or disrupted typography.
- Make drag, swipe, and wheel optional input methods; provide previous and next controls or another keyboard path.
- Cancel momentum when a new gesture begins.
- Pause continuous motion during meaningful interaction and when the page is not visible.
- For `prefers-reduced-motion: reduce`, remove inertia, orbiting, autoplay, zoom travel, and text disruption. Preserve content and selection with instant changes or a short opacity transition.
- Do not claim accessibility compliance without testing.

## Review standard

Flag motion when it:

- teleports or replaces objects that should remain identifiable;
- uses random stagger without a spatial source;
- queues stale hover states;
- remains in constant motion beside reading content;
- makes scale decorative rather than meaningful;
- depends on drag, hover, or animation to expose essential content;
- creates layout work on each animation frame;
- transforms a sticky owner instead of an inner scene layer;
- is longer or more elaborate than the state change warrants.

## Output format

Return the mode-appropriate result:

### Planning

- Motion thesis and selected primitive.
- Start, transition, and settled states.
- Motion hierarchy, timing, interruption, and reduced-motion behavior.
- Accessibility, performance, implementation, and validation notes.

### Implementation

- Summary of the applied motion behavior.
- Files changed and the role of each change.
- Selected primitive, motion hierarchy, reduced-motion result, accessibility behavior, and performance strategy.
- Tests or checks run and any manual checks that remain.

### Review

| Priority | Issue | Evidence | Recommendation |
|---|---|---|---|

Also report the inferred primitive, motion hierarchy, reduced-motion result, accessibility behavior, performance strategy, and any evidence limits.

## Quality bar

The task is complete only when:

- The chosen primitive explains the state change more clearly than a simpler transition would.
- Object identity, direction, response, interruption, settle, and rest are coherent.
- Full-motion and reduced-motion states preserve the same content and task outcome.
- Pointer, touch, keyboard, and focus behavior have equivalent usable paths where applicable.
- High-frequency motion avoids repeated layout measurement and stale queued states.
- Review findings cite concrete interface states, code, or observable behavior.
- Implementation work follows project conventions and includes proportionate validation.

## Edge cases

- If the project does not use GSAP, preserve its existing stack unless the user asks to add GSAP; express the same principles with the available platform APIs or provide a plan.
- If reference media is unavailable, use the bundled pattern catalog and disclose that no clip-specific comparison was performed.
- If several state changes need different primitives, choose one primary primitive per state change and keep shared timing and physical rules consistent.
- If animation fails or JavaScript is unavailable, essential content and controls must remain usable.
- If a sticky or scroll-owned element must appear to transform, animate an inner scene layer instead of the sticky owner.
- If a concept conflicts with reduced-motion, keyboard, or content-access requirements, preserve the task outcome and state relationship while simplifying the choreography.

## Related skills

- `motion-behavior-planner` for a library-neutral motion plan without implementation.
- `motion-experience-director` for a broader site-wide motion system.
- `motion-animation-accessibility-audit` for a comprehensive motion accessibility audit.
- `creative-technologist` for wider frontend feasibility and progressive-enhancement planning.
