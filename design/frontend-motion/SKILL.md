---
name: frontend-motion
description: "When deciding whether a frontend interaction benefits from motion, or designing or reviewing state, enter/exit, and gesture motion — make movement purposeful, continuous, accessible, and economical."
---

# Frontend Motion

**Motion earns its frames.** Preserve orientation, causality, and direct control;
when they do not improve, prefer no motion.

- Give every motion a purpose—feedback, state indication, orientation,
  explanation, or a bridge across a jarring change—and gate its prominence by
  frequency. Repeated, keyboard, and task-focused interactions need the most
  restraint; delight belongs only where it will not delay work.
- Keep state, enter, and exit motion spatially and causally continuous. Match a
  transform origin to the source when one exists, preserve an object's path and
  identity, and make a reversal or interruption begin from what is visibly on
  screen.
- Choose CSS transitions for explicit, retargetable property changes; use
  keyframes only for bounded authored sequences; use gestures and springs when
  input, velocity, or interruption determines the result. Name every
  transitioned property exactly.
- Prefer native gestures when they fit; preserve scrolling, navigation and input
  semantics. For custom manipulation, track the pointer live, retain its grab
  offset, release capture on completion/cancellation, and choose the endpoint
  from position and velocity rather than a discontinuous snap.
- Hand off a usable reduced-motion path with `frontend-accessibility`, and
  profile motion before trading rendering cost for decoration. Read
  [references/REFERENCE.md](references/REFERENCE.md) for mechanics and the
  compact vocabulary.

When `frontend-design` is installed, use its
[shared review contract](../frontend-design/references/REVIEW.md). Otherwise report
focused motion findings, exact evidence, user impact and verification gaps directly.
Review-only requests stay read-only; do not install siblings or duplicate the full
review schema.
