---
name: tsh-i18n
description: |
  Internationalization for TSH Clients Console (English/Arabic with RTL). Use when:
  (1) Adding new text strings that need translation
  (2) Creating components with user-facing text
  (3) Working with RTL layout for Arabic
  (4) Setting up new pages with proper i18n
  (5) Debugging translation issues
  (6) Adding metadata translations for SEO
---

# TSH Internationalization (i18n)

## File Locations

| File | Purpose |
|------|---------|
| `src/messages/en.json` | English translations |
| `src/messages/ar.json` | Arabic translations |
| `src/i18n/request.ts` | i18n config |
| `src/i18n/routing.ts` | Locale routing |

## Adding Translations

### Step 1: Add to en.json
```json
{
  "namespace": {
    "keyName": "English text",
    "greeting": "Hello, {name}!",
    "count": "You have {count} items"
  }
}
```

### Step 2: Add to ar.json
```json
{
  "namespace": {
    "keyName": "النص العربي",
    "greeting": "مرحباً، {name}!",
    "count": "لديك {count} عناصر"
  }
}
```

## Using Translations

### Client Components
```typescript
'use client';
import { useTranslations } from 'next-intl';

export function MyComponent() {
  const t = useTranslations('namespace');

  return (
    <div>
      <h1>{t('keyName')}</h1>
      <p>{t('greeting', { name: 'Ahmed' })}</p>
      <p>{t('count', { count: 5 })}</p>
    </div>
  );
}
```

### Server Components
```typescript
import { getTranslations } from 'next-intl/server';

export default async function Page() {
  const t = await getTranslations('namespace');
  return <h1>{t('keyName')}</h1>;
}
```

### Metadata (SEO)
```typescript
import { getTranslations } from 'next-intl/server';

export async function generateMetadata({ params: { locale } }) {
  const t = await getTranslations({ locale, namespace: 'pageName' });
  return {
    title: t('title'),
    description: t('description'),
  };
}
```

## RTL Layout Patterns

### Direction-Aware Spacing (Use These)
```html
<!-- Logical properties that flip in RTL -->
<div className="ms-4">  <!-- margin-start -->
<div className="me-4">  <!-- margin-end -->
<div className="ps-4">  <!-- padding-start -->
<div className="pe-4">  <!-- padding-end -->
<div className="text-start">  <!-- text-align: start -->
<div className="text-end">    <!-- text-align: end -->
```

### Flip Elements in RTL
```html
<!-- Flip icons -->
<ChevronRight className="h-4 w-4 rtl:rotate-180" />

<!-- Reverse flex -->
<div className="flex rtl:flex-row-reverse">

<!-- Reverse spacing -->
<div className="flex space-x-4 rtl:space-x-reverse">
```

### Get Current Direction
```typescript
import { useLocale } from 'next-intl';

function Component() {
  const locale = useLocale();
  const isRTL = locale === 'ar';

  return <div dir={isRTL ? 'rtl' : 'ltr'}>...</div>;
}
```

## Common Translation Namespaces

| Namespace | Purpose |
|-----------|---------|
| `common` | Shared strings (buttons, actions) |
| `navigation` | Menu items, nav links |
| `products` | Product-related text |
| `orders` | Order-related text |
| `auth` | Login, authentication |
| `dashboard` | Dashboard labels |
| `errors` | Error messages |

## Standard Keys

Always include these in new namespaces:
```json
{
  "namespace": {
    "title": "Page Title",
    "loading": "Loading...",
    "error": "An error occurred",
    "empty": "No items found",
    "retry": "Try again"
  }
}
```

## Products Namespace Reference

```json
{
  "products": {
    "title": "Products",
    "search": "Search products",
    "inStock": "In Stock",
    "outOfStock": "Out of Stock",
    "lowStock": "Only {count} left",
    "contactForPrice": "Contact for price",
    "addToCart": "Add to Cart",
    "viewDetails": "View Details"
  }
}
```

Arabic:
```json
{
  "products": {
    "title": "المنتجات",
    "search": "البحث عن منتجات",
    "inStock": "متوفر",
    "outOfStock": "غير متوفر",
    "lowStock": "متبقي {count} فقط",
    "contactForPrice": "اتصل للسعر",
    "addToCart": "أضف إلى السلة",
    "viewDetails": "عرض التفاصيل"
  }
}
```

## Checklist for New Pages

- [ ] Add page namespace to en.json
- [ ] Add page namespace to ar.json
- [ ] Use `useTranslations` in client components
- [ ] Use `getTranslations` in server components
- [ ] Add `generateMetadata` for SEO
- [ ] Test RTL layout in Arabic
- [ ] Use logical properties (ms-, me-, ps-, pe-)
- [ ] Flip directional icons with `rtl:rotate-180`
