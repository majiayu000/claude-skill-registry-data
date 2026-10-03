---
name: i18n-check
layer: stack
description: Pre-commit i18n check. Scans changed files for untranslated strings, missing locale keys, and locale sync issues. Fast and focused — only checks what changed. Use before committing or as a review add-on.
argument-hint: "[--scope <app> | --fix]"
allowed-tools: Bash, Read, Grep, Glob, Edit, Agent
---

# i18n Pre-Commit Check

Fast, focused translation check for changed files only. Catches the 4 most common i18n mistakes before they ship.

## Modes

| Invocation | What it checks |
|------------|---------------|
| `/i18n-check` | All uncommitted changed `.vue` files + their locale files |
| `/i18n-check --scope <app>` | Only files under `apps/<app>/` |
| `/i18n-check --fix` | Check + auto-fix all findings |

## What It Catches

### 1. Hardcoded Labels (Most Common)

Scan changed `.vue` files for user-visible text NOT wrapped in `$t()` or `t()`:

**Must be translated:**
- `label="..."` on `UFormField` (should be `:label="$t(...)"`)
- `title="..."` on `CroutonTableHeader` (should be `:title="$t(...)"`)
- `add-label="..."` on `CroutonFormRepeater` (should be `:add-label="$t(...)"`)
- `placeholder="..."` on inputs (should be `:placeholder="$t(...)"`)
- `dependent-label="..."` on dependent field loaders
- Static `{ label: 'Text', value: '...' }` arrays in select options (should be computed with `$t()`)
- Raw text in `<p>`, `<h1>`-`<h6>`, `<span>` that isn't interpolation or a component
- Button text content that isn't `{{ t(...) }}` or `{{ $t(...) }}`
- Tab/navigation labels in JS arrays (e.g., `{ label: 'Scheduling', value: 'scheduling' }`)

**Skip (not translatable):**
- CSS class strings, icon names (`i-lucide-*`)
- Route paths, collection names, field names in `name="..."` attributes
- Component names, event handlers
- Boolean/number props
- Dynamic `:label` already using `$t()` or `t()`
- Comments, `console.log()`, error messages in catch blocks
- Test files

### 2. Raw PascalCase/camelCase Titles

Detect table headers or page titles using raw collection names:
```vue
<!-- BAD: Raw collection name as title -->
title="BookingsLocations"
title="PagesPages"

<!-- GOOD: Translated or formatted -->
:title="$t('bookings.collections.locations.title')"
:title="useFormatCollections().collectionWithCapital('pagesPages')"
```

### 3. Locale Key Sync

For each app with changed locale files, or apps whose components were changed:
- Compare key structure across `en.json`, `nl.json`, `fr.json`
- Flag keys present in `en` but missing from `nl` or `fr`
- Flag values in `nl`/`fr` that are identical to `en` (likely untranslated copy-paste)

### 4. Missing Locale Infrastructure

If a changed `.vue` file uses `$t()` or `t()` but the layer has no locale files, flag it.

## Workflow

### Step 1: Gather changed files

```bash
# Get all changed .vue files (staged + unstaged)
git diff --name-only --diff-filter=ACMR HEAD | grep '\.vue$'
git diff --name-only --cached --diff-filter=ACMR | grep '\.vue$'
# Also check untracked .vue files
git ls-files --others --exclude-standard | grep '\.vue$'
```

If `--scope` is set, filter to `apps/<scope>/**`.

### Step 2: Scan templates for hardcoded text

For each changed `.vue` file, read it and check:

**Pattern matching (in `<template>` section only):**

```
# Hardcoded label props (should use :label with $t)
label="[A-Z].*"  on UFormField, CroutonFormReferenceSelect, etc.

# Hardcoded title props
title="[A-Z].*"  on CroutonTableHeader

# Static select option arrays in <script>
{ label: 'Text', value: '...' }  (not inside computed(() => ...))

# Tab/navigation items with static labels
{ label: 'Text', value: '...' }  in navigationItems or similar arrays
```

### Step 3: Check locale files

Find the locale directory for each changed component's layer:
```
apps/{app}/layers/{layer}/i18n/locales/{en,nl,fr}.json
```

Read all three and compare:
1. Flatten all keys to dot-notation
2. Find keys in `en` missing from `nl` and `fr`
3. Find values in `nl`/`fr` identical to `en` (possible untranslated)

### Step 4: Report

#### If clean:
```
## i18n Check: clean ✅
Checked N file(s), no translation issues found.
```

#### If issues found:
```
## i18n Check: N issue(s) found

### Hardcoded Labels (X)
| File | Line | Text | Suggested Key |
|------|------|------|---------------|
| `path/to/File.vue` | 43 | `label="Location"` | `bookings.fields.location` |

### Raw Collection Titles (X)
| File | Line | Current | Fix |
|------|------|---------|-----|
| `path/to/List.vue` | 34 | `title="BookingsLocations"` | `:title="$t('bookings.collections.locations.title')"` |

### Missing Locale Keys (X)
| Key | Missing From |
|-----|-------------|
| `bookings.fields.slot` | nl, fr |

### Possibly Untranslated (X)
| Key | Value (same as en) |
|-----|-------------------|
| `bookings.fields.name` | "Name" (nl), "Name" (fr) |
```

### Step 5: Auto-fix (if `--fix`)

When `--fix` is passed:

1. **Hardcoded labels** → Replace `label="Text"` with `:label="$t('suggested.key')"`
2. **Raw titles** → Replace with `$t()` or `useFormatCollections()`
3. **Static select arrays** → Wrap in `computed()` with `$t()` calls
4. **Missing locale keys** → Add to `nl.json`/`fr.json` with English placeholder
5. **Add `useI18n()` import** if needed for computed select options

After fixing, show what was changed and suggest the user verify translations in `nl.json`/`fr.json`.

## Key Naming Convention

When suggesting keys, follow this pattern:
```
{layer}.collections.{collection}.title    → Collection list titles
{layer}.fields.{fieldName}               → Form field labels
{layer}.actions.{actionName}             → Button/action labels
{layer}.tabs.{tabName}                   → Tab/navigation labels
{layer}.messages.{messageName}           → Helper text, toasts
{layer}.{enumGroup}.{value}              → Select option labels
```

Examples:
- `bookings.fields.location` → "Location" field label
- `bookings.actions.addTimeSlot` → "Add Time Slot" button
- `bookings.triggerTypes.booking_created` → Select option

## Integration with /commit

This check runs automatically as part of `/commit` when changed files include `.vue` files in an app with i18n configured. It runs AFTER `/sync-docs` and BEFORE the actual commit.

If issues are found:
- **With `--fix`**: Fix and include fixes in the commit
- **Without `--fix`**: Report findings and ask "Fix before committing? (y/n/skip)"

## Rules

1. **Only check changed files** — never scan the whole repo (use `/i18n-audit` for that)
2. **Suggest specific keys** — don't just say "needs translation", propose the key path
3. **Don't flag internal strings** — error messages in `catch`, `console.log`, dev-only text are fine
4. **Trust existing patterns** — if a file already uses `$t()` consistently and one label is hardcoded, that's likely an oversight worth flagging
5. **Locale files are authoritative** — if a key exists in the locale file, trust it's intentional