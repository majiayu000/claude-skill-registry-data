---
name: wasp-database
description: Complete database migration workflow and schema management for Wasp projects. Use when modifying schema.prisma, running migrations, or working with database models. Includes MANDATORY restart requirement and PostgreSQL setup.
triggers:
  [
    "migration",
    "schema change",
    "database",
    "prisma",
    "migrate",
    "schema.prisma",
    "database model",
    "postgres",
    "db migrate",
    "entity",
    "wasp db",
  ]
version: 1.0
last_updated: 2025-10-18
allowed_tools: [Edit, Bash, Read]
---

# Wasp Database Migration Skill

## Quick Reference

**When to use this skill:**

- Modifying database schema
- Adding/changing models or fields
- Running migrations
- Database setup and configuration
- Schema errors or type mismatches

**Key concepts:**

- ALWAYS use `wasp db migrate-dev` (NEVER `prisma migrate dev`)
- MANDATORY restart after migration for types to update
- PostgreSQL required for enums and PgBoss jobs
- Migration files are immutable (never edit/delete)

---

## Critical Rules

**NEVER use:** `npx prisma migrate dev` (WRONG)
**ALWAYS use:** `wasp db migrate-dev` (CORRECT)

**MANDATORY:** Restart `../scripts/safe-start.sh` after migration (multi-worktree safe, types regenerate)

**NO exceptions:** Even "simple" changes require restart - types will be stale without it

---

## Complete Migration Workflow

### Step 1: Edit schema.prisma

**Location:** `app/schema.prisma`

**Common schema patterns:**

```prisma
// Primary key with auto-increment
model Task {
  id          Int      @id @default(autoincrement())
  description String
  isDone      Boolean  @default(false)
  createdAt   DateTime @default(now())

  // Relations
  user        User     @relation(fields: [userId], references: [id])
  userId      Int
}

// Optional fields (add ?)
model User {
  id       Int      @id @default(autoincrement())
  email    String?  @unique  // Optional
  username String   @unique   // Required
}

// Enums (requires PostgreSQL)
enum TaskStatus {
  TODO
  IN_PROGRESS
  DONE
}

model Task {
  status TaskStatus @default(TODO)
}

// Unique constraints
model User {
  email String @unique

  @@unique([organizationId, username])  // Composite unique
}
```

**Common field types:**

- `String` - Text
- `Int` - Integer
- `Boolean` - True/false
- `DateTime` - Timestamp
- `Json` - JSON data
- `String?` - Optional string
- Add `@unique` for unique constraint
- Add `@default(...)` for default value

---

### Step 2: Run Migration

```bash
wasp db migrate-dev --name "Descriptive migration name"
```

**Examples of good migration names:**

- ✅ "Add email to User"
- ✅ "Create Task model"
- ✅ "Add status field to Task"
- ✅ "Add unique constraint to username"
- ❌ "Update" (too vague)
- ❌ "Changes" (not descriptive)
- ❌ "Migration" (meaningless)

**What this command does:**

1. Generates SQL migration file in `app/migrations/`
2. Applies migration to database
3. Updates Prisma client
4. **DOES NOT** regenerate Wasp types (requires restart!)

**Command output:**

```
Applying migration `20251018120000_add_email_to_user`
✓ Generated Prisma Client to ./node_modules/@prisma/client
```

---

### Step 3: RESTART Wasp (MANDATORY)

```bash
# Stop current wasp (Ctrl+C), then safe-start (multi-worktree safe)
../scripts/safe-start.sh
```

**Why restart is MANDATORY:**

- Wasp types only regenerate on restart
- TypeScript won't see new fields without restart
- NO exceptions - ALWAYS restart after migration
- Even for "small" changes like adding one field

**Common error if you skip restart:**

```
Property 'email' does not exist on type 'User'
```

**Fix:** Stop wasp (Ctrl+C) and run `../scripts/safe-start.sh` (multi-worktree safe)

---

### Step 4: Verify Types Updated

**Check that new fields appear in TypeScript imports:**

```typescript
import type { Task } from "wasp/entities";

// Task type now includes new fields
const task: Task = {
  id: 1,
  description: "Test",
  status: "TODO", // New field visible after restart
  createdAt: new Date(),
};
```

**If fields still missing:**

1. Confirm migration ran successfully
2. Verify you restarted wasp
3. Check for TypeScript cache issues: `wasp clean && ../scripts/safe-start.sh`

---

## Database Configuration

### schema.prisma Structure

**Required structure:**

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"  // or "sqlite" for development
  url      = env("DATABASE_URL")  // ✅ MUST use env()
}

// Your models below
model User {
  id Int @id @default(autoincrement())
}
```

**Critical rules:**

- ✅ Use `env("DATABASE_URL")` for database URL
- ❌ NEVER hardcode database URLs
- ✅ Keep schema.prisma in `app/schema.prisma`
- ❌ DO NOT configure database in main.wasp

---

### PostgreSQL vs SQLite

**PostgreSQL (Production & Recommended):**

- ✅ Supports Prisma enums
- ✅ Supports PgBoss (background jobs)
- ✅ Production-ready
- ✅ Better performance
- ❌ Requires PostgreSQL server

**SQLite (Development Only):**

- ✅ No setup required
- ✅ Quick for prototyping
- ❌ NO enum support
- ❌ NO PgBoss support
- ❌ Limited concurrent writes

**Recommendation:** Use PostgreSQL from the start if you need enums or jobs.

**Switch from SQLite to PostgreSQL:**

```prisma
// Before (SQLite)
datasource db {
  provider = "sqlite"
  url      = env("DATABASE_URL")
}

// After (PostgreSQL)
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

Then update `.env.server`:

```bash
DATABASE_URL="postgresql://username:password@localhost:5432/myapp_dev"
```

---

## Common Migration Errors

### Error: "Cannot find module 'wasp/entities'"

**Cause:** Forgot to restart wasp after migration

**Fix:**

```bash
# Stop wasp (Ctrl+C), then safe-start (multi-worktree safe)
../scripts/safe-start.sh
```

---

### Error: "Property 'newField' does not exist on type 'User'"

**Cause:** Types not regenerated (forgot restart)

**Fix:** Restart `../scripts/safe-start.sh` (multi-worktree safe)

**Verification:**

```typescript
import type { User } from "wasp/entities";
// Check if type includes new field in IDE autocomplete
```

---

### Error: "Migration failed: relation already exists"

**Cause:** Database out of sync with migrations

**Fix (Development only!):**

```bash
# WARNING: This deletes all data!
wasp db reset
wasp db migrate-dev "Fresh start"
../scripts/safe-start.sh  # Multi-worktree safe
```

**Production fix:** Never use `db reset` in production. Contact database admin.

---

### Error: "Enum types are not supported by sqlite"

**Cause:** Using enums with SQLite

**Fix:** Switch to PostgreSQL:

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

Update `.env.server`:

```bash
DATABASE_URL="postgresql://localhost:5432/myapp_dev"
```

---

### Error: "Environment variable not found: DATABASE_URL"

**Cause:** Missing .env.server file

**Fix:** Create `app/.env.server`:

```bash
DATABASE_URL="postgresql://localhost:5432/myapp_dev"
```

---

## Best Practices

### ✅ DO:

- Use descriptive migration names
- Commit migration files to git
- Restart immediately after migration
- Use `wasp db migrate-dev` command
- Use `env("DATABASE_URL")` in schema.prisma
- Test migrations in development first
- Keep schema.prisma in app root

### ❌ NEVER:

- Delete migration files (breaks history)
- Edit existing migrations (create new one instead)
- Use `prisma migrate dev` directly
- Skip restart after migration
- Hardcode database URLs
- Force migrations in production
- Use `wasp db reset` in production

---

## Migration Workflow Examples

### Example 1: Add Field to Existing Model

**Scenario:** Add email field to User model

**Step 1: Edit schema.prisma**

```prisma
// Before
model User {
  id Int @id @default(autoincrement())
}

// After
model User {
  id    Int     @id @default(autoincrement())
  email String? @unique
}
```

**Step 2: Run migration**

```bash
wasp db migrate-dev "Add email to User"
```

**Step 3: Restart wasp**

```bash
# Ctrl+C to stop, then safe-start (multi-worktree safe)
../scripts/safe-start.sh
```

**Step 4: Verify in code**

```typescript
import type { User } from "wasp/entities";

// email field now available on User type
```

---

### Example 2: Create New Model

**Scenario:** Create Task model with relations

**Step 1: Edit schema.prisma**

```prisma
model Task {
  id          Int      @id @default(autoincrement())
  description String
  isDone      Boolean  @default(false)
  createdAt   DateTime @default(now())
  user        User     @relation(fields: [userId], references: [id])
  userId      Int
}

model User {
  id    Int    @id @default(autoincrement())
  tasks Task[] // Add back-relation
}
```

**Step 2: Run migration**

```bash
wasp db migrate-dev "Create Task model"
```

**Step 3: Restart wasp**

---

### Example 3: Add Relation Between Models

**Scenario:** Add User-Task relation

**Step 1: Edit schema.prisma**

```prisma
model User {
  id    Int    @id @default(autoincrement())
  tasks Task[] // Add this line
}

model Task {
  id          Int     @id @default(autoincrement())
  description String
  user        User    @relation(fields: [userId], references: [id])
  userId      Int
}
```

**Step 2: Run migration**

```bash
wasp db migrate-dev "Add User-Task relation"
```

**Step 3: Restart wasp**

---

### Example 4: Add Enum (PostgreSQL only)

**Scenario:** Add TaskStatus enum

**Step 1: Verify PostgreSQL**

```prisma
datasource db {
  provider = "postgresql"  // Required for enums
}
```

**Step 2: Add enum to schema.prisma**

```prisma
enum TaskStatus {
  TODO
  IN_PROGRESS
  DONE
}

model Task {
  id     Int        @id @default(autoincrement())
  status TaskStatus @default(TODO)
}
```

**Step 3: Run migration**

```bash
wasp db migrate-dev "Add TaskStatus enum"
```

**Step 4: Restart wasp**

**Step 5: Use in code**

```typescript
import type { TaskStatus } from "wasp/entities"; // Type import
import { TaskStatus } from "@prisma/client"; // Value import

// Usage
const status: TaskStatus = TaskStatus.TODO;
```

---

## PostgreSQL Setup

### Local Development (macOS)

```bash
# Install PostgreSQL via Homebrew
brew install postgresql
brew services start postgresql

# Create database
createdb myapp_dev
```

### Local Development (Linux)

```bash
# Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start service
sudo service postgresql start

# Create database
sudo -u postgres createdb myapp_dev
```

### .env.server Configuration

**Create/update:** `app/.env.server`

```bash
DATABASE_URL="postgresql://username:password@localhost:5432/myapp_dev"
```

**Format breakdown:**

- `postgresql://` - Protocol
- `username:password` - Database credentials
- `localhost:5432` - Host and port
- `myapp_dev` - Database name

**Example for local development:**

```bash
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/myapp_dev"
```

---

### Docker Alternative

**Start PostgreSQL in Docker:**

```bash
docker run --name postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres
```

**Create database:**

```bash
docker exec -it postgres psql -U postgres -c "CREATE DATABASE myapp_dev;"
```

**.env.server:**

```bash
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/myapp_dev"
```

---

## Troubleshooting

### Database connection failed

**Check 1: PostgreSQL running**

```bash
pg_isready
# Expected: localhost:5432 - accepting connections
```

**Check 2: DATABASE_URL in .env.server**

```bash
cat app/.env.server
# Verify DATABASE_URL is set
```

**Check 3: Database exists**

```bash
psql $DATABASE_URL -c "SELECT 1;"
# Should connect successfully
```

---

### Migrations out of sync

**Development only - reset database:**

```bash
# WARNING: Deletes all data!
wasp db reset
wasp db migrate-dev "Fresh start"
../scripts/safe-start.sh  # Multi-worktree safe
```

**Production - manual sync:**

1. Never use `db reset`
2. Contact database admin
3. Apply migrations manually if needed

---

### Types not showing new fields

**Always the same fix:** Restart `../scripts/safe-start.sh` (multi-worktree safe)

**If still broken:**

```bash
wasp clean
../scripts/safe-start.sh  # Multi-worktree safe
```

---

### Enum not working

**Check 1: PostgreSQL?**

```prisma
datasource db {
  provider = "postgresql"  // NOT sqlite
}
```

**Check 2: Import values correctly?**

```typescript
// ✅ CORRECT - Runtime values
import { TaskStatus } from "@prisma/client";
const status = TaskStatus.TODO;

// ✅ CORRECT - Type annotation
import type { TaskStatus } from "wasp/entities";
const status: TaskStatus = "TODO";

// ❌ WRONG - Runtime values from wasp/entities
import { TaskStatus } from "wasp/entities"; // Type only, not values!
```

---

## Quick Checklist

**Migration workflow:**

- [ ] Edit schema.prisma
- [ ] Run `wasp db migrate-dev "Description"`
- [ ] Wait for completion
- [ ] **RESTART `../scripts/safe-start.sh`** (Ctrl+C, then safe-start - multi-worktree safe)
- [ ] Verify types updated in TypeScript

**Database setup:**

- [ ] PostgreSQL installed and running (for enums/jobs)
- [ ] DATABASE_URL set in .env.server
- [ ] Database created
- [ ] Connection tested

**After changes:**

- [ ] Migration file committed to git
- [ ] Types visible in IDE autocomplete
- [ ] No TypeScript errors
- [ ] Application runs without errors

---

## Critical Commands

```bash
# Run migration (CORRECT)
wasp db migrate-dev "Description"

# Reset database (dev only - DELETES DATA!)
wasp db reset

# Open Prisma Studio (database GUI)
wasp db studio

# Check migration status
wasp db migrate status
```

---

## References

**Complete guide:**

- `docs/TROUBLESHOOTING-GUIDE.md` (Database Issues section)
- `.tmp/extraction/wave1-agent-a-cursor-rules.md` (Migration workflow)

**Related skills:**

- `wasp-operations` - For using entities in operations
- `tdd-workflow` - For testing database changes

**External docs:**

- Prisma Schema: https://www.prisma.io/docs/concepts/components/prisma-schema
- Wasp Database: https://wasp.sh/docs/data-model/entities
