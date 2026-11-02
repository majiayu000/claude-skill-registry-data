---
name: set-up-realtime
description: Use when adding live server-push updates to a frontend SPA - a WebSocket seam with backoff reconnect that writes validated pushed data into the TanStack Query cache and exposes connection status as UI state.
---

# Set Up Realtime

Live server→client updates, written into the Query cache through the same server/UI boundary the rest of the app uses. A realtime message carries *server data*, so it lands in the cache — never a store. The one new thing realtime adds is the connection *status*, which is UI state.

Scope: server→client push (live lists, dashboards, notification badges). Collaborative editing / presence / CRDT is out of scope — see `./realtime-patterns.md`.

## 1. Audit current state

```bash
grep -rnE "new WebSocket|EventSource|socket\.io|pusher|ably|@supabase.*realtime" src/ 2>/dev/null   # existing realtime to wrap
ls src/libs/realtime.ts src/stores/useRealtimeStatusStore.ts .claude/stack-profile.md 2>/dev/null
grep -n "lists:" src/libs/queryKeys.ts 2>/dev/null      # is the lists() factory accessor present?
grep -n "VITE_REALTIME_URL" src/libs/env.ts 2>/dev/null
```

Read `.claude/stack-profile.md` if present: `frontend.framework` decides the branch in step 3; `backend.track` of `supabase` means use Supabase Realtime behind the same seam (`realtime-patterns.md`, "When to deviate"); `package_manager` replaces `pnpm`.

**Prerequisites:** `set-up-state-management` (the `queryClient`, the `queryKeys` factory, the cache-as-truth boundary). Recommended: `set-up-auth` (the connection authenticates the same way the `fetcher` does) and `validate-env` (owns the `VITE_REALTIME_URL` read). Scattered `new WebSocket` / vendor calls in components are an audit finding — wrap them behind the seam (step 5).

## 2. Decide what to do
- No realtime → full setup (steps 4–7).
- Vendor SDK or raw `WebSocket` called from components → introduce the seam and route calls through it.
- Seam present but no reconnect/status handling → add the missing resilience (step 5).
- Everything present → confirm live data writes to the cache (not a store) and exit "Realtime already in place."

## 3. Detect framework
React → hook (`src/hooks/`) + Zustand status store. Vue → composable (`src/composables/`) + Pinia status store. The seam (`src/libs/realtime.ts`) is plain TS, identical for both.

## 4. Extend the env schema and the cache types

**Env (`validate-env` in place — preferred).** Add `VITE_REALTIME_URL` as **optional** (a `ws:`/`wss:` URL), so its absence disables realtime instead of failing the boot check:
```ts
// src/libs/env.ts — add to the schema object (blankToUndefined is defined at the top of that file)
VITE_REALTIME_URL: z.preprocess(blankToUndefined, z.url({ protocol: /^wss?$/ }).optional()),
```
Without `validate-env`, the seam reads `import.meta.env.VITE_REALTIME_URL` directly; note the deviation in the README and consider running `validate-env`.

**Cache types.** `set-up-state-management` already built the `lists()` / `details()` key factory the bridge needs (`grep` above). Replace the hand-written `Todo` type with a Zod schema, so pushed payloads can be validated by the same type the cache holds (in a feature layout the schema lives in `features/todos/schemas/`):
```ts
// src/libs/queryKeys.ts — replaces `export type Todo = …`; keep the rest of the file
import { z } from 'zod';

export const TodoSchema = z.object({ id: z.string(), text: z.string(), done: z.boolean() });
export type Todo = z.infer<typeof TodoSchema>;
```

## 5. Write the seam, the status store and the bridge

Copy these from [`./realtime-code.md`](./realtime-code.md), framework branch as detected:
- `src/libs/realtime.ts` — the seam: one shared WebSocket, topic routing, backoff reconnect with jitter, waits while offline, closes when the last listener leaves, no-op without a URL, validates the envelope of every frame.
- `src/stores/useRealtimeStatusStore.ts` — connection status (`idle | connecting | open | reconnecting | offline`), the only state realtime puts in a store.
- `src/hooks/useRealtimeSync.ts` (React) or `src/composables/useRealtimeSync.ts` (Vue) — the cache bridge: validates each pushed payload with `TodoSchema`, patches the entity with `setQueryData`, invalidates `lists()`, mirrors status into the store, and refetches after every re-open that follows a gap.
- `src/components/atoms/ConnectionStatus/` — an announced `role="status"` badge for `connecting`, `reconnecting`, `offline`.

The `{ topic, data }` envelope and the `subscribe` / `unsubscribe` frames are an assumed protocol: change them in `realtime.ts` only, to match your backend or a vendor SDK (`./realtime-patterns.md`). The server must check the `Origin` header on the handshake: a browser sends same-site cookies on a WebSocket upgrade, so an unchecked endpoint is open to cross-site hijacking (`../../core/_shared/security-baseline.md`).

`captureError` is the seam from `set-up-error-boundaries`. If that skill has not run, run it first, or use `console.error` in the bridge.

## 6. Wire it at the app root

The bridge runs inside the Query provider. Mount it once.

### React — in `src/App.tsx`
```tsx
import { useRealtimeSync } from '@/hooks/useRealtimeSync';

export default function App() {
  useRealtimeSync(); // once, under <QueryClientProvider> (set-up-state-management)
  // …rest of the app
}
```

### Vue — in `src/App.vue`
```vue
<script setup lang="ts">
import { useRealtimeSync } from '@/composables/useRealtimeSync';
useRealtimeSync(); // once; VueQueryPlugin + Pinia are installed in main.ts
</script>
```

## 7. Verify

```bash
pnpm typecheck   # seam, bridge, store and cache types compile
```

Add the browser test from `./realtime-code.md` ("Test") once `configure-test-stack` has run: it checks that valid frames reach the handler, malformed frames (`null`, non-JSON) are ignored, and a dropped socket reconnects and re-subscribes.

Manual: with `VITE_REALTIME_URL` set, run `pnpm dev`, push a `todos` event from the server, and confirm the list updates without a refresh. Kill the connection: the badge shows "Reconnecting…"; restore it: data refetches. Toggle the browser offline, then online: the same refetch happens. Unset `VITE_REALTIME_URL`: no socket opens and the app runs normally.

## References
- ./realtime-code.md — the seam, store, bridge, badge and test, framework by framework.
- ./realtime-patterns.md — the cache-not-store rule, hybrid write, reconnect recovery, payload validation, and the SSE / vendor / high-volume / collaborative deviations.
- ../set-up-state-management/SKILL.md — the `queryClient` + `queryKeys` factory this writes through; the server/UI boundary.
- ../set-up-auth/SKILL.md — how the connection authenticates (cookie on the handshake; token-as-first-frame variant).
- ../validate-env/SKILL.md — the `env` seam that owns `VITE_REALTIME_URL`.
- ../set-up-error-boundaries/SKILL.md — the `captureError` seam the bridge reports malformed payloads to.
- ../_shared/conventions.md — `libs/` seam location, the `stores/` rule, hooks vs composables.
