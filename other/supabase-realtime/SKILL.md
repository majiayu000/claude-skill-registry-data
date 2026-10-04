---
name: supabase-realtime
description: "Doctrine for all Supabase realtime: postgres_changes, broadcast, presence. Use before writing a `.channel(`/useChannel subscription, echo suppression, reconnect logic, an autosave loop beside realtime, or replacing polling with live updates, or when the tab freezes, messages duplicate, or a subscription delivers nothing."
---

# Supabase Realtime — the Matrx doctrine

> Cross-repo node: [`common-docs/systems/architecture/realtime/STATE.md`](../../../../common-docs/systems/architecture/realtime/STATE.md). `@ai-matrx/realtime` absorbs these rules as code — its README is the doctrine's home (R8) and this page is the frontend-specific companion.
>
> 🚨 **As of 2026-08-31 the package is PUBLISHED (0.1.0), installed here as `"latest"`, and mounted ONCE at `providers/RealtimeHost.tsx` (wired in `app/Providers.tsx`). New realtime work uses the package — writing a fresh `.channel(` in this repo is a code-review defect.** Read the package README first; `useChannel` / `usePresence` / `useTyping` come from `@ai-matrx/realtime/react`, and non-hook owners (Redux middleware, refcounted module-level subscriptions) use `useRealtimeManager()` + `manager.open(...)`.
>
> 🚨 **AS OF 2026-09-07 THE MIGRATION IS COMPLETE. `grep -rn "\.channel(" features lib app components hooks providers` returns ZERO call sites in this repo** — every remaining match is prose in a file header describing a body that was deleted. There is no "not-yet-migrated" list any more, and the per-feature table below is history, kept only so a reader can see what each conversion cost and gained.
>
> **The ONLY files allowed to touch a channel:**
>
> | File | Role |
> |---|---|
> | `providers/RealtimeHost.tsx` | THE ONE `<RealtimeProvider>` mount |
> | `lib/realtime/sharedChannel.ts` | The ONE host-shaped refcount (`openShared`) — several surfaces sharing one pg-changes subject |
> | `lib/extension-bridge/bridgeChannel.ts` | Identity-only spec for the foreign extension wire |
>
> Anything else writing `.channel(` is a code-review defect. Per-channel closure table + live proof: `../../../common-docs/projects/npm-package-extraction/DUPLICATION-CENSUS.md` § The realtime closure.
>
> 🚨 **THE ADMISSION RULE: a `private: true` channel's TOPIC PREFIX must be registered in `platform.realtime_topic_prefix`.** Supabase authorizes a private channel by running RLS on `realtime.messages` ONCE, at join time, with `realtime.topic()` set to the topic asked for. This database had RLS ENABLED on that table and ZERO POLICIES from the day it was created until 2026-09-21 — so **every private channel on the platform was refused, forever, silently**. Lane REALTIME wrote the one policy (`platform_topics_admit_their_own`); it dispatches by topic prefix to the owning schema's own access rule through the registry, and **a prefix nobody has registered is still refused**. The scheduler's `scheduler:user:<user_id>` channel lived in exactly that state from the day it was written — `private: true`, shipped, joining nothing — until lane REALTIME-2 registered `scheduler.realtime_topic_admits` (measured before: `CHANNEL_ERROR`; after: `SUBSCRIBED`, delivering in 252 ms). **The answering function asks that schema's EXISTING access rule — the same question its own read doors ask — never a new one invented for the socket**, and it is narrowed when the payload is DATA rather than a notice: `custom:table` carries ids and re-reads through `custom.read_records`, so the read door's own ladder decides; `scheduler:user` carries whole rows, so exactly the person the topic names is admitted. Registered prefixes today: `custom:table`, `scheduler:user`. Guard: **`pnpm check:private-channel-admission`** — every `private: true` declaration in this repo, `aidream/apps/shared/*/src`, `matrx-extend` and `matrx-local`, its topic prefix resolved through the TypeScript AST from `defineChannelNamespace`, diffed against the live registry; an unresolvable site FAILS (annotate `// realtime-admission: <prefix>` and it verifies that instead), and no credentials FAILS as UNMEASURED. In the release gates beside `check:realtime-publication`.
>
> 🚨 **THE PUBLICATION RULE: a table you subscribe to with `postgres_changes` must be in the `supabase_realtime` publication.** It is not granted by `platform.create_entity_table` — it is a separate, idempotent migration guarded on `pg_publication_tables` (precedent: `migrations/meet_realtime_publication.sql`). Miss it and the channel joins, reports `SUBSCRIBED`, and delivers NOTHING, forever, with no error anywhere. Four instances shipped — `workbench.notes` (data loss), `tool.ui` + `app.definition`, `users.user_memory` + `iam.permissions`, and all six `communication.meet_*`. Guard: **`pnpm check:realtime-publication`** — a TypeScript-AST resolver over every binding in this repo AND `aidream/apps/shared/*/src`, diffed against the live publication; a binding it cannot resolve statically FAILS as UNRESOLVED (annotate the call site `// realtime-publication: <schema>.<table>` and it verifies that instead). In CI, and blocking in the release gates.
>
> **Which door to use:**
>
> | You are… | Use |
> |---|---|
> | a React component | `useChannel` / `usePresence` / `useTyping` from `@ai-matrx/realtime/react` |
> | several surfaces sharing ONE pg-changes subject | `openShared(manager, topic, buildSpec)` from `lib/realtime/sharedChannel` |
> | Redux middleware, a thunk, a plain service module | `subscribeToRealtimeManager(specFactory)` from `@ai-matrx/realtime` (0.6.0) — **never** `createRealtimeManager`, which is a second write ledger |
> | on an RLS-authorized Database Broadcast topic | add `private: true` (0.7.0) — never hand-roll `config.private` + `realtime.setAuth()` |
> | talking to a separately released peer that owns the payload | `wire: {mode:"raw"}` + `foreignTopic`, and buy back `isOwnMessage` / `eventKey` |
>
> Rules 1–5 below are the package's job now, not yours. They are kept because knowing WHY the package does what it does is what stops someone re-adding a "helpful" copy beside it.

> 🚨 **THE PHANTOM CONFLICT (2026-09-13): a `version` the ledger never saw is NEVER an echo.** `version` moves on EVERY row update (a desktop sync stamping `file_path`, an ingest job writing metadata). `@ai-matrx/realtime` 0.8.0 classifies by revision first and delivers anything newer than it holds — same actor, same content, pending write or not. Register your own writes WITH their number (`begin({ revision: expectedVersion + 1 })`, `settle(ticket, { revision: response.version })`, `observe({ revision })`), hand the reducer the WHOLE row, and pair every compare-and-swap with `guardedUpdate({ rebase })` from `@ai-matrx/data` 0.14.0 so a bump the client still missed is retried, never shown. Reference: `features/notes` (three layers, each with a failing-then-passing guard).

Realtime + Redux + autosave is the most freeze-prone combination in this app. Every historical browser lockup traced to one of the mechanisms below. Reference implementations: **`features/notes/redux/realtimeMiddleware.ts`** (postgres_changes, the canonical one), `features/files/redux/realtime-middleware.ts` (request-ledger id-dedup variant), `features/data-tables/collab/SupabaseYjsProvider.ts` (broadcast CRDT).

## Rule 1 — Suppress your own echoes, timestamp-monotonic FIRST

**Supabase sends you your OWN writes.** The realtime echo of your UPDATE arrives **50–500ms AFTER** your REST response has already returned the fresh row — so by the time the echo lands, any "in-flight save" flag is already cleared. **Flag-only suppression always misses the echo.**

The canonical guard (`isOwnEcho` in the notes middleware + the same check in its slice merge):

1. **Strictly older `updated_at` than local state → drop.** An echo that isn't newer carries zero information.
2. **Equal `updated_at` → drop only if content fields also match local** (a same-millisecond collaborator write must still land).
3. **While a save is in flight** (`_savingNoteIds`-style flag), additionally content-match: divergent collaborator payloads must still reach the store (that's a real conflict).
4. Parse timestamps with `Date.parse` on both sides; if either is unparseable, fall through to content-match — degrade to delivering, never to silently dropping.

Apply the same monotonic guard **inside the reducer merge** too (`applyServerNoteUpsert`): list fetches and realtime race, and a stale payload merged into state regresses `updated_at`, which then fails the next save's optimistic lock → sticky false conflict.

Alternative for INSERT-heavy streams (DM messages): **id + client_message_id dedup** (optimistic row carries a client id; the echo confirms it). Still add the monotonic rule for UPDATE payloads, and **early-drop `sender_id === userId` before any per-event network call** — own echoes must never cost an RPC or a refetch.

**What an unsuppressed echo does** (the notes freeze, 2026-07): echo of save N arrives while the user typed toward N+1 → dirty-local ≠ server → false `conflict` → conflict UI does O(n²) diff work per render → next save clears it → its echo re-arms it. Self-sustaining main-thread saturation.

## Rule 2 — One batched dispatch per payload; no heavy work per event

- List/history hydration: **ONE dispatch for the whole page** (`upsertNotesFromServer` pattern). A dispatch-per-row loop notifies every subscriber and re-runs every sorted selector once PER ROW — O(N²·log N), a freeze on large datasets.
- Never run an N+1 RPC waterfall per event (one `get_*_user_info` per participant per message). Cache identity lookups in a module map; batch where possible.
- Never compute O(content) work (diffs, LCS, full-corpus filters, O(all-rows) projections) inline in JSX or per event — memoize keyed on the actual input.
- Event-driven refetches (`focus`, `visibilitychange`, per-INSERT list reloads) get a **min-interval gate or debounce**. An unthrottled "reload everything on any event" handler is a storm waiting for busy traffic.

## Rule 3 — Reconnect: backoff + catch-up, and the counter survives flaps

- On `CHANNEL_ERROR` / `TIMED_OUT`: exponential backoff (1s → 30s cap), resubscribe, then **catch-up fetch** (events during the gap are lost forever — realtime has no replay).
- **Do NOT reset the attempt counter on `SUBSCRIBED`.** Reset it only after the channel stays healthy ~30s (`BACKOFF_RESET_AFTER_MS` in the notes middleware). A flapping channel otherwise cycles at the 1s floor forever, each cycle firing a full catch-up fetch.
- The catch-up fetch's own completion must not re-trigger subscription (guard: only (re)subscribe when the channel is missing or the user changed).

## Rule 4 — Lifecycle: middleware-owned, one channel per feature, unique topics

- **Prefer a Redux middleware** as the subscription owner (start on first data load, stop on state reset). Component effects resubscribe on identity churn and multiply channels across mounts — the `useConversations` bug ran one global subscription (each doing a full N+1 reload per event) per mounted picker/panel.
- **One channel per feature.** postgres_changes + broadcast + presence can share a channel — don't run three.
- **Never write a topic string by hand.** On the package this is automatic: `defineChannelNamespace` names the feature's channel and the manager gives every connection attempt a unique instance topic. On a not-yet-migrated channel, wrap the topic in `uniqueChannelTopic()` — canonically `@ai-matrx/realtime`, still re-exported by `@ai-matrx/data/db` for the call sites that have not moved. Static topics collide with the still-joined channel on React 19 double-invoked effects / Fast Refresh and throw "cannot add postgres_changes callbacks after subscribe()".
- Callbacks and mutable values the handler needs: hold in refs / read from `storeApi.getState()` at event time — never in effect deps.

## Rule 5 — Server-side prerequisites (silent-zero-events checklist)

A subscription that compiles but receives nothing has one of these:
1. Table not in the `supabase_realtime` **publication** (the notes 2026-07-10 data-loss bug).
2. Middleware written but never **registered in `lib/redux/store.ts`** (same bug, part 2).
3. **RLS** filters the events (realtime is RLS-authorized — that's a feature; use it instead of client-side owner filters, but it means grants gate delivery).
4. `REPLICA IDENTITY FULL` missing when you need old-row data or RLS-on-DELETE.
5. New table not yet in PostgREST/realtime schema cache (`notify pgrst, 'reload schema'`).

## Rule 6 — Choosing the transport

- **postgres_changes** — durable rows where RLS must gate delivery (notes, files, tasks). The default for entity sync.
- **broadcast** — ephemeral or high-frequency data with no authorization nuance (CRDT updates, typing). Set `self: false` unless the sender genuinely needs its own event. **Never manually broadcast a row you also INSERT** — every subscriber gets it twice.
- **presence** — who's-here rosters (typing, online, multiplayer). Ephemeral only.
- Attribution without presence: if the table has **`updated_by`** (the `_stamp_actor` trigger stamps it platform-wide), every UPDATE payload already identifies its editor — resolve email via `get_user_emails_by_ids` (cached), as the notes "X is editing" bubble does. Reach for a presence channel only when you need is-connected state, not just who-last-wrote.

## Live-collaboration UX (the notes pattern — reuse, don't reinvent)

`features/notes/` ships the reference "who is editing" UX:
- Middleware: `announceEditor()` — on non-self UPDATE, dispatch `setNoteEditor` (userId + cached email), idle-clear timer (8s), late email resolution never resurrects/extends a stale entry.
- State: `noteEditors: Record<entityId, NoteEditorPresence>` + curried `selectNoteEditor(id)`.
- UI: `NotePresenceBanner` (name + animated `notes-editing-dots`), `RecentChangeOverlay` `editorLabel` bubble anchored to the exact changed text, `editorDisplayName()` (email local-part, "Someone" fallback).

## Verification checklist (every realtime change)

- [ ] Two browser sessions (two users): edits in A appear in B; **typing in A while B saves never flags a conflict in A**.
- [ ] Console: no per-keystroke `[RT]` upsert/suppression spam while typing (own echoes silent).
- [ ] Own writes cost zero extra RPCs/refetches (network tab during a send/save burst).
- [ ] Kill the network for 30s, restore: catch-up fetch fires once, missed rows appear, no reconnect loop at 1s.
- [ ] Table verified in the `supabase_realtime` publication + middleware registered in the store.

## Per-feature state — ALL MIGRATED 2026-09-07 (history)

> Two former suspects are gone, not fixed: `features/public-chat/.../SidebarChats.tsx` was deleted with the orphaned `/p/chat` surface (`d2d94ab10d`) and `features/transcripts/context/TranscriptsContext.tsx` with the app-root TranscriptsProvider (`e504edcdc8`). Every other file named on this page still exists. The *behavior* claims below carry their original 2026-07-15 date — they were not re-probed.

Every row below is now on `@ai-matrx/realtime`. The interesting column is the last one — what the conversion actually FIXED, because "it still works" was never the bar:

| Feature | What it is now | What the conversion fixed |
|---|---|---|
| Notes (`features/notes/redux/realtimeMiddleware.ts`) | `subscribeToRealtimeManager` + ledger registered at `markNoteSaving`/`markNoteSaved` WITH `revision` (`version`+1 on begin, the response's `version` on settle) | Deleted its ~60-line `isOwnEcho`, its backoff ladder and its alarm constants. Gained a backfill that fires on tab wake and network restore, not only after a channel error. |
| Files (`features/files/redux/realtime-middleware.ts`) | `subscribeToRealtimeManager`, 5 bindings | Static topic → unique instance topic. Reconcile moved from the SUBSCRIBED callback to `onBackfill`, so a slept tab now reconciles at all. Its request-id ledger STAYS (a different mechanism). |
| Transcript studio | `subscribeToRealtimeManager` ×2 | Neither channel had a catch-up; both do now (all six lists re-read via the service, not the thunks — graph fragmentation). |
| Data tables (`SupabaseYjsProvider`) | broadcast room, `manager` injected | Gained the ordered handler queue (it ships 200KB frames), and a CRDT catch-up: re-send `y-request-state`, because Yjs cannot know what it missed. |
| Education game room | broadcast + presence room | Fixed GHOST PLAYERS — a crashed client's presence entry had nothing to expire it. Echo suppression is now ON (the old `self:true` only existed to paper over a missing local roster rebuild). |
| Scheduler (`lib/scheduler-client/`) | `private: true` + raw wire | Stopped hand-rolling the `config.private` + `setAuth` dance; gained a `resync` signal its three callers now act on. |
| Matrx Local bridge (`features/ai-work/`) | raw wire + `foreignTopic` | Deleted a channel-per-RPC and the queue that serialized every call. |
| Everything else (file-analysis ×3, rag-job, agent-lists, transcripts, memory, code tabs, page-extraction ×2, data-tables snapshots ×2, marketing crawls, vision-interview) | namespaces + `onBackfill` | Every one of them was non-reconnecting: they went silently stale after a laptop sleep behind a screen that looked healthy. |

Polling loops that should become realtime (candidates, verified 2026-07-15): `features/ai-runs/hooks/useAiTasks.ts`, `features/code/redux/codeEditHistoryThunks.ts` (its own Phase-2 comment says so), `features/cms/hooks/useCmsAdminActivity.ts`, `features/pdf/scanner/useScanSaveFlow.ts`, admin events/scanner-health/sandbox status pages.

Full history + invariants: `features/notes/FEATURE.md` § Freeze-loop doctrine. CLAUDE.md carries the one-line pointer under Core invariants → Realtime.
