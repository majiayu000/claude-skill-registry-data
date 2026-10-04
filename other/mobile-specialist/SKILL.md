---
name: mobile-specialist
description: iOS, Android, React Native, and Flutter mobile app development. Use when
  asked to build a mobile screen or component, implement native device features (camera,
  GPS, push notifications, biometrics), fix a React Native or Flutter issue, set up
  mobile CI/CD, optimize mobile app performance, or handle platform-specific behavior
  differences.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: development
  tags:
  - mobile
  - react-native
  - flutter
  - ios
  - android
  - expo
---

# Mobile Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `React Native`, `Flutter`, `mobile app`.
- The requested work fits this skill's lane: Mobile screens/components, native device features, React Native/Flutter issues, mobile CI/CD.
- The request needs this domain's specific workflow, checks, or deliverable shape rather than a neighboring specialist.

## First actions
1. `Glob('**/package.json', '**/pubspec.yaml', '**/android/app/build.gradle', '**/ios/Podfile')` — identify mobile framework
2. Confirm: React Native (bare/Expo), Flutter, native iOS (Swift), or native Android (Kotlin)
3. Identify target platforms: iOS only, Android only, or both

## Decision rules
- For cross-platform: React Native with Expo for most cases; Flutter for performance-critical or highly custom UI
- For native features: always check if an Expo module exists before writing native code
- Platform differences must be handled explicitly — no silent fallbacks

## Output contract
- Components follow platform-specific style conventions (iOS Human Interface Guidelines, Material Design for Android)
- TypeScript types included for React Native components
- Platform-specific code uses `Platform.OS` guards or `.ios.tsx` / `.android.tsx` file extensions

## Constraints
- NEVER ship secrets, API keys, or signing material inside application source or bundled assets.
- NEVER assume parity across iOS, Android, React Native, and Flutter without checking platform-specific behavior.
- Scope boundary: backend API design and cloud infrastructure changes belong to the relevant backend or cloud specialist.

## Reference
- `references/legacy-agent.md`: React Native patterns, Flutter widgets, native feature integration, mobile CI/CD
