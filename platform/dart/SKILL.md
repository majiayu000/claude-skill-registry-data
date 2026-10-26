---
name: dart
description: Use when building Dart and Flutter apps — a single-screen phone dashboard, API clients generated from OpenAPI, state management, widget and unit tests, and building an Android APK to install on a real device. Also use when the app works in the emulator but not on a phone, or when generated client code drifts from the server.
---

# Dart and Flutter

Default: stable Flutter channel, Dart with sound null safety, `flutter_lints`, a generated API client from the server's OpenAPI document, `flutter test`, release APK for Android.

## Setup

1. `flutter create --platforms=android,web app`; run `flutter doctor` until the Android toolchain is green.
2. Turn on `analysis_options.yaml` with `flutter_lints` and keep `flutter analyze` at zero issues.
3. Keep server URLs in build-time defines (`--dart-define=API_BASE=...`), not in source.

## API clients from OpenAPI

- Generate the client with `openapi-generator` (dart-dio or dart) from the server's published spec, into a separate package.
- Regenerate whenever the spec changes and commit the generated code with the spec version in the commit message; compile errors then point to every affected call.
- Wrap the generated client in a small repository class so widgets do not depend on generated types directly.

## UI for at-a-glance use

- A one-screen dashboard (what to do today, what expires soon) beats a menu of screens for daily use. Sort by urgency and show dates as relative ("tomorrow", "in 3 days").
- Pull-to-refresh plus refresh on resume (`AppLifecycleState.resumed`) keeps data current without polling.
- Show stale data with a "last updated" time instead of a blank screen when offline.

## State

- Start with `StatefulWidget` + `ValueNotifier`/`ChangeNotifier`; adopt Riverpod or Bloc when several screens share async state.
- Keep business rules (dates, sorting) in plain Dart classes with unit tests.

## Building for a phone

```bash
flutter build apk --release
adb install -r build/app/outputs/flutter-apk/app-release.apk
```

- Release builds need a signing configuration; keep the keystore and its password outside the repository.
- Android blocks clear-text HTTP by default; use HTTPS, or allow a specific development host in the network security config.

## Verification loop

1. `flutter analyze` — zero issues.
2. `flutter test` — unit and widget tests (use `pumpAndSettle` carefully; it waits forever on infinite animations).
3. Install the release APK on a real device and check one full flow.

## Pitfalls

- **Emulator localhost:** inside the Android emulator, `localhost` is the emulator itself; the host machine is reached through the special alias address documented in the emulator networking guide. A real phone needs the machine's LAN address or a public endpoint.
- **`BuildContext` across async gaps:** check `mounted` before using context after `await`.
- **Time zones and dates:** `DateTime.now()` is local; parse server timestamps with offsets and compare dates, not instants, for "today" logic.
- **Generated code in reviews:** keep it in its own directory so diffs of hand-written code stay readable.
- **Dependency upgrades** often require bumping the Gradle and Kotlin versions in `android/`; upgrade them together.
