---
name: monarch-session-context
description: "Standing context for the Monarch Android app at D:\\Monarch — the single-fixed-text-scale decision and how it is implemented, the art generator's paper-film trap and quota behaviour, and the ANDROID_SERIAL rule that stops instrumented runs wiping the owner's phone. Use before touching Monarch's theme, artwork, or any Gradle instrumented task."
---

# Monarch standing context

Project: `D:\Monarch` — Kotlin + Jetpack Compose + Room fitness app. Owner's
phone is a Samsung S25 Ultra, adb serial `R5GL14GXV3J`; an emulator
`emulator-5554` is usually also attached.

## One fixed text scale (owner decision — do not re-litigate)

The owner asked for **a single text scale**: the Android system font setting
must not affect Monarch at all.

Implemented in `MainActivity.attachBaseContext`:

```kotlin
override fun attachBaseContext(newBase: Context) {
    val pinned = Configuration(newBase.resources.configuration).apply {
        fontScale = FIXED_FONT_SCALE          // 1f, in ui/theme/Theme.kt
    }
    super.attachBaseContext(newBase.createConfigurationContext(pinned))
}
```

**Do not** implement this as a `CompositionLocalProvider(LocalDensity provides …)`
in the theme. That covers only the tree it is provided to: a `Dialog`,
`AlertDialog`, `Popup`, `DropdownMenu` or `ModalBottomSheet` composes in its own
window and re-reads the platform configuration, so it keeps scaling while every
screen behind it holds still. Measured: with the theme pinned, a dialog title
still grew 409px → 756px between system 1.0x and 2.0x.

Consequences already applied — do not re-add:

- The per-screen large-type defences were **deleted** (nav-label cap, XP rail
  growth, step-dial fallback, stacked tab segments, scaled FAB clearance).
- The accessibility cost is recorded in the `docs/TODO.md` decisions table.

Proof method: set `settings put system font_scale` to 0.85 / 1.0 / 2.0, dump
`uiautomator` at each, and compare text-node widths/heights. Correct result is
**zero differing nodes**. Include a dialog in the comparison — the screens alone
will not reveal a leak.

## Artwork generation (`tools/art.py`)

- Routes `gemini-3.1-flash-image` through the omp `google-antigravity` provider.
- **Paper film trap.** Density keying maps blank paper to a LOW alpha, not zero:
  78–91% of a canvas came back at alpha 3–24, invisible in isolation and plainly
  a lighter box on Monarch's near-black panels. Cut at source with a soft knee
  above the histogram gap; `backdrop_audit` now reports a `film` percentage.
  Corner checks and opaque-coverage checks both pass a film-laden image.
- **Sketch frame.** The model draws its own faint border in the margin. Crop
  ~7% off each edge or it reads as the same box.
- **Quota.** Roughly 9–10 images per reset, then `QUOTA_EXHAUSTED` from
  cloudcode-pa. Batches must be resumable: `tools/art_batches/run.py` skips ids
  already drawn and stops with a named reason.
- Never half-wire a catalogue (e.g. 4 of 10 crests): mixed generated and
  procedural art looks worse than either set alone.

## App icon

`tools/icon_install.py` turns one keyed PNG into all 20 mipmap files. It scales
art into the centre **66%** (the adaptive mask keeps only 72dp of 108dp) and
writes the monochrome layer as flat white on the source alpha (Android tints it,
so colour there is meaningless). It refuses an unkeyed or empty source. Judge an
icon **on the launcher**, never from the PNG.

## Running tests — the data-safety rule

Always pin instrumented runs to the emulator:

```bash
ANDROID_SERIAL=emulator-5554 ./gradlew :app:connectedDebugAndroidTest
```

The suite calls `pm clear` and deletes rows from the app's own database. With
the owner's phone attached, an unpinned run destroys their real training
history. The gate also **uninstalls the app** afterwards, so reinstall before
driving the UI or a sweep will silently measure the launcher.

## Gate

```bash
ANDROID_SERIAL=emulator-5554 ./gradlew :app:assembleDebug :app:testDebugUnitTest \
  :app:connectedDebugAndroidTest :app:lintRelease
```

Expect lint 10 (each audited) and zero compiler warnings. CI runs on GitHub via
`.github/workflows/ci.yml` with `cancel-in-progress: true`, so rapid pushes
cancel each other — "CI is green" is a statement about HEAD only.
