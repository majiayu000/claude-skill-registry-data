---
name: build-ag-ui-agent
description: >-
  Load this skill when building or fixing the agent server behind an AG-UI canvas: an endpoint that
  calls an LLM with the canvas's frontend tools and streams AG-UI events over SSE. Trigger on "build
  the AG-UI server", "connect Claude to my canvas", "replace the mock agent".
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Needs uv and Python 3.11+, with fastapi, uvicorn, ag-ui-protocol 1.x and anthropic 1.9+
  installed by uv, plus network access to the Claude API and credentials the Anthropic SDK can
  find (ANTHROPIC_API_KEY or an `ant auth login` profile). Without credentials the server starts
  but every run ends in RUN_ERROR.
license: Apache-2.0
---

# Build the AG-UI agent server

The canvas owns what the user sees, and this server owns what the model sees. Most bugs in an
AG-UI backend come from mixing the two up: building the model's history out of the UI's messages,
or running a tool that belongs to the canvas. The work is done when every check in Procedure step 3
passes.

## Procedure

### 1. Start from the bundled server

Start from `${CLAUDE_SKILL_DIR}/assets/agent-server/` (`main.py`, `pyproject.toml`). Copy it to
`server/` beside the canvas's `web/`, keeping `agent/` (the mock, still the fastest way to test a
component), and run `uv run uvicorn main:app --port 8000` from `server/`, with the mock stopped.
The canvas's Vite proxy already points at that port, and `AGENT_ORIGIN` overrides it. It uses
Claude through the official `anthropic` SDK by default, with `AGENT_MODEL` defaulting to
`claude-opus-5-5`. For a different provider, keep the structure in the Rules below and swap only
`run_claude`.

### 2. Add a backend tool

This is for a tool the server runs itself, such as a database lookup the model needs before
choosing a component:

```python
async def lookup_orders(args: dict[str, Any]) -> str:
    region = args.get("region")
    if not isinstance(region, str):  # eager streaming: the API did not validate this
        return "error: region must be a string"
    return json.dumps(await db.orders_by_region(region))


BACKEND_TOOLS["lookup_orders"] = (
    "Order totals for one region. Call before showing order data.",
    {
        "type": "object",
        "properties": {"region": {"type": "string"}},
        "required": ["region"],
    },
    lookup_orders,
)
```

The loop runs it, streams `TOOL_CALL_RESULT`, and continues without a new run from the canvas. An
action with side effects the user should confirm first goes through
`ceh-ag-ui:add-human-approval`, not straight into `BACKEND_TOOLS`.

### 3. Verify

1. `uv run python -c "import main"` succeeds with no credentials, because the import makes no
   network call.
2. With credentials, run the canvas against the server:
   - "show me a table of three fruits and their prices" places `show_table` and then gets a short
     acknowledgement.
   - A follow-up question in the same thread works. That confirms the transcript was appended, not
     rebuilt.
   - Press Stop mid-render and send another message. The next run succeeds, which confirms rule 4.
3. Without credentials, test the loop with a scripted stand-in for `client.beta.messages.stream`
   that yields `content_block_*` events and a final message with `stop_reason: "tool_use"`. Then
   confirm that each request's `messages` starts with the previous request's `messages`.

### 4. Harden before deploying

- **Persist `THREADS`.** The template keeps them in memory, in one process (marked `less-code:`). A
  restart loses every conversation, and a second replica sees none of them. Store them keyed by
  `threadId` in Redis or Postgres. Store the transcript exactly as it was appended, because a
  thinking block changed on the way through storage is invalid.
- **CORS:** the dev canvas goes through the Vite proxy. A deployed canvas calls the server directly,
  so allow exactly its origin with FastAPI's `CORSMiddleware`, never `*` alongside credentials.
- **Auth:** decide who may start runs on a thread before exposing the endpoint. `threadId` is
  client-chosen, so a guessable id lets anyone read or continue someone else's conversation.

## Rules

### One request, one run

```
POST /agent  RunAgentInput{threadId, runId, messages, tools, state, resume}
  → RUN_STARTED
  → TEXT_MESSAGE_START / CONTENT… / END          (model text, streamed)
  → TOOL_CALL_START / ARGS… / END                 (model tool call, streamed)
  → TOOL_CALL_RESULT                               (only for tools the SERVER ran)
  → RUN_FINISHED          or          RUN_ERROR    (exactly one, always last)
```

- **Every run ends with exactly one `RUN_FINISHED` or `RUN_ERROR`.** A stream that simply stops
  leaves the canvas spinning. The template wraps the whole loop, so any exception becomes
  `RUN_ERROR`, and nothing follows it.
- **Stream as you go.** Map each model content block onto the matching AG-UI event as it arrives
  (`content_block_start`, then `delta`, then `stop`). Take each index's block kind from its
  `content_block_start` event.

### The six rules

1. **Keep the model's own transcript per thread, and append only what is new.** AG-UI messages are
   the UI's view. They carry no thinking blocks and are shaped differently from provider messages.
   Rebuilding the provider history from them on every run edits the past: it drops Claude's
   thinking blocks (which breaks the preserved-thinking check on current models) and restarts the
   prompt cache every time. The template stores `Thread.transcript` keyed by `threadId`, appends
   the final `content` of each response unchanged, and folds in only unseen AG-UI message ids.
   Those are new user text and the canvas's tool results.
2. **Pass the canvas's tools through, and never run them.** `run.tools` holds the catalogue. Send
   them to the model as tools. When the model calls one, stream the call and **end the run**. The
   canvas validates the call, renders it, and starts the next run with a `role: "tool"` message.
3. **Answer every tool call in one user turn.** When the model calls a backend tool and a frontend
   tool in the same turn, run the backend one now, stream its `TOOL_CALL_RESULT`, and **hold** its
   `tool_result` (`Thread.held`). Send it together with the canvas's results on the next run.
   Splitting one turn's results across two user messages is rejected by the API.
4. **A call the canvas never answers still needs a result.** The user can press Stop, or type
   something new, before a component renders. On the next run, add an error `tool_result` for every
   call in `Thread.awaiting` that has no answer. Otherwise the transcript has an unpaired
   `tool_use` and every later request fails.
5. **The browser does not write the prompt.** Ignore `system` and `developer` messages from the
   client, and ignore assistant messages too, since the server produced those. The system prompt
   lives on the server. Treat `run.tools` descriptions and schemas as untrusted input. They shape
   what the model does, so a deployed server should accept only the catalogue it expects, for
   example by comparing tool names against an allowlist.
6. **Styling never enters the prompt.** The system prompt tells the model the app fixes how
   components look. The canvas strips anything outside a schema anyway, but a model that keeps
   trying to style wastes turns.

### Claude-specific choices in the template

The template follows `claude-api` defaults. When changing them, check that skill's current guidance
rather than recalling it:

- **Streaming with `max_tokens=64000`, `effort: "medium"` set explicitly.** The default effort
  differs by model. Use `low` for a snappier chat and `high` for hard analysis.
- **`eager_input_streaming: True` on every tool**, so arguments stream into `TOOL_CALL_ARGS` while
  they are generated. The trade-off is that the API no longer validates the input. The canvas
  validates frontend calls with zod, and **backend handlers must validate their own input**.
- **`fallbacks: "default"`** with the `server-side-fallback-2026-07-01` beta, so a policy refusal
  is retried on a fallback model. `echoable()` keeps only the text from before a mid-output
  fallback block, as the API requires. A final `refusal` becomes `RUN_ERROR` with
  `code: "refusal"`.
- **Stop reasons, checked before acting:** `max_tokens` with a tool call means the arguments were
  truncated, so end with `RUN_ERROR` and do not hand them to the canvas. `pause_turn` means loop
  again. `tool_use` means the tool rules above apply.
- **No forced `tool_choice`.** Current Claude models reject `any` and `tool`. Steer toward
  components in the system prompt instead.

## Hands off to

- A backend tool whose side effects the user should confirm first: `ceh-ag-ui:add-human-approval`.
- A value the agent keeps updating while it works: `ceh-ag-ui:add-live-state-panel`.
- The canvas this server answers does not exist yet: `ceh-ag-ui:build-ag-ui`.
