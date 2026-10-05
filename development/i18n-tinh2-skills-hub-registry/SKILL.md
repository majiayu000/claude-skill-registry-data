---
name: i18n
description: "Set up internationalization by extracting all hardcoded user-facing strings to locale files. Triggers: you need to add multi-language support, extract hardcoded strings, set up locale files."
version: "2.0.1"
category: ux
platforms:
  - CLAUDE_CODE
---

You are in AUTONOMOUS MODE. Do NOT ask questions. Execute the full pipeline below
without pausing for user input. Make reasonable decisions using sensible defaults.

PURPOSE:
Set up complete internationalization (i18n) for the current project. Auto-detect the
framework, scan for all hardcoded user-facing strings, extract them to locale files,
install and configure the appropriate i18n library, and handle pluralization, interpolation,
date/number formatting, and RTL layout support.

INPUT:
$ARGUMENTS

The user may specify:
1. Target locales -- e.g., "en,es,fr,de,ja,ar" (default: "en" as base locale).
2. A specific i18n library preference.
3. Scope -- specific directories or screens to process.
4. RTL support -- explicitly request Arabic/Hebrew layout handling.
If no arguments, set up English as the base locale with extraction of all hardcoded strings.

============================================================
PHASE 1 -- FRAMEWORK AND I18N LIBRARY DETECTION
============================================================

Detect the framework and determine the appropriate i18n library:

| Indicator | Framework | I18n Library |
|-----------|-----------|-------------|
| pubspec.yaml | Flutter | flutter_localizations + intl / easy_localization |
| next.config.* with i18n or package.json with "next" | Next.js | next-intl or next-i18next |
| package.json with "react" (no next) | React | react-intl (FormatJS) or react-i18next |
| package.json with "vue" | Vue | vue-i18n |
| package.json with "@angular/core" | Angular | @angular/localize or ngx-translate |
| package.json with "svelte" | Svelte | svelte-i18n |
| Podfile or *.xcodeproj | iOS (Swift) | NSLocalizedString + Localizable.strings |
| build.gradle with android | Android (Kotlin) | strings.xml resources |

Check for existing i18n setup:
- Existing locale files (en.json, messages_en.arb, Localizable.strings)
- Existing i18n library in dependencies
- Existing translation function usage (t(), $t(), intl.message, etc.)

If an i18n library is already configured, extend it rather than replacing it.

Record: FRAMEWORK, I18N_LIBRARY, LOCALE_DIR, BASE_LOCALE, TARGET_LOCALES

============================================================
PHASE 2 -- STRING EXTRACTION SCAN
============================================================

Scan the entire source tree for hardcoded user-facing strings.

Step 2.1 -- Identify User-Facing Strings

Search for strings that are displayed to users:
- **Text content:** String literals inside Text(), <p>, <span>, <h1-h6>, <label>, <button>,
  placeholder, title, aria-label, alt text, tooltip, snackbar, toast, dialog content
- **Error messages:** Strings in error handlers, validation messages, catch blocks
- **Labels:** Form labels, button text, navigation items, tab labels, menu items
- **Status text:** Loading messages, empty states, success/failure messages
- **Notifications:** Push notification titles and bodies, in-app alerts

For each string found, record:
- The string value
- File path and line number
- Context (button label, heading, body text, error message, placeholder, etc.)
- Whether it contains dynamic values that need interpolation

Step 2.2 -- Exclude Non-User-Facing Strings

Do NOT extract:
- Log messages (console.log, logger.info, print for debug)
- Code identifiers (route paths, CSS class names, enum values)
- API endpoints and URLs
- Environment variable names
- Test assertions and test data
- Comments and documentation
- String constants used only for programmatic logic (switch cases, map keys)

Step 2.3 -- Generate Translation Key Map

For each extracted string, generate a namespaced translation key:
- Use dot-notation namespacing: `screen.section.element`
- Examples:
  - "Save Changes" on profile screen -> `profile.actions.save`
  - "No items found" empty state -> `items.empty.title`
  - "Are you sure?" delete dialog -> `common.dialog.confirmDelete`
  - "{{count}} items selected" -> `items.selectedCount` (with interpolation)

Group keys by screen/feature for maintainability.
Use a `common` namespace for strings reused across screens (OK, Cancel, Save, Delete, etc.).

Produce the key map:
| Key | English Value | Context | Interpolation | File |
|-----|--------------|---------|---------------|------|

============================================================
PHASE 3 -- LOCALE FILE GENERATION
============================================================

Step 3.1 -- Create Base Locale File

Generate the locale file in the format appropriate for the detected library:

**JSON format** (react-intl, next-intl, vue-i18n, svelte-i18n):
Create `src/locales/en.json` or `messages/en.json`:
```json
{
  "common": {
    "actions": {
      "save": "Save",
      "cancel": "Cancel",
      "delete": "Delete"
    }
  },
  "profile": {
    "title": "My Profile",
    "actions": {
      "save": "Save Changes"
    }
  }
}
```

**ARB format** (Flutter):
Create `lib/l10n/app_en.arb`:
```json
{
  "@@locale": "en",
  "commonSave": "Save",
  "@commonSave": { "description": "Save action button" },
  "itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}",
  "@itemCount": { "description": "Item count with pluralization", "placeholders": { "count": { "type": "int" } } }
}
```

**Localizable.strings** (iOS):
Create `en.lproj/Localizable.strings`.

**strings.xml** (Android):
Create `res/values/strings.xml`.

Step 3.2 -- Handle Interpolation

Convert strings with dynamic values to use the library's interpolation syntax:
- react-intl: `{count} items` or ICU format `{count, plural, one {# item} other {# items}}`
- next-intl: `{count} items`
- vue-i18n: `{count} items` or `@:common.save`
- Flutter intl: `{count, plural, =0{No items} =1{1 item} other{{count} items}}`
- i18next: `{{count}} items` with `count` option

Step 3.3 -- Handle Pluralization

Identify strings that represent countable items and apply plural rules:
- English: one/other
- Languages with more forms (e.g., Arabic has zero/one/two/few/many/other)

Use ICU MessageFormat where the library supports it.

Step 3.4 -- Generate Target Locale Files

For each target locale beyond the base:
1. Create the locale file with the same key structure.
2. Copy English values as placeholders with a `[TRANSLATE]` prefix.
3. Set common values that are universal (OK, Email, etc.) to their known translations.

Example: `src/locales/es.json` with `"commonSave": "[TRANSLATE] Save"`.

Commit: "feat(i18n): generate locale files with extracted strings"

============================================================
PHASE 4 -- I18N LIBRARY SETUP
============================================================

Step 4.1 -- Install Dependencies

Install the i18n library and any required dependencies:
- **react-intl:** `npm install react-intl`
- **next-intl:** `npm install next-intl`
- **vue-i18n:** `npm install vue-i18n`
- **angular:** `ng add @angular/localize`
- **Flutter:** Add `flutter_localizations`, `intl` to pubspec.yaml
- **i18next:** `npm install i18next react-i18next`

Use the project's package manager (npm/yarn/pnpm based on lockfile).

Step 4.2 -- Configure Provider/Plugin

Set up the i18n provider at the application root:

**React/Next.js (react-intl):**
- Create `src/i18n/config.ts` with locale detection and message loading
- Wrap the app root with `<IntlProvider>`
- Configure locale detection from browser or URL

**Next.js (next-intl):**
- Update `next.config.*` with i18n locale configuration
- Create middleware for locale routing
- Set up `NextIntlClientProvider` in root layout

**Vue:**
- Create `src/i18n/index.ts` with createI18n configuration
- Register plugin in main app entry

**Flutter:**
- Add `localizationsDelegates` and `supportedLocales` to MaterialApp
- Generate localization files with `flutter gen-l10n`
- Create `l10n.yaml` configuration file

**Angular:**
- Configure `angular.json` with i18n locales
- Set up LOCALE_ID provider

Step 4.3 -- Configure Date and Number Formatting

Set up locale-aware formatting:
- **Dates:** Use Intl.DateTimeFormat (web) or DateFormat (Flutter) with locale parameter
- **Numbers:** Use Intl.NumberFormat (web) or NumberFormat (Flutter) with locale parameter
- **Currency:** Configure currency display per locale
- Create formatting utility functions that accept locale as parameter

Step 4.4 -- RTL Layout Support (if Arabic, Hebrew, or Urdu in target locales)

If any RTL locale is requested:
- **CSS:** Add `[dir="rtl"]` selectors or use logical properties (`margin-inline-start` instead of `margin-left`)
- **Flutter:** Wrap directional widgets with `Directionality` or use `TextDirection.rtl`
- **Next.js:** Set `dir` attribute on `<html>` based on locale
- Configure text alignment to use `start`/`end` instead of `left`/`right`
- Mirror horizontal icons (arrows, chevrons) for RTL
- Test that layouts do not break with RTL text direction

Commit: "feat(i18n): configure i18n library with locale detection and formatting"

============================================================
PHASE 5 -- STRING REPLACEMENT
============================================================

Replace all hardcoded strings in the codebase with translation function calls:

Step 5.1 -- Replace Strings

For each extracted string, replace the hardcoded value with the i18n function:
- **react-intl:** `<FormattedMessage id="key" />` or `intl.formatMessage({ id: 'key' })`
- **next-intl:** `t('key')` or `<NextIntlClientProvider>`
- **vue-i18n:** `{{ $t('key') }}` or `t('key')` in setup
- **Flutter:** `AppLocalizations.of(context)!.keyName`
- **i18next:** `t('key')` or `<Trans i18nKey="key" />`
- **Angular:** `{{ 'key' | translate }}` or `$localize`

Step 5.2 -- Handle Interpolated Strings

Replace strings with dynamic values:
```
// Before
`Welcome, ${user.name}!`

// After (react-intl)
intl.formatMessage({ id: 'greeting.welcome' }, { name: user.name })

// After (Flutter)
AppLocalizations.of(context)!.greetingWelcome(user.name)
```

Step 5.3 -- Handle Conditional Strings

Replace pluralized or conditional strings:
```
// Before
`${count} item${count !== 1 ? 's' : ''}`

// After (react-intl with ICU)
intl.formatMessage({ id: 'items.count' }, { count })
// In locale file: "{count, plural, one {# item} other {# items}}"
```

Commit per screen or feature module:
- "fix(i18n): extract strings from [screen/module] to locale keys"

============================================================
PHASE 6 -- VERIFICATION
============================================================

Step 6.1 -- Static Analysis

Run the appropriate linter/analyzer:
- Flutter: `flutter analyze` and `flutter gen-l10n`
- TypeScript: `tsc --noEmit`
- Framework linter if configured

Fix all errors introduced by the i18n integration.

Step 6.2 -- String Coverage Audit

Re-scan the codebase for any remaining hardcoded user-facing strings:
- Report strings found vs strings extracted
- Coverage percentage
- List any intentionally skipped strings with rationale

Step 6.3 -- Locale File Validation

Verify locale files:
- All keys present in base locale exist in every target locale
- No orphaned keys (keys in locale file not used in code)
- ICU message syntax is valid
- Interpolation placeholders match between locales


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing fixes, re-validate:

1. Re-run the specific UX/accessibility checks that originally found issues.
2. Run the project's test suite to verify fixes didn't break functionality.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat up to 3 iterations.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context

============================================================
OUTPUT
============================================================

```
## I18n Setup Complete

### Framework: [detected]
### I18n Library: [library]
### Base Locale: [locale]
### Target Locales: [list]

### Files Created/Modified
| File | Purpose |
|------|---------|
| [path] | [description] |

### String Extraction Summary
| Category | Count |
|----------|-------|
| Total strings found | N |
| Strings extracted | N |
| Strings skipped (non-user-facing) | N |
| Unique translation keys | N |
| Common/shared keys | N |
| Keys with interpolation | N |
| Keys with pluralization | N |

### Locale File Status
| Locale | Keys | Translated | Needs Translation |
|--------|------|-----------|-------------------|
| en | N | N (base) | 0 |
| es | N | N | N |

### Coverage
- Screens processed: N/N
- Strings replaced: N/N (N%)
- Remaining hardcoded: N (with rationale)
```

============================================================
NEXT STEPS
============================================================

After i18n setup:
- Translate the `[TRANSLATE]`-prefixed values in each target locale file.
- "Run `/ux` to audit UX quality including localized content."
- "Run `/responsive` to verify layouts do not break with longer translated strings."
- "Run `/design-system` to ensure text styles accommodate variable-length translations."
- For professional translations, export locale files to a translation management platform (Crowdin, Lokalise, Phrase).


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /i18n — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT extract log messages, debug strings, or code-only identifiers -- these are not user-facing.
- Do NOT use auto-translation APIs to fill in target locales -- use placeholder markers instead.
- Do NOT create deeply nested key structures beyond 3 levels -- keep keys flat and scannable.
- Do NOT use string concatenation for translated text -- use interpolation placeholders.
- Do NOT hardcode locale names in conditional logic -- use the i18n library's locale detection.
- Do NOT skip pluralization for countable items -- different languages have different plural rules.
- Do NOT remove the original English strings from code comments -- they serve as context for translators.
- Do NOT overwrite existing locale files without reading them first -- merge new keys into existing files.
- Do NOT assume left-to-right layout -- use logical CSS properties and directional-aware widgets.
