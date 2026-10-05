---
name: vexplain
description: Generate documentation for any RTL module from Verilog source files
effort: medium
allowed-tools: Read, Write, Grep, Glob
---

# Verilog Reader

## Overview

This guide defines the workflow for generating documentation for a Verilog RTL
module from its source files. The RTL is the ground truth: the generated document
describes the module **as implemented**, accurately enough that another skill can
instantiate, drive, and reason about it without reading the source (see
`.claude/skills/shared/ModuleDocContract.md`).

### Target Resolution & Name Derivation

The input is a single target module, identified by a file path or a module name.
Resolve it to one top-level Verilog source file:

- A path under `./rtl` or `./lib` is the target directly.
- A bare module name resolves to `./rtl/<module>.v`, or to a `./lib` module —
  either `./lib/<module>.v` (single-file) or `./lib/<module>/<module>.v`
  (multi-file, where the top file shares the module's name).

The **module name** is the source file's base name. All output names derive from
it, not from any partial path. Other `.v` files inside a multi-file `./lib/<mod>/`
folder are submodules, not separate targets (see analysis order below).

If a single `.v` file declares more than one module, the target is the module
whose name matches the file base name; the others are treated as submodules.

### Before You Start — Re-run Safety

`vexplain` overwrites the module document. Two cases need care:

- **Existing doc — confirm first.** An `rtl/` `doc/<module>.md` may be a
  pre-implementation `vdesign` draft, and a `lib/<module>.md` is the canonical
  reference for a reusable module. Generating a *missing* doc is the intended
  use; overwriting an *existing* one is destructive — confirm with the user
  first, then regenerate wholesale from the RTL (now ground truth).
- **Unfilled backbone — stop.** If the target RTL still contains `//@` markers
  (`vflow`'s incompleteness marker, `CodingStyle §18`), it is a `vdesign`
  backbone that `vfill` has not implemented. Stop and report; do not document
  empty logic. Pre-implementation intent is `vdesign`'s job.

## Step 1 - Analyze the Design

Read the target Verilog source file and determine the function of the RTL module.

Use `.claude/skills/shared/CodingStyle.md` to interpret signal names, bus interface prefixes, and FSM patterns in the code.

If the module instantiates submodules, follow this order:

1. Check whether each submodule already has documentation.
2. If documentation exists, use it to understand the submodule behavior.
3. If documentation does not exist, read the submodule RTL code only as needed to understand the behavior of the target module.

Document only the target module. Do not duplicate documentation for submodules
that are documented elsewhere — link to their `<module>.md` instead
(`ModuleDocContract` Excluded Content).

After the analysis is complete, generate a new Markdown file according to the following output rules:

Output file rules:

- The output file must use the same base name as the Verilog file (the module name).
- The output file must use the `.md` extension.
- If the target file is under `./rtl`, place the output in `./doc/`.
- If the target file is under `./lib`, place the output in the same folder as the Verilog file.

## Step 2 - Required and Excluded Content

The generated documentation must follow the module documentation contract defined
in `.claude/skills/shared/ModuleDocContract.md` — **every required section,
§1–§11**, plus its Excluded Content rules.

Each section's facts live in a specific place in the RTL — extract them from
there, never assume:

| Contract section | Extract from |
|---|---|
| §2 Parameters | the `#(...)` declaration for the actual defaults. Legal ranges and cross-parameter constraints: derive from how each parameter is *used* (`$clog2`, part-selects, replication — a bus sliced as `[i*8 +: 8]` implies a multiple-of-8 width). If a range cannot be inferred from the code, state the default as the only verified value — do not invent a range. |
| §3 Ports | the module declaration verbatim; each output's Reset Value from the reset branch of the `always` block that drives it. |
| §4 Interface Protocol | the handshake logic itself: what gates a transfer (`valid && ready`), whether outputs are registered or combinational relative to inputs, who may deassert what. Build the **example-transaction cycle table** by walking one real transaction through the implemented logic — including a stalled/back-pressured beat. |
| §5 Reset Behavior | the reset compare (`rst_n == RS_LV` / `!rst_n`) and every assignment in the reset branch; note registers deliberately *not* reset (qualified-by-valid datapath regs, `CodingStyle §5`/`§14`). |
| §6 Timing | count the actual register stages from input to output (`_ff` registers, `s0_`/`s1_` stage chains) — never copy a latency from a proposal or comment without confirming it in the logic. |
| §7/§8 Functional / FSM | the implemented behavior; FSM states from the `localparam` state encodings and the `case` transition logic, drawn as a mermaid `stateDiagram-v2`. |
| §9 Register Map | the **address decode** — the `case (addr)` / `if (addr == ...)` in the write path and the read mux. Access type from the logic, not naming: write-decoded + readable = `RW`; read-mux-only = `RO`; write-decoded only = `WO`; self-clears on a read = `RC`; cleared by writing 1 = `W1C`. Reset values from the reset branch; word-vs-byte addressing from how the address is compared/shifted. |
| §10 Usage Constraints | the guards the logic silently *assumes*: a config register sampled only in the IDLE state implies "configure before starting"; an input used without a holding register implies a stability requirement; the overflow/illegal-input paths show what is saturated, wrapped, dropped, or flagged. |
| §11 Instantiation Template | the module declaration — mechanical; every port named, parameters at their declared defaults. |

## Step 3 - Self-check the Document

Before finishing, verify the document is an instantiation-accurate contract for
the RTL — downstream skills drive the module from it without re-reading the
source. Walk each port and parameter and confirm:

| Check | Pass condition |
|-------|----------------|
| Ports complete & exact | Every port in the module declaration appears in the Ports table with matching name, direction, and width; none added, dropped, renamed, or re-widthed (`ModuleDocContract §3`). |
| Parameters complete & exact | Every parameter appears in the Parameters table with its actual default and a legal range; section omitted only if the module has none (`§2`). |
| Reset values consistent | Each output's Reset Value column agrees with the reset logic in the RTL and with the Reset Behavior section (`§3`, `§5`). |
| Reset convention | Reset is described as synchronous, active level stated against `RS_LV` where applicable (`§5`). |
| Timing derived from RTL | Latency, pipeline depth, and throughput match the implemented register stages, not assumptions (`§6`). |
| Register map complete | Every CPU-accessible register in the RTL address decode appears in the Register Map (`§9`) with its address, access type (`W1C`/`RC` marked explicitly), and reset value; word/byte addressing stated. Section omitted only if the module has no registers. |
| Template instantiates | The Instantiation Template (`§11`) matches the module declaration exactly — every port named, every parameter at its declared default. |
| Constraints captured | Sequencing rules, input-stability assumptions, and error/boundary behavior visible in the RTL are stated in Usage Constraints (`§10`), or the section says "none" in one line. |
| Submodules linked, not duplicated | Documented submodules are referenced by link; none re-documented inline (Excluded Content). |
| No excluded content | No line-by-line code walkthrough or implementation internals (Excluded Content). |

If any check fails, fix the document and re-run the check — do not leave the doc
disagreeing with the RTL it describes.
