---
name: oRPC Form Data Helpers
description: Utilities for parsing form data and handling validation errors with bracket notation support.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Form Data Helpers

Form data helpers provide utilities for parsing HTML form data and extracting validation error messages, with full support for [bracket notation](/docs/openapi/bracket-notation).

## `parseFormData`

```ts
import { parseFormData } from '@orpc/openapi-client/helpers'

const form = new FormData()
form.append('name', 'John')
form.append('user[email]', 'john@example.com')
form.append('user[hobbies][]', 'reading')
form.append('user[hobbies][]', 'gaming')

const parsed = parseFormData(form)
// {
//   name: 'John',
//   user: {
//     email: 'john@example.com',
//     hobbies: ['reading', 'gaming']
//   }
// }
```

## `getIssueMessage`

```ts
import { getIssueMessage } from '@orpc/openapi-client/helpers'

const error = {
  data: {
    issues: [
      { path: ['user', 'email'], message: 'Invalid email format' }
    ]
  }
}

const emailError = getIssueMessage(error, 'user[email]')
// 'Invalid email format'

const tagError = getIssueMessage(error, 'user[tags][]')

const anyError = getIssueMessage('anything', 'path')
// undefined if cannot find issue
```

> `getIssueMessage` requires standard schema issue format with issues in `data.issues`.

## Usage Example

```tsx
import { getIssueMessage, parseFormData } from '@orpc/openapi-client/helpers'

export function ContactForm() {
  const [error, setError] = useState()

  const handleSubmit = (form: FormData) => {
    try {
      const data = parseFormData(form)
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
