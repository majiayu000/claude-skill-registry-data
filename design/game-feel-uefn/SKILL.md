---
name: game-feel-uefn
description: Makes actions in a UEFN map feel good with layered feedback from sound, effects and screen text, in proportion to how important the event is. Use when the owner says juice, game feel, punchy, satisfying, feedback, hit marker, reward effect, countdown cue or the map feels flat.
kind: discipline
last_reviewed: 2026-10-30
sources: [original]
---

# Game feel in UEFN

Feedback is layered and proportional: a small event gets one cue, a big event gets several at once. UEFN has no direct time freeze or camera shake, so the feel comes from sound, effects, screen text and short delays.

## When to use
- An action works but does not feel like anything (collect, hit, deliver, win, round end).
- Designing the cues for a reward, a countdown or a failure.

**When not to use:** a performance problem (use `performance-uefn-checklist`), menu or HUD layout (use `uefn-ui-widgets`), the visual effect itself (use `uefn-vfx-niagara`).

## Workflow
1. List the events that matter (pick up, hit, eliminate, deliver, round start, round end, fail). Give each an importance: routine, good, big.
2. Routine: one sound. Good: sound plus a small effect. Big: sound, effect and a line of text on screen, a beat apart.
3. Drive every cue from the event itself with one Subscribe, never from a polling loop.
4. Play it with the sound on and ask: can I tell what just happened with my eyes closed?

## Rules (symptom, cause, remedy)
- Silent success: the event changes the score but nothing plays. Add the sound first, it is the cheapest feedback.
- Machine-gun repeat: the same sound on every event. Rotate two or three variants.
- Everything is loud: every event has the big treatment. Reserve the biggest cue for the one or two events players should remember.
- Late cue: the cue plays after a Sleep or a poll. Trigger it from the event and keep the delay under a quarter second.
- Cue on the wrong player: the effect plays for everyone. Send personal cues to the agent, shared cues to all.
- Input blocked by feedback: a long message covers the screen. Keep text short and short-lived.

Details and a feedback table: `references/feedback-layers.md`.
