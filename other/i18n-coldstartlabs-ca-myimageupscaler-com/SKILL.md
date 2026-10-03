---
name: i18n
description: Internationalization and translation management. Use when adding new translations, updating existing content, creating new language support, or working with locale routing.
---

# i18n (Internationalization)

**CRITICAL: NEVER use the Edit tool on JSON locale files.** Multi-byte UTF-8 characters (Japanese, etc.) cause crashes. ALWAYS use `apply-inline` command from the translation-helper.ts script to update translations.

## Quick Reference

### Directory Structure

```
i18n/
├── config.ts              # Locale configuration, supported locales
└── (future files)

i18n.config.ts             # next-intl request configuration

locales/
├── en/
│   └── common.json        # English translations
└── es/
    └── common.json        # Spanish translations

app/[locale]/              # Locale-aware routes
├── layout.tsx             # IntlProvider wrapper
├── page.tsx               # Homepage
└── ...                    # Other pages

middleware.ts              # Locale detection and routing
```

### Key Files

| File                           | Purpose                                                          |
| ------------------------------ | ---------------------------------------------------------------- |
| `i18n/config.ts`               | Defines `SUPPORTED_LOCALES`, `DEFAULT_LOCALE`, `isValidLocale()` |
| `i18n.config.ts`               | next-intl server config with `getRequestConfig`                  |
| `locales/{locale}/common.json` | Translation strings organized by namespace                       |
| `middleware.ts`                | Detects locale from URL/cookie/header, handles routing           |

## Adding New Translation Keys

### 1. Add to English First

Edit `locales/en/common.json`:

```json
{
  "namespace": {
    "newKey": "English text here",
    "anotherKey": "More text"
  }
}
```

### 2. Add to All Other Locales

Edit `locales/es/common.json` (and any other supported locales):

```json
{
  "namespace": {
    "newKey": "Texto en español aquí",
    "anotherKey": "Más texto"
  }
}
```

### 3. Use in Component

**Client Component:**

```tsx
'use client';
import { useTranslations } from 'next-intl';

export function MyComponent() {
  const t = useTranslations('namespace');
  return <p>{t('newKey')}</p>;
}
```

**Server Component:**

```tsx
import { getTranslations } from 'next-intl/server';

export default async function MyPage() {
  const t = await getTranslations('namespace');
  return <p>{t('newKey')}</p>;
}
```

## Translation Namespaces

Organize translations by feature/area:

| Namespace   | Purpose            | Example Keys                          |
| ----------- | ------------------ | ------------------------------------- |
| `common`    | Shared UI elements | `loading`, `error`, `submit`          |
| `nav`       | Navigation items   | `features`, `pricing`, `signIn`       |
| `footer`    | Footer content     | `privacy`, `terms`, `copyright`       |
| `homepage`  | Landing page       | `heroTitle`, `ctaButton`              |
| `dashboard` | Dashboard UI       | `credits`, `history`, `settings`      |
| `auth`      | Auth forms         | `email`, `password`, `forgotPassword` |

## Adding a New Language

### 1. Update Locale Config

Edit `i18n/config.ts`:

```typescript
export const SUPPORTED_LOCALES = ['en', 'es', 'fr'] as const; // Add 'fr'

export const locales = {
  en: { label: 'English', country: 'US' },
  es: { label: 'Español', country: 'ES' },
  fr: { label: 'Français', country: 'FR' }, // Add French
} as const;
```

### 2. Add Flag Import (if using LocaleSwitcher)

Edit `client/components/i18n/LocaleSwitcher.tsx`:

```typescript
import { US, ES, FR } from 'country-flag-icons/react/3x2';

const FlagComponents = {
  US,
  ES,
  FR, // Add FR
} as const;
```

### 3. Create Translation File

Create `locales/fr/common.json`:

```json
{
  "nav": {
    "features": "Fonctionnalités",
    "pricing": "Tarifs"
  }
  // Copy structure from en/common.json and translate
}
```

### 4. Update Layout Metadata

Edit `app/[locale]/layout.tsx` alternates:

```typescript
alternates: {
  languages: {
    en: '/',
    es: '/es/',
    fr: '/fr/', // Add French
  },
},
```

## Translating a Component

### Before (Hardcoded)

```tsx
export function PricingCard() {
  return (
    <div>
      <h2>Pro Plan</h2>
      <p>Best for professionals</p>
      <button>Get Started</button>
    </div>
  );
}
```

### After (Translated)

1. Add translations to `locales/en/common.json`:

```json
{
  "pricing": {
    "proPlan": "Pro Plan",
    "proDescription": "Best for professionals",
    "getStarted": "Get Started"
  }
}
```

2. Add to `locales/es/common.json`:

```json
{
  "pricing": {
    "proPlan": "Plan Pro",
    "proDescription": "Ideal para profesionales",
    "getStarted": "Comenzar"
  }
}
```

3. Update component:

```tsx
'use client';
import { useTranslations } from 'next-intl';

export function PricingCard() {
  const t = useTranslations('pricing');
  return (
    <div>
      <h2>{t('proPlan')}</h2>
      <p>{t('proDescription')}</p>
      <button>{t('getStarted')}</button>
    </div>
  );
}
```

## Dynamic Values & Pluralization

### Interpolation

```json
{
  "greeting": "Hello, {name}!"
}
```

```tsx
t('greeting', { name: 'John' }); // "Hello, John!"
```

### Pluralization

```json
{
  "credits": "{count, plural, =0 {No credits} =1 {1 credit} other {# credits}}"
}
```

```tsx
t('credits', { count: 5 }); // "5 credits"
```

## URL Routing Rules

| URL           | Locale | Behavior                              |
| ------------- | ------ | ------------------------------------- |
| `/`           | `en`   | English (default, no prefix)          |
| `/es/`        | `es`   | Spanish (explicit prefix)             |
| `/pricing`    | `en`   | Internally rewritten to `/en/pricing` |
| `/es/pricing` | `es`   | Spanish pricing page                  |

## Middleware Locale Detection Priority

1. **URL Path** - `/es/...` → Spanish
2. **Cookie** - `locale=es` → Spanish
3. **Accept-Language Header** - Browser preference
4. **Default** - English (`en`)

## Common Issues

### Translation Not Showing

1. Check key exists in JSON file
2. Verify namespace matches: `useTranslations('namespace')`
3. Ensure component is wrapped by `NextIntlClientProvider`
4. Check for typos in key path

### Locale Not Switching

1. Verify locale is in `SUPPORTED_LOCALES`
2. Check middleware routing logic
3. Ensure cookie is being set on switch
4. Use `window.location.href` not `router.push` for full reload

### Missing Translation Warning

If a key is missing, next-intl shows the key name. Add missing translations or use fallback:

```tsx
t('maybeNotExist', { default: 'Fallback text' });
```

## Checking Translations

### Quick Check

Run the translation checker to verify completeness:

```bash
yarn i18n:check
```

This checks all locales for:

- Missing translation files
- Missing translation keys
- Untranslated content (values identical to English)

### Script Options

The check script supports various options for targeted checks:

```bash
# Check specific locale only
yarn i18n:check --locale de

# Check specific namespace only
yarn i18n:check --namespace pricing

# Combine filters
yarn i18n:check --locale de --namespace pricing

# Output as JSON (useful for CI/CD)
yarn i18n:check --json

# Show verbose output (all checked items, not just missing)
yarn i18n:check --verbose

# Show debug info (file structure, key counts)
yarn i18n:check --debug

# Check only missing keys, not files
yarn i18n:check --keys-only

# Check only missing files, not keys
yarn i18n:check --files-only
```

### Understanding the Report

The check report shows:

| Section                  | Description                                                                       |
| ------------------------ | --------------------------------------------------------------------------------- |
| **Missing Files**        | Translation files that don't exist for a locale (e.g., `pt/pricing.json` missing) |
| **Missing Keys**         | Keys present in English but missing in other locales                              |
| **Untranslated Content** | Keys where the value matches English exactly (may need translation)               |
| **Extra Files**          | Files in locale that don't exist in English (warnings)                            |
| **Extra Keys**           | Keys in locale that don't exist in English (warnings)                             |

### CI/CD Integration

The script exits with error code 1 if issues are found, making it suitable for CI/CD:

```json
{
  "scripts": {
    "i18n:check": "tsx scripts/check-translations.ts",
    "verify": "npm run tsc && npm run lint && npm run i18n:check"
  }
}
```

### Reference Locale

- **Reference**: English (`en`) is the source of truth
- All other locales are compared against English
- Always add new keys to English first, then translate

### Common Workflows

**Before committing translations:**

```bash
yarn i18n:check
```

**After adding new translation keys:**

```bash
# Check all locales for the new keys
yarn i18n:check --namespace <your-namespace>

# Check specific locale
yarn i18n:check --locale pt --namespace <your-namespace>
```

**Debugging translation issues:**

```bash
# See full file structure and key counts
yarn i18n:check --debug

# See all checked items
yarn i18n:check --verbose
```

## Checklist for New Translations

- [ ] Added key to `locales/en/common.json`
- [ ] Added translation to all other locale files (`es`, etc.)
- [ ] Used correct namespace in component
- [ ] Tested in all supported languages
- [ ] Ran `yarn i18n:check` to verify completeness
- [ ] Ran `yarn verify` before committing
