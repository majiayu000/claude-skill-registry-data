---
name: push-notifications
description: Push notifications with Firebase Cloud Messaging (FCM). Platform setup, APNs certificates, foreground/background handling, deep linking, topic subscriptions, local notifications. Use when implementing push notifications or troubleshooting FCM.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, WebFetch
---

# Push Notifications - Firebase Cloud Messaging

Push notifications with FCM for iOS and Android. Handles foreground, background, and terminated app states.

## When to Use This Skill

- Adding push notifications to a Flutter app
- Configuring Firebase Cloud Messaging
- Setting up APNs for iOS
- Implementing deep linking from notifications
- User asks "add push notifications", "FCM setup", or "notification handling"

## Questions to Ask

1. **Firebase project:** Is Firebase already configured, or need to set up from scratch?
2. **Notification types:** Marketing notifications only, or also transactional (in-app events)?
3. **Deep linking:** Should notifications open specific screens?
4. **Topics:** Need topic-based subscriptions (e.g., "news", "promotions")?
5. **Local notifications:** Need scheduled/local notifications (non-push)?

## Reference Files

```
reference/
├── models/           # Notification payload (Freezed)
├── services/         # FCM initialization, handlers
├── repositories/     # Domain interface + impl + mock
├── providers/        # Riverpod notifiers + state
└── failures/         # Sealed Failure types

templates/ios/        # Info.plist additions
templates/android/    # AndroidManifest, build.gradle
```

**See:** [implementation-guide.md](implementation-guide.md) for complete setup.

## Workflow

### Phase 1: Firebase Setup
1. Create Firebase project (if needed)
2. Add iOS app with APNs key (see firebase-setup-guide.md)
3. Add Android app with SHA-1 fingerprints
4. Download config files (GoogleService-Info.plist, google-services.json)

### Phase 2: Platform Config
1. iOS: Add Push Notification capability, Background Modes
2. Android: Add FCM dependencies and manifest entries
3. Add config files to project

### Phase 3: Implementation
1. Copy reference files to project
2. Initialize FCM in main.dart
3. Implement token registration with backend
4. Add notification handlers (foreground/background/terminated)
5. Configure deep linking (optional)

## Core API

```dart
await PushNotificationService.initialize();
final token = await PushNotificationService.getToken();
PushNotificationService.onNotificationTap.listen((payload) => ...);
```

## Notification States

| State | Handler | Behavior |
|-------|---------|----------|
| **Foreground** | `onMessage` | Show local notification or in-app banner |
| **Background** | `onBackgroundMessage` | System shows notification |
| **Terminated** | `getInitialMessage` | Check on app launch |

## Failure Types

| Type | When | UI Action |
|------|------|-----------|
| `PermissionDeniedFailure` | User denied permission | Settings prompt |
| `TokenRegistrationFailure` | Backend token save failed | Silent retry |
| `NotificationNetworkFailure` | Connection error | Retry later |
| `InvalidPayloadFailure` | Malformed notification | Log and ignore |

## Platform Requirements

### iOS
- APNs Key or Certificate in Firebase Console
- Push Notification capability
- Background Modes: Remote notifications
- `Info.plist`: FirebaseAppDelegateProxyEnabled = NO (if handling manually)

### Android
- `google-services.json` in `android/app/`
- FCM dependency in `build.gradle`
- Default notification channel

## Guides

| File | Content |
|------|---------|
| [implementation-guide.md](implementation-guide.md) | Step-by-step code setup |
| [firebase-setup-guide.md](firebase-setup-guide.md) | Firebase Console + APNs setup |
| [checklist.md](checklist.md) | Verification checklist |

## Dependencies

```yaml
dependencies:
  firebase_core: ^3.9.0
  firebase_messaging: ^15.2.0
  flutter_local_notifications: ^18.0.1  # For foreground display
```

## Checklist

- [ ] Firebase project created with iOS and Android apps
- [ ] APNs key uploaded to Firebase Console
- [ ] `GoogleService-Info.plist` added to iOS Runner
- [ ] `google-services.json` added to `android/app/`
- [ ] iOS: Push Notification capability added
- [ ] iOS: Background Modes enabled (Remote notifications)
- [ ] Android: FCM dependencies in build.gradle
- [ ] PushNotificationService initialized in main.dart
- [ ] FCM token sent to backend on login/refresh
- [ ] Foreground notification handler configured
- [ ] Background notification handler registered
- [ ] Deep linking configured (if needed)
- [ ] Permission request flow implemented

## Related Skills

- `/release` - iOS capabilities, Android signing
- `/design` - In-app notification banners
- `/i18n` - Localized notification content
- `/testing` - Test notification flows
