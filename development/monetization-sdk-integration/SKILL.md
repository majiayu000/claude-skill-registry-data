---
name: monetization-sdk-integration
description: 'Use when adding, upgrading, or auditing a third-party monetization SDK (AdMob / Google Mobile Ads incl. UMP consent; the same contract applies to any other ad or subscription SDK), or when a PR adds `import GoogleMobileAds` outside the single live-bridge file, breaks `canImport` / `.when(platforms: [.iOS])` gating, or lands without a Fake bridge. Owns the break-glass admission test, single-import-site isolation contract, and test seam. Does not cover native StoreKit 2 IAP (storekit2-iap-defaults), production ID storage (build-time-secret-injection), or App Review consequences (app-store-review-rejections).'
---

# Monetization SDK Integration

## When to invoke

- Adding a new monetization SDK (AdMob, ATT, UMP, AdMob mediation networks, RevenueCat, etc.)
- Upgrading existing AdMob / UMP versions (e.g. v11 → v13)
- Auditing PR diff that touches the monetization target's ad-bridge sources (e.g. `Sources/<AdsBridge>/`)
- Cross-platform SDK questions (iOS only? macOS catalyst? watchOS?)
- Anyone proposing "let's just `import GoogleMobileAds` over here too" — IMMEDIATE invoke

Skip when: changing pure values / protocols inside the monetization core target (no third-party touch).

## The contract

Default rule: **no third-party SDKs** in the app. Apple-platform native APIs preferred (OSLog over Sentry, MetricKit over Firebase Crashlytics, GameKit over Steam-style backend, etc.).

**Break-glass exception** is granted when ALL of:
1. The capability genuinely requires the SDK (no Apple-native alternative); e.g. AdMob banner serving has no Apple-platform equivalent
2. The SDK is shippable under the project's privacy regime (PrivacyInfo.xcprivacy supports its tracking domains)
3. The SDK's import is isolated to a SINGLE source file behind a protocol seam (see §isolation contract below)
4. The dep arrow is one-way (consumer → SDK; the SDK does not call back into the host app's code beyond delegate/callback bridges)
5. iOS-only conditional compile gating (`canImport`) — macOS / Catalyst paths must build without the SDK

If any of (1)-(5) fails: deny. Reject the SDK proposal; suggest Apple-native fallback or sit it out.

## The isolation contract

For every accepted SDK:

### File-layout invariant
- Protocol file `<SdkName>Bridge.swift` defines the seam. Plain Swift; no SDK import.
- Live impl file `Live<SdkName>Bridge.swift` is the ONLY file allowed to `import <SDKModule>`.
- All other code uses `any <SdkName>Bridge` for DI. Test seam: `Fake<SdkName>Bridge` in the matching test target (e.g. `Tests/<AdsBridge>Tests/FakeAdMobBridge.swift`).

Example for AdMob (currently shipped):
- `Sources/<AdsBridge>/AdMobBridge.swift` — protocol (the monetization target's bridge protocol file)
- `Sources/<AdsBridge>/LiveAdMobBridge.swift` — sole `import GoogleMobileAds` site
- `Tests/<AdsBridge>Tests/FakeAdMobBridge.swift` — test seam

### Cross-boundary type invariant

When the live bridge's output crosses into UI or other host code, it must cross as a platform-neutral type (e.g. SwiftUI's `AnyView`), never a raw SDK type — that's what keeps UI targets at zero SDK imports even though they display SDK-provided content. Example: `BannerViewProviding.bannerView(for:) -> AnyView?` returns `AnyView`, not a `GoogleMobileAds` type.

### Build-time audit (run before every monetization PR merge)

Canonical regex (matches Swift 6 access-level imports too):
```bash
# replace <SDKModule> / <project-sources-root> with the project's actual values
rg '^(internal |private |public |@_implementationOnly |@preconcurrency )*import <SDKModule>' <project-sources-root>
```

Expected count: **1** (live bridge file).

If > 1: the contract is broken. Either consolidate behind the existing bridge OR file an exception in the project's architecture-decisions doc (`docs/foundations.md` for consumers of `collaboration-skills:spec-phase-orchestration`) documenting WHY a second import site is necessary (with prior reviewer sign-off) — see Documentation pointers below.

### Conditional compile invariant

iOS-only SDKs (AdMob/UMP/most monetization stack):
```swift
#if canImport(GoogleMobileAds)
import GoogleMobileAds
// ... live impl code
#else
// macOS / catalyst fallback — usually NoOp returning sensible empty values
#endif
```

The Package.swift dep arrow itself must also gate the SDK to iOS:
```swift
.product(
    name: "GoogleMobileAds",
    package: "swift-package-manager-google-mobile-ads",
    condition: .when(platforms: [.iOS])
),
```

Without `condition:`, macOS build fails on `swift build` because Google ships iOS-only xcframeworks.

### Test seam invariant

A test target for the bridge ships `Fake<SdkName>Bridge` (actor or class). All unit tests inject the fake; real SDK only loaded at runtime via DI in the app's composition root. A shared testing-scaffolding target may ship shared fakes used across both ad and IAP test targets (e.g. `FakeAdProvider`, `FakeIAPClient`); the per-SDK bridge fakes live in their own test target.

`Fake` must:
- Be `Sendable` (Swift 6 actor or @unchecked Sendable + lock-guarded)
- Have a `script(...)` or per-call setter API for deterministic test outcomes
- Not import the real SDK (zero hidden dependency)

## Real-world incidents this skill encodes

### Production ID swap safety
- A Release build's `bannerAdUnitID` constant first used `fatalError("REPLACE_BEFORE_RELEASE: …")` as a transitional guard; it has since been replaced by xcconfig injection (→ `build-time-secret-injection`), which is the standing solution — the `fatalError` form is not a long-term answer on its own
- A paired-flip checklist ensures Info.plist `GADApplicationIdentifier` + bridge constant are always updated together

### Real banner landed + SDK-view-crossing seam
- The `BannerView` SwiftUI host shipped, crossing into the UI layer per the cross-boundary type invariant above. One shared `BannerSlotView` replaced per-app placeholder slots.
- ID split: `#if DEBUG` forces Google's universal test unit; Release reads the per-app prod id from `Bundle.main` via xcconfig.

### macOS conditional gating
- Initial AdMob integration left `import GoogleMobileAds` ungated → macOS build broke
- Fix: `canImport(GoogleMobileAds)` + Package.swift `condition: .when(platforms: [.iOS])` + macOS fallback uses `NoopAdProvider`

### lefthook parallel invocations — secondary effect
- Multiple SDK installs can trigger concurrent `mise exec` invocations
- Keep `lefthook.yml pre-commit.parallel: true` (matches `apple-public-repo-security`'s baseline); if a specific pair of commands genuinely races, serialize those two, not the whole file

## Anti-patterns

- **"Just import it where you need it"** — NO. Single-file isolation is the contract; multiple imports = no audit signal, no clean removal path.
- **"Skip the Fake for now, we'll add it later"** — NO. Unit tests must work from day one; integrating SDK without a test seam means every test becomes integration-test territory.
- **"Macros + canImport are too verbose; let's drop conditional gating for v2"** — NO. macOS build will break the moment a maintainer runs `swift build` on a Mac, blocking PRs.
- **"Production IDs in source for ease of swap"** — NO. Use build-config injection (`build-time-secret-injection`); a `fatalError` guard is acceptable only as a transitional step before that lands.
- **"PrivacyInfo.xcprivacy can wait until submission"** — NO. Upload-time checks only catch (a) undeclared required-reason API use, (b) a listed third-party SDK missing its manifest/signature — GoogleMobileAds and UserMessagingPlatform are not on that list — and (c) an invalid manifest (ITMS-91056), including `NSPrivacyTracking` / `NSPrivacyTrackingDomains` inconsistency (`true` with an empty domain list, `false` with domains listed); nothing checks the declaration against the app's actual network behavior. The real cost lands later: while the user hasn't granted ATT permission, requests to the domains *listed* in `NSPrivacyTrackingDomains` fail, so the list must be exact — don't pad it for safety; an omitted domain costs a privacy-label mismatch and a 5.1.x rejection, not a runtime failure. Update PrivacyInfo BEFORE adding the SDK.
- **Assuming a Swift symbol name survives a major SDK upgrade unchanged** — NO. AdMob dropped the `GAD` prefix from its Swift API at v12.0.0 (`GADBannerView` → `BannerView`, `GADRequest` → `Request`, etc.; the `GAD`-prefixed spellings remain only in the Objective-C API). Check the SDK's migration guide before a major-version bump instead of assuming old names still resolve, and re-run the isolation audit (Build-time audit above) after — a migration can silently widen the import-site count past 1.

## Pre-integration checklist

When proposing a new SDK, fill this in:

```
SDK: <name + version + GitHub URL>
Capability: <what it does that Apple-native can't>
Privacy domains: <list — must match PrivacyInfo.xcprivacy>
iOS-only / cross-platform: <iOS-only | iOS+macOS | etc.>
Bundle size impact: <KB / MB>
Tracking ATT required: <yes/no>
UMP consent required: <yes/no>
Test seam plan: <how Fake<SdkName>Bridge will look>
Isolation audit grep target count: <expected 1>
Fallback platform behaviour: <Noop / throw / etc.>
```

If any field is "TBD" or "?", do NOT proceed — research first.

## Documentation pointers

- The project's architecture-decisions doc (`docs/foundations.md` for consumers of `collaboration-skills:spec-phase-orchestration`) — the no-3rd-party rule + break-glass exception + isolation contract text
- The project's design doc — monetization design intent
- The project's plan / readiness doc — AdMob impl phase, isolation acceptance criteria, pre-submission audit step
- `Sources/<AdsBridge>/<SdkName>Bridge.swift` — protocol seam example
- `Sources/<AdsBridge>/Live<SdkName>Bridge.swift` — single-import-site example
- `<App>/Resources/PrivacyInfo.xcprivacy` — tracking domains declaration

## Related skills

- `build-time-secret-injection` — SIBLING; invoke together when wiring AdMob — that skill is the secret-handling layer (xcconfig injection), this skill is the SDK isolation and testing contract.
- `storekit2-iap-defaults` — same bridge-isolation pattern for the IAP side; `app-store-review-rejections` — ATT / PrivacyInfo consequences of shipping AdMob (5.1.2).
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
