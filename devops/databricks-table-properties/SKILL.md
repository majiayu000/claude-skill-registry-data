---
name: databricks-table-properties
description: Provides standard TBLPROPERTIES and metadata patterns for Unity Catalog Delta tables across Bronze, Silver, and Gold medallion layers. Ensures governance compliance, performance optimization, and proper metadata tagging for all table creation operations. Covers required TBLPROPERTIES by layer (Bronze, Silver DLT, Gold), mandatory CLUSTER BY AUTO configuration, Change Data Feed (CDF) enablement, auto-optimize settings, table and column comment patterns (LLM-friendly for Bronze/Silver, dual-purpose for Gold), domain values, data classification tags, and validation checklists. Use when creating Delta tables, configuring table properties, enabling CDF, setting up auto-optimize, or ensuring governance metadata consistency. Critical for preventing missing properties, incorrect clustering configurations, and governance compliance issues.
metadata:
  author: prashanth subrahmanyam
  version: "1.1"
  domain: infrastructure
  role: shared
  used_by_stages: [1, 2, 3, 4]
  last_verified: "2026-06-02"
  volatility: medium
  clients: [ide_cli, genie_code]   # deploy via databricks-asset-bundles (the spine); Genie detail via genie-code-environment
  deploy_verb: "bundle deploy --target dev"
  deploy_note: "TBLPROPERTIES/CREATE TABLE are deploy-time bundle-resource bodies (RULE_10: run during bundle deploy, retained)"
  coverage: all_stages
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-unity-catalog/SKILL.md"
      relationship: "derived"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
---

# Databricks Table Properties Standards

## Pattern Recognition
Every table creation (Bronze, Silver, Gold) uses a consistent set of TBLPROPERTIES and metadata. This rule standardizes these patterns to ensure governance compliance.

## Required Table Properties by Layer

See `assets/templates/table-properties.sql` for complete SQL templates.

### Bronze Layer Tables (11 required properties + optional retention)

```python
TBLPROPERTIES (
    'delta.enableChangeDataFeed' = 'true',
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true',
    'layer' = 'bronze',
    'source_system' = 'RetailChain',  # Update based on source
    'domain' = '<domain>',  # e.g., 'retail', 'sales', 'inventory', 'product'
    'entity_type' = '<dimension|fact>',
    'contains_pii' = '<true|false>',
    'data_classification' = '<confidential|internal>',
    'business_owner' = '<Team Name>',
    'technical_owner' = 'Data Engineering',
    # Optional: Add retention for compliance
    'retention_period' = '7_years'  # Only if required
)
```

### Silver Layer DLT Tables (15 required properties)

```python
table_properties={
    "quality": "silver",
    "delta.enableChangeDataFeed": "true",
    "delta.enableRowTracking": "true",
    "delta.enableDeletionVectors": "true",
    "delta.autoOptimize.autoCompact": "true",
    "delta.autoOptimize.optimizeWrite": "true",
    "delta.tuneFileSizesForRewrites": "true",
    "layer": "silver",
    "source_table": "<bronze_table_name>",
    "domain": "<domain>",
    "entity_type": "<dimension|fact|quarantine>",
    "contains_pii": "<true|false>",
    "data_classification": "<confidential|internal>",
    "business_owner": "<Team Name>",
    "technical_owner": "Data Engineering"
}
```

### Gold Layer Tables (14 required properties)

```python
TBLPROPERTIES (
    'delta.enableChangeDataFeed' = 'true',
    'delta.enableRowTracking' = 'true',
    'delta.enableDeletionVectors' = 'true',
    'delta.autoOptimize.autoCompact' = 'true',
    'delta.autoOptimize.optimizeWrite' = 'true',
    'layer' = 'gold',
    'source_layer' = 'silver',
    'domain' = '<domain>',
    'entity_type' = '<dimension|fact>',
    'contains_pii' = '<true|false>',
    'data_classification' = '<confidential|internal>',
    'business_owner' = '<Team Name>',
    'technical_owner' = 'Data Engineering',
    'gold_type' = '<scd2|snapshot|aggregated>'
)
```

## Clustering Configuration

**⚠️ MANDATORY: ALWAYS use automatic liquid clustering**

**NEVER specify clustering columns manually. Always use AUTO.**

```python
# For SQL DDL (Bronze, Gold)
CLUSTER BY AUTO

# For DLT Python (Silver)
cluster_by_auto=True
```

**Benefits of AUTO clustering:**
- ✅ Delta automatically selects optimal clustering columns
- ✅ Self-tuning based on query patterns
- ✅ No manual column specification needed
- ✅ Works with all data types (including BOOLEAN)
- ✅ Adapts as data and queries evolve

**❌ DO NOT DO THIS:**
```sql
CLUSTER BY (column1, column2)  -- ❌ WRONG: Never specify columns
CLUSTER BY (is_current)         -- ❌ WRONG: BOOLEAN columns don't support clustering
```

**✅ ALWAYS DO THIS:**
```sql
CLUSTER BY AUTO  -- ✅ CORRECT: Let Delta choose optimal clustering
```

## Table Comments

### Modern Pattern (RECOMMENDED for Gold Layer)
**For Gold layer tables, use dual-purpose documentation without "LLM:" prefix.**

See `data_product_accelerator/skills/gold/design-workers/06-table-documentation/SKILL.md` for comprehensive Gold layer standards.

**Pattern:**
```
[Natural description]. Business: [business context and use cases]. Technical: [implementation details].
```

**Example:**
```sql
COMMENT 'Gold layer daily sales fact table with pre-aggregated metrics at store-product-day grain. Business: Primary source for sales performance reporting including revenue, units, discounts, returns, and customer loyalty metrics. Aggregated from transaction-level Silver data for fast query performance. Used for dashboards, executive reporting, and sales analysis. Technical: Grain is one row per store-product-date combination. Pre-aggregated measures eliminate need for transaction-level scans, surrogate keys enable fast dimension joins.'
```

### Legacy Pattern (Bronze/Silver)
**For Bronze and Silver layers, "LLM:" prefix is acceptable for brevity.**

```python
# DLT Example (Silver)
@dlt.table(
    name="silver_transactions",
    comment="""LLM: Silver layer streaming fact table for point-of-sale transactions with comprehensive 
    data quality rules, price validation, discount logic verification, and referential integrity checks""",
    table_properties={...},
    cluster_by_auto=True
)

# SQL DDL Example (Bronze)
COMMENT 'LLM: Bronze layer dimension table containing retail store location details with full UC compliance. Store details to link across other views and ensure accuracy of data linkage.'
```

## Column Comments

### Gold Layer (Dual-Purpose Format)
**Every column in Gold layer must have comprehensive dual-purpose comments:**

**Pattern:**
```
[Definition]. Business: [purpose, use cases, business rules]. Technical: [data type, format, calculation, source, constraints].
```

**Examples:**
```python
# Surrogate key
store_key STRING NOT NULL 
    COMMENT 'Surrogate key uniquely identifying each version of a store record. Business: Used for joining fact tables to dimension. Technical: MD5 hash generated from store_id and processed_timestamp to ensure uniqueness across SCD Type 2 versions.'

# Business key
store_number STRING NOT NULL 
    COMMENT 'Business key identifying the physical store location. Business: The primary identifier used by store operations and field teams. Technical: Natural key from source system, same across all historical versions of this store.'

# Measure
net_revenue DECIMAL(18,2) 
    COMMENT 'Net revenue after subtracting returns from gross revenue. Business: The actual revenue realized from sales, primary KPI for financial reporting. Technical: gross_revenue - return_amount, represents true daily sales value.'
```

### Bronze/Silver Layers (Simpler Format)
**Column comments can be more concise but should still include key context:**

```python
store_number STRING NOT NULL 
    COMMENT 'Store number where the transaction occurred. Links to store dimension.'
    
transaction_date DATE NOT NULL
    COMMENT 'Transaction date from POS system. Used for daily aggregations and trending.'
```

## Domain Values

Standard domains used in this project:
- `retail` - Store and location data
- `sales` - Transaction and revenue data
- `inventory` - Stock and replenishment data
- `product` - Product master data
- `logistics` - Delivery and supply chain
- `revenue` - Financial metrics

## Data Classification Values

- `confidential` - Contains PII or sensitive business data
- `internal` - Business data without PII
- `public` - Safe for external sharing (rare)

## Validation Checklist

When creating any table, ensure:
- [ ] **Property count**: Bronze tables have 11+ TBLPROPERTIES, Silver have 15, Gold have 14
- [ ] **Cross-reference**: Properties match THIS skill's layer section, not just the calling template
- [ ] `layer` property matches the actual layer
- [ ] `domain` is from the standard list
- [ ] `entity_type` is dimension, fact, or quarantine
- [ ] `contains_pii` accurately reflects PII presence
- [ ] `data_classification` aligns with contains_pii
- [ ] `business_owner` is a real team name
- [ ] `CLUSTER BY AUTO` or `cluster_by_auto=True` is set
- [ ] Table comment starts with "LLM:"
- [ ] All columns have detailed comments

## Common Mistakes to Avoid

❌ **Don't do this:**
```python
# Missing critical properties
TBLPROPERTIES (
    'layer' = 'bronze'
)

# No clustering
CREATE TABLE my_table (...)
USING DELTA

# Minimal comment
COMMENT 'Store data'
```

✅ **Do this:**
```python
# Complete properties
TBLPROPERTIES (
    'delta.enableChangeDataFeed' = 'true',
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true',
    'layer' = 'bronze',
    'source_system' = 'RetailChain',
    'domain' = 'retail',
    'entity_type' = 'dimension',
    'contains_pii' = 'true',
    'data_classification' = 'confidential',
    'business_owner' = 'Retail Operations',
    'technical_owner' = 'Data Engineering'
)
CLUSTER BY AUTO
COMMENT 'LLM: Bronze layer dimension table containing retail store location details with full UC compliance. Store details to link across other views and ensure accuracy of data linkage.'
```

## Gotchas

- **Templates in worker skills may be incomplete.** The `copy_from_source.py` template and `data-source-approaches.md` examples in the Bronze skill contain only performance properties (CDF, auto-optimize). After copying from ANY template, cross-check every table against the required property list for its layer in THIS skill. Anti-pattern: assuming the template has all properties.
- **DEEP CLONE preserves some properties but not all.** DEEP CLONE preserves CDF settings, CLUSTER BY AUTO, column COMMENTs, PK constraints, and row tracking metadata. It does NOT automatically set governance properties (`domain`, `entity_type`, `contains_pii`, `data_classification`, `business_owner`, `technical_owner`). After every DEEP CLONE, apply the remaining enterprise TBLPROPERTIES with `ALTER TABLE ... SET TBLPROPERTIES`. See `assets/templates/table-properties.sql` for the post-clone template.
- **Skipping requirements collection makes correct properties impossible.** If per-table metadata (`entity_type`, `contains_pii`, `data_classification`) is never collected from the user or schema CSV, the agent cannot set the right values. Always resolve these before writing DDL.
- **Never use `DEFAULT` column clauses in DDL.** A `DEFAULT <expr>` clause (e.g. `is_active BOOLEAN NOT NULL DEFAULT true`) requires the `delta.feature.allowColumnDefaults` table feature, which is OFF by default — the `CREATE TABLE` fails. Do NOT enable the feature flag; declare the column without `DEFAULT` and supply the value at INSERT time. Also do not add columns the template/design never specified. See `unity-catalog-constraints` → "Never Use `DEFAULT` Column Clauses in DDL".

## References

- [Delta Lake Table Properties](https://docs.databricks.com/delta/table-properties.html)
- [Unity Catalog Governance](https://docs.databricks.com/unity-catalog/governance.html)
- [Automatic Clustering](https://docs.databricks.com/aws/en/delta/clustering#enable-or-disable-automatic-liquid-clustering)
