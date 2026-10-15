---
name: tap-drag-threshold
description: |
  Separate a tap from a drag on a surface that accepts both, and choose whether the movement threshold also gates the surface's motion. Use when building or reviewing a control that is draggable *and* has per-item click targets — a wheel or drum picker, a carousel, a slider track, a reorderable list, a map, a canvas, a crop frame, a colour field — or when a tap on such a surface does nothing, a click fires at the end of a drag, a drag that returns to where it started is mistaken for a click, the surface jumps a few pixels as a drag begins, or the cursor turns into a grabbing hand before any drag has happened.
---

# Tap and Drag on One Surface

## Rule

A surface that is both draggable and clickable needs a movement threshold, and the threshold answers
**two independent questions**. Decide them separately, because they have different failure modes:

1. **Classification** — is this gesture a tap or a drag? Sticky or re-evaluated.
2. **Semantics** — does the threshold also gate the surface's motion, and if so how does the surface
   catch up? Three strategies.

Conflating them produces a control that either swallows taps or lurches at the start of every drag.

## 1. Classification: sticky or re-evaluated

Both read the same quantity — the pointer's displacement from where it went down — and differ only in
**when** they read it.

**Sticky.** The gesture becomes a drag the first time the displacement crosses the threshold, and
stays a drag until the pointer is released. One boolean, set once, never cleared mid-gesture.

```js
// on pointermove
if (!isDrag && distance(down, current) >= THRESHOLD) isDrag = true;
```

**Re-evaluated.** The classification is computed at release, from the displacement at that moment.
No state is carried during the gesture.

```js
// on pointerup
const isDrag = distance(down, release) >= THRESHOLD;
```

### Where they agree, and where they diverge

For a **monotonic** gesture — a pointer that moves away from its origin and is released there — the
two are identical. That covers most gestures, which is why the difference is easy to miss and easy to
ship.

They diverge whenever the pointer's **path** is longer than its **displacement**: any gesture that
leaves the origin and comes back. Then re-evaluation measures a small displacement and reports a tap,
so the tap action fires at the end of what the user experienced as a drag. Concrete cases:

- A drag out and back, released near the press point.
- A drag on a looping or wrapping surface that happens to return to the same visual position.
- A drag pushed against a limit and released after easing back.
- A slow exploratory drag on a snapping surface that settles onto the detent it started from.

What re-evaluation buys in exchange is insensitivity to a **single spurious sample**. Under sticky
classification, one erroneous far-away `pointermove` — a digitizer glitch, a coalesced-event artifact,
a synthetic event in a test — permanently marks the gesture a drag. Under re-evaluation the same
sample is forgotten as soon as the next one arrives. Whether that trade is worth taking depends
entirely on input quality; on ordinary mouse and touch input it rarely comes up, and the out-and-back
misclassification does.

A gesture is also worth cancelling outright rather than classified, in the cases `pointer-drag-release`
covers: `pointercancel` means the interaction was invalidated, so neither the tap action nor the drag's
commit should run.

## 2. Semantics: what the threshold gates

Let `T` be the threshold and `d` the pointer's displacement from the press point. All three strategies
converge once `|d| ≫ T`; they differ only inside the first `T` pixels and by a constant afterwards.

| Strategy                  | Surface while `\|d\| < T` | On the frame `T` is crossed | Steady-state offset from pointer | Where a tap leaves the surface |
| ------------------------- | ------------------------- | --------------------------- | -------------------------------- | ------------------------------ |
| **A. Classify only**      | tracks `d`, 1:1           | nothing happens             | `0`                              | up to `T` from rest            |
| **B. Gate with catch-up** | still                     | steps by `≈T`               | `0`                              | exactly where it was           |
| **C. Gate with rebase**   | still                     | nothing happens             | `≈T`                             | exactly where it was           |

**A. Classify only.** The surface follows the pointer from its first pixel; the threshold is used for
nothing but labelling the gesture at release. There is no discontinuity at any point and the surface
and pointer never disagree. The cost is that a tap does move the surface, by up to `T`. On a surface
with a rest position — a wheel that snaps to a detent, a carousel that snaps to a page — that movement
is undone by the snap and is invisible at ordinary values of `T`. On a free surface with no rest
position — a map, a canvas, a free-scrolling list — a tap leaves the content permanently displaced by
a few pixels.

**B. Gate with catch-up.** The surface is held still until the threshold is crossed, then moves to the
full displacement measured from the press point. Taps are pixel-exact. The cost is a step of about `T`
on the crossing frame, in the direction of travel. How much that matters scales with the element: a
3px step on a 40px row is hard to see; the same step on a full-screen sheet or a high-contrast handle
reads as a lurch.

**C. Gate with rebase.** The surface is held still until the threshold is crossed, then tracks
displacement measured from the **crossing point** rather than the press point. Taps are pixel-exact
and there is no step. The cost is that the surface stays about `T` behind the pointer for the whole
gesture. That is most visible on short drags — with `T = 3`, a 12px drag moves the surface 9px — and on
anything where pointer and content must stay registered: a crop handle, a map, a drawing tool, a
resize gutter.

One implementation detail decides whether C works. Capture the rebase constant **once**, at the
crossing:

```js
// correct: a fixed constant for the rest of the gesture
if (!isDrag && Math.abs(d) >= T) {
  isDrag = true;
  rebase = d;
}
surface = isDrag ? d - rebase : 0;
```

Recomputing it as `T * Math.sign(d)` looks equivalent and is not: when the drag reverses direction
back through the origin the sign flips and the surface jumps by `2T`.

### Choosing

The question that decides it is usually not aesthetic: **does the surface have a rest position it
returns to?** If it does, A's cost is erased by the snap and its lack of any discontinuity is free. If
it does not, A leaves taps displacing the content, and the choice is between B's one-off step and C's
constant lag — B where the element is small or the drag is usually long, C where pointer-to-content
registration matters more than the first few pixels.

Independently of all three, `T` should not vary between controls in one product. A surface that decides
at a different distance from everything else on the page feels wrong in a way users cannot name and
reviewers do not spot.

## What Motion does

Verified against `framer-motion@12.43.0`. Motion's `drag` and `onPan` share one `PanSession`, so both
behave the same way.

- **Threshold: 3px, 2D Euclidean.** `PanSession`'s `distanceThreshold` defaults to `3`, tested as
  `distance2D(info.offset, { x: 0, y: 0 }) >= this.distanceThreshold`. Being 2D, sideways movement
  counts: a horizontal wobble can start a vertical drag.
- **Classification: sticky.** The test is `isPanStarted = this.startEvent !== null`, and `startEvent`
  is assigned on the first crossing and not cleared for the rest of the session. An out-and-back drag
  stays a drag.
- **Semantics: strategy B.** The move handler returns early until the threshold is crossed, so the
  element is still during the slop. The value applied is
  `next = this.originPoint[axis] + offset[axis]`, where `offset` is measured from the **pointerdown**
  point (`subtractPoint(point, history[0])`) and `originPoint` is captured in the pan's `onStart`
  handler — which runs on the crossing frame, not on pointerdown. So the crossing frame applies a
  displacement of about the threshold at once: the element steps ~3px into the drag.
- **Configurability: only on the manual path.** `distanceThreshold` is public on
  `DragControlOptions`, i.e. `useDragControls().start(event, { distanceThreshold })`. The automatic
  `drag` prop calls `start(event)` with no options, so it always uses `3`.
- `onDragStart` and `onPanStart` therefore fire on the crossing frame, not on pointerdown. A cursor,
  class, or lock applied in a `pointerdown` handler is applied too early to describe a drag.

Deviating from Motion in a hand-written gesture is reasonable — a snapping surface has a good reason
to prefer A — but deviate deliberately, and keep the threshold value and the stickiness, since those
are what make the control agree with every Motion-driven element beside it.

## Pattern

A hand-written gesture with the classifier separated from the semantics, so the strategy is one line:

```ts
const THRESHOLD = 3;
type Strategy = "classify-only" | "gate-catch-up" | "gate-rebase";

const start = { x: 0, y: 0, value: 0 };
let isDrag = false;
let rebase = 0;

function onPointerDown(event: PointerEvent) {
  start.x = event.clientX;
  start.y = event.clientY;
  start.value = readValue();
  isDrag = false;
  rebase = 0;
  // Which item was aimed at, read now: under strategy A the surface starts moving
  // on the next event, so the element under the pointer at release may not be the
  // one that was pressed.
  aimed = hitTest(event);
}

function onPointerMove(event: PointerEvent, strategy: Strategy) {
  const dx = event.clientX - start.x;
  const dy = event.clientY - start.y;
  // Sticky: set once, never cleared. Re-testing this at release would call an
  // out-and-back drag a tap.
  if (!isDrag && Math.hypot(dx, dy) >= THRESHOLD) {
    isDrag = true;
    rebase = dy; // captured once — see above
    onDragBegin(); // cursor, lock, class: here, not in onPointerDown
  }

  if (strategy === "classify-only") writeValue(start.value + dy);
  else if (isDrag && strategy === "gate-catch-up") writeValue(start.value + dy);
  else if (isDrag) writeValue(start.value + dy - rebase);
}

function onPointerUp() {
  if (isDrag) commitDrag();
  else if (aimed !== null) selectItem(aimed);
  onDragEnd();
}
```

## Notes

- Read the tap's target at **pointerdown**, not at release. Under strategy A the surface has moved by
  then; under any strategy a slow release can land the pointer over a neighbour.
- Where the surface has non-uniform or transformed geometry — a 3D drum, a perspective carousel, a
  rotated canvas — resolve the tap by hit-testing the DOM (a `data-` attribute on each item) rather
  than inverting the pointer's coordinate. Inverting a perspective divide means solving an equation,
  and a hit-test also cannot disagree with what the item was rendering.
- Give any element that is invisible but still laid out `pointer-events: none`. A faded-out item can
  still win a hit-test, and on a curved surface a back-facing item can sit inside the visible box.
- `:active` cannot express "is dragging". It begins at `pointerdown`, which is before the
  classification exists, so a cursor or pressed style hung off it applies to taps too. Drive it from an
  attribute or state set when the threshold is crossed. If the pointer is captured, put the drag cursor
  on `body` as well, or it reverts over whatever the pointer passes.
- A third classifier exists: threshold on **cumulative path length** rather than displacement. It
  agrees with sticky-displacement on the out-and-back case and additionally catches a slow circular
  scrub that never gets far from the origin. It costs a running sum and is worth it mainly for freehand
  surfaces.
- Time is usually the wrong axis. A press held still for two seconds and released without moving is a
  tap on most platforms; adding a duration cut-off makes a slow, careful tap fail. Reach for time only
  when the surface also has a distinct long-press action.
- `pointer-drag-release` covers the other half of the lifecycle: how the gesture ends when the release
  event never arrives, and why `pointercancel` must not be wired to the release path.
