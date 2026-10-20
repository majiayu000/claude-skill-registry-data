---
name: react-component
description: "World Pulse: When creating or modifying any React component in `src/renderer/`."
---

# React Component

**When to use:** When creating or modifying any React component in `src/renderer/`.

---

## Component Structure

Follow function-component convention with named exports:

```tsx
// Named export, not default
export function MyComponent({ prop }: { prop: string }) {
  // hooks at top
  // derived values with useMemo/useCallback
  // event handlers
  // render
  return <div className="ob-panel">{prop}</div>;
}
```

- No `React` import needed — the project uses the react-jsx transform.
- One component per file when possible; co-locate sub-components only if they are not reused elsewhere.

---

## Prop Typing

Always define props inline or with a named interface. Do not use `React.FC<Props>` — it has implicit children issues.

```tsx
interface EventCardProps {
  event: Event;          // from @shared/types
  isFeatured: boolean;
  onSelect: (event: Event) => void;
}

export function EventCard({ event, isFeatured, onSelect }: EventCardProps) { ... }
```

---

## Hooks Conventions

- Custom hooks live in `src/renderer/hooks/`.
- Custom hook names begin with `use`.
- Access Zustand store with selector functions to avoid over-rendering:

```tsx
// Good — only re-renders when `events` changes
const events = useAppStore((state) => state.events);

// Bad — re-renders on every store update
const store = useAppStore();
```

- `useEffect` dependency arrays must be exhaustive — ESLint enforces this.
- Side-effect cleanup (socket disconnect, timers) always goes in the `useEffect` return.

---

## State Management

Global state lives in `src/renderer/store/useAppStore.ts` (Zustand). Do not introduce local `useState` for data that other components need. Do not use React Context or Redux.

Mutations go through store actions, never by mutating slices directly:

```tsx
const setFeaturedEvent = useAppStore((state) => state.setFeaturedEvent);
setFeaturedEvent(event); // correct
```

---

## Tailwind Class Discipline

- Use Oblivion token classes (`bg-ob-bg-panel`, `text-ob-accent-cyan`) not Tailwind color palette classes.
- Keep class strings readable — use `clsx` or `cn` for conditional classes rather than ternary-in-className.
- Avoid arbitrary values (`w-[347px]`) — use spacing scale or add a new CSS variable.
- No inline `style` except for values that must be dynamic (e.g., computed pixel positions).

---

## Imports

Use path aliases, never relative paths that cross package boundaries:

```ts
import type { Event } from '@shared/types';  // correct
import type { Event } from '../../../shared/types'; // wrong
import { useAppStore } from '@renderer/store/useAppStore';
```

Defined aliases: `@/` → `src/`, `@shared/` → `src/shared/`, `@renderer/` → `src/renderer/`, `@server/` → `src/server/`.

---

## Anti-Patterns

- No `any` — use `unknown` with type narrowing, or a specific interface.
- No `console.log()` — only `console.warn()` and `console.error()` (ESLint `no-console` warning).
- No default exports in components — all exports are named.
- Do not import PropTypes — they are disabled in the ESLint config.
- Do not add error boundaries unless the component fetches external data; the top-level `ErrorBoundary` already exists.
