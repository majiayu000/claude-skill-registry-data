---
name: i18n
description: i18n/l10n — locale detection, translations, pluralization, RTL.
---

## Locale Detection Order

Resolve the active locale by checking sources in this priority order:

1. URL prefix (`/fr/checkout`, `/en-US/dashboard`)
2. Query parameter (`?lang=fr`)
3. `Accept-Language` HTTP header (parse quality values, e.g., `fr-CH, fr;q=0.9, en;q=0.8`)
4. Stored user preference (DB or cookie)
5. Default locale (configured at app level, e.g., `en`)

Always persist a resolved locale to the user profile once they are authenticated so subsequent sessions skip header parsing.

## Translation File Structure

Organize one file per locale per domain. Never put all keys in a single monolithic file.

```
locales/
  en/
    auth.json
    checkout.json
    common.json
    errors.json
  fr/
    auth.json
    checkout.json
    ...
```

- Load only the domains needed for the current page
- Use lazy loading for large locale bundles (import on route change)
- Commit all locale files together — never merge a feature without all locale files updated

## Key Naming Conventions

- Use flat dot-notation: `user.welcome_message`, `checkout.order_summary_title`
- Keys must be descriptive, not positional: `form.submit_button` not `label_4`
- Use snake_case for key segments
- Namespace by feature/domain prefix: `auth.`, `billing.`, `common.`
- Never reuse a key across contexts with different meanings

## Pluralization

- Use ICU Message Format or the framework's built-in plural rules (i18next, react-intl, formatjs, vue-i18n)
- Never concatenate strings to build plural sentences:

```
// Wrong
`You have ${count} ${count === 1 ? 'item' : 'items'}`

// Correct — ICU format
"cart.item_count": "{count, plural, one {# item} other {# items}}"
```

- Handle zero as a distinct plural category when the UX calls for it (`zero {No items}`)
- Languages have 2–6 plural forms; always defer to CLDR rules, not assumptions

## Date and Number Formatting

- Always use `Intl.DateTimeFormat` and `Intl.NumberFormat` — never manual string building
- Pass the active locale and relevant options:

```js
new Intl.DateTimeFormat('fr-FR', { dateStyle: 'long' }).format(date)
new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(amount)
```

- Never hardcode month names, AM/PM, decimal separators, or thousands separators
- Store all timestamps as ISO 8601 UTC in the backend; format for the user's locale on the frontend

## Currency Handling

- Store monetary amounts as integers (cents / minor units): `1999` for $19.99
- Never store amounts as floats — floating-point arithmetic introduces rounding errors
- Always store the currency code alongside the amount: `{ amount: 1999, currency: "USD" }`
- Format for display only; use `Intl.NumberFormat` with `style: 'currency'`
- Display the currency code (`USD`) alongside the symbol (`$`) for international audiences to avoid ambiguity

## RTL (Right-to-Left) Support

- Use CSS logical properties throughout — never directional properties:

| Avoid | Use instead |
|-------|------------|
| `margin-left` | `margin-inline-start` |
| `padding-right` | `padding-inline-end` |
| `text-align: left` | `text-align: start` |
| `border-left` | `border-inline-start` |
| `float: left` | `float: inline-start` |

- Set `dir="rtl"` on the `<html>` element for RTL locales
- Test layouts in Arabic (`ar`) and Hebrew (`he`) — mirroring is often imperfect without explicit testing
- Icons with directional meaning (arrows, chevrons) must be flipped in RTL

## Missing Key Fallback

- Fall through to the default locale when a key is missing in the active locale
- Log missing keys to the console in development; send to a monitoring service in production
- Never render raw key strings to end users (e.g., `"checkout.submit_button"`)
- Track translation coverage per locale; block merges when coverage drops below a threshold (e.g., 95%)

## Backend Responsibilities

- Store the user's locale preference in the database (`user.locale`)
- Return all dates and timestamps as ISO 8601 UTC strings (`2026-05-10T14:30:00Z`)
- Return currency amounts as integers with an explicit currency code
- Never format dates or numbers for a specific locale in API responses — let the frontend handle formatting
- Accept `Accept-Language` on all API endpoints for locale-sensitive responses (e.g., localized product names)
