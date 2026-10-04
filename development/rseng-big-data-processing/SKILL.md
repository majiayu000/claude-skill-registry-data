---
name: rseng-big-data-processing
description: >-
  Covers processing research data that outgrows one machine's memory:
  out-of-core and chunked computation, Dask for scaling the scientific Python
  stack, Spark for distributed tabular pipelines, lazy evaluation,
  partitioning strategies, idempotent and restartable batch jobs, and knowing
  when NOT to distribute. Use when datasets no longer fit in memory, when the
  user mentions Dask, Spark, out-of-core or larger-than-memory data, when a
  pandas/NumPy workflow hits memory limits, or when designing batch pipelines
  over many files. (Cluster job submission and job arrays are
  rseng-hpc-computing; pipeline orchestration engines are rseng-workflows; profile
  first with rseng-performance-profiling.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Big data processing for research

"Big" starts where the current tool breaks: the dataset that no
longer fits in RAM, the loop over files that no longer finishes
overnight. The escalation path matters more than any framework -
each step up costs complexity, debuggability and reproducibility,
so take the smallest step that works.

## The escalation ladder

1. Optimize in place first: columnar formats with predicate
   pushdown (Parquet - rseng-scientific-file-formats), dtype
   downcasting, reading only needed columns; profile before scaling
   (rseng-performance-profiling) - many "big data" problems are
   memory-layout problems.
2. Out-of-core on one machine: chunked iteration (read-process-
   write per chunk), memory-mapped arrays, or Dask's lazy
   collections on a single node. One machine with streaming
   processing handles far more than intuition suggests, with none
   of the distributed complexity.
3. Embarrassingly parallel batch: independent per-file/per-chunk
   jobs as cluster job arrays (rseng-hpc-computing) or a workflow
   engine (rseng-workflows) - the RIGHT answer for most research
   sweeps, and simpler than any framework.
4. Distributed frameworks: Dask (scales NumPy/pandas/xarray idioms;
   native in the Pangeo geoscience stack) or Spark (SQL-flavored
   tabular pipelines, industry-standard cluster tooling) when
   computation genuinely needs cross-partition coordination:
   shuffles, joins, global aggregations over larger-than-node data.

Skipping straight to step 4 is the classic mistake: a distributed
job that could have been a job array is slower to build, harder to
debug and harder to reproduce.

## Patterns that make batch processing trustworthy

- Idempotent tasks: running a task twice yields the same result -
  write to output paths derived from inputs and parameters, never
  append blindly.
- Restartable pipelines: skip work whose outputs already exist
  (checkpointing at the task level), so a failure at file 90,000
  costs minutes, not the weekend. Workflow engines give this for
  free (rseng-workflows).
- Fail loudly per item, not globally: quarantine failing inputs
  with logged reasons and continue; a summary of 37 failures beats
  a crash at the first.
- Validate at the boundaries: schema/sanity checks on ingest and
  before final aggregation - silent corruption scales with the data
  (rseng-data-management).
- Deterministic partitioning and seeds where randomness exists, so
  reruns are comparable.

## Framework-specific footguns

- Lazy evaluation (Dask, Spark) means errors surface at compute
  time, far from their cause: materialize small samples early while
  developing; keep transformations testable on in-memory subsets
  (rseng-testing) - the same code path at toy scale is the unit test.
- Partition sizing dominates performance: too many tiny partitions
  drown in scheduling overhead, too few lose parallelism; target
  the framework's recommended per-partition sizes and re-partition
  after heavy filters.
- Shuffles (joins, groupbys across partitions) are the expensive
  operations - restructure to avoid them where possible, and
  broadcast small tables instead of joining large-to-large.
- Cluster resources: match worker memory to partition size,
  and on shared clusters run the framework's scheduler inside the
  allocation (rseng-hpc-computing) rather than assuming the machine.
- Record framework and cluster configuration with results -
  distributed runs are part of the provenance
  (rseng-reproducible-environments, rseng-ai-declaration for
  AI-assisted pipeline work).

## Working with this skill

This skill is source-independent: its authority is the framework
documentation and community practice linked below.

Learn more (verified):
  - https://www.dask.org - Dask
  - https://spark.apache.org - Apache Spark
  - https://pangeo.io - Pangeo community practice for large-scale
    scientific data
  - https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009757 -
    Ten Simple Rules for large-scale data processing

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-green-computing - distributed runs carry energy cost
- rseng-hpc-computing - job arrays and cluster allocations
- rseng-performance-profiling - profile before scaling out
- rseng-scientific-file-formats - Parquet and chunked stores enable it
- rseng-testing - test transforms on in-memory subsets
- rseng-workflows - restartable pipelines via engines

<!-- related-skills:end -->
