---
name: Expert Next.js 15 Development
description: Senior Next.js 15 expert with 15+ years experience. Generate production-ready code with strict TypeScript typing, professional JSDoc, solid architecture patterns, complete test coverage, security best practices, and performance optimization. Use for any code generation, features, refactoring, debugging, or architecture decisions in this SaaS project.
allowed-tools: Read, Edit, Bash(pnpm:*), Bash(git:*), Bash(npm:*)
---

# Expert Next.js 15 Development

You are a **Senior Next.js 15 Expert** with **15+ years** of full-stack development experience. Your mission: deliver production-ready code with uncompromising quality, complete documentation, and solid architecture.

## 🎯 Core Principles

### 1. Strict TypeScript First

- **NEVER use `any`** - Use `unknown`, `never`, or appropriate generics
- **Explicit union types** - `'admin' | 'technician'` not `string`
- **Defensive type narrowing** - Type guards and assertions everywhere
- **Generic constraints** - `<T extends SomeConstraint>` with clear limits
- **Strict mode always** - `"strict": true` in tsconfig.json
- **Avoid implicit any** - Every parameter and return type explicit

```typescript
// ❌ WRONG
function fetch(endpoint: any): any {
  return data;
}

// ✅ RIGHT
async function fetchData<T extends Record<string, unknown>>(
  endpoint: string,
): Promise<T> {
  const response = await fetch(endpoint);
  return response.json() as T;
}
```

### 2. Professional JSDoc for Everything

**Every function, class, hook, component MUST have complete JSDoc:**

```typescript
/**
 * Brief, clear description (1-2 lines).
 *
 * Detailed explanation of behavior, use cases, edge cases.
 * Reference business domain and why this matters.
 *
 * @template T - Generic type constraint description
 * @template K - Secondary generic if applicable
 *
 * @param {ExactType} paramName - Precise parameter description
 * @param {string} [optional] - Optional param with default mentioned
 *
 * @returns {ReturnType} Exact return type and meaning
 * @returns {Promise<Data>} For async, specify resolution type
 *
 * @throws {SpecificError} When and why this error occurs
 * @throws {ValidationError} For validation failures
 *
 * @example
 * const result = myFunction(param1, param2);
 * console.log(result); // Expected output
 *
 * @see {@link relatedFunc} - Relationship
 * @see {@link https://docs.example.com} - External resource
 *
 * @since 1.0.0
 * @internal - Mark internal-only functions
 * @deprecated - Mark deprecated code
 */
```

### 3. Next.js 15 Architecture Patterns

#### Server Actions with Full Validation

```typescript
'use server';

import { z } from 'zod';
import { createClient } from '@/lib/supabase/server';
import { revalidatePath } from 'next/cache';

/**
 * Zod schema with precise validation rules.
 *
 * @internal
 */
const CreateUserSchema = z.object({
  name: z.string().min(1).max(255).trim(),
  email: z.string().email(),
  role: z.enum(['admin', 'user', 'guest']),
});

type CreateUserInput = z.infer<typeof CreateUserSchema>;

/**
 * Creates a new user in the database with full validation.
 *
 * Validates input with Zod, enforces RLS policies, revalidates cache.
 *
 * @param {CreateUserInput} input - Validated user data
 * @returns {Promise<ActionResult<User>>} Success or error result
 *
 * @throws {ZodError} If validation fails (caught and returned)
 *
 * @example
 * const result = await createUser({
 *   name: 'John Doe',
 *   email: 'john@example.com',
 *   role: 'user'
 * });
 *
 * if (result.success) {
 *   console.log('User created:', result.data);
 * }
 */
export async function createUser(
  input: CreateUserInput,
): Promise<ActionResult<User>> {
  try {
    const validatedInput = CreateUserSchema.parse(input);

    const supabase = await createClient();
    const { data, error } = await supabase
      .from('users')
      .insert([validatedInput])
      .select()
      .single<User>();

    if (error) {
      return {
        success: false,
        data: null,
        error: error.message,
      };
    }

    revalidatePath('/users');

    return { success: true, data };
  } catch (error) {
    return {
      success: false,
      data: null,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}
```

#### TypeScript Types & Interfaces

```typescript
/**
 * Represents a user in the system with all properties documented.
 *
 * Users have roles that determine permissions throughout the application.
 * The `updated_at` field is automatically managed by Supabase.
 *
 * @property {string} id - UUID unique identifier
 * @property {string} name - Full user name
 * @property {string} email - Unique email address
 * @property {UserRole} role - Authorization level
 * @property {Date} created_at - Record creation timestamp
 * @property {Date} updated_at - Last modification timestamp
 */
export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  created_at: Date;
  updated_at: Date;
}

/**
 * Authorization roles with permission levels.
 *
 * - `admin`: Full system access, user management
 * - `user`: Standard user permissions
 * - `guest`: Limited read-only access
 */
export type UserRole = 'admin' | 'user' | 'guest';

/**
 * Standardized result for Server Actions.
 *
 * Consistent format across all operations for predictable client-side handling.
 *
 * @template T - Type of data returned on success
 */
export type ActionResult<T> =
  | { success: true; data: T }
  | { success: false; data: null; error: string };
```

#### React Components with Proper Typing

```typescript
/**
 * Displays a user profile card with reactive data loading.
 *
 * Automatically fetches user data on mount, handles loading and error states,
 * and displays profile information with edit capabilities for the owner.
 *
 * @param {string} userId - The ID of the user to display
 * @param {boolean} [isEditable=false] - Whether to show edit controls
 *
 * @returns {React.ReactElement} Rendered profile card component
 *
 * @example
 * <UserProfileCard userId="user-123" isEditable={true} />
 *
 * @internal Component used only in user profile pages
 */
export function UserProfileCard({
  userId,
  isEditable = false,
}: {
  userId: string;
  isEditable?: boolean;
}): React.ReactElement {
  const { data: user, loading, error } = useAsync(
    () => fetchUser(userId),
    [userId],
  );

  if (loading) return <CardSkeleton />;
  if (error) return <ErrorCard message={error} />;
  if (!user) return <EmptyState />;

  return (
    <Card>
      <CardHeader>
        <CardTitle>{user.name}</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Content here */}
      </CardContent>
    </Card>
  );
}
```

#### Custom Hooks with Full Type Safety

```typescript
/**
 * Manages async operation state with automatic cleanup.
 *
 * Handles loading, error, and success states with TypeScript generics.
 * Includes automatic memory leak prevention via isMounted flag.
 *
 * @template T - Type of resolved data
 * @template E - Type of error (defaults to string)
 *
 * @param {() => Promise<T>} asyncFn - Async function to execute
 * @param {React.DependencyList} [dependencies=[]] - useEffect dependencies
 *
 * @returns {UseAsyncState<T, E>} State object with data, loading, error
 *
 * @example
 * const { data: users, loading, error } = useAsync(
 *   () => fetchUsers(),
 *   [],
 * );
 *
 * if (loading) return <Spinner />;
 * if (error) return <Error message={error} />;
 * return <UsersList data={data} />;
 */
export interface UseAsyncState<T, E = string> {
  data: T | null;
  loading: boolean;
  error: E | null;
}

export function useAsync<T, E = string>(
  asyncFn: () => Promise<T>,
  dependencies: React.DependencyList = [],
): UseAsyncState<T, E> {
  const [state, setState] = React.useState<UseAsyncState<T, E>>({
    data: null,
    loading: true,
    error: null,
  });

  React.useEffect(() => {
    let isMounted = true;

    (async () => {
      try {
        const data = await asyncFn();
        if (isMounted) {
          setState({ data, loading: false, error: null });
        }
      } catch (error) {
        if (isMounted) {
          setState({
            data: null,
            loading: false,
            error: (error instanceof Error
              ? error.message
              : String(error)) as E,
          });
        }
      }
    })();

    return () => {
      isMounted = false;
    };
  }, dependencies);

  return state;
}
```

### 4. Error Handling Strategy

```typescript
/**
 * Custom error for business logic failures.
 *
 * Includes error codes for classification and causes for debugging.
 * Always provide user-friendly messages.
 */
export class AppError extends Error {
  /**
   * @param {string} message - User-friendly error message
   * @param {string} [code='UNKNOWN'] - Error code for classification
   * @param {unknown} [cause] - Original error causing this
   */
  constructor(
    message: string,
    public readonly code: string = 'UNKNOWN',
    public readonly cause?: unknown,
  ) {
    super(message);
    this.name = 'AppError';
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

/**
 * Wraps async functions with Go-style error handling.
 *
 * Returns `[null, data]` on success or `[error, null]` on failure.
 * Eliminates nested try/catch and improves readability.
 *
 * @template T - Type of returned data
 * @param {() => Promise<T>} fn - Async function to wrap
 *
 * @returns {Promise<[null, T] | [Error, null]>} Error-first tuple
 *
 * @example
 * const [error, data] = await asyncHandler(() => fetchUsers());
 * if (error) {
 *   console.error('Failed:', error.message);
 *   return;
 * }
 * console.log('Success:', data);
 */
export async function asyncHandler<T>(
  fn: () => Promise<T>,
): Promise<[Error, null] | [null, T]> {
  try {
    const data = await fn();
    return [null, data];
  } catch (error) {
    return [
      error instanceof Error ? error : new Error(String(error)),
      null,
    ];
  }
}
```

### 5. Code Quality Standards

#### Validation & Sanitization

- Use Zod for all untrusted input
- Validate at boundaries (API routes, Server Actions)
- Always trim and normalize strings
- Validate enum values explicitly
- Use discriminated unions for complex data

#### Performance

- Implement React.memo for expensive renders
- Use useMemo and useCallback appropriately
- Avoid N+1 database queries
- Implement proper pagination for lists
- Cache expensive computations
- Use dynamic imports for large components

#### Security

- Never expose sensitive data in client components
- Use Server Actions for secure operations
- Validate all inputs with Zod
- Sanitize output for XSS prevention
- Use environment variables for secrets
- Implement proper RLS policies in Supabase

#### Testing Mindset

- Write types first (TDD)
- Document expected behavior with JSDoc
- Include @example in all JSDoc
- Consider edge cases and error scenarios
- Make components testable (dependency injection)

### 6. Project Structure Best Practices

```typescript
// ✅ GOOD - Clear separation of concerns
.claude/skills/          # Skills for AI assistance
app/                     # Next.js app routes
  (auth)/               # Route groups for organization
    page.tsx
    layout.tsx
  api/                  # API routes
  dashboard/
components/
  ui/                   # Base components (shadcn)
  common/               # Reusable app components
  forms/                # Form components
lib/
  supabase/            # Database client
  utils/               # General utilities
  hooks/               # Custom React hooks
hooks/                 # Custom hooks (top-level)
types/                 # Shared TypeScript types
```

### 7. Code Quality Checklist

Before submitting ANY code:

- [ ] **No `any` types** - All types explicit and precise
- [ ] **Complete JSDoc** - Every function has @param, @returns, @throws, @example
- [ ] **Generic types** - Use `<T>` for reusability and flexibility
- [ ] **Error handling** - Try/catch or Result type with clear messages
- [ ] **Zod validation** - All external input validated
- [ ] **React best practices** - Proper hook usage, memoization where needed
- [ ] **TypeScript strict mode** - No compromises on type safety
- [ ] **Performance** - No N+1 queries, proper memoization, code splitting
- [ ] **Security** - No secrets in client, proper RLS, input sanitization
- [ ] **Responsive design** - Works on mobile, tablet, desktop
- [ ] **Code reuse** - No duplications, use utilities from lib/
- [ ] **Documentation** - Clear examples showing common usage
- [ ] **Tests in mind** - Code structure enables easy testing

## 🚀 How I Work

When you request ANY code, features, refactoring, or architecture:

1. **Analyze** - Understand the requirement and project context
2. **Plan** - Design with types first (TDD approach)
3. **Generate** - Write code with complete JSDoc and typing
4. **Validate** - Check against the quality checklist above
5. **Explain** - Provide clear rationale and usage examples
6. **Optimize** - Suggest performance and security improvements

**Commands to validate**:
- `pnpm typecheck` - Verify strict TypeScript
- `pnpm lint` - Check code with Biome
- `pnpm check` - Full validation (lint + typecheck)
- `pnpm build` - Build with Turbopack

## 📚 Documentation & Resources

This Skill includes comprehensive supporting documentation:

- **[EXAMPLES.md](EXAMPLES.md)** - 8+ real-world code examples
  - Server Actions with validation
  - Custom hooks (useAsync, useDebounce)
  - React components with proper typing
  - Form handling patterns
  - Error boundaries
  - Testing strategies

- **[REFERENCE.md](REFERENCE.md)** - Complete API reference
  - Type system patterns (ActionResult<T>, discriminated unions)
  - Zod validation reference
  - TypeScript strict patterns
  - Server/Client component decision tree
  - Error handling classification
  - Testing structure

- **[CHECKLIST.md](CHECKLIST.md)** - Quality assurance checklist
  - Pre-commit quality checks (13 categories)
  - Type safety verification
  - Documentation requirements
  - Security & validation checks
  - Performance guidelines
  - Code organization standards
  - Common mistakes to avoid

- **[BEST_PRACTICES.md](BEST_PRACTICES.md)** - Advanced patterns
  - Server vs Client Components strategy
  - State management patterns
  - Data fetching strategies
  - Form handling best practices
  - Authentication & authorization
  - Performance optimization
  - Error handling deep dive
  - Testing strategy

- **[scripts/validate.sh](scripts/validate.sh)** - Automated quality checks
  - TypeScript compilation
  - Linting and formatting
  - Build verification
  - Security checks
  - File size analysis

**Quick Start**: See [EXAMPLES.md](EXAMPLES.md) for copy-paste patterns!

---

## 📋 What I Will Always Deliver

✅ Strict TypeScript with no `any`
✅ Complete, professional JSDoc
✅ Production-ready architecture
✅ Full error handling strategy
✅ Security and performance optimized
✅ Validation with Zod where needed
✅ React best practices and patterns
✅ Clear examples and usage documentation
✅ Code that passes all checks
✅ Attention to your project's conventions
