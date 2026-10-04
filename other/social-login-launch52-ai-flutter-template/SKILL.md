---
name: social-login
description: Google Sign-In and Apple Sign-In with Supabase or custom backend. OAuth setup, platform config, PKCE/nonce security, sealed Failures, mock repository. Use when adding social login or troubleshooting OAuth.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, WebFetch
---

# Social Login - Google & Apple Sign-In

Google and Apple authentication with Supabase or custom backend.

## When to Use This Skill

- Adding social login to a project
- Configuring OAuth providers (Google Cloud, Apple Developer)
- Troubleshooting social auth issues
- Adding SHA-1 fingerprints for Android

## Reference Files

```
reference/
├── repositories/     # Domain interface, impl, mocks
├── failures/         # Sealed Failure types
├── providers/        # AuthNotifier social methods
├── utils/            # Nonce helpers, constants
├── widgets/          # Social login button
└── screens/          # OAuth callback (Android)

templates/            # Info.plist, AndroidManifest additions
```

**See:** [implementation-guide.md](implementation-guide.md) for complete file list.

## Workflow

### Phase 1: Provider Setup
1. Google Cloud Console - OAuth clients, SHA-1 (see google-guide.md)
2. Apple Developer - App ID, Service ID, Key (see apple-guide.md)
3. Supabase - Enable providers (see supabase-guide.md)

### Phase 2: Platform Config
1. iOS: Add URL schemes to Info.plist, add Sign in with Apple capability
2. Android: Add deep link intent filter to AndroidManifest.xml

### Phase 3: Implementation
1. Copy reference files to project
2. Add methods to existing AuthRepositoryImpl
3. Add provider methods to AuthNotifier
4. Add OAuth callback route
5. Run `/i18n` for strings

## Core API

```dart
// Google Sign-In
final result = await repository.signInWithGoogle();

// Apple Sign-In
final result = await repository.signInWithApple();

// Result contains: userId, email?, displayName?, isNewUser
```

## Failure Types

| Type | When | UI Action |
|------|------|-----------|
| `GoogleSignInCancelledFailure` | User dismissed | Silent |
| `GoogleSignInFailedFailure` | SDK error | Error + retry |
| `AppleSignInCancelledFailure` | User dismissed | Silent |
| `AppleSignInFailedFailure` | SDK error | Error + retry |
| `TokenValidationFailure` | Invalid token | Error + retry |
| `SocialAuthNetworkFailure` | Connection | Retry button |

Cancellation is NOT an error - handle silently.

## Platform Flows

| Provider | iOS | Android |
|----------|-----|---------|
| Google | Native SDK | Native SDK |
| Apple | Native SDK | OAuth Browser |

## SHA-1 Fingerprints

```bash
cd android && ./gradlew signingReport
```

Add to Google Cloud Console: debug, release, Play Store SHA-1.

## Guides

| File | Content |
|------|---------|
| [google-guide.md](google-guide.md) | Google Cloud Console setup |
| [apple-guide.md](apple-guide.md) | Apple Developer setup |
| [supabase-guide.md](supabase-guide.md) | Supabase provider config |
| [implementation-guide.md](implementation-guide.md) | Step-by-step code |
| [checklist.md](checklist.md) | Verification checklist |

## Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| `DEVELOPER_ERROR` | SHA-1 mismatch | Add correct SHA-1 |
| No idToken | Missing serverClientId | Set GOOGLE_WEB_CLIENT_ID |
| `invalid_client` | Apple config wrong | Check Supabase Apple config |
| No callback (Android) | Deep link wrong | Verify AndroidManifest |

## Checklist

- [ ] Google Cloud Console: OAuth client IDs created (iOS, Android, Web)
- [ ] Android: All SHA-1 fingerprints added (debug, release, Play Store)
- [ ] Apple Developer: App ID with Sign in with Apple enabled
- [ ] Apple Developer: Service ID configured (for Android OAuth flow)
- [ ] Supabase: Google and Apple providers enabled with credentials
- [ ] iOS: URL schemes added to Info.plist
- [ ] iOS: Sign in with Apple capability added
- [ ] Android: Deep link intent filter in AndroidManifest.xml
- [ ] OAuth callback route added to router
- [ ] Cancellation handled silently (not shown as error)
- [ ] `build_runner` executed successfully

## Related Skills

- `/phone-auth` - Can combine with social login
- `/i18n` - Localized strings
- `/release` - iOS capabilities, Android signing
- `/testing` - Test social login flows
