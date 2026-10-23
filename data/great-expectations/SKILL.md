---
name: great-expectations
description: "Authors Great Expectations (GX Core) ExpectationSuites, builds ValidationDefinitions and Checkpoints, runs validation against tabular batches, and parses the JSON result for CI gating. Use when the user works with Great Expectations on Pandas, SQL, or Spark data."
---

# great-expectations

## Overview

GX Core is the modern Python library for programmatic data validation
workflows. The shape is: **DataSource → DataAsset → BatchDefinition →
ExpectationSuite → ValidationDefinition → Checkpoint** ([gx-overview][1]).
This skill covers authoring expectations, running them via a
ValidationDefinition or Checkpoint, parsing the JSON result, and gating
CI on it.

[1]: https://docs.greatexpectations.io/docs/core/introduction/gx_overview

## When to use

- The repo imports `great_expectations` (Python).
- The user asks about `ExpectColumn*`, `ExpectationSuite`, `Checkpoint`,
  Data Docs, or `gx.get_context()`.
- A pipeline needs row-level / column-level assertions on Pandas, SQL,
  or Spark data with a programmatic interface (rather than a YAML-only
  config like Soda).
- A CI workflow needs to gate a run on a validation result and surface
  failures in Data Docs or Slack.

## Authoring expectations

The four key objects to compose ([gx-overview][1]):

1. **DataSource** - represents a connection to a data store (Pandas /
   SQL / Spark / files).
2. **DataAsset** - a collection of records inside a DataSource (e.g. a
   table, a directory of partitioned files).
3. **BatchDefinition** - slices a DataAsset into validatable batches
   (whole table, partition, dataframe).
4. **ExpectationSuite** - a named collection of `Expectation` objects
   that describe what the data should look like.

Expectations themselves come from the `gxe` namespace ([create-an-expectation][2]):

[2]: https://docs.greatexpectations.io/docs/core/define_expectations/create_an_expectation

```python
import great_expectations as gx
from great_expectations import expectations as gxe

context = gx.get_context()

suite = context.suites.add(gx.ExpectationSuite(name="orders_suite"))

# Column-level expectations
suite.add_expectation(gxe.ExpectColumnValuesToNotBeNull(column="order_id"))
suite.add_expectation(gxe.ExpectColumnValuesToBeUnique(column="order_id"))
suite.add_expectation(
    gxe.ExpectColumnValuesToBeBetween(
        column="discount_percent", min_value=0, max_value=100
    )
)
suite.add_expectation(
    gxe.ExpectColumnValuesToBeInSet(
        column="status",
        value_set=["placed", "shipped", "completed", "returned"],
    )
)

# Table-level expectations
suite.add_expectation(gxe.ExpectTableRowCountToBeBetween(min_value=1, max_value=10_000_000))
```

The full expectation gallery (column-, table-, multi-column-, and custom
expectations) is browsable at
[greatexpectations.io/expectations](https://greatexpectations.io/expectations).

## Running

### Option A - ValidationDefinition (single-suite, single-batch)

A `ValidationDefinition` binds one `BatchDefinition` to one
`ExpectationSuite`. Calling `.run()` validates and returns a JSON-shaped
result whose `results` list reports each expectation's outcome
([run-validation-definition][3]):

[3]: https://docs.greatexpectations.io/docs/core/run_validations/run_a_validation_definition

```python
validation_definition = context.validation_definitions.get("orders_validation")

# batch_parameters maps to the underlying BatchDefinition's keys
result = validation_definition.run(batch_parameters={"year": "2026"})
print(result.success)       # bool - True only if every expectation passed
```

`batch_parameters` keys depend on how the BatchDefinition was authored:
`{"dataframe": df}` for a Pandas runtime asset, `{"year": "...", "month":
"..."}` for partitioned data, etc. ([run-validation-definition][3]).

### Option B - Checkpoint (multi-suite + actions)

A `Checkpoint` runs one or more `ValidationDefinition`s and triggers
**Actions** on the result. Actions live in
`great_expectations.checkpoint`; built-ins include
`UpdateDataDocsAction` (regenerates the Data Docs static site) and
`SlackNotificationAction` (alerts on failure) - all action class names
end with `*Action` ([checkpoint-actions][4]):

[4]: https://docs.greatexpectations.io/docs/core/trigger_actions_based_on_results/create_a_checkpoint_with_actions

```python
import great_expectations as gx
from great_expectations.checkpoint import (
    SlackNotificationAction,
    UpdateDataDocsAction,
)

context = gx.get_context()
validation_definitions = [context.validation_definitions.get("orders_validation")]

action_list = [
    SlackNotificationAction(
        name="alert_on_failure",
        slack_token="${VALIDATION_SLACK_WEBHOOK}",
        slack_channel="${VALIDATION_SLACK_CHANNEL}",
        notify_on="failure",
        show_failed_expectations=True,
    ),
    UpdateDataDocsAction(name="refresh_data_docs"),
]

checkpoint = gx.Checkpoint(
    name="orders_checkpoint",
    validation_definitions=validation_definitions,
    actions=action_list,
    result_format={"result_format": "COMPLETE"},
)

context.checkpoints.add(checkpoint)
checkpoint.run()
```

`result_format` controls how much detail the Validation Result carries.
Documented values include **SUMMARY** (default) and **COMPLETE** - use
`COMPLETE` when downstream tooling needs the failing rows /
unexpected-values list ([checkpoint-actions][4]).

## Parsing the result

`validation_definition.run()` (and the per-validation entries on a
Checkpoint result) returns a JSON-shaped object with at least
([run-validation-definition][3]):

| Field      | Meaning                                                        |
|------------|----------------------------------------------------------------|
| `success`  | Boolean - `True` only if every expectation in the suite passed. |
| `results`  | List of per-expectation outcomes (each has `success`, the expectation type, and a summary block describing the failure). |

Triage script:

```python
result = validation_definition.run()
if not result.success:
    for r in result.results:
        if not r.success:
            # r.expectation_config has the expectation type / kwargs
            # r.result has the unexpected_count / unexpected_percent
            print(r.expectation_config.type, r.result)
```

When `result_format: COMPLETE`, each `r.result` block additionally carries
`unexpected_index_list` (Pandas) or `unexpected_value_counts`, which lets
the gate report the offending rows by id rather than just a count.

## CI integration

The minimal pattern is: `gx.get_context()` from a repo-checked-in GX
project, run a Checkpoint, exit non-zero on `not result.success`. Use
`UpdateDataDocsAction` so the rendered HTML report is uploaded as a
build artifact for human triage.

```python
# scripts/run_gx_gate.py
import sys
import great_expectations as gx

context = gx.get_context()
checkpoint = context.checkpoints.get("orders_checkpoint")
result = checkpoint.run()

if not result.success:
    sys.exit(1)
```

```yaml
# .github/workflows/data-quality.yml (excerpt)
- name: Run GX checkpoint
  run: python scripts/run_gx_gate.py

- name: Upload Data Docs
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: gx-data-docs
    path: gx/uncommitted/data_docs/local_site/
```

`if: always()` is required so the Data Docs upload survives a failing
checkpoint - that's exactly when you need them for triage.

## References

- [gx-overview][1] - GX Core concept model and 4-step workflow.
- [create-an-expectation][2] - `gxe` namespace and expectation
  instantiation patterns.
- [run-validation-definition][3] - `.run(batch_parameters=...)` and the
  result object shape.
- [checkpoint-actions][4] - Checkpoint composition and built-in Actions.
