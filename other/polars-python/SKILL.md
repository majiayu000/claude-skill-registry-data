---
name: polars-python
description: Use for writing, reviewing, debugging, testing, or optimizing Python Polars DataFrame, Series, LazyFrame, Expr, selector, and I/O code, or for an explicitly requested pandas-to-Polars migration. Trigger on table construction, operation selection, lazy plans, expression-context mistakes, schema or dtype failures, joins, nested columns, missing values, and Polars performance work. Do not use for pandas-only, PySpark, Rust Polars, standalone SQL unrelated to Polars, library-neutral data tasks, Polars Cloud or On-Prem, distributed Polars, or GPU execution.
argument-hint: "[Polars task, code, error, or migration]"
---

# Polars Python

Produce version-grounded Polars code whose object types, row grain, schema,
missing-value policy, ordering, and execution boundary are deliberate and
tested.

## Boundary

Use this skill when the project already uses Polars or the user explicitly
requests Polars or a pandas-to-Polars migration. Polars SQL is in scope only
inside a Polars pipeline. Do not introduce Polars into a library-neutral,
pandas-only, PySpark, Rust, standalone-SQL, Cloud, On-Prem, distributed, or GPU
task. Preserve the caller's public return type unless the task changes it.

## Know the objects before choosing an API

| Object | Runtime meaning | Use it for |
|---|---|---|
| `DataFrame` | An eager, materialized two-dimensional table of uniquely named, equal-length typed columns. | In-memory work, an eager interface, or a collected result whose final table fits memory. |
| `Series` | One eager, materialized, named one-dimensional column with one dtype. | A one-column input/output boundary. |
| `Expr` | An unevaluated recipe for producing values from columns or literals; it is not data. | Reusable computation inside an expression context. |
| `LazyFrame` | A logical query plan that produces a table only when executed. | File-backed, multi-stage, large, or optimization-sensitive work. |
| `Schema` | The ordered mapping from column names to dtypes. | The table interface contract. |
| Selector | A schema-aware expression expander such as `cs.numeric()`. | Apply one rule to columns selected by name or dtype. |

`DataFrame` columns are `Series`. Use frame methods to change table shape and
`Expr` objects to define column computations or predicates inside those methods.
Eager and lazy frames share most expression APIs: eager contexts execute now,
while lazy contexts extend a plan. `GroupBy` and `LazyGroupBy` are builders, not
result frames; finish them with a terminal group operation, normally `.agg(...)`.
Polars has no pandas-style semantic row index—keep record labels as columns.

Read [the object and shape model](references/object-model.md) whenever object
type, dimensionality, positional selection, dtype namespaces, or return shape
is uncertain.

## Ordered workflow

1. Recover the contract from the request, callers, schema, and tests: public
   return object, row grain, keys, dtypes, missing values, and required order.
2. Classify the operation's shape effect, then choose its context or API family.
3. Choose eager, lazy, streaming, or sink execution from the real input and
   consumer boundaries.
4. Apply the relevant schema, join, time-series, reshape, migration, or UDF rule.
5. Keep native expressions in the pipeline; in lazy work, materialize only at a
   required consumer or unsupported-operation boundary.
6. Add the smallest falsifier: typed empty input, null/`NaN`, duplicate keys,
   order permutation, ambiguous rows, or dirty input.
7. Run targeted tests. Inspect a plan or measure scale only for a performance
   claim.

## Rigorous analytical contract

Separate four stages and report which ones actually ran:

| Stage | Required output |
|---|---|
| Frame | Population, row grain, keys, metric formulas, units, missingness, and required order. |
| Transform | Input/output objects, shape change, schema, execution boundary, and failure policy. |
| Validate | Cardinality, reconciliation, invariants, adversarial fixtures, and execution evidence. |
| Interpret | Evidence-supported result plus unresolved semantic, data, or numerical risk. |

Do not infer semantics from column names alone. Distinguish row count, entity
count, non-null count, numerator, denominator, and units before aggregation.
Compute a rate from aggregated numerator and denominator unless the contract
specifically defines a justified weighted alternative; never average row or
subgroup rates merely because they are available.

For consequential transformations, use at least one independent falsifier:
input-order permutation, batch partition/recombination for row-local work,
component-to-total reconciliation, eager/lazy equivalence, or a second query
formulation. Passing execution is not validation. Read [rigorous Polars
practice](references/recipes-rigorous-analysis.md) for the full checklist and
evaluated anchors.

## Choose by intent and output shape

| Required result | Use | Shape contract |
|---|---|---|
| Only selected/computed columns | `select` | Only requested outputs; expression lengths must be compatible. |
| Original columns plus additions/replacements | `with_columns` | Input height and unspecified columns remain. |
| Rows satisfying a predicate | `filter` | Same columns; only predicate `True` survives. |
| One materialized column | `get_column` | Returns `Series`; `select("x")` instead returns a one-column frame. |
| One row per group | `group_by(...).agg(...)` | Output grain is distinct group keys. |
| Group result aligned to every row | expression `.over(...)` | Default `group_to_rows` mapping preserves input grain; `explode` is shape-changing. |
| Rows chosen by position | `slice`, `head`, `tail`, or `gather` | Positions, not labels, define the result. |
| Records stacked by schema | `pl.concat` | Schema compatibility or union policy is explicit. |
| Tables combined by keys | `join` | Cardinality follows key multiplicity and join type. |
| Nested elements/fields expanded | `explode` / `unnest` | Row or column grain changes and is tested. |
| Columns converted to/from rows | `unpivot` / `pivot` | Identifier grain and generated-column policy are explicit. |

Read [the DataFrame operation map](references/dataframe-operations.md) for
construction, inspection, selectors, ordinary transformations, sorting,
deduplication, reshaping, and export.

## Canonical object flow

```python
import polars as pl


def normalized_email(column: str) -> pl.Expr:
    return pl.col(column).str.strip_chars().str.to_lowercase()


def enrich(frame: pl.DataFrame) -> pl.DataFrame:
    return (
        frame.with_columns(
            normalized_email("email").alias("email"),
            net=pl.col("quantity") * pl.col("unit_price"),
        )
        .with_columns(tax=pl.col("net") * pl.lit(0.19))
        .filter(pl.col("net").is_not_null())
        .select("order_id", "email", "net", "tax")
    )
```

The helper returns a symbolic `Expr`, so the caller chooses eager or lazy
execution. The second `with_columns` is required because sibling expressions
see the context's input schema, not aliases created by siblings. `pl.lit`
unambiguously represents a value; strings in expression-input positions often
mean column names.

## Execution boundary

- Return `LazyFrame` when the public contract requires a plan; never collect
  inside that function or collect and re-lazify to imitate laziness.
- For file-backed or multi-stage work whose final table fits memory, start with
  `scan_*`, keep one plan, and `collect()` once at the eager consumer.
- For a file or batch consumer, use an installed `sink_*` or batch API when it
  avoids materializing an oversized final `DataFrame`.
- For a small existing `DataFrame` with an eager consumer, eager expressions
  are valid; do not add `.lazy().collect()` ceremonially.
- If a required operation has no usable lazy form, materialize immediately
  before it only when the public contract permits an eager result. Record the
  optimization barrier.
- A streaming collect still materializes its final `DataFrame`; it only can
  bound intermediate memory. A `LazyFrame` is a plan, not a cached result.

Read [lazy execution and performance](references/performance.md) before making
an engine, streaming, caching, plan, or memory claim.

## High-risk semantic rules

### Expressions and schema

- Use parenthesized predicates with `&`, `|`, and `~`, never Python boolean
  operators on expressions. Every conditional branch must be independently
  valid.
- Alias derived scalar outputs. Selector and dtype expressions can expand to
  zero, one, or many columns; test expected names.
- Choose `.str`, `.dt`, `.list`, `.arr`, `.struct`, `.cat`, or `.bin` from the
  dtype rather than converting values to Python.
- `pl.len()` counts rows; expression `.count()` counts non-null values; a bare
  grouped column produces a `List`.
- Pin constructor or scan schemas when identifiers, temporal/nested values,
  empty inputs, or late dirty rows make inference unsafe. For ambiguous
  row-oriented constructor data, pass `orient="row"`.
- Keep casts strict unless invalid values becoming null is the declared policy,
  then test or count introduced nulls. Null and floating `NaN` are distinct.

Read [expression and shape rules](references/expressions.md) and [schema and
missing-data rules](references/schema-missing.md) for these branches.

### Relational, ordered, and shape-changing work

Before a join, state preserved rows, key domains/dtypes, uniqueness on both
sides, null-key behavior, output-key behavior, and order. Validate known
cardinality; otherwise prove uniqueness on the constrained side. Never cast
keys unless both represent the same domain and conversion is lossless. Read
[join rules](references/joins.md).

After an important join, measure result rows, null fact keys, unmatched
non-null fact rows, unused dimension keys, and any conserved measure required
by the analysis. A cardinality declaration proves multiplicity, not semantic
coverage or reconciliation.

Do not rely on undocumented output order from group, join, unique, pivot, or
unpivot. Preserve input order only where the chosen API guarantees it; otherwise
encode the sort keys and tie-breakers that define a survivor, list, cumulative
result, or final table. Read [join rules](references/joins.md) for as-of joins and
[time-series rules](references/time-series.md) for rolling, dynamic grouping,
calendar durations, and time zones.

### Python escape hatch

Prefer native expressions, selectors, typed namespaces, folds, windows, joins,
and reshapes. If they cannot express the operation, choose the narrowest
installed batch UDF before scalar `map_elements`; use a whole-frame UDF only
under an explicit schema contract. Declare dtype/schema, purity, null/exception
behavior, and empty/all-null behavior. Claim streamability only if arbitrary
batch boundaries cannot change results. Read [Python UDF
contracts](references/udf-contracts.md) before using any callback.

## Version grounding and completion

Inspect the installed version when a signature, keyword, dtype, engine,
warning, or capability can drift. Run `python scripts/inspect_polars.py` from
the installed skill directory for JSON evidence and read [API
grounding](references/api-grounding.md). Do not copy stale syntax from a prompt.

Translate pandas semantics rather than spellings; read [pandas
migration](references/pandas-migration.md) before a migration. Use Polars
testing helpers and typed expected frames; read [testing Polars
behavior](references/testing.md).

Do not declare completion until the return object, grain, schema, cardinality,
missing-value policy, and required order match the contract; the relevant
dirty/empty/null/duplicate/permutation fixtures pass; no accidental
materialization, unjustified Python row path, arbitrary key cast, or stale API
remains; aggregate components reconcile where required; validation status says
what executed versus what was only generated; and project checks pass or
skipped evidence and its consequence are reported.

## References

- [Core solution recipes](references/recipes-core.md)
- [Lazy and temporal recipes](references/recipes-scale.md)
- [Rigorous analytical practice and recipes](references/recipes-rigorous-analysis.md)
- [Object and shape model](references/object-model.md)
- [DataFrame operation map](references/dataframe-operations.md)
- [Expression and shape rules](references/expressions.md)
- [Schema and missing-data rules](references/schema-missing.md)
- [Join rules](references/joins.md)
- [Time-series rules](references/time-series.md)
- [Lazy execution and performance](references/performance.md)
- [Python UDF contracts](references/udf-contracts.md)
- [Pandas migration](references/pandas-migration.md)
- [Testing Polars behavior](references/testing.md)
- [API grounding](references/api-grounding.md)
