---
name: hua-ux Framework Usage
description: Guide for developing Next.js applications using the hua-ux framework
license: MIT
compatibility:
  - claude
---

# hua-ux Framework Usage Skill

This skill guides you on how to develop Next.js applications using the hua-ux framework.

## 🚨 Required Guidelines for Claude Assistants

### Required Checks Before Using Framework

```
IF (creating a new page or component) THEN
  1. Use hua-ux framework components first
     → Wrap page with `HuaUxPage`
     → Use components from `@hua-labs/ui` first
  2. Generate translation files together
     → `translations/ko/{namespace}.json`
     → `translations/en/{namespace}.json`
  3. Prefer Server Components
     → Add `'use client'` only when client features are needed
END IF
```

## Core Philosophy

**"You don't need to know Next.js. Just configure and tell AI what to do."**

## Framework Structure

### Top Layer: Framework & Config
- `hua-ux.config.ts`: Framework configuration
- `HuaUxLayout`: Automatic Provider setup
- `HuaUxPage`: Page wrapper (Motion, i18n, SEO automatically applied)

### Bottom Layer: Core Packages
- `@hua-labs/ui`: UI component library
- `@hua-labs/motion-core`: Motion/animations
- `@hua-labs/i18n-core`: Internationalization
- `@hua-labs/state`: State management

## Key Patterns

### 1. Page Creation Pattern

```tsx
// app/my-page/page.tsx
import { HuaUxPage } from '@hua-labs/hua-ux/framework';
import { useTranslation } from '@hua-labs/i18n-core';

export default function MyPage() {
  const { t } = useTranslation('my-page');
  
  return (
    <HuaUxPage title={t('title')} description={t('description')}>
      <h1>{t('title')}</h1>
      {/* content */}
    </HuaUxPage>
  );
}
```

**Important**:
- Wrapping with `HuaUxPage` automatically applies Motion, i18n, SEO
- Add translation keys to `translations/{language}/my-page.json`
- Create as Server Component (default)

### 2. Client Component Creation Pattern

```tsx
// components/MyComponent.tsx
'use client';

import { Card, Button } from '@hua-labs/ui';
import { useMotion } from '@hua-labs/hua-ux/framework';
import { useTranslation } from '@hua-labs/i18n-core';

export function MyComponent() {
  const { t } = useTranslation('my-component');
  const motion = useMotion();
  
  return (
    <Card ref={motion.ref} style={motion.style}>
      <h2>{t('title')}</h2>
      <Button>{t('button')}</Button>
    </Card>
  );
}
```

**Important**:
- Client components require `'use client'`
- Utilize framework components (`@hua-labs/ui`, `@hua-labs/motion-core`)

### 3. Translation File Pattern

```json
// translations/ko/my-page.json
{
  "title": "Title",
  "description": "Description",
  "button": "Button"
}

// translations/en/my-page.json
{
  "title": "Title",
  "description": "Description",
  "button": "Button"
}
```

**Important**:
- Add all translation keys to both Korean and English
- Namespace should match page name

## Available Components

### @hua-labs/ui
- `Button`, `Card`, `Input`, `Modal`, `Alert`, `Toast`, `Table`, `Form`, etc.
- See `ai-context.md` for detailed list

### @hua-labs/hua-ux/framework
- `HuaUxPage`: Page wrapper
- `HuaUxLayout`: Layout
- `UnifiedProviders`: Provider unification
- `useMotion`: Unified motion hook
- `useData`: Client data fetching
- `fetchData`: Server data fetching

## Configuration File

### hua-ux.config.ts

```typescript
import { defineConfig } from '@hua-labs/hua-ux/framework';

export default defineConfig({
  preset: 'product',  // 'product' or 'marketing'
  
  i18n: {
    defaultLanguage: 'ko',
    supportedLanguages: ['ko', 'en'],
  },
  
  motion: {
    defaultPreset: 'product',
    enableAnimations: true,
  },
});
```

**Preset Selection**:
- `'product'`: For product pages (professional, efficient)
- `'marketing'`: For marketing pages (dramatic, eye-catching)

## Guidelines for Claude Code Generation

1. **When Creating Pages**:
   - Wrap with `HuaUxPage`
   - Generate translation files together
   - Use `useTranslation` hook
   - Prefer Server Components

2. **When Creating Components**:
   - Add `'use client'` directive (for client components)
   - Utilize framework components
   - Consider applying motion

3. **When Adding Translations**:
   - Add both Korean and English
   - Maintain namespace consistency

4. **When Changing Configuration**:
   - Only modify `hua-ux.config.ts`
   - Prefer Preset (over manual configuration)

## References

- `ai-context.md`: Detailed project structure explanation
- `.cursorrules`: Cursor IDE rules
- Framework docs: `node_modules/@hua-labs/hua-ux/README.md`
