---
name: pfc5-ae-energy
description: Instrument and post-process PFC 5.0 asphalt damage studies using bond-break hits, clustered AE events, macro energy density, source fields, stage summaries, and auditable CSV outputs.
---

# PFC5 AE And Energy

Use this skill when a calibrated bonded/interface PFC5 asphalt model needs
damage timing, crack/AE hit statistics, event clustering, or macro energy curves.

## Required Inputs

- PFC2D/PFC3D 5.0, contact/bond failure law and event callback evidence;
- stress-strain CSV with units/sign;
- hit CSV with time, position, mode and optional force/tensor fields;
- clustering thresholds and loading-stage definitions;
- elastic modulus used by macro energy approximation.

## Workflow

1. Decide Level 1 hits, Level 2 clustered events, or a separately validated tensor route.
2. Prove PFC5 callback activation with a counter/history.
3. If native PFC energies are required, enable `set energy mechanical on` before the
   measured interval and inventory the partitions actually exposed by every active
   contact model. Export raw hits and stress-strain data without GUI-only transformations.
4. Cluster hits with `scripts/cluster_ae_events.py` when event catalogs are required.
5. Compute macro input/elastic/dissipated energy with
   `scripts/ae_energy_metrics.py`.
6. Tie events and figures to saved stages and preserve raw IDs.
7. Validate thresholds and mechanisms against experimental observations where available.

Read [ae-contract.md](references/ae-contract.md) before choosing classifications.

## Working Rules

- One bond break is a hit, not automatically one laboratory AE event.
- Macro stress-strain energy is not direct contact-energy release.
- PFC5 mechanical energy tracking is off by default, and the Burger model supplies no
  own energy partition. Missing native energy cannot be reconstructed from a later
  activation or silently replaced by the macro approximation.
- Do not claim moment-tensor mechanisms without the tensor construction and units.
- Keep scalar moment symbols distinct from tensor component names.
- Classification denominator and threshold must be defined together and used consistently.

## Output Contract

Return raw hit/event schemas, clustering parameters, energy method/units, stage
summaries, figures/tables, validation caveats and runtime status.

## Local Contents

- `references/ae-contract.md` — hit/event/energy definitions.
- `scripts/cluster_ae_events.py` — deterministic time-space clustering.
- `scripts/ae_energy_metrics.py` — macro energy-density computation.
- `agents/openai.yaml` — interface metadata.
