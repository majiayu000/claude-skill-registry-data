---
name: oslog-logger-defaults
description: Set up logging for an Apple-platform Swift app with `os.Logger` and decide its `subsystem` / `category` naming and `privacy:` interpolation. Use when choosing a logging library (`os.Logger` vs swift-log `import Logging` vs CocoaLumberjack); when writing the first `Logger(subsystem:category:)`; when deciding `.private` vs `.public` for a value; when asked what `.private` hides in Console.app, sysdiagnose, or `OSLogStore`. Does NOT cover `os_signpost` / Instruments profiling (ios-performance-engineering) or fanning logs out to trackers (telemetry-facade-pattern).
---

# OSLog / `os.Logger` Defaults

## When to invoke

- Starting a new Apple-platform project and picking a logging library.
- Writing the first `Logger` declaration.
- Deciding the default for privacy interpolation.
- User asks "OSLog vs SwiftLog vs CocoaLumberjack", "`.private` vs `.public` how to pick".

## Default decisions

- **Use Apple's built-in `os.Logger`** (`import os`); **do not pull in any third-party logging library**.
- Naming conventions:
  - `subsystem` = bundle ID (e.g. `com.example.myapp`)
  - `category` = module name (aligned with the SwiftPM target name)
- **Privacy interpolation is type-dependent, not "all private"**: dynamic strings and complex objects default to `.private`; integer, floating-point, and Boolean values default to `.public`. Any identifying numeric value (player ID, user ID, serial number) must be marked `.private` explicitly.

```swift
import os

extension Logger {
    static let engine = Logger(subsystem: "com.example.myapp", category: "Engine")
}

Logger.engine.info("user \(userId, privacy: .public) loaded puzzle \(puzzleId, privacy: .private)")
//                                    ^^^^^^^ explicit public       ^^^^^^^ explicit private —
//                                                                    identifying values need this
//                                                                    even when the type (Int, Bool)
//                                                                    would otherwise default public
```

## Rationale

- Native integration with Console.app / Instruments / the unified logging system; zero dependencies.
- Friendly to Swift 6 actor / Sendable.
- Native privacy interpolation; `.private` values are redacted whenever no debugger is attached (see "What `.private` actually means" below).
- No third-party SDK pulled in → no extra entries in `PrivacyInfo.xcprivacy`, consistent with the "no third-party tracking" stance.

### What `.private` actually means (easily misunderstood)

*Practice observed — none of the four official pages in `references/official-docs.md` state the debugger-attached or `OSLogStore` behavior below; this is derived from testing, not documented.*

- `.private` content is **redacted wherever no debugger is attached** — this includes a TestFlight user viewing their own Console.app, not only "in someone else's sysdiagnose after release."
- **When the local Xcode debugger is attached to a running process, private values are still visible.**
- **`OSLogStore` does not bypass redaction**: in a TestFlight or production build, `OSLogStore` reading its own process still sees `<private>` in place of redacted values — only a process that Xcode itself launched gets unredacted output. `.private` is redaction, not encryption; never log raw PII even under `.private`.

## Deviation considerations

- **Cross-platform shared logger interface** (Linux / Android target): use `swift-log` (`apple/swift-log`) as a facade; on Apple platforms, back it with a third-party OSLog handler package (apple/swift-log's own distribution ships no OSLog backend) so the interface stays platform-neutral.
- **Need remote log aggregation**: pair with `telemetry-facade-pattern`'s fan-out sink rather than replacing OSLog directly.
- **A third-party crash reporter requires its own logger**: usually avoidable; if not, keep its use scoped to that SDK.

## Verification checklist

- No `import Logging` / `import CocoaLumberjack` / `import Sentry` or other third-party logging.
- Each module has its own `Logger` extension with a category aligned to the module name.
- Every `.public` annotation can be explained as non-privacy-violating (e.g. non-PII, build hash).
- PII / player IDs / tokens are always `.private` (or not logged at all).

## Related skills

- `telemetry-facade-pattern`: where `OSLogSink` sits within the facade.
- `apple-three-piece-analytics`: OSLog is an Apple-only path, in the same "no third-party" stance as ASC / MetricKit / GC.
- `apple-public-repo-security`: `.private` corresponds to sysdiagnose redaction, but is still visible under a debugger — the safety reasoning for the public repo relies on this semantics.
- `ios-performance-engineering`: `OSSignposter` / `os_signpost` intervals and Instruments profiling; this skill stops at `Logger`.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
