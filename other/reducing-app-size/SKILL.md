---
name: flutter-reducing-app-size
description: Measures and optimizes the size of Flutter application bundles for deployment. Use when minimizing download size or meeting app store package constraints.
tags: [flutter, app-size, optimization, tree-shaking, deployment, release]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter App Size Optimization

## Contents
- [Core Concepts](#core-concepts)
- [Workflow: Generating Size Analysis](#workflow-generating-size-analysis)
- [Workflow: Analyzing in DevTools](#workflow-analyzing-in-devtools)
- [Workflow: Estimating iOS Download Size](#workflow-estimating-ios-download-size)
- [Workflow: Size Reduction Strategies](#workflow-size-reduction-strategies)
- [Examples](#examples)

## Core Concepts

- **Debug vs. Release:** Never use debug builds to measure app size. Debug builds include VM overhead and lack AOT compilation and tree-shaking.
- **Upload vs. Download Size:** The upload package (APK, AAB, IPA) size ≠ end-user download size. App stores filter architectures and asset densities per device.
- **AOT Tree-Shaking:** Dart AOT compiler automatically removes unused/unreachable code in profile and release modes.
- **Size Analysis JSON:** The `--analyze-size` flag generates a `*-code-size-analysis_*.json` detailing byte sizes of packages, libraries, classes, and functions.

## Workflow: Generating Size Analysis

- [ ] Determine the target platform (apk, appbundle, ios, linux, macos, windows).
- [ ] Run the Flutter build command with `--analyze-size`.
- [ ] Locate the generated `*-code-size-analysis_*.json` in `build/`.

### Platform-Specific Commands

```bash
# Android App Bundle
flutter build appbundle --analyze-size --target-platform=android-arm64

# Android APK
flutter build apk --analyze-size --target-platform=android-arm64

# iOS
flutter build ios --analyze-size

# Desktop
flutter build macos --analyze-size
```

> **Note:** iOS `--analyze-size` creates a `.app` file useful for relative sizing, but not for estimating final App Store download size. Use the iOS estimation workflow below.

## Workflow: Analyzing in DevTools

- [ ] Launch DevTools: `dart devtools`.
- [ ] Select "Open app size tool" from the landing page.
- [ ] Upload the generated `*-code-size-analysis_*.json`.
- [ ] Inspect treemap/tree view to identify large packages, libraries, or assets.
- [ ] **Feedback Loop:**
  1. Identify largest contributors to app size.
  2. Determine if the dependency/asset is strictly necessary.
  3. Remove, replace, or optimize the identified component.
  4. Regenerate Size Analysis JSON and compare using DevTools "Diff" tab.

## Workflow: Estimating iOS Download Size

- [ ] Configure app version and build number in `pubspec.yaml`.
- [ ] Generate Xcode archive: `flutter build ipa --export-method development`.
- [ ] Open archive (`build/ios/archive/*.xcarchive`) in Xcode.
- [ ] Click **Distribute App** → select **Development**.
- [ ] App Thinning: select **All compatible device variants**.
- [ ] Check **Strip Swift symbols**.
- [ ] Sign and export the IPA.
- [ ] Open exported directory and review `App Thinning Size Report.txt`.

### Reading the Size Report

```text
Variant: Runner-7433FC8E-1DF4-4299-A7E8-E00768671BEB.ipa
Supported variant descriptors: [device: iPhone12,1, os-version: 13.0]
App + On Demand Resources size: 5.4 MB compressed, 13.7 MB uncompressed
App size: 5.4 MB compressed, 13.7 MB uncompressed
```

*The compressed size = end-user download size. The uncompressed size = on-device footprint.*

## Workflow: Size Reduction Strategies

Apply these strategies to reduce the compiled footprint:

- [ ] **Split Debug Info:** Strip debug symbols and store separately.
  ```bash
  flutter build apk --obfuscate --split-debug-info=build/app/outputs/symbols
  ```
- [ ] **Remove Unused Resources:** Audit `pubspec.yaml` and `assets/` directory. Delete unreferenced images, fonts, and files.
- [ ] **Minimize Library Resources:** Review third-party packages. If a package imports massive resources (e.g., large icon sets) but only a fraction is used, consider alternatives.
- [ ] **Compress Media:** Compress PNG/JPEG assets using `pngquant`, `imageoptim`, or convert to WebP before bundling.
- [ ] **Use Deferred Components:** For large apps, use deferred loading to download features on demand.
- [ ] **Audit Dependencies:** Remove unused packages from `pubspec.yaml`. Each package adds to the binary.

### Size Impact Reference

| Optimization | Typical Savings |
|---|---|
| `--split-debug-info` + `--obfuscate` | 10-20% of binary |
| Removing unused assets | Varies (often 1-5 MB) |
| WebP conversion for images | 25-35% per image |
| Removing unused packages | Varies significantly |

## Anti-patterns

- ❌ Measuring app size from debug builds
- ❌ Assuming APK/IPA size equals user download size
- ❌ Including large icon font packages (e.g., full FontAwesome) when only a few icons are used
- ❌ Bundling uncompressed high-resolution images
- ❌ Keeping unused packages in `pubspec.yaml`

## Resources

- https://docs.flutter.dev/perf/app-size
- https://docs.flutter.dev/deployment/obfuscate
- https://docs.flutter.dev/perf/deferred-components
- https://docs.flutter.dev/deployment/android
- https://docs.flutter.dev/deployment/ios
