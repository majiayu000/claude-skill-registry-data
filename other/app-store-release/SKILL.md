---
name: app-store-release
description: Prepare, verify, and run Apple App Store or TestFlight releases for mobile apps. Use for App Store Connect, TestFlight, iOS signing, fastlane iOS lanes, metadata, screenshots, privacy labels, review submission, phased release, and App Review rejection handling.
---

# App Store Release

Use this skill when the user asks to prepare or execute an iOS release, TestFlight upload, App Store submission, metadata update, privacy review, or rejection response.

## Required source of truth

1. Inspect the repository before recommending commands.
2. If `ios/fastlane/Fastfile` exists, read it and identify the actual lanes, parameters, build command, metadata behavior, signing assumptions, and upload behavior.
3. If the task involves Apple platform rules, APIs, signing, privacy, or App Review policy, read `references/official-sources.md` and verify current facts against official Apple documentation or the Apple developer docs MCP.
4. Never expose or copy real App Store Connect API keys, issuer IDs, team IDs, private key paths, webhook URLs, or production credentials into generated public artifacts.

## Workflow

1. Determine project type: Flutter, React Native, native iOS, Kotlin Multiplatform, or another stack.
2. Determine release path: fastlane, Xcode archive, CI pipeline, EAS, manual Transporter upload, or another tool.
3. Read version sources, signing configuration, build scheme, export method, bundle identifier, and App Store Connect app mapping.
4. Check release readiness:
   - Version and build number incremented.
   - Release notes updated for all supported locales.
   - Production environment flags are explicit.
   - Privacy labels and app privacy manifest (`PrivacyInfo.xcprivacy`) match current app behavior.
   - Permission purpose strings match actual feature usage.
   - Screenshots, app preview, subtitle, description, support URL, marketing URL, and review notes are current.
   - Sign in, subscriptions, in-app purchases, push notifications, location, background modes, HealthKit, maps, or user-generated content have matching review notes when applicable.
5. Run the repository's expected verification before upload. For Flutter, prefer `dart format`, `flutter analyze`, relevant `flutter test`, and the existing build command.
6. Execute or provide the exact release command only after confirming it matches the repository's release tooling.
7. After upload, summarize build number, destination, submission status, rollout mode, and any manual App Store Connect follow-up.

## Readiness checklist

Use this checklist in the final answer when the user asks for release readiness:

| Area | Status | Evidence | Action |
| --- | --- | --- | --- |
| Version/build | Pass/Fail/Unknown | File or command | Required fix or none |
| Signing/API access | Pass/Fail/Unknown | File or lane | Required fix or none |
| Build verification | Pass/Fail/Unknown | Command output | Required fix or none |
| Metadata/release notes | Pass/Fail/Unknown | Locale files/App Store Connect | Required fix or none |
| Privacy manifest | Pass/Fail/Unknown | `.xcprivacy` files/App Store Connect | Required fix or none |
| Privacy/permissions | Pass/Fail/Unknown | plist/entitlements/App Store Connect | Required fix or none |
| Screenshots/media | Pass/Fail/Unknown | fastlane/App Store Connect | Required fix or none |
| Review submission | Pass/Fail/Unknown | lane/manual state | Required fix or none |

`Unknown` is acceptable only when the information cannot be inspected locally or requires store-console access. Do not mark an item as passed without evidence.

## fastlane adaptation

If fastlane exists, inspect the lanes instead of assuming names. Look for:

- TestFlight lanes: often `beta`, `testflight`, `internal`, or `pilot`.
- App Store lanes: often `release`, `deploy`, `appstore`, or `submit`.
- Actions: `build_app`, `gym`, `upload_to_testflight`, `upload_to_app_store`, `deliver`, `pilot`, `precheck`.
- Parameters: environment, build number, version, submit for review, automatic release, phased release, skip metadata, skip screenshots.
- Metadata folders: `ios/fastlane/metadata`.
- Screenshot folders: `ios/fastlane/screenshots`.

See `references/fastlane.md` for fastlane-specific checks.
See `references/official-sources.md` for policy-sensitive Apple source selection.
See `references/privacy.md` for privacy labels, privacy manifests, permission strings, and App Review note checks.

Flag these as high-risk unless the user explicitly confirms they are intentional:

- `submit_for_review: true` or lane defaults that submit for review.
- `automatic_release: true` or lane defaults that release automatically after review.
- `skip_screenshots: true` when no separate screenshot upload or manual App Store Connect check is documented.
- Missing `precheck` when the lane uploads metadata or submits for review.

## Output expectations

When reporting, include:

- Detected release path.
- Exact command or manual steps.
- Checks passed, checks not run, and why.
- Remaining App Store Connect manual tasks.
- Risks that could block review.

For rejection handling, lead with the likely policy or technical cause, then propose evidence, code/config changes, and App Review reply text.
