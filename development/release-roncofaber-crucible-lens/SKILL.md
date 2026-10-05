---
name: release
description: Cut, build, sign, tag, or publish a Crucible Lens release. Use only when explicitly asked to release, ship, publish, tag, bump the version, or produce signed release artifacts. Follow the ordered safeguards without improvising.
---

# Release Crucible Lens

Follow every step in order. Stop if version, changelog, build, generated configuration, or signature verification fails.

## 1. Version and changelog

Update both values in `gradle.properties`, the single source of truth:

```properties
app.versionName=X.Y.Z
app.versionCode=N
```

Review and promote the current changelog content:

1. Read the complete `Unreleased` section and consolidate entries that describe the same user-visible workflow or outcome. Remove implementation-only entries and avoid repeating an outcome across `Added`, `Changed`, and `Fixed`.
2. Preserve explicit entries for security, privacy, compatibility, migration, access-control, and breaking changes. Aim for roughly 5 to 15 meaningful bullets unless the release genuinely contains more distinct user-facing changes.
3. Rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD`.
4. Add a one- or two-sentence summary paragraph before its `###` subsections. CI requires this paragraph for release notes.
5. Add a new empty `## [Unreleased]` section above the release.

Do not reconstruct missing entries from git history during release. User-visible entries belong in the changelog when their changes land.

## 2. Build and verify artifacts

Run:

```bash
./scripts/release.sh
```

The script performs Android compilation, host tests, iOS Kotlin compilation, debug APK construction, release AAB and APK construction, generated `AppBuildConfig` verification, signature verification, and artifact copying.

Keep debug and release builds in separate Gradle invocations. `generateAppBuildConfig` derives `DEBUG` from requested task names while the shared Android compilation is not variant-split, so a combined invocation can put debug configuration into release artifacts.

Release signing comes from `KEYSTORE_PATH`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, and `KEY_PASSWORD`, with non-secret path and alias fallbacks in gitignored `local.properties`. The script prompts for missing passwords. Never commit a keystore or credential.

The script does not edit versions or the changelog, commit, tag, or push.

## 3. Inspect verification

Confirm the script reports `DEBUG = false` for the release configuration and verifies both the APK signature and the AAB signing entry. A successful Gradle build alone is insufficient because an absent signing configuration can produce an unsigned artifact.

## 4. Publish

Commit the version and changelog, push the commit, create the version tag printed by the script, then push the tag. The tag-triggered workflow creates a draft GitHub release and uses the version summary paragraph as its notes.

## Ad hoc debug build

An ad hoc test build is not a release:

```bash
./gradlew :androidApp:assembleDebug
```

Copy it under the fixed development name `crucible-lens-dev-debug.apk`. Reserve versioned artifact names for tagged releases.
