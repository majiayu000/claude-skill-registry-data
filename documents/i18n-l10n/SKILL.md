---
name: i18n-l10n
description: Internationalization and localization patterns for multi-locale support. Use when implementing translations, formatting dates/numbers/currency, or handling locale-specific content. Keywords - i18n, l10n, translations, locale, formatting, dates, currency, numbers.
compatibility: Designed for i18next with React, supports en-US, fr-CA, es-US locales
metadata:
  version: "2.0.0"
  author: jpmorgan-payments
  lastUpdated: "2025-12-24"
  priority: high
---

# i18n/l10n Guidelines

## Overview

All components must support multiple locales with proper formatting for dates, numbers, and currency.

## Supported Locales

- **en-US** (English - United States) - Default
- **fr-CA** (French - Canada)
- **es-US** (Spanish - United States)

## Core Principles

1. **Always use `useTranslation` hook** - Never hardcode text strings
2. **Locale-aware formatting** - Respect current locale for dates/numbers/currency
3. **Default values** - Always provide `defaultValue` for fallback
4. **Type assertion for `t` function** - Use `as` to avoid TypeScript overload issues

## ⚠️ CRITICAL: TypeScript Overload Issue

Always use type assertion when calling `t()` function:

```typescript
// ✅ CORRECT - Use type assertion
const t = useTranslation() as (key: string, options?: any) => string;

// Usage
const title = t('transactions.title', { defaultValue: 'Transactions' });

// ❌ WRONG - TypeScript overload error
const { t } = useTranslation();
const title = t('transactions.title', { defaultValue: 'Transactions' });
// Error: No overload matches this call
```

## Translation Pattern

```typescript
import { useTranslation } from 'react-i18next';

export const MyComponent: FC = () => {
  // ✅ Type assertion to avoid overload issues
  const t = useTranslation() as (key: string, options?: any) => string;

  return (
    <div>
      <h1>{t('component.title', { defaultValue: 'Default Title' })}</h1>
      <p>{t('component.description', { 
        defaultValue: 'Description text',
        name: userName 
      })}</p>
    </div>
  );
};
```

## Translation Keys

### Namespace Organization

- Each component/feature: own namespace (`transactions`, `accounts`)
- Common translations: `common` namespace
- Validation: `validation` namespace

### Key Structure

```typescript
// ✅ GOOD - Hierarchical, descriptive
t('transactions.columns.date', { defaultValue: 'Date' })
t('transactions.errors.failedToLoadTitle', { defaultValue: 'Failed to load transactions' })
t('transactions.toolbar.allStatuses', { defaultValue: 'All statuses' })

// ❌ BAD - Flat, ambiguous
t('date')
t('error')
t('all')
```

### Default Values

Always provide `defaultValue`:

```typescript
// ✅ GOOD - With default
t('transactions.title', { defaultValue: 'Transactions' })

// ❌ BAD - No fallback
t('transactions.title')
```

## Locale Detection

Use the `useLocale()` hook:

```typescript
import { useLocale } from '@/lib/hooks';

const MyComponent = () => {
  const locale = useLocale(); // Returns 'en-US', 'fr-CA', etc.
  // Use locale for formatting
};
```

### Language Code vs Locale String

- **Language Code**: i18next format ('enUS', 'frCA')
- **Locale String**: Intl API format ('en-US', 'fr-CA')
- **Convert** using `getLocaleFromLanguage()` utility

## Date Formatting

### Rules

1. Always use locale parameter (never hardcode 'en-US')
2. Use appropriate format (Date vs DateTime)
3. Handle undefined/null with fallback

### Pattern

```typescript
import { useLocale } from '@/lib/hooks';

const MyComponent = () => {
  const t = useTranslation() as (key: string, options?: any) => string;
  const locale = useLocale();
  const naText = t('common:na', { defaultValue: 'N/A' });

  // Date only
  const formatDate = (date?: string): string => {
    if (!date) return naText;
    return new Date(date).toLocaleDateString(locale, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  // Date and time
  const formatDateTime = (date?: string): string => {
    if (!date) return naText;
    return new Date(date).toLocaleString(locale, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };
};
```

### Do's and Don'ts

```typescript
// ✅ DO - Use locale from hook
const locale = useLocale();
const formatted = new Date(date).toLocaleDateString(locale, {...});

// ✅ DO - Provide fallback
if (!date) return naText;

// ❌ DON'T - Hardcode locale
new Date(date).toLocaleDateString('en-US', {...});

// ❌ DON'T - No fallback
new Date(date).toLocaleDateString(locale, {...});
```

## Currency Formatting

### Rules

1. Use `formatNumberToCurrency` utility
2. Always pass locale
3. Handle undefined amounts

### Pattern

```typescript
import { formatNumberToCurrency } from './utils';
import { useLocale } from '@/lib/hooks';

const MyComponent = () => {
  const locale = useLocale();
  const t = useTranslation() as (key: string, options?: any) => string;
  const naText = t('common:na', { defaultValue: 'N/A' });

  const formattedAmount = transaction.amount
    ? formatNumberToCurrency(
        transaction.amount,
        transaction.currency ?? 'USD',
        locale
      )
    : naText;
};
```

### Utility Function

```typescript
/**
 * Formats a number as currency using the specified locale
 * @param amount - The amount to format
 * @param currency - The currency code (e.g., 'USD', 'CAD')
 * @param locale - The locale string (defaults to 'en-US')
 * @returns Formatted currency string
 */
export const formatNumberToCurrency = (
  amount: number,
  currency: string,
  locale: string = 'en-US'
): string => {
  const formatter = new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
  });
  return formatter.format(amount);
};
```

## Number Formatting

```typescript
// Basic number
const formatNumber = (value: number, locale: string = 'en-US'): string => {
  return new Intl.NumberFormat(locale).format(value);
};

// Percentage
const formatPercentage = (value: number, locale: string = 'en-US'): string => {
  return new Intl.NumberFormat(locale, {
    style: 'percent',
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(value);
};

// Decimal places
const formatDecimal = (
  value: number,
  decimals: number = 2,
  locale: string = 'en-US'
): string => {
  return new Intl.NumberFormat(locale, {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
};
```

## Pluralization

```typescript
// Translation file
{
  "items": "{{count}} item",
  "items_plural": "{{count}} items"
}

// Component
const itemCount = t('items', { 
  defaultValue: '{{count}} item',
  count: items.length 
});
// count=1: "1 item"
// count=2: "2 items"
```

## Interpolation

```typescript
// Translation file
{
  "welcome": "Welcome, {{name}}!",
  "balance": "Your balance is {{amount}}"
}

// Component
const welcome = t('welcome', { 
  defaultValue: 'Welcome, {{name}}!',
  name: userName 
});

const balance = t('balance', { 
  defaultValue: 'Your balance is {{amount}}',
  amount: formatNumberToCurrency(amount, 'USD', locale)
});
```

## Context-Specific Translations

```typescript
// Translation file
{
  "status_pending": "Pending",
  "status_completed": "Completed",
  "status_failed": "Failed"
}

// Component
const getStatusText = (status: Status): string => {
  return t(`status_${status.toLowerCase()}`, { 
    defaultValue: status 
  });
};
```

## Best Practices

1. **Type assertion** - Always use `as` for `t` function
2. **Default values** - Required for all translation calls
3. **Locale parameter** - Never hardcode, use `useLocale()`
4. **Fallback text** - Handle undefined/null values
5. **Namespace organization** - Group related translations
6. **Descriptive keys** - Use hierarchical, clear keys
7. **Consistent formatting** - Use utility functions

## Common Patterns

### Form Labels and Placeholders

```typescript
const t = useTranslation() as (key: string, options?: any) => string;

<Input
  label={t('form.email.label', { defaultValue: 'Email Address' })}
  placeholder={t('form.email.placeholder', { defaultValue: 'Enter your email' })}
  error={t('form.email.error', { defaultValue: 'Invalid email address' })}
/>
```

### Error Messages

```typescript
const t = useTranslation() as (key: string, options?: any) => string;

<ServerErrorAlert
  error={apiError}
  customErrorMessage={{
    "400": t('errors.badRequest', { 
      defaultValue: 'Please check your information.' 
    }),
    "401": t('errors.unauthorized', { 
      defaultValue: 'Please log in again.' 
    }),
    "500": t('errors.serverError', { 
      defaultValue: 'An unexpected error occurred.' 
    }),
    default: t('errors.default', { 
      defaultValue: 'An error occurred.' 
    }),
  }}
/>
```

### Table Columns

```typescript
const columns = [
  {
    key: 'date',
    label: t('columns.date', { defaultValue: 'Date' }),
    render: (row) => formatDate(row.date, locale),
  },
  {
    key: 'amount',
    label: t('columns.amount', { defaultValue: 'Amount' }),
    render: (row) => formatNumberToCurrency(row.amount, row.currency, locale),
  },
];
```

## Testing with Locales

```typescript
import { renderWithProviders } from '@test-utils';

test('displays formatted date in French', () => {
  renderWithProviders(<Component />, { locale: 'fr-CA' });
  
  expect(screen.getByText(/janv/i)).toBeInTheDocument();
});

test('displays formatted currency in Canadian dollars', () => {
  renderWithProviders(<Component />, { locale: 'fr-CA' });
  
  expect(screen.getByText(/\$\s*1\s*234,56/)).toBeInTheDocument();
});
```

## Anti-Patterns

❌ Hardcoded text strings  
❌ Hardcoded 'en-US' locale  
❌ Missing default values  
❌ No fallback for undefined values  
❌ Not using type assertion for `t` function  
❌ Flat, ambiguous translation keys  

## References

- See `.github/copilot-instructions.md` for i18n patterns
- i18next documentation: https://www.i18next.com/
- Intl API: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl
