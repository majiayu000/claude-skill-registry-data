---
name: feature-init
description: Initialize new feature with Clean Architecture folder structure and skeleton files. Creates scaffold for domain, data, and presentation layers with TODOs. Use AFTER /plan to create the initial structure, then run /domain and /data to fill in details.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Feature Init - Initialize Feature Structure

Initialize a new feature with Clean Architecture folder structure and skeleton files. Creates the scaffold, then `/domain` and `/data` fill in the details.

## When to Use This Skill

- Creating a new feature from scratch (after `/plan`)
- User asks to "create feature", "init feature", "scaffold feature", or "add new feature"
- Starting a new feature module

## Dependency Rules

```
┌─────────────┐
│   Domain    │  ← No dependencies (pure Dart, no Flutter)
└──────┬──────┘
       │
   ┌───┴───┐
   ▼       ▼
┌──────┐ ┌──────────────┐
│ Data │ │ Presentation │  ← Both depend on Domain only
└──────┘ └──────────────┘
```

Data and Presentation must NEVER depend on each other.

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Feature folder | snake_case | `user_profile` |
| Entity | `{Feature}` | `UserProfile` |
| Repository interface | `{Feature}Repository` | `UserProfileRepository` |
| Repository impl | `{Feature}RepositoryImpl` | `UserProfileRepositoryImpl` |
| Model (DTO) | `{Feature}Model` | `UserProfileModel` |
| State | `{Feature}State` | `UserProfileState` |
| Notifier | `{Feature}Notifier` | `UserProfileNotifier` |
| Screen | `{Feature}Screen` | `UserProfileScreen` |

## Commands

```bash
# Check all features and completeness
dart run .claude/skills/feature-init/scripts/check.dart

# Generate new feature (recommended)
dart run .claude/skills/feature-init/scripts/check.dart --generate feature_name

# Validate dependencies
dart run .claude/skills/feature-init/scripts/check.dart --validate feature_name
```

## Workflow

### 1. Gather Requirements

Ask: Feature name (snake_case)? What does it do? What screens? Needs API?

### 2. Generate Scaffold

Use the script or [templates.md](templates.md) to create skeleton files:
- `domain/entities/` - Pure domain model (skeleton)
- `domain/repositories/` - Interface (skeleton)
- `data/models/` - DTO skeleton with `toEntity()`/`fromEntity()`
- `data/repositories/` - Implementation skeleton
- `presentation/providers/` - State + Notifier skeleton
- `presentation/screens/` - Consumer widget skeleton
- `i18n/` - Localization template

### 3. Hand Off to Specialized Skills

After scaffolding, direct user to fill in details:
1. `/domain {feature}` - Fill in domain layer details (entities, enums, interfaces)
2. `/data {feature}` - Fill in data layer details (DTOs, repository impl, API calls)
3. `/i18n {feature}` - Add localized strings
4. `/testing {feature}` - Create test files
5. `/design` - Polish the UI
6. `/a11y` - Add Semantics widgets
7. Add route to `app_router.dart`
8. Add repository provider to `core/providers.dart`
9. Run `dart run build_runner build`

## Feature Types

**Standard (Default)**: Full domain + data + presentation. Use for most features - even "simple" ones like onboarding need data persistence.

**Data-Only**: Domain + data without screens. Use for shared services (analytics, notifications).

## Guides

| Guide | Use For |
|-------|---------|
| [templates.md](templates.md) | Skeleton templates, naming conventions, checklist |
| [examples.md](examples.md) | Complete "bookmarks" feature example |
| [scripts/check.dart](scripts/check.dart) | Automated scaffold generation and validation |

## Checklist

- [ ] Feature folder created with snake_case name
- [ ] Domain layer: entity, repository interface created
- [ ] Data layer: model with `toEntity()`/`fromEntity()`, repository impl
- [ ] Presentation layer: state, notifier, screen
- [ ] i18n template created at `i18n/{feature}.i18n.yaml`
- [ ] Route added to `app_router.dart`
- [ ] Repository provider added to `core/providers.dart`
- [ ] `build_runner` executed successfully
- [ ] No circular dependencies between layers

## Related Skills

- `/plan` - Run BEFORE this skill to plan feature requirements
- `/domain` - Run AFTER to fill in domain layer details
- `/data` - Run AFTER to fill in data layer implementation
- `/presentation` - Run AFTER to fill in presentation layer (states, notifiers, screens)
- `/i18n` - Add localized strings
- `/testing` - Create test files
- `/design` - Polish UI components
- `/a11y` - Add accessibility support
