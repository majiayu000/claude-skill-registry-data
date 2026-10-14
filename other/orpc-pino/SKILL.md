---
name: oRPC Pino Integration
description: Integrate oRPC with Pino for structured logging and request tracking.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Pino Integration

[Pino](https://getpino.io/) is a fast and lightweight JSON logger.

## Installation

```sh
npm install @orpc/experimental-pino@latest pino@latest
```

## Setup

```ts
import { LoggingHandlerPlugin } from '@orpc/experimental-pino'
import pino from 'pino'

const logger = pino()

const handler = new RPCHandler(router, {
  plugins: [
    new LoggingHandlerPlugin({
      logger,
      generateId: ({ request }) => crypto.randomUUID(),
      logRequestResponse: true,
      logRequestAbort: true,
    }),
  ],
})
```

> For development, use [pino-pretty](https://github.com/pinojs/pino-pretty):

```bash
npm run dev | npx pino-pretty
```

## Using the Logger

```ts
import { getLogger, LoggerContext } from '@orpc/experimental-pino'

interface ORPCContext extends LoggerContext {}

const procedure = os
  .$context<ORPCContext>()
  .handler(({ context }) => {
    const logger = getLogger(context)

    logger?.info('Processing request')
    logger?.debug({ userId: 123 }, 'User data')

    return { success: true }
  })
```

## Custom Logger per Request

Useful when integrating with [pino-http](https://github.com/pinojs/pino-http):

```ts
import {
  CONTEXT_LOGGER_SYMBOL,
  LoggerContext,
  LoggingHandlerPlugin
} from '@orpc/experimental-pino'

const logger = pino()
const httpLogger = pinoHttp({ logger })

interface ORPCContext extends LoggerContext {}

const handler = new RPCHandler(router, {
  plugins: [new LoggingHandlerPlugin({ logger })],
})

const server = createServer(async (req, res) => {
  httpLogger(req, res)

  const { matched } = await handler.handle(req, res, {
    prefix: '/api',
    context: {
      [CONTEXT_LOGGER_SYMBOL]: req.log,
    },
  })

  if (!matched) {
    res.statusCode = 404
    res.end('Not Found')
  }
})
```
