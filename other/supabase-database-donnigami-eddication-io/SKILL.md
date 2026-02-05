---
name: supabase-database
description: World-class expert Supabase database specialist covering PostgreSQL, real-time subscriptions, authentication, storage, RLS policies, and Edge Functions. Use when designing databases, writing queries, implementing authentication, setting up real-time features, or building production-grade applications with Supabase.
---

# Supabase Database Expert - World-Class Edition

## Project Context: DriverConnect (eddication.io)

**IMPORTANT**: This project is a Fuel Delivery Management System using Supabase as the primary database.

### Supabase Project Details

- **Project URL**: <https://supabase.com/dashboard/project/myplpshpcordggbbtblg>
- **Dashboard**: <https://supabase.com/dashboard/project/myplpshpcordggbbtblg/sql/new>
- **Main Folder**: `PTGLG/driverconnect/`
- **Migrations Folder**: `supabase/migrations/`
- **Edge Functions**: `supabase/functions/`

### Complete Database Schema Reference

📄 **Full Schema Documentation**: [docs/database-schema-reference.md](../../../docs/database-schema-reference.md)

This document contains:

- Complete table definitions with all columns
- Indexes, constraints, and foreign keys
- RLS policies for each table
- Storage buckets configuration
- Database functions and triggers
- Migration files reference

### Key Database Tables (Live Status: 16 tables exist)

| Category | Table | Purpose | Key Fields |
| :--- | :--- | :--- | :--- |
| **Core Jobs** | `jobdata` | Delivery jobs/stops | reference, ship_to_code, status, checkin/checkout |
| | `driver_jobs` | Trip headers (actual name) | reference, vehicle_desc, drivers, status |
| | `driver_stop` | Individual stops (actual name) | trip_id, sequence, destination_name, status |
| **User Mgmt** | `user_profiles` | Driver/user profiles | user_id (LINE), status (PENDING/APPROVED), user_type |
| **Location** | `station` | Service stations (PTC) | plant code, stationKey, lat/lng |
| | `customer` | Customer locations | stationKey, name, lat/lng |
| | `origin` | Job departure points | originKey, routeCode, name |
| **Tracking** | `driver_live_locations` | Real-time GPS | driver_user_id, lat/lng, last_updated |
| | `driver_logs` | Audit trail | action, details, location |
| **Safety** | `driver_alcohol_checks` | Alcohol tests (actual name) | alcohol_value, image_url, checked_at |
| | `fuel_siphoning` | Siphoning incidents | liters, siphon_date, evidence_image_url |
| **Monitoring** | `admin_alerts` | Alert rules | rule_type, threshold, recipients |
| | `triggered_alerts` | Triggered alerts | alert_rule_id, message, status |
| | `app_settings` | App config | id, value, type |
| | `report_schedules` | Report schedules | report_name, frequency, recipients |
| **Reviews** | `review_data` | Service reviews | rating, signature_url, feedback |

### Tables NOT Found (from migrations)

| Table | Note |
| :--- | :--- |
| `trips` | Use `driver_jobs` instead |
| `trip_stops` | Use `driver_stop` instead |
| `profiles` (CRM) | CRM tables not created |
| `tiers` | CRM tables not created |
| `news_promotions` | CRM tables not created |
| `customer_segments` | CRM tables not created |
| `alcohol_checks` | Use `driver_alcohol_checks` instead |
| `google_chat_webhooks` | Not created |

### Current RLS Status

⚠️ **SECURITY ALERT**: Anon RLS policies use `WITH CHECK (true)` - requires application-layer ownership verification via `shared/driver-auth.js`

### Edge Functions Deployed

- `geocode` - Nominatim geocoding service (avoid CORS)
- `enrich-coordinates` - Location coordinate enrichment

### Migration Workflow

```bash
cd supabase
node apply-migration.js  # Outputs SQL to console
# Copy SQL to Supabase Dashboard > SQL Editor > Run
```

---

## Overview

You are a world-class expert in Supabase - the open-source Firebase alternative. You possess deep knowledge of PostgreSQL, real-time subscriptions, authentication systems, object storage, Row Level Security, and serverless edge functions. You design scalable, secure, and performant database architectures for production applications.

---

# Philosophy & Principles

## Core Principles
1. **Security First** - RLS policies for every table, defense in depth
2. **Performance Matters** - Proper indexing, query optimization, connection pooling
3. **Data Integrity** - Constraints, validations, and transactions
4. **Scalability** - Design for growth from day one
5. **Observability** - Logging, metrics, and monitoring
6. **Developer Experience** - Type-safe queries, clear error messages

## Best Practices Mindset
- **Always use RLS** - Never trust client-side checks
- **Use prepared statements** - Prevent SQL injection
- **Index strategically** - Not everything needs an index
- **Document schemas** - Comments on tables and columns
- **Version control migrations** - Every change in source control
- **Test in staging** - Never test in production

---

# Architecture Overview

## Supabase Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Application Layer                       │
│    Web App    │    Mobile App    │    Backend Services     │
├─────────────────────────────────────────────────────────────┤
│                     Supabase Client SDKs                    │
│    JavaScript  │    Python  │    Dart  │    Swift  │  Go   │
├─────────────────────────────────────────────────────────────┤
│                    Supabase Platform API                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │   Auth   │ │ Database │ │ Storage  │ │  Realtime│       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
├─────────────────────────────────────────────────────────────┤
│                    PostgreSQL Database                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │   RLS    │ │  Triggers│ │ Functions│ │  Extensions│      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
├─────────────────────────────────────────────────────────────┤
│                    Infrastructure Layer                     │
│    PostgreSQL 15+  │  pg_catalog  │  Logical Replication   │
└─────────────────────────────────────────────────────────────┘
```

## Service Overview

| Service | Purpose | Key Features |
|---------|---------|--------------|
| **Database** | PostgreSQL 15+ | RLS, Functions, Triggers, Extensions |
| **Auth** | User management | JWT, OAuth, SAML, Magic Links |
| **Storage** | Object storage | S3-compatible, RLS, Transformations |
| **Realtime** | Live updates | WebSocket, Presence, Broadcast |
| **Edge Functions** | Serverless | Deno runtime, global CDN |
| **Vector** | AI/ML | Embeddings, similarity search |
| **Studio** | Management UI | Table editor, SQL editor, Logs |

---

# Database Design Mastery

## Schema Design Patterns

### Naming Conventions
```sql
-- Tables: plural, snake_case
CREATE TABLE users (...);
CREATE TABLE user_profiles (...);
CREATE TABLE orders (...);
CREATE TABLE order_items (...);

-- Columns: snake_case
CREATE TABLE users (
  user_id UUID,
  first_name TEXT,
  email_address TEXT,
  created_at TIMESTAMPTZ
);

-- Indexes: idx_table_columns
CREATE INDEX idx_users_email ON users(email_address);
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at);

-- Foreign keys: fk_table_column
CONSTRAINT fk_orders_user_id FOREIGN KEY (user_id) REFERENCES users(id)

-- Functions: verb_noun
create_function get_user_orders()
create_function calculate_order_total()

-- Triggers: trg_table_action
CREATE TRIGGER trg_users_updated_at
```

### Primary Key Strategies
```sql
-- 1. UUID v4 (Random) - Best for distributed systems
id UUID PRIMARY KEY DEFAULT gen_random_uuid()

-- 2. UUID v7 (Time-sorted) - Best for indexes and clustering
-- Requires: CREATE EXTENSION IF NOT EXISTS pgcrypto;
id UUID PRIMARY KEY DEFAULT uuid_generate_v7()

-- 3. CUID - Collision-resistant, sortable
id TEXT PRIMARY KEY DEFAULT cuid_generate()

-- 4. Custom sequential prefix
order_id TEXT PRIMARY KEY DEFAULT
  'ORD-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' ||
  LPAD(nextval('order_seq')::TEXT, 6, '0')

-- 5. Composite keys (for junction tables)
CREATE TABLE user_roles (
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
  PRIMARY KEY (user_id, role_id)
);
```

### Foreign Key Best Practices
```sql
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status ORDER_STATUS NOT NULL DEFAULT 'pending',
  shipping_address_id UUID REFERENCES addresses(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ON DELETE options:
-- CASCADE: Delete child rows when parent is deleted
-- SET NULL: Set FK to NULL (requires column to be nullable)
-- SET DEFAULT: Set FK to default value
-- RESTRICT: Prevent deletion (default)
-- NO ACTION: Similar to RESTRICT but deferrable

-- Index foreign keys for performance
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_shipping_address ON orders(shipping_address_id);
```

### Timestamps Patterns
```sql
-- Standard timestamp columns
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMPTZ  -- Soft delete
);

-- Auto-update trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Apply to all tables with updated_at
CREATE TRIGGER update_products_updated_at
  BEFORE UPDATE ON products
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();
```

### Enum Types
```sql
-- Create enum types
CREATE TYPE order_status AS ENUM (
  'pending',
  'confirmed',
  'processing',
  'shipped',
  'delivered',
  'cancelled',
  'refunded'
);

CREATE TYPE user_role AS ENUM (
  'customer',
  'driver',
  'admin',
  'superadmin'
);

-- Use in tables
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  status order_status NOT NULL DEFAULT 'pending'
);

-- Alter enum (add new value)
ALTER TYPE order_status ADD VALUE 'archived' AFTER 'refunded';

-- Note: Cannot remove values or rename easily
-- Use views or mappings for display names
```

---

# Row Level Security (RLS) Deep Dive

## RLS Fundamentals

```sql
-- Enable RLS on a table
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Disable for service role (troubleshooting)
ALTER TABLE profiles FORCE ROW LEVEL SECURITY;
```

## Policy Patterns

### 1. User Own Data Only
```sql
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username TEXT UNIQUE,
  avatar_url TEXT,
  full_name TEXT
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Users can view their own profile
CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

-- Users can insert their own profile
CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- Users can delete their own profile
CREATE POLICY "Users can delete own profile"
  ON profiles FOR DELETE
  USING (auth.uid() = id);
```

### 2. Public Read, Authenticated Write
```sql
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),
  title TEXT NOT NULL,
  content TEXT,
  published BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Everyone can view published posts
CREATE POLICY "Public can view published posts"
  ON posts FOR SELECT
  USING (published = true);

-- Authenticated users can view all their posts
CREATE POLICY "Users can view own posts"
  ON posts FOR SELECT
  USING (auth.uid() = user_id);

-- Authenticated users can create posts
CREATE POLICY "Authenticated users can create posts"
  ON posts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can only update their own posts
CREATE POLICY "Users can update own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);
```

### 3. Role-Based Access Control (RBAC)
```sql
-- User roles table
CREATE TABLE user_roles (
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  role user_role NOT NULL,
  granted_at TIMESTAMPTZ DEFAULT NOW(),
  granted_by UUID REFERENCES auth.users(id),
  PRIMARY KEY (user_id, role)
);

ALTER TABLE user_roles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own roles"
  ON user_roles FOR SELECT
  USING (auth.uid() = user_id);

-- Admin policies for sensitive data
CREATE TABLE sensitive_data (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  data TEXT NOT NULL
);

ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

-- Only admins can do anything
CREATE POLICY "Admins can do everything"
  ON sensitive_data FOR ALL
  USING (
    auth.uid() IN (
      SELECT user_id FROM user_roles WHERE role = 'admin'
    )
  );

-- Service role bypasses RLS (for backend operations)
```

### 4. Team/Organization Multi-Tenancy
```sql
-- Team membership
CREATE TABLE team_members (
  team_id UUID NOT NULL,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  role TEXT NOT NULL DEFAULT 'member', -- owner, admin, member, guest
  joined_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (team_id, user_id)
);

-- Team resources
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  team_id UUID NOT NULL,
  name TEXT NOT NULL,
  created_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Users can access projects from their teams
CREATE POLICY "Team members can view team projects"
  ON projects FOR SELECT
  USING (
    team_id IN (
      SELECT team_id FROM team_members WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Team members can insert team projects"
  ON projects FOR INSERT
  WITH CHECK (
    team_id IN (
      SELECT team_id FROM team_members WHERE user_id = auth.uid()
    )
  );

CREATE POLICY "Team members can update team projects"
  ON projects FOR UPDATE
  USING (
    team_id IN (
      SELECT team_id FROM team_members WHERE user_id = auth.uid()
    )
  );
```

### 5. Hierarchical Data Access
```sql
-- Organization hierarchy
CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  parent_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  path LTREE NOT NULL  -- Requires: CREATE EXTENSION ltree;
);

-- Users can access data in their org and all children
CREATE POLICY "Users can access org and sub-orgs"
  ON organizations FOR SELECT
  USING (
    id IN (
      WITH RECURSIVE org_tree AS (
        SELECT id FROM organizations WHERE id = (
          SELECT org_id FROM user_orgs WHERE user_id = auth.uid()
        )
        UNION ALL
        SELECT o.id FROM organizations o
        INNER JOIN org_tree ot ON o.parent_id = ot.id
      )
      SELECT id FROM org_tree
    )
  );
```

### 6. Time-Based Access
```sql
-- Subscriptions with expiration
CREATE TABLE subscriptions (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id),
  plan TEXT NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL
);

ALTER TABLE premium_content ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Active subscribers can access premium content"
  ON premium_content FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM subscriptions
      WHERE user_id = auth.uid()
      AND expires_at > NOW()
    )
  );
```

---

# Advanced PostgreSQL Features

## Full-Text Search

```sql
-- Basic full-text search
CREATE TABLE articles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  content TEXT,
  search_vector tsvector GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(content, '')), 'B')
  ) STORED
);

-- GIN index for fast searching
CREATE INDEX articles_search_idx ON articles USING GIN (search_vector);

-- Search query
SELECT
  id,
  title,
  ts_headline('english', content, to_tsquery('english', 'search & query')) as preview
FROM articles
WHERE search_vector @@ to_tsquery('english', 'search & query')
ORDER BY ts_rank(search_vector, to_tsquery('english', 'search & query')) DESC
LIMIT 20;

-- Advanced: Phrase search
WHERE search_vector @@ phraseto_tsquery('english', 'exact phrase');

-- Advanced: Fuzzy search with trigrams
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX articles_content_trgm_idx ON articles USING GIN (content gin_trgm_ops);

SELECT * FROM articles
WHERE content % 'fuzzy serch qery'  -- Finds close matches
ORDER BY similarity(content, 'fuzzy serch qery') DESC;
```

## JSONB Operations

```sql
-- JSONB column for flexible schema
CREATE TABLE settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  config JSONB DEFAULT '{}'::jsonb,
  metadata JSONB
);

-- GIN index for JSONB
CREATE INDEX settings_config_idx ON settings USING GIN (config);

-- Query operators
SELECT * FROM settings WHERE config->>'theme' = 'dark';
SELECT * FROM settings WHERE config->'preferences'->'notifications'->>'email' = 'true';
SELECT * FROM settings WHERE config @> '{"theme": "dark"}';  -- Contains
SELECT * FROM settings WHERE config ? 'theme';  -- Has key
SELECT * FROM settings WHERE config ?| array['theme', 'language'];  -- Has any key

-- Update JSONB
UPDATE settings
SET config = jsonb_set(config, '{theme}', '"light"')
WHERE id = $1;

-- Append to array
UPDATE settings
SET config = jsonb_set(config, '{items}', config->'items' || '"new_item"')
WHERE id = $1;

-- Remove key
UPDATE settings
SET config = config - 'deprecated_field'
WHERE id = $1;

-- JSONB aggregation
SELECT
  user_id,
  jsonb_object_agg(key, value) as aggregated_config
FROM settings
GROUP BY user_id;
```

## Array Operations

```sql
-- Arrays in columns
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tags TEXT[] DEFAULT '{}',
  mentions UUID[] DEFAULT '{}'
);

-- Array index
CREATE INDEX posts_tags_idx ON posts USING GIN (tags);

-- Query arrays
SELECT * FROM posts WHERE 'tech' = ANY(tags);
SELECT * FROM posts WHERE tags @> ARRAY['tech', 'programming'];  -- Contains all
SELECT * FROM posts WHERE tags && ARRAY['tech', 'news'];  -- Contains any
SELECT * FROM posts WHERE array_length(tags, 1) > 5;

-- Modify arrays
UPDATE posts SET tags = array_append(tags, 'new_tag') WHERE id = $1;
UPDATE posts SET tags = array_remove(tags, 'old_tag') WHERE id = $1;
UPDATE posts SET tags = array_prepend('first_tag', tags) WHERE id = $1;

-- Unnest array to rows
SELECT unnest(ARRAY[1,2,3]) AS value;

-- Aggregate rows to array
SELECT ARRAY_AGG(id) FROM posts;
SELECT ARRAY_AGG(DISTINCT tag) FROM posts, unnest(tags) AS tag;
```

## Window Functions

```sql
-- Row numbers
SELECT
  id,
  user_id,
  created_at,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS row_num,
  RANK() OVER (PARTITION BY user_id ORDER BY created_at) AS rank,
  DENSE_RANK() OVER (PARTITION BY user_id ORDER BY created_at) AS dense_rank
FROM orders;

-- Running totals
SELECT
  id,
  amount,
  SUM(amount) OVER (
    ORDER BY created_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total
FROM transactions;

-- Moving averages
SELECT
  date,
  value,
  AVG(value) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS moving_avg_7day
FROM metrics;

-- First/last values
SELECT
  user_id,
  event_time,
  event_type,
  FIRST_VALUE(event_type) OVER (
    PARTITION BY user_id ORDER BY event_time
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS first_event,
  LAST_VALUE(event_type) OVER (
    PARTITION BY user_id ORDER BY event_time
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS last_event
FROM events;
```

## CTEs (Common Table Expressions)

```sql
-- Basic CTE
WITH user_stats AS (
  SELECT
    user_id,
    COUNT(*) as order_count,
    SUM(total) as total_spent
  FROM orders
  GROUP BY user_id
)
SELECT u.*, us.order_count, us.total_spent
FROM users u
JOIN user_stats us ON u.id = us.user_id;

-- Recursive CTE (hierarchy)
WITH RECURSIVE org_tree AS (
  -- Base case: top level orgs
  SELECT id, name, parent_id, 1 AS level
  FROM organizations
  WHERE parent_id IS NULL

  UNION ALL

  -- Recursive case: children
  SELECT o.id, o.name, o.parent_id, ot.level + 1
  FROM organizations o
  INNER JOIN org_tree ot ON o.parent_id = ot.id
)
SELECT * FROM org_tree ORDER BY level, name;

-- CTE for data modification
WITH new_orders AS (
  INSERT INTO orders (user_id, total)
  VALUES ($1, $2)
  RETURNING *
)
INSERT INTO order_log (order_id, status)
SELECT id, 'created' FROM new_orders;
```

## Materialized Views

```sql
-- Create materialized view for expensive aggregations
CREATE MATERIALIZED VIEW user_order_summary AS
SELECT
  u.id,
  u.email,
  COUNT(o.id) FILTER (WHERE o.status = 'completed') as completed_orders,
  COALESCE(SUM(o.total) FILTER (WHERE o.status = 'completed'), 0) as total_spent,
  MAX(o.created_at) as last_order_at
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.email
WITH DATA;

-- Create unique index for concurrent refresh
CREATE UNIQUE INDEX user_order_summary_id_idx
  ON user_order_summary (id);

-- Refresh materialized view
REFRESH MATERIALIZED VIEW user_order_summary;

-- Concurrent refresh (doesn't block reads)
REFRESH MATERIALIZED VIEW CONCURRENTLY user_order_summary;
```

---

# Database Functions & Triggers

## Advanced Functions

```sql
-- Function with security definer (runs with elevated permissions)
CREATE OR REPLACE FUNCTION get_user_with_profile(user_id UUID)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  result JSONB;
BEGIN
  SELECT jsonb_build_object(
    'id', u.id,
    'email', u.email,
    'profile', p
  ) INTO result
  FROM auth.users u
  LEFT JOIN profiles p ON p.id = u.id
  WHERE u.id = get_user_with_profile.user_id;

  RETURN result;
END;
$$;

-- Grant execute to authenticated users
GRANT EXECUTE ON FUNCTION get_user_with_profile(UUID) TO authenticated;

-- Function returning table
CREATE OR REPLACE FUNCTION get_user_orders(user_id UUID, status_order TEXT DEFAULT NULL)
RETURNS TABLE (
  id UUID,
  total NUMERIC,
  status TEXT,
  created_at TIMESTAMPTZ
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT o.id, o.total, o.status, o.created_at
  FROM orders o
  WHERE o.user_id = get_user_orders.user_id
  AND (status_order IS NULL OR o.status = status_order)
  ORDER BY o.created_at DESC;
END;
$$;

-- Function with error handling
CREATE OR REPLACE FUNCTION transfer_funds(
  from_user UUID,
  to_user UUID,
  amount NUMERIC
)
RETURNS JSONB
LANGUAGE plpgsql
AS $$
DECLARE
  from_balance NUMERIC;
BEGIN
  -- Check sender's balance
  SELECT balance INTO from_balance
  FROM wallets
  WHERE user_id = from_user
  FOR UPDATE;  -- Lock row

  IF from_balance < amount THEN
    RAISE EXCEPTION 'Insufficient funds. Balance: %', from_balance;
  END IF;

  -- Perform transfer
  UPDATE wallets SET balance = balance - amount WHERE user_id = from_user;
  UPDATE wallets SET balance = balance + amount WHERE user_id = to_user;

  -- Log transaction
  INSERT INTO transactions (from_user, to_user, amount)
  VALUES (from_user, to_user, amount);

  RETURN jsonb_build_object('success', true, 'amount', amount);
EXCEPTION
  WHEN OTHERS THEN
    RETURN jsonb_build_object('success', false, 'error', SQLERRM);
END;
$$;
```

## Trigger Patterns

```sql
-- Auto-create profile on user signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name, avatar_url)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'full_name', ''),
    COALESCE(NEW.raw_user_meta_data->>'avatar_url', '')
  );
  RETURN NEW;
END;
$$;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION handle_new_user();

-- Audit logging trigger
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  table_name TEXT NOT NULL,
  record_id UUID NOT NULL,
  action TEXT NOT NULL,  -- INSERT, UPDATE, DELETE
  old_data JSONB,
  new_data JSONB,
  changed_by UUID,
  changed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  IF TG_OP = 'DELETE' THEN
    INSERT INTO audit_logs (table_name, record_id, action, old_data, changed_by)
    VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', row_to_json(OLD), auth.uid());
    RETURN OLD;
  ELSIF TG_OP = 'UPDATE' THEN
    INSERT INTO audit_logs (table_name, record_id, action, old_data, new_data, changed_by)
    VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', row_to_json(OLD), row_to_json(NEW), auth.uid());
    RETURN NEW;
  ELSIF TG_OP = 'INSERT' THEN
    INSERT INTO audit_logs (table_name, record_id, action, new_data, changed_by)
    VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', row_to_json(NEW), auth.uid());
    RETURN NEW;
  END IF;
END;
$$;

-- Apply to tables
CREATE TRIGGER audit_users
  AFTER INSERT OR UPDATE OR DELETE ON users
  FOR EACH ROW
  EXECUTE FUNCTION audit_trigger_func();

-- Soft delete trigger
CREATE OR REPLACE FUNCTION soft_delete_trigger()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.deleted_at = NOW();
  RETURN NEW;
END;
$$;

CREATE TRIGGER soft_delete_posts
  BEFORE DELETE ON posts
  FOR EACH ROW
  EXECUTE FUNCTION soft_delete_trigger();

-- Then use INSTEAD OF trigger or update instead of delete
-- Or: Override delete at application level
```

---

# Performance Optimization

## Indexing Strategies

```sql
-- B-tree index (default, best for equality and range queries)
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
-- Good for: WHERE user_id = $1 AND status = $2
-- Also good for: WHERE user_id = $1 (but not reverse)
-- Not useful for: WHERE status = $2

-- Partial index (smaller, faster)
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;
CREATE INDEX idx_recent_orders ON orders(created_at) WHERE created_at > NOW() - INTERVAL '1 year';

-- Unique index
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Covering index (INCLUDE columns for index-only scans)
CREATE INDEX idx_orders_user_created_covering
  ON orders(user_id, created_at)
  INCLUDE (status, total);

-- Expression index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
-- Use with: WHERE LOWER(email) = LOWER('user@example.com')

-- JSONB GIN index
CREATE INDEX idx_settings_config ON settings USING GIN (config);

-- JSONB path index (PostgreSQL 14+)
CREATE INDEX idx_settings_config_path ON settings USING GIN (
  jsonb_path_ops
);

-- Full-text search GIN index
CREATE INDEX idx_articles_search ON articles USING GIN (search_vector);

-- Concurrent index creation (doesn't block writes)
CREATE INDEX CONCURRENTLY idx_large_table_column ON large_table(column);
```

## Query Optimization

```sql
-- Analyze query performance
EXPLAIN ANALYZE
SELECT u.*, o.*
FROM users u
JOIN orders o ON o.user_id = u.id
WHERE u.email = 'user@example.com';

-- Common issues and fixes

-- 1. N+1 query problem
-- Bad: Multiple queries
-- SELECT * FROM posts WHERE user_id = $1;
-- For each post: SELECT * FROM comments WHERE post_id = $1;

-- Good: Single query with join
SELECT
  p.*,
  jsonb_agg(c) as comments
FROM posts p
LEFT JOIN comments c ON c.post_id = p.id
WHERE p.user_id = $1
GROUP BY p.id;

-- 2. Missing indexes
-- Check: EXPLAIN shows Seq Scan instead of Index Scan
-- Fix: Add appropriate index

-- 3. Functions in WHERE clause prevent index usage
-- Bad: WHERE LOWER(email) = 'test@example.com'
-- Good: WHERE email = 'test@example.com' (store lowercased)

-- 4. OR conditions often can't use index efficiently
-- Bad: WHERE email = $1 OR username = $1
-- Good: Separate queries or UNION

-- 5. Large OFFSET is slow
-- Bad: OFFSET 100000 LIMIT 10
-- Good: Use cursor-based pagination
SELECT * FROM posts
WHERE id > (SELECT id FROM posts ORDER BY id LIMIT 1 OFFSET 100000)
ORDER BY id
LIMIT 10;
```

## Connection Pooling

```sql
-- PgBouncer configuration for connection pooling

-- Transaction pooling mode (recommended for serverless)
[databases]
your_database = host=db.xxx.supabase.co port=5432 dbname=postgres

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 50
min_pool_size = 10
server_lifetime = 3600
server_idle_timeout = 600
server_connect_timeout = 15

-- Connection limits in Supabase
-- Check: SELECT count(*) FROM pg_stat_activity;
-- Set per-project connection limits in dashboard
```

---

# Realtime Subscriptions

## Realtime Setup

```sql
-- Enable replication for your tables
ALTER PUBLICATION supabase_realtime ADD TABLE products;

-- Enable for specific columns
ALTER PUBLICATION supabase_realtime
ADD TABLE products
WITH (publish = 'insert,update,delete');

-- Filter updates (only publish when specific columns change)
ALTER PUBLICATION supabase_realtime
ADD TABLE products
WITH (publish = 'update');
-- Then use row-level security to filter
```

## Client-Side Realtime

```typescript
// Subscribe to all changes
const channel = supabase
  .channel('custom-channel')
  .on(
    'postgres_changes',
    {
      event: '*',  // INSERT, UPDATE, DELETE, *
      schema: 'public',
      table: 'products'
    },
    (payload) => {
      console.log('Change received!', payload)
    }
  )
  .subscribe()

// Subscribe with filter
const channel = supabase
  .channel('products-changes')
  .on(
    'postgres_changes',
    {
      event: 'UPDATE',
      schema: 'public',
      table: 'products',
      filter: 'user_id=eq.user123'  // Only changes for this user
    },
    (payload) => console.log(payload)
  )
  .subscribe()

// Subscribe to specific row
const channel = supabase
  .channel('product-123')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'products',
      filter: 'id=eq.123'
    },
    (payload) => console.log(payload)
  )
  .subscribe()

// Unsubscribe
supabase.removeChannel(channel)
// or unsubscribe all
supabase.removeAllChannels()
```

## Presence System

```typescript
// Track user presence
const channel = supabase.channel('room-1')

// Track presence
channel
  .on('presence', { event: 'sync' }, () => {
    const newState = channel.presenceState()
    console.log('Sync', newState)
  })
  .on('presence', { event: 'join' }, ({ key, newPresences }) => {
    console.log('Join', key, newPresences)
  })
  .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
    console.log('Leave', key, leftPresences)
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      // Track current user
      await channel.track({
        user_id: userId,
        online_at: new Date().toISOString()
      })
    }
  })

// Untrack presence
await channel.untrack()
```

## Broadcast Features

```typescript
// Send broadcast to all subscribers
const channel = supabase.channel('chat-room')

channel
  .on('broadcast', { event: 'message' }, ({ payload }) => {
    console.log('Broadcast received', payload)
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      // Send broadcast
      await channel.send({
        type: 'broadcast',
        event: 'message',
        payload: { user: 'user1', message: 'Hello!' }
      })
    }
  })
```

---

# Authentication Deep Dive

## Auth Flows

```typescript
// Email/Password Signup
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'SecurePassword123!',
  options: {
    data: {
      first_name: 'John',
      last_name: 'Doe'
    },
    emailRedirectTo: `${window.location.origin}/auth/callback`
  }
})

// Email Confirmation
// User receives email, clicks confirmation link
// Handle redirect in your app:
const { data, error } = await supabase.auth.getSession()

// Sign In
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'SecurePassword123!'
})

// Sign Out
const { error } = await supabase.auth.signOut()

// Magic Link (Passwordless)
const { data, error } = await supabase.auth.signInWithOtp({
  email: 'user@example.com',
  options: {
    emailRedirectTo: `${window.location.origin}/auth/callback`
  }
})

// OAuth (Google, GitHub, etc.)
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: `${window.location.origin}/auth/callback`,
    queryParams: {
      access_type: 'offline',
      prompt: 'consent'
    }
  }
})

// Get current user
const { data: { user } } = await supabase.auth.getUser()

// Update user metadata
const { data, error } = await supabase.auth.updateUser({
  data: {
    display_name: 'John Doe'
  }
})

// Manage session
const { data: { session } } = await supabase.auth.getSession()
```

## JWT Handling

```typescript
// Access custom claims from JWT
// Note: This happens via RLS policies using auth.uid() and auth.jwt()

// Add custom claims via database trigger
CREATE OR REPLACE FUNCTION add_user_claims()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  -- Add custom claims to the user's raw_user_meta_data
  NEW.raw_user_meta_data = jsonb_set(
    COALESCE(NEW.raw_user_meta_data, '{}'::jsonb),
    '{role}',
    (SELECT role FROM user_profiles WHERE id = NEW.id)::jsonb
  );
  RETURN NEW;
END;
$$;

// Access claims in RLS
CREATE POLICY "Users with admin role can access"
ON sensitive_data FOR SELECT
USING (
  auth.jwt()->>'role' = 'admin'
);
```

## Multi-Factor Authentication (MFA)

```typescript
// Enable MFA for a user
const { data, error } = await supabase.auth.mfa.enroll({
  factorType: 'totp',
  friendlyName: 'My Authenticator App'
})

// Verify MFA challenge
const { data, error } = await supabase.auth.mfa.verify({
  factorId: factorId,
  challengeId: challengeId,
  code: '123456'
})

// List enrolled factors
const { data, error } = await supabase.auth.mfa.listFactors()
```

---

# Storage Management

## Storage Buckets

```sql
-- Create bucket via SQL
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', true);

-- Or via client
const { data, error } = await supabase.storage.createBucket('avatars', {
  public: true,
  fileSizeLimit: 1024 * 1024 * 2,  // 2MB
  allowedMimeTypes: ['image/png', 'image/jpeg', 'image/webp']
})

-- Enable RLS for storage
ALTER TABLE storage.objects ENABLE ROW LEVEL SECURITY;

-- Public read access for avatars
CREATE POLICY "Public avatars are viewable"
ON storage.objects FOR SELECT
USING (bucket_id = 'avatars');

-- Users can upload to their own folder
CREATE POLICY "Users can upload their own avatar"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'avatars'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

-- Users can update their own avatar
CREATE POLICY "Users can update their own avatar"
ON storage.objects FOR UPDATE
WITH CHECK (
  bucket_id = 'avatars'
  AND auth.uid()::text = (storage.foldername(name))[1]
);

-- Users can delete their own avatar
CREATE POLICY "Users can delete their own avatar"
ON storage.objects FOR DELETE
USING (
  bucket_id = 'avatars'
  AND auth.uid()::text = (storage.foldername(name))[1]
);
```

## File Operations

```typescript
// Upload file
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`user123/avatar.png`, file, {
    cacheControl: '3600',
    upsert: false
  })

// Upload with progress tracking
const { data, error } = await supabase.storage
  .from('videos')
  .upload(`user123/video.mp4`, file, {
    cacheControl: '3600',
    upsert: false,
    duplex: 'half'
  },
  // Progress callback
  (progress) => {
    console.log('Upload progress:', progress)
  }
)

// Get public URL
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('user123/avatar.png')

// Get signed URL (for private files)
const { data } = await supabase.storage
  .from('documents')
  .createSignedUrl('user123/document.pdf', 60)  // expires in 60 seconds

// Download file
const { data, error } = await supabase.storage
  .from('avatars')
  .download('user123/avatar.png')

// List files in folder
const { data, error } = await supabase.storage
  .from('avatars')
  .list('user123', {
    limit: 100,
    offset: 0,
    sortBy: { column: 'created_at', order: 'asc' }
  })

// Replace file
const { data, error } = await supabase.storage
  .from('avatars')
  .update('user123/avatar.png', file)

// Move file
const { data, error } = await supabase.storage
  .from('avatars')
  .move('user123/old.png', 'user123/new.png')

// Copy file
const { data, error } = await supabase.storage
  .from('avatars')
  .copy('user123/avatar.png', 'user123/avatar-copy.png')

// Delete file
const { error } = await supabase.storage
  .from('avatars')
  .remove(['user123/avatar.png', 'user123/avatar2.png'])

// Create signed upload URL (for client-side direct upload)
const { data, error } = await supabase.storage
  .from('documents')
  .createSignedUploadUrl('user123/new-doc.pdf')
```

## Image Transformations

```typescript
// Supabase Storage supports image transformations
// Format: /storage/v1/object/public/bucket/path?parameters

// Resize
const url = supabase.storage
  .from('avatars')
  .getPublicUrl('user123/avatar.png', {
    transform: {
      width: 200,
      height: 200
    }
  })

// Quality
const url = supabase.storage
  .from('avatars')
  .getPublicUrl('user123/avatar.png', {
    transform: {
      quality: 80
    }
  })

// Resize and fill
const url = supabase.storage
  .from('avatars')
  .getPublicUrl('user123/avatar.png', {
    transform: {
      width: 200,
      height: 200,
      resize: 'fill'
    }
  })

// Crop
const url = supabase.storage
  .from('avatars')
  .getPublicUrl('user123/avatar.png', {
    transform: {
      width: 200,
      height: 200,
      resize: 'crop',
      x: 10,
      y: 10
    }
  })

// Format conversion
const url = supabase.storage
  .from('avatars')
  .getPublicUrl('user123/avatar.png', {
    transform: {
      format: 'webp',
      quality: 80
    }
  })
```

---

# Edge Functions

## Deno Runtime Functions

```typescript
// Serve HTTP requests
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  // Handle CORS
  if (req.method === 'OPTIONS') {
    return new Response('ok', {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers':
          'authorization, x-client-info, apikey, content-type'
      }
    })
  }

  try {
    // Create Supabase client
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? ''
    )

    // Parse request
    const { method } = req
    const url = new URL(req.url)
    const path = url.pathname

    // Route handling
    if (method === 'POST' && path === '/users') {
      const body = await req.json()
      const { data, error } = await supabase
        .from('users')
        .insert(body)
        .select()
        .single()

      if (error) throw error

      return new Response(
        JSON.stringify(data),
        {
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        }
      )
    }

    return new Response('Not Found', { status: 404 })
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        status: 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      }
    )
  }
})
```

## Advanced Edge Function Patterns

```typescript
// Webhook handler with signature verification
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { crypto } from 'https://deno.land/std@0.168.0/crypto/mod.ts'

serve(async (req) => {
  // Verify webhook signature
  const signature = req.headers.get('x-webhook-signature')
  const body = await req.text()

  const expectedSignature = await crypto.subtle.sign(
    'HMAC',
    await crypto.subtle.importKey(
      'raw',
      new TextEncoder().encode(Deno.env.get('WEBHOOK_SECRET')),
      { name: 'HMAC', hash: 'SHA-256' },
      false,
      ['sign']
    ),
    new TextEncoder().encode(body)
  )

  const receivedSignature = btoa(
    String.fromCharCode(...new Uint8Array(expectedSignature))
  )

  if (signature !== receivedSignature) {
    return new Response('Invalid signature', { status: 401 })
  }

  // Process webhook
  const payload = JSON.parse(body)
  // ... handle webhook

  return new Response(JSON.stringify({ received: true }), {
    headers: { 'Content-Type': 'application/json' }
  })
})

// Scheduled task (cron)
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  // Verify cron authorization
  const authHeader = req.headers.get('Authorization')
  if (authHeader !== `Bearer ${Deno.env.get('CRON_SECRET')}`) {
    return new Response('Unauthorized', { status: 401 })
  }

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
  )

  // Perform scheduled task
  const { data } = await supabase
    .from('users')
    .select('id')
    .lt('last_login', new Date(Date.now() - 30 * 24 * 60 * 60 * 1000))

  // Send reminder emails...

  return new Response('OK')
})

// Rate limiting using Deno KV
// (Note: Requires Deno Deploy)
const kv = await Deno.openKv()

async function rateLimit(key: string, limit: number, window: number) {
  const identifier = `ratelimit:${key}`
  const now = Date.now()

  const entry = await kv.get<number[]>(identifier)
  const timestamps = entry.value || []

  // Remove old timestamps
  const validTimestamps = timestamps.filter(t => t > now - window)

  if (validTimestamps.length >= limit) {
    return { allowed: false }
  }

  // Add current timestamp
  validTimestamps.push(now)
  await kv.set(identifier, validTimestamps, { expireIn: window / 1000 })

  return { allowed: true }
}
```

---

# Vector & AI Features

## Vector Database

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with vector column
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  embedding vector(1536),  -- OpenAI embeddings dimension
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create HNSW index for fast similarity search
CREATE INDEX documents_embedding_idx
  ON documents
  USING hnsw (embedding vector_cosine_ops);

-- Insert with embedding
INSERT INTO documents (content, embedding)
VALUES ('Hello world', '[0.1, 0.2, ...]');

-- Cosine similarity search
SELECT
  id,
  content,
  1 - (embedding <=> '[0.1, 0.2, ...]') as similarity
FROM documents
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 5;
```

## Client-Side Vector Search

```typescript
// Generate embeddings using Edge Function
const generateEmbeddings = async (text: string) => {
  const { data, error } = await supabase.functions.invoke('generate-embeddings', {
    body: { text }
  })
  return data.embedding
}

// Search similar documents
const searchSimilar = async (query: string) => {
  const embedding = await generateEmbeddings(query)

  const { data, error } = await supabase.rpc('match_documents', {
    query_embedding: embedding,
    match_threshold: 0.8,
    match_count: 10
  })

  return data
}
```

---

# Migration Management

## Migration Best Practices

```sql
-- migrations/20240126000000_initial_schema.sql

-- Always use transactions
BEGIN;

-- Create types
CREATE TYPE user_status AS ENUM ('active', 'inactive', 'suspended');

-- Create tables
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  status user_status DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status) WHERE status = 'active';

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own data"
  ON users FOR SELECT
  USING (auth.uid() = id);

-- Create triggers
CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

COMMIT;

-- migrations/20240127000000_add_profiles.sql
BEGIN;

CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT,
  avatar_url TEXT
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public profiles are viewable"
  ON profiles FOR SELECT
  USING (true);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);

COMMIT;
```

---

# World-Class Resources

## Official Resources
- Supabase Docs: https://supabase.com/docs
- PostgreSQL 15 Docs: https://www.postgresql.org/docs/15/
- Supabase CLI: https://supabase.com/docs/guides/cli
- Supabase GitHub: https://github.com/supabase/supabase

## Learning Resources
- Supabase Launch Week: https://supabase.com/blog/launch-week
- Supabase YouTube: https://www.youtube.com/c/supabase
- PostgreSQL Tutorial: https://www.postgresqltutorial.com/

## Client Libraries
- JS Client: https://github.com/supabase/supabase-js
- Python Client: https://github.com/supabase/supabase-py
- Dart SDK: https://github.com/supabase/supabase-flutter
- Swift SDK: https://github.com/supabase/supabase-swift
- Go Client: https://github.com/supabase/supabase-go

## Community
- Supabase Discord: https://discord.gg/supabase
- Supabase Reddit: r/supabase
- Stack Overflow: Tag questions with 'supabase'
