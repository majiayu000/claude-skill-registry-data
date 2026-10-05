---
name: prisma
description: Prisma ORM — schema DSL, migrations, Prisma Client, Studio, edge deployment.
---

## prisma

### Schema DSL (`schema.prisma`)
- **Models**: `model User { id Int @id @default(autoincrement()) }` with field types, attributes, default values.
- **Enums**: `enum Role { USER ADMIN }` used as field types.
- **Relations**: `@relation` with `fields: [authorId] references: [id]` for one-to-many, many-to-many.
- **Attributes**: `@unique`, `@index`, `@default(now())`, `@updatedAt`.

### Migrations
- `prisma migrate dev` — generate + apply migration; `prisma migrate deploy` — apply in CI/prod.
- `prisma migrate reset` — drop + recreate; `prisma migrate status` — check drift.
- Use `prisma migrate resolve` to fix migration history conflicts.

### Prisma Client
- `new PrismaClient()` — instantiate; `prisma.user.findMany()` — CRUD.
- Filtering: `where: { email: { contains: "example.com" } }`; sorting: `orderBy: { name: "asc" }`; pagination: `take: 10, skip: 20`.
- Include/nested reads: `include: { posts: true }`; select specific fields.

### Prisma Studio
- `npx prisma studio` — GUI for browsing/editing data.

### Extensions & Edge
- Zod schemas auto-generated via `prisma-zod` for validation.
- `@prisma/client` works on Edge (Neon, Cloudflare D1) via `@prisma/adapter-neon` or `@prisma/adapter-pg`.
- Policy/permission layer: `@prisma/extension-policy` or middleware middleware hooks.
- Connection pooling with PgBouncer for serverless.
