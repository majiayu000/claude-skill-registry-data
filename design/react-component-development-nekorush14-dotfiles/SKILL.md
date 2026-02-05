---
name: react-component-development
description: Design and implement React components with hooks, composition patterns, and performance optimization. Use when creating React components, implementing custom hooks, or optimizing component performance.
---

# React Component Development Specialist

Specialized in creating reusable, performant React components using modern patterns and hooks.

## When to Use This Skill

- Creating functional React components
- Implementing built-in hooks (useState, useEffect, useContext, etc.)
- Designing custom hooks
- Optimizing component performance
- Implementing component composition patterns
- Building compound components
- Managing component props and types

## Core Principles

- **Functional Components**: Use function components over class components
- **Hooks for Logic**: Use hooks to encapsulate and reuse stateful logic
- **Composition Over Inheritance**: Compose components to build complex UIs
- **Single Responsibility**: Each component has one clear purpose
- **Props Typing**: Always type props with TypeScript
- **Performance Awareness**: Use memo, useMemo, and useCallback judiciously

## Implementation Guidelines

### Basic Component Structure

```typescript
import { FC } from 'react'

interface UserCardProps {
  id: string
  name: string
  email: string
  onDelete?: (id: string) => void
}

// WHY: FC type provides children prop automatically if needed
export const UserCard: FC<UserCardProps> = ({ id, name, email, onDelete }) => {
  return (
    <div className="user-card">
      <h3>{name}</h3>
      <p>{email}</p>
      {onDelete && (
        <button onClick={() => onDelete(id)}>Delete</button>
      )}
    </div>
  )
}

// Alternative: explicit return type
export function UserCard({ id, name, email, onDelete }: UserCardProps): JSX.Element {
  return (
    <div className="user-card">
      <h3>{name}</h3>
      <p>{email}</p>
      {onDelete && (
        <button onClick={() => onDelete(id)}>Delete</button>
      )}
    </div>
  )
}
```

### Props Patterns

```typescript
// Optional props
interface ButtonProps {
  label: string
  onClick: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary' | 'danger'
}

// Props with children
interface CardProps {
  title: string
  children: React.ReactNode
}

// Props extending HTML attributes
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string
  error?: string
}

export const Input: FC<InputProps> = ({ label, error, ...inputProps }) => {
  return (
    <div>
      <label>{label}</label>
      <input {...inputProps} />
      {error && <span className="error">{error}</span>}
    </div>
  )
}

// Discriminated union for props
type AlertProps =
  | { variant: 'success'; message: string }
  | { variant: 'error'; message: string; onRetry: () => void }
  | { variant: 'warning'; message: string; dismissible: boolean }

export const Alert: FC<AlertProps> = (props) => {
  // WHY: TypeScript narrows type based on variant
  switch (props.variant) {
    case 'success':
      return <div className="alert-success">{props.message}</div>
    case 'error':
      return (
        <div className="alert-error">
          {props.message}
          <button onClick={props.onRetry}>Retry</button>
        </div>
      )
    case 'warning':
      return (
        <div className="alert-warning">
          {props.message}
          {props.dismissible && <button>Dismiss</button>}
        </div>
      )
  }
}
```

### useState Hook

```typescript
import { useState } from 'react'

export const Counter: FC = () => {
  // Basic state
  const [count, setCount] = useState(0)

  // State with type inference
  const [user, setUser] = useState<User | null>(null)

  // State with function initializer (lazy initialization)
  const [items, setItems] = useState(() => {
    // WHY: Expensive computation runs only once
    return loadItemsFromLocalStorage()
  })

  // Functional updates
  const increment = () => {
    // WHY: Use functional update when new state depends on previous state
    setCount(prevCount => prevCount + 1)
  }

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
    </div>
  )
}
```

### useEffect Hook

```typescript
import { useEffect, useState } from 'react'

export const UserProfile: FC<{ userId: string }> = ({ userId }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  // Effect with cleanup
  useEffect(() => {
    let isMounted = true

    const fetchUser = async () => {
      setLoading(true)
      try {
        const data = await api.getUser(userId)
        // WHY: Check if component is still mounted before updating state
        if (isMounted) {
          setUser(data)
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    fetchUser()

    // Cleanup function
    return () => {
      isMounted = false
    }
  }, [userId]) // Dependency array

  if (loading) return <div>Loading...</div>
  if (!user) return <div>User not found</div>

  return <div>{user.name}</div>
}

// Effect for event listeners
export const WindowSize: FC = () => {
  const [size, setSize] = useState({ width: 0, height: 0 })

  useEffect(() => {
    const handleResize = () => {
      setSize({
        width: window.innerWidth,
        height: window.innerHeight,
      })
    }

    window.addEventListener('resize', handleResize)
    handleResize() // Initial size

    // WHY: Remove event listener on unmount to prevent memory leaks
    return () => {
      window.removeEventListener('resize', handleResize)
    }
  }, []) // Empty array - run once on mount
}
```

### useContext Hook

```typescript
import { createContext, useContext, FC, ReactNode } from 'react'

interface ThemeContextValue {
  theme: 'light' | 'dark'
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined)

export const ThemeProvider: FC<{ children: ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light')

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

// Custom hook for consuming context
export const useTheme = (): ThemeContextValue => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}

// Usage in component
export const ThemedButton: FC = () => {
  const { theme, toggleTheme } = useTheme()

  return (
    <button
      onClick={toggleTheme}
      className={theme === 'light' ? 'btn-light' : 'btn-dark'}
    >
      Toggle Theme
    </button>
  )
}
```

### useReducer Hook

```typescript
import { useReducer } from 'react'

type State = {
  count: number
  step: number
}

type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'setStep'; payload: number }
  | { type: 'reset' }

// WHY: Reducer pattern for complex state logic
function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + state.step }
    case 'decrement':
      return { ...state, count: state.count - state.step }
    case 'setStep':
      return { ...state, step: action.payload }
    case 'reset':
      return { count: 0, step: 1 }
    default:
      return state
  }
}

export const Counter: FC = () => {
  const [state, dispatch] = useReducer(reducer, { count: 0, step: 1 })

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
      <input
        type="number"
        value={state.step}
        onChange={(e) => dispatch({ type: 'setStep', payload: Number(e.target.value) })}
      />
    </div>
  )
}
```

### useRef Hook

```typescript
import { useRef, useEffect } from 'react'

// Ref for DOM access
export const FocusInput: FC = () => {
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    // WHY: Focus input on mount
    inputRef.current?.focus()
  }, [])

  return <input ref={inputRef} />
}

// Ref for mutable value (doesn't trigger re-render)
export const Timer: FC = () => {
  const [count, setCount] = useState(0)
  const intervalRef = useRef<number | null>(null)

  const start = () => {
    if (intervalRef.current) return

    // WHY: Store interval ID in ref to access in cleanup
    intervalRef.current = window.setInterval(() => {
      setCount(c => c + 1)
    }, 1000)
  }

  const stop = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }
  }

  useEffect(() => {
    return () => stop() // Cleanup on unmount
  }, [])

  return (
    <div>
      <p>{count}</p>
      <button onClick={start}>Start</button>
      <button onClick={stop}>Stop</button>
    </div>
  )
}
```

### Custom Hooks

```typescript
// Custom hook for fetching data
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let isMounted = true

    const fetchData = async () => {
      try {
        setLoading(true)
        const response = await fetch(url)
        const json = await response.json()
        if (isMounted) {
          setData(json)
          setError(null)
        }
      } catch (err) {
        if (isMounted) {
          setError(err instanceof Error ? err.message : 'Unknown error')
        }
      } finally {
        if (isMounted) {
          setLoading(false)
        }
      }
    }

    fetchData()

    return () => {
      isMounted = false
    }
  }, [url])

  return { data, loading, error }
}

// Usage
export const UserList: FC = () => {
  const { data: users, loading, error } = useFetch<User[]>('/api/users')

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <ul>
      {users?.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}

// Custom hook for local storage
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch {
      return initialValue
    }
  })

  // WHY: Sync with localStorage when value changes
  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.error('Error saving to localStorage:', error)
    }
  }, [key, value])

  return [value, setValue] as const
}
```

### Performance Optimization

```typescript
import { memo, useMemo, useCallback } from 'react'

// memo - prevent unnecessary re-renders
interface ItemProps {
  id: string
  name: string
  onClick: (id: string) => void
}

// WHY: Component re-renders only when props change
export const Item = memo<ItemProps>(({ id, name, onClick }) => {
  return (
    <div onClick={() => onClick(id)}>
      {name}
    </div>
  )
})

// useMemo - memoize expensive computations
export const ExpensiveList: FC<{ items: Item[] }> = ({ items }) => {
  // WHY: Recalculate only when items change
  const sortedItems = useMemo(() => {
    return [...items].sort((a, b) => a.name.localeCompare(b.name))
  }, [items])

  return (
    <ul>
      {sortedItems.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  )
}

// useCallback - memoize function references
export const TodoList: FC = () => {
  const [todos, setTodos] = useState<Todo[]>([])

  // WHY: Prevent creating new function on every render
  const handleToggle = useCallback((id: string) => {
    setTodos(prev =>
      prev.map(todo =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    )
  }, []) // No dependencies - function never changes

  return (
    <ul>
      {todos.map(todo => (
        <Item key={todo.id} {...todo} onClick={handleToggle} />
      ))}
    </ul>
  )
}
```

### Component Composition

```typescript
// Composition with children
interface CardProps {
  children: React.ReactNode
}

export const Card: FC<CardProps> = ({ children }) => {
  return <div className="card">{children}</div>
}

export const CardHeader: FC<CardProps> = ({ children }) => {
  return <div className="card-header">{children}</div>
}

export const CardBody: FC<CardProps> = ({ children }) => {
  return <div className="card-body">{children}</div>
}

// Usage
export const UserCard: FC = () => {
  return (
    <Card>
      <CardHeader>User Profile</CardHeader>
      <CardBody>
        <p>Name: John Doe</p>
        <p>Email: john@example.com</p>
      </CardBody>
    </Card>
  )
}

// Compound Component pattern
interface TabsContextValue {
  activeTab: string
  setActiveTab: (tab: string) => void
}

const TabsContext = createContext<TabsContextValue | undefined>(undefined)

export const Tabs: FC<{ children: ReactNode; defaultTab: string }> = ({
  children,
  defaultTab,
}) => {
  const [activeTab, setActiveTab] = useState(defaultTab)

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  )
}

export const TabList: FC<{ children: ReactNode }> = ({ children }) => {
  return <div className="tab-list">{children}</div>
}

export const Tab: FC<{ value: string; children: ReactNode }> = ({ value, children }) => {
  const context = useContext(TabsContext)
  if (!context) throw new Error('Tab must be used within Tabs')

  const { activeTab, setActiveTab } = context
  const isActive = activeTab === value

  return (
    <button
      className={isActive ? 'tab-active' : 'tab'}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  )
}

export const TabPanel: FC<{ value: string; children: ReactNode }> = ({ value, children }) => {
  const context = useContext(TabsContext)
  if (!context) throw new Error('TabPanel must be used within Tabs')

  const { activeTab } = context
  if (activeTab !== value) return null

  return <div className="tab-panel">{children}</div>
}

// Usage
export const Dashboard: FC = () => {
  return (
    <Tabs defaultTab="overview">
      <TabList>
        <Tab value="overview">Overview</Tab>
        <Tab value="analytics">Analytics</Tab>
        <Tab value="settings">Settings</Tab>
      </TabList>
      <TabPanel value="overview">Overview content</TabPanel>
      <TabPanel value="analytics">Analytics content</TabPanel>
      <TabPanel value="settings">Settings content</TabPanel>
    </Tabs>
  )
}
```

## Tools to Use

- `Read`: Read existing React components
- `Write`: Create new component files
- `Edit`: Modify existing components
- `Bash`: Run tests, type checker, and linters

### Bash Commands

```bash
# Type checking
tsc --noEmit

# Run tests
vitest
vitest --ui

# Linting
eslint src/ --ext .tsx

# Formatting
prettier --write "src/**/*.tsx"
```

## Workflow

1. **Understand Requirements**: Clarify component requirements and API
2. **Write Tests First**: Use `vitest-react-testing` skill
3. **Verify Tests Fail**: Confirm tests fail correctly (Red)
4. **Define Props**: Start with TypeScript interface for props
5. **Implement Component**: Build component with hooks
6. **Run Tests**: Ensure tests pass (Green)
7. **Run Type Checker**: Ensure no type errors
8. **Optimize**: Add memo, useMemo, useCallback if needed
9. **Refactor**: Improve code quality
10. **Commit**: Create atomic commit

## Related Skills

- `typescript-core-development`: For type definitions
- `react-state-management`: For complex state logic
- `vitest-react-testing`: For component testing
- `storybook-development`: For component documentation

## Coding Standards

See [React Coding Standards](../_shared/react-coding-standards.md)

## TDD Workflow

Follow [Frontend TDD Workflow](../_shared/frontend-tdd-workflow.md)

## Key Reminders

- Always use functional components with hooks
- Type all props with TypeScript interfaces
- Use built-in hooks before creating custom ones
- Extract reusable logic into custom hooks
- Use memo, useMemo, useCallback for performance (but don't over-optimize)
- Prefer composition over complex component hierarchies
- Clean up effects with return function
- Use functional setState updates when depending on previous state
- Keep components focused on single responsibility
- Write tests before implementation (TDD)
- Run type checker to catch errors early
- Write comments explaining WHY, not WHAT
