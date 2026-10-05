---
name: motion-resilience
description: Test and repair animated interactions under interruption, reversal, repeated input, lifecycle changes, and reduced motion. Use for motion-related state or responsiveness defects, not adding decorative animation.
---

# Motion resilience

Make the interaction remain correct while motion is incomplete or absent. Preserve purposeful motion and the project's existing mechanism; do not judge quality through universal duration or easing rules.

## Establish behavior

Identify the trigger, authoritative state, intended destination, animated properties, focus behavior, and cleanup lifecycle. Determine whether animation completion improperly controls business state, input availability, or removal. Note any deliberate input policy before treating repeated activation as a bug.

Use `assets/interruption-cases.json` to select applicable sequences. Exercise them with existing browser/test tools and isolated data. Use animation lifecycle hooks or controlled clocks for reproducible tests where supported; real-time pointer interactions remain useful for perceived responsiveness.

## Interrupt deliberately

Reverse an action before completion, activate it repeatedly, close or navigate during motion, and reopen when relevant. Observe whether the newest supported intent wins, stale callbacks run, overlays intercept input, focus is lost, or detached elements leave work behind.

Test reduced motion through an actual media preference when available. Verify that state changes, cleanup, and feedback still work when motion is shortened or removed. A zero-duration transition may not emit the event the implementation expects; test the actual lifecycle rather than assuming equivalence.

Use representative input devices and runtime conditions only when available. Do not claim touch testing from mouse clicks or real-device performance from a desktop screenshot. Profile if performance is the reported defect; visual smoothness alone is not a frame-time measurement.

## Fix and recheck

Report findings for review requests; apply scoped repairs when authorized. Prefer interruption-safe behavior, explicit cleanup, and state independent of decorative completion. Preserve meaningful focus entry/restoration and prevent hidden exiting elements from blocking input when appropriate.

Re-run the original sequence, normal completion, the reverse direction, and reduced motion. Add focused regression coverage for a reproduced race or lifecycle defect using the existing stack. Avoid a new animation library when a small correction suffices.

Report event order, timing relative to the transition, final state, focus/input behavior, and limitations. Keep static concerns separate from reproduced failures, and do not manufacture motion defects merely because a style differs from a reference.
