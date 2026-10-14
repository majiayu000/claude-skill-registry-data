---
name: oRPC Browser Adapter
description: Type-safe communication between browser scripts using Message Port Adapter.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Browser Adapter

Enable type-safe communication between browser scripts using the [Message Port Adapter](/docs/adapters/message-port).

## Between Extension Scripts

> Browser extension Message Passing API doesn't support transferring binary data. Workaround: extend the RPC JSON Serializer to encode binary data as Base64.

**Server (background/content script):**

```ts
import { RPCHandler } from '@orpc/server/message-port'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  interceptors: [onError(e => console.error(e))],
})

browser.runtime.onConnect.addListener((port) => {
  handler.upgrade(port, { context: {} })
})
```

**Client:**

```ts
import { RPCLink } from '@orpc/client/message-port'

const port = browser.runtime.connect()

const link = new RPCLink({ port })
```

## Window to Window

**Opener:**

```ts
const handler = new RPCHandler(router)

window.addEventListener('message', (event) => {
  if (event.data instanceof MessagePort) {
    handler.upgrade(event.data, { context: {} })
    event.data.start()
  }
})

window.open('/example/popup', 'popup', 'width=680,height=520')
```

**Popup:**

```ts
const { port1: serverPort, port2: clientPort } = new MessageChannel()

window.opener.postMessage(serverPort, '*', [serverPort])

const link = new RPCLink({ port: clientPort })

clientPort.start()
```

## Advanced Relay Pattern

For scripts running in the ["MAIN" world](https://developer.chrome.com/docs/extensions/reference/manifest/content-scripts#world-timings) that can't access `browser.runtime`, use a relay content script in the **"ISOLATED" world**:

```ts
// relay
window.addEventListener('message', (event) => {
  if (event.data instanceof MessagePort) {
    const port = browser.runtime.connect()

    event.data.addEventListener('message', e => port.postMessage(e.data))
    event.data.addEventListener('close', () => port.disconnect())
    port.onMessage.addListener(msg => event.data.postMessage(msg))
    port.onDisconnect.addListener(() => event.data.close())

    event.data.start()
  }
})
```
