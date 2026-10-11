---
name: compose-hand-drawn-edge-artifacts
description: "Use when hand-drawn or ink-style Compose borders look torn, jagged or zig-zag on a real device (worse on high-density screens), when a panel corner shows a bright notch or spike, or when an accent tick blobs at a corner or floats off a rounded edge."
---

# Hand-drawn Compose edges: artifact triage

Procedural "ink" UI (jittered outlines, brush ticks) produces a specific family
of defects that compile clean, pass every test, and only show on a real screen.
Each has a measurable cause — do not eyeball-tune constants.

With a personal phone attached, pin instrumented runs to the emulator first —
see `android-physical-phone-safe-verify`. Raster art that shows a lighter box on
a dark panel is a paper-wash film, not an edge defect — see
`monarch-art-generation` (Trap 1).

## 1. Rough / "torn" outlines → polyline kinks

**Symptom:** edges read as a zig-zag or torn ribbon, worse on high-density
screens.

**Cause:** the outline joins jittered points with `lineTo`. Every point is a
sharp vertex; at ~55px facets on 450dpi that is visible as a kink.

**Fix:** curve *through* the jitter — original points become quadratic control
points, midpoints become anchors:

```kotlin
private fun smoothClosedPath(pts: FloatArray): Path {
    val n = pts.size / 2
    val path = Path()
    if (n < 3) return path
    fun x(i: Int) = pts[((i % n) + n) % n * 2]
    fun y(i: Int) = pts[((i % n) + n) % n * 2 + 1]
    var mx = (x(0) + x(1)) / 2f; var my = (y(0) + y(1)) / 2f
    path.moveTo(mx, my)
    for (i in 1..n) {
        val nx = (x(i) + x(i + 1)) / 2f; val ny = (y(i) + y(i + 1)) / 2f
        path.quadraticTo(x(i), y(i), nx, ny); mx = nx; my = ny
    }
    path.close(); return path
}
```

Apply to **every** outline kind — rect shape, circle shape, cut-corner plate,
filled dots. Grep for `lineTo(` in the theme package; each one is a suspect.

## 2. Bright notch at a corner → miter spike

**Symptom:** a small bright mark shooting past a panel's corner.

**Cause:** `Stroke()` defaults to `StrokeJoin.Miter`. A near-180° turn in a
jittered path produces a spike whose length grows without bound.

**Fix:** always stroke procedural paths with round join and cap.

```kotlin
fun stroke(px: Float) = Stroke(px, cap = StrokeCap.Round, join = StrokeJoin.Round)
```

## 3. Accent ticks that blob or float

**Symptoms:** a fat bright blob at a corner; or, once outlines are smoothed, an
accent mark detached from the edge.

**Causes:**
- A tapered tick helper is thick at `from`. Anchoring *two* ticks at the same
  corner point stacks two full-width ends on the same pixels.
- Straight ticks drawn at bounding-box coordinates cannot follow a wobbled,
  rounded corner.
- Drawing the accent on an inner child measures a different box than the element
  carrying the border.

**Fix — make the accent a stretch of the border itself**, on the *same* modifier
chain as the border:

```kotlin
val outline = when (val o = shape.createOutline(size, layoutDirection, this)) {
    is Outline.Generic -> o.path
    is Outline.Rounded -> Path().apply { addRoundRect(o.roundRect) }
    is Outline.Rectangle -> Path().apply { addRect(o.rect) }
}
val measure = PathMeasure().apply { setPath(outline, false) }
// Find where the path PASSES the corner; a fixed fraction lands mid-edge.
fun nearest(target: Offset): Float { /* sample ~96 points, argmin distance */ }
measure.getSegment(at - run / 2f, at + run / 2f, seg, true)
```

Weight matters: ~1.5dp line plus a ~4dp bleed at ~0.2 alpha reads as a mark;
2–3dp at full alpha reads as a highlighter.

## 4. Verification loop

1. `adb -s <phone> install -r -t app-debug.apk`, force-stop, launch, `screencap`.
2. Crop and magnify the suspect region with PIL (`Image.NEAREST`) — a full
   screenshot hides a 6px artifact.
3. Quantify when possible (most-green pixel, corner alpha mean) so "better" is
   a number, not an impression.
4. Retake if a heads-up notification lands over the region being judged before
   concluding anything is missing (`android-physical-phone-safe-verify`).
