---
name: data-quality-test-generator
description: Generate comprehensive dbt test suites following FF Analytics data quality standards and dbt 1.10+ syntax. This skill should be used when creating tests for new dbt models, adding tests to existing models, standardizing test coverage, or implementing data quality gates. Covers grain uniqueness, FK relationships, enum validation, and freshness tests.
---

# Data Quality Test Generator

Generate comprehensive dbt test suites for Fantasy Football Analytics models following Kimball patterns, implementation requirements, and dbt 1.10+ syntax.

## When to Use This Skill

Use this skill proactively when:

- Creating tests for new dbt models (staging, facts, dimensions, marts)
- User asks to "add tests for {model}" or "improve test coverage"
- Implementing data quality gates per implementation requirements
- Standardizing existing tests to dbt 1.10+ syntax
- Creating tests alongside models (integration with dbt-model-builder skill)

## dbt 1.10+ Syntax Requirements

**CRITICAL**: FF Analytics uses dbt 1.10+ which requires the new syntax:

- Use `data_tests:` not `tests:`
- Wrap test arguments in `arguments:` block
- Use `config:` for test configuration (severity, where clauses)

### Correct vs Incorrect Syntax

**✅ CORRECT (dbt 1.10+):**

```yaml
data_tests:
  - accepted_values:
      arguments:
        values: ['value1', 'value2']
      config:
        severity: error
```

**❌ INCORRECT (old syntax):**

```yaml
tests:
  - accepted_values:
      values: ['value1', 'value2']
      severity: error
```

## Test Generation by Model Type

### Task 1: Staging Model Tests

Staging models normalize raw provider data and require schema conformance tests.

**Test Priorities:**

1. **not_null** on all primary key columns
2. **unique** on single-column natural keys
3. **accepted_values** on categorical/enum columns
4. Basic data type validation

**Example Pattern:**

```yaml
version: 2

models:
  - name: stg_nflverse__weekly
    description: "NFLverse weekly player stats"

    columns:
      - name: player_id
        description: "gsis_id from nflverse"
        data_tests:
          - not_null

      - name: season
        data_tests:
          - not_null
          - dbt_utils.expression_is_true:
              arguments:
                expression: ">= 2020"  # Reasonable season bounds

      - name: week
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

      - name: position
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']
```

**See**: `references/example_staging_tests.yml`

### Task 2: Fact Table Tests

Fact tables capture measurable events and require grain + FK + measure validation.

**Test Priorities:**

1. **Grain uniqueness** using `dbt_utils.unique_combination_of_columns`
2. **Relationship tests** for all foreign keys to dimensions
3. **not_null** on required measures
4. **accepted_values** on 2×2 model enums (measure_domain, stat_kind, horizon)
5. **Expression tests** for business logic (non-negative scores, etc.)

**Example Pattern:**

```yaml
version: 2

models:
  - name: fact_player_stats
    description: "Player statistics fact table (grain: player + game + stat)"

    # Grain uniqueness test
    data_tests:
      - dbt_utils.unique_combination_of_columns:
          arguments:
            combination_of_columns:
              - player_id
              - game_id
              - stat_name
              - measure_domain
              - stat_kind
          config:
            severity: error

    columns:
      # Foreign key to dim_player
      - name: player_id
        description: "Foreign key to dim_player (mfl_id)"
        data_tests:
          - not_null
          - relationships:
              arguments:
                to: ref('dim_player')
                field: player_id

      # Foreign key to dim_game
      - name: game_id
        description: "Foreign key to dim_game"
        data_tests:
          - not_null
          - relationships:
              arguments:
                to: ref('dim_game')
                field: game_id

      # 2x2 model enum: measure_domain
      - name: measure_domain
        description: "Real-world vs fantasy scoring dimension"
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['real_world', 'fantasy']

      # 2x2 model enum: stat_kind
      - name: stat_kind
        description: "Actuals vs projections dimension"
        data_tests:
          - not_null
          - accepted_values:
              arguments:
                values: ['actual', 'projection']

      # Measure validation
      - name: stat_value
        description: "Value of the statistical measure"
        data_tests:
          - not_null
```

**See**: `references/example_fact_tests.yml`

### Task 3: Dimension Table Tests

Dimensions provide descriptive context and require uniqueness + SCD validation.

**Test Priorities:**

1. **unique** + **not_null** on surrogate key (dimension PK)
2. **not_null** on natural key columns
3. **SCD Type 2 tests** (if applicable):
   - `valid_from <= valid_to` (or valid_to IS NULL for current)
   - No overlapping date ranges for same natural key
4. **accepted_values** on categorical attributes

**Example Pattern:**

```yaml
version: 2

models:
  - name: dim_player
    description: "Player dimension with SCD Type 2 history"

    columns:
      # Surrogate key
      - name: player_sk
        description: "Surrogate key for SCD Type 2"
        data_tests:
          - unique
          - not_null

      # Natural key
      - name: player_id
        description: "Natural key (mfl_id canonical)"
        data_tests:
          - not_null

      # SCD Type 2 validity
      - name: valid_from
        description: "Start of validity period"
        data_tests:
          - not_null

      - name: valid_to
        description: "End of validity period (NULL = current)"

      # SCD Type 2 date logic test
      - name: _scd_validation
        description: "Ensure valid_from <= valid_to when valid_to is not null"
        data_tests:
          - dbt_utils.expression_is_true:
              arguments:
                expression: "valid_from <= COALESCE(valid_to, CURRENT_DATE + INTERVAL '100 years')"

      # Categorical attributes
      - name: position
        description: "Player position"
        data_tests:
          - accepted_values:
              arguments:
                values: ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']

      - name: status
        description: "Active/Inactive/Retired"
        data_tests:
          - accepted_values:
              arguments:
                values: ['active', 'inactive', 'retired', 'unknown']
```

**See**: `references/example_dimension_tests.yml`

### Task 4: Mart Tests

Marts are analytics-ready views requiring business logic validation.

**Test Priorities:**

1. **Row count thresholds** (dbt_utils.expression_is_true on table)
2. **Metric validation** (non-negative fantasy points, reasonable ranges)
3. **Partition completeness** (all weeks/seasons represented)
4. **Aggregate consistency** (totals match source facts)

**Example Pattern:**

```yaml
version: 2

models:
  - name: mart_fantasy_actuals_weekly
    description: "Weekly fantasy points by player (analytics-ready)"

    data_tests:
      # Minimum row count threshold
      - dbt_utils.expression_is_true:
          arguments:
            expression: "(SELECT COUNT(*) FROM {{ ref('mart_fantasy_actuals_weekly') }}) > 10000"
          config:
            severity: warn

    columns:
      - name: player_name
        data_tests:
          - not_null

      - name: fantasy_points
        description: "Total fantasy points for the week"
        data_tests:
          - not_null
          - dbt_utils.expression_is_true:
              arguments:
                expression: ">= 0"  # Fantasy points can't be negative

      - name: games_played
        data_tests:
          - accepted_values:
              arguments:
                values: [0, 1]  # Weekly grain, max 1 game per week
```

### Task 5: Source Freshness Tests

Implement freshness monitoring for critical data sources.

**Example Freshness Policies** (always check latest documentation for the most up to date policies)

- **NFLverse**: warn_after 24h, error_after 48h (during season)
- **Commissioner Sheets**: warn_after 12h, error_after 24h
- **KTC**: warn_after 48h, error_after 96h (less time-sensitive)

**Example Pattern:**

```yaml
version: 2

sources:
  - name: nflverse
    description: "NFLverse data provider"
    freshness:
      warn_after: {count: 24, period: hour}
      error_after: {count: 48, period: hour}

    tables:
      - name: weekly
        description: "Weekly player statistics"
        identifier: "dt=*/**"  # Partitioned by date

        # Freshness test on max snapshot_date
        freshness:
          warn_after: {count: 24, period: hour}
          error_after: {count: 48, period: hour}
```

## Data Quality Requirements

The following tests are **required** in general:

1. **Accepted values on enums** - All categorical columns must have accepted_values tests
2. **Freshness tests** - All source tables must have warn/error thresholds
3. **Grain uniqueness** - All fact tables must test grain with unique_combination_of_columns
4. **FK relationships** - All foreign keys must have relationship tests to dimensions

## Best Practices

### Test Coverage Targets

- **Staging models**: >80% column coverage (focus on PKs and enums)
- **Fact tables**: 100% grain + FK coverage
- **Dimensions**: 100% PK/NK coverage
- **Marts**: Business logic validation (thresholds, non-negative, etc.)

### Test Naming

Tests are auto-named by dbt. For custom tests, use descriptive names:

```yaml
- name: _custom_business_rule
  description: "Validate that revenue >= cost for all transactions"
```

### Severity Levels

- **error**: Blocking failures (grain violations, missing FKs)
- **warn**: Non-blocking issues (freshness delays, low row counts)

```yaml
config:
  severity: warn  # Use for non-critical tests
```

### Where Clauses

Use `where` clauses to filter test scope:

```yaml
data_tests:
  - relationships:
      arguments:
        to: ref('dim_player')
        field: player_id
      config:
        where: "player_id IS NOT NULL AND season >= 2020"
```

## Integration with Other Skills

- **dbt-model-builder**: Create tests alongside model creation

## Resources

### assets/

- `test_suite_template.yml` - Base template with dbt 1.10+ syntax for common test patterns

### references/

- `example_fact_tests.yml` - Complete fact table test suite (fact_player_projections)
- `example_staging_tests.yml` - Staging model test patterns
- `example_dimension_tests.yml` - Dimension table test patterns with SCD Type 2 validation

## Common Test Patterns

### Testing 2×2 Model Enums

The 2×2 stat model uses consistent enums across all facts:

```yaml
# measure_domain: real_world vs fantasy
- name: measure_domain
  data_tests:
    - accepted_values:
        arguments:
          values: ['real_world', 'fantasy']

# stat_kind: actual vs projection
- name: stat_kind
  data_tests:
    - accepted_values:
        arguments:
          values: ['actual', 'projection']

# horizon: projection timeframe (only for stat_kind='projection')
- name: horizon
  data_tests:
    - accepted_values:
        arguments:
          values: ['weekly', 'full_season', 'rest_of_season']
      config:
        where: "stat_kind = 'projection'"
```

### Testing Date Ranges

```yaml
- name: game_date
  data_tests:
    - dbt_utils.expression_is_true:
        arguments:
          expression: ">= '2020-01-01'"  # Reasonable lower bound
    - dbt_utils.expression_is_true:
        arguments:
          expression: "<= CURRENT_DATE + INTERVAL '1 year'"  # No future dates beyond 1 year
```

### Testing Aggregations

```yaml
# Ensure weekly totals match season totals
- name: _season_total_consistency
  data_tests:
    - dbt_utils.expression_is_true:
        arguments:
          expression: |
            (
              SELECT SUM(weekly_points)
              FROM {{ ref('mart_weekly_points') }}
              WHERE season = 2024
            ) = (
              SELECT season_total
              FROM {{ ref('mart_season_totals') }}
              WHERE season = 2024
            )
```
