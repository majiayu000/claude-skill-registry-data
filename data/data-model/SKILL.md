---
name: data_model
description: Adding new data models - schema, shared zod, entity pattern, and oRPC routes. Use when user asks to create a new entity, model, or feature that needs database tables.
---

# Data Model Development

This skill covers the full workflow for adding new data models to OpenPromo, from database schema to API routes.

## Quick Scaffold Workflow

### 1. Run the Scaffold Script

```bash
python .claude/skills/data_model/scripts/scaffold.py <EntityName> <domain>

# Examples:
python .claude/skills/data_model/scripts/scaffold.py Campaign marketing
python .claude/skills/data_model/scripts/scaffold.py BlogPost content --dry-run
```

This generates all 4 files:
- `packages/core/src/schemas/{entity-name}.sql.ts`
- `packages/core/src/domain/{domain}/entity/Ent{EntityName}.ts`
- `packages/shared/src/{domain}/{entity-name}.ts`
- `packages/dash/worker/src/orpc/routes/{entity-name}.ts`

### 2. Post-Scaffold Steps

The script auto-updates all index files (entity, domain, shared, oRPC). After running:

1. **Add custom fields** to schema: `packages/core/src/schemas/{entity-name}.sql.ts`
2. **Generate migration**: `cd packages/core && pnpm db generate`
3. **Run lint**: `pnpm lint`

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: Schema (packages/core/src/schemas/{name}.sql.ts)       │
│  - Drizzle table definitions, enums, JSONB types                │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│  Step 2: Shared (packages/shared/src/{domain}/index.ts)         │
│  - Zod schemas for API contracts, shared across FE/BE           │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│  Step 3: Entity (packages/core/src/domain/{domain}/entity/)     │
│  - Business logic encapsulation using Ent pattern               │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│  Step 4: oRPC Routes (packages/dash/worker/src/orpc/routes/)    │
│  - API endpoints with workspace middleware                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│  Step 5: Generate Migration                                     │
│  - cd packages/core && pnpm db generate                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Reference: Schema Patterns

Location: `packages/core/src/schemas/{name}.sql.ts`

### Key Patterns

| Pattern | Usage |
|---------|-------|
| `...id` | ULID primary key with auto-generation |
| `...workspaceID` | Multi-tenant workspace foreign key |
| `...timestamps` | createdAt/updatedAt with auto-update |
| `ulid("field_id")` | ULID foreign key reference |
| `pgEnum` + `z.enum` | Type-safe enums in DB and TypeScript |
| `jsonb().$type<T>()` | Typed JSONB columns |
| `uniqueIndex` | Unique constraints |
| `index` | Query performance indexes |

### Foreign Key References

```typescript
import { examplesTable } from "./examples.sql";

export const exampleItemsTable = pgTable("example_items", {
  ...id,
  ...workspaceID,
  ...timestamps,
  exampleId: ulid("example_id")
    .references(() => examplesTable.id, { onDelete: "cascade" })
    .notNull(),
});
```

---

## Reference: Entity Patterns

Location: `packages/core/src/domain/{domain}/entity/Ent{Name}.ts`

| Pattern | Usage |
|---------|-------|
| `extends Ent<T>` | Base class for serialization |
| `static type` | Type identifier for serialization |
| `Schemas()` | Input validation schemas |
| `fn(schema, handler)` | Schema-validated methods |
| `Actor.workspaceID()` | Get current workspace from context |
| `fromID` | Workspace-scoped lookup |
| `fromIDSystem` | System lookup (no workspace check) |
| `toJSON()` | Return raw data for API responses |

---

## Reference: oRPC Patterns

Location: `packages/dash/worker/src/orpc/routes/{name}.ts`

### Workspace Role Mappers

| Role | Permission Level |
|------|------------------|
| `workspaceRoleMappers.viewer` | Read-only access |
| `workspaceRoleMappers.editor` | Create/update access |
| `workspaceRoleMappers.admin` | Full access including delete |

---

## Common Patterns

### Pagination

```typescript
static list = fn(z.object({
  page: z.number().int().positive().default(1),
  pageSize: z.number().int().positive().max(100).default(20),
}), async (input) => {
  const workspaceId = Actor.workspaceID();
  const offset = (input.page - 1) * input.pageSize;

  const items = await db()
    .select()
    .from(table)
    .where(eq(table.workspaceId, workspaceId))
    .orderBy(desc(table.createdAt))
    .limit(input.pageSize)
    .offset(offset);

  return items.map((i) => new EntItem(i));
});
```

### Upsert Pattern

```typescript
static upsert = fn(schema, async (input) => {
  const workspaceId = Actor.workspaceID();

  const [existing] = await db()
    .select()
    .from(table)
    .where(and(
      eq(table.workspaceId, workspaceId),
      eq(table.uniqueField, input.uniqueField)
    ))
    .limit(1);

  if (existing) {
    const [updated] = await db()
      .update(table)
      .set({ ...input })
      .where(eq(table.id, existing.id))
      .returning();
    return { item: new EntItem(updated), isNew: false };
  }

  const [created] = await db()
    .insert(table)
    .values({ workspaceId, ...input })
    .returning();
  return { item: new EntItem(created), isNew: true };
});
```

### Soft Delete

```typescript
// In schema
deletedAt: timestamp(),

// In entity
async archive(): Promise<void> {
  await db()
    .update(table)
    .set({ deletedAt: new Date() })
    .where(eq(table.id, this.data.id));
}

// In list queries - exclude soft-deleted
const conditions = [
  eq(table.workspaceId, Actor.workspaceID()),
  isNull(table.deletedAt),
];
```

---

## Checklist

- [ ] Schema file created with `...id`, `...workspaceID`, `...timestamps`
- [ ] Enums have both `pgEnum` and `z.enum` definitions
- [ ] JSONB types have zod schemas
- [ ] Proper indexes defined for queries
- [ ] Types exported with `$inferSelect`, `$inferInsert`
- [ ] Shared zod schemas created
- [ ] Entity class with `static type`, `Schemas()`, `fromID`, `list`, `toJSON`
- [ ] Entity exported from domain index
- [ ] oRPC routes use `createWorkspaceInputSchema`
- [ ] Routes use appropriate `workspaceRoleMappers`
- [ ] Router registered in orpc index
- [ ] Migration generated with `pnpm db generate`
- [ ] `pnpm lint` passes

---

## Reference Files

| Layer | Example File |
|-------|--------------|
| Schema | `packages/core/src/schemas/radar.sql.ts` |
| Entity | `packages/core/src/domain/radar/entity/EntRadarSource.ts` |
| oRPC Route | `packages/dash/worker/src/orpc/routes/radar.ts` |
| Shared | `packages/shared/src/content/index.ts` |
