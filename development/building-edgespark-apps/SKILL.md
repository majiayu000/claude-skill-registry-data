---
name: building-edgespark-apps
description: Build and modify EdgeSpark apps. Use when a project has edgespark.toml, the user mentions EdgeSpark, or work involves the edgespark CLI, server SDK types, storage/auth/database workflows, deployment, or @edgespark/web.
---

# EdgeSpark App Development

Use this skill for EdgeSpark-specific implementation and workflow decisions.

This skill is not EdgeSpark documentation. For exact contracts, read source, generated types, CLI help, and docs/Mintlify MCP. Use this skill for workflow, guardrails, and bug-prevention.

The reliable public surface in this repo is:

- the `edgespark` CLI
- scaffolded project structure from `edgespark init`
- generated `src/__generated__/edgespark.d.ts`
- generated `src/__generated__/server-types.d.ts`
- the `@edgespark/web` browser SDK

Use `@edgespark/web` and `authUI.mount()` as the default browser auth path for this repo unless custom forms are explicitly requested.

## Read Order

Read only what is needed for the task:

1. `edgespark.toml`
2. repo or project agent instruction file (`AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`)
3. `src/__generated__/edgespark.d.ts`
4. `src/__generated__/server-types.d.ts`
5. `src/defs/index.ts`, `src/defs/db_schema.ts`, `src/defs/db_relations.ts`, `src/defs/runtime.ts`, `src/defs/storage_schema.ts`
6. `node_modules/@edgespark/web/dist/index.d.ts` when installed for exact browser SDK types
7. `node_modules/@edgespark/web/README.md` when installed for managed auth appearance variable meanings and defaults

Then load the specific reference you need:

- Day-to-day development workflows by surface: [dev-workflow.md](references/dev-workflow.md)
- Scaffold layout and generated-file rules: [project-structure.md](references/project-structure.md)
- Error-prone server-side usage patterns: [server-patterns.md](references/server-patterns.md)
- Small web usage patterns for `@edgespark/web`: [web-patterns.md](references/web-patterns.md)
- Auth config, OAuth providers, callback URLs, managed auth theming, and Google One Tap: [auth-patterns.md](references/auth-patterns.md)

## Hard Rules

- Run `edgespark <command> --help` before assuming flags or exact behavior.
- Run `edgespark` commands on behalf of the user. Only hand off steps that explicitly require a human browser action.
- Never run multiple `edgespark` commands in parallel.
- Treat scaffolded `src/__generated__/edgespark.d.ts` and `src/__generated__/server-types.d.ts` as placeholders until `edgespark pull types` populates them.
- Do not edit files under `src/__generated__/`.
- Use `@edgespark/web` for new browser code.
- Use `es.api.fetch()` for app API calls, not bare `fetch()` to same-origin app routes.
- Use `authUI.mount()` for managed auth UI unless custom forms are explicitly requested.
- For managed auth theming, use `appearance.theme` and `appearance.variables` from `@edgespark/web`; do not tell users to edit SDK CSS for routine light/dark or brand theming.
- For custom browser auth flows, use `client.auth` from `@edgespark/web`, not manual `/api/_es/auth/*` calls.
- Import `auth` from `edgespark/http`, not `edgespark`.
- Auth is a managed service at `/api/_es/auth/`. OAuth callback URLs use `/api/_es/auth/callback/<provider>`, not `/api/auth/`.
- Treat `/api/_es/auth/*`, storage provider details, and deployment internals as platform implementation details unless the user is explicitly debugging them.
- Do not import runtime SDK values from `edgespark` inside `src/defs/**`.
- Use `db.batch()` instead of `db.transaction()`.
- Use migration workflow for schema changes. Do not use DDL through `edgespark db sql`.
- Store S3 URIs in the database and return presigned URLs to clients.
- For client-originated uploads, generate presigned PUT URLs instead of streaming files through the Worker.
- Update `src/defs/runtime.ts` before using `vars.get()` or `secret.get()`.
- Use `edgespark ... --help` for exact command syntax instead of duplicating help text in this skill.
- If exact behavior is unclear, prefer source code, generated types, or docs MCP over guessing.

## Default Workflow

For the operational workflow by area, read [dev-workflow.md](references/dev-workflow.md).

### Existing project

1. Read generated type files first.
2. Read the relevant defs files before changing schema, storage, or runtime keys.
3. Read the web SDK types before touching auth or browser API code.

### Fresh scaffold

1. Inspect `edgespark.toml` to confirm server-only vs full-stack layout.
2. If generated files are placeholders, run `edgespark pull types` before making SDK assumptions.
3. Follow the scaffolded root, `server/`, and `web/` agent instruction files for package boundaries.

## When Stuck

1. Read the generated type files again before assuming an API shape.
2. Run the relevant `edgespark ... --help` command before guessing flags.
3. Use docs/Mintlify MCP for product documentation details.

## Quick Start

Server:

```ts
import { db, storage, vars, secret, ctx } from "edgespark";
import { auth } from "edgespark/http";
import { posts, buckets } from "@defs";
import { Hono } from "hono";
import { eq } from "drizzle-orm";

const app = new Hono()
  .get("/api/posts", async (c) => {
    return c.json(await db.select().from(posts));
  })
  .post("/api/posts", async (c) => {
    const data = await c.req.json();
    const [post] = await db.insert(posts)
      .values({ ...data, user_id: auth.user!.id })
      .returning();
    return c.json(post, 201);
  });

export default app;
```

Web:

```ts
import { createEdgeSpark } from "@edgespark/web";
import "@edgespark/web/styles.css";

const es = createEdgeSpark();

es.authUI.mount(document.getElementById("auth")!, {
  redirectTo: "/dashboard",
});

const res = await es.api.fetch("/api/posts");
const posts = await res.json();
```
