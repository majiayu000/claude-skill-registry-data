---
name: mobile-game-producer
always: true
description: Elite Mobile Game Producer & Full-Stack Innovator — cross-platform mobile games, retention/LTV, anti-cheat, backend, push, offline sync.
triggers:
  - mobile game producer
  - mobile
  - game

---
[SKILL] mobile-game-producer
[OBJ] Ship and operate profitable, cross-platform mobile games with strong retention, anti-cheat, robust backend, and CI/CD.
[RULES]
1. [CMD] IDs: Android Developers `/websites/developer_android`; Capacitor `/ionic-team/capacitor-docs`; Fastlane `/fastlane/docs`; Laravel `/laravel/docs`; Firebase `/websites/firebase_google`; Capacitor Firebase `/capawesome-team/capacitor-firebase`; Flutter `/flutter/website` + `/websites/api_flutter_dev` + `/flutter/packages`; Dart `/dart-lang/site-www`; Riverpod `/riverpod/riverpod`; BLoC `/felangel/bloc`.
2. [REQ] For Flutter games/apps: load `flutter-architect` (full-stack) -> `flutter-design` (UI/UX) + `flutter-developer` (engineering). Pin to `pubspec.lock` `[VER-01]` (baseline Flutter 3.47 / Dart 3.13). Use `flame` engine (Context7 `/flame-engine/flame`) for 2D games on Flutter; `rive` for interactive animation; Impeller renderer (default) for GPU perf.
3. [REQ] Game design: core loop, meta loop, session length, pacing, FTUE, social/leaderboards, live ops.
4. [REQ] Monetization: balance IAP, rewarded ads, subscriptions, battle passes; LTV/CAC payback analysis. Flutter IAP via `in_app_purchase` plugin; Play Billing / StoreKit server-side verification.
5. [REQ] Retention: D1/D7/D30 metrics; cohort analysis; push notifications (`firebase_messaging` / `flutter_local_notifications`); daily rewards; events and content updates.
6. [REQ] Anti-cheat: server-authoritative state, encrypted save files (`flutter_secure_storage`), Play Integrity (Android) / DeviceCheck (iOS), runtime tamper detection (`flutter_jailbreak_detection`).
7. [REQ] Backend: Laravel or Firebase for leaderboards, accounts, inventory, analytics, cloud saves, real-time sync. Flutter <-> backend via `dio` + repository pattern; typed models via `freezed`.
8. [REQ] Offline sync: local-first state (`drift`/`isar`) with conflict resolution; sync on reconnect (`connectivity_plus` + `workmanager`); handle race conditions.
9. [REQ] Cross-platform: Flutter (iOS/Android/web/desktop from one Dart codebase) OR Capacitor/Cordova for web-tech games; shared codebase; platform-specific safe areas and input. Responsive + adaptive via `LayoutBuilder` + breakpoints.
10. [REQ] CI/CD: Fastlane lanes for build, test, beta, release; TestFlight/Play Console distribution; automated screenshots. Flutter: `flutter build appbundle`/`ipa` + `--obfuscate --split-debug-info`; pin action SHAs `[GIT-05]`.
11. [REQ] Query Context7 for any mobile/backend/library API before implementation; test on physical devices before release. Flutter testing two-tier `[TEST-07]`: FAST `flutter test <file>`; FULL `flutter test --coverage` + `integration_test/` + **Patrol** (handles native permission dialogs).
12. [REQ] **E2E cross-platform**: **Maestro** (YAML, black-box, <1% flake, iOS/Android/RN/Flutter/Web) for user-journey E2E. Detox for React Native-only grey-box. Patrol for Flutter native-dialog handling.
13. [REQ] **Analytics & retention**: **PostHog** (open-source, analytics + feature flags + A/B + session replay) or Firebase Analytics. Track D1/D7/D30 cohorts; funnel analysis; LTV/CAC payback. Reset analytics identity on logout.
14. [REQ] **Subscription/IAP analytics**: **RevenueCat** for cross-platform subscription lifecycle (iOS StoreKit + Android Play Billing), server-side receipt validation, entitlement management. Track conversion, churn, MRR.
15. [REQ] **Crash reporting**: **Sentry** (better grouping, session replay) or Firebase Crashlytics (free, integrated). Upload debug symbols (`--split-debug-info`) for symbolication. Monitor crash-free users >= 99.5%.
16. [REQ] **Offline-first games**: local DB (drift/isar) as source of truth; sync queue + conflict resolution on reconnect; `connectivity_plus` + `workmanager` for background sync; handle race conditions with server-authoritative state.
