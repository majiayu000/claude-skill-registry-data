---
name: i18n-setup-wizard
description: Sets up complete internationalization infrastructure for React, Vue, Next.js, or vanilla JS with framework config, translation files, and language switching. Use when user asks to "setup i18n", "add translations", "multi-language support", or "internationalization setup".
allowed-tools: [Read, Write, Bash, Glob]
---

# i18n Setup Wizard

Complete internationalization setup with framework configs, translation files, and language switching.

## When to Use

- "Setup i18n for React"
- "Add multi-language support"
- "Configure internationalization"
- "Setup translations"
- "Add language switcher"

## Instructions

### 1. Detect Framework

```bash
# Check framework
grep "react" package.json && echo "React"
grep "next" package.json && echo "Next.js"
grep "vue" package.json && echo "Vue"
```

### 2. Install i18n Library

## React (react-i18next)

```bash
npm install react-i18next i18next i18next-http-backend i18next-browser-languagedetector
```

**Setup i18n.js:**
```javascript
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'
import Backend from 'i18next-http-backend'

i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    debug: process.env.NODE_ENV === 'development',
    interpolation: {
      escapeValue: false, // React already escapes
    },
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },
  })

export default i18n
```

**App.jsx:**
```javascript
import './i18n'
import { Suspense } from 'react'

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <YourApp />
    </Suspense>
  )
}
```

**Component usage:**
```javascript
import { useTranslation } from 'react-i18next'

function MyComponent() {
  const { t, i18n } = useTranslation()

  return (
    <div>
      <h1>{t('welcome.title')}</h1>
      <p>{t('welcome.description')}</p>

      <button onClick={() => i18n.changeLanguage('es')}>
        Español
      </button>
    </div>
  )
}
```

## Next.js (next-i18next)

```bash
npm install next-i18next react-i18next i18next
```

**next.config.js:**
```javascript
const { i18n } = require('./next-i18next.config')

module.exports = {
  i18n,
}
```

**next-i18next.config.js:**
```javascript
module.exports = {
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'es', 'fr', 'de'],
  },
}
```

**_app.js:**
```javascript
import { appWithTranslation } from 'next-i18next'

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}

export default appWithTranslation(MyApp)
```

**Page:**
```javascript
import { useTranslation } from 'next-i18next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'

export default function Home() {
  const { t } = useTranslation('common')

  return <h1>{t('welcome')}</h1>
}

export async function getStaticProps({ locale }) {
  return {
    props: {
      ...(await serverSideTranslations(locale, ['common'])),
    },
  }
}
```

## Vue (vue-i18n)

```bash
npm install vue-i18n@9
```

**i18n.js:**
```javascript
import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import es from './locales/es.json'

const i18n = createI18n({
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    es,
  },
})

export default i18n
```

**main.js:**
```javascript
import { createApp } from 'vue'
import App from './App.vue'
import i18n from './i18n'

createApp(App)
  .use(i18n)
  .mount('#app')
```

**Component:**
```vue
<template>
  <div>
    <h1>{{ $t('welcome.title') }}</h1>
    <p>{{ $t('welcome.description') }}</p>

    <select v-model="$i18n.locale">
      <option value="en">English</option>
      <option value="es">Español</option>
    </select>
  </div>
</template>
```

### 3. Create Translation Files

**Directory structure:**
```
public/
  locales/
    en/
      common.json
      home.json
      auth.json
    es/
      common.json
      home.json
      auth.json
    fr/
      common.json
      home.json
      auth.json
```

**en/common.json:**
```json
{
  "nav": {
    "home": "Home",
    "about": "About",
    "contact": "Contact"
  },
  "button": {
    "submit": "Submit",
    "cancel": "Cancel",
    "save": "Save",
    "delete": "Delete"
  },
  "message": {
    "success": "Operation successful",
    "error": "An error occurred",
    "loading": "Loading..."
  }
}
```

**en/home.json:**
```json
{
  "hero": {
    "title": "Welcome to Our App",
    "subtitle": "Build amazing things",
    "cta": "Get Started"
  },
  "features": {
    "title": "Features",
    "feature1": "Fast and reliable",
    "feature2": "Easy to use",
    "feature3": "Secure by default"
  }
}
```

### 4. Language Switcher Component

**React:**
```javascript
import { useTranslation } from 'react-i18next'

const languages = {
  en: { name: 'English', flag: '🇬🇧' },
  es: { name: 'Español', flag: '🇪🇸' },
  fr: { name: 'Français', flag: '🇫🇷' },
  de: { name: 'Deutsch', flag: '🇩🇪' },
}

function LanguageSwitcher() {
  const { i18n } = useTranslation()

  return (
    <select
      value={i18n.language}
      onChange={(e) => i18n.changeLanguage(e.target.value)}
      className="language-select"
    >
      {Object.entries(languages).map(([code, { name, flag }]) => (
        <option key={code} value={code}>
          {flag} {name}
        </option>
      ))}
    </select>
  )
}
```

**Vue:**
```vue
<template>
  <div class="language-switcher">
    <button
      v-for="lang in languages"
      :key="lang.code"
      @click="$i18n.locale = lang.code"
      :class="{ active: $i18n.locale === lang.code }"
    >
      {{ lang.flag }} {{ lang.name }}
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      languages: [
        { code: 'en', name: 'English', flag: '🇬🇧' },
        { code: 'es', name: 'Español', flag: '🇪🇸' },
        { code: 'fr', name: 'Français', flag: '🇫🇷' },
      ],
    }
  },
}
</script>
```

### 5. Advanced Features

**Pluralization:**
```json
{
  "items": {
    "count_one": "{{count}} item",
    "count_other": "{{count}} items"
  }
}
```

```javascript
t('items.count', { count: 1 })  // "1 item"
t('items.count', { count: 5 })  // "5 items"
```

**Interpolation:**
```json
{
  "greeting": "Hello, {{name}}!",
  "welcome": "Welcome back, {{name}}. You have {{count}} messages."
}
```

```javascript
t('greeting', { name: 'John' })  // "Hello, John!"
t('welcome', { name: 'John', count: 5 })
```

**Date/Number Formatting:**
```javascript
import { useTranslation } from 'react-i18next'

function Component() {
  const { t, i18n } = useTranslation()

  const date = new Date()
  const number = 1234.56

  return (
    <div>
      <p>{new Intl.DateTimeFormat(i18n.language).format(date)}</p>
      <p>{new Intl.NumberFormat(i18n.language).format(number)}</p>
      <p>
        {new Intl.NumberFormat(i18n.language, {
          style: 'currency',
          currency: 'USD',
        }).format(number)}
      </p>
    </div>
  )
}
```

### 6. RTL Support

**Detect RTL languages:**
```javascript
const RTL_LANGUAGES = ['ar', 'he', 'fa', 'ur']

function setDirection(language) {
  const isRTL = RTL_LANGUAGES.includes(language)
  document.dir = isRTL ? 'rtl' : 'ltr'
  document.documentElement.lang = language
}

// On language change
i18n.on('languageChanged', (lng) => {
  setDirection(lng)
})
```

**CSS for RTL:**
```css
[dir='rtl'] {
  text-align: right;
}

[dir='rtl'] .margin-left {
  margin-right: 1rem;
  margin-left: 0;
}

/* Or use logical properties */
.element {
  margin-inline-start: 1rem; /* Respects dir attribute */
  padding-inline-end: 0.5rem;
}
```

### 7. SEO Configuration

**Next.js:**
```javascript
import Head from 'next/head'
import { useTranslation } from 'next-i18next'

function MyPage() {
  const { t } = useTranslation()

  return (
    <>
      <Head>
        <title>{t('page.title')}</title>
        <meta name="description" content={t('page.description')} />
        <link rel="alternate" hrefLang="en" href="https://example.com/en" />
        <link rel="alternate" hrefLang="es" href="https://example.com/es" />
      </Head>
      {/* Page content */}
    </>
  )
}
```

### 8. Translation Management

**Scripts in package.json:**
```json
{
  "scripts": {
    "i18n:extract": "i18next-scanner",
    "i18n:sync": "node scripts/sync-translations.js",
    "i18n:validate": "node scripts/validate-translations.js"
  }
}
```

**Validation script:**
```javascript
// scripts/validate-translations.js
const fs = require('fs')
const path = require('path')

const locales = ['en', 'es', 'fr']
const namespaces = ['common', 'home', 'auth']

const baseTranslations = JSON.parse(
  fs.readFileSync('public/locales/en/common.json', 'utf8')
)

locales.forEach(locale => {
  namespaces.forEach(ns => {
    const file = `public/locales/${locale}/${ns}.json`
    const translations = JSON.parse(fs.readFileSync(file, 'utf8'))

    // Check for missing keys
    Object.keys(baseTranslations).forEach(key => {
      if (!translations[key]) {
        console.warn(`Missing key "${key}" in ${locale}/${ns}.json`)
      }
    })
  })
})
```

### 9. Best Practices

- Store translations in separate files by namespace
- Use descriptive keys: `home.hero.title` not `text1`
- Keep translation files in version control
- Use variables for dynamic content
- Support pluralization from the start
- Consider RTL languages
- Implement language detection
- Provide fallback language
- Add SEO meta tags
- Test all languages

### 10. Testing

```javascript
import { render, screen } from '@testing-library/react'
import { I18nextProvider } from 'react-i18next'
import i18n from 'i18next'

const mockI18n = i18n.createInstance()
mockI18n.init({
  lng: 'en',
  resources: {
    en: {
      translation: {
        'welcome.title': 'Welcome',
      },
    },
  },
})

test('renders translated text', () => {
  render(
    <I18nextProvider i18n={mockI18n}>
      <MyComponent />
    </I18nextProvider>
  )

  expect(screen.getByText('Welcome')).toBeInTheDocument()
})
```

## Quick Setup Checklist

- [ ] Install i18n library
- [ ] Create i18n configuration
- [ ] Setup translation files structure
- [ ] Create initial translations (en)
- [ ] Add language switcher
- [ ] Implement language detection
- [ ] Add RTL support (if needed)
- [ ] Configure SEO (hrefLang tags)
- [ ] Add translation validation
- [ ] Test all languages
