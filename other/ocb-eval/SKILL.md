---
name: ocb-eval
description: Evaluates the performance and scalability of Object-Oriented Databases (OODBs) under varying schema complexities and workload sizes. It specifically probes how database structure and clustering policies affect response times and I/O efficiency. Use when the user wants to benchmark on OCB (Object Clustering Benchmark), or asks about evaluating this task. Reports average response time.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1611.09172
  bibtex_key: darmont2016benchmarking
  confidence: high
---

# ocb-eval

> Benchmarking OODBs with a Generic Tool — Darmont et al. (2016) (arXiv:1611.09172, 2016)

## What this evaluates

Evaluates the performance and scalability of Object-Oriented Databases (OODBs) under varying schema complexities and workload sizes. It specifically probes how database structure and clustering policies affect response times and I/O efficiency.

## Datasets

- **OCB (Object Clustering Benchmark)** — total ?; splits: default (-1)

## Metrics

- `average response time` **(primary)** — range: other
  - Mean wall-clock execution time per transaction, computed over 100 replications.
- `average number of I/Os` — range: other
  - Mean count of disk input/output operations required to execute a transaction, averaged over 100 replications.

## Input / output format

**Input**: Synthetically generated object-oriented database schema defined by parameters: number of classes (NC), number of instances (NO), and maximum inter-object references (MAXNREF), along with a predefined workload of transactions (e.g., hierarchy traversals).

**Output**: Numerical performance measurements: average response time (ms), average I/O count, database generation time (s), and final database size (MB).

## Scoring recipe

```python
# For each configuration (NC, NO, MAXNREF):
1. Generate object base using OCB parameters
2. Execute workload transactions on the target OODB
3. Record response time and I/O count per transaction
4. Repeat steps 2-3 exactly 100 times
5. Compute mean(response_times) and mean(io_counts)
6. Report generation time and final disk size
```

## Common pitfalls

- Directly comparing performance across different OODBs without controlling for hardware, OS, or system features (e.g., concurrency, security overhead).
- Assuming I/O count directly correlates with response time across all systems, as higher-level features can decouple disk access from wall-clock time.

## Evidence (verbatim from paper)

> The scope of this study is limited raw performance results, i.e., the average response time and the average number of I/Os necessary to execute the operations. Note: All our experiments have been replicated 100 times so that mean tendencies could be assessed.

## Citation

```bibtex
@misc{darmont2016benchmarking,
  title={Benchmarking OODBs with a Generic Tool},
  author={Darmont et al. (2016)},
  year={2016},
  note={arXiv:1611.09172}
}
```

- arXiv: 1611.09172
