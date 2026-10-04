---
name: account-deletion
description: Implement GDPR/App Store/Play Store compliant account deletion with confirmation flow, data cleanup, and auth sign-out. Use when adding "delete account", "remove account", or "user data deletion" features. Required for both App Store and Play Store compliance.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Account Deletion

Implements GDPR, App Store, and Play Store compliant account deletion with proper confirmation flows, backend data cleanup, and secure sign-out. Required by both Apple App Store and Google Play Store guidelines for apps with account creation.

## When to Use This Skill

- Adding account deletion to settings screen
- App Store or Play Store review requires account deletion
- Implementing GDPR "right to erasure"
- User asks "add delete account", "remove account option"
- Settings feature needs user data deletion

## When NOT to Use This Skill

- User just wants to sign out - Use `/auth` signOut method
- Deleting app data only (no account) - Manual implementation
- Admin user deletion - Custom admin feature

## Questions to Ask

1. **Backend type:** Supabase, Firebase, or Custom API?
2. **Confirmation method:** Password re-entry, typed confirmation, or simple dialog?
3. **Grace period:** Immediate deletion or scheduled (e.g., 30 days)?
4. **Data cleanup:** What user data needs deletion? (storage, analytics, etc.)

## Quick Reference

### App Store & Play Store Requirements

| Requirement | Implementation |
|-------------|----------------|
| Easy to find | Settings > Account > Delete Account |
| Clear explanation | Show what data will be deleted |
| Confirmation | Require explicit user action |
| Complete deletion | Remove all user data from backend |
| In-app option | Must be accessible within the app (not just web) |

### GDPR Compliance

| Right | Implementation |
|-------|----------------|
| Right to erasure | Full account + data deletion |
| Clear consent | Explicit confirmation required |
| Data portability | (Optional) Export before deletion |

### Confirmation Methods

| Method | Security | UX | Use Case |
|--------|----------|-----|----------|
| Password re-entry | High | Low | Financial/sensitive apps |
| Type "DELETE" | Medium | Medium | Standard apps |
| Simple dialog | Low | High | Low-risk apps |

## Workflow

### Phase 1: Ask Questions

Use AskUserQuestion to gather:
- Backend type (Supabase/Firebase/Custom)
- Confirmation method preference
- Grace period requirements
- Data cleanup scope

### Phase 2: Domain Layer

Create in `lib/features/settings/domain/`:
1. `AccountDeletionFailure` - Failure types
2. Extend `SettingsRepository` with `deleteAccount()` method

**See:** [implementation-guide.md](implementation-guide.md) for code.

### Phase 3: Data Layer

Create in `lib/features/settings/data/`:
1. Implement `deleteAccount()` in repository
2. Add backend-specific deletion logic (Supabase/Firebase/API)
3. Add data cleanup (storage, analytics reset)

**See:** `reference/repositories/` for implementations.

### Phase 4: Presentation Layer

Create in `lib/features/settings/presentation/`:
1. `DeleteAccountButton` widget
2. `DeleteAccountDialog` with confirmation
3. `AccountDeletionNotifier` for state management
4. Add to Settings screen

**See:** `reference/screens/` and `reference/widgets/` for code.

### Phase 5: Integration

1. Add delete account option to settings screen
2. Wire up confirmation dialog
3. Handle success (navigate to login)
4. Handle errors (show failure message)

### Phase 6: Testing

```bash
dart run .claude/skills/account-deletion/scripts/check.dart
```

## File Structure

- `lib/features/settings/domain/failures/account_deletion_failure.dart`
- `lib/features/settings/data/repositories/settings_repository_impl.dart` (extended)
- `lib/features/settings/presentation/providers/account_deletion_notifier.dart`
- `lib/features/settings/presentation/widgets/delete_account_button.dart`
- `lib/features/settings/presentation/widgets/delete_account_dialog.dart`

## Core API

**See:** `reference/providers/account_deletion_notifier.dart` for full usage.

| Method | Purpose |
|--------|---------|
| `deleteAccount({confirmation})` | Deletes account with optional confirmation |
| `reset()` | Resets state to initial |
| `validateConfirmation(input)` | Validates "DELETE" input |

## Failure Types

| Type | When | UI Action |
|------|------|-----------|
| `AccountDeletionNetworkFailure` | No connection | Retry button |
| `AccountDeletionServerFailure` | Backend error | Generic error |
| `AccountDeletionAuthFailure` | Not authenticated | Navigate to login |
| `AccountDeletionConfirmationFailure` | Wrong confirmation | Show validation error |

## Guides

| File | Content |
|------|---------|
| [implementation-guide.md](implementation-guide.md) | Step-by-step with code examples |
| [checklist.md](checklist.md) | Implementation verification |

## Reference Files

**See:** `reference/` for complete implementations:

- `reference/failures/` - AccountDeletionFailure sealed class
- `reference/repositories/` - Supabase, Firebase, API implementations
- `reference/providers/` - AccountDeletionNotifier
- `reference/widgets/` - DeleteAccountButton, DeleteAccountDialog
- `reference/screens/` - Settings screen integration

## Commands

```bash
# Validate implementation
dart run .claude/skills/account-deletion/scripts/check.dart

# Check specific feature
dart run .claude/skills/account-deletion/scripts/check.dart --feature settings
```

## Checklist

- [ ] `AccountDeletionFailure` sealed class created
- [ ] `deleteAccount()` in repository with backend deletion
- [ ] User data cleanup (storage, analytics) + auth sign-out
- [ ] `DeleteAccountButton` and `DeleteAccountDialog` widgets
- [ ] `AccountDeletionNotifier` with loading/error states
- [ ] Settings screen integration with clear explanation
- [ ] Explicit confirmation required before deletion
- [ ] App Store/Play Store: Easy to find, complete deletion, in-app option

**See:** [checklist.md](checklist.md) for detailed verification.

## Common Issues

| Issue | Solution |
|-------|----------|
| "User not authenticated" | Check auth state before deletion, handle expired session |
| Data remains after deletion | Clean up: Supabase/Firebase record, SecureStorage, SharedPrefs, Analytics |
| Dialog dismissed accidentally | Set `barrierDismissible: false` on showDialog |
| Stuck on loading | Add disposal check (`if (_disposed) return`) after async operations |

**See:** [implementation-guide.md](implementation-guide.md) for detailed solutions.

## Related Skills

- `/auth` - Provides signOut method used after deletion
- `/i18n` - Localize deletion strings
- `/testing` - Write tests for deletion flow
- `/design` - UI polish for deletion flow

## Next Steps

After `/account-deletion`: Run `/i18n settings`, `/testing settings`, then `/design`.
