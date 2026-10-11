---
name: compose-procedural-art-verification
description: "Build and prove seeded procedural Canvas art in Jetpack Compose (relic sigils, crest emblems, generated avatars) — deriving stable art from a hash, proving no two catalogue entries render the same figure without screenshotting each one, and the two traps that silently ruin it: a Canvas with no height constraint inside a Row, and delegated agents stubbing a hardcoded glyph. Use when asked for procedurally generated art/icons, or when generated marks look identical or invisible on device."
---

## When to use

Asked for "proc gen art", generated icons, or unique-per-item visuals in a Compose app —
especially when the item set is **continuous or open-ended** (a rolled multiplier, a user id,
an arbitrary name) so a fixed asset set cannot cover it.

Also use when generated marks render **identical to each other**, or render **invisible** on device.

## Decide: procedural vs generated assets

Procedural Canvas wins when:
- the value space is continuous/unbounded (`low + (high-low)*t` rolls, hashes, user ids),
- art must scale from a 40.dp list row to a 96.dp hero with no extra files,
- an existing seeded visual language already reads well in the app (match it).

Generated image assets (e.g. an image model) win for hero/marketing art with a **fixed, small**
catalogue. Don't mix: if the repo already rejected hand-drawn SVG icons, geometric/abstract
procedural marks are a different thing — say so explicitly rather than re-litigating.

## Recipe

1. **Stable hash, not `hashCode()`.** Roll your own so it is identical on JVM and in any
   verification script:
   ```kotlin
   private fun seedOf(name: String): Int =
       name.fold(0) { acc, c -> acc * 31 + c.code } and Int.MAX_VALUE
   ```
2. **Seed → spec in `remember(name)`.** Never call `Random()` unseeded in a composable; it
   re-shuffles on recomposition. Derive every parameter from disjoint slices (`seed % 6`,
   `(seed / 7) % 360`, `(seed shr (i*2)) and 3`).
3. **Archetypes, not one shape rotated.** 3–4 structurally different figures selected by
   `seed % N` reads as a designed set; one shape with varying rotation reads as a bug.
4. **All geometry from `size` inside `Canvas`** so one composable serves every call site;
   caller controls size via `modifier`.
5. **Caller supplies palette** (`primary`/`accent` params) so the mark inherits the item's
   existing colour identity instead of inventing a second convention.

## Trap 1 — Canvas with no height collapses silently

```kotlin
Row {
    Box(modifier) { Canvas(Modifier.fillMaxSize()) { drawArc(...) } }  // weight(1f) → height = text height
}
```
A `Canvas(fillMaxSize)` inside an unconstrained `Row` slot gets its height from its *siblings*,
so an arc/gauge flattens to an invisible sliver. It compiles, it draws, it is just 4px tall.
**Fix:** give the art a square box — `Modifier.size(112.dp)` or `aspectRatio(1f)` — never a bare
`weight(1f)`. Symptom: "the dial/arc I wrote never appears" while the text inside it renders fine.

## Trap 2 — prove distinctness arithmetically, not by eye

Screenshotting 10 catalogue entries is slow and misses near-collisions. Replicate the *same*
hash in a throwaway script and compare full parameter tuples:

```python
def seed(s):
    a = 0
    for c in s: a = (a*31 + ord(c)) & 0xFFFFFFFF
    if a >= 2**31: a -= 2**32          # emulate Kotlin Int overflow
    return a & 0x7FFFFFFF
sig = {i: (seed(i) % 4, ...) for i in CATALOGUE_IDS}
print("distinct:", len(set(sig.values())), "of", len(sig))
```
Expect `N of N`. A first pass commonly yields e.g. `8 of 10` — fix by adding an orthogonal
dimension (per-item tilt, bit-driven silhouette) and re-running, *then* screenshot two or three
to confirm the rendering matches the arithmetic.

## Trap 3 — delegated agents stub the mark

When fanning this out to subagents, they will hand back a compiling file whose plate contains a
**hardcoded glyph** (`Text("M")`) or the wrong import (`androidx.compose.foundation.layout.LazyRow`
instead of `androidx.compose.foundation.lazy.LazyRow`). Both compile-by-inspection "fine" in their
report. Always diff the delivered file for literals and build once yourself before believing it.

## Verify

1. `assembleDebug` + unit suite green.
2. Distinctness script prints `N of N`.
3. Install and screenshot **at least two** entries that the script says differ — confirms the
   spec actually reaches the canvas.
4. Check the art is visible at its *smallest* call site, not just the hero one.

## Motion

If the house rules forbid hard flashing (Monarch does), use long periods: `tween(48_000, LinearEasing)`
for a drift, `infiniteRepeatable(tween(2_500+), RepeatMode.Reverse)` for a breath. Reserve motion for
the item that is *currently active*; animating every row is noise.
