---
name: vdoc
description: Aggregate all per-module documentation into a single comprehensive IP document
---

# Verilog IP Documenter

## Overview

This guide defines the workflow for collecting all documentation generated during the development process and synthesizing it into a single, comprehensive IP-level document.

The input is the IP name. The output is a single Markdown file `./doc/<ip_name>.md` covering the full IP.

## Step 1 - Collect Documentation Sources

**Read the module docs as the primary source — do not also read every `_req.md`
and `_proposal.md`.** The `ModuleDocContract` guarantees `./doc/<module>.md` is
complete enough to "instantiate, drive, and reason about the module without
reading its RTL," so it already carries the interface and functional content this
skill aggregates. Reading the requirement and proposal for every module on top of
the doc is redundant and the largest token cost here; pull from them only as a
fallback (see the Read priority below).

| Source | Location | Content | When to read |
|--------|----------|---------|--------------|
| Module docs | `./doc/<module>.md` | Per-module interface and functional description | **Always** — primary source |
| Top-level skeleton | `./rtl/<ip_name>_top.v` | Top-level ports and inter-module wiring | **Always** |
| Library module docs | `./lib/**/<module>.md` | Reused library module documentation | **Always** (for reused modules) |
| Synthesis report | `./synth/<ip_name>/synth_report.md` | Utilization, Fmax, power | If present (grep the summary tables, §7) |
| Proposals | `./ddoc/<module>_proposal.md` | Architecture, algorithm, timing diagrams | **Fallback only** — when the module doc lacks the algorithm/timing detail the Architecture section (§2) needs |
| Requirements | `./ddoc/<module>_req.md` | Original per-module requirements | **Rarely** — only to resolve a contradiction in a module doc |

Build a list of all submodules in the IP by walking the instantiation hierarchy from the top-level skeleton, following the shared procedure in `.claude/skills/shared/HierarchyFilelist.md` (use its grep-based extraction — do not read every RTL file).

## Step 2 - Detect and Fill Documentation Gaps

For each submodule in the IP:

1. Check whether a documentation file exists in `./doc/` or `./lib/`.
2. If documentation is missing, use `vexplain` to generate it from the RTL source before proceeding.
3. If a proposal file is missing but the RTL exists, note it as a gap — do not infer architecture that is not documented.

Do not proceed to Step 3 until all submodules have documentation.

## Step 3 - Generate IP Document

Create the IP document at `./doc/<ip_name>.md`.

### Required Sections

#### 1. IP Overview

- One paragraph describing the IP purpose, target use case, and key features
- List of all submodules with a one-line description each

#### 2. Architecture

- Block diagram of the IP showing all submodules and their connections, drawn in mermaid format
- Source: varch proposal or top-level skeleton

#### 3. Top-Level Port Description

- Full port table with columns: Name, Direction, Width, Description
- Source: `./rtl/<ip_name>_top.v`

#### 4. Inter-Module Interface Table

- One table per interface between submodules
- Columns: Signal Name, Direction (relative to master), Width, Description
- Source: varch proposal and top-level skeleton wire declarations

#### 5. Submodule Descriptions

For each submodule, include a condensed summary:

- Purpose (one paragraph)
- Port table
- Key functional behavior

Do not copy the full module doc verbatim — summarize to the level useful for IP integration.

#### 6. Integration Guide

- Instantiation example of the top-level module with all ports connected
- Parameter descriptions and recommended values
- Any constraints or requirements for correct operation (clock frequency, reset sequence, interface protocol)

#### 7. Synthesis Results _(include only if `./synth/<ip_name>/synth_report.md` exists)_

Pull all values directly from `synth/<ip_name>/synth_report.md`. Do not modify or re-interpret the numbers.

Include:

- **Configuration table**: target part, clock constraint, synthesis mode, date
- **Resource utilization table**: LUT, FF, BRAM, DSP (used / available / %)
- **Timing summary table**: clock period, WNS, TNS, Fmax, PASS/FAIL status
- **Power estimate table**: Dynamic, Static, Total
- **Synthesis warnings**: list notable warnings, or state "None"
- A note at the bottom: `Full synthesis artifacts: synth/<ip_name>/`

If the synthesis report is absent, omit this section entirely — do not add a placeholder or note its absence.

### Writing Rules

- Write for an engineer integrating the IP, not for someone implementing it
- Do not include implementation internals or low-level RTL details
- Keep submodule summaries concise — link to `./doc/<module>.md` for full detail
- All block diagrams must use mermaid format
