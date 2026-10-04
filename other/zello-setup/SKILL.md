---
name: zello-setup
description: Install the Zello SDK, configure Android native build via Expo config plugins, set up Firebase FCM, and declare required permissions for EnforcementMAPS.
---

# Zello Setup

This skill covers everything needed to get the Zello SDK installed and building in the EnforcementMAPS Expo managed workflow.

## Prerequisites

Before starting, ensure:
- Zello Work subscription is active with a network created
- SDK credentials (`issuer` + `credentialKey`) obtained from Zello Work admin console
- Firebase project created for `au.melbourne.patrolzones` with FCM enabled

## Package Installation

Use pnpm (the project's package manager):

```bash
# Core SDK
pnpm add @zelloptt/react-native-zello-sdk

# Firebase (required for background PTT wake)
pnpm add @react-native-firebase/app @react-native-firebase/messaging

# Build properties (for Kotlin/Gradle config)
pnpm add expo-build-properties
```

### Peer Dependencies

The SDK requires `react` ≥ 18 and `react-native` ≥ 0.73 — both already satisfied by the project (React 19.1.0, RN 0.81.5).

### What NOT to Install

- `zello-android-client-sdk` — bundled inside the RN wrapper automatically
- Expo FCM notification plugins — Zello manages its own FCM channel

## Android Native Configuration

EnforcementMAPS uses Expo managed workflow. All native config goes through `app.config.ts` — never edit `android/` files directly.

### Plugins Array

Add to the existing `plugins` array in `app.config.ts`:

```typescript
plugins: [
  'expo-router',
  'expo-secure-store',
  ['expo-notifications', { defaultChannel: 'default' }],
  // ── Zello PTT ──────────────────────────────────────────
  '@react-native-firebase/app',
  ['expo-build-properties', {
    android: {
      kotlinVersion: '1.9.24',
      enableProguardInReleaseBuilds: true,
      packagingOptions: {
        pickFirst: ['**/kotlin/**'],
      },
    },
  }],
],
```

### Firebase google-services.json

Place at project root and reference in `app.config.ts`:

```typescript
android: {
  package: 'au.melbourne.patrolzones',
  googleServicesFile: './google-services.json',
  // ...existing config
},
```

Add `google-services.json` to `.gitignore` — credentials must not be committed.

### Zello Maven Repository

Handled automatically by the React Native SDK's autolinking. No manual Gradle changes needed in Expo managed workflow.

## Permissions

Update the `android.permissions` array in `app.config.ts`:

```typescript
android: {
  permissions: [
    // Existing
    'ACCESS_FINE_LOCATION',
    'ACCESS_COARSE_LOCATION',
    // Zello PTT
    'RECORD_AUDIO',
    'BLUETOOTH_CONNECT',
    'POST_NOTIFICATIONS',
    'FOREGROUND_SERVICE',
    'FOREGROUND_SERVICE_MICROPHONE',
  ],
},
```

| Permission | Purpose | Runtime Prompt? |
|------------|---------|----------------|
| RECORD_AUDIO | PTT voice capture | Yes (Android 6+) |
| BLUETOOTH_CONNECT | Hardware PTT button | Yes (Android 12+) |
| POST_NOTIFICATIONS | Foreground service notification | Yes (Android 13+) |
| FOREGROUND_SERVICE | Keep Zello alive in background | No (manifest only) |
| FOREGROUND_SERVICE_MICROPHONE | Mic access in foreground service | No (manifest only) |

### Runtime Permission Hook

Request on first PTT tap, not on app launch:

```typescript
// src/features/zello/hooks/useZelloPermissions.ts
import { PermissionsAndroid, Platform } from 'react-native';

export async function requestZelloPermissions(): Promise<boolean> {
  if (Platform.OS !== 'android') return true;
  const grants = await PermissionsAndroid.requestMultiple([
    PermissionsAndroid.PERMISSIONS.RECORD_AUDIO,
    PermissionsAndroid.PERMISSIONS.BLUETOOTH_CONNECT,
    PermissionsAndroid.PERMISSIONS.POST_NOTIFICATIONS,
  ]);
  return grants[PermissionsAndroid.PERMISSIONS.RECORD_AUDIO] === 'granted';
}
```

## Environment Variables

Add to `.env.example` and all `eas.json` build profiles:

```env
EXPO_PUBLIC_ZELLO_NETWORK_ISSUER=
EXPO_PUBLIC_ZELLO_CREDENTIAL_KEY=
```

## Build Verification

Create a dev build to verify native linking:

```bash
eas build --platform android --profile development
```

Watch for:
- ✅ `@zelloptt/react-native-zello-sdk` in autolinking output
- ✅ `@react-native-firebase/app` resolved
- ❌ Hilt/Dagger errors → see `zello-troubleshooting` skill

The Zello SDK **cannot** run in Expo Go — it requires an EAS dev build. See the `expo-dev-client` skill from `use-expo` for dev build workflow.

## Detailed Documentation

Full installation and config docs at `docs/dev/zello/`:
- `02-installation.md` — Package details
- `03-android-native-config.md` — Expo plugin config
- `04-permissions.md` — Permission details and timing
