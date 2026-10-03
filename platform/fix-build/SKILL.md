---
name: fix-build
description: Diagnose and fix a failing iOS or Android build. Use when the build is broken, pod install or Gradle fails, or the user asks to fix a native build error.
argument-hint: "[ios|android]"
---

Fix the failing native build. Work the problem, do not shotgun it.

1. Identify the project shape first: Expo with CNG (no committed native folders, or folders marked generated), bare workflow, or plain React Native. Check for `app.json`/`app.config.*`, `eas.json`, and whether `ios/` and `android/` are committed.

2. Reproduce the failure and capture the full log:
   - If the user provided a platform in `$ARGUMENTS`, build that one. Otherwise ask which platform failed, or build the one whose error the user pasted.
   - Expo projects: `npx expo run:ios` / `npx expo run:android` (or `cd ios && pod install` first when pods are the suspect)
   - Plain React Native without the expo package: `npx react-native run-ios` / `npx react-native run-android`
   - Pipe output to a file so nothing scrolls away.

3. Find the FIRST real error in the log, not the last line. Android: deepest `Caused by:`. iOS: first `error:` line and the build step above it. Quote the exact error to the user in one line before fixing anything.

4. Apply the native-build-errors skill's playbook for that error family. Choose the smallest fix that addresses the cause. Cache cleaning goes in the documented order, never as step one, and each destructive step gets stated before it runs.

5. If the error names a third-party library, search its GitHub issues for the exact error string plus the React Native version before patching anything locally.

6. Rebuild to verify. A fix without a green rebuild is a guess. If the rebuild surfaces a NEW first error, that is progress; repeat from step 3.

7. Close with a short report: root cause, what changed, and whether the fix has release implications (a new native dependency or config change means the next release must be a store build, not an OTA update).
