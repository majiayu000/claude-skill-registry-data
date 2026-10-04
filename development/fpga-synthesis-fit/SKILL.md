---
name: fpga-synthesis-fit
description: Use when synthesizing RTL to an FPGA with yosys/nextpnr (ECP5/Lattice and similar), fighting area or routing congestion, measuring Fmax, deciding why a design won't fit or route, or instantiating block RAM; covers the pre-pack vs post-pack metric trap
---

# FPGA Synthesis and Fit

## Overview

Getting RTL to fit and route on an FPGA is a measurement problem before it is an optimization problem. The tools report several different "area" numbers and most of them lie about what will actually fit. Optimizing against the wrong number burns hours and can make the real result worse.

**Core principle:** Judge fit and timing by the post-pack, post-place numbers (nextpnr `TRELLIS_COMB` and the critical-path report), never by the synthesis-stage estimate. Measure with data before you change RTL.

## When to Use

- Synthesizing with yosys + nextpnr (ECP5/prjtrellis or a similar open flow)
- A design won't fit, or the router thrashes and never converges
- Measuring Fmax or per-module area
- Building a ROM/RAM and unsure whether it became block RAM or flops
- Generating a bring-up bitstream and picking its clock

## The Metric Trap: Pre-Pack LUT4 != Post-Pack TRELLIS_COMB

yosys `stat` after `synth_ecp5` reports `LUT4`, which is pre-pack. nextpnr reports `TRELLIS_COMB`, which is post-pack (LUT4 plus PFUMX, L6MUX21, and carry packed into slices). These differ, sometimes a lot.

A change that cuts `LUT4` can be neutral or worse for `TRELLIS_COMB`. Replacing a barrel shifter with a mux tree is the classic example: barrel shifters pack densely into carry chains, mux trees spread into PFUMX/L6MUX. Always judge by the nextpnr `Device utilisation: TRELLIS_COMB` line. An 80% pre-pack can be a 91% post-pack that won't route.

## Routing Congestion: Thresholds and Seeds

- The router thrashes above roughly 85% `TRELLIS_COMB`. At 89 to 91% it can churn for an hour or two, sometimes never converging. Around 80% routes in minutes.
- **Seeds matter enormously on congested designs.** The same netlist that sticks at tens of thousands of overused wires under one seed can converge cleanly to zero under another in half an hour. If a route thrashes, kill it and try other seeds before touching RTL. Watch the "overused" column trend toward zero; that is convergence.
- 100% BRAM utilization also congests routing (fixed EBR columns, no placement slack). Keep BRAM under about 90% too.

## Measure Utilisation Before You Route, And Bound Every Long Command

nextpnr prints the packed `TRELLIS_COMB` utilisation BEFORE it starts routing. To read the fit number you do not need a finished route: run `timeout 150 nextpnr-ecp5 ... --textcfg /dev/null`, grep the utilisation line, and let the timeout kill the (irrelevant) routing attempt. Only launch a real, seed-swept route once util is already under about 88%; above that the router thrashes and a launched-and-waited route can hang for half an hour or more without converging.

Wrap every long tool command in `timeout` (synth `timeout 600 yosys ...`, a bounded route `timeout 1800` per seed). A non-converging route must not be able to hang you. This matters doubly for an agent driving builds: a thrashing route at 94% util blocks indefinitely otherwise. Decouple measurement from routing, attempt a full route only once the design actually fits, and report progress on anything long-running.

## Memory: Don't Trust Inference, Instantiate Block RAM

yosys memory inference (`memory_bram`) from generic RTL is unreliable, especially with an init value plus a write port plus read latency. It falls back to flops or maps wrong. For ROMs and RAMs, instantiate the primitive (DP16KD on ECP5) directly.

**The flop-ROM trap:** a ROM built as a register array with per-entry reset values (a `RegisterFile(resetValue: contents)`) synthesizes to a giant flop array plus an N:1 read mux, not block RAM, because per-entry reset can't map to BRAM (BRAM init comes from the bitstream, not reset). A 679x139 ROM becomes about 94k flops, four times a whole LFE5U-25F. Always check whether your "ROM" is actually flops; the yosys generic stat shows it as N `$sdffe`. Fix with an explicit DP16KD carrying INITVAL.

See `dp16kd-initval-packing.md` in this skill directory for the exact INITVAL bit layout and the port mapping. Derive packing from yosys's own `brams_map_16kd.v`; do not reinvent it. The DP16KD registered read IS your read-pipeline stage, so don't add a separate one. Keep a flop fallback for simulation at the same read latency, since you can't sim a DP16KD blackbox honoring INITVAL.

## Measuring Area and Fmax When Full Synth Is Intractable

- Full-design `synth_ecp5` with abc9 can take over an hour on a big design. `-noabc9` inflates LUT counts four to eight times (unfittable, useless for judging fit). Neither full path is quick.
- **Per-module area:** synth one module with `synth_ecp5` (abc9 is fine on a single module, minutes) and read its mapped `TRELLIS_COMB`. Caveat: a module synthed standalone with undriven inputs lets `opt` prune most of it, reporting a misleading near-zero. For in-context size, run the full-design generic stat (read, hierarchy, proc, `opt -fast`, stat, no abc9) and read per-module cell counts and `$mux`/`$add` to find the giant and its type (mux-bound vs arithmetic vs memory).
- **Fmax:** wrap the module under test in a timing harness that shift-registers all inputs from one serial pin and XORs all outputs to one register, so nextpnr sees about three IOs instead of hundreds. Synth with abc9, run `nextpnr-ecp5 --freq <target>`, read "Max frequency for clock". The output XOR adds a little artificial depth, so it slightly under-reports; fine for relative comparison.
- Always read the critical-path report before optimizing for timing. The bottleneck is usually a specific primitive (a single-cycle DSP multiply's partial-product carry chain), not "logic depth" in general. Fix that primitive, re-read, and stop optimizing a resource once it leaves the critical path. The RTL transforms that move that needle live in `rtl-area-timing`.

## Clocking A Bring-Up Bitstream

The PLL output, the UART baud divisor, and the timer timebase all derive from the configured clock frequency. If the logic only meets 29 MHz, you must regenerate the bitstream at a clock at or below Fmax (24 MHz, say). Running a 48-MHz-configured bitstream on hardware that only times at 29 MHz fails with setup violations AND a wrong baud rate. Pick a clean integer PLL divide (48/24 = 2).

## Tooling Notes

- `ecppack` lives in prjtrellis (nixpkgs `trellis`), often not in the same shell as yosys/nextpnr. Bring it in separately.
- `nextpnr --timing-allow-fail` lets P&R finish and emit a config/bitstream even when timing fails the constraint, useful to get a bit running at a lower real clock.

## In this skill directory
- `dp16kd-initval-packing.md` - the DP16KD INITVAL bit layout and port mapping.
- `multiseed-routing-and-timeouts.md` - racing seeds, decoupling fit-measurement from routing, bounding every EDA command with a timeout, and "places != routes".
- `toolchain-primitive-limits.md` - what the open flow physically cannot emit (no OBUFDS, inert MMCM phase, no ODELAY, missing site types), a netlist-identical clocking param that flips routability, cross-vendor case-ROM inference explosion, and why a chipdb fork needs a matching binary.

## Midstall House Style

- ECP5 (OrangeCrab 25F, iCESugar) via the open yosys/nextpnr/prjtrellis flow is the reference; the `creek` core was fit to a 25F by working these numbers (208% to 88.5% post-pack).
- aarch64-linux dev box; package tools in Nix without hacks (see `nix-eda-packaging`).
- Write docs and comments in ASD-STE100 Simplified Technical English. No em dashes, no emoji. Pairs with `rtl-area-timing`, `fpga-bringup`, and `rohd-rtl-gotchas`.
