---
name: pyarrow-python
description: Use for writing, reviewing, debugging, testing, or optimizing Python code that uses PyArrow arrays, schemas, Tables, RecordBatches, RecordBatchReaders, compute kernels, Dataset scans, Parquet, or Arrow IPC and C data interfaces. Trigger on schema drift, null/type semantics, chunking, batch streaming, predicate projection pushdown, conversion, and memory ownership. Do not use for pandas-only transformations, Polars-only expressions, generic SQL, Arrow Flight service design, C++/Rust Arrow, or Parquet work that does not use PyArrow.
argument-hint: "[PyArrow task, code, schema, error, or data boundary]"
---

# PyArrow Python

Produce schema-explicit columnar code whose logical object, batch boundary,
null behavior, memory lifetime, and materialization point are deliberate.

## Boundary

Use this skill when the implementation directly uses `pyarrow` or must expose an
Arrow-compatible boundary. Do not introduce PyArrow merely to perform a small
Python-list or pandas transformation. Keep storage-format questions in scope
only when PyArrow reads or writes them. Arrow Flight servers, Acero internals,
and non-Python implementations require their own guidance.

## Classify the object first

| Object | Meaning | Use it for |
|---|---|---|
| `DataType` / `Field` / `Schema` | Immutable type and named-field contracts, including nullability and metadata. | Pinning a boundary before constructing or scanning data. |
| `Scalar` | One typed value, possibly null. | Kernel arguments and scalar results. |
| `Array` | One contiguous typed column backed by buffers. | A single physical column segment. |
| `ChunkedArray` | One logical column made of zero or more same-typed arrays. | Table columns and multi-source results; chunk count is not row count. |
| `RecordBatch` | Equal-length arrays under one schema. | Bounded transport or processing batches. |
| `Table` | A logical table whose columns may be chunked. | Materialized tabular results that fit the required memory boundary. |
| `RecordBatchReader` | A schema plus a consumable stream of batches. | Streaming interchange when the consumer can process batches once. |
| `Dataset` | A logical collection of fragments with a unified schema. | Discovering and querying multi-file or partitioned data. |
| `Scanner` | A dataset scan with projection, filter, and batching options bound. | Deferred dataset execution and bounded batch iteration. |

Arrays and schemas are immutable. A `Table` is materialized but may be
physically chunked; `combine_chunks()` can allocate and is not routine cleanup.
A `Dataset` describes sources, while a `Scanner` describes the read. Calling
`to_table()` materializes all selected rows; `to_batches()` preserves a batch
boundary. Read [the object and memory model](references/object-model.md) when
chunking, buffers, ownership, dictionaries, nested types, or zero-copy claims
matter.

## Ordered workflow

1. Recover the boundary contract: input object, output object, schema, field
   nullability, row order if required, batch size, and ownership lifetime.
2. Choose `Array`, `RecordBatch`, `Table`, `RecordBatchReader`, `Dataset`, or
   `Scanner` from that contract; do not default every job to `Table`.
3. Pin types where empty input, identifiers, timestamps, decimals, nested data,
   dictionary encoding, or cross-language interchange make inference unsafe.
4. Push dataset projection and predicates into the scan. Materialize only at a
   consumer that requires all rows.
5. Use `pyarrow.compute` kernels for Arrow data. Do not convert to Python rows
   or pandas solely to perform a supported kernel operation.
6. Test schema equality separately from value equality, and include empty,
   null, multi-chunk, and multi-batch inputs.
7. Inspect the installed API before using a drifting option or claiming a
   zero-copy, pushdown, or memory property.

## Choose by required result

| Required result | Use | Critical condition |
|---|---|---|
| One typed column | `pa.array(..., type=...)` | Conversion and null policy are explicit. |
| One bounded set of equal-length columns | `pa.record_batch(..., schema=...)` | All arrays conform to the same schema and length. |
| One logical materialized table | `pa.table(..., schema=...)` | Total selected result fits the boundary. |
| Consumable batches with a common schema | `RecordBatchReader` | The consumer accepts a one-pass stream. |
| Multi-file discovery and pruning | `pyarrow.dataset.dataset` | Format, filesystem, partitioning, and schema are known or inspected. |
| Deferred filtered/projected scan | `dataset.scanner(...)` | Use dataset expressions such as `ds.field`, not eager masks. |
| Elementwise, vector, aggregate, or selection work | `pyarrow.compute` | Choose kernel null semantics and checked/safe behavior deliberately. |
| Portable Arrow stream/file serialization | `pyarrow.ipc` | Choose stream for sequential batches, file for random-access footer metadata. |
| Analytical columnar storage | Parquet APIs or Dataset writer | Schema, partition layout, row groups, overwrite policy, and reader compatibility are explicit. |

Read [the operation map](references/operations.md) before choosing construction,
compute, dataset, serialization, or conversion APIs.

## Canonical typed scan

```python
from collections.abc import Iterator
from pathlib import Path

import pyarrow as pa
import pyarrow.dataset as ds


ORDER_SCHEMA = pa.schema(
    [
        pa.field("order_id", pa.uint64(), nullable=False),
        pa.field("country", pa.string(), nullable=False),
        pa.field("amount", pa.decimal128(18, 2), nullable=True),
    ]
)


def scan_orders(root: Path, country: str) -> Iterator[pa.RecordBatch]:
    dataset = ds.dataset(
        root,
        format="parquet",
        schema=ORDER_SCHEMA,
        partitioning="hive",
    )
    scanner = dataset.scanner(
        columns=["order_id", "country", "amount"],
        filter=ds.field("country") == country,
        batch_size=65_536,
    )
    yield from scanner.to_batches()
```

This returns bounded batches rather than concatenating the whole dataset. The
explicit schema prevents empty or heterogeneous fragments from silently
changing the boundary. Whether the filter is pruned by partitions/statistics or
evaluated after reading depends on the fragments and expression; verify a
performance claim instead of inferring it from the code.

## High-risk rules

### Types, nulls, and chunks

- Treat field nullability as a contract. A nullable type does not mean nulls
  have been checked for domain validity.
- Do not assume `nullable=False` validates constructed values. PyArrow table
  construction can attach a non-nullable field to an array that still contains
  nulls. Build typed arrays, reject a nonzero `null_count` for required fields,
  then construct the batch or table under the exact schema.
- Use safe casts by default. Permit truncation, overflow, temporal-unit loss, or
  invalid UTF-8 only when the contract names that loss and a test proves it.
- Arrow null and floating `NaN` are distinct. Choose kernel options explicitly
  when either affects filtering, aggregation, or equality.
- Compute functions commonly propagate nulls; Boolean kernels also have Kleene
  variants. Select the truth table required by the domain.
- Do not assume one chunk. Test with a multi-chunk `Table`, and call
  `combine_chunks()` only for an API that requires contiguous buffers or after
  measurement justifies the allocation.
- Dictionary, list, large-list, struct, map, decimal, and timestamp types carry
  semantics that Python containers do not preserve automatically. Pin the exact
  Arrow type at external boundaries.

### Datasets and materialization

- Use dataset `Expression` objects for scan filters and projections. A Python
  function or eager Boolean array cannot provide file/row-group pruning.
- Include partition columns in the declared schema and specify partitioning
  when directory names encode values. Do not infer a partition convention from
  one path example.
- `to_table()` loads the selected result; use `to_batches()` or a
  `RecordBatchReader` when total size is not proven safe.
- Preserve scanner/reader lifetime until consumption completes. Do not return a
  view over memory whose producer or foreign owner is already gone.
- “Zero-copy” is conditional on type, layout, alignment, mutability, and the
  source/consumer protocol. Verify actual buffers or document the allowed copy;
  never promise zero-copy from an API name alone.

### Conversion and storage

Conversions to pandas, NumPy, or Python objects can allocate, change nullable
representations, or lose nested/dictionary metadata. State the consumer and
test round trips only for properties the contract requires. For Parquet or IPC,
test the persisted schema and representative values after reopening the
artifact; an in-memory pre-write assertion is insufficient. Run [the installed-API inspector](scripts/inspect_pyarrow.py), read [version and
API grounding](references/version-grounding.md), and use [testing Arrow
boundaries](references/testing.md).

## Completion gate

Do not declare completion until the public object type and consumption model
match the caller; schema names, order, types, nullability, metadata requirements,
and time-zone/decimal semantics are asserted; empty, null, multi-chunk, and
multi-batch cases pass; dataset projection/filtering occurs before
materialization where required; conversions and writes are reopened or
round-tripped; and every copy, allocation, ordering, and pushdown claim is
measured or qualified. Report skipped checks and their consequence.

## References

- [Object and memory model](references/object-model.md)
- [Operation map](references/operations.md)
- [Version and API grounding](references/version-grounding.md)
- [Testing Arrow boundaries](references/testing.md)
