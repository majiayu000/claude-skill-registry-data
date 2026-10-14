---
name: 01-grain-definition
description: Grain definition patterns for fact tables during the Gold layer design phase. Use when choosing grain types (transaction, aggregated, snapshot), documenting grain in YAML schemas, and applying the PK-grain decision tree to determine whether a fact table needs aggregation. Prevents costly table rewrites by catching grain ambiguity before implementation.
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

# Fact Table Grain Definition Patterns

## Overview

Fact tables have a **grain** — the level of detail at which measurements are stored. Misunderstanding grain (transaction-level vs aggregated) causes 5% of Gold layer bugs but has high impact (complete table rewrite required). This skill provides patterns to **define and document grain during the design phase** so that implementation is unambiguous.

**Key Principle:** The PRIMARY KEY you choose in the YAML schema reveals the grain. Get this right during design and the merge script writes itself.

**Companion skill:** For runtime grain validation before MERGE, see `pipeline-workers/04-grain-validation/SKILL.md`.

## When to Use This Skill

- Designing fact table YAML schemas (choosing grain type)
- Deciding between transaction, aggregated, or snapshot patterns
- Documenting grain in YAML `table_properties` and column comments
- Applying the PK-grain decision tree to determine aggregation needs
- Reviewing fact table designs for grain ambiguity

## Understanding Fact Table Grain

### Grain Definition

**Grain:** The combination of dimensions that uniquely identifies one measurement row.

### Grain Examples

| Grain | Description | Primary Key | Row Represents |
|-------|-------------|-------------|----------------|
| **Transaction** | One row per event | `transaction_id` | Individual sale |
| **Daily Summary** | One row per day-store-product | `date_key, store_key, product_key` | Daily totals |
| **Hourly Aggregate** | One row per hour-cluster | `date_key, hour_of_day, cluster_key` | Hourly metrics |
| **Snapshot** | One row per entity-date | `entity_key, snapshot_date_key` | Daily snapshot |

## Grain Type Decision Tree

```
PRIMARY KEY column count?
├─ 1 column
│  ├─ Ends with _id, _uid? → Transaction Grain
│  ├─ Is date_key? → Daily Snapshot Grain
│  └─ Otherwise → Unknown (manual review)
│
└─ Multiple columns (Composite PK)
   ├─ Contains date_key + dimension keys? → Aggregated Grain
   ├─ Contains entity_key + date_key? → Snapshot Grain
   └─ Otherwise → Composite (manual review)
```

## Grain Type Descriptions

### Transaction-Level Fact

**When to Use:**
- **One row per business event** (sale, click, API call)
- **Primary Key:** Single surrogate key (`transaction_id`, `event_id`, `request_id`)
- **Measures:** Individual event metrics (amount, duration, count=1)

**Key Characteristics:**
- ✅ No `.groupBy()` or `.agg()` in merge script
- ✅ Single surrogate key as PRIMARY KEY
- ✅ Measures are direct pass-through (no SUM, AVG, COUNT)
- ✅ One source row → one target row

### Aggregated Fact

**When to Use:**
- **Pre-aggregated summaries** (daily sales, hourly usage)
- **Primary Key:** Composite key of dimensions defining grain (`date_key, store_key, product_key`)
- **Measures:** Aggregated metrics (total_revenue, avg_latency, request_count)

**Key Characteristics:**
- ✅ Uses `.groupBy()` on grain dimensions
- ✅ Uses `.agg()` with SUM, COUNT, AVG, MAX
- ✅ Composite PRIMARY KEY matches `.groupBy()` columns
- ✅ Multiple source rows → one target row per grain

### Snapshot Fact

**When to Use:**
- **Point-in-time state** (daily inventory levels, account balances)
- **Primary Key:** Entity + date (`entity_key, snapshot_date_key`)
- **Measures:** Current values at snapshot time (on_hand_quantity, balance_amount)

**Key Characteristics:**
- ✅ No aggregation (snapshots already at correct grain)
- ✅ May need deduplication (latest snapshot wins)
- ✅ Composite PK: entity keys + snapshot date
- ✅ Measures are point-in-time values (not SUMs)

## YAML Grain Documentation

### Common Mistake: Ambiguous YAML Grain

```yaml
# ❌ BAD: Grain not explicitly documented
table_name: fact_model_serving_inference
primary_key:
  columns:
    - date_key
    - endpoint_key
    - model_key
# What grain is this? Daily aggregate? Hourly? Per request?
```

### Correct: Document Grain Explicitly

```yaml
# ✅ GOOD: Grain explicitly documented
table_name: fact_model_serving_inference
grain: "Daily aggregate per endpoint-model combination"
grain_type: aggregated
primary_key:
  columns:
    - date_key
    - endpoint_key
    - model_key
measures:
  - name: request_count
    aggregation: SUM
  - name: avg_latency_ms
    aggregation: AVG
```

### Required YAML Fields for Grain Clarity

Every fact table YAML schema MUST include:

| Field | Location | Example |
|-------|----------|---------|
| `grain` | `table_properties.grain` | `"daily_store_product"` |
| `grain_type` | `table_properties.grain_type` or top-level | `"aggregated"` / `"transaction"` / `"snapshot"` |
| Composite PK | `primary_key.columns` | `["date_key", "store_key", "product_key"]` |
| Measure aggregation | `measures[].aggregation` (optional) | `SUM`, `AVG`, `COUNT` |

## Grain Documentation Template

Use this docstring pattern in fact table merge scripts (enforced during implementation):

```python
def merge_fact_[table_name](spark, catalog, silver_schema, gold_schema):
    """
    Merge fact_[table_name] from Silver to Gold.
    
    GRAIN: [Describe grain in plain English]
    - Example: "One row per date-store-product combination (daily aggregate)"
    - Example: "One row per individual query execution (transaction level)"
    
    PRIMARY KEY: [List PK columns]
    - Example: (date_key, store_key, product_key)
    - Example: (query_key)
    
    GRAIN TYPE: [transaction | aggregated | snapshot]
    
    AGGREGATION: [Required | Not Required]
    - If Required: GroupBy on [dimensions], Aggregate [measures]
    """
```

## Validation Checklist (Design Phase)

Before finalizing any fact table YAML schema:

- [ ] Read PRIMARY KEY columns and infer grain type using decision tree
- [ ] Document grain type explicitly in YAML (`grain`, `grain_type`)
- [ ] Document grain in plain English in YAML `description`
- [ ] Determine if aggregation will be required during implementation

## Common Mistakes to Avoid

| Mistake | Impact | Prevention |
|---------|--------|------------|
| No `grain` in YAML | Implementation guesses wrong grain → table rewrite | Always document grain in YAML |
| Composite PK without grain_type | Ambiguous: daily aggregate or hourly? | Add `grain_type: aggregated` |
| Single PK that looks composite | Confusion during merge script writing | Document clearly: "transaction-level" |

## Reference Files

- **[Grain Definition Patterns](references/grain-definition-patterns.md)** — Detailed pattern descriptions for transaction, aggregated, and snapshot grains with DDL examples

## Related Skills

- **Grain Validation (Implementation):** `pipeline-workers/04-grain-validation/SKILL.md` — Runtime validation of grain before MERGE operations
- **Fact Table Merge Patterns:** `pipeline-workers/02-merge-patterns/SKILL.md` — SCD Type 1/2 and aggregation merge patterns

## References

- [Kimball Dimensional Modeling](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/) - Grain definition
- [AgentSkills.io Specification](https://agentskills.io/specification)

## Inputs

- **From orchestrator Phase 0/1:** Source schema inventory with table classifications (dimension/fact/bridge), inferred FK relationships, and domain groupings

## Outputs

- Grain type decision for each fact table (transaction / aggregated / snapshot)
- Documented `grain` and `grain_type` fields in each fact table YAML schema
- PK structure aligned to grain type

## Design Notes to Carry Forward

After completing this skill, note:
- [ ] Grain type for each fact table (transaction/aggregated/snapshot)
- [ ] Which fact tables require `.groupBy().agg()` during implementation (aggregated grain)
- [ ] Which fact tables have snapshot semantics (need dedup-latest logic)

## Next Step

Proceed to `design-workers/02-dimension-patterns/SKILL.md` to apply dimension design patterns (role-playing, junk, degenerate, hierarchy flattening).

---

**Pattern Origin:** Bug #84 (wrong fact table grain), 2% of Gold bugs but high impact
**Key Lesson:** DDL PRIMARY KEY reveals grain. Composite PK = aggregated, single PK = transaction.
**Impact:** Prevents costly table rewrites by catching grain mismatches before implementation
