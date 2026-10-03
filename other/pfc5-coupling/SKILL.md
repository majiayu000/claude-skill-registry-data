---
name: pfc5-coupling
description: Plan and validate PFC 5.0 asphalt fluid, pore-pressure, buoyancy, seepage, and PFC-FLAC coupling contracts while keeping version-specific commands and licensed coupling assets external.
---

# PFC5 Coupling

Use this skill when a PFC5 asphalt study requires fluid forces, pore pressure,
seepage, buoyancy, or discrete-continuum handoff.

## Required Inputs

- PFC2D/PFC3D 5.0 and coupled product/version/license;
- coupling type, units, physics assumptions and update direction;
- mesh/boundary/interface data and coordinate mapping;
- fluid density/viscosity or continuum material/state variables;
- exchange interval, conservation checks and validation targets.

## Workflow

1. Decide whether a simpler prescribed force/pressure boundary is sufficient.
2. Freeze the coupling contract in JSON using [coupling-contract.md](references/coupling-contract.md).
3. Validate paths, units, fields and intervals with
   `scripts/validate_coupling_contract.py`.
4. Test one-way exchange on a minimal licensed PFC5 case.
5. Add two-way iteration only after sign, scale and conservation checks pass.
6. Export exchanged fields, residuals, timestamps and restart state.
7. Run mesh/update-interval/boundary sensitivity and physical validation.

## Working Rules

- This skill does not bundle DLLs, commercial examples or unverified command files.
- Do not assume a coupling API from another major version exists in PFC5.
- PFC and continuum meshes need an explicit coordinate, unit and sign mapping.
- A file-level contract check is not a coupled runtime validation.

## Output Contract

Return the JSON contract, external dependencies, mapping tables, validation report,
exchange/residual histories, sensitivity results and runtime status.

## Local Contents

- `references/coupling-contract.md` — portable coupling schema.
- `scripts/validate_coupling_contract.py` — deterministic contract validator.
- `agents/openai.yaml` — interface metadata.
