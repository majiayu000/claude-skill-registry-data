---
name: metrickit
description: "Collect and analyze on-device performance metrics and crash diagnostics using MetricKit. Use when setting up MXMetricManager, handling MXMetricPayload or MXDiagnosticPayload, processing crash/hang/disk-write diagnostics via MXCallStackTree, adding custom signpost metrics, or uploading telemetry to an analytics backend."
---

# MetricKit

Collect aggregated performance metrics and crash diagnostics from production
devices using MetricKit. The framework delivers daily metric payloads (CPU,
memory, launch time, hang rate, animation hitches, network usage) and
immediate diagnostic payloads (crashes, hangs, disk-write exceptions) with
full call-stack trees for triage.

## Contents

- [Subscriber Setup](#subscriber-setup)
- [Receiving Metric Payloads](#receiving-metric-payloads)
- [Receiving Diagnostic Payloads](#receiving-diagnostic-payloads)
- [Key Metrics](#key-metrics)
- [Call Stack Trees](#call-stack-trees)
- [Custom Signpost Metrics](#custom-signpost-metrics)
- [Exporting and Uploading Payloads](#exporting-and-uploading-payloads)
- [Extended Launch Measurement](#extended-launch-measurement)
- [Xcode Organizer Integration](#xcode-organizer-integration)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Subscriber Setup

Register a subscriber as early as possible — ideally in
`application(_:didFinishLaunchingWithOptions:)` or `App.init`. MetricKit
starts accumulating reports after the first access to `MXMetricManager.shared`.

```swift
import MetricKit

final class MetricsSubscriber: NSObject, MXMetricManagerSubscriber {
    static let shared = MetricsSubscriber()

    func subscribe() {
        MXMetricManager.shared.add(self)
    }

    func unsubscribe() {
        MXMetricManager.shared.remove(self)
    }

    func didReceive(_ payloads: [MXMetricPayload]) {
        // Handle daily metrics
    }

    func didReceive(_ payloads: [MXDiagnosticPayload]) {
        // Handle diagnostics (crashes, hangs, disk writes)
    }
}
```

### UIKit Registration

```swift
func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
) -> Bool {
    MetricsSubscriber.shared.subscribe()
    return true
}
```

### SwiftUI Registration

```swift
@main
struct MyApp: App {
    init() {
        MetricsSubscriber.shared.subscribe()
    }
    var body: some Scene {
        WindowGroup { ContentView() }
    }
}
```

## Receiving Metric Payloads

`MXMetricPayload` arrives approximately once per 24 hours containing
aggregated metrics. The array may contain multiple payloads if prior
deliveries were missed.

```swift
func didReceive(_ payloads: [MXMetricPayload]) {
    for payload in payloads {
        let begin = payload.timeStampBegin
        let end = payload.timeStampEnd
        let version = payload.latestApplicationVersion

        // Persist raw JSON before processing
        let jsonData = payload.jsonRepresentation()
        persistPayload(jsonData, from: begin, to: end)

        processMetrics(payload)
    }
}
```

**Availability**: `MXMetricPayload` — iOS 13.0+, macOS 10.15+, visionOS 1.0+

## Receiving Diagnostic Payloads

`MXDiagnosticPayload` delivers crash, hang, CPU exception, disk-write, and
app-launch diagnostics. On iOS 15+ and macOS 12+, diagnostics arrive
immediately rather than bundled with the daily report.

```swift
func didReceive(_ payloads: [MXDiagnosticPayload]) {
    for payload in payloads {
        let jsonData = payload.jsonRepresentation()
        persistPayload(jsonData)

        if let crashes = payload.crashDiagnostics {
            for crash in crashes {
                handleCrash(crash)
            }
        }
        if let hangs = payload.hangDiagnostics {
            for hang in hangs {
                handleHang(hang)
            }
        }
        if let diskWrites = payload.diskWriteExceptionDiagnostics {
            for diskWrite in diskWrites {
                handleDiskWrite(diskWrite)
            }
        }
        if let cpuExceptions = payload.cpuExceptionDiagnostics {
            for cpuException in cpuExceptions {
                handleCPUException(cpuException)
            }
        }
        if let launchDiags = payload.appLaunchDiagnostics {
            for launchDiag in launchDiags {
                handleSlowLaunch(launchDiag)
            }
        }
    }
}
```

**Availability**: `MXDiagnosticPayload` — iOS 14.0+, macOS 12.0+, visionOS 1.0+

## Key Metrics

### Launch Time — MXAppLaunchMetric

```swift
if let launch = payload.applicationLaunchMetrics {
    let firstDraw = launch.histogrammedTimeToFirstDraw
    let optimized = launch.histogrammedOptimizedTimeToFirstDraw
    let resume = launch.histogrammedApplicationResumeTime
    let extended = launch.histogrammedExtendedLaunch
}
```

### Run Time — MXAppRunTimeMetric

```swift
if let runTime = payload.applicationTimeMetrics {
    let fg = runTime.cumulativeForegroundTime    // Measurement<UnitDuration>
    let bg = runTime.cumulativeBackgroundTime
    let bgAudio = runTime.cumulativeBackgroundAudioTime
    let bgLocation = runTime.cumulativeBackgroundLocationTime
}
```

### CPU, Memory, and Responsiveness

```swift
if let cpu = payload.cpuMetrics {
    let cpuTime = cpu.cumulativeCPUTime              // Measurement<UnitDuration>
}
if let memory = payload.memoryMetrics {
    let peakMemory = memory.peakMemoryUsage           // Measurement<UnitInformationStorage>
}
if let responsiveness = payload.applicationResponsivenessMetrics {
    let hangTime = responsiveness.histogrammedApplicationHangTime
}
if let animation = payload.animationMetrics {
    let scrollHitchRate = animation.scrollHitchTimeRatio  // Measurement<Unit>
}
```

### Network and Cellular

```swift
if let network = payload.networkTransferMetrics {
    let wifiUp = network.cumulativeWifiUpload          // Measurement<UnitInformationStorage>
    let wifiDown = network.cumulativeWifiDownload
    let cellUp = network.cumulativeCellularUpload
    let cellDown = network.cumulativeCellularDownload
}
```

### App Exit Metrics

```swift
if let exits = payload.applicationExitMetrics {
    let fg = exits.foregroundExitData
    let bg = exits.backgroundExitData
    // Inspect normal, abnormal, watchdog, memory, etc.
}
```

## Call Stack Trees

`MXCallStackTree` is attached to each diagnostic. Use `jsonRepresentation()` to extract frame data, then symbolicate with `atos` or by uploading dSYMs to your analytics service.

See [references/metrickit-patterns.md](references/metrickit-patterns.md) for crash/hang handling code and JSON structure details.

**Availability**: `MXCallStackTree` — iOS 14.0+, macOS 12.0+, visionOS 1.0+

## Custom Signpost Metrics

Use `mxSignpost` with a MetricKit log handle to capture custom performance
intervals. These appear in the daily `MXMetricPayload` under `signpostMetrics`.

```swift
let metricLog = MXMetricManager.makeLogHandle(category: "Networking")
```

See [references/metrickit-patterns.md](references/metrickit-patterns.md) for signpost emission patterns and reading custom metrics from payloads.

## Exporting and Uploading Payloads

Both payload types provide `jsonRepresentation()` for serialization. Always persist raw JSON to disk before processing — the system delivers each payload once. Use `pastPayloads` and `pastDiagnosticPayloads` on launch to recover missed deliveries.

See [references/metrickit-patterns.md](references/metrickit-patterns.md) for export code and past payload retrieval.

## Extended Launch Measurement

Track post-first-draw setup work as part of the launch metric:

```swift
let taskID = MXLaunchTaskID("com.example.app.loadDatabase")
MXMetricManager.shared.extendLaunchMeasurement(forTaskID: taskID)
await database.load()
MXMetricManager.shared.finishExtendedLaunchMeasurement(forTaskID: taskID)
```

Extended launch times appear under `histogrammedExtendedLaunch` in `MXAppLaunchMetric`.

## Xcode Organizer Integration

Xcode Organizer shows aggregated MetricKit data across opted-in users. Use it for trend analysis alongside on-device collection routed to your own backend.

See [references/metrickit-patterns.md](references/metrickit-patterns.md) for Organizer tab details.

## Common Mistakes

### DON'T: Subscribe to MXMetricManager too late

The system may deliver pending payloads shortly after launch. Subscribing
late (e.g., in a view controller) risks missing them entirely.

```swift
// WRONG — subscribing in a view controller
override func viewDidLoad() {
    super.viewDidLoad()
    MXMetricManager.shared.add(self)
}

// CORRECT — subscribe in application(_:didFinishLaunchingWithOptions:)
func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions opts: [UIApplication.LaunchOptionsKey: Any]?
) -> Bool {
    MXMetricManager.shared.add(metricsSubscriber)
    return true
}
```

### DON'T: Ignore MXDiagnosticPayload

Only handling `MXMetricPayload` means you miss crash, hang, and disk-write
diagnostics — the most actionable data MetricKit provides.

```swift
// WRONG — only implementing metric callback
func didReceive(_ payloads: [MXMetricPayload]) { /* ... */ }

// CORRECT — implement both callbacks
func didReceive(_ payloads: [MXMetricPayload]) { /* ... */ }
func didReceive(_ payloads: [MXDiagnosticPayload]) { /* ... */ }
```

### DON'T: Process payloads without persisting first

The system delivers each payload once. If your subscriber crashes during
processing, the data is lost permanently.

```swift
// WRONG — process inline, crash loses data
func didReceive(_ payloads: [MXDiagnosticPayload]) {
    for p in payloads {
        riskyProcessing(p)  // If this crashes, payload is gone
    }
}

// CORRECT — persist raw JSON first, then process
func didReceive(_ payloads: [MXDiagnosticPayload]) {
    for p in payloads {
        let json = p.jsonRepresentation()
        try? json.write(to: localCacheURL())   // Safe on disk
        Task.detached { self.processAsync(json) }
    }
}
```

### DON'T: Do heavy work synchronously in didReceive

The callback runs on an arbitrary thread. Blocking it with heavy processing
or synchronous network calls delays delivery of subsequent payloads.

```swift
// WRONG — synchronous upload in callback
func didReceive(_ payloads: [MXMetricPayload]) {
    for p in payloads {
        let data = p.jsonRepresentation()
        URLSession.shared.uploadTask(with: request, from: data).resume()  // sync wait
    }
}

// CORRECT — persist and dispatch async
func didReceive(_ payloads: [MXMetricPayload]) {
    for p in payloads {
        let json = p.jsonRepresentation()
        persistLocally(json)
        Task.detached(priority: .utility) {
            await self.uploadToBackend(json)
        }
    }
}
```

### DON'T: Expect immediate data in development

MetricKit aggregates data over 24-hour windows. Payloads do not arrive
immediately after instrumenting. Use Xcode Organizer or simulated payloads
for faster iteration during development.

## Review Checklist

- [ ] `MXMetricManager.shared.add(subscriber)` called in `application(_:didFinishLaunchingWithOptions:)` or `App.init`
- [ ] Subscriber conforms to `MXMetricManagerSubscriber` and inherits `NSObject`
- [ ] Both `didReceive(_: [MXMetricPayload])` and `didReceive(_: [MXDiagnosticPayload])` implemented
- [ ] Raw `jsonRepresentation()` persisted to disk before processing
- [ ] Heavy processing dispatched asynchronously off the callback thread
- [ ] `MXCallStackTree` JSON uploaded with dSYMs for symbolication
- [ ] Custom signpost metrics limited to critical code paths
- [ ] `pastPayloads` and `pastDiagnosticPayloads` checked on launch for missed deliveries
- [ ] Extended launch tasks call both `extendLaunchMeasurement` and `finishExtendedLaunchMeasurement`
- [ ] Analytics backend accepts and stores MetricKit JSON format
- [ ] Xcode Organizer reviewed for regression trends alongside on-device data

## References

- Extended patterns: [references/metrickit-patterns.md](references/metrickit-patterns.md)
- [MetricKit framework](https://sosumi.ai/documentation/metrickit)
- [MXMetricManager](https://sosumi.ai/documentation/metrickit/mxmetricmanager)
- [MXMetricManagerSubscriber](https://sosumi.ai/documentation/metrickit/mxmetricmanagersubscriber)
- [MXMetricPayload](https://sosumi.ai/documentation/metrickit/mxmetricpayload)
- [MXDiagnosticPayload](https://sosumi.ai/documentation/metrickit/mxdiagnosticpayload)
