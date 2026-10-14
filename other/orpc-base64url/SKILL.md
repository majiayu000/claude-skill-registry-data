---
name: oRPC Base64Url Helpers
description: Functions to encode and decode base64url strings (URL-safe variant of base64).
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Base64Url Helpers

Base64Url helpers provide functions to encode and decode base64url strings, a URL-safe variant of base64 encoding used in web tokens, data serialization, and APIs.

```ts
import { decodeBase64url, encodeBase64url } from '@orpc/server/helpers'

const originalText = 'Hello World'
const textBytes = new TextEncoder().encode(originalText)
const encodedData = encodeBase64url(textBytes)
const decodedBytes = decodeBase64url(encodedData)
const decodedText = new TextDecoder().decode(decodedBytes) // 'Hello World'
```

> `decodeBase64url` accepts `undefined` or `null` and returns `undefined` for invalid inputs.
