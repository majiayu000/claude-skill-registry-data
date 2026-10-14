---
name: oRPC Sentry Integration
description: Integrate oRPC with Sentry for error tracking and performance monitoring.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Sentry Integration

Based on the [OpenTelemetry Integration](/docs/integrations/opentelemetry).

## Installation

```sh
npm install @orpc/otel@latest
```

## Setup

```ts
import * as Sentry from '@sentry/node'
import { ORPCInstrumentation } from '@orpc/otel'

Sentry.init({
  dsn: '...',
  sendDefaultPii: true,
  tracesSampleRate: 1.0,
  openTelemetryInstrumentations: [
    new ORPCInstrumentation(),
  ]
})
```

## Capturing Errors

Since Sentry does not yet collect [OpenTelemetry span events](https://opentelemetry.io/docs/concepts/signals/traces/#span-events), capture errors from business logic manually:

```ts
import * as Sentry from '@sentry/node'
import { os } from '@orpc/server'

export const sentryMiddleware = os.middleware(async ({ next }) => {
  try {
    return await next()
  } catch (error) {
    Sentry.captureException(error)
    throw error
  }
})

export const base = os.use(sentryMiddleware)
```
