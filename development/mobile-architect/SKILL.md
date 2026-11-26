---
name: mobile-architect
always: true
description: Principal Mobile Architect — cross-platform mobile app architecture, Flutter + React Native/Expo, state management, offline-first, CI/CD, testing, security, observability. Synthesizes patterns from 8 production repos (2026). Do not use for mobile game producer tasks — use `mobile-game-producer` instead.
triggers:
  - mobile architect
  - mobile

---
[SKILL] mobile-architect
[OBJ] Architect, bootstrap, and govern production-grade cross-platform mobile apps — Flutter and React Native/Expo — owning architecture, state, persistence, networking, testing, CI/CD, security, and observability across both ecosystems.
[PERSONAS] MOBILE (primary), DEV (primary), ARCH (secondary), UX (secondary), QA (secondary).
[SUB-SKILLS] `flutter-architect` (Flutter full-stack) -> `flutter-design` + `flutter-developer`; `mobile-game-producer` (games). Cross-ref `frontend-frameworks-lord` for RN.

[RULES]
1. [CMD] Context7 IDs: Flutter `/flutter/website`; Dart `/dart-lang/site-www`; Riverpod `/riverpod/riverpod`; BLoC `/felangel/bloc`; Freezed `/rrousselGit/freezed`; Drift `/simolus3/drift`; Dio `/cfug/dio`; go_router `/flutter/packages`; Expo `/expo/expo`; React Native `/facebook/react-native`; TanStack Query `/tanstack/query`; Zustand `/pmndrs/zustand`; Zod `/colinhacks/zod`; Unistyles `/jpudysz/react-native-unistyles`; MMKV `/mrousavy/react-native-mmkv`; Sentry `/getsentry/sentry-react-native`; PostHog `/PostHog/posthog-js`; Maestro `/mobile-dev-inc/maestro`; Patrol `/leanflutter/patrol`; RevenueCat `/RevenueCat/react-native-purchases`.
2. [REQ] `[VER-01]` Pin to lockfile exact versions. Flutter: read `pubspec.lock` -> load `tech-stack/flutter.md` (baseline Flutter 3.47 / Dart 3.13). RN: read `package-lock.json` -> load `tech-stack/expo-sdk-56.md` (baseline Expo SDK 56 / RN 0.86 / React 19.2). NEVER assume version.
3. [REQ] **Framework selection decision tree**:
   - UI pixel-perfection across platforms + single codebase + non-hardware-dependent -> **Flutter** (Impeller, 60/120fps).
   - JS/TS team + fast MVP + easier hiring + web support -> **React Native + Expo** (New Architecture, JSI).
   - iOS-only + Apple Intelligence APIs + highest App Store approval -> **Swift**.
   - Android-only + deep hardware (BLE, camera2, Automotive) -> **Kotlin + Jetpack Compose**.
   - Share logic only (not UI) between iOS+Android -> **Kotlin Multiplatform (KMP)**.
   - Web games/apps wrapped as native -> **Capacitor**.
4. [REQ] **Architecture (both platforms)**: Feature-first Clean Architecture. Layers: presentation -> domain -> data. Domain depends on nothing. Data depends on domain. Presentation depends on domain. No cross-feature imports. No business logic in UI. No backend SDK in domain/presentation (backend isolation).
5. [REQ] **State management**:
   - Flutter: Riverpod 3.x with `@riverpod` code-gen (default) OR BLoC 9.x (enterprise/event-driven). NEVER Provider for new projects. NEVER `setState` for app-wide state.
   - RN: TanStack Query v5 (server state) + Zustand v5 (client state) + React Hook Form + Zod (forms). NEVER React Context for auth.
6. [REQ] **Offline-first**: local DB as source of truth. Flutter: `drift` (SQL) + `hive` (KV). RN: `WatermelonDB` (SQL) + `MMKV` (KV). Sync: revision-based delta sync on reconnect; conflict resolution (LWW / field-level merge / server-wins). Background: `workmanager` (Flutter) / `expo-background-fetch` (RN). Connectivity: `connectivity_plus` (Flutter) / `@react-native-community/netinfo` (RN).
7. [REQ] **Navigation**:
   - Flutter: `go_router` + `go_router_builder` (TypedGoRoute, compile-time safe) + `StatefulShellRoute.indexedStack` (bottom nav state preservation) + **Router Refresh Pattern** (`_RouterRefreshNotifier` + `ref.listen` — redirect without router rebuild) + `PopScope` (predictive back).
   - RN: Expo Router (file-based, typed routes) + `Stack.Protected` (auth guards) + groups `(auth)/` `(main)/` `(tabs)/`.
8. [REQ] **Networking**:
   - Flutter: `dio` (interceptors) + optional `retrofit` (type-safe `@RestApi()`) + `freezed` + `json_serializable`. **Freezed Failure union**: `network/cache/auth/server/permission/unknown`.
   - RN: `axios` (auth interceptors, auto-token, 401 auto-logout) + TanStack Query (caching, retry, optimistic). **Query cache buster**: `user:${userId}` to prevent cross-user leaks.
9. [REQ] **Authentication**:
   - Flutter: Firebase Auth (confined to `data/` layer) + `flutter_secure_storage` + multi-flavor (`main_staging.dart` / `main_production.dart`).
   - RN: Supabase email OTP / custom JWT + `expo-secure-store` (Keychain/Keystore) + **Ordered logout cleanup** (cancelQueries -> posthog.reset -> sentry.setUser(null) -> queryClient.clear -> authStore.reset -> signOut -> router.replace).
10. [REQ] **Design system**:
    - Flutter: `ColorScheme.fromSeed()` + `Theme.of(context)` ONLY + `FlexColorScheme` v8 + `ThemeExtension` for tokens. Material 3 default ON.
    - RN: `react-native-unistyles` v3 (semantic tokens, compiled stylesheets) + `StyleSheet.create((theme) => ({...}))` + responsive helpers `rf()/hs()/vs()`.
    - Both: light/dark/system themes; WCAG AA contrast; tap targets >= 44pt (RN) / 48dp (Flutter); no hardcoded colors/sizes; responsive breakpoints (compact <600, medium 600-840, expanded >840).
11. [REQ] **i18n & RTL**:
    - Flutter: `flutter_localizations` + `intl` + ARB OR **Slang** (compile-time safe). RTL: `EdgeInsetsDirectional` / `AlignmentDirectional`.
    - RN: `react-i18next` + `I18nManager.forceRTL(isArabic)` + ESLint plugin for translation completeness.
    - Both: never hardcode user-facing strings; validation messages use i18n keys; test RTL with `Directionality(textDirection: TextDirection.rtl)` (Flutter) / `I18nManager.forceRTL(true)` (RN).
12. [REQ] **Testing two-tier** `[TEST-07]`:
    - Flutter: FAST `flutter test <file>`; FULL `flutter test --coverage` + `integration_test/` + **Patrol** (native dialogs). Mock: `mocktail`.
    - RN: FAST `jest <pattern>`; FULL `jest --coverage` + **Maestro** (YAML E2E, <1% flake, all platforms). Mock: `jest-expo` + RNTL.
    - Both: AAA pattern; one behavior per test; factories not hardcoded IDs/dates `[TEST-03]`; accessibility-first (`getByRole`/`getByLabelText`); testID convention `{feature}-{element}-{action}`.
13. [REQ] **CI/CD**:
    - Flutter: GitHub Actions (orchestrator) + Codemagic (build farm, macOS M2) + Fastlane (store submission). Pipeline: `dart format` -> `flutter analyze --fatal-infos` -> `flutter test` -> `flutter build appbundle/ipa --obfuscate --split-debug-info` -> sign -> deploy.
    - RN: EAS Workflows (build + submit + OTA update) + GitHub Actions (tests/lint). `eas-cli build --no-wait` (fire-and-forget) + webhooks. Environment-specific scripts.
    - Both: pin action SHAs `[GIT-05]`; OIDC keyless; SBOM + Cosign; auto-increment version for production.
14. [REQ] **Observability**: Sentry (crash + session replay) + PostHog (analytics + feature flags + A/B + session replay). Wire observers into router for screen tracking. Reset identity on logout. Upload debug symbols for symbolication. Monitor crash-free users >= 99.5%.
15. [REQ] **Security** `[SEC-01..10]`: zero-trust input validation; no secrets in code (`--dart-define` / `EXPO_PUBLIC_*`); HTTPS + cert pinning; secure storage for tokens; obfuscate release; Play Integrity / DeviceCheck; no PII in logs.
16. [REQ] **IAP/Monetization**: `in_app_purchase` (Flutter) / `react-native-iap` (RN) + **RevenueCat** (subscription lifecycle, server-side validation, cross-platform entitlements). Balance IAP, rewarded ads, subscriptions, battle passes.
17. [REQ] **AI instruction files**: Every mobile project MUST include `AGENTS.md` (architectural vetos, banned patterns, state rules, backend isolation) + `.cursorrules` (IDE-specific) + `docs/AI-GUIDE.md` (pattern cookbook with file templates). Reference: rn-copilot's AI ecosystem.
18. [REQ] **Component library**: 30+ production-ready UI components with variants API, press animations, full accessibility (ARIA roles), barrel exports. Flutter: extract widgets to classes (not methods). RN: `src/common/components/` with `ComponentName.tsx` + `.types.ts` + `.styles.ts` + `index.ts`.
19. [REQ] Query Context7 for ANY mobile library/framework API before implementation. Test on physical devices (iOS + Android) before declaring done. Run quality gates before done.
20. [REQ] **Cross-platform feature detection**: Flutter `Platform.isIOS`/`kIsWeb`; RN `Platform.OS`. SafeArea for notches. Adaptive widgets (Cupertino/Material). `LayoutBuilder` + breakpoints for responsive.

[PROHIBIT]
- `setState` (Flutter) / React Context (RN) for app-wide/shared state.
- AsyncStorage (RN) for auth tokens — use `expo-secure-store`.
- Backend SDK (Firebase/Supabase) imports outside `data/` layer.
- Hardcoded colors/sizes in widgets — use theme tokens.
- `dynamic` (Flutter) / `any` (RN) in public APIs.
- Business logic / HTTP / DB calls inside `build()` (Flutter) / render (RN).
- Secrets committed to repo / hardcoded API keys.
- `WillPopScope` (deprecated — use `PopScope`).
- `Navigator.push` for complex Flutter apps (use `go_router`).
- Raw `Map` route args (use typed classes).
- `git add .` / `git add -A` `[GIT-06]`.
- Skipping FULL test suite + coverage before done `[TEST-07]`.
