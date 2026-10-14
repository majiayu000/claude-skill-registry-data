---
name: oRPC Cookie Helpers
description: Functions for managing HTTP cookies in web applications.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Cookie Helpers

The Cookie helpers provide functions to set and get HTTP cookies.

```ts
import { deleteCookie, getCookie, setCookie } from '@orpc/server/helpers'

const reqHeaders = new Headers()
const resHeaders = new Headers()

setCookie(resHeaders, 'sessionId', 'abc123', {
  secure: true,
  maxAge: 3600
})

deleteCookie(resHeaders, 'sessionId')

const sessionId = getCookie(reqHeaders, 'sessionId')
```

> Both helpers accept `undefined` as headers for seamless integration with [Request Headers Plugin](/docs/plugins/request-headers) or [Response Headers Plugin](/docs/plugins/response-headers).

## Security with Signing and Encryption

Combine cookies with [signing](/docs/helpers/signing) or [encryption](/docs/helpers/encryption):

```ts
import { getCookie, setCookie, sign, unsign } from '@orpc/server/helpers'

const secret = 'your-secret-key'

setCookie(resHeaders, 'sessionId', await sign('abc123', secret), {
  httpOnly: true,
  secure: true,
  maxAge: 3600
})

const signedSessionId = await unsign(getCookie(reqHeaders, 'sessionId'), secret)
```
