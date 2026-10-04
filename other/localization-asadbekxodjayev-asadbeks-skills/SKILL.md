---
name: localization
description: Best practices for i18n / localization in web apps (i18next / react-i18next and similar). Auto-activates when adding or editing user-facing text, translation keys, locale files, language switching/routing, translating backend enums, or number/date/currency formatting. Framework-agnostic.
---

# Localization (i18n)

Goal: every user-facing string is translatable, present in **all** locales, and rendered through the i18n layer — never hardcoded. Keep keys stable and semantic; keep locale files in sync.

## Core principles

1. **No hardcoded user-facing strings.** Route every label/message through the translate function (`t('...')` / `<Trans>`). This includes placeholders, aria-labels, toasts, validation messages, empty/error states.
2. **One source of truth for languages.** Keep the supported-language list and the default/fallback in a single config module (e.g. `i18n.ts`) and import it — don't re-list languages ad hoc. A helper to validate a language code (`isLangType`) avoids bad values.
3. **Keys live in all locales.** When you add a key, add it to **every** locale file. A missing key silently falls back to the default language — easy to ship a gap. Keep file shapes identical across locales.
4. **Stable, semantic keys.** Use dot-path nesting grouped by screen/feature (`cargoList.searchPlaceholder`) plus a shared bucket for reusable strings (`common.save`). camelCase keys; reserve UPPER_SNAKE_CASE for enum-value keys.
5. **Interpolation, not concatenation.** Use `{{var}}` placeholders (`t('items.count', { count })`) instead of string concatenation, so word order can vary per language.

## Setup (i18next example)

```ts
i18n.use(httpBackend).use(initReactI18next).init({
  supportedLngs: langCodes,
  fallbackLng: DEFAULT_LANG,
  lng: savedLanguage,                  // from storage, validated
  interpolation: { escapeValue: false }, // the view layer already escapes
  backend: { loadPath: '/locales/{{lng}}.json' },
})
```
- Lazy-load locales over HTTP (`i18next-http-backend`) so the bundle isn't bloated by every language.
- Persist the chosen language (e.g. `localStorage`), validate it on read, fall back to default.
- Decide up front: **namespaces** (split large apps into multiple files per language) vs a **single flat file** with dot-path nesting. Be consistent.

## Consuming translations

```tsx
const { t, i18n } = useTranslation()
<input placeholder={t('search.placeholder')} />
<span>{t('items.count', { count })}</span>
t('actions.reset', { defaultValue: 'Reset' })   // inline fallback for safety
```
- For rich text with embedded markup, use `<Trans i18nKey="...">`.
- Pluralization: prefer i18next's plural suffixes (`key_one` / `key_other`) over hand-rolled singular/plural keys, when the i18n lib supports it.

## Translating backend enums / dynamic labels (central helper pattern)

Never render raw enum strings from the API. Write **one helper per enum domain** that normalizes the raw value and looks up a key, with a graceful default:

```ts
export function enumLabel(t: TFunction, raw: string): string {
  const key = raw.trim().toUpperCase().replace(/[\s-]+/g, '_')
  if (!key) return '—'
  return t(`<enumGroup>.${key}`, { defaultValue: raw.replace(/_/g, ' ') })
}
```
- Add each enum value as a key under its group in **all** locale files; the helper picks them up automatically.
- For values the backend itself localizes (it returns `{ names: { en, ru, … } }` or `name_en`/`name_ru`), select by current language with a fallback chain (`current → default → first available`) instead of a locale-file key.

## Language switching & routing

- If language is in the URL (e.g. `/:lang/...`), a provider should read the segment, validate it, call `changeLanguage`, persist it, and redirect bare/invalid paths to a valid prefix. Build links through typed path helpers (see [[routing-pages]]), never hardcode the prefix.
- Send the active language to the backend via a request header (e.g. `Accept-Language` / a custom `X-Language`) — see [[api-communication]]. If some languages aren't supported server-side yet, map them to a supported one for the header while still localizing fully on the client.

## Number / date / currency formatting

Use the platform `Intl` APIs (`Intl.NumberFormat`, `Intl.DateTimeFormat`) or a date lib's locale support — **not** translation keys. Map your app language codes to BCP-47 locales (e.g. `en → en-US`). Special-case currencies/units that need bespoke symbols or rounding.

## Don'ts

- Don't hardcode strings or render raw enum values in the UI.
- Don't add a key to only some locale files (creates silent fallback gaps).
- Don't build sentences by concatenation — use interpolation.
- Don't scatter the supported-language list — import it from one config.
- Don't hardcode language/route prefixes — use typed path helpers.
