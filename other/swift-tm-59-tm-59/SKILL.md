---
name: swift
description: Use when writing Swift outside Xcode apps — Swift Package Manager command-line tools with swift-argument-parser, date and expiry calculations with Foundation, XCTest or Swift Testing, and building on Linux or in Docker. Also use when Foundation behaves differently on Linux than on macOS, or when date arithmetic is off by a day.
---

# Swift (packages and command-line tools)

Default: current Swift toolchain, Swift Package Manager, `swift-argument-parser`, Swift Testing or XCTest, builds verified on Linux (official `swift` Docker image) as well as macOS.

## Setup

1. `swift package init --type executable --name tool`; split into a library target (`ToolCore`) and an executable target so logic is testable.
2. Add `swift-argument-parser` as a dependency and mark the entry type `@main struct Tool: ParsableCommand`.
3. Commit `Package.resolved` for executables.

## Dates and expiry logic

For "best before" estimates and "eat this first" ordering:

- Work in calendar days with `Calendar` and `DateComponents`, not by adding `86400` seconds — daylight-saving changes and time zones break second arithmetic.
- Pin the calendar and time zone explicitly (`Calendar(identifier: .gregorian)`, a fixed `TimeZone`) in both code and tests.
- Store rules as data (category → default shelf life, opened vs unopened) and keep the estimation a pure function.
- Sort by days remaining, then by a waste-cost estimate, and print why an item is first.

## Command-line ergonomics

- Use `@Option`, `@Flag` and `@Argument` with help text; `validate()` for cross-field checks.
- Output human-readable tables by default and `--json` for scripts (`JSONEncoder` with `.sortedKeys` for stable output).

## Testing

- Put fixed "today" dates in tests; never call `Date()` inside logic — inject it.
- Test month ends, leap days and time zone boundaries.

## Verification loop

1. `swift build -c release` with no warnings.
2. `swift test`.
3. `docker run --rm -v "$PWD":/w -w /w swift:latest swift test` (pin a specific tag) to prove it builds on Linux.

## Pitfalls

- **Foundation on Linux** (swift-corelibs-foundation) lags macOS in some APIs and formatting details; avoid relying on exact `DateFormatter` output across platforms — use ISO 8601 formatting.
- **`DateFormatter` without `locale = Locale(identifier: "en_US_POSIX")`** parses fixed-format strings differently depending on user settings.
- **Value vs reference semantics:** structs copy on assignment; classes share. Mutating a struct inside a collection needs index access, not a loop variable.
- **Force unwraps (`!`)** in CLI code turn bad input into crashes; use `guard let` with a clear error.
- **Concurrency checking** in newer language modes flags non-`Sendable` types crossing tasks; keep CLI code synchronous unless it truly needs concurrency.
