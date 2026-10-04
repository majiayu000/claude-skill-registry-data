---
name: express
description: "Build Express.js routers and middleware with request validation, async error handling, and clear application structure."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["express", "nodejs", "middleware", "http", "api", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Express.js HTTP APIs AI Skill Guide

## Overview & Engine Architecture

Express is a minimal Node HTTP framework built around middleware chains and routers. Request flows top-to-bottom; the first matching route wins unless `next()` continues. Agents keep middleware ordered correctly (parsers before handlers, error middleware last), wrap async routes so rejections reach the error handler, and validate input before business logic.

```
req -> middleware... -> router -> handler
                              \-> next(err) -> error middleware -> res
```

## When to use this skill

- Building REST/JSON APIs on Node
- Splitting apps into domain routers
- Fixing hanging requests from unhandled async errors
- Adding auth, logging, and rate-limit middleware

## Operational directives

1. Mount `express.json()` / urlencoded only where needed; cap body size.
2. Put four-arg error middleware `(err, req, res, next)` after all routes.
3. Wrap async handlers or use a helper so rejected promises call `next(err)`.
4. Use `Router()` per domain; keep `app.js` / `server.js` thin.
5. Never trust `req.body` shape - validate with zod/joi or similar.

## App sketch

```js
import express from "express";

const app = express();
app.use(express.json({ limit: "100kb" }));

const items = express.Router();

items.get("/", (_req, res) => {
  res.json([{ id: 1, sku: "A" }]);
});

items.post("/", (req, res, next) => {
  Promise.resolve()
    .then(() => {
      const sku = req.body?.sku;
      if (typeof sku !== "string" || !sku) {
        const err = new Error("sku required");
        err.status = 400;
        throw err;
      }
      res.status(201).json({ id: 2, sku });
    })
    .catch(next);
});

app.use("/items", items);

app.use((err, _req, res, _next) => {
  const status = err.status ?? 500;
  res.status(status).json({ error: err.message ?? "internal error" });
});

app.listen(3000);
```

## Commands

```bash
npm install express
node --watch src/server.js
NODE_ENV=production node src/server.js
```

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| Async throw without `next` | Hanging or crash | Async wrapper / catch |
| Error middleware before routes | Never runs | Mount last |
| Giant monolithic `app.js` | Hard to test | Domain routers |
| Trusting proxy headers blindly | Spoofed IPs | `trust proxy` + known hops |

## Best practices

- Centralize CORS, helmet, and request logging at the edge.
- Return consistent error JSON shapes for clients.
- Prefer explicit status codes (`201`, `204`, `409`).
- Test with supertest against the `app` export (not `listen` in tests).

## Limitations

- Express 4 vs 5 middleware and path syntax differ - match package major.
- WebSockets need `ws` or Socket.IO alongside Express.
- TypeScript types (`@types/express`) must align with the Express major version.

## Related skills

- `@nodejs` - runtime, ESM, process hygiene
- `@graphql-apis` - GraphQL layers often mounted on Express
- `@prisma` - persistence behind route handlers
