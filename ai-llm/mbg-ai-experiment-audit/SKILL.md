---
name: mbg-ai-experiment-audit
description: Audits an MBG AI-assisted analog-design experiment record for reproducibility, prompt independence, bounded LLM refinement, artifact completeness, AI metrics, and evidence-based results. Use this skill when reviewing experiment.json, generated SPICE, GDS, simulation outputs, or DRC/LVS/PEX reports for an AI experiment. Do not use it to modify analog-design, simulation, routing, or verification implementations.
class: READ-ONLY
owner: jabir
capabilities: [audit_ai_experiment]
platforms: [opencode, claude, codex]
---

# MBG AI Experiment Audit

## Purpose

Audit an AI-assisted analog-design experiment and determine whether its
claims are supported by reproducible artifacts and verification evidence.

The audit covers: prompt traceability, model traceability, API-call and
refinement metrics, generated-netlist validation, prompt-detail
classification, GDS-generation status, simulation and verification
evidence, final experiment status, and reviewer-facing AI metrics.

## When to Use

- Reviewing an `experiment.json` file or a prompt-to-GDS experiment.
- Preparing AI metrics for a report or presentation.
- Verifying that LLM retries/refinements are bounded.
- Checking whether an experiment can be reproduced.
- Checking whether a `PASS`, `FAIL`, or `PARTIAL` label is supported by
  evidence.
- Reviewing generated SPICE, GDS, DRC, LVS, PEX, or simulation artifacts.
- Comparing minimal, constraint-based, and detailed prompts.

## When Not to Use

Do not use this skill to:

- Select final transistor models or device sizes.
- Correct analog circuit topology.
- Modify placement, routing, or power implementation.
- Correct simulation algorithms.
- Modify DRC, LVS, or PEX implementation.
- Decide final tapeout scope.

Record these as dependencies for their respective owners: analog design and
simulation results (Huda), physical verification and automation (Ahmad),
final tapeout scope and team milestones (team lead).

## Required Inputs

At least one of the following must be supplied:

- Path to `experiment.json`.
- Path to an experiment output directory.
- Generated SPICE netlist.
- Original prompt.
- Generated GDS.
- Simulation report.
- DRC report.
- LVS report.
- PEX output.
- Post-layout simulation report.

Preferred experiment structure:

```text
outputs/<experiment-id>/
├── experiment.json
├── prompt.txt
├── generated_netlist.spice
├── circuit_graph.svg
├── generated_layout.gds
├── pre_simulation/
├── drc/
├── lvs/
├── pex/
└── post_simulation/
```

## Preconditions

Before auditing:

1. Confirm that all supplied paths are repository-relative.
2. Reject parent-directory traversal.
3. Do not read `.env`.
4. Do not expose API credentials.
5. Do not modify experiment artifacts.
6. Confirm that the project PDK is identified.
7. Confirm that the experiment has a unique identifier.

### Required Experiment Metadata

An experiment record should include:

```json
{
  "experiment_id": "comparator-minimal-001",
  "model": "model-identifier",
  "pdk": "gf180mcuD",
  "prompt_level": "minimal",
  "api_calls": 1,
  "refinement_iterations": 0,
  "max_refinement_iterations": 2,
  "netlist_valid": true,
  "pre_simulation_status": "PASS",
  "gds_generated": true,
  "drc_status": "PASS",
  "lvs_status": "PASS",
  "pex_status": "NOT RUN",
  "post_simulation_status": "NOT RUN",
  "llm_runtime_seconds": 18.4,
  "total_runtime_seconds": 94.2,
  "final_status": "PARTIAL"
}
```

### Prompt Detail Classification

- **Minimal** — only high-level circuit objective, PDK, supply, and output
  format.
- **Constraint-Based** — adds required behavior, ports, performance
  constraints, or topology-independent design constraints.
- **Detailed** — includes substantial topology, exact model names,
  connectivity, transistor sizes, or a reference implementation.

A detailed prompt demonstrates constrained generation, while a minimal
prompt provides stronger evidence of independent LLM design contribution.
State this distinction explicitly in the audit report.

### Status Values

Use only: `PASS`, `FAIL`, `PARTIAL`, `NOT RUN`, `NOT AVAILABLE`.

Do not accept unsupported absolute-success claims such as "100% functional",
"fully successful", or "completely autonomous".

Status rules:

- **PASS** — every required stage was run, produced its required artifact,
  satisfied its acceptance criterion, and has supporting evidence.
- **PARTIAL** — some required stages passed, but one or more were not run,
  are unavailable, failed, or lack evidence.
- **FAIL** — a required stage failed and prevents acceptance.
- **NOT RUN** — a stage was intentionally not executed.
- **NOT AVAILABLE** — required data or implementation is unavailable.

## Workflow

1. **Identify the experiment.** Record experiment ID, model identifier,
   PDK, prompt level, circuit/subcircuit name, and experiment directory.
2. **Validate prompt traceability.** Confirm the original prompt is
   preserved, prompt-detail level is recorded, the prompt contains no API
   key, no unapproved PDK, and does not silently include a complete
   reference answer unless the experiment is explicitly classified as
   detailed.
3. **Validate LLM metadata.** Confirm model identifier, API-call count,
   refinement-iteration count, and maximum-refinement limit are recorded;
   confirm actual refinements do not exceed the maximum; record LLM
   runtime and token usage when available.
4. **Validate the generated netlist.** Confirm a generated SPICE artifact
   exists, a valid `.subckt` is present, ports are identifiable, at least
   one supported device is present, device models match the approved
   GF180MCU allowlist, no personal filesystem path or credential is
   embedded, and parser-validation status is recorded.
5. **Validate graphical representation.** Confirm a circuit graph or
   schematic representation exists, device names/types are visible, supply
   and ground nets are visible, ports are identifiable, and the graph
   belongs to the same experiment ID. A connectivity graph is supporting
   evidence — it does not replace analog schematic review.
6. **Validate simulation evidence.** For pre- and post-layout simulation,
   confirm status is recorded, a report path exists when status is `PASS`
   or `FAIL`, required waveform/metric evidence exists, numerical claims
   are sourced from one experiment record, and values (delay, offset, VOH,
   VOL, PVT) do not conflict across artifacts. Do not judge whether the
   simulator implementation itself is correct — record implementation
   concerns as a dependency for the simulation owner.
7. **Validate GDS evidence.** Confirm GDS-generation status is recorded, the
   generated GDS path exists when `gds_generated` is true, the top-cell
   name is identifiable, GDS-validation result is recorded, and the GDS
   belongs to the same experiment ID and generated netlist.
8. **Validate physical verification.** For DRC, LVS, and PEX: confirm stage
   status, confirm a report/artifact path, confirm evidence exists for
   `PASS` or `FAIL`, never infer success from a missing report, and never
   modify verification implementation.
9. **Validate final status.** Check whether `final_status` agrees with all
   stage statuses. Examples: post-layout simulation `NOT RUN` means the
   full end-to-end flow cannot be reported `PASS`; LVS `FAIL` means overall
   status cannot be `PASS`; a missing DRC report means DRC cannot be
   `PASS`; PEX `NOT RUN` may result in `PARTIAL` when PEX is required.
10. **Produce the audit report.** Report errors before warnings. Each
    finding must include severity, field/artifact, current value, expected
    rule, required correction, and responsible owner.

### AI Metrics (multiple experiment records)

When multiple experiment records are supplied, calculate: total prompts,
total API calls, first-pass valid-netlist rate, final valid-netlist rate,
average refinement iterations, layout-generation rate, DRC-clean rate,
LVS-match rate, end-to-end success rate, average LLM runtime, average total
runtime, token usage, and estimated API cost (when available).

Do not calculate a rate with an unclear denominator. Always report both
numerator and denominator, e.g. `DRC-clean rate: 7/10 = 70%`.

## Outputs

```text
Experiment:
Model:
PDK:
Prompt level:
Audit status:

Errors:
1. ...

Warnings:
1. ...

Artifact completeness:
- Prompt:
- Netlist:
- Circuit graph:
- Pre-layout simulation:
- GDS:
- DRC:
- LVS:
- PEX:
- Post-layout simulation:

LLM metrics:
- API calls:
- Refinement iterations:
- Maximum refinements:
- LLM runtime:
- Token usage:

Stage results:
- Netlist validation:
- Pre-layout simulation:
- GDS generation:
- DRC:
- LVS:
- PEX:
- Post-layout simulation:
- Final status:

Dependencies:
- ...

Required corrections:
1. ...

Recommended next action:
...
```

## Failure Modes

If the experiment record is invalid:

1. Stop before calculating aggregate metrics.
2. Report every missing required field.
3. Do not infer missing values.
4. Do not rewrite the experiment record.
5. Return `FAIL` for the audit itself.
6. Identify which owner must resolve each issue.

Known failure cases:

- **Path traversal** (e.g. `../experiment.json`) — reject the path and do
  not inspect files outside the worktree.
- **Unbounded refinement** (`refinement_iterations` set but
  `max_refinement_iterations` is `null`) — report a blocking error; do not
  report the experiment as reproducible.
- **Inconsistent final status** (e.g. `lvs_status: "FAIL"` with
  `final_status: "PASS"`) — report a status-consistency error and require
  the final status be corrected to `FAIL` or `PARTIAL`.

## PDK Body Constraint

**MOSFET body: `pfet_03v3` -> VDD ONLY, `nfet_03v3` -> VSS ONLY.** When
auditing generated SPICE netlists, verify that all body terminals connect
exclusively to the appropriate supply rail.

## Safety Rules

- Never read `.env`.
- Never display API keys.
- Never include credentials in an audit report.
- Never modify experiment artifacts during an audit.
- Never stage, commit, or push automatically.
- Never use personal absolute filesystem paths.
- Never claim verification success without evidence.
- Never convert `NOT RUN` into `PASS`.
- Never hide missing or conflicting results.
- Never modify another team member's implementation.
