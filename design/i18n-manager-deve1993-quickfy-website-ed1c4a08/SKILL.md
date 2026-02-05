---
name: i18n-manager
description: Expert in internationalization (i18n) and localization (l10n) with i18next, react-intl, multi-language support, RTL layouts, locale-specific formatting, translation management, and automated text extraction
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Internationalization Manager

Expert skill for building multi-language applications with complete i18n/l10n support. Specializes in i18next, react-intl, RTL layouts, locale formatting, translation workflows, and automated text extraction.

## Core Capabilities

### 1. i18n Setup & Configuration
- **i18next**: Most popular i18n framework
- **react-i18next**: React integration
- **react-intl**: FormatJS implementation
- **next-i18next**: Next.js integration
- **vue-i18n**: Vue.js integration
- **Language Detection**: Browser, URL, cookie
- **Namespace Organization**: Modular translations

### 2. Translation Management
- **JSON Format**: Simple key-value translations
- **Nested Keys**: Hierarchical organization
- **Pluralization**: ICU message format
- **Interpolation**: Dynamic values in translations
- **Context**: Gender, formality variations
- **Fallback**: Missing translation handling
- **Lazy Loading**: Load translations on demand

### 3. RTL (Right-to-Left) Support
- **Arabic**: العربية
- **Hebrew**: עברית
- **Persian**: فارسی
- **Urdu**: اردو
- **CSS Logical Properties**: start/end vs left/right
- **Mirroring**: Icons, layouts, animations
- **BiDi Text**: Mixed LTR/RTL content

### 4. Locale-Specific Formatting
- **Dates**: Intl.DateTimeFormat
- **Numbers**: Intl.NumberFormat
- **Currency**: Format with symbols
- **Relative Time**: "2 hours ago"
- **Lists**: Conjunction formatting
- **Phone Numbers**: Country-specific formats
- **Addresses**: Locale-specific orders

### 5. Text Extraction & Automation
- **Hardcoded Text Detection**: Find non-i18n strings
- **Key Generation**: Auto-generate translation keys
- **Missing Translations**: Detect untranslated keys
- **Unused Keys**: Find and remove dead translations
- **Translation Coverage**: Report per-language coverage
- **CI/CD Integration**: Automated checks

### 6. Translation Workflow
- **Developer Flow**: Mark strings for translation
- **Translator Flow**: Provide context and examples
- **Review Flow**: Approval process
- **Update Flow**: Handle translation updates
- **Version Control**: Track translation changes
- **Translation Services**: Crowdin, Lokalise, POEditor

### 7. SEO & Performance
- **URL Localization**: /en/about, /es/acerca
- **Meta Tags**: Translated titles, descriptions
- **hreflang**: Search engine language hints
- **Language Switcher**: User language selection
- **Code Splitting**: Load only needed translations
- **Caching**: CDN and browser caching

## Workflow

### Phase 1: i18n Planning
1. **Define Requirements**
   - Which languages? (start with 2-3)
   - RTL support needed?
   - Date/currency formats?
   - Translation workflow?

2. **Choose Solution**
   - i18next (flexible, popular)
   - react-intl (FormatJS, enterprise)
   - Custom solution
   - Library integration

3. **Plan Structure**
   - Translation file organization
   - Namespace strategy
   - Key naming convention
   - Fallback language

### Phase 2: Implementation
1. **Setup i18n**
   - Install dependencies
   - Configure i18n
   - Create translation files
   - Add language detector

2. **Add Translations**
   - Extract hardcoded text
   - Generate translation keys
   - Create base language
   - Add fallback translations

3. **Implement RTL**
   - Add dir="rtl" support
   - Convert CSS to logical properties
   - Mirror icons/images
   - Test layout

4. **Add Formatting**
   - Date formatting
   - Number formatting
   - Currency formatting
   - Relative time

### Phase 3: Translation Workflow
1. **Developer Tools**
   - Missing key warnings
   - Translation extraction
   - Key generation scripts
   - Hot reload translations

2. **Translator Tools**
   - Translation platform integration
   - Context screenshots
   - Translation memory
   - Plural/gender rules

3. **Quality Assurance**
   - Translation coverage reports
   - Unused key detection
   - Consistency checks
   - Automated tests

## Implementation Patterns

### i18next Setup

```typescript
// i18n.ts
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'
import Backend from 'i18next-http-backend'

i18n
  // Load translations from backend
  .use(Backend)
  // Detect user language
  .use(LanguageDetector)
  // Pass i18n instance to react-i18next
  .use(initReactI18next)
  // Initialize
  .init({
    // Fallback language
    fallbackLng: 'en',

    // Supported languages
    supportedLngs: ['en', 'es', 'fr', 'de', 'ar', 'he'],

    // Debug mode (development only)
    debug: process.env.NODE_ENV === 'development',

    // Interpolation options
    interpolation: {
      escapeValue: false, // React already escapes
    },

    // Backend options
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },

    // Detection options
    detection: {
      order: ['querystring', 'cookie', 'localStorage', 'navigator'],
      caches: ['localStorage', 'cookie'],
    },

    // Namespaces
    ns: ['common', 'auth', 'dashboard'],
    defaultNS: 'common',

    // React options
    react: {
      useSuspense: true,
    },
  })

export default i18n
```

### Translation Files

```json
// public/locales/en/common.json
{
  "app": {
    "title": "My Application",
    "description": "Welcome to our amazing app"
  },
  "navigation": {
    "home": "Home",
    "about": "About",
    "contact": "Contact"
  },
  "actions": {
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete",
    "confirm": "Confirm"
  },
  "messages": {
    "success": "Operation completed successfully",
    "error": "An error occurred",
    "loading": "Loading..."
  },
  "validation": {
    "required": "This field is required",
    "email": "Please enter a valid email",
    "minLength": "Must be at least {{count}} characters"
  }
}

// public/locales/en/auth.json
{
  "login": {
    "title": "Log In",
    "email": "Email Address",
    "password": "Password",
    "submit": "Log In",
    "forgotPassword": "Forgot password?",
    "noAccount": "Don't have an account?",
    "signUp": "Sign up"
  },
  "register": {
    "title": "Create Account",
    "submit": "Sign Up",
    "hasAccount": "Already have an account?",
    "logIn": "Log in"
  }
}
```

### Using Translations in Components

```tsx
// Component.tsx
import { useTranslation } from 'react-i18next'

export function Welcome() {
  const { t, i18n } = useTranslation('common')

  return (
    <div>
      {/* Simple translation */}
      <h1>{t('app.title')}</h1>
      <p>{t('app.description')}</p>

      {/* Translation with interpolation */}
      <p>{t('validation.minLength', { count: 8 })}</p>

      {/* Current language */}
      <p>Language: {i18n.language}</p>

      {/* Change language */}
      <button onClick={() => i18n.changeLanguage('es')}>
        Español
      </button>
    </div>
  )
}
```

### Pluralization

```json
// Pluralization in i18next (ICU format)
{
  "items": "{{count}} item",
  "items_one": "{{count}} item",
  "items_other": "{{count}} items",

  // Complex pluralization
  "cart": {
    "zero": "Your cart is empty",
    "one": "You have {{count}} item in your cart",
    "other": "You have {{count}} items in your cart"
  }
}
```

```tsx
// Usage
const { t } = useTranslation()

<p>{t('items', { count: 0 })}</p>  // "0 items"
<p>{t('items', { count: 1 })}</p>  // "1 item"
<p>{t('items', { count: 5 })}</p>  // "5 items"
```

### Context-Aware Translations

```json
{
  "friend": "Friend",
  "friend_male": "Friend (male)",
  "friend_female": "Friend (female)",

  "welcome": "Welcome",
  "welcome_formal": "Welcome (formal)",
  "welcome_informal": "Hi there!"
}
```

```tsx
// Usage with context
const { t } = useTranslation()

<p>{t('friend', { context: 'male' })}</p>  // "Friend (male)"
<p>{t('welcome', { context: 'formal' })}</p>  // "Welcome (formal)"
```

### RTL Support

```tsx
// RTLProvider.tsx
import { useEffect } from 'react'
import { useTranslation } from 'react-i18next'

const RTL_LANGUAGES = ['ar', 'he', 'fa', 'ur']

export function RTLProvider({ children }: { children: React.ReactNode }) {
  const { i18n } = useTranslation()

  useEffect(() => {
    const isRTL = RTL_LANGUAGES.includes(i18n.language)
    document.documentElement.dir = isRTL ? 'rtl' : 'ltr'
    document.documentElement.lang = i18n.language
  }, [i18n.language])

  return <>{children}</>
}

// App.tsx
import { RTLProvider } from './RTLProvider'

function App() {
  return (
    <RTLProvider>
      <YourApp />
    </RTLProvider>
  )
}
```

### RTL-Aware CSS

```css
/* ❌ BAD - Hard-coded direction */
.sidebar {
  margin-left: 20px;
  text-align: left;
}

/* ✅ GOOD - Logical properties (auto RTL) */
.sidebar {
  margin-inline-start: 20px;
  text-align: start;
}

/* ✅ GOOD - RTL-specific rules */
[dir="rtl"] .sidebar {
  margin-right: 20px;
  margin-left: 0;
}

/* ✅ GOOD - CSS logical properties */
.container {
  padding-inline: 20px;      /* horizontal padding */
  padding-block: 10px;       /* vertical padding */
  border-inline-start: 1px;  /* left border (LTR), right border (RTL) */
  border-inline-end: 1px;    /* right border (LTR), left border (RTL) */
}
```

### Date Formatting

```tsx
// DateFormatter.tsx
import { useTranslation } from 'react-i18next'

export function DateFormatter({ date }: { date: Date }) {
  const { i18n } = useTranslation()

  // Automatic locale-based formatting
  const formatted = new Intl.DateTimeFormat(i18n.language, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date)

  return <time dateTime={date.toISOString()}>{formatted}</time>
}

// Usage
<DateFormatter date={new Date('2024-01-15')} />
// en: "January 15, 2024"
// es: "15 de enero de 2024"
// fr: "15 janvier 2024"
// de: "15. Januar 2024"
```

### Number & Currency Formatting

```tsx
// NumberFormatter.tsx
import { useTranslation } from 'react-i18next'

export function CurrencyFormatter({
  amount,
  currency = 'USD',
}: {
  amount: number
  currency?: string
}) {
  const { i18n } = useTranslation()

  const formatted = new Intl.NumberFormat(i18n.language, {
    style: 'currency',
    currency,
  }).format(amount)

  return <span>{formatted}</span>
}

// Usage
<CurrencyFormatter amount={1234.56} currency="USD" />
// en-US: "$1,234.56"
// de-DE: "1.234,56 $"
// fr-FR: "1 234,56 $US"

<CurrencyFormatter amount={1234.56} currency="EUR" />
// en-US: "€1,234.56"
// de-DE: "1.234,56 €"
// fr-FR: "1 234,56 €"
```

### Language Switcher

```tsx
// LanguageSwitcher.tsx
import { useTranslation } from 'react-i18next'

const LANGUAGES = [
  { code: 'en', name: 'English', flag: '🇬🇧' },
  { code: 'es', name: 'Español', flag: '🇪🇸' },
  { code: 'fr', name: 'Français', flag: '🇫🇷' },
  { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
  { code: 'ar', name: 'العربية', flag: '🇸🇦', rtl: true },
  { code: 'he', name: 'עברית', flag: '🇮🇱', rtl: true },
]

export function LanguageSwitcher() {
  const { i18n } = useTranslation()

  const changeLanguage = async (lng: string) => {
    await i18n.changeLanguage(lng)

    // Update URL (optional)
    const url = new URL(window.location.href)
    url.searchParams.set('lng', lng)
    window.history.pushState({}, '', url)

    // Update dir attribute
    const isRTL = LANGUAGES.find((l) => l.code === lng)?.rtl
    document.documentElement.dir = isRTL ? 'rtl' : 'ltr'
  }

  return (
    <div className="language-switcher">
      <select
        value={i18n.language}
        onChange={(e) => changeLanguage(e.target.value)}
        aria-label="Select language"
      >
        {LANGUAGES.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.flag} {lang.name}
          </option>
        ))}
      </select>
    </div>
  )
}
```

### Translation Extraction Script

```typescript
// scripts/extract-translations.ts
import fs from 'fs'
import path from 'path'
import { glob } from 'glob'

interface Translation {
  key: string
  defaultValue: string
  file: string
  line: number
}

async function extractTranslations() {
  const translations: Translation[] = []

  // Find all source files
  const files = await glob('src/**/*.{ts,tsx}')

  for (const file of files) {
    const content = fs.readFileSync(file, 'utf-8')
    const lines = content.split('\n')

    // Find t('key') or t("key") calls
    const tRegex = /t\(['"]([^'"]+)['"]/g
    const matches = content.matchAll(tRegex)

    for (const match of matches) {
      const key = match[1]
      const lineNumber = content.substring(0, match.index).split('\n').length

      translations.push({
        key,
        defaultValue: '', // Extract from default value if present
        file,
        line: lineNumber,
      })
    }
  }

  // Group by namespace
  const byNamespace: Record<string, Translation[]> = {}

  for (const trans of translations) {
    const [namespace] = trans.key.split('.')
    if (!byNamespace[namespace]) {
      byNamespace[namespace] = []
    }
    byNamespace[namespace].push(trans)
  }

  // Output JSON files
  for (const [namespace, keys] of Object.entries(byNamespace)) {
    const outputPath = path.join('public', 'locales', 'en', `${namespace}.json`)

    // Load existing translations
    let existing: Record<string, any> = {}
    if (fs.existsSync(outputPath)) {
      existing = JSON.parse(fs.readFileSync(outputPath, 'utf-8'))
    }

    // Add new keys
    for (const { key } of keys) {
      const keyPath = key.split('.')
      let current = existing

      for (let i = 1; i < keyPath.length; i++) {
        const part = keyPath[i]
        if (i === keyPath.length - 1) {
          if (!current[part]) {
            current[part] = `TODO: Translate ${key}`
          }
        } else {
          if (!current[part]) {
            current[part] = {}
          }
          current = current[part]
        }
      }
    }

    // Write back
    fs.writeFileSync(outputPath, JSON.stringify(existing, null, 2))
  }

  console.log(`✅ Extracted ${translations.length} translation keys`)
}

extractTranslations()
```

### Missing Translation Detection

```typescript
// scripts/check-translations.ts
import fs from 'fs'
import path from 'path'

const SUPPORTED_LANGUAGES = ['en', 'es', 'fr', 'de', 'ar', 'he']
const NAMESPACES = ['common', 'auth', 'dashboard']

function loadTranslations(lang: string, namespace: string): Record<string, any> {
  const filePath = path.join('public', 'locales', lang, `${namespace}.json`)

  if (!fs.existsSync(filePath)) {
    return {}
  }

  return JSON.parse(fs.readFileSync(filePath, 'utf-8'))
}

function getAllKeys(obj: Record<string, any>, prefix = ''): string[] {
  let keys: string[] = []

  for (const [key, value] of Object.entries(obj)) {
    const fullKey = prefix ? `${prefix}.${key}` : key

    if (typeof value === 'object' && value !== null) {
      keys = keys.concat(getAllKeys(value, fullKey))
    } else {
      keys.push(fullKey)
    }
  }

  return keys
}

function checkTranslations() {
  const baseLanguage = 'en'
  let hasErrors = false

  for (const namespace of NAMESPACES) {
    const baseTranslations = loadTranslations(baseLanguage, namespace)
    const baseKeys = new Set(getAllKeys(baseTranslations))

    console.log(`\n📦 Namespace: ${namespace}`)
    console.log(`   Base keys (${baseLanguage}): ${baseKeys.size}`)

    for (const lang of SUPPORTED_LANGUAGES) {
      if (lang === baseLanguage) continue

      const translations = loadTranslations(lang, namespace)
      const keys = new Set(getAllKeys(translations))

      // Missing keys
      const missing = Array.from(baseKeys).filter((key) => !keys.has(key))

      // Extra keys (not in base)
      const extra = Array.from(keys).filter((key) => !baseKeys.has(key))

      if (missing.length > 0 || extra.length > 0) {
        hasErrors = true
        console.log(`\n   ❌ ${lang}:`)

        if (missing.length > 0) {
          console.log(`      Missing ${missing.length} keys:`)
          missing.slice(0, 5).forEach((key) => console.log(`        - ${key}`))
          if (missing.length > 5) {
            console.log(`        ... and ${missing.length - 5} more`)
          }
        }

        if (extra.length > 0) {
          console.log(`      Extra ${extra.length} keys:`)
          extra.slice(0, 5).forEach((key) => console.log(`        - ${key}`))
        }
      } else {
        console.log(`   ✅ ${lang}: Complete (${keys.size} keys)`)
      }
    }
  }

  if (hasErrors) {
    console.log('\n❌ Translation check failed\n')
    process.exit(1)
  } else {
    console.log('\n✅ All translations are complete!\n')
  }
}

checkTranslations()
```

## Best Practices

### Translation Keys
```typescript
// ✅ GOOD - Hierarchical, descriptive keys
t('auth.login.title')
t('dashboard.widgets.revenue.title')
t('errors.validation.required')

// ❌ BAD - Flat, unclear keys
t('loginTitle')
t('title1')
t('err1')
```

### Context & Examples
```json
{
  "button": {
    "save": "Save",
    "_comment": "Button text for saving changes",
    "_example": "Click 'Save' to save your changes"
  }
}
```

### Avoid HTML in Translations
```json
// ❌ BAD
{
  "message": "Click <a href='/help'>here</a> for help"
}

// ✅ GOOD
{
  "message": "Click {{link}} for help",
  "link": "here"
}
```

```tsx
// Usage
<Trans i18nKey="message">
  Click <a href="/help">{{link: t('link')}}</a> for help
</Trans>
```

### Pluralization
```json
{
  "items_zero": "No items",
  "items_one": "{{count}} item",
  "items_other": "{{count}} items"
}
```

### Gender & Formality
```json
{
  "welcome_male": "Welcome, Mr. {{name}}",
  "welcome_female": "Welcome, Ms. {{name}}",
  "welcome_formal": "Good day, {{name}}",
  "welcome_informal": "Hey {{name}}!"
}
```

## When to Use This Skill

Activate this skill when you need to:
- Add multi-language support to an application
- Setup i18next or react-intl
- Implement RTL layouts
- Extract hardcoded text for translation
- Create translation management workflows
- Add locale-specific formatting (dates, numbers, currency)
- Build language switchers
- Integrate with translation services (Crowdin, Lokalise)
- Detect missing translations
- Optimize i18n performance

## Integration with Agents

```typescript
// Agent Explore → Find all hardcoded strings
// i18n-manager → Extract and create translation keys

// Example workflow:
1. Agent scans codebase for hardcoded text
2. Agent finds: 150 strings not using t()
3. i18n-manager generates translation keys
4. i18n-manager creates JSON files for all languages
5. Agent verifies: All text now translatable
```

## Output Format

When implementing i18n, provide:
1. **Complete i18n Setup**: Configuration files
2. **Translation Files**: JSON with all keys
3. **Component Integration**: How to use translations
4. **RTL Support**: CSS and layout changes
5. **Extraction Scripts**: Automated text extraction
6. **Testing Guide**: How to test translations
7. **Documentation**: Translation workflow for team

Always build applications that are accessible to users worldwide in their native language.
