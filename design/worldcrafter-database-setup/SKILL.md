---
name: worldcrafter-database-setup
description: Create database tables with Prisma ORM, migrations, and RLS policies. Use when user needs "create database table", "add [model] model", "set up RLS", "create migration", "store data in database", or "design schema". Generates Prisma models with proper naming conventions, creates migrations, sets up Row-Level Security policies, and syncs test database. Includes WorldCrafter patterns for relationships, tags, comments, activity logs, versions, world membership, collections, wiki pages, and bookmarks. Typically the FIRST skill for new features. Do NOT use for UI/forms (use worldcrafter-feature-builder), simple routes (use worldcrafter-route-creator), tests only (use worldcrafter-test-generator), or auth logic only (use worldcrafter-auth-guard).
---

# WorldCrafter Database Setup

**Version:** 2.0.0
**Last Updated:** 2025-01-09

This skill provides tools and guidance for setting up database tables with Prisma ORM, implementing Row-Level Security (RLS) policies, and managing database migrations in WorldCrafter.

## Skill Metadata

**Related Skills:**
- `worldcrafter-feature-builder` - Use after database is created to build UI layer
- `worldcrafter-auth-guard` - Use to implement RLS policies and auth checks
- `worldcrafter-test-generator` - Use to test database operations

**Example Use Cases:**
- "Create a BlogPost table with title, content, and author" → Generates Prisma model, creates migration, sets up RLS policies for author-only access
- "Add a Comment model that belongs to posts" → Creates Comment model with post relationship, migration, and RLS for authenticated users
- "Add a tagging system for worlds and characters" → Creates Tag and EntityTag models with polymorphic relationships, migration, and RLS policies
- "Create activity logging for all CRUD operations" → Creates ActivityLog model with action tracking, migration, and RLS for read access

## When to Use This Skill

Use this skill when:
- Adding new database tables to the application
- Creating relationships between existing tables
- Setting up Row-Level Security (RLS) policies
- Running database migrations
- Syncing schema changes to test database
- Implementing database triggers
- Troubleshooting database schema issues

## Database Setup Process

### Phase 1: Design Database Schema

1. **Understand data requirements**
   - What data needs to be stored?
   - What are the relationships with existing tables?
   - What fields are required vs optional?
   - What constraints are needed (unique, foreign keys)?
   - Reference `references/prisma-patterns.md` for common patterns

2. **Plan Row-Level Security**
   - Who should be able to read this data?
   - Who should be able to create/update/delete?
   - Reference `references/rls-policies.md` for policy templates

### Phase 2: Create Prisma Model

**Manual Approach:**
1. Open `prisma/schema.prisma`
2. Add new model following WorldCrafter conventions:
   - Model name: PascalCase (e.g., `BlogPost`)
   - Table name: snake_case with `@@map("table_name")`
   - Fields: camelCase in model, snake_case in DB with `@map("field_name")`
   - Always include `id`, `createdAt`, `updatedAt`

**Automated Approach:**
Use the scaffolding script to generate the model interactively:
```bash
python .claude/skills/worldcrafter-database-setup/scripts/generate_model.py
```

This will:
- Prompt for model name
- Generate model with standard fields
- Add to schema.prisma
- Follow all WorldCrafter conventions

Reference `assets/templates/model-template.prisma` for examples.

### Phase 3: Create Database Migration

**Development workflow (quick iteration):**
```bash
npx prisma db push
```
- Pushes schema directly to database
- No migration file created
- Good for rapid prototyping

**Production workflow (recommended):**
```bash
npx prisma migrate dev --name add_table_name
```
- Creates migration file in `prisma/migrations/`
- Maintains migration history
- Regenerates Prisma Client automatically
- Required for production deployments

**Migration naming conventions:**
- `add_users_table` - New table
- `add_user_role_field` - New field
- `update_users_constraints` - Constraint changes
- `add_users_rls_policies` - RLS policies

### Phase 4: Set Up Row-Level Security (RLS)

RLS is **critical** for security - it enforces database-level access control so users can only access their own data.

**Generate RLS policies:**
```bash
python .claude/skills/worldcrafter-database-setup/scripts/generate_rls.py <table_name>
```

This generates SQL for:
- Enabling RLS on the table
- Common policy templates (read own, write own, etc.)
- Saves to `prisma/migrations/sql/rls_<table_name>.sql`

**Apply RLS policies:**
```bash
npm run db:rls
```

**Manual RLS setup:**
1. Create SQL file in `prisma/migrations/<timestamp>_add_<table>_rls/migration.sql`
2. Add RLS policies (reference `references/rls-policies.md`)
3. Run `npm run db:rls` to apply

**Common RLS patterns** (from `references/rls-policies.md`):

```sql
-- Enable RLS
ALTER TABLE public.table_name ENABLE ROW LEVEL SECURITY;

-- Users can read own data
CREATE POLICY "Users can read own data"
  ON public.table_name
  FOR SELECT
  USING (auth.uid() = user_id);

-- Users can update own data
CREATE POLICY "Users can update own data"
  ON public.table_name
  FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Users can insert own data
CREATE POLICY "Users can insert own data"
  ON public.table_name
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Public read, authenticated write
CREATE POLICY "Anyone can read"
  ON public.table_name
  FOR SELECT
  USING (true);

CREATE POLICY "Authenticated users can create"
  ON public.table_name
  FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);
```

### Phase 5: Sync to Test Database

After creating migrations, sync to test database:

```bash
npm run db:test:sync
```

Or with seeding:
```bash
npm run db:test:sync -- --seed
```

This ensures integration tests run against the latest schema.

### Phase 6: Verify and Test

1. **Verify schema changes:**
   ```bash
   npx prisma studio
   ```
   Opens GUI to view database structure

2. **Verify Prisma Client types:**
   ```typescript
   import { prisma } from '@/lib/prisma'

   // TypeScript should autocomplete new model
   const result = await prisma.yourNewModel.findMany()
   ```

3. **Test RLS policies:**
   - Create integration test
   - Verify users can only access their own data
   - Test all CRUD operations

4. **Run type checking:**
   ```bash
   npm run build
   ```

## Common Database Patterns

### Basic Model

```prisma
model BlogPost {
  id        String   @id @default(cuid())
  title     String
  content   String
  published Boolean  @default(false)
  authorId  String   @map("author_id")
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  author User @relation(fields: [authorId], references: [id], onDelete: Cascade)

  @@map("blog_posts")
}
```

### One-to-Many Relationship

```prisma
model User {
  id    String @id
  posts BlogPost[] // One user has many posts
}

model BlogPost {
  id       String @id @default(cuid())
  authorId String @map("author_id")

  author User @relation(fields: [authorId], references: [id], onDelete: Cascade)

  @@map("blog_posts")
}
```

### Many-to-Many Relationship

```prisma
model Post {
  id   String @id @default(cuid())
  tags PostTag[]
}

model Tag {
  id    String @id @default(cuid())
  name  String @unique
  posts PostTag[]
}

// Junction table
model PostTag {
  postId String @map("post_id")
  tagId  String @map("tag_id")

  post Post @relation(fields: [postId], references: [id], onDelete: Cascade)
  tag  Tag  @relation(fields: [tagId], references: [id], onDelete: Cascade)

  @@id([postId, tagId])
  @@map("post_tags")
}
```

### Enum Fields

```prisma
enum UserRole {
  USER
  ADMIN
  MODERATOR
}

model User {
  id   String   @id
  role UserRole @default(USER)
}
```

### JSON Fields

```prisma
model UserSettings {
  id       String @id @default(cuid())
  userId   String @unique @map("user_id")
  metadata Json?  // Optional JSON field

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@map("user_settings")
}
```

## Database Scripts Reference

### Generate Model (Interactive)
```bash
python .claude/skills/worldcrafter-database-setup/scripts/generate_model.py
```

### Generate RLS Policies
```bash
python .claude/skills/worldcrafter-database-setup/scripts/generate_rls.py <table_name>
```

### Sync Databases
```bash
python .claude/skills/worldcrafter-database-setup/scripts/sync_databases.py
```

## Prisma Commands Reference

```bash
# Push schema to dev database (no migration file)
npx prisma db push

# Create migration
npx prisma migrate dev --name migration_name

# Apply migrations to production
npx prisma migrate deploy

# Reset database (WARNING: deletes all data)
npx prisma migrate reset

# Regenerate Prisma Client
npx prisma generate

# Open Prisma Studio GUI
npx prisma studio

# Format schema file
npx prisma format

# Validate schema
npx prisma validate
```

## WorldCrafter Database Commands

```bash
# Apply RLS policies
npm run db:rls

# Sync schema to test database
npm run db:test:sync

# Push schema to test database
npm run db:test:push

# Seed test database
npm run db:test:seed

# Open Prisma Studio
npm run db:studio
```

## Troubleshooting

### Migration fails
- Check syntax in `prisma/schema.prisma`
- Run `npx prisma validate`
- Check database connection strings in `.env`
- Ensure `DIRECT_DATABASE_URL` (port 5432) is used for migrations

### Type errors after schema changes
- Run `npx prisma generate` to regenerate client
- Restart TypeScript server in IDE
- Run `npm run build` to verify

### RLS policies not working
- Verify RLS is enabled: `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`
- Check policy conditions match your use case
- Test with `psql` or Supabase SQL editor
- Verify `auth.uid()` is returning expected user ID

### Test database out of sync
- Run `npm run db:test:sync` to resync
- Check `.env.test` has correct database URL
- Verify test database is separate from dev database

## Reference Files

- `references/prisma-patterns.md` - Detailed Prisma schema patterns
- `references/worldcrafter-complete-schema.md` - Complete WorldCrafter PRD schema (relationships, tags, comments, activity logs, versions, members, collections, wiki, bookmarks)
- `references/rls-policies.md` - RLS policy templates and examples (includes all WorldCrafter tables)
- `references/migration-workflow.md` - Migration best practices
- `references/related-skills.md` - How this skill works with other WorldCrafter skills
- `assets/templates/model-template.prisma` - Model templates
- `assets/templates/rls-template.sql` - RLS SQL templates

## Skill Orchestration

This skill is typically the FIRST step in feature development, providing the data layer foundation.

### Common Workflows

**Database-First Feature Development:**
1. **worldcrafter-database-setup** (this skill) - Create tables, migrations, RLS policies
2. **worldcrafter-feature-builder** - Build UI layer with forms and Server Actions
3. **worldcrafter-auth-guard** - Enhance auth checks (RLS provides base security)

**Schema Evolution:**
1. **worldcrafter-database-setup** (this skill) - Modify existing schema
2. Update existing feature code to use new schema
3. **worldcrafter-test-generator** - Add tests for schema changes

**Data Model Only:**
1. **worldcrafter-database-setup** (this skill) - Create data model
2. UI built later when needed

### When Claude Should Use Multiple Skills

Claude will orchestrate database-setup with other skills when:
- User wants a "complete feature" → database-setup first, then feature-builder
- User mentions "authentication" AND "database" → database-setup for tables, auth-guard for protection
- User wants "database with tests" → database-setup first, then test-generator

**Example orchestration:**
```
User: "Create a blog post system with user authentication"

Claude's workflow:
1. worldcrafter-database-setup (this skill):
   - Create BlogPost model with authorId
   - Add RLS: users can only edit their own posts
   - Generate migration

2. worldcrafter-feature-builder:
   - Create blog post form
   - Create Server Actions using BlogPost model
   - Add validation

3. worldcrafter-auth-guard:
   - Add auth checks to blog routes
   - Ensure only authenticated users can create posts
```

### Skill Selection Guidance

**Choose this skill when:**
- User explicitly mentions "database", "table", "model", "schema"
- User describes data that needs to be stored
- Feature needs persistent data storage
- User asks about RLS or migrations

**Choose worldcrafter-feature-builder instead when:**
- User wants complete feature without mentioning database specifically
- Feature-builder can create simple features and call database-setup if needed

**Use this skill FIRST when:**
- Building new feature from scratch
- Data model must be designed before UI
- RLS policies need to be planned upfront

## Success Criteria

A complete database setup includes:
- ✅ Prisma model with proper naming conventions
- ✅ Migration file created and applied
- ✅ RLS policies enabled and configured
- ✅ Test database synced
- ✅ Prisma Client regenerated
- ✅ Type checking passes (`npm run build`)
- ✅ Integration tests verify RLS policies work
- ✅ Database visible in Prisma Studio
