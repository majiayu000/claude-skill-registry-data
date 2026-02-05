---
name: opensaas-migration
description: Expert knowledge for migrating projects to OpenSaaS Stack. Use when discussing migration strategies, access control patterns, or OpenSaaS Stack configuration best practices.
---

# OpenSaaS Stack Migration

Expert guidance for migrating existing projects to OpenSaaS Stack.

## When to Use This Skill

Use this skill when:

- Planning a migration from Prisma, KeystoneJS, or Next.js
- Designing access control patterns
- Configuring `opensaas.config.ts`
- Troubleshooting migration issues
- Explaining OpenSaaS Stack concepts

## Migration Process

### 1. Install Required Packages

**IMPORTANT: Always install packages before starting migration**

Detect the user's package manager (check for `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, or `bun.lockb`) and use their preferred package manager.

**Required packages:**

```bash
# Using npm
npm install --save-dev @opensaas/stack-cli
npm install @opensaas/stack-core

# Using pnpm
pnpm add -D @opensaas/stack-cli
pnpm add @opensaas/stack-core

# Using yarn
yarn add -D @opensaas/stack-cli
yarn add @opensaas/stack-core

# Using bun
bun add -D @opensaas/stack-cli
bun add @opensaas/stack-core
```

**Optional packages (based on user needs):**

- `@opensaas/stack-auth` - If the project needs authentication
- `@opensaas/stack-ui` - If the project needs the admin UI
- `@opensaas/stack-tiptap` - If the project needs rich text editing
- `@opensaas/stack-storage` - If the project needs file storage
- `@opensaas/stack-rag` - If the project needs semantic search/RAG

**Database adapters (required for Prisma 7):**

SQLite:

```bash
npm install better-sqlite3 @prisma/adapter-better-sqlite3
```

PostgreSQL:

```bash
npm install pg @prisma/adapter-pg
```

Neon (serverless PostgreSQL):

```bash
npm install @neondatabase/serverless @prisma/adapter-neon ws
```

### 2. Uninstall Old Packages (KeystoneJS Only)

**IMPORTANT: For KeystoneJS projects, uninstall KeystoneJS packages before installing OpenSaaS**

KeystoneJS migrations should preserve the existing file structure and just swap packages. Do NOT create a new project structure.

```bash
# Detect package manager and uninstall KeystoneJS packages
npm uninstall @keystone-6/core @keystone-6/auth @keystone-6/fields-document
# Or with pnpm
pnpm remove @keystone-6/core @keystone-6/auth @keystone-6/fields-document
```

Remove all `@keystone-6/*` packages from `package.json`.

### 3. Schema Analysis

**Prisma Projects:**

- Analyze existing `schema.prisma`
- Identify models, fields, and relationships
- Note any Prisma-specific features used

**KeystoneJS Projects:**

- Review list definitions in `keystone.config.ts` or `keystone.ts`
- Map KeystoneJS fields to OpenSaaS fields
- Identify access control patterns
- **Note the existing file structure** - preserve it during migration

### 4. Access Control Design

**Common Patterns:**

```typescript
// Public read, authenticated write
operation: {
  query: () => true,
  create: ({ session }) => !!session?.userId,
  update: ({ session }) => !!session?.userId,
  delete: ({ session }) => !!session?.userId,
}

// Author-only access
operation: {
  query: () => true,
  update: ({ session, item }) => item.authorId === session?.userId,
  delete: ({ session, item }) => item.authorId === session?.userId,
}

// Admin-only
operation: {
  query: ({ session }) => session?.role === 'admin',
  create: ({ session }) => session?.role === 'admin',
  update: ({ session }) => session?.role === 'admin',
  delete: ({ session }) => session?.role === 'admin',
}

// Filter-based access
operation: {
  query: ({ session }) => ({
    where: { authorId: { equals: session?.userId } }
  }),
}
```

### 5. Field Mapping

**Prisma to OpenSaaS:**

| Prisma Type | OpenSaaS Field                 |
| ----------- | ------------------------------ |
| `String`    | `text()`                       |
| `Int`       | `integer()`                    |
| `Boolean`   | `checkbox()`                   |
| `DateTime`  | `timestamp()`                  |
| `Enum`      | `select({ options: [...] })`   |
| `Relation`  | `relationship({ ref: '...' })` |

**KeystoneJS to OpenSaaS:**

| KeystoneJS Field | OpenSaaS Field   |
| ---------------- | ---------------- |
| `text`           | `text()`         |
| `integer`        | `integer()`      |
| `checkbox`       | `checkbox()`     |
| `timestamp`      | `timestamp()`    |
| `select`         | `select()`       |
| `relationship`   | `relationship()` |
| `password`       | `password()`     |

### 6. Database Configuration

**SQLite (Development):**

```typescript
import { PrismaBetterSQLite3 } from '@prisma/adapter-better-sqlite3'
import Database from 'better-sqlite3'

export default config({
  db: {
    provider: 'sqlite',
    url: process.env.DATABASE_URL || 'file:./dev.db',
    prismaClientConstructor: (PrismaClient) => {
      const db = new Database(process.env.DATABASE_URL || './dev.db')
      const adapter = new PrismaBetterSQLite3(db)
      return new PrismaClient({ adapter })
    },
  },
})
```

**PostgreSQL (Production):**

```typescript
import { PrismaPg } from '@prisma/adapter-pg'
import pg from 'pg'

export default config({
  db: {
    provider: 'postgresql',
    url: process.env.DATABASE_URL,
    prismaClientConstructor: (PrismaClient) => {
      const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL })
      const adapter = new PrismaPg(pool)
      return new PrismaClient({ adapter })
    },
  },
})
```

## KeystoneJS Migration Strategy

**CRITICAL: KeystoneJS projects should be migrated IN PLACE**

Do NOT create a new project structure. Instead:

### File Structure Preservation

**Keep existing files and update them:**

1. **Rename config file:**
   - `keystone.config.ts` → `opensaas.config.ts`
   - OR `keystone.ts` → `opensaas.config.ts`

2. **Update imports in ALL files:**

   ```typescript
   // Before (KeystoneJS)
   import { config, list } from '@keystone-6/core'
   import { text, relationship, timestamp } from '@keystone-6/core/fields'

   // After (OpenSaaS)
   import { config, list } from '@opensaas/stack-core'
   import { text, relationship, timestamp } from '@opensaas/stack-core/fields'
   ```

3. **Rename KeystoneJS concepts to OpenSaaS:**
   - `keystone.config.ts` → `opensaas.config.ts`
   - `Keystone` references → `OpenSaaS` or remove entirely
   - Keep all other file names and structure as-is

4. **Update schema/list definitions:**
   - Keep existing list definitions
   - Update field imports from `@keystone-6/core/fields` to `@opensaas/stack-core/fields`
   - Adapt access control syntax (KeystoneJS and OpenSaaS are similar)
   - Keep existing GraphQL API file structure

5. **Preserve API routes and pages:**
   - Keep existing Next.js pages
   - Update any KeystoneJS context calls to use OpenSaaS context
   - Maintain existing route structure

### Import Mapping

| KeystoneJS Import             | OpenSaaS Import               |
| ----------------------------- | ----------------------------- |
| `@keystone-6/core`            | `@opensaas/stack-core`        |
| `@keystone-6/core/fields`     | `@opensaas/stack-core/fields` |
| `@keystone-6/auth`            | `@opensaas/stack-auth`        |
| `@keystone-6/fields-document` | `@opensaas/stack-tiptap`      |

### Example: KeystoneJS to OpenSaaS Config

**Before (keystone.config.ts):**

```typescript
import { config, list } from '@keystone-6/core'
import { text, relationship, timestamp } from '@keystone-6/core/fields'

export default config({
  db: {
    provider: 'postgresql',
    url: process.env.DATABASE_URL,
  },
  lists: {
    Post: list({
      fields: {
        title: text({ validation: { isRequired: true } }),
        content: text({ ui: { displayMode: 'textarea' } }),
        author: relationship({ ref: 'User.posts' }),
        publishedAt: timestamp(),
      },
    }),
  },
})
```

**After (opensaas.config.ts):**

```typescript
import { config, list } from '@opensaas/stack-core'
import { text, relationship, timestamp } from '@opensaas/stack-core/fields'
import { PrismaPg } from '@prisma/adapter-pg'
import pg from 'pg'

export default config({
  db: {
    provider: 'postgresql',
    url: process.env.DATABASE_URL,
    prismaClientConstructor: (PrismaClient) => {
      const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL })
      const adapter = new PrismaPg(pool)
      return new PrismaClient({ adapter })
    },
  },
  lists: {
    Post: list({
      fields: {
        title: text({ validation: { isRequired: true } }),
        content: text(), // Note: OpenSaaS text() doesn't have ui.displayMode
        author: relationship({ ref: 'User.posts' }),
        publishedAt: timestamp(),
      },
    }),
  },
})
```

### Steps for KeystoneJS Migration

1. **Uninstall KeystoneJS packages** (see step 2 above)
2. **Install OpenSaaS packages** (see step 1 above)
3. **Rename** `keystone.config.ts` to `opensaas.config.ts`
4. **Find and replace** in ALL project files:
   - `@keystone-6/core` → `@opensaas/stack-core`
   - `@keystone-6/core/fields` → `@opensaas/stack-core/fields`
   - `@keystone-6/auth` → `@opensaas/stack-auth`
5. **Add Prisma adapter** to database config (required for Prisma 7)
6. **Update context creation** in API routes/pages
7. **Test** - the app structure should remain identical

**DO NOT:**

- Create new folders or reorganize the project
- Move files to different locations
- Create a new "OpenSaaS structure"
- Change API endpoints or routes

**DO:**

- Keep existing file structure
- Update imports only
- Adapt config to OpenSaaS syntax
- Preserve existing API routes and pages

## Common Migration Challenges

### Challenge: Preserving Existing Data

**Solution:**

- Use `opensaas generate` to create Prisma schema
- Use `prisma db push` instead of migrations for existing databases
- Never use `prisma migrate dev` with existing data

### Challenge: Complex Access Control

**Solution:**

- Start with simple boolean access control
- Iterate to filter-based access as needed
- Use field-level access for sensitive data

### Challenge: Custom Field Types

**Solution:**

- Create custom field builders extending `BaseFieldConfig`
- Implement `getZodSchema`, `getPrismaType`, `getTypeScriptType`
- Register UI components for admin interface

### Challenge: KeystoneJS Document Field

**Solution:**

- Replace with `@opensaas/stack-tiptap` rich text field
- Or create custom field type for document structure
- May require data migration for existing documents

## Migration Checklist

### For Prisma Projects:

- [ ] **Detect package manager** (npm, pnpm, yarn, or bun)
- [ ] **Install required packages** (@opensaas/stack-cli, @opensaas/stack-core)
- [ ] **Install optional packages** (auth, ui, etc. based on needs)
- [ ] **Install database adapter** (better-sqlite3, pg, etc.)
- [ ] Analyze existing schema
- [ ] Design access control patterns
- [ ] Create `opensaas.config.ts`
- [ ] Configure database adapter in config
- [ ] Run `opensaas generate` (or `npx opensaas generate`)
- [ ] Run `prisma generate` (or `npx prisma generate`)
- [ ] Run `prisma db push` (or `npx prisma db push`)
- [ ] Test access control
- [ ] Verify admin UI (if using @opensaas/stack-ui)
- [ ] Update application code to use context
- [ ] Test all CRUD operations
- [ ] Deploy to production

### For KeystoneJS Projects:

- [ ] **Detect package manager** (npm, pnpm, yarn, or bun)
- [ ] **Uninstall ALL KeystoneJS packages** (@keystone-6/\*)
- [ ] **Install required packages** (@opensaas/stack-cli, @opensaas/stack-core)
- [ ] **Install optional packages** (auth, ui, tiptap for document fields)
- [ ] **Install database adapter** (pg, @prisma/adapter-pg for PostgreSQL)
- [ ] **Rename** `keystone.config.ts` to `opensaas.config.ts`
- [ ] **Update imports** in config file (KeystoneJS → OpenSaaS)
- [ ] **Find and replace imports** in ALL project files
- [ ] **Add Prisma adapter** to database config
- [ ] **Update context creation** in API routes
- [ ] Analyze and adapt access control patterns
- [ ] Run `opensaas generate`
- [ ] Run `prisma generate`
- [ ] Run `prisma db push`
- [ ] Test existing API routes
- [ ] Test existing pages/UI
- [ ] Test all CRUD operations
- [ ] Verify no broken imports
- [ ] Deploy to production

## Best Practices

1. **Start Simple**: Begin with basic access control, refine later
2. **Test Access Control**: Verify permissions work as expected
3. **Use Context Everywhere**: Replace direct Prisma calls with `context.db`
4. **Leverage Plugins**: Use `@opensaas/stack-auth` for authentication
5. **Version Control**: Commit `opensaas.config.ts` to git
6. **Document Decisions**: Comment complex access control logic

## Reporting Issues

**When you encounter bugs or missing features in OpenSaaS Stack:**

If during migration you discover:

- Bugs in OpenSaaS Stack packages
- Missing features that would improve the migration experience
- Documentation gaps or errors
- API inconsistencies or unexpected behavior

**Use the `github-issue-creator` agent** to create a GitHub issue on the `OpenSaasAU/stack` repository:

```
Invoke the github-issue-creator agent with:
- Clear description of the bug or missing feature
- Steps to reproduce (if applicable)
- Expected vs actual behavior
- Affected files and line numbers
- Your suggested solution (if you have one)
```

This ensures bugs and feature requests are properly tracked and addressed by the OpenSaaS Stack team, improving the experience for future users.

**Example:**

If you notice that the migration command doesn't properly handle Prisma enums, invoke the github-issue-creator agent:

> "Found a bug: The migration generator doesn't convert Prisma enums to OpenSaaS select fields. Enums are being ignored during schema analysis in packages/cli/src/migration/introspectors/prisma-introspector.ts"

The agent will create a detailed GitHub issue with reproduction steps and proposed solution.

## Resources

- [OpenSaaS Stack Documentation](https://stack.opensaas.au/)
- [Migration Guide](https://stack.opensaas.au/guides/migration)
- [Access Control Guide](https://stack.opensaas.au/core-concepts/access-control)
- [Field Types](https://stack.opensaas.au/core-concepts/field-types)
