---
name: differential-verification
description: Use when verifying a hardware DUT (a CPU core, FPGA, or netlist) against a golden reference model, building coverage-guided fuzzing, or detecting where silicon diverges from a simulator like Spike, an emulator, or SPICE
---

# Differential Verification

## Overview

You trust a design by running it against something you already trust and comparing. The DUT (device under test) executes a stimulus; a golden reference model executes the same stimulus; you compare the resulting state. A mismatch is a bug in one of them, and finding which is the work.

**Core principle:** Same stimulus, two executors, compare state. Everything else (fuzzing, coverage, campaigns) exists to generate good stimulus and to localize the divergence. The comparison is only as good as the state you capture and how honestly you name it.

## When to Use

- Checking a CPU core against an ISA simulator (Spike, an emulator)
- Checking an FPGA's observed outputs against a golden function
- Checking a netlist against a circuit simulation (SPICE/ngspice)
- Building a coverage-guided fuzzer for any of the above
- Comparing silicon behavior to a simulator and chasing where they disagree

## The Core Loop

```
generate stimulus -> run on DUT -> capture DUT state
                  -> run on golden model -> capture golden state
                  -> compare -> divergence? report : record coverage
```

1. **One stimulus, two runs.** Drive the DUT and the reference with the identical input (the same program, the same vector, the same netlist excitation).
2. **Capture comparable state.** Final register file, memory regions, PC, retired-instruction trace, or node activity, whatever both sides can produce.
3. **Compare honestly.** A field you read but record as "absent" or `false` is a false pass waiting to happen. Make sure a captured value is actually compared.

## Name State By The Hardware, Not The ABI

Capture and compare register state under raw hardware names: `x0..x31`, `pc`, raw CSR names. ABI aliases (`a0`, `ra`, `sp`) are a rendering concern for the frontend only. If the comparison layer speaks ABI names, two tools will eventually disagree about which physical register `a0` is and you'll chase a phantom mismatch.

## Coverage-Guided Fuzzing

Random stimulus plateaus fast. Close the loop with coverage:

- **Match the model to the hardware it stands in for.** When the golden side is a sim model of a registered memory, give it the SAME read latency as the real FPGA primitive (a registered BRAM read is latency 1). A faster sim model verifies behavior the silicon will not have. See `fpga-synthesis-fit`.
- **Maintain a coverage map** (which PCs/edges/encodings/nodes the corpus has exercised) fed by a real coverage source on the executor.
- **Favor novelty.** A power scheduler should spend more energy on seeds that hit new coverage, less on seeds that retread.
- **Layer the generator.** A structured layer emits legal programs (for a CPU, lower randomized IR to legal machine code, for example via a real codegen backend); a raw layer emits corner-case encodings the structured layer would never produce. You need both: legal-but-weird and illegal-but-revealing.

## Coverage Divergence Is Itself A Signal

Track coverage on *both* the simulator and the silicon. When the same stimulus exercises different coverage on the two, that divergence is a finding in its own right, even before an architectural state mismatch shows up. An optional strict mode can flip the verdict on coverage divergence alone.

## Localizing A Divergence

When state mismatches:

1. Confirm the stimulus was truly identical (same entry PC, same loaded segments, same memory init). Plenty of "bugs" are setup skew.
2. Shrink the stimulus to the minimal failing case.
3. Compare step-by-step (per-instruction or per-cycle) to find the first point of divergence, not just the end state.
4. Then decide which side is wrong. The golden model is not automatically right; reference models have bugs too.

## Red Flags

| Smell | Do instead |
|-------|------------|
| Reading a value but recording it as absent/false | Verify captured fields are actually compared |
| State keyed by ABI names | Key by hardware names, render ABI on the frontend |
| Pure random fuzzing | Coverage-guided with a novelty scheduler |
| Only comparing final state | Find the first diverging step |
| Assuming the golden model is correct | Localize, then decide which side is wrong |
| Strict checks toggled off to get a pass | Fix the divergence; see silicon-grade-discipline |
| Test checks only that the transaction completed | Assert the read-back data, not just the handshake |
| Model ignores byte-enables or leaves DQ/DQS as X | Compare on a channel-faithful model or on hardware |
| Blaming silicon before the emulator ran | Reproduce on a golden model with perfect memory first |
| Two "identical" builds differ, editing RTL | FASM-diff the bitstreams; byte-identical means a physical difference |
| Rebuilding the toolchain on a theorized root cause | Validate a cheap fix empirically first; the cause may be secondary |
| Testing writes and reads together on a dead lane | Bisect with a read-only oracle (DDR MPR or pre-written pattern) |

## Midstall House Style

- Heimdall is the reference: Rust post-silicon verification for Aegis FPGA and the River CPU, coverage-guided fuzzer, golden models include Spike (one-shot), a native emulator, and ngspice for netlists. State keys are `x0..x31`/`pc`/raw CSR; ABI names are render-only.
- Library-first: the verification crates are usable as libraries, not just by the bundled CLI/daemon. Maximum test coverage, this goes to silicon.
- After every structural RTL change, re-run the full matrix; it catches off-by-one stalls, stale reads, and extend bugs a hand-picked test misses. See `rtl-area-timing`.
- See `sim-honesty-and-false-passes.md` in this directory: the false-pass modes (a model that drops byte-enables or DQ/DQS, an ACK-liveness-only test), the variance-vs-determinism rule that tells metastability from a logic bug, reproducing on perfect memory to exonerate the hardware, why a paced debug probe can lie, FASM-diffing two "identical" builds (byte-identical means a physical difference), validating a cheap fix before a toolchain rebuild, and bisecting a dead DDR lane with a read-only MPR oracle.
- Write docs and comments in ASD-STE100 Simplified Technical English. No em dashes, no emoji. Pairs with `codegen-validation` (which uses this loop on generated code) and `fpga-bringup`.
