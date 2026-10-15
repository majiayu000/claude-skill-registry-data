---
name: preserve-backdrop-filter
description: Diagnose and prevent CSS backdrop-filter regressions caused by animated ancestors, Backdrop Root boundaries, and Motion or Framer Motion style retention. Use when frosted glass loses blur during or after opacity, filter, scale, transform, or AnimatePresence animations, or when reviewing animated glass UI.
---

# Backdrop Filter and Motion

## Keep the model straight

`backdrop-filter` samples pixels behind an element only as far as its nearest
**Backdrop Root**. Do not confuse a stacking context or compositing layer with a
Backdrop Root: they overlap, but they are not the same boundary.

Inspect ancestors between the glass element and the intended backdrop. The
Filter Effects Level 2 draft defines a Backdrop Root when an element has:

- `filter` whose computed value is not `none`
- `opacity` below `1`
- a non-`none` mask, `mask-image`, `mask-border`, or `clip-path`
- `backdrop-filter` whose computed value is not `none`
- `mix-blend-mode` other than `normal`
- `will-change` naming a property that would create a Backdrop Root

The document root is also a Backdrop Root. A transform, positioned element, or
`z-index` can create a stacking context without normatively creating a Backdrop
Root. Treat those as separate geometry/compositor suspects, not proof of this
bug, and verify browser behavior where draft-spec conformance may lag.

## Avoid animation traps

- Never animate `filter` or opacity below `1` on an **ancestor** of glass that
  must keep sampling content outside that ancestor.
- Distinguish `filter: none` from `filter: blur(0px)`. Only `none` avoids the
  normative root trigger; a zero-radius filter is still a filter function.
- Animate decorative blur on a descendant inside the glass, such as the icon.
- Animate scale and opacity on the glass element itself when the whole control
  must enter. Its own opacity does not become an ancestor boundary for its own
  backdrop, though it does affect descendants.
- Avoid leaving `will-change: filter`, `opacity`, or `backdrop-filter` on an
  ancestor as a permanent optimization.
- Do not run a CSS `transition` for `transform` while Motion owns scale or
  transform on the same element.

## Account for Motion behavior

Verify the installed Motion version before depending on engine details. In
Motion v12:

- `opacity`, `filter`, and `transform` are WAAPI acceleration candidates.
- Native animations use `fill: "both"`, holding their boundary keyframes.
- On completion, `NativeAnimation` writes the final keyframe to inline style,
  cancels the WAAPI animation, then reports completion.
- `scale` is rendered through the element's `transform` style.
- `AnimatePresence` keeps an exiting element mounted until its exit completes,
  so its Backdrop Root effects remain active throughout exit.

Therefore, fixing only the final frame is insufficient when the animated
hierarchy is wrong during entry or exit. Fix the hierarchy first. If stable DOM
must contain no animation-owned styles, remove `filter`, `opacity`, and
`transform` in `onAnimationComplete` and cover that cleanup with a test.

## Prefer this structure

```tsx
<div className="absolute inset-y-0 flex items-center">
  {/* static ancestor */}
  <MotionGlassButton
    initial={{ opacity: 0, scale: 0.9 }}
    animate={{ opacity: 1, scale: 1 }}
    exit={{ opacity: 0, scale: 0.9 }}
  >
    <motion.span initial={{ filter: "blur(4px)" }} animate={{ filter: "none" }}>
      <ArrowIcon />
    </motion.span>
  </MotionGlassButton>
</div>;
```

Keep every ancestor above `MotionGlassButton` free of animated filter, partial
opacity, masks, blending, and relevant `will-change` declarations.

## Diagnose in this order

1. Inspect computed styles on the glass and every ancestor during entry, stable
   state, and exit—not just after the animation.
2. Find the nearest Backdrop Root trigger from the list above.
3. Inspect `element.getAnimations()` and inline `style` after Motion completes.
4. Move visual blur below the glass or move opacity/scale onto the glass itself.
5. Verify real pixels over a patterned backdrop; DOM assertions alone cannot
   prove that blur rendered.
6. Add regression checks that the positioning ancestor stays free of `filter`,
   `opacity`, and `transform`, and that Motion-owned inline styles are cleaned up.

## Sources

- Filter Effects Module Level 2, “Backdrop Root”: <https://drafts.fxtf.org/filter-effects-2/#BackdropRoot>
- MDN `backdrop-filter`: <https://developer.mozilla.org/docs/Web/CSS/backdrop-filter>
- Motion v12 source paths (implementation details; re-check on upgrades):
  `animation/waapi/utils/accelerated-values`,
  `animation/waapi/start-waapi-animation`, and `animation/NativeAnimation`
