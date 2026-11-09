---
name: run-app
description: Build, install, launch and screenshot a house Android debug variant on an emulator via the Android CLI, and run a journey on it when one is named.
argument_hint: "[avd] [flavour] [journey]"
allowed_tools: Bash(android info*), Bash(android emulator list*), Bash(android emulator start *), Bash(android run *), Bash(android screen *), Bash(android layout*), Bash(android input *), Bash(./gradlew :app:assemble*), Bash(adb devices*), Bash(adb logcat *), Bash(adb shell monkey *)
preamble: playbook
---

# Run the app: {@args}

Defaults: the default phone AVD named in `{@home}machine.md`, and the project's default debug flavour and application id
from its {@project_file_full}. Load the `android-cli` skill if any command below is unfamiliar.

Skills named below are optional companions. When one is missing, follow `references/companions.md` in {@skill_named android-kit/standards} and continue.

1. `android info`, then confirm the compile SDK platform is installed (`ls $ANDROID_HOME/platforms`, because the `android sdk list` pattern filter misses `android-37.0`-style names).
2. `android emulator list`. If the AVD is not running, `android emulator start <avd>` and wait until `adb devices` shows `device`.
3. Build: `./gradlew :app:assemble<Flavour>Debug` (capitalise the flavour, and omit the flavour segment if the project has none).
4. Install and launch: `android run --apks <apk path from the build output> --device <serial>` (never `--debug`, because it makes
   the app wait for a debugger and the screen shows "Waiting For Debugger"). If the launch does not come to the foreground,
   `adb shell monkey -p <applicationId> -c android.intent.category.LAUNCHER 1`. Flavoured apps suffix the id (e.g. `.sit`).
5. On the first screen, `android screen`, then save the PNG to the session scratchpad as `<avd>-<flavour>-<screen>.png`.
   `android layout` when the caller needs the view tree.
6. When the caller names a journey file, hand it to the `android-verifier` agent with the device serial, the application
   id, the scratchpad directory and confirmation that the app is launched. It returns the JSON result described in
   `references/journeys.md` in {@skill_named android-kit/standards}.
7. Report: device serial and AVD, variant, APK path, launch result, screenshot path(s), the journey result if one ran,
   and the last 30 lines of `adb logcat -d -s AndroidRuntime` if anything crashed.

<!-- if: skill_allowlist -->
Device commands outside `allowed-tools`, such as uninstall or emulator removal, use the approval policy and prompt. A request to run the app authorizes its normal build, install and launch steps.
<!-- else -->
Use the configured approval policy for device commands. A request to run the app authorizes its normal build, install and launch steps.
<!-- end -->
