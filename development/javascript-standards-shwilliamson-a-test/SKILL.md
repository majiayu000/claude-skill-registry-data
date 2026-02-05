---
name: javascript-standards
description: JavaScript and TypeScript coding standards, conventions, and best practices. Use when writing, reviewing, or testing JS/TS code.
---

# JavaScript/TypeScript Coding Standards

## New Project Preferences

When starting new frontend projects, prefer:

- **React 18** with TypeScript
- **Vite** for development server
- **Parcel** for production bundling
- **shadcn/ui** for components
- **Tailwind CSS 3** for styling

## General Preferences

- **TypeScript over JavaScript** for new code
- **ESM over CommonJS** (`import`/`export` not `require`)
- **Prettier** for formatting, **ESLint** for linting
- **Strict TypeScript** (`"strict": true` in tsconfig)

## Style Guide

### Formatting (Prettier defaults)
- Line length: 80-100 characters
- Single quotes for strings
- Semicolons: consistent (prefer with)
- Trailing commas: ES5 or all
- 2 space indentation

### Naming Conventions
```typescript
// Files: kebab-case or PascalCase for components
user-service.ts
UserProfile.tsx

// Variables and functions: camelCase
const activeUsers = [];
function getUserById(userId: string): User {}

// Classes and types: PascalCase
class UserService {}
interface UserProfile {}
type UserId = string;

// Constants: SCREAMING_SNAKE_CASE or camelCase
const MAX_RETRY_ATTEMPTS = 3;
const defaultTimeout = 30000; // also acceptable

// React components: PascalCase
function UserCard({ user }: UserCardProps) {}
const ProfileHeader: React.FC<Props> = () => {};

// Boolean variables: is/has/should prefix
const isActive = true;
const hasPermission = false;
const shouldRefetch = true;
```

## TypeScript

### Type Definitions
```typescript
// Prefer interfaces for objects that can be extended
interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

// Use type for unions, intersections, mapped types
type UserId = string | number;
type UserWithPosts = User & { posts: Post[] };
type Readonly<T> = { readonly [K in keyof T]: T[K] };

// Avoid `any` - use `unknown` for truly unknown types
function parseJSON(json: string): unknown {
  return JSON.parse(json);
}

// Use generics for reusable types
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}
```

### Strict Null Checking
```typescript
// Always handle null/undefined explicitly
function getUser(id: string): User | null {
  const user = users.get(id);
  return user ?? null;
}

// Use optional chaining and nullish coalescing
const userName = user?.profile?.name ?? 'Anonymous';

// Non-null assertion only when you're certain
const element = document.getElementById('app')!;
```

### Enums and Constants
```typescript
// Prefer const objects over enums for better tree-shaking
const UserRole = {
  Admin: 'admin',
  User: 'user',
  Guest: 'guest',
} as const;

type UserRole = typeof UserRole[keyof typeof UserRole];

// If using enums, prefer string enums
enum Status {
  Pending = 'pending',
  Active = 'active',
  Inactive = 'inactive',
}
```

## Functions

```typescript
// Use arrow functions for callbacks and short functions
const doubled = numbers.map((n) => n * 2);

// Use function declarations for top-level/hoisted functions
function processUser(user: User): ProcessedUser {
  // ...
}

// Default parameters over optional with fallback
function greet(name: string, greeting = 'Hello'): string {
  return `${greeting}, ${name}!`;
}

// Destructure parameters for objects
function createUser({ email, name, role = 'user' }: CreateUserParams): User {
  // ...
}

// Use rest parameters over arguments
function sum(...numbers: number[]): number {
  return numbers.reduce((a, b) => a + b, 0);
}
```

## Async Code

```typescript
// Prefer async/await over .then() chains
async function fetchUserData(userId: string): Promise<UserData> {
  const user = await fetchUser(userId);
  const posts = await fetchPosts(userId);
  return { user, posts };
}

// Use Promise.all for concurrent operations
async function fetchAllData(userId: string): Promise<AllData> {
  const [user, posts, settings] = await Promise.all([
    fetchUser(userId),
    fetchPosts(userId),
    fetchSettings(userId),
  ]);
  return { user, posts, settings };
}

// Handle errors appropriately
async function safeOperation(): Promise<Result | null> {
  try {
    return await riskyOperation();
  } catch (error) {
    if (error instanceof NetworkError) {
      console.error('Network error:', error.message);
      return null;
    }
    throw error; // Re-throw unexpected errors
  }
}
```

## React Patterns

```typescript
// Functional components with TypeScript
interface UserCardProps {
  user: User;
  onEdit?: (user: User) => void;
  className?: string;
}

function UserCard({ user, onEdit, className }: UserCardProps) {
  return (
    <div className={className}>
      <h2>{user.name}</h2>
      {onEdit && <button onClick={() => onEdit(user)}>Edit</button>}
    </div>
  );
}

// Custom hooks
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        const data = await fetchUser(userId);
        if (!cancelled) setUser(data);
      } catch (e) {
        if (!cancelled) setError(e as Error);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => { cancelled = true; };
  }, [userId]);

  return { user, loading, error };
}

// Memoization
const ExpensiveComponent = memo(function ExpensiveComponent({ data }: Props) {
  const processed = useMemo(() => expensiveProcess(data), [data]);
  const handleClick = useCallback(() => onClick(data.id), [data.id, onClick]);

  return <div onClick={handleClick}>{processed}</div>;
});
```

## Error Handling

```typescript
// Custom error classes
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
  ) {
    super(message);
    this.name = 'AppError';
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} with id ${id} not found`, 'NOT_FOUND', 404);
    this.name = 'NotFoundError';
  }
}

// Type guards for error handling
function isAppError(error: unknown): error is AppError {
  return error instanceof AppError;
}

function handleError(error: unknown): Response {
  if (isAppError(error)) {
    return { status: error.statusCode, message: error.message };
  }
  console.error('Unexpected error:', error);
  return { status: 500, message: 'Internal server error' };
}
```

## Testing

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
// or: import { jest } from '@jest/globals';

describe('UserService', () => {
  let service: UserService;
  let mockDb: MockDatabase;

  beforeEach(() => {
    mockDb = createMockDatabase();
    service = new UserService(mockDb);
  });

  it('should fetch user by id', async () => {
    mockDb.users.get.mockResolvedValue({ id: '1', name: 'Test' });

    const user = await service.getUser('1');

    expect(user).toEqual({ id: '1', name: 'Test' });
    expect(mockDb.users.get).toHaveBeenCalledWith('1');
  });

  it('should throw NotFoundError for missing user', async () => {
    mockDb.users.get.mockResolvedValue(null);

    await expect(service.getUser('999')).rejects.toThrow(NotFoundError);
  });
});

// React Testing Library
import { render, screen, fireEvent } from '@testing-library/react';

describe('UserCard', () => {
  it('should display user name', () => {
    render(<UserCard user={{ id: '1', name: 'John' }} />);

    expect(screen.getByText('John')).toBeInTheDocument();
  });

  it('should call onEdit when button clicked', () => {
    const onEdit = vi.fn();
    render(<UserCard user={{ id: '1', name: 'John' }} onEdit={onEdit} />);

    fireEvent.click(screen.getByRole('button', { name: /edit/i }));

    expect(onEdit).toHaveBeenCalledWith({ id: '1', name: 'John' });
  });
});
```

## Project Commands

Check `.claude/commands.md` for project-specific commands. Common JS/TS commands:

```bash
# Dependencies
npm install
npm ci  # Clean install for CI

# Development
npm run dev
npm run build

# Linting & Formatting
npm run lint
npm run lint -- --fix
npm run format

# Testing
npm test
npm run test:watch
npm run test:coverage

# Type checking
npm run typecheck
npx tsc --noEmit
```
