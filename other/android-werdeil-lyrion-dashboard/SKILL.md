---
name: android
description: >-
  Work on the Android app — the thin WebView wrapper in `android/`. Use this
  whenever a task touches the Kotlin sources, the Gradle build, the WebView
  shell, the native settings screen, LMS server auto-discovery, the JS↔native
  bridge, app strings/i18n, or the Android CI/lint. Covers the "shell only, UI
  lives on the web" principle, the debug/release signing split, the static
  versioning F-Droid needs, and the min/target SDKs, so changes fit the wrapper.
---

# Android app (WebView wrapper)

The Android app is a **thin native shell**: the whole UI is the web dashboard served by the Flask app, loaded in a full-screen WebView. Same principle as [lms-material-app](https://github.com/CDrummond/lms-material-app). Don't rebuild dashboard UI natively — if a feature belongs on screen, it belongs in the web page; the app only provides shell concerns (window, settings, discovery, a native bridge).

Everything lives under `android/`. Package `com.werdeil.lyriondashboard`, Kotlin, Gradle KTS, `minSdk = 26` (Android 8.0), `targetSdk = 35`, `compileSdk = 37`, Java/JVM 17.

## Layout

```
android/app/src/main/
├── java/com/werdeil/lyriondashboard/
│   ├── MainActivity.kt        # the WebView host + JS bridge
│   ├── SettingsActivity.kt    # native settings screen
│   ├── ServerDiscovery.kt     # LMS auto-discovery (UDP broadcast)
│   └── Insets.kt              # edge-to-edge window insets
├── res/values/strings.xml      # EN strings   (values-fr/ = FR)
├── res/xml/preferences.xml      # settings screen definition
└── AndroidManifest.xml
```

## Build & lint

```bash
cd android
./gradlew assembleDebug   # -> app/build/outputs/apk/debug/app-debug.apk
./gradlew lintDebug       # Android Lint (gates CI)
```

CI is `.github/workflows/android.yml`: on every push touching `android/**` it runs `lintDebug` then `assembleDebug` and uploads the debug APK as an artifact. The release APK is built and attached only when a GitHub release is published (see the `release` skill).

## Signing: debug vs release

- **Debug** is signed with a **committed** `app/debug.keystore` (standard debug credentials) on purpose — so every ephemeral CI runner signs with the same key and Android will update the app over a previous install instead of refusing. Debug builds also use an `applicationIdSuffix = ".debug"` and a distinct label, so they install **side by side** with the release app.
- **Release** signing is driven by environment variables (`ANDROID_KEYSTORE_PATH` and friends) so the release keystore is never committed. Without them a *local* release build stays unsigned, which is also what F-Droid wants — but the release workflow refuses to publish an unsigned APK: it validates the keystore up front and runs `apksigner verify` on the result (see the `release` skill).

## Versioning (must stay static)

`versionName` and `versionCode` in `app/build.gradle.kts` are **static literals**, committed, because F-Droid builds from the tagged source and parses them from that file. `versionCode` packs the semver as `X*10000 + Y*100 + Z`. Don't compute them at build time. Bumping is the Release workflow's job — see the `release` skill.

## The JS ↔ native bridge

`MainActivity` injects a `window.LyrionApp` object into the page. The web JS detects it, adds `body.in-app`, and wires the header menu to `bridge.openMenu()` / `openSettings()` and the card's pull-to-refresh gesture to `bridge.reload()` (see the `frontend` skill). If you add a native capability the page should call, expose it as a method on that bridge and guard the page-side use behind the object's presence, matching the existing pattern.

## Auto-discovery

`ServerDiscovery` finds the Lyrion server via **UDP broadcast on port 3483** (the standard LMS discovery protocol) and suggests `http://<host>:1111` (assumes the dashboard runs on the same host). Caveat baked into the UX: discovery can't cross a VPN tunnel, so the settings screen lets the user enter the URL manually. Cleartext HTTP is allowed (LAN-only app).

## Strings / i18n

App strings are bilingual like the web app: `res/values/strings.xml` (EN) and `res/values-fr/strings.xml` (FR) must carry the same keys. Store-listing texts live under `fastlane/metadata/android/{en-US,fr-FR}/`. Add a new string to both locales — never one only. The same tree holds `images/icon.png`, the 512x512 render of `static/favicon.svg` that F-Droid shows on the app page: its indexer cannot render the adaptive-icon XML, so without that bitmap the listing has no icon. `full_description.txt` is never hard-wrapped — F-Droid clients keep every newline, so a paragraph wrapped at 70 columns renders ragged; one paragraph (and one bullet) is one line, however long.

## Checklist

1. Keep it a shell — new UI goes in the web page, not native views.
2. New user string → both `values/` and `values-fr/` strings.xml.
3. New native capability the page uses → method on `window.LyrionApp`, guarded page-side by the bridge's presence.
4. Leave `versionName`/`versionCode` static; bump via the Release workflow.
5. `./gradlew lintDebug assembleDebug` clean before pushing (CI runs both).
