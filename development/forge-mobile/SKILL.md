---
name: forge-mobile
description: "Forge: mobile apps — React Native/Expo/Flutter: mobile app, iOS, Android, Expo, EAS, Flutter, apk, ipa, secure storage, deep link, App Store, Play Store."
---

# Forge playbook — Mobile app (React Native / Expo / Flutter)

The `mobile-dev` specialist leads the native work under `build-boss`. Native UX/touch/layout defers to `ui-boss`; any backend/API the app calls defers to `forge-integration`; if it handles money defer to `forge-payments`. The core honesty rule for mobile: a Metro/dev bundler running is **not** a shipped app — the release binary must actually build and launch on a real device or emulator, and you must say so with evidence.

## Hard rules (non-negotiable)
- **A native build that actually installs.** The app compiles to the real artifact (Android `.apk`/`.aab`, iOS `.ipa`, or an Expo dev/prod build) and **installs + launches** on a device or emulator/simulator — verified, not assumed. "It runs in Expo Go / Metro" is not proof a standalone build works.
- **No secrets in the client bundle.** A mobile bundle is trivially extractable (decompile the APK, read the JS bundle). Real secrets (API signing keys, private tokens) stay **server-side behind an API**; only genuinely public keys ship. Nothing sensitive committed or baked into the binary.
- **Secure token storage.** Auth tokens / credentials live in the OS secure store — `expo-secure-store`, `react-native-keychain` (iOS Keychain / Android Keystore), or Flutter `flutter_secure_storage` — **never** `AsyncStorage` / `SharedPreferences` / plain files.
- **Least-privilege permissions with rationale.** Request only permissions the app actually uses; iOS requires a real usage-description string per permission (`NSCameraUsageDescription`, etc.) or App Store rejection; Android manifest kept minimal.
- **Offline-where-promised actually works.** If offline use is promised, cached reads, queued writes, and a clear "no connection" state exist — not network calls that silently fail.
- **No test/demo/mock data, no debug menus, no `__DEV__`-only shortcuts in the release build.** Release signing configured (Android release keystore, iOS distribution), version/build numbers set, app icon + splash present.

## Team (conditional by stack/level)
Lead: `build-boss`. Native work: **`mobile-dev`** (RN/Expo/Flutter). Support: `ui-boss` (touch targets, safe-area/notch, keyboard, orientation, dark mode), `test-boss` (device/emulator QA — Detox or Maestro for RN, `flutter test` + integration_test for Flutter), `security-boss` (secure storage + secrets audit), `typescript-reviewer` and/or `react-reviewer` for RN code (RN is React-based). Backend calls: `forge-integration` team.

## Skills / commands / MCP
RN / Expo / Flutter docs via Context7 (exact API + version behaviour). For React Native use `/react-build` + `/react-review`; for Flutter use `/flutter-build` + `/flutter-review` + `/flutter-test`. `systematic-debugging` for native/build/native-dependency failures. Popup/settings screens that are essentially web content can borrow `forge-website` conventions (real content, a11y). **Opt-in / environment-gated deps (be honest):** a real **iOS** build needs **macOS + Xcode** — not available on this owner's Windows host; use **Expo EAS Build** (cloud, requires an Expo account) or an Android target instead, and label an iOS build **not-run** if no Mac/EAS is available. **Android** builds need the Android SDK + an emulator or device. Forge writes the code + config regardless; it cannot conjure a toolchain that isn't installed.

## Fan-out & flow
L2 a single-screen or small app; L3 multi-screen + navigation + offline + native modules + a store build; L4 phased for a large app with several native integrations.
**Serial:** app architecture (navigation + state + data layer) → screens → secure-storage + offline layer → device/emulator QA → release build → store-readiness pass.
**Parallel:** independent screens/features build in parallel **once** the navigation contract and data layer are fixed (that contract is the integration seam — you are the integration layer).

## Domain gates
- Release binary **builds and installs + launches** on a device or emulator (evidence: build output + a launch screenshot/log), not just Metro/Expo Go.
- No secrets in the JS bundle or committed; tokens in secure store (Keychain/Keystore/SecureStore), not AsyncStorage/SharedPreferences.
- Permissions minimal and justified — iOS usage-description strings present, Android manifest minimal.
- Offline paths work where promised (cached reads, queued writes, no-connection UI) — or offline is honestly declared out of scope.
- Safe-area/notch, keyboard avoidance, orientation, and dark mode (if supported) handled; touch targets adequate (~44pt); long lists use `FlatList`/virtualization, not a giant `ScrollView`.
- No test/demo/mock data, no debug menu, no `__DEV__` shortcut in the release build; release signing configured; app icon + splash + version set.

## Ship-readiness (unique)
Release build produced and **installed + launched** on a real device or emulator (real output attached); secrets confirmed out of the bundle; secure token storage proven; permissions minimal with real rationale strings; offline behaviour verified where promised; icon/splash/version set; no mock data or debug menus in the release artifact. iOS is macOS/Xcode-gated — if no Mac/EAS was available, mark the iOS build **not-run** honestly rather than implying it shipped. Store-listing assets (screenshots, privacy disclosure, data-safety form) are noted as **owner action**. Advisory checklist; optionally run `security-boss` / `codex-reviewer` on the secret + secure-storage paths — recommended, not a blocker.
