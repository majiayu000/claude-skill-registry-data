---
name: auth
description: Generate base authentication feature scaffold with Clean Architecture. Creates shared auth infrastructure (AuthRepository, AuthNotifier, UserProfile, LoginScreen) that /social-login and /phone-auth extend. Run after /core, before specific auth methods.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Auth - Base Authentication Scaffold

Creates the authentication feature foundation with Clean Architecture. This skill generates shared infrastructure that `/social-login` and `/phone-auth` build upon.

## When to Use This Skill

- After `/core` skill completes
- Before adding specific auth methods (`/social-login`, `/phone-auth`)
- Setting up auth from scratch
- User asks to "add authentication" or "create auth"

## Questions to Ask

1. **Backend type:** Supabase or Custom API?
2. **Auth methods:** (multi-select) Social Login, Phone OTP, Email/Password
3. **User profile fields:** Custom fields beyond id/email? (e.g., displayName, avatarUrl)

## What This Skill Creates

Base auth infrastructure that specific auth skills extend:

| Component | Purpose | Extended By |
|-----------|---------|-------------|
| `AuthRepository` | Base interface (signOut, getCurrentUser) | social-login, phone-auth |
| `AuthNotifier` | State management with disposal safety | All auth screens |
| `AuthState` | Sealed states (loading, authenticated, error) | All auth screens |
| `UserProfile` | User model | All auth methods |
| `AuthResult` | Sign-in result with isNewUser flag | social-login, phone-auth |
| `LoginScreen` | Base scaffold for auth UI | Buttons added by methods |
| `AuthFailure` | Base failure types | Extended by methods |

## Reference Files

```
reference/
├── models/           # UserProfile, AuthResult
├── repositories/     # Interface, Supabase impl, mock
├── providers/        # AuthState, AuthNotifier
├── screens/          # LoginScreen scaffold
└── failures/         # Base auth failure types
```

**See:** [implementation-guide.md](implementation-guide.md) for complete file list.

## Workflow

### Phase 1: Ask Questions

Use AskUserQuestion to gather:
- Backend type (Supabase vs Custom API)
- Which auth methods needed
- Custom user profile fields

### Phase 2: Generate Structure

Create standard Clean Architecture feature:

```
lib/features/auth/
├── data/          # models/, repositories/
├── domain/        # failures/, repositories/
├── presentation/  # providers/, screens/
└── i18n/          # auth.i18n.yaml
```

**See:** [implementation-guide.md](implementation-guide.md) for complete structure.

### Phase 3: Copy Reference Files

1. Copy models from `reference/models/`
2. Copy repository interface from `reference/repositories/`
3. Copy implementation (Supabase or API base)
4. Copy providers from `reference/providers/`
5. Copy login screen scaffold from `reference/screens/`

### Phase 4: Register Providers

Add to `lib/core/providers.dart`:

```dart
@riverpod
AuthRepository authRepository(Ref ref) {
  if (DebugConstants.useMockAuth) {
    return MockAuthRepository();
  }
  return AuthRepositoryImpl(Supabase.instance.client);
}
```

### Phase 5: Add Routes

Add to `lib/core/router/app_router.dart`:

```dart
GoRoute(
  path: '/login',
  builder: (context, state) => const LoginScreen(),
),
```

### Phase 6: Run Build

```bash
dart run build_runner build --delete-conflicting-outputs
```

## Core API

```dart
// Check current auth state
final user = await repository.getCurrentUser();

// Sign out
await repository.signOut();

// Listen to auth changes
repository.authStateChanges.listen((user) => ...);
```

## Auth States

| State | When | UI |
|-------|------|-----|
| `initial` | App start, checking auth | Splash |
| `loading` | Sign-in in progress | Loading indicator |
| `authenticated(user)` | User signed in | Navigate to home |
| `unauthenticated` | No user / signed out | Show login |
| `error(message)` | Auth failed | Error + retry |

## Base Failure Types

| Type | When | UI Action |
|------|------|-----------|
| `AuthNetworkFailure` | Connection error | Retry button |
| `AuthServerFailure` | Backend error | Generic error |
| `AuthSessionExpiredFailure` | Token expired | Re-login |
| `AuthUnknownFailure` | Unexpected error | Generic error |

Specific auth methods add their own failure types (see `/social-login`, `/phone-auth`).

## Next Steps

After running `/auth`, run these skills based on your selection:

| If Selected | Run | Creates |
|-------------|-----|---------|
| Social Login | `/social-login` | Google + Apple Sign-In |
| Phone OTP | `/phone-auth` | Phone verification |
| Email/Password | (built-in) | Email auth methods |

Then:
1. `/i18n auth` - Localize strings
2. `/design` - Polish UI
3. `/testing auth` - Write tests

## Integration Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    LoginScreen                          │
│  ┌────────────┐ ┌────────────┐ ┌────────────────────┐  │
│  │ Email Form │ │ Social Btns│ │ Phone Number Input │  │
│  │ (built-in) │ │(/social)   │ │   (/phone-auth)    │  │
│  └─────┬──────┘ └─────┬──────┘ └─────────┬──────────┘  │
└────────┼──────────────┼──────────────────┼─────────────┘
         │              │                  │
    ┌────┴──────────────┴──────────────────┴────┐
    │              AuthNotifier                  │
    │  signInWithEmail | signInWithGoogle | ... │
    └──────────────────┬────────────────────────┘
                       │
    ┌──────────────────┴────────────────────────┐
    │             AuthRepository                 │
    │ implements: SocialAuthRepo, PhoneAuthRepo │
    └───────────────────────────────────────────┘
```

## Guides

| File | Content |
|------|---------|
| [implementation-guide.md](implementation-guide.md) | Step-by-step with code examples |
| [checklist.md](checklist.md) | Implementation verification |

## Checklist

- [ ] AuthRepository interface created with signOut, getCurrentUser, authStateChanges
- [ ] AuthNotifier extends AsyncNotifier with disposal safety
- [ ] AuthState is sealed (initial, loading, authenticated, unauthenticated, error)
- [ ] UserProfile model created with required fields
- [ ] Repository implementation matches backend type (Supabase/Custom)
- [ ] Provider registered in `lib/core/providers.dart`
- [ ] Login route added to router
- [ ] `build_runner` executed successfully
- [ ] Mock repository created for testing

## Related Skills

- `/social-login` - Google + Apple Sign-In (extends auth)
- `/phone-auth` - Phone OTP (extends auth)
- `/core` - Run before auth (creates services)
- `/design` - Login screen UI polish
- `/i18n` - Localized auth strings
