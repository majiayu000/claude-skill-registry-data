---
name: deploy
description: Execute the complete TestFlight deployment workflow for this Flutter iOS app. Use when the user asks to deploy, release, publish, or upload the app to TestFlight, or says things like "deploy to testflight", "release a new build", "push to beta testers", or "upload to app store connect".
---

# Deploy to TestFlight

Deploy this Flutter app to TestFlight using Fastlane.

## Workflow

### 1. Code Quality Check

```bash
flutter analyze
```

Stop if errors are found. Warnings are acceptable.

### 2. Version Check

Read current version from `pubspec.yaml`. Ask user:
- Bump version? If yes, update `pubspec.yaml`
- Update What's New dialog? If yes, edit `lib/dialogs/whats_new_dialog.dart`

### 3. Build

```bash
flutter build ipa --release
```

Verify IPA created at `build/ios/ipa/myapp.ipa`.

### 4. Generate Changelog

Generate changelog from commits since last tag:

```bash
# Get commits since last tag (or all commits if no tags)
git log $(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)..HEAD --oneline
```

Present the commits to the user and ask them to confirm or edit the changelog text for TestFlight.

### 5. Deploy

```bash
cd ios && fastlane beta_with_changelog changelog:"<user-confirmed changelog>"
```

### 6. Commit Changes

After successful upload, commit the version bump and What's New dialog changes:

```bash
git add pubspec.yaml lib/dialogs/whats_new_dialog.dart
git commit -m "chore: bump version to <version> and update What's New dialog"
git push origin main
```

### 7. Tag Release

Create a git tag for this release:

```bash
git tag -a v<version> -m "Release <version>"
git push origin v<version>
```

### 8. Confirm

Report success with:
- Version deployed
- Tag created
- Changelog used
- Note: Build available in TestFlight after Apple processing (~10-30 min)

## Fastlane Setup

Located in `ios/fastlane/`:
- `Appfile` - Bundle identifier
- `Fastfile` - Deployment lanes (`beta`, `beta_with_changelog`)
- `AuthKey_*.p8` - App Store Connect API key (gitignored)

## Quick Deploy (No Prompts)

For rapid deployment without version/changelog prompts:

```bash
flutter build ipa --release && cd ios && fastlane beta
```
