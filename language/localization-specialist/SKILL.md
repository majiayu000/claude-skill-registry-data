---
name: localization-specialist
description: Internationalization (i18n) and localization (l10n) implementation for
  web and mobile applications. Use when asked to add multi-language support, set up
  i18n frameworks (i18next, react-intl, Flask-Babel), extract strings for translation,
  handle RTL languages, implement locale-aware date/number/currency formatting, or
  manage translation files.
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: development
  tags:
  - i18n
  - l10n
  - localization
  - internationalization
  - translation
  - rtl
---

# Localization Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `add multi-language support`, `i18n`, `l10n`.
- The requested work fits this skill's lane: i18n setup, translation file management, RTL support, locale-aware formatting.
- The request needs this domain's specific workflow, checks, or deliverable shape rather than a neighboring specialist.

## First actions
1. `Glob('**/locales/**', '**/i18n/**', '**/translations/**', '**/*.po', '**/*.ftl')` — find existing locale files
2. Identify i18n framework in use (i18next, react-intl, GNU gettext, etc.)
3. Identify target languages and whether RTL support is needed

## Decision rules
- If an i18n framework is already in use: extend its conventions instead of introducing a second localization system.
- If user-facing dates, numbers, or currencies are involved: use locale-aware formatting utilities rather than string templates.
- If strings are hardcoded in code or templates: extract them before translation work begins.

## Output contract
- Translation files in correct format for the framework (JSON for i18next, PO files for gettext, etc.)
- Extracted strings use namespaced keys (not flat strings)
- RTL layout changes documented separately from translation changes

## Constraints
- NEVER hardcode translated copy in multiple places when a shared translation key should be used instead.
- NEVER assume left-to-right layout only; check RTL impact anywhere layout or spacing is language-sensitive.
- Scope boundary: copywriting and marketing tone decisions belong to the relevant content or marketing skill.

## Reference
- `references/legacy-agent.md`: i18n framework patterns, string extraction, RTL implementation, locale formatting
