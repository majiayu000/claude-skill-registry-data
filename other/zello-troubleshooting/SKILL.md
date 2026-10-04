---
name: zello-troubleshooting
description: Diagnose and fix Zello SDK build errors, runtime issues, Expo Go incompatibility, EAS build failures, Metro cache problems, and audio/permission issues in EnforcementMAPS.
---

# Zello Troubleshooting

This skill covers common issues when building and running the Zello SDK in the EnforcementMAPS Expo managed workflow.

## Build Errors

### Hilt / Dagger Annotation Processor Failure

```
error: [Hilt] ProcessedRootSentinel(...)
```

**Why:** Zello's native Android SDK uses Hilt internally. The Expo managed workflow may not configure the kapt/ksp annotation processor by default.

**Fix:** Ensure `expo-build-properties` is installed and configured:

```typescript
['expo-build-properties', {
  android: {
    kotlinVersion: '1.9.24',
    enableProguardInReleaseBuilds: true,
  },
}],
```

### Maven Repository Not Found

```
Could not resolve com.zello:zello-sdk
```

**Why:** The Zello Maven repo (`https://zello.jfrog.io/artifactory/maven/`) wasn't added.

**Fix:** The RN SDK's `build.gradle` should handle this via autolinking. If not, create a custom Expo config plugin to add the Maven URL. Check that `@zelloptt/react-native-zello-sdk` is in `node_modules/` and re-run `pnpm install`.

### Duplicate Class Errors

```
Duplicate class kotlin.collections.jdk8.*
```

**Fix:** Add packaging options via `expo-build-properties`:

```typescript
android: {
  packagingOptions: {
    pickFirst: ['**/kotlin/**'],
  },
},
```

## Runtime Errors

### "Zello is not connected" When Sending PTT

**Why:** `Zello.send()` called before `onConnected` event fired.

**Fix:** Guard PTT actions on connection state from the `useZelloStatus()` hook. Disable the PTT button until `connected === true`.

### No Audio on Incoming Message

**Why:** Audio focus not acquired, or device volume at zero.

**Fix:** Check device volume. The SDK manages audio focus, but other apps (especially `expo-notifications` sounds) may interfere. Avoid playing notification sounds during active PTT.

### Microphone Permission Denied Silently

**Why:** On Android 11+, after two denials the OS stops showing the permission prompt.

**Fix:** Detect `NEVER_ASK_AGAIN` state and direct the user to Settings → App Permissions with a clear, jargon-free message.

## Expo-Specific Issues

### "Cannot use native module in Expo Go"

**Expected behaviour.** The Zello SDK is a native module and requires an EAS dev build. It will **never** work in Expo Go.

```bash
eas build --platform android --profile development
```

### Metro Bundler Cannot Resolve Zello SDK

**Fix:** Clear Metro cache:

```bash
pnpm start --clear
```

### EAS Build Timeout

**Why:** Zello's native dependencies (Hilt, protobuf) increase build time significantly.

**Fix:** Increase the resource class in `eas.json`:

```json
"android": {
  "resourceClass": "m-medium"
}
```

## Debugging

### Enable SDK Logging

```typescript
Zello.setLogLevel('debug');
```

### Check Connection State

```typescript
Zello.Listener.on('onConnectFailed', ({ error }) => {
  console.error('[ZELLO] Connection failed:', error);
});
```

### Verify FCM Token Delivery

Check Firebase console → Cloud Messaging → Diagnostics for delivery status to `au.melbourne.patrolzones`.

## Error Handling Pattern

Follow the project's `http.ts` pattern — log technical details internally, show user-friendly messages externally. The CLAUDE.md rule: "Error messages should be helpful, not technical."

## Detailed Documentation

See `docs/dev/zello/13-troubleshooting.md` for the complete troubleshooting guide.
