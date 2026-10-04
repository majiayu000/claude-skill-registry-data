---
name: i18n
description: Internationalization and localization
license: MIT
metadata:
  audience: developers
  category: software-development
---

## What I do
- Prepare software for multiple languages
- Handle text expansion and contraction
- Manage date, time, and number formats
- Support right-to-left (RTL) languages
- Implement locale-specific content
- Structure translation workflows

## When to use me
When building applications that need to support multiple languages, regions, or cultural preferences.

## Key Concepts

### i18n vs l10n
```
i18n: Internationalization - code preparation
l10n: Localization - language/region adaptation
```

### Implementation Patterns
```javascript
// Translation keys
t('greeting', { name: 'John' })
// en.json: "Hello, {name}!"
// es.json: "¡Hola, {name}!"

// Pluralization
t('items', { count: n, plural: true })
// en: 1 item, 5 items
// ru: 1 предмет, 5 предметов
```

### Common Libraries
```python
# Python
from babel import Locale
from django.utils import translation

# JavaScript
import i18next from 'i18next';
import { IntlMessageFormat } from 'intl-messageformat';

# Java
import java.text.MessageFormat;
import java.util.Locale;
```

### RTL Support
```css
[dir="rtl"] {
  direction: rtl;
  text-align: right;
}

/* Swap left/right specific styles */
.sidebar { margin-left: 1rem; }
[dir="rtl"] .sidebar { margin-right: 1rem; }
```

### Formatting by Locale
```
Dates: en-US: 1/15/2026, en-GB: 15/01/2026
Numbers: en: 1,234.56, de: 1.234,56
Currency: $1,234.56, €1.234,56
```

### Best Practices
1. Externalize all strings
2. Use ICU message format
3. Test with pseudo-locales
4. Plan for text expansion (+30%)
5. Separate locale from logic
6. Use language codes (ISO 639-1)
