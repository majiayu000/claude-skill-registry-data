---
name: nuxt-ui-tools-i18n
description: Use this skill for internal i18n work in this repository. Covers locale ownership, provider wiring, lazy schema text contracts, and the maintenance surfaces that must stay in sync when package or playground translations change.
---

# nuxt-ui-tools I18n Maintainer

Use this skill for internal repository work involving:

- `src/runtime/i18n/*`
- package-owned table or spreadsheet copy
- locale message structure
- lazy schema text support
- playground translation architecture
- consumer guidance around translations

## Canonical Read Order

Read first:

- `AGENTS.md`
- `.agents/skills/nuxt-ui-tools-maintainer/SKILL.md`

Then inspect:

- `src/runtime/i18n/types.ts`
- `src/runtime/i18n/locales/*.ts`
- `src/runtime/i18n/use-locale.ts`
- the owning runtime utils/components for the text surface you are changing

## Ownership Rules

There are two different translation paths in this repository.

### Package-owned UI copy

This is the built-in chrome owned by `ui-tools`, for example:

- table footer labels
- filter operator labels
- column-panel labels
- spreadsheet step chrome
- built-in empty states and actions

This copy belongs in:

- `src/runtime/i18n/types.ts`
- `src/runtime/i18n/locales/en.ts`
- `src/runtime/i18n/locales/fr.ts`

Resolve this copy through `useUiToolsLocale()`.

Do not leave hardcoded English strings inside runtime components when the package owns the wording.

### Schema-owned copy

This is consumer-provided text such as:

- table column labels
- filter labels and placeholders
- date preset labels and descriptions
- spreadsheet step scenario text
- option labels sourced from app data

This copy must stay translation-friendly by contract.

Preferred public surface:

- `string`
- `number`
- `() => string | number`

Only widen further when a surface genuinely needs rendered content.

## Non-Negotiable Rule

If a schema text surface is raw-string-only and blocks consumer i18n, fix the owning type and owning resolver.

Do not:

- wrap the entire schema in `computed(() => defineSchema(...))`
- duplicate state to force locale updates
- add one-off bilingual helpers in the playground

## Locale Structure

Keep locale messages grouped by feature and sub-feature.

Preferred shape:

- `table.header.*`
- `table.footer.*`
- `table.filters.panel.*`
- `spreadsheet.steps.review.*`

Do not dump unrelated labels into flat objects.

## Runtime Checklist

When adding a new package-owned text surface:

1. add the message key to `src/runtime/i18n/types.ts`
2. add English and French values
3. replace the hardcoded runtime string with `t('...')`
4. verify the affected playground route in both `en` and `fr`

When refactoring or removing an i18n surface:

1. delete locale keys that are no longer used
2. delete the matching fields from the centralized message interface
3. delete any helpers or dead code branches that only existed for those keys

Do not keep stale locale entries around after UI changes.

Unused translation keys are misleading maintenance debt and should be cleaned up in the same task that made them obsolete.

When widening a schema surface for i18n:

1. update the relevant public type
2. update the owning normalize/resolve utility
3. update any components that assumed a raw string
4. replace playground demo literals with translation keys through `() => t('...')`
5. update consumer skills

## Playground Rule

The playground is part of the validation surface.

If a demo route includes visible scenario text, workbook headers, example labels, or schema-owned UI copy, keep it translatable with real translation keys.

Do not treat the playground as exempt from i18n just because it is demo content.
