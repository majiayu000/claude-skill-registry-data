---
name: documenting-dbt-models
description: Document a dbt project — model and column descriptions in schema.yml, source definitions, exposures, doc blocks, and generated docs/lineage. Use when adding descriptions to dbt models, documenting sources or dashboards as exposures, setting up dbt docs, or improving data catalog coverage.
---

# Documenting dbt Models

## When to use

- Adding or improving descriptions for models, columns, and sources.
- Registering downstream dashboards/apps as exposures for lineage.
- Setting up `dbt docs` generation and reusable doc blocks.
- Do NOT use for writing tests (use `testing-dbt-projects`).

## Workflow

```
- [ ] Describe each model: what it is, its grain, and who uses it
- [ ] Describe key columns (keys, enums, money, dates)
- [ ] Reuse repeated definitions with doc blocks
- [ ] Register BI dashboards as exposures
- [ ] Run dbt docs generate and review lineage
```

1. **Model description** states the grain and purpose in one or two lines — the
   grain is the most valuable fact for a consumer.
2. **Column descriptions** for keys, enums, money, and dates; skip self-evident
   ones to avoid noise.
3. **Doc blocks** (`{% docs %}`) for definitions reused across models (e.g. what
   "active customer" means) so they stay consistent.
4. **Exposures** connect models to the dashboards/ML jobs that consume them, so
   lineage and `dbt build --select +exposure` work.

## Patterns

**schema.yml with descriptions:**

```yaml
models:
  - name: fct_orders
    description: "One row per order line. Grain: order_id + line_number. Feeds Finance revenue dashboard."
    columns:
      - name: order_id
        description: "Natural order identifier from the shop system."
      - name: status
        description: '{{ doc("order_status") }}'
```

**Reusable doc block** (in a `.md` file under `models/`):

```markdown
{% docs order_status %}
Lifecycle status: placed → shipped → delivered, or cancelled at any point.
{% enddocs %}
```

**Exposure:**

```yaml
exposures:
  - name: revenue_dashboard
    type: dashboard
    maturity: high
    url: https://bi.example.com/revenue
    depends_on:
      - ref('fct_orders')
      - ref('dim_customer')
    owner: { name: Data Team, email: data@example.com }
```

Then `dbt docs generate && dbt docs serve` renders descriptions and a lineage
graph including exposures.

## Common pitfalls

- **Restating the column name** ("order_id is the order id") — add only what the
  name cannot convey (source, units, grain, meaning of enum values).
- **Omitting the grain** — the single most useful line for any consumer.
- **Duplicating definitions** across models instead of using a doc block — they
  drift apart.
- **No exposures** — lineage stops at the warehouse and you cannot see what breaks
  downstream when a model changes.
