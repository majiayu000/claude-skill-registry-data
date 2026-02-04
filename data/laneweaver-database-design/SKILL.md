---
name: laneweaver-database-design
description: Design PostgreSQL 17 schemas for laneweaverTMS using Supabase conventions - UUIDs, ENUMs, audit trails, soft deletes, triggers, functions, views, and atomic migration patterns.
---

# Database Design - PostgreSQL 17 + Supabase for laneweaverTMS

## When to Use This Skill

Use when:
- Designing new database tables and schemas
- Creating database migrations
- Planning table relationships and foreign keys
- Defining indexes for query optimization
- Creating database constraints and validation rules
- Implementing audit trails and soft deletes
- Writing database functions and triggers
- Designing views for calculated data
- Setting up row-level security (RLS) policies
- Implementing polymorphic relationships

## Primary Keys & IDs

### UUID Pattern (Standard for All Tables)

```sql
-- ✅ Correct: UUID primary key
CREATE TABLE public.loads (
    id UUID DEFAULT gen_random_uuid() NOT NULL,
    load_number TEXT NOT NULL,
    -- ...
    CONSTRAINT loads_pkey PRIMARY KEY (id)
);
```

**Why UUIDs?**
- Global uniqueness across distributed systems
- No sequential guessing of IDs (security)
- Enables data federation and merging
- Works with Supabase realtime subscriptions

### Exception: users Table

```sql
-- ✅ Exception: users table uses INT4
CREATE TABLE public.users (
    id INT4 GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    -- ...
);
```

**Impact**: All audit columns (`created_by`, `updated_by`, `deleted_by`) use `INT4` to reference `users.id`.

## Required Audit Columns

**Every table MUST include these audit columns**:

```sql
CREATE TABLE public.loads (
    id UUID DEFAULT gen_random_uuid() NOT NULL,

    -- Business fields...

    -- Standard audit columns (REQUIRED ON ALL TABLES)
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    created_by INT4,  -- References users.id
    updated_by INT4,  -- References users.id
    deleted_at TIMESTAMPTZ,  -- Soft delete: NULL = active
    deleted_by INT4,  -- User who deleted the record

    CONSTRAINT loads_pkey PRIMARY KEY (id)
);
```

### Soft Delete Pattern

- **Pattern**: `deleted_at TIMESTAMPTZ` (NULL = active, non-NULL = deleted)
- **NEVER hard delete** - always use `UPDATE SET deleted_at = now()`
- **Query active records**: `WHERE deleted_at IS NULL`

```sql
-- ✅ Correct: Soft delete
UPDATE loads SET deleted_at = now(), deleted_by = $1 WHERE id = $2;

-- ❌ Wrong: Hard delete
DELETE FROM loads WHERE id = $1;

-- ✅ Correct: Query active records only
SELECT * FROM loads WHERE deleted_at IS NULL;
```

## Data Types (Required)

laneweaverTMS follows PostgreSQL best practices with these domain-specific conventions:

| Data | Type | laneweaverTMS Convention |
|------|------|--------------------------|
| **IDs** | `UUID` | All tables except users (uses INT4) |
| **User References** | `INT4` | audit columns (created_by, updated_by, deleted_by) |
| **Timestamps** | `TIMESTAMPTZ` | All temporal data |
| **Money** | `NUMERIC(10,2)` | customer_rate, carrier_rate |
| **Strings** | `TEXT` | load_number, notes, etc. |

These conventions align with PostgreSQL best practices for production databases.

### NEVER Use These Types

```sql
-- ❌ NEVER use these types:
TIMESTAMP         -- Missing timezone → Use TIMESTAMPTZ
VARCHAR(n)        -- Arbitrary limits → Use TEXT
CHAR(n)           -- Fixed length → Use TEXT
MONEY             -- Currency type → Use NUMERIC(10,2)
SERIAL            -- Auto-increment → Use UUID or GENERATED ALWAYS AS IDENTITY
BIGSERIAL         -- Auto-increment → Use UUID or GENERATED ALWAYS AS IDENTITY
JSON              -- Slower than JSONB → Use JSONB
REAL              -- Imprecise for money → Use NUMERIC
FLOAT             -- Imprecise for money → Use NUMERIC
```

## ENUM Types

### When to Use ENUMs

Use PostgreSQL ENUMs for:
- Small, stable value sets (status workflows, categories)
- Type safety at the database level
- Performance (ENUMs stored as integers internally)

**laneweaverTMS has 32+ ENUMs defined**:
- `load_status`, `tender_status`, `invoice_status`, `carrier_bill_status`
- `call_outcome`, `task_status_enum`, `task_priority_enum`
- `mode_of_transport_list`, `stop_type_list`, `trailer_requirements_list`
- `accessorial_category_type`, `email_status`, `feed_item_type`

### Creating ENUMs

```sql
-- Migration: Create load_status ENUM

CREATE TYPE public.load_status AS ENUM (
    'uncovered',
    'assigned',
    'dispatched',
    'at_origin',
    'in_transit',
    'at_destination',
    'delivered'
);

COMMENT ON TYPE public.load_status IS
    'Load lifecycle: uncovered → assigned → dispatched → at_origin → in_transit → at_destination → delivered';
```

**Pattern**:
- Values use `snake_case` (e.g., `'in_transit'`, `'left_voicemail'`)
- Create ENUM in separate migration file BEFORE table creation
- Always include COMMENT explaining lifecycle or valid values

### Using ENUMs in Tables

```sql
CREATE TABLE public.loads (
    id UUID DEFAULT gen_random_uuid() NOT NULL,
    load_status public.load_status DEFAULT 'uncovered'::public.load_status NOT NULL,
    -- ...
);
```

### Modifying ENUMs

```sql
-- ✅ Safe: Adding values (no table rewrite)
ALTER TYPE load_status ADD VALUE 'cancelled';

-- ❌ Risky: Removing values (requires recreation)
-- Must create new type, migrate data, drop old type, rename new type
```

## Constraints

### CHECK Constraints

Use for business rules and validation:

```sql
-- ✅ Positive amounts
ALTER TABLE loads ADD CONSTRAINT chk_loads_customer_rate_positive
    CHECK (customer_rate > 0);

-- ✅ Valid ranges
ALTER TABLE load_cognition ADD CONSTRAINT chk_load_cognition_latitude_range
    CHECK (latitude >= -90 AND latitude <= 90);

-- ✅ Logical consistency
ALTER TABLE stops ADD CONSTRAINT chk_stops_appointment_logic
    CHECK (
        (appointment_required = false AND appointment_time IS NULL)
        OR (appointment_required = true AND appointment_time IS NOT NULL)
    );

-- ✅ JSONB structure validation
ALTER TABLE customer_invoices ADD CONSTRAINT chk_invoices_line_items_object
    CHECK (jsonb_typeof(line_items) = 'object');

-- ✅ ENUM validation for polymorphic types
ALTER TABLE documents ADD CONSTRAINT chk_documents_documentable_type
    CHECK (documentable_type = ANY (ARRAY['load'::text, 'account'::text, 'carrier'::text, 'facility'::text, 'rfp'::text]));
```

### UNIQUE Constraints

```sql
-- ✅ Natural keys
ALTER TABLE loads ADD CONSTRAINT loads_load_number_key
    UNIQUE (load_number);

-- ✅ Business uniqueness
ALTER TABLE carriers ADD CONSTRAINT carriers_mc_number_key
    UNIQUE (mc_number);

-- ✅ Composite uniqueness
ALTER TABLE load_references ADD CONSTRAINT load_references_load_reference_unique
    UNIQUE (load_id, reference_type_id);

-- ✅ One NULL allowed (PostgreSQL 15+)
ALTER TABLE carriers ADD CONSTRAINT uq_carriers_dot_number
    UNIQUE NULLS NOT DISTINCT (dot_number);
```

### Foreign Key Constraints

```sql
-- ✅ CASCADE: Delete children when parent deleted
ALTER TABLE stops
    ADD CONSTRAINT stops_load_id_fkey
    FOREIGN KEY (load_id) REFERENCES loads(id) ON DELETE CASCADE;

-- ✅ SET NULL: Preserve record, nullify FK
ALTER TABLE loads
    ADD CONSTRAINT loads_tender_id_fkey
    FOREIGN KEY (tender_id) REFERENCES tenders(id) ON DELETE SET NULL;

-- ✅ RESTRICT: Prevent deletion if children exist
ALTER TABLE loads
    ADD CONSTRAINT loads_account_id_fkey
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE RESTRICT;

-- ✅ Audit columns: Always SET NULL
ALTER TABLE loads
    ADD CONSTRAINT loads_created_by_fkey
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL;
```

## Indexing Strategy

### Critical Rule: Manual FK Indexes

**PostgreSQL does NOT auto-index foreign keys. You MUST create indexes manually.**

```sql
-- ✅ Required: Index all foreign keys
CREATE INDEX idx_loads_tender_id ON public.loads(tender_id);
CREATE INDEX idx_loads_carrier_id ON public.loads(carrier_id);
CREATE INDEX idx_stops_load_id ON public.stops(load_id);
CREATE INDEX idx_stops_facility_id ON public.stops(facility_id);
```

### Partial Indexes

```sql
-- ✅ Soft deletes: Index active records only
CREATE INDEX idx_loads_deleted_at ON public.loads(deleted_at)
    WHERE deleted_at IS NULL;

-- ✅ Nullable FKs: Index non-null values only
CREATE INDEX idx_loads_tender_id ON public.loads(tender_id)
    WHERE tender_id IS NOT NULL;

-- ✅ Conditional indexes for specific queries
CREATE INDEX idx_carrier_bills_quick_pay ON public.carrier_bills(quick_pay_requested)
    WHERE quick_pay_requested = true;
```

### Status and Timestamp Indexes

```sql
-- ✅ Status columns (for filtering)
CREATE INDEX idx_loads_load_status ON public.loads(load_status);
CREATE INDEX idx_carrier_bills_bill_status ON public.carrier_bills(bill_status);

-- ✅ Timestamp columns (for sorting, filtering, range queries)
CREATE INDEX idx_loads_created_at ON public.loads(created_at);
CREATE INDEX idx_calls_called_at ON public.calls(called_at);
CREATE INDEX idx_carrier_bills_scheduled_payment_date ON public.carrier_bills(scheduled_payment_date);
```

### Audit Column Indexes

```sql
-- ✅ Partial indexes for audit columns
CREATE INDEX idx_loads_created_by ON public.loads(created_by)
    WHERE created_by IS NOT NULL;
CREATE INDEX idx_loads_updated_by ON public.loads(updated_by)
    WHERE updated_by IS NOT NULL;
```

### GIN Indexes (JSONB, Arrays)

```sql
-- ✅ JSONB containment queries
CREATE INDEX idx_facilities_operating_hours ON public.facilities
    USING GIN (operating_hours);

-- ✅ Array containment
CREATE INDEX idx_loads_equipment_types ON public.loads
    USING GIN (equipment_types);

-- ✅ Full-text search
CREATE INDEX idx_accounts_search ON public.accounts
    USING GIN (to_tsvector('english', name || ' ' || COALESCE(domain_name, '')));
```

### Index Naming Convention

**Pattern**: `idx_[table]_[column(s)]`

```sql
CREATE INDEX idx_loads_account_id ON loads(account_id);
CREATE INDEX idx_loads_load_status ON loads(load_status);
CREATE INDEX idx_carrier_bounces_carrier_id ON carrier_bounces(carrier_id);
```

## Database Functions

### Security Pattern (REQUIRED)

**All functions MUST follow Supabase security best practices:**

**laneweaverTMS Convention:**

All functions follow Supabase security best practices with:
- `SECURITY INVOKER` - ensures function runs with caller's privileges
- `SET search_path = 'public'` - prevents schema search path attacks
```sql
CREATE OR REPLACE FUNCTION public.function_name()
RETURNS type
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = 'public'
AS $$
-- Function body
$$;
```

### Trigger Functions

```sql
-- ✅ Updated_at trigger function (reusable)
CREATE OR REPLACE FUNCTION public.update_timestamp()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = 'public'
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

-- ✅ Sync trigger for denormalization
CREATE OR REPLACE FUNCTION public.sync_load_cancelled_status()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = 'public'
AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE loads SET is_cancelled = true WHERE id = NEW.load_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE loads SET is_cancelled = false WHERE id = OLD.load_id;
    END IF;
    RETURN NULL;
END;
$$;

COMMENT ON FUNCTION public.sync_load_cancelled_status() IS
    'Syncs loads.is_cancelled when load_cancellations records are inserted/deleted';

-- ✅ Validation trigger
CREATE OR REPLACE FUNCTION public.validate_commodity_temperature()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = 'public'
AS $$
BEGIN
    IF NEW.temperature_min IS NOT NULL AND NEW.temperature_max IS NOT NULL THEN
        IF NEW.temperature_min > NEW.temperature_max THEN
            RAISE EXCEPTION 'temperature_min cannot be greater than temperature_max';
        END IF;
    END IF;

    IF NEW.temperature_unit IS NOT NULL AND NEW.temperature_unit NOT IN ('F', 'C') THEN
        RAISE EXCEPTION 'temperature_unit must be F or C';
    END IF;

    RETURN NEW;
END;
$$;
```

### Business Logic Functions

```sql
CREATE OR REPLACE FUNCTION public.create_load_from_tender(
    p_tender_id UUID,
    p_user_id UUID,
    p_carrier_id UUID
)
RETURNS UUID
LANGUAGE plpgsql
SECURITY INVOKER
SET search_path = 'public'
AS $$
DECLARE
    v_load_id UUID;
    v_load_number TEXT;
BEGIN
    -- Generate load number
    v_load_number := public.generate_load_number();

    -- Create load from tender
    INSERT INTO loads (
        id, load_number, tender_id, carrier_id,
        load_status, created_by, updated_by
    )
    VALUES (
        gen_random_uuid(), v_load_number, p_tender_id, p_carrier_id,
        'assigned'::load_status, p_user_id, p_user_id
    )
    RETURNING id INTO v_load_id;

    -- Update tender status
    UPDATE tenders
    SET tender_status = 'planned'::tender_status,
        planned_at = now(),
        updated_by = p_user_id
    WHERE id = p_tender_id;

    RETURN v_load_id;
END;
$$;

COMMENT ON FUNCTION public.create_load_from_tender(UUID, UUID, UUID) IS
    'Creates load from tender, generates L-XXXXXX number, updates tender status to planned';
```

## Triggers

### Standard Patterns

Every table should have:

#### 1. Updated_at Trigger

```sql
CREATE TRIGGER trg_loads_updated_at
    BEFORE UPDATE ON public.loads
    FOR EACH ROW
    EXECUTE FUNCTION public.update_timestamp();
```

#### 2. Audit Log Trigger

```sql
CREATE TRIGGER audit_loads_trigger
    AFTER INSERT OR UPDATE OR DELETE ON public.loads
    FOR EACH ROW
    EXECUTE FUNCTION public.audit_trigger_function();
```

### Sync Triggers (Denormalization)

```sql
-- Sync load billing flags to loads table
CREATE TRIGGER trg_sync_load_billing_flags
    AFTER INSERT OR UPDATE OF pod_received, carrier_bill_received ON public.load_billing
    FOR EACH ROW
    EXECUTE FUNCTION public.sync_load_billing_flags();

-- Sync cancelled status from load_cancellations
CREATE TRIGGER trg_sync_load_cancelled_status
    AFTER INSERT OR DELETE ON public.load_cancellations
    FOR EACH ROW
    EXECUTE FUNCTION public.sync_load_cancelled_status();
```

### Validation Triggers

```sql
-- Validate commodity temperature range
CREATE TRIGGER validate_commodity_temperature
    BEFORE INSERT OR UPDATE ON public.commodities
    FOR EACH ROW
    EXECUTE FUNCTION public.validate_commodity_temperature();

-- Enforce driver title requirement
CREATE TRIGGER enforce_driver_title_trigger
    BEFORE INSERT OR UPDATE ON public.load_cognition
    FOR EACH ROW
    EXECUTE FUNCTION public.validate_driver_title();
```

### Auto-Generated Values

```sql
-- Auto-generate tender number
CREATE TRIGGER trg_set_tender_number
    BEFORE INSERT ON public.tenders
    FOR EACH ROW
    EXECUTE FUNCTION public.set_tender_number();

-- Auto-create load versions
CREATE TRIGGER trg_load_versioning
    AFTER INSERT OR UPDATE ON public.loads
    FOR EACH ROW
    EXECUTE FUNCTION public.create_load_version();
```

## Views

### RLS-Aware Views (Required Pattern)

**All views MUST use `WITH (security_invoker='on')`** for Row-Level Security compatibility:

```sql
CREATE OR REPLACE VIEW public.loads_with_financials
WITH (security_invoker = on)
AS
SELECT
    l.id,
    l.load_number,
    l.load_status,
    l.customer_rate,
    l.carrier_rate,

    -- Calculated financial metrics
    (l.customer_rate - COALESCE(l.carrier_rate, 0)) AS gross_profit,
    CASE
        WHEN l.customer_rate > 0
        THEN ((l.customer_rate - COALESCE(l.carrier_rate, 0)) / l.customer_rate * 100)
        ELSE 0
    END AS profit_margin_percent,

    -- Aggregate accessorials
    (SELECT COALESCE(SUM(amount), 0)
     FROM customer_accessorials
     WHERE load_id = l.id AND deleted_at IS NULL) AS customer_accessorials_total,

    (SELECT COALESCE(SUM(amount), 0)
     FROM carrier_accessorials
     WHERE load_id = l.id AND deleted_at IS NULL) AS carrier_accessorials_total,

    -- Net profit
    ((l.customer_rate + (SELECT COALESCE(SUM(amount), 0) FROM customer_accessorials WHERE load_id = l.id AND deleted_at IS NULL)) -
     (COALESCE(l.carrier_rate, 0) + (SELECT COALESCE(SUM(amount), 0) FROM carrier_accessorials WHERE load_id = l.id AND deleted_at IS NULL))) AS net_profit

FROM public.loads l
WHERE l.deleted_at IS NULL;

COMMENT ON VIEW public.loads_with_financials IS
    'Loads with calculated financial metrics (gross profit, margin %, accessorials, net profit)';
```

### Lifecycle Views

```sql
CREATE OR REPLACE VIEW public.life_of_load_flow
WITH (security_invoker = on)
AS
SELECT
    -- Load
    l.id AS load_id,
    l.load_number,
    l.load_status,

    -- Tender
    t.id AS tender_id,
    t.tender_number,
    t.tender_status,

    -- Quote
    cq.id AS quote_id,
    cq.quote_number,

    -- Account
    a.id AS account_id,
    a.name AS account_name,

    -- Financial summary
    l.customer_rate,
    l.carrier_rate,
    (l.customer_rate - COALESCE(l.carrier_rate, 0)) AS gross_profit,

    -- Billing status
    lb.pod_received,
    lb.carrier_bill_received,
    lb.invoice_ready

FROM public.loads l
LEFT JOIN public.tenders t ON l.tender_id = t.id
LEFT JOIN public.customer_quotes cq ON t.quote_id = cq.id
LEFT JOIN public.accounts a ON t.account_id = a.id
LEFT JOIN public.load_billing lb ON l.id = lb.load_id

WHERE l.deleted_at IS NULL;

COMMENT ON VIEW public.life_of_load_flow IS
    'Complete load lifecycle: quote → tender → load → billing with financial metrics';
```

## Migration Patterns

### Atomic Migration Strategy

**One logical change per migration file**:

1. Create ENUM (separate file)
2. Create table (separate file)
3. Add indexes (separate file)
4. Add foreign keys (inline or separate file)
5. Add triggers (separate file)
6. Add functions (separate file)
7. Add views (separate file)
8. Add RLS policies (separate file)

### Migration File Naming

**Format**: `[YYYYMMDDHHMMSS]_[descriptive_name].sql`

Examples:
- `20251216171743_create_tender_status_enum.sql`
- `20251217055251_create_carrier_bounces_table.sql`
- `20251216172549_add_tenders_indexes_and_audit.sql`
- `20251217060132_add_carrier_bounces_updated_at_trigger.sql`

### Migration File Structure

```sql
-- Header comment describing purpose
-- Migration: Create carrier_bounces table for tracking carrier falloffs

-- Create table with inline constraints
CREATE TABLE public.carrier_bounces (
    -- Primary key
    id UUID DEFAULT gen_random_uuid() NOT NULL,

    -- Foreign keys
    carrier_id UUID NOT NULL,
    load_id UUID NOT NULL,

    -- Core fields
    reason TEXT,
    bounce_time TIMESTAMPTZ NOT NULL DEFAULT now(),
    carrier_rate NUMERIC(10,2),

    -- Standard audit columns (see "Required Audit Columns" section above)
    created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    created_by INT4,
    updated_by INT4,
    deleted_at TIMESTAMPTZ,
    deleted_by INT4,

    -- Constraints
    CONSTRAINT carrier_bounces_pkey PRIMARY KEY (id),
    CONSTRAINT fk_carrier_bounces_carrier_id
        FOREIGN KEY (carrier_id) REFERENCES carriers(id) ON DELETE RESTRICT,
    CONSTRAINT fk_carrier_bounces_load_id
        FOREIGN KEY (load_id) REFERENCES loads(id) ON DELETE RESTRICT
);

-- Table comment
COMMENT ON TABLE public.carrier_bounces IS
    'Tracks when carriers back out of committed loads. Used for reliability scoring and bounce history.';

-- Column comments
COMMENT ON COLUMN public.carrier_bounces.carrier_id IS 'Carrier that bounced on the load';
COMMENT ON COLUMN public.carrier_bounces.load_id IS 'Load the carrier bounced from';
COMMENT ON COLUMN public.carrier_bounces.reason IS 'Reason provided for the bounce (free text)';
COMMENT ON COLUMN public.carrier_bounces.bounce_time IS 'Timestamp when bounce occurred';
```

### Separate Migration: Indexes

```sql
-- Migration: Add indexes to carrier_bounces table

-- Foreign key indexes (REQUIRED - PostgreSQL doesn't auto-index FKs)
CREATE INDEX idx_carrier_bounces_carrier_id
    ON public.carrier_bounces(carrier_id);

CREATE INDEX idx_carrier_bounces_load_id
    ON public.carrier_bounces(load_id);

-- Soft delete partial index
CREATE INDEX idx_carrier_bounces_deleted_at
    ON public.carrier_bounces(deleted_at)
    WHERE deleted_at IS NULL;

-- Timestamp index for filtering
CREATE INDEX idx_carrier_bounces_bounce_time
    ON public.carrier_bounces(bounce_time);

-- Audit column indexes
CREATE INDEX idx_carrier_bounces_created_by
    ON public.carrier_bounces(created_by)
    WHERE created_by IS NOT NULL;
```

### Separate Migration: Triggers

```sql
-- Migration: Add triggers to carrier_bounces table

-- Updated_at trigger
CREATE TRIGGER trg_carrier_bounces_updated_at
    BEFORE UPDATE ON public.carrier_bounces
    FOR EACH ROW
    EXECUTE FUNCTION public.update_timestamp();

COMMENT ON TRIGGER trg_carrier_bounces_updated_at ON public.carrier_bounces IS
    'Automatically updates updated_at timestamp on row modification';

-- Audit trigger
CREATE TRIGGER audit_carrier_bounces_trigger
    AFTER INSERT OR UPDATE OR DELETE ON public.carrier_bounces
    FOR EACH ROW
    EXECUTE FUNCTION public.audit_trigger_function();

COMMENT ON TRIGGER audit_carrier_bounces_trigger ON public.carrier_bounces IS
    'Logs all changes to audit_log table for compliance tracking';
```

## Polymorphic Relationships

### Pattern: Type + ID Columns

Allows a single table to reference multiple entity types:

```sql
-- ✅ Polymorphic: calls can reference accounts, contacts, RFPs, loads
CREATE TABLE public.calls (
    id UUID DEFAULT gen_random_uuid() NOT NULL,

    -- Polymorphic relationship
    related_to_table TEXT NOT NULL,  -- 'account', 'contact', 'rfp', 'load'
    related_to_id UUID NOT NULL,

    -- Call fields
    call_outcome public.call_outcome,
    called_at TIMESTAMPTZ DEFAULT now() NOT NULL,
    notes TEXT,

    -- Audit columns...

    CONSTRAINT calls_pkey PRIMARY KEY (id),
    CONSTRAINT chk_calls_related_to_table
        CHECK (related_to_table = ANY (ARRAY['account'::text, 'contact'::text, 'rfp'::text, 'load'::text]))
);

-- Index for polymorphic lookup
CREATE INDEX idx_calls_related_to
    ON public.calls(related_to_table, related_to_id);

-- Query calls for specific account
SELECT * FROM calls
WHERE related_to_table = 'account'
  AND related_to_id = '123e4567-e89b-12d3-a456-426614174000';
```

### Examples in laneweaverTMS

- **calls**: `related_to_table` + `related_to_id` (accounts, contacts, RFPs, loads)
- **documents**: `documentable_type` + `documentable_id` (loads, accounts, carriers, facilities, rfps)

## Generated Columns

### Pattern: Calculated Values

```sql
-- ✅ Generated column for invoice readiness
ALTER TABLE public.load_billing
ADD COLUMN invoice_ready BOOLEAN
    GENERATED ALWAYS AS (pod_received AND carrier_bill_received) STORED;

COMMENT ON COLUMN public.load_billing.invoice_ready IS
    'Generated: true when both POD and carrier bill are received';

-- Query using generated column
SELECT * FROM load_billing WHERE invoice_ready = true;

-- Index on generated column
CREATE INDEX idx_load_billing_invoice_ready
    ON public.load_billing(invoice_ready)
    WHERE invoice_ready = true;
```

### When to Use Generated Columns

- Frequently queried JSONB fields
- Complex boolean logic (invoice_ready = pod_received AND carrier_bill_received)
- Calculated values used in WHERE clauses or indexes

## Row-Level Security (RLS)

### Enable RLS on Tables

```sql
-- Enable RLS
ALTER TABLE loads ENABLE ROW LEVEL SECURITY;

-- Development policy (permissive for authenticated users)
CREATE POLICY "Authenticated users can select loads"
    ON loads
    FOR SELECT
    TO authenticated
    USING (true);

-- Production policy (organization isolation)
CREATE POLICY "Users see only their organization's loads"
    ON loads
    FOR SELECT
    TO authenticated
    USING (
        account_id IN (
            SELECT account_id
            FROM user_accounts
            WHERE user_id = auth.uid()
        )
    );

-- Admin bypass
CREATE POLICY "Admins see all loads"
    ON loads
    FOR ALL
    TO admin_users
    USING (true)
    WITH CHECK (true);
```

## JSONB Usage

### When to Use JSONB

Use JSONB for:
- Semi-structured, optional attributes (not core relations)
- Flexible configuration data
- Event payloads or raw data snapshots
- Nested data structures

**Examples in laneweaverTMS**:
- `facilities.operating_hours` - Flexible schedule data
- `customer_invoices.line_items` - Invoice line item details
- `audit_log.old_data`, `audit_log.new_data` - Change tracking
- `tenders.edi_raw_data` - EDI 204 payload

### JSONB Best Practices

```sql
-- ✅ Default to empty object (avoid NULL checks)
ALTER TABLE facilities
ADD COLUMN operating_hours JSONB NOT NULL DEFAULT '{}'::jsonb;

-- ✅ CHECK constraint for structure
ALTER TABLE customer_invoices
ADD CONSTRAINT chk_invoices_line_items_object
    CHECK (jsonb_typeof(line_items) = 'object');

-- ✅ GIN index for containment queries
CREATE INDEX idx_facilities_operating_hours
    ON facilities USING GIN (operating_hours);

-- ✅ Extract frequently queried fields as generated columns
ALTER TABLE facilities
ADD COLUMN is_open_24_7 BOOLEAN
    GENERATED ALWAYS AS (
        (operating_hours->>'is_24_7')::boolean
    ) STORED;
```

## Database Design Checklist

```
Schema Design:
□ UUID primary keys on all tables (except users which uses INT4)
□ Required audit columns on ALL tables (created_at, updated_at, created_by, updated_by, deleted_at, deleted_by)
□ Soft delete pattern with deleted_at (no hard deletes)
□ Foreign keys with appropriate CASCADE/SET NULL/RESTRICT
□ CHECK constraints for business validation
□ UNIQUE constraints for natural keys
□ ENUMs for stable value sets (status workflows, categories)
□ TIMESTAMPTZ for all timestamps (NEVER TIMESTAMP)
□ TEXT for strings (NEVER VARCHAR or CHAR)
□ NUMERIC for money (NEVER REAL, FLOAT, or MONEY type)
□ JSONB for flexible data (NEVER JSON)

Indexes:
□ All foreign keys manually indexed (PostgreSQL doesn't auto-index)
□ Partial indexes for soft deletes (WHERE deleted_at IS NULL)
□ Partial indexes for nullable FKs (WHERE column IS NOT NULL)
□ Status columns indexed
□ Timestamp columns indexed
□ GIN indexes for JSONB containment queries
□ Composite indexes for multi-column queries

Functions & Triggers:
□ All functions use SECURITY INVOKER + SET search_path = 'public'
□ Updated_at trigger on all tables
□ Audit trigger on all tables (if audit_log enabled)
□ Sync triggers for denormalized columns
□ Validation triggers for business rules
□ COMMENT on all functions and triggers

Views:
□ All views use WITH (security_invoker = on)
□ Views filter deleted_at IS NULL for soft deletes
□ COMMENT on all views explaining purpose

Migrations:
□ Atomic migrations (one operation per file)
□ Naming: [YYYYMMDDHHMMSS]_[descriptive_name].sql
□ Header comment describing purpose
□ COMMENT on all tables, columns, functions, triggers, views
□ Separate files for ENUMs, tables, indexes, triggers, functions, views
□ Version controlled in supabase/migrations/

RLS:
□ RLS enabled on all tables
□ Policies defined for SELECT, INSERT, UPDATE, DELETE
□ Admin bypass policies for administrative users
```

## Key References

**Authoritative Examples** (within laneweaverTMS repository):
- Schema: `./erd.sql` (root of repository)
- Migrations: `supabase/migrations/`
- Conventions: `supabase/CLAUDE.md`

**External Resources**:
- [PostgreSQL 17 Documentation](https://www.postgresql.org/docs/17/)
- [Supabase Database Guide](https://supabase.com/docs/guides/database)

---

**Remember**: Consistency is critical. Every table follows the same patterns for audit columns, soft deletes, indexing, triggers, and comments. This makes the codebase predictable and maintainable.
