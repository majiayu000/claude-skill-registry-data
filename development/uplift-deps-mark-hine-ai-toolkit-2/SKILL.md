---
name: uplift-deps
description: "Toolchain/dependency uplift playbook for iOS apps: one axis per commit, release-note research, Package.resolved/Podfile.lock diffs, review."
disable-model-invocation: true
argument-hint: "[ticket] [what to uplift, e.g. 'Firebase' or 'deployment target 17']"
---

# Dependency uplift: $ARGUMENTS

Repo facts (workspace, schemes, build/test commands, SwiftPM vs CocoaPods, deliberate pins) come from the project's
`CLAUDE.md`. Work in plan mode until step 4 is approved.

1. **Baseline.** Clean `git status` on `feat/<ticket>-<slug>` (or the project's documented branch convention). Run the project's build and test commands and copy the
   lock files to the scratchpad: `Package.resolved` (workspace: `<ws>.xcworkspace/xcshareddata/swiftpm/Package.resolved`,
   packages: next to `Package.swift`) and `Podfile.lock` if present. Quote results.
2. **Inventory.** List in-scope items with current versions and rules: SwiftPM references in `project.pbxproj`
   (`XCRemoteSwiftPackageReference` → `requirement`) or `Package.swift`, `Podfile` entries, `.swift-version`,
   `SWIFT_VERSION`, `SWIFT_STRICT_CONCURRENCY`, `IPHONEOS_DEPLOYMENT_TARGET`, and the Xcode version in CI (`fastlane`, pipeline YAML).
3. **Research.** Send one `ios-researcher` per axis from step 4, in parallel, each asking for its inventory table. Ask for the latest stable of each item, its release notes, minimum Xcode/deployment target,
   privacy-manifest status, and the current App Store minimum Xcode/SDK requirement and date. For each pod, note whether the vendor also publishes a Swift package, and check trunk status on blog.cocoapods.org. Trunk accepts no new pods or versions from 2026-12-02, so a pod whose target version is not on trunk cannot be updated through CocoaPods.
4. **Plan.** One commit per axis, ordered Xcode/SDK → deployment target → Swift toolchain/language mode → SwiftPM packages →
   CocoaPods, only for versions already on trunk → third-party binaries. Moving a pod to SwiftPM is its own axis and usually its own ticket. Name the schemes you will build and the tests you will run. Get approval.
5. **Apply each axis.** Edit versions only where the project declares them. SwiftPM: change the rule, then
   `xcodebuild -resolvePackageDependencies -workspace <ws> -scheme "<scheme>"`. CocoaPods: `pod update <Pod>` (never a
   bare `pod update`). If the version is not on trunk, stop and report the SwiftPM migration as a follow-up. Rebuild every scheme in `CLAUDE.md`, plus one Release build
   (`xcodebuild build -configuration Release -destination 'generic/platform=iOS' CODE_SIGNING_ALLOWED=NO`) for toolchain
   or deployment-target axes. Run the tests that passed at baseline. Diff the lock files against the baseline copies and
   list transitive changes. New or bumped SDKs on Apple's required-reason list must ship `PrivacyInfo.xcprivacy`.
6. **Runtime check** when an SDK with native code or a swizzling/analytics SDK changed: `/ios-kit:run-app`, launch plus one
   authenticated screen. The `ios-verifier` agent runs the baseline tests and the smoke check and returns the evidence.
7. **Review.** `ios-reviewer`. Confirm each Blocker and Major against the code first, and decline a refuted one with the counter-evidence. Fix the rest, then re-run the compile check and the affected tests. Send the same reviewer the finding IDs and their "Verified fixed when" criteria to re-review the fix delta. Stop after two re-review rounds and report anything still open.
8. **Commit, only if asked.** Follow the shared Git conventions. Do not push unless asked.
9. **Report** table: item, old, new, build result, test result, notable transitive changes, follow-ups.
