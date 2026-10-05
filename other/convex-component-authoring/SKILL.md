---
name: convex-component-authoring
description: Creates reusable Convex components with defineComponent, a clean client wrapper, their own schema, and an npm publish setup. Use when extracting a feature into a package, building something for the Convex component directory, or when a component's functions are not showing up in the parent app.
---

# Convex component authoring

Produces a self contained component: its own `convex.config.ts`, schema, functions, and a typed client wrapper the parent app calls. The one rule: a component cannot read the parent's tables, `ctx.auth`, or `process.env`. Whatever it needs, the app passes in as arguments.

## When to reach for this

- Extracting a feature (counters, rate limits, audit logs, notifications) into a package
- Building something for the Convex component directory
- A component's functions are missing from `components.<name>` in the parent app
- A third party integration should own its own tables and background jobs
- The same backend module is needed in several apps

## Component or helper function

| Need | Use |
| --- | --- |
| Shared logic over the app's own tables | Plain TypeScript helper in `convex/lib/` |
| Its own tables with a schema the app cannot touch | Component |
| Isolated functions that run in their own transaction | Component |
| Reuse across apps with one install line | Component |
| A React hook or client utility only | npm library, no component |

If the feature does not need persistent state behind an API boundary, a helper function is less work and easier to type.

## Folder layout

```
my-component/
  package.json
  src/
    component/
      convex.config.ts     # defineComponent("counter")
      schema.ts            # tables only this component can see
      public.ts            # queries, mutations, actions
      _generated/          # created by npx convex codegen
    client/
      index.ts             # wrapper class the app imports
  example/
    convex/
      convex.config.ts     # app.use(counter) for local testing
```

For a local only component, put the `component/` contents at `convex/components/<name>/` and skip `client/` and `package.json`.

## Define the component

```typescript
// src/component/convex.config.ts
import { defineComponent } from "convex/server";

const component = defineComponent("counter");
export default component;
```

```typescript
// src/component/schema.ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  counters: defineTable({
    name: v.string(),
    value: v.number(),
  }).index("by_name", ["name"]),
});
```

Functions import `query` and `mutation` from the component's own `_generated/server`, never from the app's. Every public function needs `args` and `returns` validators; without them the parent sees `any`.

```typescript
// src/component/public.ts
import { v } from "convex/values";
import { mutation, query } from "./_generated/server.js";

export const add = mutation({
  args: { name: v.string(), amount: v.number() },
  returns: v.number(),
  handler: async (ctx, args) => {
    const existing = await ctx.db
      .query("counters")
      .withIndex("by_name", (q) => q.eq("name", args.name))
      .unique();
    if (!existing) {
      await ctx.db.insert("counters", { name: args.name, value: args.amount });
      return args.amount;
    }
    const value = existing.value + args.amount;
    await ctx.db.patch(existing._id, { value });
    return value;
  },
});

export const get = query({
  args: { name: v.string() },
  returns: v.number(),
  handler: async (ctx, args) => {
    const counter = await ctx.db
      .query("counters")
      .withIndex("by_name", (q) => q.eq("name", args.name))
      .unique();
    return counter?.value ?? 0;
  },
});
```

## Register it in the parent

```typescript
// convex/convex.config.ts (parent app)
import { defineApp } from "convex/server";
import counter from "@acme/counter/convex.config.js";
// local component: import counter from "./components/counter/convex.config.js";

const app = defineApp();
app.use(counter);
// A second instance under a different name:
// app.use(counter, { name: "pageViews" });
export default app;
```

Run `npx convex dev`. It generates `components.counter` in the app's `convex/_generated/api` and the component's own `_generated/` folder. The reference path mirrors the file: a function in `public.ts` is `components.counter.public.add`.

Component functions arrive in the parent as internal references. Call them with `ctx.runQuery` and `ctx.runMutation`; clients cannot hit them directly.

## Client wrapper class

The wrapper runs in the app's environment, so it can read `ctx.auth` and `process.env` and pass what the component needs. It takes the component reference first and options second.

```typescript
// src/client/index.ts
import type {
  GenericDataModel,
  GenericMutationCtx,
  GenericQueryCtx,
} from "convex/server";
import type { ComponentApi } from "../component/_generated/component.js";

// Pick only the capabilities each method needs so any ctx with runQuery works
type QueryCtx = Pick<GenericQueryCtx<GenericDataModel>, "runQuery">;
type MutationCtx = Pick<GenericMutationCtx<GenericDataModel>, "runMutation">;

export class Counter {
  constructor(
    public component: ComponentApi,
    private options: { prefix?: string } = {},
  ) {}

  private key(name: string): string {
    return this.options.prefix ? `${this.options.prefix}:${name}` : name;
  }

  async add(ctx: MutationCtx, name: string, amount = 1): Promise<number> {
    return await ctx.runMutation(this.component.public.add, {
      name: this.key(name),
      amount,
    });
  }

  async get(ctx: QueryCtx, name: string): Promise<number> {
    return await ctx.runQuery(this.component.public.get, { name: this.key(name) });
  }
}
```

```typescript
// convex/counter.ts (parent app)
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";
import { components } from "./_generated/api";
import { Counter } from "@acme/counter";

const counter = new Counter(components.counter, { prefix: "app" });

// The app owns auth. The component only sees the string it is handed.
export const incrementMine = mutation({
  args: {},
  returns: v.number(),
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");
    return await counter.add(ctx, identity.subject);
  },
});

export const getMine = query({
  args: {},
  returns: v.number(),
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");
    return await counter.get(ctx, identity.subject);
  },
});
```

These app side functions are what React calls through `api.counter.incrementMine`. The app decides on auth and rate limits; the component stays generic.

## Boundary rules

- **No parent tables.** `v.id("users")` inside a component refers to a component table named `users`, not the app's. Accept parent ids as `v.string()`.
- **Ids become strings.** Every `Id<"counters">` in the component is `string` in `ComponentApi`. Return them as strings on purpose.
- **No `ctx.auth`.** Resolve the user in the app and pass `userId`.
- **No app `process.env`.** Declare typed env in `defineComponent("name", { env: { API_KEY: v.string() } })` and let the app supply it with `app.use(c, { env: { API_KEY: ... } })`, or pass the value as a function argument.
- **`.paginate()` does not work across the boundary.** Use `paginator` from `convex-helpers` inside the component.
- **HTTP routes** in a component's `http.ts` are mounted by the app with `httpPrefix`. Component HTTP actions have no `ctx.auth`.
- **Callbacks into the app** travel as function handles: `createFunctionHandle(internal.x.y)` in the app, stored as `v.string()`, cast to `FunctionHandle<"mutation">` in the component.

Publishing to npm (exports map, build order, README, versioning) is covered in [references/publishing.md](references/publishing.md); open it when the component will be installed from a package rather than a local folder.

## Common mistakes

| Mistake | Why it breaks | Do instead |
| --- | --- | --- |
| Functions missing from `components.<name>` | `app.use(...)` not added, or `npx convex dev` has not run since | Register in `convex.config.ts`, run dev, check the reference path matches the file name |
| Importing `mutation` from the app's `_generated/server` | The function registers on the app, not the component | Import from the component's own `./_generated/server.js` |
| Calling `api.counter.add` from React | Component functions are internal references in the parent | Write an app mutation that calls `ctx.runMutation(components.counter.public.add)` |
| `v.id("users")` in component args | Table numbers differ per component, validation fails | `v.string()` at the boundary |
| `ctx.auth.getUserIdentity()` inside the component | Always returns no user | Authenticate in the app, pass `userId` |
| `process.env.MY_KEY` inside the component | Undefined at runtime | Declare env in `defineComponent` or pass as an argument |
| Public function without `returns` | Parent sees `any`, loses type safety | Add validators to every public function |
| Reading component env at module scope | Undefined during deploy analysis | Read `env.X` inside the handler |

## Checklist

- [ ] Decided a component is needed rather than a helper function
- [ ] `convex.config.ts` calls `defineComponent("<name>")` and exports it
- [ ] Schema lives in the component; no `v.id()` for parent tables anywhere
- [ ] Functions import from the component's own `_generated/server`
- [ ] Every public function has `args` and `returns` validators
- [ ] Parent registers with `app.use(...)` and `npx convex dev` runs clean
- [ ] Client wrapper takes `ComponentApi` first, options second, uses `Pick` ctx types
- [ ] App side wrapper functions handle auth and pass ids as strings
- [ ] No `ctx.auth`, `process.env`, or `.paginate()` inside the component
- [ ] Tested through an example app that installs the component

## Docs

- https://docs.convex.dev/llms.txt
- https://docs.convex.dev/components/authoring
- https://docs.convex.dev/components/using
- https://www.convex.dev/components
