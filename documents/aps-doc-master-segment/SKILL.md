---
name: aps-doc-master-segment
description: Expert documentation generation for CDP Master Segment (Parent Segment) configurations. Analyzes master segment tables using TD MCP, extracts attribute and behavior schemas, documents star schema relationships, and creates comprehensive segment documentation. Use when documenting CDP parent segments.
---

# APS Master Segment Documentation Expert

Specialized skill for generating comprehensive documentation for CDP Master Segment (Parent Segment) configurations with complete attribute and behavior analysis.

## When to Use This Skill

Use this skill when:
- Documenting CDP Master Segment (Parent Segment) configurations
- Creating documentation for customer 360 parent segments
- Documenting segment attributes and behavior tables
- Generating star schema documentation for CDP audiences

**Example requests:**
```
"Document the master segment configuration for segment ID 1035571"
"Create parent segment documentation for customers master segment"
"Document CDP audience segment with database cdp_audience_1234567"
```

---

## 🚨 MANDATORY: Database Access Required

**WITHOUT database access = NO documentation. Period.**

**Two Methods to Access CDP Database:**

### Method 1: TD MCP Server (Preferred)

If TD MCP server is configured:
```
Use MCP tools to query CDP database:
- mcp__treasuredata__* tools for database operations
```

### Method 2: tdx CLI (Fallback)

If TD MCP is NOT configured, use tdx-basic skill:
```bash
# Use tdx commands to query database
tdx use database cdp_audience_<master_segment_id>
tdx tables
tdx describe <table_name>
```

**Required Inputs:**
1. **Master Segment ID** (e.g., 1035571) OR **Master Segment Name**
2. **Master Segment Database** (format: `cdp_audience_<master_segment_id>`)
3. **Master Table Name** (typically the primary fact table)

**Before proceeding:**
1. Check if TD MCP server is available (look for mcp__treasuredata__* tools)
2. If TD MCP NOT available, use tdx-basic skill with Bash tool
3. Confirm master segment database exists
4. Query table schemas using available method
5. STOP if cannot access database

**Documentation MUST contain:**
- Real table names from actual CDP database
- Actual column schemas from master and attribute tables
- Real behavior table structures
- Working SQL examples from actual schema

**NO generic placeholders. Only real, extracted data from TD MCP.**

---

## REQUIRED Documentation Template

**Follow this EXACT structure (analyzed from production examples):**

```markdown
# Parent Segment Configuration: {Master Segment Name}

**Last Updated:** {date}
**Master Segment ID:** {master_segment_id}
**Database:** {database_name}
**Master Table:** {master_table_name}

---

## Executive Summary

{Brief description of the parent segment purpose and business value}

### Key Metrics

* **Total Attributes:** {X} customer profile fields
* **Behavior Tables:** {Y} event tracking tables
* **Data Sources:** {List primary data sources}
* **Total Behavior Columns:** {Z} detailed event properties

---

## Architecture Overview

### Star Schema Data Model

{Describe star schema with master table as central fact table}

{ASCII diagram showing:
- Master table (center) with primary key
- Attribute tables (1:1 relationship) connected via foreign key
- Behavior tables (1:many relationship) connected via foreign key
- Clear cardinality indicators}

### Key Relationships:

* **Master Table (Fact):** {database}.{master_table} - One record per unique entity
* **Primary Key:** {primary_key_column} - Unique identifier
* **Foreign Key:** All attribute and behavior tables join via {primary_key_column}
* **Cardinality:**
    * Master to Attributes: **1:1** (one entity = one attribute record)
    * Master to Behaviors: **1:Many** (one entity = many event records)

### Master Table Structure

* **Database:** {database_name}
* **Primary Table:** {master_table_name}
* **Primary Key:** {primary_key_column}
* **Total Fields:** {N} fields directly in master table
* **Related Attribute Tables:**
    {List all attribute tables discovered from database}

### Behavior Tables (Event Streams)

{List all behavior tables with column counts}

**Note:** CDP automatically adds the `behavior_` prefix to all behavior table names in the audience database.

### Data Integration

{List source systems detected from table schemas or metadata}

---

## {Entity} Attributes ({Total} Fields)

{Group attributes by logical category - analyze from actual schema}

### {Category Number}. {Category Name} ({X} fields)

{Examples of categories based on actual data:
- Core Identity & Contact Information
- Address & Location
- Transaction & Purchase Behavior
- Customer Lifecycle & Engagement
- Email Marketing Engagement
- SMS Marketing Engagement
- Web & Digital Engagement
- Customer Preferences & Interests}

| Attribute Name | Data Type | Source | Business Use |
| --- | --- | --- | --- |
| {column_name} | {data_type} | {table}.{column} | {inferred business purpose} |

{Repeat for all attributes in category}

---

{Repeat for each category}

---

## Behavior Tables ({N} Event Streams)

### {Number}. {Behavior Table Display Name} ({X} columns)

**Table:** {behavior_table_name}
**Purpose:** {Inferred from table name and schema}

| Column Name | Data Type | Description |
| --- | --- | --- |
| {column_name} | {data_type} | {inferred purpose from column name} |

{List all columns from actual schema}

**Business Applications:**

* {Inferred use case 1}
* {Inferred use case 2}
* {Inferred use case 3}

---

{Repeat for each behavior table}

---

## Business Value & Use Cases

{Dynamically generate use cases based on attributes discovered in master segment}

### Marketing Campaign Segmentation

{Create 2-3 segment examples using ACTUAL attributes found:}
- If lifetime_value/revenue columns exist → High-Value Customer Targeting example
- If days_since_last_*/last_*_date columns exist → Win-Back Campaign example
- If engagement_score/page_views/events columns exist → Enthusiast Targeting example
- If transaction/order columns exist → Purchase Behavior Segmentation example

**Example Format (use real column names):**
```
High-Value Customer Targeting:
* {actual_ltv_column} > {reasonable_threshold}
* {actual_orders_column} > {reasonable_threshold}
* {actual_engagement_column} > {reasonable_threshold}
```

### Personalization Strategies

{Generate strategies ONLY if these attribute types exist:}
- If preference columns (cuisine_*, dietary_*, brand_*) → Preference-Based Personalization
- If product affinity columns → Product Recommendation Strategy
- If skill/level columns → Content Difficulty Matching
- If behavioral columns → Behavioral Trigger Strategy

### Performance Analytics

{Generate analytics ONLY based on metrics actually present:}
- If multiple channel engagement scores exist → Channel Effectiveness Comparison
- If conversion/rate columns exist → Conversion Funnel Analysis
- If content engagement metrics exist → Content Performance Tracking
- If attribution columns exist → Marketing Attribution Analysis

### Customer Lifecycle Management

{Generate lifecycle strategies ONLY if these columns exist:}
- If tenure/acquisition date columns → Onboarding Journey tracking
- If repeat/frequency columns → Loyalty & Retention programs
- If recency columns (days_since_*, last_*_date) → Churn Prevention strategies
- If lifecycle stage columns → Stage-Based Marketing

**CRITICAL:** Do NOT include sections if relevant attributes don't exist. Only generate use cases for attribute types actually present in the schema.

---

## Technical Specifications

### Data Refresh Schedule

* **Frequency:** [To be configured based on segment settings]
* **Timezone:** [To be configured]
* **Engine Version:** cdpaudience (Hive)

### Data Quality & Governance

{List privacy/compliance measures detected from schema}
* **Privacy Compliance:** {Hash columns found, e.g., email_hash, phone_hash}
* **Consent Tracking:** {Consent columns found}
* **Data Lineage:** {Lineage tracking columns found}
* **Validation:** {Validation flag columns found}

### Integration Points

{List source systems inferred from column names or metadata}

---

## Recommendations for Business Teams

{Generate recommendations dynamically based on actual attributes discovered}

### For Marketing Teams

{Create 3-4 actionable recommendations ONLY if these attribute types exist:}
1. If engagement_score/open_rate/click_rate columns → "Start with high-engagement segments ({actual_column} > {threshold})"
2. If preference columns (cuisine_*, dietary_*, brand_*) → "Test preference-based targeting using {actual_preference_columns}"
3. If tenure/lifecycle columns → "Implement lifecycle campaigns based on {actual_lifecycle_column}"
4. If behavior event tables → "Leverage behavioral triggers from {actual_behavior_table}"

**Format:** Use actual column names, not generic placeholders

### For Analytics Teams

{Create 3-4 recommendations ONLY if these attribute types exist:}
1. If value/revenue columns → "Build predictive models using {actual_ltv_column} and {actual_metric_columns}"
2. If multiple event tables → "Create customer journey maps combining {actual_behavior_tables}"
3. If attribution/source columns → "Analyze attribution using {actual_utm/source_columns}"
4. If multiple engagement metrics → "Monitor KPIs across {list_of_actual_channel_metrics}"

### For Product Teams

{Create 3-4 recommendations ONLY if these attribute types exist:}
1. If content engagement columns → "Optimize recommendations using {actual_engagement_score_column}"
2. If conversion/funnel columns → "Improve conversion funnels with {actual_conversion_metric}"
3. If preference data → "Enhance personalization based on {actual_preference_columns}"
4. If behavior patterns → "Identify feature opportunities from {actual_behavior_table} patterns"

**CRITICAL:**
- Only include team sections if relevant attributes exist for that team's work
- Use ACTUAL column names from schema, not examples
- Suggest realistic thresholds based on column data types
- If a team has no relevant attributes, OMIT that team section entirely

---

## Support & Questions

For questions about this parent segment configuration or assistance with creating child segments, please contact:

* **CDP Team:** [Contact information]
* **Data Engineering:** [Contact information]
* **Marketing Operations:** [Contact information]

---

**Document Status:** Production Ready
**Version:** 1.0
**Created:** {date}
```

---

**Template Usage Notes:**

**Phase 1: Master Segment Discovery**

**If TD MCP available:**
1. Use TD MCP tools to query: `SHOW TABLES IN {cdp_audience_database}`
2. Use TD MCP tools to describe tables

**If TD MCP NOT available:**
1. Use tdx-basic skill with Bash:
   ```bash
   tdx use database cdp_audience_<master_segment_id>
   tdx tables
   ```
2. For each table:
   ```bash
   tdx describe <table_name>
   ```

**Common Discovery Steps:**
1. Identify master table (typically without `behavior_` prefix)
2. Identify all attribute tables (tables with 1:1 relationship to master)
3. Identify all behavior tables (tables with `behavior_` prefix)

**Phase 2: Schema Extraction**

**If TD MCP available:**
1. Use MCP tools: `DESCRIBE {database}.{master_table}`
2. Query schema for each attribute table via MCP
3. Query schema for each behavior table via MCP

**If TD MCP NOT available:**
1. Use tdx commands via Bash:
   ```bash
   tdx describe <master_table>
   tdx describe <attribute_table_1>
   tdx describe <attribute_table_2>
   tdx describe behavior_<table_name>
   ```

**Common Extraction Steps:**
1. Extract primary key from master table
2. Verify foreign key relationships
3. Collect all column names and data types

**Phase 3: Documentation Generation**
1. Create star schema ASCII diagram with actual table names
2. Group attributes by logical category (analyze column names)
3. Document each attribute with real data type and source
4. Document each behavior table with full column list
5. Infer business uses from column names and data types
6. Generate example segment criteria using real metrics
7. Create recommendations based on actual available data

**Key Principles:**
- **Prefer TD MCP** but fallback to tdx CLI if MCP unavailable
- **Use tdx-basic skill** when using tdx commands via Bash
- **Extract real schemas** - no assumed or generic structures
- **Infer intelligently** - derive business meaning from technical column names
- **Group logically** - categorize attributes by business domain
- **NO placeholders** - every attribute/behavior must be from actual schema
- **Dynamic discovery** - discover all tables and columns from database

## Summary

This skill generates production-ready master segment documentation by:
- **Querying database schemas** via TD MCP (preferred) or tdx CLI (fallback)
- **Following exact template** structure from production examples
- **Discovering dynamically** all attribute and behavior tables
- **Extracting real schemas** with actual column names and data types
- **Inferring business value** from technical metadata
- **Creating comprehensive documentation** with star schema, attributes, behaviors, and use cases

**Key capability:** Transforms any CDP master segment into professional Confluence documentation by analyzing actual database schemas using available TD access methods (MCP or tdx CLI).

**Fallback Strategy:** If TD MCP server not configured, automatically uses tdx-basic skill to query schemas via tdx CLI commands.
