---
name: synced-store
description: "Build apps that USE synced-store for real-time multiplayer state. PROACTIVELY load when: designing a new Poe tile's state/schema (even before any file exists), discussing how to hide, gate, or restrict visibility of data to specific users or to the server, writing schema.ts/mutators/*.ts/client-config.ts/backend-config.ts for a Poe tile, using createPoeTileTestHarness, calling store.subscribe/store.mutate, or wiring entry.tsx with setupStore."
---
<!-- owner: jyoung-q -->

# Synced-Store Reference

Real-time sync engine (like Replicache). Each app instance = one server-side SQLite DB + per-client IndexedDB copies. Mutators run optimistically on the client and authoritatively on the server. Actions run server-only (AI calls, HTTP, randomness).

- Mutators and actions are portable store code, not normal browser/Node code: mutators run on the client and then on the backend, and actions run on the backend. Backend execution happens in a special store-function runtime where ambient timer APIs such as `setTimeout` / `clearTimeout` are not available.
- WARNING: Synced-store mutations and `externalMutations` work while offline and gracefully sync to the server. Actions and `ctx.platform.call(...)` only run on the server; client-side `ctx.platform.call(...)` in a mutator always throws. Mutator platform calls are discouraged, must be guarded with `ctx.isServer`, must be awaited, must be idempotent/read-only because optimistic-lock conflicts can retry the server mutator attempt, and should be used only for short one-off work because mutators are processed one at a time. Effects from `ctx.enqueueAction(...)` in a mutator will not happen until the mutation syncs to the server. Avoid actions when a mutator can express the behavior.

This file is a snippet index. Load the linked reference when you need detail.

## `synced-store/tile-schema-version.ts` — single source of truth

```ts
// Plain constant file — no Zod, no schema imports. Both client-config.ts
// and schema.ts read from here so the version can never drift between
// client and server. When you add migrations later, `schema.ts` keeps
// importing this same constant alongside the migrations registry.
export const TILE_SCHEMA_VERSION = 1;
```

See [→ schema-migrations.md](references/schema-migrations.md) for bumping the version with a migration.

## `schema.ts` — the contract

```ts
import { z } from "zod";
import { defineSchema, table, singletonTable, item } from "poe-tiles-sdk/v1/backend.js";
import { TILE_SCHEMA_VERSION } from "./tile-schema-version";

export const tileSchema = defineSchema({
  schemaVersion: TILE_SCHEMA_VERSION,
  tables: {
    todos: {
      schema: table(z.object({
        id: z.string(),
        text: z.string(),
        done: z.boolean(),
        updatedAt: z.number(),
      })),
      searchable: { textField: "text", timestampField: "updatedAt" },
    },
    settings: {
      schema: singletonTable(
        item("theme", z.enum(["light", "dark"])),
        item("pageSize", z.number()),
      ),
    },
  },
  mutators: {
    setTodo: {
      description: "Create or update a todo",
      input: z.object({ id: z.string(), text: z.string(), done: z.boolean().optional(), updatedAt: z.number() }),
    },
    removeTodo: { input: z.object({ id: z.string() }) },
  },
  actions: {
    suggestTodo: {
      description: "Ask an LLM for a todo suggestion",
      input: z.object({ prompt: z.string() }),
      output: z.object({ text: z.string() }),
    },
  },
});
export type TileSchema = typeof tileSchema;
```

- Homogeneous collection: `table(valueSchema)` — itemKeys are dynamic.
- Single-row record: `table(schema)` with a fixed itemKey like `"game"` (no no-key `singletonTable(schema)` form).
- Typed settings bag: `singletonTable(item(key, schema), ...)` — per-key value types [→ singleton-tables.md](references/singleton-tables.md).
- Lighter bundles (no Zod): Valibot or JSON Schema [→ schema-libraries.md](references/schema-libraries.md).
- Searchable in Poe search / MCP tools [→ searchable-tables.md](references/searchable-tables.md).
- Bump `TILE_SCHEMA_VERSION` only for backwards-incompatible changes that require a migration. DO NOT bump it merely when adding a new mutator or a new field on a table [→ schema-migrations.md](references/schema-migrations.md).

## Mutators + shared data helpers

Keep each mutator handler in its own file under `synced-store/mutators/`.
Compose the exported mutator map in `synced-store/mutators/index.ts`.
Put read-only data loading helpers in `synced-store/data/` so query,
mutation, and action code can share them without importing write-only helpers.

`synced-store/data/todos.ts`:

```ts
import type { InferReadContext, InferSchemaTableTypes } from "poe-tiles-sdk/v1/client.js";
import type { TileSchema } from "../schema";

export type TileTableTypes = InferSchemaTableTypes<TileSchema>;
export type Todo = TileTableTypes["todos"];
export type TileReadCtx = InferReadContext<TileSchema>;

export async function readTodo(ctx: TileReadCtx, id: string): Promise<Todo | undefined> {
  return (await ctx.table("todos").get(id)) as Todo | undefined;
}
```

`synced-store/mutators/types.ts`:

```ts
import type { InferMutatorHandlers } from "poe-tiles-sdk/v1/client.js";
import type { TileSchema } from "../schema";

export type TileMutators = InferMutatorHandlers<TileSchema>;
export type TileMutator<Name extends keyof TileMutators> = TileMutators[Name];
```

`synced-store/mutators/set-todo.ts`:

```ts
import { readTodo, type Todo } from "../data/todos";
import type { TileMutator } from "./types";

// `updatedAt` is a REQUIRED input — the caller passes Date.now() at the call site.
// Reading the clock inside a mutator is not rebase-safe: the mutator re-runs on
// the server and during rebase, each seeing a different "now".
export const setTodo: TileMutator<"setTodo"> = async (ctx, input) => {
  const existing = await readTodo(ctx, input.id);
  const todo: Todo = {
    id: input.id,
    text: input.text,
    done: input.done ?? existing?.done ?? false,
    updatedAt: input.updatedAt,
  };
  await ctx.table("todos").set({ itemKey: input.id, value: todo });
};
```

`synced-store/mutators/remove-todo.ts`:

```ts
import type { TileMutator } from "./types";

export const removeTodo: TileMutator<"removeTodo"> = async (ctx, input) => {
  await ctx.table("todos").delete(input.id);
};
```

`synced-store/mutators/index.ts`:

```ts
import { removeTodo } from "./remove-todo";
import { setTodo } from "./set-todo";
import type { TileMutators } from "./types";

export const tileMutators: TileMutators = {
  setTodo,
  removeTodo,
};

export type { TileMutator, TileMutators } from "./types";
```

Read [→ mutator-rules.md](references/mutator-rules.md) before writing mutators. Key rules:
- Generate IDs + timestamps at the **call site** (not inside the mutator) — mutators run multiple times (optimistic + server + rebase).
- Explicit values, never toggles: `done: true`, NOT `done: !existing.done`.
- Read-before-write when merging — makes the mutator safe as both create and update.
- `.set()` takes `{ itemKey, value }`, not positional args.
- Private/server-only writes: `ctx.privateOfUser(userId).table(...)`, `ctx.serverOnly().table(...)` — see [data-visibility.md](references/data-visibility.md).

## `actions.ts` — server-only handlers

```ts
import type { InferActionHandlers } from "poe-tiles-sdk/v1/backend.js";
import type { TileSchema } from "./schema";

export const tileActions: InferActionHandlers<TileSchema> = {
  suggestTodo: async (ctx, input) => {
    const existing = await ctx.table("todos").scan().values().toArray(); // reads are fine
    const stream = await ctx.platform.call("poe.botStream.open", {
      botName: "GPT-4o-mini",
      queryRequest: {
        version: "1.0",
        type: "query",
        query: [{ role: "user", content: `Suggest a todo after ${existing.length} existing todos` }],
        user_id: "",
        conversation_id: crypto.randomUUID(),
        message_id: crypto.randomUUID(),
      },
    });
    await stream.cancel(); // parse the stream in real AI-driven actions
    const text = "Water the plants";
    await ctx.mutate("setTodo", { id: crypto.randomUUID(), text, done: false, updatedAt: Date.now() });
    return { text };
  },
};
```

- Actions have read-only table access: `ctx.table(...)`, `ctx.privateOfUser(...).table(...)`, `ctx.serverOnly().table(...)`.
- To WRITE, call `ctx.mutate("mutatorName", input)` — there's no `.set()` / `.delete()` on action table handles.
- Platform API is a single `ctx.platform.call(name, input)` dispatch — prefer actions; guarded server-side mutator calls are discouraged, must be idempotent/read-only because optimistic-lock conflicts can retry the server attempt, and should only be used for short one-off work [→ platform.md](references/platform.md).
- Call from UI: `await store.action.suggestTodo({ prompt })` — flushes pending mutations first, waits for server.
- Dispatch to another store instance [→ external-stores.md](references/external-stores.md).

## `client-config.ts`, `backend-config.ts`, wiring

```ts
// synced-store/client-config.ts — client-safe, no Zod
import { defineClientConfig } from "poe-tiles-sdk/v1/client.js";
import type { tileSchema } from "./schema"; // type-only!
import { tileMutators } from "./mutators/index";
import { tileHooks } from "./hooks";
import { TILE_SCHEMA_VERSION } from "./tile-schema-version";

export const tileClientConfig = defineClientConfig<typeof tileSchema>({
  mutators: tileMutators,
  hooks: tileHooks,
  schemaVersion: TILE_SCHEMA_VERSION,
});
```

```ts
// synced-store/backend-config.ts — server-only
import { defineBackendConfig } from "poe-tiles-sdk/v1/backend.js";
import { tileSchema } from "./schema";
import { tileMutators } from "./mutators/index";
import { tileHooks } from "./hooks";
// import { tileActions } from "./actions"; // add when you introduce server-only handlers

export const tileBackendConfig = defineBackendConfig({
  schema: tileSchema,
  mutators: tileMutators,
  hooks: tileHooks,
  // actions: tileActions, // uncomment + import once actions.ts exists
});
```

```ts
// tile/src/entry.tsx — the only place that calls setupStore
import { createPoe, PostMessageEnvironment } from "poe-tiles-sdk/v1/client.js";
import { tileClientConfig } from "../../synced-store/client-config";

const Poe = createPoe({ environment: new PostMessageEnvironment() });
const store = Poe.setupStore(tileClientConfig);
// render UI with `store` as a prop
```

- Type the client: `type TileStoreClient = InferSyncedStoreClient<TileSchema>`.
- Import paths: `poe-tiles-sdk/v1/client.js` (UI), `poe-tiles-sdk/v1/backend.js` (server), `poe-tiles-sdk/v1/test-utils.js` (tests).

## Reading — inside `query` / `subscribe` / mutator ctx [→ client-api-reference.md](references/client-api-reference.md)
- One-shot: `const todo = await store.query((ctx) => ctx.table("todos").get("todo-1"))`
- Get by key: `await ctx.table("todos").get("id")` — returns value or `undefined`
- Existence check: `const exists = await ctx.table("todos").has("id")`
- All entries: `const rows = await ctx.table("todos").entries().toArray()` — `[EntryKey, value][]`
- Just values: `const vals = await ctx.table("todos").scan().values().toArray()`
- Just keys: `const keys = await ctx.table("todos").keys().toArray()`
- Prefix scan: `table.scan({ prefix: { sortKey: "2026-" }, limit: 50 })`
- Pagination: `table.scan({ limit: 50, cursor: lastEntryKey })`
- Reverse (latest N): `table.scan({ limit: 5, reverse: true })` — returns last 5 in **descending** order. Same entries via sentinel: `table.scan({ cursor: "$last", aroundCursor: { before: 5, after: 0 } })` — same set in **ascending** order (no manual reverse needed)
- Window around an anchor (UI rendering, e.g. show context around a search result): `table.scan({ cursor: { sortKey, itemKey }, aroundCursor: { before: 5, after: 45 } })` — returns up to 5 entries before the anchor, the anchor itself if present, then up to 45 after, ascending
- `aroundCursor` is **client-only** (queries / `subscribeToTable`). Mutators and actions calling it on the server throw with a pointer to the workaround: compose two `cursor + limit` scans manually if you really need server-side context around an anchor
- Current user inside a mutator/query: `ctx.userId` (NOT available on `store.userId`). From UI code, use the helper: `import { getCurrentUserId } from "poe-tiles-sdk/v1/client.js"; const myId = await getCurrentUserId(store);`
- **Read your own private table**: `await ctx.privateOfUser(ctx.userId).table("name").get("key")`. `ctx.table("name")` reads ONLY public data — even your own private rows aren't visible through it. Same goes for subscribes (`tx.privateOfUser(tx.userId).table(...)`) and tests (`store.query(tx => tx.privateOfUser(tx.userId).table(...))`)

## Writing — firing mutators from UI [→ mutator-rules.md](references/mutator-rules.md)
- Fire: `store.mutate.setTodo({ id, text, done: false, updatedAt: Date.now() })` — returns immediately, optimistic
- Await server confirmation: `const { confirmed } = await store.mutate.setTodo({ ... }); await confirmed`
- Terminal/manual inspection: `poe-tiles stores access <typeId> <instanceId>` checks the current `POE_API_KEY` user against `$users`; `poe-tiles stores schema <typeId> <instanceId>` lists mutators and generated CLI commands; `poe-tiles stores mutate <typeId> <instanceId> <mutationName> --input '<json>'` dispatches a mutator. All use the normal user-router WebSocket; see [tile-creator CLI reference](../tile-creator/references/cli.md#stores--store-operations)
- Generate IDs/timestamps HERE (at the call site), pass as input: `id: await store.makeUniqueId()`, `updatedAt: Date.now()`
- Client-side performance optimization: pass `{ pendingMutationDedupeKey }` as the second `store.mutate.*` argument only when repeated pending mutations can be coalesced so the latest value replaces earlier same-key values. Good fits: setter-style drafts, selected tool/type, cursor/hover/highlight, and passive position updates. Do NOT use it for append/send/event/counter/toggle mutations, or when a later queued mutation depends on every intermediate same-key write reaching the server.

  ```ts
  const POSITION_MUTATION_OPTIONS = {
    pendingMutationDedupeKey: "player-position",
  } as const;

  void store.mutate.updatePosition(
    { x, y, updatedAt: Date.now() },
    POSITION_MUTATION_OPTIONS,
  );
  ```

- See the mutator examples above for handler-side rules (explicit values not toggles, read-before-write, etc.)

## Sort keys — ordering large, accumulating tables (advanced)

Most stores don't need this. Reach for a `sortKey` only when a table accumulates a large, ever-growing amount of linearly-ordered data (e.g. chat messages) and you need cheap range scans or "load more" pagination without ever loading the whole table into memory. A todo list, a settings singleton, or any table whose row count stays small and bounded doesn't need one — a plain `scan()` over the whole table is simpler and fine.

- `sortKey` is an **ordering-only** field, separate from `itemKey` (identity). Pass it in `.set()`: `ctx.table("events").set({ sortKey, itemKey, value })`. Omit it and it defaults to `""` — scans order by `(sortKey, itemKey)`, so rows without a sortKey sort together, before any explicit one.
- Data with no `sortKey` is always **eagerly downloaded** — it's exempt from pull-window budgeting and syncs to every client regardless of `pullWindows`/`firstRenderBytes`. Data with a `sortKey` is **lazily downloaded** — subject to windowing/budget, loaded progressively as `pullWindows` and `firstRenderBytes` allow. This is why the feature only pays off for large, unbounded tables: giving rows a `sortKey` is what makes them lazy in the first place.
- Generate sort keys with `ctx.getNextSortKey({ namespace })` inside a mutator — it returns a monotonically increasing `{namespace}/{number}` key, safe under concurrent and offline writes. Don't hand-roll a `Date.now()`-based sort key: clock skew across clients/devices can produce collisions or out-of-order keys.
- **Existing `itemKey`-prefix scans are unaffected.** `sortKey` and `itemKey` prefix filters are independent axes of `scan({ prefix })` — adding a `sortKey` to some or all rows in a table does not change the results of `table.scan({ prefix: { itemKey: "..." } })`.
- Pairs with two schema-level options that make ordering pay off for pull performance once row counts get large, both declared on `defineSchema({ ... })`:
  - `pullWindows: [{ namespace, direction, cursor? }]` — stream a namespace `"ascending"`, `"descending"`, or `"outward"` from an anchor, instead of pulling the whole table on every sync.
  - `firstRenderBytes` — caps the initial synchronous payload size so first render doesn't block on the full history.
- Only configure `pullWindows` / `firstRenderBytes` once a table's row count can grow unbounded — they add real complexity and aren't needed for small/bounded tables.

## Subscribing — reactive UI [→ ui-patterns.md](references/ui-patterns.md)
- React/Preact: `const unsub = store.subscribe((ctx) => ctx.table("todos").entries().toArray(), (entries) => setTodos(entries.map(([, v]) => v)))`
- SolidJS (change diffs): `store.subscribeToTable("todos", (entries, changes) => { /* changes.added|modified|removed */ })`
- Solid + `reconcile()` to preserve DOM nodes across updates (see `docs/solidjs-best-practices.md`)
- React hook with loading state: `const { data, isLoading } = useLiveQuery(store, (ctx) => ctx.table("todos").entries().toArray())` from `poe-tiles-sdk/v1/react`
- Subscribe to a key prefix: `store.subscribe((ctx) => ctx.table("users").scan({ prefix: { itemKey: "alice" } }).entries().toArray(), (entries) => {})`
- Treat subscriptions for local actions as firing twice: optimistic local mutation, then authoritative server confirmation/rebase. Any subscription-driven animation, sound, toast, or derived side effect must de-dupe by event id, version, timestamp, or previous-state comparison.
- Animations via subscribeToTable change diffs: see `docs/synced-store-animation-guide.md`

## Mutator context [→ mutator-rules.md](references/mutator-rules.md) + [server-forking.md](references/server-forking.md)
- `ctx.table(name)` — public
- `ctx.privateOfUser(userId).table(name)` — per-user private (throws on client if `userId !== ctx.userId`)
- `ctx.serverOnly().table(name)` — server-only (throws on client; guard writes with `if (ctx.isServer)`)
- `ctx.isServer` — branch for pending indicators (`isPending: !ctx.isServer`) or server-only writes. Avoid otherwise
- `ctx.enqueueAction("name", input)` — call UNCONDITIONALLY; no-op on client, runs on server after commit. **In tests, call `store.action.<name>(...)` directly after the mutator** to deterministically wait for the action to run — don't rely on `setTimeout`/`tick`. [→ testing-actions.md](references/testing-actions.md#awaiting-mutators-that-enqueue-actions)
- Skip optimistic entirely when outcome depends on unreadable data: `if (!ctx.isServer) return`
- Sending notifications from a mutator: `await notifyActivity(ctx, input)` — updates the manager sidebar (preview / unread bump), optionally enqueues an OS push, and can optionally append one app-owned announcement to the containing chat via `postToChat`.

  ```ts
  await notifyActivity(ctx, {
    preview: string,           // sidebar preview text (e.g. last message)
    previewTimestamp: number,  // bumps the space in the recents list
    unread: "increment",       // optional; uses the default simple unread
                               // policy and bumps each non-caller recipient's
                               // app-owned unread count. Omit for a
                               // preview/sortKey refresh only.
    unreadToCaller: true,      // optional; system-attributed receipt that
                               // should also increment the caller. Requires
                               // unread: "increment" and caller targeting.

    // Optional. Omit → fan out to every active member.
    // Client pass is a no-op unless ctx.userId is in this list (or omitted);
    // the server's authoritative pass does the real fan-out.
    targetUserIds?: string[],

    // Optional. If present, every activity recipient EXCEPT the caller
    // gets an OS push (default sender-suppression). Use `pushToCaller: true`
    // to include the caller (e.g. system-attributed pushes); throws if the
    // caller isn't in the activity recipient set.
    push?: {
      title: string,           // notification title (sender / app name)
      body: string,            // notification body (preview / message text)
      pushToCaller?: boolean,  // default false — don't push your own action
    },

    // Optional. Appends one announcement row to the chat room resolved from
    // this store's pinned $$system/room. No caller-provided chat id. Chat
    // ignores messageId for row identity, uses its next msg/... sortKey, and
    // derives a separate chat-owned itemKey from that sortKey.
    postToChat?: {
      messageId: string,
      text: string,
      timestamp: number,
    },
  });
  ```

### Validation order: throw BEFORE the `isServer` gate

When a mutator validates its input (turn checks, slot conflicts, phase gates), put the `throw` **above** any `if (!ctx.isServer) return;` so it runs on the client's optimistic pass. Otherwise the optimistic mutation succeeds locally and the server-side rejection is silent (see "Server throws don't reject `confirmed`" below). Validate using public/own-private state up top; only gate writes that touch `serverOnly()` or other users' `privateOfUser` tables.

```typescript
makeMove: async (ctx, input) => {
  // CHEAP CHECKS FIRST — they run on both client (optimistic) and server.
  // A bad call rejects the outer `await store.mutate.makeMove(...)` synchronously.
  const game = await ctx.table("game").get("state");
  if (game?.status !== "playing") throw new Error("Game is not in play");
  if (game.currentPlayer !== ctx.userId) throw new Error("Not your turn");

  // SERVER-ONLY work below this line. The board lives in serverOnly(), so we
  // can't validate the move further on the client — accept the optimistic
  // pass as a no-op and let the server do the real work.
  if (!ctx.isServer) return;
  const board = await ctx.serverOnly().table("board").get("state");
  // ... apply move, advance turn, etc.
},
```

Worked example — a `startRound` mutator that validates role coverage with public state before doing any server-only randomness:

```typescript
startRound: async (ctx) => {
  const phase = await ctx.table("game").get("phase");
  if (phase !== "setup") throw new Error(`Cannot start in phase ${phase}`);

  // Public state — readable on client + server, so this throw rejects the
  // optimistic call synchronously when roles aren't filled.
  const players = (await ctx.table("players").entries().toArray()).map(([, v]) => v);
  const hasRedSpy = players.some((p) => p.team === "red" && p.role === "spymaster");
  const hasBlueSpy = players.some((p) => p.team === "blue" && p.role === "spymaster");
  if (!hasRedSpy || !hasBlueSpy) throw new Error("Both teams need a spymaster");

  // Server-only work below — randomness, hidden board placement, etc.
  if (!ctx.isServer) return;
  const seed = crypto.getRandomValues(new Uint32Array(1))[0]!;
  await ctx.serverOnly().table("board").set({ itemKey: "state", value: layoutFor(seed) });
  await ctx.table("game").set({ itemKey: "phase", value: "playing" });
},
```

## Actions — more detail [→ actions.md](references/actions.md) + [platform.md](references/platform.md)
- Handler shape and basic wiring shown in `actions.ts` example above.
- Stream bot responses, MCP tool exposure, multi-step actions — see `actions.md`.
- Testing actions and server-side platform calls with mocked `ctx.platform.call(...)` [→ testing-actions.md](references/testing-actions.md).

## Inter-app communication [→ external-stores.md](references/external-stores.md)

Read this reference when you want different apps to communicate with each other or trigger mutations on each other.

## System hooks — react to membership / parenting / permission changes
Declare hooks in a client-safe module and wire them into **both** `defineClientConfig({ hooks })` and `defineBackendConfig({ hooks })`. Backend hooks run on the server within the same atomic transaction as the system mutator that fired them. Client hooks run optimistically for fresh creator launches before server data arrives, then the server-authoritative data replaces that overlay. Receive a `MutationContext` — treat hooks like mutators (read + write tables, follow rebase-safe rules). If a hook has server-only side effects, split the deterministic writes into a shared helper and keep the server-only tail backend-local, or guard that tail with `if (ctx.isServer)`. `onInit` is supplied by `poe-tiles-kernel` for new child-room launches and root-group genesis. Read the current room topology from `await ctx.table("$$system").get("room")`; `ctx.userId` identifies the initiating user for user/external-store bootstraps, while `ctx.isSystem` indicates the hook is running in trusted system scope. The input carries a read-only snapshot of the parent room's users for child rooms.

```ts
import type { SystemHookMap } from "poe-tiles-sdk/v1/client.js";

export const tileHooks = {
  onInit: async (ctx, { parentRoomUsers }) => {
    const room = await ctx.table("$$system").get("room");
    if (room?.type === "rootGroup") {
      // Seed app-owned rows for a newly started group here.
      // A fresh rootGroup genesis always has an empty parentRoomUsers.
    }
  },
  onAddUsers: async (ctx, { userId }) => {
    await ctx.table("scores").set({ itemKey: userId, value: { userId, score: 0 } });
  },
  onRemoveUser: async (ctx, { userId }) => { /* cleanup */ },
  onAnonymizeUser: async (ctx, { userId }) => { /* scrub app references */ },
  onSetTitle: async (ctx, { userId, title }) => { /* title is string | null — null when the custom title is cleared/reset to the default; handle both */ },
  onGrantPermission: async (ctx, { userId, permission }) => { /* e.g. log audit row */ },
  onRevokePermission: async (ctx, { userId, permission }) => { /* e.g. tear down role-specific state */ },
  onChildInstancesAdded: async (ctx, { instances }) => { /* e.g. index child rows */ },
  onRoomMemberInstanceMovedOut: async (ctx, { storeTypeId, instanceId, toRoom }) => { /* e.g. record departure */ },
} satisfies Partial<SystemHookMap>;
```

- `onInit(ctx, { parentRoomUsers })` — new root-group or child-room tile initialized. Read `await ctx.table("$$system").get("room")` for the current room topology, and use `ctx.userId` for the initiating user when the bootstrap came from a user/external store; use `ctx.isSystem`, not `ctx.source.type === "system"`, to detect trusted system scope. `parentRoomUsers` is a **read-only snapshot** of the active parent room roster (`PoeUserInfo[]`) for child rooms and empty for root groups — useful to detect a fresh rootGroup genesis or to react to the parent roster, never a way to admit members. Apps may write their own tables on both passes. Do **not** write `$users` directly, and do not try to pull parent-room users into the tile: membership is platform-owned. The host seats the launcher at genesis (and both users when the tile is launched from a 2-person room, i.e. a DM); anyone else joins through the host picker/invite flows.
- Use `onInit` for deterministic one-time bootstrap, not membership. It is a good place to seed app-owned rows such as an initial activity or transcript message (`"{name} started the group"`).
- `onAddUsers(ctx, { userId })` — user joined the instance. Use it to auto-seat newly added users into roles, seats, teams, or turn order, and to append membership activity. The `$users` row has already been written when the hook runs, so read `await ctx.table("$users").get(userId)` for `addedBy` and optional `addedBatchUserIds`, then read `$userInfo` to write messages like `"{name} added {usernames...}"` or coalesce a multi-user add into one announcement.
- `onRemoveUser(ctx, { userId })` — user removed
- `onAnonymizeUser(ctx, { userId })` — user hard-deleted/anonymized
- `onSetTitle(ctx, { userId, title })` — title changed; `title` is `string | null` — it is `null` when the custom title is cleared/reset to the default, so handle the null (reset) case rather than interpolating `null`
- `onGrantPermission(ctx, { userId, permission })` — permission granted
- `onRevokePermission(ctx, { userId, permission })` — permission revoked
- `onAddTileInstanceToRoom(ctx, { storeTypeId, instanceId })` — an app instance was registered as a member of this room (fires on the room store after a new `$room_member_instances` row is written; suppressed on idempotent re-registers)
- `onChangeTileParent(ctx, { previousParent, parent })` — this tile instance gained, lost, or changed its parent rootGroup
- `onAddChildTile(ctx, { typeId, instanceId, room })` — a rootGroup gained one net-new child tile row
- `onChildInstancesAdded(ctx, { instances })` — a rootGroup gained one or more net-new child tile rows
- `onRoomMemberInstanceMovedOut(ctx, { storeTypeId, instanceId, toRoom, ... })` — a member app instance is removed from this room

### Hook constraints
- **Client hook mirrors are the default.** Every backend hook should have a client-config entry so fresh prepared stores can run the same hook optimistically before server results arrive. Hooks must be browser-safe: deterministic, no backend imports, no platform calls on the client, and no server-only table reads/writes unless guarded with `if (ctx.isServer)`. A hook whose only useful work is server-only should still be represented by a client-safe no-op or shared partial helper, so future optimistic hook inputs do not silently do nothing.
- **Hooks can write app tables across visibility tiers.** Hooks run inside system mutators, but app public tables, server-only tables, and app private tables (including `ctx.privateOfUser(otherUserId)`) are app data, not reserved system tables. They still must not write reserved system tables such as `$users` or `$$system` directly — membership is platform-owned (the host seats users at launch; pickers/invites admit the rest), so hooks never add members. Use cross-user private writes sparingly for durable per-user projections tied directly to the hook event; regular mutators or actions are still clearer for user-initiated fan-out.
- **Hook ctx is loosely typed.** The `hooks` field is `Partial<SystemHookMap>`, so the `ctx` your handler receives types its tables as `Record<string, JSONValue>` rather than your schema's value types. If your hook needs typed reads/writes (anything beyond `ctx.userId`), cast: `ctx as unknown as InferMutationContext<TileSchema>`. See "Typing helpers extracted from a schema" below.

## Typing helpers extracted from a schema
The exported types `InferMutatorHandlers<Schema>`, `InferSchemaTableTypes<Schema>`, etc. cover the common cases. For helpers, prefer the schema-level context aliases:

```ts
import type {
  InferActionContext,
  InferMutationContext,
  InferReadContext,
} from "poe-tiles-sdk/v1/client.js";
import type { TileSchema } from "./schema";

export type TileReadCtx = InferReadContext<TileSchema>;
export type TileMutationCtx = InferMutationContext<TileSchema>;
export type TileActionCtx = InferActionContext<TileSchema>;
```

- `InferReadContext<Schema>` is the best default for shared data-loading helpers. It is a read-only context and accepts query, mutation, and action ctx values.
- `InferMutationContext<Schema>` is for helpers that write or enqueue actions.
- `InferActionContext<Schema>` is for helpers that need action-only fields such as `ctx.mutate`.

One situation still needs special care:

> **Caveat — `InferSchemaTableTypes` and singleton tables.** For tables defined with `singletonTable(item(key, schema), ...)`, `InferSchemaTableTypes<Schema>["myTable"]` returns the `SingletonTableBrand & {state: T}` bag, not the per-key value union. Reader-side `ctx.table("myTable").get("key")` correctly narrows to the inner item, so runtime calls work — but `type T = TileTableTypes["myTable"]` looks like it works (no error at the extraction step) and then blows up downstream because none of your fields are on the bag type. Cope: derive the singleton item type from the Zod schema instead — `type Theme = z.infer<typeof themeSchema>`, defining `themeSchema` next to the `singletonTable(...)` call. Tracked as a real bug in the helper; this note is interim guidance.

**Casting a hook ctx.** Hooks declare their context loosely (see "Hook ctx is loosely typed" above):

```ts
hooks: {
  onAddUsers: async (ctx, { userId }) => {
    await onUserJoin(ctx as unknown as TileMutationCtx, userId);
  },
}
```

The cast is safe at runtime — the platform passes the same `MutationContext` shape; only the static types are loose.

## Data visibility — pick a tier before writing schema [→ data-visibility.md](references/data-visibility.md)
- Public (default): everyone in the instance sees it
- `privateOfUser(userId)`: only that user — write one copy per recipient when roles are assigned
- `serverOnly()`: never syncs to clients — expose derived results via actions
- Red flag: if you're designing client-side filtering or action-gating to hide data, you picked the wrong tier

## System tables — read-only, platform-populated [→ getting-user-info-of-members.md](references/getting-user-info-of-members.md)
Apps can READ but NOT WRITE these `$`-prefixed tables. The platform populates them.
- `$users` — membership roster. ItemKey = userId. Use `ctx.table("$users").entries().toArray()`, filter `!u.removedAt` for current members.
- `$userInfo` — profile data (`displayName`, `username`, `profilePicture`). ItemKey = userId.
- Optimistic first-mount system rows (`$$system.room`, `$users`, `$userInfo`) carry `_pendingSync: true` until the first server pull replaces them. Use it when UI needs to distinguish a locally seeded member from one fully admitted by the platform.
- `$$system:createdBy` — `{storeTypeId, instanceId}` of the app instance that originally spawned this one (e.g. via `apps.openChild`). First-writer-wins; absent for root apps and instances first reached via cross-store dispatch. Read with `await ctx.table("$$system").get("createdBy")`.

  **Encouraged: surface the current user's avatar + display name somewhere in the UI** (header, sidebar, "playing as ..." chip). It anchors the user inside the app instance — without it, multi-user apps feel ambiguous about identity, especially across device switches.

  **For multi-player tiles, also render the avatars of co-players and opponents** where the action is — at the table, on the board, beside each move, score row, and turn indicator — not just the current user. Seeing real faces is what makes a session feel like playing *with people* rather than against software, and it's a core part of what makes social games rewarding. Enumerate members from `$users`, look each up in `$userInfo`, and design for a missing `profilePicture` (initials fallback). Full recipe → [getting-user-info-of-members.md](references/getting-user-info-of-members.md#rendering-co-player-avatars).

  ```ts
  // Current user (avatar + name in the header) — recommended for every app
  const me = await ctx.table("$userInfo").get(ctx.userId);
  // me?.profilePicture, me?.displayName, me?.username

  // Another user (rendering an avatar next to their move/message)
  const other = await ctx.table("$userInfo").get(otherUserId);

  // Anywhere with ctx — same data, ergonomic helper:
  import { getUserInfo } from "poe-tiles-sdk/v1/client.js";
  const info = await getUserInfo(ctx, userId);
  ```

## Client lifecycle [→ client-api-reference.md](references/client-api-reference.md)
- Wait for authoritative data: `await store.waitForBootstrap()` (none of these are required — queries/mutations work immediately)
- Sortable unique id: `const id = await store.makeUniqueId()` — for use as itemKey or input to `store.mutate.*`
- Pending mutations: `store.getPendingCount()`, `store.onPendingMutationsChanged((m) => showSaving(m.length > 0))`
- Connection status: `store.connectionStatus`, `store.onConnectionStatusChange(fn)`, `store.isOnline`
- Error hooks: `store.onBackgroundError(fn)` for async sync errors, `store.onFailedMutation(fn)` for mutation-only failures, `store.onDisconnected(fn)`, `store.onSchemaVersionMismatch(fn)`, `store.onLibraryVersionMismatch(fn)`, `store.onDisposed(fn)` — kick / auth-failure codes arrive via `onDisconnected`
- Background-error toast: the SDK auto-shows a generic `BackgroundError:` toast for every background error (except `no_access_to_this_store`, which gets a blocking overlay) with zero app code, and always fires a `reportError` event. There is **no per-error opt-out** — you cannot mark a specific expected error as suppressible. So keep *expected* errors out of the throw/background-error path entirely (see the "Don't throw for expected error cases" gotcha).
- Teardown: `store.dispose()` — closes WebSocket, not reversible

## Testing [→ testing.md](references/testing.md)
- Harness: `const harness = createPoeTileTestHarness<TileSchema>({ store: { backendConfig: tileBackendConfig } })`
- Client: `const { store } = await harness.createClient({ userId: "alice" })`
- Multi-client:
    - A single mutate-then-peer-query works — the harness propagates synchronously enough.
    - **For ANY sequence of cross-client mutations where the next step depends on a prior client's writes being server-confirmed, bare `await store.mutate.X(...)` is NOT sufficient.** This includes final-submitter mutators that aggregate everyone's state (e.g. "all players have submitted → reveal").
    - Fix option A: await `.confirmed` between clients — `const r = await alice.mutate.X(...); await r.confirmed;`
    - Fix option B (preferred): gate with `waitForKeyExists` / `waitForKeyMatch` / `waitForValue` / `waitForAllClients` from `poe-tiles-sdk/v1/test-utils.js`. The `waitFor*` helpers also produce descriptive timeout errors.
    - `store.query`, `store.subscribe`, `waitFor`, and `waitForAllClients` take a `(tx) => ...` reader callback. Do not pass a helper that expects the store/client object; type reusable readers against `InferReadContext<TileSchema>` instead. Key/value wait helpers use `{ table, key, ... }` options.
    - Full family + example [→ testing.md](references/testing.md#multi-client-tests)
- Observing optimistic state before server sync [→ testing-network-control.md](references/testing-network-control.md)
- Comparing optimistic vs server-verified values for the same mutation [→ testing-optimistic-values-and-server-verified-values.md](references/testing-optimistic-values-and-server-verified-values.md)
- Message reordering / concurrent mutations [→ testing-race-conditions.md](references/testing-race-conditions.md)
- Disconnect/reconnect, offline retry [→ testing-network-failures.md](references/testing-network-failures.md)
- Deterministic bot streams (`Poe.stream()` / `Poe.call()`) [→ testing-bot-streaming.md](references/testing-bot-streaming.md)
- Mock `ctx.platform.call(...)` in action / guarded server-mutator tests [→ testing-actions.md](references/testing-actions.md)
- Awaiting mutators that `enqueueAction` (call `store.action.X(...)` directly) [→ testing-actions.md](references/testing-actions.md#awaiting-mutators-that-enqueue-actions)
- E2E with TestServer + Playwright blob-frame [→ testing.md](references/testing.md)

## Gotchas that bite everyone
- **Subscriptions fire twice per mutation** — once when the optimistic write lands locally, again when the server-confirmed result rebases. Callbacks must be idempotent: don't `mutate` / trigger sounds or animations / push to an array / increment a counter from inside a subscribe callback without dedup. 
- **`store.userId` does NOT exist** — read `ctx.userId` inside a subscribe/query/mutator callback, or in UI code call `getCurrentUserId(store)` (from `poe-tiles-sdk/v1/client.js`)
- **`ctx.table(name)` does NOT see your own private rows** — even reading your own data needs `ctx.privateOfUser(ctx.userId).table(name)`. The same applies to subscribes (`tx.privateOfUser(tx.userId).table(...)`) and tests
- **Server-only throws are silently rolled back** — a `throw` inside `if (ctx.isServer) { ... }` does NOT reject the outer `await store.mutate.X(...)` or its `.confirmed` promise. The client's optimistic mutation just disappears and the user sees nothing. Validate with public/own-private data BEFORE the `isServer` gate so the throw runs on the optimistic pass and rejects synchronously. To observe server-rejected mutations and other async sync errors from the client, subscribe with `store.onBackgroundError(...)`; use `store.onFailedMutation(...)` only when mutation-specific handling is enough. See "Validation order" above
- **Don't throw for expected error cases — early-return, or write the error to the store.** A throw in a mutator that survives to the server becomes a `failed_mutation` background error, which the SDK surfaces as a generic `BackgroundError:` toast AND fires a `reportError` event. There is no per-error opt-out — you **cannot** selectively suppress the toast for a single expected error. So route expected failures away from `throw` entirely:
    - **Benign / idempotent / redundant-replay** ("already started", "already joined", "already claimed", or an outcome that depends on unreadable server-only data) → **early `return`**. Pending mutations replay on every rebase and can race the same action from another client/device, so these replays are normal, not errors; a throw here also logs `"Synced State | Error rebasing mutation"` to the user's console on every rebase.
    - **An expected failure the UI must react to** (seat taken, hand folded, quota hit, validation the user should see) → **don't throw; write an error/status row to the store** and let clients subscribe, infer, and render it. This is the multi-user-correct channel: every client sees the state, not just the one caller who awaited `store.mutate.X(...)`. Throwing would only reach that caller (and only via `.confirmed`/`onBackgroundError`) and would spuriously toast.
    - Throw only for genuinely invalid actions that indicate a bug, never for a state the app is expected to hit in normal use. [→ mutator-rules.md](references/mutator-rules.md) rule 5
- **`await store.mutate.X(...)` does NOT wait for server confirmation in cross-client tests** — it resolves once the optimistic mutation is in pendingMutations.
    - When it bites: sequential mutations from different clients where the next step reads server-aggregate state (e.g. an "all-players-submitted → reveal" mutator that scans the public players table). The next client's mutator may run before the prior client's writes are committed, so its scan sees stale `hasSubmitted: false` rows and the reveal never fires.
    - Symptom: tests pass with 2 clients (timing happens to win), then fail at 3+ — exactly the "scaled past two players" regression.
    - Also bites when verifying a remote client sees a public-flag flip in their own DOM/query — bare `await mutate()` won't have flushed by the time you assert.
    - Fix: prefer `waitForKeyMatch` / `waitForValue` between cross-client steps, or at minimum `await r.confirmed` after each `await client.mutate.X(...)`.
- **Hooks can write app private tables for any user** - system hooks may update app-owned public, server-only, and private rows, including `ctx.privateOfUser(otherUserId).table(...)`. They still cannot write reserved system tables such as `$users` or `$$system` directly. `onInit` can seed app rows for new root groups by reading `$$system.room`; it cannot add members — `parentRoomUsers` is a read-only snapshot and membership is platform-owned.
- **`.set()` takes `{ itemKey, value }`**, not positional args
- **Generate IDs + `Date.now()` outside mutators**, pass as input — mutators run on client + server + rebase
- **Use explicit values, not toggles** — rebase sees current state, so `!current.done` can flip the wrong way
- **Read-before-write when merging fields** — makes the mutator safe as both create and update, and safe to replay
- **`ctx.enqueueAction` needs no `isServer` guard** — it's already a client no-op
- **Type-only schema import on the client** — `client.ts`, `client-config.ts`, data helpers, mutator files, and any other file that ends up in the iframe bundle must `import type { tileSchema }`, never `import { tileSchema }`. **Pulling the schema in as a value drags `poe-tiles-sdk/v1/backend.js` into the frontend, which requires `node:async_hooks` (via the recorder package) and the build fails with `Module "node:async_hooks" has been externalized for browser compatibility`. The frontend module count typically jumps 10× when this happens.** If you need a runtime constant in both schema and UI, put it in a separate `synced-store/constants.ts` (no zod, no SDK imports) and import from there.
- **Share pure logic** — extract anything used by both mutators and UI into a shared module

## Constraints & limits [→ limitations.md](references/limitations.md)
- Size limits, JSON-only data types, kick codes, last-writer-wins, optimistic-lock retries
