---
name: bel-crm-schema-write-db
description: This skill should be used when working with the CRM PostgreSQL database for sales, contacts, companies, and opportunities. Use this skill when the user asks to insert, update, query, or analyze data in the CRM database (may be called crm or db), or when SQL queries need to be created for company_site, person, sales_opportunity, or event tables. This skill provides comprehensive schema knowledge and PostgreSQL-specific SQL examples tailored to the CRM data model.
---

# BEL CRM Schema Write DB

## CRITICAL: Read SQL Rules First!

**Before writing ANY SQL, consult the `bel-crm-sql-rules` skill!**

Key limitations of the PostgreSQL MCP server:
- **NO `RETURNING` clause** - will cause syntax error
- **NO `ON CONFLICT`** - will fail (also: no UNIQUE constraints on name columns!)
- Use `read_query` to get IDs after INSERT

## Overview

This skill provides comprehensive knowledge of the CRM PostgreSQL database schema and generates correct, PostgreSQL-specific SQL queries for managing companies, contacts, sales opportunities, and activity events.

The CRM database uses a relational model with JSONB fields for flexible tagging and metadata, temporal tracking with timestamps, and foreign key relationships between companies, people, opportunities, and events.

## When to Use This Skill

Use this skill when:
- Creating INSERT statements for new CRM records
- Writing UPDATE queries to modify existing data
- Constructing SELECT queries with JOINs across CRM entities
- Working with JSONB fields (tags, metadata)
- Querying relationships between companies, contacts, and opportunities
- Building reports from sales pipeline data
- Tracking activities and events
- The user mentions database operations on: company_site, person, sales_opportunity, or event tables
  The user may SHORTEN that by: company_site (c:), person (p:), sales_opportunity (so:), event (e:)

## Core Capabilities

### 1. Schema Knowledge

Load `references/schema.md` to understand:
- Complete table structures with all columns and data types
- Foreign key relationships between entities
- JSONB field usage for tags and metadata
- Timestamp fields for created_at/updated_at tracking
- Entity relationship diagram

Use schema knowledge to:
- Validate column names and data types before generating SQL
- Understand which tables to JOIN for specific queries
- Handle optional vs. required fields correctly
- Use appropriate PostgreSQL data types (JSONB, NUMERIC, TIMESTAMP)

### 2. SQL Query Generation

Load `references/sql_examples.md` for PostgreSQL-specific patterns:

**INSERT Operations:**
- Insert new companies with full address and metadata
- Create person records linked to companies
- Add sales opportunities with probability tracking
- Record events with JSONB metadata

**UPDATE Operations:**
- Update company information and annual revenue
- Change person job titles and departments
- Update opportunity status and close dates
- Add/remove JSONB tags
- Modify nested JSONB metadata

**SELECT Queries:**
- Get companies with contact counts
- Fetch person details with company information
- Query open opportunities with details
- Calculate pipeline value by status
- Search by JSONB tags using `?`, `?|`, `?&` operators
- Get activity timelines for opportunities
- Complex multi-table JOINs

### 3. PostgreSQL-Specific Features

**JSONB Operations:**
```sql
-- Check if tag exists
WHERE tags ? 'enterprise'

-- Check if any tag exists
WHERE tags ?| ARRAY['prospect', 'customer']

-- Add a tag
SET tags = tags || '["new-tag"]'::jsonb

-- Remove a tag
SET tags = tags - 'old-tag'

-- Update nested metadata
SET metadata = jsonb_set(metadata, '{outcome}', '"positive"')
```

**Timestamp Handling:**
```sql
-- Current timestamp
created_at = CURRENT_TIMESTAMP

-- Date truncation
DATE_TRUNC('quarter', CURRENT_DATE)

-- Interval calculations
event_date >= CURRENT_DATE - INTERVAL '30 days'
```

**Get ID After Insert (Two-Step Pattern):**
```sql
-- Step 1: INSERT (write_query) - NO RETURNING!
INSERT INTO person (name, email, created_at, updated_at)
VALUES ('John Doe', 'john@example.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Step 2: GET ID (read_query) - separate call
SELECT id FROM person WHERE email = 'john@example.com' ORDER BY created_at DESC LIMIT 1;
```

## Workflow

### Step 1: Understand the Request

Identify what the user wants to accomplish:
- Which table(s) are involved?
- Is this an INSERT, UPDATE, SELECT, or DELETE?
- What relationships need to be considered?
- Are JSONB fields involved?

### Step 2: Load Schema Reference

If unfamiliar with the table structure, read `references/schema.md` to understand:
- Column names and data types
- Required vs. optional fields
- Foreign key relationships
- JSONB field structures

### Step 3: Load SQL Examples

Read `references/sql_examples.md` to find similar query patterns:
- Look for analogous operations in the examples
- Adapt the pattern to the specific request
- Use PostgreSQL-specific syntax

### Step 4: Generate the SQL

Create the SQL query using:
- Correct PostgreSQL syntax (see `bel-crm-sql-rules` for limitations!)
- Proper data types (especially JSONB casting with `::jsonb`)
- **NO RETURNING clauses** - use separate read_query to get IDs
- **NO ON CONFLICT** - check existence first, then INSERT or UPDATE
- Appropriate JOINs when querying multiple tables
- JSONB operators for tag/metadata queries

### Step 5: Explain the Query

Provide context for the user:
- What the query does
- Which tables are involved
- Any assumptions made
- Expected output format

## Common Patterns

### Creating a Complete Company Record

When adding a new company, include:
- Required: `name`
- Optional but recommended: address fields, industry, website
- Tags as JSONB array: `'["prospect", "technology"]'::jsonb`
- **Do NOT use RETURNING** - query for ID separately if needed

### Linking People to Companies

When adding a person:
- Set `company_site_id` to link to company
- Include job_title and department for context
- Add tags like "decision-maker", "technical", "champion"
- Query for ID after INSERT if you need to confirm

### Tracking Sales Opportunities

When creating opportunities:
- Link to both person_id and company_site_id
- Set realistic probability (0-100)
- Use common status values: 'open', 'qualified', 'proposal', 'won', 'lost'
- Include expected_close_date
- Add descriptive tags for filtering

### Recording Events

When logging activities:
- Set appropriate type: 'email', 'call', 'meeting', 'note'
- Link to person_id, company_site_id, or opportunity_id as appropriate
- Use metadata JSONB for structured details (duration, outcome, next_action)
- Set event_date to when activity occurred, not when recorded

### Querying with JOINs

When fetching related data:
- Use LEFT JOIN to include records without relationships
- Use INNER JOIN to filter to only records with relationships
- Include relevant columns from joined tables
- Consider using subqueries for aggregations (COUNT, SUM)

## Tips

1. **Always Cast JSONB**: When inserting JSONB data, cast with `::jsonb`:
   ```sql
   '["tag1", "tag2"]'::jsonb
   ```

2. **NEVER Use RETURNING**: The PostgreSQL MCP server does not support RETURNING clauses. To get the ID after insert:
   ```sql
   -- Step 1: INSERT (write_query)
   INSERT INTO person (name, email, created_at, updated_at) VALUES ('John', 'john@example.com', now(), now());

   -- Step 2: GET ID (read_query)
   SELECT id FROM person WHERE email = 'john@example.com' ORDER BY created_at DESC LIMIT 1;
   ```

3. **NEVER Use ON CONFLICT**: The MCP server doesn't support upserts. Check existence first:
   ```sql
   -- Step 1: Check (read_query)
   SELECT id FROM company_site WHERE name ILIKE '%Acme%' LIMIT 1;

   -- Step 2: INSERT if not found, UPDATE if found (write_query)
   ```

4. **Handle NULL Values**: Use IS NULL / IS NOT NULL for checking null values, not = NULL

5. **JSONB Tag Searches**: Use `?` for single tag, `?|` for any of multiple tags, `?&` for all tags

6. **Update Timestamps**: Always set `updated_at = CURRENT_TIMESTAMP` when updating records

7. **Pipeline Calculations**: Calculate weighted pipeline value:
   ```sql
   SUM(value_eur * probability / 100.0) as weighted_value
   ```

8. **See `bel-crm-sql-rules`**: For complete list of SQL limitations and correct patterns.

## Resources

### references/schema.md
Complete database schema documentation including:
- All table structures
- Column definitions and data types
- Foreign key relationships
- JSONB field examples
- Index recommendations

### references/sql_examples.md
Comprehensive PostgreSQL query examples:
- INSERT operations for all tables
- UPDATE patterns including JSONB manipulation
- SELECT queries with JOINs and aggregations
- Date/time queries
- Complex reporting queries
- Common patterns (upsert, bulk insert, conditional updates)
