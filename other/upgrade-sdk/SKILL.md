---
name: upgrade-sdk
description: Run a guided Expo SDK upgrade. Use when the user asks to upgrade the Expo SDK or React Native version.
argument-hint: "[target sdk version]"
disable-model-invocation: true
---

Upgrade this project's Expo SDK deliberately, one version at a time, following the expo-sdk-upgrade skill. `$ARGUMENTS` may name the target SDK; if the jump spans more than one major, tell the user you will land them one at a time and do the first hop now.

1. Preflight, before changing anything:
   - Confirm the working tree is clean; if not, stop and ask.
   - Create an upgrade branch.
   - Record the current state: `npx expo-doctor` output and the dependency list. This is the baseline to diff against.
   - Read the target SDK's changelog (search for the official "Expo SDK <version>" changelog post) and list the breaking changes that touch dependencies this project actually uses. Show that list to the user before proceeding.

2. Execute in the canonical order: bump `expo`, then `npx expo install --fix`, then `npx expo-doctor`. Resolve doctor complaints before building anything.

3. Regenerate natives when the project uses CNG: `npx expo prebuild --clean`. In a bare project, apply the native diffs the changelog calls out instead.

4. Verify honestly:
   - `npx tsc --noEmit` and the test suite.
   - Build and boot BOTH platforms.
   - Walk the native-heavy paths: auth, purchases, camera or media if present, push, deep links.

5. Check the OTA fence before finishing: confirm the runtime version will differ from the previous release (appVersion policy plus a version bump, or an explicit runtime bump). State plainly that the first release after this upgrade must be a store build.

6. Report: what moved, what broke and how it was fixed, which patches or workarounds became deletable, and what remains for the user to decide. Do not commit unless asked.
