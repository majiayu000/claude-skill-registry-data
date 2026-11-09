---
name: run-app
description: Build, install, launch and screenshot an iOS debug scheme on a simulator via xcodebuild and xcrun simctl, and run a journey on it when one is named.
argument-hint: "[simulator name] [scheme] [journey]"
allowed-tools: Bash(xcodebuild -version*), Bash(xcodebuild -list *), Bash(xcodebuild build *), Bash(xcodebuild -showBuildSettings *), Bash(xcrun simctl list *), Bash(xcrun simctl boot *), Bash(xcrun simctl bootstatus *), Bash(xcrun simctl install *), Bash(xcrun simctl launch *), Bash(xcrun simctl openurl *), Bash(xcrun simctl io *), Bash(xcrun simctl ui *), Bash(xcrun simctl spawn * log show *), Bash(open -a Simulator*), Bash(pod install*), Bash(axe --help), Bash(axe describe-ui *), Bash(axe tap *), Bash(axe type *), Bash(axe gesture *), Bash(axe button *), Bash(axe screenshot *)
---

# Run the app: $ARGUMENTS

Defaults: the simulator named in `~/.claude/machine.md` or the project instructions, otherwise a compatible available iPhone from `xcrun simctl list devices available`, and
the project's workspace, default debug scheme and bundle id from its `CLAUDE.md`. Never guess a scheme name. Quote `xcodebuild -list`.

1. `xcodebuild -version`, then `xcodebuild -list -workspace <ws>` and confirm the scheme exists. CocoaPods repos: run `pod install`
   first when `Pods/` is missing or `Podfile.lock` changed. SwiftPM-only repos need nothing.
2. `xcrun simctl list devices available`, then record the selected simulator UDID and use it for every subsequent command. If the simulator is not `Booted`, run `xcrun simctl boot <udid>`, then
   `xcrun simctl bootstatus <udid> -b`. `open -a Simulator` when the caller wants to watch.
3. Build: `xcodebuild build -workspace <ws> -scheme "<scheme>" -destination 'platform=iOS Simulator,id=<udid>'
   -derivedDataPath <scratchpad>/DerivedData -quiet`. On failure re-run without `-quiet` and quote the first `error:` lines.
4. Locate the product: `xcodebuild -showBuildSettings … | grep -E 'BUILT_PRODUCTS_DIR|FULL_PRODUCT_NAME'`.
   Install and launch: `xcrun simctl install <udid> <path>.app`, then `xcrun simctl launch <udid> <bundle id>` (prints the pid).
   Deep link: `xcrun simctl openurl <udid> <url>`.
5. On the first screen: `xcrun simctl io <udid> screenshot <scratchpad>/<simulator>-<scheme>-<screen>.png`.
   For accessibility or dark-mode checks: `xcrun simctl ui <udid> content_size accessibility-extra-large`,
   `xcrun simctl ui <udid> appearance dark`, then screenshot again.
6. When the caller names a journey file, hand it to the `ios-verifier` agent with the UDID, the bundle id, the scratchpad
   directory and confirmation that the app is launched. It returns the JSON result described in `references/journeys.md`
   in `ios-kit:standards`. If any action came back SKIPPED with "no driver" and this session has a simulator
   control tool that can tap and type, run the journey here with that tool, following the same reference. That result
   replaces the verifier's. When the verifier lists a missing driver under Findings, tell the user its install command once
   per session.
7. Report: simulator name, UDID and OS, scheme and configuration, `.app` path, launch pid, screenshot path(s), the journey
   result if one ran, and if the app crashed, the last 30 lines of `xcrun simctl spawn <udid> log show --last 2m --predicate 'processImagePath CONTAINS "<App>"'`.

Do not erase or delete simulators, or change privacy permissions, without user authorization. Record the existing appearance and content-size settings before a visual check and restore them afterwards. Plain simctl cannot tap or type. Interaction uses the driver order in `references/journeys.md`: a simulator control tool, then AXe, then the project's XCUITests, otherwise interaction checks are Unverified.
