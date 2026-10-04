---
name: release
description: Prepare Flutter apps for App Store and Play Store release. Use when setting up Android signing, iOS certificates, app icons, splash screens, or preparing for production deployment. Covers keystore creation, Xcode signing, store setup, and release builds.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Release - App Store & Play Store Preparation

Prepare Flutter apps for production release. Handles signing, icons, splash screens, and store setup.

## When to Use This Skill

- Setting up Android signing (keystore, key.properties)
- Configuring iOS signing (certificates, provisioning profiles)
- Creating app icons for iOS and Android
- Setting up splash screens
- Preparing for App Store Connect or Google Play Console
- Verifying release readiness
- Building release APK/AAB/IPA

## Manual vs CI/CD Release

| Approach | Use When | Signing |
|----------|----------|---------|
| **Manual** (this skill) | First release, small team | Local keystore, Xcode |
| **CI/CD** (`/ci-cd`) | Regular releases, teams | GitHub Secrets, Fastlane |

> **Recommendation:** Start with manual release. Set up CI/CD when you need automation.

## Quick Reference

### Platform Requirements

| Platform | Signing | Store | Build Command |
|----------|---------|-------|---------------|
| **Android** | Keystore + key.properties | Play Console | `flutter build appbundle --release` |
| **iOS** | Xcode Team + Provisioning | App Store Connect | `flutter build ipa --release` |

### Commands

```bash
# Audit release readiness
dart run .claude/skills/release/scripts/check.dart

# Build release
flutter build appbundle --release  # Android
flutter build ipa --release        # iOS
```

| check.dart Option | Purpose |
|-------------------|---------|
| `--platform android/ios` | Audit specific platform only |
| `--fix` | Auto-fix .gitignore patterns |
| `--checklist` | Generate markdown checklist |
| `--capabilities` | Detect required iOS capabilities |
| `--keytool-command` | Generate keystore creation command |

## Workflow

### 1. Audit Current State

```bash
dart run .claude/skills/release/scripts/check.dart
```

Identifies: Missing keystore, unsigned iOS, missing icons, uncommitted .env files.

### 2. Create Assets

See [assets-guide.md](assets-guide.md):
- App icon: 1024x1024 PNG (no transparency for iOS)
- Splash screen: Configure flutter_native_splash

### 3. Configure Android Signing

See [android-guide.md](android-guide.md):
1. Generate keystore
2. Create key.properties (DO NOT COMMIT)
3. Update build.gradle.kts
4. Create proguard-rules.pro

### 4. Configure iOS Signing

See [ios-guide.md](ios-guide.md):
1. Open Xcode
2. Select Team
3. Configure capabilities
4. Create App ID on Apple Developer

### 5. Store Setup

See platform guides:
- [android-guide.md](android-guide.md) - Play Console setup
- [ios-guide.md](ios-guide.md) - App Store Connect setup

### 6. Build & Test Release

```bash
# Android
flutter build appbundle --release

# iOS
flutter build ipa --release
```

### 7. Final Verification

See [checklist.md](checklist.md) for comprehensive pre-release checklist.

## File Structure

After release preparation:

```
android/key.properties          # Signing config (DO NOT COMMIT)
android/app/build.gradle.kts    # With signing config
android/app/proguard-rules.pro  # R8 rules
ios/Runner.xcworkspace          # With signing configured
assets/icons/app_icon.png       # 1024x1024 source icon
pubspec.yaml                    # flutter_native_splash config
.gitignore                      # Must include key.properties, *.jks
```

## Security Checklist

Critical files that must NEVER be committed:

| File | Contains | Gitignore Pattern |
|------|----------|-------------------|
| `key.properties` | Keystore passwords | `android/key.properties` |
| `*.jks` / `*.keystore` | Signing keys | `*.jks` / `*.keystore` |
| `.env` | API keys, secrets | `.env` / `.env.*` |
| `*.p8` | Apple private keys | `*.p8` |
| `google-services.json` | Firebase config (optional) | Varies |

## Checklist

**Assets:**
- [ ] App icon 1024x1024 PNG (no transparency for iOS)
- [ ] Splash screen configured
- [ ] Screenshots for store listing

**Android:**
- [ ] Keystore created and backed up securely
- [ ] key.properties configured (not committed)
- [ ] build.gradle.kts has signing config
- [ ] proguard-rules.pro created
- [ ] `flutter build appbundle --release` succeeds

**iOS:**
- [ ] Xcode Team selected
- [ ] App ID created on Apple Developer
- [ ] Provisioning profile configured
- [ ] `flutter build ipa --release` succeeds

**Store:**
- [ ] App Store Connect app created
- [ ] Play Console app created
- [ ] Privacy policy URL ready
- [ ] Store listing content prepared

**Security:**
- [ ] .gitignore has all sensitive files
- [ ] No secrets committed to repository
- [ ] Keystore backed up to secure location

## Guides

| Guide | Use For |
|-------|---------|
| [android-guide.md](android-guide.md) | Keystore, signing, Play Store, Data Safety |
| [ios-guide.md](ios-guide.md) | Xcode signing, Privacy Manifest, ATT, App Store |
| [assets-guide.md](assets-guide.md) | App icons (incl. themed), splash screens |
| [version-guide.md](version-guide.md) | Version format, store requirements |
| [checklist.md](checklist.md) | Comprehensive pre-release checklist |

## Templates

Ready-to-use files in `templates/`:

| Template | Purpose |
|----------|---------|
| `PrivacyInfo.xcprivacy` | iOS Privacy Manifest (iOS 17+) |
| `proguard-rules.pro` | Android R8/ProGuard rules |

## Related Skills

- `/ci-cd` - Automated builds and deployment pipelines
- `/testing` - Ensure tests pass before release
- `/a11y` - Accessibility compliance for store approval

## Common Issues

| Issue | Solution |
|-------|----------|
| "Keystore was tampered with" | Verify password in key.properties |
| "No signing certificate" | Xcode > Preferences > Accounts > refresh |
| ProGuard errors | Add keep rules to proguard-rules.pro |
| Icons don't update | Run `flutter clean` then rebuild |
