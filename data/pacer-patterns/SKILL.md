---
name: TanStack Pacer Patterns (Beta)
description: >-
  TanStack Pacer patterns for rate limiting, debouncing, and throttling.
  Activates when implementing search inputs, API rate limiting, or
  performance optimization. NOTE: Beta library - API may change.
version: 1.0.0
---

# TanStack Pacer Patterns (Beta)

> **Beta Library**: TanStack Pacer is in beta. APIs may change between versions.

TanStack Pacer provides utilities for rate limiting, debouncing, throttling, and async queuing.

## Debounce

Delay execution until input stops for a specified time.

### Basic Debounce
```typescript
import { debounce } from '@tanstack/pacer'

const debouncedSearch = debounce((query: string) => {
  console.log('Searching:', query)
  return fetch(`/api/search?q=${query}`)
}, 300)

// Only executes after 300ms of no calls
debouncedSearch('h')
debouncedSearch('he')
debouncedSearch('hel')
debouncedSearch('hell')
debouncedSearch('hello') // Only this executes
```

### Debounce in React
```typescript
import { useDebounce } from '@tanstack/pacer-react'
import { useState } from 'react'

function SearchInput() {
  const [query, setQuery] = useState('')

  const debouncedQuery = useDebounce(query, 300)

  // Use debouncedQuery for API calls
  const { data } = useQuery({
    queryKey: ['search', debouncedQuery],
    queryFn: () => searchApi.search(debouncedQuery),
    enabled: debouncedQuery.length > 0,
  })

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />
      {data && <SearchResults results={data} />}
    </div>
  )
}
```

### Debounced Callback
```typescript
import { useDebouncedCallback } from '@tanstack/pacer-react'

function AutoSaveEditor({ postId }: { postId: string }) {
  const [content, setContent] = useState('')
  const updatePost = useUpdatePost()

  const saveContent = useDebouncedCallback(
    async (content: string) => {
      await updatePost.mutateAsync({ id: postId, content })
    },
    1000, // Save after 1s of no typing
    { maxWait: 5000 } // But at least every 5s
  )

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newContent = e.target.value
    setContent(newContent)
    saveContent(newContent)
  }

  return (
    <textarea value={content} onChange={handleChange} />
  )
}
```

## Throttle

Limit execution to at most once per interval.

### Basic Throttle
```typescript
import { throttle } from '@tanstack/pacer'

const throttledScroll = throttle((position: number) => {
  console.log('Scroll position:', position)
}, 100)

// Executes at most once every 100ms
window.addEventListener('scroll', () => {
  throttledScroll(window.scrollY)
})
```

### Throttle in React
```typescript
import { useThrottledCallback } from '@tanstack/pacer-react'
import { useEffect } from 'react'

function ScrollTracker() {
  const trackScroll = useThrottledCallback(
    (position: number) => {
      analytics.track('scroll', { position })
    },
    500
  )

  useEffect(() => {
    const handleScroll = () => trackScroll(window.scrollY)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [trackScroll])

  return null
}
```

### Throttled API Calls
```typescript
import { useThrottledCallback } from '@tanstack/pacer-react'

function LiveSearch() {
  const [results, setResults] = useState<Result[]>([])

  const search = useThrottledCallback(
    async (query: string) => {
      const data = await searchApi.search(query)
      setResults(data)
    },
    200, // At most 5 requests per second
    { leading: true, trailing: true }
  )

  return (
    <input
      onChange={(e) => search(e.target.value)}
      placeholder="Search..."
    />
  )
}
```

## Rate Limiting

Control the rate of operations.

### Rate Limiter
```typescript
import { createRateLimiter } from '@tanstack/pacer'

const apiLimiter = createRateLimiter({
  limit: 10,      // 10 requests
  interval: 1000, // per second
})

async function fetchData(id: string) {
  await apiLimiter.acquire() // Wait if rate limited
  return fetch(`/api/data/${id}`)
}

// Safe to call rapidly - will be rate limited
await Promise.all(
  ids.map(id => fetchData(id))
)
```

### Per-Key Rate Limiting
```typescript
import { createKeyedRateLimiter } from '@tanstack/pacer'

const userLimiter = createKeyedRateLimiter({
  limit: 5,
  interval: 60000, // 5 requests per minute per user
})

async function handleUserAction(userId: string, action: Action) {
  const limiter = userLimiter.get(userId)
  if (!limiter.tryAcquire()) {
    throw new Error('Rate limited. Please try again later.')
  }
  return processAction(action)
}
```

## Async Queue

Process async operations sequentially or with concurrency limits.

### Sequential Queue
```typescript
import { createAsyncQueue } from '@tanstack/pacer'

const uploadQueue = createAsyncQueue({
  concurrency: 1, // One at a time
})

async function uploadFiles(files: File[]) {
  const results = await Promise.all(
    files.map(file =>
      uploadQueue.add(() => uploadFile(file))
    )
  )
  return results
}
```

### Concurrent Queue with Limit
```typescript
import { createAsyncQueue } from '@tanstack/pacer'

const processQueue = createAsyncQueue({
  concurrency: 3, // Max 3 concurrent
})

function ProcessingStatus() {
  const { pending, active, completed } = processQueue.status

  return (
    <div>
      <span>Pending: {pending}</span>
      <span>Active: {active}</span>
      <span>Completed: {completed}</span>
    </div>
  )
}
```

### Queue with Priority
```typescript
import { createAsyncQueue } from '@tanstack/pacer'

const taskQueue = createAsyncQueue({
  concurrency: 2,
})

// Higher priority tasks run first
taskQueue.add(() => processTask('low'), { priority: 1 })
taskQueue.add(() => processTask('high'), { priority: 10 })
taskQueue.add(() => processTask('urgent'), { priority: 100 })
```

## Integration with TanStack Query

```typescript
import { useDebounce } from '@tanstack/pacer-react'
import { useQuery } from '@tanstack/react-query'

function SearchWithDebounce() {
  const [input, setInput] = useState('')
  const debouncedInput = useDebounce(input, 300)

  const { data, isLoading } = useQuery({
    queryKey: ['search', debouncedInput],
    queryFn: () => searchApi.search(debouncedInput),
    enabled: debouncedInput.length >= 2,
  })

  return (
    <div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Search (min 2 chars)..."
      />
      {isLoading && <Spinner />}
      {data && <Results items={data} />}
    </div>
  )
}
```

## Common Use Cases

| Scenario | Solution |
|----------|----------|
| Search input | Debounce 300ms |
| Auto-save | Debounce 1s with maxWait |
| Scroll tracking | Throttle 100-200ms |
| API rate limits | Rate limiter |
| File uploads | Async queue with concurrency |
| Resize handler | Throttle 100ms |

## Conventions

1. **Debounce for inputs** - Always debounce search/filter inputs
2. **Throttle for events** - Use for scroll, resize, mousemove
3. **Rate limit APIs** - Protect against abuse
4. **Queue heavy operations** - Use for file uploads, bulk operations
5. **Cleanup** - Cancel pending operations on unmount

## Anti-Patterns

```typescript
// ❌ WRONG: No debounce on search
function Search() {
  const [query, setQuery] = useState('')
  const { data } = useQuery({
    queryKey: ['search', query], // Fires on every keystroke!
    queryFn: () => search(query),
  })
}

// ✅ CORRECT: Debounced search
function Search() {
  const [query, setQuery] = useState('')
  const debouncedQuery = useDebounce(query, 300)
  const { data } = useQuery({
    queryKey: ['search', debouncedQuery],
    queryFn: () => search(debouncedQuery),
    enabled: debouncedQuery.length > 0,
  })
}

// ❌ WRONG: Creating debounce inside render
function Component() {
  const search = debounce(() => {}, 300) // New instance every render!
}

// ✅ CORRECT: Use hook
function Component() {
  const search = useDebouncedCallback(() => {}, 300)
}
```
