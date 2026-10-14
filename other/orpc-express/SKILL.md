---
name: oRPC Express.js Adapter
description: Use oRPC inside an Express.js project.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Express.js Adapter

[Express.js](https://expressjs.com/) integration.

> Express's [body-parser](https://expressjs.com/en/resources/middleware/body-parser.html) handles common content types and oRPC will use the parsed body. But it doesn't support [Bracket Notation](/docs/openapi/bracket-notation). Register body-parsing middleware **after** your oRPC middleware or only on non-oRPC routes.

## Basic

```ts
import express from 'express'
import cors from 'cors'
import { RPCHandler } from '@orpc/server/node'
import { onError } from '@orpc/server'

const app = express()
app.use(cors())

const handler = new RPCHandler(router, {
  interceptors: [onError(e => console.error(e))],
})

app.use('/rpc{/*path}', async (req, res, next) => {
  const { matched } = await handler.handle(req, res, {
    prefix: '/rpc',
    context: {},
  })

  if (matched) return
  next()
})

app.listen(3000, () => console.log('Server listening on port 3000'))
```

> The `handler` can be any supported oRPC handler.
