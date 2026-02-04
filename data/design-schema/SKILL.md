---
name: design-schema
description: Design complete database schemas with tables, relationships, constraints, and indexes for Supabase. Triggers when user describes data models, entities, or requests schema design.
allowed-tools: Read, Write, Edit
---

# Schema Design Skill

Design comprehensive, normalized database schemas for Supabase applications.

## Purpose

Create well-structured database schemas following best practices for normalization, relationships, constraints, and indexing.

## When to Use

- User describes data requirements
- Requests database schema design
- Needs entity relationship modeling
- Asks about table structure
- Plans new feature requiring data storage

## Instructions

1. **Gather Requirements**
   - Identify all entities
   - Understand relationships
   - Determine data constraints
   - Plan for future growth

2. **Design Tables**
   - Choose appropriate column types
   - Add NOT NULL constraints
   - Define CHECK constraints
   - Include timestamps

3. **Map Relationships**
   - One-to-many with foreign keys
   - Many-to-many with junction tables
   - Self-referential if needed

4. **Add Indexes**
   - Primary keys (automatic)
   - Foreign keys
   - Frequently queried columns
   - Composite indexes for multi-column queries

5. **Implement RLS**
   - Enable on all tables
   - Create policies for each operation
   - Test policy effectiveness

6. **Generate Migration**
   - Complete SQL DDL
   - Include all constraints
   - Add helpful comments

## Example Output

```sql
-- Users and Posts Schema
-- =======================

CREATE TABLE public.users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  username TEXT UNIQUE NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,

  CONSTRAINT username_length CHECK (char_length(username) >= 3)
);

CREATE TABLE public.posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  author_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  published BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,

  CONSTRAINT title_length CHECK (char_length(title) >= 3)
);

CREATE INDEX idx_posts_author ON public.posts(author_id);
CREATE INDEX idx_posts_published ON public.posts(published, created_at DESC)
  WHERE published = true;

ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Published posts viewable by all"
  ON public.posts FOR SELECT
  USING (published = true);
```

## Output Format

1. Complete schema SQL
2. ER diagram description
3. Explanation of design decisions
4. Migration file
