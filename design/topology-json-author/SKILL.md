---
name: topology-json-author
description: Author and validate DSDS TopologyJSON from architecture descriptions, diagrams, or UI node and edge exports. Use when converting designs into simulator-ready JSON, selecting valid component types, filling queue/workload/fault fields, and checking structural consistency before simulation.
---

# Topology Json Author

## Overview

Convert architecture intent into valid, deterministic `TopologyJSON` that the DSDS simulation engine can run. Produce complete topology objects, explicit assumptions, and clear validation notes before simulation starts.

## Workflow

1. Collect inputs
- Read the architecture description, existing topology JSON, or canvas export.
- Identify explicit constraints: latency goals, availability/SLOs, providers, workload shape, and failure hypotheses.
- Capture unknowns in an assumptions list instead of leaving fields implicit.

2. Build the skeleton first
- Create `id`, `name`, `version`, `global`, `nodes`, `edges`, `workload`, `faults`, `invariants`, and `scenarios`.
- Set deterministic controls immediately: `global.seed`, `global.simulationDuration`, and `global.warmupDuration`.

3. Materialize nodes and edges
- Map every component to a valid `type` from the DSDS taxonomy.
- Populate node queueing and processing basics: `queue.workers`, `queue.capacity`, `processing.distribution`, and `processing.timeout`.
- Populate edge transport basics: `mode`, `protocol`, `latency.distribution`, `bandwidth`, and `packetLossRate`.

4. Add workload, faults, and invariants
- Choose a workload pattern that matches traffic behavior (`constant`, `poisson`, `spike`, `diurnal`, `bursty`, `sawtooth`, `replay`).
- Add high-signal fault specs first; expand only if needed.
- Encode invariants tied to the user's goals (availability, latency, consistency, security).

5. Validate before returning
- Enforce structural and semantic checks from `references/topology-json-rules.md`.
- Return the final JSON plus assumptions and validation warnings.

## Output format

Use this order unless the user asks otherwise:
1. `TopologyJSON`
2. `Assumptions`
3. `Validation notes`
4. `Follow-up questions` (only if blockers remain)

## References

- Read `references/topology-json-rules.md` for required fields, DSDS checks, and a minimal starter template.
- Use these repo sources as ground truth:
- `planning/IMPLEMENTATION_PLAN.md` (Phase 0 contract)
- `schema/complete_simulator_schema.ts` (type vocabulary)
- `canonical-catalogue/*.csv` (taxonomy, failures, invariants)
