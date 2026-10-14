---
name: 03-fact-table-patterns
description: Advanced fact table design patterns for Gold layer modeling. Covers measure additivity classification (additive, semi-additive, non-additive), factless fact tables, accumulating snapshot facts, consolidated fact tables, header/line fact patterns, late-arriving facts and dimensions, and NULL handling in measures. Use when designing fact tables beyond basic transaction/aggregate patterns, classifying measure types, or handling complex fact scenarios. Triggers on "fact pattern", "factless", "accumulating snapshot", "measure additivity", "semi-additive", "late arriving", "consolidated fact".
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

# Fact Table Design Patterns

## Overview

Beyond basic transaction and aggregated fact tables (covered in `01-grain-definition`), real-world dimensional models require specialized fact patterns to handle non-additive measures, coverage tracking, multi-stage processes, and late-arriving data. Choosing the wrong measure type or fact pattern leads to incorrect aggregations that silently produce wrong numbers in dashboards.

**Key Principle:** Store additive components in the fact table; compute non-additive metrics (ratios, percentages, averages) in the BI/semantic layer.

**Companion skill:** For grain type selection (transaction/aggregated/snapshot), see `design-workers/01-grain-definition/SKILL.md`.

## When to Use This Skill

- Classifying measures as additive, semi-additive, or non-additive
- Designing factless fact tables (event tracking, coverage)
- Modeling multi-stage business processes (accumulating snapshots)
- Combining multiple processes into consolidated fact tables
- Handling late-arriving facts or dimensions in the design
- Deciding what to store vs what to compute at query time

## Measure Additivity Classification

This is the most critical concept in fact table design. Getting it wrong means dashboards show incorrect numbers.

| Type | Definition | Can SUM Across... | Example |
|------|------------|--------------------|---------|
| **Additive** | Freely summable across ALL dimensions | All dimensions | revenue, quantity, cost |
| **Semi-Additive** | Summable across SOME dimensions, not time | Non-time dimensions only | account_balance, inventory_on_hand |
| **Non-Additive** | Cannot be summed across ANY dimension | None — must recompute | unit_price, temperature, ratio |

### Critical Rule: Store Additive Components

```yaml
# ❌ BAD: Storing a non-additive metric
columns:
  - name: avg_order_value
    type: DOUBLE
    # Cannot SUM averages across stores or dates!

# ✅ GOOD: Store the additive components
columns:
  - name: total_revenue
    type: DOUBLE
    description: "Total revenue. Business: Sum of all order amounts. Technical: Additive — safe to SUM across all dimensions."
  - name: order_count
    type: BIGINT
    description: "Number of orders. Business: Count of distinct orders. Technical: Additive — safe to SUM across all dimensions."
# avg_order_value = total_revenue / order_count (computed in semantic layer)
```

**Pragmatic Exception:** When a derived metric is queried in >80% of dashboard queries and recomputation is expensive, storing it as a pre-calculated column is acceptable — but document it clearly as non-additive and include the component columns.

```yaml
# ✅ ACCEPTABLE: Pre-calculated for performance, with components retained
columns:
  - name: total_revenue
    type: DOUBLE
  - name: transaction_count
    type: BIGINT
  - name: avg_transaction_value
    type: DOUBLE
    description: "Average transaction value. Business: Revenue per transaction. Technical: NON-ADDITIVE — do not SUM. Pre-calculated as total_revenue / transaction_count. Use components for cross-dimensional aggregation."
```

### Semi-Additive Measures

Semi-additive measures represent balances or levels at a point in time. They can be summed across non-time dimensions but require special handling across time (typically use latest value or weighted average).

```yaml
# Semi-additive: inventory levels
table_name: fact_inventory_snapshot
columns:
  - name: on_hand_quantity
    type: BIGINT
    description: "Inventory on hand. Business: Units in stock at snapshot time. Technical: SEMI-ADDITIVE — SUM across stores, but use LAST_VALUE across dates."
  - name: on_order_quantity
    type: BIGINT
    description: "Inventory on order. Business: Units ordered but not received. Technical: SEMI-ADDITIVE — same aggregation rules as on_hand_quantity."
```

## Fact Table Type Quick Reference

| Pattern | Use When | Grain | Key Characteristic |
|---------|----------|-------|--------------------|
| **Transaction** | One event = one row | Per event | Additive measures |
| **Periodic Snapshot** | Regular state capture | Per entity per period | Semi-additive measures |
| **Accumulating Snapshot** | Multi-stage process | Per process instance | Multiple date FKs |
| **Factless (Event)** | Tracking occurrence | Per event | No measures (or count=1) |
| **Factless (Coverage)** | Tracking eligibility | Per entity-period | No measures |
| **Consolidated** | Multiple processes, one table | Varies | Nullable measure groups |
| **Header/Line** | Parent-child transactions | Per line item | Header FK on fact |

## Critical Patterns

### Factless Fact Tables

When the business question is "did this event occur?" or "what was eligible?" rather than "how much?"

```yaml
# Factless: student attendance tracking
table_name: fact_student_attendance
description: "Student attendance. Business: Tracks which students attended which classes. Technical: Factless fact — presence/absence tracked by row existence."
grain: "One row per student-class-date attendance event"
grain_type: transaction
columns:
  - name: attendance_key
    type: BIGINT
    nullable: false
  - name: date_key
    type: BIGINT
    foreign_key:
      references: dim_date.date_key
  - name: student_key
    type: BIGINT
    foreign_key:
      references: dim_student.student_key
  - name: class_key
    type: BIGINT
    foreign_key:
      references: dim_class.class_key
  # No measure columns — row existence IS the fact
```

**Usage:** "Which students did NOT attend?" = all possible combinations MINUS fact rows.

### Accumulating Snapshot Facts

When a business process has defined milestones (order placed → shipped → delivered → returned):

```yaml
table_name: fact_order_fulfillment
description: "Order fulfillment pipeline. Business: Tracks orders through placement, payment, shipment, delivery. Technical: Accumulating snapshot — rows updated as milestones are reached."
grain: "One row per order (updated at each milestone)"
grain_type: accumulating_snapshot
columns:
  - name: order_key
    type: BIGINT
    nullable: false
  - name: order_date_key
    type: BIGINT
    foreign_key:
      references: dim_date.date_key
  - name: payment_date_key
    type: BIGINT
    description: "Payment date. Technical: NULL until payment received."
    foreign_key:
      references: dim_date.date_key
  - name: ship_date_key
    type: BIGINT
    description: "Ship date. Technical: NULL until order shipped."
    foreign_key:
      references: dim_date.date_key
  - name: delivery_date_key
    type: BIGINT
    description: "Delivery date. Technical: NULL until order delivered."
    foreign_key:
      references: dim_date.date_key
  - name: order_to_ship_days
    type: INT
    description: "Days from order to shipment. Technical: Derived, NULL until shipped."
  - name: ship_to_delivery_days
    type: INT
    description: "Days from ship to delivery. Technical: Derived, NULL until delivered."
```

**Key Rule:** Accumulating snapshot rows are **updated** (not inserted) as each milestone occurs. This requires MERGE with UPDATE semantics.

### NULL Handling in Facts

| Scenario | Rule |
|----------|------|
| Missing FK | Replace with Unknown member key (-1) |
| Missing additive measure | Store as NULL (not 0) — NULL excludes from SUM correctly |
| Missing semi-additive measure | Store as NULL — indicates no observation |
| Inapplicable measure | Store as NULL — this row doesn't participate |

**Critical:** NULL vs 0 matters. Zero means "we measured and the value was zero." NULL means "we did not measure" or "not applicable."

## Validation Checklist (Design Phase)

Before finalizing any fact table YAML schema:

- [ ] Every measure classified as additive, semi-additive, or non-additive
- [ ] Non-additive metrics stored as pre-calculated ONLY if justified (with components retained)
- [ ] Additive components present for any pre-calculated ratios/averages
- [ ] Factless facts have no measure columns (or just a dummy count column)
- [ ] Accumulating snapshots have multiple date FKs with explicit NULL semantics
- [ ] NULL vs 0 decision documented for each measure column

## Reference Files

- **[Fact Pattern Catalog](references/fact-pattern-catalog.md)** — Extended examples for consolidated facts, header/line facts, late-arriving data handling, and centipede fact anti-pattern with YAML templates

## Inputs

- **From `01-grain-definition`:** Grain type decisions for each fact table (transaction/aggregated/snapshot)
- **From `02-dimension-patterns`:** Dimension designs revealing FK targets, role-playing dimension views, and junk dimension keys

## Outputs

- Fact table YAML schemas with measure additivity annotations
- Measure classification table (additive/semi-additive/non-additive per column)
- Decision log for any pre-calculated non-additive columns (justification)

## Design Notes to Carry Forward

After completing this skill, note:
- [ ] Which measures are semi-additive (need special time-dimension handling in semantic layer)
- [ ] Which pre-calculated non-additive columns exist (and their component columns)
- [ ] Any factless fact tables (need special ETL: row existence tracking, no aggregation)
- [ ] Any accumulating snapshot facts (need MERGE with UPDATE, not INSERT)

## Next Step

Proceed to `design-workers/04-conformed-dimensions/SKILL.md` to plan enterprise integration patterns (bus matrix, conformed dimensions, drill-across queries).

## Related Skills

- **Grain Definition:** `design-workers/01-grain-definition/SKILL.md` — Basic grain type selection
- **Dimension Patterns:** `design-workers/02-dimension-patterns/SKILL.md` — Dimension design patterns
- **Merge Patterns (Implementation):** `pipeline-workers/02-merge-patterns/SKILL.md` — SCD and aggregation merge scripts

## References

- [Kimball Dimensional Modeling Techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)
- [AgentSkills.io Specification](https://agentskills.io/specification)
