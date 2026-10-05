---
name: cost
description: This evaluation probes a containerized framework's capability to automate the deployment and execution of distributed big data workloads. It specifically measures how execution time and monetary cloud costs scale as the cluster size increases from four to eight nodes. Use when the user has predictions and gold and needs to compute cost.
metadata:
  skill_kind: metric
  source_arxiv: 1711.09138
  bibtex_key: ceesay2017papb
  confidence: high
---

# cost

> Plug and Play Bench: Simplifying Big Data Benchmarking Using Containers — Ceesay et al. (2017) (arXiv:1711.09138, 2017)

## What this evaluates

This evaluation probes a containerized framework's capability to automate the deployment and execution of distributed big data workloads. It specifically measures how execution time and monetary cloud costs scale as the cluster size increases from four to eight nodes.

## Datasets

- **HiBench Workloads (via PAPB)** — total ?; splits: (unstated); repo https://github.com/sneceesay77/papb

## Metrics

- `cost` **(primary)** — range: £
  - COST = Σ_{i=1}^{n} (CPM * T) / SEC_IN_MNT, where n is the number of nodes, CPM is the monthly VM cost in £, T is the workload runtime in seconds, and SEC_IN_MNT is the total seconds in a month (approximated to 30 days).
- `execution_time` — range: seconds
  - Total wall-clock time in seconds to complete a workload, averaged over three independent runs to reduce bias.

## Input / output format

**Input**: Distributed big data workloads (e.g., WordCount, PageRank, KMeans, Join, Scan, Aggregation, DFSIO) with predefined data sizes, deployed on a Dockerized Ubuntu cluster (4–8 nodes) on Microsoft Azure.

**Output**: Execution time in seconds and calculated monetary cost in £ per workload.

## Scoring recipe

```python
def compute_cost(num_nodes, cpm_per_month, runtime_seconds):
    sec_in_month = 30 * 24 * 3600  # ~2,592,000
    total_cost = 0.0
    for _ in range(num_nodes):
        total_cost += (cpm_per_month * runtime_seconds) / sec_in_month
    return total_cost
```

## Common pitfalls

- The cost model only accounts for compute VM runtime and ignores storage, network egress, and cloud provider pricing tiers.
- Results are specific to a single Azure region (US East) and VM SKU (STANDARD_DS14_V2), so costs do not generalize across clouds or regions.
- Only three runs are averaged per configuration, which may underrepresent variance typical in distributed big data systems.

## Evidence (verbatim from paper)

> To approximate the cost of running a workload we use the following relationship: COST = Σ_{i=1}^{n} (CPM * T) / SEC_IN_MNT where n = number of nodes, CPM is the cost (£) of a running VM per month, T is the total time taken in seconds to run a workload and SEC_IN_MNT is the total seconds in a month (approximated to 30 days).

## Citation

```bibtex
@misc{ceesay2017papb,
  title={Plug and Play Bench: Simplifying Big Data Benchmarking Using Containers},
  author={Ceesay et al. (2017)},
  year={2017},
  note={arXiv:1711.09138}
}
```

- arXiv: 1711.09138
