---
name: i18n
description: Audit Flutter code for hardcoded strings, write clear user-friendly text following UX guidelines, and migrate strings to i18n files. Use when checking localization, finding hardcoded text, improving string clarity, writing error messages, button labels, or any user-facing text.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# i18n - Localization & UX Writing

Ensure all user-facing text is localized and crystal clear. Every string should be understandable by a 10-year-old or non-native English speaker.

## When to Use This Skill

- Checking for hardcoded strings
- Writing or improving user-facing text
- Creating error messages, button labels, confirmations
- Migrating strings to i18n files
- Reviewing string quality

## Quick Reference

### The Golden Rules

1. **Be specific, not vague** - "Could not save photo" not "Error occurred"
2. **Use plain words** - "Sign in" not "Authenticate"
3. **Buttons complete "I want to ___"** - "Delete photo" not "OK"
4. **Errors say what to do** - "Check your connection and try again"
5. **No confusing dialogs** - Never [Cancel] [OK] on a cancel confirmation

### File Structure

```
lib/
├── core/i18n/
│   ├── common.i18n.yaml        → t.common.*
│   └── translations.g.dart     → Generated
└── features/{feature}/i18n/
    └── {feature}.i18n.yaml     → t.{feature}.*
```

### Commands

```bash
# Audit for hardcoded strings
dart run .claude/skills/i18n/scripts/check.dart --audit

# Audit specific feature
dart run .claude/skills/i18n/scripts/check.dart --audit auth

# Generate missing i18n files
dart run .claude/skills/i18n/scripts/check.dart --generate

# Regenerate translations
dart run build_runner build --delete-conflicting-outputs
```

## Workflow

### 1. Audit

```bash
dart run .claude/skills/i18n/scripts/check.dart --audit {feature}
```

Look for: `Text('...')`, `title:`, `hintText:`, `label:`, SnackBar messages, Dialog content.

### 2. Evaluate & Improve

Check each string against [ux-writing-guide.md](ux-writing-guide.md). Use patterns from [examples.md](examples.md).

### 3. Add to i18n File

Create/update `lib/features/{feature}/i18n/{feature}.i18n.yaml` with proper strings.

### 4. Replace in Code

```dart
// Before: Text('Welcome back')
// After:  Text(t.auth.login.title)
```

### 5. Regenerate

```bash
dart run build_runner build --delete-conflicting-outputs
```

## Guides

| Guide | Use For |
|-------|---------|
| [setup-guide.md](setup-guide.md) | Initial slang setup, build.yaml, file structure |
| [ux-writing-guide.md](ux-writing-guide.md) | UX writing principles, patterns |
| [examples.md](examples.md) | Before/after examples by scenario |

## Checklist

- [ ] A 10-year-old would understand it
- [ ] Names the specific thing (photo, message, account)
- [ ] If error: says what happened AND what to do
- [ ] If button: completes "I want to ___"
- [ ] If confirmation: buttons clearly show outcomes
- [ ] No jargon (credentials, authenticate, invalid, terminate)

## Related Skills

- `/a11y` - Accessibility labels (add to `accessibility:` section in i18n files)
