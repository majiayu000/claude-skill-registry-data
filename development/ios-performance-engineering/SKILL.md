---
name: ios-performance-engineering
description: Measure and fix iOS/macOS performance with Instruments (Time Profiler, Allocations, Hangs, App Launch), `xctrace` in CI, `OSSignposter`, MetricKit field telemetry (`MXMetricManager`, `MXHangDiagnostic`), `XCTMetric` baselines, launch time, memory footprint, binary size, and crash triage / symbolication (`MXCrashDiagnostic`, dSYM, `atos`). Use when diagnosing hangs or hitches measured with Instruments or MetricKit, high memory, slow launch, or a large binary, reading or symbolicating a crash report, wiring MetricKit, or setting CI perf baselines. SwiftUI-specific hitch triage from code review → apple-skills:guide-swiftui-performance-audit or swiftui-expert's `.trace` toolchain; this skill owns measurement and the system-level surface.
---

# iOS Performance Engineering

## When to invoke

- Diagnosing UI slowness, scroll hitches, or app hangs.
- Investigating high memory usage, leaks, or large binary size.
- Wiring MetricKit to receive field performance data from real devices.
- Setting up `XCTMetric` / `measure {}` baselines in CI.
- Deciding whether to move work off `@MainActor` and how to do it safely.
- Evaluating launch time before a release.

## Instruments — the primary measurement tool

Never guess at a performance problem; profile first. Instruments ships with Xcode.

| Symptom | Instrument / template | Metric to read |
|---|---|---|
| High CPU / slow interactive path | Time Profiler | inverted call tree, self time > 5 ms on main thread |
| Unbounded memory growth | Allocations (Generation) | allocations that grow across repeated actions |
| Scroll / animation stutter | Animation Hitches | `hitch rate` (ms of hitch per second) |
| Main-thread freeze / spin | Hangs | block duration ≥ 250 ms |
| Slow cold launch | App Launch | time to first committed frame |
| Excessive SwiftUI re-renders | SwiftUI instrument | body invocation count, triggering property |

Key templates, condensed (full walkthrough of each template's UI: `references/instruments-templates.md`):

- **Time Profiler**: a function taking >5 ms on the main thread in an interactive path is a candidate for offloading.
- **Allocations**: the "Leaks" instrument detects reference cycles automatically but misses logical leaks (objects kept alive longer than needed).
- **Hangs instrument** (Xcode 14+): default threshold **250 ms**.
- **Hitches**: use the Animation Hitches template — the standalone "Core Animation" template no longer exists. Hitch rate (ms of hitch per second of scrolling): <5 ms/s is good; 5–10 ms/s is concerning; >10 ms/s is critical.

### `os_signpost` — annotate your own intervals

```swift
import os

let log = OSLog(subsystem: "com.example.MyApp", category: .pointsOfInterest)
let id = OSSignpostID(log: log)

os_signpost(.begin, log: log, name: "ImageDecode", signpostID: id)
let image = decodeImage(data)
os_signpost(.end, log: log, name: "ImageDecode", signpostID: id)
```

Signpost intervals appear in the Instruments timeline as coloured spans. Use `.event` for instantaneous markers (user taps, cache misses). Prefer `OSSignposter` (iOS 15+/macOS 12+, introduced WWDC 2021; Swift-only wrapper over C `os_signpost`) from the `os` framework — it supports structured metadata:

```swift
let signposter = OSSignposter(subsystem: "com.example.MyApp", category: "Render")
let state = signposter.beginInterval("TileRender", id: signposter.makeSignpostID())
// ... work ...
signposter.endInterval("TileRender", state)
```

### `xctrace` — Instruments from CI

```bash
xctrace record --template 'Time Profiler' --output trace.trace --time-limit 30s --launch -- /path/App.app
```

`--launch -- command` must come last: everything after `--` is passed through to the launched process, so `--output` / `--time-limit` have to precede it or they get swallowed as app launch arguments instead of being read by `xctrace` itself.

`xctrace` can drive any built-in or custom Instruments template headlessly and export the trace as a `.trace` file. Post-process with `xctrace export` to pull out human-readable XML. Wire this into a CI step on a dedicated Mac runner to catch regressions before they reach users.

## Hangs and hitches

The system classifies a main-thread block of **250 ms or more** as a hang and surfaces it in the Organizer → Hang Reports (Xcode 14+) and via MetricKit's `MXDiagnosticPayload.hangDiagnostics` (an array of `MXHangDiagnostic` — there is no `MXHangDiagnosticPayload` type). The scroll hitch budget depends on display refresh rate (see above). A hang that the watchdog ends (`EXC_CRASH (SIGKILL)`, code `0x8badf00d`) arrives as a crash, not a hang report — triage it via `references/crash-triage.md`.

**Moving work off `@MainActor`:**

```swift
// Wrong — blocks the main thread
func loadData() {
    let json = try! Data(contentsOf: remoteURL)   // network I/O on main thread
    items = try! JSONDecoder().decode([Item].self, from: json)
}

// Right — async, main actor only for the final UI update
func loadData() async throws {
    let json = try await URLSession.shared.data(from: remoteURL).0
    let decoded = try JSONDecoder().decode([Item].self, from: json)
    await MainActor.run { items = decoded }
}
```

For CPU-heavy processing (image decoding, compression, sorting large arrays), use `Task.detached(priority: .userInitiated)` or dispatch to a background `Actor`. Never use `DispatchQueue.global().async` in new Swift 6 code — prefer structured concurrency.

One-shot bootstrapping on first appearance belongs in `.task` — the correct Apple-recommended modifier for async work tied to view lifetime. See `swiftui-interaction-footguns` for `.task` re-fire semantics on view identity changes.

## Launch time

Launch time splits into two phases:

**Pre-main (dyld)** — loading and linking dylibs before `main()` runs. Minimise by: keeping the embedded dylib count low (prefer static libraries for non-system frameworks), avoiding `+load` methods, and not registering large numbers of `@objc` classes at startup. The **App Launch** Instruments template shows the pre-main timeline. Target: under 400 ms on a cold launch on the slowest supported device.

**Post-main / first frame** — everything from `application(_:didFinishLaunchingWithOptions:)` through the first committed frame. Defer every initialisation that is not required to display the initial screen. CloudKit containers, network prefetches, and analytics SDKs should be lazy. Measure with the **App Launch** template and the `os_signpost` `.begin`/`.end` around your own startup phases.

Common traps: eager `CKContainer.default()` on the main thread (hangs until entitlement check completes), synchronous keychain reads at app start, and large SQLite `PRAGMA` operations before the first view renders.

## Memory

**Footprint vs leaks**: Instruments Allocations shows the heap; use `vmmap` or the Memory Debugger in Xcode to see the full virtual memory map (dirty pages, compressed pages, mapped files). The OS terminates apps that exceed their footprint budget silently — a JetsamEvent log entry whose reason reads `per-process-limit` (or `highwater`). Reduce by:

- **Image downsampling**: never decode a 4K image to display it at 100 pt. Use `ImageIO` with `kCGImageSourceThumbnailMaxPixelSize` or `UIGraphicsImageRenderer` to decode at display resolution. For the `downsample(imageAt:to:scale:)` sample, read `references/samples.md`.
- **`autoreleasepool`** in tight loops that allocate many Objective-C objects (e.g. iterating `NSManagedObject` fetches, calling `UIImage(named:)` in a loop). The pool drains at the end of each `autoreleasepool { }` block rather than at the runloop turn boundary.
- **Retain cycles**: `[weak self]` in closures stored on `self`; `weak var delegate` in delegation patterns. The Leaks instrument and the Memory Graph Debugger (product menu → Debug Memory Graph) visualise the reference graph and highlight cycles in red.

## Binary size

Large binaries increase download time and App Store review scrutiny. Two primary levers:

- **Dead code stripping** (`DEAD_CODE_STRIPPING = YES` in Xcode build settings, default on for Release). Removes unreachable functions and data sections.
- **`-Osize`** (`SWIFT_OPTIMIZATION_LEVEL = -Osize`): optimises for binary size rather than speed. Typically 5–30% smaller than `-O`, with a runtime cost below 5% for most apps.

For asset catalog / app thinning, Link Map analysis, and trimming unused SDK resource bundles, read `references/official-docs.md`.

## MetricKit — field performance telemetry

MetricKit delivers on-device aggregated performance metrics to your app once per day (diagnostic payloads are delivered immediately, with no disconnect-from-Xcode condition, since iOS 15 / macOS 12). For the full `MXMetricManagerSubscriber` receiver sample, read `references/samples.md`. `MXMetricManager` / `MXMetricManagerSubscriber` are deprecated from iOS / macOS 27 in favour of `MetricManager().metricReports` (`for await`) — the catalog floor is 26, so the sample below still applies; see `apple-three-piece-analytics` and `telemetry-facade-pattern` for the 27+ shape.

MetricKit data reflects **real user conditions** (actual device, network, battery state), making it the authoritative source for field performance signals. Key metric classes:

| Class | What it measures |
|---|---|
| `MXCPUMetric` | Cumulative CPU time (user + system) |
| `MXMemoryMetric` | Peak memory (`peakMemoryUsage`) and average suspended memory (`averageSuspendedMemory`) — there is no average-memory property |
| `MXDisplayMetric` | Average pixel luminance (not the hitch signal) |
| `MXAnimationMetric` | `scrollHitchTimeRatio` — field-measured ratio of hitch time while scrolling (the hitch signal) |
| `MXDiskIOMetric` | Cumulative logical write bytes |
| `MXHangDiagnostic` | Call tree for a main-thread hang > 250 ms |
| `MXCrashDiagnostic` | Crash reason + call tree — for intake channels, symbolication and the exception-type cheat sheet, read `references/crash-triage.md` |
| `MXCPUExceptionDiagnostic` | CPU runaway above system threshold |

Wire MetricKit as a **sink** in your telemetry facade (per `telemetry-facade-pattern`) — a `MetricKitSink` that subscribes to `MXMetricManager.shared` and broadcasts payloads as `TelemetryEvent` instances. This keeps MetricKit wiring out of `AppDelegate` and testable via protocol injection. Note that MetricKit complements but does not replace the analytics tracking covered in `apple-three-piece-analytics`: MetricKit is system-generated aggregate performance data, not user behaviour events.

## `XCTMetric` and `measure {}` baselines in CI

For the `testScrollPerformance` sample wiring `XCTOSSignpostMetric.scrollDecelerationMetric`, `XCTMemoryMetric`, and `XCTCPUMetric` into `measure {}`, read `references/samples.md`.

`measure {}` runs the block `iterationCount + 1` times (default 5 recorded + 1 discarded warm-up) and records the mean of the recorded runs. On first run, set the baseline via the inline editor in Xcode. Subsequent runs fail on either of two independent thresholds, both configurable per metric: **Max % Relative Standard Deviation** (default 10%) and **Max % Deviation** from the baseline average (default 10%) — exceeding either one fails the test; it is not a single product formula. Commit baselines in `.xcbaseline` files alongside the test file.

For server-side CI (where a physical display is unavailable), use `XCTCPUMetric` and `XCTMemoryMetric` in unit tests that exercise logic without UIKit rendering. UI performance metrics require a simulator or device with an active display session.

## Verification checklist

- Profile with Instruments before claiming a fix; never tune by guessing.
- Time Profiler run completed; hot paths on the main thread identified and either offloaded or bounded.
- Allocations generation diff shows no unbounded growth across repeated user actions.
- SwiftUI instrument checked for unexpected body re-render counts on the primary screen.
- `os_signpost` intervals added around any operation expected to take > 16 ms.
- `MXMetricManagerSubscriber` registered in the composition root; payloads forwarded to the telemetry sink.
- `XCTMetric` baseline committed for the primary performance-sensitive test; CI fails on regression.
- No synchronous network or file I/O on the main thread (audited via the Hangs instrument, Time Profiler, and `os_signpost` around suspect call sites — Thread Sanitizer only detects data races and will not flag this).
- Image assets decoded at display resolution, not source resolution.
- Binary size measured with `-Osize` before each major release; asset catalog slices verified.

## Related skills

- `telemetry-facade-pattern`: wire `MetricKitSink` as one sink in the fan-out facade; keep `MXMetricManagerSubscriber` registration out of `AppDelegate`.
- `apple-three-piece-analytics`: decides *which* Apple-only sources (ASC Analytics / MetricKit / Game Center) to rely on and whether a third-party SDK is justified; this skill owns *reading and acting on* MetricKit payloads for performance diagnosis.
- `swift6-concurrency`: moving work off `@MainActor` correctly requires understanding actor isolation, `Task.detached`, and `Sendable` constraints — the primary tool for eliminating main-thread hangs.
- `swiftui-expert:swiftui-expert-skill` (aggregated external): for the **SwiftUI body-re-render** slice specifically, it ships an Instruments `.trace` analysis toolchain — prefer it for that profiling. This skill owns the broader surface (Time Profiler / Allocations / hangs / launch / memory / binary size / MetricKit / XCTMetric).
- `apple-skills:guide-swiftui-performance-audit` (aggregated external): code-first SwiftUI review (view-update causes, layout thrash) with user-run Instruments; this skill owns measurement (Instruments/xctrace/MetricKit/XCTMetric) and the non-SwiftUI surface (launch, memory, binary size).
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
