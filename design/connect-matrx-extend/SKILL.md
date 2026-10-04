---
name: connect-matrx-extend
description: "The matrx-frontend side of the matrx-extend Chrome extension bridge. Use when adding or changing a FRONTEND_RPC action handler, a window-panels deep-link the extension opens, a headless API route it calls, or debugging a silent chrome.runtime.sendMessage or Broadcast round-trip. NOT for code in matrx-extend, matrx-local, or aidream (each has its own connect-* skill)."
---

# Connect matrx-extend (frontend side)

This skill is the matrx-frontend-side how-to for the cross-repo bridge to
matrx-extend. The runtime channel **has shipped** (Phase 2): the Supabase
Broadcast subscriber, the `openPanel` handler, and the reference inbound
API route all exist (see [§ File index](#file-index)). For the full
architectural reference and master spec, see
[`../common-docs/systems/apps/extension/CHANNELS.md`](../../../../common-docs/systems/apps/extension/CHANNELS.md).

> **Wire contract — do not drift.** The Supabase Broadcast `event` field
> is `"FRONTEND_RPC"` (`BRIDGE_BROADCAST_EVENT` in
> `lib/types/bridge-envelope.ts`). The extension MUST listen/publish on
> the exact same event string (`BROADCAST_EVENT_NAME` in
> `matrx-extend/src/lib/frontend-bridge/broadcast.ts`). These two
> constants once disagreed (`"FRONTEND_RPC"` vs `"rpc"`), which silently
> dropped every cross-machine envelope — both sides joined the same
> channel but listened on different events. If a round-trip goes silent,
> check this first.

---

## 30-second mental model

matrx-frontend is the UI; matrx-extend is a Chrome extension. They
coordinate through **two substrates** that share **one envelope**:

- `chrome.runtime.onMessageExternal` (same-machine RPC; whitelisted
  origins in `wxt.config.ts`).
- Supabase Broadcast on `matrx-extension-bridge:<userId>` (cross-machine).

Both carry the same `{ channel: "FRONTEND_RPC", action, payload, requestId }`
envelope. Auth is the same Supabase project on both sides — JWTs are
reusable. UI-bound actions usually route through the existing
window-panels deep-link (`?panels=<typeKey>:<instanceId>`) instead of a
bespoke RPC.

---

## When to use this skill

- Adding a new `FRONTEND_RPC` action handler that the extension can
  invoke (e.g. `conversation.appendMessage`).
- Wiring a new window-panels deep-link entry point that the extension
  will trigger via `?panels=...`.
- Exposing a new headless API route under `app/api/extension/...` for
  extension consumption.
- Debugging silent failures in the extension → frontend round-trip
  (whitelist mismatch, auth mismatch, `requestId` not being echoed).

## When NOT to use this skill

- UI-only changes that don't cross the extension boundary (use
  `window-panels` skill instead).
- Pure Next.js routing / SSR / Server Component work (use
  `ssr-zero-layout-shift`).
- Changes inside the matrx-extend repo itself (use that repo's own
  skills via the worktree).
- Authentication scheme changes — Supabase auth is shared; touch
  `protected-resources` skill territory only when adding a new
  Super-Admin-locked surface.

---

## Quick start — adding a new `FRONTEND_RPC` action

The bridge has shipped; this is the live shape.

1. **Pick a dot-namespaced action name** —
   `conversation.appendMessage`, `panel.open`, `task.create`. Treat
   action names as public API; renaming is a breaking change.
2. **Decide where the handler lives.** Extension → frontend traffic
   lands in one of:
   - A planned headless API route (`app/api/extension/<action>/route.ts`),
     called via `fetch` from the extension SW. Use the dual-auth
     pattern from `app/api/mcp/[transport]/route.ts` (cookie OR
     Bearer; cookie wins).
   - The window-panels deep-link if the action is "open this UI" —
     add a `urlSync.key` to the registry and a `registerPanelHydrator`
     in `features/window-panels/url-sync/initUrlHydration.ts`. No
     new RPC needed.
   - A Broadcast subscriber inside the relevant Redux slice when the
     action is "react to extension event" rather than "do something
     and reply."
3. **Reply with the same `requestId`** — every reply carries the
   request's `requestId` so the caller can match. Failure replies
   include `{ ok: false, error: { code, message } }`; never throw
   across the substrate.
4. **Update both docs** — list the action in
   `../common-docs/systems/apps/extension/CHANNELS.md` § Inbound actions and in the
   matrx-extend master at `../common-docs/systems/apps/extension/CHANNELS.md`. Stale docs
   cascade across the four repos.

---

## File index

| Path | Role |
|---|---|
| `../common-docs/systems/apps/extension/CHANNELS.md` | Architecture + protocol reference for this side of the bridge. |
| `lib/supabase/messaging.ts` | Broadcast / Presence / Postgres Changes substrate. Add the `matrx-extension-bridge:<userId>` channel here. |
| `features/window-panels/registry/windowRegistry.ts` | Window registry — declare `urlSync.key` for any panel the extension will deep-link into. |
| `features/window-panels/url-sync/initUrlHydration.ts` | `registerPanelHydrator(...)` for each `urlSync.key`. |
| `app/api/agent/feedback/route.ts` | Reference Bearer-`AGENT_API_KEY` route for headless calls. |
| `app/api/mcp/[transport]/route.ts` | Reference dual-auth route (cookie OR Bearer, with `?token=` fallback). |
| `app/api/extension/append-message/route.ts` | **Live.** Reference headless inbound route for the extension. |
| `lib/extension-bridge/ExtensionBridgeSubscriber.tsx` | **Live.** Top-level subscriber mounted in `app/Providers.tsx`; routes inbound `openPanel` envelopes to the handler and replies on the same channel. |
| `lib/extension-bridge/openPanelHandler.ts` | **Live.** Validates `openPanel` payloads and dispatches `openOverlay`. |
| `lib/types/bridge-envelope.ts` | **Live.** Canonical wire-format module — channel name, `BRIDGE_BROADCAST_EVENT`, envelope/response schemas. Import from here, never re-declare. |

### Dead reference (do NOT build on this)

`utils/errorContext.ts:10` is a defensive stack-frame filter that strips
`chrome-extension://` URLs from reported errors. It is not part of the
bridge — leave it alone in unrelated PRs.

(The `chrome-extension` entry in
`features/surfaces/data/surface-candidates.ts` is now a real surface
candidate — `chrome-extension/agent-bridge` — not a dead reference.)

---

## Failure modes

### Silent — `chrome.runtime.sendMessage` returns nothing

The page origin is not in `wxt.config.ts` `externally_connectable.matches`.
No error is thrown; the callback never fires. Verify by:

1. Open the extension's service worker console (`chrome://extensions`,
   click "service worker").
2. Watch for the inbound message. If it never arrives, check the
   matches list against the current `window.location.origin`.
3. Common miss: a new Vercel preview URL pattern that the
   `https://*-armani-sadeghis-projects.vercel.app/*` rule doesn't
   cover.

### Silent — Broadcast publish succeeds, no reply

Channel name typo or the receiver isn't subscribed. Verify by:

1. Both sides MUST use the exact same channel string —
   `matrx-extension-bridge:<userId>`. No prefix drift.
2. Both sides MUST use the exact same Broadcast `event` string —
   `"FRONTEND_RPC"` (`BRIDGE_BROADCAST_EVENT` here /
   `BROADCAST_EVENT_NAME` in the extension). Supabase filters delivery by
   `event`, so a mismatch drops every message even though the channel is
   shared. This is the bug that kept Phase 2 dark until 2026-06.
3. Run `client.getChannels()` on both sides to confirm the channel is
   joined. Broadcast silently drops messages with no subscribers.
4. The subscriber must call `.subscribe()` after `.on('broadcast', ...)`.
   Forgetting this is a common silent failure.

### Loud — 401 Unauthorized on the planned headless API route

Auth check failed. Verify by:

1. If using cookie auth, the request must originate from a tab on
   this app's origin (cookies are scoped, the SW does not carry them).
2. If using Bearer, confirm the token is the user's Supabase JWT
   (not `AGENT_API_KEY` — that's for the agent feedback route only).
3. Read `app/api/mcp/[transport]/route.ts` for the canonical
   dual-auth pattern.

### Loud — Deep-link `?panels=...` does nothing

A registry entry has `urlSync.key` but no hydrator. Verify by:

1. Open the JS console after navigating with the URL — a dev assertion
   in `initUrlHydration.ts` logs an error for any `urlSync.key`
   without a matching hydrator.
2. Add the missing `registerPanelHydrator(key, (dispatch, id, args) => ...)`.

---

## Where to look next

- `../common-docs/systems/apps/extension/CHANNELS.md` — full protocol, auth model, and
  pointer to the master.
- `.matrx/AGENT_INSTRUCTIONS.md` — how cross-repo task hand-offs flow
  through this repo.
- Master cross-repo doc (in matrx-extend):
  `../common-docs/systems/apps/extension/CHANNELS.md`.
