---
name: oRPC No Throw Literal
description: Always throw Error instances instead of literal values.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# No Throw Literal

In JavaScript, you can throw any value, but it's best to throw only `Error` instances.

```ts
// eslint-disable-next-line no-throw-literal
throw 'error' // ✗ avoid
throw new Error('error') // ✓ recommended
```

> oRPC treats thrown `Error` instances as best practice, as recommended by [JavaScript Standard Style](https://standardjs.com/rules.html#throw-new-error-old-style).

## Configuration

Customize behavior by setting `throwableError` in the `Registry`:

```ts
declare module '@orpc/server' { // or '@orpc/contract', '@orpc/client'
  interface Registry {
    throwableError: Error
  }
}
```

> Avoid `any`/`unknown` for `throwableError` because it prevents the client from inferring type-safe errors. Use `null | undefined | {}` (equivalent to `unknown`) for stricter inference.

> If you configure `throwableError` as `null | undefined | {}`, check `isSuccess` instead of `error`:

```ts
const { error, data, isSuccess } = await safe(client('input'))

if (!isSuccess) {
  if (isDefinedError(error)) {
    // handle type-safe error
  }
} else {
  // handle success
}
```

## Bonus

Enable the ESLint [no-throw-literal](https://eslint.org/docs/rules/no-throw-literal) rule.
