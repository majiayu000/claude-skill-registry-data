---
name: flutter
description: Flutter/Dart rules, patterns, and checklists. Load when Flutter is detected.
---

## Detection Signals

Load this skill when **any** of the following are found:

| Signal | File / Location |
|--------|----------------|
| Flutter SDK in pubspec | `pubspec.yaml` → `sdk: flutter` |
| Main entry point | `lib/main.dart` |
| Flutter workspace | `flutter` key in `pubspec.yaml` |
| Platform directories | `android/` + `ios/` + `lib/` together |

---

## Project Structure

```
lib/
├── main.dart              # App entry, environment setup, runApp()
├── app/                   # MaterialApp/CupertinoApp, router, theme
├── features/              # Feature-first: each feature owns its own layers
│   └── auth/
│       ├── data/          # Repositories, data sources, DTOs
│       ├── domain/        # Entities, use cases, repository interfaces
│       └── presentation/  # Widgets, pages, state (BLoC/Riverpod/etc.)
├── core/                  # Shared: DI setup, network client, error handling
├── shared/                # Reusable widgets and utilities
└── l10n/                  # Localization ARB files
```

- Feature-first structure is strongly preferred over layer-first for apps with > 3 features
- `lib/` contains only Dart — never put platform-specific Swift/Kotlin in `lib/`
- Platform code goes in `android/`, `ios/`, `linux/`, `macos/`, `web/`, `windows/` respectively

---

## State Management

→ Load `skills/mobile/flutter/references/state-management.md` when choosing or implementing state management (BLoC, Cubit, Riverpod, Provider, GetX).

---

## Dart Best Practices

### Null Safety
- All new code must be null-safe — never use `!` (null assertion) without a preceding null check or a comment explaining why it is guaranteed non-null
- Prefer `??` and `?.` over null assertions
- Use `late` only for variables that are genuinely initialized before first use (e.g., in `initState`) — not as a way to defer null handling

### Async / Await
- Always `await` Futures — never fire-and-forget unless intentional (document with a comment)
- Use `Future.wait()` for parallel async operations, not sequential `await`
- Wrap top-level async errors: `FlutterError.onError` + `PlatformDispatcher.instance.onError`

### Isolates (Heavy Computation)
Use `compute()` or `Isolate.run()` for operations that block the UI thread > 16 ms:

```dart
// Decode large JSON on a background isolate
final parsed = await compute(parseHeavyJson, rawJsonString);
```

- JSON decoding of large payloads, image processing, and cryptography must run on isolates
- Do not share mutable state between isolates — pass data by message (serializable types only)

### Code Style
- Follow [Effective Dart](https://dart.dev/guides/language/effective-dart) naming conventions: `lowerCamelCase` for variables/functions, `UpperCamelCase` for types, `SCREAMING_SNAKE_CASE` for constants
- Enable and comply with `flutter_lints` (or `very_good_analysis` for stricter projects)
- Max line length: 80 characters (enforced by formatter — run `dart format .` before committing)
- Never suppress lints with `// ignore:` without a comment explaining the reason

---

## Widget Best Practices

→ Load `skills/mobile/flutter/references/widgets.md` when working with widget composition, rebuilds, performance, or platform-adaptive UI.

---

## Navigation

→ Load `skills/mobile/flutter/references/navigation.md` when working with routing, deep links, or navigation guards.

---

## Flavors (Multi-Environment)

Flavors allow separate configurations for `dev`, `staging`, and `production` without code changes.

```dart
// lib/core/config/app_config.dart
enum Flavor { development, staging, production }

class AppConfig {
  static late Flavor flavor;
  static late String apiBaseUrl;

  static void setup(Flavor f) {
    flavor = f;
    apiBaseUrl = switch (f) {
      Flavor.development => 'https://api.dev.example.com',
      Flavor.staging => 'https://api.staging.example.com',
      Flavor.production => 'https://api.example.com',
    };
  }
}
```

- Run with flavor: `flutter run --flavor development -t lib/main_development.dart`
- Never use `if (kDebugMode)` as a substitute for flavors — debug/release and dev/prod are orthogonal concerns
- CI must build each flavor separately and run tests against each

---

## Platform Channels (Native Code)

Use platform channels only when a Dart/Flutter package does not exist for the required native API.

```dart
const _channel = MethodChannel('com.company.app/biometric');

Future<bool> authenticate() async {
  try {
    return await _channel.invokeMethod<bool>('authenticate') ?? false;
  } on PlatformException catch (e) {
    return false;
  }
}
```

- Channel names must be namespaced: `com.company.app/feature`
- Always handle `MissingPluginException` and `PlatformException` on the Dart side
- Prefer **Pigeon** for type-safe, generated channel code in production apps

---

## Integration Awareness

| Service | Detection | Action |
|---------|-----------|--------|
| Firebase | `google-services.json` / `GoogleService-Info.plist` | Use `firebase_core`, initialize before `runApp()` |
| Supabase | `supabase_flutter` dep | Initialize with `Supabase.initialize()` before `runApp()` |
| Crashlytics | `firebase_crashlytics` dep | Pass `FlutterError.onError` to Crashlytics in `main()` |
| Push (FCM) | `firebase_messaging` dep | Request permission; handle background messages via top-level function |

---

## Testing

| Layer | Tool | Scope |
|-------|------|-------|
| Unit | `flutter test` + `mocktail` | Business logic, use cases, repositories |
| Widget | `flutter_test` + `WidgetTester` | Individual widget rendering and interaction |
| Golden | `golden_toolkit` | Visual regression — pixel-diff screenshots |
| Integration | `integration_test` package | Full app flow on simulator / device |

- Mock dependencies with `mocktail` — never use real network or file I/O in unit/widget tests
- Golden tests: generate goldens on CI; fail on diff; regenerate intentionally with `--update-goldens`
- Integration tests must run on a physical device or a CI device farm (Firebase Test Lab, BrowserStack)
- BLoC: test using `bloc_test` — assert emitted states for each event

---

## App Store & Play Store — Publication Checklist

### Both Platforms
- [ ] `version` and `build_number` incremented in `pubspec.yaml`
- [ ] Flutter and all dependencies on stable channel and up-to-date (`flutter pub outdated`)
- [ ] Release build tested on physical device: `flutter run --release`
- [ ] No `print()` statements in production code (`debugPrint()` only, or a proper logger)
- [ ] Privacy policy URL configured in store listing
- [ ] App icon generated in all sizes (`flutter_launcher_icons` package)
- [ ] Splash screen configured (`flutter_native_splash` package)

### iOS (App Store)
- [ ] `CFBundleIdentifier` matches App Store Connect entry
- [ ] `CFBundleShortVersionString` and `CFBundleVersion` match `pubspec.yaml` version/build
- [ ] All required `NSUsageDescription` keys set in `ios/Runner/Info.plist`
- [ ] Signed with distribution certificate via Xcode or Fastlane
- [ ] TestFlight build validated before production submission
- [ ] Bitcode setting matches App Store Connect requirements (disabled for most modern apps)

### Android (Play Store)
- [ ] `applicationId` matches Play Console entry
- [ ] `versionName` and `versionCode` match `pubspec.yaml`
- [ ] Release APK/AAB signed with the upload keystore (never commit keystore to git)
- [ ] ProGuard/R8 rules verified — check for missing keep rules with a release build
- [ ] `targetSdkVersion` ≥ current Google Play requirement
- [ ] Adaptive icon configured in `android/app/src/main/res/`
- [ ] Internal testing track validated before production rollout
- [ ] Data safety section filled in Play Console
