---
name: oRPC React Native Adapter
description: Use oRPC inside a React Native project.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# React Native Adapter

[React Native](https://reactnative.dev/) integration.

## Fetch Link

React Native includes a [Fetch API](https://reactnative.dev/docs/network), so oRPC works out of the box.

> Fetch in React Native is limited. oRPC features like [File/Blob](/docs/file-upload-download) and [Event Iterator](/docs/event-iterator) aren't supported. Follow [Support Stream #27741](https://github.com/facebook/react-native/issues/27741) for updates.

> For binary data, extend the [RPC JSON Serializer](/docs/advanced/rpc-json-serializer#extending-native-data-types) to encode as Base64.

```ts
import { RPCLink } from '@orpc/client/fetch'

const link = new RPCLink({
  url: 'http://localhost:3000/rpc',
  headers: async ({ context }) => ({
    'x-api-key': context?.something ?? ''
  })
})
```

## `expo/fetch`

If using [Expo](https://expo.dev/), use [`expo/fetch`](https://docs.expo.dev/versions/latest/sdk/expo/#expofetch-api) to expand support for [Event Iterator](/docs/event-iterator):

```ts
export const link = new RPCLink({
  url: `http://localhost:3000/rpc`,
  async fetch(request, init) {
    const { fetch } = await import('expo/fetch')

    const resp = await fetch(request.url, {
      body: await request.blob(),
      headers: request.headers,
      method: request.method,
      signal: request.signal,
      ...init,
    })

    return resp
  },
})
```
