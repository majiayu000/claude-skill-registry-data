---
name: use-expo
description: Official Expo skills for building, deploying, upgrading, and debugging Expo and React Native apps. Activates the Expo skills orchestrator which routes to the appropriate sub-skills based on context.
version: 1.0.0
license: MIT
---

# Expo Skills

You now have access to the full suite of official Expo skills. Read `./expo-skills-orchestrator.md` to determine which sub-skills apply to the current task, then load and apply them accordingly.

## Quick Reference

| Goal | Skill |
|------|-------|
| Build UI, navigation, animations, components | building-native-ui |
| Fetch data, caching, offline, React Query | native-data-fetching |
| Upgrade SDK, migrate deprecated packages | upgrading-expo |
| Set up Tailwind CSS / NativeWind | expo-tailwind-setup |
| Create dev builds, distribute via TestFlight | expo-dev-client |
| Deploy to App Store, Play Store, EAS Hosting | expo-deployment |
| Add API routes in Expo Router | expo-api-routes |
| Write EAS CI/CD workflow YAML | expo-cicd-workflows |
| SwiftUI native components | expo-ui-swift-ui |
| Jetpack Compose native components | expo-ui-jetpack-compose |
| Run web code natively (DOM components) | use-dom |

All skill files are located at `./plugins/expo/skills/<skill-name>/SKILL.md`.

Consult `./expo-skills-orchestrator.md` for routing rules and multi-skill combinations.
