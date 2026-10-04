---
name: google-play-release
description: Prepare, verify, and run Google Play releases for Android mobile apps. Use for Play Console, Android App Bundle, signing, fastlane Android lanes, testing tracks, production rollout, Data safety, target SDK policy, release notes, and Play review issue handling.
---

# Google Play Release

Use this skill when the user asks to prepare or execute an Android release, Google Play upload, internal testing release, production rollout, Data safety review, target SDK update, or Play policy issue response.

## Required source of truth

1. Inspect the repository before recommending commands.
2. If `android/fastlane/Fastfile` exists, read it and identify the actual lanes, parameters, build command, track behavior, signing assumptions, and upload behavior.
3. Treat Play policy deadlines, target SDK requirements, and Data safety requirements as time-sensitive. Read `references/official-sources.md` and verify current facts against official Google Play or Android documentation before final advice.
4. Never expose or copy real keystore passwords, service account JSON, package names, signing keys, webhook URLs, or production credentials into public artifacts.

## Workflow

1. Determine project type: Flutter, React Native, native Android, Kotlin Multiplatform, or another stack.
2. Determine release path: fastlane, Gradle, Play Console upload, CI pipeline, EAS, or another tool.
3. Read version sources, signing configuration, package/application ID, build flavor, and Play Console mapping.
4. Check release readiness:
   - `versionCode` increments and `versionName` matches release intent.
   - Release signing uses a real release keystore or Play App Signing flow; debug signing for release builds is a blocker.
   - AAB is preferred for Play production uploads unless the project has a valid APK-only reason.
   - Release notes are updated for supported locales.
   - Production environment flags are explicit.
   - Data safety answers match current app behavior and SDKs.
   - Permissions are justified by app features.
   - `android:usesCleartextTraffic` is disabled or explicitly justified by scoped network security configuration.
   - Target SDK and Play policy requirements are current.
   - App access instructions, demo account, content rating, ads declaration, financial features, health features, and user-generated content declarations are current when applicable.
5. Run the repository's expected verification before upload. For Flutter, prefer `dart format`, `flutter analyze`, relevant `flutter test`, and the existing build command.
6. Execute or provide the exact release command only after confirming it matches the repository's release tooling.
7. After upload, summarize artifact, version code, track, rollout percentage, review status, and any manual Play Console follow-up.

## Readiness checklist

Use this checklist in the final answer when the user asks for release readiness:

| Area | Status | Evidence | Action |
| --- | --- | --- | --- |
| Version code/name | Pass/Fail/Unknown | File or command | Required fix or none |
| Release signing | Pass/Fail/Unknown | Gradle/keystore/Play signing | Required fix or none |
| Play API access | Pass/Fail/Unknown | fastlane/CI/service account | Required fix or none |
| Build verification | Pass/Fail/Unknown | Command output | Required fix or none |
| Artifact | Pass/Fail/Unknown | AAB/APK path | Required fix or none |
| Release notes | Pass/Fail/Unknown | Locale files/Play Console | Required fix or none |
| Data safety/permissions | Pass/Fail/Unknown | manifest/dependencies/Play Console | Required fix or none |
| Cleartext/network security | Pass/Fail/Unknown | manifest/network security config | Required fix or none |
| Target SDK/policy | Pass/Fail/Unknown | Gradle/policy docs | Required fix or none |
| Track/rollout | Pass/Fail/Unknown | lane/manual state | Required fix or none |

`Unknown` is acceptable only when the information cannot be inspected locally or requires Play Console access. Do not mark an item as passed without evidence.

## fastlane adaptation

If fastlane exists, inspect the lanes instead of assuming names. Look for:

- Testing lanes: often `internal`, `alpha`, `beta`, or `closed`.
- Production lanes: often `production`, `release`, `deploy`, or `promote`.
- Actions: `gradle`, `upload_to_play_store`, `supply`.
- Parameters: track, rollout, release status, version code, flavor, skip upload metadata, skip upload images, skip upload screenshots.
- Metadata folders: `android/fastlane/metadata/android`.

See `references/fastlane.md` for fastlane-specific checks.
See `references/official-sources.md` for policy-sensitive Google Play source selection.
See `references/data-safety.md` for Data safety, permissions, release signing, and cleartext network checks.

If `android/fastlane/Fastfile` is absent, do not invent Play upload automation. Report a manual or CI release path, usually:

- Build an AAB with the repository's Android build command.
- Verify release signing and version code.
- Upload the AAB through Play Console or add a dedicated CI/fastlane release path.

## Output expectations

When reporting, include:

- Detected release path.
- Exact command or manual steps.
- Checks passed, checks not run, and why.
- Remaining Play Console manual tasks.
- Risks that could block review or production rollout.

For Play policy issues, lead with the likely policy or technical cause, then propose evidence, code/config changes, declaration changes, and appeal/reply text.
