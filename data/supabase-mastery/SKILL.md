---
name: supabase-mastery
description: Master Supabase patterns for migrations, RLS policies, pgvector, and authentication. Use when creating database schemas, writing migrations, implementing row-level security, setting up auth, or debugging Supabase issues. Triggers on "supabase migration", "RLS policy", "row level security", "pgvector", "supabase auth", "magic link".
---

# Supabase Mastery for Scientia Stack

Patterns from 18 production Supabase projects.

## Migration Workflow

### Creating Migrations

```bash
# Create timestamped migration
supabase migration new feature_name

# This creates: supabase/migrations/YYYYMMDDHHMMSS_feature_name.sql
```

### Migration File Structure

```sql
-- supabase/migrations/001_initial_schema.sql

-- Create tables
CREATE TABLE IF NOT EXISTS posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    sentiment TEXT CHECK (sentiment IN ('bullish', 'bearish', 'neutral')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);

-- Enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Users can view own posts"
    ON posts FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own posts"
    ON posts FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own posts"
    ON posts FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own posts"
    ON posts FOR DELETE
    USING (auth.uid() = user_id);
```

### Running Migrations

```bash
# Apply to local
supabase db reset

# Apply to remote
supabase db push

# Check status
supabase migration list
```

## Row Level Security (RLS) Patterns

### Pattern 1: User Isolation

```sql
-- Users can only access their own data
CREATE POLICY "user_isolation"
    ON table_name
    FOR ALL
    USING (auth.uid() = user_id);
```

### Pattern 2: Public Read, Private Write

```sql
-- Anyone can read, only owner can write
CREATE POLICY "public_read"
    ON posts FOR SELECT
    USING (true);

CREATE POLICY "owner_write"
    ON posts FOR INSERT
    WITH CHECK (auth.uid() = user_id);
```

### Pattern 3: Tier-Based Access

```sql
-- Based on user subscription tier
CREATE POLICY "tier_based_access"
    ON premium_features
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM user_subscriptions
            WHERE user_id = auth.uid()
            AND tier IN ('pro', 'premium', 'enterprise')
            AND expires_at > NOW()
        )
    );
```

### Pattern 4: Service Role Bypass

```sql
-- Allow service role to bypass RLS (for backend)
CREATE POLICY "service_role_bypass"
    ON table_name
    FOR ALL
    TO service_role
    USING (true);
```

## pgvector for RAG

### Enable Extension

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### Create Embeddings Table

```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding VECTOR(1536),  -- OpenAI dimensions (but we don't use OpenAI!)
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for similarity search
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
```

### Similarity Search Function

```sql
CREATE OR REPLACE FUNCTION match_documents(
    query_embedding VECTOR(1536),
    match_threshold FLOAT DEFAULT 0.7,
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    id UUID,
    content TEXT,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        d.id,
        d.content,
        1 - (d.embedding <=> query_embedding) AS similarity
    FROM documents d
    WHERE 1 - (d.embedding <=> query_embedding) > match_threshold
    ORDER BY d.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
```

## Authentication Patterns

### Magic Link (Email + Phone)

Configure in Supabase Dashboard:
1. Authentication → Providers → Email
2. Enable "Confirm email" and "Secure email change"
3. Set redirect URLs:
   - `https://your-app.vercel.app/feed`
   - `https://your-app.vercel.app`

### Frontend Implementation

```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
    process.env.VITE_SUPABASE_URL!,
    process.env.VITE_SUPABASE_ANON_KEY!
)

// Send magic link
const { error } = await supabase.auth.signInWithOtp({
    email: 'user@example.com',
    options: {
        emailRedirectTo: `${window.location.origin}/feed`
    }
})

// Check session
const { data: { session } } = await supabase.auth.getSession()
```

### Backend Service Role

```python
from supabase import create_client

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_KEY"]  # Service role for backend
)

# Service role bypasses RLS
data = supabase.table("posts").select("*").execute()
```

## Common Patterns

### JSONB for Flexible Data

```sql
CREATE TABLE user_settings (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id),
    preferences JSONB DEFAULT '{
        "theme": "dark",
        "notifications": true,
        "language": "en"
    }'::JSONB,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Query JSONB
SELECT * FROM user_settings
WHERE preferences->>'theme' = 'dark';
```

### Auto-Update Timestamps

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_posts_updated_at
    BEFORE UPDATE ON posts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

### Soft Deletes

```sql
ALTER TABLE posts ADD COLUMN deleted_at TIMESTAMPTZ;

-- Update RLS to filter deleted
CREATE POLICY "hide_deleted"
    ON posts FOR SELECT
    USING (deleted_at IS NULL AND auth.uid() = user_id);
```

## Debugging

### Check RLS Policies

```sql
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE tablename = 'your_table';
```

### Test as User

```sql
-- Set role to test RLS
SET ROLE authenticated;
SET request.jwt.claim.sub = 'user-uuid-here';

-- Run query
SELECT * FROM posts;

-- Reset
RESET ROLE;
```

### Common Issues

1. **"new row violates row-level security policy"**
   - Check INSERT policy `WITH CHECK` clause
   - Ensure `auth.uid()` matches user_id

2. **Empty results despite data existing**
   - RLS blocking access
   - Check SELECT policy `USING` clause

3. **Service role not working**
   - Ensure using `SUPABASE_SERVICE_KEY` not `ANON_KEY`
   - Check service role policy exists
