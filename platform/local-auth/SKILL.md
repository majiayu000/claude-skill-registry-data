---
name: local-auth
description: Local device authentication (biometric + device credentials). App unlock with configurable timeout, biometric change detection, optional app PIN, optional lock screen UI. Use when adding biometric login, app unlock, or secure action confirmation.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Local Auth - Device Authentication

Local device authentication using biometrics (Face ID, Touch ID, fingerprint) and device credentials (PIN, pattern, password). Configurable security levels from basic to banking-grade.

## When to Use This Skill

- Adding biometric/device unlock to an app
- Implementing app lock after background timeout
- Securing sensitive actions (payments, delete, view PII)
- User asks "biometric", "face id", "fingerprint", "app lock", "local auth"

## When NOT to Use This Skill

- **Remote authentication** - Use `/auth`, `/social-login`, `/phone-auth`
- **Session tokens** - Handled by `/auth` and `/data`
- **Secure storage** - Already in `/core` (flutter_secure_storage)

## Questions to Ask

Before generating code, ask these questions:

1. **Use case:** App unlock after timeout OR sensitive action confirmation OR both?
2. **Security level:** Trust device (simple) OR detect biometric changes (banking-grade)?
3. **Lock screen:** Generate lock screen UI OR service only?
4. **Settings toggle:** Generate enable/disable toggle widget?
5. **App PIN:** Include app-level PIN for devices without lock screen?
6. **Timeout:** How long in background before requiring re-auth? (0 = immediate)
7. **Failure behavior:** Force full re-login OR let device handle lockout?

## Quick Reference

### Dependencies

```yaml
dependencies:
  local_auth: ^2.3.0
```

### Security Levels

| Level | Biometric Change | Use Case |
|-------|------------------|----------|
| **Simple** | Trust any enrolled biometric | Social apps, low-risk |
| **Banking** | Detect changes, require re-login | Finance, health, PII |

### Authentication Options

| Option | iOS | Android |
|--------|-----|---------|
| Face ID / Face Unlock | Yes | Yes |
| Touch ID / Fingerprint | Yes | Yes |
| Passcode | Yes | Yes |
| PIN / Pattern | N/A | Yes |

### Core Components

| Component | Purpose |
|-----------|---------|
| `LocalAuthService` | Wraps local_auth, handles platform checks |
| `LocalAuthNotifier` | State management, timeout tracking |
| `LocalAuthSettings` | User preferences (enabled, timeout) |
| `LockScreen` | Optional full-screen auth prompt |
| `LocalAuthToggle` | Optional settings widget |
| `AppPinService` | Optional app-level PIN (no device lock) |

## Workflow

### Phase 1: Gather Requirements

Ask all questions from "Questions to Ask" section before proceeding.

### Phase 2: Platform Setup

1. iOS: Add `NSFaceIDUsageDescription` to Info.plist
2. Android: Add `USE_BIOMETRIC` permission to AndroidManifest.xml
3. Run `flutter pub get`

### Phase 3: Create Core Files

1. Create `LocalAuthService` in `lib/core/services/`
2. Create `LocalAuthNotifier` + state in `lib/core/providers/`
3. Create `LocalAuthSettings` for preferences

### Phase 4: Optional Components

Based on user answers:
- **Lock screen:** Create `LockScreen` widget
- **Settings toggle:** Create `LocalAuthToggle` widget
- **App PIN:** Create `AppPinService` and PIN entry UI
- **Banking security:** Add biometric state tracking

### Phase 5: Integration

1. Add `WidgetsBindingObserver` for app lifecycle
2. Configure timeout-based re-auth
3. Wrap sensitive actions with auth check

### Phase 6: Verify

```bash
dart run .claude/skills/local-auth/scripts/check.dart
```

## Core API

```dart
// Check availability
final canAuth = await localAuthService.canAuthenticate();

// Authenticate (biometricOnly: false allows PIN/pattern fallback)
final result = await localAuthService.authenticate(reason: 'Unlock');
```

**See:** `reference/services/local_auth_service.dart` for full API.

## File Structure

```
lib/core/
├── services/local_auth_service.dart    # Core service
├── providers/local_auth_provider.dart  # Notifier + settings
└── widgets/lock_screen.dart            # Optional UI
```

**See:** [checklist.md](checklist.md) for full file list with optional components.

## Failure Types

| Type | When | UI Action |
|------|------|-----------|
| `LocalAuthNotAvailable` | No biometric/lock enrolled | Show setup prompt |
| `LocalAuthNotEnrolled` | Biometric not set up | Show settings link |
| `LocalAuthFailed` | User failed auth | Retry or fallback |
| `LocalAuthCancelled` | User cancelled | Silent (not error) |
| `BiometricsChanged` | Fingerprint/face changed | Force full re-login |
| `LocalAuthLockout` | Too many failures | Show countdown/message |

## Guides

| File | Content |
|------|---------|
| [setup-guide.md](setup-guide.md) | Platform setup (iOS/Android) |
| [security-guide.md](security-guide.md) | Security levels, biometric change detection |
| [patterns-guide.md](patterns-guide.md) | Usage patterns, timeout, lifecycle |
| [troubleshooting-guide.md](troubleshooting-guide.md) | Common issues and solutions |
| [checklist.md](checklist.md) | Verification checklist |

## Reference Files

**See:** `reference/` directory for complete implementations (services, providers, widgets, utils).

## Checklist

**Platform Setup:**
- [ ] `local_auth: ^2.3.0` added to pubspec.yaml
- [ ] iOS: `NSFaceIDUsageDescription` in Info.plist
- [ ] Android: `USE_BIOMETRIC` permission in AndroidManifest.xml
- [ ] `flutter pub get` run successfully

**Core Implementation:**
- [ ] `LocalAuthService` created with availability checks
- [ ] `LocalAuthNotifier` manages auth state
- [ ] `LocalAuthSettings` stores user preferences
- [ ] App lifecycle observer tracks background time

**Optional Components:**
- [ ] Lock screen UI (if requested)
- [ ] Settings toggle widget (if requested)
- [ ] App PIN service (if requested)
- [ ] Biometric change detection (if banking-grade)

**Testing:**
- [ ] Biometric auth works on real device
- [ ] Device credential fallback works
- [ ] Timeout triggers re-auth correctly
- [ ] Cancellation handled silently

## Related Skills

- `/auth` - Base authentication (this extends it for local unlock)
- `/social-login`, `/phone-auth` - Remote auth methods
- `/design` - Lock screen UI patterns
- `/i18n` - Localized auth prompts
- `/testing` - Test local auth flows

## Next Steps

After running this skill:
1. Test on real device (simulators have limitations)
2. Run `/i18n` for auth prompt strings
3. Run `/design` for lock screen polish
4. Run `/testing` for auth flow tests
