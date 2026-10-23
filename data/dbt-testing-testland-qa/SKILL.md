---
name: dbt-testing
description: "Authors and runs dbt data tests (generic, singular, and custom-macro), parses test failure output from run_results.json, and gates dbt build on test results. Use when the user works with a dbt project, asks about model assertions, or needs CI gates on a data pipeline."
---

# dbt-testing

## Overview

dbt distinguishes **data tests** (assertions on rows, e.g. unique / not_null)
from **unit tests** (logic tests on transformations); this skill targets
data tests. The YAML key was renamed from `tests:` to `data_tests:` to
disambiguate; `tests:` remains a back-compat alias but you cannot have both
on the same resource at the same time
([data-tests][1]).

[1]: https://docs.getdbt.com/docs/build/data-tests

## When to use

- The repo contains a `dbt_project.yml` or a `models/` directory with `.sql`
  files referencing `{{ ref(...) }}` / `{{ source(...) }}`.
- The user asks about generic tests (`unique`, `not_null`, `accepted_values`,
  `relationships`) - the four built-in generics shipped with dbt
  ([data-tests][1]).
- The user mentions dbt build failures, schema drift, or wants assertions
  on data flowing through models.
- A CI workflow needs a quality gate that fails the pipeline when a model
  ships bad data.

## Authoring tests

### Generic tests in `schema.yml`

Use `data_tests:` (canonical) - `tests:` is the legacy alias and cannot
coexist with `data_tests:` on the same resource ([data-tests][1]).

```yaml
version: 2
models:
  - name: orders
    columns:
      - name: order_id
        data_tests:
          - unique
          - not_null
      - name: status
        data_tests:
          - accepted_values:
              arguments:
                values: ['placed', 'shipped', 'completed', 'returned']
      - name: customer_id
        data_tests:
          - relationships:
              arguments:
                to: ref('customers')
                field: id
```

The `arguments:` key under parameterized generics (`accepted_values`,
`relationships`) is the canonical syntax in current dbt ([data-tests][1]).

### Singular tests

Singular tests live as `.sql` files under `tests/` (or a custom `test-paths`
config). Each file is one `select` that returns **failing rows** - empty
result set means pass ([data-tests][1]).

`tests/assert_payment_total_non_negative.sql`:

```sql
-- Returns rows where the aggregated payment total is negative;
-- empty result set = test passes.
select order_id, sum(amount) as total_amount
from {{ ref('fct_payments') }}
group by 1
having sum(amount) < 0
```

> **Trap:** dbt requires you to **omit trailing semicolons** in singular
> test SQL - a `;` at the end can cause the test to fail spuriously
> ([data-tests][1]). This is unlike most SQL editors which add the
> semicolon by default.

### Custom generic tests via macros

Reusable assertions are defined as Jinja `{% test %}` blocks that take
`model` and column arguments and return a `select` of failing rows
([data-tests][1]):

```jinja
{% test column_value_in_range(model, column_name, min_value, max_value) %}
select *
from {{ model }}
where {{ column_name }} < {{ min_value }}
   or {{ column_name }} > {{ max_value }}
{% endtest %}
```

Reference once defined, then call by name in `data_tests:`. See
[references/macros.md](references/macros.md) for the canonical macro
shapes (range checks, conditional uniqueness, recency / freshness,
external referential integrity).

## Running

`dbt test` runs data tests defined on models, sources, snapshots, seeds,
plus unit tests on SQL models ([dbt-test][2]).

[2]: https://docs.getdbt.com/reference/commands/test

```bash
# Run every data test in the project
dbt test --select test_type:data

# Run every test (data + unit) on a specific model
dbt test --select orders

# Run only singular tests
dbt test --select test_type:singular

# Run only generic tests
dbt test --select test_type:generic

# Combine selectors with comma (intersection)
dbt test --select "orders,test_type:data"

# Run tests for everything in a package
dbt test --select "my_package.*"
```

`dbt build` is the integrated command that runs models, tests, snapshots,
seeds, and user-defined functions in **DAG order**. Critically, **a failing
upstream test causes downstream resources to skip** - so `dbt build` is
the right command for a pipeline that should not propagate bad data
([dbt-build][3]):

[3]: https://docs.getdbt.com/reference/commands/build

```bash
dbt build                                    # full project, DAG order
dbt build --select state:modified+           # changed nodes + descendants
dbt build --empty                            # zero-row dry run for validation
dbt build --select "test_type:unit"          # unit-test-only build subset
```

Severity can be relaxed from `error` to `warn` on a per-test basis to
prevent a single test from cascading skips downstream ([dbt-build][3]).

## Parsing failures

Both `dbt test` and `dbt build` produce **`run_results.json`** in the dbt
artifacts directory. Each result entry is a node-level record with
([run-results-json][4]):

[4]: https://docs.getdbt.com/reference/artifacts/run-results-json

| Field              | Meaning                                                      |
|--------------------|--------------------------------------------------------------|
| `unique_id`        | Node identifier (e.g. `test.<project>.<test_name>`); maps to `manifest.json`. |
| `status`           | dbt's interpretation of runtime success / failure / error. |
| `execution_time`   | Total node execution duration (seconds).                     |
| `timing`           | Per-phase breakdown (compile, execute).                      |
| `message`          | Human-readable CLI message based on adapter output.          |
| `failures`         | Count of test failures (rows returned by the test SELECT).   |
| `adapter_response` | Database-returned metadata (varies by warehouse adapter).    |
| `compiled`         | Whether the node compiled successfully.                      |
| `compiled_code`    | The rendered SQL string (useful for debugging).              |
| `relation_name`    | Fully-qualified database object name.                        |

A failing data test typically appears as `status: "fail"` with `failures:
<N>` (rows returned). A test that errored before producing rows (e.g. a
SQL compilation error) appears differently - handle both when parsing.

Quick triage with `jq`:

```bash
# List all failing test nodes
jq -r '.results[] | select(.status=="fail") | .unique_id + " (" + (.failures|tostring) + " failures)"' \
  target/run_results.json

# Surface the first 5 failure messages
jq -r '.results[] | select(.status=="fail") | .message' target/run_results.json | head -5
```

## CI integration

Use `dbt build` (not `dbt test` alone) so the pipeline halts at the first
failed assertion in the DAG and skips downstream nodes. Always upload
`target/run_results.json` (and `target/manifest.json`) as an artifact so
the failing-test list survives the run.

See [references/ci-integration.md](references/ci-integration.md) for
ready-to-paste workflow snippets for GitHub Actions, GitLab CI, and
Jenkins, plus the `--store-failures` and slim-CI patterns that scope tests
to changed nodes.

## References

- [`references/macros.md`](references/macros.md) - custom generic test
  patterns, severity overrides, conditional assertions.
- [`references/ci-integration.md`](references/ci-integration.md) - CI
  workflow snippets, slim CI via `state:modified+`, artifact upload.
- [data-tests][1] - canonical dbt docs page.
- [dbt-test][2] - `dbt test` command reference.
- [dbt-build][3] - `dbt build` command reference.
- [run-results-json][4] - `run_results.json` artifact schema.
