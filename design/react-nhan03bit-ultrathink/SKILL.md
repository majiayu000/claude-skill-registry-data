---
name: react
description: "React patterns, hooks, state management, performance optimization, component architecture, TypeScript patterns for components, and data fetching. Absorbs component-patterns, typescript-frontend, typescript-patterns, state-management, zustand, jotai, swr, tanstack-query."
layer: domain
category: frontend
triggers: ["JSX", "QueryClientProvider", "SWRConfig", "as const", "atom", "atom(", "atomFamily", "atomWithStorage", "atomic state", "branded type", "component pattern", "compound component", "conditional type", "context vs zustand", "create store", "discriminated union", "generic component", "global state", "global state react", "headless component", "hoc pattern", "jotai", "mapped type", "polymorphic component", "queryClient", "react component", "react context", "react hook", "react memo", "react pattern", "react performance", "react query", "react render", "react types", "redux", "redux toolkit", "render props", "satisfies", "selector", "signals", "stale-while-revalidate", "state architecture", "state management", "store", "swr", "tanstack query", "template literal type", "type inference", "type safe", "type-level", "typescript DX", "typescript frontend", "typescript pattern", "useAtom", "useEffect", "useInfiniteQuery", "useMutation", "useQuery", "useSWR", "useSWRInfinite", "useSWRMutation", "useShallow", "useState", "zod schema", "zustand", "zustand middleware", "zustand persist", "zustand slice", "zustand store"]
---

# react

React patterns, hooks, state management, performance optimization, component architecture, TypeScript patterns for components, and data fetching. Absorbs component-patterns, typescript-frontend, typescript-patterns, state-management, zustand, jotai, swr, tanstack-query.


## Absorbs

- `component-patterns`
- `typescript-frontend`
- `typescript-patterns`
- `state-management`
- `zustand`
- `jotai`
- `swr`
- `tanstack-query`


## Core

# React Patterns & Performance

## Purpose

Provide expert-level guidance on React component architecture, hook patterns, rendering optimization, and idiomatic React development. This skill covers React 18+ with a focus on concurrent features, Server Components readiness, and production-grade patterns.

## Key Patterns

### Component Architecture

**Compound Components** — Use when building flexible, composable UI primitives:

```tsx
// Parent owns state, children consume via context
const Tabs = ({ children, defaultValue }: TabsProps) => {
  const [active, setActive] = useState(defaultValue);
  return (
    <TabsContext.Provider value={{ active, setActive }}>
      <div role="tablist">{children}</div>
    </TabsContext.Provider>
  );
};

Tabs.Tab = ({ value, children }: TabProps) => {
  const { active, setActive } = useTabsContext();
  return (
    <button
      role="tab"
      aria-selected={active === value}
      onClick={() => setActive(value)}
      className="px-6 py-4 text-base rounded-lg transition-all duration-200 focus-visible:ring-2 focus-visible:ring-offset-2"
    >
      {children}
    </button>
  );
};
```

**Render Props vs Hooks** — Prefer hooks for logic reuse. Use render props only when the consumer needs to control rendering output that depends on the shared state:

```tsx
// Prefer: Custom hook
function useToggle(initial = false) {
  const [on, setOn] = useState(initial);
  const toggle = useCallback(() => setOn(prev => !prev), []);
  const setTrue = useCallback(() => setOn(true), []);
  const setFalse = useCallback(() => setOn(false), []);
  return { on, toggle, setTrue, setFalse } as const;
}

// Avoid: Render prop for simple logic reuse
// Only use render props when children need positional/layout control
```

**Container/Presenter Split** — Separate data-fetching and side-effect logic from rendering:

```tsx
// Container: handles data and effects
function UserProfileContainer({ userId }: { userId: string }) {
  const user = use(fetchUser(userId)); // React 19 use()
  return <UserProfileView user={user} />;
}

// Presenter: pure rendering, easy to test and storybook
function UserProfileView({ user }: { user: User }) {
  return (
    <div className="p-6 rounded-xl shadow-sm">
      <h2 className="text-xl font-semibold">{user.name}</h2>
      <p className="text-base text-gray-600">{user.bio}</p>
    </div>
  );
}
```

### Hook Patterns

**Custom Hook Rules:**
1. Always prefix with `use`
2. Call hooks at the top level only (no conditionals, loops)
3. Return stable references — wrap callbacks in `useCallback`, derived objects in `useMemo`
4. Document dependency arrays explicitly

**useEffect Discipline:**

```tsx
// GOOD: Single responsibility, clear cleanup
useEffect(() => {
  const controller = new AbortController();
  fetchData(id, { signal: controller.signal })
    .then(setData)
    .catch(err => {
      if (!controller.signal.aborted) setError(err);
    });
  return () => controller.abort();
}, [id]);

// BAD: Multiple concerns in one effect
useEffect(() => {
  fetchData(id).then(setData);
  trackPageView(id);     // separate effect
  document.title = name; // separate effect
}, [id, name]);
```

**Derived State — Never sync state from props:**

```tsx
// BAD: Syncing state from props
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(`${first} ${last}`);
}, [first, last]);

// GOOD: Derive during render
const fullName = `${first} ${last}`;

// GOOD: Expensive derivation
const sortedItems = useMemo(
  () => items.toSorted((a, b) => a.name.localeCompare(b.name)),
  [items]
);
```

### Rendering Optimization

**When to use `React.memo`:**
- Component receives the same props frequently but parent re-renders often
- Component is expensive to render (large lists, complex SVG, charts)
- Component is a leaf node in a frequently-updating tree

```tsx
// Wrap with memo when the component is expensive and receives stable-ish props
const ExpensiveList = memo(function ExpensiveList({ items }: { items: Item[] }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </ul>
  );
});
```

**When NOT to use `React.memo`:**
- The component is cheap to render
- Props change on every render anyway (new objects/arrays inline)
- The component already uses context that changes frequently

**Avoid Re-render Cascades:**

```tsx
// BAD: New object every render breaks memo
<Child style={{ color: 'red' }} />

// GOOD: Stable reference
const style = useMemo(() => ({ color: 'red' }), []);
<Child style={style} />

// BEST: Just use className
<Child className="text-red-500" />
```

**Key Prop Strategy:**
- Use stable, unique IDs from data (never array index for reorderable lists)
- Reset component state by changing key: `<Form key={formId} />`

### Concurrent React Features

**useTransition** — For non-urgent state updates:

```tsx
function SearchPage() {
  const [query, setQuery] = useState('');
  const [isPending, startTransition] = useTransition();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Urgent: update input immediately
    setQuery(e.target.value);
    // Non-urgent: filter results can wait
    startTransition(() => {
      setFilteredResults(filterBy(e.target.value));
    });
  };

  return (
    <div>
      <input
        value={query}
        onChange={handleChange}
        className="px-4 py-3 rounded-lg border transition-all duration-200 focus-visible:ring-2 focus-visible:ring-offset-2"
      />
      {isPending && <Spinner />}
      <ResultsList results={filteredResults} />
    </div>
  );
}
```

**useDeferredValue** — Defer expensive renders:

```tsx
function SearchResults({ query }: { query: string }) {
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;

  return (
    <div style={{ opacity: isStale ? 0.7 : 1, transition: 'opacity 200ms' }}>
      <SlowList query={deferredQuery} />
    </div>
  );
}
```

### Error Boundaries

Always wrap major sections in error boundaries:

```tsx
class ErrorBoundary extends Component<
  { fallback: ReactNode; children: ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('ErrorBoundary caught:', error, info);
  }

  render() {
    if (this.state.hasError) return this.props.fallback;
    return this.props.children;
  }
}
```

## Best Practices

1. **Composition over configuration** — Build small, focused components and compose them rather than adding props for every variation.
2. **Lift state only as high as necessary** — Keep state as close to where it is used as possible.
3. **Prefer controlled components** — Uncontrolled components (refs) only for integration with non-React libraries or performance-critical inputs.
4. **Type events properly** — Use `React.ChangeEvent<HTMLInputElement>` not `any`.
5. **Avoid prop drilling beyond 2 levels** — Use context or composition (children/render slots) instead.
6. **Use Suspense boundaries** — Wrap async data sources and lazy components in `<Suspense>`.
7. **Clean up all effects** — Every subscription, timer, or listener must have a cleanup function.
8. **Avoid `useEffect` for derived state** — Compute during render or use `useMemo`.
9. **Do not call setState in render** — This causes infinite loops. Derive values instead.
10. **Use `key` to reset component state** — Changing key unmounts/remounts, resetting all internal state.

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Stale closures in effects | Callback references old state | Add dependencies to array or use `useRef` for latest value |
| Object/array in dependency array | Effect runs every render | `useMemo` the value or compare individual fields |
| Forgetting cleanup | Memory leaks, zombie subscriptions | Return cleanup function from `useEffect` |
| Conditional hooks | Breaks hook ordering | Always call all hooks, guard logic inside |
| Setting state in render | Infinite loop | Derive the value or move to effect |
| Over-using context | Unnecessary re-renders on unrelated changes | Split contexts by update frequency or use selectors (Zustand) |
| Index as key in dynamic lists | Incorrect DOM reuse on reorder/delete | Use stable unique IDs |
| Fetching in useEffect without abort | Race conditions on fast navigation | Use `AbortController` or a data library (TanStack Query) |

## React 19+ Patterns

**`use()` hook** — Read promises and context in render:

```tsx
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise); // suspends until resolved
  return <div>{user.name}</div>;
}
```

**`useActionState`** — For form actions with pending state:

```tsx
function LoginForm() {
  const [state, formAction, isPending] = useActionState(loginAction, null);
  return (
    <form action={formAction}>
      <input name="email" className="px-4 py-3 rounded-lg border" />
      <button
        type="submit"
        disabled={isPending}
        className="px-6 py-4 text-base rounded-lg bg-blue-600 text-white transition-all duration-200 hover:bg-blue-700 focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50"
      >
        {isPending ? 'Signing in...' : 'Sign In'}
      </button>
      {state?.error && <p className="text-red-600 text-sm">{state.error}</p>}
    </form>
  );
}
```

**`useOptimistic`** — Optimistic UI updates:

```tsx
function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimistic] = useOptimistic(
    todos,
    (current, newTodo: Todo) => [...current, newTodo]
  );

  async function handleAdd(formData: FormData) {
    const newTodo = { id: crypto.randomUUID(), text: formData.get('text') as string };
    addOptimistic(newTodo);
    await saveTodo(newTodo);
  }

  return (
    <form action={handleAdd}>
      {optimisticTodos.map(t => <TodoItem key={t.id} todo={t} />)}
    </form>
  );
}
```


---

## From `component-patterns`

> React component patterns — compound components, render props, HOCs, headless components, polymorphic components

# React Component Patterns

## Purpose

Design flexible, reusable React components using established patterns — compound components for composable APIs, headless components for logic-only reuse, polymorphic components for element flexibility, and render props for rendering control. Each pattern solves a specific API design problem.

## Key Patterns

### Pattern Selection Guide

| Pattern | Use When | Example |
|---------|----------|---------|
| Compound Components | Building composable UI primitives with shared state | Tabs, Accordion, Menu, Select |
| Headless Components | Reusing logic without prescribing UI | useCombobox, useDialog, useTable |
| Polymorphic Components | Element type should be consumer-controlled | Button as `<a>`, Card as `<article>` |
| Render Props | Consumer controls what renders based on internal state | Virtualized list item rendering |
| HOCs | Cross-cutting concerns (rare in modern React) | withAuth, withTheme (prefer hooks) |
| Slot Pattern | Named content areas within a layout component | PageLayout with header/sidebar/main |

### Compound Components

**Context-based compound component:**

```tsx
import { createContext, useContext, useState, useCallback, type ReactNode } from 'react';

// 1. Create typed context
interface AccordionContextValue {
  openItems: Set<string>;
  toggle: (id: string) => void;
}

const AccordionContext = createContext<AccordionContextValue | null>(null);

function useAccordionContext() {
  const ctx = useContext(AccordionContext);
  if (!ctx) throw new Error('Accordion.* must be used within <Accordion>');
  return ctx;
}

// 2. Root component owns state
interface AccordionProps {
  children: ReactNode;
  type?: 'single' | 'multiple';
  defaultOpen?: string[];
}

function Accordion({ children, type = 'single', defaultOpen = [] }: AccordionProps) {
  const [openItems, setOpenItems] = useState<Set<string>>(new Set(defaultOpen));

  const toggle = useCallback((id: string) => {
    setOpenItems((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        if (type === 'single') next.clear();
        next.add(id);
      }
      return next;
    });
  }, [type]);

  return (
    <AccordionContext.Provider value={{ openItems, toggle }}>
      <div className="divide-y divide-gray-200 rounded-xl border shadow-sm">
        {children}
      </div>
    </AccordionContext.Provider>
  );
}

// 3. Child components consume context
interface AccordionItemProps {
  id: string;
  children: ReactNode;
}

function AccordionItem({ id, children }: AccordionItemProps) {
  return <div data-accordion-item={id}>{children}</div>;
}

function AccordionTrigger({ id, children }: { id: string; children: ReactNode }) {
  const { openItems, toggle } = useAccordionContext();
  const isOpen = openItems.has(id);

  return (
    <button
      onClick={() => toggle(id)}
      aria-expanded={isOpen}
      aria-controls={`accordion-panel-${id}`}
      className="flex w-full items-center justify-between px-6 py-4 text-base font-medium transition-all duration-200 hover:bg-gray-50 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
    >
      {children}
      <ChevronIcon className={`w-4 h-4 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
    </button>
  );
}

function AccordionContent({ id, children }: { id: string; children: ReactNode }) {
  const { openItems } = useAccordionContext();
  const isOpen = openItems.has(id);

  if (!isOpen) return null;

  return (
    <div id={`accordion-panel-${id}`} role="region" className="px-6 py-4 text-base">
      {children}
    </div>
  );
}

// 4. Attach sub-components
Accordion.Item = AccordionItem;
Accordion.Trigger = AccordionTrigger;
Accordion.Content = AccordionContent;

// Usage:
// <Accordion type="single" defaultOpen={["faq-1"]}>
//   <Accordion.Item id="faq-1">
//     <Accordion.Trigger id="faq-1">What is this?</Accordion.Trigger>
//     <Accordion.Content id="faq-1">An accordion component.</Accordion.Content>
//   </Accordion.Item>
// </Accordion>
```

### Headless Components (Hooks)

**Headless combobox:**

```tsx
import { useState, useCallback, useRef, useMemo } from 'react';

interface UseComboboxProps<T> {
  items: T[];
  itemToString: (item: T) => string;
  onSelect: (item: T) => void;
  filter?: (item: T, query: string) => boolean;
}

interface UseComboboxReturn<T> {
  query: string;
  setQuery: (q: string) => void;
  filteredItems: T[];
  isOpen: boolean;
  highlightedIndex: number;
  getInputProps: () => React.InputHTMLAttributes<HTMLInputElement>;
  getListProps: () => React.HTMLAttributes<HTMLUListElement>;
  getItemProps: (index: number) => React.LiHTMLAttributes<HTMLLIElement>;
}

function useCombobox<T>({
  items,
  itemToString,
  onSelect,
  filter,
}: UseComboboxProps<T>): UseComboboxReturn<T> {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const listRef = useRef<HTMLUListElement>(null);

  const defaultFilter = useCallback(
    (item: T, q: string) => itemToString(item).toLowerCase().includes(q.toLowerCase()),
    [itemToString]
  );

  const filterFn = filter ?? defaultFilter;
  const filteredItems = useMemo(
    () => (query ? items.filter((item) => filterFn(item, query)) : items),
    [items, query, filterFn]
  );

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          setHighlightedIndex((i) => Math.min(i + 1, filteredItems.length - 1));
          setIsOpen(true);
          break;
        case 'ArrowUp':
          e.preventDefault();
          setHighlightedIndex((i) => Math.max(i - 1, 0));
          break;
        case 'Enter':
          if (highlightedIndex >= 0 && filteredItems[highlightedIndex]) {
            onSelect(filteredItems[highlightedIndex]);
            setQuery(itemToString(filteredItems[highlightedIndex]));
            setIsOpen(false);
          }
          break;
        case 'Escape':
          setIsOpen(false);
          break;
      }
    },
    [filteredItems, highlightedIndex, onSelect, itemToString]
  );

  return {
    query,
    setQuery,
    filteredItems,
    isOpen,
    highlightedIndex,
    getInputProps: () => ({
      value: query,
      onChange: (e: React.ChangeEvent<HTMLInputElement>) => {
        setQuery(e.target.value);
        setIsOpen(true);
        setHighlightedIndex(-1);
      },
      onFocus: () => setIsOpen(true),
      onBlur: () => setTimeout(() => setIsOpen(false), 200),
      onKeyDown: handleKeyDown,
      role: 'combobox',
      'aria-expanded': isOpen,
      'aria-autocomplete': 'list' as const,
      'aria-activedescendant':
        highlightedIndex >= 0 ? `combobox-item-${highlightedIndex}` : undefined,
    }),
    getListProps: () => ({
      ref: listRef,
      role: 'listbox',
    }),
    getItemProps: (index: number) => ({
      id: `combobox-item-${index}`,
      role: 'option',
      'aria-selected': index === highlightedIndex,
      onClick: () => {
        onSelect(filteredItems[index]);
        setQuery(itemToString(filteredItems[index]));
        setIsOpen(false);
      },
      onMouseEnter: () => setHighlightedIndex(index),
    }),
  };
}

// Consumer provides all UI — hook provides all logic
function CityPicker({ cities }: { cities: City[] }) {
  const combobox = useCombobox({
    items: cities,
    itemToString: (city) => city.name,
    onSelect: (city) => console.log('Selected:', city),
  });

  return (
    <div className="relative">
      <input
        {...combobox.getInputProps()}
        className="w-full px-4 py-3 rounded-lg border transition-all duration-200 focus-visible:ring-2 focus-visible:ring-offset-2"
        placeholder="Search cities..."
      />
      {combobox.isOpen && combobox.filteredItems.length > 0 && (
        <ul
          {...combobox.getListProps()}
          className="absolute z-10 mt-1 w-full rounded-xl border bg-white shadow-sm"
        >
          {combobox.filteredItems.map((city, index) => (
            <li
              key={city.id}
              {...combobox.getItemProps(index)}
              className={`px-4 py-3 cursor-pointer transition-all duration-200 ${
                index === combobox.highlightedIndex ? 'bg-blue-50' : ''
              }`}
            >
              {city.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### Polymorphic Components

**Type-safe `as` prop:**

```tsx
import { type ElementType, type ComponentPropsWithoutRef } from 'react';

// Generic type that resolves props based on the `as` element
type PolymorphicProps<E extends ElementType, Props = {}> = Props &
  Omit<ComponentPropsWithoutRef<E>, keyof Props | 'as'> & {
    as?: E;
  };

// Polymorphic Button that can render as <button>, <a>, or any element
type ButtonOwnProps = {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
};

type ButtonProps<E extends ElementType = 'button'> = PolymorphicProps<E, ButtonOwnProps>;

const sizeClasses = {
  sm: 'px-4 py-2 text-sm rounded-lg',
  md: 'px-6 py-4 text-base rounded-lg',
  lg: 'px-8 py-5 text-lg rounded-lg',
};

const variantClasses = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700',
  secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
  ghost: 'bg-transparent text-gray-700 hover:bg-gray-100',
};

function Button<E extends ElementType = 'button'>({
  as,
  variant = 'primary',
  size = 'md',
  className,
  ...props
}: ButtonProps<E>) {
  const Component = as ?? 'button';

  return (
    <Component
      className={`inline-flex items-center justify-center font-medium transition-all duration-200 focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500 ${sizeClasses[size]} ${variantClasses[variant]} ${className ?? ''}`}
      {...props}
    />
  );
}

// Usage — TypeScript enforces correct props for each element
// <Button onClick={handleClick}>Click me</Button>           // button props
// <Button as="a" href="/home">Go home</Button>              // anchor props
// <Button as={Link} to="/dashboard">Dashboard</Button>      // Link props
```

### Render Props

```tsx
// Render prop for controlled rendering of list items
interface VirtualListProps<T> {
  items: T[];
  itemHeight: number;
  containerHeight: number;
  renderItem: (item: T, index: number, style: React.CSSProperties) => ReactNode;
}

function VirtualList<T>({ items, itemHeight, containerHeight, renderItem }: VirtualListProps<T>) {
  const [scrollTop, setScrollTop] = useState(0);

  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(startIndex + Math.ceil(containerHeight / itemHeight) + 1, items.length);
  const visibleItems = items.slice(startIndex, endIndex);

  return (
    <div
      style={{ height: containerHeight, overflow: 'auto' }}
      onScroll={(e) => setScrollTop(e.currentTarget.scrollTop)}
      className="rounded-xl border shadow-sm"
    >
      <div style={{ height: items.length * itemHeight, position: 'relative' }}>
        {visibleItems.map((item, i) =>
          renderItem(item, startIndex + i, {
            position: 'absolute',
            top: (startIndex + i) * itemHeight,
            height: itemHeight,
            width: '100%',
          })
        )}
      </div>
    </div>
  );
}
```

### Slot Pattern

```tsx
// Named slots for layout components
interface PageLayoutProps {
  header?: ReactNode;
  sidebar?: ReactNode;
  children: ReactNode;
  footer?: ReactNode;
}

function PageLayout({ header, sidebar, children, footer }: PageLayoutProps) {
  return (
    <div className="min-h-screen flex flex-col">
      {header && (
        <header className="sticky top-0 z-50 border-b bg-white px-6 py-4">
          {header}
        </header>
      )}
      <div className="flex flex-1">
        {sidebar && (
          <aside className="w-64 border-r p-6 hidden lg:block">
            {sidebar}
          </aside>
        )}
        <main className="flex-1 py-16 px-6">{children}</main>
      </div>
      {footer && (
        <footer className="border-t px-6 py-4">{footer}</footer>
      )}
    </div>
  );
}
```

### Controlled vs Uncontrolled Pattern

```tsx
// Component supports both controlled and uncontrolled usage
interface ToggleProps {
  defaultPressed?: boolean;  // Uncontrolled
  pressed?: boolean;         // Controlled
  onPressedChange?: (pressed: boolean) => void;
  children: ReactNode;
}

function Toggle({ defaultPressed, pressed: controlledPressed, onPressedChange, children }: ToggleProps) {
  const [uncontrolledPressed, setUncontrolledPressed] = useState(defaultPressed ?? false);
  const isControlled = controlledPressed !== undefined;
  const pressed = isControlled ? controlledPressed : uncontrolledPressed;

  const handleToggle = useCallback(() => {
    const next = !pressed;
    if (!isControlled) setUncontrolledPressed(next);
    onPressedChange?.(next);
  }, [pressed, isControlled, onPressedChange]);

  return (
    <button
      role="switch"
      aria-checked={pressed}
      onClick={handleToggle}
      className={`px-6 py-4 text-base rounded-lg transition-all duration-200 focus-visible:ring-2 focus-visible:ring-offset-2 ${
        pressed ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-900'
      }`}
    >
      {children}
    </button>
  );
}

// Uncontrolled: <Toggle defaultPressed={false}>Dark mode</Toggle>
// Controlled:   <Toggle pressed={isDark} onPressedChange={setIsDark}>Dark mode</Toggle>
```

## Best Practices

1. **Compound components for public APIs** — When building a component library, compound components give consumers maximum flexibility without prop explosion.
2. **Hooks over HOCs** — Prefer custom hooks for logic reuse. HOCs add wrapper layers and make debugging harder.
3. **Headless for design system foundations** — Build headless hooks first (logic + a11y), then wrap with styled components. This separates concerns cleanly.
4. **Support controlled and uncontrolled** — Components like inputs, toggles, and accordions should work both ways.
5. **Use context validation** — Throw descriptive errors when sub-components are used outside their parent context.
6. **Keep render props for rendering control only** — If you are just sharing logic (no rendering control needed), use a hook instead.
7. **Type polymorphic components strictly** — Use generics so TypeScript enforces correct props for each `as` element type.
8. **Prefer composition over configuration** — `<Card><Card.Header /><Card.Body /></Card>` beats `<Card header={...} body={...} />`.

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Prop explosion | Component has 20+ props for every variation | Split into compound components with named sub-components |
| Context without validation | Cryptic error when sub-component used outside provider | Throw descriptive error in `useContext` wrapper |
| HOC wrapping order | Multiple HOCs create confusing wrapper chains | Replace with hooks: `const auth = useAuth(); const theme = useTheme();` |
| Polymorphic without generics | `as="a"` allows button props, not anchor props | Use generic `PolymorphicProps<E>` type for correct prop inference |
| Render prop callback identity | New function on every render triggers child re-renders | Memoize render prop callbacks or accept stable component references |
| Headless without ARIA | Logic reused but accessibility missing | Include ARIA attributes in `getProps` return values |
| Uncontrolled to controlled switch | React warns about changing from uncontrolled to controlled | Decide mode once based on initial props; document clearly |
| Over-abstraction | Pattern used where a simple component suffices | Use patterns only when the flexibility is actually needed |


---

## From `typescript-frontend`

> TypeScript for frontend development — generics, utility types, type-safe APIs, component typing, and developer experience patterns

# TypeScript for Frontend Development

## Purpose

Provide expert guidance on TypeScript patterns specific to frontend development — component typing, generic patterns, discriminated unions, type-safe APIs, schema validation inference, and patterns that maximize developer experience (DX) through autocompletion and compile-time safety.

## Key Patterns

### Component Prop Typing

**Basic component with proper HTML attribute forwarding:**

```tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export function Button({
  variant = 'primary',
  size = 'md',
  isLoading,
  children,
  disabled,
  className,
  ...props // forwards onClick, aria-*, data-*, etc.
}: ButtonProps) {
  return (
    <button
      disabled={disabled || isLoading}
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    >
      {isLoading ? <Spinner /> : children}
    </button>
  );
}
```

**Polymorphic `as` prop:**

```tsx
type PolymorphicProps<E extends React.ElementType, P = {}> = P &
  Omit<React.ComponentPropsWithoutRef<E>, keyof P> & {
    as?: E;
  };

type TextProps<E extends React.ElementType = 'p'> = PolymorphicProps<E, {
  size?: 'sm' | 'base' | 'lg' | 'xl';
  weight?: 'normal' | 'medium' | 'bold';
}>;

export function Text<E extends React.ElementType = 'p'>({
  as,
  size = 'base',
  weight = 'normal',
  className,
  ...props
}: TextProps<E>) {
  const Component = as || 'p';
  return <Component className={cn(textVariants({ size, weight }), className)} {...props} />;
}

// Usage: fully typed, href only available when as="a"
<Text as="a" href="/about" size="lg">About Us</Text>
<Text as="h1" size="xl" weight="bold">Title</Text>
```

**Children typing patterns:**

```tsx
// Accepts any renderable content
type CardProps = {
  children: React.ReactNode;
};

// Accepts only a single element (for cloneElement patterns)
type SlotProps = {
  children: React.ReactElement;
};

// Render prop pattern
type DataListProps<T> = {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
};

// Function as children
type AnimateProps = {
  children: (styles: { opacity: number; scale: number }) => React.ReactNode;
};
```

### Discriminated Unions

**For component variants with different props:**

```tsx
// Each variant has unique required props
type NotificationProps =
  | { type: 'success'; message: string }
  | { type: 'error'; message: string; retry: () => void }
  | { type: 'loading'; progress: number }
  | { type: 'info'; message: string; action?: { label: string; onClick: () => void } };

function Notification(props: NotificationProps) {
  switch (props.type) {
    case 'success':
      return <div className="text-green-600">{props.message}</div>;
    case 'error':
      return (
        <div className="text-red-600">
          {props.message}
          <button onClick={props.retry}>Retry</button> {/* type-safe: retry exists */}
        </div>
      );
    case 'loading':
      return <ProgressBar value={props.progress} />; {/* type-safe: progress exists */}
    case 'info':
      return <div>{props.message}</div>;
  }
}
```

**For API responses:**

```tsx
type ApiResponse<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error; retryCount: number };

function useApiData<T>(fetcher: () => Promise<T>): ApiResponse<T> {
  // Implementation...
}

// Usage: TypeScript narrows automatically
const result = useApiData(fetchUser);
if (result.status === 'success') {
  console.log(result.data); // T is accessible
}
if (result.status === 'error') {
  console.log(result.error.message); // Error is accessible
}
```

### Generic Patterns

**Generic data table:**

```tsx
type Column<T> = {
  key: keyof T & string;
  header: string;
  render?: (value: T[keyof T], row: T) => React.ReactNode;
  sortable?: boolean;
};

type DataTableProps<T extends { id: string | number }> = {
  data: T[];
  columns: Column<T>[];
  onRowClick?: (row: T) => void;
  emptyMessage?: string;
};

function DataTable<T extends { id: string | number }>({
  data,
  columns,
  onRowClick,
  emptyMessage = 'No data found',
}: DataTableProps<T>) {
  // Column keys are type-safe against T
  return (
    <table>
      <thead>
        <tr>
          {columns.map(col => (
            <th key={col.key}>{col.header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map(row => (
          <tr key={row.id} onClick={() => onRowClick?.(row)}>
            {columns.map(col => (
              <td key={col.key}>
                {col.render ? col.render(row[col.key], row) : String(row[col.key])}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Usage: columns are type-checked against User
type User = { id: string; name: string; email: string; role: 'admin' | 'user' };

<DataTable<User>
  data={users}
  columns={[
    { key: 'name', header: 'Name', sortable: true },
    { key: 'email', header: 'Email' },
    { key: 'role', header: 'Role', render: (val) => <Badge>{val}</Badge> },
    // { key: 'age', header: 'Age' }, // ERROR: 'age' not in keyof User
  ]}
/>
```

**Generic select component:**

```tsx
type SelectOption<V extends string | number = string> = {
  value: V;
  label: string;
  disabled?: boolean;
};

type SelectProps<V extends string | number = string> = {
  options: SelectOption<V>[];
  value: V;
  onChange: (value: V) => void;
  placeholder?: string;
};

function Select<V extends string | number>({ options, value, onChange }: SelectProps<V>) {
  // onChange callback is type-safe — receives V, not string
}

// Usage
type Status = 'active' | 'inactive' | 'pending';
const [status, setStatus] = useState<Status>('active');

<Select<Status>
  options={[
    { value: 'active', label: 'Active' },
    { value: 'inactive', label: 'Inactive' },
    { value: 'pending', label: 'Pending' },
  ]}
  value={status}
  onChange={setStatus} // type-safe: (value: Status) => void
/>
```

### `satisfies` Operator

Use `satisfies` for type checking while preserving narrow literal types:

```tsx
// Routes configuration with type checking AND narrow types
const routes = {
  home: '/',
  dashboard: '/dashboard',
  settings: '/dashboard/settings',
  profile: '/profile/:id',
} satisfies Record<string, string>;

// routes.home is typed as '/' not string
// Enables autocomplete on route values

// Theme tokens
const colors = {
  brand: { 500: '#3b82f6', 600: '#2563eb' },
  success: { 500: '#22c55e', 600: '#16a34a' },
  danger: { 500: '#ef4444', 600: '#dc2626' },
} satisfies Record<string, Record<number, string>>;

// colors.brand[500] is '#3b82f6' not string
```

### `as const` for Literal Types

```tsx
// Define constant arrays and objects with narrowed types
const ROLES = ['admin', 'editor', 'viewer'] as const;
type Role = (typeof ROLES)[number]; // 'admin' | 'editor' | 'viewer'

// Useful for form options
const STATUS_OPTIONS = [
  { value: 'draft', label: 'Draft', icon: 'pencil' },
  { value: 'published', label: 'Published', icon: 'globe' },
  { value: 'archived', label: 'Archived', icon: 'archive' },
] as const;

type StatusValue = (typeof STATUS_OPTIONS)[number]['value'];
// 'draft' | 'published' | 'archived'
```

### Zod Schema Inference

```tsx
import { z } from 'zod';

// Define schema once, derive TypeScript type
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(100),
  email: z.string().email(),
  role: z.enum(['admin', 'editor', 'viewer']),
  preferences: z.object({
    theme: z.enum(['light', 'dark', 'system']).default('system'),
    notifications: z.boolean().default(true),
  }),
  createdAt: z.coerce.date(),
});

// Inferred type matches the schema exactly
type User = z.infer<typeof UserSchema>;

// Partial schema for updates
const UpdateUserSchema = UserSchema.pick({
  name: true,
  email: true,
  preferences: true,
}).partial();

type UpdateUser = z.infer<typeof UpdateUserSchema>;

// Form schema with refinements
const SignupSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});
```

### Type-Safe API Client

```tsx
// Define API contract
type ApiRoutes = {
  'GET /users': { response: User[]; params: { role?: Role } };
  'GET /users/:id': { response: User; params: { id: string } };
  'POST /users': { response: User; body: CreateUserInput };
  'PUT /users/:id': { response: User; body: UpdateUserInput; params: { id: string } };
  'DELETE /users/:id': { response: void; params: { id: string } };
};

// Type-safe fetch wrapper
type Method = 'GET' | 'POST' | 'PUT' | 'DELETE';

type RouteKey<M extends Method> = Extract<keyof ApiRoutes, `${M} ${string}`>;

async function api<M extends Method, R extends RouteKey<M>>(
  route: R,
  options?: ApiRoutes[R] extends { body: infer B } ? { body: B } : never
): Promise<ApiRoutes[R]['response']> {
  const [method, path] = (route as string).split(' ');
  const res = await fetch(path, {
    method,
    body: options && 'body' in options ? JSON.stringify(options.body) : undefined,
    headers: { 'Content-Type': 'application/json' },
  });
  return res.json();
}
```

### Event Handler Typing

```tsx
// Prefer specific event types
function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  const value = e.target.value; // string, type-safe
}

function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
  e.preventDefault();
  const formData = new FormData(e.currentTarget);
}

function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
  if (e.key === 'Enter') submit();
}

// For custom event callbacks
type OnSelect<T> = (item: T, event: React.MouseEvent) => void;
```

### Utility Types for Frontend

```tsx
// Make specific fields required
type WithRequired<T, K extends keyof T> = T & Required<Pick<T, K>>;
type UserWithEmail = WithRequired<Partial<User>, 'email'>;

// Make specific fields optional
type WithOptional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// Extract props from a component
type ButtonProps = React.ComponentPropsWithoutRef<typeof Button>;

// Strict omit (errors if key doesn't exist)
type StrictOmit<T, K extends keyof T> = Omit<T, K>;

// Non-nullable nested type
type DeepRequired<T> = {
  [K in keyof T]-?: T[K] extends object ? DeepRequired<T[K]> : NonNullable<T[K]>;
};
```

## Best Practices

1. **Infer over annotate** — Let TypeScript infer return types, state types, and callback types when they are obvious.
2. **Use discriminated unions** — For component variants, API states, and any branching logic.
3. **`satisfies` over `as`** — `satisfies` checks without widening; `as` silences errors.
4. **Schema-first typing** — Define Zod schemas and infer types; single source of truth.
5. **Avoid `any`** — Use `unknown` and narrow, or use generics. `any` defeats the purpose.
6. **Avoid `enum`** — Use `as const` arrays or union types. Enums have runtime overhead and quirks.
7. **Use `React.ComponentPropsWithoutRef`** — Not `React.HTMLAttributes` for proper HTML forwarding.
8. **Generic constraints** — Always constrain generics: `<T extends Record<string, unknown>>` not `<T>`.
9. **`readonly` arrays in props** — Accept `readonly T[]` to work with both mutable and immutable arrays.
10. **Strict mode always** — Enable `strict: true` in tsconfig. Non-negotiable.

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| `as` for type assertions | Hides bugs, bypasses checking | Use `satisfies`, type guards, or Zod parsing |
| `any` in event handlers | Loses all type safety | Use `React.ChangeEvent<HTMLInputElement>` etc. |
| Enum for options | Runtime overhead, poor tree-shaking | `as const` arrays with `typeof` inference |
| `Object` or `{}` types | Too wide, accepts anything | Use `Record<string, unknown>` or specific shapes |
| Missing `null` checks | Runtime errors on optional data | Enable `strictNullChecks`, use optional chaining |
| Overtyping | Complex types that obscure intent | Simpler unions, let inference work |
| Not using `readonly` | Props can be accidentally mutated | `readonly` on array/object props |
| `!` non-null assertion | Bypasses null safety | Handle null case explicitly |
| Union type in props without discriminant | Can't narrow which variant | Add a `type` or `kind` discriminant field |
| Ignoring `strict` tsconfig | Allows `any` to leak in | `strict: true` plus `noUncheckedIndexedAccess` |


---

## From `typescript-patterns`

> Advanced TypeScript patterns including branded types, discriminated unions, builder pattern, and type-level programming

# TypeScript Advanced Patterns

## Purpose

Provide expert guidance on advanced TypeScript type system patterns that enforce correctness at compile time. Covers branded/nominal types for domain primitives, discriminated unions for exhaustive state modeling, the builder pattern for type-safe fluent APIs, and type-level programming with conditional, mapped, and template literal types.

## Key Patterns

### Branded Types

Use branded types to create nominal distinctions between structurally identical types, preventing accidental misuse of primitive values.

```typescript
// Define a brand symbol for each domain primitive
declare const __brand: unique symbol;

type Brand<T, B extends string> = T & { readonly [__brand]: B };

// Domain primitives
type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;
type Email = Brand<string, "Email">;
type PositiveInt = Brand<number, "PositiveInt">;

// Smart constructors with runtime validation
function UserId(value: string): UserId {
  if (!value.match(/^usr_[a-z0-9]{12}$/)) {
    throw new Error(`Invalid UserId: ${value}`);
  }
  return value as UserId;
}

function Email(value: string): Email {
  if (!value.includes("@")) {
    throw new Error(`Invalid Email: ${value}`);
  }
  return value as Email;
}

function PositiveInt(value: number): PositiveInt {
  if (!Number.isInteger(value) || value <= 0) {
    throw new Error(`Invalid PositiveInt: ${value}`);
  }
  return value as PositiveInt;
}

// Compile-time safety: cannot mix branded types
function getUser(id: UserId): Promise<User> { /* ... */ }
function getOrder(id: OrderId): Promise<Order> { /* ... */ }

const userId = UserId("usr_abc123def456");
const orderId = OrderId("ord_xyz789ghi012");

getUser(userId);   // OK
getUser(orderId);  // Compile error: OrderId is not assignable to UserId
```

### Discriminated Unions

Model exhaustive state machines where the compiler ensures every variant is handled.

```typescript
// State machine for async data fetching
type AsyncState<T, E = Error> =
  | { status: "idle" }
  | { status: "loading"; startedAt: number }
  | { status: "success"; data: T; fetchedAt: number }
  | { status: "error"; error: E; retriesLeft: number };

// Exhaustive pattern matching helper
function assertNever(value: never): never {
  throw new Error(`Unhandled variant: ${JSON.stringify(value)}`);
}

function renderState<T>(state: AsyncState<T>): string {
  switch (state.status) {
    case "idle":
      return "Ready to load";
    case "loading":
      return `Loading since ${state.startedAt}`;
    case "success":
      return `Got ${JSON.stringify(state.data)}`;
    case "error":
      return `Error: ${state.error.message} (${state.retriesLeft} retries left)`;
    default:
      return assertNever(state); // Compile error if a variant is missed
  }
}

// Domain events as discriminated unions
type DomainEvent =
  | { type: "ORDER_PLACED"; orderId: string; items: Item[]; total: number }
  | { type: "ORDER_SHIPPED"; orderId: string; trackingNumber: string }
  | { type: "ORDER_CANCELLED"; orderId: string; reason: string }
  | { type: "REFUND_ISSUED"; orderId: string; amount: number };

// Extract a specific event type
type OrderPlacedEvent = Extract<DomainEvent, { type: "ORDER_PLACED" }>;
```

### Builder Pattern

Type-safe builder that tracks which fields have been set at the type level.

```typescript
// Track required fields at the type level
type BuilderState = {
  hasHost: boolean;
  hasPort: boolean;
  hasDatabase: boolean;
};

type ConnectionConfig = {
  host: string;
  port: number;
  database: string;
  ssl?: boolean;
  poolSize?: number;
};

class ConnectionBuilder<S extends BuilderState = {
  hasHost: false;
  hasPort: false;
  hasDatabase: false;
}> {
  private config: Partial<ConnectionConfig> = {};

  host(value: string): ConnectionBuilder<S & { hasHost: true }> {
    this.config.host = value;
    return this as any;
  }

  port(value: number): ConnectionBuilder<S & { hasPort: true }> {
    this.config.port = value;
    return this as any;
  }

  database(value: string): ConnectionBuilder<S & { hasDatabase: true }> {
    this.config.database = value;
    return this as any;
  }

  ssl(value: boolean): ConnectionBuilder<S> {
    this.config.ssl = value;
    return this;
  }

  poolSize(value: number): ConnectionBuilder<S> {
    this.config.poolSize = value;
    return this;
  }

  // build() is only available when all required fields are set
  build(
    this: ConnectionBuilder<{ hasHost: true; hasPort: true; hasDatabase: true }>
  ): ConnectionConfig {
    return this.config as ConnectionConfig;
  }
}

// Usage
const config = new ConnectionBuilder()
  .host("localhost")
  .port(5432)
  .database("myapp")
  .ssl(true)
  .build(); // OK: all required fields set

const bad = new ConnectionBuilder()
  .host("localhost")
  .build(); // Compile error: port and database missing
```

### Type-Level Programming

Conditional types, mapped types, and template literal types for compile-time computation.

```typescript
// Deep readonly that works on nested objects
type DeepReadonly<T> = T extends (infer U)[]
  ? ReadonlyArray<DeepReadonly<U>>
  : T extends object
    ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
    : T;

// Path type for deep object access: "user.address.city"
type PathKeys<T, Prefix extends string = ""> = T extends object
  ? {
      [K in keyof T & string]: K | `${K}.${PathKeys<T[K], `${Prefix}${K}.`>}`;
    }[keyof T & string]
  : never;

type User = {
  name: string;
  address: { city: string; zip: string };
  tags: string[];
};

type UserPaths = PathKeys<User>;
// "name" | "address" | "address.city" | "address.zip" | "tags"

// Template literal types for route parameters
type ExtractParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractParams<Rest>
    : T extends `${string}:${infer Param}`
      ? Param
      : never;

type RouteParams = ExtractParams<"/users/:userId/posts/:postId">;
// "userId" | "postId"

// Mapped type for API response wrappers
type ApiResponse<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
} & {
  [K in keyof T as `set${Capitalize<string & K>}`]: (value: T[K]) => void;
};
```

## Best Practices

- **Prefer branded types over plain primitives** for domain values (IDs, emails, currencies) to catch misuse at compile time rather than runtime.
- **Use discriminated unions over class hierarchies** for modeling finite state -- they compose better with pattern matching and type narrowing.
- **Always include an `assertNever` default case** in switch statements over discriminated unions to catch missing variants after refactoring.
- **Keep type-level computation shallow** -- deeply recursive conditional types slow down the compiler and produce unreadable error messages.
- **Pair branded types with Zod schemas** for runtime validation at system boundaries, keeping the brand as the internal representation.

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Casting directly to branded type | Bypasses validation, defeats the purpose | Always use a smart constructor function that validates |
| Missing `assertNever` in switches | Adding new union variants compiles silently | Add `default: return assertNever(x)` to every discriminated union switch |
| Overly deep recursive types | `Type instantiation is excessively deep` errors, IDE slowdowns | Limit recursion depth with a counter type parameter or flatten the structure |
| Builder returning `this` without type narrowing | `build()` is always callable even when required fields are missing | Use generic state tracking with conditional `this` parameter on `build()` |
| Template literal union explosion | Combining large unions via template literals creates thousands of types | Keep input unions small or use branded string types instead |
| Forgetting `as const` on literal objects | TypeScript widens `"loading"` to `string`, breaking discrimination | Use `as const` or explicit type annotations on discriminant values |


---

## From `state-management`

> Client-side state management with Zustand, Jotai, Redux Toolkit, and URL state patterns

# State Management Skill

## Purpose

Select and implement the right state management approach for React applications. This skill covers Zustand for simple-to-medium apps, Jotai for atomic state, Redux Toolkit for large-scale apps, and URL/server state patterns. The key insight: most apps need less state management than developers think.

## Key Concepts

### State Categories

```
SERVER STATE (fetched from API):
  Use: TanStack Query, SWR, or Next.js server components
  NOT Zustand/Redux. Server state belongs in a cache, not a store.

CLIENT STATE (UI interactions):
  Local:  useState, useReducer (component-scoped)
  Shared: Zustand, Jotai (cross-component)
  Global: Redux Toolkit (large-scale, complex flows)

URL STATE (route parameters, search params):
  Use: nuqs, next/navigation, URLSearchParams
  Filters, pagination, sort order belong in the URL, not in a store.

FORM STATE:
  Use: React Hook Form, useActionState
  Form data belongs in the form library, not in a store.

DECISION TREE:
  Is it server data?    -> TanStack Query / SWR / RSC
  Is it in the URL?     -> URL params (nuqs, searchParams)
  Is it form data?      -> React Hook Form
  Is it local UI state? -> useState / useReducer
  Is it shared UI state? -> Zustand (simple) or Jotai (atomic)
  Is it complex with many actions? -> Redux Toolkit
```

### Library Comparison

```
ZUSTAND:
  Mental model: Top-down store (like Redux, but simpler)
  Bundle size: ~1KB
  Best for: Shared UI state, simple to medium apps
  API: create store -> useStore hook

JOTAI:
  Mental model: Bottom-up atoms (like Recoil, but simpler)
  Bundle size: ~2KB
  Best for: Independent pieces of state, derived state
  API: atom() -> useAtom()

REDUX TOOLKIT:
  Mental model: Centralized store with slices
  Bundle size: ~10KB
  Best for: Large apps, complex state machines, middleware
  API: createSlice -> configureStore -> useSelector/useDispatch

URL STATE (nuqs):
  Mental model: State in the URL, synced with React
  Bundle size: ~2KB
  Best for: Filters, search, pagination, shareable state
  API: useQueryState()
```

## Patterns

### Zustand Store

```typescript
// stores/cart-store.ts
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  // Actions
  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
  // Computed
  totalItems: () => number;
  totalPrice: () => number;
}

export const useCartStore = create<CartState>()(
  devtools(
    persist(
      immer((set, get) => ({
        items: [],

        addItem: (item) =>
          set((state) => {
            const existing = state.items.find((i) => i.id === item.id);
            if (existing) {
              existing.quantity += 1;
            } else {
              state.items.push({ ...item, quantity: 1 });
            }
          }),

        removeItem: (id) =>
          set((state) => {
            state.items = state.items.filter((i) => i.id !== id);
          }),

        updateQuantity: (id, quantity) =>
          set((state) => {
            const item = state.items.find((i) => i.id === id);
            if (item) {
              item.quantity = Math.max(0, quantity);
              if (item.quantity === 0) {
                state.items = state.items.filter((i) => i.id !== id);
              }
            }
          }),

        clearCart: () => set({ items: [] }),

        totalItems: () => get().items.reduce((sum, i) => sum + i.quantity, 0),
        totalPrice: () => get().items.reduce((sum, i) => sum + i.price * i.quantity, 0),
      })),
      { name: 'cart-storage' }
    ),
    { name: 'CartStore' }
  )
);

// Usage in components -- subscribe to specific slices to avoid re-renders
function CartBadge() {
  const totalItems = useCartStore((s) => s.totalItems());
  return <span>{totalItems}</span>;
}

function CartPage() {
  const items = useCartStore((s) => s.items);
  const removeItem = useCartStore((s) => s.removeItem);
  // ...
}
```

### Jotai Atoms

```typescript
// atoms/theme.ts
import { atom, useAtom, useAtomValue, useSetAtom } from 'jotai';
import { atomWithStorage } from 'jotai/utils';

// Primitive atom (stored in localStorage)
export const themeAtom = atomWithStorage<'light' | 'dark' | 'system'>('theme', 'system');

// Derived atom (computed from other atoms)
export const resolvedThemeAtom = atom((get) => {
  const theme = get(themeAtom);
  if (theme !== 'system') return theme;
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
});

// Async atom (fetches data)
export const userAtom = atom(async () => {
  const res = await fetch('/api/me');
  return res.json();
});

// Write-only atom (action)
export const toggleThemeAtom = atom(null, (get, set) => {
  const current = get(themeAtom);
  set(themeAtom, current === 'dark' ? 'light' : 'dark');
});

// Usage
function ThemeToggle() {
  const theme = useAtomValue(themeAtom);
  const toggle = useSetAtom(toggleThemeAtom);
  return <button onClick={toggle}>{theme}</button>;
}
```

### URL State with nuqs

```typescript
// For filters, search, pagination -- state belongs in the URL
import { useQueryState, parseAsInteger, parseAsString } from 'nuqs';

function ProductList() {
  const [search, setSearch] = useQueryState('q', parseAsString.withDefault(''));
  const [page, setPage] = useQueryState('page', parseAsInteger.withDefault(1));
  const [sort, setSort] = useQueryState('sort', parseAsString.withDefault('newest'));

  // URL: /products?q=shoes&page=2&sort=price
  // State is shareable, bookmarkable, and survives refreshes
}
```

## Best Practices

1. **Start with server state** -- most "state management" problems are actually data fetching problems
2. **Use the URL for shareable state** -- filters, search, pagination belong in URL params
3. **Keep stores small** -- one store per domain concern, not one mega-store
4. **Subscribe to slices** -- `useStore(s => s.field)` prevents unnecessary re-renders
5. **Derive, do not duplicate** -- computed values should be derived from base state, not stored separately
6. **Colocate state** -- start with local state; lift to shared only when needed
7. **Type your stores** -- define interfaces for state shape and actions
8. **Use middleware sparingly** -- devtools in development, persist for specific stores
9. **Avoid state for server data** -- use TanStack Query or SWR for API data
10. **Test stores in isolation** -- Zustand stores can be tested without rendering components

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Storing server data in Zustand | Stale data, no cache invalidation | Use TanStack Query or SWR |
| One mega-store | Everything re-renders on any change | Split into domain-specific stores |
| Not selecting slices | Component re-renders on unrelated changes | `useStore(s => s.specificField)` |
| Duplicating derived state | Out of sync, extra updates | Use computed getters or derived atoms |
| URL state in a store | Not shareable, lost on refresh | Use URL params (nuqs) |
| Over-engineering | useState would have sufficed | Start simple, upgrade only when needed |


---

## From `zustand`

> Minimal React state management — create stores, selectors, persist middleware, useShallow, slices pattern

# Zustand

> Minimal, un-opinionated state management for React with no boilerplate.

## When to Use
- Client-side state shared across components
- Replacing useState/useContext for global state
- Simple alternative to Redux when you don't need middleware/devtools complexity

## Core Patterns

### Store Definition
```typescript
import { create } from "zustand";
import { persist, devtools } from "zustand/middleware";

interface AppStore {
  count: number;
  user: User | null;
  increment: () => void;
  setUser: (user: User) => void;
  reset: () => void;
}

const useAppStore = create<AppStore>()(
  devtools(
    persist(
      (set, get) => ({
        count: 0,
        user: null,
        increment: () => set((s) => ({ count: s.count + 1 })),
        setUser: (user) => set({ user }),
        reset: () => set({ count: 0, user: null }),
      }),
      { name: "app-store" } // localStorage key
    )
  )
);
```

### Usage in Components
```typescript
// Select specific slices to avoid unnecessary re-renders
const count = useAppStore((s) => s.count);
const increment = useAppStore((s) => s.increment);

// Shallow comparison for object slices
import { useShallow } from "zustand/react/shallow";
const { user, setUser } = useAppStore(useShallow((s) => ({ user: s.user, setUser: s.setUser })));
```

### Key Conventions
- **Selectors**: Always select specific slices, never `useStore()` without selector
- **useShallow**: Use for multi-property selections to prevent re-renders
- **Middleware**: `persist` (localStorage), `devtools` (Redux DevTools), `immer` (mutable updates)
- **Slices pattern**: Split large stores into slices combined with `...createSlice()`
- **No providers**: Zustand stores work without React context wrappers
- **Async actions**: Just use async/await inside actions, call `set()` when ready
- **Subscriptions**: `useAppStore.subscribe((state) => ...)` for side effects outside React


---

## From `jotai`

> Jotai atomic state management for React — primitive atoms, derived atoms, async atoms, atom families, and Suspense integration

# Jotai

- **Layer**: domain
- **Category**: state-management
- **Risk Level**: low
- **Triggers**: jotai, atom, useAtom, atomFamily, atomic state

## Overview

Jotai is a primitive and flexible state management library for React that takes an atomic approach.
State is built from the bottom up using individual atoms — minimal units of state that compose together.
No boilerplate, no string keys, full TypeScript inference, and React Suspense support out of the box.

## When to Use

- You need fine-grained reactivity without re-rendering entire subtrees
- State is naturally composed from small independent pieces
- You want derived/computed state that auto-updates
- You need async state that integrates with React Suspense
- You want a lightweight alternative to Redux or Zustand with less boilerplate
- You need parameterized state (atom families)

## Key Patterns

### Atom Creation

- `atom(initialValue)` — primitive atom (read-write)
- `atomWithStorage(key, initialValue)` — persisted to localStorage/sessionStorage (`jotai/utils`)
- `atomWithDefault(getDefault)` — resettable atom with a dynamic default

### Derived Atoms

- **Read-only**: `atom((get) => get(baseAtom) * 2)` — computed from other atoms
- **Write-only**: `atom(null, (get, set, update) => { set(baseAtom, update) })` — actions/setters
- **Read-write**: `atom((get) => get(a) + get(b), (get, set, val) => { set(a, val) })` — both

### Async Atoms

- Async read: `atom(async (get) => await fetch(...))` — suspends until resolved
- `loadable(asyncAtom)` — wraps async atom to avoid Suspense (`{ state, data, error }`)
- `atomWithQuery` (via `jotai-tanstack-query`) — integrates with TanStack Query

### Atom Families

- `atomFamily((param) => atom(param))` — creates parameterized atoms keyed by argument
- Use for lists, entity maps, or any state indexed by ID
- Call `atomFamily.remove(param)` to clean up unused atoms

### Provider Scoping

- **Provider-less mode**: atoms use a default store — simplest setup, works globally
- **`<Provider>`**: creates an isolated atom scope — useful for tests or subtree isolation
- `createStore()` + `<Provider store={store}>` for explicit store control

### DevTools & Debugging

- `jotai-devtools`: provides `<DevTools />` component and Redux DevTools integration
- `useAtomsDebugValue()` for inspecting all atom values in React DevTools
- Label atoms with `myAtom.debugLabel = 'myAtom'` for readable debug output

### Suspense Integration

- Async atoms suspend by default — wrap consumers in `<Suspense>`
- Use `loadable()` wrapper to opt out of Suspense per atom
- Pair with `<ErrorBoundary>` for async error handling

## Anti-Patterns

- **Giant atoms**: storing large objects in a single atom defeats fine-grained reactivity — split them
- **Atom creation in render**: never call `atom()` inside a component — define atoms at module scope
- **Ignoring cleanup in families**: `atomFamily` caches forever unless you call `.remove()`
- **Overusing providers**: provider-less mode is fine for most apps — add `<Provider>` only when scoping is needed
- **Skipping `loadable`**: if a component cannot show a fallback, wrap the async atom in `loadable()`

## Related Skills

- `react` — core rendering library
- `state-management` — general state patterns and selection guide
- `typescript-frontend` — type-safe frontend patterns
- `zustand` — alternative state management (store-based vs atomic)


---

## From `swr`

> React hooks for data fetching with stale-while-revalidate — useSWR, useSWRMutation, useSWRInfinite, optimistic updates

# SWR

layer: domain | category: data-fetching | riskLevel: low
triggers: ["swr", "stale-while-revalidate", "useSWR", "data fetching hook"]

## Overview

React hooks library for data fetching using the stale-while-revalidate HTTP cache strategy. Returns cached (stale) data first, then fetches (revalidates), and finally delivers fresh data. Built-in caching, deduplication, revalidation, and focus tracking.

## When to Use

- Client-side data fetching in React/Next.js apps
- Real-time or near-real-time data that benefits from cache-first rendering
- Paginated or infinite scroll lists
- Replacing manual `useEffect` + `useState` fetch patterns

## Key Patterns

### Basic Usage
```ts
const { data, error, isLoading, mutate } = useSWR('/api/user', fetcher)
```

### Remote Mutations
```ts
const { trigger, isMutating } = useSWRMutation('/api/user', updateUser)
```

### Infinite Scroll / Pagination
```ts
const { data, size, setSize } = useSWRInfinite(
  (index) => `/api/items?page=${index + 1}`, fetcher
)
```

### Global Configuration
```tsx
<SWRConfig value={{ fetcher, revalidateOnFocus: true, dedupingInterval: 2000 }}>
  <App />
</SWRConfig>
```

### Conditional Fetching — pass `null` key to skip
```ts
const { data } = useSWR(userId ? `/api/user/${userId}` : null, fetcher)
```

### Optimistic Updates
```ts
mutate('/api/todos', async (todos) => {
  return [...todos, newTodo]
}, { optimisticData: [...currentTodos, newTodo], rollbackOnError: true })
```

### Revalidation Strategies
- `revalidateOnFocus` — refetch on window focus (default: true)
- `refreshInterval` — polling interval in ms
- `revalidateOnReconnect` — refetch on network recovery

### Error Retry
```ts
useSWR(key, fetcher, { onErrorRetry: (err, key, config, revalidate, { retryCount }) => {
  if (retryCount >= 3) return
  setTimeout(() => revalidate({ retryCount }), 5000)
}})
```

### Cache Provider & Persistence
```tsx
<SWRConfig value={{ provider: () => new Map() }}> {/* or localStorage-backed */}
```

### Middleware
```ts
const logger = (useSWRNext) => (key, fetcher, config) => {
  const swr = useSWRNext(key, fetcher, config)
  useEffect(() => { console.log(key, swr.data) }, [swr.data])
  return swr
}
```

## Anti-Patterns

- Fetching inside `useEffect` when SWR handles it — duplicates requests
- Using mutable objects as keys — causes infinite revalidation loops
- Ignoring `isLoading` vs `isValidating` — they indicate different states
- Calling `mutate()` without a key — always scope mutations to a specific key
- Nesting `SWRConfig` without intent — inner config merges with outer

## Related Skills

react, nextjs, typescript-frontend, tanstack


---

## From `tanstack-query`

> TanStack Query (React Query) — data fetching, caching, mutations, optimistic updates, infinite scrolling, and prefetching

# TanStack Query (React Query) Patterns

## Purpose

Provide expert guidance on TanStack Query v5 for React, including data fetching, caching strategies, mutations with optimistic updates, infinite queries, prefetching, SSR hydration with Next.js, and production-grade patterns.

## Core Patterns

### 1. Provider Setup

```tsx
// providers/query-provider.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,        // 1 minute before refetch
            gcTime: 5 * 60 * 1000,       // 5 minutes in cache after unmount
            retry: 2,
            refetchOnWindowFocus: false,  // Disable for less aggressive refetching
          },
          mutations: {
            retry: 1,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {process.env.NODE_ENV === 'development' && (
        <ReactQueryDevtools initialIsOpen={false} />
      )}
    </QueryClientProvider>
  );
}
```

### 2. Query Keys Factory

```typescript
// lib/query-keys.ts
export const queryKeys = {
  // Posts
  posts: {
    all: ['posts'] as const,
    lists: () => [...queryKeys.posts.all, 'list'] as const,
    list: (filters: PostFilters) => [...queryKeys.posts.lists(), filters] as const,
    details: () => [...queryKeys.posts.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.posts.details(), id] as const,
    infinite: (filters?: PostFilters) => [...queryKeys.posts.all, 'infinite', filters] as const,
  },

  // Users
  users: {
    all: ['users'] as const,
    detail: (id: string) => [...queryKeys.users.all, id] as const,
    me: () => [...queryKeys.users.all, 'me'] as const,
  },

  // Comments
  comments: {
    all: ['comments'] as const,
    byPost: (postId: string) => [...queryKeys.comments.all, 'post', postId] as const,
  },
} as const;
```

### 3. Basic Queries with Type Safety

```typescript
// hooks/use-posts.ts
import { useQuery, useSuspenseQuery } from '@tanstack/react-query';
import { queryKeys } from '@/lib/query-keys';

interface Post {
  id: string;
  title: string;
  content: string;
  author: { id: string; name: string };
  createdAt: string;
}

interface PostFilters {
  search?: string;
  category?: string;
  page?: number;
}

async function fetchPosts(filters: PostFilters): Promise<{ posts: Post[]; total: number }> {
  const params = new URLSearchParams();
  if (filters.search) params.set('search', filters.search);
  if (filters.category) params.set('category', filters.category);
  if (filters.page) params.set('page', String(filters.page));

  const res = await fetch(`/api/posts?${params}`);
  if (!res.ok) throw new Error('Failed to fetch posts');
  return res.json();
}

// Standard query hook
export function usePosts(filters: PostFilters = {}) {
  return useQuery({
    queryKey: queryKeys.posts.list(filters),
    queryFn: () => fetchPosts(filters),
    placeholderData: (previousData) => previousData, // Keep previous data while fetching
  });
}

// Suspense query hook (for use with React Suspense)
export function usePostsSuspense(filters: PostFilters = {}) {
  return useSuspenseQuery({
    queryKey: queryKeys.posts.list(filters),
    queryFn: () => fetchPosts(filters),
  });
}

// Single post query
export function usePost(id: string) {
  return useQuery({
    queryKey: queryKeys.posts.detail(id),
    queryFn: async () => {
      const res = await fetch(`/api/posts/${id}`);
      if (!res.ok) throw new Error('Post not found');
      return res.json() as Promise<Post>;
    },
    enabled: !!id, // Only fetch when id is truthy
  });
}
```

### 4. Mutations with Optimistic Updates

```typescript
// hooks/use-create-post.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { queryKeys } from '@/lib/query-keys';

interface CreatePostInput {
  title: string;
  content: string;
  categoryId?: string;
}

export function useCreatePost() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (input: CreatePostInput) => {
      const res = await fetch('/api/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(input),
      });
      if (!res.ok) throw new Error('Failed to create post');
      return res.json() as Promise<Post>;
    },
    onSuccess: () => {
      // Invalidate all post lists so they refetch
      queryClient.invalidateQueries({ queryKey: queryKeys.posts.lists() });
    },
  });
}

// Optimistic update for toggling a like
export function useToggleLike(postId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      const res = await fetch(`/api/posts/${postId}/like`, { method: 'POST' });
      if (!res.ok) throw new Error('Failed to toggle like');
      return res.json();
    },
    onMutate: async () => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: queryKeys.posts.detail(postId) });

      // Snapshot previous value
      const previousPost = queryClient.getQueryData<Post>(queryKeys.posts.detail(postId));

      // Optimistically update
      queryClient.setQueryData<Post>(queryKeys.posts.detail(postId), (old) => {
        if (!old) return old;
        return {
          ...old,
          isLiked: !old.isLiked,
          likeCount: old.isLiked ? old.likeCount - 1 : old.likeCount + 1,
        };
      });

      return { previousPost };
    },
    onError: (_err, _vars, context) => {
      // Rollback on error
      if (context?.previousPost) {
        queryClient.setQueryData(queryKeys.posts.detail(postId), context.previousPost);
      }
    },
    onSettled: () => {
      // Refetch to ensure consistency
      queryClient.invalidateQueries({ queryKey: queryKeys.posts.detail(postId) });
    },
  });
}

// Delete with optimistic removal from list
export function useDeletePost() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (postId: string) => {
      const res = await fetch(`/api/posts/${postId}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Failed to delete post');
    },
    onMutate: async (postId) => {
      await queryClient.cancelQueries({ queryKey: queryKeys.posts.lists() });

      // Remove from all cached lists
      queryClient.setQueriesData<{ posts: Post[]; total: number }>(
        { queryKey: queryKeys.posts.lists() },
        (old) => {
          if (!old) return old;
          return {
            ...old,
            posts: old.posts.filter((p) => p.id !== postId),
            total: old.total - 1,
          };
        }
      );
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.posts.lists() });
    },
  });
}
```

### 5. Infinite Queries (Infinite Scroll)

```typescript
// hooks/use-infinite-posts.ts
import { useInfiniteQuery } from '@tanstack/react-query';
import { queryKeys } from '@/lib/query-keys';

interface PostsPage {
  posts: Post[];
  nextCursor: string | null;
  hasMore: boolean;
}

export function useInfinitePosts(filters?: PostFilters) {
  return useInfiniteQuery({
    queryKey: queryKeys.posts.infinite(filters),
    queryFn: async ({ pageParam }) => {
      const params = new URLSearchParams();
      if (pageParam) params.set('cursor', pageParam);
      if (filters?.search) params.set('search', filters.search);

      const res = await fetch(`/api/posts?${params}`);
      if (!res.ok) throw new Error('Failed to fetch posts');
      return res.json() as Promise<PostsPage>;
    },
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (lastPage) => lastPage.nextCursor ?? undefined,
  });
}
```

```tsx
// components/infinite-post-list.tsx
'use client';

import { useInfinitePosts } from '@/hooks/use-infinite-posts';
import { useInView } from 'react-intersection-observer';
import { useEffect } from 'react';

export function InfinitePostList() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage, status } =
    useInfinitePosts();

  const { ref, inView } = useInView({ threshold: 0 });

  useEffect(() => {
    if (inView && hasNextPage && !isFetchingNextPage) {
      fetchNextPage();
    }
  }, [inView, hasNextPage, isFetchingNextPage, fetchNextPage]);

  if (status === 'pending') return <PostListSkeleton />;
  if (status === 'error') return <ErrorMessage />;

  const allPosts = data.pages.flatMap((page) => page.posts);

  return (
    <div className="space-y-4">
      {allPosts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}

      {/* Sentinel element for infinite scroll */}
      <div ref={ref} className="h-10">
        {isFetchingNextPage && (
          <div className="flex justify-center py-4">
            <Spinner />
          </div>
        )}
      </div>

      {!hasNextPage && allPosts.length > 0 && (
        <p className="text-center text-text-secondary py-4">
          No more posts to load.
        </p>
      )}
    </div>
  );
}
```

### 6. Prefetching & SSR with Next.js

```tsx
// app/posts/page.tsx (Server Component)
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query';
import { queryKeys } from '@/lib/query-keys';
import { PostList } from '@/components/post-list';

export default async function PostsPage() {
  const queryClient = new QueryClient();

  await queryClient.prefetchQuery({
    queryKey: queryKeys.posts.list({}),
    queryFn: () => fetchPosts({}), // Direct fetch, no browser API needed
  });

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <PostList />
    </HydrationBoundary>
  );
}
```

```tsx
// Prefetch on hover for instant navigation
'use client';

import { useQueryClient } from '@tanstack/react-query';
import { queryKeys } from '@/lib/query-keys';
import Link from 'next/link';

export function PostLink({ post }: { post: Post }) {
  const queryClient = useQueryClient();

  const prefetch = () => {
    queryClient.prefetchQuery({
      queryKey: queryKeys.posts.detail(post.id),
      queryFn: () => fetch(`/api/posts/${post.id}`).then((r) => r.json()),
      staleTime: 30 * 1000, // Don't refetch if prefetched within 30s
    });
  };

  return (
    <Link
      href={`/posts/${post.id}`}
      onMouseEnter={prefetch}
      onFocus={prefetch}
      className="text-brand-600 hover:underline transition-all duration-200"
    >
      {post.title}
    </Link>
  );
}
```

### 7. Dependent Queries

```typescript
// Fetch user, then fetch their posts
export function useUserPosts(userId?: string) {
  const userQuery = useQuery({
    queryKey: queryKeys.users.detail(userId!),
    queryFn: () => fetchUser(userId!),
    enabled: !!userId,
  });

  const postsQuery = useQuery({
    queryKey: queryKeys.posts.list({ authorId: userId }),
    queryFn: () => fetchPosts({ authorId: userId }),
    enabled: !!userQuery.data, // Only fetch when user is loaded
  });

  return { user: userQuery, posts: postsQuery };
}
```

### 8. Typed API Client Helper

```typescript
// lib/api-client.ts
class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

export async function apiClient<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ message: 'Request failed' }));
    throw new ApiError(res.status, error.message);
  }

  return res.json();
}

// Usage in query hooks
export function usePosts(filters: PostFilters) {
  return useQuery({
    queryKey: queryKeys.posts.list(filters),
    queryFn: () => apiClient<{ posts: Post[]; total: number }>(`/posts?${buildParams(filters)}`),
  });
}
```

## Best Practices

1. **Use a query key factory** -- centralize all keys in one file for consistency and easy invalidation.
2. **Set `staleTime` globally** -- default `0` causes unnecessary refetches; 60s is a good starting point.
3. **Use `placeholderData`** for paginated queries to keep previous data visible during refetch.
4. **Invalidate broadly, fetch narrowly** -- invalidate at the list level, but queries only refetch if mounted.
5. **Use `useSuspenseQuery`** with React Suspense boundaries for cleaner loading states.
6. **Prefetch on hover/focus** for detail pages to make navigation feel instant.
7. **Always roll back optimistic updates** in `onError` with the snapshot from `onMutate`.
8. **Use `onSettled`** (not just `onSuccess`) to invalidate, ensuring consistency even after errors.
9. **Separate query functions from hooks** -- makes them testable and reusable for SSR prefetching.
10. **Use `gcTime` (not `cacheTime`)** -- renamed in v5; controls how long inactive data stays in memory.

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Inline query keys `['posts', id]` | Typos, inconsistent invalidation | Use a query key factory |
| `staleTime: 0` (default) everywhere | Excessive refetching, bandwidth waste | Set reasonable global `staleTime` |
| Fetching in `useEffect` + `useState` | Loses caching, dedup, background refetch | Use `useQuery` instead |
| Calling `queryClient.fetchQuery` in components | Bypasses React lifecycle, no auto-refetch | Use `useQuery` or `usePrefetchQuery` |
| Not handling error states | Blank screen on failure | Check `isError` or use error boundaries |
| Optimistic update without rollback | UI stuck in wrong state after API error | Always implement `onError` rollback |
| Over-invalidating with `queryKey: ['posts']` | Refetches every posts query variant | Invalidate specific sub-keys when possible |
| `refetchOnWindowFocus: true` for mutation-heavy UIs | Constant refetching disrupts user flow | Disable per-query or globally for write-heavy apps |

## Decision Guide

| Scenario | Approach |
|----------|----------|
| Simple data fetch | `useQuery` with typed fetcher |
| Server-rendered page | Prefetch in Server Component + `HydrationBoundary` |
| Infinite scroll / load more | `useInfiniteQuery` with cursor pagination |
| Form submission | `useMutation` with `onSuccess` invalidation |
| Like/toggle action | `useMutation` with optimistic update + rollback |
| Dependent data (A then B) | Chain queries with `enabled: !!parentData` |
| Real-time data | `refetchInterval: 5000` or combine with WebSocket invalidation |
| Search with debounce | Debounce input state, pass to `useQuery` queryKey |
| Prefetch next page | `queryClient.prefetchQuery` on hover or in `getNextPageParam` |

