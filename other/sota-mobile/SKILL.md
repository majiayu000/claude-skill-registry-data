---
name: sota-mobile
description: >-
  State-of-the-art mobile engineering for building and auditing iOS and Android applications. Use when the task involves mobile apps in any form — native (Swift, SwiftUI, Kotlin, Jetpack Compose), cross-platform (React Native, Flutter, Kotlin Multiplatform), Swift as a language — Swift 6 strict concurrency, actors, Sendable, ARC, SwiftPM, Swift Testing — in any target including server-side Swift (e.g. Vapor), app store submission and review (App Store, Google Play, privacy manifests, data safety), push notifications (APNs, FCM), offline-first architecture and sync, mobile security (Keychain, Keystore, certificate pinning, app attestation, OWASP MASVS), mobile performance (startup, jank, battery, app size), or mobile release operations (phased rollouts, feature flags, forced updates, crash reporting, OTA updates). Trigger keywords: mobile, iOS, Android, Swift, SwiftUI, Kotlin, Jetpack Compose, React Native, Flutter, app store, push notifications, offline-first, server-side Swift, Vapor, SwiftPM.
---

# SOTA Mobile Engineering

Expert-level rules for building new mobile apps and auditing existing ones. Mobile is unlike web or backend in three load-bearing ways, and every rule in this skill flows from them:

1. **You cannot roll back a shipped binary.** Users update on their own schedule; some never do. Every release is permanent for some cohort. Design for kill switches, forced updates, and servers that tolerate ancient clients.
2. **The device is hostile territory.** The attacker owns the hardware, can decompile the binary, and can read anything you store insecurely. Client-side checks are deterrents, not controls; enforcement lives on the server.
3. **Resources are budgeted, not abundant.** Main thread, battery, memory, radio, and background execution time are all rationed by the OS. Apps that overspend get janked, killed, or throttled.

Facts in this skill (OS versions, store policies, framework status) were verified against primary sources in June 2026. Mobile platforms move fast — when a specific deadline or version matters, re-verify against Apple/Google developer docs before relying on it.

## BUILD mode

When creating or extending a mobile app:

1. **Settle the platform decision first.** Stack choice (native vs cross-platform), minimum OS floor, and target SDK are one-way doors. Use `rules/01` decision factors; record the decision and its rationale in the repo.
2. **Establish architecture before features.** Unidirectional data flow, DI seams, module boundaries, and navigation pattern from day one (`rules/02`). Retrofitting UDF onto a ball of mutable state is a rewrite.
3. **Decide the offline posture explicitly.** "Online-only with graceful errors" is a valid choice; "accidentally breaks offline" is not. If offline-first: local DB is the source of truth, mutations queue, sync is a background concern (`rules/03`).
4. **Wire operational survival kit before v1.0 ships:** crash reporting with symbol upload, forced-update mechanism, remote kill switches for risky features, API version header on every request (`rules/06`). These cannot be added retroactively for already-shipped binaries.
5. **Security defaults from the start:** secrets in Keychain/Keystore only, TLS everywhere, deep links validated, WebView locked down (`rules/04`).
6. **Budget performance up front:** cold start, frame time, and app size budgets in CI, not as a post-launch rescue (`rules/05`).
7. **Comply with current store requirements** before first submission: privacy manifest + required-reason APIs (iOS), Data safety form + target API level + 16 KB page support + developer verification (Android) (`rules/01`, `rules/06`).

## AUDIT mode

When auditing an existing mobile app, work through the rules files in order and report findings using this convention.

### Severity levels

- **CRITICAL** — Exploitable security flaw or guaranteed user-facing breakage: secrets in SharedPreferences/UserDefaults/NSUserDefaults, tokens in deep-link URLs, unvalidated deep links reaching auth-sensitive screens, `javaScriptEnabled` WebView loading untrusted content with a JS bridge, no forced-update mechanism plus a known-bad shipped version, biometric auth gating a boolean instead of a key.
- **HIGH** — Likely production incident or store rejection: missing crash reporting/symbolication, blocking main thread on I/O, no kill switch for a server-dependent feature, store policy violations (missing privacy manifest entries, stale target API), unbounded silent-push reliance, sync without conflict resolution.
- **MEDIUM** — Degrades quality or future velocity: no DI seams (untestable), monolithic module (slow builds), missing list virtualization, no startup budget, permission prompts fired at launch, no staged rollout process.
- **LOW** — Hygiene: missing snapshot tests, inconsistent navigation patterns, unbatched analytics, image caching misconfiguration.

### Finding format

```
[SEVERITY] <rule-file>#<rule> — <one-line title>
Location: <file:line or module>
Evidence: <the offending code/config, quoted>
Impact: <what breaks, who exploits it, or what it costs>
Fix: <concrete change, with code where non-obvious>
```

Order the report by severity, then by blast radius. An audit that returns only style nits has failed — check the CRITICAL list above explicitly and state "verified absent" for each.

## Rules index

| File | Covers |
|---|---|
| [rules/01-platform-and-stack.md](rules/01-platform-and-stack.md) | Native vs cross-platform decision, React Native new architecture, Flutter, KMP/CMP status, when web/PWA suffices, minimum OS floors, target SDK policy, current platform baselines |
| [rules/02-architecture-and-state.md](rules/02-architecture-and-state.md) | Unidirectional data flow (MVVM/MVI/TCA), state modeling, dependency injection, modularization for build times, navigation patterns |
| [rules/03-offline-background-push.md](rules/03-offline-background-push.md) | Offline-first design, local DB as source of truth, sync engines, conflict resolution, mutation queues, optimistic UI, iOS background modes, WorkManager/Doze, APNs/FCM, token lifecycle, permission timing UX |
| [rules/04-security.md](rules/04-security.md) | Keychain/Keystore, certificate pinning tradeoffs and trust anchors, biometrics gating keys, App Attest/Play Integrity (device and app verdicts), token handling, deep link validation, root/jailbreak detection honesty, WebView hardening, obfuscation reality and non-debuggable releases, app-private vs shared storage and file protection classes, integrity of locally stored data, clipboard leakage and UI masking, overlays/task hijacking, intents/broadcasts, ContentProvider/FileProvider exposure, biometric fallback and lock-screen checks, pinning mechanics and audit stance, anti-dynamic-analysis checks, native-library hardening, keyboards/extensions/App Intents/widgets, device identifiers, OWASP MASVS |
| [rules/05-performance.md](rules/05-performance.md) | Startup budgets, main-thread discipline, jank/frame budgets, list virtualization, image loading, memory pressure, battery, app size, ANR avoidance, MetricKit/Android vitals |
| [rules/06-release-and-operations.md](rules/06-release-and-operations.md) | Store submission requirements, phased rollouts, feature flags/kill switches, forced updates, crash reporting, OTA updates policy, API versioning for old clients, testing strategy |
| [rules/07-swift-language.md](rules/07-swift-language.md) | Swift as a language (any target, incl. server-side Swift): Swift 6 strict concurrency (actors, Sendable, isolation), value semantics/COW, protocol-oriented design, optionals/typed throws, ARC and retain cycles, unsafe pointer/C interop, SwiftPM supply chain (Package.resolved, registry signing, binary checksums), Swift Testing vs XCTest |

## Top 10 non-negotiables

1. **Secrets live in Keychain (iOS) or Keystore-backed encrypted storage (Android) — never in UserDefaults, SharedPreferences, plist files, or hardcoded in the binary.** The binary is public; assume it is decompiled the day you ship.
2. **The server enforces; the client suggests.** Any authorization, entitlement, price, or integrity decision made only client-side is a finding. Root detection, pinning, and obfuscation are deterrents that raise cost — never the control.
3. **Never block the main thread on I/O, parsing, or crypto.** Main thread is for UI. Violations are jank on iOS and ANRs (and Play Store visibility penalties) on Android.
4. **Ship a forced-update mechanism in v1.0.** A version-check endpoint plus a blocking upgrade screen. The release where you discover you need it is the release you cannot fix.
5. **Every risky or server-dependent feature ships behind a remotely controllable kill switch.** You cannot roll back a binary; you can flip a flag.
6. **The API must tolerate every app version still in the wild.** Version every client request; never remove or repurpose fields a shipped binary reads; test the oldest supported client in CI against new server releases.
7. **Offline is a designed state, not an error state.** Local database as source of truth, queued mutations with idempotency keys, explicit conflict resolution. If you choose online-only, fail with designed UX, not spinners.
8. **Biometric auth must gate a cryptographic key, not a boolean.** `if (authenticated) { unlock() }` is patchable with one Frida hook; a key released by the secure enclave/StrongBox is not.
9. **Crash reporting with symbol upload (dSYM/mapping) wired into CI before first release**, with crash-free-session rate monitored per release and gates on staged rollout promotion.
10. **Meet current store requirements proactively:** iOS — privacy manifests and required-reason API declarations (mandatory since May 2024), built with the latest required SDK (iOS 26 SDK as of April 28, 2026); Android — target API 36 by Aug 31, 2026, Data safety form accuracy, 16 KB page-size support (required for apps targeting Android 15+; Play blocks updates without it from Feb 1, 2027).
