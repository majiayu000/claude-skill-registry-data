---
name: deno
description: Deno runtime, Deploy, Fresh framework, KV, npm compatibility, and secure-by-default JavaScript/TypeScript
layer: domain
category: runtime
triggers:
  - "deno"
  - "deno deploy"
  - "fresh framework"
  - "deno kv"
  - "deno.json"
  - "deno.lock"
  - "deno serve"
  - "deno compile"
inputs:
  - "Runtime requirements and constraints"
  - "Deployment target (Deno Deploy, self-hosted)"
  - "Framework choice (Fresh, Hono, bare Deno)"
outputs:
  - "Deno project structure and configuration"
  - "Fresh routes and islands"
  - "Deno Deploy configuration"
  - "KV storage patterns"
linksTo:
  - nodejs
  - typescript-frontend
  - hono
  - vercel
linkedFrom: []
preferredNextSkills: [hono, typescript-frontend]
fallbackSkills: [nodejs, bun]
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: [deployments]
---

# Deno

## Purpose

Build and deploy secure-by-default TypeScript/JavaScript applications using Deno 2.x. Covers the Deno runtime, Fresh framework for full-stack web apps, Deno KV for built-in key-value storage, Deno Deploy for edge hosting, and npm compatibility for leveraging the existing ecosystem.

## Core Patterns

### deno.json Configuration

```jsonc
{
  "tasks": {
    "dev": "deno run --watch --allow-net --allow-read --allow-env main.ts",
    "start": "deno run --allow-net --allow-read --allow-env main.ts",
    "test": "deno test --allow-all",
    "check": "deno check **/*.ts",
    "fmt": "deno fmt",
    "lint": "deno lint"
  },
  "imports": {
    "@std/http": "jsr:@std/http@^1.0.0",
    "@std/assert": "jsr:@std/assert@^1.0.0",
    "@std/path": "jsr:@std/path@^1.0.0",
    "hono": "jsr:@hono/hono@^4.0.0",
    "zod": "npm:zod@^3.23.0"
  },
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "preact"
  },
  "nodeModulesDir": "auto",
  "fmt": {
    "lineWidth": 100,
    "semiColons": true
  },
  "lint": {
    "rules": {
      "exclude": ["no-unused-vars"]
    }
  }
}
```

### HTTP Server (Deno.serve)

```typescript
// main.ts — Deno's built-in HTTP server
Deno.serve({ port: 8000 }, async (req: Request): Promise<Response> => {
  const url = new URL(req.url);

  if (url.pathname === "/api/health") {
    return Response.json({ status: "ok", timestamp: Date.now() });
  }

  if (url.pathname === "/api/users" && req.method === "POST") {
    const body = await req.json();
    // process body...
    return Response.json({ id: crypto.randomUUID(), ...body }, { status: 201 });
  }

  return new Response("Not Found", { status: 404 });
});
```

### Deno KV (Built-in Key-Value Store)

```typescript
const kv = await Deno.openKv(); // Local SQLite in dev, managed on Deno Deploy

// Set a value with optional expiration
await kv.set(["users", "u123"], { name: "Alice", email: "alice@example.com" });
await kv.set(["sessions", sessionId], { userId: "u123" }, { expireIn: 3600_000 });

// Get a value
const entry = await kv.get<{ name: string }>(["users", "u123"]);
console.log(entry.value?.name); // "Alice"

// List by prefix
const iter = kv.list<{ name: string }>({ prefix: ["users"] });
for await (const entry of iter) {
  console.log(entry.key, entry.value);
}

// Atomic transactions (check-and-set)
const current = await kv.get(["counters", "visits"]);
await kv.atomic()
  .check(current) // Ensures no concurrent modification
  .set(["counters", "visits"], (current.value as number ?? 0) + 1)
  .commit();

// Enqueue background jobs
await kv.enqueue({ type: "send-email", to: "alice@example.com", subject: "Welcome" });
kv.listenQueue(async (msg: { type: string; to: string; subject: string }) => {
  if (msg.type === "send-email") {
    await sendEmail(msg.to, msg.subject);
  }
});
```

### Fresh Framework (Full-Stack Web)

```
my-fresh-app/
  routes/
    index.tsx        # Page routes
    about.tsx
    api/
      users.ts       # API routes
    _app.tsx         # App wrapper
    _layout.tsx      # Shared layout
    _404.tsx         # Custom 404
    greet/
      [name].tsx     # Dynamic route
  islands/
    Counter.tsx      # Interactive client components
  components/
    Header.tsx       # Static server components
  static/
    styles.css
  fresh.config.ts
  deno.json
```

```tsx
// routes/index.tsx — Server-rendered page
import { page, define } from "fresh";
import Counter from "../islands/Counter.tsx";

export const handler = define.handlers({
  async GET(ctx) {
    const posts = await fetchPosts();
    return page({ posts });
  },
});

export default define.page<typeof handler>(({ data }) => {
  return (
    <main class="p-6">
      <h1 class="text-2xl font-bold">Blog</h1>
      {data.posts.map((post) => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
        </article>
      ))}
      {/* Only this island ships JS to the client */}
      <Counter start={0} />
    </main>
  );
});
```

```tsx
// islands/Counter.tsx — Client-side interactive component
import { useSignal } from "@preact/signals";

export default function Counter({ start }: { start: number }) {
  const count = useSignal(start);
  return (
    <div class="flex items-center gap-4">
      <button
        class="px-6 py-4 text-base rounded-lg bg-blue-600 text-white transition-all duration-200 hover:bg-blue-700 focus-visible:ring-2 focus-visible:ring-offset-2"
        onClick={() => count.value--}
      >
        -
      </button>
      <span class="text-xl">{count}</span>
      <button
        class="px-6 py-4 text-base rounded-lg bg-blue-600 text-white transition-all duration-200 hover:bg-blue-700 focus-visible:ring-2 focus-visible:ring-offset-2"
        onClick={() => count.value++}
      >
        +
      </button>
    </div>
  );
}
```

```typescript
// routes/api/users.ts — API route
import { define } from "fresh";

export const handler = define.handlers({
  async GET(_ctx) {
    const kv = await Deno.openKv();
    const users = [];
    for await (const entry of kv.list({ prefix: ["users"] })) {
      users.push(entry.value);
    }
    return Response.json(users);
  },

  async POST(ctx) {
    const body = await ctx.req.json();
    const kv = await Deno.openKv();
    const id = crypto.randomUUID();
    await kv.set(["users", id], { id, ...body });
    return Response.json({ id, ...body }, { status: 201 });
  },
});
```

### npm Compatibility

```typescript
// Import npm packages directly
import express from "npm:express@4";
import { z } from "npm:zod@3";

// Or use import map in deno.json (preferred)
// "imports": { "zod": "npm:zod@^3.23.0" }
import { z } from "zod";

// Node built-in APIs
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import process from "node:process";

const content = await readFile(join(process.cwd(), "data.json"), "utf-8");
```

### Permissions System

```bash
# Granular permissions
deno run --allow-net=api.example.com,deno.land main.ts
deno run --allow-read=./data,./config main.ts
deno run --allow-env=DATABASE_URL,API_KEY main.ts
deno run --allow-write=./output main.ts

# Development (allow all — never use in production)
deno run --allow-all main.ts

# Compile to single binary
deno compile --allow-net --allow-read --output myapp main.ts
```

## Best Practices

- **Use JSR imports** over npm where available — `jsr:@std/*` packages are Deno-native and type-safe
- **Specify granular permissions** — never deploy with `--allow-all`; whitelist specific hosts, paths, and env vars
- **Use `deno.json` import maps** instead of inline `npm:` specifiers for cleaner imports
- **Leverage Deno KV** for session storage, feature flags, rate limiting — zero config on Deno Deploy
- **Use Fresh islands sparingly** — keep most components server-rendered; only island-ify what needs interactivity
- **Pin dependency versions** in `deno.json` and commit `deno.lock` for reproducible builds
- **Use `Deno.serve`** for HTTP — it handles graceful shutdown and is optimized for the runtime
- **Run `deno check`** in CI — it type-checks without running, catching errors before deployment
- **Use `deno fmt` and `deno lint`** — built-in, zero config, no eslint/prettier setup needed

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do Instead |
|---|---|---|
| `--allow-all` in production | Defeats Deno's security model | Specify exact permissions needed |
| Inline `npm:` everywhere | Hard to manage versions | Use `deno.json` import map |
| Making everything an island | Ships unnecessary JS to client | Only island-ify interactive parts |
| Ignoring `deno.lock` | Non-reproducible builds | Commit lockfile, use `--frozen` in CI |
| Using `node:fs` when `Deno.readTextFile` exists | Misses Deno-native async APIs | Prefer `Deno.*` APIs |
| KV without atomic checks | Race conditions on concurrent writes | Use `kv.atomic().check()` for CAS |
| Skipping `deno check` | Type errors caught only at runtime | Add `deno check` to CI pipeline |

## Decision Guide

| Scenario | Recommendation |
|---|---|
| Full-stack web app with SSR | Fresh framework with Preact islands |
| API server, edge deployment | `Deno.serve` + Deno Deploy |
| Need robust routing/middleware | Hono on Deno (`jsr:@hono/hono`) |
| Simple KV/session storage | Deno KV (zero config, built-in) |
| Need relational database | Use `npm:postgres` or `npm:drizzle-orm` |
| Existing Node.js project | Deno 2.x with `nodeModulesDir: "auto"` for gradual migration |
| CLI tool distribution | `deno compile` for single-binary output |
| Need npm package ecosystem | Import via `npm:` specifier or import map |
