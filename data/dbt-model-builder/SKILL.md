---
name: dbt-model-builder
description: Create dbt models following FF Analytics Kimball patterns and 2×2 stat model. This skill should be used when creating staging models, core facts/dimensions, or analytical marts. Guides through model creation with proper grain, tests, External Parquet configuration, and per-model YAML documentation using dbt 1.10+ syntax.
---

# dbt Model Builder

Create complete dbt models for the Fantasy Football Analytics project following Kimball dimensional modeling and the 2×2 stat model (actuals/projections × real-world/fantasy).

## When to Use This Skill

Use this skill proactively when:

- Creating new dbt models (staging, core, marts)
- User asks to "create a model for {entity/process}"
- User mentions dbt modeling, dimensional modeling, or Kimball patterns
- Adding analytics-ready views or transformations
- Implementing 2×2 model quadrants (actuals/projections, real-world/fantasy scoring)

## dbt Modeling Approach

The FF Analytics project follows:

1. **Kimball Dimensional Modeling** - Facts, dimensions, conformed entities
2. **2×2 Stat Model** - Separate facts for actuals vs projections
3. **Per-Model YAML** - One `_<model>.yml` file per model
4. **External Parquet** - Large models use external=true with partitioning
5. **dbt 1.10+ syntax** - Test arguments wrapped in `arguments:` block

## Model Building Workflows

### Workflow 1: Create Staging Model

Staging models normalize raw provider data.

**Steps:**

1. **Identify source**: Determine provider and dataset
2. **Design grain**: Define one row per...
3. **Create SQL** using `assets/staging_template.sql`:
   - Name: `stg_{provider}__{dataset}.sql`
   - Materialize as view
   - Select from `{{ source('{provider}', '{dataset}') }}`
   - Rename columns to standard names
4. **Create YAML** using `assets/staging_yaml_template.yml`:
   - Name: `_stg_{provider}__{dataset}.yml`
   - Document grain and source
   - Add not_null, unique tests for PKs
   - Add accepted_values for enums
5. **Run and test**:

   ```bash
   make dbt-run --select stg_{provider}__{dataset}
   make dbt-test --select stg_{provider}__{dataset}
   ```

### Workflow 2: Create Fact Table

Fact tables capture measurable events/processes.

**Steps:**

1. **Design grain**: Define composite primary key (e.g., player_id + game_id + stat_name)
2. **Map foreign keys**: Join to conformed dimensions (`dim_player`, `dim_team`, etc.)
3. **Create SQL** using `assets/fact_template.sql`:
   - Name: `fact_{process}.sql`
   - Config: `materialized='table', external=true, partition_by=['season','week']`
   - Join staging to dimensions for FK resolution
   - Select grain keys + measures
4. **Create YAML** using `assets/fact_yaml_template.yml`:
   - Document grain explicitly
   - Add `dbt_utils.unique_combination_of_columns` for grain test
   - Add relationship tests for all FKs
   - Add not_null for required measures
5. **Run and test**:

   ```bash
   make dbt-run --select fact_{process}
   make dbt-test --select fact_{process}
   ```

**Critical**: Fact tables MUST have grain uniqueness test with dbt 1.10+ syntax:

```yaml
data_tests:
  - dbt_utils.unique_combination_of_columns:
      arguments:
        combination_of_columns:
          - column1
          - column2
      config:
        severity: error
```

### Workflow 3: Create Dimension Table

Dimensions provide descriptive context for facts.

**Steps:**

1. **Determine SCD type**: Type 1 (replace) or Type 2 (historical tracking)
2. **Design natural key**: Business key for the entity
3. **Create SQL** using `assets/dim_template.sql`:
   - Name: `dim_{entity}.sql`
   - Generate surrogate key with `dbt_utils.generate_surrogate_key()`
   - For SCD Type 2: Add valid_from, valid_to, is_current
4. **Create YAML**:
   - Document grain: "one row per {entity}"
   - Add unique test on surrogate key
   - Add not_null on natural key
5. **Run and test**

**SCD Type 2 pattern**:

- Track changes over time with validity dates
- Include version_number for multiple versions
- Set is_current flag for latest version

### Workflow 4: Create Analytical Mart (2×2 Model)

Marts provide wide-format, analytics-ready data.

**2×2 Model Quadrants:**

- `mart_real_world_actuals` - NFL stats (actuals)
- `mart_real_world_projections` - Projected NFL stats
- `mart_fantasy_actuals` - Fantasy points (actuals, apply scoring rules)
- `mart_fantasy_projections` - Projected fantasy points

**Steps:**

1. **Select quadrant**: Determine actuals vs projections, real-world vs fantasy
2. **Pivot fact table**: Convert long-form stats to wide columns
3. **Join dimensions**: Enrich with descriptive attributes
4. **Apply scoring** (fantasy quadrants only):
   - Join `dim_scoring_rule`
   - Calculate points: `{stat} * {points_per_stat}`
5. **Create SQL** using `assets/mart_template.sql`:
   - Partition by season
   - Wide format with one column per stat
6. **Run and test**

**Example pivot**:

```sql
SUM(CASE WHEN stat_name = 'passing_yards' THEN stat_value END) AS passing_yards,
SUM(CASE WHEN stat_name = 'passing_tds' THEN stat_value END) AS passing_tds
```

## Resources Provided

### references/

Real models from the codebase:

- **example_staging_model.sql** - stg_ktc_assets
- **example_staging_yaml.yml** - YAML with tests
- **example_fact_model.sql** - Fact table example
- **example_dim_model.sql** - Dimension example
- **example_mart_model.sql** - Mart example

### assets/

Templates for creating models:

- **staging_template.sql** - Staging model SQL
- **staging_yaml_template.yml** - Staging YAML with tests
- **fact_template.sql** - Fact table SQL with FK joins
- **fact_yaml_template.yml** - Fact YAML with grain test
- **dim_template.sql** - Dimension SQL with SCD Type 2
- **mart_template.sql** - Mart SQL with pivot pattern

## Best Practices

### Grain Declaration

**CRITICAL**: Every model must explicitly declare grain:

- In SQL comments: `-- Grain: one row per...`
- In YAML description
- In grain uniqueness test (facts)

### Testing Strategy

**Staging models**:

- not_null on all PKs
- unique on single-column PKs
- accepted_values on enums

**Fact tables**:

- dbt_utils.unique_combination_of_columns (grain test)
- relationships to all dimensions
- not_null on FKs and measures

**Dimensions**:

- unique on surrogate key
- not_null on natural key

### dbt 1.10+ Test Syntax

**CRITICAL**: Follow these two rules to avoid deprecation warnings:

1. **Use `data_tests:` key** (not `tests:`): dbt 1.5+ introduced `data_tests:` to distinguish from `unit_tests:`
2. **Wrap test parameters in `arguments:`**: dbt 1.10+ requires this for all generic tests with parameters

```yaml
# CORRECT - Column-level tests
columns:
  - name: position
    data_tests:  # Use data_tests:, not tests:
      - not_null
      - accepted_values:
          arguments:  # Arguments must be nested
            values: ['QB', 'RB', 'WR', 'TE']

  - name: player_id
    data_tests:
      - not_null
      - relationships:
          arguments:  # Wrap to, field in arguments:
            to: ref('dim_player')
            field: player_id
          config:  # config: is sibling to arguments:
            where: "player_id > 0"

# CORRECT - Model-level tests
data_tests:  # Use data_tests:, not tests:
  - dbt_utils.unique_combination_of_columns:
      arguments:
        combination_of_columns:
          - player_key
          - game_id

# WRONG - Deprecated syntax (will cause warnings)
columns:
  - name: position
    tests:  # WRONG - should be data_tests:
      - accepted_values:
          values: ['QB', 'RB']  # WRONG - should be under arguments:

tests:  # WRONG - should be data_tests:
  - relationships:
      to: ref('dim_player')  # WRONG - should be under arguments:
      field: player_id
```

**Key Points:**

- Always use `data_tests:` (not `tests:`)
- `arguments:` wraps test parameters (to, field, values, combination_of_columns)
- `config:` is a sibling to `arguments:`, not nested inside
- `not_null` and `unique` have no arguments, use directly

### External Parquet Configuration

Large models use External Parquet:

```sql
{{ config(
    materialized='table',
    external=true,
    partition_by=['season', 'week']
) }}
```

### Naming Conventions

- Staging: `stg_{provider}__{dataset}`
- Facts: `fact_{process}` (e.g., `fact_player_stats`)
- Dimensions: `dim_{entity}` (e.g., `dim_player`)
- Marts: `mart_{purpose}` (e.g., `mart_fantasy_actuals_weekly`)
- YAML: `_<model_name>.yml`

## Integration with Other Skills

- **data-ingestion-builder** - Create staging models after adding providers
- **data-quality-test-generator** - Enhance testing beyond basics
