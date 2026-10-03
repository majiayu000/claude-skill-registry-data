---
name: i18n
description: Internationalization and localization practices. Use when adding user-facing text, formatting dates/numbers/currency, building layouts that might need to support other languages, or reviewing code for hardcoded locale assumptions.
---

# Internationalization (i18n) & localization (l10n)

Build as if a second language is coming, even if only one ships today — retrofitting
i18n later means touching every string in the codebase; doing it from the start costs
almost nothing.

## Core rules

- **No hardcoded user-facing strings in logic/markup.** Route every user-facing
  string through a translation/lookup layer (whatever the stack's standard is —
  `i18next`/`react-intl`/`FormatJS` for web, `.strings`/`Localizable.xcstrings` for
  iOS, resource files for Android, `gettext`/`babel` for Python) — even before a
  second locale actually exists. A string concatenated from parts ("You have " + n +
  " items") breaks translation and pluralization; use a single template/message
  with placeholders instead.
- **Never format dates, numbers, or currency by hand.** Use the platform's
  locale-aware formatter (`Intl.DateTimeFormat`/`Intl.NumberFormat` on
  web/Node, `NumberFormatter`/`DateFormatter` on iOS, `ICU`-backed formatters
  elsewhere) instead of manual string interpolation — locale changes decimal
  separators, digit grouping, date order, and calendar system, not just the
  language of labels.
- **Currency is not just a number.** Store amounts with an explicit currency code
  (ISO 4217) alongside the value; format with the locale-aware currency formatter,
  which also handles the symbol placement and decimal precision correctly per
  currency (not all currencies have 2 decimal places).
- **Pluralization is not `n === 1 ? "" : "s"`.** Many languages have more plural
  categories than English (zero/one/two/few/many/other) — use the i18n library's
  plural/ICU MessageFormat support rather than hand-rolled conditionals.
- **Don't assume text length or direction.** Translated strings can run 30–200%
  longer than English; layouts must reflow, not truncate/overlap. If right-to-left
  languages are in scope, use logical CSS properties (`margin-inline-start` not
  `margin-left`) or the platform equivalent instead of hardcoded left/right.
- **Timezones**: store instants in UTC, convert to the user's local timezone only at
  display time; never store a "local" timestamp without its offset/zone.
- **Sorting/collation** is locale-dependent (e.g. accented characters, CJK) — use the
  platform's locale-aware collator instead of a raw byte/codepoint sort for anything
  user-facing.

## What not to over-engineer

If a project is genuinely single-locale with no plan to expand, don't build a full
translation pipeline for its own sake — but still avoid hand-formatted
dates/numbers/currency, since that's about correctness (locale of the *user's
machine*, not just language) even for a single-language product.

## When reviewing

Grep for string concatenation building user-facing text, manual date/number string
building (`toFixed`, hand-built date strings), and hardcoded `"$"`/comma-as-thousands
assumptions — these are the most common silent i18n bugs.
