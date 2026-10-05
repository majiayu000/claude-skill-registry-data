---
name: trace-vivado-timing-to-rtl
description: Forensic analysis of Vivado synthesis and routed timing evidence for processor RTL. Use when Codex must trace setup or hold paths at primitive, LUT, CARRY, BRAM, DSP, MUXF, register, and routed-net granularity; map physical stages back to Chisel, Scala, Verilog, pipeline events, and path families; explain logic versus routing pressure; quantify which stages a proposed change can remove or move; identify missing DCP queries; or write an evidence-backed timing report. This skill is read-only by default and stops at ranked modification directions. Use optimize-chisel-fpga-timing for RTL edits, cycle-contract proof, functional verification, and routed A/B implementation closure.
---

# Trace Vivado Timing to RTL

Build a measured map from Vivado physical timing paths to processor RTL and produce modification directions without changing the design.

## Keep the boundary clear

Use this skill for timing forensics and reports:

```text
Vivado reports or routed DCP
  -> path families
  -> primitive and net stages
  -> RTL and pipeline meaning
  -> structural opportunities and risks
```

Use `optimize-chisel-fpga-timing` when the task proceeds to:

```text
cycle-contract proof
RTL edits
assertions and Verilator tests
emitted-RTL comparison
routed A/B closure
```

For a combined request, complete this forensic workflow first, freeze the evidence, then hand the ranked candidate to the optimization skill.

## Read authority and artifacts

1. Read repository instructions, target design documents, current RTL, generated RTL, and the report directory rules.
2. Identify the exact run: source revision, dirty state, parameters, top, device, Vivado version, clock, constraints, strategy, directive, seed, and DCP hash.
3. Treat the routed run as immutable evidence. Compare current source hashes with the run manifest before using current source for semantic mapping.
4. When source has drifted, use the run snapshot, generated RTL, configuration manifest, routed netlist, and DCP. Mark any current-source mapping as unverified.
5. Prefer routed DCP evidence. Use post-place, post-synth, emitted RTL, or source only for questions their evidence level can answer.
6. Preserve raw reports and supplemental queries. Write analysis only to the user-designated report directory.

Read [evidence-and-queries.md](references/evidence-and-queries.md) when a DCP is available, reports are incomplete, or exact Tcl queries are needed.

## Build the path universe

1. Record global setup and hold closure separately.
2. Build an endpoint-worst setup universe with one path per endpoint and a stated delay or slack threshold. Record returned object count, query cap, and truncation status.
3. Summarize delay bins, endpoint pin types, setup violations, and route-ratio distribution before inspecting individual paths.
4. Preserve a raw Slack-sorted top list. Explain that the longest data path and worst Slack can differ because clock skew, uncertainty, CPR, and endpoint clock paths differ.
5. Extract paths by endpoint, startpoint, and logical family. Avoid a top-N list filled by bits of one bus.
6. Group by actual physical startpoint class, endpoint class, shared prefix, pipeline boundary, and event type. Do not assign ownership from the report filename.
7. Count each family and report maximum data delay, worst Slack, logic/route split, levels, endpoint count, and representative path.
8. State whether the family maximum data delay and worst Slack came from different endpoints.

Do not call a module absent from a top-N report timing-clean. Query it directly or mark it unmeasured.

## Compare implementations

When a prior comparable run exists:

1. Verify equal top, part, clock definition, constraints, strategies, shell, and architectural parameters.
2. Compare WNS, TNS, WHS, path counts above the threshold, data-delay distribution, route ratio, resource use, and power confidence.
3. Compare matching path families and register boundaries. Track families that entered, left, or changed position in the limiting set.
4. Attribute a change to RTL only when source identity and physical evidence support it. Treat isolated route changes as implementation variance.
5. Describe WNS migration explicitly. A lower path count can coexist with a worse WNS when a different family becomes limiting.

## Expand representative paths

Expand the global WNS path, the highest-count families, the longest-data families, and every user-targeted family. Retain at least one full physical path per selected family and record:

```text
source and destination pins
launch and capture clocks
requirement, slack, uncertainty, skew, CPR
data, logic, and route delay
logic levels and primitive counts
ordered primitive cells and sites
each following net delay and fanout
cumulative data delay
hierarchy crossings
endpoint pin type: D, CE, R, S, BRAM ADDR, EN, WE, DIN, or DOUT
```

Use one table row per primitive and pair the primitive with its following route. Include:

```text
ordinal, primitive, full cell or site
cell delay, following route delay
fanout, cumulative data delay
RTL region, semantic confidence
```

Run [extract_timing_path.py](scripts/extract_timing_path.py) on text reports to generate an initial stage table. Verify the selected block and every semantic label against the raw report.

## Map physical stages to RTL

Trace both directions:

1. From the startpoint, follow generated net names, cell inputs, and source fanout into the path.
2. From the endpoint, trace the consuming register, memory pin, enable, or reset back to its RTL assignment.
3. Search emitted SystemVerilog, current Chisel/Scala, configuration constants, and design documentation.
4. Partition the path into semantic regions such as decode, compare, overlay, arbitration, mux, add, correction, ready propagation, state maintenance, and memory control.
5. Mark every statement as one of:
   - `measured`: directly reported by Vivado;
   - `mapped`: connectivity, pin, INIT, or emitted RTL proves the function;
   - `inferred`: source-cone and consumer semantics bound the function to a region;
   - `unknown`: required evidence is missing.

Never infer a LUT's exact Boolean function from its optimized display name. Obtain cell `INIT`, input pins, driving nets, fanout, and generated-RTL correspondence when exact per-LUT attribution matters.

Read [rtl-mapping-and-reporting.md](references/rtl-mapping-and-reporting.md) for confidence rules and the report structure.

## Diagnose logic and routing

1. Report logic depth and route share independently.
2. Call a net high-fanout only from measured fanout evidence. Call high fanout causal only when that net appears on the path with a large route segment.
3. Record source and sink sites for long route segments. Check replication, hierarchy crossings, endpoint spread, congestion, control sets, and `DONT_TOUCH`.
4. Treat parallel cones as parallel even when separate reports expose each cone. A timing report shows one traversed arc, not all sibling cones in series.
5. Before claiming a mux or condition can move earlier, determine whether the controlling signal starts the path or joins it mid-cone. Moving a mid-cone side input may leave the measured source-to-endpoint level count unchanged.
6. Separate BRAM `DOUT`, `ADDR`, `EN`, `WE`, and `DIN` families. They have different optimization boundaries.

## Quantify modification directions

For every proposed change, identify the exact old physical boundary:

```text
targeted primitive levels
targeted route segments
old cumulative delay to the cut point
remaining measured suffix after the cut point
path-family count covered
unaffected path families
new or migrated startpoint candidates
new D, Q, feedback, enable, reset, and flush paths that need measurement
```

Count removable logic levels separately from associated routes. A removed route is replaced by a new route after placement, so never subtract all old route delay as guaranteed gain.

For transformations that only precompute a mux selector, state whether the data mux remains. If it remains, guaranteed logic-level reduction can be zero even when fan-in and placement improve.

For a register cut, report the current suffix after the cut and request this matrix for the next run:

```text
old end-to-end path
new register D input
new register Q output
feedback or maintenance path
CE, reset, flush, and hold controls
```

Also measure the producer-side D cone before recommending the cut. A consumer path can improve while the new register D path becomes the next bottleneck.

## Rank recommendations

Rank directions using measured coverage and structural certainty:

1. Directly removes primitive levels from the current worst family.
2. Shortens a high-count shared prefix.
3. Reduces route width, fanout, or physical span with no guaranteed level removal.
4. Moves pressure to a measurable D or feedback cone.
5. Changes a pipeline, visibility, ordering, forwarding, or flush contract.

Separate low-risk topology edits from microarchitecture changes. Do not claim cycle equivalence in this skill. State the contract that the implementation agent must prove.

## Deliver

Write a Markdown report in the scheme/version directory. Follow this order:

1. Answer-first conclusions with closure verdict and current bottlenecks.
2. Run identity, configuration, source identity, and artifact hashes.
3. Evidence completeness, supplemental pulls, and source boundary.
4. Comparable-run differences and path-family migration.
5. Full path-universe distribution and endpoint types.
6. Raw Slack-tight paths.
7. Path-family counts and representative paths.
8. Per-primitive tables and source mapping for limiting families.
9. Targeted producer-side, consumer-side, and feedback boundary analyses.
10. High-fanout, route, congestion, constraints, methodology, and QoR findings.
11. Hierarchical resource use, resource delta, and qualified power data.
12. Ranked modification directions.
13. Missing evidence and exact DCP queries.
14. Raw report index and implementation handoff.

Keep measured facts, semantic mapping, inference, comparison, and recommendation visibly separate. Report no RTL modification or functional verification unless another workflow actually performed it.
