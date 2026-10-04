---
name: mbg-ic-verify
description: Runs DRC, LVS, and PEX physical verification for GDSII layouts using Magic and netgen, with automatic port-order fixing for LVS. Use when the user asks to "run DRC", "check LVS", "extract parasitics", "verify layout", "run pex", or otherwise wants post-layout verification of an existing GDS under GF180MCU. Do not use it to generate layout (use mbg-spice-to-gds) or to run SPICE simulation.
metadata:
  short-description: Runs DRC, LVS, and PEX physical verification for GDSII layouts using Magic and netgen, with automatic port-order fixing for LVS.
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-ic-verify/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# MBG IC Layout Verification (DRC / LVS / PEX)

## DRC is dual-engine — Magic *and* KLayout

```python
from mbg.drc import run_dual_drc
s = run_dual_drc(gds_path, cell_name, workdir)
s.verdict     # PASS | FAIL | DRC_DISAGREEMENT | ERROR | CONFIGURATION_FAILURE
print(s.report())
```

**KLayout is the sign-off authority** — it runs the GF180 foundry deck from
`$PDKPATH/libs.tech/klayout/tech/drc/gf180mcu.drc`. **Magic is the
independent complementary check.** Both must be clean and must agree.

Never report DRC from Magic alone. Never treat a KLayout run that produced no
database as clean — the deck exits 0 by design, so the `.lyrdb` is the only
verdict. A `DRC_DISAGREEMENT` is a result to investigate, not a pass.

Cell-level runs exclude die-level density/fill rules (`decks=all,-density`);
an assembled die uses `decks=all`.

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

## Purpose

Run physical verification checks on GDSII layouts: Design Rule Check (DRC),
Layout vs Schematic (LVS), and Parasitic Extraction (PEX), using the
`mbg.checks` functions in
`src/mbg/checks.py`.

## When to Use

- Running DRC on a GDS file.
- Verifying LVS: does the layout match the schematic netlist.
- Extracting parasitics (PEX) for post-layout simulation.
- The user asks to "verify my layout" or "run DRC/LVS/PEX".

## When Not to Use

- Generating layout from SPICE — use `mbg-spice-to-gds`, which already runs
  DRC/LVS/PEX as part of `spice_to_gds_with_checks`.
- Running SPICE simulation (pre- or post-layout) — that is a separate
  concern handled by `mbg.simulation`, not this skill.
- Manually editing an extracted or schematic netlist outside of the
  documented `fix_port_order` / permute helpers.

## Required Inputs

- Path to a GDS file to verify (DRC), or a GDS plus a source SPICE netlist
  (string or path) to compare against (LVS), or a GDS to extract from (PEX).
- A working directory to write reports into (optional; each function
  defaults to a sensible location if omitted — read the function's own
  docstring in `core/checks.py` rather than assuming).

## Preconditions

Magic and netgen must be on `PATH`. The PDK environment variables must be
set before calling any `mbg.checks` function:

```bash
export PDK_ROOT=/foss/pdks
export PDK=gf180mcuD
export PDKPATH=/foss/pdks/gf180mcuD
```

This is the path used inside the IIC-OSIC-TOOLS container, and it is what
`mbg.checks._check_env` requires (`PDK_ROOT`, `PDK`, `PDKPATH` must all be
present in the environment or the call raises `EnvironmentError`).

If you are not running inside the container — a bare host install — do not
assume any single fixed path. Detect it instead:

1. Check whether the caller already has `PDK_ROOT`/`PDK`/`PDKPATH` exported;
   prefer that over guessing.
2. If unset, `mbg.checks.run_lvs` itself falls back to `PDK_ROOT=/foss/pdks`
   and then searches under `PDK_ROOT` for the PDK setup file before failing
   — read that fallback logic in `core/checks.py` rather than hardcoding a
   personal home directory path into a script or skill example.
3. Never write a user-specific absolute path (e.g. a particular
   contributor's home directory) into checked-in code, examples, or
   generated scripts. If a concrete PDK install path is needed for a
   one-off local run, ask the user or read it from the environment at
   runtime.

The Magic `.magicrc` file is resolved as
`$PDK_ROOT/$PDK/libs.tech/magic/$PDK.magicrc` — confirm this file exists
before assuming DRC/LVS extraction will succeed.

## Workflow

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core import run_drc, run_lvs, run_pex

# DRC
drc = run_drc("out.gds", cell_name="my_cell")
print(drc["summary"])   # "DRC: CLEAN" or "DRC: N ERRORS"

# LVS — netgen's own "permute 1 3" rule handles MOSFET D/S swapping
# natively; no manual Python permutation is required for that case.
lvs = run_lvs("out.gds", netlist_content=netlist, cell_name="my_cell")
print(lvs["summary"]["message"])  # "LVS OK" or "LVS MISMATCH"

# PEX (mode: 1=C-decoupled, 2=C-coupled, 3=full-RC)
pex = run_pex("out.gds", cell_name="my_cell", mode=2)
print(pex["summary"])   # "PEX: OK (C-coupled)"
```

### Functions

`run_drc(gds_path, cell_name=None, engine="magic", workdir=None, clean=False, timeout=600)`
Returns `{clean, report_path, error_count, log, summary}`.

`run_lvs(gds_path, netlist_path=None, netlist_content=None, cell_name=None, workdir=None, auto_fix_ports=True, auto_permute_sd=False, timeout=600)`
Auto-fixes extracted port order to match the schematic when
`auto_fix_ports=True` (the default). Netgen's `permute 1 3` rule already
handles `nfet_03v3`/`pfet_03v3` D/S swapping natively — `auto_permute_sd`
is a separate, optional Python-side permutation and is off by default.
Returns `{match, report_path, log, summary}` where `summary` has
`{match, device_mismatch, net_mismatch, port_swaps, missing_devices, message}`.

`run_pex(gds_path, cell_name=None, mode=2, subcircuit=True, pex_name=None, workdir=None, permute_sd=False, timeout=600)`
Returns `{pex_path, mode, log, summary}`.

`extract_layout_netlist(gds_path, cell_name=None, workdir=None, timeout=300)`
Extracts a SPICE netlist from GDS using Magic (no-RC / LVS mode).
Returns `{netlist_path, raw_ports, log, success}`.

`fix_port_order(extracted_path, correct_order, out_path=None)`
Reorders an extracted netlist's ports to match a target order.

`check_tools()` / `validate_gds(gds_path, cell_name=None, min_size=100)`
Environment and artifact sanity checks — call these first when a failure
is ambiguous.

## Outputs

- DRC: `summary` is `"DRC: CLEAN"` or `"DRC: N ERRORS"`.
- LVS: `summary["message"]` is `"LVS OK"` or `"LVS MISMATCH"`.
- PEX: `summary` is `"PEX: OK (C-coupled)"` or `"PEX: FAILED (...)"`.

Report every field of the returned dict that is relevant, not just the
top-line summary — `error_count`, `port_swaps`, and `missing_devices` are
often what the user actually needs to act on.

## Failure Modes

- `EnvironmentError` from `_check_env` — one or more of
  `PDK_ROOT`/`PDK`/`PDKPATH` is unset. Report the missing variable(s); do
  not invent a value.
- Missing verification script (`iic-drc.sh`, `iic-lvs.sh`, `iic-pex.sh`
  under `designs/notebooks/chipathon2026-D/scripts`) — report the exact
  path that was expected.
- `FileNotFoundError` for the GDS — confirm the path is repository-relative
  or a valid absolute path before assuming a typo.
- Auto net-merge for router-caused shorts (e.g. `net1<->net2`) is
  **disabled** in `run_lvs` — the docstring still describes the intended
  behavior, but the actual merge call is commented out in `core/checks.py`
  because it was corrupting schematic netlists. Do not report LVS results
  as if net-merge is active; a detected short must be investigated, not
  silently normalized away.
- Property errors on an otherwise-matching LVS run (W/L parameter
  warnings) are acceptable and do not by themselves mean `match: False` —
  check the `match` field itself, not just whether warnings are present.

## PDK Body Constraint

**MOSFET body: `pfet_03v3` -> VDD ONLY, `nfet_03v3` -> VSS ONLY.** When
interpreting LVS or PEX results, verify all body terminals in the source
netlist connect exclusively to the correct supply rail before accepting a
match as electrically sound.
