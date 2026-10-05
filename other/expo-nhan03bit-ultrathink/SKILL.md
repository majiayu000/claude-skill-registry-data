---
name: expo
description: Expo framework for universal React Native apps — routing, SDK modules, EAS builds, OTA updates, and config plugins
layer: domain
category: mobile
triggers:
  - "expo"
  - "expo router"
  - "eas build"
  - "eas update"
  - "expo config plugin"
  - "expo go"
  - "app.config.ts"
  - "expo modules"
inputs:
  - requirements: Target platforms (iOS, Android, Web), features, SDK modules needed
  - workflow: Expo Go | Development build | EAS Build
outputs:
  - project_config: app.config.ts and EAS configuration
  - routing: File-based navigation with Expo Router
  - native_modules: SDK module integration and config plugins
linksTo:
  - react-native
  - react
  - typescript-frontend
  - vercel
linkedFrom:
  - react-native
  - cook
  - plan
riskLevel: low
---

# Expo

Framework and platform for building universal React Native applications targeting iOS, Android, and web from a single codebase with managed native tooling.

## When to Use

- Building a new mobile or universal app with React Native
- Need file-based routing (Expo Router)
- Want managed native builds without Xcode/Android Studio (EAS Build)
- Need OTA updates without app store resubmission
- Integrating native device APIs (Camera, FileSystem, Notifications, etc.)
- Creating custom native modules with the Expo Modules API

## Key Patterns

- **Expo Router**: File-based routing in `app/` directory — layouts, groups, dynamic routes, typed routes
- **Expo SDK Modules**: Curated native APIs — Camera, FileSystem, Notifications, SecureStore, Haptics, Location
- **EAS Build**: Cloud-native iOS/Android builds; `eas build --platform all`
- **EAS Submit**: Automated App Store and Google Play submission; `eas submit`
- **Config Plugins**: Modify native projects declaratively via `app.config.ts` plugins array
- **Development Builds vs Expo Go**: Dev builds include custom native code; Expo Go for SDK-only prototyping
- **EAS Update**: OTA JS/asset updates without store review; branch-based deployment channels
- **Expo Modules API**: Write custom native modules in Swift/Kotlin with typed bridge
- **app.config.ts**: Dynamic configuration with environment variables, build profiles, and plugin composition
- **Universal Apps**: Single codebase for iOS, Android, and web with platform-specific overrides via `.ios.tsx`/`.android.tsx`/`.web.tsx`

## Anti-Patterns

| Anti-Pattern | Why | Instead |
|---|---|---|
| Ejecting prematurely | Loses managed workflow benefits | Use config plugins or dev builds first |
| Using Expo Go for production testing | Missing custom native modules | Use development builds (`npx expo run:ios`) |
| Hardcoding env values in app.json | Leaks secrets, no per-environment config | Use `app.config.ts` with `process.env` |
| Skipping EAS Update channels | Pushes untested updates to production | Use branch-based channels (preview, production) |
| AsyncStorage for secrets | Unencrypted on device | Use `expo-secure-store` |
| Ignoring `expo-dev-client` | Slow iteration with full EAS builds | Install dev client for local native testing |

## Related Skills

`react-native` `react` `typescript-frontend` `vercel`
