---
name: duo-performance
description: "Keeps an iPhone Duo app smooth when the phone folds and unfolds. One fold changes the app's layout size in several steps (a full-width view went 382 → 466 → 951 → 867 pt on open), and every body that reads the size runs at each step; at 120 Hz a frame lasts 8.3 ms. Measures what each fold costs the main thread on the iPhone Duo simulator with duo-fold-cost (Instruments' Hangs and os_signpost instruments while duo-pose folds the phone, with a saved run to compare against), finds the cause, and fixes it: no sorting, formatting or decoding in body, the size read once as a small value, identity kept across poses, lazy rows, follow-up work after the fold settles. Splits hitch and hang time by pose from real users with iOS 27 MetricKit and StateReporting. Says what the simulator can't measure (frame rate, hitches, the SwiftUI instrument) and what to check on a device. Use when a Duo app freezes, stutters or drops frames on fold or unfold, before a release, or to keep a fold from getting slower."
metadata:
  verified: "Xcode 27.1 (27A9275), iOS 27.1 simulator, device: no"
  sources: "https://github.com/Kimeur/duology/blob/main/reference/sources.md"
---

# duo-performance

Make opening and closing iPhone Duo cheap for your app, prove it with numbers, and keep it that way.

Load other skills for the work around it: `duo-transitions` (the motion itself, the 120 Hz frame budget, `CADisplayLink`, the hinge stream), `duo-layout` and `duo-continuity` (one layout that changes shape, state that survives the fold), `duo-pose-matrix` (`duo-pose`, which this skill's script uses), `duo-testing` (launch switches and sample data).

Labels: *measured* means we ran it on the iPhone Duo simulator (iOS 27.1) on 6 November 2026; details in [references/evidence.md](references/evidence.md). *Unverified* means we could not confirm it. Nothing here has run on a real iPhone Duo; [references/device-checks.md](references/device-checks.md) lists what to check there.

## What one fold costs

- **Several resizes, not one.** While the window grows from 466 to 951 pt (`duo-transitions`), a full-width view went through three widths in about 100 ms (*measured*): 382 → 466 → 951 → 867 pt, as the safe area insets changed. UIKit updates the scene metrics (`Window / UpdateSceneMetrics` signposts, three in that open), and SwiftUI reruns `body` for every view that reads the size, lays out again and commits a frame. Closing changed that view's width once, to 382 pt.
- **The budget.** Both displays run up to 120 Hz; a frame lasts 8.3 ms ([Understanding hitches](https://developer.apple.com/documentation/xcode/understanding-hitches-in-your-app)). While the main thread runs without going back to its run loop, the app can't commit a new frame; only animations already handed to the render server keep moving.
- **What an app pays** (*measured*, Release builds, median of 3 folds):

  | App | Open: longest stretch / busy | Close: longest / busy |
  |---|---|---|
  | A grid of 3,000 cells, work done once | 29 ms / 71 ms | 14 ms / 45 ms |
  | The same, with a sort and a date formatter in `body` | 486 ms / 517 ms | 137 ms / 154 ms |
  | `Ledger` eval fixture: 2,000 rows, all the mistakes below | 2,913 ms / 4,370 ms | 1,645 ms / 1,683 ms |
  | `Ledger` fixed by hand with the steps below | 86 ms / 115 ms | 15 ms / 45 ms |

- **The first fold after launch costs the most** (*measured*: 71 and 43 ms longest on the fast grid, then 15 to 30 ms; 269 ms on the fixed `Ledger`, then 86 and 14 ms). Caches, first layouts of the wide variant and first appearances happen then.
- These are simulator numbers: it runs on the Mac's CPU and draws at 60 Hz (`maximumFramesPerSecond` = 60, *measured* in Duology's [device facts](https://github.com/Kimeur/duology/blob/main/reference/device-facts.md#displays)). Use them to compare and to find causes. They are not device timings.

## Rules

1. Measure before you change anything, and after. Same Mac, same simulator, a Release build, at least 3 cycles.
2. `body` only describes views. No sorting, filtering, grouping, summing, formatter creation, date or number formatting of many items, image decoding or I/O in it. Do that once, when the data changes.
3. Read the size once, high up, and pass down the one value the layout needs (a Boolean, a column count). Not a `GeometryReader` per row.
4. Keep identity through the fold: one layout that changes shape (`AnyLayout`, a custom `Layout`), never an `if` that builds the same content twice, never `.id(size)`.
5. Long content is lazy: `List`, `LazyVStack`, `LazyVGrid`.
6. Work that follows a fold (new prefetch, a reload for a new column count) waits until the fold settles, and runs off the main thread when it can.
7. Smoothness is tested on a device. The simulator can't show 120 Hz or count hitches.

## Step 1. Measure on the simulator

`scripts/duo-fold-cost` folds the phone with `duo-pose` while Instruments records the app's main thread, then reports each fold. The app needs no changes.

Needs: Xcode 27.1, the iPhone Duo simulator booted and shown in Device Hub, the app installed, and `duo-pose status` saying "Ready" (it presses Device Hub's pose buttons through the Accessibility permission; see `duo-pose-matrix`). It uses an existing simulator and never creates one.

```bash
DD=/tmp/myapp-dd; UDID=<the iPhone Duo UDID>
DEVELOPER_DIR=/Applications/Xcode-27.1.app/Contents/Developer xcodebuild -project MyApp.xcodeproj \
  -scheme MyApp -configuration Release -destination "id=$UDID" -derivedDataPath "$DD" build
xcrun simctl install "$UDID" "$DD/Build/Products/Release-iphonesimulator/MyApp.app"
scripts/duo-fold-cost run com.example.myapp --save before.json
```

```text
Fold (median)           longest     busy   >8.3ms  stalls  hangs
closed -> open           2913 ms  4370 ms        3       3      2   (3 runs)
open -> closed           1645 ms  1683 ms        3       3      1   (3 runs)
```

| Column | What it is |
|---|---|
| longest | The longest time the main thread ran without going back to its run loop: the app can't commit a frame before it ends. Watch this one first. |
| busy | The main thread's total running time during the fold. |
| >8.3ms | Stretches longer than one 120 Hz frame. |
| stalls | UIKit's own count of update cycles that stalled (`UpdateCycle.Stalls`). |
| hangs | What Instruments' Hangs instrument reported (its threshold: 100 ms). |

- Change the poses with `--poses open,book,tabletop,closed`, the count with `--cycles 5`, and pass launch arguments after `--` (`-- -sampleData`). Launch the app on the screen you want to measure (`duo-testing`, launch switches).
- After a change: `scripts/duo-fold-cost run com.example.myapp --compare before.json`. It prints what got slower or faster, and exits 1 when a median grew by at least 25 % and 20 ms.
- `--time-profiler` adds the Time Profiler instrument and names the code the main thread was in during each fold's longest stretch (*measured* on the slow grid: `closure #1 in slowSorted(_:)` 79 %). It keeps the trace for Instruments.

How it works, every column and exit code, and recording a trace by hand: [references/measure.md](references/measure.md).

## Step 2. Find the cause

1. Run with `--time-profiler`. Mostly your code in the longest stretch: move that work out of `body`. Mostly "(system)": SwiftUI and UIKit are laying out or rebuilding too many views (*measured* on `Ledger`: 81 to 83 % system, the rest in `EntryRow.body`). For more, open the trace in Instruments at the fold's time.
2. See why a view's `body` runs on a fold: add `let _ = Self._printChanges()` as its first line for a run, fold, and read the console ([WWDC23 Demystify SwiftUI performance](https://developer.apple.com/videos/play/wwdc2023/10160/)). Remove it after.
3. Mark your own work with an `OSSignposter` interval: it shows next to the fold in the os_signpost instrument.
4. Read the list of causes below against your `body` properties: each fold runs them several times.

On the simulator, Instruments' SwiftUI template doesn't record (*measured*: "Hitches is not supported on this platform."), the SwiftUI instrument added to a recording gets no data, and `XCTHitchMetric` returns no values. Use them on a device.

## Step 3. Fix

| What the trace shows | Cause | Fix |
|---|---|---|
| One long stretch per resize step, in your `body` | Sorting, grouping, summing or formatting in `body` | Do it once in a model when the data changes; `body` reads finished values |
| Long stretches in layout, many rows | A non-lazy stack of every row | `List`, `LazyVStack` or `LazyVGrid` |
| Rows re-laid out at every step | A `GeometryReader` in each row | Read the size once, high up; pass a value |
| The whole screen rebuilt, scroll and selection lost | `if wide { … } else { … }` building the same views twice, or `.id(width)` | `AnyLayout` or a custom `Layout`; no `.id` tied to the size |
| The same action runs several times per fold | `onGeometryChange` returning the raw size | Return the small value the layout needs: it runs only when that changes |
| Work right after the fold | A reload or prefetch on each resize step | `.task(id:)` on the small value, with a short wait, off the main thread |
| Images decode again at each size (*unverified* on Duo) | Decoding at the view's current size | Decode once, sized for the largest display, off the main thread |

Code for each fix, all typechecked: [references/fixes.md](references/fixes.md).

## Step 4. Keep it from coming back

- Keep a saved run per Mac (`--save main.json` on the main branch) and run `--compare main.json` before merging work that touches a screen people fold on. Numbers from different Macs don't compare.
- Put the work you moved out of `body` in plain functions or a model, and test them on the Mac with `XCTClockMetric` or a logic test (`duo-testing`). They are where a regression comes back.
- Run `duo-fold-cost` before each release, next to `/duo-ship`.

## Step 5. From real users (iOS 27)

MetricKit can split its daily report by a state the app reports, with the StateReporting framework ([MetricManager](https://developer.apple.com/documentation/metrickit/metricmanager), [StateReporter](https://developer.apple.com/documentation/statereporting/statereporter)). State entries carry hang time, hitch time, terminations and signpost intervals ([MetricReport](https://developer.apple.com/documentation/metrickit/metricreport)). Report the pose, and you get hitches and hangs per pose from real phones.

- Report `closed`, `open`, `book` or `tabletop` from the fold geometry, once the pose has held for half a second: one fold passes through several sizes, and Apple warns that reporting faster than "user interaction timescales" can be rate-limited.
- Mark each fold as an animation interval with `mxSignpostAnimationIntervalBegin`, so the report counts hitches during folds.
- *Measured* on the simulator: the pose transitions show in Instruments (Points of Interest, a State Reporting track), labelled correctly in all four poses. The fold intervals from MetricKit's log handle didn't appear, and no report arrives on the simulator.

The code, which also builds for iOS 26 and does nothing there: [references/field.md](references/field.md).

## Step 6. On a device

The simulator can't tell you whether folds are smooth at 120 Hz. On an iPhone Duo, profile Open and Close with the Animation Hitches template, run your UI tests with `XCTHitchMetric`, and watch the Hitches metric in Xcode Organizer. The list, with what we expect and what would change this skill: [references/device-checks.md](references/device-checks.md).

## Checklist

- [ ] A saved `duo-fold-cost` run from before the change, and a `--compare` after it
- [ ] No sorting, grouping, summing, formatter creation or decoding in any `body`
- [ ] The size read once per screen, as the value the layout needs
- [ ] One layout that changes shape; no `if` that builds the same content twice; no `.id` tied to the size
- [ ] Long content in `List`, `LazyVStack` or `LazyVGrid`
- [ ] Follow-up work in `.task(id:)` after the fold settles, off the main thread
- [ ] Images decoded once, for the largest display
- [ ] Pose reported to MetricKit (iOS 27), fold intervals marked
- [ ] Device checks done, or listed as not done
