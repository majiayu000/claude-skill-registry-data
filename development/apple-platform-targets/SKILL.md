---
name: apple-platform-targets
description: 'Default minimum deployment target for Apple-platform Swift Apps — iOS 26 / macOS 26 on the Xcode 26 toolchain (Swift 6 language mode) — and how to deviate down (iOS 18 / 17) or up. Use when starting a new Apple-platform project, writing the Package.swift `platforms:` list, deciding whether an API newer than the floor is worth bumping for or a client requirement forces dropping below it, or when asked "what should the minimum iOS / macOS version be". Entry point of the bootstrap chain; does NOT own language mode → swift6-concurrency, or module layout → swiftpm-modularization.'
---

# Apple Platform Deployment Targets

## When to invoke

- Starting a new iOS / macOS App and setting the minimum deployment version.
- Writing the `platforms:` block in `Package.swift`.
- Deciding whether an API newer than the floor (next major) is worth bumping for, or whether a client / user-base requirement forces dropping below the floor.
- User asks about minimum iOS / macOS version or whether to support the previous major version.

## Kickoff order

This skill is the entry point for a new Apple-platform project — decide these defaults in this order, each via its own skill:

1. **Platform** (this skill) — minimum deployment target.
2. `swiftpm-modularization` — package / module shape.
3. `swift6-concurrency` — language mode and concurrency checking.
4. `swift-testing-baseline` — test framework and snapshot strategy.
5. `oslog-logger-defaults`, `telemetry-facade-pattern`, `apple-three-piece-analytics` — logging, telemetry facade, and analytics stack.
6. `mise-tool-management` — CLI tool version manager.
7. `xcode-cloud-single-track-ci` — CI pipeline.

Then, per screen rather than per project: `swiftui-navigation-architecture`, `ios-accessibility-engineering` (invoke deliberately on every new screen — it doesn't auto-trigger on routine SwiftUI work).

## Default decisions

- **iOS 26 / macOS 26** as the default minimum deployment target.
- Toolchain: **Xcode 26.x** (Swift 6.2+ compiler). Language mode is decided in `swift6-concurrency`, not here — Xcode 26 builds Swift 6 mode for any floor, so the floor is a product decision, not a toolchain one.
- Do not auto-bump with each Xcode major — bumping requires an explicit decision recorded in `foundations.md` (`collaboration-skills:spec-phase-orchestration` layout).
- That no-auto-bump rule covers the **deployment floor**, not the toolchain: the toolchain line must move ahead of Apple's App Store Connect SDK minimum (since April 28, 2026: Xcode 26; from April 2027: the 27 SDKs), in one PR that updates the README / `foundations.md` toolchain line and the Xcode Cloud workflow (`xcode-cloud-single-track-ci`). Xcode 27 installs and runs only on Apple silicon Macs with macOS Tahoe 26.6 or later.
- Keep `Package.swift` `platforms: [.iOS(.v26), .macOS(.v26)]` **aligned** with every App target's `IPHONEOS_DEPLOYMENT_TARGET` / `MACOSX_DEPLOYMENT_TARGET`; no skew. `.v26` requires `// swift-tools-version: 6.2` (6.0 / 6.1 report `'v26' is unavailable`).

## Rationale

- iOS 26 / macOS 26 is the first OS pair with Liquid Glass: on a 26 floor the system chrome (toolbars, tab bars, sheets, `.glassEffect()`) is one design language, with no `#available` fork and no legacy-look branch to test.
- The floor no longer buys toolchain features — Xcode 26 compiles Swift 6 mode and the Swift 6.2 concurrency additions for older floors too. What a lower floor costs is a second UI generation to maintain; what it buys is users who haven't updated.
- Solo / small projects have no installed base to protect, and Apple's adoption curve puts the current major on the large majority of active devices within months of release, so the compatibility tax is small.
- Locking out auto-bumps prevents blindly chasing each Xcode major (each new major, e.g. iOS 27 / macOS 27) and cutting off users mid-cycle.

## Deviation considerations

### Drop down to iOS 18 / macOS 15

- **Trigger**: an existing user base still on 18 / 15; a client or reviewer requires N-1 support; TestFlight testers who cannot upgrade.
- **Cost**: every Liquid Glass API (`.glassEffect()`, `GlassEffectContainer`, `.tabBarMinimizeBehavior`) needs `#available(iOS 26, *)` guards, and the pre-26 look of toolbars / tab bars / sheets must be snapshot-tested separately; iOS 26-only Foundation and SwiftData additions are off-limits.
- **How to record**: note "deviating from apple-platform-targets default" in `foundations.md` with the reason and the list of guarded APIs.

### Drop down to iOS 17 / macOS 14 or lower

- **Trigger**: education, enterprise intranet, or low-end markets with a large older-device pool.
- **Cost**: everything above, plus the Swift 6 runtime-dependent features that need an iOS 18 runtime (full SE-0427 noncopyable-generics support) and iOS 18+ SwiftData fixes. Note what a lower floor does *not* cost: `@Observable` has been available since iOS 17.0, and Swift 6 language-mode checking is a compile-time toolchain feature independent of the deployment target.
- **Advice**: record which APIs are off-limits and which behaviours need polyfills.

### Bump up to iOS 27 / macOS 27 (or newer)

- **Trigger**: an API that exists only in the newest major.
- **Conditions**: brand-new App with no user base, or a personal / showcase project willing to cut off the previous major.
- **Cost**: TestFlight testers and App Review devices must be on the newest major; the catalog's other skills are written against the 26 baseline; `.v27` needs `// swift-tools-version: 6.4` (Xcode 27+).
- **How to record**: same `foundations.md` note.

## Verification checklist when locking targets

- `Package.swift` `platforms:` matches every App target's deployment target build setting.
- The Xcode version is recorded in the README / `foundations.md` toolchain line and matches the Xcode Cloud workflow's Xcode setting (`.mise.toml` pins CLI tools, not Xcode — see `mise-tool-management`).

## Related skills

- `swift6-concurrency`: language mode is independent of the deployment floor on Xcode 26; read it next in the kickoff order.
- `xcode-cloud-single-track-ci`: CI Xcode version lock.
- `mise-tool-management`: pins CLI tools, not Xcode itself.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
