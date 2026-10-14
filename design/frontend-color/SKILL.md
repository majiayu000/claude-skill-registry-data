---
name: frontend-color
description: "When defining, changing, or reviewing UI color tokens, themes, contrast, gamut, or light/dark/increased-contrast appearances — preserve semantic meaning and verify rendered pairs."
---

# Frontend Color

**Mindset: meaning before paint.** A color is a role in a rendered interface, not
an isolated swatch. Preserve the project's tokens, components, and motion
language; do not migrate an established color notation unless that migration is
explicitly the task.

- Start with the role and state: foreground, surface, border, focus, status, or
  action. One meaning per semantic token; do not borrow a same-looking token
  from another role.
- Measure the *rendered* foreground/background pair, including opacity,
  overlays, gradients, images, and state layers. Check every relevant light,
  dark, and increased-contrast appearance rather than inferring one from
  another. Accessibility requirements belong to `frontend-accessibility` and
  override a decorative color treatment.
- Use a perceptual space such as OKLCH when creating or tuning a palette and it
  fits the existing system: adjust perceived lightness before hue or chroma,
  then remeasure. Keep the project's existing notation for localized work.
- Treat gamut as a delivery constraint. Verify saturated colors in the target
  gamut; provide a deliberate baseline before wider-gamut enhancement, never
  rely on clipping to choose the result.
- Tune dark appearance as its own palette, including chroma and hierarchy; do
  not mechanically invert light tokens. Increased contrast must retain role
  meaning while making separations observable.

For non-obvious compositing and gamut cases, read
[references/REFERENCE.md](references/REFERENCE.md).

When `frontend-design` is installed, use its
[shared review contract](../frontend-design/references/REVIEW.md). Otherwise report
focused color findings, exact evidence, user impact and verification gaps directly.
Review-only requests stay read-only; do not install siblings or duplicate the full
review schema.
