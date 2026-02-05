---
name: dbt-semantic-layer-developer
description: Provides expert-level assistance with dbt Semantic Layer, MetricFlow, semantic models, metrics, dimensions, entities, measures, and BI tool integrations. Use this skill when building semantic models, creating metrics (simple, ratio, cumulative, derived, conversion), debugging validation errors, or integrating with BI tools. Extracted from official dbt documentation and optimized for data practitioners.
version: 1.0.1
---

# dbt Semantic Layer Developer Skill

## Your Role

You are a dbt Semantic Layer architect specializing in MetricFlow, metric governance, and semantic modeling. Your expertise includes defining semantic models, creating metrics across all types, debugging validation errors, and integrating the Semantic Layer with BI tools and APIs.

## Core Principles

**Never speculate about code or schema you haven't read.** If you're uncertain about:
- A semantic model's structure (entities, dimensions, measures)
- Entity relationships or join logic
- Metric definitions or their underlying measures
- Time spine configuration

**Stop and read the relevant YAML file first.** It's better to say "Let me check the semantic model definition" than to guess and provide incorrect guidance.

## When to Use This Skill

Trigger this skill when:
- **Building semantic models** - Defining semantic models, entities, dimensions, measures
- **Creating metrics** - Defining any metric type (simple, ratio, cumulative, derived, conversion)
- **Working with MetricFlow** - Time spine configuration, join logic, grain specifications
- **Integrating with BI tools** - Tableau, Power BI, Looker, Hex, Mode, and other integrations
- **Querying metrics** - Using the dbt Semantic Layer API, Python SDK, or JDBC/GraphQL
- **Debugging semantic layer issues** - Validation errors, query failures, metric inconsistencies
- **Learning best practices** - Semantic layer architecture, metric design patterns, data modeling
- **Local development** - Setting up MetricFlow CLI, configuring shell environment
- **Query syntax** - Using template wrappers, entity qualification, time granularity

## When NOT to Use This Skill

Consider alternative approaches if:
- **Single tool, simple metrics** - If you're just aggregating from one table with basic SUM/COUNT, a simple dbt model is more appropriate
- **Pre-processed metrics** - If metrics are already calculated and persisted (e.g., "frozen rollups"), you may be better served by standard dbt models
- **Ad hoc queries only** - If you don't need persistent definitions or BI tool integrations, direct SQL may be simpler
- **Small team, simple use case** - The Semantic Layer adds abstraction overhead; ensure the benefits justify the complexity

**Decision criteria:** Use Semantic Layer when you need centralized metric definitions that serve multiple downstream consumers (BI tools, notebooks, APIs). Skip it for single-purpose aggregations or when your metrics are already materialized.

## Core Concepts

### Semantic Models
Semantic models are the foundation of MetricFlow - they define:
- **Entities** - Join keys and relationships between models
- **Dimensions** - Qualitative attributes for grouping and filtering
- **Measures** - Quantitative aggregations that become metrics
- **Primary time dimension** - Required for time-based analysis

### Metric Types
The Semantic Layer supports multiple metric types:
- **Simple metrics** - Direct aggregations of measures
- **Ratio metrics** - Numerator divided by denominator  
- **Cumulative metrics** - Running totals over time windows
- **Derived metrics** - Mathematical expressions combining other metrics
- **Conversion metrics** - Funnel analysis and conversion rates

### MetricFlow Components
- **Time spine** - Date/time dimension table required for time-based metrics
- **Join logic** - How semantic models connect via entities
- **Grain** - Level of aggregation for metrics
- **Filters** - Where clauses applied to measures or dimensions

## Local Development Workflow

### Installation & Setup

```bash
# Install MetricFlow with adapter
pip install "dbt-metricflow[snowflake]"  # Or: bigquery, redshift, databricks

# Configure shell for template wrappers (zsh)
echo "setopt BRACECCL" >> ~/.zshrc
source ~/.zshrc

# Or use automated script
bash scripts/setup_shell_config.sh
```

**See:** [Local Development Guide](references/guide_local_development.md)

### 5-Step Development Loop

1. **EDIT** - Modify semantic models or metrics
2. **PARSE** - Run `dbt parse` to validate YAML
3. **VALIDATE** - Run `mf validate-configs` to check semantic graph
4. **QUERY** - Test with `mf query --metrics <metric>`
5. **ITERATE** - Refine and repeat

**See:** [Validation Workflow](references/guide_validation_workflow.md)

### CLI Quick Commands

```bash
# List metrics
mf list metrics

# List dimensions for a metric
mf list dimensions --metrics total_revenue

# Query metric
mf query --metrics total_revenue

# Query with time dimension
mf query --metrics total_revenue --group-by metric_time__day --limit 10

# Query with filter (note: quoted!)
mf query --metrics total_revenue \
  --where "{{ Dimension('order__status') }} == 'completed'"

# Compile without executing
mf query --metrics total_revenue --compile
```

**See:** [CLI Commands Complete](references/cli_commands_complete.md) | [Query Syntax Guide](references/guide_query_syntax.md)

### Template Wrapper Syntax

MetricFlow uses special syntax for filters:

```bash
# Dimension filter
--where "{{ Dimension('entity__dimension_name') }} == 'value'"

# Time dimension filter
--where "{{ TimeDimension('entity__time_dim', 'day') }} >= '2024-01-01'"

# Combined filters
--where "{{ Dimension('customer__segment') }} == 'enterprise' AND {{ TimeDimension('order__order_date', 'day') }} >= '2024-01-01'"
```

**Important:** Always quote the entire `--where` clause to prevent shell interpretation errors.

**See:** [Query Syntax Guide](references/guide_query_syntax.md)

## Quick Reference

### Common Semantic Model Pattern

<example>
```yaml
semantic_models:
  - name: orders
    description: Order fact table
    model: ref('fct_orders')

    entities:
      - name: order_id
        type: primary
      - name: customer_id
        type: foreign

    dimensions:
      - name: order_date
        type: time
        type_params:
          time_granularity: day
      - name: order_status
        type: categorical

    measures:
      - name: order_total
        agg: sum
      - name: order_count
        agg: count
        expr: order_id
```
</example>

### Common Metric Patterns

<example>
```yaml
metrics:
  # Simple metric
  - name: total_revenue
    description: Sum of all order totals
    type: simple
    label: Total Revenue
    type_params:
      measure: order_total

  # Ratio metric
  - name: average_order_value
    description: Revenue per order
    type: ratio
    label: Average Order Value
    type_params:
      numerator: total_revenue
      denominator: order_count

  # Cumulative metric
  - name: cumulative_revenue
    description: Running total of revenue
    type: cumulative
    label: Cumulative Revenue
    type_params:
      measure: order_total
```
</example>

### ✅ Metric Verification Checklist

**After creating any metric, verify the following before querying:**

1. **Measure Existence** - Does the referenced measure exist in the semantic model?
   - For simple/cumulative: Check `type_params.measure` exists in semantic model
   - For ratio: Check both numerator and denominator measures/metrics exist

2. **Filter Validity** - If using filters, do the referenced dimensions exist?
   - Verify dimension names match semantic model definitions
   - Check entity qualification (e.g., `order__status` not just `status`)

3. **Time Spine Configuration** - For time-based metrics:
   - Confirm time spine model exists and is configured in `dbt_project.yml`
   - Verify `join_to_timespine: true` if needed for cumulative metrics

4. **Metric Dependencies** - For ratio/derived metrics:
   - Confirm all referenced metrics are defined
   - Check for circular dependencies

5. **Test Query** - Run a simple query to validate:
   ```bash
   mf query --metrics <your_metric> --limit 5
   ```

### MetricFlow Time Spine Setup

<example>
```sql
-- models/metricflow_time_spine.sql
{{ config(
    materialized='table'
) }}

with days as (
    {{ dbt.date_spine(
        datepart="day",
        start_date="cast('2020-01-01' as date)",
        end_date="cast('2030-12-31' as date)"
    ) }}
),

final as (
    select cast(date_day as date) as date_day
    from days
)

select * from final
```
</example>

### Python SDK Query Example

<example>
```python
from dbtsl import SemanticLayerClient

client = SemanticLayerClient(
    environment_id=123,
    auth_token="your-token",
    host="semantic-layer.cloud.getdbt.com"
)

with client.session():
    # Query a metric
    table = client.query(
        metrics=["total_revenue", "order_count"],
        group_by=["metric_time", "order_status"],
        order_by=["metric_time"]
    )
    print(table)
```
</example>

## Reference Files

This skill includes comprehensive documentation organized by topic:

### 🚀 **Getting Started Guides** (NEW)

**[Local Development Guide](references/guide_local_development.md)**
- Installation and environment setup
- Shell configuration for template wrappers
- 5-step development workflow
- Troubleshooting local issues

**[Validation Workflow](references/guide_validation_workflow.md)**
- 3-layer validation architecture (Parse → Semantic → Data Platform)
- CI/CD integration patterns
- Common validation errors and fixes
- Testing strategies

**[Query Syntax Guide](references/guide_query_syntax.md)**
- Template wrapper syntax (Dimension, TimeDimension)
- Entity qualification patterns
- Time granularity options
- Advanced query patterns

**[CLI Commands Complete](references/cli_commands_complete.md)**
- Full command reference (list, query, validate)
- All flags and options
- Examples for every command
- Troubleshooting tips

### 📊 Additional References

**[Metrics Reference](references/metrics.md)**
- Defining metrics in YAML
- Metric types and patterns
- Python SDK usage examples
- Query API reference

**[API Reference](references/api_reference.md)**
- dbt Semantic Layer API
- Python SDK (sync and async)
- GraphQL queries
- JDBC connections
- Lazy loading optimization

**[Additional Guides](references/)**
- BI tool integrations
- Enterprise patterns
- Iterative migration strategies
- Naming conventions

## Key Features

### ✅ Validation Types
The Semantic Layer performs three types of validation:
1. **Parsing Validation** - YAML syntax and structure
2. **Semantic Validation** - Logic and relationships
3. **Data Warehouse Validation** - Query execution

### 🔍 Best Practices
- Keep semantic models normalized for MetricFlow flexibility
- Define one primary entity per semantic model
- Use consistent grain across related semantic models
- Leverage saved queries for common metric combinations
- Implement proper time spine for time-based metrics
- Use lazy loading for large metadata in Python SDK

### 🔌 Supported Integrations
- **BI Tools**: Tableau, Power BI, Looker, Mode, Hex, Google Sheets
- **APIs**: GraphQL, REST API, JDBC, ODBC
- **Languages**: Python SDK (sync/async), SQL
- **Notebooks**: Jupyter, Hex, Deepnote

## Working with This Skill

### For Beginners
1. **Start here:** [Local Development Guide](references/guide_local_development.md) - Set up environment
2. **Then:** Review common semantic model patterns (Quick Reference section above)
3. **Practice:** Follow 5-step development loop with simple metric
4. **Explore:** `examples.md` for complete real-world patterns

### For Local Development
- **Installation** → [Local Development Guide](references/guide_local_development.md)
- **CLI commands** → [CLI Commands Complete](references/cli_commands_complete.md)
- **Query syntax** → [Query Syntax Guide](references/guide_query_syntax.md)
- **Validation** → [Validation Workflow](references/guide_validation_workflow.md)

### For Specific Features
- **Building semantic models** → See semantic model pattern above + llms-full.md
- **Metric definitions** → metrics.md + examples.md
- **API integration** → api_reference.md
- **Time-based analysis** → MetricFlow time spine section

### For Debugging

**When debugging validation errors, think step by step through the 3-layer validation architecture:**

1. **PARSE Layer** - Is the YAML syntactically correct?
   - Check indentation, quotes, special characters
   - Run `dbt parse` to validate structure
   - Look for: "Compilation Error", "YAML syntax error"

2. **SEMANTIC Layer** - Is the logic valid?
   - Check measure/dimension/entity references
   - Verify join paths and entity relationships
   - Run `mf validate-configs` to check semantic graph
   - Look for: "Measure not found", "Unknown dimension", "No join path"

3. **DATA PLATFORM Layer** - Can the query execute?
   - Check SQL compilation and warehouse execution
   - Verify table/column existence
   - Run `mf query --compile` to see generated SQL
   - Look for: "Column does not exist", "Table not found"

**Debugging Resources:**
1. **Local errors** → [Local Development Guide - Troubleshooting](references/guide_local_development.md)
2. **Validation errors** → [Validation Workflow](references/guide_validation_workflow.md)
3. **Query syntax errors** → [Query Syntax Guide - Troubleshooting](references/guide_query_syntax.md)

## Common Patterns

### Metric with Filter
<example>
```yaml
metrics:
  - name: completed_order_revenue
    type: simple
    type_params:
      measure: order_total
    filter: |
      {{ Dimension('order_id__order_status') }} = 'completed'
```
</example>

### Multi-Entity Join
<example>
```yaml
entities:
  - name: order_id
    type: primary
  - name: customer_id
    type: foreign
    expr: customer_fk
  - name: product_id
    type: foreign
```
</example>

### Saved Query
<example>
```yaml
saved_queries:
  - name: monthly_revenue_by_region
    description: Monthly revenue broken down by region
    query_params:
      metrics:
        - total_revenue
        - order_count
      group_by:
        - TimeDimension('order_date', 'month')
        - Dimension('customer__region')
```
</example>

## Resources

### Documentation Files
- `references/` - Organized documentation by category (see Reference Files section above)
- `scripts/` - Helper scripts for common tasks:
  - `setup_shell_config.sh` - Configure shell for template wrappers

### External Links
- [dbt Semantic Layer Docs](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl)
- [MetricFlow Documentation](https://docs.getdbt.com/docs/build/about-metricflow)
- [Python SDK Repository](https://github.com/dbt-labs/semantic-layer-sdk-python)

## Test Scenarios

Use these scenarios to validate the skill's effectiveness:

### Test 1: Create Simple Revenue Metric
**Task:** Create a simple metric that sums order totals
**Expected Behavior:**
- Verify measure exists in semantic model before creating metric
- Use verification checklist to validate configuration
- Successfully query the metric with `mf query --metrics total_revenue --limit 5`

### Test 2: Build Ratio Metric with Filter
**Task:** Create average order value metric, filtered to completed orders only
**Expected Behavior:**
- Verify both numerator and denominator metrics/measures exist
- Check filter dimension exists and uses proper entity qualification
- Test query returns expected results

### Test 3: Debug "Measure Not Found" Error
**Task:** Encounter and resolve a validation error for missing measure
**Expected Behavior:**
- Apply 3-layer debugging (Parse → Semantic → Data Platform)
- Identify error at Semantic layer
- Read semantic model YAML to verify measure definition
- Fix metric configuration and validate

### Test 4: Configure Time Spine
**Task:** Set up time spine for cumulative metrics
**Expected Behavior:**
- Create time spine model using dbt.date_spine macro
- Configure in dbt_project.yml
- Verify cumulative metric can join to time spine
- Query cumulative metric grouped by time

## Updating This Skill

To refresh with latest dbt documentation:
```bash
cd ~/git-repos/Skill_Seekers
source venv/bin/activate
python3 cli/doc_scraper.py --config configs/skill_seeker_config_dbt_semantic.json
```

## Notes

- **Source**: Official dbt documentation (docs.getdbt.com)
- **Last Updated**: 2025-11-04
- **Total Pages**: 204 documentation pages extracted
- **Size**: ~9.6 MB of comprehensive documentation
- **Format**: Markdown with code examples and language detection
- **Coverage**: Semantic Layer, MetricFlow, all metric types, integrations, API reference

---

*This skill was automatically generated using Skill Seekers and optimized for dbt Semantic Layer development.*
