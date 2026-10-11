---
name: sessions
description: This skill should be used when the user asks about "grammY session", "store user state", "ctx.session", "session storage", "Redis session", "MongoDB session", "PostgreSQL session", "free session storage", "lazy session", "multi session", or needs to persist per-chat data across messages.
---

# grammY — Sessions

The `session` middleware attaches a `ctx.session` object to every chat. Modify it freely in your handlers — grammY persists it after each update. Choose an in-memory store for development, a real database for production, or grammY's free hosted storage for hobby bots.

## Type the session shape

Always declare `SessionData` and a `SessionFlavor`-augmented context:

```typescript
import { Bot, Context, SessionFlavor, session } from "grammy";

interface SessionData {
  counter: number;
  language: string;
  state: "idle" | "awaiting_name" | "awaiting_email";
}

type MyContext = Context & SessionFlavor<SessionData>;

const bot = new Bot<MyContext>(process.env.BOT_TOKEN!);
```

## In-memory (development only)

```typescript
bot.use(session({
  initial: (): SessionData => ({
    counter: 0,
    language: "en",
    state: "idle",
  }),
}));

bot.on("message", (ctx) => {
  ctx.session.counter++;
  return ctx.reply(`Counter: ${ctx.session.counter}`);
});
```

`MemorySessionStorage` is the default — data is lost on process restart. **Never use in production.**

## Free hosted storage (zero-config production)

For hobby bots without infrastructure, use grammY's free key-value storage (rate-limited, intended for small bots):

```bash
npm install @grammyjs/storage-free
```

```typescript
import { freeStorage } from "@grammyjs/storage-free";

bot.use(session({
  initial: (): SessionData => ({ counter: 0, language: "en", state: "idle" }),
  storage: freeStorage<SessionData>(bot.token),
}));
```

Free storage is keyed by your bot token — different bots get isolated namespaces automatically.

## External storages

Install the storage adapter for your database:

| Database | Package |
|---|---|
| Redis | `@grammyjs/storage-redis` (uses `ioredis`) |
| MongoDB | `@grammyjs/storage-mongodb` |
| PostgreSQL | `@grammyjs/storage-psql` |
| Supabase | `@grammyjs/storage-supabase` |
| File | `@grammyjs/storage-file` |
| Cloudflare KV | `@grammyjs/storage-cloudflare` |
| AWS DynamoDB | `@grammyjs/storage-dynamodb` |
| AWS S3 | `@grammyjs/storage-s3` |
| Prisma | `@grammyjs/storage-prisma` |
| TypeORM | `@grammyjs/storage-typeorm` |
| Firestore | `@grammyjs/storage-firestore` |
| PocketBase | `@grammyjs/storage-pocketbase` |
| Bun SQL | `@grammyjs/storage-bun` |

**Deno KV** (also the store behind Deno Deploy) has an adapter too, but it is a Deno-only package published on JSR — the `storage-denokv` package in the grammyjs scope — not on npm. On Deno, the other adapters come from the shared storages module of the grammY docs (see "External Storage Solutions" on grammy.dev/plugins/session).

### Redis example

```typescript
import { RedisAdapter } from "@grammyjs/storage-redis";
import IORedis from "ioredis";

const redis = new IORedis(process.env.REDIS_URL!);

bot.use(session({
  initial: () => ({ counter: 0 } as SessionData),
  storage: new RedisAdapter({ instance: redis }),
}));
```

### MongoDB example

```typescript
import { MongoDBAdapter } from "@grammyjs/storage-mongodb";
import { MongoClient } from "mongodb";

const client = new MongoClient(process.env.MONGO_URI!);
await client.connect();
const collection = client.db("mybot").collection<{ key: string; value: SessionData }>("sessions");

bot.use(session({
  initial: () => ({ counter: 0 } as SessionData),
  storage: new MongoDBAdapter({ collection }),
}));
```

## Session key — per chat vs per user

By default `getSessionKey: (ctx) => ctx.chat?.id.toString()` — one session per chat. Switch to per-user (across all chats) like this:

```typescript
bot.use(session({
  initial: () => ({ counter: 0 } as SessionData),
  getSessionKey: (ctx) => ctx.from?.id.toString(),  // per-user
}));
```

Or per `(user, chat)` pair:

```typescript
getSessionKey: (ctx) =>
  ctx.from && ctx.chat ? `${ctx.from.id}:${ctx.chat.id}` : undefined,
```

Return `undefined` to skip session loading for that update.

## Lazy sessions — defer the read

Default `session` always reads from storage before middleware runs. `lazySession` only reads when you `await ctx.session`:

```typescript
import { lazySession, type LazySessionFlavor } from "grammy";

type MyContext = Context & LazySessionFlavor<SessionData>;

bot.use(lazySession({
  initial: () => ({ counter: 0 } as SessionData),
  storage: new RedisAdapter({ instance: redis }),
}));

bot.on("message:text", async (ctx) => {
  if (!ctx.message.text.startsWith("/admin")) return; // skip → no DB read
  const data = await ctx.session;                      // DB read happens here
  data.counter++;
});
```

Use lazy sessions when most updates don't touch state — big win on read-heavy bots.

You can also assign a *promise* to `ctx.session`; grammY awaits it before writing back:

```typescript
ctx.session = ctx.session.then((s) => {
  s.counter = 0;
  return s;
});
```

## Multi-sessions — split data into separate storages

Different fragments of session data can live in different backends — e.g. hot counters in Redis, cold preferences in MongoDB:

```typescript
bot.use(session({
  type: "multi",
  counters: {
    initial: () => ({ hits: 0 }),
    storage: new RedisAdapter({ instance: redis }),
  },
  prefs: {
    initial: () => ({ language: "en" }),
    storage: new MongoDBAdapter({ collection: prefsColl }),
  },
}));

bot.on("message", (ctx) => {
  ctx.session.counters.hits++;
  ctx.session.prefs.language; // unchanged
});
```

Each fragment can have its own `getSessionKey`, `prefix`, and `initial`.

## Session migrations — add a field safely

When you add a new field to `SessionData`, existing stored sessions don't have it. Handle this in `initial` (called on miss) AND defensively in handlers, or run a one-time migration script.

```typescript
interface SessionData {
  counter: number;
  language: string;
  // newly added:
  notifications: boolean;
}

bot.use(session({
  initial: () => ({ counter: 0, language: "en", notifications: true }),
}));

bot.on("message", (ctx) => {
  // Treat the field as possibly missing for one rollout
  ctx.session.notifications ??= true;
});
```

## When NOT to use sessions

- **Multi-step user input wizards** — use the `conversations` plugin instead. It snapshots the entire control flow, not just data, so you can `await conversation.wait()` in normal-looking code.
- **Anything global** — session is per-chat or per-user. Global config belongs in env vars or a regular DB table you read directly.
- **Long-lived large blobs** — session is rewritten on every update. Keep it under a few KB; for larger data, store an ID in session and the blob in a separate table.