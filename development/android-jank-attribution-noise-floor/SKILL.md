---
name: android-jank-attribution-noise-floor
description: "Measure Android scroll jank at realistic data volume and decide whether a frame-time difference is real — seeding the app's LIVE database via am instrument (the Gradle task uninstalls the app and takes the data with it), using a data-independent screen as a control, and establishing the emulator's noise floor before attributing anything. Use when a screen \"feels slow at scale\", before accepting a Compose remember/memoisation optimisation, or when dumpsys gfxinfo numbers are about to be quoted."
---

# Jank attribution and the emulator noise floor

Frame-time numbers from a software-rendered emulator are noisy enough to invent
a defect and then to "confirm" a fix that did nothing. This skill is the
procedure that keeps both from happening.

## 1. Get real data into the REAL database

Scale tests usually seed an isolated DB, so the on-device UI has never rendered
more than a handful of rows. Seed the app's own database with a throwaway
instrumented class that asserts nothing:

```kotlin
val db = MonarchDatabase.create(context, MonarchDatabase.NAME)  // the LIVE name
```

**Run it with `am instrument`, not Gradle.** `connectedDebugAndroidTest`
uninstalls the app when it finishes and destroys everything you just seeded:

```bash
adb install -r -t app/build/outputs/apk/debug/app-debug.apk
adb install -r -t app/build/outputs/apk/androidTest/debug/<test>.apk
adb shell am instrument -w -e class <pkg>.LiveDbScaleSeeder \
    <pkg>.test/androidx.test.runner.AndroidJUnitRunner
adb shell run-as <pkg> ls -l /data/data/<pkg>/databases/   # prove it landed
```

Delete the seeder and `pm clear` the app afterwards. It is scaffolding, not a test.

## 2. Measure with a control, never alone

```bash
adb shell dumpsys gfxinfo <pkg> reset
# ~6 swipes down, ~4 up, ~0.35s apart
adb shell dumpsys gfxinfo <pkg>   # Janky frames: N (P%), 95th percentile
```

Two controls are mandatory:

- **An empty-database run of the same screens.** Data-dependent cost only exists
  if the seeded run is worse than the empty one.
- **A screen whose content does not depend on the data.** If that screen also
  moves between runs, you are measuring the renderer, not the app.

## 3. Establish the noise floor BEFORE concluding

Repeat one identical sweep 5 times and take the range:

```
Codex janky% across 5 identical sweeps: 37.6 32.0 32.6 36.6 26.5  -> 11-point range
```

Any difference smaller than that range is not evidence. A real observed case:
a 26% -> 57% gap looked decisive, the memoisation that "fixed" it moved
57.0 -> 53.9 (inside the noise), and the data-independent control screen swung
26.8 -> 49.6 on unchanged code. Correct verdict: **the emulator cannot attribute
frame time; a real-device measurement is owed.**

## 4. Judge the optimisation on its own merits

Work that runs per-recomposition over the whole dataset (`groupBy`, `sortedBy`,
`sumOf` on `ui.*` collections inside composition) is worth hoisting into
`remember(key)` on algorithmic grounds. Say that plainly in the comment. Do NOT
write "measured as N% janky" unless the number survived step 3.

## 5. The `LazyListScope` trap — and when to revert

A `LazyColumn` content lambda is **not composable**, so it cannot `remember`.
Memoising work inside it forces the state read up into the parent body, which
adds a recomposition hop before content appears. Under a paused Compose test
clock (`compose.mainClock.advanceTimeBy`) that extra hop makes content miss the
assertion window and an existing test fails.

Attribute before blaming the test:

```bash
git show HEAD:<file> > /tmp/orig.kt   # swap in HEAD's copy of the ONE file
# run the single test against HEAD's copy, then against yours
```

If HEAD passes and yours fails, the change caused it. An optimisation with no
measurable benefit does not get to weaken a passing test — **revert it**. If it
is ever shown to matter, move the derivation into the ViewModel flow (off-frame
entirely) rather than hoisting reads in the UI.

## Windows/git gotcha seen while doing this

After Python rewrites a file during mutation testing, `cmp` may report differing
bytes while `git diff` shows nothing — that is `core.autocrlf=true` (worktree
CRLF, `git show` emits LF), not damage. Check `git status` and `git diff`, not
`cmp`, before panicking.
