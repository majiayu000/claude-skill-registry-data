---
name: zello-background
description: Configure Zello background services, FCM push alongside Expo Push Tokens, foreground service notifications, and battery optimisation for reliable PTT during extended patrols.
---

# Zello Background Services & Push

This skill covers how Zello stays alive in the background for reliable PTT during officer patrols, and how its FCM requirements coexist with the app's existing Expo Push system.

## Current Push Architecture

EnforcementMAPS uses **Expo Push Tokens** via `expo-notifications`:

```
Device → Expo Push Service → FCM → Device
```

`usePushNotifications.ts` registers an Expo Push Token on login and sends it to the MAPS API via `presenceService.registerDevice()`.

## Zello Push Architecture

Zello requires **native FCM** for PTT wake-up:

```
Zello Server → FCM → Device → Zello SDK wakes → Audio stream starts
```

## Coexistence Strategy

Both systems share the same Firebase project but handle messages independently:

1. **Expo Push** continues using `expo-notifications` for dispatch alerts (Code21), system notifications
2. **Zello FCM** uses `@react-native-firebase/messaging` for PTT wake-up

Zello's FCM messages include a Zello-specific data payload that the SDK intercepts automatically. Non-Zello messages pass through to `expo-notifications` as before.

### Firebase Background Handler

```typescript
// src/features/zello/zello-fcm-handler.ts
import messaging from '@react-native-firebase/messaging';

// Register at app root level — Zello intercepts its own messages
messaging().setBackgroundMessageHandler(async (remoteMessage) => {
  console.log('[ZELLO-FCM] Background message:', remoteMessage.messageId);
});
```

## Foreground Service

On Android, Zello runs a **foreground service** to maintain the audio connection. This shows a persistent notification in the status bar. The SDK manages this automatically when connected.

The SDK creates its own notification channel. Ensure `POST_NOTIFICATIONS` permission is granted (see `zello-setup` skill).

## Battery Optimisation

Critical for patrol reliability. Instruct officers to **disable battery optimisation** for EnforcementMAPS in Android settings. Without this, the OS may kill the foreground service during extended patrols.

Prompt on app startup:

```typescript
import { Linking, Alert } from 'react-native';

function promptBatteryOptimisation() {
  Alert.alert(
    'Battery Optimisation',
    'For reliable radio, disable battery optimisation for this app.',
    [
      { text: 'Open Settings', onPress: () => Linking.openSettings() },
      { text: 'Later', style: 'cancel' },
    ]
  );
}
```

## Key Rules

- **Do not** replace `expo-notifications` with Firebase messaging for app-level notifications — they serve different purposes
- Zello handles its own FCM registration internally after `connect()`
- `google-services.json` must match the `au.melbourne.patrolzones` package name

## Detailed Documentation

See `docs/dev/zello/09-background-push.md` for the full background services guide.
