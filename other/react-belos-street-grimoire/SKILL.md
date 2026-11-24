---
name: react
description: React Hooks, TypeScript, component patterns, and modern React best practices. Use when writing React components, hooks, context, or using Suspense/ErrorBoundary/Lazy loading.
---

# React

> Based on React 19 with TypeScript. Always use functional components with Hooks.

## Preferences

- Prefer TypeScript over JavaScript
- Prefer functional components over class components
- Prefer composition over inheritance
- Use `useMemo` and `useCallback` judiciously for performance optimization
- Avoid prop drilling with Context or composition

## Core

| Topic | Description | Reference |
|-------|-------------|-----------|
| Hooks | useState, useEffect, useCallback, useMemo, useRef, useContext, useReducer, useId, useTransition, useDeferredValue, useSyncExternalStore | [hooks](references/hooks.md) |
| Component Patterns | Function components, props, children, composition, render props, forwardRef, memo | [components-patterns](references/components-patterns.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Advanced Features | Suspense, Error Boundary, Lazy loading, Context, Refs, Portals | [advanced-features](references/advanced-features.md) |

## Quick Reference

### Function Component with TypeScript

```tsx
import { useState, useEffect, useCallback, useMemo } from 'react'

interface Props {
  title: string
  count?: number
  onUpdate: (value: string) => void
}

export function MyComponent({ title, count = 0, onUpdate }: Props) {
  const [value, setValue] = useState<string>('')

  const doubled = useMemo(() => count * 2, [count])

  const handleClick = useCallback(() => {
    onUpdate(value)
  }, [onUpdate, value])

  useEffect(() => {
    console.log('Component mounted or count changed:', count)
    return () => console.log('Cleanup')
  }, [count])

  return (
    <div>
      <h1>{title} - {doubled}</h1>
      <button onClick={handleClick}>Click</button>
    </div>
  )
}
```

### Key Imports

```ts
// State & Refs
import { useState, useRef, useReducer, useId } from 'react'

// Effects & Lifecycle
import { useEffect, useLayoutEffect, useInsertionEffect } from 'react'

// Performance
import { useMemo, useCallback, useTransition, useDeferredValue } from 'react'

// Context & Refs
import { useContext, useRef, forwardRef, useImperativeHandle, useSyncExternalStore } from 'react'

// Components
import { memo, useDeferredValue, Suspense, lazy, createContext, createRef } from 'react'
```
