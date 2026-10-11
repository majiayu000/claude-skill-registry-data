---
name: android
description: Android engineering rules — permissions, release signing, Kotlin/Compose. Load for Android.
---

## Scope

This skill is the **engineering** half of Android support: platform rules that apply to any Android task — permissions, release signing, distribution, and native code standards.

The **design** half lives in `skills/mobile/material-design/SKILL.md` (color system, typography scale, components, motion, adaptive layout, accessibility). Load it **only when the task touches UI** — screen layout, navigation, visual or interaction design. A signing, build, or non-UI logic task does not need it.

## Design & UX (non-negotiable, applies even to non-UI tasks)

- Support **edge-to-edge** layout — use `WindowInsets` to avoid overlap with system bars
- Use **adaptive icons** (`mipmap-anydpi-v26/`) — required for Android 8.0+
- Support **back gesture** (predictive back on Android 14+) — register `OnBackPressedCallback` instead of overriding `onBackPressed()`
- Test on both small screens (< 5") and large screens / foldables

## Permissions & Privacy

- Declare only the permissions you actually use in `AndroidManifest.xml`
- Request runtime permissions with `ActivityResultContracts.RequestPermission`
- Handle `shouldShowRequestPermissionRationale()` — show an explanation before re-requesting
- Target the latest stable `targetSdkVersion` required by Google Play
- Fill the **Data Safety** section in Play Console accurately — it is legally binding

## Code Signing & Release

- The upload keystore must be stored securely (EAS Credentials, 1Password, or CI secret store) — **never commit it to the repository**
- Use **Android App Bundle (AAB)** for Play Store submissions — not APK
- Enable **R8/ProGuard** for release builds; test the release build locally before submitting to catch missing keep rules
- `versionCode` must be monotonically increasing — Play Store rejects builds with the same or lower version code

## Native Kotlin / Jetpack Compose Standards

- Prefer **Jetpack Compose** for new screens; use **Views/XML** only when Compose cannot achieve the required behavior or when maintaining existing View-based code
- Use `ViewModel` + `StateFlow`/`SharedFlow` for UI state — never hold state in Activities or Fragments
- Use **Room** for local persistence; **DataStore** for preferences (not SharedPreferences for new code)
- `suspend` functions and `Flow` over callbacks for all new async code
- Never run network or database operations on the main thread
