---
name: 04-conformed-dimensions
description: Enterprise integration patterns for Gold layer dimensional models. Covers conformed dimensions, the enterprise data warehouse bus matrix, shrunken/rollup dimensions, conformed facts, and drill-across query patterns. Use when planning dimensions shared across multiple fact tables, creating a bus matrix for enterprise integration, designing rollup dimensions, or enabling cross-process analytics. Triggers on "conformed dimension", "bus matrix", "drill-across", "shrunken dimension", "rollup", "enterprise integration", "cross-process".
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: bundle_deploy
deploy_note: "Design-phase pattern; output feeds the Gold design/setup artifacts deployed downstream via `bundle deploy --target dev`. No standalone resource."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.0.0"
  domain: gold
  role: worker
  pipeline_stage: 1
  pipeline_stage_name: gold-design
  called_by:
    - gold-layer-design
  standalone: true
  last_verified: "2026-02-19"
  volatility: low
  upstream_sources: []
---

# Conformed Dimensions & Enterprise Integration

## Overview

A dimensional model becomes an **enterprise data warehouse** when dimensions are shared (conformed) across multiple fact tables, enabling consistent drill-across queries. Without conformed dimensions, each fact table becomes an isolated silo — users cannot compare sales with inventory with marketing in a single report.

**Key Principle:** Conformed dimensions are built once, used everywhere. They must have identical column names, data types, and domain values across all fact tables that reference them.

**Anti-Pattern:** Never join fact tables directly to each other. Instead, use conformed dimensions to "drill across" from one fact to another.

## When to Use This Skill

- Planning which dimensions will be shared across multiple fact tables
- Building an enterprise data warehouse bus matrix
- Designing shrunken (rollup) dimensions for aggregate fact tables
- Enabling cross-process analytics (e.g., comparing sales with returns with inventory)
- Reviewing a dimensional model for consistency before ERD creation

## The Bus Matrix

The bus matrix is the master planning document for a dimensional model. It maps business processes (fact tables) to the dimensions they use, revealing which dimensions must be conformed.

### Bus Matrix Template

| Business Process (Fact) | dim_date | dim_customer | dim_product | dim_store | dim_employee | dim_promotion |
|------------------------|----------|-------------|-------------|-----------|-------------|---------------|
| **fact_sales_daily** | X | X | X | X | | X |
| **fact_inventory_snapshot** | X | | X | X | | |
| **fact_returns** | X | X | X | X | X | |
| **fact_promotions** | X | | X | X | | X |

### Reading the Bus Matrix

- **Columns with multiple X's** = conformed dimensions (shared across processes)
- **dim_date, dim_product, dim_store** have X in every row → must be conformed
- **dim_employee** only appears in returns → does not need conformance yet
- **Rows** represent individual star schemas (fact + its dimensions)

### Key Rules

1. **Build the bus matrix before creating ERDs** — it is the blueprint for the entire model
2. Every X means the fact table has a foreign key to that dimension
3. Conformed dimensions must have **identical** column definitions across all references
4. The bus matrix drives domain grouping for ERD organization

## Conformed Dimension Rules

### What Makes a Dimension "Conformed"

| Requirement | Detail |
|------------|--------|
| **Same name** | `dim_product` everywhere (not `dim_product_sales` and `dim_product_inventory`) |
| **Same keys** | `product_key` is the same surrogate key in all fact tables |
| **Same attributes** | Column names, types, and domain values are identical |
| **Same grain** | One row per product (not one row per product-store) |
| **Single source** | Built once, referenced by all fact tables |

### Common Conformance Violation

```yaml
# ❌ BAD: Two separate "product" dimensions with different attributes
# fact_sales references dim_product_sales (has price columns)
# fact_inventory references dim_product_inventory (has warehouse columns)

# ✅ GOOD: One conformed dim_product with ALL attributes
table_name: dim_product
columns:
  - name: product_key
    type: BIGINT
  - name: product_name
    type: STRING
  - name: list_price        # Used by sales
    type: DOUBLE
  - name: warehouse_zone    # Used by inventory
    type: STRING
```

## Shrunken (Rollup) Dimensions

When an aggregate fact table operates at a coarser grain than the base fact, it needs a **shrunken dimension** — a strict subset of rows from the conformed dimension.

### Example

```yaml
# Base dimension: one row per store
table_name: dim_store
columns:
  - name: store_key
    type: BIGINT
  - name: store_name
    type: STRING
  - name: district_name
    type: STRING
  - name: region_name
    type: STRING

# Shrunken dimension: one row per district (rollup of stores)
table_name: dim_district
description: "District rollup dimension. Business: Geographic districts. Technical: Shrunken dimension — subset of dim_store rolled up to district grain."
columns:
  - name: district_key
    type: BIGINT
  - name: district_name
    type: STRING
  - name: region_name
    type: STRING
```

### Key Rules

- Shrunken dimensions must be **strict subsets** of the conformed dimension
- Column names and domain values must match the parent dimension exactly
- Shrunken dimensions are used with aggregate fact tables (pre-computed summaries)
- Always maintain a FK relationship between the base dimension and shrunken dimension

## Conformed Facts

Just as dimensions must be conformed, **facts (measures)** that appear in multiple fact tables must use identical definitions.

| Rule | Detail |
|------|--------|
| **Same name** | `revenue` in fact_sales = `revenue` in fact_returns (not `sales_revenue` vs `return_revenue`) |
| **Same calculation** | quantity × unit_price in both tables |
| **Same units** | USD everywhere (not USD in sales, EUR in international) |
| **Same data type** | DOUBLE in all tables |

If the same measure has different semantics in different processes, use **different names** (e.g., `gross_revenue` vs `net_revenue`).

## Drill-Across Queries

### What Is Drill-Across

Drill-across combines measures from multiple fact tables using conformed dimensions as the join key. This is the primary benefit of conformed dimensions.

### Pattern

```sql
-- Drill-across: combine sales and inventory using conformed dimensions
WITH sales AS (
  SELECT date_key, product_key, store_key, SUM(revenue) AS total_revenue
  FROM fact_sales_daily
  GROUP BY date_key, product_key, store_key
),
inventory AS (
  SELECT date_key, product_key, store_key, on_hand_quantity
  FROM fact_inventory_snapshot
)
SELECT
  d.date_value,
  p.product_name,
  s.store_name,
  COALESCE(sales.total_revenue, 0) AS total_revenue,
  COALESCE(inventory.on_hand_quantity, 0) AS on_hand_quantity
FROM dim_date d
JOIN dim_product p ON ...
JOIN dim_store s ON ...
LEFT JOIN sales ON sales.date_key = d.date_key
  AND sales.product_key = p.product_key
  AND sales.store_key = s.store_key
LEFT JOIN inventory ON inventory.date_key = d.date_key
  AND inventory.product_key = p.product_key
  AND inventory.store_key = s.store_key
```

### Critical Anti-Pattern: Direct Fact-to-Fact Joins

**NEVER** join one fact table directly to another fact table.

```sql
-- ❌ BAD: Direct fact-to-fact join
SELECT * FROM fact_sales s
JOIN fact_inventory i ON s.product_key = i.product_key AND s.date_key = i.date_key
-- This produces a Cartesian explosion if grains don't match!
```

**Why:** Fact tables at different grains produce incorrect Cartesian products. Always drill across through conformed dimensions using separate aggregated subqueries.

## Validation Checklist (Design Phase)

Before finalizing the enterprise model:

- [ ] Bus matrix created mapping all fact tables to their dimensions
- [ ] Conformed dimensions identified (dimensions with X in multiple bus matrix rows)
- [ ] Conformed dimensions have identical column definitions everywhere
- [ ] No duplicate dimensions for the same business concept
- [ ] Shrunken dimensions documented as subsets of their parent dimension
- [ ] Conformed facts use identical names, calculations, and units
- [ ] No fact-to-fact joins planned in any query patterns

## Reference Files

- **[Conformed Dimension Examples](references/conformed-dimension-examples.md)** — Bus matrix template, shrunken dimension YAML examples, drill-across SQL patterns, and multi-star integration examples

## Inputs

- **From `01-grain-definition`:** Fact table grain definitions (determines which dimensions each fact needs)
- **From `02-dimension-patterns`:** Dimension designs (reveals which dimensions exist and their attributes)
- **From `03-fact-table-patterns`:** Fact table designs with measure classifications

## Outputs

- Enterprise bus matrix (fact tables × dimensions)
- List of conformed dimensions with conformance requirements
- Shrunken dimension designs (if aggregate facts exist)
- Conformed fact definitions (measures that appear in multiple facts)

## Design Notes to Carry Forward

After completing this skill, note:
- [ ] The bus matrix (which fact references which dimensions)
- [ ] Which dimensions are conformed (shared across multiple facts)
- [ ] Any shrunken dimensions needed for aggregate facts
- [ ] Drill-across query patterns planned for cross-process analytics

## Next Step

Proceed to `design-workers/05-erd-diagrams/SKILL.md` to create ERD diagrams that visualize the dimensional model. The bus matrix from this step drives domain grouping and relationship documentation.

## Related Skills

- **Grain Definition:** `design-workers/01-grain-definition/SKILL.md` — Grain types for fact tables
- **Dimension Patterns:** `design-workers/02-dimension-patterns/SKILL.md` — Individual dimension patterns
- **Fact Table Patterns:** `design-workers/03-fact-table-patterns/SKILL.md` — Fact table design patterns
- **ERD Diagrams:** `design-workers/05-erd-diagrams/SKILL.md` — Visualizing the model

## References

- [Kimball Dimensional Modeling Techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
- [AgentSkills.io Specification](https://agentskills.io/specification)
