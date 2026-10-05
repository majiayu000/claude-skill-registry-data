---
name: vfill
description: Implement Verilog code from an approved design proposal, then lint and simulate
effort: medium
allowed-tools: Read, Write, Bash, Grep
---

# Verilog Writer

## Overview

This guide defines the workflow for implementing a Verilog module from an approved design proposal.

Before starting, read:

1. The target Verilog source file — for `//@` annotations and port declarations
2. The proposal file `./ddoc/<module_name>_proposal.md` (same folder as the requirement file) — this is the source of truth for the implementation

## Prerequisites

| Tool      | Purpose                             | Check                 |
|-----------|-------------------------------------|-----------------------|
| Verilator | Verilog lint                        | `verilator --version` |
| xvlog     | Xilinx Verilog compiler / lint      | `xvlog --version`     |
| xelab     | Xilinx elaborator                   | `xelab --version`     |
| xsim      | Xilinx simulator                    | `xsim --version`      |

Before running any lint or simulation step, verify the tool it needs is
installed using the check command above. If a required tool is missing, **stop
and report which tool is unavailable — never fabricate lint, simulation, or
elaboration results.** The Verilog can still be filled in (Step 1) without the
tools, but Steps 2 and 3 must not be reported as passed unless they actually
ran. (When invoked under `vflow`, this surfaces as `✗ BLOCKED (tool
unavailable: <tool>)` for the dependent phase.)

## Before You Start — Re-run Safety

Before editing, check `rtl/<module>.v` for `//@` markers (the signal `vflow`
uses for completion, CodingStyle §18):

| State | Detect | Action |
|-------|--------|--------|
| **Backbone** | `//@` markers present | First run — implement, then convert every `//@` away. |
| **Already filled** | no `//@` left / real logic present | Filled before: do not re-fill from scratch. Make the requested change as an incremental edit, **update the proposal's `## Implementation Notes (vfill)` section in place rather than appending a duplicate**, then re-lint and re-simulate. |

## Step 1 - Fill in the Verilog Code

Complete the target Verilog source file based on:

- The approved proposal file
- The coding style rules defined in `.claude/skills/shared/CodingStyle.md`
- The design patterns in `.claude/skills/shared/DesignPatterns.md` — when the
  proposal names a pattern (or the backbone is clearly shaped like one of those
  indexed there), build that pattern's canonical shape and honor its **Ruling**
  rather than picking a different valid shape. Adapt the names, widths, and reset
  scope to this module.

The filled file is synthesizable RTL, so it must be **plain Verilog-2005 (IEEE
1364-2005) only — no SystemVerilog constructs** (CodingStyle §0), and must carry
`` `default_nettype none `` at the top restored with `` `default_nettype wire ``
at the end (CodingStyle §14).

When the target module uses submodules, follow this lookup order:

1. Read the submodule documentation first — only its port/parameter section, not the whole file. It could be in `./doc`, `./lib` and sub-folder, or `./rtl`
2. Read the submodule RTL code only if the documentation is not sufficient

Do not read RTL code unless additional information is required to understand the interface or behavior.

After completing the Verilog code:

1. Record the design updates and important notes in the proposal's `## Implementation Notes (vfill)` section (seeded empty by `vdesign`; add the section if an older proposal lacks it). Write inside this section only, updating in place on re-runs — `vdesign`'s re-run safety check detects a filled module by this section having content. This information will help understand the module's functionality and behavior, and can be used during the debugging phase.
2. **True up the module doc.** `doc/<module>.md` was written by `vdesign` with *intended* values; if the implementation deviated — actual latency or pipeline depth, a reset value, a protocol detail, a register field or access type — update the affected sections (`ModuleDocContract`, esp. Timing §6 and Register Map §9) to the **as-built** behavior. The doc's whole purpose is to be used instead of reading the RTL; a doc that still describes the intent after the implementation drifted silently breaks every downstream consumer (`vassert`, `vtestgen`, `vveri`, `vdoc`, `vpackage`). No deviation → no edit.
3. Convert all `//@` annotations to regular `//` comments.

## Step 2 - Clean the Code

Run lint in two passes. Both must pass before proceeding to simulation.

Run these commands from a scratch directory (e.g. `./tb/<module_name>`, the same
folder used for simulation in Step 3) so `xvlog`/`xelab` write `xsim.dir` and
their logs there instead of polluting the repository root. Express RTL/library
paths relative to that directory.

Redirect each tool to a log file and read back **only the finding lines**, never
the full transcript — Verilator prefixes findings with `%Error`/`%Warning`:

```bash
verilator … 2>&1 | tee lint.log    # then inspect: grep -nE '%(Error|Warning)' lint.log
```

### Pass 1 — Verilator

```bash
verilator --lint-only --top-module <top_module> -y <path_to_rtl_folder> -y <path_to_library_folder> -y <path_to_library_submodule_folder> <path_to_top_module_file>
```

Where:
- `--top-module <top_module>` specifies the top-level module name
- `-y <path_to_rtl_folder>` specifies the path to the project RTL folder, relative to the scratch dir, for example `-y ../../rtl`
- `-y <path_to_library_folder>` specifies the path to the library root folder, for example `-y ../../lib`
- `-y <path_to_library_submodule_folder>` specifies the path to a submodule folder inside the library, for example `-y ../../lib/module_1`
- `<path_to_top_module_file>` specifies the path to the file containing the top-level module, for example `../../rtl/top_module.v`

Add one `-y` option for each required library subfolder. The `-y` paths are
*search directories*: Verilator discovers each instantiated submodule by name
itself, so this pass needs no explicit per-file list — just point it at every
folder that holds a required module.

### Pass 2 — Xilinx xvlog + xelab

```bash
xvlog -nolog <rtl_files>
xelab -nolog --top <top_module>
```

Where `<rtl_files>` is the explicit list of all Verilog source files required by
the design (unlike Verilator's `-y` search paths, `xvlog` needs the files named).
Build the list by the walk in `.claude/skills/shared/HierarchyFilelist.md`:
recurse from the filled module, searching `./rtl/` first then `./lib/`,
de-duplicate a file shared by multiple parents, and treat a submodule whose
source cannot be found as a **hard error** — report the missing module and its
parent rather than silently dropping it. The same `<rtl_files>` list feeds the
simulation step (Step 3). For a single small module this walk is short, so do
not generate a persisted filelist — that artifact belongs to the IP-level skills.

### Step 2A - Resolve Lint Issues

Review all warnings and errors from both tools.

For each warning or error:

1. Determine whether it is caused by incorrect RTL code, missing files, missing include paths, or intentional design behavior.
2. Propose a fix.
3. If the user chooses to ignore a warning, suppress it explicitly using a lint directive.
4. Apply the fix only if it does not conflict with the approved design.

For Verilator, use the following format to suppress a specific warning:

```verilog
/* verilator lint_off <WARNING_CODE> */
    a <= b;     // line of code that causes the warning
/* verilator lint_on <WARNING_CODE> */
```

After all proposed fixes have been applied, re-run the lint pass that failed and
re-grep its log — do not re-echo whole logs each iteration.

Repeat this process until:

- No remaining lint errors exist in either tool
- Remaining warnings, if any, are explicitly justified and cannot be safely removed without changing the intended design

Do not ignore warnings silently.

## Step 3 - Functional Simulation

Generate a self-checking testbench file `<module_name>_tb.sv` in the folder `./tb/<module_name>`. All compile and simulation commands must run from inside this folder. The testbench is verification code, so it is SystemVerilog (`.sv`) — permitted under `tb/` per CodingStyle §0; only the synthesizable RTL is restricted to Verilog-2005.

The testbench must:

- Cover every operating scenario from the approved design
- Assert outputs against expected values using `$error` on mismatch
- End by printing exactly one verdict token (CodingStyle §19): `[FINISH] PASS`
  when every scenario passed, `[FINISH] FAIL` on any mismatch — then `$finish`.
  This is the single machine-readable result; print diagnostic context on
  `[ERROR] time= ...` lines, not in the verdict.

Run simulation using xsim from inside `./tb/<module_name>`. All paths must be relative to that folder — use `../../rtl` for the RTL folder and `../../lib` for the library folder.

```bash
xvlog -nolog <rtl_files>
xvlog -nolog -sv <testbench_file>
xelab -nolog --top <testbench_module> --snapshot sim_snap --timescale 1ns/1ps --override_timeunit --override_timeprecision
xsim sim_snap --runall --nolog | tee sim.log
```

The bench prints many `$display` lines, but only the result matters: read back
`grep -nE '\[ERROR\]|\[FINISH\]' sim.log`, not the full transcript. This is what
the `[FINISH]`/`[ERROR]` convention is for. On a re-run after a fix, re-grep —
do not re-ingest the whole log.

To allow users to rerun the testbench later, write these commands into a script
at `./tb/<module_name>/run.sh` and run that file, rather than issuing the
commands ad-hoc.

### Step 3A - Resolve Simulation Failures

For each failing scenario:

1. Determine whether the fault is in the RTL or the testbench.
2. Propose a fix.
3. Apply the fix only if it does not conflict with the approved design.

Repeat until all scenarios pass.

## Step 4 - Self-Check

Confirm before declaring the module complete — this is the handoff `vflow`
relies on:

- [ ] No `//@` markers remain in `rtl/<module>.v` (a stray one keeps `vflow` at IN PROGRESS — CodingStyle §18).
- [ ] Verilog-2005 only, with `` `default_nettype none ``/`` wire `` bookends (§0, §14).
- [ ] Both lint passes clean; any surviving warning has a paired narrow waiver.
- [ ] Simulation passes every scenario; `./tb/<module_name>/run.sh` reproduces the run.
- [ ] Proposal notes updated once (not duplicated — see Re-run Safety).
- [ ] `doc/<module>.md` matches the **as-built** behavior — latency, reset values, register map — updated wherever the implementation deviated from the proposal.

If a tool was unavailable, report which check could not run — don't mark it passed.

## Known Issues and Fixes

This section records issues encountered when running this skill and how they were resolved. Use it to avoid repeating the same mistakes.

<!-- Add entries below as issues are discovered. Format:
### [Tool] - <short issue title>
**Symptom:** what was observed
**Cause:** root cause
**Fix:** what was done to resolve it
-->

