---
name: apple-three-piece-analytics
description: 'Choose analytics and metrics sources for a solo / small-team Apple app and decide whether a third-party tracking SDK is justified. Use when picking an analytics SDK; when asked "should I add Firebase / Mixpanel / Amplitude / TelemetryDeck"; when asked what App Store Connect Analytics, MetricKit (`MXMetricPayload`) or Game Center can measure without an SDK; when the analytics choice drives `PrivacyInfo.xcprivacy` or forces ATT. Does NOT own MetricKit perf wiring (ios-performance-engineering), App Review privacy-label parity (app-store-review-rejections), or sink code (telemetry-facade-pattern).'
---

# Apple Three-Piece Analytics

## When to invoke

- Deciding on an analytics SDK.
- Evaluating Firebase / TelemetryDeck / Mixpanel / Amplitude / Sentry.
- Writing `PrivacyInfo.xcprivacy`.
- User asks "what metrics should I track", "what can I see without a third-party SDK".

## Scope

Owns the source-selection decision and its PrivacyInfo/ATT consequence. Does NOT own MetricKit wiring or payload interpretation → `ios-performance-engineering`; sink code → `telemetry-facade-pattern`; App Review privacy-label parity → `app-store-review-rejections`.

## Default decisions

### v1 uses the Apple three-piece set

| Source | What it provides | Where to view |
|---|---|---|
| **App Store Connect Analytics** | Downloads, sessions, active devices, retention, sources, store conversion | App Store Connect web |
| **MetricKit** (`MXMetricPayload`, `MXDiagnosticPayload`) | Performance & diagnostics: crash / hang / launch time / jank / energy / memory | The App receives them → persist to log / optionally upload later |
| **MetricKit, iOS / macOS 27+** (`MetricManager().metricReports` / `.diagnosticReports`, `for await`) | Same coverage; `MXMetricManager` / `MXMetricPayload` / `MXMetricManagerSubscriber` are deprecated starting iOS / macOS 27 | Same — catalog default is iOS 26, so no forced migration yet |
| **Game Center** (if it's a game) | Leaderboards / achievement completion / peer-player comparison | Game Center API / Game Center app |

> **macOS caveat**: Apple's API lists `MXMetricManagerSubscriber` on macOS 12 and later; which payloads a Mac actually delivers is not documented. Verify delivery on a device at your macOS floor, and fall back to App Store Connect Analytics + targeted `OSSignposter` traces if payloads don't arrive.

### Privacy / Manifest

- **`PrivacyInfo.xcprivacy` is a required deliverable** (hard App Store submission requirement since 2024-05-01 for any app using a required-reason API).
- **No third-party SDK doesn't mean a minimal manifest.** The required-reason API rule applies to the App's own code, not just third-party SDKs: using `UserDefaults`, file-modification timestamps, system boot time, disk-space APIs, or active-keyboards APIs each requires a declared entry in `NSPrivacyAccessedAPITypes` (e.g. `UserDefaults` → reason `CA92.1`); otherwise Apple sends a missing-reason email, and since 2024-05-01 such uploads aren't accepted by App Store Connect (details in `app-store-review-rejections`'s privacy-manifest reference). Almost every app uses `UserDefaults`, so the manifest needs at least that entry plus `NSPrivacyTracking: false`.
- **No ATT prompt needed** (no IDFA use case).
- CloudKit / Game Center's user-facing privacy notices are handled at the system layer by Apple; the App only needs to declare data usage in PrivacyInfo.

### What's not covered (explicitly accepted)

- Micro-behaviour streams like "which button was tapped" or "how long was spent on a screen" are **not** covered by the three-piece set.
- Confirm v1 doesn't need to answer these questions; deviate if it does.

## Rationale

- At solo / small-team scale, the three pieces cover most key questions (installs / retention / performance / crashes / player comparisons).
- No third-party SDK → no ATT, no extra tracking-domain disclosures, small build size, and the privacy claim is verifiable by readers via grep on `import`. (The required-reason API entries above are still needed — they come from the App's own code, not a third-party SDK.)
- Positive for a public-repo showcase ("no third-party tracking" is a credible commitment).

## Deviation considerations

### Adopt TelemetryDeck (privacy-friendly first)

- **Trigger**: actually need the micro-behaviour stream of "which button, where do users get stuck".
- **Priority**: TelemetryDeck > Firebase — Firebase does not require ATT and only reads the IDFA if AdSupport is linked, and has shipped its own `PrivacyInfo.xcprivacy` since 10.22.0 (2024-03); the reason to prefer TelemetryDeck is the smaller data-collection disclosure surface (tracking domains, more collected-data-type entries) and build size.
- **How to integrate**: swap in the `TrackingSink` implementation via `telemetry-facade-pattern`; call sites change nothing.

### Adopt Sentry / Crashlytics

- **Trigger**: MetricKit `MXDiagnosticPayload` persistence still isn't enough for the incident workflow.
- **Cost**: third-party SDK, extra PrivacyInfo entries, build size.

## Verification checklist

- `PrivacyInfo.xcprivacy` exists and passes App Store Connect validation.
- No `import Firebase*` / `import Sentry` / `import Amplitude`, etc.
- MetricKit subscription is wired (iOS ≤ 26: `MXMetricManager.shared.add(...)`; iOS 27+: `MetricManager()` and `for await` over `metricReports` / `diagnosticReports`).
- Game Center entitlement aligns with leaderboard / achievement definitions (for games).

## Related skills

- `telemetry-facade-pattern`: the sink implementations for each piece.
- `oslog-logger-defaults`: MetricKit payloads persist via OSLog.
- `apple-public-repo-security`: "no PII / no third-party SDK" is one of the public-repo commitments.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
