---
name: aps-doc-golden
description: Expert documentation generation for golden layers. Detects SCD types, documents business rules, metric definitions, aggregation logic, and data quality scoring. Use when documenting golden layer tables.
---

# APS Golden Layer Documentation Expert

Specialized skill for generating comprehensive documentation for golden layer tables - the final, analytics-ready data layer.

## When to Use This Skill

Use this skill when:
- Documenting golden layer tables
- Creating documentation for customer 360 tables
- Documenting SCD (Slowly Changing Dimension) implementations
- Generating documentation for metric calculations
- Documenting aggregation and business rule logic

**Example requests:**
```
"Document the golden layer customer master table"
"Create documentation for customer 360 golden table"
"Document SCD Type 2 implementation"
"Generate golden layer documentation following this template: [Confluence URL]"
```

---

## 🚨 MANDATORY: Codebase Access Required

**WITHOUT codebase access = NO documentation. Period.**

**If no codebase access provided:**
```
I cannot create technical documentation without codebase access.

Required:
- Directory path to golden layer workflows
- Access to .dig, .sql, .yml files

Without access, I cannot extract SCD logic, business rules, or table schemas.
Provide path: "Code is in /path/to/golden_layer/"
```

**Before proceeding:**
1. Ask for codebase path if not provided
2. Use Glob to verify files exist
3. STOP if cannot read files

**Documentation MUST contain:**
- Real SCD columns from actual SQL
- Actual business rules and CASE statements
- Real table/column names
- Working SQL examples from code

**NO generic placeholders. Only real, extracted data.**

## REQUIRED Documentation Template

**Follow this EXACT structure (analyzed from production examples):**

### For Parent Golden Layer Page:

```markdown
# Golden Layer - Unified Customer Data Platform (CDP)

## Overview
{Brief description of purpose}

**Purpose:**
- {Purpose 1}
- {Purpose 2}

**Key Features:**
- {Feature from actual workflow}
- {Feature from actual workflow}

---

## Architecture

### Layer Structure
{Text diagram showing data flow from sources → staging → enriched → golden}

### Data Sources
{Table with Source, System, Purpose, Priority}

---

## Data Flow

### High-Level Flow
{Text diagram showing:
1. Workflow Trigger
2. Parallel Table Creation
3. Atomic Table Replacement
4. Completion & Notification}

---

## Table Structure

### Attribute Tables
{Table with: Table name, Record count, Purpose, Key Metrics}
{Format: One row per customer (unified_id)}

### Behavior Tables
{Table with: Table name, Record count, Purpose, Granularity}
{Format: Event-level data (many rows per unified_id)}

---

## Workflow Orchestration

### Digdag Workflow: {golden_runner.dig}
{Structure showing:
- _export configuration
- +start
- +create_all_tables (_parallel: true)
- Sub-tasks list
- +complete
- _error}

**Execution Pattern:**
- Parallel Processing details
- Error Handling details

---

## Deployment Pattern

### Atomic Table Replacement (_tmp Pattern)
{4-step pattern:
1. DROP TABLE IF EXISTS _tmp
2. CREATE TABLE _tmp
3. DROP TABLE IF EXISTS production
4. RENAME _tmp to production}

**Benefits:**
{List benefits}

---

## How to Run

### Prerequisites
{List 4 prerequisites}

### Manual Execution
- Via Console
- Via Command Line

### Scheduled Execution
{Recommended schedule with cron example}

**Execution Time:**
{Table showing components and typical duration}

---

## Key Concepts

### 1. Master Data Management (MDM)
{Source Priority with COALESCE pattern}
{Priority Rationale}

### 2. Transaction Metrics Aggregation
{Real aggregation examples from codebase}

### 3. Atomic Blocking
{Related attributes from same source example}

### 4. Unified ID
{Unified ID description and usage}

### 5. Survivorship vs Aggregation
{Table showing pattern, use case, example}

---

## Data Quality & Governance

### Built-In Data Quality Measures
1. Deduplication
2. NULL Handling
3. Data Type Consistency
4. Referential Integrity

### Monitoring & Validation
{Post-Run Validation Queries}

**Data Freshness:**
{Table showing update frequency and latency}

---

## File Structure
{Directory tree showing workflow and SQL files}

---

## Related Documentation
{Links to related pages if applicable}

---

## Summary
{Brief recap of capabilities}
```

---

### For Golden Attributes Parent Page:

```markdown
# Golden Attributes

{Parent page links to 5 child pages for each attribute table}
```

---

### For Individual Golden Attribute Child Pages:

```markdown
# {Attribute Table Name}

**Purpose**: Comprehensive documentation of all attributes in {table_name}.sql
**Coverage**: {table_name}.sql - {X} Attributes | All Verified Against Current SQL

---

## {table_name}.sql - Complete Attribute Reference ({X} Attributes)

### {Category Name} ({Y} attributes)

{Examples: Identity & Contact, Profile - Name, Profile - Address, Transaction Metrics, Transaction Dates, User Lifecycle, Consent & Engagement, Activity Tracking, Preferences, Platform IDs, Metadata}

#### {Attribute Number}. {attribute_name}

**Location**: `{table_name}.sql:{line_number}`
**Data Type**: {VARCHAR/BIGINT/DOUBLE/ARRAY/TIMESTAMP/etc.}
**Description**: {Clear description from actual implementation}
**Priority**: {source1}(1) > {source2}(2) > {source3}(3) {if applicable}
**Implementation**:

```sql
{Real SQL from actual file - COALESCE, CASE, aggregation, etc.}
```

**Source**: {Source table(s) from actual code}
**Status**: ✅ CORRECT / ⚠️ PARTIAL {with notes if applicable}

{Special notes if applicable:}
- **Atomic Survivorship**: {Explain if related attributes must come from same source}
- **Calculation**: {Explain derived field logic}
- **Filter Logic**: {Explain WHERE clauses or exclusions}

---

{Repeat for all attributes, grouped by category}

---

{Repeat for each category}

---

## Summary

**Total Attributes**: {X}
**Fully Implemented**: {Y} ({Z}%)
**Partially Implemented**: {N} ({M}%)

{If applicable:}
**Pending Attributes** (awaiting integration):
- {List attributes pending future data source integration}

**Key Implementation Patterns**:
- **Atomic Survivorship**: {Real examples from codebase}
- **CTE-based Aggregation**: {Real examples from codebase}
- **Multi-source Concatenation**: {Real examples from codebase}
- **Single-source Strategy**: {Real examples from codebase}

---

**Last Updated**: {date}
**SQL File**: `golden/queries/{table_name}.sql`
**Total Lines**: {line_count}
```

---

### For Golden Behaviors Child Page:

```markdown
# Golden Behaviors

## Overview
{Brief description of behavior tables}

**Common Pattern:**
- All tables filter for unified_id IS NOT NULL
- Uses _tmp table pattern for atomic replacement
- Source: enriched tables from staging database
- Grain: One record per event

---

## {Behavior Table Number}. {Behavior Table Name}

{Examples: Transaction Behaviors, Email Behaviors, SMS Behaviors, Web Events, Web Pageviews, Marketing Automation Behaviors, etc.}

### Purpose
{Store specific behavior/event type with customer linkage}

### Table Details
- Source: {source_db}.{enriched_source_table}
- Target: {database}.{behavior_table_name}
- Grain: One record per {event type}
- Filter: {Specific metric/event filter if applicable}
- File: {behavior_table_name}.sql

### Description
{Captures specific events/behaviors from actual codebase}

### Key Characteristics
- {List from actual implementation}
- {Exclusion logic if applicable - e.g., cancelled transactions}

### Metrics Tracked {if applicable}
{Table with Metric Name and Description}
{Real metrics from codebase}

### Filter Logic
```sql
WHERE unified_id IS NOT NULL
    {AND additional filters from actual SQL}
```

---

{Repeat for each behavior table in actual codebase}

---

## Deployment Pattern

{4-step _tmp pattern with SQL example}

**This pattern ensures:**
- Zero downtime during updates
- Data consistency
- Atomic replacement of data

---

## Summary Statistics

{Table showing Behavior Type, Metric Count, Source Table}
```

---

**Template Usage Notes:**
- Read actual .dig workflows and .sql files from golden layer codebase
- **Dynamically discover** all attribute and behavior tables from actual code
- Extract REAL table names, attribute lists, metrics from SQL files
- Document REAL COALESCE patterns, aggregation logic, survivorship rules
- Include working SQL examples with actual line numbers from codebase
- Create parent + child pages based on actual table structure found in code
- Document _tmp pattern for atomic deployment
- **NO customer-specific hardcoding** - discover everything from codebase
- **Follow same template structure** for all customers but with their actual data

## Summary

This skill generates production-ready golden layer documentation by:
- **Dynamically analyzing** actual .dig workflows and .sql files from codebase
- **Auto-discovering** all attribute and behavior tables by reading SQL files
- Following the exact template structure shown above for **any customer**
- Extracting real MDM rules, aggregation patterns, and table structures
- Creating parent + child page documentation based on actual code structure

**Key capability:** Transforms **any** golden layer codebase into professional Confluence documentation with dynamically-generated attribute/behavior catalog following consistent template structure.
