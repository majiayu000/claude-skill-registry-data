---
name: soda-checks
description: "Authors and runs SodaCL (Soda Checks Language) checks against SQL warehouses (Snowflake, BigQuery, Postgres, Redshift, etc.) via `soda scan`, configures scan profiles in configuration.yml, and gates CI on scan exit code. Use when the user works with Soda Core / Soda Cloud or needs YAML-driven warehouse data quality."
---

# soda-checks

## Overview

SodaCL (Soda Checks Language) is a YAML-based domain-specific language for
data reliability. A typical Soda project ships two YAML files - 
`configuration.yml` (data source connection) and `checks.yml` (assertions) - and runs them through the `soda scan` CLI ([sodacl-overview][1],
[sodacl-quickstart][2]).

[1]: https://docs.soda.io/soda-v3/soda-cl-overview.md
[2]: https://docs.soda.io/soda-v3/soda-cl-overview/quick-start-sodacl.md

This skill covers SodaCL authoring, scan configuration, running, and CI
integration. Use it when you want **YAML-only assertions on warehouse
tables** without writing Python (in contrast to Great Expectations, which
is Python-first) or compiling a dbt project.

## When to use

- The repo has `configuration.yml` + `checks.yml` (the canonical Soda
  filenames per [sodacl-quickstart][2]).
- The user asks about `checks for <table>:`, `missing_count`,
  `duplicate_count`, `freshness`, or `invalid_count` - SodaCL check types
  per [sodacl-overview][1].
- A pipeline needs warehouse-side data quality with no programmatic
  glue: SQL warehouses (Snowflake, BigQuery, Postgres, Redshift) are
  first-class data sources.
- A team uses Soda Cloud for cross-team observability of scan results.

## Authoring checks

### File shape

`checks.yml` is a list of `checks for <dataset>:` blocks. Each block lists
assertions in SodaCL syntax ([sodacl-overview][1]):

```yaml
# checks.yml
checks for orders:
  - row_count between 1 and 10000000
  - missing_count(order_id) = 0
  - duplicate_count(order_id) = 0
  - invalid_percent(email) < 1 %:
      valid format: email
  - freshness(updated_at) < 1d

checks for customers:
  - row_count > 0
  - missing_count(customer_id) = 0
  - schema:
      warn:
        when required column missing: [created_at]
      fail:
        when forbidden column present: [pii_ssn, pii_dob]
```

### Common check types

The check vocabulary in SodaCL ([sodacl-overview][1]):

| Check               | Example                                          |
|---------------------|--------------------------------------------------|
| `row_count`         | `row_count between 10 and 1000`                  |
| `missing_count(c)`  | `missing_count(birth_date) = 0`                  |
| `missing_percent(c)`| `missing_percent(email) < 1 %`                   |
| `duplicate_count(c)`| `duplicate_count(phone) = 0`                     |
| `invalid_count(c)`  | `invalid_count(phone) = 0` (with `valid format`) |
| `freshness(col)`    | `freshness(start_date) < 1d`                     |
| Aggregates          | `avg(safety_stock_level) > 50`                   |
| `schema`            | required / forbidden columns (warn/fail blocks)  |

### Thresholds and severity

Thresholds use comparison operators inline with the check
(`< 1%`, `between 10 and 1000`, `= 0`). The `schema` check supports
explicit `warn:` and `fail:` alert configurations to differentiate
severity ([sodacl-overview][1]):

```yaml
checks for transactions:
  - schema:
      warn:
        when required column missing: [updated_at]
      fail:
        when forbidden column present: [pii*]
```

For non-schema checks, alert configurations apply via the
`alert configurations:` syntax - see Soda's optional-config docs at
https://docs.soda.io/soda-v3/sodacl-reference/optional-config.md for
the full grammar.

## Configuration

`configuration.yml` defines one or more data sources and (optionally)
Soda Cloud credentials. Use environment-variable substitution for
secrets - Soda expands `${ ENV_VAR }` at scan time
([quick-start-dev][3]):

[3]: https://docs.soda.io/soda-v3/use-case-guides/quick-start-dev.md

```yaml
# configuration.yml
data_source warehouse:
  type: snowflake
  username: ${ SNOWFLAKE_USER }
  password: ${ SNOWFLAKE_PASS }
  account: ${ SNOWFLAKE_ACCOUNT }
  database: analytics
  warehouse: compute_wh
  role: analyst
  schema: public

soda_cloud:
  host: cloud.us.soda.io
  api_key_id: ${ SODA_CLOUD_API_KEY }
  api_key_secret: ${ SODA_CLOUD_API_SECRET }
```

The `soda_cloud:` block is optional - omit it for a fully local scan.

## Running

Canonical CLI invocation ([sodacl-quickstart][2]):

```bash
soda scan -d warehouse -c configuration.yml checks.yml
```

Where:

- `-d warehouse` matches the `data_source <name>:` key in
  `configuration.yml`.
- `-c configuration.yml` points at the connection file.
- The trailing positional argument is the checks file (you can pass
  multiple).

Multiple checks files run in one scan:

```bash
soda scan -d warehouse -c configuration.yml \
  checks/orders.yml checks/customers.yml checks/transactions.yml
```

Each scan produces a checks pass/fail summary in stdout and (when
`soda_cloud:` is configured) reports to Soda Cloud.

## Parsing scan results

A failing scan exits non-zero and prints a per-check pass/fail line. For
machine consumption, the [Soda GitHub Action][4] converts scan results to
a markdown table and posts the findings as a PR comment
([quick-start-dev][3]). For other CI systems, parse stdout with the
filtering snippet below.

[4]: https://docs.soda.io/soda-v3/integrate-soda/integrate-github.md

```bash
# Capture and filter the scan output
soda scan -d warehouse -c configuration.yml checks.yml | tee scan.log

# Surface failing checks for the PR comment / job summary
grep -E '^\s*FAIL' scan.log || echo "All checks passed"
```

> **Note:** if your team needs structured (JSON) scan output for richer
> downstream reporting, check the current `soda scan` flag set on
> https://docs.soda.io/ - flag availability evolves between major Soda
> Library / Soda Core versions.

## CI integration

The minimal pattern is: install the Soda library + warehouse adapter,
run `soda scan`, exit non-zero on failure, upload the scan log as an
artifact.

```yaml
# .github/workflows/soda-scan.yml
name: soda

on:
  pull_request:
  push:
    branches: [main]

jobs:
  soda-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Soda + adapter
        # Pin versions; Soda Library has both a free OSS and commercial track.
        run: pip install 'soda-core' 'soda-core-snowflake'

      - name: Run scan
        env:
          SNOWFLAKE_USER:    ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_PASS:    ${{ secrets.SNOWFLAKE_PASS }}
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
        run: |
          soda scan -d warehouse -c configuration.yml checks.yml | tee scan.log

      - name: Upload scan log
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: soda-scan-log
          path: scan.log
          retention-days: 14
```

The `if: always()` on the artifact upload is required to capture the log
on a failed scan - when you most need it for triage. For a managed
GitHub-Action wrapper that auto-comments on PRs, see the
[Soda GitHub Action][4].

## References

- [sodacl-overview][1] - SodaCL concept overview, common check types,
  threshold syntax.
- [sodacl-quickstart][2] - quickstart with canonical CLI invocation
  and default filenames.
- [quick-start-dev][3] - `configuration.yml` shape, env-var
  substitution, CI-flow example.
- [Soda GitHub Action][4] - first-party CI-action wrapper.
