---
name: exasol-udfs
description: "Exasol User Defined Functions (UDFs) and Script Language Containers (SLCs). Covers `CREATE SCRIPT`, SCALAR and SET functions, variadic scripts with `EMITS(...)` and `default_output_columns`, the `ExaIterator` and `ExaMetadata` APIs, Python, Java, Lua, and R scripts, Lua execute scripts and `pquery`, BucketFS file access, GPU-accelerated UDFs, `ALTER SESSION SET SCRIPT_LANGUAGES` activation, and building custom Script Language Containers with `exaslct`, `exaslpm`, and `packages.yml`."
---

# Exasol UDFs & Script Language Containers

UDFs extend SQL with custom logic that runs inside the Exasol cluster: per-row
transforms, custom aggregation, ML inference against a model in BucketFS,
external API calls, and DataFrame batch processing. They execute in a Script
Language Container — a Docker-based runtime whose contents you can replace when
the default packages are not enough.

## Two Decisions Before Any Route

**SCALAR or SET?**

| | SCALAR | SET |
|---|--------|-----|
| **Input** | One row at a time | Group of rows (via GROUP BY) |
| **Output** | `RETURNS <type>` (single value) | `EMITS (col1 TYPE, ...)` (zero or more rows) |
| **Row iteration** | Not needed | `ctx.next()` loop required |
| **SQL usage** | `SELECT udf(col) FROM t` | `SELECT udf(col) FROM t GROUP BY key` |
| **Use case** | Per-row transforms | Aggregation, ML batch predict, multi-row emit |

**Which language?**

| Language | Startup | Best For | Expandable via SLC? |
|----------|---------|----------|---------------------|
| **Python 3** (3.10 or 3.12) | ~200ms | ML, data science, pandas, string processing | Yes |
| **Java** (11 or 17) | ~1s | Enterprise libs, type safety, Virtual Schema adapters | Yes |
| **Lua 5.4** | <10ms | Low-latency transforms, row-level security | No (natively compiled into Exasol) |
| **R** (4.4) | ~200ms | Statistical modeling, R model deployment | Yes |

## Routing Algorithm

Choose the narrowest matching route. Several often apply — a Python UDF that
reads a model needs routes 1 and 2 — so load all matching references.

1. **Write the `CREATE SCRIPT` statement** — syntax for any language, variadic scripts
   - Trigger phrases: `CREATE SCRIPT`, `SCALAR`, `SET EMITS`, `RETURNS`, `variadic script`, `dynamic parameters`, `EMITS(...)`, `default_output_columns`, `%scriptclass`, `%jar`, `R UDF`, `Lua UDF`
   - Load: `references/create-script-syntax.md`

2. **Python UDF internals** — context API, type mapping, DataFrames, BucketFS reads, testing
   - Trigger phrases: `Python UDF`, `ctx.emit`, `ctx.next`, `get_dataframe`, `pandas`, `pickle`, `load model`, `udf-mock-python`, `dynamic import`, `memory limit`
   - Load: `references/udf-python.md`

3. **Java or Lua UDF internals** — `ExaIterator`, `ExaMetadata`, JARs, JVM options, adapters, Lua libraries
   - Trigger phrases: `Java UDF`, `ExaIterator`, `ExaMetadata`, `getString`, `%jar`, `JVM options`, `script imports`, `ADAPTER script`, `remote debugging`, `Lua context`
   - Load: `references/udf-java-lua.md`

4. **Build or deploy a Script Language Container** — flavors, packages, activation, troubleshooting
   - Trigger phrases: `SLC`, `Script Language Container`, `exaslct`, `exaslpm`, `packages.yml`, `custom packages`, `flavor`, `conda`, `CUDA`, `GPU UDF`, `SCRIPT_LANGUAGES`, `ALTER SESSION`, `ALTER SYSTEM`, `security-scan`
   - Load: `references/slc-reference.md`

5. **Orchestrate SQL from inside the database** — not a UDF
   - Trigger phrases: `execute script`, `Lua execute`, `pquery`, `in-database orchestration`, `iterative algorithm`, `multi-step SQL workflow`
   - Load: `references/lua-execute-scripts.md`

Route 5 is a genuine fork, not a variant of the others: use a Lua execute script
rather than a UDF when the task is to orchestrate multi-step or iterative SQL
workflows from within the database.

## Performance Notes

- **Load once, use many**: load models and other resources at module level, outside the row loop.
- **Use SET for batching**: collect rows into a list or DataFrame and process in bulk.
- **Lua for low latency**: avoids JVM and Python startup overhead entirely.
- **Parallelism is automatic**: UDFs run on all cluster nodes simultaneously.
- **GPU work needs a CUDA SLC**: the UDF API is unchanged, but the container and host driver are not — see `references/slc-reference.md`.

## Related Skills

- **exasol-bucketfs**: uploading the JARs, models, and containers that UDFs read.
- **exasol-distributed-ml**: end-to-end distributed training and inference pipelines built on these UDFs.
