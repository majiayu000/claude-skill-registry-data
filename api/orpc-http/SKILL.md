---
name: oRPC HTTP Adapter
description: How to use oRPC over HTTP with various server and client adapters.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# HTTP

oRPC includes built-in HTTP support, making it easy to expose RPC endpoints.

## Server Adapters

| Adapter      | Target                                                                                              |
| ------------ | --------------------------------------------------------------------------------------------------- |
| `fetch`      | [MDN Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) (Browser, Bun, Deno, Cloudflare Workers) |
| `node`       | Node.js built-in [`http`](https://nodejs.org/api/http.html)/[`http2`](https://nodejs.org/api/http2.html) |
| `fastify`    | [Fastify](https://fastify.dev/)                                                                     |
| `aws-lambda` | [AWS Lambda](https://aws.amazon.com/lambda/)                                                        |

### Node.js Example

```ts
import { createServer } from 'node:http'
import { RPCHandler } from '@orpc/server/node'
import { CORSPlugin } from '@orpc/server/plugins'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  plugins: [new CORSPlugin()],
  interceptors: [onError(e => console.error(e))],
})

const server = createServer(async (req, res) => {
  const { matched } = await handler.handle(req, res, {
    prefix: '/rpc',
    context: {}
  })

  if (matched) return

  res.statusCode = 404
  res.end('Not found')
})

server.listen(3000)
```

### Bun Example

```ts
Bun.serve({
  async fetch(request: Request) {
    const { matched, response } = await handler.handle(request, {
      prefix: '/rpc',
      context: {}
    })
    if (matched) return response
    return new Response('Not found', { status: 404 })
  }
})
```

### Cloudflare Workers Example

```ts
export default {
  async fetch(request: Request, env: any, ctx: ExecutionContext) {
    const { matched, response } = await handler.handle(request, {
      prefix: '/rpc',
      context: {}
    })
    if (matched) return response
    return new Response('Not found', { status: 404 })
  }
}
```

### AWS Lambda Example

```ts
import { APIGatewayProxyEventV2 } from 'aws-lambda'
import { RPCHandler } from '@orpc/server/aws-lambda'

export const handler = awslambda.streamifyResponse<APIGatewayProxyEventV2>(async (event, responseStream, context) => {
  const { matched } = await rpcHandler.handle(event, responseStream, {
    prefix: '/rpc',
    context: {}
  })

  if (matched) return

  awslambda.HttpResponseStream.from(responseStream, { statusCode: 404 })
  responseStream.write('Not found')
  responseStream.end()
})
```

## Client Adapters

| Adapter | Target           |
| ------- | ---------------- |
| `fetch` | MDN Fetch API    |

```ts
import { RPCLink } from '@orpc/client/fetch'

const link = new RPCLink({
  url: 'http://localhost:3000/rpc',
  headers: () => ({ 'x-api-key': 'my-api-key' }),
})
```

## Event Iterator Options

HTTP adapters provide reliability features for streaming Event Iterators:

```ts
const handler = new RPCHandler(router, {
  eventIteratorInitialCommentEnabled: true,
  eventIteratorInitialComment: 'start',
  eventIteratorKeepAliveEnabled: true,
  eventIteratorKeepAliveInterval: 5000,
  eventIteratorKeepAliveComment: '',
})
```

### Initial Comment

Sends comment when stream starts to flush response headers early.

* `eventIteratorInitialCommentEnabled` (default: `true`)
* `eventIteratorInitialComment` (default: `''`)

### Keep-Alive Comments

Sends periodic comments during inactivity to prevent timeouts.

* `eventIteratorKeepAliveEnabled` (default: `true`)
* `eventIteratorKeepAliveInterval` (default: `5000`)
* `eventIteratorKeepAliveComment` (default: `''`)
