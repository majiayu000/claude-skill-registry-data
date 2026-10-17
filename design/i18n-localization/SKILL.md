---
name: i18n-localization
description: Internationalize properly — external strings, ICU formats, RTL, locale-aware everything, tested.
version: 1
triggers: i18n, localization, translations, rtl, internationalization, locales
category: Engineering & code
blurb: Internationalize properly — external strings, locale-aware formats, RTL support, tested.
archetype: knowledge
example: Plan internationalization for this app the right way.
---

# i18n & Localization

Global-ready means: no hardcoded text, formats that follow the locale, and layouts that survive any language. Translation is the last 10%; engineering is the other 90%.

## When to use
- Building anything user-facing that may ship in more than one language.
- Adding a language; fixing broken formats (dates, numbers, currency, plurals).
- Reviewing UI for translatability.

## Method
1. **Externalize everything**: all user-visible strings in resources with stable keys; zero concatenation — word order varies by language; full sentences are translation units.
2. **Formats via platform APIs**: `Intl`-class formatting for dates, times, numbers, currency, lists, relative time; never hand-rolled masks; store timestamps in UTC, render local.
3. **Plurals & grammar**: ICU MessageFormat (plural/select); never `count + " items"`; gender/declension handled where the language requires it.
4. **Layout that flexes**: language length variance (+30–100%); no fixed-width text containers; buttons wrap safely; test with pseudo-localization (accented, elongated) before real translations.
5. **RTL readiness**: logical CSS properties (start/end, not left/right) where RTL is possible; mirrored icons reviewed; one RTL smoke locale if in scope.
6. **Content workflow**: TMS or controlled files; glossaries for product terms (brand names untranslated); context notes for translators; machine translation drafts → human review for anything shipped.
7. **Locale testing**: pseudo-loc pass in CI where possible; per-locale unit tests for formats; screenshots of key screens per language on changes.

## Quality gates
- [ ] No hardcoded UI strings; lint catches them.
- [ ] Dates/numbers/currency via locale APIs with tests.
- [ ] Pseudo-localization pass done; layout survives long strings.
- [ ] Glossary respected; brand terms protected.

## Red lines
- No string concatenation for grammar; no raw machine translation shipped unreviewed for legal or sensitive text.

## Related
`ux-ui-design` · `frontend-engineering` · `technical-writing`.
