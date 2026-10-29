---
name: mbg-voltage-reference
description: Designs, characterises and lays out a voltage reference (bandgap with vertical PNPs and poly resistors, or MOS-only zero-TC) on gf180mcuD with the MBG tools — topology choice, first-cut sizing equations, the `mbg measure vref` recipe across temperature, supply, corners and IBIAS, and layout matching through placement hints. Use when the task is a voltage or current reference, a bandgap, a PTAT/CTAT generator or a VREF.md-style specification. Do not use it for amplifiers (use mbg-pex-aware-flow with `mbg measure ota`) or for verification of an existing GDS (use mbg-ic-verify).
class: GENERATING
owner: huda
capabilities: [measure_reference, check_netlist, agent_cli]
platforms: [opencode, claude, codex]
---

# Voltage references with MBG

Worked examples, with every number reproducible:
`results/claude-code_vref_1v2_bgr/REPORT.md` (bandgap, 19 devices) and
`results/claude-code_vref_1v2_cmos/REPORT.md` (MOS-only, 5 devices). Both use
the `prompt-test/VREF.md` interface: `.subckt <name> VDD VSS VREF IBIAS`,
VDD 3.3 V, 20 µA pushed into IBIAS, 1 pF on VREF.

## 1. Pick the topology from the specification

| need | topology | what limits it |
| :--- | :--- | :--- |
| TC ≤ ~50 ppm/°C, VREF set by physics, small process spread | **bandgap**: VBE + (R2/R1)·VT·ln N | OTA gain (line regulation, PSRR), resistor matching, area |
| MOS only, smallest area, TC ≤ ~100 ppm/°C, trim available | **ZTC**: a diode-connected MOSFET biased at its zero-TC current | VREF follows the threshold corner (±12 %), depends on bias current |
| sub-1 V output | current-mode bandgap (sum PTAT + CTAT currents into a resistor) | more resistors, more matching |

gf180mcuD devices for references (check `scripts/mbg pdk info --section devices`):

* vertical PNP `pnp_10p00x10p00` and `pnp_05p00x05p00` — subcircuits, instance
  as `XQn c b e pnp_…`; the collector is the substrate and must be `VSS`.
  The 10×10 cell has 4× the emitter area of the 5×5 cell.
* `ppolyf_u_1k` high-resistance poly (~1 kΩ/□) — `XRn a b VSS ppolyf_u_1k
  r_width=1u r_length=25u`; build ratios from equal unit segments.
* `nfet_03v3` / `pfet_03v3` only (3.3 V supply).

## 2. First-cut sizing

**Bandgap** (three-branch PMOS mirror; OTA forces the emitters of Q1 and
R1+Q2 equal):

* N = emitter-area ratio Q2:Q1. One 5×5 vs two 10×10 in parallel gives N = 8
  with three cells; ln 8 = 2.08.
* Branch current I = VT·ln N / R1. With R1 = 10 kΩ (10 squares of 1 µm) and
  VT = 25.9 mV, I ≈ 5.4 µA.
* VREF = VBE3 + I·R2 = VBE3 + (R2/R1)·VT·ln N. At ~5 µA a 5×5 PNP has
  VBE ≈ 0.67–0.70 V, so R2/R1 ≈ 10 for 1.2 V (the worked example: R1 = 10
  squares, R2 = 4 × 25 squares). **Sweep R2 by ±10 % and keep the
  TC minimum** — the curvature puts it a little away from the first-order value.
* OTA inputs sit at VBE ≈ 0.7 V: use a **PMOS input pair** (an NMOS pair has
  no headroom there).
* The OTA output drives the mirror gates (PG). PG must be inside the OTA's
  output range: with VDD 3.3 V and a few µA, long mirror PMOS (L ≈ 8 µm) keep
  |VGS| small enough. A first candidate that does not regulate (VREF far off,
  line regulation ~1 V/V) almost always has PG pinned at a rail —
  `mbg sim run --analysis op --probes PG VA VB` shows it.
* Startup: the zero-current state is stable. Using the IBIAS pin keeps the
  common interface: IBIAS into a node with an NMOS to VSS gated by VREF, and a
  second NMOS gated by that node pulling PG low. Once VREF is up the first
  NMOS sinks IBIAS and the second turns off. Size the VREF-gated NMOS wide
  enough (W/L ≈ 8) that it still sinks 40 µA at ss and −40 °C; check with
  `--ibias-sweep`.

**ZTC MOS-only**: characterise first, then size.

```bash
# ztc.spice:  .subckt ztc G VSS / XM1 G G VSS VSS nfet_03v3 W=2u L=0.5u nf=1 / .ends
scripts/mbg sim run ztc.spice --analysis dc --supplies '{"VSS":0}' --sources '{"G":0.5}' \
    --sweep '{"source":"G","start":0.4,"stop":1.8,"step":0.005}' --probes 'i(Vsrc0)' --temp -40
```

Repeat at 27 and 125 °C (and for each L); the crossing of the I–V curves is
the ZTC point. Each run writes `dc.csv` in its run directory.
For `nfet_03v3` it is ≈1.17 V at L = 0.4 µm (1.11 V at 0.28 µm, 1.06 V at
8 µm); for `pfet_03v3` |VGS| ≈ 1.35–1.42 V. Bias the diode at its ZTC current
through a mirror from IBIAS; long-L mirror PMOS (4 µm) improve line regulation.

## 3. Measure — one call per candidate

```bash
scripts/mbg measure vref --design ref1 --spec vref_md --quick            # fast: typical, no PSRR/startup
scripts/mbg measure vref --design ref1 --spec vref_md --corners all \
    --ibias-sweep 5u 10u 20u 30u 40u                                     # full gate
```

The recipe returns VREF at 27 °C, box-method TC over −40…125 °C, line
regulation and ΔVREF over 3.0–3.6 V, IVDD excluding IBIAS, IBIAS sensitivity,
PSRR at low frequency and startup time on a VDD ramp, per corner; the BJT and
resistor model corners follow the MOS corner. `--spec vref_md` is the
VREF.md gate; `--spec bandgap` the stretch targets (±2 %, 50 ppm/°C, 5 mV/V,
−40 dB, 100 µs). Temperature and line sweeps are written as CSV in the run
directory.

Keep a candidate log (change → VREF, TC typ/worst, line regulation) and bound
it; both worked examples needed 10–16 candidates.

## 4. Lay out for matching

```bash
scripts/mbg netlist check --design ref1      # a bandgap is above the tested ceiling: expect ABOVE_TESTED_CEILING
scripts/mbg layout generate --design ref1 --hints hints.json
scripts/mbg layout view --design ref1
```

* Put the PNPs in one row, side by side (`order`), the unit cells of Q2
  between Q1 and Q3 where possible.
* Interdigitate R1 inside the R2 string so both see the same gradient:
  `{"order": {"3": ["XR2a", "XR2b", "XR1", "XR2c", "XR2d"]}}`.
* Group the OTA input pair (`groups: [{"kind": "diff_pair", …}]`) and keep
  the mirror PMOS in one row.

## 5. Post-layout

```bash
scripts/mbg measure vref outputs/ref1/layout/<cell>.pex.spice --post-layout --spec vref_md --corners all
```

PEX is capacitance-only (Magic mode 2): DC metrics should match the
schematic to within a millivolt, PSRR and startup move. A large DC shift or a
stepped temperature curve is an extraction problem, not physics — look at
the poly resistor and MIM parameters in the PEX netlist first (they must be
in µm; `checks.run_pex` converts Magic's scaled values).

## Report

State the topology, why, the candidate log, gate and stretch results pre-
and post-layout, the process spread, and what the design does not do (no
trim, no Monte Carlo, BGR above the tested ceiling). A MOS-only reference
that tracks the threshold corner is a threshold reference — say so.
