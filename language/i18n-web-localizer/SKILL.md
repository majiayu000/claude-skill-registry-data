---
name: i18n-web-localizer
description: Expert internationalization (i18n) implementation for React, Vite, and Next.js web applications with French and English language support. Use when the user asks to (1) add multilingual/bilingual support to a web app, (2) implement French and/or English translations, (3) create language toggle/switcher components, (4) refactor an existing app for i18n, (5) set up translation files and locale management, (6) implement Next.js internationalized routing, or (7) configure react-i18next or next-intl. Triggers on mentions of "bilingual", "multilingual", "i18n", "internationalization", "localization", "translate", "French/English toggle", "language switcher", or requests to support multiple languages in React/Vite/Next.js applications.
---

# i18n Web Localizer

Expert skill for implementing internationalization in React, Vite, and Next.js applications with French (Canadian) and English support.

## Core Workflow

### Step 1: Analyze the Project

Before implementation:

1. Identify framework: React+Vite, Next.js App Router, or Next.js Pages Router
2. Scan components for hardcoded text
3. Check for existing i18n setup
4. Determine routing requirements (URL-based vs cookie/localStorage)

### Step 2: Choose Library

| Framework | Primary Library | Docs |
|-----------|-----------------|------|
| React + Vite | react-i18next | react.i18next.com |
| Next.js App Router | next-intl | next-intl-docs.vercel.app |
| Next.js Pages Router | next-i18next | github.com/i18next/next-i18next |

### Step 3: Implementation

**React + Vite**: See [references/react-vite-i18n.md](references/react-vite-i18n.md)

**Next.js**: See [references/nextjs-i18n.md](references/nextjs-i18n.md)

### Step 4: Extract and Translate

1. Identify all user-facing strings
2. Create translation keys using dot notation
3. Populate translation files
4. Follow [references/translation-guidelines.md](references/translation-guidelines.md)

### Step 5: Implement Language Toggler

See `assets/togglers/` for ready-to-use components.

## Translation File Structure

```
locales/
├── en/
│   ├── common.json
│   └── [page].json
└── fr/
    ├── common.json
    └── [page].json
```

## Key Naming Convention

Use dot notation: `{namespace}.{section}.{element}`

```json
{
  "nav.home": "Home",
  "button.submit": "Submit",
  "error.required": "This field is required",
  "page.home.title": "Welcome"
}
```

## Refactoring Checklist

- [ ] Install dependencies
- [ ] Create i18n config
- [ ] Set up translation files (en/, fr/)
- [ ] Replace hardcoded strings with `t()` calls
- [ ] Add language toggler
- [ ] Handle date/number formatting
- [ ] Configure SSR/SSG (Next.js)
- [ ] Test both languages
- [ ] Set up language persistence

## Quick Reference

### react-i18next

```tsx
import { useTranslation } from 'react-i18next';

function Component() {
  const { t, i18n } = useTranslation();
  return (
    <div>
      <h1>{t('page.title')}</h1>
      <button onClick={() => i18n.changeLanguage('fr')}>FR</button>
    </div>
  );
}
```

### next-intl (App Router)

```tsx
import { useTranslations } from 'next-intl';

export default function Page() {
  const t = useTranslations('HomePage');
  return <h1>{t('title')}</h1>;
}
```

## Critical Notes

- Set `<html lang={locale}>` for accessibility
- French strings are 20-30% longer than English—test layouts
- Use `fr-CA` for French Canadian
- Handle missing translations with fallbacks
- Use ICU format for pluralization
