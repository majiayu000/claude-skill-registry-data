---
name: jotai-patterns
description: Jotai atomic state management patterns. Use when implementing fine-grained reactive state.
---

# Jotai Patterns Skill

This skill covers Jotai atomic state management for React applications.

## When to Use

Use this skill when:
- Need fine-grained reactivity
- Building complex state dependencies
- Want provider-less global state
- Prefer atomic/bottom-up state design

## Core Principle

**ATOMS ARE PRIMITIVES** - Build complex state from simple atoms. Components subscribe only to atoms they use.

## Basic Atoms

```typescript
import { atom, useAtom, useAtomValue, useSetAtom } from 'jotai';

// Primitive atom
const countAtom = atom(0);

// Usage
function Counter(): React.ReactElement {
  const [count, setCount] = useAtom(countAtom);

  return (
    <button onClick={() => setCount((c) => c + 1)}>
      Count: {count}
    </button>
  );
}

// Read-only usage
function CountDisplay(): React.ReactElement {
  const count = useAtomValue(countAtom);
  return <span>Count: {count}</span>;
}

// Write-only usage
function IncrementButton(): React.ReactElement {
  const setCount = useSetAtom(countAtom);
  return <button onClick={() => setCount((c) => c + 1)}>+</button>;
}
```

## Derived Atoms

### Read-Only Derived

```typescript
const countAtom = atom(0);

// Derived atom (read-only)
const doubleCountAtom = atom((get) => get(countAtom) * 2);

const isEvenAtom = atom((get) => get(countAtom) % 2 === 0);

// Multiple dependencies
const usersAtom = atom<User[]>([]);
const filterAtom = atom('');

const filteredUsersAtom = atom((get) => {
  const users = get(usersAtom);
  const filter = get(filterAtom).toLowerCase();

  if (!filter) return users;
  return users.filter((user) =>
    user.name.toLowerCase().includes(filter)
  );
});
```

### Read-Write Derived

```typescript
const celsiusAtom = atom(0);

// Read-write derived atom
const fahrenheitAtom = atom(
  (get) => get(celsiusAtom) * (9 / 5) + 32,
  (get, set, newFahrenheit: number) => {
    set(celsiusAtom, (newFahrenheit - 32) * (5 / 9));
  }
);

// Usage - both read and write work
function TemperatureConverter(): React.ReactElement {
  const [celsius, setCelsius] = useAtom(celsiusAtom);
  const [fahrenheit, setFahrenheit] = useAtom(fahrenheitAtom);

  return (
    <div>
      <input
        type="number"
        value={celsius}
        onChange={(e) => setCelsius(Number(e.target.value))}
      />
      °C =
      <input
        type="number"
        value={fahrenheit}
        onChange={(e) => setFahrenheit(Number(e.target.value))}
      />
      °F
    </div>
  );
}
```

## Async Atoms

```typescript
// Async read atom
const userAtom = atom(async () => {
  const response = await fetch('/api/user');
  return response.json() as Promise<User>;
});

// Usage with Suspense
function UserProfile(): React.ReactElement {
  const user = useAtomValue(userAtom);
  return <h1>{user.name}</h1>;
}

function App(): React.ReactElement {
  return (
    <Suspense fallback={<Loading />}>
      <UserProfile />
    </Suspense>
  );
}

// Async with dependencies
const userIdAtom = atom('1');

const userDataAtom = atom(async (get) => {
  const userId = get(userIdAtom);
  const response = await fetch(`/api/users/${userId}`);
  return response.json() as Promise<User>;
});
```

## Write-Only Atoms (Actions)

```typescript
const todosAtom = atom<Todo[]>([]);

// Write-only atom for actions
const addTodoAtom = atom(null, (get, set, text: string) => {
  const newTodo: Todo = {
    id: crypto.randomUUID(),
    text,
    completed: false,
  };
  set(todosAtom, [...get(todosAtom), newTodo]);
});

const toggleTodoAtom = atom(null, (get, set, id: string) => {
  set(
    todosAtom,
    get(todosAtom).map((todo) =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    )
  );
});

const removeTodoAtom = atom(null, (get, set, id: string) => {
  set(
    todosAtom,
    get(todosAtom).filter((todo) => todo.id !== id)
  );
});

// Usage
function AddTodo(): React.ReactElement {
  const addTodo = useSetAtom(addTodoAtom);
  const [text, setText] = useState('');

  const handleSubmit = (e: FormEvent): void => {
    e.preventDefault();
    if (text.trim()) {
      addTodo(text);
      setText('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <button type="submit">Add</button>
    </form>
  );
}
```

## Atom Families

```typescript
import { atomFamily } from 'jotai/utils';

// Create atoms dynamically
const todoAtomFamily = atomFamily((id: string) =>
  atom<Todo | null>(null)
);

// Usage
function TodoItem({ id }: { id: string }): React.ReactElement {
  const [todo, setTodo] = useAtom(todoAtomFamily(id));

  if (!todo) return null;

  return (
    <div>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() =>
          setTodo({ ...todo, completed: !todo.completed })
        }
      />
      {todo.text}
    </div>
  );
}
```

## Persistence

```typescript
import { atomWithStorage } from 'jotai/utils';

// Persisted to localStorage
const themeAtom = atomWithStorage<'light' | 'dark'>('theme', 'light');

const settingsAtom = atomWithStorage('settings', {
  notifications: true,
  language: 'en',
});

// Usage - automatically syncs with localStorage
function ThemeToggle(): React.ReactElement {
  const [theme, setTheme] = useAtom(themeAtom);

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      {theme}
    </button>
  );
}
```

## Reset Atoms

```typescript
import { atomWithReset, useResetAtom, RESET } from 'jotai/utils';

const formAtom = atomWithReset({
  name: '',
  email: '',
  message: '',
});

function ContactForm(): React.ReactElement {
  const [form, setForm] = useAtom(formAtom);
  const resetForm = useResetAtom(formAtom);

  // Or use RESET symbol
  // setForm(RESET);

  return (
    <form>
      <input
        value={form.name}
        onChange={(e) => setForm({ ...form, name: e.target.value })}
      />
      <button type="button" onClick={resetForm}>
        Reset
      </button>
    </form>
  );
}
```

## Combining with TanStack Query

```typescript
import { atomWithQuery } from 'jotai-tanstack-query';

const userIdAtom = atom('1');

const userAtom = atomWithQuery((get) => ({
  queryKey: ['user', get(userIdAtom)],
  queryFn: () => fetchUser(get(userIdAtom)),
}));

function UserProfile(): React.ReactElement {
  const [{ data: user, isLoading }] = useAtom(userAtom);

  if (isLoading) return <Loading />;
  return <div>{user?.name}</div>;
}
```

## DevTools

```typescript
import { useAtomsDebugValue } from 'jotai-devtools';

function App(): React.ReactElement {
  useAtomsDebugValue(); // Shows atoms in React DevTools

  return <Main />;
}
```

## Best Practices

1. **Start with primitive atoms** - Build complex from simple
2. **Use derived atoms** - Avoid duplicating state
3. **Keep atoms small** - One concern per atom
4. **Use atom families** - For dynamic/collection state
5. **Prefer useAtomValue/useSetAtom** - When only reading or writing

## Jotai vs Zustand

| Feature | Jotai | Zustand |
|---------|-------|---------|
| Model | Bottom-up (atoms) | Top-down (store) |
| Subscriptions | Automatic (fine-grained) | Manual (selectors) |
| Provider | Optional | Not needed |
| Async | Built-in | Manual |
| DevTools | Separate package | Middleware |
| Best for | Complex dependencies | Simple global state |

## When to Use Jotai

- Complex state dependencies
- Fine-grained re-render control
- Derived state calculations
- Code splitting state
- When you think in "atoms"

## Notes

- Atoms are not stored in a single object
- Each atom can be code-split
- No provider needed (uses React context internally)
- Works great with React Suspense
