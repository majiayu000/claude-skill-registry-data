---
name: hono
description: Build ultra-fast web APIs and full-stack apps with Hono — runs on Cloudflare Workers, Deno, Bun, Node.js, and any WinterCG-compatible runtime. 
category: AI & Agents
source: antigravity
tags: [typescript, node, api, claude, ai, security, aws]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/hono
---


# Hono Web Framework

## Overview

Hono (炎, "flame" in Japanese) is a small, ultrafast web framework built on Web Standards (`Request`/`Response`/`fetch`). It runs anywhere: Cloudflare Workers, Deno Deploy, Bun, Node.js, AWS Lambda, and any WinterCG-compatible runtime — with the same code. Hono's router is one of the fastest available, and its middleware system, built-in JSX support, and RPC client make it a strong choice for edge APIs, BFFs, and lightweight full-stack apps.

## When to Use This Skill

- Use when building a REST or RPC API for edge deployment (Cloudflare Workers, Deno Deploy)
- Use when you need a minimal but type-safe server framework for Bun or Node.js
- Use when building a Backend for Frontend (BFF) layer with low latency requirements
- Use when migrating from Express but wanting better TypeScript support and edge compatibility
- Use when the user asks about Hono routing, middleware, `c.req`, `c.json`, or `hc()` RPC client

## How It Works

### Step 1: Project Setup

**Cloudflare Workers (recommended for edge):**
```bash
npm create hono@latest my-api
# Select: cloudflare-workers
cd my-api
npm install
npm run dev    # Wrangler local dev
npm run deploy # Deploy to Cloudflare
```

**Bun / Node.js:**
```bash
mkdir my-api && cd my-api
bun init
bun add hono
```

```typescript
// src/index.ts (Bun)
import { Hono } from 'hono';

const app = new Hono();

app.get('/', c => c.text('Hello Hono!'));

export default {
  port: 3000,
  fetch: app.fetch,
};
```

### Step 2: Routing

```typescript
import { Hono } from 'hono';

const app = new Hono();

// Basic methods
app.get('/posts', c => c.json({ posts: [] }));
app.post('/posts', c => c.json({ created: true }, 201));
app.put('/posts/:id', c => c.json({ updated: true }));
app.delete('/posts/:id', c => c.json({ deleted: true }));

// Route params and query strings
app.get('/posts/:id', async c => {
  const id = c.req.param('id');
  const format = c.req.query('format') ?? 'json';
  return c.json({ id, format });
});

// Wildcard
app.get('/static/*', c => c.text('static file'));

export default app;
```

**Chained routing:**
```typescript
app
  .get('/users', listUsers)
  .post('/users', createUser)
  .get('/users/:id', getUser)
  .patch('/users/:id', updateUser)
  .delete('/users/:id', deleteUser);
```

### Step 3: Middleware

Hono middleware works exactly like `fetch` interceptors — before and after handlers:

```typescript
import { Hono } from 'hono';
import { logger } from 'hono/logger';
import { cors } from 'hono/cors';
import { bearerAuth } from 'hono/bearer-auth';

const app = new Hono();

// Built-in middleware
app.use('*', logger());
app.use('/api/*', cors({ origin: 'https://myapp.com' }));
app.use('/api/admin/*', bearerAuth({ token: process.env.API_TOKEN! }));

// Custom middleware
app.use('*', async (c, next) => {
  c.set('requestId', crypto.randomUUID());
  await next();
  c.header('X-Request-Id', c.get('requestId'));
});
```

**Available built-in middleware:** `logger`, `cors`, `csrf`, `etag`, `cache`, `basicAuth`, `bearerAuth`, `jwt`, `compress`, `bodyLimit`, `timeout`, `prettyJSON`, `secureHeaders`.

### Step 4: Request and Response Helpers

```typescript
app.post('/submit', async c => {
  // Parse body
  const body = await c.req.json<{ name: string; email: string }>();
  const form = await c.req.formData();
  const text = await c.req.text();

  // Headers and cookies
  const auth = c.req.header('authorization');
  const token = getCookie(c, 'session');

  // Responses
  return c.json({ ok: true });                        // JSON
  return c.text('hello');                             // plain text
  return c.html('<h1>Hello</h1>');                    // HTML
  return c.redirect('/dashboard', 302);              // redirect
  return new Response(stream, { status: 200 });       // raw Response
});
```

### Step 5: Zod Validator Middleware

```typescript
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const createPostSchema = z.object({
  title: z.string().min(1).max(200),
  body: z.string().min(1),
  tags: z.array(z.string()).default([]),
});

app.post(
  '/posts',
  zValidator('json', createPostSchema),
  async c => {
    const data = c.req.valid('json'); // fully typed
    const post = await db.post.create({ data });
    return c.json(post, 201);
  }
);
```

### Step 6: Route Groups and App Composition

```typescript
// src/routes/posts.ts
import { Hono } from 'hono';

const posts = new Hono();

posts.get('/', async c => { /* list posts */ });
posts.post('/', async c => { /* create post */ });
posts.get('/:id', async c => { /* get post */ });

export default posts;
```

```typescript
// src/index.ts
import { Hono } from 'hono';
import posts from './routes/posts';
import users from './routes/users';

const app = new Hono().basePath('/api');

app.route('/posts', posts);
app.route('/users', users);

export default app;
```

### Step 7: RPC Client (End-to-End Type Safety)

Hono's RPC mode exports route types that the `
