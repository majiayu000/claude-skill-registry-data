---
name: frontend-patterns
description: React/Next.js structural patterns — component composition, custom hooks, state layering, data fetching, memoization, virtualization, forms, and error boundaries — as practised in the devskyy dashboard at frontend/. Use when building or reviewing a component, hook, API route, or state container under frontend/ (Next.js 16 + React 19). Do NOT use for the WordPress theme (no React — that is skyyrose-wp-platform / css-cascade-discipline), and do NOT use for animation specifics (motion-ui) or accessibility semantics (frontend-a11y).
origin: ECC
---

# Frontend Development Patterns

Modern frontend patterns for React, Next.js, and performant user interfaces.

## When to use

**Observable events:**

- You are adding or editing a component, hook, or context under `frontend/app/`, `frontend/components/`, or `frontend/lib/`.
- You are adding an API route under `frontend/app/api/**/route.ts` — the auth-coverage gate will reject it unwrapped (see Verification check 3).
- A dashboard list renders hundreds of rows and scrolling stutters (virtualization).
- A component re-renders on every parent update (memoization).
- You are choosing where a piece of state lives — server cache, persistent store, or session.

**When NOT to use:**

- **`wordpress-theme/skyyrose-flagship/`** — PHP templates and vanilla JS. There is no React, no hooks, no bundler-scoped CSS. Use `skyyrose-wp-platform` for the theme and `css-cascade-discipline` for its styles.
- **Animation behaviour** — `AnimatePresence`, tokens, reduced motion: `motion-ui`.
- **Accessibility semantics** — labels, ARIA, focus order: `frontend-a11y`.
- **Trivial single-line edits** where the pattern is already established in the file. Match the file, do not restructure it.

## Inputs

| Required before starting | How to confirm | If absent |
|---|---|---|
| `frontend/node_modules` installed | `ls -d frontend/node_modules` | **STOP.** Run `npm install` — **npm, never pnpm** (`ERR_INVALID_THIS` on Node 22+ breaks Vercel deploys). No checks below can run without it. |
| Which state layer owns this data | read `frontend/CLAUDE.md` → "State management — three layers" | **STOP.** Guessing produces a fourth parallel store. Server/API data → TanStack Query; persistent cart → Zustand `persist`; admin auth → NextAuth `useSession()`. `jotai` is installed but unused — do not introduce atoms without confirming the domain is not already one of the three. |
| Whether the module is server-only | grep the file for `node:fs`, `server-only`, `next-auth` | **STOP.** `lib/catalog.ts` uses `node:fs` (`catalog.ts:13`); importing it from a `'use client'` component **crashes the build**. Client code must call `/api/catalog`. |
| For a new API route: its auth decision | read `frontend/lib/api-auth.ts` and `lib/api-public-routes.ts` | **STOP.** Do not add to `PUBLIC_API_ROUTES` without writing the reason beside it. Per-handler auth is fail-OPEN by nature; the coverage test is what restores fail-closed. |
| For new tests: the runner's `include` list | read `frontend/vitest.config.ts` | **STOP.** The config uses an explicit `include` (`lib/wp/**`, `tests/**`), not a glob, because most of the dashboard cannot be imported under vitest. A suite written outside those paths is silently **skipped** — and a skipped security test is indistinguishable from a passing one. |

## Procedure

1. **Read the target file and its neighbours first.** Match the existing pattern; do not introduce a second way of doing what the file already does.
2. **Place the state in the right layer** (table above). Server data does not belong in `useState`.
3. **Import through the barrel** — always `@/lib/api`, never `@/lib/api/endpoints/*` directly. To add an endpoint: file in `lib/api/endpoints/`, Zod schema in `lib/api/schemas.ts`, register in `lib/api/index.ts`.
4. **Keep the server/client boundary intact.** Anything touching `node:fs`, `next-auth`, or `next/server` stays server-side; client components call the REST route instead.
5. **Wrap every new API handler**: `export const GET = withAuth(getHandler);`. Unauthenticated must return **401 JSON, never a redirect** — a 302 to `/login` is followed transparently and hands the caller an HTML page with status 200, which parses as success.
6. **Reach for memoization only against a measured re-render**, not preemptively. `useMemo`/`useCallback` on cheap values costs more than it saves.
7. **Virtualize lists past a few hundred rows** (`@tanstack/react-virtual`), rather than paginating a UI that should scroll.
8. **Validate at the boundary with Zod**, and derive the TypeScript type from the schema rather than declaring it twice.
9. **Run the Verification checks below** and paste real output.

## Component Patterns

### Composition Over Inheritance

```typescript
// ✅ GOOD: Component composition
interface CardProps {
  children: React.ReactNode
  variant?: 'default' | 'outlined'
}

export function Card({ children, variant = 'default' }: CardProps) {
  return <div className={`card card-${variant}`}>{children}</div>
}

export function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="card-header">{children}</div>
}

export function CardBody({ children }: { children: React.ReactNode }) {
  return <div className="card-body">{children}</div>
}

// Usage
<Card>
  <CardHeader>Title</CardHeader>
  <CardBody>Content</CardBody>
</Card>
```

### Compound Components

```typescript
interface TabsContextValue {
  activeTab: string
  setActiveTab: (tab: string) => void
}

const TabsContext = createContext<TabsContextValue | undefined>(undefined)

export function Tabs({ children, defaultTab }: {
  children: React.ReactNode
  defaultTab: string
}) {
  const [activeTab, setActiveTab] = useState(defaultTab)

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  )
}

export function TabList({ children }: { children: React.ReactNode }) {
  return <div className="tab-list">{children}</div>
}

export function Tab({ id, children }: { id: string, children: React.ReactNode }) {
  const context = useContext(TabsContext)
  if (!context) throw new Error('Tab must be used within Tabs')

  return (
    <button
      className={context.activeTab === id ? 'active' : ''}
      onClick={() => context.setActiveTab(id)}
    >
      {children}
    </button>
  )
}

// Usage
<Tabs defaultTab="overview">
  <TabList>
    <Tab id="overview">Overview</Tab>
    <Tab id="details">Details</Tab>
  </TabList>
</Tabs>
```

### Render Props Pattern

```typescript
interface DataLoaderProps<T> {
  url: string
  children: (data: T | null, loading: boolean, error: Error | null) => React.ReactNode
}

export function DataLoader<T>({ url, children }: DataLoaderProps<T>) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false))
  }, [url])

  return <>{children(data, loading, error)}</>
}

// Usage
<DataLoader<Market[]> url="/api/markets">
  {(markets, loading, error) => {
    if (loading) return <Spinner />
    if (error) return <Error error={error} />
    return <MarketList markets={markets!} />
  }}
</DataLoader>
```

## Custom Hooks Patterns

### State Management Hook

```typescript
export function useToggle(initialValue = false): [boolean, () => void] {
  const [value, setValue] = useState(initialValue)

  const toggle = useCallback(() => {
    setValue(v => !v)
  }, [])

  return [value, toggle]
}

// Usage
const [isOpen, toggleOpen] = useToggle()
```

### Async Data Fetching Hook

```typescript
interface UseQueryOptions<T> {
  onSuccess?: (data: T) => void
  onError?: (error: Error) => void
  enabled?: boolean
}

export function useQuery<T>(
  key: string,
  fetcher: () => Promise<T>,
  options?: UseQueryOptions<T>
) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [loading, setLoading] = useState(false)

  const refetch = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const result = await fetcher()
      setData(result)
      options?.onSuccess?.(result)
    } catch (err) {
      const error = err as Error
      setError(error)
      options?.onError?.(error)
    } finally {
      setLoading(false)
    }
  }, [fetcher, options])

  useEffect(() => {
    if (options?.enabled !== false) {
      refetch()
    }
  }, [key, refetch, options?.enabled])

  return { data, error, loading, refetch }
}

// Usage
const { data: markets, loading, error, refetch } = useQuery(
  'markets',
  () => fetch('/api/markets').then(r => r.json()),
  {
    onSuccess: data => console.log('Fetched', data.length, 'markets'),
    onError: err => console.error('Failed:', err)
  }
)
```

### Debounce Hook

```typescript
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(handler)
  }, [value, delay])

  return debouncedValue
}

// Usage
const [searchQuery, setSearchQuery] = useState('')
const debouncedQuery = useDebounce(searchQuery, 500)

useEffect(() => {
  if (debouncedQuery) {
    performSearch(debouncedQuery)
  }
}, [debouncedQuery])
```

## State Management Patterns

### Context + Reducer Pattern

```typescript
interface State {
  markets: Market[]
  selectedMarket: Market | null
  loading: boolean
}

type Action =
  | { type: 'SET_MARKETS'; payload: Market[] }
  | { type: 'SELECT_MARKET'; payload: Market }
  | { type: 'SET_LOADING'; payload: boolean }

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'SET_MARKETS':
      return { ...state, markets: action.payload }
    case 'SELECT_MARKET':
      return { ...state, selectedMarket: action.payload }
    case 'SET_LOADING':
      return { ...state, loading: action.payload }
    default:
      return state
  }
}

const MarketContext = createContext<{
  state: State
  dispatch: Dispatch<Action>
} | undefined>(undefined)

export function MarketProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(reducer, {
    markets: [],
    selectedMarket: null,
    loading: false
  })

  return (
    <MarketContext.Provider value={{ state, dispatch }}>
      {children}
    </MarketContext.Provider>
  )
}

export function useMarkets() {
  const context = useContext(MarketContext)
  if (!context) throw new Error('useMarkets must be used within MarketProvider')
  return context
}
```

## Performance Optimization

### Memoization

```typescript
// ✅ useMemo for expensive computations
const sortedMarkets = useMemo(() => {
  return markets.sort((a, b) => b.volume - a.volume)
}, [markets])

// ✅ useCallback for functions passed to children
const handleSearch = useCallback((query: string) => {
  setSearchQuery(query)
}, [])

// ✅ React.memo for pure components
export const MarketCard = React.memo<MarketCardProps>(({ market }) => {
  return (
    <div className="market-card">
      <h3>{market.name}</h3>
      <p>{market.description}</p>
    </div>
  )
})
```

### Code Splitting & Lazy Loading

```typescript
import { lazy, Suspense } from 'react'

// ✅ Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'))
const ThreeJsBackground = lazy(() => import('./ThreeJsBackground'))

export function Dashboard() {
  return (
    <div>
      <Suspense fallback={<ChartSkeleton />}>
        <HeavyChart data={data} />
      </Suspense>

      <Suspense fallback={null}>
        <ThreeJsBackground />
      </Suspense>
    </div>
  )
}
```

### Virtualization for Long Lists

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'

export function VirtualMarketList({ markets }: { markets: Market[] }) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: markets.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 100,  // Estimated row height
    overscan: 5  // Extra items to render
  })

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          position: 'relative'
        }}
      >
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`
            }}
          >
            <MarketCard market={markets[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  )
}
```

## Form Handling Patterns

### Controlled Form with Validation

```typescript
interface FormData {
  name: string
  description: string
  endDate: string
}

interface FormErrors {
  name?: string
  description?: string
  endDate?: string
}

export function CreateMarketForm() {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    description: '',
    endDate: ''
  })

  const [errors, setErrors] = useState<FormErrors>({})

  const validate = (): boolean => {
    const newErrors: FormErrors = {}

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required'
    } else if (formData.name.length > 200) {
      newErrors.name = 'Name must be under 200 characters'
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required'
    }

    if (!formData.endDate) {
      newErrors.endDate = 'End date is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!validate()) return

    try {
      await createMarket(formData)
      // Success handling
    } catch (error) {
      // Error handling
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={formData.name}
        onChange={e => setFormData(prev => ({ ...prev, name: e.target.value }))}
        placeholder="Market name"
      />
      {errors.name && <span className="error">{errors.name}</span>}

      {/* Other fields */}

      <button type="submit">Create Market</button>
    </form>
  )
}
```

## Error Boundary Pattern

```typescript
interface ErrorBoundaryState {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  ErrorBoundaryState
> {
  state: ErrorBoundaryState = {
    hasError: false,
    error: null
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error boundary caught:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      )
    }

    return this.props.children
  }
}

// Usage
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

## Animation Patterns

### Framer Motion Animations

```typescript
import { motion, AnimatePresence } from 'framer-motion'

// ✅ List animations
export function AnimatedMarketList({ markets }: { markets: Market[] }) {
  return (
    <AnimatePresence>
      {markets.map(market => (
        <motion.div
          key={market.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.3 }}
        >
          <MarketCard market={market} />
        </motion.div>
      ))}
    </AnimatePresence>
  )
}

// ✅ Modal animations
export function Modal({ isOpen, onClose, children }: ModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            className="modal-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
          <motion.div
            className="modal-content"
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

## Accessibility Patterns

### Keyboard Navigation

```typescript
export function Dropdown({ options, onSelect }: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [activeIndex, setActiveIndex] = useState(0)

  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault()
        setActiveIndex(i => Math.min(i + 1, options.length - 1))
        break
      case 'ArrowUp':
        e.preventDefault()
        setActiveIndex(i => Math.max(i - 1, 0))
        break
      case 'Enter':
        e.preventDefault()
        onSelect(options[activeIndex])
        setIsOpen(false)
        break
      case 'Escape':
        setIsOpen(false)
        break
    }
  }

  return (
    <div
      role="combobox"
      aria-expanded={isOpen}
      aria-haspopup="listbox"
      onKeyDown={handleKeyDown}
    >
      {/* Dropdown implementation */}
    </div>
  )
}
```

### Focus Management

```typescript
export function Modal({ isOpen, onClose, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null)
  const previousFocusRef = useRef<HTMLElement | null>(null)

  useEffect(() => {
    if (isOpen) {
      // Save currently focused element
      previousFocusRef.current = document.activeElement as HTMLElement

      // Focus modal
      modalRef.current?.focus()
    } else {
      // Restore focus when closing
      previousFocusRef.current?.focus()
    }
  }, [isOpen])

  return isOpen ? (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
      onKeyDown={e => e.key === 'Escape' && onClose()}
    >
      {children}
    </div>
  ) : null
}
```

**Remember**: Modern frontend patterns enable maintainable, performant user interfaces. Choose patterns that fit your project complexity.

---

## Verification

Run from `frontend/`. Three independent checks, each able to return "no".

1. **Types compile.** Catches the boundary violations this codebase actually hits — a server-only import pulled into a client component, a prop shape drifting from its Zod schema, a hook returning the wrong tuple.

```bash
cd frontend && npx tsc --noEmit
```
**PASS:** exits 0 and prints `TypeScript: No errors found`.
**Observed 2026-07-28: `TypeScript: No errors found`** `[repro]`.

2. **Unit suites still green.**

```bash
cd frontend && npx vitest run lib/wp/__tests__/throttle.test.ts
```
**PASS:** `PASS (3) FAIL (0)`.
**Observed 2026-07-28: `PASS (3) FAIL (0)`** `[test]`.

3. **Every API route is gated — the fail-closed gate (rule 2 in code form).** This suite walks `app/api/**/route.ts` on disk and rejects any exported handler that is neither `withAuth`-wrapped nor explicitly exempted. It is the reason a forgotten route cannot ship unprotected.

```bash
cd frontend && npx vitest run tests/api-auth-coverage.test.ts
```
**PASS:** `PASS (37) FAIL (0)` — and the count *rises* when you add a route. A new route that does not raise it was not detected.
**Observed 2026-07-28: `PASS (37) FAIL (0)`** `[test]`.

**Prove the check can fail (rule 3).** Check 3 is the one worth breaking once: add a throwaway
`app/api/__proof/route.ts` exporting a bare `export async function GET() {}`, re-run the suite, confirm
it goes **red** naming that route, then delete the file and confirm green again. A gate never observed
failing is a guess with a citation.

**A gate that dies is not a gate that passed (rule 1).** `vitest` exits non-zero for a *config* error
(bad `include`, unresolvable import) exactly as it does for a failing assertion, and it exits **zero**
when its `include` matches nothing. `No test files found` is therefore an artifact, not a pass — read
the counts, not just the exit code. (bug-230, ×6.)

**A SKIP is not a PASS (rule 2).** `vitest.config.ts` deliberately excludes `tests/e2e/**` (Playwright
owns it) and cannot import anything behind `server-only` or `next-auth`. So request-path behaviour —
does the admin page actually render, does the 401 actually return JSON — is **unverified by the above**.
Closer: `npm run test:e2e` (Playwright, `tests/e2e/`) or the `run-devskyy-dashboard` skill for a booted
smoke. Do not report a route as working on type-check evidence alone.

**Attribution (rule 4).** These three are green in the pristine tree, so any red is presumptively yours —
but confirm rather than assume when the failure looks unrelated:

```bash
mkdir -p /tmp/fe-attr && git archive HEAD frontend/lib frontend/tests | tar -x -C /tmp/fe-attr
```
Compare against that copy. **Never `git stash`** — the stack is shared across worktrees.

## Worked example

**Task (2026-07-28):** confirm the dashboard's structural gates are green before adding a hook.

```bash
$ cd frontend && npx tsc --noEmit
TypeScript: No errors found

$ npx vitest run lib/wp/__tests__/throttle.test.ts
PASS (3) FAIL (0)

$ npx vitest run tests/api-auth-coverage.test.ts
PASS (37) FAIL (0)
```

All three green `[test]`. The 37-case count is the load-bearing number: it is one assertion per
route handler discovered **on disk**, so it tracks the filesystem rather than a hand-maintained list.
That is what makes it fail closed — adding `app/api/foo/route.ts` without `withAuth` turns it red
without anyone remembering to update a test.

**Honest scope:** this proves the committed tree type-checks and its unit gates pass `[test]`. It does
**not** prove the dashboard renders, that auth works against a live session, or that anything is correct
on `devskyy.app` — those need Playwright and a deployment probe respectively. Reporting "the dashboard
is working" from this output would be the `[repo]`/`[test]` → `[live]` jump the evidence rules ban
(bug-287).

## Failure modes

| Symptom | Root cause | Fix |
|---|---|---|
| Build crashes importing catalog data into a component | `lib/catalog.ts` uses `node:fs` (`catalog.ts:13`); pulled into a `'use client'` tree | Call `/api/catalog` from the client instead |
| A `fetch` from an admin page returns HTML with status 200 | Unauthenticated API redirected 302 → `/login`, transparently followed | Handlers must return **401 JSON**; wrap with `withAuth()` |
| New API route ships unprotected | Per-handler auth is fail-open by construction | `tests/api-auth-coverage.test.ts` — never bypass it by adding to `PUBLIC_API_ROUTES` without a written reason |
| A new test suite "passes" but never ran | `vitest.config.ts` uses an explicit `include`; the file is outside it | Put suites in `lib/wp/**` or `tests/**`, keep them framework-free, and check the count rose |
| `useAuth()` returns undefined in an admin page | Two auth systems: admin is NextAuth (`useSession()`), storefront is `AuthContext` | Use `useSession()` under `/admin/*` |
| Vercel build crashes on a doubled path | `outputFileTracingRoot` / `turbopack.root` set unconditionally | Leave the `!process.env.VERCEL` guard in `next.config.ts:13` alone |
| Deploy fails with `ERR_INVALID_THIS` | pnpm on Node 22+ | Use npm |
| Direct import from `@/lib/api/endpoints/*` compiles but the page 404s the call | Barrel bypassed; endpoint never registered in `lib/api/index.ts` | Import from `@/lib/api`; register the endpoint |
| Memoization added, nothing got faster | `useMemo`/`useCallback` on cheap values | Measure first; remove speculative memoization |
| A killed `vitest` run reported as clean | Gate died — output is an artifact | Re-run; read counts not exit code (bug-230) |
