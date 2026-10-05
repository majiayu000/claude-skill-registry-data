---
name: optimize-chisel-fpga-timing
description: Diagnose and optimize timing-critical Chisel RTL for FPGA implementation while preserving cycle semantics. Use for Vivado timing bottlenecks, long ready or admission paths, queue and issue selection, free-list bank mapping, priority encoders, one-hot arbitration, wide muxes, late-arriving forwarding or override data, high-fanout controls, cross-module predicates, register-boundary changes, emitted-Verilog inspection, or routed-DCP A/B analysis. Also use when a source-level simplification needs proof that it changes timing without changing architectural state.
---

# Optimize Chisel FPGA Timing

Optimize from cycle contracts and implementation evidence. Treat a source edit as a timing hypothesis until emitted RTL and routed implementation data confirm it.

## Establish authority and scope

1. Read repository instructions, design documents, current RTL, module-local notes, tests, and existing timing reports.
2. Separate target behavior, current implementation, reference implementation, and proposed optimization.
3. Freeze the requested edit boundary. Preserve backups and independent experiment directories.
4. Record source revision, configuration, clock constraint, synthesis and implementation strategy, seed, DCP identity, and report paths.

Do not add pipeline latency, table-entry fields, interfaces, or conservative guards without authorization. A timing edit that changes fire timing, ordering, visible latency, or flush behavior is a microarchitecture change and requires explicit approval.

## Freeze the cycle contract

For every affected signal, state:

```text
producer
consumer
combinational expression
register boundary
valid interval
fire condition
hold requirement under backpressure
flush and reset behavior
same-cycle state updates
```

Classify each condition as one of:

- `state-changing`: directly enables allocation, issue, write, release, or architectural effects;
- `admission-only`: only decides whether work may enter;
- `data-select`: chooses data or an index;
- `assertion-only`: checks an upstream contract.

This classification controls which conditions may be removed, delayed, replicated, or converted into registered hints.

## Build an evidence-backed path model

Use the strongest available evidence:

1. Routed DCP path and utilization reports.
2. Post-route netlist and primitive mapping.
3. Post-synthesis netlist.
4. Emitted SystemVerilog.
5. Chisel source topology.

When a routed DCP exists, expose the path stage by stage. Record source and destination pins, requirement, slack, logic delay, route delay, logic levels, primitive sequence, net fanout, sites, and hierarchy crossings. Query related control, incoming, outgoing, and feedback paths.

For a proposed register-boundary move, always inspect this matrix:

```text
old end-to-end path
new register D-input path
new register Q-output path
state feedback or maintenance path
control path to enable/reset/flush
```

Do not infer causality from high fanout, source hierarchy, LUT count, or global WNS alone. Placement and route delay can dominate a logically shallow cone.

Read [vivado-evidence.md](references/vivado-evidence.md) before making measured timing claims.

## Select the smallest topology change

Read [rtl-patterns.md](references/rtl-patterns.md), then choose the narrowest applicable pattern:

|Observed topology|Preferred first experiment|
|---|---|
|Current bank state plus phase mux drives `valid` or `ready`|Expose next-state availability and register the next mapped result|
|Priority selection plus age wrap sits on an output path|Register priority results computed from the same next-state version as the entries|
|Wide line or Bundle mux precedes narrow extraction|Extract required slices in parallel, then mux the narrow values|
|A wide mux precedes the same pure transform on either selected value|Apply the transform to each candidate in parallel, then mux the narrower results|
|Full-width equality or transport is only needed inside a known address or identity region|Carry and compare a compact representation plus an explicit alias-boundary guard|
|Aligned `Mux1H` results feed a shared arithmetic operation, and the selector is derived from the same late source|Compute the operation per candidate in parallel, then use the one-hot selector on the final results|
|Late forwarding or override data is selected before an operation-class mux|Build the ordinary class-selected base in parallel, then use the late candidate as one qualified final override|
|Global tag or ROB-head compare feeds every issue candidate|Capture a local per-entry predicate one cycle earlier|
|A registered update is reconstructed from stable identity fields plus a late acceptance signal|Register the stable update identity at its producer boundary and keep only the late acceptance gate combinational|
|Small fixed dispatch width uses `PopCount`, dynamic shifts, or serial selection|Enumerate fixed count classes and precompute OH rotations|
|An invalid-lane condition only affects admission|Remove it only after proving every state mutation remains fire-gated|
|A late transaction-valid signal drives synchronous RAM read enable, while unused read data has no side effect|Drive the read from stable port ownership and qualify all downstream state changes with the separately pipelined valid|
|A rare global flush or recovery event has a long combinational source-to-consumer path, and consumers can legally observe it one cycle later|Register the complete event bundle, delay all coupled payloads together, and prove the intervening cycle cannot create an irreversible side effect|
|An already registered flush or global control has route-dominated fanout across distant consumer regions|Create same-edge registered replicas, partition consumers by physical region, and verify that synthesis preserved the replicas|
|Zero-mask special case wraps `PriorityEncoderOH`|Use the encoder's natural zero output|
|`Mux(selOH.orR, Mux1H(selOH, data), 0.U)` wraps a one-hot-or-zero selector|Use `Mux1H` directly after proving zero-hot must produce zero and the outer predicate adds no kill or hold semantics|
|Wide internal Bundle carries unused fields|Rely on firtool dead-code elimination after checking emitted RTL|

Prefer balanced trees, masks, one-hot selection, local state, fixed-width cases, and explicit register boundaries. Mux only fields consumed on the critical path.

## Check every register-boundary move

A useful register cut must satisfy all of these:

1. The registered fact is derivable one cycle early.
2. Data, selector, validity, and identity come from the same logical state version.
3. Backpressure stability remains valid.
4. Flush and reset initialize the new register consistently.
5. The new D-input maintenance cone is acceptable.
6. The new Q-output cone is shorter at the real consumer.
7. Feedback does not recreate the original path through another route.

Registering a final result can overload its D input. Registering smaller intermediate results can balance D-side and Q-side delay. Compare both structures in RTL or isolated synthesis before choosing.

## Implement and prove semantic equivalence

Make the minimum source edit. Add assertions for the contract that makes the optimization legal:

```scala
assert(PopCount(selOH) <= 1.U)
assert((allocMask & ~fireMask) === 0.U)
assert(!stateWrite || requestValid)
```

Adapt names and widths to the module. Do not add runtime muxes solely to duplicate an invariant already guaranteed upstream.

Inspect emitted SystemVerilog before a full implementation run:

- confirm the targeted LUT, mux, comparator, encoder, or dependency chain changed;
- confirm unused Bundle fields and registers were removed;
- confirm state writes remain gated by the intended fire event;
- search for accidental serial priority chains and duplicated wide compares;
- verify reset, flush, and valid logic survived as intended.

Run focused Verilator tests covering normal traffic, empty/full boundaries, sparse lanes, simultaneous events, backpressure, flush, reset, and assertions. Use symmetric tests that compare the old and new designs when practical.

## Re-run implementation and compare

Use the same configuration and constraints for A/B comparison. Re-query the exact old path and all new boundary paths. Report:

- path delay and slack changes;
- logic and route delay separately;
- level and primitive changes;
- endpoint migration;
- LUT, FF, BRAM, and hierarchy movement;
- functional test evidence;
- any placement, strategy, or seed differences.

Treat fixed-DCP frequency calculations as estimates. A positive WNS under one constraint proves closure at that constraint and does not prove the maximum frequency. A generated bitstream with negative WNS is still a timing failure.

Read [case-studies.md](references/case-studies.md) for project-derived examples and failure modes.

## Deliver

Report concisely:

1. Original path, stage-by-stage delay, and dominant logic or routing segment.
2. Cycle contract and proof that the edit preserves it.
3. Source files and exact topology change.
4. Added assertions and deliberately omitted redundant guards.
5. Emitted-RTL evidence.
6. Verilator commands, seeds, results, and logs.
7. Routed A/B evidence with D-side, Q-side, feedback, and control paths.
8. Resource cost and remaining bottleneck.
9. Unverified claims and the artifact required to verify them.
