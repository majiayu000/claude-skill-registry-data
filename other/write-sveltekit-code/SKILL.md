---
name: write-sveltekit-code
description: >-
  Load this skill when adding or modifying SvelteKit routes, writing load functions, managing shared
  state with Svelte 5 runes, or building components. Auto-load whenever a +page.svelte,
  +page.server.ts, +page.ts, shared-state .svelte.ts module, or component file is created or
  modified.
disable-model-invocation: false
user-invocable: false
paths:
  - "**/*.svelte"
  - "**/*.svelte.ts"
  - "**/+page*.ts"
  - "**/+layout*.ts"
  - "**/+server.ts"
compatibility: >-
  Requires Node.js 20+ or `bun` on PATH, with `@sveltejs/kit`, `svelte`, and `vite` installed as
  project dependencies and network access for the first install. None is assumed to be present
  globally; the dev server also needs a free local port.
license: Apache-2.0
---

# Write SvelteKit Code

Write SvelteKit routes and components on Svelte 5 runes, with data loaded in `load` functions and
every network call going through one API client. Done when no component writes shared state directly
and no server code touches a shared-state module.

## Procedure

1. Pick the route file by where the load runs: `+page.server.ts` for credentials or DB, `+page.ts`
   otherwise.
2. Return data from `load` and throw `error()` or `redirect()` from `@sveltejs/kit`.
3. Keep shared state in a `.svelte.ts` module under `$lib/state/`, written from API responses only
   and only in the browser.
4. Pass components props and callbacks, and send every request through `apiClient`.
5. Show errors through the central message map with the `correlation_id`.

## Rules

### Route file naming

| File                | Purpose                                                                        |
| ------------------- | ------------------------------------------------------------------------------ |
| `+page.svelte`      | Page UI component                                                              |
| `+page.server.ts`   | Server-only load function and form actions (access to private env vars and DB) |
| `+page.ts`          | Universal load function (runs on server + client)                              |
| `+layout.svelte`    | Layout wrapper applied to child routes                                         |
| `+layout.server.ts` | Server-only layout load                                                        |
| `+error.svelte`     | Error page for this route segment                                              |

Use `+page.server.ts` when the load requires server-side credentials or direct database access.

### Load functions

```ts
export const load: PageServerLoad = async ({ params }) => {
  const session = await apiClient.getSession(params.session_id);
  if (!session) error(404, "Session not found"); // SvelteKit error(), not throw new Error()
  return { session };
};
```

- Throw `error()` from `@sveltejs/kit` for HTTP errors
- Use `redirect()` from `@sveltejs/kit` for redirects — do not call `goto()` inside load functions
- Load functions return data; they do not directly mutate state

### Shared state: runes in `.svelte.ts` modules

Svelte 5 is the standard: use runes, not `svelte/store` (`writable` / `derived`). Shared state lives
in one `.svelte.ts` module under `src/lib/state/`. It is updated **only** from API responses, through
the module's exported functions — never mutated directly by components, so the server stays the
source of truth and every change has one traceable writer.

**Browser-only.** Module-level state lives once per server process, so during server rendering it is
shared across every user's request and can leak one user's data to another. Never write a
shared-state module on the server. Per-user data on the server goes through `load` data or context
(`setContext` in a layout, `getContext` in components). Load functions stay pure and never set
shared state.

```ts
// src/lib/state/session.svelte.ts
import { browser } from "$app/environment";

// Reassigned $state cannot be exported, so export an object and mutate its property.
export const sessionState = $state<{ current: SessionState | null }>({
  current: null,
});

export function setSession(next: SessionState | null) {
  if (!browser) return; // never write per-user state on the server: the module is shared across requests
  sessionState.current = next;
}

// Derived state cannot be exported either, so export a function that computes it.
export function getOpenItems() {
  return sessionState.current?.items.filter((i) => i.status === "open") ?? [];
}
```

- Do not define shared state inside components — it lives in `$lib/state/`
- Call `getOpenItems()` inside a template or a `$derived` so the read stays reactive

### Components: props only, no direct state writes

```svelte
<script lang="ts">
  type Props = {
    items: Item[];
    onItemClick: (id: string) => void;  // callback, not a direct state write
  };
  let { items, onItemClick }: Props = $props();
</script>
```

### Centralized API client

All `fetch` calls go through `src/lib/api/client.ts`. Components and shared-state modules never call `fetch` directly, so the base URL, headers, and error parsing live in one place and tests mock one boundary.

```ts
export const apiClient = {
  async sendMessage(
    sessionId: string,
    content: string,
  ): Promise<MessageResponse> {
    const response = await fetch(
      `${PUBLIC_API_BASE_URL}/sessions/${sessionId}/message`,
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
import { PUBLIC_API_BASE_URL } from "$env/static/public"; // safe for browser
import { DATABASE_URL } from "$env/static/private"; // server-only
```

Never use `import.meta.env.VITE_*`: the `$env` modules enforce the public/private split at build
time, and `VITE_*` does not.

### Error handling

```ts
class ApiRequestError extends Error {
  constructor(
    public readonly status: number,
    public readonly error: ApiError,
  ) {
    super(error.message);
  }
}
```

Component pattern:

```svelte
<script lang="ts">
  let error = $state<string | null>(null);
  let loading = $state(false);

  async function handleSend() {
    error = null; loading = true;
    try {
      const result = await apiClient.sendMessage(sessionId, input);
      onSuccess(result.state);
    } catch (e) {
      error = e instanceof ApiRequestError
        ? e.error.message
        : 'An unexpected error occurred. Please try again.';
    } finally { loading = false; }
  }
</script>

{#if error}<p class="error">{error}</p>{/if}
```

- Never expose internal error codes or stack traces to users
- Map `error.code` values to user-friendly messages in a centralized map
- Always show the `correlation_id` so users can report it

### Derived values: `$derived` and `$derived.by`

```svelte
<script lang="ts">
  let { items }: { items: Item[] } = $props();
  const openCount = $derived(items.filter((i) => i.status === 'open').length);
</script>
```

Do not put complex logic in a `$derived` expression — use `$derived.by(() => { ... })` or extract a named function.
