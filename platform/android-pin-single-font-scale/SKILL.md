---
name: android-pin-single-font-scale
description: "Use when an owner wants one fixed text scale ('I just want the single scale'), large-font defences multiply, or after pinning a Dialog still scales text or ignores a theme-level override. Also when a popup or AlertDialog does, or before claiming a pinned text scale or any app-wide CompositionLocal holds in every window."
---

# Pin a Compose app to one text scale

Use when an owner decides the app should ignore the system font setting, or when per-screen
large-type defences keep multiplying (a nav label cap here, a control that stacks there) and each
one is a branch nobody verifies again. Ironvellum is already pinned (`monarch-session-context`).

## Pin the configuration in the Activity

Override the configuration once, in each Activity's `attachBaseContext` (Ironvellum has one,
`MainActivity`):

```kotlin
override fun attachBaseContext(newBase: Context) {
    val pinned = Configuration(newBase.resources.configuration).apply {
        fontScale = FIXED_FONT_SCALE              // pin ONLY the text scale
    }
    super.attachBaseContext(newBase.createConfigurationContext(pinned))
}

const val FIXED_FONT_SCALE = 1f
```

Every window the activity opens inherits this context: screens, `Dialog`, `AlertDialog`, popups
and menus. Only `fontScale` is touched, so display size (density) still applies. Pinning density
as well would freeze a different setting, which is usually not what was asked for.

## Why not a CompositionLocal in the theme

Overriding `LocalDensity` in the theme covers **the tree it is provided to, and nothing else**.
A `Dialog` or `Popup` hosts its content in its own window and composition, which re-provides the
platform `LocalDensity`. The leak is invisible in code review and to a sweep of the activity's
screens. Measured with the theme pinned at `fontScale = 1f`:

```
weigh-in dialog "LOG BODY READING":   system 1.0x -> 409px    system 2.0x -> 756px
every screen behind it:               identical at both
```

Re-pinning inside each dialog worked but had to be remembered at every call site, and the first
sweep for them missed three `AlertDialog`s. The activity override replaced the per-dialog
wrappers, the theme provider and the source scan that guarded them (D:/Monarch, 2026-09-16).

If the Activity is out of reach, that is the fallback: re-provide
`Density(current.density, FIXED_FONT_SCALE)` inside every dialog's **content** (providing it
around the `Dialog(...)` call changes nothing, because the new composition starts inside it),
and guard the call sites with a source scan, mutation-proven by unwrapping one dialog. The old
scan matched `\n\s*Dialog\(`, which never sees `AlertDialog(`.

Treat any other app-wide CompositionLocal override (layout direction, locale, custom theme
locals) the same way: unproven inside a dialog until measured there, and re-provided inside the
dialog's content if it leaks.

## Prove it — geometry across settings, including a dialog

A screenshot at one scale proves nothing. Compare measured text-node geometry at several system
settings and expect **zero differences**, on the screens **and inside an open dialog**:

```python
for scale in ("0.85", "1.0", "2.0"):
    sh("shell", "settings", "put", "system", "font_scale", scale)
    # force-stop, relaunch, wait, OPEN THE DIALOG, then uiautomator dump
    geom[scale] = {text: (w, h) for each text node}
diff = [k for k in shared if geom["1.0"][k] != geom[scale][k]]   # must be []
```

- "0 differing nodes" on the screens alone is true and irrelevant: that sweep walks the
  activity's composition, and a dialog is a different window. After the activity pin an
  `AlertDialog` measured identical at 1.0x and 2.0x.
- Include a setting **below** 1.0: a pin must hold in both directions. Telling a cap from a
  freeze is in `android-font-scale-verification`.
- Re-check any control that previously had a large-type branch (a tab row that stacked, a dial
  that yielded) and confirm it now renders one way at every setting.
- Always restore the device setting afterwards. The traps that void a sweep (an empty
  `settings get` from a gone device, a gate that uninstalled the app) are in
  `android-font-scale-verification`; keep instrumented suites off a real phone
  (`android-physical-phone-safe-verify`).

## Then delete the defences — this is the point

The pin is only worth it if the per-screen workarounds go with it. Typical removals: font-scale
label caps, `heightIn` growth added for oversized labels, fallback layouts above a threshold,
`maxLines` that varied by scale, spacers scaled to clear a text-sized floating button, per-dialog
re-pin wrappers, and any test pinning those formulas. Delete them rather than leaving branches
that can no longer fire.

Finish with `grep -rn "fontScale"` over the source: nothing outside the pin site should
reference it. A surviving reference is a branch that can never fire.

## Say the cost out loud

Pinning the scale is an accessibility regression against Android's guidance: enlarged system
text no longer enlarges the app. Record it as an owner decision with the tradeoff named, not as
an implementation detail. It matters if the app ever faces a store accessibility review.
