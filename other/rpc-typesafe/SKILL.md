---
name: rpc-typesafe
description: This skill activates when setting up Hono RPC client, configuring type-safe API calls, or discussing client-server type sharing. It provides patterns for the hc client, type inference, and React Query integration.
---

# Hono RPC Type Safety

Patterns for type-safe client-server communication with Hono.

## Server Setup

### Export App Type

```typescript
// src/index.ts
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()

// Define routes with validators for full type inference
const routes = app
  .get('/users', async (c) => {
    return c.json({ users: [{ id: '1', name: 'John' }] })
  })
  .post('/users',
    zValidator('json', z.object({
      email: z.string().email(),
      name: z.string()
    })),
    async (c) => {
      const data = c.req.valid('json')
      return c.json({ id: crypto.randomUUID(), ...data }, 201)
    }
  )
  .get('/users/:id', async (c) => {
    const id = c.req.param('id')
    return c.json({ id, name: 'John' })
  })

export default routes

// CRITICAL: Export type for client
export type AppType = typeof routes
```

### Route Chaining for Type Inference

```typescript
// Chain routes to preserve types
const userRoutes = new Hono()
  .get('/', async (c) => c.json({ users: [] }))
  .post('/',
    zValidator('json', createUserSchema),
    async (c) => c.json({ id: '1' }, 201)
  )

const postRoutes = new Hono()
  .get('/', async (c) => c.json({ posts: [] }))
  .post('/',
    zValidator('json', createPostSchema),
    async (c) => c.json({ id: '1' }, 201)
  )

// Compose and export
const app = new Hono()
  .route('/users', userRoutes)
  .route('/posts', postRoutes)

export type AppType = typeof app
```

## Client Setup

### Basic Client

```typescript
// client.ts
import { hc } from 'hono/client'
import type { AppType } from './server'

// Create typed client
const client = hc<AppType>('http://localhost:8787')

// Type-safe requests
const res = await client.users.$get()
const data = await res.json() // Typed!
```

### Client Factory

```typescript
// lib/api-client.ts
import { hc } from 'hono/client'
import type { AppType } from '@/server'

export function createClient(baseUrl: string, token?: string) {
  return hc<AppType>(baseUrl, {
    headers: token ? { Authorization: `Bearer ${token}` } : undefined
  })
}

// Default instance
export const api = createClient(
  process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8787'
)
```

## Request Patterns

### GET Requests

```typescript
// Simple GET
const res = await api.users.$get()
const { users } = await res.json()

// GET with query params
const res = await api.users.$get({
  query: {
    page: 1,
    limit: 20,
    search: 'john'
  }
})

// GET with path params
const res = await api.users[':id'].$get({
  param: { id: 'user-123' }
})
```

### POST Requests

```typescript
// POST with JSON body
const res = await api.users.$post({
  json: {
    email: 'user@example.com',
    name: 'New User'
  }
})

if (res.ok) {
  const user = await res.json()
  console.log(user.id) // Typed!
}
```

### PUT/PATCH Requests

```typescript
const res = await api.users[':id'].$put({
  param: { id: 'user-123' },
  json: {
    name: 'Updated Name'
  }
})
```

### DELETE Requests

```typescript
const res = await api.users[':id'].$delete({
  param: { id: 'user-123' }
})

if (res.status === 204) {
  console.log('Deleted successfully')
}
```

## Type Utilities

### InferRequestType / InferResponseType

```typescript
import { hc, InferRequestType, InferResponseType } from 'hono/client'
import type { AppType } from './server'

// Get specific endpoint type
type CreateUserRequest = InferRequestType<typeof api.users.$post>['json']
// { email: string; name: string }

type UserResponse = InferResponseType<typeof api.users[':id'].$get>
// { id: string; name: string }

// Use in functions
async function createUser(data: CreateUserRequest): Promise<UserResponse> {
  const res = await api.users.$post({ json: data })
  return res.json()
}
```

### URL Generation

```typescript
// Generate URL without making request
const url = api.users[':id'].$url({
  param: { id: 'user-123' }
})
// 'http://localhost:8787/users/user-123'

// Useful for links, prefetching, etc.
```

## Error Handling

### Response Status Checking

```typescript
async function getUser(id: string) {
  const res = await api.users[':id'].$get({ param: { id } })

  if (!res.ok) {
    if (res.status === 404) {
      throw new Error('User not found')
    }
    throw new Error(`API error: ${res.status}`)
  }

  return res.json()
}
```

### Typed Error Responses

```typescript
// Server defines error format
app.get('/users/:id', async (c) => {
  const user = await getUser(c.req.param('id'))

  if (!user) {
    return c.json({ error: 'User not found' }, 404)
  }

  return c.json(user)
})

// Client handles typed errors
const res = await api.users[':id'].$get({ param: { id } })

if (res.status === 404) {
  const { error } = await res.json()
  console.log(error) // 'User not found'
}
```

## React Query Integration

### Query Hooks

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api-client'

// List query
export function useUsers(page = 1) {
  return useQuery({
    queryKey: ['users', page],
    queryFn: async () => {
      const res = await api.users.$get({ query: { page } })
      if (!res.ok) throw new Error('Failed to fetch users')
      return res.json()
    }
  })
}

// Single item query
export function useUser(id: string) {
  return useQuery({
    queryKey: ['users', id],
    queryFn: async () => {
      const res = await api.users[':id'].$get({ param: { id } })
      if (!res.ok) throw new Error('User not found')
      return res.json()
    },
    enabled: !!id
  })
}
```

### Mutation Hooks

```typescript
export function useCreateUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: { email: string; name: string }) => {
      const res = await api.users.$post({ json: data })
      if (!res.ok) throw new Error('Failed to create user')
      return res.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    }
  })
}

export function useUpdateUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: { name: string } }) => {
      const res = await api.users[':id'].$put({ param: { id }, json: data })
      if (!res.ok) throw new Error('Failed to update user')
      return res.json()
    },
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['users', id] })
    }
  })
}
```

### Component Usage

```typescript
function UserList() {
  const { data, isLoading, error } = useUsers()
  const createUser = useCreateUser()

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div>
      {data?.users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}

      <button
        onClick={() => createUser.mutate({
          email: 'new@example.com',
          name: 'New User'
        })}
      >
        Add User
      </button>
    </div>
  )
}
```

## Configuration Requirements

### TypeScript Config

Both server and client need strict mode:

```json
{
  "compilerOptions": {
    "strict": true,
    "moduleResolution": "bundler"
  }
}
```

### Status Codes for Type Discrimination

```typescript
// Server: Explicit status codes enable type inference
app.post('/users', async (c) => {
  return c.json({ id: '1', name: 'User' }, 201) // 201 for created
})

app.get('/users/:id', async (c) => {
  const user = await getUser(id)
  if (!user) {
    return c.json({ error: 'Not found' }, 404) // 404 for not found
  }
  return c.json(user, 200) // 200 for success
})
```

## Best Practices

1. **Always export `AppType`** from server
2. **Chain routes** for proper type inference
3. **Use `zValidator`** for automatic request type inference
4. **Specify status codes** for response type discrimination
5. **Use `strict: true`** in both server and client tsconfig
6. **Create typed error handlers** for consistent error responses
7. **Wrap in React Query** for caching and state management
8. **Use `InferRequestType`/`InferResponseType`** for complex types
