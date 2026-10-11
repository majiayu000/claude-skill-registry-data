---
name: android-font-scale-verification
description: "Use when checking font-scale safety, text clips, overlaps, wraps mid-word or controls vanish at large font scale, a label cap ignores smaller text, or owners say big text looks bad but sweeps pass. Also before calling a layout font-scale safe, or when a segmented label slices, letterSpacing keeps growing after fontSize is capped, text overflows a fixed ring or hides under a floating button, or a geometric detector reports '0 issues'."
---

# Android font-scale verification

Large-text users run 1.3–2.0x, and some run below 1.0. Layouts that look fine at 1.0x fail in
ways neither one screenshot nor a bounds sweep shows alone: measure across scales, then look.

If the app deliberately pins one text scale (Ironvellum does, see `monarch-session-context`),
identical geometry at every setting is the intended result. Prove the pin with
`android-pin-single-font-scale` instead of sweeping it for defects.

## The sweep, and the traps that void it

Per scale, per screen: set, relaunch, dump, screenshot.

```bash
adb -s "$SERIAL" shell settings get system font_scale    # record it; restore it at the end
adb -s "$SERIAL" shell settings put system font_scale 2.0
adb -s "$SERIAL" shell am force-stop "$PKG"
adb -s "$SERIAL" shell monkey -p "$PKG" -c android.intent.category.LAUNCHER 1
adb -s "$SERIAL" shell uiautomator dump /sdcard/ui.xml && adb -s "$SERIAL" shell cat /sdcard/ui.xml
adb -s "$SERIAL" exec-out screencap -p > .tmp/shots/<screen>-2.0.png
# ALWAYS restore when done, and say which value you restored
adb -s "$SERIAL" shell settings put system font_scale <recorded>
```

- **Device gone.** `settings get system font_scale` returns an empty string when the device is
  disconnected. That is a failed call, not a device at default. Check `adb devices` first.
- **App uninstalled.** An instrumented run uninstalls the app, so a sweep straight after a gate
  drives the launcher and reports every screen "unreachable" or clean. Reinstall without
  silencing the output (`install >/dev/null` hides the failure) and confirm the app's nav bar is
  in the dump before trusting any measurement.
- **A real phone attached.** Pin every command with `-s`/`ANDROID_SERIAL`; keeping destructive
  suites off it and restoring its settings: `android-physical-phone-safe-verify`.
- **Wrong node.** `enabled` and `selected` sit on the clickable ancestor, not the label's text
  node: `compose-control-tap-verification`.

## 1. Sentinel strings find what the eye misses

The highest-value check is the cheapest: assert the primary control's text is present in the
dump at each scale.

```python
for s in ("ACCEPT QUEST", "LOG WEIGHT", "SIGN IN"):
    print("OK" if s in dump else "MISSING", s)
```

A real case: nine full-screen visual inspections at 1.5x and 2.0x all passed while the app's
primary button **did not exist** at 2.0x. One string check caught it immediately.

Presence is not enough: the control's bottom must sit above the nav bar's top (both bounds come
from the dump). A control missing on a non-scrolling screen is usually the `Column` measure-order
collapse, a CTA declared after an unweighted header measured at zero height; the fix is in
`android-display-size-layout-collapse`.

## 2. Absence only matters on a screen that does not scroll

Before calling a missing sentinel a defect, swipe and re-dump:

```python
for i in range(8):
    if mark in dump(): break
    adb("shell","input","swipe","540","1700","540","800","250")
```

Two "regressions" found this way were both reachable after one swipe. Only non-scrolling
screens (typically the dashboard) make first-viewport absence a real failure.

## 3. Measure the same label across scales, including below 1.0

A cap on text growth is commonly written as a divide, and it is wrong:

```kotlin
fontSize = style.fontSize / LocalDensity.current.fontScale   // WRONG: freezes the size
```

`sp` already multiplies by `fontScale`, so dividing renders **one physical size at every
setting**, including below 1.0: a user who asked for *smaller* text is ignored. It has shipped
before. Cap the growth instead, and cap `letterSpacing` too, because it is declared in `sp` as
well:

```kotlin
fun labelScale(fontScale: Float) =
    if (fontScale <= 0f) 1f else minOf(fontScale, CAP) / fontScale

val s = labelScale(LocalDensity.current.fontScale)   // in the composable
Text(
    label,
    fontSize = style.fontSize * s,
    letterSpacing = style.letterSpacing * s,
)
```

Prove it from the dump: sweep **0.85, 0.9, 1.0, 1.3, 1.5, 2.0** and compare one label's width.

```
capped:              0.85 -> 86   0.9 -> 92   1.0 -> 102   1.3/1.5/2.0 -> 118    rises, then plateaus
frozen:              identical at every scale, including 0.85 and 0.9
tracking unclamped:  1.0 -> 102   1.5 -> 112   2.0 -> 123                        ~10% / ~20% growth
```

Identical widths above the cap prove the cap holds; smaller widths below 1.0 prove it is not a
freeze. A sweep of 1.0x and up cannot tell the two apart. Capping nav labels is a defensible
tradeoff (the icon and the `contentDescription` carry the meaning, and neither scales); argue it
in a comment rather than doing it silently.

"Broken on all screens" is a hypothesis, not a location. Probe several labels on several screens
at every scale before agreeing with the scope. One frozen surface among correct ones is common;
measuring tells them apart, and the same numbers then prove the fix.

## 4. Read the screenshots: defects a bounds sweep passes

A bounds sweep ("no node off-screen, nothing squished, every node grew") measures **geometry**.
It does not see sliced words, a control parked on top of content, or text that is the right size
for the wrong reason. When an owner looking at a real screen says it "looks really bad" while the
sweep is green, **the owner is right and the sweep is answering a different question.** Read the
1.0x and 2.0x screenshot of every screen before claiming anything.

- **Equal-width segments slice their labels.** A segmented control giving each option
  `Modifier.weight(1f)` cannot hold three words at 2.0x: `BODY | TRAINING | ACTIVITY` renders as
  `BODY | TRAININACTIVIT`, mid-word, with no ellipsis to hint at it. Above ~1.3x lay the segments
  out in a `Column` inside the same bordered group so every label stays whole, and verify the
  normal scale is untouched (all labels share one y).
- **Text inside a fixed-size container.** A counter drawn inside a ring (`Modifier.size(104.dp)`)
  or a rail (`Modifier.height(20.dp)`) overflows its own container once the type grows. Let the
  container grow (`heightIn(min = …)`, `size(base * scale)`) or let the decorative shape
  **yield** to a plain row that cannot overflow.
- **A fixed spacer clearing a text-sized floating button.** `Spacer(Modifier.height(128.dp))`
  under a list clears an `ExtendedFloatingActionButton` at 1.0x only. The button is text and
  grows, so the last row ends up underneath it. Scale the clearance:
  `128.dp * fontScale.coerceIn(1f, 2f)`.

Dump signals worth extracting, as a *supplement* to looking:
- nodes whose text ends in `…` (ellipsised: something is hidden)
- per-label width across scales (section 3)
- identical y for segmented labels (still a row) vs distinct y (stacked)

## 5. Validate any geometric detector against a known-bad build

A heuristic that has never fired proves nothing. Revert the fix, rebuild, and confirm the
detector flags it.

A width-based squish detector (`w < 90 && h > 2w`) reported **0 issues** on a build whose nav
labels demonstrably wrapped mid-word; the wrapped labels measured `154x162px`, far outside the
threshold. The discriminating signal was the aspect ratio of a single-word label: **1.05 broken
vs 0.29–0.40 fixed**.

## 6. Mutation-prove the fix

Rebuild the pre-fix source and confirm the symptom returns:

```bash
git show HEAD~2:path/to/Screen.kt > .tmp/prefix.kt   # repo-local, not /tmp
```

`/tmp` is not reliably shared between git-bash and a Python subprocess on Windows; use a
repo-local `.tmp/`. Restore afterwards and confirm `git status` is clean, which also proves the
restore was byte-exact.

## What to record

State what was measured and what was not, and which scale you restored. No instrumented suite
guards this: tests run at the device's own font scale, so a regression needs the manual sweep.
Where large text forces a real product tradeoff (e.g. a card that fits its CTA but not its
list), present costed options to the owner instead of choosing silently.
