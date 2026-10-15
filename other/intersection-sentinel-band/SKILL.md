---
name: intersection-sentinel-band
description: |
  Put a scroll trigger's look-ahead distance in the sentinel's own height — a band with real extent — instead of in the observer's `rootMargin`. Use when building or fixing infinite scroll, load-more-on-scroll, prefetch-ahead, or any "am I near the end" trigger, and especially when a `rootMargin` look-ahead appears to do nothing and the trigger only fires once the user has already reached the bottom.
---

# Intersection Sentinel Band

## Rule

The look-ahead distance belongs to the sentinel's geometry, not to `rootMargin`. Give the sentinel
real height spanning the distance you want to trigger at, and ask the observer for no margin at all.

`rootMargin` is the trap. It is clipped by every scrolling ancestor between the target and the root,
and the default `root: null` is the viewport — so a sentinel inside a scroll container, which is the
normal infinite-scroll shape, has its expanded region clipped straight back to that container's
visible box. The look-ahead silently becomes zero. Nothing errors; the trigger just does not fire
until the user is already at the end.

Measured in Chrome: 600px scroll container, 3000px of content, sentinel at the end, 2000px of
look-ahead asked for. Look-ahead is how many pixels before the bottom the callback first reports
intersecting.

| sentinel    | `root`      | `rootMargin`   | look-ahead |
| ----------- | ----------- | -------------- | ---------- |
| 1px point   | `null`      | `0 0 2000px 0` | **1px**    |
| 1px point   | `null`      | `0`            | 1px        |
| 1px point   | (container) | `0 0 2000px 0` | 2001px     |
| 2000px band | `null`      | `0`            | **2000px** |
| 2000px band | (container) | `0`            | 2000px     |

The first two rows are the same number: the margin bought nothing. A band cannot be clipped away,
because it _is_ content. Passing the real scroll node as `root` is the other fix and measures the
same — but it depends on holding that node, which a virtualizer or a parent usually owns, and it
splits one distance across two places that have to agree.

## Pattern

```tsx
const BAND_PX = 2000;

<div
  aria-hidden
  ref={sentinelRef}
  // The negative margin cancels the height, so the band covers the last 2000px of content
  // for free: its bottom edge still lands where content ends, and `scrollHeight` is
  // unchanged (measured: 3000px of content, 3000px with the band). It now overlaps the
  // last screen of content, so without `pointer-events: none` it would swallow every click
  // there.
  style={{ height: BAND_PX, marginTop: -BAND_PX, pointerEvents: "none" }}
/>;
```

```ts
new IntersectionObserver(callback, { rootMargin: "0px" });
```

## Notes

- **Do not also expand `rootMargin`.** The height _is_ the trigger distance. Keeping both puts one
  threshold in two places, and the margin is the half that silently stops working.
- **Put it in normal flow, after the content.** A flow sibling among absolutely positioned children
  lands at `y=0` — permanently in view at the top of a long list, firing everything on frame one.
- **`isIntersecting` is a state, not an event**, and a band holds that state far longer than a point
  did. Deduplicate on the work ("page N already requested"), never on "fired once".
- **Content shorter than the band is fine, but the trigger is then always on.** Measured with 900px
  of content and a 2000px band: `scrollHeight` still 900, and the sentinel intersects at every scroll
  position including the first frame. Firing immediately is correct — a list shorter than your
  look-ahead does need more — but it makes back-pressure load-bearing rather than optional, since
  `isIntersecting` never goes false to pace you. The 1100px of excess hangs above the content's top,
  unreachable (top overflow is never scrollable) and invisible, but overlapping whatever sits above
  it — the second reason for `pointer-events: none`.
- **Measure its `bottom`**, not its `top` — the bottom edge is where rendered content ends.
- **Space it with `margin`, not `padding`.** Padding enlarges the measured box; margin is invisible
  to `getBoundingClientRect`. With `margin-top: gap - BAND_PX` the band costs exactly `gap`.
- **`position: absolute; bottom: 0` measures identically** (same `scrollHeight`, same 2000px
  look-ahead) and drops the negative margin, so prefer it when the band belongs at the bottom of a
  positioned container. It cannot mark the end of a _rendered prefix_ mid-container, which is what
  the in-flow version buys.
- **A band does not protect against a skipped frame.** Its trigger window is exactly as wide as a
  correctly-rooted `rootMargin`'s, and measured, both miss a single-frame jump that clears the whole
  window and both fire when the jump lands inside it. What decides whether it can be skipped is
  whether the sentinel can be scrolled _past_ at all: at the end of content its window is terminal,
  so any jump to the bottom lands in it; with content below it — placeholders for unmounted rows —
  one frame can clear it. Widen the span for that, don't change its shape.
