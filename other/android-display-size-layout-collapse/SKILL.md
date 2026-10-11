---
name: android-display-size-layout-collapse
description: "Diagnose Android/Compose layouts that lose a primary control at the largest Display size (density) setting, alone or combined with large text — covers why screenHeightDp never fires as a threshold, why a weighted child inside verticalScroll collapses, measuring the window instead of the display, and the calendar-dependent instrumented test that fails three mornings a year. Use when a button goes missing on a non-scrolling screen, or before claiming a layout survives accessibility display settings."
---

# Display-size layout collapse

Font scale is only half the accessibility geometry. **Display size** (density)
is a separate slider, and users who raise one usually raise both. The failure
is a control that is not merely ugly but *absent*.

Companion to `android-font-scale-verification`, which covers the text-scale
axis and the sentinel-string method. This one covers density and the layout
traps that appear when space genuinely runs out.

## Drive both axes from adb

```bash
adb shell wm density 540            # stock is often 420; 540 ≈ largest "Display size"
adb shell settings put system font_scale 2.0
adb shell wm size                   # px never changes; only dp does
# restore
adb shell wm density 420 && adb shell settings put system font_scale 1.0
```

Usable width in dp = `px / (density / 160)`. 1080px at 540 → **320dp**, the
narrowest configuration a real user can produce on a phone.

Force-stop and relaunch after every change; a configuration change mid-process
can leave a stale layout.

## The test matrix that matters

Three points, not a grid: **stock**, **stock + 2.0x text**, **largest display +
2.0x text**. The third is where things break, and each fix must be re-checked
at the first so the normal case is untouched.

## Trap 1 — `screenHeightDp` never fires as a threshold

The largest display size still reports ~693dp of height, because raising
density shrinks *everything*, including the elements you are trying to fit. A
threshold like `screenHeightDp >= 560` silently never triggers.

What actually overflows is **text lines**, so divide:

```kotlin
val room = windowHeightDp / LocalDensity.current.fontScale
// stock 891 · largest display + 2x text 347 → threshold 400 fires only there
```

In an app that pins its text scale (`android-pin-single-font-scale`), `fontScale` never changes:
divide by the pinned constant instead (Ironvellum uses `FIXED_FONT_SCALE`).

Derive the threshold from three real measurements; do not guess a round number.

## Trap 2 — measure the window, not the display

`LocalConfiguration.current.screenHeightDp` describes the whole display, so it
is wrong in split screen, and lint flags it (`ConfigurationScreenWidthHeight`).

```kotlin
val density = LocalDensity.current
val windowHeightDp = with(density) { LocalWindowInfo.current.containerSize.height.toDp().value }
```

Take the lint hint here rather than suppressing it — the replacement is more
correct, not merely quieter.

## Trap 3 — scrolling the page collapses a weighted panel

The instinct when content overflows is to wrap the screen in `verticalScroll`.
If any child uses `Modifier.weight(...)`, that child now measures against an
**infinite** height constraint and collapses to nothing — usually the very
panel holding the missing control. Scrolling and weighting are mutually
exclusive in one column.

## Trap 4 — unweighted children win the measure pass

In a `Column`, unweighted children are measured first, in declaration order.
A header declared before the button takes all the height it wants, and a
button declared last is measured at **zero height**: present in the tree, zero
pixels, unreachable.

Fix by making the thing that must survive the *only* unweighted child:

```kotlin
Column(Modifier.weight(1f, fill = false).verticalScroll(rememberScrollState())) {
    Title(); Note(); Rows()      // everything that may shrink
}
PrimaryButton()                   // unweighted → measured first → always laid out
```

## When space is genuinely gone, choose what yields

If the screen still cannot fit, drop the largest **purely informative** element
and say so in a comment: which element, why it was picked, and where that
information still exists. Never let the primary action be the thing that goes.
Surface the tradeoff as an owner decision with costed options rather than
choosing silently.

## Trap 5 — the calendar breaks instrumented tests, not the app

A flow test that drives "today's" content fails on the days your seed data does
not cover — three mornings a year, on a machine nobody is watching. Walk the UI
to a day that has content instead of trusting the clock:

```kotlin
if (allText().any { it == "REST DAY" }) { /* pick a day from the week rail */ }
```

Same shape for anything keyed on today: streaks, weekly rails, "this month".

## Verification

Assert the control by **sentinel string plus bounds** at each of the three
configurations, and on a scrolling screen confirm reachability by swiping
before calling absence a defect. Then mutation-test: rebuild the pre-fix
layout, confirm the control disappears, restore. A layout fix nobody watched
fail is not proven.
