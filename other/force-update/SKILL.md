---
name: force-update
description: Implement in-app update prompts with version checking, force/soft updates, Android In-App Updates, and store redirects. Supports Supabase and Firebase Remote Config backends. Use when adding update dialogs, version management, or blocking outdated app versions.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Force Update / App Update

Implement version checking and in-app update prompts to keep users on supported app versions.

## When to Use This Skill

- Adding force update functionality to block outdated versions
- Implementing soft update prompts for optional updates
- Setting up Android In-App Updates for seamless upgrades
- Configuring version management via Supabase or Firebase Remote Config
- User asks "force update", "app update", "version check", or "update dialog"

## When NOT to Use This Skill

- OTA code updates (Flutter doesn't support this like React Native) - Use store updates
- App store submission process - Use `/release` instead
- CI/CD build versioning - Use `/ci-cd` instead

## Questions to Ask

1. **Update strategy:** Force update only, soft update only, or both?
2. **Backend:** Supabase, Firebase Remote Config, or custom REST API?
3. **Android In-App Updates:** Enable flexible/immediate updates via Play Store?
4. **Minimum version logic:** Per-platform, per-feature, or global minimum?

## Quick Reference

### Update Types

| Type | Behavior | When to Use |
|------|----------|-------------|
| **Force Update** | Blocks app until updated | Security fixes, breaking API changes |
| **Soft Update** | Dismissible prompt | New features, minor improvements |
| **In-App Update (Android)** | Download without leaving app | Any update, better UX |
| **Maintenance Mode** | Blocks app entirely | Server downtime, critical issues |

### Version Comparison

| Current | Minimum | Force Min | Result |
|---------|---------|-----------|--------|
| 1.0.0 | 1.2.0 | 1.1.0 | Force update required |
| 1.1.5 | 1.2.0 | 1.1.0 | Soft update available |
| 1.2.0 | 1.2.0 | 1.1.0 | Up to date |

### Commands

```bash
# Validate force-update implementation
dart run .claude/skills/force-update/scripts/check.dart

# Check specific aspects
dart run .claude/skills/force-update/scripts/check.dart --check version-service
dart run .claude/skills/force-update/scripts/check.dart --check dialogs
```

## Workflow

### Phase 1: Setup Dependencies

1. Add required packages to `pubspec.yaml`:
   - `package_info_plus` - Get current app version
   - `in_app_update` (Android only) - Play Store in-app updates
   - `url_launcher` - Open app stores

2. Configure version source (choose one):
   - **Supabase:** Create `app_versions` table
   - **Firebase Remote Config:** Add version parameters

### Phase 2: Implement Version Service

1. Create `AppVersionService` in `lib/core/services/`
2. Implement version comparison logic (semantic versioning)
3. Add platform-specific store URLs
4. Create `VersionInfo` model with Freezed

### Phase 3: Add Update UI

1. Create `ForceUpdateScreen` - Full-screen blocker
2. Create `SoftUpdateDialog` - Dismissible bottom sheet
3. Create `MaintenanceScreen` - Server downtime blocker
4. Implement `UpdateNotifier` with Riverpod

### Phase 4: Integrate Check

1. Add version check to app startup (`main.dart` or splash)
2. Handle background-to-foreground transitions
3. Configure periodic checks for long sessions

### Phase 5: Android In-App Updates (Optional)

1. Implement `InAppUpdateService` wrapper
2. Choose update type: flexible (background) or immediate (blocking)
3. Handle download progress and install prompts

## Core API

**See:** `reference/` for complete implementations. Basic usage:

```dart
final versionInfo = await ref.read(versionServiceProvider).checkVersion();
// Handle: versionInfo.status (upToDate, softUpdateAvailable, forceUpdateRequired, maintenanceMode)
```

## File Structure

After using this skill:

```
lib/
├── core/
│   └── services/
│       ├── app_version_service.dart
│       └── in_app_update_service.dart   # Android only
└── features/
    └── force_update/
        ├── domain/
        │   ├── entities/
        │   │   └── version_info.dart
        │   └── enums/
        │       └── update_status.dart
        ├── data/
        │   ├── models/
        │   │   └── version_info_dto.dart
        │   └── repositories/
        │       └── version_repository_impl.dart
        └── presentation/
            ├── screens/
            │   ├── force_update_screen.dart
            │   └── maintenance_screen.dart
            ├── widgets/
            │   └── soft_update_dialog.dart
            └── providers/
                └── update_notifier.dart
```

## Failure Types

| Type | When | UI Action |
|------|------|-----------|
| `VersionCheckFailure` | Network error checking version | Retry or continue (configurable) |
| `StoreOpenFailure` | Can't open app store | Show manual store link |
| `InAppUpdateFailure` | Android update download failed | Fallback to store redirect |

## Guides

| File | Content |
|------|---------|
| [version-checking-guide.md](version-checking-guide.md) | Backend setup, version comparison logic |
| [update-dialogs-guide.md](update-dialogs-guide.md) | Dialog behavior, frequency limits, back prevention |
| [in-app-updates-guide.md](in-app-updates-guide.md) | Android Play Store in-app updates |

## Reference Files

**See:** `reference/` for complete implementations:

- `reference/entities/` - VersionInfo, UpdateStatus
- `reference/services/` - AppVersionService, InAppUpdateService
- `reference/providers/` - UpdateNotifier with Riverpod
- `reference/screens/` - ForceUpdateScreen, MaintenanceScreen
- `reference/widgets/` - SoftUpdateDialog

## Checklist

**Backend Setup:**
- [ ] Version endpoint configured (Supabase table or Remote Config)
- [ ] Minimum version field set
- [ ] Force minimum version field set
- [ ] Platform-specific versions if needed (iOS/Android)

**Version Service:**
- [ ] `package_info_plus` added to dependencies
- [ ] `AppVersionService` created
- [ ] Semantic version comparison implemented
- [ ] Store URLs configured for both platforms

**Update UI:**
- [ ] `ForceUpdateScreen` implemented (non-dismissible)
- [ ] `SoftUpdateDialog` implemented (dismissible)
- [ ] `MaintenanceScreen` implemented
- [ ] Update button opens correct store

**Integration:**
- [ ] Version check runs on app startup
- [ ] Version check runs on foreground resume
- [ ] Error handling for network failures
- [ ] Analytics events for update prompts

**Android In-App Updates (if enabled):**
- [ ] `in_app_update` package added
- [ ] `InAppUpdateService` wrapper created
- [ ] Flexible vs immediate strategy chosen
- [ ] Download progress UI implemented

## Related Skills

- `/release` - App store preparation and signing
- `/ci-cd` - Build versioning and deployment
- `/analytics` - Track update prompt interactions
- `/i18n` - Localize update dialog strings
- `/design` - Polish update screen UI
- `/a11y` - Add accessibility to update screens

## Common Issues

**See:** [version-checking-guide.md](version-checking-guide.md) for error handling, caching, and troubleshooting.

Key points:
- Use timeout on version checks to avoid blocking app launch
- iOS store URL format: `https://apps.apple.com/app/id{APP_ID}`
- Android In-App Updates only work with Play Store installs

## Next Steps

After implementing force update:
1. `/i18n` - Localize all user-facing strings
2. `/design` - Polish UI, loading states, visual feedback
3. `/a11y` - Add semantic labels, ensure accessibility
4. `/analytics` - Add update prompt tracking events
5. `/ci-cd` - Automate version bumping in CI
