---
name: devup-api
description: |
  Type-safe API client generator from OpenAPI schemas with full ecosystem support.
  
  TRIGGER WHEN:
  - Setting up API client with OpenAPI schema (@devup-api/fetch)
  - Making typed API requests (GET, POST, PUT, PATCH, DELETE)
  - Using React Query hooks (@devup-api/react-query)
  - Using Zod validation schemas (@devup-api/zod)
  - Building forms with react-hook-form (@devup-api/hookform)
  - Creating CRUD interfaces (@devup-api/ui)
  - Configuring Vite/Next.js/Webpack/Rsbuild plugins
  - Implementing authentication middleware
  - Using DevupObject for type references
---

# devup-api Usage Guide

Type-safe API client from OpenAPI. Zero generics, auto-generated types.

## Setup

### Install

```bash
# Core + Build Plugin (choose one)
npm install @devup-api/fetch @devup-api/vite-plugin      # Vite
npm install @devup-api/fetch @devup-api/next-plugin      # Next.js
npm install @devup-api/fetch @devup-api/webpack-plugin   # Webpack
npm install @devup-api/fetch @devup-api/rsbuild-plugin   # Rsbuild

# Optional Integrations
npm install @devup-api/react-query @tanstack/react-query  # React Query
npm install @devup-api/zod zod                            # Zod validation
npm install @devup-api/hookform react-hook-form zod       # Hook Form
npm install @devup-api/ui @tanstack/react-query react-hook-form zod  # CRUD UI
```

### Configure Build Tool

```ts
// vite.config.ts
import devupApi from '@devup-api/vite-plugin'
export default defineConfig({ plugins: [devupApi()] })

// next.config.ts
import devupApi from '@devup-api/next-plugin'
export default devupApi({ reactStrictMode: true })
```

### tsconfig.json

```json
{ "include": ["src", "df/**/*.d.ts"] }
```

Place `openapi.json` in project root, run `npm run dev`.

---

## @devup-api/fetch — API Client

### Create Client

```ts
import { createApi, type DevupObject } from '@devup-api/fetch'

const api = createApi('https://api.example.com')
// or with options
const api = createApi({ baseUrl: 'https://api.example.com', headers: { 'X-Custom': 'value' } })
```

### HTTP Methods

```ts
// GET
const users = await api.get('getUsers', { query: { page: 1, limit: 20 } })
const user = await api.get('/users/{id}', { params: { id: '123' } })

// POST
const created = await api.post('createUser', { body: { name: 'John', email: 'john@example.com' } })

// PUT / PATCH / DELETE
await api.put('/users/{id}', { params: { id: '1' }, body: { name: 'Jane', email: 'jane@example.com' } })
await api.patch('/users/{id}', { params: { id: '1' }, body: { name: 'Jane' } })
await api.delete('/users/{id}', { params: { id: '1' } })
```

### Response Handling

```ts
const result = await api.get('getUser', { params: { id: '1' } })

if (result.data) {
  console.log(result.data.name)    // typed response
} else if (result.error) {
  console.error(result.error)       // typed error
}
console.log(result.response.status) // raw Response
```

### DevupObject (Type References)

Use `DevupObject` directly in type annotations without redefining types:

```ts
// Direct usage in variable declarations
const user: DevupObject['User'] = await fetchUser()
const body: DevupObject<'request'>['CreateUserBody'] = { name: 'John', email: 'john@example.com' }
const error: DevupObject<'error'>['ErrorResponse'] = result.error

// Direct usage in function parameters
function displayUser(user: DevupObject['User']) { /* ... */ }

// Direct usage in component props
function UserCard({ user }: { user: DevupObject['User'] }) { /* ... */ }

// Multi-server types
const product: DevupObject<'response', 'openapi2.json'>['Product'] = data
```

### Middleware

```ts
// Auth
api.use({
  onRequest: async ({ request }) => {
    const token = localStorage.getItem('token')
    if (token) {
      const headers = new Headers(request.headers)
      headers.set('Authorization', `Bearer ${token}`)
      return new Request(request, { headers })
    }
  }
})

// Token Refresh
api.use({
  onResponse: async ({ request, response }) => {
    if (response.status === 401) {
      const newToken = await refreshToken()
      const headers = new Headers(request.headers)
      headers.set('Authorization', `Bearer ${newToken}`)
      return fetch(new Request(request, { headers }))
    }
  }
})
```

---

## @devup-api/react-query — React Query Hooks

```ts
import { createApi } from '@devup-api/fetch'
import { createQueryClient } from '@devup-api/react-query'

const api = createApi('https://api.example.com')
const queryClient = createQueryClient(api)
```

### useQuery

```tsx
const { data, isLoading, error, refetch } = queryClient.useQuery(
  'get',
  '/users/{id}',
  { params: { id: userId } },
  { staleTime: 5 * 60 * 1000 }  // React Query options
)
```

### useMutation

```tsx
const mutation = queryClient.useMutation('post', 'createUser', {
  onSuccess: (data) => {
    tanstackQueryClient.invalidateQueries({ queryKey: ['get', 'getUsers'] })
  }
})

mutation.mutate({ body: { name: 'John', email: 'john@example.com' } })
```

### useSuspenseQuery

```tsx
// Use with React Suspense
const { data } = queryClient.useSuspenseQuery('get', 'getUsers', {})
```

### useInfiniteQuery

```tsx
const { data, fetchNextPage, hasNextPage } = queryClient.useInfiniteQuery(
  'get',
  'getUsers',
  {
    initialPageParam: 1,
    getNextPageParam: (lastPage) => lastPage.nextPage
  }
)
```

### useQueries (Parallel)

```tsx
const results = queryClient.useQueries([
  ['get', '/users/{id}', { params: { id: '1' } }],
  ['get', '/users/{id}', { params: { id: '2' } }],
])
```

---

## @devup-api/zod — Runtime Validation

Schemas auto-generated from OpenAPI via virtual module.

```ts
import { schemas, responseSchemas, requestSchemas, errorSchemas, pathSchemas } from '@devup-api/zod'

// By category
const userSchema = responseSchemas.User
const createUserSchema = requestSchemas.CreateUserRequest
const errorSchema = errorSchemas.ApiError

// By path/operationId (for forms)
const schema = pathSchemas.post['createUser']
const schema = pathSchemas.put['/users/{id}']

// Multi-server
const productSchema = schemas['openapi2.json'].response.Product

// Validate
const result = userSchema.safeParse(data)
if (result.success) {
  console.log(result.data)
} else {
  console.error(result.error.issues)
}

// Type inference
import { z } from 'zod'
type User = z.infer<typeof responseSchemas.User>
```

---

## @devup-api/hookform — React Hook Form Integration

Auto-validation with Zod schemas from OpenAPI.

```tsx
import { createApi } from '@devup-api/fetch'
import { ApiForm, useFormContext, useWatch, useFieldArray, Controller } from '@devup-api/hookform'

const api = createApi('https://api.example.com')
```

### Basic Form

```tsx
function FormFields() {
  const { register, formState: { errors, isSubmitting } } = useFormContext()
  return (
    <>
      <input {...register('name')} />
      {errors.name && <span>{errors.name.message}</span>}
      <input {...register('email')} type="email" />
      {errors.email && <span>{errors.email.message}</span>}
      <button type="submit" disabled={isSubmitting}>Submit</button>
    </>
  )
}

function CreateUserForm() {
  return (
    <ApiForm
      api={api}
      method="post"
      path="createUser"
      onSuccess={(data) => console.log('Created:', data)}
      onError={(error) => console.error('Error:', error)}
      onValidationError={(errors) => console.log('Validation:', errors)}
    >
      <FormFields />
    </ApiForm>
  )
}
```

### Edit Form

```tsx
<ApiForm
  api={api}
  method="put"
  path="/users/{id}"
  requestOptions={{ params: { id: '123' } }}
  defaultValues={{ name: 'John', email: 'john@example.com' }}
  mode="onChange"
  resetOnSuccess
  onSuccess={(data) => console.log('Updated:', data)}
>
  <FormFields />
</ApiForm>
```

### Props

| Prop | Type | Description |
|------|------|-------------|
| `api` | `DevupApi` | API client |
| `method` | `'post' \| 'put' \| 'patch' \| 'delete'` | HTTP method |
| `path` | `string` | operationId or path |
| `requestOptions` | `{ params?, query?, headers? }` | Additional request options |
| `defaultValues` | `object` | Form default values |
| `mode` | `'onSubmit' \| 'onBlur' \| 'onChange'` | Validation mode |
| `resetOnSuccess` | `boolean` | Reset form after success |
| `onSuccess` | `(data) => void` | Success callback |
| `onError` | `(error) => void` | API error callback |
| `onValidationError` | `(errors) => void` | Validation error callback |

---

## @devup-api/ui — CRUD Components

Auto-generated CRUD from OpenAPI tags.

### OpenAPI Tags

```yaml
paths:
  /users/{id}:
    get:
      tags: [devup:user:one]      # GET single (required)
    put:
      tags: [devup:user:edit]     # PUT update
    patch:
      tags: [devup:user:fix]      # PATCH update
  /users:
    post:
      tags: [devup:user:create]   # POST create (required)
```

### Usage

```tsx
import { createApi } from '@devup-api/fetch'
import { ApiCrud } from '@devup-api/ui'
import { crudConfigs } from '@devup-api/ui/crud'

const api = createApi('https://api.example.com')
```

### Create Mode (no params)

```tsx
<ApiCrud
  config={crudConfigs.user}
  api={api}
  fields={[
    { name: 'name', label: 'Name', type: 'text', required: true },
    { name: 'email', label: 'Email', type: 'email', required: true },
  ]}
  onCreateSuccess={(data) => console.log('Created:', data)}
/>
```

### Edit Mode (with params)

```tsx
<ApiCrud
  config={crudConfigs.user}
  api={api}
  params={{ id: userId }}
  editMode="fix"  // 'edit' (PUT) or 'fix' (PATCH)
  fields={fields}
  oneLoading={<div>Loading...</div>}
  oneFallback={<div>Not found</div>}
  onUpdateSuccess={(data) => console.log('Updated:', data)}
/>
```

### Headless Mode (Render Function)

```tsx
<ApiCrud config={crudConfigs.user} api={api} params={{ id: userId }}>
  {({ form, mode, submit, isLoading, one }) => (
    <form onSubmit={(e) => { e.preventDefault(); submit() }}>
      <input {...form.register('name')} />
      <input {...form.register('email')} />
      <button disabled={isLoading}>
        {mode === 'create' ? 'Create' : 'Save'}
      </button>
    </form>
  )}
</ApiCrud>
```

### Custom Renderers

```tsx
<ApiCrud
  config={crudConfigs.user}
  api={api}
  fields={fields}
  renderField={(field, form) => (
    <div key={field.name}>
      <label>{field.label}</label>
      <input {...form.register(field.name)} />
    </div>
  )}
  renderSubmit={({ isLoading, mode }) => (
    <button disabled={isLoading}>{mode === 'create' ? 'Create' : 'Update'}</button>
  )}
/>
```

### useApiCrud Hook

```tsx
import { useApiCrud } from '@devup-api/ui'

const crud = useApiCrud({
  config: crudConfigs.user,
  api,
  params: userId ? { id: userId } : undefined,
  onCreateSuccess: (data) => console.log('Created:', data),
  onUpdateSuccess: (data) => console.log('Updated:', data),
})

// crud.mode: 'create' | 'edit'
// crud.form: UseFormReturn
// crud.one: { data, isLoading, isError }
// crud.create: { mutate, isPending }
// crud.update: { mutate, isPending }
// crud.submit: () => void
// crud.isLoading: boolean
```

### Field Types

`text` | `number` | `email` | `password` | `url` | `tel` | `textarea` | `select` | `checkbox` | `radio` | `date` | `datetime` | `time` | `file` | `hidden` | `array` | `object`

---

## Multiple API Servers

```ts
// Plugin config
devupApi({ openapiFiles: ['openapi.json', 'openapi2.json'] })

// Usage
const api1 = createApi({ baseUrl: 'https://api1.com' })
const api2 = createApi({ baseUrl: 'https://api2.com', serverName: 'openapi2.json' })

// Types - use directly without redefining
const user: DevupObject['User'] = data                                   // openapi.json
const product: DevupObject<'response', 'openapi2.json'>['Product'] = data // openapi2.json
```

---

## Plugin Options

```ts
interface DevupApiOptions {
  openapiFiles?: string | string[]           // default: 'openapi.json'
  tempDir?: string                           // default: 'df'
  convertCase?: 'snake' | 'camel' | 'pascal' | 'maintain'  // default: 'camel'
  requestDefaultNonNullable?: boolean        // default: false
  responseDefaultNonNullable?: boolean       // default: true
}
```

---

## Common Patterns

### Request Cancellation

```ts
const controller = new AbortController()
setTimeout(() => controller.abort(), 5000)
await api.get('getUsers', { signal: controller.signal })
```

### File Upload

```ts
const formData = new FormData()
formData.append('file', file)
await api.post('/upload', { body: formData })
```

### Environment URL

```ts
const api = createApi(import.meta.env.VITE_API_URL || 'http://localhost:3000')
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Types not appearing | Run `npm run dev`, check tsconfig includes `df/**/*.d.ts` |
| operationId not found | Use path `/users/{id}` or verify openapi.json operationId |
| Zod schemas empty | Ensure bundler plugin is configured, run dev server |
| CRUD config missing | Add `devup:{name}:one` and `devup:{name}:create` tags to OpenAPI |
