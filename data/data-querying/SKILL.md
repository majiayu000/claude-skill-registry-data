---
name: data-querying
description: Write and verify SQL queries with BigQuery. Use when executing bq commands, writing SQL queries, or including query results in documents.
---

# Data Querying

## Verification Requirement

All queries MUST be executed with `bq` and verified before inclusion. Never include unverified queries or fabricated data.

## Query Process

1. **Dry run**: Validate syntax and check cost

   ```bash
   bq query --project_id=<PROJECT_ID> --use_legacy_sql=false --dry_run "SELECT ..."
   ```

   Cost: ~$5/TB. <1GB is light, 2GB+ needs optimization.

2. **Execute**: Run and confirm results

   ```bash
   bq query --project_id=<PROJECT_ID> --use_legacy_sql=false --format=csv "SELECT ..."
   ```

3. **Learn**: Study existing queries in project docs for patterns.

## Query Design

- Specify exact date ranges
- Filter partitioned tables by partition key
- Avoid correlated subqueries (use JOINs/CTEs)
- Filter early with CTEs before joining large tables

## Documentation

1. Execute exact query with `bq`
2. Copy real output only
3. State time period and what query measures
