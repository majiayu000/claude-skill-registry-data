---
name: symbolication-setup
description: Configure crash symbolication for readable stack traces. Use when setting up dSYMs (iOS), ProGuard/R8 mappings (Android), or source maps (React Native).
triggers:
  - "configure dSYMs"
  - "crash symbols"
  - "ProGuard mappings"
  - "readable stack traces"
  - "set up symbolication"
  - "source maps upload"
priority: 1
---

# Symbolication Setup

Make crash stack traces readable instead of memory addresses or minified code.

## Why It Matters

Without symbolication:
```
0x104a3b2c8 <redacted> + 123
```

With symbolication:
```
PaymentViewController.processPayment() line 47
```

**Unsymbolicated crashes are useless for debugging.**

## Platform Setup

### iOS (dSYMs)

**Xcode Build Phase Script:**
```bash
# Add to Build Phases → New Run Script Phase
if [ "${CONFIGURATION}" = "Release" ]; then
    # Sentry
    sentry-cli upload-dif --include-sources "${DWARF_DSYM_FOLDER_PATH}"

    # Or Crashlytics
    "${PODS_ROOT}/FirebaseCrashlytics/upload-symbols" \
        -gsp "${PROJECT_DIR}/GoogleService-Info.plist" \
        -p ios "${DWARF_DSYM_FOLDER_PATH}"
fi
```

**Find missing dSYMs:**
```bash
# Recent archives
find ~/Library/Developer/Xcode/Archives -name "*.dSYM" -mtime -7

# Verify UUID matches
dwarfdump --uuid MyApp.app.dSYM
```

### Android (ProGuard/R8)

**build.gradle.kts:**
```kotlin
android {
    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}

// Sentry auto-upload
sentry {
    autoUploadProguardMapping.set(true)
    uploadNativeSymbols.set(true)
}

// Or manual upload in CI
// sentry-cli upload-proguard --android-manifest app/build/.../AndroidManifest.xml mapping.txt
```

**Keep rules for crash reporting:**
```proguard
# proguard-rules.pro
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile

# Keep Sentry classes
-keep class io.sentry.** { *; }
```

### React Native (Source Maps)

**Expo (app.json):**
```json
{
  "expo": {
    "plugins": [
      ["@sentry/react-native/expo", {
        "organization": "your-org",
        "project": "your-project"
      }]
    ],
    "hooks": {
      "postPublish": [{
        "file": "sentry-expo/upload-sourcemaps"
      }]
    }
  }
}
```

**Bare React Native (CI):**
```bash
# After build
sentry-cli releases files $VERSION upload-sourcemaps \
    --dist $BUILD_NUMBER \
    ./build/sourcemaps
```

**Hermes bytecode:**
```bash
# Hermes requires source maps - verify with:
sentry-cli sourcemaps explain <event-id>
```

## Verification Checklist

- [ ] Release builds upload symbols automatically
- [ ] CI pipeline includes symbol upload step
- [ ] Test crash shows readable stack trace
- [ ] Source maps include original source (not just line numbers)
- [ ] Build numbers match between app and uploaded symbols

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `<redacted>` in stack | Missing dSYM | Upload dSYM for that build |
| Line numbers wrong | Source map mismatch | Verify release/dist strings match |
| Only framework symbols | App dSYM missing | Check archive includes app dSYM |
| `<unknown>` in RN | Hermes without source maps | Configure Hermes source map generation |

## Vendor Commands

| Vendor | Verify Upload |
|--------|---------------|
| Sentry | `sentry-cli debug-files check <UUID>` |
| Crashlytics | Firebase Console → Crashlytics → Missing dSYMs |
| Bugsnag | `bugsnag-cli upload` with `--dry-run` |
| Datadog | Dashboard → Error Tracking → Symbol Files |
| bitdrift | Dashboard or CLI for dSYM, Gradle plugin for ProGuard |

## Related Skills

- See `skills/crash-instrumentation` for breadcrumb strategies and crash context
- Symbolication is Tier 1 in `skills/instrumentation-planning`
