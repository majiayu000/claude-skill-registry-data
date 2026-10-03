---
name: prep-release
description: Pre-release audit for a React Native app. Use when the user is about to submit to the App Store or Play Store, cut a release, or asks for a release checklist run.
argument-hint: "[ios|android|both]"
disable-model-invocation: true
---

Run a pre-release audit for `$ARGUMENTS` (default: both platforms). Verify in the actual project files; never assume. Output a pass/fail table with evidence, so the user can fix failures and rerun.

Check, with the eas-release skill as the rulebook:

1. **Versioning**: user-facing version bumped since the last release tag; build numbers set to auto-increment or manually bumped; git tag plan stated.
2. **OTA fence**: runtime version policy present; if any native dependency or config plugin changed since the last store build, flag that this release MUST be a store build and OTA publishing to old channels is forbidden until it ships.
3. **Permissions honesty**: cross-check declared permissions and usage strings (Info.plist keys, Android permissions) against what the code actually imports. Camera/mic/location/notification strings present where used, and no leftover permissions from removed features, which reviewers flag.
4. **Secrets scan**: grep the source and app config for things that must not ship: private API keys, service-role or server keys, live payment secrets, hardcoded backend admin URLs. Public/publishable keys are fine; call out anything ambiguous.
5. **Store hygiene**: account deletion path exists if accounts exist; restore purchases reachable if IAP exists; sign-in options meet platform rules; privacy labels and data safety answers match the SDK list (list the SDKs that collect data so the user can compare).
6. **Config sanity**: production build profile points at production backend; no debug flags, staging URLs or test paywalls behind release config; app icon and splash present for both platforms.
7. **Quality gates**: typecheck, lint and tests pass; if there is a preview/QA build lane, confirm the release candidate went through it.
8. **Android native alignment**: when a build artifact is at hand, verify 16 KB page alignment of native libraries (`zipalign -c -P 16 -v 4` on an APK built from the bundle); Play rejects unaligned `.so` files for apps targeting Android 15+. Without an artifact, list native dependencies whose last release predates the requirement as warnings.

Rules of engagement: read-only plus running the project's own check commands. Findings come back as blocker vs warning, each with file evidence. End with a plain verdict: ready to submit, or the ordered list of what blocks it.
