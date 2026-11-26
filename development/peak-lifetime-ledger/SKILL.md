---
name: peak-lifetime-ledger
description: Use when mapping ecdsa.fail q1152/lower peak-qubit pressure, especially Trailmix/Ludicrous fold, add, codec, and GCD phases, before editing or scaling compute.
---

# Gipfelbuech (peak-lifetime-ledger)

## Job

Turn trace output into a concrete list of live-state pressure points. Use this
before structural edits so a candidate is tied to the exact phase, callsite,
register family, and Toffoli cost that creates the q1153/q1152 wall.

## Required Inputs

Run from an isolated route tree:

```bash
TRACE_TLM_PROFILE=1 \
TRACE_TLM_FOLD=1 \
TRACE_TLM_FOLD_ALLOC=1 \
TRACE_TLM_PHASE_COST=1 \
TRACE_TLM_PHASE_COST_REGIONS=1 \
./target/release/build_circuit >/tmp/peak_build.log 2>/tmp/peak_trace.err
```

If transcript/tape overlap matters, also run:

```bash
TRACE_PHASE_ACTIVE=1 TRACE_PHASE_ACTIVE_TOP=40 TRACE_TLM_TAIL=1 \
./target/release/build_circuit >/tmp/tape_build.log 2>/tmp/tape_trace.err
```

## Ledger Fields

Record each pressure point as:

```text
phase=<name> peak_q=<n> op_idx=<n> emitted_ops=<n>
callsite=<function/region> live=<register families/qid bands>
ccx=<n> ccz=<n> tape_bits=<n> fold_chunk=<n>
candidate=<what could be delayed/loaned/re-encoded>
proof_obligation=<why it remains value/phase/ancilla exact>
```

## Rules

- Do not edit from a vague "peak is high" claim.
- Prioritize peaks where a single resident family can be delayed, hosted, or
  streamed without adding more Toffoli than the target q tier can afford.
- Separate qubit pressure from Toffoli pressure. A route can be lower-Q and
  still lose Q*T.
- Treat count-only deltas as candidate evidence only.

## Output

Write the ledger to the lane state directory and post the top three pressure
points to the team channel with the next falsifiable check.
