---
name: oRPC Better Auth Integration
description: Use Better Auth inside your oRPC projects without any extra overhead.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Better Auth Integration

[Better Auth](https://better-auth.com/) is a framework-agnostic, universal authentication and authorization framework for TypeScript.

## Step 1: Define Context Headers

Access request headers in your context — manually or via the [Request Headers Plugin](/docs/plugins/request-headers).

### Option A: Manual

```ts
import { os } from '@orpc/server'

export const base = os.$context<{ headers: Headers }>()
```

### Option B: Request Headers Plugin

Use the plugin's setup.

## Step 2: Create Auth Middleware

```ts
import { auth } from './auth' // Your Better Auth instance
import { base } from './context'
import { ORPCError } from '@orpc/server'

export const authMiddleware = base.middleware(async ({ context, next }) => {
  const sessionData = await auth.api.getSession({
    headers: context.headers,
  })

  if (!sessionData?.session || !sessionData?.user) {
    throw new ORPCError('UNAUTHORIZED')
  }

  return next({
    context: {
      session: sessionData.session,
      user: sessionData.user
    },
  })
})
```

## Usage

Create an `authorized` base that includes the auth middleware:

```ts
import { base } from './context'
import { authMiddleware } from './middlewares/auth'

export const authorized = base.use(authMiddleware)
```

Now use it to create authenticated procedures:

```ts
import { authorized } from './authorized'

export const getMessages = authorized.handler(({ context }) => {
  // context.session and context.user are guaranteed to be defined
})
```
