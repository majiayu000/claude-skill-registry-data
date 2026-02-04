---
name: react-patterns
description: Modern React 19+ patterns with TypeScript
---

# React Patterns

**Purpose**: Modern React 19+ with TypeScript (type safety, error handling, component best practices)

- Keywords: component, react, hook, jsx, tsx, useState, useEffect, useCallback, useMemo, ReactNode, form, FormEvent, input, validation, props, children, ref, render, conditional

## Quick Reference

| Pattern | ✅ Modern (React 19+) | ❌ Avoid |
|---------|----------------------|----------|
| Components | Named exports | Default exports |
| Props | `readonly` always | Mutable props |
| Types | No `React.FC` | `React.FC<Props>` |
| Props | Explicit typing | `defaultProps` |
| State | Discriminated unions | Bag of optionals |
| Error handling | Result types | Unchecked try/catch |

## Component Structure

```tsx
import type { ReactNode } from "react"

interface ButtonProps {
  readonly variant: "primary" | "secondary"
  readonly onClick: () => void
  readonly disabled?: boolean          // Safe defaults only
  readonly userId: string | undefined  // Critical: explicit
  readonly children?: ReactNode
}

export function Button({ variant, onClick, disabled, children }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={variant === "primary" ? "btn-primary" : "btn-secondary"}
    >
      {children}
    </button>
  )
}
```

**Key**:
- Named export (not default)
- No `React.FC` (outdated in React 19)
- Props interface with `readonly`
- Explicit `undefined` for critical fields
- Optional `?` only for safe defaults

## State with Discriminated Unions

```tsx
import { useState, useEffect } from "react"

type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error }

export function UserProfile({ userId }: { readonly userId: string }) {
  const [state, setState] = useState<AsyncState<User>>({ status: "idle" })

  useEffect(() => {
    setState({ status: "loading" })
    fetchUser(userId).then(
      data => setState({ status: "success", data }),
      error => setState({ status: "error", error })
    )
  }, [userId])

  switch (state.status) {
    case "idle": return null
    case "loading": return <Spinner />
    case "success": return <UserCard user={state.data} />
    case "error": return <ErrorMessage error={state.error} />
  }
}
```

## Event Handlers

```tsx
export function OrderForm() {
  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    // ...
  }

  const handleAmountChange = (value: string) => { /* ... */ }

  return <form onSubmit={handleSubmit}>...</form>
}
```

**Convention**: `handle*` prefix

## Props Readonly Always

```tsx
interface OrderFormProps {
  readonly initialAmount: string
  readonly onSubmit: (order: Order) => void
  readonly onCancel?: () => void
}

export function OrderForm({ initialAmount, onSubmit }: OrderFormProps) {
  return <form>...</form>
}
```

## Result Types

```tsx
type Result<T, E extends Error> =
  | { ok: true; value: T }
  | { ok: false; error: E }

const parseJson = (input: string): Result<unknown, Error> => {
  try {
    return { ok: true, value: JSON.parse(input) }
  } catch (e) {
    return { ok: false, error: e as Error }
  }
}

// Usage
const result = parseJson(userInput)
if (!result.ok) return <Error message={result.error.message} />
// TypeScript knows result.value is safe
```

**When to throw vs Result**:
- ✅ Throw: Framework handlers, validation, critical failures
- ✅ Result: Parsing (JSON/dates), file ops, network

## Check Latest Docs First

**Identify framework**:
- `next.config.js` = Next.js
- `routeTree.gen.ts` = TanStack Start
- `convex/` = Convex

**Consult**:
- [React 19](https://react.dev/blog/2024/12/05/react-19)
- [React 19.2](https://react.dev/blog/2025/10/01/react-19-2)
- [TypeScript 5.9+](https://typescriptlang.org/docs/handbook/release-notes/typescript-5-9.html)
- Framework docs (Next.js 16, TanStack Start v1, Convex)

## JSDoc When Helpful

```tsx
/**
 * Formats bitcoin amount with proper decimals
 * @link {parseBitcoinAmount} for parsing
 */
export function formatBitcoinAmount(sats: number): string {
  return (sats / 100_000_000).toFixed(8)
}
```

**Guidelines**: Only when behavior isn't self-evident, use `@link` for internal refs

## Avoid Outdated Patterns

```tsx
// ❌ React.FC (discouraged React 19)
const Button: React.FC<Props> = ({ children }) => { }

// ❌ defaultProps (deprecated React 19)
Button.defaultProps = { variant: "primary" }

// ✅ ES6 defaults
export function Button({ variant = "primary" }: Props) { }

// ❌ Default exports (except framework requirements)
export default function MyComponent() { }

// ❌ Mutable props
interface Props { count: number }  // Should be readonly
```

## Resources

- `resources/react-19-2-features.md` - useEffectEvent, Activity, cacheSignal
- `resources/hooks-best-practices.md` - useEffect, useCallback, useMemo
- `resources/error-boundaries.md` - Error boundary patterns
- `resources/performance.md` - React.memo, useMemo, useCallback
