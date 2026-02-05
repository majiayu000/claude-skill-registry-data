---
name: eas-ios-simulator-builds
description: Create and use iOS simulator development builds with EAS for Expo/React Native apps. Use when setting up simulator-only profiles, building, installing, and running dev clients on iOS simulators.
license: MIT
metadata:
  author: amannhimself.dev
---

# EAS iOS Simulator Builds

## Overview

How to set up and run iOS simulator development builds with EAS (no Apple credentials required). Focused on creating simulator-only profiles, building, installing, and running the Expo dev client on iOS simulators.

## Quick start

- Prereqs: macOS with Xcode + Command Line Tools installed; EAS CLI installed; iOS Simulator available.
- Install `expo-dev-client` if not present: `bunx expo install expo-dev-client`.
- Use the simulator profile when building: `bunx eas build --profile ios-sim --platform ios`.
- Install/run after build: download the `.tar.gz`, extract the `.app`, then `xcrun simctl install booted path/to.app` and `xcrun simctl launch booted host.exp.Exponent` (or the app bundle ID).

## Profile setup (eas.json)

Add a simulator-only profile (no signing):

```jsonc
{
  "build": {
    "ios-sim": {
      "extends": "development",
      "ios": {
        "simulator": true
      }
    }
  }
}
```

Notes:

- `simulator: true` ensures a simulator build (no Apple account/signing).
- Keep bundle identifiers consistent with your app config; OTA/runtimeVersion rules still apply.

## Build & install

1. Build: `bunx eas build --profile ios-sim --platform ios`
   - This produces a `.tar.gz` containing the `.app` bundle.
2. Extract: `tar -xzf <downloaded>.tar.gz`
3. Install on a booted simulator: `xcrun simctl install booted <path/to>.app`
4. Launch: `xcrun simctl launch booted <bundleIdentifier>` (check your `app.config.ts`/`app.json` for the identifier).

## Run with your app

- Start the Metro server: `bunx expo start` (or with your APP_VARIANT env if applicable).
- Open the installed dev client in Simulator and scan the QR or use the Metro URL to load the app.

## Troubleshooting

- If the simulator isn’t booted, start one from Xcode or `xcrun simctl boot "iPhone 15"` before install.
- If the app won’t launch, verify the bundle identifier matches the installed app (`simctl get_app_container booted <bundleIdentifier>`).
- Clear cache if loading issues: `bunx expo start -c`.
- If you accidentally build a device build, ensure `simulator: true` is set in the profile you’re using.
