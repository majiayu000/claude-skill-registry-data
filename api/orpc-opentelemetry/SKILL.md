---
name: oRPC OpenTelemetry Integration
description: Integrate oRPC with OpenTelemetry for distributed tracing.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# OpenTelemetry Integration

[OpenTelemetry](https://opentelemetry.io/) provides observability APIs and instrumentation for applications.

## Installation

```sh
npm install @orpc/otel@latest
```

## Setup

```ts
// server
import { NodeSDK } from '@opentelemetry/sdk-node'
import { ORPCInstrumentation } from '@orpc/otel'

const sdk = new NodeSDK({
  instrumentations: [
    new ORPCInstrumentation(),
  ],
})

sdk.start()
```

```ts
// client
import { WebTracerProvider } from '@opentelemetry/sdk-trace-web'
import { registerInstrumentations } from '@opentelemetry/instrumentation'
import { ORPCInstrumentation } from '@orpc/otel'

const provider = new WebTracerProvider()
provider.register()

registerInstrumentations({
  instrumentations: [new ORPCInstrumentation()],
})
```

## Middleware Span

```ts
import { trace } from '@opentelemetry/api'

export const someMiddleware = os.middleware(async (ctx, next) => {
  const span = trace.getActiveSpan()

  span?.setAttribute('someAttribute', 'someValue')
  span?.addEvent('someEvent')

  return next()
})

Object.defineProperty(someMiddleware, 'name', {
  value: 'someName',
})
```

> Define `name` property on middleware to improve span naming.

## Handling Uncaught Exceptions

```ts
import { SpanStatusCode, trace } from '@opentelemetry/api'

const tracer = trace.getTracer('uncaught-errors')

function recordError(eventName: string, reason: unknown) {
  const span = tracer.startSpan(eventName)
  const message = String(reason)

  if (reason instanceof Error) {
    span.recordException(reason)
  } else {
    span.recordException({ message })
  }

  span.setStatus({ code: SpanStatusCode.ERROR, message })
  span.end()
}

process.on('uncaughtException', (reason) => {
  recordError('uncaughtException', reason)
})

process.on('unhandledRejection', (reason) => {
  recordError('unhandledRejection', reason)
})
```

## Capture Abort Signals

```ts
const handler = new RPCHandler(router, {
  interceptors: [
    ({ request, next }) => {
      const span = trace.getActiveSpan()

      request.signal?.addEventListener('abort', () => {
        span?.addEvent('aborted', { reason: String(request.signal?.reason) })
      })

      return next()
    },
  ],
})
```

## Context Propagation

When using HTTP/fetch adapters, set up HTTP instrumentation for [context propagation](https://opentelemetry.io/docs/concepts/context-propagation/) on both client and server.
