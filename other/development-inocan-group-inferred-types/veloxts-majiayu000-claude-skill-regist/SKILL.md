---
name: veloxts
description: VeloxTS framework assistant for building full-stack TypeScript APIs. Helps with procedures, generators (velox make), REST routes, authentication, validation, and common errors. Use when creating endpoints, adding features, debugging issues, or learning VeloxTS patterns.
---

# VeloxTS Development Assistant

I help you build type-safe full-stack applications with VeloxTS. Ask me about:

- Creating API endpoints (procedures)
- Generating code (`velox make resource`, `namespace`, `procedure`)
- REST route inference from naming conventions
- Authentication and guards
- Validation with Zod schemas
- Troubleshooting common errors

## Quick Decision: Which Generator?

**"I want to create a new database entity"**
```bash
velox make resource Post        # RECOMMENDED - creates everything
```
Creates: Prisma model + Zod schema + Procedures + Tests + Auto-registers

**"I have an existing Prisma model"**
```bash
velox make namespace Order      # For existing models
```
Creates: Zod schema + Procedures (no Prisma injection)

**"I need a single endpoint"**
```bash
velox make procedure health     # Quick single procedure
```
Creates: Procedure file with inline schemas

See [GENERATORS.md](GENERATORS.md) for detailed guidance.

## Procedure Naming = REST Routes

VeloxTS infers HTTP methods from procedure names:

| Name Pattern | HTTP | Route | Hook Type |
|--------------|------|-------|-----------|
| `getUser` | GET | `/users/:id` | `useQuery` |
| `listUsers` | GET | `/users` | `useQuery` |
| `findUsers` | GET | `/users` (search) | `useQuery` |
| `createUser` | POST | `/users` | `useMutation` |
| `updateUser` | PUT | `/users/:id` | `useMutation` |
| `patchUser` | PATCH | `/users/:id` | `useMutation` |
| `deleteUser` | DELETE | `/users/:id` | `useMutation` |

**Critical**: Non-standard names (like `fetchUsers`) are treated as mutations!

See [PROCEDURES.md](PROCEDURES.md) for the complete API reference.

## Common Tasks

### Create a New Resource

```bash
# Full CRUD with pagination
velox make resource BlogPost --crud --paginated

# With soft delete
velox make resource Comment --soft-delete

# Interactive field definition
velox make resource Product -i
```

### Add Authentication

```typescript
import { authenticated, hasRole } from '@veloxts/auth';

// Require login
getProfile: procedure()
  .guard(authenticated)
  .query(({ ctx }) => ctx.user),

// Require admin role
deleteUser: procedure()
  .guard(hasRole('admin'))
  .input(z.object({ id: z.string().uuid() }))
  .mutation(async ({ ctx, input }) => {
    await ctx.db.user.delete({ where: { id: input.id } });
    return { success: true };
  }),
```

### Add Pagination

```typescript
import { paginationInputSchema } from '@veloxts/velox';

listPosts: procedure()
  .input(paginationInputSchema.optional())
  .output(z.object({
    data: z.array(PostSchema),
    meta: z.object({
      page: z.number(),
      limit: z.number(),
      total: z.number(),
      totalPages: z.number(),
    }),
  }))
  .query(async ({ input, ctx }) => {
    const page = input?.page ?? 1;
    const limit = input?.limit ?? 10;
    const skip = (page - 1) * limit;

    const [data, total] = await Promise.all([
      ctx.db.post.findMany({ skip, take: limit }),
      ctx.db.post.count(),
    ]);

    return {
      data,
      meta: { page, limit, total, totalPages: Math.ceil(total / limit) },
    };
  }),
```

### Custom REST Route

```typescript
// Override automatic inference
publishPost: procedure()
  .input(z.object({ id: z.string().uuid() }))
  .output(PostSchema)
  .rest({ method: 'POST', path: '/posts/:id/publish' })  // No /api prefix!
  .mutation(async ({ ctx, input }) => {
    return ctx.db.post.update({
      where: { id: input.id },
      data: { publishedAt: new Date() },
    });
  }),
```

## Troubleshooting

### "useQuery is not a function"

Your procedure name doesn't follow query conventions:

```typescript
// BAD - "fetchUsers" is not a query prefix
const { data } = api.users.fetchUsers.useQuery({});

// GOOD - "listUsers" is a query prefix
const { data } = api.users.listUsers.useQuery({});
```

### "procedure.input is not a function"

Missing parentheses after `procedure`:

```typescript
// BAD
getUser: procedure.input(...)

// GOOD
getUser: procedure().input(...)
```

### Prisma Decimal validation fails

Use transforms for decimal fields:

```typescript
// Input
price: z.coerce.number().positive()

// Output
price: z.any().transform((val) => Number(val))
```

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more solutions.

## Project Structure

```
apps/
├── api/                    # Backend
│   ├── src/
│   │   ├── procedures/     # API endpoints (velox make procedure)
│   │   ├── schemas/        # Zod validation (velox make schema)
│   │   └── config/         # App configuration
│   └── prisma/
│       └── schema.prisma   # Database schema
│
└── web/                    # Frontend
    └── src/
        ├── routes/         # Pages
        └── components/     # UI components
```

## CLI Quick Reference

```bash
# Development
pnpm dev                    # Start API (3030) + Web (8080) with HMR
pnpm velox dev --verbose    # API only with timing metrics

# Database
pnpm db:push                # Apply schema changes
pnpm db:studio              # Open Prisma Studio
pnpm velox migrate status   # Check migration status

# Code Generation
pnpm velox make resource Post --crud      # Full resource
pnpm velox make namespace Order           # Namespace + schema
pnpm velox make procedure health          # Single procedure

# Seeding
pnpm velox db seed                        # Run all seeders
pnpm velox db seed --fresh                # Truncate + seed
```

## Detailed Guides

- [GENERATORS.md](GENERATORS.md) - Complete generator reference with decision tree
- [PROCEDURES.md](PROCEDURES.md) - Procedure API, guards, context, validation
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Error messages and fixes
