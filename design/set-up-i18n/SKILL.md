---
name: set-up-i18n
description: Use when internationalizing a frontend project — sets up i18next + react-i18next (React) or vue-i18n (Vue) with typed message keys, lazy-loaded per-locale catalogs, Intl-based number/date/relative formatting, and a persisted locale choice detected from the browser.
---

# Set Up i18n

## 1. Audit current state

```bash
cat .claude/stack-profile.md 2>/dev/null || cat ~/.claude/stack-profile.md 2>/dev/null   # frontend.framework, frontend.meta, package_manager
grep -E '"(i18next|react-i18next|vue-i18n)"' package.json 2>/dev/null
ls src/locales 2>/dev/null
grep -rn ">[A-Z][a-z]\+ [a-z]" src/components 2>/dev/null | head   # hardcoded UI strings (rough)
```

Read `frontend.framework` (react → i18next, vue → vue-i18n) and `frontend.meta`: `nuxt` → `@nuxtjs/i18n`, `next` → `next-intl` or the framework's routing i18n; this skill is the Vite-SPA path. Commands use pnpm; translate for `package_manager`. **Prerequisite:** `@/` alias. The locale switcher is UI state (per `set-up-state-management`).

## 2. Decide what to do
- No i18n → full setup.
- Library present, strings still hardcoded → extract to catalogs (step 5) + type the keys (step 7).
- Set up, no lazy loading → split catalogs per locale (step 6).

## 3. Detect framework
React → **i18next** + **react-i18next**. Vue → **vue-i18n** (Composition API). Both format with the **`Intl`** APIs. Why these libraries: `i18n-patterns.md`.

## 4. Install

### React
```bash
pnpm add i18next react-i18next
```
### Vue
```bash
pnpm add vue-i18n
```

## 5. Message catalogs

```
src/locales/
├── en/common.json
└── de/common.json
```
```json
// src/locales/en/common.json
{
  "greeting": "Hello, {{name}}",
  "todos": { "count_one": "{{count}} todo", "count_other": "{{count}} todos" }
}
```
Keys are namespaced and use interpolation + plurals — never concatenate sentence fragments.

**Default locale pair: `de` + `en`.** Both catalogs ship from day one with the same keys; `en` is the fallback (and the type source for keys). German strings run ~30 % longer — design components to wrap, never to fit one English word. Use the informal or formal German address consistently per product (`du` vs `Sie`), decided once in the catalog, not per string.

## 6. Initialize (with the default locale only; lazy-load the rest)

```ts
// src/libs/i18n.ts (React)
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from '@/locales/en/common.json';

export const SUPPORTED_LOCALES = ['de', 'en'] as const;
export type Locale = (typeof SUPPORTED_LOCALES)[number];
const browser = navigator.language.split('-')[0];
export const initialLocale: Locale = SUPPORTED_LOCALES.includes(browser as Locale)
  ? (browser as Locale)
  : 'en';

i18n.use(initReactI18next).init({
  resources: { en: { common: en } },
  lng: 'en', // switched to initialLocale by loadLocale() at boot — no untranslated flash
  fallbackLng: 'en',
  defaultNS: 'common',
  interpolation: { escapeValue: false }, // React already escapes
});

export async function loadLocale(lng: Locale) {
  if (!i18n.hasResourceBundle(lng, 'common')) {
    const messages = await import(`@/locales/${lng}/common.json`);
    i18n.addResourceBundle(lng, 'common', messages.default);
  }
  await i18n.changeLanguage(lng);
}

export default i18n;
```
Only `en` ships in the bundle (the `@/` alias in the dynamic `import()` must be an absolute path in `vite.config.ts`, as the `configure-typescript` alias setup has it; Vite prints an `INEFFECTIVE_DYNAMIC_IMPORT` notice for `en` because it is also imported statically — harmless, `loadLocale` skips it); `main.tsx` awaits `loadLocale(persistedLocale ?? initialLocale)` before the first render, so a German visitor never sees English first. `persistedLocale` comes from the locale store (step 9); `initialLocale` covers first visits. In Nuxt/Next, `navigator` does not exist on the server — use `@nuxtjs/i18n` / the request's `Accept-Language` instead of this module. Vue: `createI18n({ legacy: false, locale, fallbackLocale: 'en', messages: { en } })` + dynamic `import()` + `i18n.global.setLocaleMessage` to lazy-add.

## 7. Type the keys (autocomplete + no missing-key bugs)

```ts
// src/types/i18next.d.ts (React)
import 'i18next';
import type common from '@/locales/en/common.json';

declare module 'i18next' {
  interface CustomTypeOptions {
    defaultNS: 'common';
    resources: { common: typeof common };
  }
}
```
Now `t('greeting')` autocompletes and `t('typo')` is a type error. Limit: i18next infers interpolation variables only from `as const` TS resources or `.d.ts` interfaces, not from JSON, so `t('greeting', { nam: 'x' })` is not caught.

Vue (vue-i18n 11): declare the schema globally from the default catalog. Do not use `createI18n<[MessageSchema], 'en' | 'de'>` here: it requires every listed locale in `messages`, which defeats lazy loading.
```ts
// src/libs/i18n.ts
import { createI18n } from 'vue-i18n';
import enMessages from '@/locales/en/common.json';

declare module 'vue-i18n' {
  export interface DefineLocaleMessage extends Readonly<typeof enMessages> {}
}

export const i18n = createI18n({
  legacy: false, // Composition API
  locale: 'en',
  fallbackLocale: 'en',
  messages: { en: enMessages },
});
```
Limit (checked against vue-i18n 11.4): `t()` accepts any string key, so the schema gives autocomplete and typed results, **not** a compile error on `t('typo')`. Close the gap in lint with `@intlify/eslint-plugin-vue-i18n` (`no-missing-keys`) and with the key-parity test in `i18n-patterns.md`. Vue catalogs use `{name}` and pipe plurals (`"no todos | one todo | {count} todos"`), not the `{{name}}` / `_one` form from step 5.

## 8. Format with `Intl`, not by hand

```ts
new Intl.NumberFormat(locale, { style: 'currency', currency: 'EUR' }).format(amount);
new Intl.DateTimeFormat(locale, { dateStyle: 'medium' }).format(date);
new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-1, 'day'); // "yesterday"
```
i18next (`t('k', { val, formatParams })`) and vue-i18n (`$n`/`$d`) wrap `Intl` — use those or `Intl` directly. Never hand-roll date/number/plural logic.

## 9. Locale switch = persisted UI state

A small store holds the chosen locale; switching lazy-loads then sets it:
```ts
// on switch: await loadLocale(next); store.setLocale(next);  (loadLocale also changes the language)
document.documentElement.lang = next; // screen readers pick the voice from <html lang>; see set-up-document-head
```
Persist the choice (like the theme store) and default to the browser locale on first visit.

## 10. Verify
```bash
pnpm typecheck   # typed keys compile; a wrong key fails
pnpm dev            # switch locale → catalog lazy-loads, strings + formats update
```

## References
- ./i18n-patterns.md — typed keys, lazy loading, Intl formatting, locale-is-UI-state, plurals/interpolation, extraction, when to skip.
- ../_shared/glossary.md — locale choice as UI state.
- ../_shared/conventions.md — `@/` alias, `libs/` seam.
