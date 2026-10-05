---
name: data-quality
description: Use when validating a dataset or building quality checks into a pipeline. Covers profiling, schema and constraint validation, freshness and completeness checks, anomaly detection, and failing a pipeline correctly.
metadata:
  category: data
  version: 1.0.0
  tags: [data-quality, validation, profiling, pipelines, testing]
---

# Data Quality

## Purpose

Catch bad data before it reaches a dashboard, a model, or a customer. A pipeline that silently propagates corrupt data is worse than one that fails, because the failure is discovered downstream, later, by someone who trusts the number.

## When to Use

- Ingesting data from a source you do not control.
- Building quality gates into a pipeline.
- Investigating a metric that looks wrong.
- Auditing a dataset before it is used for analysis or training.

## Capabilities

- Profiling: distributions, cardinality, null rates, outliers.
- Schema validation and type enforcement.
- Constraint checks: uniqueness, referential integrity, ranges, formats.
- Freshness, completeness, and volume anomaly detection.
- Quarantine and alerting patterns.

## Inputs

- The dataset and its expected schema.
- The business rules the data must satisfy.
- Historical volume and distribution, for anomaly baselines.

## Outputs

- A profile of the data as it actually is, not as documented.
- Validation checks that run on every load.
- A quarantine path for rows that fail, and an alert when they do.

## Workflow

1. **Profile before you trust** — Row count, null rate, cardinality, min/max, and the distribution of every column. The documented schema and the actual data disagree more often than not.
2. **Validate the schema at the boundary** — Column presence, types, and nullability, checked on ingest. A silently added column or a type change upstream is the most common pipeline break.
3. **Assert the business rules** — Uniqueness on keys, referential integrity, valid ranges, and formats. `total_cents >= 0` is a rule; assert it.
4. **Check freshness and volume** — Is the data recent, and is there roughly as much of it as usual? A pipeline that runs successfully on an empty file is the failure that is hardest to notice.
5. **Quarantine, do not drop** — Failing rows go to a quarantine table with the reason. Dropping them silently destroys the evidence needed to fix the source.
6. **Fail loudly and stop** — A pipeline that continues past a failed quality gate has published bad data. Stop, alert, and keep the previous good version live.

## Best Practices

- A pipeline that succeeds on zero rows is the most dangerous kind of success. Always assert a minimum expected volume.
- Check the distribution, not just the schema. A column that is technically valid but where the null rate jumped from 2% to 60% overnight indicates a broken upstream, and no type check will catch it.
- Quality checks belong in the pipeline, not in a separate job that runs afterwards. By then, the data has been consumed.
- Fail the pipeline on a hard rule violation (duplicate primary keys); warn on a soft one (unusual distribution). Treating everything as fatal trains people to disable the checks.
- Version the expectations alongside the data schema. A rule that was correct last year may be wrong now, and it should be updated deliberately rather than deleted in frustration.
- Every quarantined row needs the reason attached. "Failed validation" without a reason is not actionable.

## Examples

**Quality gate with hard and soft rules:**

```python
import pandera as pa
from pandera.typing import Series

class OrderSchema(pa.DataFrameModel):
    order_id: Series[str]      = pa.Field(unique=True, str_matches=r"^ord_[0-9A-Z]{10}$")
    customer_id: Series[str]   = pa.Field(nullable=False)
    total_cents: Series[int]   = pa.Field(ge=0, le=100_000_000)   # no negatives, no absurd values
    currency: Series[str]      = pa.Field(isin=["USD", "EUR", "GBP"])
    created_at: Series[pa.DateTime] = pa.Field(nullable=False)

    class Config:
        strict = True          # an unexpected column is an error, not a shrug
        coerce = False         # a wrong type is an error, not a silent conversion


def load(df: pd.DataFrame) -> pd.DataFrame:
    try:
        valid = OrderSchema.validate(df, lazy=True)   # collect all failures, not just the first
    except pa.errors.SchemaErrors as e:
        failures = e.failure_cases                     # row index + column + reason
        quarantine.write(df.loc[failures["index"].dropna().unique()], reasons=failures)
        alert(f"{len(failures)} rows quarantined on orders load", failures.head(20))
        raise PipelineHalted("orders failed schema validation")   # do not publish

    return valid
```

**The check that catches the silent failure:**

```python
# Volume and freshness. A pipeline that "succeeded" with 0 rows, or with
# yesterday's data, has failed in the way that is hardest to notice.
expected = baseline.median_rows(window_days=28)
actual = len(df)

if actual == 0:
    raise PipelineHalted("orders load produced 0 rows — upstream is likely broken")

if actual < expected * 0.5:
    alert(f"orders volume anomaly: {actual} rows vs a 28-day median of {expected}")

max_age = utcnow() - df["created_at"].max()
if max_age > timedelta(hours=6):
    raise PipelineHalted(f"orders data is stale: newest record is {max_age} old")
```

## Notes

- The most valuable check in any pipeline is the volume anomaly check, because it catches the failures where every individual row is valid and the dataset as a whole is wrong.
- Great Expectations, Pandera, and dbt tests all do this job; the tool matters far less than whether the checks run on every load and actually stop the pipeline.
- Data quality is a contract with the upstream producer. When a check fails repeatedly for the same reason, the fix belongs upstream, not in an ever-growing set of cleaning rules.
