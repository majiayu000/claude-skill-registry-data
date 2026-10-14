---
name: oRPC Server Action
description: Integrate oRPC procedures with React Server Actions.
license: MIT
metadata:
  author: Ali Torki
  homepage: https://github.com/ali-master
  version: "1.0.0"
---

# Server Action

React [Server Actions](https://react.dev/reference/rsc/server-functions) let client components invoke async server functions. With oRPC, append `.actionable` to enable Server Action compatibility.

## Server Side

```ts
'use server'

import { redirect } from 'next/navigation'
import { onError, onSuccess, os } from '@orpc/server'
import * as z from 'zod'

export const ping = os
  .input(z.object({ name: z.string() }))
  .handler(async ({ input }) => `Hello, ${input.name}`)
  .actionable({
    context: async () => ({}),
    interceptors: [
      onSuccess(async output => redirect(`/some-where`)),
      onError(async error => console.error(error)),
    ],
  })
```

> Use [Execution Context](/docs/context#execution-context) instead of [Initial Context](/docs/context#initial-context).

> Special errors (`redirect`, `notFound`) are only supported in [Next.js](https://nextjs.org/) and [TanStack Start](https://tanstack.com/start/latest).

## Client Side

```tsx
'use client'

import { ping } from './actions'

export function MyComponent() {
  const [name, setName] = useState('')

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    const [error, data] = await ping({ name })
    console.log(error, data)
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={name} onChange={e => setName(e.target.value)} />
      <button type="submit">Submit</button>
    </form>
  )
}
```

## Type-Safe Error Handling

```ts
export const someAction = os
  .input(z.object({ name: z.string() }))
  .errors({
    SOME_ERROR: {
      message: 'Some error message',
      data: z.object({ some: z.string() }),
    },
  })
  .handler(async ({ input }) => `Hello, ${input.name}`)
  .actionable()
```

```ts
'use client'

const [error, data] = await someAction({ name: 'John' })

if (error) {
  if (error.defined) {
    console.log(error.data) // Typed error data
  }
} else {
  console.log(data)
}
```

## `@orpc/react` Package

### Installation

```sh
npm install @orpc/react@latest
```

### `useServerAction` Hook

```tsx
'use client'

import { useServerAction } from '@orpc/react/hooks'
import { isDefinedError, onError } from '@orpc/client'

export function MyComponent() {
  const { execute, data, error, status } = useServerAction(someAction, {
    interceptors: [
      onError((error) => {
        if (isDefinedError(error)) {
          console.error(error.data)
        }
      }),
    ],
  })

  const action = async (form: FormData) => {
    const name = form.get('name') as string
    execute({ name })
  }

  return (
    <form action={action}>
      <input type="text" name="name" required />
      <button type="submit">Submit</button>
      {status === 'pending' && <p>Loading...</p>}
    </form>
  )
}
```

### `useOptimisticServerAction` Hook

```tsx
import { useOptimisticServerAction } from '@orpc/react/hooks'
import { onSuccessDeferred } from '@orpc/react'

export function MyComponent() {
  const [todos, setTodos] = useState<Todo[]>([])

  const { execute, optimisticState } = useOptimisticServerAction(someAction, {
    optimisticPassthrough: todos,
    optimisticReducer: (currentState, newTodo) => [...currentState, newTodo],
    interceptors: [
      onSuccessDeferred(({ data }) => {
        setTodos(prevTodos => [...prevTodos, data])
      }),
    ],
  })

  const handleSubmit = (form: FormData) => {
    const todo = form.get('todo') as string
    execute({ todo })
  }

  return (
    <div>
      <ul>
        {optimisticState.map(todo => <li key={todo.todo}>{todo.todo}</li>)}
      </ul>
      <form action={handleSubmit}>
        <input type="text" name="todo" required />
        <button type="submit">Add Todo</button>
      </form>
    </div>
  )
}
```

### `createFormAction` Utility

```tsx
import { createFormAction } from '@orpc/react'

const dosomething = os
  .input(z.object({
    user: z.object({
      name: z.string(),
      age: z.coerce.number(),
    }),
  }))
  .handler(({ input }) => {
    console.log('Form action called!', input)
  })

export const redirectSomeWhereForm = createFormAction(dosomething, {
  interceptors: [
    onSuccess(async () => {
      redirect('/some-where')
    }),
  ],
})

export function MyComponent() {
  return (
    <form action={redirectSomeWhereForm}>
      <input type="text" name="user[name]" required />
      <input type="number" name="user[age]" required />
      <button type="submit">Submit</button>
    </form>
  )
}
```

> `ORPCError` with status `401`/`403`/`404` is automatically converted to Next.js errors.

### Form Data Utilities

```tsx
import { getIssueMessage, parseFormData } from '@orpc/react'

export function MyComponent() {
  const { execute, data, error, status } = useServerAction(someAction)

  return (
    <form action={(form) => { execute(parseFormData(form)) }}>
      <label>
        Name:
        <input name="user[name]" type="text" />
        <span>{getIssueMessage(error, 'user[name]')}</span>
      </label>

      <button disabled={status === 'pending'}>Submit</button>
    </form>
  )
}
```
