---
name: image-to-code
description: Implement an interface faithfully from supplied or approved images. Triggers on "image to code", "设计图转代码".
---

# Image to Code

## When to use

- Implement an interface faithfully from supplied or approved images.

**Not for:** frontend-design for code-first design; imagegen for images only.

## Steps

1. Inspect references and target dimensions; separate visible layout from unspecified behavior. Generate images only within the agreed workflow.

2. Extract layout, type, colors, spacing and assets; ask about consequential ambiguity rather than inferring interaction from pixels.

3. Implement semantic controls and reusable components in the actual framework, including required responsive and interaction states.

4. Run screenshots at matching dimensions, compare and correct material differences; test core interactions and report fidelity limits.

## Verify

- Comparisons use actual matching viewports; interaction and responsive behavior work without unsupported fidelity claims.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [design-principles.md](../../../references/design-principles.md) — design discipline (CRAP, hierarchy before decoration, design every state, accessibility non-optional)
- [visual-direction.md](../../../skills/03-design/frontend-design/references/visual-direction.md) — shared web variation engine (9 axes, hero scale, composition anchors, anti-slop)
