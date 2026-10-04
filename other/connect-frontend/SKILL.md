---
name: connect-frontend
description: "Outbound bridge from matrx-extend to aimatrx.com. Use when sending FRONTEND_RPC to a tab, opening a `?panels=` deep link, relaying across machines over Supabase Broadcast, or an `externally_connectable` message silently vanishes. NOT for matrx-frontend-repo changes (use matrx-frontend's connect-matrx-extend)."
---

# connect-frontend — outbound calls into the aimatrx.com admin app

The matrx-frontend Next.js 16 app at aimatrx.com is the third leg of the
Matrx client triangle. Channel C is live over direct external messaging and
Supabase Broadcast, sharing the `FRONTEND_RPC` action surface.

## When to use

- Sending a message from the extension into a specific aimatrx.com tab.
- Triggering a window-panels overlay on aimatrx.com from the extension
  (e.g. open a chat overlay focused on a conversation).
- Relaying state between an extension on machine A and the user's
  aimatrx.com session on machine B (cross-machine).
- Wiring a page-side WebMCP dispatcher so registered tools on
  aimatrx.com can be invoked from the agent.

## When NOT to use

- Changes to the matrx-frontend source. Switch to that repo and use
  its `connect-matrx-extend` skill.
- Trying to make the extension "control" aimatrx.com via DOM injection.
  That works for arbitrary sites but a first-party app should use the
  proper bridge primitives below.
- Confusing this with the chat-side `matrx-extend-tool-display` skill;
  those are unrelated.

## 30-second mental model

```
SAME MACHINE                         CROSS MACHINE
─────────────                        ─────────────
aimatrx.com page                     aimatrx.com on machine B
  │ chrome.runtime.sendMessage(        │
  │   extId, payload)                  │ supabase.broadcast.send(
  ▼                                    │   "matrx-extension-bridge:<userId>",
extension SW receives                  │   { direction, action,
  (gated by manifest's                 │     requestId, payload, timestamp })
   externally_connectable              ▼
   whitelist)                       extension SW subscribes to the
                                    same channel and relays into
                                    chat / tools as needed
```

Plus the deep-link shape that triggers a window-panels overlay
without any messaging at all:

```
https://aimatrx.com/<route>?panels=<typeKey>:<instanceId>
```

The frontend's window-panels parser opens that overlay on page load.

## Quick start

**Same-machine call from the extension to a tab:**

```ts
chrome.runtime.sendMessage(extensionId, {
  channel: "FRONTEND_RPC",
  action: "openPanel",
  requestId: crypto.randomUUID(),
  payload: { typeKey: "chat", instanceId: "abc-123" },
  timestamp: Date.now(),
});
```

**Cross-machine relay via Supabase Broadcast:**

Both ends ride `@ai-matrx/realtime` — never hand-write `supabase.channel(...)`
(the guard `tests/unit/realtime-adoption.test.ts` fails on one). The topic and
the payload shape are the PEER's contract, so the channel declares
`foreignTopic` and `wire: {mode:"raw"}`: the envelope this package normally adds
would change the wire under a program that ships on its own release train.

```ts
// In this repo, just call publishToFrontend() from
// src/lib/frontend-bridge/broadcast.ts — it owns the channel. The shape:
const bridge = defineChannelNamespace({
  namespace: "extension-bridge",
  parts: ["userId"],
  description: "matrx-extend ↔ matrx-frontend RPC bridge (foreign wire).",
  foreignTopic: "matrx-extension-bridge",
});

const channel = manager.open({
  topic: bridge.topic({ userId }),
  wire: { mode: "raw", acceptEchoFromSelf: true },
  broadcast: [{ event: "FRONTEND_RPC", onMessage: ({ data }) => route(data) }],
  eventKey: (_source, p) => `${p.direction}:${p.requestId}`,
  onBackfill: () => {},
});

channel.send("FRONTEND_RPC", {
  direction: "extension->frontend",
  action: "open_panel",
  requestId: crypto.randomUUID(),
  payload: { typeKey: "chat", instanceId: "abc-123" },
  timestamp: Date.now(),
});
```

**Open an overlay without messaging at all:**

```ts
chrome.tabs.create({
  url: "https://aimatrx.com/?panels=chat:abc-123",
});
```

## `externally_connectable` whitelist

Manifest v3 does not accept port wildcards. The exact whitelist for
this extension is (memorize, do not improvise):

- `https://*-armani-sadeghis-projects.vercel.app/*`
- `https://*.aimatrx.com/*`
- `https://*.mymatrx.com/*`
- `http://localhost/*`
- `http://127.0.0.1/*`

Any other origin attempting `chrome.runtime.sendMessage(extId, ...)`
will silently fail. Adding a new origin = manifest change + reload.

## File index (extension side)

| File | Role |
|---|---|
| `src/lib/frontend-bridge/handler.ts` | Shared ping/capabilities/openPanel/callTool action surface |
| `src/lib/frontend-bridge/broadcast.ts` | Cross-machine request/reply adapter |
| `src/lib/background/bootstrap.ts` | External-message listener + lifecycle wiring |
| `wxt.config.ts` | Live `externally_connectable` manifest allowlist |

## Frontend-side reference (read-only from this repo)

- `lib/supabase/messaging.ts` — production-ready Broadcast bridge on
  the frontend; channel name and payload shape match the snippet above.
- The window-panels deep-link parser — handles
  `?panels=<typeKey>:<instanceId>`; stable contract.

The frontend exposes `POST /api/extension/append-message`. Headless extension
calls use the user's Supabase Bearer token; every database operation stays on
that caller-scoped client so RLS remains authoritative.

## Failure modes

- **Silent: page never receives the message.** The page origin is not
  on the `externally_connectable` whitelist. There is no error;
  `sendMessage` resolves to `undefined` and the page sees nothing.
- **Silent: cross-machine Broadcast never fires.** Both clients must
  subscribe to the **same channel name**
  (`matrx-extension-bridge:<userId>` — note the colon) before sending.
  Supabase Broadcast does not retain messages.
- **Loud: deep-link 404.** The route exists but `?panels=` is malformed.
  The parser expects `<typeKey>:<instanceId>`; both halves required.
- **Authorization trap:** a topic containing the user UUID is not itself an
  auth boundary. Cross-machine channels require `private: true` on both sides
  plus `realtime.messages` RLS policies.

## Pointer

For the full topology, the FORBIDDEN domain list (de-spaced forms of
`m a t r x . a p p` and `m a t r i x . c o m` — never reference either),
the production URL map, and the parallel channels (A and B), see
[`/Users/armanisadeghi/code/common-docs/systems/apps/extension/CHANNELS.md`](/Users/armanisadeghi/code/common-docs/systems/apps/extension/CHANNELS.md).
