---
name: mbg-pex-aware-flow
description: Drives the MBG two-loop design methodology — pre-layout optimization, then PEX-aware post-layout optimization. Use whenever a design has performance targets (gain, bandwidth, phase margin, offset, delay, power) and must be taken from specification to a sign-off candidate. Use it to decide what to do when post-layout simulation misses spec. Do not use it for layout-only tasks with no performance target (use mbg-spice-to-gds), or for pure verification of an existing GDS (use mbg-ic-verify).
license: Apache-2.0
compatibility: opencode
metadata:
  owner: huda
  project: microelectronic-block-generator
  status: experimental
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-pex-aware-flow/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# PEX-Aware Design Flow

Canonical definition: `.ai/knowledge/DESIGN_FLOW.md`. Read it before deviating
from anything here.

## The rule that governs everything

**MBG has two optimization loops.** Pre-layout optimization finds a nominal
circuit. PEX-aware optimization closes the loop on layout parasitics and
produces the sign-off candidate.

**PEX is feedback, not a final stamp.** A PEX specification miss starts an
iteration; it does not end the run.

Pre-layout PASS ≠ finished design.

## DRC is dual-engine

Step 6 below is **two** checks on the same GDS: **KLayout DRC** (GF180
foundry deck — the sign-off authority) and **Magic DRC** (independent
complementary check), reconciled into one verdict.

`PASS` requires both clean and agreeing. Magic failing while KLayout is clean
is `DRC_DISAGREEMENT` — investigate; it is not a pass. A KLayout or rule-deck
that is missing is `CONFIGURATION_FAILURE`. LVS and PEX are `SKIP`ped unless
the reconciled DRC verdict passes.

## Procedure

1. **Read the target specifications.** No targets ⇒ `CONFIGURATION_FAILURE`;
   ask the user rather than inventing numbers.
2. Inspect the starting netlist.
3. **Pre-layout simulation.**
4. Evaluate against the targets. If any required spec fails, adjust sizing or
   bias and repeat, up to `max_pre_iterations`.
5. Once pre-layout passes: **generate layout**.
6. **DRC.** Fail ⇒ LVS/PEX/PEX-sim are `SKIP`.
7. **LVS.** Fail ⇒ PEX/PEX-sim are `SKIP`.
8. **PEX extraction.**
9. **PEX simulation** — a *separate* stage from extraction.
10. Evaluate the extracted results against **the same** targets.
11. If PEX misses spec:
    a. compare pre-layout vs PEX to see which metrics degraded and by how much;
    b. identify the parasitic-sensitive nodes/devices behind the worst ones;
    c. adjust circuit parameters **and/or** layout constraints;
    d. regenerate the layout;
    e. re-run DRC → LVS → PEX → PEX simulation;
    f. repeat until pass or a stop condition.
12. Stop when specs pass, an iteration/convergence limit is hit, or a
    tool/configuration failure blocks progress.
13. Produce the design-flow report.

## Running it

```python
from mbg import Spec, DesignPoint, FlowConfig, DesignFlow, make_hooks

specs = [Spec("gain_db", ">=", 30.0, " dB"), Spec("bw_hz", ">=", 100e6, " Hz")]
hooks = make_hooks(cell=cell, in_node="in", out_node="out",
                   supplies={"vdd": 3.3, "vss": 0.0},
                   spec_names=[s.name for s in specs])
res = DesignFlow(hooks, FlowConfig(specs=specs, outdir=outdir)).run(
    DesignPoint(cell=cell, netlist=netlist))
print(res.summary())
```

`res.status` ∈ `PASS | FAIL | NOT_CONVERGED | ERROR`;
`res.failure` ∈ `NONE | SPEC_FAILURE | TOOL_FAILURE | VERIFICATION_FAILURE |
DESIGN_FAILURE | CONFIGURATION_FAILURE | TIMEOUT`.
History: `<outdir>/history.json`. Best design: `res.best_pex_iteration`.

Supply your own `tune_pre` / `tune_post` to `FlowHooks` when you want to
decide the changes yourself — the bundled ones are simple documented
heuristics, not an analog optimizer.

## Reading a failure correctly

| What you see | What it means | What to do |
| --- | --- | --- |
| `PEX extraction PASS`, `spec FAIL` | toolchain fine, design short | fine-tune, regenerate, re-verify |
| `TOOL_FAILURE` | Magic/netgen/ngspice broke | fix the tool; **do not tune** |
| `VERIFICATION_FAILURE` | DRC or LVS said no | fix the layout; PEX was correctly skipped |
| `NOT_CONVERGED` | ran out of iterations | report the best iteration and the gap |
| metric `MISSING` | simulation produced no value | investigate; never read as a pass |

## Diagnosing a PEX miss

Use `res.degradation` (worst first). Typical signatures:

- **bandwidth down, DC gain unchanged** — capacitive loading. Widen or shorten
  the critical net; reduce fan-out capacitance; check the output node route.
- **gain down** — series resistance or a lost operating point. Widen supply
  and critical-net metal.
- **phase margin down** — added pole from load capacitance; revisit
  compensation and the dominant-pole node.
- **matched-pair metric skewed** — asymmetric routing. Constrain matched
  routing rather than resizing.

## Never

- declare success after pre-layout simulation only;
- declare success after DRC/LVS only;
- declare success because PEX extraction completed;
- treat a tool crash as a specification failure;
- simulate PEX on a layout that failed DRC or LVS;
- iterate without a bound;
- invent specification numbers the user did not give.
