---
name: mobile-release-coordinator
description: Coordinate cross-platform mobile releases and select the correct platform-specific release skill. Use when the user asks to prepare, check, or publish a mobile app release without specifying only App Store or only Google Play.
---

# Mobile Release Coordinator

Use this skill as the entrypoint for general mobile release requests such as "prepare release", "publish the app", "check store readiness", or "ship to both stores".

## Route to platform skills

- For iOS, App Store Connect, TestFlight, App Review, or Apple signing: use `app-store-release`.
- For Android, Google Play, Play Console, Android signing, or Data safety: use `google-play-release`.
- For both platforms: run shared checks first, then handle iOS and Android separately.

## Shared workflow

1. Inspect the repository structure and identify project stack.
2. Detect release tooling:
   - `ios/fastlane/Fastfile`
   - `android/fastlane/Fastfile`
   - Flutter build scripts
   - Gradle tasks
   - Xcode workspace/project
   - CI workflows
3. Identify version source and ensure platform versions are aligned when the product expects them to be aligned.
4. Check common release materials:
   - Release notes
   - Store screenshots
   - Privacy policy URL
   - Support URL
   - Demo account or review instructions
   - Production API/environment flags
   - Store privacy artifacts such as `PrivacyInfo.xcprivacy`, App Privacy, and Google Play Data safety
   - Release signing and store API credentials without exposing secret values
   - Analytics, crash reporting, push, sign-in, location, payments, subscriptions, maps, user content, AI features
5. Run platform-specific skill workflows.
6. Summarize shared risks and platform-specific blockers separately.

## Detection hints

- Flutter: `pubspec.yaml`, `android/`, `ios/`, `flutter build`.
- React Native: `package.json`, `ios/`, `android/`, Metro, Gradle, Xcode project.
- Expo/EAS: `app.json`, `app.config.*`, `eas.json`.
- Native iOS: `.xcodeproj` or `.xcworkspace` without shared cross-platform project files.
- Native Android: `settings.gradle`, `build.gradle`, `gradlew`, Kotlin/Java source.
- fastlane iOS: `ios/fastlane/Fastfile`.
- fastlane Android: `android/fastlane/Fastfile`.

## Output format

For multi-store checks, report:

1. Shared release state.
2. iOS/App Store state.
3. Android/Google Play state.
4. Blockers.
5. Exact next commands or manual console steps.

Always separate:

- Locally verified facts.
- Store-console checks that remain manual.
- Risky release automation defaults such as submit, auto-release, production rollout, or debug signing fallback.

## Rules

- Do not assume one platform's release state implies the other is ready.
- Do not run production release commands unless the user explicitly asked for execution and the repository command has been inspected.
- Treat current store policies as time-sensitive and verify official sources before making policy claims.
- Keep generated open-source examples free of real identifiers and credentials.
