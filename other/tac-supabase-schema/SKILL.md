---
name: tac-supabase-schema
description: >-
  Load when writing or modifying Supabase migrations, RLS policies, RPC functions, triggers, or generated types in tac-express. Covers schema conventions, RLS-by-role enforcement, SECURITY DEFINER usage, trigger patterns, and type regeneration.
---

# Supabase Schema & Migrations

## Migration Files

```
supabase/migrations/YYYYMMDDHHMM__descriptive_name.sql
```

- Never DROP without `IF EXISTS`
- Never DELETE data in a migration — soft-delete via `deleted_at` column
- Always add `created_at TIMESTAMPTZ DEFAULT NOW()` and `updated_at TIMESTAMPTZ DEFAULT NOW()` to new tables
- Include the reverse migration as a comment at the bottom of the file

```sql
-- supabase/migrations/202504101200__add_tracking_events.sql

CREATE TABLE IF NOT EXISTS tracking_events (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  awb_number  TEXT NOT NULL,
  status      TEXT NOT NULL,
  description TEXT,
  location    TEXT,
  hub_code    TEXT,
  source      TEXT NOT NULL DEFAULT 'STAFF',
  staff_id    UUID REFERENCES auth.users(id),
  staff_name  TEXT,
  metadata    JSONB,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Reverse: DROP TABLE IF EXISTS tracking_events;
```

---

## RLS: Every Table Must Have It

Enable RLS immediately and add at least one policy before committing:

```sql
ALTER TABLE tracking_events ENABLE ROW LEVEL SECURITY;

-- Read: authenticated users only
CREATE POLICY "authenticated_read_tracking_events"
ON tracking_events FOR SELECT
TO authenticated
USING (true);

-- Insert: staff and above
CREATE POLICY "staff_insert_tracking_events"
ON tracking_events FOR INSERT
TO authenticated
WITH CHECK (get_user_role() IN ('ADMIN', 'MANAGER', 'STAFF'));
```

---

## RBAC with get_user_role()

The project uses a custom `get_user_role()` RPC that reads the user's role from the `profiles` table:

```sql
-- Use in RLS policies (never inline the role lookup):
USING (get_user_role() IN ('ADMIN', 'MANAGER'))
WITH CHECK (get_user_role() = 'ADMIN')

-- Never do this (direct join in policy — slow, fragile):
-- USING (EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'ADMIN'))
```

---

## SECURITY DEFINER Functions

Use when you need to bypass RLS for a controlled operation:

```sql
CREATE OR REPLACE FUNCTION insert_tracking_event(
  p_awb_number TEXT,
  p_status     TEXT,
  p_location   TEXT DEFAULT NULL
)
RETURNS tracking_events
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_event tracking_events;
BEGIN
  -- Always validate auth.uid() first in SECURITY DEFINER functions
  IF auth.uid() IS NULL THEN
    RAISE EXCEPTION 'Not authenticated';
  END IF;

  INSERT INTO tracking_events (awb_number, status, location, staff_id)
  VALUES (p_awb_number, p_status, p_location, auth.uid())
  RETURNING * INTO v_event;

  RETURN v_event;
END;
$$;
```

---

## ADR-004: Status Trigger Pattern

Shipment status is event-derived. Maintain it via a trigger:

```sql
CREATE OR REPLACE FUNCTION update_shipment_status_from_events()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  UPDATE shipments
  SET
    status     = NEW.status,
    updated_at = NOW()
  WHERE awb_number = NEW.awb_number;

  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_update_shipment_status
AFTER INSERT ON tracking_events
FOR EACH ROW
EXECUTE FUNCTION update_shipment_status_from_events();
```

---

## updated_at Auto-Update Trigger

Add to every table that has `updated_at`:

```sql
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_set_updated_at
BEFORE UPDATE ON shipments
FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

---

## Indexes

Add indexes for every foreign key and common query filter:

```sql
-- Foreign keys
CREATE INDEX IF NOT EXISTS idx_tracking_events_awb ON tracking_events(awb_number);
CREATE INDEX IF NOT EXISTS idx_tracking_events_staff ON tracking_events(staff_id);

-- Common filters
CREATE INDEX IF NOT EXISTS idx_shipments_status ON shipments(status);
CREATE INDEX IF NOT EXISTS idx_shipments_origin_hub ON shipments(origin_hub);
CREATE INDEX IF NOT EXISTS idx_shipments_created_at ON shipments(created_at DESC);
```

---

## Type Regeneration

After any schema change, regenerate TypeScript types:

```bash
# Against local Supabase (preferred)
pnpm dlx supabase gen types typescript --local > packages/database/src/database.types.ts

# Against remote (if local isn't running)
pnpm dlx supabase gen types typescript --project-id <project-ref> > packages/database/src/database.types.ts

# Then verify no TypeScript errors were introduced:
pnpm typecheck
```

---

## Pre-Migration Checklist

```
[ ] Migration file named YYYYMMDDHHMM__descriptive_name.sql
[ ] No DROP without IF EXISTS
[ ] RLS enabled on every new table
[ ] At least one RLS policy per table operation (SELECT/INSERT/UPDATE/DELETE)
[ ] get_user_role() used in RBAC policies (not inline profile join)
[ ] SECURITY DEFINER functions validate auth.uid() first
[ ] updated_at trigger added to tables with that column
[ ] Indexes added for FKs and common query filters
[ ] Types regenerated and pnpm typecheck passes
[ ] Reverse migration documented in a comment
```
