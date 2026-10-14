---
name: oRPC Request Validation Plugin
description: A plugin that blocks invalid requests before they reach your server.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Request Validation Plugin

Ensures only valid requests are sent to your server. Especially useful for applications that depend on server-side validation.

> Best suited for [Contract-First Development](/docs/contract-first/define-contract). [Minified Contract](/docs/contract-first/router-to-contract#minify-export-the-contract-router-for-the-client) is **not supported**.

## Setup

```ts
import { RPCLink } from '@orpc/client/fetch'
import { RequestValidationPlugin } from '@orpc/contract/plugins'

const link = new RPCLink({
  url: 'http://localhost:3000/rpc',
  plugins: [
    new RequestValidationPlugin(contract),
  ],
})

const client: ContractRouterClient<typeof contract> = createORPCClient(link)
```

> The `link` can be any supported oRPC link.

## Form Validation

Remove heavy form validation libraries and rely on oRPC's validation errors:

```tsx
import { getIssueMessage, parseFormData } from '@orpc/openapi-client/helpers'

export function ContactForm() {
  const [error, setError] = useState()

  const handleSubmit = async (form: FormData) => {
    try {
      const output = await client.someProcedure(parseFormData(form))
      console.log(output)
    } catch (error) {
      setError(error)
    }
  }

  return (
    <form action={handleSubmit}>
      <input name="user[name]" type="text" />
      <span>{getIssueMessage(error, 'user[name]')}</span>

      <input name="user[emails][]" type="email" />
      <span>{getIssueMessage(error, 'user[emails][]')}</span>

      <button type="submit">Submit</button>
    </form>
  )
}
```
