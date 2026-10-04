---
name: ci-cd
description: Set up CI/CD pipelines with GitHub Actions and Fastlane for Flutter apps. Automates testing, building, and deployment to Firebase App Distribution, TestFlight, and Play Store. Use when setting up automated workflows or preparing for release.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# CI/CD - Automated Build & Deploy

Set up robust CI/CD pipelines for Flutter apps using GitHub Actions and Fastlane. Automates the entire flow from code push to app store deployment.

## When to Use This Skill

- Setting up CI/CD for a new Flutter project
- Adding automated testing to pull requests
- Configuring deployment to Firebase App Distribution
- Setting up TestFlight (iOS) or Play Store (Android) releases
- Implementing semantic versioning automation
- Optimizing build times with caching

## Architecture Overview

**GitHub Actions Pipeline:** CI (on PR: analyze, test) → Build (on merge: APK/IPA) → Deploy (on tag: stores)

**Fastlane:** iOS (match → build → TestFlight) | Android (gradle → Play Store)

## Quick Reference

### Workflow Types

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **ci.yml** | PR, push | Lint, test, analyze |
| **build-android.yml** | Push to main | Build APK/AAB artifacts |
| **build-ios.yml** | Push to main | Build iOS (no codesign) |
| **deploy-firebase-android.yml** | Beta/alpha tags | Firebase App Distribution (Android) |
| **deploy-firebase-ios.yml** | Beta/alpha tags | Firebase App Distribution (iOS) |
| **deploy-testflight.yml** | Release tags | TestFlight |
| **deploy-playstore.yml** | Release tags | Play Store |
| **release.yml** | Manual | Bump version, create tag |

### Quick Start

```bash
# Interactive setup - creates config file, then generates all CI/CD files
dart run .claude/skills/ci-cd/scripts/setup.dart
```

This will:
1. Create `ci-cd-config.yaml` with all options
2. Open it for you to fill in your values
3. Run again to generate all workflows and Fastlane files

### Other Commands

```bash
dart run .claude/skills/ci-cd/scripts/check.dart       # Validate setup
cd ios && bundle exec fastlane beta                    # Fastlane iOS
cd android && bundle exec fastlane beta                # Fastlane Android
./scripts/bump_version.sh patch                        # Bump version
```

## Workflow

### 1. Prerequisites Check

Before setting up CI/CD, ensure project builds and tests pass:

```bash
flutter build apk --debug && flutter build ios --debug --no-codesign
flutter test && flutter analyze
```

### 2. Create Workflow Files

```bash
mkdir -p .github/workflows
```

Create workflows in order:
1. **ci.yml** - Basic PR checks (required for all projects)
2. **build.yml** - Build artifacts (if deploying)
3. **deploy-firebase.yml** - Firebase App Distribution (for testers)
4. **deploy-ios.yml** / **deploy-android.yml** - Store deployment

See [workflows-guide.md](workflows-guide.md) for templates.

### 3. Configure Secrets

Add to GitHub repository Settings → Secrets and variables → Actions:

| Secret | Purpose | Required For |
|--------|---------|--------------|
| `FIREBASE_SERVICE_ACCOUNT` | Firebase deployment | Firebase App Dist |
| `FIREBASE_APP_ID_ANDROID` | Android App ID | Firebase App Dist |
| `FIREBASE_APP_ID_IOS` | iOS App ID | Firebase App Dist |
| `MATCH_PASSWORD` | Fastlane match encryption | iOS signing |
| `MATCH_GIT_BASIC_AUTHORIZATION` | Match repo access | iOS signing |
| `APP_STORE_CONNECT_API_KEY` | App Store Connect | TestFlight |
| `APP_STORE_CONNECT_ISSUER_ID` | API Key Issuer | TestFlight |
| `APP_STORE_CONNECT_KEY_ID` | API Key ID | TestFlight |
| `GOOGLE_SERVICE_ACCOUNT_KEY` | Play Store access | Play Store |

### 4. Set Up Fastlane (Optional)

```bash
gem install fastlane && cd ios && fastlane init  # iOS
cd android && fastlane init                       # Android
```

See [fastlane-guide.md](fastlane-guide.md) and [versioning-guide.md](versioning-guide.md) for configuration.

## Checklist

**GitHub Actions:**
- [ ] `.github/workflows/ci.yml` exists
- [ ] Workflow uses `subosito/flutter-action` with caching
- [ ] Secrets configured in repository settings
- [ ] Branch protection requires CI to pass

**Fastlane (if deploying):**
- [ ] `ios/fastlane/Fastfile` configured
- [ ] `android/fastlane/Fastfile` configured
- [ ] Match set up for iOS signing
- [ ] Service accounts configured

**Versioning:**
- [ ] Version bump script exists
- [ ] Changelog pattern documented
- [ ] Tag triggers deployment

## Caching Strategy

Proper caching reduces build times by 30-50%:

| What to Cache | Key Pattern | Restore Key |
|---------------|-------------|-------------|
| Flutter SDK | `flutter-${{ runner.os }}-${{ inputs.flutter-version }}` | `flutter-${{ runner.os }}-` |
| Pub cache | `pub-${{ runner.os }}-${{ hashFiles('**/pubspec.lock') }}` | `pub-${{ runner.os }}-` |
| build_runner | `build-runner-${{ hashFiles('**/pubspec.lock') }}` | `build-runner-` |
| Gradle | `gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}` | `gradle-` |
| CocoaPods | `pods-${{ hashFiles('**/Podfile.lock') }}` | `pods-` |

## Security Best Practices

1. **Never commit secrets** - Use GitHub Secrets or environment variables
2. **Restrict workflow permissions** - Use `permissions:` block
3. **Pin action versions** - Use SHA or exact versions, not `@main`
4. **Use OIDC** - For cloud providers (Firebase, GCP) when possible
5. **Limit deployment branches** - Only deploy from protected branches

## Templates

Ready-to-use files in `templates/`: bump_version scripts, workflows/*.yml (ci, build, deploy), fastlane/{ios,android}/ (Fastfile, Appfile, Gemfile).

> **Note:** Template Fastfiles include advanced lanes. The setup script creates minimal files.

```bash
# Copy templates manually (or use setup.dart)
mkdir -p .github/workflows ios/fastlane android/fastlane
cp .claude/skills/ci-cd/templates/workflows/*.yml .github/workflows/
cp .claude/skills/ci-cd/templates/fastlane/ios/* ios/fastlane/
```

## Guides

| Guide | Use For |
|-------|---------|
| [workflows-guide.md](workflows-guide.md) | GitHub Actions concepts & customization |
| [fastlane-guide.md](fastlane-guide.md) | iOS/Android deployment setup |
| [versioning-guide.md](versioning-guide.md) | Semantic versioning patterns |
| [debug-symbols-guide.md](debug-symbols-guide.md) | dSYM/mapping upload for crash reporting |

## Related Skills

- `/release` - Manual release preparation (signing, icons, store setup) - do this first
- `/analytics` - Crash reporting setup, provides upload scripts
- `/testing` - Ensure tests pass before deployment

## Sources

Based on: [Flutter CI/CD with GitHub Actions](https://medium.com/@akashvyasce/automate-your-flutter-builds-with-ci-cd-using-github-actions-55a7790c3f74), [Fastlane Flutter Docs](https://docs.fastlane.tools/getting-started/cross-platform/flutter/), [Flutter Official CD Guide](https://docs.flutter.dev/deployment/cd)
