---
name: mbg-spice-to-gds
description: Converts a SPICE subcircuit netlist into a DRC-clean GDSII layout using gLayout, via the single entry point spice_to_gds_with_checks(netlist). Use when the user asks to generate GDS from SPICE, convert a netlist to layout, "layout my circuit", or "spice to gds" for the GF180MCU 3.3V PDK. Do not use for manual step-by-step placement/routing, simulation-only tasks, or verification-only tasks on an already-built GDS (use mbg-ic-verify for that).
license: Apache-2.0
compatibility: opencode
metadata:
  owner: huda
  project: microelectronic-block-generator
  status: experimental
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-spice-to-gds/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# MBG SPICE to GDS Layout Generator

## Before you read anything: context economy

This repository is big enough that *how* you gather information decides
whether you finish. A measured session here spent **87% of a 1 MB
conversation on tool output** — one file re-read 22 times, `git status`
polled 27+ times, and 33 KB spent searching `$HOME` for a repo whose path
was already in `$MBG_ROOT`. Read `mbg-context-economy` first. The short
version: resolve the repo from `$MBG_ROOT`, index a file before opening it,
never re-read what is already in context, do not poll git state, and climb
the verification ladder cheapest-first. Reading less is the goal; **checking
less is not**.

## Pipeline Entry Point

`spice_to_gds_with_checks(netlist)` is the single entry point. It drives the
DesignContext flow: analog-aware placement, the DRC-aware grid router, internal
OPEN/SHORT verification, then Magic DRC + netgen LVS + PEX.

Measured on the four reference blocks (inverter, ring oscillator, 5T OTA,
StrongArm comparator): 4/4 pass DRC and LVS. The older shape-router path passed
0/4 because it mislabelled top-level pins; it is still reachable via
`legacy=True` for comparison but should not be used for new work.

Returned keys: `outdir`, `gds_path`, `svg_path`, `cell_name`, `drc`, `lvs`,
`pex`, `all_pass`, plus `context`, `verification` and `metrics`.


## Outputs Produced

Every run emits a full view set beside the GDS, recorded in `<cell>.views.json`:

| View | File | Notes |
| --- | --- | --- |
| GDS | `<cell>.gds` | the implementation |
| LEF | `<cell>.lef` | abstract for the floorplanner, written by Magic |
| Liberty | `<cell>.lib` | hard-macro abstract; no timing arcs, none were characterised |
| Verilog | `<cell>.v` | black-box declaration; signal pins are `inout` |
| SVG | `<cell>.svg` | preview |
| Schematic SPICE | `<cell>.spice` | the source netlist |
| Extracted SPICE | `<cell>_extracted.spice` | from Magic |
| PEX SPICE | `<cell>.pex.spice` | post-layout with parasitics |
| DRC / LVS | `<cell>.magic.drc.rpt`, `<cell>.lvs.out` | tool output, verbatim |

Signal pins are declared `inout` deliberately: a SPICE netlist records
connectivity, not direction, so anything else would be invented.

## Power Rails

VDD and VSS rails are generated automatically on the top metal, with via drops
registered as access points on the supply nets so the router connects to them.
Drops land on the routing grid — off-grid drops are the one thing the track
pitch cannot keep DRC-legal. Disable with `power_rails=False`.

## Deep N-Well

GF180MCU has no deep-n-well transistor model, so isolation is inferred from
connectivity: an NMOS whose bulk is not on the global ground can only be built
with a deep n-well. Isolation propagates across a matching group, because a
differential pair with DNW on one side only is not matched. Override with
`PlacementConfig(dnwell_devices={...})` or `with_dnwell=True`.

## Passive Devices (resistors and MIM capacitors)

Passives are built by `mbg.passives` from raw PDK layers, **not** by gLayout.
That is not a preference — gLayout cannot produce either device in a form
gf180mcuD recognises:

| Device | gLayout builds | gf180 Magic expects | Result if used |
|---|---|---|---|
| Resistor | a diode-connected **pfet** (its own docstring says so) | `ppolyf_u` = POLY & SBLK & PPLUS & RESDEF | extracts as `pfet_03v3`, LVS can never match |
| MIM cap | MIM on **met2/met3** | `mimcc mimcap metal5` over **metal4** | Magic extracts *no device at all* — the cap silently vanishes |

Write passives the natural way; both spellings are accepted:

```spice
XR1 vin  vout ppolyf_u W=1u L=4u                    * or r_width=/r_length=
XC1 vout vss  cap_mim_2f0_m4m5_noshield W=5u L=5u   * or c_width=/c_length=
```

Three constraints that surprise people:

- **`W >= 0.80 um`** for a poly resistor (PRES.1).
- **MIM top plate `>= 5.0 um`** (MIMTM.8a). There is no smaller MIM in gf180;
  a request below this is rejected rather than silently resized.
- **Only `ppolyf_u` has a native generator.** Another passive resistor model
  (`npolyf_u`, `rm1`, ...) raises `UnsupportedDeviceError` instead of being
  built from a different primitive, because substituting a device that
  extracts under another name is exactly how a layout passes DRC and then
  fails LVS for reasons nobody can find.

Two non-obvious rules are already handled and should not be "fixed":

- A resistor contact must land in the window **0.22-0.44 um** from the
  salicide block. *Both* bounds report as `PRES.7`, so a too-far contact looks
  like a spacing error and moving it further away never helps.
- The MIM's terminals come out on **met3**, not on the plates. Magic derives
  the bottom plate as `bloat-all *mim *m4` — the whole connected metal4 shape
  — and then requires 1.2 um of clearance from any unrelated metal4, so a
  router reaching the plates directly cannot satisfy MIMTM.1/MIMTM.3.

## Chip Integration

```bash
python3 scripts/integrate_modules.py --librelane --top chip_top
```

Collects every module that published a views manifest into a LibreLane macro
integration: top-level Verilog, `config.json`, `info.yaml` and per-module
`lvs_config.json`. If LibreLane is not installed the configuration is still
written and the run is reported `NOT RUN` — never as passing.

## Purpose

Convert a SPICE subcircuit netlist into a DRC-clean GDSII layout with
auto-placement, power delivery, and negotiated-congestion routing, using the
project's single supported pipeline entry point.

## When to Use

- Converting a SPICE netlist to a GDS layout.
- Running the full layout + verification pipeline in one call.
- The user asks to "generate layout", "spice to gds", or "create GDS".

## When Not to Use

- Manual step-by-step placement or routing — inspect
  `mbg.placement_engine` / `mbg.router` directly instead (see
  `mbg-placement-debug` / `mbg-routing-debug`), or use a full-automate
  workflow that still calls the same pipeline entry point underneath.
- Simulation-only tasks with no layout requested.
- Verification-only tasks on an existing GDS — use `mbg-ic-verify`.
- Diagnosing why a placement or route failed — use `mbg-placement-debug` or
  `mbg-routing-debug`; this skill only describes the happy-path call.

## Required Inputs

- A SPICE subcircuit netlist string containing a `.subckt` definition with
  at least one supported device (`XM1`-style MOSFETs, resistors, MIM caps).
- PDK environment variables set (see Preconditions).
- Optional: an explicit output GDS path; otherwise the pipeline derives one
  from the subcircuit name.

## Preconditions

- `PDK_ROOT`, `PDK`, and `PDKPATH` must be set before calling the pipeline.
  Inside the IIC-OSIC-TOOLS container the project standard is:

  ```bash
  export PDK_ROOT=/foss/pdks
  export PDK=gf180mcuD
  export PDKPATH=/foss/pdks/gf180mcuD
  ```

  On a host-only install (no container), do not hardcode a personal home
  directory. Detect the actual PDK root instead, for example by checking
  whether `$PDK_ROOT/$PDK` exists, or by asking the user which PDK
  installation path to use. `mbg.checks` in
  `src/mbg/checks.py` already falls back to
  `/foss/pdks` when `PDK_ROOT` is unset, and `run_lvs` additionally searches
  under `PDK_ROOT` for the PDK setup file — read that module before assuming
  a path.
- The netlist must reference only `nfet_03v3` / `pfet_03v3` devices for the
  GF180MCU 3.3V flow (auto-detected from the `.lib`/`.inc` line by
  `mbg.spice_parser.parse_netlist_with_pdk`; the pipeline also supports
  `sky130` when that PDK is detected).
- Minimum five transistors is the informal threshold for meaningful analog
  layout mode; smaller circuits may still run but are not the intended case.

## PDK Constraints (GF180MCU 3.3V)

| Constraint | Value |
|-----------|-------|
| Supply | 3.3V single |
| MOSFET models | `nfet_03v3` / `pfet_03v3` ONLY |
| W limit | project guidance varies 5-10um per finger — check `AGENTS.md` and `mbg.pdk_rules` for the authoritative limit before sizing |
| L limit | project guidance varies 5-10um — same caveat |
| **Body** | **`pfet_03v3` -> VDD ONLY, `nfet_03v3` -> VSS ONLY** |
| Device prefix | `XM1` (not `M1`) |
| Fingers vs multipliers | Prefer `nf=N` over `m=N` for matching and compactness |

## Workflow

1. Load the netlist string. Reference the PDK library relative to
   `$PDK_ROOT`, never a hardcoded personal path:

   ```python
   from mbg.pipeline import spice_to_gds_with_checks

   netlist = """
   .lib "$PDK_ROOT/gf180mcuD/libs.tech/ngspice/sm141064.ngspice" typical
   .subckt my_design vdd vss in out
   XM1 out in vdd vdd pfet_03v3 L=1u W=4u nf=1
   XM2 out in vss vss nfet_03v3 L=1u W=2u nf=1
   .ends
   """
   ```

   In a live shell, expand `$PDK_ROOT` before writing the `.lib` line, or
   have the calling script substitute the real environment value — do not
   commit a resolved absolute path into a checked-in netlist example.
2. Call **only** `spice_to_gds_with_checks(netlist)`. Never call
   `mbg.placement_engine.place`, `mbg.router.GridRouter`, or
   `mbg.power` functions manually to produce a "final" layout — those are
   internals the pipeline already orchestrates.
3. The pipeline internally: parses the netlist and auto-detects the PDK,
   activates the PDK via gdsfactory, places devices, adds power strips,
   auto-routes, adds pin labels, and writes the GDS.
4. Inspect the returned dict (see Outputs) and report DRC/LVS/PEX results
   exactly as returned — never upgrade a `FAIL` or missing report to a
   claimed pass.

## Outputs

`spice_to_gds_with_checks(netlist)` returns:

| Key | Description |
|-----|-------------|
| `outdir` | Output directory path (named after the cell) |
| `gds_path` | GDS file path |
| `svg_path` | SVG preview path (may be `None` if preview generation failed) |
| `cell_name` | Top subcircuit name |
| `drc` | DRC result dict from `run_drc` |
| `lvs` | LVS result dict from `run_lvs` |
| `pex` | PEX result dict from `run_pex` |
| `drc_signoff` | Dual-engine verdict from `run_dual_drc` — Magic AND KLayout |
| `verification` | Internal connectivity: `opens`, `shorts`, `missing_access`, `clean` |
| `metrics` | `routing_summary()`: routed/total nets, wire length, vias, congestion |
| `context` | The `DesignContext` the layout was built from |
| `all_pass` | All four legs: Magic DRC clean AND `drc_signoff["verdict"] == "PASS"` AND LVS match AND internal connectivity clean |

`all_pass` is the whole gate, not a DRC summary. Two things it deliberately
includes:

* **The KLayout sign-off verdict, not Magic alone.** KLayout runs the GF180
  foundry deck and is the sign-off authority (see `mbg-ic-verify`); Magic is
  the independent complementary check. `all_pass` once read `drc["clean"]`
  only, so a design KLayout had FAILED — or never checked, because it was
  not configured — could still report `all_pass=True`. `NOT_CONFIGURED`
  counts as a failure on purpose: an engine that did not run has not agreed
  to anything.
* **Internal connectivity**, including `missing_access` — a SPICE terminal
  the layout never gave an access point to. It produces no geometry, so
  `opens` cannot see it; without this leg an unconnected device terminal
  could reach external LVS as the first thing that noticed.

Since v0.2 this entry point drives the `DesignContext` path
(`spice_to_gds_with_checks_ctx` in `src/mbg/pipeline.py`). The original
shape-router path is reached only with `legacy=True` or via
`spice_to_gds_with_checks_legacy()`.

## Failure Modes

- Missing `PDK_ROOT`/`PDK`/`PDKPATH` — the pipeline raises before layout
  starts; do not silently set a personal fallback path.
- Netlist has no `.subckt` or zero parsed components — the pipeline raises
  `ValueError` before layout starts.
- `drc["clean"]` is `False`, `drc_signoff["verdict"]` is not `PASS`,
  `lvs["match"]` is `False`, `verification["clean"]` is `False`, or
  `pex["pex_path"]` is `None` — report each stage's own `summary`/`reason`
  field verbatim; do not claim `all_pass` when the dict says otherwise, and
  do not report a Magic-clean result as "DRC clean" without the sign-off
  verdict beside it.
- Floating/unrouted internal nets — inspect with `mbg-routing-debug`
  (`mbg.connectivity.verify`) rather than guessing from the SVG preview.
