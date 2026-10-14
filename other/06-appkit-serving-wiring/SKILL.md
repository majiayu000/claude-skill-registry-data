---
name: 06-appkit-serving-wiring
description: >
  Wire a Databricks Model Serving or Agent endpoint into an existing AppKit project
  using the Serving plugin. Covers endpoint registration, app.yaml resource binding,
  streaming and invoke React hooks, conversation state management, agent response
  mapping, and server-side proxy patterns. PRD-independent patterns that apply to
  any AppKit + Serving app. Use after registering the Serving plugin via
  04-appkit-plugin-add. Triggers on "wire agent", "agent endpoint", "serving plugin",
  "agent UI", "chat interface", "connect agent", "model serving", "useServingStream",
  "useServingInvoke", "agent chat", "wire serving", "serving wiring".
license: Apache-2.0
compatibility: Requires Serving plugin registered via 04-appkit-plugin-add, Node.js v22+, Databricks CLI >= 0.295.0
allowed-tools: Bash(databricks:*) Bash(npm:*) Bash(curl:*) Bash(node:*) Read
clients: [ide_cli, genie_code]
bundle_resource: apps
deploy_verb: apps_deploy
deploy_note: >
  Serving wiring is source editing (server.ts plugin config, React hooks, optional proxy routes) —
  client-agnostic. IDE: `databricks serving-endpoints get/query --profile $PROFILE` for verification,
  `npm run build` gates locally, then `databricks apps deploy --profile $PROFILE`. Genie Code: run
  `serving-endpoints get/query` via `runDatabricksCli` (read-tier, omit `--profile`); local `npm run build`
  gates are an IDE convenience (skip — platform builds server-side); deploy per `03-appkit-deploy`
  (`runDatabricksCli` or SDK fallback). Verify the deployed app via browser or the OAuth-session test —
  `auth token` + raw Bearer `curl` is hard-blocked on Genie Code.
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.1.0"
  domain: apps
  role: serving-wiring
  standalone: false
  last_verified: "2026-06-02"
  volatility: medium
  upstream_sources:
    - name: "databricks-agent-skills/databricks-model-serving"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-model-serving/SKILL.md"
      relationship: "extended"
      last_synced: "2026-04-27"
      sync_commit: "manifest-v2-2026-04-22"
    - name: "databricks-agent-skills/databricks-apps"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-apps/SKILL.md"
      relationship: "extended"
      last_synced: "2026-04-27"
      sync_commit: "manifest-v2-2026-04-22"
---

# Wire Serving Endpoint into AppKit

Connect a Databricks Model Serving or Agent endpoint to an AppKit app using the Serving plugin. Build streaming chat UIs, single-shot query interfaces, or server-side proxy routes that post-process agent responses.

## When to Use

- Wiring a deployed Agent or Model Serving endpoint into an AppKit app
- Building a streaming chat interface for a conversational agent
- Adding a single-shot inference call to a page (classification, summarization, etc.)
- Post-processing agent responses server-side before sending to the frontend

**Not for registering the plugin.** Use `04-appkit-plugin-add` with [references/plugin-serving.md](../04-appkit-plugin-add/references/plugin-serving.md) to install and configure the Serving plugin first.
**Not for deploying.** Use `03-appkit-deploy` after wiring is complete.
**Not for deploying the agent itself.** The agent endpoint must already exist on Databricks Model Serving.

---

## Before You Begin

**Prerequisites — verify these before proceeding:**

1. Agent endpoint is deployed on Databricks Model Serving and in `READY` state
2. The Serving plugin is registered in `server/server.ts` (via `04-appkit-plugin-add`)
3. Endpoint added as an **app resource** with `CAN_QUERY` permission (via Databricks Apps UI or `app.yaml` resources)
4. `app.yaml` has `DATABRICKS_SERVING_ENDPOINT_NAME` with `valueFrom: serving-endpoint`
5. `npm run build` passes with the Serving plugin imported
6. `serving` export is available in your installed AppKit version (see [04-appkit-plugin-add/SKILL.md](../04-appkit-plugin-add/SKILL.md) Step 1b). If `typeof require('@databricks/appkit').serving === "undefined"`, stop here — read [references/custom-proxy-fallback.md](references/custom-proxy-fallback.md) and skip Step 3.

**Upstream docs (always check for latest):**

```bash
npx @databricks/appkit docs "serving"
```

> **Key architectural difference from Lakebase wiring:** The Serving plugin auto-registers HTTP routes (`/api/serving/:alias/invoke` and `/api/serving/:alias/stream`) via the plugin lifecycle — like the Genie plugin. You do NOT need `server.extend()` to create routes for basic invoke/stream calls. Use `server.extend()` only when you need a custom server-side proxy route that post-processes the agent's response (Step 6).

### Working in Genie Code (client routing)

All the **code** in this skill — plugin config, hooks, proxy routes — is written the same way on both clients. Only the toolchain commands and the deployed-app verification differ. `$APP_NAME` / `$PROFILE` / endpoint name resolve from `.vibecoding-state.md` when a prior phase wrote it (don't re-derive). Apply these substitutions:

| IDE/CLI (as written) | Genie Code substitution |
|----------------------|--------------------------|
| `databricks serving-endpoints get/query … --profile $PROFILE` (Step 1) | run via `runDatabricksCli` (read-tier, pre-approved), **omit `--profile`** |
| `npm run build` gates (Steps 3, 8) — "**You MUST run `npm run build`**" | **IDE-only** convenience — no local Node toolchain. Skip; the platform builds **server-side** on deploy and surfaces errors in `databricks apps logs <name>` |
| `npm run dev` | not available (and blocked pre-deploy: `serving()` needs platform-injected env) — verify on the deployed app |
| `npx @databricks/appkit docs "serving"` | npx absent (P9) — WebFetch https://databricks.github.io/appkit/docs/plugins/serving |
| `databricks auth token` + `curl -H "Authorization: Bearer …"` (Steps 9b/9c) | hard-blocked / raw Bearer rejected by the Apps OAuth gate → use **browser** (open the app URL, test chat) **or** the 3-hop OAuth `requests.Session()` test in `03-appkit-deploy` |
| `databricks apps deploy …` (Step 9a) | see the `03-appkit-deploy` deploy-routing contract (`runDatabricksCli`, else SDK `w.apps.deploy(... SNAPSHOT)`) |

Paths are relative to `apps_lakebase/$APP_NAME` — inside your git-cloned workshop project (`artifact_root`) on Genie Code, never the read-only `.assistant/skills` copy and never `/tmp`. See `skills/genie-code-environment` for the full manifest.

---

## Decision Defaults

When multiple approaches are valid, use these defaults. Override only if the use case demands it.

| Decision | Default | Rationale |
|----------|---------|-----------|
| Streaming or invoke? | `useServingStream` for agent chat; `useServingInvoke` for single-shot | Agents are typically slow — streaming gives progressive UX feedback |
| Single or multiple endpoints? | Single (reads `DATABRICKS_SERVING_ENDPOINT_NAME`) | Multi-endpoint via `endpoints: {}` config is an advanced pattern |
| Chat UI pattern | Scrollable message list + input box + streaming indicator | Most agent UIs are conversational |
| Conversation state | Client-side `useState<Message[]>` array | `useServingStream` is stateless; the app must manage history |
| Agent response mapping | Show raw text by default | Not all agents return structured data; see [references/agent-response-mapping.md](references/agent-response-mapping.md) for structured patterns |
| OBO auth | Always (AppKit default) | Per-user `CAN_QUERY` enforcement on the serving endpoint |
| Timeout | 120000ms (2 minutes) | Agent endpoints may be slow; configurable via `serving({ timeout })` |
| `npm run dev` before deploy? | No — `npm run build` only | Serving plugin may throw `ConfigurationError` when env vars are not set |
| Check endpoint schema first? | Yes — verify streaming support | Endpoints without an OpenAPI streaming schema produce `chunk: unknown` |

---

## Step 1: Verify Endpoint Access

Confirm the serving endpoint is reachable and in `READY` state before writing any code.

### 1a. Check Endpoint Status

```bash
databricks serving-endpoints get <endpoint-name> --profile $PROFILE --output json | jq '.state'
```

Expected output includes `"ready": "READY"`. If the endpoint is not ready, wait for it to finish provisioning before proceeding.

### 1b. Test with a Sample Query

```bash
databricks serving-endpoints query <endpoint-name> \
  --profile $PROFILE \
  --input '{"messages": [{"role": "user", "content": "Hello"}]}'
```

If this returns a valid response, the endpoint is accessible and the agent is functional.

### 1c. Automated Test Script

```bash
bash apps_lakebase/skills/06-appkit-serving-wiring/scripts/test-serving-endpoint.sh \
  --endpoint-name <endpoint-name> --profile $PROFILE
```

**Gate:** The endpoint responds with `READY` status and returns a non-empty response to the sample query.

---

## Step 2: Configure app.yaml

### 2a. Add the Serving Endpoint as an App Resource

The endpoint must be registered as a resource in the Databricks Apps UI or in the `app.yaml` resources section:

- **Resource key:** `serving-endpoint` (default)
- **Permission:** `CAN_QUERY`
- **Requirement:** Endpoint must be in `READY` state

If using the Databricks Apps UI: navigate to your app's settings, add a Model Serving Endpoint resource, select the endpoint, and grant `CAN_QUERY`.

### 2b. Add the Environment Variable

```yaml
env:
  - name: DATABRICKS_SERVING_ENDPOINT_NAME
    valueFrom: serving-endpoint
```

> **Critical — env var name mismatch:** The Databricks Apps platform injects `SERVING_ENDPOINT=<name>` via the resource binding, but the AppKit Serving plugin reads `DATABRICKS_SERVING_ENDPOINT_NAME`. You MUST explicitly declare the env var in `app.yaml` with the name `DATABRICKS_SERVING_ENDPOINT_NAME` and use `valueFrom: serving-endpoint` so the platform maps the resource value to the name the plugin expects.

### 2c. Local Development (.env)

For local dev, set the env var directly:

```env
DATABRICKS_SERVING_ENDPOINT_NAME=<your-endpoint-name>
```

Local dev also requires Databricks authentication (CLI profile or `DATABRICKS_HOST` + `DATABRICKS_TOKEN` in `.env`).

**Gate:** `app.yaml` contains the `DATABRICKS_SERVING_ENDPOINT_NAME` env var with `valueFrom: serving-endpoint`.

---

## Step 3: Register in server/server.ts

> **If `serving` is undefined in your installed AppKit version**, stop here and read [references/custom-proxy-fallback.md](references/custom-proxy-fallback.md) instead of proceeding with Step 3. The bundler will silently accept a nonexistent `serving` import and fail at client build or runtime.

### 3a. Single Endpoint (Default)

```typescript
import { createApp, server, serving } from "@databricks/appkit";

await createApp({
  plugins: [
    server(),
    serving(),
  ],
});
```

With no configuration, the plugin reads `DATABRICKS_SERVING_ENDPOINT_NAME` from the environment and registers it under the `default` alias. Routes are auto-registered at `/api/serving/invoke` and `/api/serving/stream`.

### 3b. Multiple Endpoints with Aliases

```typescript
await createApp({
  plugins: [
    server(),
    serving({
      endpoints: {
        agent:      { env: "DATABRICKS_SERVING_ENDPOINT_NAME" },
        classifier: { env: "DATABRICKS_CLASSIFIER_ENDPOINT_NAME" },
      },
      timeout: 120000,
    }),
  ],
});
```

Each alias gets its own route pair: `/api/serving/agent/invoke`, `/api/serving/agent/stream`, etc.

### 3c. Targeting a Specific Model

If the endpoint serves multiple models, bypass traffic routing:

```typescript
serving({
  endpoints: {
    agent: {
      env: "DATABRICKS_SERVING_ENDPOINT_NAME",
      servedModel: "my-agent-v2",
    },
  },
});
```

> **Unlike Lakebase wiring, no `server.extend()` routes are needed here.** The plugin auto-registers the HTTP endpoints. The `server.extend()` pattern is only needed if you want a custom proxy route (Step 6).

**Gate:** `npm run build` passes with the `serving()` plugin imported and configured.

---

## Step 4: Wire Frontend — Streaming Chat

**You MUST read [references/chat-ui-patterns.md](references/chat-ui-patterns.md)** for the full conversation state management pattern before building a chat UI.

### 4a. Basic Streaming Hook

```tsx
import { useServingStream } from "@databricks/appkit-ui/react";

function AgentChat() {
  const { stream, chunks, streaming, error, reset } = useServingStream(
    { messages: [{ role: "user", content: userInput }] },
    {
      alias: "agent",
      onComplete: (finalChunks) => {
        console.log("Agent done:", finalChunks.length, "chunks");
      },
    },
  );

  return (
    <>
      <button onClick={stream} disabled={streaming}>Ask Agent</button>
      <button onClick={reset}>Clear</button>
      {chunks.map((c, i) => <pre key={i}>{JSON.stringify(c)}</pre>)}
      {error && <p className="text-red-600">{error}</p>}
    </>
  );
}
```

### 4b. Conversation State Management

`useServingStream` is **stateless** — it doesn't track history across calls. For multi-turn chat, manage messages in `useState` and pass the full array on each request:

```tsx
const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);

const { stream, chunks, streaming, error, reset } = useServingStream(
  {
    messages: [
      ...messages,
      { role: "user", content: currentInput },
    ],
  },
  {
    alias: "agent",
    onComplete: (finalChunks) => {
      const text = finalChunks
        .map((c: any) => c.choices?.[0]?.delta?.content ?? "")
        .join("");
      setMessages((prev) => [
        ...prev,
        { role: "user", content: currentInput },
        { role: "assistant", content: text },
      ]);
      reset();
    },
  },
);
```

Key rules:
- Pass the **full conversation history** on every call so the agent has context
- Append the assistant message **in `onComplete`**, not during streaming
- Call `reset()` after capturing the response to clear chunks for the next turn
- For long conversations, consider a sliding window to stay within token limits

> **Request body timing:** The first argument to `useServingStream` is the request body sent when `stream()` is called. Verify the hook re-reads this argument at call time, not at mount time. If the messages array appears stale (always sends the initial empty array), use a `useRef` to hold current messages — see [references/chat-ui-patterns.md](references/chat-ui-patterns.md) for the `useRef` fallback pattern. Test multi-turn early: send two messages and confirm the second request includes the first exchange.

### 4c. Streaming Chunk Format

Databricks emits streaming chunks in **two different shapes** depending on how the endpoint was deployed:

- **Databricks Responses API** (agents deployed via `databricks.agents.deploy()` with `ResponsesAgent`): `{ type: "response.output_text.delta", delta: "..." }`
- **OpenAI Chat Completion** (custom Model Serving, OpenAI-compatible pyfunc): `chunk.choices[0].delta.content`

A parser that reads only `choices[0].delta.content` will silently produce empty output against a Responses-API endpoint. Before writing the parser, **read [references/sse-format-patterns.md](references/sse-format-patterns.md)** for the `curl` pre-deploy format test and a dual-format parser you can copy directly.

Minimal dual-format extractor (use against both endpoint types):

```typescript
function extractDelta(chunk: any): string {
  if (chunk.type === "response.output_text.delta") return chunk.delta ?? "";
  return chunk.choices?.[0]?.delta?.content ?? "";
}
```

For the full SSE reader (buffering, `[DONE]` handling, unknown-chunk warnings, and the `curl` pre-deploy format test), read [references/sse-format-patterns.md](references/sse-format-patterns.md).

**Gate:** The streaming chat component renders in the browser with `npm run build` succeeding. Full runtime testing happens after deployment (Step 9).

---

## Step 5: Wire Frontend — Invoke (Optional)

For single-shot queries where streaming is unnecessary:

```tsx
import { useServingInvoke } from "@databricks/appkit-ui/react";

function AgentQuery() {
  const { invoke, data, loading, error } = useServingInvoke(
    { messages: [{ role: "user", content: "Summarize Q3 sales" }] },
    { alias: "agent" },
  );

  return (
    <>
      <button onClick={invoke} disabled={loading}>Run</button>
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
      {error && <p className="text-red-600">{error}</p>}
    </>
  );
}
```

`useServingInvoke` returns typed `data` when the endpoint has an OpenAPI response schema. The `invoke()` function returns a promise with the response data (or `null` on error), so you can also `await` it.

**Gate:** `npm run build` passes.

---

## Step 6: Server-Side Proxy (Optional)

Use `server.extend()` when you need to post-process agent responses before sending them to the frontend — e.g., extracting structured data from tool calls, adding business logic, or chaining with other plugins.

### 6a. Proxy Route Pattern

```typescript
const AppKit = await createApp({
  plugins: [server({ autoStart: false }), serving()],
});

AppKit.server.extend((app) => {
  app.post("/api/ask-agent", async (req, res) => {
    try {
      const result = await AppKit.serving("agent")
        .asUser(req)
        .invoke({ messages: req.body.messages });

      // Post-process the result here (see Step 7)
      res.json(result);
    } catch (err) {
      console.warn(`[Serving] /api/ask-agent error: ${err}`);
      res.status(500).json({ error: "Agent request failed" });
    }
  });
});

await AppKit.server.start();
```

> **Gotcha — `autoStart: false` is required** when using `server.extend()`. Without it, the server starts before `extend()` runs and routes are never registered. Same pattern as Lakebase wiring.

> **Local dev note:** In development mode (`NODE_ENV=development`), if `.asUser(req)` is called without a user token (no `x-forwarded-access-token` header), AppKit logs a warning and skips user impersonation — the operation runs with default credentials instead. This is expected behavior during local development; the warning is not an error.

### 6b. Streaming Proxy

```typescript
app.post("/api/ask-agent/stream", async (req, res) => {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");

  try {
    for await (const chunk of AppKit.serving("agent").asUser(req).stream({
      messages: req.body.messages,
    })) {
      res.write(`data: ${JSON.stringify(chunk)}\n\n`);
    }
    res.write("data: [DONE]\n\n");
    res.end();
  } catch (err) {
    res.write(`data: ${JSON.stringify({ error: String(err) })}\n\n`);
    res.end();
  }
});
```

**Gate:** `npm run build` passes with the extended server routes.

### 6c. Custom Proxy Fallback (When `serving` Is Not Exported)

If the Step 1b check in `04-appkit-plugin-add` returned `typeof serving === "undefined"`, replace Steps 3–5 with a custom proxy. The full pattern lives in [references/custom-proxy-fallback.md](references/custom-proxy-fallback.md); the three pieces agents most commonly get wrong are inlined here.

**Auth — use `config.authenticate(headers)`, NOT `config.getToken()`:**

```typescript
import { getExecutionContext } from "@databricks/appkit";

async function getServingHeaders() {
  const ctx = getExecutionContext();
  const config = ctx.client.config;
  await config.ensureResolved();
  const host = (config.host ?? "").replace(/\/$/, "");
  const h = new Headers();
  await config.authenticate(h);
  h.set("Content-Type", "application/json");
  const out: Record<string, string> = {};
  h.forEach((v, k) => { out[k] = v; });
  return { host, headers: out };
}
```

> **Anti-patterns that will fail at deploy time:**
> - `config.getToken()` — method does not exist on AppKit `Config`.
> - `process.env.DATABRICKS_HOST` directly — may lack `https://`; use `config.host` instead.

**Payload — transform `messages` → `input`:**

```typescript
function buildAgentPayload(body: any, stream = false) {
  return {
    input: body.messages ?? body.input ?? [],
    ...(stream ? { stream: true } : {}),
    ...(body.context ? { context: body.context } : {}),
  };
}
```

Sending `{messages: ...}` directly produces `400: Model is missing inputs ['input']`.

**Routes:** mirror the plugin surface (`/api/serving/invoke`, `/api/serving/stream`) so the frontend hooks in Step 4 work unchanged. See [references/custom-proxy-fallback.md](references/custom-proxy-fallback.md) for the full Express handlers including SSE passthrough.

**Gate:** `npm run build` passes with the custom proxy routes.

---

## Step 7: Map Agent Output to Structured UI (Optional)

**You MUST read [references/agent-response-mapping.md](references/agent-response-mapping.md)** before implementing this step. It covers three patterns:

1. **Structured Output Schema** — endpoint defines an output schema; `useServingInvoke` returns typed data
2. **Tool Results Extraction** — agent uses tools that return JSON/tabular data; extract and map server-side
3. **Text Parsing** — regex extraction from free-text responses (last resort)

This step generalizes the mapper pattern from `agentic-framework/agents/agent-ui-wiring-prompt.md`, where booking agent Genie results were mapped to `Listing` objects. The reference file provides PRD-independent templates.

Choose based on your agent's output:

| Agent Output Type | Pattern | Where |
|-------------------|---------|-------|
| Typed JSON (OpenAPI schema) | Pattern 1 | Frontend only |
| Tool call results (SQL, API) | Pattern 2 | Server proxy (Step 6) + frontend |
| Free text with embedded data | Pattern 3 | Server proxy (Step 6) + frontend |
| Conversational text only | Skip this step | Frontend (Step 4 or 5) |

---

## Step 8: Build Gate

**You MUST run `npm run build` and fix all errors before proceeding to deployment.**

```bash
cd apps_lakebase/$APP_NAME
npm run build
```

This validates all TypeScript, imports, and bundling without executing the code.

> **Do NOT run `npm run dev` at this step** if you haven't deployed yet. The `serving()` plugin may throw `ConfigurationError` when `DATABRICKS_SERVING_ENDPOINT_NAME` is not set. These env vars are injected by the platform after the serving endpoint resource is bound. Use `npm run build` only for local validation. Runtime testing with `npm run dev` is available after deployment or after configuring `.env` with connection details.

### What to Verify at This Step

- Zero TypeScript errors
- All `@databricks/appkit` and `@databricks/appkit-ui` imports resolve
- `serving()` plugin configuration compiles
- Frontend hooks (`useServingStream`, `useServingInvoke`) compile with correct types
- Any `server.extend()` routes (Step 6) compile

---

## Step 9: Deploy and Test

### 9a. Deploy

Use `03-appkit-deploy` to deploy the app:

```bash
databricks apps deploy --profile $PROFILE
```

### 9b. Verify Auto-Registered Endpoints

After deployment, test the Serving plugin's auto-registered endpoints:

```bash
APP_URL=$(databricks apps get $APP_NAME --profile $PROFILE --output json | jq -r '.url')
TOKEN=$(databricks auth token --profile $PROFILE --output json | jq -r '.access_token')

curl -s -X POST "${APP_URL}/api/serving/invoke" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}' | jq .
```

For named aliases, use `/api/serving/<alias>/invoke` instead.

> **Client note — Genie Code:** this `auth token` + raw Bearer `curl` does not work (`auth token` hard-blocked; AppKit's OAuth gate rejects raw Bearer → 401). Verify instead via **browser** (open the app URL and test the chat UI) or the **3-hop OAuth `requests.Session()`** pattern in `03-appkit-deploy` "Testing Deployed App APIs", then assert on `databricks apps logs <name>`.

### 9c. Automated Test

```bash
bash apps_lakebase/skills/06-appkit-serving-wiring/scripts/test-serving-endpoint.sh \
  --base-url "$APP_URL" \
  --alias "default"
```

### 9d. Verify Frontend

Open the app URL in a browser and test:
- The chat input accepts a message
- Streaming responses appear progressively
- Conversation history persists across turns
- Error states display correctly when the agent fails
- **A domain-specific data question returns data (not just a greeting).** If the agent greets but returns nothing for a question that should hit a tool / Genie / SQL (e.g., "how many bookings last month?"), the tool-calling path is broken. AI Playground may still work because it uses OBO; the app's SP does not. Check Genie Space / warehouse / UC grants via [09-simple-agent-scaffold/references/post-deploy-permissions.md](../../../data_product_accelerator/skills/genai-agents/09-simple-agent-scaffold/references/post-deploy-permissions.md).

**Gate:** The agent responds to queries via the deployed app's UI and API endpoints.

---

## Gotchas (Summary)

Detailed callouts are embedded inline at the relevant step. This table is a compact reference.

| Gotcha | Fix | Step |
|--------|-----|------|
| Serving plugin crashes without `DATABRICKS_SERVING_ENDPOINT_NAME` | Expected before first deploy; use `npm run build` only | 3, 8 |
| Platform injects `SERVING_ENDPOINT` but AppKit reads `DATABRICKS_SERVING_ENDPOINT_NAME` | Name the env var explicitly in `app.yaml` with `valueFrom: serving-endpoint` | 2 |
| Streaming chunks typed as `unknown` when endpoint lacks OpenAPI streaming schema | Use `useServingInvoke` instead, or cast chunks after logging shape | 4 |
| `useServingStream` is stateless — no built-in conversation history | Manage message array in `useState`; pass full history on each call | 4 |
| Endpoint not in `READY` state | Verify via `databricks serving-endpoints get <name>` before wiring | 1 |
| `autoStart: true` on hooks fires on mount | Only use for demo/single-shot; omit for interactive chat | 4, 5 |
| Custom `server.extend()` routes need `autoStart: false` on `server()` plugin | Same pattern as Lakebase wiring — call `AppKit.server.start()` after extend | 6 |
| Type generation fails silently when endpoint env var not set | Generated types fall back to `unknown`; endpoint still usable, just untyped | 3 |
| 403 on invoke/stream endpoints | User lacks `CAN_QUERY` on the serving endpoint; verify app resource binding | 2, 9 |
| `npm run dev` crashes without env vars | Use `npm run build` only before first deploy; after deploy, configure `.env` | 8 |
| Agent timeout (no response within 120s) | Increase `timeout` in `serving()` config or simplify the prompt | 3 |
| `400: Model is missing inputs ['input']` when calling agent endpoint | Payload sent `{"messages":[...]}` but agent expects `{"input":[...]}`. The plugin normalizes this; a custom proxy must transform — see [references/custom-proxy-fallback.md](references/custom-proxy-fallback.md) | 3, 6c |
| Stream returns 200, UI stays blank | Parser reads `choices[0].delta.content` but endpoint emits Databricks Responses API (`type: "response.output_text.delta"`). Use dual parser from [references/sse-format-patterns.md](references/sse-format-patterns.md) | 4 |
| `TypeError: Failed to parse URL` when calling endpoint from a custom proxy | Using `process.env.DATABRICKS_HOST` which may lack `https://`. Use `config.host` from `getExecutionContext().client.config` — see [references/custom-proxy-fallback.md](references/custom-proxy-fallback.md) | 6c |
| `TypeError: config.getToken is not a function` in custom proxy auth | AppKit `Config` does not expose `getToken()`. Use `await config.authenticate(headers)` — see [references/custom-proxy-fallback.md](references/custom-proxy-fallback.md) | 6c |
| `serving` export missing in older AppKit versions | Run Step 1b check (`node -e ...`) BEFORE importing; fall back to Step 6c custom proxy if undefined | 3, 6c |

---

## Anti-Patterns (Things Agents Reach For That Fail)

| Anti-Pattern | Why It Fails | Correct Approach |
|--------------|--------------|------------------|
| Import `serving` without verifying the export | tsdown bundles silently; fails only at tsc/runtime | Run Step 1b `node -e` check first |
| Guess the SDK auth API (`getToken`, raw env vars) | AppKit `Config` exposes only `authenticate(headers)` | Step 6c `getServingHeaders` |
| Forward `{messages:...}` straight to an Agent endpoint | Agent expects `{input:...}` at top level | Step 6c `buildAgentPayload` |
| Parse only `choices[0].delta.content` | Databricks Responses API emits `response.output_text.delta` | Step 4c dual parser |
| `rm -f package-lock.json && npm install` to "fix" deps | Picks up local proxy URLs, breaks platform install | `--package-lock-only`, or delete and let platform resolve |
| Delete the app to "start fresh" | New SP loses ownership of Lakebase schemas | Fix the deploy; DROP+recreate schemas only as last resort |
| Ship after one "Hello" response | Tool-calling path may still be broken | Test a real domain question before declaring done |

---

## Quick Reference

| Task | Command / Pattern |
|------|------------------|
| Check live Serving docs | `npx @databricks/appkit docs "serving"` |
| Check endpoint status | `databricks serving-endpoints get <name> --profile $PROFILE` |
| Build gate | `npm run build` (must pass with zero errors) |
| Test invoke endpoint (after deploy) | `curl -s -X POST "$APP_URL/api/serving/invoke" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"messages":[{"role":"user","content":"Hello"}]}'` |
| Test with script (after deploy) | `bash apps_lakebase/skills/06-appkit-serving-wiring/scripts/test-serving-endpoint.sh --base-url "$APP_URL"` |
| Frontend streaming hook | `useServingStream({ messages }, { alias: "agent" })` |
| Frontend invoke hook | `useServingInvoke({ messages }, { alias: "agent" })` |
| Server-side invoke | `AppKit.serving("agent").asUser(req).invoke({ messages })` |
| Server-side stream | `for await (const chunk of AppKit.serving("agent").stream({ messages }))` |

---

## See Also

- Upstream platform skills: [`databricks-model-serving`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-model-serving) and [`databricks-apps`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-apps) (both tracked in `upstream_sources`).
- AppKit Serving plugin docs: [databricks.github.io/appkit/docs/plugins/serving](https://databricks.github.io/appkit/docs/plugins/serving)

