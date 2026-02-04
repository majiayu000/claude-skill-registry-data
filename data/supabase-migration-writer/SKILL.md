---
name: supabase-migration-writer
description: Expert assistant for creating database migrations for the KR92 Bible Voice Supabase project. Use when creating database migrations, adding tables, modifying schemas, creating RPC functions, or writing rollback scripts.
---

# Supabase Migration Writer

## Capabilities
- Generate SQL migration files with proper structure
- Create tables with appropriate RLS policies
- Add indexes for performance
- Document schema changes in API docs
- Handle data type selection and constraints

## Migration File Structure

### Naming Convention
```
YYYYMMDDHHMMSS_description.sql
```

Example: `20250124120000_add_user_notes_table.sql`

### Location
```
supabase/migrations/
```

## Usage Examples

### Example 1: Create New Table Migration
**User:** "Create a migration for user_notes table to store Bible study notes"

**Assistant:**
```sql
-- Migration: 20250124120000_add_user_notes_table.sql

-- Create user_notes table
CREATE TABLE IF NOT EXISTS public.user_notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  verse_id UUID REFERENCES bible_schema.verses(id) ON DELETE CASCADE,
  osis TEXT,
  note_text TEXT NOT NULL,
  tags TEXT[] DEFAULT '{}',
  is_private BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Add indexes for performance
CREATE INDEX idx_user_notes_user_id ON public.user_notes(user_id);
CREATE INDEX idx_user_notes_verse_id ON public.user_notes(verse_id);
CREATE INDEX idx_user_notes_created_at ON public.user_notes(created_at DESC);
CREATE INDEX idx_user_notes_tags ON public.user_notes USING GIN(tags);

-- Enable RLS
ALTER TABLE public.user_notes ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own notes"
ON public.user_notes
FOR SELECT
TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "Users can insert own notes"
ON public.user_notes
FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own notes"
ON public.user_notes
FOR UPDATE
TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can delete own notes"
ON public.user_notes
FOR DELETE
TO authenticated
USING (user_id = auth.uid());

-- Trigger for updated_at
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON public.user_notes
FOR EACH ROW
EXECUTE FUNCTION public.handle_updated_at();

-- Comments for documentation
COMMENT ON TABLE public.user_notes IS 'User-created Bible study notes';
COMMENT ON COLUMN public.user_notes.verse_id IS 'Optional reference to specific verse';
COMMENT ON COLUMN public.user_notes.osis IS 'OSIS reference for the note';
COMMENT ON COLUMN public.user_notes.is_private IS 'Whether note is private or shareable';
```

### Example 2: Add Column Migration
**User:** "Add a 'color' column to highlights table"

**Assistant:**
```sql
-- Migration: 20250124121500_add_color_to_highlights.sql

-- Add color column with default
ALTER TABLE public.highlights
ADD COLUMN IF NOT EXISTS color TEXT DEFAULT 'yellow'
CHECK (color IN ('yellow', 'green', 'blue', 'pink', 'orange'));

-- Add index if color will be filtered
CREATE INDEX IF NOT EXISTS idx_highlights_color
ON public.highlights(color);

-- Update comment
COMMENT ON COLUMN public.highlights.color IS 'Highlight color: yellow, green, blue, pink, or orange';

-- Backfill existing rows if needed
UPDATE public.highlights
SET color = 'yellow'
WHERE color IS NULL;
```

### Example 3: Create RPC Function Migration
**User:** "Create RPC function to get user's recent notes"

**Assistant:**
```sql
-- Migration: 20250124122000_add_get_user_recent_notes_function.sql

CREATE OR REPLACE FUNCTION public.get_user_recent_notes(
  p_user_id UUID DEFAULT auth.uid(),
  p_limit INT DEFAULT 20
)
RETURNS TABLE (
  note_id UUID,
  verse_id UUID,
  osis TEXT,
  note_text TEXT,
  tags TEXT[],
  created_at TIMESTAMPTZ,
  verse_text TEXT,
  book_name TEXT,
  chapter_number INT,
  verse_number INT
)
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path TO 'public', 'bible_schema'
AS $$
  SELECT
    n.id AS note_id,
    n.verse_id,
    n.osis,
    n.note_text,
    n.tags,
    n.created_at,
    v.text AS verse_text,
    b.name_fi AS book_name,
    v.chapter_number,
    v.verse_number
  FROM user_notes n
  LEFT JOIN bible_schema.verses v ON n.verse_id = v.id
  LEFT JOIN bible_schema.books b ON v.book_id = b.id
  WHERE n.user_id = p_user_id
  ORDER BY n.created_at DESC
  LIMIT p_limit;
$$;

-- Grant execute permission
GRANT EXECUTE ON FUNCTION public.get_user_recent_notes TO authenticated;

-- Add comment
COMMENT ON FUNCTION public.get_user_recent_notes IS
'Get recent Bible study notes for a user with verse context';
```

### Example 4: Create Index Migration
**User:** "Add search index to user_notes.note_text"

**Assistant:**
```sql
-- Migration: 20250124123000_add_search_index_to_notes.sql

-- Add search vector column
ALTER TABLE public.user_notes
ADD COLUMN IF NOT EXISTS search_tsv tsvector;

-- Create function to update search vector
CREATE OR REPLACE FUNCTION public.user_notes_search_tsv_trigger()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.search_tsv := to_tsvector('finnish', coalesce(NEW.note_text, ''));
  RETURN NEW;
END;
$$;

-- Create trigger
CREATE TRIGGER user_notes_search_tsv_update
BEFORE INSERT OR UPDATE ON public.user_notes
FOR EACH ROW
EXECUTE FUNCTION public.user_notes_search_tsv_trigger();

-- Backfill existing rows
UPDATE public.user_notes
SET search_tsv = to_tsvector('finnish', note_text);

-- Create GIN index for fast search
CREATE INDEX idx_user_notes_search_tsv
ON public.user_notes USING GIN(search_tsv);

-- Create search function
CREATE OR REPLACE FUNCTION public.search_user_notes(
  p_query TEXT,
  p_user_id UUID DEFAULT auth.uid(),
  p_limit INT DEFAULT 50
)
RETURNS TABLE (
  note_id UUID,
  note_text TEXT,
  osis TEXT,
  created_at TIMESTAMPTZ,
  rank REAL
)
LANGUAGE sql
STABLE
AS $$
  SELECT
    id,
    note_text,
    osis,
    created_at,
    ts_rank(search_tsv, websearch_to_tsquery('finnish', p_query)) AS rank
  FROM user_notes
  WHERE user_id = p_user_id
    AND search_tsv @@ websearch_to_tsquery('finnish', p_query)
  ORDER BY rank DESC, created_at DESC
  LIMIT p_limit;
$$;
```

### Example 5: Rollback Migration
**User:** "Create rollback for user_notes table"

**Assistant:**
```sql
-- Migration: 20250124124000_rollback_user_notes.sql

-- Drop RLS policies
DROP POLICY IF EXISTS "Users can delete own notes" ON public.user_notes;
DROP POLICY IF EXISTS "Users can update own notes" ON public.user_notes;
DROP POLICY IF EXISTS "Users can insert own notes" ON public.user_notes;
DROP POLICY IF EXISTS "Users can view own notes" ON public.user_notes;

-- Drop triggers
DROP TRIGGER IF EXISTS set_updated_at ON public.user_notes;

-- Drop indexes
DROP INDEX IF EXISTS idx_user_notes_tags;
DROP INDEX IF EXISTS idx_user_notes_created_at;
DROP INDEX IF EXISTS idx_user_notes_verse_id;
DROP INDEX IF EXISTS idx_user_notes_user_id;

-- Drop table
DROP TABLE IF EXISTS public.user_notes;
```

## Migration Best Practices

### 1. Use IF NOT EXISTS / IF EXISTS
```sql
CREATE TABLE IF NOT EXISTS table_name (...);
DROP TABLE IF EXISTS table_name;
ALTER TABLE table_name ADD COLUMN IF NOT EXISTS column_name type;
```

### 2. Add Timestamps
```sql
created_at TIMESTAMPTZ DEFAULT now(),
updated_at TIMESTAMPTZ DEFAULT now()
```

### 3. Foreign Key Constraints
```sql
user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE
verse_id UUID REFERENCES bible_schema.verses(id) ON DELETE SET NULL
```

### 4. Indexes for Performance
```sql
-- Foreign keys
CREATE INDEX idx_table_user_id ON table_name(user_id);

-- Frequently filtered columns
CREATE INDEX idx_table_status ON table_name(status);

-- Timestamp queries
CREATE INDEX idx_table_created_at ON table_name(created_at DESC);

-- Full-text search
CREATE INDEX idx_table_search ON table_name USING GIN(search_tsv);

-- Array columns
CREATE INDEX idx_table_tags ON table_name USING GIN(tags);
```

### 5. Data Types

| Use Case | Type | Example |
|----------|------|---------|
| ID | UUID | `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` |
| User reference | UUID | `user_id UUID REFERENCES auth.users(id)` |
| Short text | TEXT | `name TEXT NOT NULL` |
| Long text | TEXT | `content TEXT` |
| Boolean | BOOLEAN | `is_active BOOLEAN DEFAULT true` |
| Timestamp | TIMESTAMPTZ | `created_at TIMESTAMPTZ DEFAULT now()` |
| Number | INTEGER | `count INTEGER DEFAULT 0` |
| Decimal | NUMERIC | `price NUMERIC(10,2)` |
| JSON | JSONB | `metadata JSONB DEFAULT '{}'` |
| Array | TEXT[] | `tags TEXT[] DEFAULT '{}'` |
| Enum | TEXT + CHECK | `status TEXT CHECK (status IN ('draft', 'published'))` |

### 6. Constraints
```sql
-- Not null
column_name TEXT NOT NULL

-- Unique
email TEXT UNIQUE

-- Check
age INT CHECK (age >= 0)

-- Default
status TEXT DEFAULT 'active'

-- Composite unique
UNIQUE(user_id, verse_id)
```

### 7. Comments
```sql
COMMENT ON TABLE table_name IS 'Description of table purpose';
COMMENT ON COLUMN table_name.column_name IS 'Description of column';
```

### 8. RLS Always
```sql
ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;
```

### 9. Updated At Trigger
```sql
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON table_name
FOR EACH ROW
EXECUTE FUNCTION public.handle_updated_at();
```

### 10. Security Definer for Functions
```sql
CREATE FUNCTION function_name(...)
LANGUAGE sql
SECURITY DEFINER
SET search_path TO 'public'
AS $$...$$;
```

## Schema Selection

| Schema | Purpose |
|--------|---------|
| `public` | User data, application tables |
| `bible_schema` | Bible text, AI system, topics |
| `feedback` | Feedback system |
| `auth` | Supabase auth (managed) |
| `storage` | Supabase storage (managed) |

## Testing Migrations

### Local Testing
```bash
# Apply migration
supabase db push

# Reset and reapply
supabase db reset
```

### Production Deployment
- Migrations auto-deploy via Lovable Cloud
- Test in dev environment first
- Review migration in Supabase Dashboard

## Documentation Updates

After creating migration, update:
1. `Docs/03-API.md` - Add new tables/functions
2. `Docs/02-DESIGN.md` - Update architecture if needed
3. `CLAUDE.MD` - Update schema reference if major change

## Advanced PostgreSQL Features

For advanced PostgreSQL-specific guidance, you can leverage the **pg-aiguide plugin** with these specialized skills:

### Available PostgreSQL Skills

1. **`pg:design-postgres-tables`**
   - Comprehensive PostgreSQL-specific table design reference
   - Data types, indexing strategies, constraints
   - Performance patterns and best practices
   - Advanced features (partitioning, triggers, etc.)

2. **`pg:setup-timescaledb-hypertables`**
   - Design and set up TimescaleDB hypertables
   - Configure compression, retention policies
   - Set up continuous aggregates for time-series data
   - Optimal partition and chunk configuration

3. **`pg:find-hypertable-candidates`**
   - Analyze existing tables for TimescaleDB conversion
   - Identify time-series data patterns
   - Evaluate performance improvement opportunities

4. **`pg:migrate-postgres-tables-to-hypertables`**
   - Step-by-step migration to TimescaleDB
   - Zero-downtime migration strategies
   - Performance validation and optimization

### When to Use pg-aiguide

- **Complex indexing requirements** - Multi-column indexes, partial indexes, expression indexes
- **Time-series data** - Bible reading analytics, usage logs, AI usage tracking
- **Performance optimization** - Query planning, index selection, partition strategies
- **Advanced data types** - Arrays, JSONB, full-text search, geometric types
- **PostgreSQL-specific features** - CTEs, window functions, materialized views

### Example Usage

```typescript
// If you need help with table design or time-series optimization:
// Invoke: /pg:design-postgres-tables
// Or: /pg:setup-timescaledb-hypertables

// For example, optimizing ai_usage_logs as a hypertable:
// 1. Use pg:find-hypertable-candidates to analyze ai_usage_logs
// 2. Use pg:setup-timescaledb-hypertables to configure optimal settings
// 3. Use pg:migrate-postgres-tables-to-hypertables for migration
```

## Related Documentation
- See `Docs/03-API.md` for current schema
- See `Docs/02-DESIGN.md` for architecture
- See `Docs/04-DEV-WORKFLOW.md` for deployment process
