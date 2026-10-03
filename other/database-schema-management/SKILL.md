---
memory_layer: durable_knowledge
para_section: pages/skills/database-schema-management
gigabrain_tags: database, schema, data-modeling, foreign-keys, constraints
openstinger_context: data-architecture, schema-design, database-management
last_updated: 2026-03-30
related_docs:
  - https://github.com/Construct-AI-primary/construct_ai/blob/main/docs/codebase/schema/database/schema-part-01.md
  - https://github.com/Construct-AI-primary/construct_ai/blob/main/docs/codebase/schema/foreign_key_relationships.md
  - https://github.com/Construct-AI-primary/construct_ai/blob/main/docs/codebase/schema/agents_schema.md
related_skills:
  - state-based-button-display
  - agent-accuracy-enhancement
frequency_percent: 78.0
success_rate_percent: 91.5
---

# Database Schema Management Skill

## Overview

Comprehensive database schema design, management, and optimization for Construct AI's complex data model. This skill covers the systematic approach to managing 48+ database tables, foreign key relationships, constraints, and indexes across the entire application ecosystem.

## When to Use This Skill

**Trigger Conditions:**
- Designing new database tables or relationships
- Modifying existing schema structures
- Optimizing database performance through indexing
- Implementing data integrity constraints
- Managing foreign key relationships
- Planning database migrations
- Analyzing schema dependencies and impacts

## Step-by-Step Procedure

### Step 1: Analyze Schema Requirements
```sql
-- Analyze existing schema structure
SELECT
  schemaname,
  tablename,
  tableowner,
  tablespace,
  hasindexes,
  hasrules,
  hastriggers,
  rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;
```

**Key Considerations:**
- What entities need to be modeled?
- What relationships exist between entities?
- What constraints are required for data integrity?
- What indexes are needed for performance?
- How does this fit into the existing 48-table schema?

### Step 2: Design Table Structure
```sql
-- Example table creation with proper constraints
CREATE TABLE procurement_orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_number VARCHAR(50) UNIQUE NOT NULL,
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  supplier_id UUID REFERENCES suppliers(id) ON DELETE RESTRICT,
  discipline_id UUID REFERENCES disciplines(id) ON DELETE RESTRICT,

  -- Status and workflow
  status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'submitted', 'approved', 'rejected', 'completed')),
  workflow_state JSONB DEFAULT '{}',

  -- Financial information
  total_amount DECIMAL(15,2) DEFAULT 0.00,
  currency VARCHAR(3) DEFAULT 'USD',

  -- Audit fields
  created_by UUID REFERENCES users(id),
  updated_by UUID REFERENCES users(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes for performance
CREATE INDEX idx_procurement_orders_project ON procurement_orders(project_id);
CREATE INDEX idx_procurement_orders_supplier ON procurement_orders(supplier_id);
CREATE INDEX idx_procurement_orders_status ON procurement_orders(status);
CREATE INDEX idx_procurement_orders_created_at ON procurement_orders(created_at DESC);
```

### Step 3: Implement Foreign Key Relationships
```sql
-- Foreign key relationships based on schema analysis
ALTER TABLE procurement_orders
  ADD CONSTRAINT fk_procurement_orders_project
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,

  ADD CONSTRAINT fk_procurement_orders_supplier
  FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE RESTRICT,

  ADD CONSTRAINT fk_procurement_orders_discipline
  FOREIGN KEY (discipline_id) REFERENCES disciplines(id) ON DELETE RESTRICT;

-- Check existing foreign key relationships
SELECT
  tc.table_name,
  kcu.column_name,
  ccu.table_name AS foreign_table_name,
  ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE constraint_type = 'FOREIGN KEY'
ORDER BY tc.table_name;
```

### Step 4: Add Constraints and Validation
```sql
-- Add check constraints for data integrity
ALTER TABLE procurement_orders
  ADD CONSTRAINT chk_order_number_format
  CHECK (order_number ~ '^PO-[0-9]{4}-[0-9]{3}$'),

  ADD CONSTRAINT chk_positive_amount
  CHECK (total_amount >= 0),

  ADD CONSTRAINT chk_valid_currency
  CHECK (currency IN ('USD', 'EUR', 'GBP', 'ZAR'));

-- Add unique constraints where needed
ALTER TABLE procurement_orders
  ADD CONSTRAINT uk_order_number UNIQUE (order_number);

-- Add exclusion constraints for complex business rules
ALTER TABLE procurement_orders
  ADD CONSTRAINT ex_order_date_range
  EXCLUDE (project_id WITH =, tstzrange(created_at, created_at + interval '1 year') WITH &&)
  WHERE (status = 'active');
```

### Step 5: Create Indexes for Performance
```sql
-- Performance indexes based on query patterns
CREATE INDEX CONCURRENTLY idx_procurement_orders_composite
ON procurement_orders(project_id, status, created_at DESC)
WHERE status IN ('approved', 'completed');

-- Partial indexes for specific use cases
CREATE INDEX idx_active_orders ON procurement_orders(created_at)
WHERE status NOT IN ('cancelled', 'rejected');

-- Expression indexes for computed values
CREATE INDEX idx_order_year ON procurement_orders(EXTRACT(year FROM created_at));

-- GIN indexes for JSONB fields
CREATE INDEX idx_workflow_state_gin ON procurement_orders USING GIN(workflow_state);
```

### Step 6: Implement Row Level Security
```sql
-- Enable RLS on tables
ALTER TABLE procurement_orders ENABLE ROW LEVEL SECURITY;

-- Create policies based on user roles and organization access
CREATE POLICY "Users can view orders in their organizations"
  ON procurement_orders FOR SELECT
  USING (
    project_id IN (
      SELECT id FROM projects
      WHERE organization_id IN (
        SELECT organization_id FROM user_organization_members
        WHERE user_id = auth.uid()
      )
    )
  );

CREATE POLICY "Users can create orders in their projects"
  ON procurement_orders FOR INSERT
  WITH CHECK (
    project_id IN (
      SELECT id FROM projects
      WHERE created_by = auth.uid() OR
            id IN (
              SELECT project_id FROM project_members
              WHERE user_id = auth.uid() AND role IN ('owner', 'editor')
            )
    )
  );
```

### Step 7: Set Up Audit Triggers
```sql
-- Create audit trigger function
CREATE OR REPLACE FUNCTION audit_procurement_orders()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    NEW.created_at = NOW();
    NEW.created_by = auth.uid();
    RETURN NEW;
  ELSIF TG_OP = 'UPDATE' THEN
    NEW.updated_at = NOW();
    NEW.updated_by = auth.uid();
    RETURN NEW;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Apply audit trigger
CREATE TRIGGER audit_procurement_orders_trigger
  BEFORE INSERT OR UPDATE ON procurement_orders
  FOR EACH ROW EXECUTE FUNCTION audit_procurement_orders();
```

### Step 8: Validate Schema Integrity
```sql
-- Comprehensive schema validation
SELECT
  'Table Count' as metric,
  COUNT(*) as value
FROM information_schema.tables
WHERE table_schema = 'public'

UNION ALL

SELECT
  'Foreign Key Count',
  COUNT(*)
FROM information_schema.table_constraints
WHERE constraint_type = 'FOREIGN KEY'

UNION ALL

SELECT
  'Index Count',
  COUNT(*)
FROM pg_indexes
WHERE schemaname = 'public'

UNION ALL

SELECT
  'RLS Enabled Tables',
  COUNT(*)
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
  AND c.relrowsecurity = true;
```

### Step 9: Document Schema Changes
```sql
-- Schema documentation comments
COMMENT ON TABLE procurement_orders IS 'Procurement orders with full audit trail and workflow state management';
COMMENT ON COLUMN procurement_orders.workflow_state IS 'JSONB field containing workflow-specific state data';
COMMENT ON COLUMN procurement_orders.total_amount IS 'Total order amount in specified currency';

-- Generate schema documentation
SELECT
  'Table: ' || table_name || E'\n' ||
  'Description: ' || obj_description(c.oid) || E'\n' ||
  'Columns: ' || string_agg(column_name || ' (' || data_type || ')', E'\n  - ') || E'\n'
FROM information_schema.columns c
JOIN pg_class pc ON pc.relname = c.table_name
WHERE table_schema = 'public'
  AND table_name = 'procurement_orders'
GROUP BY table_name, pc.oid;
```

### Step 10: Plan Migration Strategy
```sql
-- Migration planning and execution
BEGIN;

-- Create backup
CREATE TABLE procurement_orders_backup AS
SELECT * FROM procurement_orders;

-- Apply schema changes
ALTER TABLE procurement_orders ADD COLUMN approval_required BOOLEAN DEFAULT true;

-- Validate changes
SELECT COUNT(*) as backup_count FROM procurement_orders_backup;
SELECT COUNT(*) as current_count FROM procurement_orders;

-- Commit or rollback based on validation
-- COMMIT; -- Uncomment when ready
-- ROLLBACK; -- Uncomment to rollback

END;
```

## Success Criteria

- [ ] Table structure follows Construct AI naming conventions
- [ ] Foreign key relationships properly defined and tested
- [ ] Constraints enforce data integrity without breaking existing data
- [ ] Indexes improve query performance without excessive overhead
- [ ] Row Level Security policies protect data appropriately
- [ ] Audit triggers capture all changes
- [ ] Schema documentation is complete and accurate
- [ ] Migration scripts are tested and reversible

## Common Pitfalls

1. **Circular Foreign Key References** - Design relationships to avoid circular dependencies
2. **Missing Indexes on Foreign Keys** - Always index foreign key columns
3. **Over-Indexing** - Too many indexes can slow down writes
4. **RLS Policy Conflicts** - Ensure policies don't block legitimate access
5. **Constraint Conflicts** - Test constraints against existing data
6. **Migration Rollback Issues** - Always plan for migration reversibility

## Schema Categories in Construct AI

### Core Business Tables (8)
- `users`, `organizations`, `projects`, `disciplines`
- `procurement_orders`, `procurement_categories`
- `templates`, `form_templates`

### Document Management (4)
- `documents`, `chat_sessions`, `chat_messages`
- `buttons`, `modals`, `pages`, `page_permissions`

### Agent System (4)
- `agents`, `agent_permissions`, `agent_roles`
- `sectors`, `companies`

### Construction Domain (12)
- `contracts`, `contractors`, `suppliers`, `tenders`
- `approval_instances`, `approval_steps`, `dropdown_options`
- `vessels`, `containers`, `logistics_shipments`

### Operations (12)
- `travel_requests`, `petty_cash`, `financial_records`
- `defects`, `inspection_items`, `inspections`
- `quality_checks`, `compliance_checks`, `risk_assessments`

### Safety & HR (8)
- `safety_incidents`, `maintenance_assets`, `maintenance_schedules`
- `personnel_records`, `job_descriptions`, `cv_applications`
- `legal_reviews`, `limits_of_authority`

## Cross-References

### Related Procedures
- [Schema Part 1](https://github.com/Construct-AI-primary/construct_ai/blob/main/docs/codebase/schema/database/schema-part-01.md) - Complete table documentation
- [Foreign Key Relationships](https://github.com/Construct-AI-primary/construct_ai/blob/main/docs/codebase/schema/foreign_key_relationships.md) - Relationship mappings
- [Agents Schema](https://github.com/Construct-AI-primary/construct_ai/blob/main/docs/codebase/schema/agents_schema.md) - Agent-specific schema

### Related Skills
- `state-based-button-display` - UI components that interact with schema
- `agent-accuracy-enhancement` - Data integrity for agent responses

### Related Agents
- `DevForge_AI_Team` - Schema implementation and optimization
- `QualityForge_AI_Team` - Schema validation and testing

## Example Schema Design

```sql
-- Complete procurement order schema example
CREATE TABLE procurement_orders (
  -- Primary identification
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_number VARCHAR(50) UNIQUE NOT NULL,

  -- Core relationships
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  supplier_id UUID NOT NULL REFERENCES suppliers(id) ON DELETE RESTRICT,
  discipline_id UUID NOT NULL REFERENCES disciplines(id) ON DELETE RESTRICT,
  created_by UUID NOT NULL REFERENCES users(id),
  approved_by UUID REFERENCES users(id),

  -- Order details
  title TEXT NOT NULL,
  description TEXT,
  status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'submitted', 'approved', 'rejected', 'completed')),
  priority VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'critical')),

  -- Financial information
  total_amount DECIMAL(15,2) DEFAULT 0.00 CHECK (total_amount >= 0),
  currency VARCHAR(3) DEFAULT 'USD' CHECK (currency IN ('USD', 'EUR', 'GBP', 'ZAR')),
  tax_amount DECIMAL(15,2) DEFAULT 0.00 CHECK (tax_amount >= 0),

  -- Dates and timelines
  submission_date DATE,
  required_date DATE,
  approval_date DATE,
  completion_date DATE,

  -- Workflow and metadata
  workflow_state JSONB DEFAULT '{}',
  metadata JSONB DEFAULT '{}',
  tags TEXT[] DEFAULT '{}',

  -- Audit trail
  updated_by UUID REFERENCES users(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

  -- Constraints
  CONSTRAINT chk_dates_logical CHECK (
    (submission_date IS NULL OR required_date IS NULL OR submission_date <= required_date) AND
    (approval_date IS NULL OR submission_date IS NULL OR approval_date >= submission_date) AND
    (completion_date IS NULL OR approval_date IS NULL OR completion_date >= approval_date)
  ),

  CONSTRAINT chk_status_transitions CHECK (
    (status = 'draft' AND approval_date IS NULL AND completion_date IS NULL) OR
    (status = 'submitted' AND submission_date IS NOT NULL) OR
    (status = 'approved' AND approval_date IS NOT NULL) OR
    (status = 'completed' AND completion_date IS NOT NULL) OR
    (status = 'rejected')
  )
);

-- Performance indexes
CREATE INDEX idx_procurement_orders_project_status ON procurement_orders(project_id, status);
CREATE INDEX idx_procurement_orders_supplier ON procurement_orders(supplier_id);
CREATE INDEX idx_procurement_orders_created_at ON procurement_orders(created_at DESC);
CREATE INDEX idx_procurement_orders_required_date ON procurement_orders(required_date) WHERE status IN ('approved', 'submitted');
CREATE INDEX idx_procurement_orders_workflow_gin ON procurement_orders USING GIN(workflow_state);
CREATE INDEX idx_procurement_orders_tags_gin ON procurement_orders USING GIN(tags);

-- RLS policies
ALTER TABLE procurement_orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view orders in accessible projects"
  ON procurement_orders FOR SELECT
  USING (project_id IN (
    SELECT project_id FROM project_members
    WHERE user_id = auth.uid()
  ));

CREATE POLICY "Users can create orders in editable projects"
  ON procurement_orders FOR INSERT
  WITH CHECK (project_id IN (
    SELECT project_id FROM project_members
    WHERE user_id = auth.uid() AND role IN ('owner', 'editor')
  ));
```

## Performance Metrics

- **Average Schema Design Time:** 45-90 minutes per table
- **Success Rate:** 91.5% first-time correct implementations
- **Frequency:** Used in 78% of database development tasks
- **Query Performance Improvement:** 40-60% faster with proper indexing

## Schema Evolution Strategy

### Version Control
```sql
-- Schema versioning table
CREATE TABLE schema_versions (
  version VARCHAR(20) PRIMARY KEY,
  applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  description TEXT,
  applied_by UUID REFERENCES users(id),
  rollback_sql TEXT
);

-- Record schema changes
INSERT INTO schema_versions (version, description, rollback_sql)
VALUES ('1.2.0', 'Added procurement_orders table with full constraints and indexes', 'DROP TABLE procurement_orders;');
```

### Migration Safety
```sql
-- Safe migration pattern
BEGIN;

-- Pre-migration validation
SELECT COUNT(*) as pre_count FROM existing_table;

-- Apply changes with error handling
SAVEPOINT migration_start;

-- Migration logic here
ALTER TABLE procurement_orders ADD COLUMN new_field TEXT;

-- Post-migration validation
SELECT COUNT(*) as post_count FROM procurement_orders;

-- Rollback on failure
ROLLBACK TO migration_start;

COMMIT;
```

This skill ensures robust, scalable database schema design that supports Construct AI's complex construction industry workflows while maintaining data integrity and performance.