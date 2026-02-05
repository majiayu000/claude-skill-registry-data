---
name: vercel-analytics
description: Implements privacy-friendly web analytics with Vercel Analytics for traffic insights and Web Vitals. Use when tracking page views and performance metrics in Next.js applications deployed on Vercel.
---

# Vercel Analytics

Privacy-friendly, real-time traffic insights and Web Vitals for Vercel-deployed applications. Zero configuration with automatic Core Web Vitals tracking.

## Quick Start

```bash
npm install @vercel/analytics
```

### Next.js App Router

```tsx
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### Next.js Pages Router

```tsx
// pages/_app.tsx
import { Analytics } from '@vercel/analytics/react';
import type { AppProps } from 'next/app';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <>
      <Component {...pageProps} />
      <Analytics />
    </>
  );
}
```

## Configuration Options

```tsx
import { Analytics } from '@vercel/analytics/react';

<Analytics
  mode="production"  // 'production' | 'development' | 'auto'
  debug={false}      // Enable debug mode
  beforeSend={(event) => {
    // Modify or filter events before sending
    if (event.url.includes('/private')) {
      return null;  // Don't track
    }
    return event;
  }}
/>
```

## Custom Events

Track custom events beyond page views.

```tsx
import { track } from '@vercel/analytics';

// Basic event
track('signup_clicked');

// Event with properties
track('item_purchased', {
  productId: 'prod_123',
  price: 29.99,
  currency: 'USD',
});

// Form submission
function ContactForm() {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    track('contact_form_submitted', {
      source: 'footer',
    });
    // Submit form...
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

### Server-Side Tracking

```typescript
// app/api/checkout/route.ts
import { track } from '@vercel/analytics/server';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const { orderId, amount } = await request.json();

  await track('purchase_completed', {
    orderId,
    amount,
  });

  return NextResponse.json({ success: true });
}
```

## Web Vitals (Speed Insights)

Track Core Web Vitals with Vercel Speed Insights.

```bash
npm install @vercel/speed-insights
```

```tsx
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/next';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
```

### Custom Web Vitals Reporting

```tsx
// app/layout.tsx
'use client';

import { useReportWebVitals } from 'next/web-vitals';

export function WebVitals() {
  useReportWebVitals((metric) => {
    console.log(metric);
    // {
    //   id: 'v3-1234567890',
    //   name: 'LCP',
    //   value: 2500,
    //   rating: 'good',
    //   delta: 2500,
    //   entries: [...],
    //   navigationType: 'navigate',
    // }

    // Send to your analytics
    // gtag('event', metric.name, { value: metric.value });
  });

  return null;
}
```

## Instrumentation Client

For advanced analytics setup:

```typescript
// instrumentation-client.ts
export function register() {
  // Initialize analytics, error tracking, etc.
  console.log('Analytics initialized');
}
```

## React (Non-Next.js)

```tsx
import { inject } from '@vercel/analytics';

// Call once on app load
inject();

// Or with options
inject({
  mode: 'production',
  debug: true,
});
```

### React Component

```tsx
import { Analytics } from '@vercel/analytics/react';

function App() {
  return (
    <>
      <YourApp />
      <Analytics />
    </>
  );
}
```

## Event Filtering

```tsx
<Analytics
  beforeSend={(event) => {
    // Remove query params from URLs
    const url = new URL(event.url);
    url.search = '';
    event.url = url.toString();

    // Filter specific paths
    if (event.url.includes('/admin')) {
      return null;
    }

    return event;
  }}
/>
```

## Development Mode

Analytics are disabled by default in development. Override:

```tsx
<Analytics mode="development" debug={true} />
```

Or use environment variable:

```bash
# .env.local
NEXT_PUBLIC_VERCEL_ANALYTICS_DEBUG=true
```

## Viewing Analytics

Analytics are available in the Vercel Dashboard:

1. Go to your project on Vercel
2. Click "Analytics" tab
3. View page views, unique visitors, referrers, and more

## With Other Frameworks

### SvelteKit

```svelte
<!-- src/routes/+layout.svelte -->
<script>
  import { inject } from '@vercel/analytics';
  import { browser } from '$app/environment';

  if (browser) {
    inject();
  }
</script>

<slot />
```

### Astro

```astro
---
// src/layouts/Layout.astro
import { Analytics } from '@vercel/analytics/react';
---

<html>
  <body>
    <slot />
    <Analytics client:only="react" />
  </body>
</html>
```

### Vue/Nuxt

```vue
<!-- app.vue -->
<script setup>
import { inject } from '@vercel/analytics'

onMounted(() => {
  inject()
})
</script>
```

## TypeScript

```typescript
import { track } from '@vercel/analytics';

interface PurchaseEvent {
  productId: string;
  price: number;
  quantity: number;
}

function trackPurchase(event: PurchaseEvent) {
  track('purchase', event);
}
```

## Privacy Features

- No cookies used
- GDPR compliant
- No personal data collected
- IP addresses are anonymized
- Data stored in EU or US (your choice)

## Best Practices

1. **Add Analytics component once** - In root layout
2. **Use beforeSend for PII** - Filter sensitive URLs
3. **Add Speed Insights** - For Core Web Vitals
4. **Track meaningful events** - Conversions, signups, purchases
5. **Use server-side tracking** - For sensitive operations
6. **Enable in production only** - Default behavior
