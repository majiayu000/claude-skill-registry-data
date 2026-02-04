---
name: Managing Supabase Schema Migrations
description: Guides creation, validation, and application of Supabase database migrations with RLS policy checks and type generation. Use when adding tables, modifying schema, or updating database structure.
---

# Managing Supabase Schema Migrations

Safe workflow for database schema changes with automatic type generation and RLS validation.

## When to Use This Skill

- Adding new tables
- Modifying existing columns
- Creating indexes
- Adding or updating RLS policies
- Any database schema changes

## Migration Workflow

Follow these steps for safe migrations:

### Step 1: Create Migration File

```bash
# Create a new migration with descriptive name
supabase migration new add_recipe_tags_table

# Or with bash helper
bash .claude/skills/supabase-migrations/scripts/create-migration.sh "add_recipe_tags_table"
```

This creates: `supabase/migrations/[timestamp]_add_recipe_tags_table.sql`

### Step 2: Write Migration SQL

Edit the generated file with your schema changes.

**Example: Adding a new table**
```sql
-- Create recipe_tags table
CREATE TABLE IF NOT EXISTS public.recipe_tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  recipe_id UUID NOT NULL REFERENCES public.saved_recipes(id) ON DELETE CASCADE,
  tag VARCHAR(50) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),

  -- Ensure unique tag per recipe
  UNIQUE(recipe_id, tag)
);

-- Create index for faster lookups
CREATE INDEX idx_recipe_tags_recipe_id ON public.recipe_tags(recipe_id);
CREATE INDEX idx_recipe_tags_tag ON public.recipe_tags(tag);

-- Enable RLS
ALTER TABLE public.recipe_tags ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Users can only see tags for recipes they own
CREATE POLICY "Users can view their own recipe tags"
  ON public.recipe_tags
  FOR SELECT
  USING (
    recipe_id IN (
      SELECT id FROM public.saved_recipes WHERE user_id = auth.uid()
    )
  );

-- RLS Policy: Users can insert tags for their own recipes
CREATE POLICY "Users can insert tags for their recipes"
  ON public.recipe_tags
  FOR INSERT
  WITH CHECK (
    recipe_id IN (
      SELECT id FROM public.saved_recipes WHERE user_id = auth.uid()
    )
  );

-- RLS Policy: Users can delete tags from their own recipes
CREATE POLICY "Users can delete their recipe tags"
  ON public.recipe_tags
  FOR DELETE
  USING (
    recipe_id IN (
      SELECT id FROM public.saved_recipes WHERE user_id = auth.uid()
    )
  );
```

**Common migration patterns:** See [supabase-security.md](../../modules/supabase-security.md)

### Step 3: Validate RLS Policies

**CRITICAL:** Every table MUST have RLS enabled and policies defined.

```bash
# Check if migration includes RLS
bash .claude/skills/supabase-migrations/scripts/validate-rls.sh supabase/migrations/[your-migration-file].sql
```

Checks for:
- `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`
- At least one `CREATE POLICY` statement

### Step 4: Test Migration Locally

Apply migration to local Supabase instance first:

```bash
# Ensure local Supabase is running
supabase start

# Apply migration to local database
supabase db push

# Check status
supabase db diff
```

If errors occur:
- Fix the SQL in migration file
- Reset local DB: `supabase db reset`
- Try again: `supabase db push`

### Step 5: Regenerate TypeScript Types

After successful local migration, update types:

```bash
# Generate types from local database
bash .claude/skills/supabase-migrations/scripts/update-types.sh

# Or manually:
supabase gen types typescript --local > lib/supabase/types.ts
```

This updates `lib/supabase/types.ts` with new schema.

### Step 6: Update Application Code

Search codebase for files that need updating:

```bash
# Find files using the affected table
grep -r "from('old_table_name')" app/ components/ lib/
```

Update TypeScript code to use new types:
```typescript
import type { Database } from '@/lib/supabase/types'
type RecipeTag = Database['public']['Tables']['recipe_tags']['Row']
```

### Step 7: Test Changes

- Run build: `npm run build` (must pass)
- Run tests: `npm test` (must pass)
- Test affected features manually

### Step 8: Apply to Production

**Only after local testing passes:**

```bash
# Push migration to remote database
supabase db push --remote

# Or via Supabase Dashboard:
# 1. Copy migration SQL
# 2. Run in SQL Editor
# 3. Verify with table view
```

**Important:** Migrations are irreversible in production. Always test locally first.

## Migration Safety Checklist

Before applying to production:

- [ ] Migration tested locally with `supabase db push`?
- [ ] RLS enabled on all new tables?
- [ ] RLS policies created (SELECT, INSERT, UPDATE, DELETE)?
- [ ] Indexes created for foreign keys and frequent queries?
- [ ] Types regenerated with `update-types.sh`?
- [ ] Application code updated to use new schema?
- [ ] Build passes (`npm run build`)?
- [ ] Tests pass (`npm test`)?
- [ ] Manual testing of affected features completed?

## Common Migration Patterns

### Adding a Column
```sql
ALTER TABLE public.saved_recipes
ADD COLUMN difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard'));
```

### Renaming a Column
```sql
ALTER TABLE public.saved_recipes
RENAME COLUMN old_name TO new_name;
```

### Adding an Index
```sql
CREATE INDEX idx_recipes_user_id ON public.saved_recipes(user_id);
```

### Adding a Foreign Key
```sql
ALTER TABLE public.recipe_images
ADD CONSTRAINT fk_recipe_images_recipe_id
FOREIGN KEY (recipe_id)
REFERENCES public.saved_recipes(id)
ON DELETE CASCADE;
```

## RLS Policy Patterns

### Policy: User owns resource
```sql
CREATE POLICY "Users can view their own recipes"
  ON public.saved_recipes
  FOR SELECT
  USING (user_id = auth.uid());
```

### Policy: Public read, authenticated write
```sql
CREATE POLICY "Anyone can view recipes"
  ON public.saved_recipes
  FOR SELECT
  USING (true);

CREATE POLICY "Authenticated users can insert"
  ON public.saved_recipes
  FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);
```

### Policy: Relationship-based access
```sql
CREATE POLICY "Users can view tags for their recipes"
  ON public.recipe_tags
  FOR SELECT
  USING (
    recipe_id IN (
      SELECT id FROM public.saved_recipes WHERE user_id = auth.uid()
    )
  );
```

**More RLS patterns:** See [supabase-security.md](../../modules/supabase-security.md#rls-policies)

## Rollback Strategy

If a migration causes issues in production:

**Option 1: Create reverse migration**
```bash
supabase migration new revert_add_recipe_tags

# Write SQL to undo changes
# - DROP TABLE
# - DROP COLUMN
# - etc.
```

**Option 2: Restore from backup** (via Supabase Dashboard)
- Settings → Database → Point-in-time Recovery
- Select time before migration
- Restore (creates new project)

**Prevention is better:** Always test locally first!

## Script Usage

### create-migration.sh
```bash
bash .claude/skills/supabase-migrations/scripts/create-migration.sh "migration_name"
```
Creates timestamped migration file.

### validate-rls.sh
```bash
bash .claude/skills/supabase-migrations/scripts/validate-rls.sh supabase/migrations/[file].sql
```
Checks for RLS policies in migration.

### update-types.sh
```bash
bash .claude/skills/supabase-migrations/scripts/update-types.sh
```
Regenerates TypeScript types from local database.

## Common Issues

### "Supabase not running"
```bash
supabase start
```

### "Migration file not found"
Check path: `supabase/migrations/[timestamp]_name.sql`

### "RLS validation failed"
Add `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` and `CREATE POLICY` statements.

### "Types not updating"
```bash
supabase db reset
supabase db push
bash .claude/skills/supabase-migrations/scripts/update-types.sh
```

### "Build errors after migration"
- Check type imports: `Database['public']['Tables']['table_name']['Row']`
- Update queries to match new schema
- Fix any breaking column renames

## Quick Reference

**Create migration:**
```bash
supabase migration new name
```

**Test locally:**
```bash
supabase db push
```

**Update types:**
```bash
supabase gen types typescript --local > lib/supabase/types.ts
```

**Apply to production:**
```bash
supabase db push --remote
```

## Related Documentation

- **Supabase security patterns:** [supabase-security.md](../../modules/supabase-security.md)
- **TypeScript type safety:** [typescript-standards.md](../../modules/typescript-standards.md)
- **Pre-commit checks:** Use `pre-commit-quality` skill after code changes
