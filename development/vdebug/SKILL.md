---
name: vdebug
description: Trace failing signals through the RTL hierarchy, classify root cause, and write a debug report per issue — no fix is proposed
effort: medium
---

# Verilog Debugger

## Overview

This guide defines the workflow for diagnosing RTL failures captured in issue reports. Starting from the failure context, the skill traces signal paths statically through the module hierarchy, observes intermediate nodes with a temporary testbench probe when needed, and classifies the root cause with file-level precision.

**This skill diagnoses root cause only. It does not propose or apply any code change.**

### Operating Modes

| Mode | Input | Use case |
|------|-------|----------|
| **Single** | IP name + issue number (e.g. `foo issue_003`) | Deep-dive on one specific issue |
| **Batch** | IP name only (e.g. `foo`) | Process all open issues; group by root cause |

In batch mode, **cluster before tracing** to avoid re-tracing a shared root once
per failure:

1. Triage every issue file first (cheap — just the `[ERROR]` register address
   each maps to) and group issues whose failing output is the same or adjacent.
2. Read the IP-level context (`doc/<ip_name>.md`, `rtl/<ip_name>_top.v`) **once**
   and reuse it for all clusters.
3. Trace each cluster's shared signal path **once** (Step 3), then write a report
   for every issue in the cluster from that single trace.

Process clusters from the lowest issue number upward.

### Outputs

- `./issue/<ip_name>/debug_NNN_<tcname>.md` — one per issue analyzed (NNN matches the issue number)
- `./issue/<ip_name>/debug_summary.md` — batch mode only; root cause grouping across all analyzed issues

### Before You Start — Re-run Safety & Scope

`vdebug` is a read-and-diagnose skill with one deliberate, temporary write: the
optional probe in Step 4. Two scope rules make re-runs safe:

- **Never write to `rtl/` or `lib/`.** Diagnosis reads synthesizable source but
  never edits it. All probing happens in a disposable testbench include
  (`tb/<ip_name>/vdebug_probe.svh`, Step 4) that reaches internal nodes by
  hierarchical reference (`u_dut.<inst>.<sig>`) — the DUT is never instrumented.
- **Clean stale probes first.** A prior run may have aborted between Step 4A and
  4C. Before starting, confirm no probe artifact survives:
  `grep -rn "vdebug probe" tb/<ip_name>/` returns nothing,
  `tb/<ip_name>/vdebug_probe.svh` does not exist, and no `tb_*.sv` still
  `` `include ``s it. Remove any leftover before diagnosing.

Re-running on an already-analyzed issue overwrites its `debug_NNN_<tcname>.md`.
That is non-destructive: the report regenerates from the issue file and the RTL,
both ground truth, so no confirmation is needed.

## Prerequisites

Steps 1–3 (triage and static tracing) need **no external tool** — a fully static
diagnosis is the common path. The simulator is required **only if Step 4 (dynamic
probing) is reached**:

| Tool  | Purpose              | Check             |
|-------|----------------------|-------------------|
| xvlog | Verilog compile      | `xvlog --version` |
| xelab | Elaborator           | `xelab --version` |
| xsim  | Simulator            | `xsim --version`  |

If Step 4 is reached and any tool above is unavailable, do not guess a verdict:
stop probing and classify the issue `INCONCLUSIVE` (Step 5), recording which probe
would resolve it.

## Step 1 - Triage the Issue

Read `./issue/<ip_name>/issue_NNN_<tcname>.md`. Extract:

- The failing testcase file and module name
- The verbatim `Failure Summary` line
- Each `[ERROR]` line and the `[FINISH] FAIL` line from the Simulation Log. An
  `[ERROR]` line is a single CPU-bus read mismatch — `time`, register `address`,
  observed value, expected value. Testcases check through the CPU bus only, so the
  log carries CPU-readable register values, **never internal node values**.
- The reproduction commands (compile, elaborate, run)

Build a working set of facts: the failing register address, its observed value,
the expected value, and the simulation time. Map that address through the reg-map
(in `dut.vh` / the module doc) to the DUT output or status register it reflects —
that mapped signal is the top-level node Step 3 traces backward from.

## Step 2 - Understand the Test

Read `./tb/<ip_name>/tb_<name>.sv` (and the reusable sequences it calls in `dut.vh`). Identify:

- The stimulus sequence applied to the DUT (what inputs, in what order, under what conditions)
- The reference model or expected-value computation inside the testbench
- The exact check that fired (the `[ERROR]` line, e.g. from `cpu_read_check` or an explicit compare) — which output it checked and how the expected value was derived
- Whether the `[ERROR]` signal values captured at failure time are consistent with the stimulus (i.e., whether the testcase itself could be the source of the error)

If the expected value in the testcase is clearly wrong (miscalculated, wrong port name, incorrect timing assumption), note it immediately. Classification in Step 5 will be `TC_BUG`.

## Step 3 - Trace the Signal Path (Static Analysis)

This is the primary debug method. Perform static RTL analysis before considering any simulation run.

Read `./doc/<ip_name>.md` and `./rtl/<ip_name>_top.v` to understand the IP structure (in batch mode read these once and reuse across all clusters).

Starting from the failing output port, trace backwards through the hierarchy using this process:

1. Identify which submodule at the current level drives the failing signal (look at wire assignments and port connections in the instantiation).
2. Read that submodule's documentation first (generate it with `vexplain` if missing). If the doc explains the signal's behavior and it matches spec, treat this module as correct and do not open its RTL — descend no further on this branch.
3. Only when the doc is inconclusive, open the RTL: `Grep` the signal name to find the `always`/`assign` that drives it, and read just that block plus its inputs — not the whole file.
4. List every upstream signal that feeds into that block.
5. Determine which upstream signal must have carried the wrong value. Only the top-level (CPU-readable) value comes from the `[ERROR]` line — deeper node values are not in the log. Reason from the logic which upstream is implicated; mark its value `unknown` until a Step 4 probe confirms it.
6. Descend into the submodule that produced the wrong upstream signal and repeat from step 1.

Continue until one of the following stopping conditions is met:

- A logic expression clearly computes the wrong result (wrong operator, wrong condition, missing case branch, off-by-one in counter)
- An FSM is in an unexpected state — check `localparam` state definitions and state transition conditions
- A pipeline stage register holds a wrong value traceable to a known incorrect computation upstream
- A primary input was driven with a value that the RTL was not designed to handle (testcase issue)

Use `.claude/skills/shared/CodingStyle.md` to interpret signal names while tracing — register suffixes (`_ff`), pipeline-stage prefixes (`s0_`/`s1_`), bus-direction prefixes (`s_`/`m_`), and `<master>2<slave>` internal bus names all carry timing and module-pair information.

Record the full chain as a table:

| Level | Signal | Module | File | Value at Failure |
|-------|--------|--------|------|-----------------|
| Top output | `m_data` | `foo_top` | `rtl/foo_top.v` | `0x00` (expected `0xFF`) |
| Stage 1 | `s1_result_ff` | `foo_proc` | `rtl/foo_proc.v` | `0x00` |
| Stage 0 | `s0_sum` | `foo_proc` | `rtl/foo_proc.v` | unknown |
| Root | `s0_op_sel` | `foo_ctrl` | `rtl/foo_ctrl.v` | `1'b0` (should be `1'b1`) |

Only the top row's value is read from the `[ERROR]` line; every deeper row is
`unknown` until a Step 4 probe fills it. The example above shows a *completed*
trace — its root value was confirmed by probing, not taken from the log.

If static analysis fully identifies the root cause, skip Step 4. But if any value
in the trace table is still `unknown` at the suspected root, the `RTL_BUG` verdict
is a hypothesis, not a confirmed fact — prefer one confirming probe run (Step 4)
before classifying, when a simulator is available.

## Step 4 - Dynamic Probing (Only If Step 3 Is Inconclusive)

Use probing only when static tracing reaches a point where multiple upstream
signals could be the source and none of their values appear in the `[ERROR]`
dump. Probing is white-box but **never modifies `rtl/` or `lib/`**: it reads
internal DUT nodes by hierarchical reference from a disposable testbench include.

### 4A — Add the Probe Include

Create `tb/<ip_name>/vdebug_probe.svh` with one probe block that samples the
suspect nodes from the Step 3 trace table. Reach each node by hierarchical
reference rooted at the DUT instance — `vtestgen` names it **`u_dut`** in
`dut.vh` — using the exact instance path from the trace, including
`generate`/array labels where present (e.g. `u_dut.g_lane[0].u_fifo.wptr`).
Clock the probe on the bench clock (the DUT's clock-port name declared in the
testcase, e.g. `clk`):

```systemverilog
// vdebug probe — temporary; delete this file and its `include before Step 5
always @(posedge clk)   // bench clock = the DUT clock-port name in the testcase
    if (<narrow_enable>)   // e.g. a cycle range or a sequence-phase flag
        $display("[PROBE] t=%0t s0_sum=%0h op_sel=%0b state=%0d",
                 $time, u_dut.u_proc.s0_sum, u_dut.u_ctrl.op_sel, u_dut.u_ctrl.state);
```

Then add one line at module scope inside the failing `tb_<name>.sv` (e.g. just
before `endmodule`):

```systemverilog
`include "vdebug_probe.svh"   // vdebug probe — temporary
```

Notes:
- The file is `.svh`, not `.sv`, on purpose: the Makefile auto-discovers
  `tb_*.sv` as testcases, and a `.svh` include is correctly ignored by that scan.
- Hierarchical refs reach the whole trace at once, so probe every `unknown` node
  from the Step 3 table in this single block — no need to probe one level per run.
  Keep `<narrow_enable>` tight to limit output volume.

### 4B — Re-run

Run from inside `tb/<ip_name>/`. The probe changes the testcase build, so force a
rebuild by dropping the stale sim dir first:

```bash
rm -rf sim/tb_<name>
make tb_<name>
# probe output: sim/tb_<name>/simulate.log
```

Locate the `[PROBE]` lines nearest the failure time and extract the values.

If elaboration fails with a hierarchical-name-not-found error, the referenced net
was optimized away or the path is wrong: re-derive the path from the RTL
instantiation chain, and if it is correct, elaborate with debug kept (e.g.
`xelab -debug typical`) so the node is preserved.

### 4C — Remove the Probe

Delete `tb/<ip_name>/vdebug_probe.svh` and remove the `` `include `` line from
`tb_<name>.sv`. Then confirm nothing survives:

```bash
grep -rn "vdebug probe" tb/<ip_name>/   # must print nothing
ls tb/<ip_name>/vdebug_probe.svh        # must not exist
```

The DUT under `rtl/`/`lib/` was never touched, so no RTL cleanup is required —
only the testbench include. Never carry a probe artifact into Step 5.

## Step 5 - Classify Root Cause

Assign exactly one classification:

| Class | Meaning |
|-------|---------|
| `RTL_BUG` | A logic block in a specific file computes the wrong value; behavior disagrees with the design documentation or proposal |
| `TC_BUG` | The testcase stimulus or assertion is incorrect; RTL behavior is consistent with its specification |
| `DOC_AMBIGUITY` | RTL behavior and testcase expectation both have a reasonable interpretation; the specification is unclear or contradictory |
| `INCONCLUSIVE` | Static tracing left the root unresolved and dynamic probing could not run (simulator unavailable, or the node is unobservable); the report names the exact probe that would resolve it |

For `RTL_BUG`: identify the file, module, and the specific `always` block or `assign` statement. State what it currently computes and what it should compute, citing the relevant section of the design proposal or module documentation as the specification.

For `TC_BUG`: identify the testcase file and the specific assertion or stimulus that is wrong. State why it is incorrect.

For `DOC_AMBIGUITY`: quote the conflicting specification sections and describe the ambiguity.

For `INCONCLUSIVE`: state the lowest node in the trace whose value is still unknown, the hierarchical probe that would observe it, and why it could not be run. Do not fall back to guessing one of the other three classes.

## Step 6 - Confirm Root-Cause Groups (Batch Mode Only)

The clusters formed up front (Operating Modes) were grouped by failing output. Now
that each cluster is traced, confirm its members truly share one root-cause
location (same file + same module + same block) and split any that diverged. A
single RTL bug can surface as several failures; one confirmed group per root
prevents redundant fix effort.

## Step 7 - Write Debug Report(s)

### Per-issue report: `./issue/<ip_name>/debug_NNN_<tcname>.md`

NNN must match the issue number from the corresponding `issue_NNN_<tcname>.md`.

Write the following sections:

**Section: Issue Reference**
A single link to the corresponding issue file: `issue_NNN_<tcname>.md`.

**Section: Classification**
One of `RTL_BUG`, `TC_BUG`, `DOC_AMBIGUITY`, or `INCONCLUSIVE`.

**Section: Root Cause Location**
The location for the chosen class, per its definition in Step 5 (file/module/block for `RTL_BUG`; testcase file + line for `TC_BUG`; both conflicting sources for `DOC_AMBIGUITY`; deepest node reached for `INCONCLUSIVE`).

**Section: Root Cause Description**
Two to four sentences expanding the Step 5 finding for the chosen class, citing the relevant proposal or documentation section by name.

**Section: Signal Trace**
The full chain table from Step 3, filled with signal names, module names, file paths, and values at failure time. Include every level traversed, even if intermediate values were correct.

**Section: Evidence**
The `[ERROR]` and `[FINISH] FAIL` lines from the original issue report, plus any `[PROBE]` lines collected in Step 4 if probing was performed.

**Closing note**
End the file with a blockquote: `> This report identifies root cause only. No code change is proposed.`

---

### Batch summary: `./issue/<ip_name>/debug_summary.md`

Write this file only in batch mode, after all per-issue reports are complete.

**Section: Results**
A table with the total issues analyzed and a per-classification breakdown.
**Use exactly this shape — one classification per row, the count in its own
column on the same row** — because `vflow`'s scanner (`scan.sh`) reads the
`RTL_BUG` count from this table to decide Phase 6, and it parses the first bare
integer on the line that contains `RTL_BUG`. A header-row layout
(`| RTL_BUG | TC_BUG | ... |` with counts on the next line) hides the number
from that parse and forces a manual fallback, so keep the count on the
`RTL_BUG` row itself:

```markdown
| Classification | Count |
|----------------|-------|
| Total analyzed | <N>   |
| RTL_BUG        | <N>   |
| TC_BUG         | <N>   |
| DOC_AMBIGUITY  | <N>   |
| INCONCLUSIVE   | <N>   |
```

**Section: Root Cause Groups**
One sub-section per unique root cause location. Each sub-section lists:
- Root cause location (file, module, block)
- Classification
- All issue numbers that share this root cause, each linking to its `debug_NNN_<tcname>.md`

**Section: Unique Issues**
Issues that do not share a root cause with any other issue — listed individually with a one-line summary.

**Closing note**
End with a blockquote: `> This summary identifies root causes only. No code changes are proposed.`

## Step 8 - Self-check Before Finishing

Verify each report against its sources before declaring it done — it is consumed
by whoever fixes the bug, who must trust it without re-tracing:

| Check | Pass condition |
|-------|----------------|
| Classification supported | The verdict follows from the Evidence and Signal Trace, not assertion; `INCONCLUSIVE` is used rather than a guessed class when the root is unresolved. |
| Trace unbroken | The Signal Trace runs from the failing top-level output down to the named root with no skipped level; every row has a module and file. |
| Root location is real | The cited file, module, and block actually exist — open them and confirm the named `always`/`assign` (or testcase line) is present, not assumed. |
| Spec cited | `RTL_BUG`/`DOC_AMBIGUITY` quote the proposal or module-doc section that defines correct behavior, by name. |
| No RTL mutation | Every write this session went to `tb/` (the probe include) or `issue/` (the reports); no `Edit`/`Write` ever targeted a file under `rtl/` or `lib/`. |
| Probe cleaned | If Step 4 ran, `tb/<ip_name>/vdebug_probe.svh` is gone, the `` `include `` is removed, and `grep -rn "vdebug probe" tb/<ip_name>/` is empty. |
| Boundary held | No fix or code change is proposed anywhere in the report. |

If any check fails, fix the report (or clean the artifact) and re-run the check.

## Known Issues and Fixes

This section records issues encountered when running this skill and how they were resolved.

<!-- Add entries below as issues are discovered. Format:
### [Tool] - <short issue title>
**Symptom:** what was observed
**Cause:** root cause
**Fix:** what was done to resolve it
-->
