---
name: oRPC Encryption Helpers
description: Functions to encrypt and decrypt sensitive data using AES-GCM.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Encryption Helpers

Encryption helpers provide functions to encrypt and decrypt sensitive data using AES-GCM with PBKDF2 key derivation.

> Encryption is more CPU-intensive than [signing](/docs/helpers/signing). For edge runtimes like Cloudflare Workers, ensure >200ms per request budget.

```ts
import { decrypt, encrypt } from '@orpc/server/helpers'

const secret = 'your-encryption-key'
const sensitiveData = 'user-email@example.com'

const encryptedData = await encrypt(sensitiveData, secret)
// 'Rq7wF8...' (base64url encoded, unreadable)

const decryptedData = await decrypt(encryptedData, secret)
// 'user-email@example.com'
```

> `decrypt` accepts `undefined`/`null` and returns `undefined` for invalid inputs.
