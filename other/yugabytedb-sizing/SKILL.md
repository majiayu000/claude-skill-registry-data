---
name: yugabytedb-sizing
description: >
  Calculate and recommend optimal YugabyteDB cluster sizing based on workload inputs. Use this
  skill whenever the user asks about YugabyteDB cluster sizing, capacity planning, node count,
  vCPU requirements, storage sizing, memory recommendations, or wants to know how many nodes
  they need for a given workload. Trigger when user mentions "size my cluster", "how many nodes",
  "YugabyteDB capacity", "YugabyteDB hardware requirements", QPS with YugabyteDB, or asks about
  CPU/storage/memory for a YugabyteDB deployment. Also trigger when the user provides workload
  metrics (QPS, read/write ratio, table size) and asks for infrastructure recommendations.
  Covers both YSQL (PostgreSQL-compatible) and YCQL (Cassandra-compatible) APIs.
---

# YugabyteDB Cluster Sizing Calculator

Size a YugabyteDB cluster from workload inputs: node count, vCPU, memory, storage, IOPS, disk
throughput, network and failure resilience, targeting ≤65% CPU. **Always run the bundled script**
(`scripts/sizing_calc.py`) — never compute by hand.

Rules:
- RF must be 1, 3, 5 or 7 (the script rejects others). Never recommend RF=1 for production.
- **Always state that the sizing is indicative** and that the user should test with their actual
  workload to fine-tune production sizing.
- CPU comes from measured CPU cost per operation (TPC-C, sysbench and YCQL benchmark runs), not
  from latency. Details: [references/cpu-model.md](references/cpu-model.md).

## Workflow

1. **Pick the API.** `--api ysql` (default) or `--api ycql`. Cassandra, CQL, port 9042, partition
   keys or TTL → YCQL; PostgreSQL, SQL, joins or port 5433 → YSQL. Ask if unclear.
2. **Gather inputs** (table below). Ask for the required ones; use defaults for the rest.
3. **Choose the CPU basis, best first:**
   1. *Calibration* — if the user has a running cluster or PoC with a similar mix, ask for its QPS
      and average CPU% (`--observed-qps`, `--observed-cpu-pct`; plus `--observed-nodes` /
      `--observed-vcpu-per-node` if its shape differs from the target).
   2. *Workload profile* — pick `--workload` from the user's description of their queries.
   3. Only if neither is available, let the script auto-select a profile from the read/write mix,
      and say so in the answer.
4. **Run the script.** For production, add `--size-for zone`. When the node size is open, use
   `--compare 8,16,32` instead of `--vcpu-per-node`.
5. **Present the result** (see *Presenting results*), including every ⚠️ warning the script prints.

## Inputs

| Input | Required? | Flag | Notes |
|---|---|---|---|
| API | Required | `--api` | `ysql` (default) or `ycql` |
| QPS **or** TPS | Required | `--qps`, or `--tps` + `--statements-per-txn` | Peak statements/s, or transactions/s × statements per transaction |
| Transaction mix | Recommended | `--statements-per-txn`, `--distributed-txn-pct` | Multi-statement transactions are distributed (commit + intents); single-statement ones use the fast path |
| Write % / Read % | Required | `--write-pct`, `--read-pct` | Must sum to 100 |
| vCPU/node | Required | `--vcpu-per-node` or `--compare 8,16,32` | Cap at 32–64 cores per node |
| RF | Required | `--rf` | Default 3 |
| Table size (GB) | Required | `--table-size-gb` | Raw, uncompressed |
| Workload profile | Recommended | `--workload` | YSQL: `kv` (point ops), `oltp` (transactional, indexed), `complex` (joins/aggregations), `analytics` (scans). YCQL: `point`, `range`, `lwt` (LWT or indexed writes) |
| Observed QPS + CPU% | Recommended | `--observed-qps`, `--observed-cpu-pct` | Calibration from a running cluster — the most accurate basis |
| Avg latency (ms) | Optional | `--avg-exec-ms` | Not used for CPU; feeds the concurrency check (in-flight vs backends) |
| Topology | Optional | `--zones`, `--regions`, `--preferred-region`, `--region-rtt-ms` | Multi-AZ (zones = RF) is the default; `--zones 1` for single AZ; `--regions 3` for a synchronous multi-region cluster (one replica per region) |
| Write pipelining | Optional | `--write-pipelining` | **YSQL only**: `ysql_enable_write_pipelining` (GA in 2026.1.2, off by default) — writes replicate in the background and a transaction pays ~2 round trips at COMMIT instead of one per write. Latency only; CPU unchanged |
| Read offload | Optional | `--follower-read-pct`, `--read-replica-read-pct`, `--read-replica-rf` | Share of reads that tolerate bounded staleness, served by followers or a read-replica cluster |
| Disk limits | Optional | `--disk-iops`, `--disk-mibps` | Default gp3 max (16,000 IOPS, 1,000 MiB/s); nodes are added to fit. Pass NVMe/io2 limits if used |
| Avg row size | Optional | `--avg-row-bytes` | Default 512; drives WAL, disk and network |
| Data growth | Optional | `--growth-rate-pct` | Default 30%/yr |
| xCluster | Optional | `--xcluster` | +10% CPU, 24 h WAL retention |
| CDC | Optional | `--cdc` | **YSQL only**: +5% CPU, 8 h WAL retention |
| Objects (tables + indexes) | Optional | `--num-objects` | Schema tablet floor; YCQL secondary indexes are tables |
| TTL | Optional | `--ttl-days` | **YCQL only**: caps storage growth at the TTL steady state |
| Connection Manager | Optional | `--connection-manager` | **YSQL only**: 10 backends/vCPU, ~10 clients/backend |
| CPU architecture / hardware | Optional | `--cpu-arch arm`, `--cpu-cost-scale` | Graviton ×1.10; older hardware ~1.15 (m6i) to ~1.5 (m5/c5/i3) |

All other parameters and their defaults: [references/defaults.md](references/defaults.md).

## Running the script

```bash
# Typical YSQL sizing
python3 scripts/sizing_calc.py --qps 10000 --write-pct 30 --read-pct 70 --workload oltp \
  --vcpu-per-node 16 --rf 3 --table-size-gb 500 --size-for zone

# YCQL
python3 scripts/sizing_calc.py --api ycql --qps 100000 --write-pct 30 --read-pct 70 \
  --workload point --vcpu-per-node 16 --rf 3 --table-size-gb 500

# Calibrated from a running cluster (observed shape defaults to RF nodes × target vCPU)
python3 scripts/sizing_calc.py ... --observed-qps 8000 --observed-cpu-pct 40 \
  [--observed-nodes 6 --observed-vcpu-per-node 8]

# Compare node sizes (replaces --vcpu-per-node; with --compare, pass --observed-vcpu-per-node too)
python3 scripts/sizing_calc.py ... --compare 8,16,32 --size-for zone

# NVMe / io2 instead of gp3
python3 scripts/sizing_calc.py ... --disk-iops 200000 --disk-mibps 4000

# Single AZ, Graviton, previous-gen hardware, Connection Manager, xCluster
python3 scripts/sizing_calc.py ... --zones 1 --cpu-arch arm --cpu-cost-scale 1.15 \
  --connection-manager --xcluster

# YCQL with TTL
python3 scripts/sizing_calc.py --api ycql ... --ttl-days 30

# Transactions: 3,000 TPS of 6-statement transactions (QPS = 18,000; distributed by default)
python3 scripts/sizing_calc.py --tps 3000 --statements-per-txn 6 --write-pct 30 --read-pct 70 --workload kv ...

# Multi-region (3 regions, one replica each), leaders pinned to the app's region, 40% follower reads
python3 scripts/sizing_calc.py ... --regions 3 --preferred-region --region-rtt-ms 40 --follower-read-pct 40

# Same, with write pipelining (multi-statement transactions across regions)
python3 scripts/sizing_calc.py ... --regions 3 --preferred-region --write-pipelining

# Read-replica cluster for 30% of reads (e.g. remote-region reporting)
python3 scripts/sizing_calc.py ... --read-replica-read-pct 30 --read-replica-rf 1
```

**Output format**: `--format text` (default) for the answer; `--format html > sizing.html` when the
user wants a shareable report (self-contained page — write it to a file and give the path);
`--format json` for programmatic use.

**Comparison logic** (`--compare`): among node sizes that meet the CPU target and survive a zone
loss, take those within 10% of the lowest total vCPU and pick the one with the fewest nodes.

## Presenting results

Lead with the recommendation (nodes × vCPU, RAM and storage per node), then:
- **CPU basis**: calibrated, or which workload profile was used — and if it was auto-selected,
  say so and ask the user to confirm.
- **Failure resilience**: CPU after losing a node and a zone. If a zone loss exceeds 65%,
  recommend `--size-for zone` (or show its result).
- **What constrains the size**: CPU, storage cap, disk limits or failure headroom. When disk adds
  nodes, present the choice of more gp3 nodes vs fewer NVMe/io2 nodes.
- **Disk and network**: IOPS and MiB/s to provision per node; cross-AZ traffic and its monthly
  cost for multi-AZ clusters.
- **Concurrency**: if latency was given and the workload is connection-bound, recommend more
  nodes or Connection Manager. In multi-region layouts the effective latency includes the
  cross-region round trips the script adds.
- **Multi-region**: added latency per statement; with `--preferred-region`, the leader-region vs
  follower-region CPU and the fact that every region is sized to take over leadership. For YSQL
  the report also shows the latency with write pipelining — recommend
  `ysql_enable_write_pipelining=true` (2026.1.2+, set on every yb-master and yb-tserver) when
  multi-statement write transactions cross regions or the workload is connection-bound.
- **Transactions and read offload**: distributed-transaction CPU, and the read-replica cluster
  (nodes, RAM, storage) as a separate line item.
- **Storage growth**: 1- and 2-year storage per node.
- **Deployment notes** the script prints (YCQL memory flags, Connection Manager flags).
- The indicative-sizing disclaimer.

## Edge cases

- **Minimum cluster**: RF nodes. Scale out in multiples of RF.
- **Read-heavy or remote-region reads**: if reads tolerate bounded staleness (30 s default),
  model follower reads (`--follower-read-pct`) or a read-replica cluster (`--read-replica-read-pct`).
  Both need read-only transactions with `yb_read_from_followers` (YSQL) or consistency ONE (YCQL).
- **Multi-region choices**: a synchronous stretch cluster (`--regions`) pays a cross-region round
  trip on every write; for active-active with async replication, size each xCluster universe
  separately with `--xcluster`; for geo-partitioned data, size each region's partition separately.
- **Transactions**: single-statement writes use the fast path; any `BEGIN … COMMIT` block with
  writes is a distributed transaction (`--statements-per-txn` > 1 assumes so). The `oltp` profile
  already includes TPC-C's distributed-transaction cost, so the overhead is added only to the
  fast-path profiles (YSQL `kv`, YCQL `point`/`range`).
- **Bursty workloads**: size for peak QPS; add headroom or plan for horizontal scaling.
- **YCQL secondary indexes**: each index is a table (`--num-objects`) and requires
  `transactions = {'enabled': true}` — use `--workload lwt`.
- **YSQL + YCQL on one cluster**: size each workload separately and add the vCPUs; keep
  `use_memory_defaults_optimized_for_ysql=true` if YSQL is used.
- **Connection Manager client count**: if the user states expected client connections per node,
  pass `--cm-client-ratio` ≈ clients ÷ backends (e.g. 2,000 ÷ 160 → 13); it sets reported
  capacity only — CPU and RAM follow the backend pool.
- **Kubernetes**: StatefulSets, one pod per node; match pod requests to the per-node figures.
- **Large nodes**: use the `latency-performance` tuned profile on 32/64-core machines.
- **Managed / cloud instances**: match to available shapes (e.g. r6g.4xlarge = 16 vCPU / 128 GB).
- **Data sources**: the YSQL costs come from single-AZ runs; the YCQL costs from older hardware
  scaled ×0.6. Calibrate from the user's own cluster whenever one exists.

## References

- [references/cpu-model.md](references/cpu-model.md) — CPU cost model, measured sources, workload
  profiles, calibration, capacity per node
- [references/methodology.md](references/methodology.md) — step-by-step formulas for every output
- [references/defaults.md](references/defaults.md) — every default and its flag
- [references/examples.md](references/examples.md) — worked YSQL and YCQL examples

Tests (for maintainers): `python3 -m unittest discover -s tests -v` from the skill directory.
Golden files in `tests/golden/` pin reference scenarios and benchmark reproductions; after an
intentional model change, run with `UPDATE_GOLDEN=1` and review `git diff tests/golden/`.
