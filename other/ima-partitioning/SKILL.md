---
name: ima-partitioning
description: "Use when sizing an ARINC 653 partition schedule, writing the partition configuration table, or reviewing inter-partition communication ports against frame, period, and latency budgets for certification. Compute and validate ARINC 653 integrated modular avionics (IMA) partition configurations: check partition schedule feasibility by summing the partition durations within the major frame and verifying that each partition receives its period slot, build the partition configuration table from frame and window data, bound sampling port and queuing port message latency for inter-partition communication, and scope the health monitoring responsibilities for fault detection and recovery. Trigger: ARINC 653, IMA, partition scheduling, major frame, MAF, sampling port, queuing port, inter-partition communication, health monitoring."
license: Apache-2.0
compliance: STANDARDS-REF
standards:
  - id: do-178c
    reference-only: true
gated: false
domain: avionics
pack: avionics
compatibility: "agentskills.io SKILL.md; any SKILL.md host (Claude Code, Hermes, OpenClaw)"
metadata:
  domain: avionics
  subdomain: ima
  tags: [arinc-653, ima, partition, partitioning, major-frame, maf, sampling-port, queuing-port, inter-partition-communication, health-monitoring, partition-configuration-table]
  version: 0.1.0
  author: Aero Agent Skills
---

# ARINC 653 IMA Partitioning (avionics/ima/ima-partitioning)

Use when the task is integrated modular avionics (IMA) partitioning for
civil avionics: ARINC 653 partition schedule feasibility, the partition
configuration table, inter-partition communication through sampling
and queuing ports, and health monitoring responsibilities. The module is
data-driven: you supply the major frame (MAF) duration and the partition
list with window durations and periods, and the functions compute the
frame load, the utilization, the slack, and the feasibility verdict, then
bound the sampling and queuing port latencies.

## Domain quick reference

- ARINC 653 defines partitioning for IMA: applications run isolated from
  one another in partitions, each with its own memory space and its own
  schedule windows on the processor.
- A partition configuration table assigns each partition a window
  duration d and a period p inside a repeating major frame (MAF) of
  duration M; the MAF must be a common multiple of every period so the
  cyclic schedule repeats evenly (period divides the MAF).
- Frame load: each partition with period p executes M / p windows per
  frame, so the allocated time per frame is the sum of d x (M / p).
  Worked: MAF 40 ms with partitions of 10 ms at period 20 ms and 15 ms
  at period 40 ms allocates 20 + 15 = 35 ms, utilization 0.875, slack
  5 ms, feasible.
- Feasibility: the frame load must not exceed the MAF (equivalently the
  utilization sum of d / p must be at most 1), and each window duration
  must fit inside its own period slot. Worked: MAF 40 ms with windows
  10, 20, and 15 ms at period 40 ms allocates 45 ms, an over-subscribed
  frame that is infeasible.
- Sampling ports carry the latest message (freshness semantics): a new
  message overwrites the previous one, and the receiver reads whatever
  is current. Worst-case latency is one sending period plus the wire
  transmission time of the message. Worked: 100-byte message at 100
  Mbps takes 0.008 ms on the wire; a 10 ms sampling period gives 10.008
  ms worst-case latency.
- Queuing ports carry messages in FIFO order with a bounded queue depth.
  Worst-case latency is the queue depth times the sending period plus
  the transmission time of the final message. Worked: depth 4 at 10 ms
  with the same message gives 40.008 ms.
- Health monitoring responsibilities: each partition monitors its own
  execution, the module monitors partition states and the schedule, and
  faults are reported to the health monitor, which runs the configured
  recovery action for the fault level.
- The exact ARINC 653 configuration rules, window arithmetic, port
  attributes, and health monitor behavior are revision-specific standard
  data; confirm them against the current revision before freezing a
  partition configuration table.

## Workflow

1. Collect the MAF duration and, for each partition, its name, window
   duration, and period.
2. Run schedule_feasibility(maf_ms, partitions): the function validates
   the inputs, checks every period against the MAF and every duration
   against its period slot, sums the frame load, and returns the
   verdict with the utilization and the slack.
3. An infeasible verdict lists the violations: re-tune durations,
   periods, or the MAF until the frame load fits and every slot is
   legal.
4. Wrap the accepted schedule in a PartitionSchedule object to keep the
   frame, load, utilization, slack, and violations together for the
   configuration record.
5. For each inter-partition communication path, choose the port type:
   sampling_port_latency_ms for freshness traffic and
   queuing_port_latency_ms for FIFO traffic, passing the sending
   period, the message size, the link bit rate, and (for queuing) the
   queue depth. A message larger than the port capacity raises
   ValueError.
6. Record the partition configuration table (MAF, per-partition window
   and period, frame load, slack) and the port latency bounds for the
   certification package and the integrator.
7. Confirm the health monitoring responsibilities for the module: which
   faults are detected in each partition, where they are reported, and
   which recovery action runs for each fault level.

## Pitfalls

- Routing this leaf: ARINC 653 partition scheduling and IPC ports are
  this leaf; a 429 word decode routes to arinc429-protocol, a virtual
  link bandwidth question routes to arinc664-afdx, and a MIL-STD-1553
  command/response bus routes to mil-std-1553. A partition schedule is
  not a data bus question.
- Confusing the MAF with a frame size: the major frame is a time
  interval (milliseconds) that repeats; it is not a byte count and not
  a network frame.
- A period that does not divide the MAF: the cyclic schedule cannot
  repeat evenly, so the configuration is invalid even when the load
  looks small.
- A window duration larger than its own period: the partition cannot
  finish one execution before its next slot starts.
- Over-subscription: the frame load must fit the MAF; a set that
  allocates more than the frame is re-tuned, not force-fitted.
- Sampling versus queuing semantics: sampling ports overwrite (latest
  wins), queuing ports preserve order; applying freshness semantics to
  a queuing path, or FIFO ordering to a sampling path, mis-states the
  latency bound.
- Treating the configuration as fixed: window arithmetic, port
  attributes, and health monitor behavior are revision-specific
  standard data; confirm every value against the current revision
  before freezing the table.

## Behavior contract (gate 3)

The partition schedule feasibility, sampling port latency, queuing port
latency, and transmission time helpers are exercised by the gate 3
contract test: scripts/test_ima_partitioning.py against
scripts/ima_partitioning_logic.py (stdlib unittest, offline). Run:
python3 scripts/test_ima_partitioning.py

## Compliance

- Standards referenced, not reproduced: the ARINC 653 text is
  proprietary (ARINC/SAE ITC) and is not yet in standards-map.yaml;
  this leaf keys to the closest existing map entry, do-178c (IMA
  software and robust partitioning are DO-178C topics), listed
  reference-only. Summary only per standards-map.yaml.
- The module implements the schedule arithmetic, port latency, and
  health monitoring scoping from common engineering practice; no
  standard table is embedded in the code or this page.
- compliance: STANDARDS-REF, gated: false.
