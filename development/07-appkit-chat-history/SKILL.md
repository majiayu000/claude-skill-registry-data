---
name: 07-appkit-chat-history
description: >
  Add persistent chat history to an AppKit application using the Lakebase plugin
  and the Serving plugin (both AppKit-native, no Vercel AI SDK). Covers database
  schema, session auth middleware, a server-side proxy route that streams from
  `AppKit.serving("agent").asUser(req).stream()` while persisting assistant
  messages and capturing MLflow `trace_id`, the history API routes, a history
  sidebar, and ephemeral-mode fallback. Use when asked to persist conversations,
  add chat history, save messages, or build a conversation sidebar. Triggers on
  "chat history", "save conversations", "persistent chat", "conversation sidebar",
  "message storage", "save messages", "ephemeral chat".
license: Apache-2.0
compatibility: Requires 05-appkit-lakebase-wiring and 06-appkit-serving-wiring complete, Node.js v22+, Databricks CLI >= 0.295.0
allowed-tools: Bash(databricks:*) Bash(npm:*) Bash(curl:*) Bash(node:*) Read
clients: [ide_cli, genie_code]
bundle_resource: apps
deploy_verb: apps_deploy
deploy_note: >
  Chat-history persistence is source editing (server.ts DDL/routes, sidebar, hooks) — client-agnostic.
  The `chat` schema/table DDL runs **server-side on app startup** under the SP (RULE_10 Deploy-First) on both
  clients — never run it locally. IDE: `npm run build`/`npm test` gates, `databricks bundle validate
  --profile $PROFILE`, then `databricks apps deploy --profile $PROFILE`. Genie Code: local `npm` gates are an
  IDE convenience (server-side build on deploy); run `bundle validate` via `runDatabricksCli` (omit
  `--profile`; `--target dev` if targetless blocked); deploy per `03-appkit-deploy`. `apps validate` is
  hard-blocked and (per Step 9) unsafe for Lakebase apps — skip on both clients. Verify via browser + logs.
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.2.0"
  domain: apps
  role: chat-history
  standalone: false
  last_verified: "2026-06-02"
  volatility: medium
  upstream_sources:
    - name: "databricks-agent-skills/databricks-lakebase"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-lakebase/SKILL.md"
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

# Add Persistent Chat History to an AppKit Application

Persist chat conversations in Lakebase so users can revisit past conversations, using AppKit-native primitives only: `AppKit.lakebase.query()` for persistence, `AppKit.serving("agent").asUser(req).stream()` for the agent stream, and `server.extend()` with `autoStart: false` for the proxy route.

**No Vercel AI SDK, no `@databricks/ai-sdk-provider`, no `streamText`.** This skill builds on top of the agent wiring already established in [06-appkit-serving-wiring](../06-appkit-serving-wiring/SKILL.md).

## When to Use

- Adding persistent conversation storage to an AppKit chat interface built with `useServingStream`
- Building a sidebar with conversation history
- Supporting ephemeral mode (graceful degradation when Lakebase is unavailable)
- Capturing `trace_id` server-side for later feedback logging (see [08-appkit-feedback](../08-appkit-feedback/SKILL.md))

**Not for agent streaming fundamentals.** Use [06-appkit-serving-wiring](../06-appkit-serving-wiring/SKILL.md) to wire `useServingStream` and the base `/api/serving/:alias/stream` route first.

**Not for plugin registration.** Use [04-appkit-plugin-add](../04-appkit-plugin-add/SKILL.md) + [05-appkit-lakebase-wiring](../05-appkit-lakebase-wiring/SKILL.md) to register the Lakebase plugin and declare bundle resources first.

---

## Prerequisites

Verify all of these before proceeding:

1. Lakebase plugin registered in `server/server.ts` with bundle resources deployed (see [05-appkit-lakebase-wiring](../05-appkit-lakebase-wiring/SKILL.md))
2. Serving plugin registered in `server/server.ts` with a working agent endpoint (see [06-appkit-serving-wiring](../06-appkit-serving-wiring/SKILL.md))
3. `useServingStream` renders a basic chat UI that works end-to-end
4. App deployed at least once so the Service Principal exists and can create schemas
5. `AppKit.server` is constructed with `server({ autoStart: false })` and `AppKit.server.start()` is called after `AppKit.server.extend(...)`

**Upstream docs (always check for latest):**

```bash
npx @databricks/appkit docs "lakebase"
npx @databricks/appkit docs "serving"
```

### Working in Genie Code (client routing)

Everything in this skill is **source editing + server-side code** (DDL, proxy route, sidebar, hooks) — written the same way on both clients. The DDL runs server-side on startup (Step 1) and is already client-agnostic. Only local gates and the deployed-app checks differ:

| IDE/CLI (as written) | Genie Code substitution |
|----------------------|--------------------------|
| `npm run build` / `npm test` gates (Steps 1–8) | **IDE-only** convenience — no local Node toolchain. Skip; the platform builds **server-side** on deploy, and the retry tests run in CI or post-clone where npm exists. Errors surface in `databricks apps logs <name>` |
| `npm run dev` | not available — verify on the deployed app |
| `npx @databricks/appkit docs …` | npx absent (P9) — WebFetch https://databricks.github.io/appkit/docs/plugins/ |
| `databricks bundle validate --profile $PROFILE` (Step 9) | run via `runDatabricksCli` (omit `--profile`; `--target dev` if a targetless validate is guardrail-blocked) — this is the canonical gate on both clients |
| `databricks apps validate` (Step 9) | hard-blocked **and** unsafe for Lakebase apps (boots locally) — skip on both clients, rely on `bundle validate` + server-side build logs |
| local `curl http://localhost:8000/api/…` gates (Steps 3, 7) | no local dev server — exercise the routes on the **deployed** app via browser, or the OAuth-session `requests.Session()` test in `03-appkit-deploy` |
| `databricks apps deploy …` | see the `03-appkit-deploy` deploy-routing contract (`runDatabricksCli`, else SDK `w.apps.deploy(... SNAPSHOT)`) |

Paths are relative to `apps_lakebase/$APP_NAME` — inside your git-cloned workshop project (`artifact_root`) on Genie Code, never the read-only `.assistant/skills` copy and never `/tmp`. See `skills/genie-code-environment` for the full manifest.

---

## Architecture

```
Browser (useServingStream or direct fetch)
  │
  ▼
AppKit Server — server.extend() proxy route /api/chat
  │
  ├─► AppKit.lakebase.query()                 (persist chat record, user message)
  │
  ├─► AppKit.serving("agent").asUser(req).stream({ messages })
  │      │
  │      └─ for await (chunk of stream):
  │         1. Forward chunk to client as SSE
  │         2. Accumulate assistant text via dual-format extractor
  │         3. Scan chunk for trace_id
  │
  └─► AppKit.lakebase.query()                 (INSERT assistant message + traceId on stream close)
```

This pattern extends the `server.extend()` streaming proxy already documented in [06-appkit-serving-wiring/SKILL.md](../06-appkit-serving-wiring/SKILL.md) Step 6b. The only additions are the Lakebase inserts and the text/traceId accumulators.

---

## Step 1: Create the Chat Schema

Add idempotent DDL after `createApp()` in `server/server.ts`. The `chat` schema is deliberately isolated from application data schemas so it doesn't collide with other tables.

> **RULE_10 — this DDL is intentionally in-app, not a bundle resource or a `psql` script.** `initChatSchema()` runs **server-side on every app startup** via `AppKit.lakebase.query()`, so the app's Service Principal owns the schema, tables, and indexes (the same Deploy-First Pattern as `05-appkit-lakebase-wiring` Step 1d). This is **client-agnostic** — it executes identically whether the app was deployed from an IDE or Genie Code, and there is **no client-side `psql`/DDL step**. Do not move it into `databricks.yml` or a setup script: idempotent `CREATE … IF NOT EXISTS` on startup is the correct, SP-owning pattern.

```typescript
async function initChatSchema() {
  try {
    await AppKit.lakebase.query(`CREATE SCHEMA IF NOT EXISTS chat`);

    await AppKit.lakebase.query(`
      CREATE TABLE IF NOT EXISTS chat."User" (
        id TEXT PRIMARY KEY NOT NULL,
        email VARCHAR(64) NOT NULL
      )
    `);

    await AppKit.lakebase.query(`
      CREATE TABLE IF NOT EXISTS chat."Chat" (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        title TEXT NOT NULL DEFAULT 'New chat',
        "userId" TEXT NOT NULL,
        visibility VARCHAR(10) NOT NULL DEFAULT 'private',
        "lastContext" JSONB
      )
    `);

    await AppKit.lakebase.query(`
      CREATE TABLE IF NOT EXISTS chat."Message" (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        "chatId" UUID NOT NULL REFERENCES chat."Chat"(id) ON DELETE CASCADE,
        role VARCHAR(20) NOT NULL,
        parts JSON NOT NULL DEFAULT '[]',
        attachments JSON NOT NULL DEFAULT '[]',
        "createdAt" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        "traceId" TEXT
      )
    `);

    await AppKit.lakebase.query(`
      CREATE TABLE IF NOT EXISTS chat."Vote" (
        "chatId" UUID NOT NULL REFERENCES chat."Chat"(id) ON DELETE CASCADE,
        "messageId" UUID NOT NULL REFERENCES chat."Message"(id) ON DELETE CASCADE,
        "isUpvoted" BOOLEAN NOT NULL,
        PRIMARY KEY ("chatId", "messageId")
      )
    `);

    await AppKit.lakebase.query(`
      CREATE INDEX IF NOT EXISTS idx_chat_user ON chat."Chat" ("userId", "createdAt" DESC)
    `);
    await AppKit.lakebase.query(`
      CREATE INDEX IF NOT EXISTS idx_message_chat ON chat."Message" ("chatId", "createdAt" ASC)
    `);

    console.log("[Chat] Schema initialized");
  } catch (err) {
    console.warn("[Chat] Schema init failed (may not have DB access):", err);
  }
}

await initChatSchema();
```

See [references/chat-schema.md](references/chat-schema.md) for the full ER diagram, per-column rationale, and optional Drizzle ORM migration path.

**Gate:** Schema init runs on startup. A subsequent `npm run build` passes, and deploying the app produces server logs containing `[Chat] Schema initialized`.

---

## Step 2: Add Auth Middleware

Add Express middleware to parse the OBO user identity once per request and attach it to `req.session`. This avoids calling a helper function inline in every route handler.

> **Header contract.** Databricks Apps sets four canonical user headers on every request:
>
> - `x-forwarded-email` — end user's email (the value AppKit and downstream agents use as the canonical user attribute)
> - `x-forwarded-preferred-username` — preferred username (often equals the email)
> - `x-forwarded-user` — stable workspace user id
> - `x-forwarded-access-token` — downscoped OBO token (only present when `user_api_scopes` is declared)
>
> `x-forwarded-user-info` is **not** a canonical Databricks Apps header and must not be used. Earlier internal patterns assumed a JSON-blob header existed; it does not. Read the canonical headers above directly.

```typescript
interface AppSession {
  userId: string;
  email: string;
  name?: string;
  authenticated: boolean;
}

declare global {
  namespace Express {
    interface Request {
      session?: AppSession;
    }
  }
}

function readCanonicalUserHeaders(req: import("express").Request) {
  const email = req.headers["x-forwarded-email"];
  const preferred = req.headers["x-forwarded-preferred-username"];
  const user = req.headers["x-forwarded-user"];

  const pick = (h: string | string[] | undefined): string | undefined =>
    typeof h === "string" && h.length > 0 ? h : undefined;

  return {
    email: pick(email),
    preferredUsername: pick(preferred),
    userId: pick(user),
  };
}

function authMiddleware(
  req: import("express").Request,
  _res: import("express").Response,
  next: import("express").NextFunction,
) {
  const canonical = readCanonicalUserHeaders(req);
  if (canonical.email || canonical.userId) {
    // userId persists in Lakebase as TEXT — prefer the email so it lines up
    // with MLflow AssessmentSource.source_id. Fall back to x-forwarded-user.
    const userId = canonical.email ?? canonical.userId!;
    const email = canonical.email ?? canonical.preferredUsername ?? "unknown@local";
    req.session = {
      userId,
      email,
      name: canonical.preferredUsername,
      authenticated: true,
    };
  } else {
    req.session = {
      userId: process.env.DEV_USER_EMAIL ?? "local-dev-user",
      email: process.env.DEV_USER_EMAIL ?? "dev@local",
      authenticated: false,
    };
  }
  next();
}

function requireAuth(
  req: import("express").Request,
  res: import("express").Response,
  next: import("express").NextFunction,
) {
  if (!req.session) {
    return res.status(401).json({ error: "Authentication required" });
  }
  next();
}

function requireChatAccess(
  req: import("express").Request,
  res: import("express").Response,
  next: import("express").NextFunction,
) {
  const chatId = req.params.chatId;
  if (!chatId) return next();
  AppKit.lakebase
    .query(`SELECT "userId", visibility FROM chat."Chat" WHERE id = $1`, [chatId])
    .then((result) => {
      if (result.rows.length === 0) return res.status(404).json({ error: "Chat not found" });
      const chat = result.rows[0];
      if (chat.userId !== req.session?.userId && chat.visibility !== "public") {
        return res.status(403).json({ error: "Access denied" });
      }
      next();
    })
    .catch(() => next());
}
```

Apply the middleware to all chat routes:

```typescript
AppKit.server.extend((app) => {
  app.use("/api/chat", authMiddleware, requireAuth);
  app.use("/api/history", authMiddleware, requireAuth);
  app.use("/api/messages", authMiddleware, requireAuth);
  app.use("/api/feedback", authMiddleware, requireAuth);
  app.use("/api/session", authMiddleware);
});
```

Route handlers then read `req.session.userId` instead of calling a helper.

See [references/session-auth.md](references/session-auth.md) for the full middleware reference, OBO header format, and access control rules.

**Gate:** `npm run build` passes with the middleware imports. Hitting any protected route without the canonical `x-forwarded-email` / `x-forwarded-user` headers (i.e. running outside the Databricks Apps platform) returns the local-dev fallback identity.

---

## Step 3: Add History API Routes

These routes power the sidebar and message loading. All use `AppKit.lakebase.query()` — no ORM.

```typescript
AppKit.server.extend((app) => {
  async function ensureUser(req: import("express").Request) {
    const userId = req.session!.userId;
    const email = req.session!.email;
    await AppKit.lakebase.query(
      `INSERT INTO chat."User" (id, email) VALUES ($1, $2) ON CONFLICT (id) DO NOTHING`,
      [userId, email],
    );
    return userId;
  }

  app.get("/api/history", async (req, res) => {
    try {
      const userId = await ensureUser(req);
      const limit = Math.min(parseInt(req.query.limit as string) || 20, 100);
      const startingAfter = req.query.starting_after as string | undefined;
      const endingBefore = req.query.ending_before as string | undefined;

      let sql: string;
      let params: unknown[];

      if (startingAfter) {
        sql = `SELECT id, title, "createdAt", visibility
               FROM chat."Chat"
               WHERE "userId" = $1
                 AND "createdAt" < (SELECT "createdAt" FROM chat."Chat" WHERE id = $2)
               ORDER BY "createdAt" DESC
               LIMIT $3`;
        params = [userId, startingAfter, limit + 1];
      } else if (endingBefore) {
        sql = `SELECT * FROM (
                 SELECT id, title, "createdAt", visibility
                 FROM chat."Chat"
                 WHERE "userId" = $1
                   AND "createdAt" > (SELECT "createdAt" FROM chat."Chat" WHERE id = $2)
                 ORDER BY "createdAt" ASC
                 LIMIT $3
               ) sub ORDER BY "createdAt" DESC`;
        params = [userId, endingBefore, limit + 1];
      } else {
        sql = `SELECT id, title, "createdAt", visibility
               FROM chat."Chat"
               WHERE "userId" = $1
               ORDER BY "createdAt" DESC
               LIMIT $2`;
        params = [userId, limit + 1];
      }

      const result = await AppKit.lakebase.query(sql, params);
      const hasMore = result.rows.length > limit;
      const data = hasMore ? result.rows.slice(0, limit) : result.rows;

      res.json({ data, hasMore });
    } catch (err) {
      console.warn("[History] Failed, returning 204 for ephemeral mode:", err);
      res.status(204).end();
    }
  });

  app.get("/api/messages/:chatId", requireChatAccess, async (req, res) => {
    try {
      const result = await AppKit.lakebase.query(
        `SELECT id, role, parts, "traceId", "createdAt"
         FROM chat."Message"
         WHERE "chatId" = $1
         ORDER BY "createdAt" ASC`,
        [req.params.chatId],
      );
      res.json({ data: result.rows, source: "live" });
    } catch (err) {
      console.warn("[Messages] Failed:", err);
      res.json({ data: [], source: "mock" });
    }
  });

  app.delete("/api/chat/:chatId", async (req, res) => {
    try {
      const userId = req.session!.userId;
      const chat = await AppKit.lakebase.query(
        `SELECT "userId" FROM chat."Chat" WHERE id = $1`,
        [req.params.chatId],
      );
      if (chat.rows.length === 0 || chat.rows[0].userId !== userId) {
        return res.status(404).json({ error: "Chat not found" });
      }
      await AppKit.lakebase.query(`DELETE FROM chat."Chat" WHERE id = $1`, [req.params.chatId]);
      res.json({ success: true });
    } catch (err) {
      console.error("[Delete] Failed:", err);
      res.status(500).json({ error: "Failed to delete chat" });
    }
  });

  app.patch("/api/chat/:chatId/visibility", async (req, res) => {
    const { visibility } = req.body;
    if (!["public", "private"].includes(visibility)) {
      return res.status(400).json({ error: "visibility must be 'public' or 'private'" });
    }
    try {
      const userId = req.session!.userId;
      const chat = await AppKit.lakebase.query(
        `SELECT "userId" FROM chat."Chat" WHERE id = $1`,
        [req.params.chatId],
      );
      if (chat.rows.length === 0 || chat.rows[0].userId !== userId) {
        return res.status(403).json({ error: "Only the chat owner can change visibility" });
      }
      await AppKit.lakebase.query(
        `UPDATE chat."Chat" SET visibility = $1 WHERE id = $2`,
        [visibility, req.params.chatId],
      );
      res.json({ success: true, visibility });
    } catch (err) {
      console.error("[Visibility] Failed:", err);
      res.status(500).json({ error: "Failed to update visibility" });
    }
  });

  app.get("/api/session", async (req, res) => {
    res.json({
      user: {
        id: req.session!.userId,
        email: req.session!.email,
        name: req.session?.name,
      },
      authenticated: req.session!.authenticated,
    });
  });
});
```

**Gate:**

```bash
curl -s "http://localhost:8000/api/history" \
  -H "x-forwarded-email: dev@local" \
  -H "x-forwarded-preferred-username: dev@local" \
  -H "x-forwarded-user: dev-user" | jq .
```

Returns `{ data: [], hasMore: false }` initially. After a conversation is saved (Step 4), it shows up here.

---

## Step 4: Stream + Persist Assistant Message (AppKit-Native)

This is the only step that deviates significantly from the source pattern. Instead of the AI SDK's `streamText() + onFinish()`, use a `server.extend()` proxy over `AppKit.serving("agent").asUser(req).stream(...)` — the exact pattern from [06-appkit-serving-wiring/SKILL.md](../06-appkit-serving-wiring/SKILL.md) Step 6b, extended with Lakebase persistence and trace-ID capture.

> **Prerequisite — `autoStart: false` on the server plugin.** Your `createApp` must be declared as:
>
> ```typescript
> const AppKit = await createApp({
>   plugins: [
>     server({ autoStart: false }),
>     serving(),
>     lakebase(),
>   ],
> });
> ```
>
> The final `await AppKit.server.start()` call happens after all `server.extend(...)` blocks. Same pattern already in [06-appkit-serving-wiring](../06-appkit-serving-wiring/SKILL.md) Step 6a.

### 4a. Import the Chunk Helpers

Add to `server/server.ts` (or a new `server/chunk-helpers.ts`, since `tsdown unbundle: true` preserves relative imports — see [05-appkit-lakebase-wiring](../05-appkit-lakebase-wiring/SKILL.md) build system note):

```typescript
type Chunk = {
  type?: string;
  delta?: string;
  choices?: Array<{ delta?: { content?: string } }>;
  databricks_output?: { trace?: { info?: { trace_id?: string } } };
  trace_id?: string;
};

function extractDelta(chunk: Chunk): string {
  if (chunk.type === "response.output_text.delta" && typeof chunk.delta === "string") {
    return chunk.delta;
  }
  const openAiDelta = chunk.choices?.[0]?.delta?.content;
  if (typeof openAiDelta === "string") return openAiDelta;
  return "";
}

function extractTraceId(chunk: Chunk): string | null {
  const tid = chunk?.databricks_output?.trace?.info?.trace_id;
  if (typeof tid === "string") return tid;
  if (typeof chunk?.trace_id === "string") return chunk.trace_id;
  return null;
}
```

The `extractDelta` function is the same dual-format parser documented in [06-appkit-serving-wiring/references/sse-format-patterns.md](../06-appkit-serving-wiring/references/sse-format-patterns.md). The `extractTraceId` function is documented in detail in [08-appkit-feedback/references/trace-extraction.md](../08-appkit-feedback/references/trace-extraction.md) — feel free to import it from there once Step 1 of `08-appkit-feedback` is complete.

### 4b. The `/api/chat` Proxy Route

```typescript
AppKit.server.extend((app) => {
  // In-memory fallback for ephemeral mode (when Lakebase is unavailable).
  // Used by 08-appkit-feedback to look up traceId when DB lookup fails.
  const messageMetaStore = new Map<string, { chatId: string; traceId: string | null }>();

  let dbAvailable = true;
  async function dbQuery(sql: string, params: unknown[]) {
    if (!dbAvailable) return { rows: [] as any[] };
    try {
      return await AppKit.lakebase.query(sql, params);
    } catch (err) {
      console.warn("[Chat] DB query failed, entering ephemeral mode:", err);
      dbAvailable = false;
      return { rows: [] as any[] };
    }
  }

  app.post("/api/chat", async (req, res) => {
    const { id: chatId, messages } = req.body as {
      id?: string;
      messages: Array<{ role: string; content: string; id?: string }>;
    };
    const userId = req.session!.userId;

    if (!messages || !Array.isArray(messages)) {
      return res.status(400).json({ error: "messages array required" });
    }

    // 1. Create chat record if new, persist user message
    if (chatId) {
      const existing = await dbQuery(`SELECT id FROM chat."Chat" WHERE id = $1`, [chatId]);
      if (existing.rows.length === 0) {
        await dbQuery(
          `INSERT INTO chat."User" (id, email) VALUES ($1, $2) ON CONFLICT (id) DO NOTHING`,
          [userId, req.session!.email],
        );
        await dbQuery(
          `INSERT INTO chat."Chat" (id, title, "userId", "createdAt")
           VALUES ($1, 'New chat', $2, CURRENT_TIMESTAMP)`,
          [chatId, userId],
        );

        // Fire-and-forget title generation
        const firstUserMsg = messages.find((m) => m.role === "user");
        if (firstUserMsg) {
          generateTitle(firstUserMsg.content, req)
            .then((title) =>
              dbQuery(`UPDATE chat."Chat" SET title = $1 WHERE id = $2`, [title, chatId]),
            )
            .catch((err) => console.warn("[Title] Generation failed:", err));
        }
      }
    }

    const lastUserMsg = messages[messages.length - 1];
    if (lastUserMsg?.role === "user") {
      const userMsgId = lastUserMsg.id ?? crypto.randomUUID();
      await dbQuery(
        `INSERT INTO chat."Message" (id, "chatId", role, parts, "createdAt")
         VALUES ($1, $2, 'user', $3, CURRENT_TIMESTAMP)
         ON CONFLICT (id) DO NOTHING`,
        [userMsgId, chatId, JSON.stringify([{ type: "text", text: lastUserMsg.content }])],
      );
    }

    // 2. Open SSE stream and proxy the agent
    res.setHeader("Content-Type", "text/event-stream");
    res.setHeader("Cache-Control", "no-cache");
    res.setHeader("Connection", "keep-alive");

    const assistantMsgId = crypto.randomUUID();
    let accumulatedText = "";
    let traceId: string | null = null;

    try {
      for await (const chunk of AppKit.serving("agent").asUser(req).stream({ messages })) {
        // Forward chunk to client
        res.write(`data: ${JSON.stringify(chunk)}\n\n`);

        // Accumulate assistant text and capture trace_id
        const parsed = chunk as Chunk;
        const delta = extractDelta(parsed);
        if (delta) accumulatedText += delta;

        const tid = extractTraceId(parsed);
        if (tid) traceId = tid;
      }

      // Emit metadata so the client can associate feedback with this message
      res.write(
        `data: ${JSON.stringify({ type: "meta", assistantMessageId: assistantMsgId, traceId })}\n\n`,
      );
      res.write("data: [DONE]\n\n");
      res.end();
    } catch (err) {
      console.error("[Chat] Stream error:", err);
      res.write(`data: ${JSON.stringify({ type: "error", error: String(err) })}\n\n`);
      res.end();
    }

    // 3. Persist the assistant message after the stream closes
    if (accumulatedText) {
      await dbQuery(
        `INSERT INTO chat."Message" (id, "chatId", role, parts, "traceId", "createdAt")
         VALUES ($1, $2, 'assistant', $3, $4, CURRENT_TIMESTAMP)`,
        [
          assistantMsgId,
          chatId,
          JSON.stringify([{ type: "text", text: accumulatedText }]),
          traceId,
        ],
      );

      // Always populate meta store so 08-appkit-feedback can look up traceId
      // even when Lakebase is unavailable.
      messageMetaStore.set(assistantMsgId, { chatId: chatId ?? "", traceId });
    }
  });

  async function generateTitle(firstUserContent: string, req: import("express").Request): Promise<string> {
    try {
      const result = await AppKit.serving("agent").asUser(req).invoke({
        messages: [
          {
            role: "system",
            content:
              "Generate a 4-6 word title summarizing this conversation. Respond with only the title, no punctuation.",
          },
          { role: "user", content: firstUserContent.slice(0, 500) },
        ],
      });
      const text =
        (result as any)?.choices?.[0]?.message?.content ??
        (result as any)?.output?.[0]?.content?.[0]?.text ??
        "New chat";
      return String(text).trim().slice(0, 80);
    } catch {
      return firstUserContent.slice(0, 60);
    }
  }

  // Export for 08-appkit-feedback
  (globalThis as any).__appkitMessageMetaStore = messageMetaStore;
});

await AppKit.server.start();
```

Key points:

- **Zero AI-SDK imports.** Only `@databricks/appkit` (`AppKit.serving`, `AppKit.lakebase`) and native Express.
- The `for await (const chunk of ...)` loop is the same pattern as [06-appkit-serving-wiring/SKILL.md](../06-appkit-serving-wiring/SKILL.md) Step 6b — only the body is extended.
- `accumulatedText` is assembled server-side using the dual-format `extractDelta`. This is what gets persisted, not the raw chunk stream.
- `traceId` is scanned on every chunk — it usually arrives on the last chunk but checking each one is safer.
- The `meta` SSE event lets the client associate `assistantMessageId` + `traceId` with the message it just rendered. The client stores these on the message object so feedback works even if Lakebase is unavailable.
- `messageMetaStore` is the ephemeral-mode fallback for feedback lookups. [08-appkit-feedback](../08-appkit-feedback/SKILL.md) reads it when the DB lookup returns no rows.

### 4c. Client-Side Integration

The chat client from [06-appkit-serving-wiring/references/chat-ui-patterns.md](../06-appkit-serving-wiring/references/chat-ui-patterns.md) already uses `useServingStream` to render the conversation. To persist, replace the direct call with a fetch to `/api/chat`:

```tsx
import { useState, useRef } from "react";

interface Message {
  id?: string;
  role: "user" | "assistant";
  content: string;
  traceId?: string | null;
}

function ChatPage({ chatId }: { chatId?: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [streaming, setStreaming] = useState(false);
  const [input, setInput] = useState("");
  const cid = useRef(chatId ?? crypto.randomUUID());

  async function sendMessage() {
    if (!input.trim() || streaming) return;
    const userMsg: Message = { role: "user", content: input };
    const nextMessages = [...messages, userMsg];
    setMessages(nextMessages);
    setInput("");
    setStreaming(true);

    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: cid.current, messages: nextMessages }),
    });

    if (!res.body) {
      setStreaming(false);
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let assistantText = "";
    let assistantMessageId: string | undefined;
    let traceId: string | null = null;

    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      let idx: number;
      while ((idx = buffer.indexOf("\n\n")) !== -1) {
        const block = buffer.slice(0, idx);
        buffer = buffer.slice(idx + 2);
        const dataLine = block.split("\n").find((l) => l.startsWith("data: "))?.slice(6);
        if (!dataLine || dataLine === "[DONE]") continue;
        try {
          const parsed = JSON.parse(dataLine);
          if (parsed.type === "meta") {
            assistantMessageId = parsed.assistantMessageId;
            traceId = parsed.traceId ?? null;
          } else if (parsed.type === "error") {
            console.error("[Chat] stream error:", parsed.error);
          } else {
            // Use the same extractDelta logic on the client
            const delta =
              parsed.type === "response.output_text.delta"
                ? parsed.delta ?? ""
                : parsed.choices?.[0]?.delta?.content ?? "";
            if (delta) {
              assistantText += delta;
              setMessages((prev) => {
                const next = [...prev];
                next[next.length - 1] = { role: "assistant", content: assistantText };
                return next;
              });
            }
          }
        } catch {
          /* keepalive or partial */
        }
      }
    }

    setMessages((prev) => {
      const next = [...prev];
      next[next.length - 1] = {
        role: "assistant",
        content: assistantText,
        id: assistantMessageId,
        traceId,
      };
      return next;
    });
    setStreaming(false);
  }

  return (
    <div className="flex flex-col h-full">
      {/* ... render messages, input, etc. Use MessageBubble from chat-ui-patterns.md */}
    </div>
  );
}
```

The `id` and `traceId` fields on the rendered assistant message are what [08-appkit-feedback](../08-appkit-feedback/SKILL.md) reads from — without them, the feedback button can't link to MLflow.

**Gate:** `npm run build` passes. After a test conversation, `GET /api/messages/<chatId>` returns both the user and assistant messages with the assistant's `traceId` populated.

---

## Step 5: Build the History Sidebar

Plain React + `fetch` — zero SDK dependencies.

```tsx
import { useState, useEffect } from "react";
import { NavLink, useNavigate } from "react-router-dom";

interface ChatSummary {
  id: string;
  title: string;
  createdAt: string;
}

export function ChatSidebar() {
  const [chats, setChats] = useState<ChatSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [hasMore, setHasMore] = useState(false);
  const [ephemeral, setEphemeral] = useState(false);
  const navigate = useNavigate();

  const loadChats = (startingAfter?: string) => {
    const params = new URLSearchParams();
    if (startingAfter) params.set("starting_after", startingAfter);
    fetch(`/api/history?${params}`)
      .then((res) => {
        if (res.status === 204) {
          setEphemeral(true);
          return null;
        }
        return res.json();
      })
      .then((data) => {
        if (data) {
          setChats((prev) => (startingAfter ? [...prev, ...data.data] : data.data));
          setHasMore(data.hasMore ?? false);
        }
      })
      .catch(() => setEphemeral(true))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadChats();
  }, []);

  const deleteChat = async (chatId: string) => {
    await fetch(`/api/chat/${chatId}`, { method: "DELETE" });
    setChats((prev) => prev.filter((c) => c.id !== chatId));
  };

  if (loading) {
    return (
      <aside className="w-64 border-r bg-muted/30 p-3">
        <div className="animate-pulse space-y-2">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-8 rounded bg-muted" />
          ))}
        </div>
      </aside>
    );
  }

  return (
    <aside className="w-64 border-r bg-muted/30 p-3 flex flex-col">
      <button
        onClick={() => navigate("/chat")}
        className="mb-3 w-full rounded-md border bg-background px-3 py-2 text-sm font-medium hover:bg-muted"
      >
        + New Chat
      </button>

      {ephemeral && (
        <div className="mb-2 rounded bg-yellow-100 px-2 py-1 text-xs text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-200">
          Ephemeral — no history
        </div>
      )}

      <div className="flex-1 overflow-y-auto space-y-1">
        {chats.length === 0 && !ephemeral && (
          <p className="text-xs text-muted-foreground px-2">No conversations yet</p>
        )}
        {chats.map((chat) => (
          <div key={chat.id} className="group flex items-center">
            <NavLink
              to={`/chat/${chat.id}`}
              className={({ isActive }) =>
                `flex-1 truncate rounded px-2 py-1.5 text-sm ${
                  isActive ? "bg-muted font-medium" : "hover:bg-muted/50"
                }`
              }
            >
              {chat.title}
            </NavLink>
            <button
              onClick={() => deleteChat(chat.id)}
              className="hidden group-hover:block px-1 text-xs text-muted-foreground hover:text-destructive"
            >
              ×
            </button>
          </div>
        ))}
        {hasMore && (
          <button
            onClick={() => {
              const last = chats[chats.length - 1];
              if (last) loadChats(last.id);
            }}
            className="w-full rounded px-2 py-1.5 text-xs text-muted-foreground hover:bg-muted/50"
          >
            Load more...
          </button>
        )}
      </div>
    </aside>
  );
}
```

Wire into the router:

```tsx
function ChatLayout() {
  return (
    <div className="flex h-[calc(100vh-4rem)]">
      <ChatSidebar />
      <div className="flex-1">
        <Outlet />
      </div>
    </div>
  );
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "chat",
        element: <ChatLayout />,
        children: [
          { index: true, element: <ChatPage /> },
          { path: ":chatId", element: <ChatPage /> },
        ],
      },
    ],
  },
]);
```

**Gate:** Sidebar renders, lists conversations, and "Load more" pagination works when `hasMore` is true.

---

## Step 6: Load Existing Messages on Navigation

When navigating to an existing chat, fetch prior messages and hydrate `ChatPage` state:

```tsx
import { useParams } from "react-router-dom";

export function ChatPage() {
  const { chatId } = useParams();
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    if (!chatId) {
      setMessages([]);
      return;
    }
    fetch(`/api/messages/${chatId}`)
      .then((res) => res.json())
      .then((data) => {
        if (data?.data) {
          setMessages(
            data.data.map((m: { id: string; role: string; parts: Array<{ type: string; text?: string }>; traceId?: string }) => ({
              id: m.id,
              role: m.role as "user" | "assistant",
              content: m.parts?.find((p) => p.type === "text")?.text ?? "",
              traceId: m.traceId ?? null,
            })),
          );
        }
      })
      .catch(() => {});
  }, [chatId]);

  // ... rest of ChatPage (sendMessage, render, etc.)
}
```

**Gate:** Clicking a past conversation in the sidebar loads its messages and the `traceId` is preserved on assistant messages (visible in React DevTools).

---

## Step 7: Ephemeral Mode

When Lakebase is unavailable, the chat still works — only persistence is skipped. This mirrors the `mock fallback` pattern from [05-appkit-lakebase-wiring/SKILL.md](../05-appkit-lakebase-wiring/SKILL.md).

Verify ephemeral mode manually by deploying without the `postgres` app resource binding. Expected behavior:

- `GET /api/history` returns `204 No Content` → sidebar shows "Ephemeral — no history"
- `POST /api/chat` still streams a response (the `dbQuery` wrapper short-circuits on `dbAvailable = false`)
- The `meta` SSE event still fires with `traceId`, so [08-appkit-feedback](../08-appkit-feedback/SKILL.md) can still log MLflow assessments via the in-memory `messageMetaStore`

No new code needed — the `dbQuery` helper in Step 4b already handles the degradation transparently.

**Gate:** With Lakebase resource binding removed, the chat streams responses normally and the sidebar displays the "Ephemeral" banner.

---

## Step 8: Lakebase Cold-Start Retry Policy

Lakebase Autoscaling closes idle pool connections, so the **first request after idle** can hit `psycopg.errors.AdminShutdown` or `psycopg_pool.PoolClosed` even when Lakebase is healthy. The `dbQuery` wrapper in Step 4b currently flips `dbAvailable = false` on the first error — that is too aggressive for cold-start failures and will silently force the chat into ephemeral mode for the rest of the process lifetime. Add an explicit retry contract.

This mirrors the `lakebase_cold_start_retry_policy` contract owned by the Track A custom-agent skill — see [02-agent-framework SKILL.md](../../../genai-agents/tracks/A-custom-agent-apps/02-agent-framework/SKILL.md) ("Lakebase cold-start retry policy and lazy init"). Both the Node AppKit chat route and the Python agent must honor the same retry contract so that user-visible behavior is consistent across stacks.

### Retry contract

Capture the same fields the Track A agent captures, expressed in Node terms (`pg`/AppKit's `lakebase` plugin uses `node-postgres` semantics — the canonical class names are listed below):

```typescript
// server/lakebase-retry.ts
const lakebaseColdStartRetryPolicy = {
  // Canonical first-request-after-idle failure modes. AppKit's lakebase
  // plugin surfaces these as PostgresError instances with these `code`s
  // and `severity: "FATAL"`. Match by code, NOT by string-matching the
  // error message.
  retryOn: [
    "57P01", // admin_shutdown — Lakebase autoscaler closed the prior connection
    "57P03", // cannot_connect_now — pool not yet ready after cold start
    "ECONNRESET", // socket-level reset during cold start
    "POOL_CLOSED", // synthetic — emitted when AppKit closes the pool mid-request
  ],
  maxAttempts: 3,
  initialBackoffSeconds: 5, // exponential: 5s, 10s, 20s
} as const;

// Pool close policy on graceful shutdown. AppKit handles this via its
// own `server.on("close", ...)` lifecycle — do not close the pool from
// inside a request handler.
const lakebasePoolClosePolicy = "close_on_app_shutdown" as const;
```

Wrap `AppKit.lakebase.query` with the policy and use it in place of the `dbQuery` helper from Step 4b:

```typescript
async function withColdStartRetry<T>(fn: () => Promise<T>): Promise<T> {
  const { retryOn, maxAttempts, initialBackoffSeconds } = lakebaseColdStartRetryPolicy;
  let lastErr: unknown;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastErr = err;
      const code = (err as { code?: string })?.code;
      const matches = code !== undefined && retryOn.includes(code as (typeof retryOn)[number]);
      if (!matches || attempt + 1 === maxAttempts) throw err;
      const backoffMs = initialBackoffSeconds * 1000 * 2 ** attempt;
      console.warn(
        `[Lakebase] cold-start retry ${attempt + 1}/${maxAttempts} after ${code} — sleeping ${backoffMs}ms`,
      );
      await new Promise((r) => setTimeout(r, backoffMs));
    }
  }
  throw lastErr;
}

async function dbQuery(sql: string, params: unknown[]) {
  if (!dbAvailable) return { rows: [] as any[] };
  try {
    return await withColdStartRetry(() => AppKit.lakebase.query(sql, params));
  } catch (err) {
    // Only flip to ephemeral mode after the retry budget is exhausted.
    console.warn("[Chat] DB query failed after cold-start retries, entering ephemeral mode:", err);
    dbAvailable = false;
    return { rows: [] as any[] };
  }
}
```

### DO / DON'T

**DO** match by `error.code` against the canonical class list above. PostgresErrors have stable SQLSTATE codes; their human-readable messages are localized and change between minor versions.

**DO** keep the `lakebaseColdStartRetryPolicy` object in one module — `server/lakebase-retry.ts` — and import it into `server.ts`. Tests need to reference the same constants.

**DON'T** catch a bare `Error` or `unknown` and retry. Retrying on application-level errors (bad SQL, missing schema) hides bugs.

**DON'T** flip `dbAvailable = false` on the first error. The whole point of the retry policy is to absorb the cold-start kick without dropping into ephemeral mode for every subsequent request.

**DON'T** close the pool inside a request handler. Pool close is `lakebasePoolClosePolicy: close_on_app_shutdown` — it belongs in the AppKit server lifecycle hook, not in route code.

### First-request-retry test

Add a test that simulates a single cold-start failure and asserts the second attempt succeeds. This is the test that gates `preflight_check_registry.lakebase_cold_start_retry_policy_present` for the AppKit stack — without it, the rollup considers the policy "documented but not exercised."

```typescript
// server/__tests__/lakebase-cold-start.test.ts
import { describe, it, expect, vi } from "vitest";

describe("Lakebase cold-start retry", () => {
  it("retries on AdminShutdown (57P01) and succeeds on the second attempt", async () => {
    const adminShutdown = Object.assign(new Error("terminating connection"), {
      code: "57P01",
      severity: "FATAL",
    });
    const query = vi
      .fn()
      .mockRejectedValueOnce(adminShutdown)
      .mockResolvedValueOnce({ rows: [{ ok: 1 }] });

    // Inject the mocked query into withColdStartRetry — same wrapper used in production.
    const result = await withColdStartRetry(() => query());

    expect(query).toHaveBeenCalledTimes(2);
    expect(result.rows).toEqual([{ ok: 1 }]);
  });

  it("retries up to maxAttempts then re-throws", async () => {
    const poolClosed = Object.assign(new Error("pool closed"), { code: "POOL_CLOSED" });
    const query = vi.fn().mockRejectedValue(poolClosed);

    await expect(withColdStartRetry(() => query())).rejects.toMatchObject({ code: "POOL_CLOSED" });
    expect(query).toHaveBeenCalledTimes(3); // maxAttempts
  });

  it("does NOT retry on application-level errors (e.g. 42P01 undefined_table)", async () => {
    const undefinedTable = Object.assign(new Error('relation "chat.Chat" does not exist'), {
      code: "42P01",
    });
    const query = vi.fn().mockRejectedValue(undefinedTable);

    await expect(withColdStartRetry(() => query())).rejects.toMatchObject({ code: "42P01" });
    expect(query).toHaveBeenCalledTimes(1); // no retry
  });
});
```

Run with `npm test -- lakebase-cold-start`. All three tests must pass before declaring Step 8 complete.

**Gate:** `npm test` passes the three retry tests above. Deploy logs show no spurious `entering ephemeral mode` warnings during the first request after a 5+ minute idle period.

---

## Step 9: Validator Choice — `bundle validate` vs `apps validate`

Two validators ship with the Databricks CLI. They check different things, and one of them is **unsafe to run locally for a Lakebase-backed AppKit project**.

| Validator | What it checks | Use it when |
|-----------|----------------|-------------|
| `databricks bundle validate --profile $PROFILE` | Bundle config: `databricks.yml` resource declarations, `valueFrom` references, `serving_endpoint` schema fields, `postgres_*` resource shape, target environment variables. **Pure config validation — never boots the app.** | Always, before every `databricks apps deploy`. This is the canonical bundle-config gate. |
| `databricks apps validate --profile $PROFILE` | App manifest: `app.yaml` schema, command line, env-var bindings. **May initialize a local boot of the app** to type-check resource bindings. | Only for app-config-only changes, in workspaces where every `valueFrom` resolves locally. |

### Why `databricks apps validate` is dangerous for Lakebase apps

`databricks apps validate` can boot the AppKit server locally to verify that env-var bindings resolve. On a Lakebase-backed app, that local boot:

1. Calls `AppKit.lakebase.query()` from `initChatSchema()` (Step 1).
2. Resolves `LAKEBASE_ENDPOINT` from the local environment, **not** the deployed app's env (because deployed `valueFrom: postgres` is only resolved at platform startup).
3. Either fails outright (no Lakebase endpoint locally) or — worse — succeeds against an unrelated dev Postgres and writes the `chat` schema there.

This produces validation errors that are **not** representative of the deployed environment. Engineers then "fix" them by adding fake local Postgres URIs to `.env`, which masks real bundle-config issues that `databricks bundle validate` would have caught.

### Required gates

For any deploy from this skill:

```bash
# REQUIRED — bundle config gate. Never skip.
databricks bundle validate --profile $PROFILE

# OPTIONAL — only safe for app-config-only changes (no schema init, no Lakebase touch).
# Do NOT run for Lakebase-backed apps unless you have a local Postgres URI that mirrors
# the deployed schema. If unsure, skip this step — `bundle validate` already covers
# bundle config and `databricks apps deploy` will surface app.yaml errors at deploy time.
databricks apps validate --profile $PROFILE
```

> **Client note — Genie Code:** run `bundle validate` via `runDatabricksCli` (omit `--profile`; add `--target dev` if a targetless validate is guardrail-blocked). **Skip `apps validate` entirely** — it is hard-blocked on Genie Code *and* unsafe for Lakebase apps (boots locally against `initChatSchema()`); rely on `bundle validate` + the server-side build logs after deploy.

> **Treat `bundle validate` warnings as errors.** This is a load-bearing rule from the rollup ("`databricks bundle validate` warnings can be load-bearing errors", Skill 06d). Common warning-as-error cases for this skill: `unknown field: endpoint_name` on a `serving_endpoint` (rename to `name:`), `valueFrom: postgres` with no `postgres_*` resource declared, missing `permission` field on a declared resource. See [03-appkit-deploy SKILL.md](../03-appkit-deploy/SKILL.md) "Common Errors" for the canonical fix table.

**Gate:** `databricks bundle validate --profile $PROFILE` exits 0 with no warnings. Deploy is gated on this; `databricks apps validate` is not run for Lakebase-backed builds (or, if it is run, the failure is correlated against `bundle validate` first).

---

## Validation Gate

All must pass before declaring chat history complete:

- [ ] `CREATE SCHEMA chat` and all four tables created successfully (check deploy logs for `[Chat] Schema initialized`)
- [ ] `npm run build` passes with zero TypeScript errors
- [ ] `GET /api/history` returns `{ data, hasMore }` (or `204` in ephemeral mode)
- [ ] `GET /api/history?starting_after=<id>` returns the next page
- [ ] `GET /api/messages/:chatId` returns message list with `traceId` populated on assistant messages
- [ ] `PATCH /api/chat/:chatId/visibility` changes visibility (owner only)
- [ ] `POST /api/chat` streams responses and persists both user and assistant messages
- [ ] Assistant messages have a non-null `traceId` when the agent endpoint has MLflow tracing enabled
- [ ] Chat sidebar renders, lists conversations, and "Load more" works
- [ ] Navigating to a past chat loads its messages
- [ ] New chats appear in the sidebar after the first exchange
- [ ] Chat titles are auto-generated from the first user message
- [ ] Deleting a chat removes it from the sidebar and cascades to messages + votes
- [ ] Auth middleware attaches `req.session` to all chat routes
- [ ] App works in ephemeral mode when Lakebase is unavailable (sidebar shows "Ephemeral")
- [ ] Zero imports of `ai` or `@databricks/ai-sdk-provider` anywhere in `server/`
- [ ] `lakebaseColdStartRetryPolicy` is captured as a named constant matching the Track A contract (`retryOn` ⊇ `["57P01", "POOL_CLOSED"]`, `maxAttempts: 3`, `initialBackoffSeconds: 5`)
- [ ] First-request-retry test passes: simulated `57P01` on attempt 1 succeeds on attempt 2 (Step 8 test suite)
- [ ] `dbAvailable` flips to `false` only after `maxAttempts` retries fail, not on the first error
- [ ] `databricks bundle validate --profile $PROFILE` exits 0 with no warnings (warnings treated as errors per Skill 06d)
- [ ] `databricks apps validate` is **not** run as a deploy gate for this Lakebase-backed app (or, if run, only after `bundle validate` is green)

---

## Gotchas

| Gotcha | Fix | Step |
|--------|-----|------|
| `server.extend()` routes never registered | Set `server({ autoStart: false })` on plugin registration; call `AppKit.server.start()` after all `extend()` blocks | 4 |
| `trace_id` is always null | Endpoint doesn't have MLflow tracing enabled. Redeploy agent with `databricks.agents.deploy(..., enable_trace=True)` | 4 |
| `accumulatedText` is empty but UI shows streaming text | Parser reads only `choices[0].delta.content` on a Databricks Responses-API endpoint. Use the dual `extractDelta` from [06-appkit-serving-wiring/references/sse-format-patterns.md](../06-appkit-serving-wiring/references/sse-format-patterns.md) | 4a |
| Assistant message is persisted but client-side UI doesn't know the id | Missing the `meta` SSE event. Verify the server emits `{ type: "meta", assistantMessageId, traceId }` before `[DONE]` | 4b |
| Sidebar always shows "Ephemeral" even when deployed | `postgres` app resource binding missing in `databricks.yml` — see [05-appkit-lakebase-wiring](../05-appkit-lakebase-wiring/SKILL.md) Phase 2 | 7 |
| Title generation blocks the response | Fire-and-forget (`.then().catch()`), never `await` the title call inside the chat route | 4b |
| 403 on `/api/chat/:chatId/visibility` | User is not the chat owner — verify `req.session.userId === chat.userId` | 3 |
| Local dev without `DEV_USER_EMAIL` | All chats are owned by `"local-dev-user"`. Set `DEV_USER_EMAIL` in `.env` to attribute correctly | 2 |
| Read `x-forwarded-user-info` to identify the user | That header does not exist on Databricks Apps. Use the canonical `x-forwarded-email` / `x-forwarded-preferred-username` / `x-forwarded-user` triplet | 2 |
| Need to forward user identity to a separate Agent App | Set `x-app-user-email` outbound from the inbound `x-forwarded-email`. See [06d-appkit-agent-app-proxy](../06d-appkit-agent-app-proxy/SKILL.md) Header Contract | — |
| First request after idle hits `57P01 admin_shutdown` and the chat silently goes ephemeral for the rest of the process | `dbQuery` flipped `dbAvailable = false` on the first error. Wrap with `withColdStartRetry` from `lakebase_cold_start_retry_policy` and only flip after `maxAttempts` exhausts | 8 |
| Retry policy catches application errors (e.g. missing `chat."Chat"` table → `42P01`) and masks bugs | Match by SQLSTATE `code` against the canonical `retryOn` list, never by `instanceof Error` or string matching | 8 |
| `databricks apps validate` boots the app locally, fails on Lakebase init, and "validation errors" don't reproduce after deploy | Stop running `databricks apps validate` as a gate. Use `databricks bundle validate` for bundle config; let the platform run app boot at deploy time | 9 |
| `bundle validate` warns but does not error; deploy succeeds; runtime fails with `error resolving resource postgres` | `bundle validate` warnings are load-bearing. Treat any warning as an error and fix before deploy. See [03-appkit-deploy SKILL.md](../03-appkit-deploy/SKILL.md) Common Errors | 9 |

---

## What's Next

- **User feedback on assistant responses:** [08-appkit-feedback](../08-appkit-feedback/SKILL.md) — add thumbs up/down linked to MLflow assessments using the `traceId` captured here.

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [05-appkit-lakebase-wiring](../05-appkit-lakebase-wiring/SKILL.md) | Prerequisite — Lakebase plugin + bundle resources |
| [06-appkit-serving-wiring](../06-appkit-serving-wiring/SKILL.md) | Prerequisite — Serving plugin, `useServingStream`, dual-format SSE parser |
| [08-appkit-feedback](../08-appkit-feedback/SKILL.md) | Next step — user feedback + MLflow assessments |
| [04-appkit-plugin-add](../04-appkit-plugin-add/SKILL.md) | Reference — Lakebase and Serving plugin configuration |
| [03-appkit-deploy](../03-appkit-deploy/SKILL.md) | Deploy the app so the Service Principal creates the `chat` schema; also owns `bundle validate` warning-as-error contract (Step 9) |
| [Track A 02-agent-framework](../../../genai-agents/tracks/A-custom-agent-apps/02-agent-framework/SKILL.md) | Owns the canonical `lakebase_cold_start_retry_policy` contract (Step 8). Both stacks must honor the same `retry_on` / `max_attempts` / `initial_backoff_seconds` shape. |

---

## See Also

- Upstream platform skills: [`databricks-lakebase`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-lakebase) and [`databricks-apps`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-apps) (both tracked in `upstream_sources`).
- AppKit plugin docs: [Lakebase](https://databricks.github.io/appkit/docs/plugins/lakebase), [Serving](https://databricks.github.io/appkit/docs/plugins/serving).

