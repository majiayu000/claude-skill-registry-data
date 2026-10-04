---
name: error-handling
description: Frontend error handling patterns for Next.js — error boundaries, API error display, form validation errors, and global error recovery strategies. Use when implementing error states, debugging error UI, or designing error recovery flows.
trigger: 需要实现错误处理
input: 错误处理需求
output: 错误处理代码
next: 无
dependencies: 无
---

# Frontend Error Handling (Next.js)

Systematic approach to error handling in Next.js applications.

## Error Boundary Hierarchy

Next.js provides built-in error boundaries at every route segment level:

```
app/
├── error.tsx              ← Global error boundary (wraps entire app)
├── layout.tsx
├── dashboard/
│   ├── error.tsx          ← Dashboard-specific error boundary
│   ├── page.tsx
│   └── settings/
│       ├── error.tsx      ← Settings-specific error boundary
│       └── page.tsx
```

### Root Error Boundary (`app/error.tsx`)

```tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div role="alert">
      <h1>Something went wrong</h1>
      <p>We've been notified. Please try again.</p>
      <button onClick={() => reset()}>Try again</button>
      {/* In dev: show error.message for debugging */}
      {process.env.NODE_ENV === 'development' && (
        <pre>{error.message}</pre>
      )}
    </div>
  )
}
```

### Segment Error Boundary (`app/dashboard/error.tsx`)

```tsx
'use client'

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="p-6 rounded-lg border border-red-200 bg-red-50" role="alert">
      <h2>Dashboard unavailable</h2>
      <p>{error.message || 'Failed to load dashboard data'}</p>
      <button onClick={() => reset()}>Retry</button>
    </div>
  )
}
```

## Server Action Error Handling

```tsx
'use server'

export async function createPost(formData: FormData) {
  try {
    const title = formData.get('title')
    if (!title || typeof title !== 'string') {
      return { error: 'Title is required' }
    }
    if (title.length < 3) {
      return { error: 'Title must be at least 3 characters' }
    }

    await db.post.create({ title })
    return { success: true }
  } catch (e) {
    console.error('createPost failed:', e)
    return { error: 'Failed to create post. Please try again.' }
  }
}
```

```tsx
// Client-side handling
'use client'

export function PostForm() {
  const [state, formAction, pending] = useActionState(createPost, null)

  return (
    <form action={formAction}>
      <input name="title" aria-invalid={state?.error ? true : undefined} />
      {state?.error && <p role="alert" className="text-red-500">{state.error}</p>}
      <button disabled={pending}>{pending ? 'Creating...' : 'Create'}</button>
    </form>
  )
}
```

## API / Fetch Error Handling

```tsx
// lib/fetch.ts — unified fetch wrapper
export async function apiFetch<T>(
  url: string,
  options?: RequestInit
): Promise<{ data: T | null; error: string | null }> {
  try {
    const res = await fetch(url, options)
    if (!res.ok) {
      const body = await res.json().catch(() => ({}))
      return { data: null, error: body.message || `Request failed (${res.status})` }
    }
    return { data: await res.json(), error: null }
  } catch (e) {
    return { data: null, error: 'Network error. Please check your connection.' }
  }
}
```

## Global Error Handling

### `global-error.tsx` (Root fallback)

```tsx
'use client'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <html>
      <body>
        <div role="alert">
          <h1>Critical error</h1>
          <button onClick={() => reset()}>Reload page</button>
        </div>
      </body>
    </html>
  )
}
```

## User-Facing Error Messages

| Error Type | User Message | Action |
|-----------|-------------|--------|
| Network offline | "You appear to be offline" | Retry button |
| Server error (5xx) | "Our servers are busy. Please try again." | Retry button |
| Not found (404) | "This page doesn't exist" | Go home link |
| Validation | Specific field error message | Fix input |
| Rate limited | "Too many requests. Please wait." | Countdown timer |
| Auth expired | "Your session has expired" | Login button |

## Checklist

- [ ] Every route segment has an `error.tsx` boundary
- [ ] Server Actions return structured `{ data, error }` objects (never throw on expected errors)
- [ ] API fetch calls have a wrapper with consistent error typing
- [ ] Error messages are user-friendly, not raw error objects
- [ ] Forms show inline validation with `role="alert"`
- [ ] `global-error.tsx` exists (catches root layout errors)
- [ ] Errors are logged server-side for debugging
- [ ] Retry/reset mechanisms available for recoverable errors
- [ ] No raw `error.message` exposed in production