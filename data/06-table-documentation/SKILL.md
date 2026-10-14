---
name: 06-table-documentation
description: Comprehensive documentation standards for Gold layer tables including naming conventions, column descriptions, and metadata requirements. Use when creating Gold layer tables, columns, or writing documentation to ensure dual-purpose descriptions that serve both business users and technical users (including LLMs like Genie). Includes YAML schema consultation patterns, surrogate key patterns, SCD Type 2 documentation, and implementation guidance for Silver table naming conventions.
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: bundle_deploy
deploy_note: "Design-phase pattern; output feeds the Gold design/setup artifacts deployed downstream via `bundle deploy --target dev`. No standalone resource."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.0"
  domain: gold
  role: worker
  pipeline_stage: 1
  pipeline_stage_name: gold-design
  called_by:
    - gold-layer-design
  standalone: true
  last_verified: "2026-02-07"
  volatility: low
  upstream_sources: []  # Internal documentation patterns
---
# Gold Layer Documentation Standards

## Overview

Gold layer tables require comprehensive, dual-purpose documentation that serves both business users and technical users (including LLMs like Genie). This skill standardizes naming conventions, description formats, and metadata requirements for production-grade Gold layer implementations.

## When to Use This Skill

- Creating Gold layer table DDL with comments
- Writing column descriptions for dimensions and facts
- Documenting surrogate keys, business keys, and foreign keys
- Implementing SCD Type 2 dimensions
- Setting up table properties and governance metadata
- Preparing documentation for Genie Spaces and AI/BI tools

## Critical Rules

### 1. YAML Schema Files Are Single Source of Truth

**CRITICAL:** Before writing any Gold layer SQL (TVFs, queries, MERGE statements), ALWAYS consult the YAML schema definitions in `gold_layer_design/yaml/**/*.yaml`.

**Why:** 100% of SQL compilation errors in production deployments were caused by not consulting YAML schemas first.

### 2. Dual-Purpose Documentation

Every description must serve **both business and technical audiences** without requiring an "LLM:" prefix.

**Pattern:**
```
[Natural description]. Business: [business context and use cases]. Technical: [implementation details and calculations].
```

See [LLM Optimization Guide](references/llm-optimization.md) for complete patterns.

### 3. Surrogate Keys as Primary Keys

- **Surrogate keys** (store_key, product_key, date_key) are PRIMARY KEYS
- **Business keys** (store_number, upc_code, date) are denormalized for readability
- **Facts reference surrogate PKs** via foreign keys

## Quick Reference

### Column Naming Conventions

| Column Type | Pattern | Example | Notes |
|-------------|---------|---------|-------|
| Surrogate Key | `{entity}_key` | `store_key`, `product_key` | Always NOT NULL, PRIMARY KEY |
| Business Key | Natural name | `store_number`, `upc_code` | Denormalized in facts |
| Foreign Key | `{entity}_key` | `store_key` | References surrogate PK |
| Measure | Descriptive | `net_revenue`, `units_sold` | Include calculation formula |
| Percentage | `{name}_pct` | `return_rate_pct` | Document NULL handling |
| Boolean Flag | `is_{state}` | `is_current`, `is_weekend` | Document TRUE/FALSE meanings |
| Timestamp | `{purpose}_timestamp` | `record_created_timestamp` | Document update behavior |

### Table Comment Structure

Every Gold table comment must include:
1. Layer and purpose
2. Grain (what one row represents)
3. Business use cases
4. Technical implementation

See [Documentation Templates](references/documentation-templates.md) for complete examples.

### Required Table Properties

```python
TBLPROPERTIES (
    # Performance
    'delta.enableChangeDataFeed' = 'true',
    'delta.enableRowTracking' = 'true',
    'delta.enableDeletionVectors' = 'true',
    'delta.autoOptimize.autoCompact' = 'true',
    'delta.autoOptimize.optimizeWrite' = 'true',
    
    # Layer and Quality
    'quality' = 'gold',
    'layer' = 'gold',
    'source_layer' = 'silver',
    'source_table' = '<silver_source_table>',
    
    # Domain and Classification
    'domain' = '<retail|sales|inventory|product>',
    'entity_type' = '<dimension|fact>',
    
    # Governance
    'contains_pii' = '<true|false>',
    'data_classification' = '<confidential|internal|public>',
    'business_owner' = '<Team Name>',
    'technical_owner' = 'Data Engineering',
    
    # Dimension-specific
    'scd_type' = '<1|2>',
    
    # Fact-specific
    'grain' = '<description of grain>',
    'gold_type' = '<aggregated|snapshot>'
)
```

## Core Patterns

### Column Description Format

**Standard Template:**
```
[One-sentence definition]. Business: [Business purpose, use cases, and context]. Technical: [Data type, format, calculation logic, source, constraints].
```

**Example - Surrogate Key:**
```python
store_key STRING NOT NULL COMMENT 'Surrogate key uniquely identifying each version of a store record. Business: Used for joining fact tables to dimension. Technical: MD5 hash generated from store_id and processed_timestamp to ensure uniqueness across SCD Type 2 versions.'
```

**Example - Measure:**
```python
net_revenue DECIMAL(18,2) COMMENT 'Net revenue after subtracting returns from gross revenue. Business: The actual revenue realized from sales, primary KPI for financial reporting. Technical: gross_revenue - return_amount, represents true daily sales value.'
```

See [Documentation Templates](references/documentation-templates.md) for examples by field type.

### Table Comment Patterns

**Dimension Table:**
```python
COMMENT 'Gold layer conformed {entity} dimension with {SCD Type}. Business: {Business purpose, history tracking, use cases}. Technical: {SCD implementation details, key strategy, update behavior}.'
```

**Fact Table:**
```python
COMMENT 'Gold layer {period} {subject} fact table with {aggregation level} at {grain}. Business: {Primary use cases, metrics included, reporting purpose}. Technical: Grain is {what one row represents}. {Performance optimizations, key relationships}.'
```

### SCD Type 2 Pattern

For slowly changing dimensions, include:
- `effective_from TIMESTAMP NOT NULL` - Start timestamp
- `effective_to TIMESTAMP` - End timestamp (NULL = current)
- `is_current BOOLEAN NOT NULL` - Current version flag

Always filter with `WHERE is_current = true` when joining to facts.

## Validation Checklist

### Naming Conventions
- [ ] Surrogate keys use `{entity}_key` pattern
- [ ] Business keys use natural terminology
- [ ] Measures use descriptive names (no cryptic abbreviations)
- [ ] Percentages end with `_pct`
- [ ] Boolean flags start with `is_` or action verb
- [ ] Timestamps end with `_timestamp`
- [ ] SCD fields use `effective_from`, `effective_to`, `is_current`

### Column Documentation
- [ ] Every column has a comment
- [ ] Comments follow: `[Definition]. Business: [context]. Technical: [details].` format
- [ ] Surrogate keys document hash generation method
- [ ] Business keys document source and immutability
- [ ] Foreign keys document referenced table and column
- [ ] Measures document calculation formula
- [ ] Flags document TRUE/FALSE meanings
- [ ] Timestamps document update behavior

### Table Documentation
- [ ] Table comment includes layer and grain
- [ ] Table comment explains business use cases
- [ ] Table comment describes technical implementation
- [ ] TBLPROPERTIES includes all required fields
- [ ] `grain` property set for fact tables
- [ ] `scd_type` property set for dimensions
- [ ] `CLUSTER BY AUTO` specified

### Primary and Foreign Keys
- [ ] Surrogate keys are NOT NULL
- [ ] PRIMARY KEYs defined on surrogate keys
- [ ] FOREIGN KEYs reference surrogate PKs
- [ ] Facts have composite PKs matching grain
- [ ] UNIQUE constraints on business keys (where applicable)

## Common Mistakes to Avoid

### ❌ Mistake 1: Using "LLM:" prefix
```python
# OLD PATTERN (Don't use)
store_key STRING NOT NULL COMMENT 'LLM: Surrogate key (unique per version)'
```

### ✅ Correct: Natural dual-purpose description
```python
store_key STRING NOT NULL COMMENT 'Surrogate key uniquely identifying each version of a store record. Business: Used for joining fact tables to dimension. Technical: MD5 hash generated from store_id and processed_timestamp to ensure uniqueness across SCD Type 2 versions.'
```

### ❌ Mistake 2: Business key as PRIMARY KEY
```python
# WRONG: Breaks dimensional modeling
CREATE TABLE dim_store (
    store_key STRING NOT NULL,
    store_number STRING NOT NULL PRIMARY KEY,  -- ❌ Wrong
    ...
)
```

### ✅ Correct: Surrogate key as PRIMARY KEY
```python
CREATE TABLE dim_store (
    store_key STRING NOT NULL,
    store_number STRING NOT NULL,
    ...
    CONSTRAINT pk_dim_store PRIMARY KEY (store_key) NOT ENFORCED,  -- ✅ Correct
    CONSTRAINT uk_store_number UNIQUE (store_number) NOT ENFORCED  -- Business key is UNIQUE
)
```

### ❌ Mistake 3: Missing grain in TBLPROPERTIES
```python
# Fact table without grain
TBLPROPERTIES (
    'layer' = 'gold',
    'entity_type' = 'fact'
    # Missing 'grain' property
)
```

### ✅ Correct: Grain documented
```python
TBLPROPERTIES (
    'layer' = 'gold',
    'entity_type' = 'fact',
    'grain' = 'daily_store_product'  -- ✅ Clear grain definition
)
```

## Reference Files

### Documentation Templates
[references/documentation-templates.md](references/documentation-templates.md) - Complete column and table comment templates with examples for all field types (surrogate keys, business keys, foreign keys, measures, percentages, boolean flags, timestamps, SCD Type 2 fields).

### LLM Optimization
[references/llm-optimization.md](references/llm-optimization.md) - Dual-purpose documentation patterns optimized for Genie and AI/BI tools, including natural language optimization techniques and testing strategies.

## Assets

### Documentation Template
[assets/templates/gold-table-docs.yaml](assets/templates/gold-table-docs.yaml) - YAML template for Gold layer table documentation with all required fields and examples.

## References

### Dimensional Modeling
- [Kimball Dimensional Modeling](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
- [Star Schema Design](https://docs.databricks.com/lakehouse-architecture/medallion.html)

### Unity Catalog
- [Unity Catalog Constraints](https://docs.databricks.com/data-governance/unity-catalog/constraints.html)
- [Primary and Foreign Keys](https://docs.databricks.com/tables/constraints.html#declare-primary-key-and-foreign-key-relationships)

### Delta Lake
- [Delta Table Properties](https://docs.delta.io/latest/table-properties.html)
- [Automatic Clustering](https://docs.databricks.com/aws/en/delta/clustering#enable-or-disable-automatic-liquid-clustering)

## Inputs

- **From `05-erd-diagrams`:** ERD diagrams with domain groupings, table/column names, and relationship notation
- **From `01-grain-definition` through `04-conformed-dimensions`:** Grain types, dimension patterns, fact table patterns, and conformed dimension list

## Outputs

- YAML schema files with dual-purpose descriptions for every table and column
- Complete TBLPROPERTIES metadata (layer, domain, entity_type, grain, scd_type)
- Surrogate key patterns and SCD Type 2 field documentation
- Column-level lineage metadata embedded in each YAML

## Design Notes to Carry Forward

After completing this skill, note:
- [ ] Which dimensions use SCD Type 2 (need effective_from, effective_to, is_current fields)
- [ ] YAML files are the single source of truth — implementation reads from them
- [ ] Any non-standard column descriptions that may need semantic layer attention

## Next Step

Proceed to `design-workers/07-design-validation/SKILL.md` to cross-validate all design artifacts (YAML ↔ ERD ↔ Lineage) before handoff to implementation.
