---
name: oRPC Electron Adapter
description: Use oRPC inside an Electron project via Message Port Adapter.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Electron Adapter

Establish type-safe communication between processes in [Electron](https://www.electronjs.org/) using the [Message Port Adapter](/docs/adapters/message-port).

## Main Process

Listen for a port sent from the renderer, then upgrade it:

```ts
import { RPCHandler } from '@orpc/server/message-port'
import { onError } from '@orpc/server'

const handler = new RPCHandler(router, {
  interceptors: [onError(e => console.error(e))],
})

app.whenReady().then(() => {
  ipcMain.on('start-orpc-server', async (event) => {
    const [serverPort] = event.ports
    handler.upgrade(serverPort)
    serverPort.start()
  })
})
```

## Preload Process

Forward the port from renderer to main:

```ts
window.addEventListener('message', (event) => {
  if (event.data === 'start-orpc-client') {
    const [serverPort] = event.ports
    ipcRenderer.postMessage('start-orpc-server', null, [serverPort])
  }
})
```

## Renderer Process

```ts
const { port1: clientPort, port2: serverPort } = new MessageChannel()

window.postMessage('start-orpc-client', '*', [serverPort])

const link = new RPCLink({ port: clientPort })

clientPort.start()
```
