---
name: project-context
description: Provides architecture knowledge for the dealflow-network project including tRPC router patterns, Drizzle ORM conventions, authentication flow, file organization, and collaborative contact system. Use when working on this codebase, adding features, or understanding existing patterns.
---

# Dealflow Network - Project Context

## Architecture Overview

**Stack:** React 19 + Vite + Express + tRPC + Drizzle ORM + MySQL
**Auth:** Magic link (passwordless JWT-based)
**UI:** Radix UI + Tailwind CSS v4

## Directory Structure

```
client/src/
  _core/              # Core hooks (useAuth)
  components/         # Reusable components
    ui/              # Radix UI wrappers
  pages/              # Route-level components
  lib/                # Utilities (trpc.ts)

server/
  _core/              # Infrastructure (auth, LLM, env)
  routers.ts          # Main tRPC router
  db.ts               # Database functions
  db-collaborative.ts # Collaborative contact system
  services/           # Business logic

shared/
  _core/
    const.ts          # Shared constants
    types.ts          # Shared types

drizzle/
  schema.ts           # Table definitions
  migrations/         # SQL migrations
```

## Path Aliases

```typescript
"@/*"       → "./client/src/*"
"@shared/*" → "./shared/*"
```

## tRPC Patterns

### Procedure Types
- `publicProcedure` - No auth required
- `protectedProcedure` - Requires authenticated user
- `adminProcedure` - Requires admin role

### Router Structure (server/routers.ts)
```typescript
export const appRouter = router({
  auth: router({ me, logout, emailGateLogin }),
  contacts: router({ list, get, search, create, update, delete }),
  companies: router({ ... }),
  events: router({ ... }),
  graph: router({ ... }),
  relationships: router({ ... }),
});
```

### Input Validation
All inputs use Zod schemas:
```typescript
.input(z.object({
  id: z.number(),
  name: z.string().optional(),
}))
```

### Client Usage
```typescript
const { data } = trpc.contacts.list.useQuery();
const mutation = trpc.contacts.create.useMutation({
  onSuccess: () => utils.contacts.list.invalidate(),
});
```

## Drizzle ORM Patterns

### Table Definition (drizzle/schema.ts)
```typescript
export const contacts = mysqlTable("contacts", {
  id: int("id").autoincrement().primaryKey(),
  name: varchar("name", { length: 255 }).notNull(),
  email: varchar("email", { length: 320 }),
  createdAt: timestamp("createdAt").defaultNow(),
});

export type Contact = typeof contacts.$inferSelect;
export type InsertContact = typeof contacts.$inferInsert;
```

### Database Connection (server/db.ts)
```typescript
const db = await getDb();
const results = await db.select().from(contacts).where(eq(contacts.id, id));
```

### Migrations
```bash
npm run db:push  # Generate and apply migrations
```

## Authentication Flow

1. User enters email on login page
2. Backend generates JWT (15-min expiry) - `server/_core/magic-link.ts`
3. Email sent with magic link URL
4. Token verified -> session cookie created (30-day expiry)
5. Cookie name: `app_session_id` (shared/_core/const.ts)

**Auth Hook:** `client/src/_core/hooks/useAuth.ts`
```typescript
const { user, isAuthenticated, logout } = useAuth();
```

## Collaborative Contact System

**Key File:** `server/db-collaborative.ts`

### Duplicate Detection (priority order)
1. Email (exact match)
2. LinkedIn URL (exact match)
3. Name + Company (exact match)

### Core Function
```typescript
const { contactId, isNew, matchedBy } = await createOrLinkContact(userId, contactData);
```

## Key Conventions

- **Database fields:** camelCase (e.g., linkedinUrl, createdAt)
- **File names:** kebab-case (e.g., db-collaborative.ts)
- **Functions:** camelCase with verb (e.g., createContact, findDuplicates)
- **No emoji** in code or commits
- **Error handling:** tRPC errors with codes (UNAUTHORIZED, BAD_REQUEST)

## Common Commands

```bash
npm run dev      # Development server
npm run build    # Production build
npm run check    # TypeScript check
npm run test     # Run Vitest tests
npm run db:push  # Database migrations
```

## Key Files Reference

| Purpose | File |
|---------|------|
| tRPC router | `server/routers.ts` |
| Database schema | `drizzle/schema.ts` |
| Auth hook | `client/src/_core/hooks/useAuth.ts` |
| tRPC client | `client/src/lib/trpc.ts` |
| Shared types | `shared/_core/types.ts` |
| Environment | `server/_core/env.ts` |
