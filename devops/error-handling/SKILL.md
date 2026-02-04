---
name: error-handling
description: Comprehensive error handling patterns for API responses, React Error Boundaries, webhook processing, user-facing messages, and monitoring with Baselime.
---

# Error Handling

## Key Files

- Error utilities: `shared/utils/errors.ts`
- Global error boundary: `app/error.tsx`
- Baselime monitoring: `client/components/monitoring/BaselimeProvider.tsx`
- API middleware patterns: `app/api/*/route.ts`

## Standard Error Response Format

All API errors must follow the standardized format:

```typescript
interface IErrorResponse {
  success: false;
  error: {
    code: ErrorCode | string;
    message: string;
    details?: Record<string, unknown>;
    requestId?: string;
  };
}

// Usage
import { createErrorResponse, ErrorCodes } from '@shared/utils/errors';

return createErrorResponse(
  ErrorCodes.INSUFFICIENT_CREDITS,
  'You need 5 credits to upscale this image',
  402,
  { required: 5, current: 2 }
);
```

## Common Error Codes

Use predefined error codes from `ErrorCodes`:

```typescript
// 4xx Client Errors
ErrorCodes.INVALID_REQUEST - Malformed request
ErrorCodes.UNAUTHORIZED - Authentication required
ErrorCodes.FORBIDDEN - Permission denied
ErrorCodes.NOT_FOUND - Resource not found
ErrorCodes.INSUFFICIENT_CREDITS - Not enough credits
ErrorCodes.RATE_LIMITED - Too many requests
ErrorCodes.VALIDATION_ERROR - Invalid data
ErrorCodes.TIER_RESTRICTED - Feature requires higher tier

// 5xx Server Errors
ErrorCodes.INTERNAL_ERROR - Unexpected server error
ErrorCodes.AI_UNAVAILABLE - AI service down
ErrorCodes.PROCESSING_FAILED - Processing operation failed
```

## React Error Boundaries

### Global Error Boundary

The global error boundary (`app/error.tsx`) catches all unhandled errors:

```typescript
'use client';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log to monitoring
    console.error('Global error caught:', error);

    // Send to Baselime if available
    if (window.baselime) {
      window.baselime.logError(error, {
        digest: error.digest,
        boundary: 'global-error',
      });
    }
  }, [error]);

  return (
    <div>
      <h1>Application Error</h1>
      <p>We encountered an unexpected error.</p>
      <button onClick={reset}>Try Again</button>
    </div>
  );
}
```

### Component-Level Error Boundaries

Create reusable error boundaries for specific features:

```typescript
'use client';

interface IErrorBoundaryProps {
  children: ReactNode;
  fallback?: ComponentType<{ error: Error; reset: () => void }>;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

export function ErrorBoundary({
  children,
  fallback: FallbackComponent,
  onError
}: IErrorBoundaryProps) {
  return (
    <div className="error-boundary">
      {children}
    </div>
  );
}
```

## API Route Error Handling

### Route Handler Pattern

```typescript
import { createErrorResponse, ErrorCodes } from '@shared/utils/errors';
import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Validate request
    const body = await request.json();
    if (!body.required) {
      return createErrorResponse(ErrorCodes.VALIDATION_ERROR, 'Missing required field: required');
    }

    // Process request
    const result = await processData(body);

    return Response.json({ success: true, data: result });
  } catch (error) {
    console.error('Route handler error:', error);

    // Handle specific errors
    if (error instanceof AppError) {
      return createErrorResponse(error.code, error.message, error.statusCode, error.details);
    }

    // Handle unexpected errors
    return createErrorResponse(ErrorCodes.INTERNAL_ERROR, 'An unexpected error occurred', 500);
  }
}
```

### Validation Error Pattern

```typescript
import { z } from 'zod';
import { createErrorResponse, ErrorCodes } from '@shared/utils/errors';

const schema = z.object({
  email: z.string().email(),
  credits: z.number().min(0),
});

export async function validateInput(data: unknown) {
  try {
    return schema.parse(data);
  } catch (error) {
    if (error instanceof z.ZodError) {
      return createErrorResponse(ErrorCodes.VALIDATION_ERROR, 'Invalid request data', 400, {
        fields: error.errors.map(e => e.path.join('.')),
      });
    }
    throw error;
  }
}
```

## Webhook Error Handling

### Stripe Webhooks

```typescript
import Stripe from 'stripe';
import { createErrorResponse, ErrorCodes } from '@shared/utils/errors';

export async function handleWebhook(request: Request) {
  const body = await request.text();
  const signature = request.headers.get('stripe-signature');

  try {
    // Verify webhook signature
    const event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET
    );

    // Process event
    await processWebhookEvent(event);

    return Response.json({ received: true });
  } catch (error) {
    // Retry on signature verification failure
    if (error instanceof Stripe.errors.StripeSignatureError) {
      console.error('Webhook signature verification failed:', error);
      return new Response('Webhook signature verification failed', {
        status: 401,
      });
    }

    // Log other errors but respond with success to avoid retries
    console.error('Webhook processing error:', error);
    return Response.json({ received: true });
  }
}
```

### Retry Pattern for Webhooks

```typescript
export async function processWithRetry<T>(
  operation: () => Promise<T>,
  maxRetries: number = 3,
  delay: number = 1000
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error as Error;

      if (attempt === maxRetries) {
        break;
      }

      // Exponential backoff
      await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, attempt)));
    }
  }

  throw lastError!;
}
```

## User-Facing Error Messages

### Client-Side Error Display

```typescript
'use client';

import { useNotificationStore } from '@client/store/notifications';

interface IApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

export function useErrorHandler() {
  const { addNotification } = useNotificationStore();

  return (error: IApiError | Error | unknown) => {
    if (error && typeof error === 'object' && 'code' in error) {
      const apiError = error as IApiError;

      // Map error codes to user-friendly messages
      const userMessages: Record<string, string> = {
        [ErrorCodes.INSUFFICIENT_CREDITS]:
          'You need more credits to perform this action. Please upgrade your plan.',
        [ErrorCodes.RATE_LIMITED]: 'Too many requests. Please wait a moment and try again.',
        [ErrorCodes.TIER_RESTRICTED]: 'This feature is available with a paid subscription.',
        [ErrorCodes.AI_UNAVAILABLE]:
          'Our AI service is temporarily unavailable. Please try again later.',
      };

      const message = userMessages[apiError.code] || apiError.message;

      addNotification({
        type: 'error',
        title: 'Error',
        message,
        duration: 5000,
      });
    } else {
      // Handle generic errors
      addNotification({
        type: 'error',
        title: 'Error',
        title: 'An unexpected error occurred',
        message: 'Please try again or contact support if the issue persists.',
        duration: 5000,
      });
    }
  };
}
```

### Graceful Degradation

```typescript
'use client';

interface IDataLoaderProps {
  url: string;
  fallback?: ReactNode;
  children: (data: unknown) => ReactNode;
}

export function DataLoader({ url, fallback, children }: IDataLoaderProps) {
  const { data, error, isLoading } = useFetch(url);

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (error) {
    // Show fallback if provided
    if (fallback) {
      return fallback;
    }

    // Show error message with retry
    return (
      <div className="error-state">
        <p>Failed to load data</p>
        <button onClick={() => window.location.reload()}>
          Try Again
        </button>
      </div>
    );
  }

  return <>{children(data)}</>;
}
```

## Error Monitoring with Baselime

### Setup Provider

```typescript
// app/providers.tsx
import { BaselimeProvider } from '@client/components/monitoring/BaselimeProvider';

export function Providers({ children }: { children: ReactNode }) {
  return (
    <BaselimeProvider>
      <QueryClientProvider>{children}</QueryClientProvider>
    </BaselimeProvider>
  );
}
```

### Error Logging

```typescript
// Custom error logging hook
export function useErrorLogging() {
  return (error: Error, context?: Record<string, unknown>) => {
    // Always log to console
    console.error('Application error:', error, context);

    // Send to Baselime if available
    if (typeof window !== 'undefined' && window.baselime) {
      window.baselime.logError(error, {
        url: window.location.href,
        userAgent: navigator.userAgent,
        timestamp: new Date().toISOString(),
        ...context,
      });
    }
  };
}
```

### Server-Side Error Logging

```typescript
// server/utils/logging.ts
import baselime from '@baselime/node-logger';

export function logError(error: Error, context?: Record<string, unknown>) {
  const logData = {
    error: {
      name: error.name,
      message: error.message,
      stack: error.stack,
    },
    context,
    timestamp: new Date().toISOString(),
  };

  console.error('Server error:', logData);

  // Send to Baselime
  baselime.error('Server error', logData);
}
```

## Error Handling Best Practices

### 1. Validate Early, Fail Fast

```typescript
// Good: Validate at the edge
export async function handleUpload(request: Request) {
  const { file, options } = await validateUploadRequest(request);
  // Proceed with valid data
}

// Bad: Validate deep in the logic
export async function processUpload(data: unknown) {
  // Validate here after expensive operations
}
```

### 2. Use Specific Error Types

```typescript
// Create custom error classes
export class InsufficientCreditsError extends AppError {
  constructor(required: number, current: number) {
    super(ErrorCodes.INSUFFICIENT_CREDITS, `Need ${required} credits, have ${current}`, 402, {
      required,
      current,
    });
  }
}
```

### 3. Never Expose Stack Traces to Users

```typescript
// Good: Safe error responses
return createErrorResponse(ErrorCodes.INTERNAL_ERROR, 'An unexpected error occurred');

// Bad: Exposing internals
return Response.json({
  error: error.stack, // Security risk!
});
```

### 4. Implement Circuit Breakers

```typescript
class CircuitBreaker {
  private failures = 0;
  private lastFailure = 0;
  private state: 'closed' | 'open' | 'half-open' = 'closed';

  async execute<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      throw new Error('Circuit breaker is open');
    }

    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
}
```

### 5. Request ID Tracking

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  const requestId = crypto.randomUUID();
  request.headers.set('x-request-id', requestId);
  // Continue...
}

// API route
export async function GET(request: NextRequest) {
  const requestId = request.headers.get('x-request-id');

  try {
    // Process request...
  } catch (error) {
    return createErrorResponse(
      ErrorCodes.INTERNAL_ERROR,
      'An error occurred',
      500,
      undefined,
      requestId
    );
  }
}
```

## Testing Error Scenarios

```typescript
// Test error responses
describe('API Error Handling', () => {
  it('returns proper error format for validation errors', async () => {
    const response = await POST(
      new Request('http://localhost/api/test', {
        method: 'POST',
        body: JSON.stringify({ invalid: 'data' }),
      })
    );

    const body = await response.json();

    expect(response.status).toBe(400);
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('VALIDATION_ERROR');
    expect(body.error.message).toBeDefined();
  });
});
```

## Environment-Specific Handling

```typescript
// Development: Show detailed errors
if (isDevelopment()) {
  return createErrorResponse(ErrorCodes.INTERNAL_ERROR, error.message, 500, { stack: error.stack });
}

// Production: Generic error message
return createErrorResponse(ErrorCodes.INTERNAL_ERROR, 'An unexpected error occurred');
```
