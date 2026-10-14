---
name: 02-dimension-patterns
description: Dimension design patterns for Gold layer modeling. Covers role-playing dimensions, degenerate dimensions, junk dimensions, mini-dimensions, outrigger dimensions, denormalized hierarchies, null handling, and flags as textual attributes. Use when designing dimension tables, choosing between dimension patterns, handling NULLs in dimensions, or flattening hierarchies. Triggers on "dimension pattern", "role-playing", "junk dimension", "degenerate dimension", "mini-dimension", "hierarchy", "NULL handling".
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

# Dimension Design Patterns

## Overview

Beyond basic dimension tables, real-world dimensional models require specialized patterns to handle time-variant roles, degenerate keys, low-cardinality flags, deep hierarchies, and NULL values. Choosing the wrong pattern leads to query complexity, redundant joins, or data quality issues that surface late in development.

**Key Principle:** Denormalize aggressively within dimensions. Each dimension row should carry all the context a query needs without requiring additional joins.

**Companion skill:** For SCD Type 1/2 documentation standards (surrogate keys, effective dates, is_current flags), see `design-workers/06-table-documentation/SKILL.md`.

## When to Use This Skill

- Designing dimension tables that play multiple roles (e.g., order_date vs ship_date)
- Deciding whether to create a junk dimension for low-cardinality flags
- Handling NULL foreign keys or missing dimension attributes
- Flattening hierarchies (org charts, product categories, geographies)
- Choosing between outrigger dimensions vs denormalization

## Dimension Pattern Quick Reference

| Pattern | Use When | Key Rule |
|---------|----------|----------|
| **Role-Playing** | Same dimension used in multiple FK roles | Create views, not copies |
| **Degenerate** | Dimension has no attributes beyond the key | Store as fact table column, no dim table |
| **Junk** | Multiple low-cardinality flags/indicators | Combine into one dimension |
| **Mini-Dimension** | Rapidly changing subset of a large dimension | Split volatile attributes into separate dim |
| **Outrigger** | Dimension references another dimension | FK from dim to dim (use sparingly) |
| **Denormalized Hierarchy** | Multi-level hierarchy (org, geography) | Flatten all levels into one row |
| **Multiple Hierarchies** | Same dimension has alternate rollup paths | Add columns for each hierarchy path |

## Critical Rules

### 1. Denormalize, Do Not Snowflake

**NEVER** normalize dimension tables into sub-tables (snowflaking). Every join a BI tool must traverse degrades query performance and confuses business users.

```yaml
# ❌ BAD: Snowflaked (separate tables for each hierarchy level)
# dim_product → dim_subcategory → dim_category → dim_department

# ✅ GOOD: Denormalized flat dimension
table_name: dim_product
columns:
  - name: product_key
    type: BIGINT
    nullable: false
  - name: product_name
    type: STRING
  - name: subcategory_name    # Flattened from subcategory table
    type: STRING
  - name: category_name       # Flattened from category table
    type: STRING
  - name: department_name     # Flattened from department table
    type: STRING
```

### 2. Replace NULLs with Descriptive Values

Dimension foreign keys should **never** be NULL. Instead, point to a dedicated "Unknown" or "Not Applicable" row in the dimension table.

```yaml
# ✅ GOOD: Unknown member row in dimension
# dim_customer row: customer_key = -1, customer_name = "Unknown", ...
# fact_orders: customer_key = -1 (instead of NULL)
```

**Why:** NULLs break GROUP BY aggregations, confuse BI tools, and make outer joins necessary. An "Unknown" row participates cleanly in all queries.

### 3. Flags Must Be Textual Attributes

Never store boolean flags as `true`/`false` or `0`/`1` in **business-sourced** dimensions. Use full textual descriptions instead.

```yaml
# ❌ BAD: Boolean flags
- name: is_active
  type: BOOLEAN

# ✅ GOOD: Textual attributes
- name: active_status
  type: STRING
  description: "Active status indicator. Business: Shows whether entity is currently active. Technical: Values are 'Active' or 'Inactive'."
```

**Why:** BI reports display raw values. "Active" reads better than "true" in dashboards and Genie responses.

**Exception — generated date/time dimensions.** `dim_date` (and `dim_time` if present) are fully generated from a date range, not sourced from a business system. Their indicator columns (`is_weekend`, `is_holiday`, `is_business_day`, `is_month_end`, …) MAY be `BOOLEAN`. These columns are read almost exclusively by date-range filters and SQL predicates where `day_of_week IN (1,7)` or `is_weekend = TRUE` is idiomatic, and they are already well-described by their column names. The canonical template in `references/yaml-schema-patterns.md` uses BOOLEAN for these columns, and the Phase 8 semantic validator whitelists them.

Every other dimension — including any derived business dimension that aggregates or classifies transactional data — MUST follow the textual-attribute rule above.

### 4. Avoid Abstract Generic Dimensions

Never create catch-all "entity" or "type" dimensions that combine unrelated business concepts.

```yaml
# ❌ BAD: Generic dimension combining unrelated concepts
table_name: dim_entity  # Contains customers, products, stores...

# ✅ GOOD: Separate dimensions per business concept
table_name: dim_customer
table_name: dim_product
table_name: dim_store
```

## Pattern Details

### Role-Playing Dimensions

When the same dimension (e.g., `dim_date`) appears in multiple foreign key roles on a fact table:

```yaml
# Fact table references dim_date three times
table_name: fact_orders
columns:
  - name: order_date_key
    type: BIGINT
    description: "Order placement date. Business: When the order was placed. Technical: FK to dim_date."
    foreign_key:
      references: dim_date.date_key
  - name: ship_date_key
    type: BIGINT
    description: "Shipment date. Business: When the order shipped. Technical: FK to dim_date."
    foreign_key:
      references: dim_date.date_key
  - name: delivery_date_key
    type: BIGINT
    description: "Delivery date. Business: When customer received order. Technical: FK to dim_date."
    foreign_key:
      references: dim_date.date_key
```

**Implementation:** Create SQL views (`dim_order_date`, `dim_ship_date`, `dim_delivery_date`) over the single physical `dim_date` table. Do NOT create separate physical tables.

### Degenerate Dimensions

When a dimension key has no meaningful attributes beyond the key itself (e.g., order number, invoice number):

```yaml
# ✅ Store directly on the fact table — no separate dimension table
table_name: fact_order_lines
columns:
  - name: order_number
    type: STRING
    description: "Order number. Business: Groups line items belonging to same order. Technical: Degenerate dimension — no separate dim table."
```

**Rule:** If the only attribute is the key itself, it belongs on the fact table as a degenerate dimension.

### Junk Dimensions

When a fact table has multiple low-cardinality flags (2-5 possible values each), combine them into a single junk dimension instead of cluttering the fact table.

```yaml
table_name: dim_order_flags
description: "Order flag combinations. Business: Categorizes orders by processing characteristics. Technical: Junk dimension combining low-cardinality indicators."
columns:
  - name: order_flag_key
    type: BIGINT
    nullable: false
  - name: payment_method
    type: STRING    # "Credit Card", "Debit Card", "Cash", "Gift Card"
  - name: shipping_priority
    type: STRING    # "Standard", "Express", "Overnight"
  - name: gift_wrap_status
    type: STRING    # "Gift Wrapped", "Not Gift Wrapped"
  - name: return_eligibility
    type: STRING    # "Returnable", "Final Sale"
```

**Threshold:** Create a junk dimension when you have 3+ flags with combined cardinality under ~50 combinations.

## Validation Checklist (Design Phase)

Before finalizing any dimension YAML schema:

- [ ] No snowflaked sub-tables — all hierarchies flattened into dimension
- [ ] NULL handling defined — "Unknown" row planned for each dimension
- [ ] All flags are textual (STRING), not BOOLEAN
- [ ] Role-playing dimensions use views, not physical copies
- [ ] Degenerate dimensions stored on fact table, no empty dim tables
- [ ] Junk dimension considered for 3+ low-cardinality flags
- [ ] No abstract generic dimensions combining unrelated concepts

## Reference Files

- **[Dimension Pattern Catalog](references/dimension-pattern-catalog.md)** — Extended examples for mini-dimensions, outrigger dimensions, multiple hierarchies, and bridge tables with YAML templates

## Inputs

- **From `01-grain-definition`:** Fact table grain definitions and PK structure (reveals which dimensions are needed as FK targets)
- **From orchestrator Phase 0/1:** Source schema inventory with table classifications (dimension/fact/bridge)

## Outputs

- Dimension table YAML schemas with pattern annotations (role-playing, degenerate, junk, etc.)
- NULL handling strategy document (which dimensions get "Unknown" rows)
- Hierarchy flattening decisions (which levels to denormalize)

## Design Notes to Carry Forward

After completing this skill, note:
- [ ] Which dimensions are role-playing (need views during implementation)
- [ ] Which dimensions have "Unknown" member rows planned
- [ ] Which flags were combined into junk dimensions (and the junk dimension name)
- [ ] Any mini-dimension splits (volatile attributes separated from main dimension)

## Next Step

Proceed to `design-workers/03-fact-table-patterns/SKILL.md` to apply advanced fact table patterns (measure additivity, factless facts, accumulating snapshots).

## Related Skills

- **Grain Definition:** `design-workers/01-grain-definition/SKILL.md` — Grain types for fact tables
- **Table Documentation:** `design-workers/06-table-documentation/SKILL.md` — SCD Type 1/2 documentation, surrogate key standards
- **ERD Diagrams:** `design-workers/05-erd-diagrams/SKILL.md` — Visualizing dimension-fact relationships

## References

- [Kimball Dimensional Modeling Techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
- [AgentSkills.io Specification](https://agentskills.io/specification)
