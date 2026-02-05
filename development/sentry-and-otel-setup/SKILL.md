---
name: sentry-and-otel-setup
description: This skill should be used when adding error tracking and performance monitoring with Sentry and OpenTelemetry tracing to Next.js applications. Apply when setting up error monitoring, configuring tracing for Server Actions and routes, implementing logging wrappers, adding performance instrumentation, or establishing observability for debugging production issues.
---

# Sentry and OpenTelemetry Setup

## Overview

Configure comprehensive error tracking and performance monitoring using Sentry with OpenTelemetry (OTel) instrumentation for Next.js applications, including automatic error capture, distributed tracing, and custom logging.

## Installation and Configuration

### 1. Install Sentry

Install Sentry Next.js SDK:

```bash
npm install @sentry/nextjs
```

Run Sentry wizard for automatic configuration:

```bash
npx @sentry/wizard@latest -i nextjs
```

This creates:
- `sentry.client.config.ts` - Client-side configuration
- `sentry.server.config.ts` - Server-side configuration
- `sentry.edge.config.ts` - Edge runtime configuration
- `instrumentation.ts` - OpenTelemetry setup
- Updates `next.config.js` with Sentry webpack plugin

### 2. Configure Environment Variables

Add Sentry credentials to `.env.local`:

```env
SENTRY_DSN=https://your-dsn@sentry.io/project-id
SENTRY_ORG=your-org
SENTRY_PROJECT=your-project
NEXT_PUBLIC_SENTRY_DSN=https://your-dsn@sentry.io/project-id
```

Get DSN from Sentry dashboard: Settings > Projects > [Your Project] > Client Keys (DSN)

**For production**, add these to deployment environment variables.

### 3. Update Sentry Configurations

Customize `sentry.server.config.ts` using the template from `assets/sentry-server-config.ts`:

- Set environment (development, staging, production)
- Configure sample rates for performance monitoring
- Enable tracing for Server Actions and API routes
- Set up error filtering and breadcrumbs

Customize `sentry.client.config.ts` using the template from `assets/sentry-client-config.ts`:

- Configure replay sessions for debugging
- Set error boundaries
- Enable performance monitoring for user interactions

### 4. Add Instrumentation Hook

Create or update `instrumentation.ts` in project root using the template from `assets/instrumentation.ts`. This:

- Initializes OpenTelemetry before app starts
- Registers Sentry as trace provider
- Enables distributed tracing across services
- Runs only once on server startup

**Note**: Requires `experimental.instrumentationHook` in `next.config.js` (added by Sentry wizard).

### 5. Create Logging Wrapper

Create `lib/logger.ts` using the template from `assets/logger.ts`. This provides:

- Structured logging with context
- Automatic Sentry integration
- Different log levels (debug, info, warn, error)
- Request context capture

Use instead of `console.log` for better debugging:

```typescript
import { logger } from '@/lib/logger';

logger.info('User logged in', { userId: user.id });
logger.error('Failed to save data', { error, userId });
```

### 6. Add Error Boundary (Client Components)

Create `components/error-boundary.tsx` using the template from `assets/error-boundary.tsx`. This:

- Catches React errors in client components
- Sends errors to Sentry
- Shows fallback UI
- Provides error recovery

Use in layouts or pages:

```typescript
import { ErrorBoundary } from '@/components/error-boundary';

export default function Layout({ children }) {
  return (
    <ErrorBoundary>
      {children}
    </ErrorBoundary>
  );
}
```

### 7. Create Custom Error Page

Update `app/error.tsx` using the template from `assets/error-page.tsx`. This:

- Shows user-friendly error messages
- Captures errors in Server Components
- Provides retry functionality
- Sends errors to Sentry

### 8. Add Global Error Handler

Update `app/global-error.tsx` using the template from `assets/global-error.tsx`. This:

- Catches errors in root layout
- Last resort error boundary
- Required for catching layout errors

## Tracing Server Actions

### Manual Instrumentation

Wrap Server Actions with Sentry tracing:

```typescript
'use server';

import { logger } from '@/lib/logger';
import * as Sentry from '@sentry/nextjs';

export async function createPost(formData: FormData) {
  return await Sentry.startSpan(
    { name: 'createPost', op: 'server.action' },
    async () => {
      try {
        const title = formData.get('title') as string;

        logger.info('Creating post', { title });

        // Your logic here
        const post = await prisma.post.create({
          data: { title, content: '...' },
        });

        logger.info('Post created', { postId: post.id });
        return { success: true, post };

      } catch (error) {
        logger.error('Failed to create post', { error });
        Sentry.captureException(error);
        throw error;
      }
    }
  );
}
```

### Automatic Instrumentation

Sentry automatically instruments:
- Next.js API routes
- Server Components (partial)
- Fetch requests
- Database queries (with OTel)

## Monitoring Patterns

### 1. Capture User Context

Associate errors with users:

```typescript
import * as Sentry from '@sentry/nextjs';
import { getCurrentUser } from '@/lib/auth/utils';

export async function setUserContext() {
  const user = await getCurrentUser();

  if (user) {
    Sentry.setUser({
      id: user.id,
      email: user.email,
    });
  }
}
```

Call in layouts or middleware to track user context globally.

### 2. Add Custom Tags

Tag errors for filtering:

```typescript
Sentry.setTag('feature', 'worldbuilding');
Sentry.setTag('entity_type', 'character');

// Now errors are tagged and filterable in Sentry dashboard
```

### 3. Add Breadcrumbs

Track user actions leading to errors:

```typescript
Sentry.addBreadcrumb({
  category: 'user_action',
  message: 'User clicked create entity',
  level: 'info',
  data: {
    entityType: 'character',
    worldId: 'world-123',
  },
});
```

### 4. Performance Monitoring

Track custom operations:

```typescript
import * as Sentry from '@sentry/nextjs';

export async function complexOperation() {
  const transaction = Sentry.startTransaction({
    name: 'Complex World Generation',
    op: 'task',
  });

  // Step 1
  const span1 = transaction.startChild({
    op: 'generate.terrain',
    description: 'Generate terrain data',
  });
  await generateTerrain();
  span1.finish();

  // Step 2
  const span2 = transaction.startChild({
    op: 'generate.biomes',
    description: 'Generate biome data',
  });
  await generateBiomes();
  span2.finish();

  transaction.finish();
}
```

### 5. Database Query Tracing

Prisma automatically integrates with OTel:

```typescript
// Queries are automatically traced if OTel is configured
const users = await prisma.user.findMany();
// Shows up in Sentry as a database span
```

## Configuration Options

### Sample Rates

Control how many events are sent to Sentry (avoid quota limits):

```typescript
// sentry.server.config.ts
Sentry.init({
  dsn: process.env.SENTRY_DSN,

  // Percentage of errors to capture (1.0 = 100%)
  sampleRate: 1.0,

  // Percentage of transactions to trace
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,

  // Percentage of sessions to replay
  replaysSessionSampleRate: 0.1,

  // Percentage of error sessions to replay
  replaysOnErrorSampleRate: 1.0,
});
```

### Environment Detection

Configure different settings per environment:

```typescript
Sentry.init({
  environment: process.env.NODE_ENV,
  enabled: process.env.NODE_ENV !== 'development', // Disable in dev

  beforeSend(event, hint) {
    // Filter out specific errors
    if (event.exception?.values?.[0]?.value?.includes('ResizeObserver')) {
      return null; // Don't send to Sentry
    }
    return event;
  },
});
```

### Source Maps

Ensure source maps are uploaded for readable stack traces:

```typescript
// next.config.js (added by Sentry wizard)
const { withSentryConfig } = require('@sentry/nextjs');

module.exports = withSentryConfig(
  nextConfig,
  {
    silent: true,
    org: process.env.SENTRY_ORG,
    project: process.env.SENTRY_PROJECT,
  },
  {
    hideSourceMaps: true,
    widenClientFileUpload: true,
  }
);
```

## Best Practices

1. **Use logger wrapper**: Centralize logging for consistency
2. **Set user context**: Associate errors with users for debugging
3. **Add breadcrumbs**: Track user journey before errors
4. **Monitor performance**: Use tracing for slow operations
5. **Filter noise**: Exclude known non-critical errors
6. **Configure sample rates**: Balance visibility with quota
7. **Test in staging**: Verify Sentry integration before production
8. **Review regularly**: Check Sentry dashboard for patterns

## Troubleshooting

**Sentry not capturing errors**: Check DSN is correct and Sentry is initialized. Verify `instrumentation.ts` exports `register()`.

**Source maps not working**: Ensure auth token is set and source maps are uploaded during build. Check Sentry dashboard > Settings > Source Maps.

**High quota usage**: Reduce sample rates in production. Filter out noisy errors with `beforeSend`.

**Traces not appearing**: Verify `tracesSampleRate` > 0. Check OpenTelemetry is initialized in `instrumentation.ts`.

**Client errors not captured**: Ensure `NEXT_PUBLIC_SENTRY_DSN` is set and accessible from browser.

## Resources

### scripts/

No executable scripts needed for this skill.

### references/

- `sentry-best-practices.md` - Error handling patterns, performance monitoring strategies, and quota management
- `otel-integration.md` - OpenTelemetry concepts, custom instrumentation, and distributed tracing setup

### assets/

- `sentry-server-config.ts` - Server-side Sentry configuration with tracing and sampling
- `sentry-client-config.ts` - Client-side Sentry configuration with replay and error boundaries
- `instrumentation.ts` - OpenTelemetry initialization and Sentry integration
- `logger.ts` - Structured logging wrapper with Sentry integration
- `error-boundary.tsx` - React error boundary component for client-side error handling
- `error-page.tsx` - Custom error page for Server Component errors
- `global-error.tsx` - Global error handler for root layout errors
