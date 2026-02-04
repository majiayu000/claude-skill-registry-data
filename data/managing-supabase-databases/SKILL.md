---
name: managing-supabase-databases
description: Creating and managing Supabase PostgreSQL databases for StickerNest. Use when the user asks to create tables, add columns, write migrations, design schemas, implement RLS policies, optimize indexes, partition tables, or scale the database. Covers enterprise-grade security, performance optimization, and social features.
---

# Managing Supabase Databases for StickerNest

This skill covers enterprise-grade database design for Supabase/PostgreSQL, optimized for thousands of concurrent users with zero data leakage and cutting-edge performance.

## Database Location

- **Schema file**: `supabase/schema.sql`
- **Migrations**: `supabase/migrations/###_description.sql`
- **Services**: `src/services/` (TypeScript interfaces)

---

## Core Principles

### 1. Defense in Depth
Every table MUST have:
- Row Level Security (RLS) enabled
- Explicit policies for SELECT, INSERT, UPDATE, DELETE
- Indexes on all foreign keys and RLS filter columns
- Audit timestamps (`created_at`, `updated_at`)

### 2. Performance First
- Wrap RLS functions in `(SELECT ...)` for caching
- Use composite indexes for multi-column queries
- Partition time-series data (activities, notifications, chat)
- Add `CONCURRENTLY` to production index creation

### 3. Zero Trust
- Never rely on client validation alone
- Use CHECK constraints for data integrity
- Implement rate limiting via database functions
- Log sensitive operations for audit trails

---

## Migration File Template

```sql
-- Migration: ###_description.sql
-- Author: AI Assistant
-- Date: YYYY-MM-DD
-- Description: Brief description of changes
--
-- ROLLBACK INSTRUCTIONS:
-- To undo this migration, run the commands in the ROLLBACK section at bottom

-- =============================================
-- FORWARD MIGRATION
-- =============================================

BEGIN;

-- 1. Create tables
-- 2. Add indexes
-- 3. Enable RLS
-- 4. Create policies
-- 5. Add triggers
-- 6. Enable realtime

COMMIT;

-- =============================================
-- ROLLBACK (run manually if needed)
-- =============================================
/*
BEGIN;

DROP TABLE IF EXISTS public.new_table CASCADE;
-- Additional rollback commands...

COMMIT;
*/
```

---

## Table Design Template

```sql
CREATE TABLE IF NOT EXISTS public.{table_name} (
    -- Primary key (always UUID for distributed systems)
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

    -- Foreign keys with ON DELETE behavior
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,

    -- Core data columns
    content TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'archived', 'deleted')),

    -- JSONB for flexible metadata (indexed with GIN)
    metadata JSONB DEFAULT '{}'::jsonb,

    -- Audit timestamps
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,

    -- Soft delete (optional - for recoverable data)
    deleted_at TIMESTAMPTZ
);

-- CRITICAL: Index all foreign keys and RLS columns
CREATE INDEX idx_{table_name}_user_id ON public.{table_name}(user_id);
CREATE INDEX idx_{table_name}_created_at ON public.{table_name}(created_at DESC);

-- GIN index for JSONB queries (if using metadata filters)
CREATE INDEX idx_{table_name}_metadata ON public.{table_name} USING GIN (metadata);

-- Composite index for common query patterns
CREATE INDEX idx_{table_name}_user_status ON public.{table_name}(user_id, status)
    WHERE deleted_at IS NULL;
```

---

## RLS Policy Patterns

### Pattern 1: Owner-Only Access
```sql
-- Enable RLS (REQUIRED)
ALTER TABLE public.{table_name} ENABLE ROW LEVEL SECURITY;

-- CRITICAL: Wrap auth.uid() in SELECT for 100x performance boost
CREATE POLICY "{table_name}_select_own"
ON public.{table_name} FOR SELECT
TO authenticated  -- Restrict to authenticated users FIRST
USING (user_id = (SELECT auth.uid()));

CREATE POLICY "{table_name}_insert_own"
ON public.{table_name} FOR INSERT
TO authenticated
WITH CHECK (user_id = (SELECT auth.uid()));

CREATE POLICY "{table_name}_update_own"
ON public.{table_name} FOR UPDATE
TO authenticated
USING (user_id = (SELECT auth.uid()));

CREATE POLICY "{table_name}_delete_own"
ON public.{table_name} FOR DELETE
TO authenticated
USING (user_id = (SELECT auth.uid()));
```

### Pattern 2: Public Read, Private Write
```sql
CREATE POLICY "{table_name}_select_public"
ON public.{table_name} FOR SELECT
USING (true);  -- Anyone can read

CREATE POLICY "{table_name}_insert_authenticated"
ON public.{table_name} FOR INSERT
TO authenticated
WITH CHECK (user_id = (SELECT auth.uid()));
```

### Pattern 3: Team/Canvas Based Access
```sql
-- Optimized: Pre-filter by user's accessible resources
CREATE POLICY "{table_name}_select_canvas"
ON public.{table_name} FOR SELECT
TO authenticated
USING (
    canvas_id IN (
        SELECT c.id FROM canvases c
        WHERE c.user_id = (SELECT auth.uid())
           OR c.visibility = 'public'
    )
);
```

### Pattern 4: Friend/Follow Based Access
```sql
-- For content visible to friends only
CREATE POLICY "{table_name}_select_friends"
ON public.{table_name} FOR SELECT
TO authenticated
USING (
    user_id = (SELECT auth.uid())
    OR user_id IN (
        SELECT following_id FROM follows
        WHERE follower_id = (SELECT auth.uid())
    )
);
```

---

## High-Scale Patterns

### Time-Series Partitioning (for activities, notifications, chat)
```sql
-- Create partitioned table for activities (10M+ rows)
CREATE TABLE public.activities (
    id UUID DEFAULT gen_random_uuid(),
    actor_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    verb TEXT NOT NULL,
    object_type TEXT NOT NULL,
    object_id TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    PRIMARY KEY (id, created_at)  -- Include partition key in PK
) PARTITION BY RANGE (created_at);

-- Create monthly partitions (auto-create via cron or edge function)
CREATE TABLE activities_2025_01 PARTITION OF public.activities
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE activities_2025_02 PARTITION OF public.activities
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- Index on each partition (faster than global index)
CREATE INDEX idx_activities_2025_01_actor
ON activities_2025_01(actor_id, created_at DESC);
```

### Materialized Views for Analytics
```sql
-- Pre-compute expensive aggregations
CREATE MATERIALIZED VIEW public.user_stats AS
SELECT
    p.id AS user_id,
    COUNT(DISTINCT f1.follower_id) AS follower_count,
    COUNT(DISTINCT f2.following_id) AS following_count,
    COUNT(DISTINCT a.id) AS activity_count
FROM profiles p
LEFT JOIN follows f1 ON f1.following_id = p.id
LEFT JOIN follows f2 ON f2.follower_id = p.id
LEFT JOIN activities a ON a.actor_id = p.id
GROUP BY p.id;

-- Refresh via cron (not realtime)
CREATE UNIQUE INDEX idx_user_stats_user_id ON public.user_stats(user_id);
```

### Security Definer Functions (for complex RLS)
```sql
-- Create a function that bypasses RLS for efficiency
CREATE OR REPLACE FUNCTION public.get_user_accessible_canvases(user_uuid UUID)
RETURNS SETOF UUID
LANGUAGE sql
SECURITY DEFINER  -- Runs with creator's permissions
STABLE           -- Can be cached within transaction
AS $$
    SELECT id FROM canvases
    WHERE user_id = user_uuid
       OR visibility = 'public'
$$;

-- Use in RLS policy
CREATE POLICY "canvas_access"
ON public.widgets FOR SELECT
USING (
    canvas_id IN (SELECT * FROM public.get_user_accessible_canvases((SELECT auth.uid())))
);
```

---

## Social Features Schema

### Chat Messages (with threading)
```sql
CREATE TABLE IF NOT EXISTS public.chat_messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    canvas_id TEXT NOT NULL REFERENCES public.canvases(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    content TEXT NOT NULL CHECK (char_length(content) <= 10000),
    reply_to UUID REFERENCES public.chat_messages(id) ON DELETE SET NULL,
    metadata JSONB DEFAULT '{}'::jsonb,  -- For reactions, attachments
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    deleted_at TIMESTAMPTZ  -- Soft delete for moderation
);

-- Performance indexes
CREATE INDEX idx_chat_messages_canvas_id
ON public.chat_messages(canvas_id, created_at DESC);
CREATE INDEX idx_chat_messages_user_id ON public.chat_messages(user_id);
CREATE INDEX idx_chat_messages_reply_to ON public.chat_messages(reply_to)
    WHERE reply_to IS NOT NULL;

-- RLS
ALTER TABLE public.chat_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "chat_select_canvas_access"
ON public.chat_messages FOR SELECT
TO authenticated
USING (
    canvas_id IN (
        SELECT id FROM canvases
        WHERE user_id = (SELECT auth.uid())
           OR visibility IN ('public', 'unlisted')
    )
    AND deleted_at IS NULL
);

CREATE POLICY "chat_insert_authenticated"
ON public.chat_messages FOR INSERT
TO authenticated
WITH CHECK (user_id = (SELECT auth.uid()));

CREATE POLICY "chat_update_own"
ON public.chat_messages FOR UPDATE
TO authenticated
USING (user_id = (SELECT auth.uid()));

CREATE POLICY "chat_delete_own"
ON public.chat_messages FOR DELETE
TO authenticated
USING (user_id = (SELECT auth.uid()));
```

### User Blocks (bidirectional blocking)
```sql
CREATE TABLE IF NOT EXISTS public.blocks (
    blocker_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    blocked_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    reason TEXT,  -- Optional: 'spam', 'harassment', etc.
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    PRIMARY KEY (blocker_id, blocked_id),
    CHECK (blocker_id != blocked_id)  -- Can't block yourself
);

CREATE INDEX idx_blocks_blocked_id ON public.blocks(blocked_id);

ALTER TABLE public.blocks ENABLE ROW LEVEL SECURITY;

-- Only blocker can see their blocks
CREATE POLICY "blocks_select_own"
ON public.blocks FOR SELECT
TO authenticated
USING (blocker_id = (SELECT auth.uid()));

CREATE POLICY "blocks_insert_own"
ON public.blocks FOR INSERT
TO authenticated
WITH CHECK (blocker_id = (SELECT auth.uid()));

CREATE POLICY "blocks_delete_own"
ON public.blocks FOR DELETE
TO authenticated
USING (blocker_id = (SELECT auth.uid()));

-- Helper function to check if blocked
CREATE OR REPLACE FUNCTION public.is_blocked(user1 UUID, user2 UUID)
RETURNS BOOLEAN
LANGUAGE sql
STABLE
SECURITY DEFINER
AS $$
    SELECT EXISTS (
        SELECT 1 FROM blocks
        WHERE (blocker_id = user1 AND blocked_id = user2)
           OR (blocker_id = user2 AND blocked_id = user1)
    )
$$;
```

### Comments (polymorphic - works on any object)
```sql
CREATE TABLE IF NOT EXISTS public.comments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    -- Polymorphic reference: 'canvas', 'widget', 'activity'
    target_type TEXT NOT NULL CHECK (target_type IN ('canvas', 'widget', 'activity')),
    target_id TEXT NOT NULL,
    parent_id UUID REFERENCES public.comments(id) ON DELETE CASCADE,  -- Threading
    content TEXT NOT NULL CHECK (char_length(content) BETWEEN 1 AND 5000),
    upvotes INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    deleted_at TIMESTAMPTZ
);

-- Indexes for efficient querying
CREATE INDEX idx_comments_target
ON public.comments(target_type, target_id, created_at DESC);
CREATE INDEX idx_comments_user_id ON public.comments(user_id);
CREATE INDEX idx_comments_parent_id ON public.comments(parent_id)
    WHERE parent_id IS NOT NULL;

ALTER TABLE public.comments ENABLE ROW LEVEL SECURITY;

-- Public read (respecting blocks)
CREATE POLICY "comments_select_public"
ON public.comments FOR SELECT
USING (
    deleted_at IS NULL
    AND NOT public.is_blocked((SELECT auth.uid()), user_id)
);

CREATE POLICY "comments_insert_authenticated"
ON public.comments FOR INSERT
TO authenticated
WITH CHECK (user_id = (SELECT auth.uid()));

CREATE POLICY "comments_update_own"
ON public.comments FOR UPDATE
TO authenticated
USING (user_id = (SELECT auth.uid()));

CREATE POLICY "comments_delete_own"
ON public.comments FOR DELETE
TO authenticated
USING (user_id = (SELECT auth.uid()));
```

### Direct Messages (DMs)
```sql
-- DM conversations between two users
CREATE TABLE IF NOT EXISTS public.dm_conversations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user1_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    user2_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    last_message_at TIMESTAMPTZ DEFAULT now(),
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    UNIQUE (user1_id, user2_id),
    CHECK (user1_id < user2_id)  -- Canonical ordering
);

CREATE TABLE IF NOT EXISTS public.dm_messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    conversation_id UUID NOT NULL REFERENCES public.dm_conversations(id) ON DELETE CASCADE,
    sender_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    content TEXT NOT NULL CHECK (char_length(content) <= 10000),
    read_at TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_dm_messages_conversation
ON public.dm_messages(conversation_id, created_at DESC);
CREATE INDEX idx_dm_conversations_users
ON public.dm_conversations(user1_id, user2_id);

-- Helper to get or create conversation
CREATE OR REPLACE FUNCTION public.get_or_create_dm_conversation(other_user UUID)
RETURNS UUID
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    my_id UUID := auth.uid();
    conv_id UUID;
    u1 UUID;
    u2 UUID;
BEGIN
    -- Canonical ordering
    IF my_id < other_user THEN
        u1 := my_id; u2 := other_user;
    ELSE
        u1 := other_user; u2 := my_id;
    END IF;

    -- Check if blocked
    IF public.is_blocked(my_id, other_user) THEN
        RAISE EXCEPTION 'Cannot message blocked user';
    END IF;

    -- Get or create
    SELECT id INTO conv_id
    FROM dm_conversations
    WHERE user1_id = u1 AND user2_id = u2;

    IF conv_id IS NULL THEN
        INSERT INTO dm_conversations (user1_id, user2_id)
        VALUES (u1, u2)
        RETURNING id INTO conv_id;
    END IF;

    RETURN conv_id;
END;
$$;
```

---

## Triggers

### Auto-Update Timestamps
```sql
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables with updated_at
CREATE TRIGGER update_{table_name}_updated_at
    BEFORE UPDATE ON public.{table_name}
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();
```

### Create Notification on Follow
```sql
CREATE OR REPLACE FUNCTION public.create_follow_notification()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO notifications (recipient_id, actor_id, type, metadata)
    VALUES (
        NEW.following_id,
        NEW.follower_id,
        'follow',
        jsonb_build_object('follower_id', NEW.follower_id)
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER on_follow_create_notification
    AFTER INSERT ON public.follows
    FOR EACH ROW
    EXECUTE FUNCTION public.create_follow_notification();
```

---

## Realtime Configuration

```sql
-- Enable realtime for tables that need live updates
ALTER PUBLICATION supabase_realtime ADD TABLE public.chat_messages;
ALTER PUBLICATION supabase_realtime ADD TABLE public.notifications;
ALTER PUBLICATION supabase_realtime ADD TABLE public.dm_messages;
ALTER PUBLICATION supabase_realtime ADD TABLE public.activities;

-- Note: profiles, follows, blocks should NOT be realtime
-- (too many updates, use polling or explicit refresh)
```

---

## Performance Checklist

Before deploying any migration:

- [ ] All foreign keys have indexes
- [ ] RLS filter columns have indexes
- [ ] `auth.uid()` wrapped in `(SELECT ...)`
- [ ] Role restrictions (`TO authenticated`) on policies
- [ ] Composite indexes for common query patterns
- [ ] GIN indexes on JSONB columns used in queries
- [ ] Soft delete for recoverable data
- [ ] CHECK constraints for data validation
- [ ] Triggers for auto-computed fields
- [ ] Realtime enabled only where needed
- [ ] Rollback instructions documented

---

## Existing Schema Reference

| Table | File | Status |
|-------|------|--------|
| `canvases` | `supabase/schema.sql` | Complete |
| `widget_instances` | `supabase/schema.sql` | Complete |
| `pipelines` | `supabase/schema.sql` | Complete |
| `profiles` | `migrations/003_social_layer.sql` | Complete |
| `follows` | `migrations/003_social_layer.sql` | Complete |
| `activities` | `migrations/003_social_layer.sql` | Complete |
| `notifications` | `migrations/003_social_layer.sql` | Complete |
| `chat_messages` | **MISSING** - Service expects it | Needs migration |
| `blocks` | **MISSING** - Service expects it | Needs migration |
| `comments` | **MISSING** - Widget expects it | Needs migration |
| `dm_conversations` | **MISSING** | Needs migration |
| `dm_messages` | **MISSING** | Needs migration |

---

## Sources & Best Practices

- [Supabase RLS Performance Guide](https://supabase.com/docs/guides/troubleshooting/rls-performance-and-best-practices-Z5Jjwv)
- [Managing PostgreSQL Indexes](https://supabase.com/docs/guides/database/postgres/indexes)
- [Row Level Security Docs](https://supabase.com/docs/guides/database/postgres/row-level-security)
