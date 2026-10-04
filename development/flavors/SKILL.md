---
name: flavors
description: Configure environment flavors (dev, staging, prod) for Flutter apps. Sets up compile-time variables via --dart-define-from-file, Gradle productFlavors, Xcode schemes, and per-environment configuration. Use when adding multi-environment support or separating dev/staging/prod builds.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Flavors - Environment Configuration

Configure dev, staging, and production environments with separate configurations, bundle IDs, and app names.

## When to Use This Skill

- Setting up multiple environments (dev, staging, prod)
- Separating API endpoints per environment
- Using different bundle IDs for each environment
- Configuring environment-specific Firebase/Supabase projects
- User asks "add flavors", "setup environments", "separate dev/prod"

## When NOT to Use This Skill

- Single environment projects - Use `/init` with single `.env`
- CI/CD setup - Use `/ci-cd` after flavors are configured
- Basic Firebase setup - Use `/analytics` first, then add per-flavor config

## Important: Migration from flutter_dotenv

**This skill REPLACES `flutter_dotenv` runtime loading with compile-time variables.**

If your project uses `/init`'s approach (`await dotenv.load()`), running `/flavors` will:
1. Remove `flutter_dotenv` dependency
2. Replace `.env` runtime loading with `--dart-define-from-file` build flags
3. Create `FlavorConfig` class using `String.fromEnvironment()`

**Why compile-time?** Secrets are not bundled in the app binary - they're injected at build time.

## Integration with /core

**FlavorConfig** handles:
- Flavor identification (`isDev`, `isProd`, `isStaging`)
- Per-flavor API URLs and service credentials

**DebugConstants** (from `/core`) handles:
- Debug/mock flags (`useMockAuth`, `useMockApi`)
- Logging and UI debug options

Keep feature flags in `DebugConstants`, flavor config in `FlavorConfig`.

## Questions to Ask

1. **Flavor count:** How many environments? (dev + prod, dev + staging + prod)
2. **Bundle ID pattern:** How should bundle IDs differ? (suffix: .dev)
3. **App name pattern:** How should app names differ? (suffix: " (Dev)")
4. **Firebase:** Separate Firebase projects per flavor? (yes/no)
5. **Supabase:** Separate Supabase projects per flavor? (yes/no)

## Quick Reference

| Flavor | Bundle ID Suffix | App Name Suffix | Purpose |
|--------|------------------|-----------------|---------|
| **dev** | `.dev` | ` (Dev)` | Local development |
| **staging** | `.staging` | ` (Staging)` | QA/testing |
| **prod** | *(none)* | *(none)* | Production release |

### Key Commands

```bash
flutter run --flavor dev --dart-define-from-file=.env.dev
flutter run --flavor prod --dart-define-from-file=.env.prod
dart run .claude/skills/flavors/scripts/check.dart
```

## Workflow

### Phase 1: Gather Requirements

Confirm: flavor count, base bundle ID, base app name, Firebase/Supabase per flavor.

### Phase 2: Create Environment Files

Create `.env.{flavor}` files. See `templates/env-files/`.

### Phase 3: Configure Android

Update `android/app/build.gradle`. See [android-guide.md](android-guide.md).

### Phase 4: Configure iOS

Create xcconfig files and Xcode schemes. See [ios-guide.md](ios-guide.md).

### Phase 5: Create FlavorConfig

Generate `lib/core/config/flavor_config.dart` from `reference/flavor_config.dart`.

### Phase 6: Migrate main.dart

Remove `flutter_dotenv`, use `FlavorConfig`. See `reference/main_flavored.dart`.

### Phase 7: Update .gitignore

Add `.env.dev`, `.env.staging`, `.env.prod`.

### Phase 8: Verify Setup

```bash
dart run .claude/skills/flavors/scripts/check.dart
flutter build apk --flavor dev --dart-define-from-file=.env.dev
```

## Guides

| Guide | Content |
|-------|---------|
| [android-guide.md](android-guide.md) | Gradle productFlavors, signing configs |
| [ios-guide.md](ios-guide.md) | Xcode schemes, xcconfig files |
| [firebase-guide.md](firebase-guide.md) | Per-flavor Firebase setup (see `/analytics` for basic setup) |
| [checklist.md](checklist.md) | Verification checklist |

## Templates

| Template | Purpose |
|----------|---------|
| `templates/env-files/` | .env.dev, .env.staging, .env.prod |
| `templates/android/` | build.gradle flavor config |
| `templates/ios/` | xcconfig files |
| `templates/vscode/` | launch.json configurations |

## Checklist

**Environment Files:**
- [ ] `.env.dev` and `.env.prod` exist
- [ ] All `.env.*` files in `.gitignore`
- [ ] `flutter_dotenv` removed from pubspec.yaml (if migrating)

**Android:**
- [ ] `build.gradle` has `flavorDimensions` and `productFlavors`
- [ ] Each flavor has `applicationIdSuffix` and `resValue` app name

**iOS:**
- [ ] `Dev.xcconfig` and `Prod.xcconfig` exist
- [ ] Xcode schemes created for each flavor

**Dart:**
- [ ] `lib/core/config/flavor_config.dart` exists
- [ ] `main.dart` does NOT use `dotenv.load()`
- [ ] `main.dart` uses `FlavorConfig`

**Build:**
- [ ] `flutter build apk --flavor dev` succeeds
- [ ] `flutter build apk --flavor prod` succeeds

## Related Skills

- `/init` - Creates project with single `.env` (flavors replaces this approach)
- `/core` - DebugConstants for mock/debug flags (complementary to FlavorConfig)
- `/ci-cd` - Add flavor-aware CI/CD pipelines after this skill
- `/analytics` - Basic Firebase setup; use before per-flavor config
- `/release` - Prepare production flavor for app stores

## Common Issues

### "Flavor not found" Error

Ensure flavor names match exactly in `build.gradle`, iOS schemes, and `.env.{flavor}` files.

### Environment Variables Empty

Using `dotenv.env['KEY']`? Switch to `String.fromEnvironment('KEY')`.

### Build works but wrong config

Ensure you're passing `--dart-define-from-file=.env.{flavor}` flag.

## Next Steps

1. `/ci-cd` - Update GitHub Actions for multi-flavor builds
2. `/analytics` - Configure per-flavor Firebase Analytics
3. `/release` - Prepare production signing
