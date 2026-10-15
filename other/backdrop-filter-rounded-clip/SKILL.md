---
name: backdrop-filter-rounded-clip
description: |
  Inside a rounded `overflow: hidden` frame, keep translucent colour off the element that carries `backdrop-filter` — split the material into a tint layer and a blur layer. Use when a frosted / glass bar, sheet header, toolbar, or overlay sits at the edge of a rounded card and a bright 1px hairline traces the corner curve, when a blurred layer's edge shows a second arc of the wrong radius inside the corner, or when reaching for `mask` / `isolation: isolate` / `opacity` to "clip everything at once" and the blur then stops blurring.
---

# Backdrop Filter Rounded Clip

## Rule

In a frame rounded with `border-radius` + `overflow: hidden`, the element carrying translucent
**colour** must not be the element carrying `backdrop-filter`. Use two layers: blur with no
background, tint with no filter.

`backdrop-filter` promotes its element to its own compositing layer, and the ancestor's rounded
clip is then rasterised **separately** for that layer. Its coverage along the corner curve does not
agree with the unpromoted main layer's, by a subpixel. When the promoted layer is the one tinting,
that disagreement is a ring where the content underneath comes through **untinted** — a bright
hairline tracing the corner, brightest where the curve meets the straight edge.

Every layer inside the frame being square does not help, and the frame is not at fault. Only which
layer carries the colour matters.

## Measured

Chromium, 2× device pixels. 400px frame, 16px radius, 84px bar, solid bright content under a
`rgba(10,10,12,.6)` tint. `threadPx` is how many of the 3600 device pixels in a 30×30 CSS corner box
differ by more than 8 luma from the same arrangement with `backdrop-filter` removed — that control is
pixel-exact, because over a solid colour a blur is a no-op. `arcStep` is the largest step between
adjacent pixels along a line 6px below the top edge over a smooth gradient, floor 1.0.

| arrangement                           | threadPx | arcStep | verdict                     |
| ------------------------------------- | -------: | ------: | --------------------------- |
| one layer: tint **and** blur          |  **248** |     0.9 | the hairline                |
| tint alone + blur alone, both square  |   **25** |     0.9 | **ship this**               |
| ...blur radius = frame radius         |    **2** |     0.9 | best pixels, couples radii  |
| ...blur radius 12px wider than frame  |    **0** | **3.3** | second arc, visibly wrong   |
| one layer + no-op `mask` on the frame |   **32** |     0.7 | blur clamps at the top edge |

Splitting is a 10× reduction in ring area. The 25 that remain sit near the tangent points rather
than tracing the curve and are not visible at 10× magnification.

## Pattern

```tsx
<div className="relative overflow-hidden rounded-2xl">
  <div className="absolute inset-0">{content}</div>

  <div className="relative">
    <div
      aria-hidden
      // Blur: filter only, no background of its own.
      className="pointer-events-none absolute inset-0 backdrop-blur-md"
    />
    <div
      aria-hidden
      // Tint: colour only, no filter. Overdrawn 1px on the three outer edges.
      className="pointer-events-none absolute -top-px -inset-x-px bottom-0 bg-white/70"
    />
    <div className="relative p-4">{children}</div>
  </div>
</div>;
```

Four layers, and each one is load-bearing:

- **Frame** owns the only radius and the only clip. Everything inside it is square.
- **Blur** carries the filter and no background, so a subpixel disagreement in _its_ clip coverage can
  only mean a hairline-thin ring that is slightly less blurred — invisible.
- **Tint** carries the colour and no filter, so it is not promoted and the frame's clip rasterises it
  exactly as it does the content. The 1px outset means the clip cuts through tint rather than through
  the join between tint and whatever is behind the frame.
- **Content** needs a positioned layer of its own, because positioned elements paint above
  non-positioned in-flow siblings whatever the DOM order — the three have to be peers for order to
  decide.

## Notes

- **Overdraw the tint, never the blur, and never the bottom edge.** The 1px outset on top and sides
  is paint the clip is meant to eat. Overdrawing the bottom moves the edge that content below the bar
  is aligned or measured against.
- **Do not give the filtered layer a radius.** Wider than the frame's removes the ring (it never
  reaches the curve) but paints a second arc of a visibly different radius inside the corner — two
  radii on one corner reads as a mistake far more loudly than a hairline. Equal to the frame's
  measures best of all, and still loses: the radius has to track the frame's across two files, and
  `border-radius: inherit` cannot carry it unless the layer is a direct child of the frame.
- **Everything that flattens a subtree also forms a backdrop root.** `mask-image`, `opacity < 1`,
  `filter`, `isolation: isolate`, `mix-blend-mode`. A no-op `mask-image: linear-gradient(#000,#000)`
  on the frame does force flatten-then-clip and does remove the hairline — and then the blur can only
  sample what is painted inside the frame, so it clamps at the frame's top edge and bands over
  detailed content. The same trap kills `isolate` used to push a material behind content with a
  negative z-index: the filter's own subtree is empty, so it silently stops blurring.
  `preserve-backdrop-filter` covers backdrop roots on their own; here they matter because
  flattening the subtree is the most tempting wrong answer to a corner hairline.
- **Keep both layers out of flow if anything measures the box.** A negative margin overdraws just as
  well and takes the measured height with it; absolutely positioned layers are paint only.
- **Solid content cannot tell you whether a blur is running.** Blurring a flat colour is a no-op, and
  a smooth gradient is nearly one. Test with 3px hard stripes: blurred reads as flat grey, unblurred
  stays crisp. Verify this on any "fix" — an arrangement that scores well by having quietly stopped
  blurring is not a fix.
- **Measure the corner differentially.** A translucent layer at partial coverage is _marginally
  brighter than its own interior_, because the tint's effective alpha falls with coverage faster than
  the content's contribution does. So "brightest pixel in the corner" has a nonzero floor in a
  perfectly correct render and cannot separate the defect from the floor. Diff against the same
  render with the filter removed instead, and count pixels rather than taking a peak — a peak cannot
  tell a ring tracing the whole curve from two pixels at the tangent point.
- **Magnify with `imageSmoothingEnabled = false`.** Interpolated upscales turn a one-device-pixel
  hairline into a soft gradient that is easy to dismiss as ordinary anti-aliasing.
- Numbers are Chromium at 2×. Whether other engines split the clip the same way is untested, and
  `threadPx` is the kind of figure that is an implementation detail.
