---
name: oRPC RPC Protocol
description: Learn about the RPC protocol used by RPCHandler.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# RPC Protocol

The RPC protocol enables remote procedure calls over HTTP using JSON, supporting native data types.

## Routing

Procedure determined by `pathname`:

```bash
curl https://example.com/rpc/planet/create
```

Calls `planet.create` with `/rpc` prefix.

## Input

Input can be in URL query parameters or request body.

> Default RPCHandler blocks GET requests via [StrictGetMethodPlugin](/docs/plugins/strict-get-method) except for explicit allowed.

### Input in URL Query

```ts
const url = new URL('https://example.com/rpc/planet/create')

url.searchParams.append('data', JSON.stringify({
  json: {
    name: 'Earth',
    detached_at: '2022-01-01T00:00:00.000Z'
  },
  meta: [[1, 'detached_at']]
}))

const response = await fetch(url)
```

### Input in Request Body

```bash
curl -X POST https://example.com/rpc/planet/create \
  -H 'Content-Type: application/json' \
  -d '{
    "json": {
      "name": "Earth",
      "detached_at": "2022-01-01T00:00:00.000Z"
    },
    "meta": [[1, "detached_at"]]
  }'
```

### Input with File

```ts
const form = new FormData()

form.set('data', JSON.stringify({
  json: {
    name: 'Earth',
    thumbnail: {},
    images: [{}, {}]
  },
  meta: [[1, 'detached_at']],
  maps: [['images', 0], ['images', 1]]
}))

form.set('0', new Blob([''], { type: 'image/png' }))
form.set('1', new Blob([''], { type: 'image/png' }))

await fetch('https://example.com/rpc/planet/create', {
  method: 'POST',
  body: form
})
```

## Success Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "json": {
    "id": "1",
    "name": "Earth",
    "detached_at": "2022-01-01T00:00:00.000Z"
  },
  "meta": [[0, "id"], [1, "detached_at"]]
}
```

## Error Response

```http
HTTP/1.1 500 Internal Server Error

{
  "json": {
    "defined": false,
    "code": "INTERNAL_SERVER_ERROR",
    "status": 500,
    "message": "Internal server error",
    "data": {}
  },
  "meta": []
}
```

## Meta

Format: `[type: number, ...path: (string | number)[]]`

### Supported Types

| Type | Description |
| ---- | ----------- |
| 0    | bigint      |
| 1    | date        |
| 2    | nan         |
| 3    | undefined   |
| 4    | url         |
| 5    | regexp      |
| 6    | set         |
| 7    | map         |

## Maps

Used with `FormData` to map files/blobs to paths in `json`.
