---
name: rtl-area-timing
description: Use when optimizing RTL microarchitecture for area or clock frequency (Fmax), a design is too big to fit or too slow to meet timing, a wide multiply or barrel shifter is the critical path, or a "compute everything and select" datapath is too large
---

# RTL Area and Timing Optimization

## Overview

Making RTL smaller or faster is a sequence of structural decisions, each justified by a measurement. The wins are rarely where intuition points: the giant is often a structure you didn't think of (a "ROM" that is really 94k flops), and the critical path is usually one specific primitive, not "logic depth" in general.

**Core principle:** Diagnose with data, change one structure, re-measure. Optimize the actual critical path or the actual giant, and stop the moment it stops being the bottleneck. Guessing wastes builds and can place worse.

## When to Use

- A design won't fit, or misses its timing constraint
- A wide multiply, barrel shifter, or big mux is suspected of dominating
- A microcoded or "compute all handlers and select" datapath is too large
- You're about to "optimize" something without having read the reports

This is the RTL-technique companion to `fpga-synthesis-fit` (the tool methodology for measuring). Measure there, transform here.

## Pipeline A Wide Multiply Internally

A single-cycle NxN multiply (64x64) maps to DSP tiles plus a long partial-product carry chain, and that chain is usually the critical path.

Registering only the multiply's OUTPUT does not break the internal carry chain; the operands-to-output path is still essentially the whole multiply. You must pipeline INTERNALLY: decompose into smaller products (four 32x32), register the partial products, then sum the shifted partials in a second registered stage. Make the op multi-cycle with a small stall counter. On ECP5 this took a 64x64 from about 33 MHz to about 47 MHz.

Registering the multiply INPUTS too gave diminishing returns and placed worse. Stop once the multiply leaves the critical path; re-read the report to confirm.

## Serialize A Wide Operator To Reclaim Area

Pipelining a multiply buys Fmax; SERIALIZING it buys area. Replace a single-cycle 64x64 multiply with a multi-cycle shift-add (radix-2^k, one small `wide * chunk` product per step reused across steps) and the whole partial-product reduction tree disappears, halving the DSP count. The same shape works for divide: one iterative restoring shift-subtract divider replaces eight combinational div/rem trees (which were 60% of an SoC) with a small datapath plus a stall counter, on the same resident-mopStep stall pattern as a multi-cycle FP op. On an area-first, latency-tolerant core this is close to free, and the serialized operator usually sits on the critical path too, so it buys Fmax as a side effect.

Correction to a common misread: a multiplier CAN be a post-pack area lever even when it looks tiny pre-pack. Its partial-product mux cells (PFUMX, L6MUX21) hide in the pre-pack LUT4 count but pack into slices post-pack, so an "only 843 LUT4, not worth it" judgement made pre-pack is wrong against `TRELLIS_COMB`. Measure post-pack (see the metric trap in `fpga-synthesis-fit`).

## Default Config Bloat: Size Generic IP To The Instance

A reusable peripheral sized by its default can dominate area on a small SoC. An interrupt controller defaulting to 32 sources, instantiated on an SoC with 3, builds a 32-wide priority and claim mux tree: one such block was 917 cells, about 16% of a small design, and dropped to 133 cells when sized to the real source count (`sources: devices.length + 1`). Audit every parameterized block's effective size against what the instance truly needs before hand-trimming RTL; the default is often the biggest single win and the easiest.

## "Compute Everything And Select" Is Area-Heavy

A microcoded exec or decoder that computes all handler datapaths in parallel and muxes the winner by opcode builds every handler's logic. Real area wins:

- **Remove unreachable/dead arms.** A memory-size case covering byte/half for atomics, when atomics only exist at word/dword, is dead logic. Provably correct, removes structurally-distinct logic, about 6% in one case.
- **Share a single resource** (one ALU, one memory port) routed by control signals.
- **Do not source-level deduplicate identical operand reads.** yosys already CSEs them, so it is a no-op for area. Only removing structurally-distinct logic (dead arms, different widths, a separate adder) actually shrinks the design.

## Variable Barrel Shift: Replace With Fixed-Slice Mux, But Measure

`addr >> (base + k*stride)` is a 64-bit barrel shifter plus a multiply. If it extracts a FIXED field per `k` (a page-table VPN[level] slice), replace it with a mux of fixed slices.

But on ECP5 this can be post-pack neutral: barrel shifters and mux trees pack to similar slice counts. It reduces pre-pack LUT4 but may not move `TRELLIS_COMB`. Measure post-pack before believing the win (see the metric trap in `fpga-synthesis-fit`).

## Share One Comparator Across Signed/Unsigned And Widths

Sign-extension from W to 2W bits is monotonic for BOTH signed and unsigned W-bit ordering (it maps the two halves of the W-bit range to two ordered ranges in the wider unsigned space). So one comparator on sign-extended operands computes signed min/max AND unsigned minu/maxu, useful for AMOs and ALUs.

Verify the stored RESULT width: compute at XLEN but store the low `size.bits`, and match the surrounding code's sign-vs-zero extension of the stored value. A test once caught a sign/zero-extend mismatch on the store side here.

## Verification Discipline That Paid Off

- **Build the optimized unit standalone first** with a golden test (bit-for-bit vs a reference) before wiring it in. De-risks correctness and locks the interface.
- **After every structural change, re-run the full functional matrix.** A cycle-accurate vs-reference matrix catches FSM/timing regressions a hand-picked test misses; it caught an off-by-one stall, a stale read, and an AMO store-extend bug. See `differential-verification`.
- **When you change the read latency of a shared memory, give the sim model the same latency as the FPGA primitive** so the matrix verifies real hardware behavior, not a faster sim variant.

## Spec "May" vs "Must": Don't Call Permissible Behavior A Bug

Before making hardware stricter to "fix" it, check whether the old behavior is permitted by the spec. Pre-Svade RISC-V PERMITS hardware page-table A/D-bit update; "always update A/D" is a legal implementation, not a violation. Making it Svade-strict (fault on A=0) is an ISA-policy choice tied to what the core advertises (Svadu/Svade), and it needs the tests' page tables updated to set A/D. It is not a free correctness fix. One such change hung 12 tests for no clear gain and was reverted.

## Process

- Diagnose with data before optimizing: per-module cell counts, the critical-path report, the generic-cell-type breakdown (`$mux` vs `$add` vs `$sdffe`). Don't guess the bottleneck.
- The biggest area win is often a structural surprise (a flop-ROM), not the thing you assumed (interpreter logic depth).
- When a build thrashes or hangs, check whether it is converging (a trend) before killing it; conversely, don't wait hours on a flat-lined metric.

## Midstall House Style

- River on ECP5 is the reference: internal multiply pipelining, microcode area trims, comparator sharing, all measured against the matrix and the post-pack reports.
- See `measured-area-surprises.md` in this directory: an iterative multiply that INCREASED area in one config (a DSP win, not always a LUT win), why the "compute everything and select" hoist only wins on distinct selectors (yosys already CSEs the rest), and how to recognize you have hit the floor.
- Write docs and comments in ASD-STE100 Simplified Technical English. No em dashes, no emoji. Measure with `fpga-synthesis-fit`; verify with `differential-verification`.
