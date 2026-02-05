---
name: component-designing
description: Component and type design for TypeScript + React code. Use when planning new features, designing components and custom hooks, preventing primitive obsession, or when refactoring reveals need for new abstractions. Focuses on feature-based architecture and type safety.
---

# Component Designing

Component and type design for TypeScript + React applications.
Use when planning new features or identifying need for new abstractions during refactoring.

## When to Use
- Planning a new feature (before writing code)
- Refactoring reveals need for new components/hooks
- Linter failures suggest better abstractions
- When you need to think through component architecture
- Designing state management approach

## Purpose
Design clean, well-composed components and types that:
- Prevent primitive obsession (use branded types, Zod schemas)
- Ensure type safety with TypeScript
- Follow component composition patterns
- Implement feature-based architecture
- Create reusable custom hooks

## Workflow

### 0. Architecture Pattern Analysis (FIRST STEP)

**Default: Always use feature-based architecture** (group by feature, not technical layer).

Scan codebase structure:
- **Feature-based**: `src/features/auth/{LoginForm,useAuth,types,AuthContext}.tsx` ✅
- **Technical layers**: `src/{components,hooks,contexts}/auth.tsx` ⚠️

**Decision Flow**:
1. **Pure feature-based** → Continue pattern, implement as `src/features/[new-feature]/`
2. **Pure technical layers** → Propose: Start migration with `docs/architecture/feature-based-migration.md`, implement new feature as first feature slice
3. **Mixed (migrating)** → Check for migration docs, continue pattern as feature-based

**Always ask user approval with options:**
- Option A: Feature-based (recommended for cohesion/maintainability)
- Option B: Match existing pattern (if time-constrained)
- Acknowledge: Time pressure, team decisions, consistency needs are valid

**If migration needed**, create/update `docs/architecture/feature-based-migration.md`:
```markdown
# Feature-Based Architecture Migration Plan
## Current State: [technical-layers/mixed]
## Target: Feature-based structure in src/features/[feature]/
## Strategy: New features feature-based, migrate existing incrementally
## Progress: [x] [new-feature] (this PR), [ ] existing features
```

See reference.md section #2 for detailed patterns.

---

### 1. Understand Domain

- What is the problem domain?
- What are the main UI concepts/interactions?
- What state needs to be managed?
- What are the user flows?
- How does this fit into existing architecture?

### 2. Identify Core Abstractions

Ask for each concept:
- Is this currently a primitive (string, number, boolean)?
- Does it have validation rules?
- Is it a UI concept (component)?
- Is it reusable logic (custom hook)?
- Is it shared state (context)?
- Does it need type safety (branded type)?

### 3. Design Self-Validating Types

For primitives with validation (Email, UserId, Port):

**Option A: Zod Schemas (Recommended)**
```typescript
import { z } from 'zod'

// Schema definition with validation
export const EmailSchema = z.string().email().min(1)
export const UserIdSchema = z.string().uuid()

// Extract type from schema
export type Email = z.infer<typeof EmailSchema>
export type UserId = z.infer<typeof UserIdSchema>

// Validation function
export function validateEmail(value: unknown): Email {
  return EmailSchema.parse(value) // Throws on invalid
}
```

**Option B: Branded Types (TypeScript)**
```typescript
// Brand for nominal typing
declare const __brand: unique symbol
type Brand<T, TBrand> = T & { [__brand]: TBrand }

export type Email = Brand<string, 'Email'>
export type UserId = Brand<string, 'UserId'>

// Validating constructor
export function createEmail(value: string): Email {
  if (!value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
    throw new Error('Invalid email format')
  }
  return value as Email
}

export function createUserId(value: string): UserId {
  if (!value || value.length === 0) {
    throw new Error('UserId cannot be empty')
  }
  return value as UserId
}
```

**When to use which:**
- Zod: Form validation, API parsing, runtime validation
- Branded types: Type safety without runtime overhead

### 4. Design Component Structure

**Component Types:**

**A. Presentational Components (Pure UI)**
- No state management
- Props-driven
- Reusable across features
- 100% testable

```typescript
interface ButtonProps {
  label: string
  onClick: () => void
  variant?: 'primary' | 'secondary'
  disabled?: boolean
}

export function Button({ label, onClick, variant = 'primary', disabled = false }: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant}`}
      onClick={onClick}
      disabled={disabled}
    >
      {label}
    </button>
  )
}
```

**B. Container Components (Logic + State)**
- Manage state
- Handle side effects
- Coordinate data fetching
- Compose presentational components

```typescript
export function LoginContainer() {
  const { login, isLoading, error } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async () => {
    try {
      const validEmail = EmailSchema.parse(email)
      await login(validEmail, password)
    } catch (error) {
      // Handle error
    }
  }

  return (
    <LoginForm
      email={email}
      password={password}
      onEmailChange={setEmail}
      onPasswordChange={setPassword}
      onSubmit={handleSubmit}
      isLoading={isLoading}
      error={error}
    />
  )
}
```

### 5. Design Custom Hooks

Extract reusable logic into custom hooks:

```typescript
// Single responsibility: Form state management
export function useFormState<T>(initialValues: T) {
  const [values, setValues] = useState<T>(initialValues)
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({})

  const setValue = <K extends keyof T>(key: K, value: T[K]) => {
    setValues(prev => ({ ...prev, [key]: value }))
    setErrors(prev => ({ ...prev, [key]: undefined }))
  }

  const reset = () => {
    setValues(initialValues)
    setErrors({})
  }

  return { values, errors, setValue, setErrors, reset }
}

// Single responsibility: Data fetching
export function useUsers() {
  const [users, setUsers] = useState<User[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const fetchUsers = async () => {
      setIsLoading(true)
      try {
        const data = await api.getUsers()
        setUsers(data)
      } catch (err) {
        setError(err as Error)
      } finally {
        setIsLoading(false)
      }
    }
    fetchUsers()
  }, [])

  return { users, isLoading, error }
}
```

### 6. Design Context for Shared State

When state is needed across 3+ component levels:

```typescript
interface AuthContextValue {
  user: User | null
  login: (email: Email, password: string) => Promise<void>
  logout: () => Promise<void>
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  const login = async (email: Email, password: string) => {
    const user = await api.login(email, password)
    setUser(user)
  }

  const logout = async () => {
    await api.logout()
    setUser(null)
  }

  const value = useMemo(
    () => ({ user, login, logout, isAuthenticated: !!user }),
    [user]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

### 7. Plan Feature Structure

**Feature-based structure (Recommended)**:
```
src/features/auth/
├── components/
│   ├── LoginForm.tsx          # Presentational
│   ├── LoginForm.test.tsx
│   ├── RegisterForm.tsx
│   └── RegisterForm.test.tsx
├── hooks/
│   ├── useAuth.ts             # Custom hook
│   ├── useAuth.test.ts
│   ├── useFormValidation.ts
│   └── useFormValidation.test.ts
├── context/
│   ├── AuthContext.tsx        # Shared state
│   └── AuthContext.test.tsx
├── types.ts                    # Email, UserId, etc.
├── api.ts                      # API calls
└── index.ts                    # Public exports
```

**Bad structure (Technical layers)**:
```
src/
├── components/LoginForm.tsx
├── hooks/useAuth.ts
├── contexts/AuthContext.tsx
└── types/auth.ts
```

### 8. Review Against Principles

Check design against (see reference.md):
- [ ] No primitive obsession (use Zod/branded types)
- [ ] Feature-based architecture
- [ ] Component composition over prop drilling
- [ ] Custom hooks for reusable logic
- [ ] Context only when needed (3+ levels)
- [ ] Clear separation: presentational vs container
- [ ] Props interfaces well-defined

## Output Format

After design phase:

```
🎨 DESIGN PLAN

Feature: User Authentication

Core Domain Types:
✅ Email (Zod schema) - RFC 5322 validation, used in login/register
✅ UserId (branded type) - Non-empty string, prevents invalid IDs
✅ User (interface) - { id: UserId, email: Email, name: string }

Components:
✅ LoginForm (Presentational)
   Props: { email, password, onSubmit, isLoading, error }
   Responsibility: UI only, no state

✅ LoginContainer (Container)
   Responsibility: State management, form handling, validation
   Uses: LoginForm, useAuth hook

✅ RegisterForm (Presentational)
   Props: { formData, onSubmit, isLoading, errors }
   Responsibility: UI only, no state

Custom Hooks:
✅ useAuth
   Returns: { user, login, logout, isAuthenticated, isLoading }
   Responsibility: Auth operations and state

✅ useFormValidation
   Returns: { values, errors, setValue, validate, reset }
   Responsibility: Form state and validation logic

Context:
✅ AuthContext
   Provides: { user, login, logout, isAuthenticated }
   Used by: Protected routes, user menu, profile pages
   Reason: Auth state needed across entire app

Feature Structure:
📁 src/features/auth/
  ├── components/
  │   ├── LoginForm.tsx
  │   ├── LoginForm.test.tsx
  │   ├── RegisterForm.tsx
  │   └── RegisterForm.test.tsx
  ├── hooks/
  │   ├── useAuth.ts
  │   ├── useAuth.test.ts
  │   ├── useFormValidation.ts
  │   └── useFormValidation.test.ts
  ├── context/
  │   ├── AuthContext.tsx
  │   └── AuthContext.test.tsx
  ├── types.ts
  ├── api.ts
  └── index.ts

Design Decisions:
- Email and UserId as validated types prevent runtime errors
- Zod for Email (form validation), branded type for UserId (type safety)
- LoginForm is presentational for reusability and testability
- useAuth hook encapsulates auth logic for reuse across components
- AuthContext provides auth state to avoid prop drilling
- Feature-based structure keeps all auth code together

Integration Points:
- Consumed by: App routes, protected route wrapper, user menu
- Depends on: API client, token storage
- Events: User login/logout events for analytics

Next Steps:
1. Create types with validation (Zod schemas + branded types)
2. Write tests for types and hooks (Jest + RTL)
3. Implement presentational components (LoginForm)
4. Implement container components (LoginContainer)
5. Add context provider (AuthContext)
6. Integration tests for full flows

Ready to implement? Use @testing skill for test structure.
```

## Key Principles

See reference.md for detailed principles:
- Primitive obsession prevention (Zod schemas, branded types)
- Component composition patterns
- Feature-based architecture
- Custom hooks for reusable logic
- Context for shared state (use sparingly)
- Props interfaces and type safety

## Pre-Code Review Questions

Before writing code, ask:
- Can logic be moved into custom hooks?
- Is this component presentational or container?
- Should state be local or context?
- Have I avoided primitive obsession?
- Is validation in the right place?
- Does this follow feature-based architecture?
- Are components small and focused?

Only after satisfactory answers, proceed to implementation.

See reference.md for complete design principles and examples.
