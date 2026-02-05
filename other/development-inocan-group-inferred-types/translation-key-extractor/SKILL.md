---
name: translation-key-extractor
description: Extracts hardcoded strings from code and converts them to translation keys for i18n. Use when user asks to "extract translations", "find hardcoded strings", "internationalize code", "setup i18n", or "create translation files".
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# Translation Key Extractor

Automatically finds hardcoded strings in code and converts them to translation keys for internationalization (i18n).

## When to Use

- "Extract hardcoded strings for translation"
- "Find all translatable text"
- "Convert strings to i18n keys"
- "Setup internationalization"
- "Create translation files from code"
- "Prepare code for multiple languages"

## Instructions

### 1. Scan for Hardcoded Strings

Identify strings that need translation:

```bash
# Find string literals in JavaScript/TypeScript
grep -r "[\"\'\`][A-Z]" src/ --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx"

# Find Python strings
grep -r "[\"'][A-Z]" . --include="*.py"

# Exclude imports, technical strings, CSS, etc.
```

Present findings with context:
- File and line number
- Surrounding code
- String content
- Suggested key name

### 2. Detect i18n Framework

Check what's already installed:

```bash
# React
grep -E "(react-i18next|react-intl|formatjs)" package.json

# Vue
grep -E "(vue-i18n)" package.json

# Python
grep -E "(gettext|Babel)" requirements.txt

# Ruby
grep -E "(i18n)" Gemfile
```

If none found, offer to install appropriate framework.

### 3. Generate Translation Keys

Create meaningful keys from strings:

**Rules:**
- Use dot notation: `common.button.save`
- Lowercase with underscores or camelCase
- Descriptive but concise
- Organized by scope (page, component, common)

**Examples:**
```
"Save changes" → "common.button.save"
"Welcome to our app" → "home.hero.welcome"
"Invalid email address" → "validation.email.invalid"
"Settings" → "navigation.settings"
"Are you sure?" → "common.confirm.message"
```

### 4. Create/Update Translation Files

Based on framework, create appropriate structure:

**react-i18next (en.json):**
```json
{
  "common": {
    "button": {
      "save": "Save changes",
      "cancel": "Cancel",
      "delete": "Delete"
    },
    "confirm": {
      "message": "Are you sure?",
      "yes": "Yes",
      "no": "No"
    }
  },
  "home": {
    "hero": {
      "welcome": "Welcome to our app",
      "subtitle": "Build amazing things"
    }
  },
  "validation": {
    "email": {
      "invalid": "Invalid email address",
      "required": "Email is required"
    }
  }
}
```

**Vue i18n (en.js):**
```javascript
export default {
  common: {
    button: {
      save: 'Save changes',
      cancel: 'Cancel'
    }
  },
  home: {
    hero: {
      welcome: 'Welcome to our app'
    }
  }
}
```

**gettext (.po file):**
```
msgid "save"
msgstr "Save changes"

msgid "welcome"
msgstr "Welcome to our app"
```

### 5. Replace Strings in Code

Transform hardcoded strings to use i18n:

**React (react-i18next):**
```jsx
// Before
<button>Save changes</button>
<h1>Welcome to our app</h1>
<p className="error">Invalid email address</p>

// After
import { useTranslation } from 'react-i18next'

function Component() {
  const { t } = useTranslation()

  return (
    <>
      <button>{t('common.button.save')}</button>
      <h1>{t('home.hero.welcome')}</h1>
      <p className="error">{t('validation.email.invalid')}</p>
    </>
  )
}
```

**Vue (vue-i18n):**
```vue
<!-- Before -->
<template>
  <button>Save changes</button>
  <h1>Welcome to our app</h1>
</template>

<!-- After -->
<template>
  <button>{{ $t('common.button.save') }}</button>
  <h1>{{ $t('home.hero.welcome') }}</h1>
</template>
```

**Python (gettext):**
```python
# Before
print("Welcome to our app")
error_message = "Invalid email address"

# After
from gettext import gettext as _

print(_("Welcome to our app"))
error_message = _("Invalid email address")
```

### 6. Handle Special Cases

**Dynamic content:**
```jsx
// Variables in strings
const message = `Welcome, ${name}!`

// Convert to
const message = t('welcome.greeting', { name })

// Translation file
{
  "welcome": {
    "greeting": "Welcome, {{name}}!"
  }
}
```

**Pluralization:**
```jsx
// Before
const message = count === 1 ? '1 item' : `${count} items`

// After
const message = t('items.count', { count })

// Translation file
{
  "items": {
    "count_one": "{{count}} item",
    "count_other": "{{count}} items"
  }
}
```

**Rich text/HTML:**
```jsx
// Before
<p>Visit our <a href="/help">help center</a></p>

// After (react-i18next with Trans component)
<Trans i18nKey="help.message">
  Visit our <a href="/help">help center</a>
</Trans>

// Translation file
{
  "help": {
    "message": "Visit our <1>help center</1>"
  }
}
```

### 7. Setup i18n Framework (if needed)

**React (react-i18next):**
```bash
npm install react-i18next i18next
```

```javascript
// i18n.js
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import en from './locales/en.json'
import es from './locales/es.json'

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: en },
      es: { translation: es }
    },
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  })

export default i18n

// index.js
import './i18n'
import App from './App'

ReactDOM.render(<App />, document.getElementById('root'))
```

**Vue (vue-i18n):**
```bash
npm install vue-i18n
```

```javascript
// i18n.js
import { createI18n } from 'vue-i18n'
import en from './locales/en'
import es from './locales/es'

const i18n = createI18n({
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    es
  }
})

export default i18n

// main.js
import { createApp } from 'vue'
import App from './App.vue'
import i18n from './i18n'

createApp(App).use(i18n).mount('#app')
```

### 8. Create Translation Template

For other languages:

```json
// locales/es.json (Spanish - empty template)
{
  "common": {
    "button": {
      "save": "",
      "cancel": "",
      "delete": ""
    }
  }
}
```

Or provide English as placeholders for translators:

```json
// locales/es.json
{
  "common": {
    "button": {
      "save": "[ES] Save changes",  // Translator replaces this
      "cancel": "[ES] Cancel",
      "delete": "[ES] Delete"
    }
  }
}
```

### 9. String Detection Rules

**Include:**
- User-visible text
- Error messages
- Labels and placeholders
- Navigation items
- Notifications/alerts
- Help text and tooltips

**Exclude:**
- Technical identifiers (IDs, keys)
- API endpoints
- Class names, CSS
- Console logs (unless user-facing)
- Test data
- Environment variables
- Regular expressions

**Example filtering:**
```javascript
// Extract
"Save changes"  ✅
"Welcome"  ✅
"Error: Invalid input"  ✅

// Don't extract
"userId"  ❌
"/api/users"  ❌
"btn-primary"  ❌
console.log("Debug info")  ❌
```

### 10. Provide Migration Plan

1. Setup i18n framework
2. Create translation files
3. Replace strings file by file
4. Test each component
5. Create template for other languages
6. Send to translators
7. Add language switcher UI
8. Test with all locales

### Best Practices

**Key Naming:**
```
✅ Good:
- common.button.save
- home.hero.title
- errors.validation.email

❌ Bad:
- string1
- text_for_button
- thisIsAReallyLongKeyNameThatSaysExactlyWhatTheStringIs
```

**Organization:**
```
locales/
  en/
    common.json       # Shared across app
    home.json         # Home page specific
    auth.json         # Authentication
    validation.json   # Error messages
  es/
    common.json
    home.json
    ...
```

**Performance:**
- Lazy load translations per page/feature
- Use namespaces to avoid loading all translations
- Cache translations in production

**Context:**
```json
{
  "button": {
    "save": "Save",           // Generic
    "save_changes": "Save changes",  // Specific
    "save_draft": "Save as draft"    // Different context
  }
}
```
