---
name: mobile-crash-sdk
category: observability
description: Use when an "enable observability" card asks for crash reporting on a mobile (iOS, Android, React Native, Flutter) or desktop app - adding Sentry or Firebase Crashlytics with release and environment tags, symbol upload, and session tracking so crash-free users can be read
source: getsentry/sentry-cocoa, sentry-java, sentry-react-native, Firebase Crashlytics docs (MIT/Apache-2.0), adapted
---

# Mobile crash reporting

The mobile golden signal is crash-free users per release. It needs three things from the app: a crash SDK, the release (version + build) and environment on every event, and session tracking — without sessions a tool knows how many crashes there were but not out of how many users.

## Sentry

- **iOS** (`sentry-cocoa`, Swift Package Manager): `SentrySDK.start { o in o.dsn = …; o.releaseName = "\(bundleId)@\(version)+\(build)"; o.environment = "production"; o.enableAutoSessionTracking = true }` at app launch. Upload dSYMs in the release build (`sentry-cli debug-files upload` or the Fastlane `sentry_debug_files_upload` action) or crashes arrive unsymbolicated.
- **Android** (`io.sentry:sentry-android` + the `io.sentry.android.gradle` plugin): DSN, release and environment in the manifest `<meta-data>` or `SentryAndroid.init`; the Gradle plugin uploads the R8/ProGuard mapping per build.
- **React Native**: `@sentry/react-native` (its wizard wires both native projects and source maps). **Flutter**: `sentry_flutter` with `SentryFlutter.init`, and `--split-debug-info` symbols uploaded.
- The DSN is not a secret, but the `sentry-cli` auth token used for uploads is: a CI secret, never in the repository.

## Firebase Crashlytics

- **iOS**: `FirebaseCrashlytics` via SPM, `FirebaseApp.configure()`, and the `upload-symbols` run script phase for dSYMs.
- **Android**: `com.google.firebase:firebase-crashlytics` and the `com.google.firebase.crashlytics` Gradle plugin (mapping upload on release builds).
- Crashlytics takes the version from the app itself; set the environment as a custom key (`Crashlytics.crashlytics().setCustomValue("staging", forKey: "environment")`) and keep debug builds out (`setCrashlyticsCollectionEnabled(false)` there).
- Crash-free users is reported by the Firebase console; Google Play's Android vitals (and App Store Connect's metrics) give the store-side view a store data source reads.

## Desktop (Electron)

`@sentry/electron` in both the main and renderer processes, release from `app.getVersion()`, native crash minidumps enabled.

## In the task

- One SDK, initialised before anything else at launch; no personal data in breadcrumbs (strip request bodies, emails, tokens).
- Acceptance criteria: "Given a build of this release crashes on a test device, then the crash appears in <Sentry|Crashlytics> symbolicated, tagged with this version and environment"; "Given the app is opened, then a session is recorded for this release."
- A store build has to ship before any of this is visible: say so, and tell the person which data source (Sentry, Google Play vitals, App Store metrics) to add so `mobile.crash_free_users` can be bound.
