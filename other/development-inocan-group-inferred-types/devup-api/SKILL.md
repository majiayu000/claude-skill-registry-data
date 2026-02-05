---
name: devup-api
description: A tool for generating fully typed API clients from OpenAPI schemas. It offers a fetch-compatible API, auto-generated types without generics, and integrates with major build tools like Vite, Next.js, and Webpack.
---

# devup-api

This skill helps you invoke the `devup-api` library to generate and use fully typed API clients in your TypeScript projects. `devup-api` reads your `openapi.json` and automatically generates a type-safe client that feels like `fetch` but with strict typing for paths, parameters, bodies, and responses.

## Key Features

- **OpenAPI-driven:** Generates types directly from `openapi.json`.
- **Fetch-compatible:** Ergonomic API similar to standard `fetch`.
- **Zero Generics:** No complex generic types to manage manually.
- **Build Tool Integration:** Plugins for Vite, Next.js, Webpack, and Rsbuild.
- **React Query Integration:** First-class support for TanStack React Query with `@devup-api/react-query`.
- **Multiple API Servers:** Support for multiple OpenAPI schemas with `serverName` and `DevupObject` type access.
- **Two-phase Typing:** "Cold Typing" (relaxed types for initial setup) and "Boild Typing" (strict types after generation - named after "boiled" and inspired by "boilerplate").

## Usage Instructions

### 1. Installation

Install the core fetch package and the plugin for your build tool:

```bash
npm install @devup-api/fetch @devup-api/vite-plugin  # For Vite
# OR
npm install @devup-api/fetch @devup-api/next-plugin  # For Next.js
# See README for Webpack and Rsbuild
```

### 2. Configuration

Add the plugin to your build configuration (e.g., `vite.config.ts`, `next.config.ts`).

**Vite Example:**
```ts
import { defineConfig } from 'vite'
import devupApi from '@devup-api/vite-plugin'

export default defineConfig({
  plugins: [devupApi()],
})
```

### 3. TypeScript Setup

Include the generated types in your `tsconfig.json`:

```json
{
  "include": [
    "src",
    "df/**/*.d.ts" 
  ]
}
```
*Note: `df` is the default temporary directory.*

### 4. Create and Use Client

```ts
import { createApi } from '@devup-api/fetch'

// Initialize
const api = createApi('https://api.example.com')

// GET Request (using operationId or path)
const users = await api.get('getUsers', { query: { page: 1 } })
// OR
const user = await api.get('/users/{id}', { params: { id: '123' } })

// POST Request
const newUser = await api.post('createUser', {
  body: { name: 'Alice', email: 'alice@example.com' }
})
```

## Examples

### Complete Workflow

1.  **Project Setup:** Ensure `openapi.json` is in your project root.
2.  **Configure:** Add `devup-api/vite-plugin` to `vite.config.ts`.
3.  **Run:** Run `npm run dev` or `npm run build`. This generates `df/api.d.ts`.
4.  **Code:** Use `createApi` to make requests. IntelliSense will now show available paths and required parameters.

### Handling Responses

`devup-api` returns an object with either `data` (success) or `error` (failure).

```ts
const response = await api.get('getUser', { params: { id: '1' } })

if (response.data) {
  console.log('User Name:', response.data.name)
} else if (response.error) {
  console.error('Error:', response.error.message)
}
```

## Using DevupObject for Type References

`DevupObject` provides direct access to generated schema types:

```ts
import { createApi, type DevupObject } from '@devup-api/fetch'

// Access response types
type User = DevupObject['User']

// Access request/error types
type CreateUserRequest = DevupObject<'request'>['CreateUserBody']
type ApiError = DevupObject<'error'>['ErrorResponse']

// For multiple OpenAPI schemas, specify the server name
type Product = DevupObject<'response', 'openapi2.json'>['Product']
```

## Multiple API Servers

Support multiple OpenAPI schemas with `serverName`:

```ts
import { createApi, type DevupObject } from '@devup-api/fetch'

// Default server
const api = createApi({ baseUrl: 'https://api.example.com' })

// Second server
const api2 = createApi({
  baseUrl: 'https://api.another-service.com',
  serverName: 'openapi2.json',
})

// Types from different schemas
type User = DevupObject['User']  // openapi.json
type Product = DevupObject<'response', 'openapi2.json'>['Product']  // openapi2.json
```

## React Query Integration

For React applications using TanStack React Query, use `@devup-api/react-query`:

```bash
npm install @devup-api/react-query @tanstack/react-query
```

```ts
import { createApi } from '@devup-api/fetch'
import { createQueryClient } from '@devup-api/react-query'

const api = createApi('https://api.example.com')
const queryClient = createQueryClient(api)

// useQuery
const { data } = queryClient.useQuery('get', '/users/{id}', { params: { id: '123' } })

// useMutation
const mutation = queryClient.useMutation('post', 'createUser')

// useSuspenseQuery
const { data } = queryClient.useSuspenseQuery('get', 'getUsers', {})

// useInfiniteQuery
const { data, fetchNextPage } = queryClient.useInfiniteQuery('get', 'getUsers', {
  initialPageParam: 1,
  getNextPageParam: (lastPage) => lastPage.nextPage,
})
```

## Guidelines

-   **"Cold" vs "Boild" Typing:** When you first start, types might be `any` (Cold Typing ❄️). Run your build command (`dev` or `build`) to generate the types and enable strict checking (Boild Typing 🔥 - the warm opposite of cold, with zero boilerplate needed!).
-   **Operation IDs vs Paths:** You can use either the OpenAPI `operationId` (e.g., `getUsers`) or the URL path (e.g., `/users`). `operationId` is often more concise.
-   **Generated Files:** Do not manually edit the files in the `df` (or configured temp) directory. They are auto-generated.
-   **Verification:** If types seem missing, ensure `tsconfig.json` includes the generated folder and that the build script has run at least once.
-   **Advanced Features:** devup-api supports authentication, file uploads, request interceptors, retry logic, caching, and more through custom fetch implementations.
