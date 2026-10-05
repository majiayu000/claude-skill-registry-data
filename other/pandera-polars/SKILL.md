---
name: pandera-polars
description: Use for writing, reviewing, debugging, or testing Pandera schemas and runtime validation for Polars DataFrame or LazyFrame pipelines installed with pandera[polars]. Trigger on pandera.polars DataFrameSchema, DataFrameModel, Column, Field, Check, PolarsData, decorators, coercion, strictness, lazy error collection, and validation-depth decisions. Do not use for pandas-backed Pandera, Pydantic object models, Polars transformations without Pandera, static dataframe typing alone, or generic data-quality platforms.
argument-hint: "[Pandera Polars schema, validation task, code, or failure]"
---

# Pandera for Polars

Create executable Polars dataframe contracts whose backend, validation depth,
coercion, failure aggregation, and pipeline boundary are explicit.

## Boundary

Use this skill only for Pandera's Polars backend. Import it as
`pandera.polars`; pandas, Ibis, PySpark, and Narwhals-backed behavior differs.
Use the Polars skill for transformation semantics and this skill for runtime
dataframe contracts. Do not replace ordinary Python object validation with a
one-row dataframe schema.

## Know the objects and overloaded words

| Object | Runtime meaning | Use it for |
|---|---|---|
| `DataFrameSchema` | An executable schema object containing Polars column and dataframe checks. | Dynamic/programmatic schemas and schema composition. |
| `Column` | A named column contract: dtype, nullability, requirement, uniqueness, coercion, and checks. | Per-column structural and value rules. |
| `Check` | A predicate contract evaluated by the backend. | Domain constraints not captured by dtype/nullability. |
| `DataFrameModel` | A class-declared schema compiled from annotations, `Field`s, checks, and config. | Reusable named contracts with type-checker-friendly declarations. |
| `Field` | Declarative column constraints inside a `DataFrameModel`. | Built-in comparisons, membership, aliases, nullable/unique behavior. |
| `PolarsData` | Custom-check input holding a `LazyFrame` and optional column key. | Native vectorized Polars checks. |
| `SchemaError` / `SchemaErrors` | One validation failure or an aggregate of failures. | Machine-readable failure handling and diagnostics. |

Two kinds of “lazy” must remain separate:

- `pl.LazyFrame` is a deferred Polars query. Pandera's native Polars validation
  checks schema-level properties by default and does not automatically execute
  all data-level checks on an uncollected plan.
- `schema.validate(..., lazy=True)` requests accumulation of multiple validation
  failures before raising; it does not make eager validation computationally
  lazy.

Read [the schema and validation model](references/object-model.md) before
choosing a schema style or claiming that values were checked.

## Ordered workflow

1. Recover the data contract: accepted frame type, ordered/required columns,
   exact dtypes, nullable fields, uniqueness, extra-column policy, allowed
   coercions, cross-column invariants, and failure interface.
2. Import `pandera.polars as pa`. Confirm the installed Pandera and Polars
   versions before copying a backend feature or signature.
3. Choose `DataFrameSchema` for dynamic composition or `DataFrameModel` for a
   stable named contract. Do not maintain both as independent sources of truth.
4. Encode structural rules first, then built-in vectorized checks, then the
   smallest native custom check that remains.
5. Choose validation depth from the input object. If data-level checks are
   required for a `LazyFrame`, collect or otherwise establish a supported
   execution boundary; do not report schema-only validation as full validation.
6. Choose `coerce`, `strict`, and `lazy` independently. Each changes a different
   contract.
7. Validate at ingress, after an untrusted/shape-changing stage, or before
   egress—not after every expression by habit.
8. Test one failure for every rule and inspect `failure_cases`/error categories,
   not exception prose alone.

## Decision table

| Need | Use | Do not confuse it with |
|---|---|---|
| Programmatic/reusable schema value | `pa.DataFrameSchema` | A Python class instance model. |
| Declarative named dataframe contract | `pa.DataFrameModel` | Pydantic `BaseModel`. |
| Reject unspecified columns | `strict=True` | `required=True`, which concerns declared columns. |
| Drop unspecified columns intentionally | Installed `strict="filter"` support | Silent schema drift; test passthrough loss. |
| Convert compatible inputs | `coerce=True` at the chosen scope | Validation-only behavior; coercion mutates the returned representation. |
| Gather all failures | `validate(..., lazy=True)` | A Polars `LazyFrame`. |
| Vectorized custom column rule | `Check` receiving `PolarsData` and returning Boolean `LazyFrame` output | Python element callbacks. |
| Cross-column invariant | Dataframe-level native check | A column check that cannot see the needed peer fields. |

Read [the operation map](references/operations.md) for schemas, models, checks,
decorators, and pipeline placement.

## Canonical strict contract

```python
import pandera.polars as pa
import polars as pl


ORDERS = pa.DataFrameSchema(
    {
        "order_id": pa.Column(
            pl.Int64,
            checks=pa.Check.ge(1),
            nullable=False,
            unique=True,
        ),
        "country": pa.Column(
            pl.String,
            checks=pa.Check.isin(["DE", "FR", "NL"]),
            nullable=False,
        ),
        "amount": pa.Column(
            pl.Float64,
            checks=pa.Check.ge(0),
            nullable=True,
        ),
    },
    strict=True,
    coerce=False,
)


def validate_orders(frame: pl.DataFrame) -> pl.DataFrame:
    return ORDERS.validate(frame, lazy=True)
```

This rejects extra columns, does not silently coerce identifiers or amounts,
checks all data-level rules on an eager frame, and aggregates failures. If the
boundary intentionally normalizes compatible types, turn on coercion and test
the returned dtypes and failed dirty values; do not use coercion to make an
unknown schema “pass.”

## Custom checks without Python row paths

```python
import pandera.polars as pa
import polars as pl
from pandera.polars import PolarsData


def start_before_end(data: PolarsData) -> pl.LazyFrame:
    return data.lazyframe.select(pl.col("start") <= pl.col("end"))


INTERVALS = pa.DataFrameSchema(
    {
        "start": pa.Column(pl.Datetime),
        "end": pa.Column(pl.Datetime),
    },
    checks=pa.Check(start_before_end),
)
```

A native custom check returns a Boolean `LazyFrame` shape accepted by the
backend. Avoid `element_wise=True` for a vectorizable condition; the Polars
backend implements elementwise Python callbacks through a slower row path.

## High-risk rules

- Backend imports are part of correctness. Do not use top-level or
  `pandera.pandas` examples in Polars code.
- `nullable`, `required`, `unique`, `strict`, and `coerce` are independent.
  State each required policy rather than relying on defaults.
- A schema validates its declared contract, not business completeness. Add
  cross-column checks for relational invariants and tests for duplicate/null
  combinations where needed.
- DataFrame validation can return a coerced/filtered frame. Use the returned
  value; do not validate and then continue with the unvalidated original.
- For a `LazyFrame`, establish whether schema-only validation is acceptable. If
  row values must be proven, validate an eager boundary or a currently
  documented supported full-data path.
- Treat validation errors as structured evidence. Preserve useful failure cases
  without leaking sensitive source values in logs or API responses.
- Feature support differs by backend. Do not copy pandas-only index, groupby
  check, parser, hypothesis, synthesis, or custom-registration patterns into a
  Polars schema without current evidence.

Run [the backend inspector](scripts/inspect_pandera_polars.py), read [version and backend grounding](references/version-grounding.md), and use [the
validation test matrix](references/testing.md).

## Completion gate

Do not declare completion until the import selects the Polars backend; the
schema style has one source of truth; exact dtypes, required/null/unique/extra
and coercion policies are asserted; eager versus lazy-frame validation depth is
tested; vectorizable rules stay native; the returned validated frame is used;
every rule has a failing example; aggregated failures are asserted structurally;
and installed-version checks cover backend-specific syntax. Report any
schema-only LazyFrame validation or skipped dependency execution explicitly.

## References

- [Schema and validation model](references/object-model.md)
- [Operation map](references/operations.md)
- [Version and backend grounding](references/version-grounding.md)
- [Testing Pandera Polars contracts](references/testing.md)
