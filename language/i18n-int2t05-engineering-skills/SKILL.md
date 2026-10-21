---
name: i18n
description: Implement or audit localization for supported product locales. Triggers on "i18n", "国际化".
---

# Internationalization (i18n)

## When to use

- Implement or audit localization for supported product locales.

**Not for:** frontend-design for general layout.

## Steps

1. Identify actual locales, tooling, translation ownership and affected surfaces.

2. Extract messages and use locale-aware pluralization, dates, numbers and routing in the actual rendering model.

3. Handle expansion, fonts, accessibility and fallbacks; add or test RTL only when relevant to supported locales.

4. Exercise translations, missing messages, locale persistence and relevant server/client boundaries.

## Verify

- Supported messages and formatting are correct; routing and layout evidence covers actual locale requirements.

## References

- [engineering-principles.md](../../../references/engineering-principles.md) — shared decision boundaries, scope and verification.
- [references/i18n-checklist.md](references/i18n-checklist.md) — locale-surface audit template, ICU syntax reference, RTL conversion checklist, locale-detection patterns, test-locale matrix
- [references/server-i18n.md](references/server-i18n.md) — RSC / App Router message loading, per-locale bundle splitting, request-scoped locale, hydration alignment
