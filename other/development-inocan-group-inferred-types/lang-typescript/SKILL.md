---
name: lang-typescript
description: TypeScript 5.9+ development specialist covering SolidJS, TanStack Start, Valibot validation, and modern TypeScript patterns. Use when developing TypeScript applications, SolidJS components, TanStack Start pages, or type-safe APIs.
version: 0.0.1
updated: 2025-12-30
status: active
credit: modu-ai/moai-adk
---

## Quick Reference (30 seconds)

TypeScript 5.9+ Development Specialist - Modern TypeScript with SolidJS, TanStack Start, and type-safe API patterns.

Auto-Triggers: `.ts`, `.tsx`, `.mts`, `.cts` files, TypeScript configurations, SolidJS/TanStack Start projects

Core Stack:
- TypeScript 5.9: Deferred module evaluation, decorators, satisfies operator
- SolidJS: Fine-grained reactivity, signals, stores
- TanStack Start: Full-stack framework with file-based routing, server functions
- Valibot: Tree-shakable schema validation
- Testing: Vitest, Solid Testing Library, Playwright


---

## Implementation Guide (5 minutes)

### TypeScript 5.9 Key Features

Satisfies Operator - Type checking without widening:
```typescript
type Colors = "red" | "green" | "blue";
const palette = {
  red: [255, 0, 0],
  green: "#00ff00",
  blue: [0, 0, 255],
} satisfies Record<Colors, string | number[]>;

palette.red.map((n) => n * 2); // Works - red is number[]
palette.green.toUpperCase();   // Works - green is string
```

Deferred Module Evaluation:
```typescript
import defer * as analytics from "./heavy-analytics";
function trackEvent(name: string) {
  analytics.track(name); // Loads module on first use
}
```

Modern Decorators (Stage 3):
```typescript
function logged<T extends (...args: any[]) => any>(
  target: T,
  context: ClassMethodDecoratorContext
) {
  return function (this: ThisParameterType<T>, ...args: Parameters<T>) {
    console.log(`Calling ${String(context.name)}`);
    return target.apply(this, args);
  };
}

class API {
  @logged
  async fetchUser(id: string) { return fetch(`/api/users/${id}`); }
}
```

### Solid JS Patterns

**CRITICAL: This is SolidJS, NOT React!**

**SolidJS uses different primitives than React. Never use React hooks!**

| SolidJS | React (DON'T USE) |
|---------|-------------------|
| `createSignal()` | `useState()` |
| `createEffect()` | `useEffect()` |
| `createStore()` | `useState()` |
| `createMemo()` | `useMemo()` |
| `<For>` | `array.map()` |
| `<Show>` | `&&` conditional |

#### Signal Pattern (Simple State)

```tsx
import { createSignal } from "solid-js";

const Counter: Component = () => {
    // Signal returns [getter, setter]
    const [count, setCount] = createSignal(0);

    // Getter is a function - must call it
    const increment = () => {
        setCount(count() + 1);  // count() to read
    };

    // Can also use callback form
    const decrement = () => {
        setCount(c => c - 1);   // Callback receives current value
    };

    return (
        <div>
            <p>Count: {count()}</p>  {/* Must call count() */}
            <button onClick={increment}>+</button>
            <button onClick={decrement}>-</button>
        </div>
    );
};
```

**Key points:**
- Signals return `[getter, setter]`
- Getters are functions: `count()` not `count`
- Setter can take value or callback
- Signals are reactive - UI updates automatically

#### Store Pattern (Complex State)

```tsx
import { createStore } from "solid-js/store";

interface FormState {
    firstName: string;
    lastName: string;
    email: string;
    preferences: {
        theme: "light" | "dark";
        notifications: boolean;
    };
}

const UserForm: Component = () => {
    const [formState, setFormState] = createStore<FormState>({
        firstName: "",
        lastName: "",
        email: "",
        preferences: {
            theme: "light",
            notifications: true,
        },
    });

    // Update top-level field
    const updateFirstName = (value: string) => {
        setFormState("firstName", value);
    };

    // Update nested field
    const updateTheme = (theme: "light" | "dark") => {
        setFormState("preferences", "theme", theme);
    };

    // Update multiple fields
    const updatePreferences = () => {
        setFormState("preferences", {
            theme: "dark",
            notifications: false,
        });
    };

    return (
        <form>
            <input
                value={formState.firstName}
                onInput={(e) => setFormState("firstName", e.currentTarget.value)}
            />
            <input
                value={formState.email}
                onInput={(e) => setFormState("email", e.currentTarget.value)}
            />
        </form>
    );
};
```

**When to use stores:**
- Forms with multiple fields
- Nested state objects
- Arrays that need reactivity
- State that needs granular updates

#### Memo Pattern (Computed Values)

```tsx
import { createSignal, createMemo } from "solid-js";

const UserProfile: Component = () => {
    const [firstName, setFirstName] = createSignal("John");
    const [lastName, setLastName] = createSignal("Doe");

    // Memoized computed value
    const fullName = createMemo(() => {
        return `${firstName()} ${lastName()}`;
    });

    // Only recalculates when firstName or lastName changes
    const initials = createMemo(() => {
        return `${firstName()[0]}${lastName()[0]}`;
    });

    return (
        <div>
            <p>Full Name: {fullName()}</p>
            <p>Initials: {initials()}</p>
        </div>
    );
};
```

**Use memos for:**
- Expensive computations
- Derived state
- Filtering/mapping data
- Values used in multiple places

#### Resource Pattern (Data Fetching)

##### Basic usage
```tsx
import { createSignal, createEffect } from "solid-js";

const DataFetcher: Component = () => {
    const [userId, setUserId] = createSignal("123");
    const [userData, setUserData] = createSignal(null);

    // Effect runs when dependencies change
    createEffect(() => {
        const id = userId();  // Dependency tracking

        fetch(`/api/users/${id}`)
            .then(res => res.json())
            .then(data => setUserData(data));
    });

    return <div>{/* ... */}</div>;
};
```

##### With source

```tsx
const [userId, setUserId] = createSignal(1);

const [user] = createResource(userId, async (id) => {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
});

// Automatically refetches when userId changes
setUserId(2);
```

##### With actions

```tsx
const [posts, { refetch, mutate }] = createResource(fetchPosts);

// Manual refetch
await refetch();

// Optimistic update
mutate((posts) => [...posts, newPost]);
```

##### Error handling

```tsx
const [data] = createResource(async () => {
  const response = await fetch('/api/data');
  if (!response.ok) throw new Error('Failed to fetch');
  return response.json();
});

// In JSX
<ErrorBoundary fallback={<div>Error loading data</div>}>
  <div>{data()?.title}</div>
</ErrorBoundary>
```

##### With initial value

```tsx
const [user] = createResource(() => fetchUser(), {
  initialValue: { name: "Loading...", id: 0 },
});

// user() is never undefined
console.log(user().name); // "Loading..." initially
```

**Use effects for:**
- API calls
- Data fetching
- Local storage updates
- Subscriptions

#### Effect Pattern (Side Effects)

```tsx
import { createSignal, createEffect } from "solid-js";

const DataFetcher: Component = () => {
    const [userId, setUserId] = createSignal("123");
    const [userData, setUserData] = createSignal(null);

    // Effect runs when dependencies change
    createEffect(() => {
        const id = userId();  // Dependency tracking

        fetch(`/api/users/${id}`)
            .then(res => res.json())
            .then(data => setUserData(data));
    });

    return <div>{/* ... */}</div>;
};
```

**Use effects for:**
- DOM manipulation
- Logging/analytics

#### Component Pattern

```tsx
import { Component, createSignal } from "solid-js";
import styles from "./MyComponent.module.scss";

interface MyComponentProps {
    title: string;
    initialCount?: number;
    onSubmit?: (value: number) => void;
}

const MyComponent: Component<MyComponentProps> = (props) => {
    const [count, setCount] = createSignal(props.initialCount || 0);

    const handleSubmit = () => {
        props.onSubmit?.(count());
    };

    return (
        <div class={styles.container}>
            <h2>{props.title}</h2>
            <p>Count: {count()}</p>
            <button onClick={() => setCount(c => c + 1)}>Increment</button>
            <button onClick={handleSubmit}>Submit</button>
        </div>
    );
};

export default MyComponent;
```

**Conventions:**
- Use `Component<Props>` type
- Props interface above component
- CSS modules for styling
- `class` not `className`
- Export default at end

#### Conditional Rendering

```tsx
import { Show } from "solid-js";

const ConditionalExample: Component = () => {
    const [user, setUser] = createSignal<User | null>(null);
    const [isLoading, setIsLoading] = createSignal(true);

    return (
        <div>
            {/* Show/hide pattern */}
            <Show when={isLoading()}>
                <Spinner />
            </Show>

            {/* Show with fallback */}
            <Show when={user()} fallback={<p>No user found</p>}>
                {(u) => <UserProfile user={u()} />}
            </Show>

            {/* Multiple conditions */}
            <Show
                when={!isLoading() && user()}
                fallback={<p>Loading or no user...</p>}
            >
                {(u) => <p>Welcome, {u().name}!</p>}
            </Show>
        </div>
    );
};
```

**Use `<Show>` instead of `&&` operator:**
- ✅ `<Show when={condition}><Component /></Show>`
- ❌ `{condition && <Component />}`

#### List Rendering

```tsx
import { For, Index } from "solid-js";

interface User {
    id: string;
    name: string;
}

const UserList: Component = () => {
    const [users, setUsers] = createSignal<User[]>([
        { id: "1", name: "Alice" },
        { id: "2", name: "Bob" },
    ]);

    return (
        <div>
            {/* For - use when items have stable identity */}
            <For each={users()}>
                {(user) => (
                    <div class={styles.userCard}>
                        <p>{user.name}</p>
                    </div>
                )}
            </For>

            {/* Index - use when items don't have stable identity */}
            <Index each={users()}>
                {(user, index) => (
                    <div>
                        {index}: {user().name}
                    </div>
                )}
            </Index>
        </div>
    );
};
```

**Use `<For>` instead of `array.map()`:**
- ✅ `<For each={items()}>{(item) => <div>{item.name}</div>}</For>`
- ❌ `{items().map(item => <div>{item.name}</div>)}`

#### Event Handling

```tsx
const EventExample: Component = () => {
    const [value, setValue] = createSignal("");

    // Input event (onInput, not onChange)
    const handleInput = (e: InputEvent) => {
        const target = e.currentTarget as HTMLInputElement;
        setValue(target.value);
    };

    // Click event
    const handleClick = (e: MouseEvent) => {
        e.preventDefault();
        console.log("Clicked!");
    };

    // Submit event
    const handleSubmit = (e: SubmitEvent) => {
        e.preventDefault();
        console.log("Submitted:", value());
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={value()}
                onInput={handleInput}
            />
            <button onClick={handleClick}>Click</button>
        </form>
    );
};
```

**Event naming:**
- `onInput` for text inputs (not `onChange`)
- `onClick` for clicks
- `onSubmit` for forms
- camelCase event names

#### Refs

```tsx
import { onMount } from "solid-js";

const RefExample: Component = () => {
    let inputRef: HTMLInputElement | undefined;

    onMount(() => {
        // Access ref after mount
        inputRef?.focus();
    });

    return (
        <input
            ref={inputRef}
            type="text"
        />
    );
};
```

**Use `ref` prop, not `useRef()`:**
- ✅ `let inputRef; <input ref={inputRef} />`
- ❌ `const inputRef = useRef()`

#### Lifecycle

```tsx
import { onMount, onCleanup, createEffect } from "solid-js";

const LifecycleExample: Component = () => {
    // Runs once after mount
    onMount(() => {
        console.log("Component mounted");
        fetchData();
    });

    // Cleanup function
    onCleanup(() => {
        console.log("Component will unmount");
        cancelSubscription();
    });

    // Effect with cleanup
    createEffect(() => {
        const subscription = subscribe();

        onCleanup(() => {
            subscription.unsubscribe();
        });
    });

    return <div>...</div>;
};
```

#### Dynamic Classes

```tsx
import { createSignal } from "solid-js";
import styles from "./Button.module.scss";

const Button: Component<{ variant?: "primary" | "secondary" }> = (props) => {
    const [isActive, setIsActive] = createSignal(false);

    return (
        <button
            class={styles.button}
            classList={{
                [styles.primary]: props.variant === "primary",
                [styles.secondary]: props.variant === "secondary",
                [styles.active]: isActive(),
            }}
            onClick={() => setIsActive(!isActive())}
        >
            Click me
        </button>
    );
};
```

**Use `classList` for conditional classes:**
- ✅ `classList={{ [styles.active]: isActive() }}`
- ❌ `className={isActive() ? styles.active : ""}`

#### Context Pattern

```tsx
import { createContext, useContext, JSX } from "solid-js";
import { createStore } from "solid-js/store";

// Context type
type AppContextValue = {
    user: () => User | null;
    theme: () => "light" | "dark";
    setTheme: (theme: "light" | "dark") => void;
};

// Create context
const AppContext = createContext<AppContextValue>();

// Provider component
export function AppProvider(props: { children: JSX.Element }) {
    const [state, setState] = createStore({
        user: null as User | null,
        theme: "light" as "light" | "dark",
    });

    const value: AppContextValue = {
        user: () => state.user,
        theme: () => state.theme,
        setTheme: (theme) => setState("theme", theme),
    };

    return (
        <AppContext.Provider value={value}>
            {props.children}
        </AppContext.Provider>
    );
}

// Hook to use context
export function useApp() {
    const context = useContext(AppContext);
    if (!context) {
        throw new Error("useApp must be used within AppProvider");
    }
    return context;
}
```

#### Error Boundary

```tsx
import { ErrorBoundary } from "solid-js";

const App: Component = () => {
    return (
        <ErrorBoundary fallback={(err) => <ErrorView error={err} />}>
            <MainApp />
        </ErrorBoundary>
    );
};

const ErrorView: Component<{ error: Error }> = (props) => {
    return (
        <div>
            <h1>Something went wrong</h1>
            <pre>{props.error.message}</pre>
        </div>
    );
};
```

#### Common Anti-Patterns

##### ❌ Using React Hooks

```tsx
// DON'T DO THIS
const [state, setState] = useState(0);  // Wrong!
const value = useMemo(() => compute());  // Wrong!
useEffect(() => { /* ... */ });          // Wrong!
```

##### ❌ Forgetting to Call Signals

```tsx
// DON'T DO THIS
<p>Count: {count}</p>  // Wrong! count is a function

// DO THIS
<p>Count: {count()}</p>  // Correct!
```

##### ❌ Using Array.map()

```tsx
// DON'T DO THIS
{items().map(item => <div>{item.name}</div>)}

// DO THIS
<For each={items()}>
    {(item) => <div>{item.name}</div>}
</For>
```

##### ❌ Using && for Conditionals

```tsx
// DON'T DO THIS
{condition && <Component />}

// DO THIS
<Show when={condition}>
    <Component />
</Show>
```

#### Summary

**Key Patterns:**
1. Use `createSignal()` for simple state
2. Use `createStore()` for complex/nested state
3. Use `createMemo()` for computed values
4. Use `createResource()` for managing asynchronous data fetching and loading states
4. Use `createEffect()` for side effects
5. Use `<For>` for lists, not `array.map()`
6. Use `<Show>` for conditionals, not `&&`
7. Call signals as functions: `count()`
8. Use `Component<Props>` type
9. Use `class` not `className`
10. Use `onInput` not `onChange`

**Remember: This is SolidJS, NOT React!**

### TanStack Start

TanStack Start is a full-stack framework built on TanStack Router and Vinxi. It provides type-safe routing, server functions, and SSR out of the box.

Route Structure:
```
app/
  components/           # Shared components
  routes/               # File-based routing
    __root.tsx          # Root layout (wraps everything)
    index.tsx           # / route
    posts/
      index.tsx         # /posts
      $id.tsx           # /posts/:id (Dynamic route)
  client.tsx            # Client entry point
  router.tsx            # Router configuration
  ssr.tsx               # Server entry point
app.config.ts           # Vinxi/TanStack Start config
```

Route Definition:
```typescript
// app/routes/posts/$id.tsx
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/posts/$id')({
  // Params are automatically typed based on the file path
  loader: async ({ params }) => {
    return fetchPost(params.id)
  },
  component: PostComponent,
})

function PostComponent() {
  // Type-safe access to loader data
  const post = Route.useLoaderData()
  return <h1>{post.title}</h1>
}
```

Server Functions:
```typescript
import { createServerFn } from '@tanstack/start'
import { valibotValidator } from '@tanstack/valibot-adapter'
import * as v from 'valibot'

const UpdateUserSchema = v.object({
  id: v.pipe(v.string(), v.uuid()),
  name: v.pipe(v.string(), v.minLength(2), v.maxLength(100)),
  email: v.pipe(v.string(), v.email()),
})

// This function runs ONLY on the server
export const updateUser = createServerFn({ method: 'POST' })
  .validator(valibotValidator(UpdateUserSchema))
  .handler(async ({ data }) => {
    const user = await db.user.update({
      where: { id: data.id },
      data: { name: data.name, email: data.email },
    })
    return user
  })
```

Data Loading Pattern:
```typescript
// app/routes/users.tsx
import { createFileRoute } from '@tanstack/react-router'
import { createServerFn } from '@tanstack/start'

const getUsers = createServerFn({ method: 'GET' }).handler(async () => {
  return db.users.findMany()
})

export const Route = createFileRoute('/users')({
  loader: () => getUsers(),
  component: () => {
    const users = Route.useLoaderData()
    return (
      <ul>
        {users.map(user => <li key={user.id}>{user.name}</li>)}
      </ul>
    )
  }
})
```

Middleware:
```typescript
import { createMiddleware } from '@tanstack/start'

const authMiddleware = createMiddleware()
  .server(async ({ next, context }) => {
    const session = await getSession()
    if (!session) throw new Error('Unauthorized')
    return next({ context: { userId: session.userId } })
  })

const getUserProfile = createServerFn({ method: 'GET' })
  .middleware([authMiddleware])
  .handler(async ({ context }) => {
    // context.userId is typed and guaranteed
    return db.users.find(context.userId)
  })
```

### Valibot Schema Patterns

Complex Validation:
```typescript
import * as v from "valibot";

const UserSchema = v.object({
  id: v.pipe(v.string(), v.uuid()),
  name: v.pipe(v.string(), v.minLength(2), v.maxLength(100)),
  email: v.pipe(v.string(), v.email()),
  role: v.picklist(["admin", "user", "guest"]),
  createdAt: v.pipe(v.string(), v.isoTimestamp(), v.transform((s) => new Date(s))),
});

type User = v.InferOutput<typeof UserSchema>;

const CreateUserSchema = v.pipe(
  v.object({
    name: v.pipe(v.string(), v.minLength(2), v.maxLength(100)),
    email: v.pipe(v.string(), v.email()),
    password: v.pipe(v.string(), v.minLength(8)),
    confirmPassword: v.string(),
  }),
  v.forward(
    v.partialCheck(
      [["password"], ["confirmPassword"]],
      (input) => input.password === input.confirmPassword,
      "Passwords don't match"
    ),
    ["confirmPassword"]
  )
);

// Discriminated unions with v.variant
const EventSchema = v.variant("type", [
  v.object({ type: v.literal("click"), x: v.number(), y: v.number() }),
  v.object({ type: v.literal("keypress"), key: v.string() }),
  v.object({ type: v.literal("scroll"), delta: v.number() }),
]);

// Parsing
const result = v.safeParse(UserSchema, data);
if (result.success) {
  console.log(result.output);
} else {
  console.log(result.issues);
}
```

### State Management

SolidJS provides built-in reactive primitives. For complex global state, use stores with context.

Global Store with Context:
```typescript
import { createContext, useContext, ParentComponent } from "solid-js";
import { createStore, SetStoreFunction } from "solid-js/store";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
}

type AuthContextValue = [AuthState, {
  login: (user: User) => void;
  logout: () => void;
}];

const AuthContext = createContext<AuthContextValue>();

export const AuthProvider: ParentComponent = (props) => {
  const [state, setState] = createStore<AuthState>({
    user: null,
    isAuthenticated: false,
  });

  const actions = {
    login: (user: User) => setState({ user, isAuthenticated: true }),
    logout: () => setState({ user: null, isAuthenticated: false }),
  };

  return (
    <AuthContext.Provider value={[state, actions]}>
      {props.children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}

// Usage
function UserProfile() {
  const [auth, { logout }] = useAuth();
  return (
    <Show when={auth.user}>
      {(user) => (
        <div>
          <p>Welcome, {user().name}</p>
          <button onClick={logout}>Logout</button>
        </div>
      )}
    </Show>
  );
}
```

---

## Advanced Patterns

For comprehensive documentation including advanced TypeScript patterns, performance optimization, testing strategies, and deployment configurations, see:

- [reference.md](reference.md) - Complete API reference, Context7 library mappings, advanced type patterns
- [examples.md](examples.md) - Production-ready code examples, full-stack patterns, testing templates

### Context7 Integration

```typescript
// TypeScript - mcp__context7__get_library_docs("/microsoft/TypeScript", "decorators satisfies", 1)
// SolidJS - mcp__context7__get_library_docs("/solidjs/solid", "createSignal createStore", 1)
// TanStack Start - mcp__context7__get_library_docs("/tanstack/start", "server-functions routing", 1)
// TanStack Router - mcp__context7__get_library_docs("/tanstack/router", "file-based-routing loaders", 1)
// Valibot - mcp__context7__get_library_docs("/fabian-hiller/valibot", "schema validation pipe", 1)
```

---

## Works Well With

- `moai-domain-frontend` - UI components, styling patterns
- `moai-domain-backend` - API design, database integration
- `moai-workflow-testing` - Testing strategies and patterns
- `moai-foundation-quality` - Code quality standards
- `moai-essentials-debug` - Debugging TypeScript applications

---

## Quick Troubleshooting

TypeScript Errors:
```bash
bun run typecheck                    # Type check only
bunx tsc --generateTrace ./trace     # Performance trace
```

SolidJS/TanStack Start Issues:
```bash
bun run dev                         # Development mode
bun run build                       # Check for build errors
rm -rf .vinxi .output && bun run dev  # Clear cache
```

Type Safety:
```typescript
// Exhaustive check
function assertNever(x: never): never { throw new Error(`Unexpected: ${x}`); }

// Type guard
function isUser(v: unknown): v is User {
  return typeof v === "object" && v !== null && "id" in v;
}
```

---

Version: 1.1.0
Last Updated: 2025-12-30
