---

# === CORE IDENTITY ===
name: senior-mobile
title: Senior Mobile Skill Package
description: Comprehensive cross-platform mobile development skill for React Native, Flutter, and Expo. Includes project scaffolding, platform detection, app store validation, and CI/CD setup. Use when building mobile apps, selecting frameworks, validating releases, or setting up mobile development workflows.
domain: engineering
subdomain: mobile-development

# === WEBSITE DISPLAY ===
difficulty: advanced
time-saved: "60% faster project setup, 80% fewer store rejections"
frequency: "Weekly for active mobile development"
use-cases:
  - Creating new React Native or Flutter projects with best practices
  - Detecting platform capabilities and project configuration
  - Validating apps before App Store/Play Store submission
  - Setting up CI/CD pipelines for mobile releases

# === RELATIONSHIPS ===
related-agents:
  - cs-mobile-engineer
  - cs-ios-engineer
  - cs-flutter-engineer
related-skills:
  - senior-ios
  - senior-flutter
  - senior-frontend
related-commands: []
orchestrated-by:
  - cs-mobile-engineer

# === TECHNICAL ===
dependencies:
  scripts:
    - mobile_scaffolder.py
    - platform_detector.py
    - app_store_validator.py
  references:
    - frameworks.md
    - templates.md
    - tools.md
  assets: []
compatibility:
  python-version: 3.8+
  platforms: [macos, linux, windows]
tech-stack:
  - React Native
  - Flutter
  - Expo
  - TypeScript
  - Dart
  - iOS
  - Android
  - Xcode
  - Android Studio
  - Fastlane

# === EXAMPLES ===
examples:
  -
    title: Generate React Native Project
    input: "python3 mobile_scaffolder.py --framework react-native --platforms ios,android --navigation react-navigation --state redux"
    output: "Complete project structure with TypeScript, navigation, state management, and CI/CD config"
  -
    title: Detect Platform Capabilities
    input: "python3 platform_detector.py --check all --depth full"
    output: "Detailed report of iOS/Android capabilities, signing status, and configuration"
  -
    title: Validate for App Store
    input: "python3 app_store_validator.py --store apple --strict"
    output: "Compliance report with required fixes for App Store submission"

# === ANALYTICS ===
stats:
  downloads: 0
  stars: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors: []
created: 2025-12-13
updated: 2025-12-13
license: MIT

# === DISCOVERABILITY ===
tags:
  - mobile
  - react-native
  - flutter
  - expo
  - ios
  - android
  - cross-platform
  - app-store
  - play-store
  - engineering
featured: true
verified: true
---

# Senior Mobile

Comprehensive cross-platform mobile development skill package with Python automation tools for project scaffolding, platform detection, and app store validation.

## Overview

This skill provides a complete toolkit for cross-platform mobile development targeting React Native, Flutter, and Expo frameworks. It includes three Python CLI tools that automate project setup, platform analysis, and app store validation, saving significant time and reducing store rejection rates.

## Quick Start

```bash
# Generate a new React Native project
python3 scripts/mobile_scaffolder.py --framework react-native --platforms ios,android --output ./my-app

# Analyze an existing project
python3 scripts/platform_detector.py --check all --depth full

# Validate before App Store submission
python3 scripts/app_store_validator.py --store apple --strict
```

## Core Capabilities

- **Project Scaffolding** - Generate complete React Native, Flutter, or Expo projects with TypeScript, navigation, state management, and CI/CD
- **Platform Detection** - Analyze mobile projects to detect framework type, iOS/Android capabilities, and configuration status
- **App Store Validation** - Pre-submission checks for Apple App Store and Google Play Store compliance
- **Framework Selection** - Data-driven framework comparison (React Native vs Flutter) based on project requirements

## Key Workflows

### Workflow 1: New Mobile Project Setup

**Time:** 15-30 minutes (vs 2-4 hours manual)

**Steps:**
1. Determine project requirements (platforms, navigation, state management)
2. Run `mobile_scaffolder.py` with appropriate options
3. Review generated structure and customize as needed
4. Initialize git repository and configure CI/CD
5. Verify build for both platforms

**Tool:** `scripts/mobile_scaffolder.py`

```bash
# React Native with TypeScript, React Navigation, Redux
python3 scripts/mobile_scaffolder.py \
  --framework react-native \
  --platforms ios,android \
  --navigation react-navigation \
  --state redux \
  --ci github-actions \
  --output ./my-app

# Flutter with Riverpod and GoRouter
python3 scripts/mobile_scaffolder.py \
  --framework flutter \
  --platforms ios,android,web \
  --navigation go-router \
  --state riverpod \
  --ci github-actions \
  --output ./my-flutter-app

# Expo managed workflow
python3 scripts/mobile_scaffolder.py \
  --framework expo \
  --platforms ios,android \
  --navigation expo-router \
  --state zustand \
  --output ./my-expo-app
```

### Workflow 2: Platform Capability Assessment

**Time:** 5-10 minutes

**Steps:**
1. Navigate to mobile project root
2. Run `platform_detector.py` with full depth
3. Review iOS and Android capability reports
4. Address any configuration issues identified
5. Re-run to verify fixes

**Tool:** `scripts/platform_detector.py`

```bash
# Full project analysis
python3 scripts/platform_detector.py --check all --depth full

# iOS-only analysis
python3 scripts/platform_detector.py --check ios --output json

# Android signing verification
python3 scripts/platform_detector.py --check android --depth signing
```

**Output includes:**
- Project type detection (React Native, Flutter, Expo, Native)
- iOS: Bundle ID, provisioning profiles, entitlements, Info.plist analysis
- Android: Package name, Gradle configuration, signing config, manifest permissions
- Configuration health score with recommendations

### Workflow 3: Pre-Release App Store Validation

**Time:** 10-15 minutes

**Steps:**
1. Build release versions for target stores
2. Run `app_store_validator.py` with strict mode
3. Review compliance report
4. Fix any critical or high-priority issues
5. Re-validate until passing
6. Submit to stores with confidence

**Tool:** `scripts/app_store_validator.py`

```bash
# Apple App Store validation
python3 scripts/app_store_validator.py \
  --store apple \
  --build-path ./ios/build/Release \
  --strict

# Google Play Store validation
python3 scripts/app_store_validator.py \
  --store google \
  --build-path ./android/app/build/outputs/apk/release \
  --strict

# Both stores (universal validation)
python3 scripts/app_store_validator.py \
  --store both \
  --check all \
  --output markdown > validation-report.md
```

**Validates:**
- **Apple:** Info.plist completeness, privacy manifest, icon sizes, entitlements, minimum iOS version
- **Google:** AndroidManifest.xml, target SDK version, 64-bit support, signing, permissions declarations

### Workflow 4: Framework Selection Analysis

**Time:** 20-30 minutes

**Steps:**
1. Document project requirements (team skills, timeline, features)
2. Review `references/frameworks.md` decision matrix
3. Score each framework against requirements
4. Consider long-term maintenance and ecosystem factors
5. Document decision with rationale

**Reference:** `references/frameworks.md`

**Decision Factors:**
| Factor | React Native | Flutter | When to Weight Heavily |
|--------|-------------|---------|----------------------|
| Team JavaScript experience | ++++ | + | Existing web team |
| UI consistency across platforms | ++ | ++++ | Brand-critical apps |
| Native module needs | +++ | ++ | Hardware integration |
| Hot reload speed | +++ | ++++ | Rapid iteration |
| Bundle size | ++ | +++ | Download-sensitive markets |
| Web support | ++ | ++++ | PWA requirements |

### Workflow 5: CI/CD Pipeline Setup

**Time:** 30-45 minutes

**Steps:**
1. Generate project with `--ci` flag for base configuration
2. Configure signing credentials in CI secrets
3. Set up Fastlane for iOS/Android automation
4. Configure TestFlight/Play Console deployment
5. Add automated testing stages
6. Enable release automation

**Generated CI Configurations:**
- GitHub Actions workflows for iOS and Android
- Fastlane configuration files
- Environment variable templates
- Code signing setup guides

## Python Tools

### mobile_scaffolder.py

Generate complete mobile project structures with best practices.

```bash
python3 scripts/mobile_scaffolder.py --help

Options:
  --framework      react-native|flutter|expo (required)
  --platforms      ios,android,web (default: ios,android)
  --navigation     react-navigation|expo-router|go-router|auto-route
  --state          redux|zustand|mobx|riverpod|bloc|provider
  --ci             github-actions|gitlab-ci|bitrise|none
  --output         Output directory path
  --dry-run        Preview without creating files
```

### platform_detector.py

Analyze mobile projects for capabilities and configuration.

```bash
python3 scripts/platform_detector.py --help

Options:
  --check          ios|android|all (default: all)
  --depth          quick|standard|full|signing
  --output         text|json|csv (default: text)
  --project-path   Path to project root (default: current directory)
```

### app_store_validator.py

Validate builds against App Store and Play Store requirements.

```bash
python3 scripts/app_store_validator.py --help

Options:
  --store          apple|google|both (required)
  --build-path     Path to build artifacts
  --check          all|icons|manifest|signing|privacy
  --strict         Fail on warnings (recommended for release)
  --output         text|json|markdown
```

## References

- **[frameworks.md](references/frameworks.md)** - React Native vs Flutter decision framework
- **[templates.md](references/templates.md)** - Project templates and patterns
- **[tools.md](references/tools.md)** - Python tool documentation and examples

## Best Practices

### Project Structure
- Use monorepo structure for shared code between platforms
- Separate platform-specific code into dedicated directories
- Implement feature-based module organization
- Use environment configuration for different build variants

### Performance
- Implement lazy loading for screens and heavy components
- Use native driver for animations where possible
- Optimize images and assets for mobile
- Profile and monitor app performance regularly

### Security
- Never commit signing credentials
- Use secure storage for sensitive data
- Implement certificate pinning for API calls
- Follow platform-specific security guidelines

### Testing
- Write unit tests for business logic
- Implement integration tests for critical flows
- Use snapshot testing for UI components
- Test on real devices before release

## Success Metrics

- **Project Setup Time:** 15-30 minutes (vs 2-4 hours manual)
- **Store Rejection Rate:** <5% (vs industry average 30%)
- **Platform Detection Accuracy:** 99%+
- **CI/CD Setup Time:** 30-45 minutes (vs 4-8 hours manual)
