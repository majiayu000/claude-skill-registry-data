---
name: oRPC SuperJson
description: Replace the default oRPC RPC serializer with SuperJson.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# SuperJson

Replace the default oRPC RPC serializer with [SuperJson](https://github.com/blitz-js/superjson).

> Default oRPC serializer is faster and more efficient, but SuperJson is widely adopted.

## SuperJson Serializer

> Only supports SuperJson-compatible data types plus `AsyncIteratorObject` at root for Event Iterator. Not all [RPC supported types](/docs/rpc-handler#supported-data-types) work.

```ts
import { createORPCErrorFromJson, ErrorEvent, isORPCErrorJson, mapEventIterator, toORPCError } from '@orpc/client'
import type { StandardRPCSerializer } from '@orpc/client/standard'
import { isAsyncIteratorObject } from '@orpc/shared'
import SuperJSON from 'superjson'

export class SuperJSONSerializer implements Pick<StandardRPCSerializer, keyof StandardRPCSerializer> {
  serialize(data: unknown): object {
    if (isAsyncIteratorObject(data)) {
      return mapEventIterator(data, {
        value: async (value) => SuperJSON.serialize(value),
        error: async (e) => new ErrorEvent({
          data: SuperJSON.serialize(toORPCError(e).toJSON()),
          cause: e,
        }),
      })
    }
    return SuperJSON.serialize(data)
  }

  deserialize(data: any): unknown {
    if (isAsyncIteratorObject(data)) {
      return mapEventIterator(data, {
        value: async value => SuperJSON.deserialize(value),
        error: async (e) => {
          if (!(e instanceof ErrorEvent)) return e
          const deserialized = SuperJSON.deserialize(e.data as any)
          if (isORPCErrorJson(deserialized)) {
            return createORPCErrorFromJson(deserialized, { cause: e })
          }
          return new ErrorEvent({ data: deserialized, cause: e })
        },
      })
    }
    return SuperJSON.deserialize(data)
  }
}
```

## SuperJson Handler

```ts
import { FetchHandler } from '@orpc/server/fetch'
import { StrictGetMethodPlugin } from '@orpc/server/plugins'
import { StandardHandler, StandardRPCCodec, StandardRPCMatcher } from '@orpc/server/standard'

export class SuperJSONHandler<T extends Context> extends FetchHandler<T> {
  constructor(router, options = {}) {
    options.plugins ??= []
    if (options.strictGetMethodPluginEnabled ?? true) {
      options.plugins.push(new StrictGetMethodPlugin())
    }

    const serializer = new SuperJSONSerializer()
    const matcher = new StandardRPCMatcher()
    const codec = new StandardRPCCodec(serializer as any)

    super(new StandardHandler(router, matcher, codec, options), options)
  }
}
```

## SuperJson Link

```ts
import { StandardLink, StandardRPCLinkCodec } from '@orpc/client/standard'
import { LinkFetchClient } from '@orpc/client/fetch'

export class SuperJSONLink<T extends ClientContext> extends StandardLink<T> {
  constructor(options) {
    const linkClient = new LinkFetchClient(options)
    const serializer = new SuperJSONSerializer()
    const linkCodec = new StandardRPCLinkCodec(serializer as any, options)

    super(linkCodec, linkClient, options)
  }
}
```
