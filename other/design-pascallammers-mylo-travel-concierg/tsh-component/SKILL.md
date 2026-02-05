---
name: tsh-component
description: |
  UI component patterns for TSH Clients Console (Next.js, shadcn/ui, RTL). Use when:
  (1) Creating new React components
  (2) Building pages with proper structure
  (3) Implementing loading skeletons
  (4) Adding responsive design
  (5) Supporting dark mode and RTL
  (6) Using shadcn/ui components correctly
---

# TSH Component Patterns

## Component Structure

```
src/components/
├── ui/           # shadcn/ui primitives (don't edit)
├── layout/       # Layout: header, nav, menu
├── products/     # Product components
├── orders/       # Order components
├── dashboard/    # Dashboard components
└── providers/    # Context providers
```

## Page Component Pattern

### Server Component (Page)
```typescript
// src/app/[locale]/(main)/page-name/page.tsx
import { getTranslations } from 'next-intl/server';
import { Suspense } from 'react';
import { PageContent } from '@/components/page-name/page-content';
import { PageSkeleton } from '@/components/page-name/page-skeleton';

export async function generateMetadata({ params: { locale } }) {
  const t = await getTranslations({ locale, namespace: 'pageName' });
  return { title: t('title') };
}

export default async function PageName() {
  return (
    <div className="container mx-auto px-4 py-6">
      <Suspense fallback={<PageSkeleton />}>
        <PageContent />
      </Suspense>
    </div>
  );
}
```

## Client Component Pattern

```typescript
// src/components/feature/component-name.tsx
'use client';

import { useTranslations } from 'next-intl';
import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface ComponentProps {
  data: DataType;
  onAction?: (id: string) => void;
}

export function ComponentName({ data, onAction }: ComponentProps) {
  const t = useTranslations('namespace');
  const [isLoading, setIsLoading] = useState(false);

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t('title')}</CardTitle>
      </CardHeader>
      <CardContent className="p-4">
        {/* Content */}
      </CardContent>
    </Card>
  );
}
```

## Loading Skeleton Pattern

```typescript
// src/components/feature/component-skeleton.tsx
import { Skeleton } from '@/components/ui/skeleton';
import { Card, CardContent } from '@/components/ui/card';

export function ComponentSkeleton() {
  return (
    <Card>
      <CardContent className="p-4 space-y-3">
        <Skeleton className="h-6 w-48" />
        <Skeleton className="h-4 w-32" />
        <Skeleton className="h-20 w-full" />
      </CardContent>
    </Card>
  );
}

// For grids
export function GridSkeleton({ count = 6 }: { count?: number }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {Array.from({ length: count }).map((_, i) => (
        <ComponentSkeleton key={i} />
      ))}
    </div>
  );
}
```

## Product Card Pattern

```typescript
'use client';

import { useTranslations } from 'next-intl';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface ProductCardProps {
  product: {
    id: string;
    name: string;
    image_url?: string;
    price: number;
    currency: string;
    inPriceList: boolean;
    stock: number;
  };
}

export function ProductCard({ product }: ProductCardProps) {
  const t = useTranslations('products');

  return (
    <Card className="overflow-hidden hover:shadow-lg transition-shadow">
      {/* Image */}
      <div className="aspect-square relative bg-muted">
        <img
          src={product.image_url || '/placeholder.png'}
          alt={product.name}
          className="object-cover w-full h-full"
        />
      </div>

      <CardContent className="p-4">
        {/* Name */}
        <h3 className="font-medium line-clamp-2 min-h-[3rem]">
          {product.name}
        </h3>

        {/* Price */}
        <div className="mt-2">
          {product.inPriceList ? (
            <span className="text-lg font-bold">
              {product.price.toLocaleString()} {product.currency}
            </span>
          ) : (
            <span className="text-muted-foreground text-sm">
              {t('contactForPrice')}
            </span>
          )}
        </div>

        {/* Stock */}
        <Badge
          variant={product.stock > 0 ? 'default' : 'secondary'}
          className="mt-2"
        >
          {product.stock > 0 ? t('inStock') : t('outOfStock')}
        </Badge>
      </CardContent>
    </Card>
  );
}
```

## RTL Layout Patterns

### Direction-Aware Spacing
```html
<!-- Use these logical properties -->
<div className="ms-4">  <!-- margin-start -->
<div className="me-4">  <!-- margin-end -->
<div className="ps-4">  <!-- padding-start -->
<div className="pe-4">  <!-- padding-end -->
<div className="text-start">  <!-- left in LTR, right in RTL -->
<div className="text-end">    <!-- right in LTR, left in RTL -->
```

### Flip Icons in RTL
```html
<ChevronRight className="h-4 w-4 rtl:rotate-180" />
<ArrowRight className="h-4 w-4 rtl:rotate-180" />
```

### Reverse Flex in RTL
```html
<div className="flex rtl:flex-row-reverse">
<div className="flex space-x-4 rtl:space-x-reverse">
```

## Dark Mode Patterns

```html
<!-- Background -->
<div className="bg-background">

<!-- Text -->
<p className="text-foreground">
<span className="text-muted-foreground">

<!-- Cards -->
<Card className="bg-card">

<!-- Borders -->
<div className="border-border">
```

## Responsive Patterns

```html
<!-- Mobile-first grid -->
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">

<!-- Responsive padding -->
<div className="px-4 md:px-6 lg:px-8">

<!-- Hide/show -->
<div className="hidden md:block">  <!-- Show on md+ -->
<div className="md:hidden">        <!-- Hide on md+ -->

<!-- Responsive text -->
<h1 className="text-xl md:text-2xl lg:text-3xl">
```

## Empty State Pattern

```typescript
import { PackageOpen } from 'lucide-react';

export function EmptyState({
  title,
  description,
  action,
}: {
  title: string;
  description: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <PackageOpen className="h-12 w-12 text-muted-foreground mb-4" />
      <h3 className="text-lg font-medium">{title}</h3>
      <p className="text-muted-foreground mt-1 max-w-sm">{description}</p>
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}
```

## Form Pattern

```typescript
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';

export function SearchForm({ onSearch }: { onSearch: (q: string) => void }) {
  const t = useTranslations('common');
  const [query, setQuery] = useState('');

  return (
    <form onSubmit={(e) => { e.preventDefault(); onSearch(query); }} className="flex gap-2">
      <div className="flex-1">
        <Label htmlFor="search" className="sr-only">
          {t('search')}
        </Label>
        <Input
          id="search"
          type="search"
          placeholder={t('searchPlaceholder')}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>
      <Button type="submit">{t('search')}</Button>
    </form>
  );
}
```

## Available shadcn/ui Components

```
avatar, badge, button, card, input, label,
scroll-area, select, separator, sheet,
skeleton, switch, tabs
```

Add new:
```bash
npx shadcn@latest add [component-name]
```

## Component Checklist

- [ ] TypeScript interfaces defined
- [ ] Props properly typed
- [ ] `useTranslations` for all text
- [ ] RTL layout considered (ms-, me-, rtl:)
- [ ] Dark mode works (bg-background, text-foreground)
- [ ] Loading skeleton created
- [ ] Error state handled
- [ ] Responsive design (mobile-first)
- [ ] Accessibility (aria labels, semantic HTML)
