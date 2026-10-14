---
name: frontend-typography
description: "When frontend text is being chosen, loaded, sized, wrapped, truncated, or reviewed for readable hierarchy, stable values, input behavior, or language and bidi rendering."
---

# Frontend Typography

**Typography is controlled restraint.** Make reading and meaning stable before
making type expressive: each role earns its face, scale step, weight, and line
behavior.

- Choose and load only the font faces, styles, and weights the interface uses;
  retain a compatible fallback and avoid synthetic emphasis unless it is
  intentional. Build a small role-based scale whose visual hierarchy follows
  the content hierarchy.
- Tune line height and measure for the role, not a one-size rule. Decide whether
  each text lane wraps, breaks long tokens, or truncates; truncation of useful
  content needs a way to reach the full value.
- Stabilize changing money, counts, and IDs with tabular figures where supported.
  Inputs should inherit the intended type treatment, keep entered text legible,
  and never make a placeholder carry the label's job.
- Treat language as rendering input: set the appropriate `lang` and direction
  boundary, preserve digit order, isolate mixed-direction values when needed,
  and use punctuation and nonbreaking opportunities deliberately.
- Stress every text policy in narrow lanes with long localized names, money,
  IDs, and labels. `frontend-layout` keeps those lanes shrinkable and reachable;
  this skill keeps their text readable without overflow or accidental loss.

For selected edge cases, read [REFERENCE.md](REFERENCE.md).

When `frontend-design` is installed, use its
[shared review contract](../frontend-design/references/REVIEW.md). Otherwise report
focused typography findings, exact evidence, user impact and verification gaps
directly. Review-only requests stay read-only; do not install siblings or duplicate
the full review schema.
