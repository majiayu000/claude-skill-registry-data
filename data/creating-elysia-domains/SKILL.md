---
name: creating-elysia-domains
description: Creates new domain modules in the Nexus Elysia API with proper typing for Eden Treaty consumers (Dashboard, The Machine)
---

# Creating Elysia Domains

This skill guides creation of new feature domains in the Nexus API following established patterns for type-safe API development.

## Capabilities

- Create domain directory structure
- Define Drizzle database schemas
- Create Elysia `t.*` types for API contracts
- Implement repository and service layers
- Build typed route handlers
- Enable Eden Treaty type inference for consumers

## Domain Structure

Create in `apps/nexus/src/domains/<domain-name>/`:

```
domains/<domain-name>/
├── schema.ts      # Drizzle table definitions
├── types.ts       # Elysia t.* types for API contracts
├── service.ts     # Business logic
├── repository.ts  # Database queries
├── routes.ts      # Elysia route handlers
└── index.ts       # Re-exports
```

## File Templates

### schema.ts
```typescript
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

export const items = sqliteTable("items", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
  status: text("status", { enum: ["active", "inactive"] }).notNull().default("active"),
  createdAt: integer("created_at", { mode: "timestamp" }).notNull(),
  updatedAt: integer("updated_at", { mode: "timestamp" }).notNull(),
});

export type Item = typeof items.$inferSelect;
export type NewItem = typeof items.$inferInsert;
```

### types.ts
```typescript
import { t } from "elysia";

export const ItemParams = t.Object({
  id: t.String(),
});

export const CreateItemBody = t.Object({
  name: t.String({ minLength: 1 }),
  status: t.Optional(t.Union([t.Literal("active"), t.Literal("inactive")])),
});

export const UpdateItemBody = t.Object({
  name: t.Optional(t.String({ minLength: 1 })),
  status: t.Optional(t.Union([t.Literal("active"), t.Literal("inactive")])),
});

export const ItemResponse = t.Object({
  id: t.String(),
  name: t.String(),
  status: t.Union([t.Literal("active"), t.Literal("inactive")]),
  createdAt: t.String(),
  updatedAt: t.String(),
});

export const ItemListResponse = t.Array(ItemResponse);
```

### repository.ts
```typescript
import { eq } from "drizzle-orm";
import { db } from "../../infra/database";
import { items, type Item, type NewItem } from "./schema";

export const itemRepository = {
  async findAll(): Promise<Item[]> {
    return db.select().from(items);
  },

  async findById(id: string): Promise<Item | undefined> {
    const results = await db.select().from(items).where(eq(items.id, id));
    return results[0];
  },

  async create(data: NewItem): Promise<Item> {
    const results = await db.insert(items).values(data).returning();
    return results[0];
  },

  async update(id: string, data: Partial<NewItem>): Promise<Item | undefined> {
    const results = await db
      .update(items)
      .set({ ...data, updatedAt: new Date() })
      .where(eq(items.id, id))
      .returning();
    return results[0];
  },

  async delete(id: string): Promise<boolean> {
    const results = await db.delete(items).where(eq(items.id, id)).returning();
    return results.length > 0;
  },
};
```

### service.ts
```typescript
import { randomUUID } from "crypto";
import { itemRepository } from "./repository";
import type { Item } from "./schema";

export const itemService = {
  async list(): Promise<Item[]> {
    return itemRepository.findAll();
  },

  async get(id: string): Promise<Item | null> {
    return (await itemRepository.findById(id)) ?? null;
  },

  async create(data: { name: string; status?: "active" | "inactive" }): Promise<Item> {
    const now = new Date();
    return itemRepository.create({
      id: randomUUID(),
      name: data.name,
      status: data.status ?? "active",
      createdAt: now,
      updatedAt: now,
    });
  },

  async update(id: string, data: Partial<{ name: string; status: "active" | "inactive" }>): Promise<Item | null> {
    return (await itemRepository.update(id, data)) ?? null;
  },

  async delete(id: string): Promise<boolean> {
    return itemRepository.delete(id);
  },
};
```

### routes.ts
```typescript
import { Elysia } from "elysia";
import { itemService } from "./service";
import {
  ItemParams,
  CreateItemBody,
  UpdateItemBody,
  ItemResponse,
  ItemListResponse,
} from "./types";

const formatItem = (item: any) => ({
  ...item,
  createdAt: item.createdAt.toISOString(),
  updatedAt: item.updatedAt.toISOString(),
});

export const itemRoutes = new Elysia({ prefix: "/items" })
  .get("/", async () => {
    const items = await itemService.list();
    return items.map(formatItem);
  }, {
    response: ItemListResponse,
    detail: { tags: ["Items"], summary: "List all items" },
  })

  .get("/:id", async ({ params, error }) => {
    const item = await itemService.get(params.id);
    if (!item) return error(404, { message: "Item not found" });
    return formatItem(item);
  }, {
    params: ItemParams,
    response: ItemResponse,
  })

  .post("/", async ({ body }) => {
    const item = await itemService.create(body);
    return formatItem(item);
  }, {
    body: CreateItemBody,
    response: ItemResponse,
  })

  .patch("/:id", async ({ params, body, error }) => {
    const item = await itemService.update(params.id, body);
    if (!item) return error(404, { message: "Item not found" });
    return formatItem(item);
  }, {
    params: ItemParams,
    body: UpdateItemBody,
    response: ItemResponse,
  })

  .delete("/:id", async ({ params, error }) => {
    const deleted = await itemService.delete(params.id);
    if (!deleted) return error(404, { message: "Item not found" });
    return { success: true };
  }, {
    params: ItemParams,
  });
```

## Registration

Add to `apps/nexus/src/app.ts`:
```typescript
import { itemRoutes } from "./domains/items/routes";

const app = new Elysia()
  .use(itemRoutes)
```

## Eden Treaty Usage

### Dashboard (React)
```typescript
import { treaty } from "@elysiajs/eden";
import type { App } from "@nexus/app";

const api = treaty<App>(import.meta.env.VITE_API_URL);

const { data: items } = await api.items.get();
const { data: item } = await api.items({ id: "123" }).get();
const { data: newItem } = await api.items.post({ name: "Test" });
```

### The Machine (Discord Bot)
```typescript
import { treaty } from "@elysiajs/eden";
import type { App } from "@nexus/app";

const api = treaty<App>(process.env.API_URL!);
const items = await api.items.get();
```

## Critical Rules

1. **Never duplicate types** - Dashboard and The Machine import from Nexus via Eden Treaty
2. **Use `t.*` types** - Enables Eden type inference
3. **Export App type** - Required for consumers
4. **Format dates as ISO strings** - JSON serialization compatibility

## Protected Routes

```typescript
import { autheliaMiddleware } from "../../middleware/authelia";

export const protectedRoutes = new Elysia({ prefix: "/admin" })
  .use(autheliaMiddleware)
  .get("/dashboard", async ({ user }) => {
    return { message: `Hello ${user.name}` };
  });
```

## Commands

```bash
bun run db:push          # Push schema changes
bun run typecheck:api    # Verify types
bun run dev:api          # Start dev server
```
