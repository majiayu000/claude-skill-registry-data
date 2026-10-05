---
name: telemetry-facade-pattern
description: Design the app-side event pipeline that fans one `telemetry.observe(event)` call out to logging, tracking, MetricKit and Game Center sinks. Use when deciding whether Logger and analytics tracking share one interface; when adding a `TelemetrySink` / `MetricKitSink` / `GameCenterSink`; when a wired-looking sink never fires (score not submitted, achievement not unlocked, `GKLeaderboard.submitScore` unreached); when sink order or UI-blocking sink I/O matters. Does NOT choose the Logger API (oslog-logger-defaults) or which analytics sources to use (apple-three-piece-analytics).
---

# Telemetry Facade Pattern

## When to invoke

- Starting a new project and designing the logger / tracker / metrics interface.
- About to introduce OSLog and any tracking / analytics at the same time.
- Wanting to preserve flexibility for "swap the tracking provider later".
- User asks "should Logger and Tracking be separate", "how should the event interface look".

## Default decisions

### A single `Telemetry` target

- Create one `Telemetry` target inside the SwiftPM Package.
- It contains:
  - `TelemetryEvent` value type (enum / struct, `Sendable`)
  - `TelemetrySink` protocol:
    ```swift
    public protocol TelemetrySink: Sendable {
        func receive(_ event: TelemetryEvent) async
    }
    ```
  - The main facade — choose the type per the table below. The facade fans out to multiple sinks.

    | Facade type | Use when | Cost |
    |---|---|---|
    | `actor Telemetry` (default) | any sink holds subscription identity (e.g. `MXMetricManagerSubscriber`) or does async I/O | `observe` is `async` |
    | `struct Telemetry: Sendable` | every sink is fully synchronous and stateless | no lifecycle owner for stateful sinks |
  - Default sinks (see below)

### Call sites describe only "what happened"

```swift
telemetry.observe(.sessionCompleted(id: sessionId, durationMs: 12_345))
```

- The call site **doesn't know** who will consume the event.
- Swapping providers / adding sinks only requires replacing a sink; call sites change nothing.

### Default sink set

| Sink | Receives | Purpose |
|---|---|---|
| `OSLogSink` | All events | Human-readable debug messages |
| `TrackingSink` (default `NoOpTrackingSink`) | Business events | v1 has no third-party tracking but the protocol is reserved; future swaps require zero call-site changes |
| `MetricKitSink` | OS 26 and earlier: `MXMetricManagerSubscriber` (≤26). OS 27+: hold a single `MetricManager()` instance (27+) | Performance / diagnostics persistence — base-class and actor-viability details: trap 6 in `references/wiring-traps.md` |
| `GameCenterSink` (games) | Completion / achievement events | Submit score / unlock achievement |

```swift
public struct NoOpTrackingSink: TelemetrySink {
    public init() {}
    public func receive(_ event: TelemetryEvent) async { /* intentionally empty */ }
}
```

### Composition root wiring

- The App target's DI composition root injects sinks into the facade.
- Sinks are **failure-isolated** (one sink throwing or timing out must not stop the others) but **not order-free**: the facade forwards in array order, and a sink that reads state another sink writes must come after it (see trap 2).

For the six composition-root wiring traps (existing-but-unwired sinks, sink
ordering, blocking I/O on the gameplay path, late-binding, sink-fired vs
terminal-call-succeeded — `GKLeaderboard.submitScore` / `GKAchievement.report`
never reached — and `MetricKitSink`'s OS-version-dependent base class), read
`references/wiring-traps.md`.

## Rationale

- Decouples call sites from consumers: v1 can use `telemetry.observe(...)` with no external tracking, and a future TelemetryDeck / in-house pipeline only swaps the sink.
- OSLog + Tracking + MetricKit + GameCenter are all "event streams"; one unified interface is easier to maintain than four separate ones.
- Easy to test: inject a fake sink and assert on the event stream.

## Deviation considerations

- **Minimal App, OSLog only**: you can skip the `Telemetry` target and use `Logger` directly. But **if you anticipate adding tracking / metrics later**, building the facade up front pays off.
- **Need *routing* between sinks** (e.g. a MetricKit payload re-emitted into `TrackingSink`): handle routing inside the facade; call sites still unchanged.
- **Cross-platform** (Android / Linux): facade interface stays platform-neutral; sink implementations are per-platform.

## Verification checklist

- The `Telemetry` target is standalone; UI / Engine don't directly depend on anything beyond OSLog.
- `TelemetryEvent` is a value type, `Sendable`.
- A default `NoOpTrackingSink` is provided and wired in the composition root.
- Tests assert on event streams via fake sinks, not by parsing OSLog output.
- **The live composition root's sinks array actually contains every sink you
  intend to fire** (not just that the sink type exists) — the "existing-but-unwired" failure mode.
- Read/write-dependent sinks are ordered so writers precede readers, with a test
  pinning the order.
- I/O sinks on a gameplay-reachable completion path forward non-blocking; the
  interactive path is never frozen by a sink's CloudKit/GameKit work.
- The terminal platform call (GameKit/StoreKit) is reached and device-verified —
  not just the sink.

## Related skills

- `oslog-logger-defaults`: the concrete `OSLogSink` implementation dependency.
- `apple-three-piece-analytics`: each piece corresponds to one sink.
- `swiftpm-modularization`: why `Telemetry` is its own target.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
