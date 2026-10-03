---
name: pfc5-asphalt-workflow
description: Orchestrate PFC2D/PFC3D 5.0 asphalt-mixture case handoff, specimen generation, fistPkg26 integration, Burger calibration, Marshall or rutting tests, validation, and reproducible delivery; use whenever a user mentions PFC5 asphalt, AC mixtures, fistPkg, Marshall, wheel tracking, or rutting.
---

# PFC5 Asphalt Workflow

Use this skill as the primary entrypoint for a complete asphalt-mixture task that targets
PFC 5.0. Keep the PFC5 case internally version-pure and route narrow work to the sibling
skills listed below.

## When to use

Use this skill when the request includes one or more of:

- PFC2D/PFC3D 5.0 asphalt, asphalt concrete, AC-13/16/20, mastic, aggregate or voids;
- fistPkg/FISHTank material generation or its compression, diametral or tension tests;
- Burger viscoelastic contacts for asphalt mortar;
- Marshall stability/flow or wheel-tracking/rutting;
- auditing an existing asphalt case for unsupported-version contamination.
- migrating, restoring, or resuming an existing private PFC5 asphalt case.

If the user targets another PFC major version, stop and state that this package is
out of scope; do not route to a removed sibling or translate commands implicitly.

## Required inputs

Before production code, obtain or mark as unresolved:

1. product (PFC2D or PFC3D 5.0); do not require a particular PFC5.0 subversion;
2. unit system and stress/strain sign convention;
3. test type and the complete standard method chain (sampling, preparation, forming,
   density/void, performance and field-validation methods), including whether a legacy
   2011 method must be reproduced;
4. specimen geometry and dimensional idealization;
5. sieve-by-sieve gradation, constituent densities, binder/aggregate convention and
   target air-void content;
6. aggregate representation (balls/clumps) and minimum resolvable particle size;
7. contact-pair hypothesis and calibrated macro targets at the test temperature/rate;
   for an intersection case, include the vertical-horizontal load law, contact-model
   mixture policy and any physical-to-accelerated time mapping;
8. legal `<FISTPKG_ROOT>`, PFC runtime route and run budget;
9. required saves, histories, raw exports, figures and acceptance tolerances.

Never silently invent missing gradation, standard values, Burger parameters, or measured
targets.

## Version and evidence gates

Read [version-matrix.md](references/version-matrix.md),
[fistpkg-contract.md](references/fistpkg-contract.md), and
[standards-policy.md](references/standards-policy.md) before writing a case. Use
[standards-method-map.md](references/standards-method-map.md) to classify each standard
as a material method, design input, field validation method or acceptance context. Use
[standards-source-ledger.json](references/standards-source-ledger.json) to bind reviewed
method claims to a source edition, printed-page locator and file digest without bundling
the standards text.

- PFC5 uses its own `cmat`, wall and FISH syntax. Reject unsupported newer-major
  command families instead of attempting an implicit port.
- Run `scripts/check_fistpkg.py "<FISTPKG_ROOT>"` before relying on fistPkg.
- Treat the user's licensed fistPkg files as external inputs. Never vendor their FISH,
  DLL, PDFs, projects or saves into this skill package.
- The checker proves file compatibility only. A case is not validated until PFC executes
  a minimal syntax probe and the intended pilot case.

## Workflow

### P-1 — Audit an existing private case

When the request starts from an existing project, route first to `pfc5-case-handoff`.
Protect the source, freeze included/excluded branches, verify integrity and portable
dependencies, then restore the claimed last-good save and run a bounded audit before any
full rebuild. Keep accepted, restart-only, diagnostic-only and obsolete states distinct.
Skip this phase for a genuinely new case.

### P0 — Freeze the case contract

Copy [pfc5-asphalt-intake.yaml](templates/pfc5-asphalt-intake.yaml) into the case
directory and complete it. Record every value with units and provenance. Every
`method_chain` item is an independent source record; do not reuse one global edition,
source ID or reviewer across aggregate, forming, performance and field methods. Repeat a
role when several methods or project records contribute, and use `not_applicable` rather
than deleting a required role.

### P1 — Choose the material abstraction

Route to `pfc-asphalt-mixture`.

- A homogenized-mastic route normally uses explicit aggregate particles/clumps,
  unresolved mastic represented by contact laws, and residual pore space.
- An explicit fine-particle route adds resolvable fine aggregate/filler particles; it is
  not automatically a literal three-particle-phase binder model.
- Document which real phase each object/contact represents and what the model cannot
  resolve.

Perform volume and mass closure before particle generation. Do not assume nominal sieve
fractions equal DEM particle radii.

### P2 — Build and compact

Route the command skeleton, staged saves, contact installation order and static
version audit to `pfc5-core-modeling`. Route reusable controllers, histories and
callbacks to `pfc5-fish`; every callback still needs a minimal PFC5 runtime probe.

Use separate PFC5 stages:

```text
00_parameters
10_boundaries
20_aggregate_generation
30_settle_or_expand
40_compact
50_install_final_contacts
60_equilibrate_and_instrument
70_test
80_export_and_verify
```

At every milestone record seed, particle/clump counts, mass/volume closure, void content,
coordination/contact counts, equilibrium metric and save name. A target height alone does
not prove target void content.

### P3 — Install and calibrate contacts

Route Burger work to `pfc-burger-viscoelastic` and fistPkg baseline tests to
`pfc-fishtank-tests`. Use `pfc5-servo-calibration` for wall-servo sign probes,
gain bounds, parameter ledgers, guarded two-target updates and independent-case
confirmation.

1. verify a two-body or small-RVE contact probe in a PFC5.0 runtime;
2. separate existing-contact reassignment from future-contact defaults;
3. equilibrate after contact changes and preserve the pre-load state;
4. calibrate elastic response, strength/interface response and time-temperature response
   in a declared sequence;
5. confirm the result on an independent seed/specimen or loading condition.

Contact-level Burger constants are not obtained by directly renaming DSR/BBR parameters;
they must be fitted through a model-scale response with units and geometry held fixed.

### P4 — Run the selected test

| Test | Route | Extra gate |
| --- | --- | --- |
| compression/diametral/tension/creep | `pfc5-standard-tests`; optionally `pfc-fishtank-tests` | forming/density/performance method chain, specimen formula, sign convention and exact baseline provenance |
| Marshall | `pfc-marshall-test` | T 0702 forming handoff, T 0709 edition, curved-head kinematics, raw/corrected curve audit |
| wheel tracking/rutting | `pfc-rutting-test` | T 0703 or field-cut specimen handoff, T 0719 edition, count convention, load control and seven-position/equivalent rut measurement |
| intersection braking/acceleration rutting | `pfc-rutting-test` | separate vertical/horizontal reaction targets, boundary sensitivity, shear-component/depth contract and surrogate-equivalence evidence |
| transient load or stress wave | `pfc5-dynamics-wave` | wavelength/resolution, direction and timestep contract |
| AE or energy interpretation | `pfc5-ae-energy` | explicit hit/event rule and declared energy convention |
| fluid, seepage or coupled boundary | `pfc5-coupling` | exchange contract, units and independently validated solver sides |
| other mechanical path | project-specific PFC5 extension | verify every command in an actual PFC5 runtime |

Do not describe Marshall as a Brazilian-tension simulation merely because it reuses
`dc.fis`; only its controller skeleton is reused.

### P5 — Verify, validate and deliver

Required checks:

- version-pure syntax and external-source manifest;
- geometry node/element contract when importing CAD or a mesh;
- equilibrium and quasi-static/inertial evidence;
- seed, resolution, timestep/damping and boundary sensitivity;
- mass/volume/air-void closure;
- reaction force versus prescribed load and duplicate displacement measurement;
- for accelerated or coupled rutting, unaccelerated pilot comparison, contact-model
  population audit, vector-reaction error, displacement asymmetry and shear-depth profile;
- curve shape, scalar targets and failure/rutting pattern against experiments;
- rerun instructions and explicit list of unpassed runtime gates.

## Specialist routing

| Need | Skill |
| --- | --- |
| private-case migration, restore-first audit and handoff | `pfc5-case-handoff` |
| command skeleton, stages, contact lifecycle, source audit | `pfc5-core-modeling` |
| PFC5 FISH functions, histories and callbacks | `pfc5-fish` |
| servo control and guarded calibration updates | `pfc5-servo-calibration` |
| CAD/mesh conversion contracts | `pfc5-geometry-import` |
| compression, diametral, tension and creep metrics | `pfc5-standard-tests` |
| dynamic loading and stress-wave resolution | `pfc5-dynamics-wave` |
| AE hit clustering and energy bookkeeping | `pfc5-ae-energy` |
| fluid, seepage and solver-coupling contracts | `pfc5-coupling` |
| aggregate/gradation/void/specimen | `pfc-asphalt-mixture` |
| Burger theory, PFC5 commands and calibration | `pfc-burger-viscoelastic` |
| fistPkg26 external framework | `pfc-fishtank-tests` |
| Marshall controller adaptation | `pfc-marshall-test` |
| wheel-tracking/rutting | `pfc-rutting-test` |
| CSV/image post-processing | `pfc-postprocessing` or `pfc-vedo-postprocess` |
| unsupported test type | project-specific PFC5 extension; no cross-version fallback |

## Output contract

Deliver:

- completed case intake and source/version manifest;
- PFC5-only stage map and thin driver;
- gradation plus mass/volume/void closure tables;
- contact assignment and calibrated parameter tables with units and temperature/rate;
- fistPkg dependency-check result and copied-case provenance;
- milestone saves and convergence/load-control evidence;
- raw histories, calculated test metrics and validation comparison;
- exact rerun instructions;
- `runtime_validated: true/false` with all unpassed gates named.

## Local contents

- `references/version-matrix.md` — PFC5-only acceptance and rejection boundary.
- `references/fistpkg-contract.md` — fistPkg26 external dependency contract.
- `references/standards-policy.md` — current-versus-legacy test-standard rules.
- `references/standards-method-map.md` — roles and method-chain routing for the reviewed asphalt, aggregate, design, field, maintenance and acceptance standards.
- `references/standards-source-ledger.json` — source identity, digest, review scope and claim records; no standards text.
- `references/runtime-verification-manifest.json` — hash-bound record of the four PFC5 runtime probes and the retained evidence level.
- `references/intersection-rutting-research-evidence.md` — external-paper evidence,
  transferable modeling ideas and explicit non-default boundaries for mixed contacts,
  time compression and vertical-horizontal rutting.
- `scripts/check_fistpkg.py` — backward-compatible entry point for the checker owned by `pfc-fishtank-tests`.
- `scripts/check_runtime_manifest.py` — verifies that recorded runtime evidence still matches the current probe sources.
- `templates/pfc5-asphalt-intake.yaml` — case intake and provenance template.
- `tests/test_check_fistpkg.py` — deterministic checker tests.
- `tests/test_pfc5_runtime_assets.py` — source-boundary and runtime-manifest regression tests.
- `dependencies.json` — validated package-level contract for the PFC5 specialist skills.
