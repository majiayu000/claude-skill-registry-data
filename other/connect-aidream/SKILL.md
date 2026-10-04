---
name: connect-aidream
description: "Outbound contract from matrx-extend to the aidream backend. Use when exposing a new extension capability to aidream, adding a `client.state['browser-dom']` key, wiring a `load_chrome_tools` category, posting tool results or resuming after `tool_delegated`, or 'the model never sees my tool'. NOT for aidream-repo changes (use aidream's connect-matrx-extend)."
---

# connect-aidream — outbound calls into the AI Dream backend

The matrx-extend extension talks to aidream over a single SSE-streamed
chat endpoint. The contract that defines what tools the LLM gets to see,
and what state it gets to read, is the **capability envelope**. This
skill is the entry point when you're working in this repo and need to
extend or debug what flows out to aidream.

## When to use

- Adding a new key to `client.state["browser-dom"]` (e.g. a new flag the
  server needs to gate tool advertisement on).
- Wiring a new tool category that the model can call `load_chrome_tools`
  with (extension side: handler + alias; server side: routing).
- Debugging "the model never sees my tool" — usually a discovery / merge
  bug, not a handler bug.
- Reading or extending the `RESOURCE_CHANGED kind=active_tools` event
  family that the extension subscribes to for live tool-set updates.

## When NOT to use

- Changes to aidream's Python source. Switch to that repo and use its
  `connect-matrx-extend` skill.
- Changes to a tool **handler** (the code that actually runs in the
  service worker when a tool fires). That's local to this repo and lives
  in `src/lib/tools/handlers/`.
- Changes to how the extension renders a tool in the chat surface —
  that's the `matrx-extend-tool-display` skill.

## 30-second mental model

```
extension → POST /ai/agent/{agent_id} ─┐
  client.capabilities = ["browser-dom"]│
  client.state["browser-dom"] = {…}    │
                                       ▼
                                aidream apply_unified_tools
                                  (tool_merge.py)
                                       │
                                advertises load_chrome_tools to LLM
                                       │
                              LLM calls load_chrome_tools(category="forms")
                                       │
                                browser_discovery.py reads state,
                                queues tool changes (add/remove)
                                       │
                                  RESOURCE_CHANGED kind=active_tools
                                       ▼
                              extension updates Tools-tab badge,
                              records loaded category
```

## Quick start

When you need the server to gate a tool category on a new flag:

1. **Extension side** — add the flag to the `browser-dom` state bundle
   that ships with every chat request. The bundle is the small
   orchestration object (~12 keys today) sent under
   `client.state["browser-dom"]`.
2. **Server side** — extend `browser_discovery.py` to read the new flag
   and filter the category-routing table. (This is server work; switch
   repos to do it.)
3. **Verify** — admin → Tools tab → trigger `load_chrome_tools` for the
   gated category; confirm the tools appear iff the flag is true.

The server-to-extension event you watch for is
`RESOURCE_CHANGED kind=active_tools`. The extension already subscribes
to this and updates `useActiveToolsStore` so the next request hints the
loaded categories back. No new event plumbing needed.

## Client-tool resume contract (load-bearing — read before touching tool results)

The aidream backend HARD-SUSPENDS the loop when a client-delegated tool is
pending: it persists the turn, emits a `complete` phase, and **ends the
SSE stream**. The originating stream is GONE the moment the model
delegates a client tool. To continue, the extension must:

1. POST the tool result through `postToolResults`
   (`src/lib/api/routes/tool-results.ts`) — the ONE funnel.
2. Read the response. When `data.continuation_needed === true`, broadcast
   `CHANNELS.STREAM_CONTINUE` with `{conversationId, userRequestId}`. The
   SW dispatcher already does this in `dispatch.ts::postResult` — do NOT
   add a second tool-result POST path that bypasses it.
3. The sidepanel's `useChatStream` subscribes to `STREAM_CONTINUE` and
   runs `resumeRun(conversationId, userRequestId)`: pushes a fresh
   assistant bubble, allocates a new `runId`, rebuilds the
   `client.state["browser-dom"]` envelope against the current active tab,
   and `STREAM_START`s against `conversationResumePath(conversationId)`.
   The existing `STREAM_CHUNK` consumer routes the continuation chunks
   into the new bubble.

**Invariant.** Never wait on the original stream after a `tool_delegated`
event. It has ended. Adding a "listen for more events on the closed
stream" pattern reintroduces the entire bug class this protocol exists
to kill.

**Disambiguation — `src/lib/stream/resume.ts::attemptResume` is NOT this.**
That file is the SEPARATE, still-unbuilt **stall-recovery cursor-replay**
feature (keyed by `request_id` + a cursor of events seen; triggered by
the watchdog on a stall). It points at `GET /ai/agent/runs/{request_id}/resume?cursor=`
which the backend has not built. Do not conflate. The canonical doc that
covers both, with the differences laid out, is
[`matrx-frontend/features/agents/docs/CLIENT_TOOL_SUSPEND_RESUME.md`](../../../../matrx-frontend/features/agents/docs/CLIENT_TOOL_SUSPEND_RESUME.md).

### Wire shape

```
SW → server:  POST /ai/conversations/{id}/tool_results
              body: { results: [{call_id, tool_name, output, is_error, error_message}] }

server → SW:  200 { resolved, already_resolved, not_found,
                     continuation_needed: bool,
                     user_request_id: string|null,
                     conversation_id: string }

(if continuation_needed === true)

SW → sidepanel (broadcast):  CHANNELS.STREAM_CONTINUE
                              { conversationId, userRequestId }

sidepanel → server:  POST /ai/conversations/{id}/resume
                     body: { user_request_id, client: { capabilities: [...], state: {...} } }
                     → 200 NDJSON stream of the continuation
                     → 409 outstanding_delegated_calls (more answers still pending)
                     → 404 conversation not found
```

The server reconstructs the conversation from the DB on every `/resume`
call; the answer the SW just POSTed is already embedded — do NOT include
the tool result in the resume body.

## File index (extension side)

| File | Role |
|---|---|
| `src/lib/chat/context/v2-bundled.ts` | The canonical context shape; `browser-dom` state lives in the orchestration bundle attached to every chat request |
| `src/lib/tools/aliases.ts` | Wire-format aliasing — strips `matrx-extend__` and bundle prefixes (e.g. `forms__fill_form`) before dispatch |
| `src/lib/tools/registry.ts` | `lookup(name)`, `assistantToolNames`, `pilotToolNames` — local handler library |
| `src/lib/tools/dispatch.ts` | SW dispatcher; subscribes to `STREAM_OPENED` + `STREAM_CHUNK`, runs handlers, posts results |
| `src/lib/tools/handlers/*.ts` | One file per tool domain; signatures and Zod schemas |
| common-docs/systems/agents/agent-tools/STATE.md | Full wire-format playbook (canonical `:` vs wire `__`) |

## Server-side reference (read-only from this repo)

- `aidream/api/utils/tool_merge.py::apply_unified_tools` — the unified
  merge that decides which tools the LLM sees on each turn.
- `packages/matrx-ai/matrx_ai/capabilities/browser_dom.py` — capability
  definition; the JSON metadata sibling lists every always-on tool.
- `packages/matrx-ai/matrx_ai/tools/implementations/browser_discovery.py`
  — server-side handler for `load_chrome_tools`; reads
  `client.state["browser-dom"]` and decides the add/remove list.

## Extending an existing capability vs. injecting inline

- **Extend the existing `browser-dom` capability** when the new tool
  belongs to a category and follows the discovery loop (cheap; reuses
  the always-on `load_chrome_tools`).
- **Inject inline via the unified tool merge** (`apply_unified_tools`)
  only when the tool is request-specific or shouldn't be discoverable
  by category. Inline tools cost the full schema in the prompt every
  turn — use sparingly.

## Cross-turn limitation (current state, May 2026)

Tool mutations are per-request only. Each new user message restarts with
`[load_chrome_tools]` — discovery re-runs. Discovery is cheap
(server-side lookup, no LLM round-trip), so this is acceptable.
Cross-request persistence (`cx_conversation.dynamic_tool_state`) is the
Phase D-persist roadmap item in aidream's `TOOL_INJECTION_REFACTOR.md`.
**No extension changes are needed when it lands.** Do not work around
this limitation in extension code; let the server-side fix arrive.

## Failure modes

- **Silent: tool never advertised.** Usually means
  `client.state["browser-dom"]` is missing a flag the server gates on,
  or a category-routing rule excludes it. Check the request payload in
  DevTools Network tab; confirm state keys; then look at server logs.
- **Loud: schema rejection at provider.** Tool name has `:` instead of
  `__`. The wire format is `__`; canonical is `:`. See
  common-docs/systems/agents/agent-tools/STATE.md §1.
- **Silent: dispatch falls through to default.** Handler isn't keyed on
  the bare local name. Aliasing in `src/lib/tools/aliases.ts` must
  strip both `matrx-extend__` and bundle-style `<bundle>__` prefixes.

## Pointer

For the full topology and the parallel inbound channels, see
[`/Users/armanisadeghi/code/common-docs/systems/apps/extension/CHANNELS.md`](/Users/armanisadeghi/code/common-docs/systems/apps/extension/CHANNELS.md).
