---
name: fade-glass-by-strength
description: |
  Never fade a `backdrop-filter` layer with `opacity` or a uniform-alpha `mask` — animate its geometry, or the blur radius and tint alpha together. Use when a frosted / glass panel, sheet, toolbar, or overlay enters or leaves and the blur looks dirty, washed out, half-sharp, or double-exposed, when the backdrop's detail stays crisp through a glass surface mid-transition, or when a design asks for "50% opacity glass".
---

# Fade Glass by Strength

## Rule

A layer carrying `backdrop-filter` may only be at `opacity: 1` or `opacity: 0`. To make glass appear
or disappear, animate one of:

- **its geometry** — `transform`, `clip-path`, or size, at full material strength (preferred);
- **its material** — blur radius and tint alpha together, `opacity` untouched.

A uniform-alpha `mask-image` is not a workaround; it composites identically.

## Why

`backdrop-filter` **replaces** what is behind the element with a processed copy of it. `opacity`
**blends** the element back over what is behind it — which is still the unprocessed original. Both at
once means the backdrop is composited twice:

```text
result = α · (blurred backdrop + content) + (1 − α) · sharp backdrop
```

So a partly-transparent glass layer is not less frosted, it is a double exposure: `1 − α` of the
backdrop's original detail survives at full sharpness, on top of a washed copy of the frost. Nothing
physical behaves this way. Real glass fades by scattering less, or by not being there.

Masks lose to the same formula: mask alpha controls **where** the material is, not **how much** of it
there is. That is why a gradient mask reads fine (a narrow falloff band looks like a natural edge)
while a flat 50% mask reads broken.

## Observed

Chromium 2×, panels over 3px hard stripes — a blur turns those flat grey, so crisp stripes prove the
frost is not doing its job. Screenshot comparison, not a pixel metric:

| arrangement                            | stripes inside the panel          | verdict            |
| -------------------------------------- | --------------------------------- | ------------------ |
| `blur(16px)`, tint `.18`, opacity 1    | gone, flat grey                   | correct frost      |
| ...plus `opacity: .5`                  | **crisp, at about half contrast** | double exposure    |
| ...plus uniform `.5` alpha mask        | **crisp, identical to opacity**   | same math          |
| `blur(8px)`, tint `.09`, opacity 1     | gone, flat grey                   | **ship this**      |
| `opacity: .5` over a **flat** backdrop | none to see                       | undetectable, fine |

Two things the transparent versions also lose that the half-strength one keeps: the inset hairline
and the corner radius wash out with everything else, so the panel reads unfinished rather than
translucent. And blur radius saturates early — once the radius passes the backdrop's detail scale,
more radius changes nothing, so the tint alpha is what carries the perceived ramp.

## Pattern

```tsx
// ✗ the whole material fades, backdrop detail bleeds through
<motion.div
  className="backdrop-blur-xl bg-white/20"
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
/>;

// ✓ geometry moves, material stays at full strength
<motion.div
  className="backdrop-blur-xl bg-white/20"
  initial={{ y: "100%" }}
  animate={{ y: 0 }}
/>;

// ✓ or ramp the material itself, one value driving every layer of it
<motion.div
  style={{
    backdropFilter: useMotionTemplate`blur(${useTransform(p, [0, 1], [0, 24])}px)`,
    backgroundColor: useMotionTemplate`rgb(255 255 255 / ${useTransform(p, [0, 1], [0, 0.18])})`,
    borderColor: useMotionTemplate`rgb(255 255 255 / ${useTransform(p, [0, 1], [0, 0.3])})`,
  }}
/>;
```

## Notes

- **Prefer geometry.** It is the cheapest, it is what native sheets do, and it sidesteps every
  compositing question here. Reach for a material ramp only when the surface has to materialise in
  place.
- **A flat backdrop excuses everything.** Blurring a solid colour is a no-op, so over a flat or
  low-contrast backdrop an `opacity` fade is indistinguishable from a correct one — and under about
  150ms nobody resolves the ghost either. Do not add a material ramp to a case that cannot show the
  defect.
- **Ramping the radius re-runs the blur every frame.** It is GPU work proportional to area; measure
  before ramping a full-screen surface, and prefer holding the radius fixed while only the tint alpha
  moves.
- **`blur(0px)` is not `none`.** They do not interpolate between each other, so keep the same filter
  function through the animation and only drop to `none` on completion, to release the layer.
- **Never put the fade on an ancestor.** `opacity < 1` on an ancestor is a different and worse bug:
  it forms a backdrop root, so the blur samples only inside that ancestor and vanishes entirely.
  `preserve-backdrop-filter` covers that case.
- Verified in Chromium only. The compositing order is spec-defined, so the artefact should be
  universal, but the exact look over a given backdrop is worth checking per engine.

## Sources

- Filter Effects Module Level 2, `backdrop-filter`:
  <https://drafts.fxtf.org/filter-effects-2/#BackdropFilterProperty>
- Compositing and Blending Level 1, simple alpha compositing:
  <https://drafts.fxtf.org/compositing-1/#simplealphacompositing>
