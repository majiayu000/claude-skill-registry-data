---
name: expo-modules
description: Guide for authoring and developing Expo modules using the Expo Modules API.
---

# Developing Expo Modules

This skill helps you create and develop expo-modules for React Native app to call native iOS code.

## When to use this skill

Use this skill when you need to:
- Create or modify Expo modules for React Native applications.
- Interface with native iOS code using the Expo Modules API.

## Creating a new Expo module

This only needs to be done once per module.

1. Run `bunx create-expo-module@latest --local` to scaffold a new local Expo module.
2. Follow the prompts to set up your module.

## Developing

1. Navigate to your module directory, likely `./modules/<your-module-name>`.
2. Make code changes to the .ts and .swift files as needed.

## Building and testing

Each time you make changes to the native code, you need to rebuild the native bundle and run the app.

```
bunx expo run:ios \
  --device "Kevin's iPhone" \
  --scheme tindeqtrackerdev
```

## Further reading

[Module API Reference](https://docs.expo.dev/modules/module-api/)
