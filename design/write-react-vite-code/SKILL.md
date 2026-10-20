---
name: write-react-vite-code
description: >-
  Load this skill when writing React code in a Vite project: components, hooks, React Router, state,
  data fetching, Vite env vars. Auto-load when a .tsx file or vite.config.ts is created or modified.
disable-model-invocation: false
user-invocable: false
paths:
  - "**/*.tsx"
  - "**/vite.config.ts"
compatibility: >-
  Requires Node.js 20+ or `bun` on PATH, with `react`, `react-dom`, and `vite` installed as
  project dependencies and network access for the first install. None is assumed to be present
  globally; the dev server also needs a free local port.
license: Apache-2.0
---

# Write React + Vite Code

Write React components that render props, with effects and data fetching in hooks and every network
call going through one API client. Done when no component fetches directly and no secret reaches the
bundle.

## Procedure

1. Write the component presentational: props in, callbacks out, one component per file.
2. Put effects and data fetching in a `use*` hook that owns one concern.
3. Keep state local until it is genuinely shared across distant components.
4. Send every request through `apiClient`, and read config from `VITE_`-prefixed vars only.
5. Show errors through the central message map with the `correlation_id`, under an error boundary.

## Rules

### Components: presentational by default

Components render props and call callbacks. Side effects and data fetching live in hooks, not in render.

```tsx
type Props = {
  items: Item[];
  onItemClick: (id: string) => void; // callback, not a direct store write
};

export function ItemPanel({ items, onItemClick }: Props) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>
          <button onClick={() => onItemClick(item.id)}>{item.label}</button>
        </li>
      ))}
    </ul>
  );
}
```

- One component per file; filename `PascalCase.tsx` matching the component name.
- No business logic in components — extract it into hooks or `src/lib` modules.
- Always type props explicitly; never use `any` (see `ceh-web-frontend:configure-bun-vite-env`).

### Hooks

- Follow the Rules of Hooks: call hooks at the top level only, never conditionally.
- Custom hooks are named `use*` and own one concern (data fetching, subscription, derived state).
- Specify exhaustive `useEffect` dependency arrays — do not silence the lint rule.
- Prefer derived values computed during render over `useState` + `useEffect` mirrors.
- StrictMode mounts every component twice in development, so an effect that performs a one-time
  action (send a message, create a session, log an analytics event) fires twice. Make the action
  idempotent, or guard it with a `useRef(false)` flag set on the first run.

```tsx
export function useSession(sessionId: string) {
  const [state, setState] = useState<SessionState | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    apiClient
      .getSession(sessionId)
      .then((s) => active && setState(s))
      .catch((e) => active && setError(toMessage(e)));
    return () => {
      active = false;
    };
  }, [sessionId]);

  return { state, error };
}
```

### State management

- Local UI state: `useState` / `useReducer`.
- Shared server state: a data-fetching library (TanStack Query) or a small store — not prop drilling through many layers.
- Do not reach for a global store until state is genuinely shared across distant components.

### Render cost

A state change re-renders the owning component and its whole subtree, so where state lives decides
what re-renders.

- Keep state in the lowest component that needs it. State lifted to a page re-renders the page on
  every keystroke.
- Key list items by a stable id, never the array index, when the list can reorder, insert, or
  delete. An index key re-mounts rows and mixes up their local state.
- Every consumer of a context re-renders when its value changes. Pass a `useMemo`'d value, never an
  inline object, and split a context whose parts change at different rates.
- Define the config objects a library compares by reference (graph styles, grid column
  definitions, editor extensions) at module level. Created inside a component, a new object on
  every render makes the library tear down and remount its children.
- Reach for `memo`, `useMemo`, and `useCallback` only after the React DevTools Profiler shows a slow
  render. Unmeasured memoization adds code and dependency-array bugs for no gain.
- Render long lists (hundreds of rows) through a virtualizer, and load route components with
  `React.lazy` so a page's code ships when it is visited.

### Routing

Use **React Router**. Define routes in one place; keep route components thin (they compose hooks + presentational components).

```tsx
const router = createBrowserRouter([
  { path: "/", element: <Home /> },
  { path: "/sessions/:sessionId", element: <SessionPage /> },
]);
```

- Read route params with `useParams`, navigate with `useNavigate` — never mutate `window.location`.

### Centralized API client

All `fetch` calls go through `src/lib/api/client.ts`. Components and hooks never call `fetch` directly, so the base URL, headers, and error parsing live in one place and tests mock one boundary.

```ts
export const apiClient = {
  async sendMessage(
    sessionId: string,
    content: string,
  ): Promise<MessageResponse> {
    const response = await fetch(
      `${import.meta.env.VITE_API_BASE_URL}/sessions/${sessionId}/message`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content }),
      },
    );
    if (!response.ok) {
      const err = await response.json();
      throw new ApiRequestError(response.status, err.error);
    }
    return response.json();
  },
};
```

- Cookie auth against an API on another origin needs `credentials: "include"` on every request
  in the client. Without it the browser drops the cookie and every call fails auth.
- When a 401 triggers a token refresh, concurrent 401s share one in-flight refresh promise. Each
  refreshing on its own makes the second refresh fail on the already rotated token, which logs
  the user out.
- A streaming endpoint that needs POST or an auth header is read with `fetch` and a
  `ReadableStream` reader, because `EventSource` sends only GET and no custom headers.

### Environment variables

```ts
const apiBase = import.meta.env.VITE_API_BASE_URL; // exposed to the browser — VITE_ prefix required
```

- Only `VITE_`-prefixed vars are exposed to client code. Never put secrets in them.
- Server-only secrets belong in a backend, never in a Vite frontend bundle.

### Error handling

```tsx
class ApiRequestError extends Error {
  constructor(
    public readonly status: number,
    public readonly error: ApiError,
  ) {
    super(error.message);
  }
}
```

- Never expose internal error codes or stack traces to users.
- Map `error.code` values to user-friendly messages in a centralized map.
- Always surface the `correlation_id` so users can report it.
- Wrap route subtrees in an error boundary so one failure does not blank the app.
