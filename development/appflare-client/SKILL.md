---
name: appflare-client
description: Use the Appflare generated client in frontends, including creating new Appflare() with endpoint, wsEndpoint and bearer-token storage, calling appflare.queries/appflare.mutations with .run() and { data, error }, the React and React Native hooks useQuery, useInfiniteQuery and useMutation from appflare/react with TanStack Query, typed optimistic updates and cache writes (optimistic, updateCache, useAppflareCache), persisting the query cache to localStorage or AsyncStorage for local-first loading, realtime subscriptions, Better Auth sign-up and sign-in through appflare.auth, and uploads through appflare.storage. Use when wiring a web or mobile app to an Appflare backend, fetching or mutating data from UI code, making the UI update instantly before the server answers, caching data offline, adding live updates, or implementing login.
metadata:
  author: appflare
  version: "0.4.0"
---

# Appflare client

## Workflow

- [ ] Find the generated client: `<backend package>/_generated/client`, or `dist/_generated/client` when the backend builds with `tsc`
- [ ] Create **one** shared client module (e.g. `lib/appflare.ts`)
- [ ] Wrap the React tree in `AppflareQueryProvider` (or TanStack's `QueryClientProvider`)
- [ ] Call routes through `appflare.queries.*` and `appflare.mutations.*`. Names mirror handler file paths
- [ ] After backend changes, run `bun appflare dev` in the backend so the client types update

## Shared client

```ts
// lib/appflare.ts
import { Appflare } from "my-backend/_generated/client";

export const appflare = new Appflare({
	endpoint: import.meta.env.VITE_API_URL,          // e.g. http://localhost:8787
	wsEndpoint: import.meta.env.VITE_API_WS_URL,     // e.g. ws://localhost:8787 (needed for realtime)
	onGetAuthToken: () => localStorage.getItem("appflare-token") ?? "",
	onSetAuthToken: (token) => localStorage.setItem("appflare-token", token),
});
```

For React Native, store the token with AsyncStorage or SecureStore. On the Android emulator, use `http://10.0.2.2:8787` instead of localhost.

## Plain calls

```ts
const { data, error } = await appflare.queries.tasks.listTasks.run({ projectId, limit: 20 });
if (error) throw new Error(`${error.status} ${error.message}`);

await appflare.mutations.tasks.completeTask.run({ id: 42 });
```

## React

```tsx
// App root: cache persisted across reloads, shown before the network answers
import { AppflareQueryProvider, createAppflareQueryClient } from "appflare/react";

const queryClient = createAppflareQueryClient();

<AppflareQueryProvider client={queryClient} persist={{ storage: localStorage }}>
	<App />
</AppflareQueryProvider>;
```

```tsx
import { useMutation, useQuery } from "appflare/react";
import { appflare } from "../lib/appflare";

const listTasks = appflare.queries.tasks.listTasks;

export function Tasks({ projectId }: { projectId: string }) {
	const tasks = useQuery(listTasks, { projectId }, {
		realtime: { enabled: true },
	});
	const complete = useMutation(appflare.mutations.tasks.completeTask, {
		// Typed from the routes; rolled back automatically if the mutation fails.
		optimistic: ({ id }, cache) =>
			cache.update(listTasks, (list) =>
				list.map((t) => (t.id === id ? { ...t, done: true } : t)),
			),
	});

	if (tasks.isLoading) return <p>Loading…</p>;
	if (tasks.error) return <p>{tasks.error.message}</p>;
	return tasks.data?.map((t) => (
		<button key={t.id} onClick={() => complete.mutate({ id: t.id })}>{t.title}</button>
	));
}
```

Optimistic and cache rules:

- `optimistic(args, cache)` runs before the request. Its writes survive refetches and realtime pushes while pending, roll back on error, and the touched queries refetch once it settles (`reconcile: false` to skip).
- `updateCache(result, args, cache)` writes the server response; `invalidates: [route]` refetches routes after success.
- `useAppflareCache()` gives the same typed `cache` anywhere: `get`, `set`, `update`, `getInfinite`, `updateInfinite`, `updatePages`, `invalidate`, `optimistic`.
- `cache.update(route, updater)` changes every cached args variant; `cache.update(route, args, updater)` only one. Use `updatePages` / `updateInfinite` for `useInfiniteQuery` data.
- Persistence saves server data only, never pending optimistic writes. Bump `persist.buster` when cached data shapes change.

## Auth

```ts
await appflare.auth.signUp.email({ email, password, name });
await appflare.auth.signIn.email({ email, password }); // token stored via onSetAuthToken
await appflare.auth.signOut();                         // then clear your stored token
```

The server needs Better Auth's `bearer()` plugin so responses include `set-auth-token`.

## Gotchas

- `run()` returns `{ data, error }` for HTTP failures and doesn't throw. It **does** throw a `ZodError` if the args fail the route schema on the client.
- Hooks throw `Error` objects that carry a `status` property, so use TanStack's `error` state.
- A `Date` returned by a handler arrives as an ISO **string**, even though the type says `Date`.
- Query args go in the URL, and the server converts them to the handler's arg types, so numbers, booleans, arrays and objects work without client-side tricks.
- A route whose handler takes no args (`args: {}`) is callable with no arguments: `route.run()` and `useQuery(route)`.
- Unhandled server errors return `{ message: "Internal error", requestId }`. Show `error.message` for expected failures (`ctx.error`) and log the `requestId` otherwise. Constraint failures carry a `code` such as `unique_violation` in `error.body`.
- Realtime needs `wsEndpoint`. `subscribe()` only pushes **changes**; hooks load initial data for you.
- `useInfiniteQuery` realtime pushes replace only the **first** page.
- `route.queryKey()` with no args matches all cached variants, which makes it a good key for invalidation.
- `clientOptions` in `appflare.config.ts` only types `appflare.auth`. Pass runtime Better Auth client plugins through `new Appflare({ authOptions: { plugins: [...] } })`.
- `appflare.storage.download()` expects JSON but the route streams bytes. Use `storage.preview({ path })` as a URL instead.

## References

- Read [references/react-hooks.md](references/react-hooks.md) when you need hook options (queryOptions, requestOptions, realtime callbacks), infinite pagination, the full optimistic/cache API, persistence options (AsyncStorage, `maxAge`, `buster`, `shouldPersist`), or client types such as `InferRouteInput`, `InferRouteOutput` and `InferQueryData`.
- Read [references/auth.md](references/auth.md) when implementing sign-in or sign-up, OTP or admin client plugins, token storage, role-aware UI, or storage uploads from the client.
