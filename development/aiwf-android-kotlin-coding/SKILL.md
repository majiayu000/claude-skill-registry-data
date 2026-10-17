---
name: aiwf-android-kotlin-coding
description: Use for Android and Kotlin app work involving Gradle Kotlin DSL, Jetpack Compose, lifecycle and state, Room, Retrofit or OkHttp, coroutines and Flow, ONNX Runtime, Firebase, APK or AAB builds, ADB, emulators, and real-device validation.
---

# AIWF Android Kotlin Coding

## Core Rule

Inspect the app's pinned Android Gradle Plugin, Gradle wrapper, Kotlin, JDK, SDK levels, version catalog, modules, and device target before changing code. Keep UI, data, network, inference, and secrets boundaries explicit.

## Workflow

1. Read project guidance, `settings.gradle.kts`, root and module build files, `gradle/libs.versions.toml`, manifests, ProGuard rules, tests, and CI.
2. Classify the change: Compose UI, lifecycle/state, Room/data, network/API, on-device model runtime, native/JNI, build/signing, or device integration.
3. Follow the existing architecture. Keep screen state in the established state holder, hoist reusable component state, and collect asynchronous data with lifecycle-aware project patterns.
4. Keep blocking I/O and model inference off the main thread. Preserve coroutine cancellation and avoid work that outlives its owner.
5. Validate locally, then on an emulator or device only when the task needs device behavior.

## Guardrails

- Do not upgrade Gradle, Android Gradle Plugin, Kotlin, Compose BOM, compile SDK, or target SDK as a hidden fix.
- Do not embed live API keys in source, resources, `BuildConfig`, APK assets, logs, or committed property files. Client-side secrets are recoverable.
- Keep Room schema and migrations aligned; add `aiwf-data-storage` for schema or migration work.
- Preserve Compose semantics, content descriptions, focus, touch targets, adaptive layout, loading, error, and offline states.
- Treat `127.0.0.1` on a physical phone as the phone. Use an approved LAN address or an explicit `adb reverse` mapping for a host service.
- Do not install APKs, flash devices, alter signing material, or run connected tests unless Shawn requested device-side work.
- Add `aiwf-cpp-coding` for JNI or native C++ and `aiwf-nvidia-cuda-cudnn-sdk` only for supported NVIDIA Android or Jetson targets.

## Validation

Prefer repository tasks. Typical checks are:

```powershell
.\gradlew.bat :app:testDebugUnitTest
.\gradlew.bat :app:lintDebug
.\gradlew.bat :app:assembleDebug
adb devices -l
```

Run connected or screenshot tests only when a configured emulator/device is available. Report the exact variant and device used.

## Primary Sources

- Android app architecture: https://developer.android.com/topic/architecture
- Compose state: https://developer.android.com/develop/ui/compose/state
- Compose testing: https://developer.android.com/develop/ui/compose/testing
- Android Debug Bridge: https://developer.android.com/tools/adb
