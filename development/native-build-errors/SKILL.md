---
name: native-build-errors
description: Diagnosing failed iOS and Android builds. Use for pod install, Gradle, Xcode or linker errors, pasted native build output, CocoaPods, Kotlin, JDK, codegen and cache problems.
user-invocable: false
---

# Native build failure triage

## The one rule that matters

Native build logs bury the real error under hundreds of lines of noise. Always find the FIRST real error, not the last line. The last line is usually a generic "build failed" wrapper around the actual cause.

- Android: search the log for `FAILURE:` and `Caused by:`. The deepest `Caused by:` is the real one. Also look for `> Task :app:... FAILED` to identify which task died.
- iOS: search for `error:` (lowercase, with colon). Ignore `warning:`. When xcodebuild output is huge, the failing step name right above the first `error:` tells you which pod or script phase broke.

Never start by nuking caches. Read the error first. Cache-nuking is step 8, not step 1.

## iOS playbook

**pod install fails**
- `None of your spec sources contain a spec satisfying the dependency`: the lockfile and Podfile disagree, usually after a branch switch or dependency bump. Start gentle: `cd ios && pod install --repo-update`. Only if that fails, remove `Pods/` and `Podfile.lock` and reinstall; in an RN project the lockfile regenerates from package.json, which is why this is acceptable here and not for JS lockfiles (see the last-resort section).
- Ruby/ffi errors on Apple Silicon: the project's Ruby is too old or gems were built for the wrong arch. Prefer the version from `.ruby-version`. `bundle install && bundle exec pod install` beats global pods.
- `could not find compatible versions for pod X`: two libraries pin conflicting versions of a shared native dependency (common with Firebase and GoogleUtilities). Check which two, then upgrade the older library instead of pinning in the Podfile if possible.

**Xcode build fails after pods succeeded**
- `No such module 'X'`: the pod exists but the workspace was not used, or DerivedData holds a stale module map. Confirm you opened `.xcworkspace`, then `rm -rf ~/Library/Developer/Xcode/DerivedData`.
- Duplicate symbols or `use_frameworks!` conflicts: static and dynamic linkage mixing, classic with Firebase. In Expo projects set `useFrameworks: "static"` via expo-build-properties instead of hand-editing the Podfile.
- Signing errors on device builds: set the development team in Xcode once, or use EAS credentials. Do not commit personal team IDs into the project file of a shared repo.
- A script phase fails (Hermes, sourcemaps, `[CP-User]`): open the phase's own log section. These phases inherit PATH from Xcode, not your shell, so tools installed via nvm or asdf may not resolve. Hardcoding node paths in `.xcode.env.local` fixes most of it.

**Clean order for iOS, least to most destructive**
1. Rebuild once (transient failures are real)
2. `rm -rf ios/build`
3. `rm -rf ~/Library/Developer/Xcode/DerivedData`
4. `cd ios && rm -rf Pods Podfile.lock && pod install`
5. In Expo CNG projects: `npx expo prebuild --clean -p ios` (this regenerates the whole ios folder, so any manual edits there will be lost; that is the point)

## Android playbook

**Toolchain mismatches, the top cause**
- AGP 8.x requires JDK 17. `Unsupported class file major version` or `invalid source release` means the JDK does not match. Check `java -version` and JAVA_HOME, and remember Android Studio ships its own JDK that Gradle may or may not use (`org.gradle.java.home`).
- Kotlin version clashes: `Module was compiled with an incompatible version of Kotlin`. One library bundles a newer Kotlin than your project. Either upgrade the project's `kotlinVersion` (Expo: android build properties) or upgrade the offending library. Do not pin random forks.

**Dependency and merge failures**
- `Duplicate class` errors: two libraries ship the same classes, usually play-services or kotlin-stdlib variants. Find both with `./gradlew :app:dependencies`, then exclude from the one that should not provide it.
- Manifest merger failed: a library demands a higher minSdk or a conflicting attribute. The error names the library; raise your minSdk only if the library really is required.
- `Could not find com.x:y:z`: a library references a repository you do not have. Check whether the library's install docs require an extra maven block.

**Build environment**
- OOM (`Java heap space`, daemon crashes): raise `org.gradle.jvmargs=-Xmx4g` in gradle.properties.
- Stale codegen or CMake state after upgrades: `rm -rf android/app/.cxx android/app/build android/build`, then rebuild. This fixes most "worked before the upgrade" cases.
- Missing SDK: `local.properties` must point at the SDK dir; CI needs ANDROID_HOME.
- Native `.so` alignment: Google Play requires 16 KB page alignment for native libraries on newer target API levels. If a precompiled `.so` from an old library fails the check, the library needs an update; there is no clean workaround on your side.

**Clean order for Android**
1. Rebuild once
2. `cd android && ./gradlew --stop && ./gradlew clean`
3. `rm -rf android/app/.cxx android/.gradle`
4. Expo CNG: `npx expo prebuild --clean -p android`

## Last resort, in this order

```bash
watchman watch-del-all
rm -rf node_modules
npm install            # or yarn/pnpm, keep the project's lockfile
npx expo prebuild --clean   # CNG projects only
```

Deleting the lockfile is not part of this list. That changes dependency resolution across the whole tree and belongs to a deliberate upgrade, not to build debugging.

## When the error names a specific library

Search the library's GitHub issues with the exact error string plus your React Native version before writing any patch. More often than not there is an open issue with either a released fix (upgrade) or a known patch (use patch-package and leave a comment linking the issue so the patch can be deleted later).
