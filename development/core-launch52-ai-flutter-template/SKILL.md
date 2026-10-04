---
name: core
description: Generate core infrastructure for Flutter apps. Creates theme system (AppColors, AppTheme), router (GoRouter), services (SecureStorage, SharedPrefs, Supabase), error handling (Failures), and providers. Run after /init, before /auth.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Core - Infrastructure Generation

Generates the core infrastructure that all features depend on.

## When to Use This Skill

- After `/init` completes
- Before adding any features or `/auth`
- Setting up app-wide infrastructure
- User asks to "generate core", "create infrastructure", or "setup theme/router"

## What This Skill Creates

- `lib/app.dart` - Root app widget with MaterialApp.router
- `lib/core/theme/` - AppColors, AppTypography, AppTheme
- `lib/core/router/` - GoRouter configuration
- `lib/core/services/` - SecureStorage, SharedPrefs, Supabase, iOS network permission
- `lib/core/errors/` - Typed failures and exceptions
- `lib/core/constants/` - App constants, legal URLs, storage keys, debug flags
- `lib/core/network/` - Dio client (if custom API)
- `lib/core/navigation/` - StatefulShellRoute (if bottom nav)
- `lib/core/providers.dart` - Core Riverpod providers

## Workflow

### Phase 1: Gather Requirements

Use AskUserQuestion to confirm settings from `/init`:

1. **Primary Color** (hex, from /init or ask)
2. **Theme Mode** (light/dark/both)
3. **Use Supabase?** (from /init)
4. **Use Custom API?** (from /init)
5. **Bottom Navigation?** (yes/no - determines shell creation)
6. **Privacy Policy URL?** (can be placeholder, required before release)
7. **Terms of Service URL?** (can be placeholder, required before release)

### Phase 2: Create Directory Structure

```bash
mkdir -p lib/core/{constants,errors,network,router,navigation,services,theme,utils,widgets}
mkdir -p lib/features
```

### Phase 3: Generate Files

Copy from `reference/` directories and customize:

| Category | Files | Notes |
|----------|-------|-------|
| `theme/` | app_colors, app_typography, app_theme | Customize primary color |
| `services/` | secure_storage, shared_prefs, ios_network_permission | Always |
| `services/` | supabase_service | If Supabase = yes |
| `network/` | dio_client | If Custom API = yes |
| `router/` | app_router | Customize routes |
| `navigation/` | main_shell | If bottom nav = yes |
| `errors/` | failures, exceptions | Always |
| `constants/` | app_constants, legal_constants, storage_keys, debug_constants | Always |
| `utils/` | legal_utils | Always |
| root | providers.dart | Customize based on services |

**Note:** `ios_network_permission_service.dart` triggers the iOS permission dialog early to prevent first API call failures.

### Phase 10: Generate App Widget

Copy `reference/app.dart` and customize with theme/router.

### Phase 11: Update main.dart

Replace placeholder with actual App():

```dart
import 'app.dart';

runApp(const ProviderScope(child: App()));
```

### Phase 12: Verify

```bash
dart run build_runner build --delete-conflicting-outputs
flutter analyze
```

## Reference Files

| Directory | Content |
|-----------|---------|
| `reference/theme/` | AppColors, AppTypography, AppTheme |
| `reference/router/` | GoRouter setup |
| `reference/navigation/` | StatefulShellRoute scaffold |
| `reference/services/` | Storage, Supabase, iOS permission services |
| `reference/network/` | Dio client with interceptors |
| `reference/errors/` | Failure types, exceptions |
| `reference/constants/` | App constants, legal URLs, storage keys, debug flags |
| `reference/utils/` | Legal URL utilities |
| `reference/` | app.dart, providers.dart |

## Guides

This skill is code-heavy with all templates in `reference/`. No separate guides needed.

**Related guidance from other skills:**

| Topic | See |
|-------|-----|
| Architecture patterns | `.claude/skills/plan/architecture.md` |
| Color usage (contrast, dark mode) | `/design` → `visual-guide.md` |
| Typography sizes & hierarchy | `/design` → `visual-guide.md` |
| Color contrast requirements | `/a11y` → `semantics-guide.md` |
| Text scaling accessibility | `/a11y` → `testing-guide.md` |

## Quick Reference

```dart
AppColors.primary; AppTheme.light(); // Theme
context.go('/dashboard'); context.push('/profile'); // Router
ref.watch(secureStorageProvider).write('key', 'value'); // Secure storage
ref.watch(sharedPrefsProvider).setBool('onboarded', true); // Shared prefs
triggerIOSNetworkPermission(); // iOS permission (call in main.dart)
```

## Next Steps

After `/core`:

1. `/auth` - Add authentication feature
2. `/feature-init dashboard` - Initialize dashboard scaffold
3. `/i18n` - Add localization

## Checklist

- [ ] `lib/app.dart` created with MaterialApp.router
- [ ] `lib/core/theme/` has AppColors, AppTypography, AppTheme
- [ ] `lib/core/router/app_router.dart` configured
- [ ] `lib/core/services/` has required services
- [ ] `lib/core/services/ios_network_permission_service.dart` created
- [ ] `lib/core/errors/failures.dart` has typed failures
- [ ] `lib/core/constants/` has storage keys, legal URLs, and debug flags
- [ ] `lib/core/utils/legal_utils.dart` created
- [ ] `lib/core/providers.dart` exports all providers
- [ ] `main.dart` updated to use App()
- [ ] `main.dart` calls `triggerIOSNetworkPermission()` early
- [ ] `build_runner` executed successfully
- [ ] `flutter analyze` passes

## Related Skills

- `/init` - Run before core (project setup)
- `/auth` - Run after core (authentication)
- `/feature-init` - Initialize feature scaffolds after core
- `/design` - UI patterns reference
