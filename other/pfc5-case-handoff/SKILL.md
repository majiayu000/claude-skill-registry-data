---
name: pfc5-case-handoff
description: Audit, recover, and prepare portable handoffs of existing private PFC2D/PFC3D 5.0 asphalt cases, including integrity manifests, path portability, saved-state claims, cheap restore-first validation, and legacy-state quarantine.
---

# PFC5 Case Handoff

Use this skill when an existing private PFC 5.0 asphalt case must be moved, resumed,
reviewed, or handed to another operator or machine. It owns the handoff contract; route
model changes to `pfc5-core-modeling` and FISH changes to `pfc5-fish`.

## When To Use

- migrate a case to another machine or working directory;
- resume from staged saves after an interrupted or failed run;
- audit a project, save-state tree, driver files, or external dependencies before edits;
- separate accepted, restart-only, diagnostic-only, and obsolete states;
- prepare a private handoff without publishing project code, data, parameters, or saves.

Do not use this skill to redesign the material model, invent missing parameters, or
authorize the next experimental phase.

## Required Inputs

- private source root and a writable migration copy;
- expected PFC2D/PFC3D 5.0 product, exact observed release if available, and runtime route;
- intended entrypoint working directory and driver files;
- claimed last-good save plus its acceptance evidence;
- in-scope and explicitly excluded branches;
- external dependency names, legal access route, and optional digests;
- allowed first action, run budget, and changes that still require user approval.

If the exact runtime release is unknown, record it as unresolved. Never infer runtime
compatibility from file extensions, project metadata, or an old log alone.

## Workflow

1. Freeze scope and protect the source. Work in a migration copy; record excluded and
   paused branches before touching executable files.
2. Inventory files, verify any supplied digest manifest, and run
   `scripts/audit_pfc5_handoff.py` against the private root. Treat its result as static
   evidence only.
3. Identify the exact PFC5 product/release. If the available runtime is another major
   version, stop instead of translating syntax.
4. Classify every proposed entrypoint and save as `accepted`, `restart_only`,
   `diagnostic_only`, `failed`, `obsolete`, or `unknown`. A filename such as "final" is
   not evidence.
5. Restore the claimed last-good save first. Check object and boundary counts, extents,
   units, contact state, callbacks, and the saved acceptance metrics before an expensive
   rebuild.
6. Run the smallest portable audit or probe that can test the handoff claim. Preserve
   the original save and write new results under distinct names.
7. If recovery is needed, branch only from a state whose geometry/object invariants are
   known. Do not loosen the final gate merely because an intermediate solve stopped.
8. Complete `templates/pfc5-case-handoff.yaml`, regenerate the integrity manifest, and
   report unresolved runtime, physics, provenance, and authorization gates.

Read [portable-handoff-contract.md](references/portable-handoff-contract.md) before
packaging a handoff or selecting a recovery point.

## Privacy And Packaging Boundary

- Keep PFC projects, saves, logs, licensed sources, standards, raw inputs, calibrated
  parameters, and project-specific scripts in the private case.
- Publish only generalized instructions, empty schemas, synthetic tests, and tooling
  that does not encode the private case.
- In external summaries, report finding categories, counts, validation status, and
  unresolved gates. Omit private paths, filenames, source excerpts, hashes, material
  identities, geometry, seeds, parameters, and results unless the user explicitly asks
  for them.
- Use relative paths or placeholders in handoff documentation. A digest proves identity,
  not redistribution permission.

## Non-Negotiable Gates

- source copy protected and migration scope explicit;
- PFC5 major-version match confirmed before runtime action;
- no private absolute path or ambiguous `localdir` save behavior in the portable chain;
- every required `call` and `restore` target accounted for;
- claimed accepted save restored and checked before rebuild;
- object conservation, geometry, equilibrium, and contact-state claims recorded
  separately;
- diagnostic geometry or porosity metrics are not relabeled as physical or normative
  acceptance;
- later Burger, loading, or standard-metric phases remain pending unless already in the
  authorized scope.

## Output Contract

Deliver a private handoff manifest, integrity result, runtime identity, entrypoint/CWD
map, save-state classification, restore-first audit result, portable run sequence,
external-dependency ledger, quarantined legacy list, and exact unresolved gates. Mark
`runtime_validated` true only for the actions actually executed in PFC5.

## Local Contents

- `references/portable-handoff-contract.md` — state taxonomy, restore-first audit,
  recovery, privacy, and packaging rules.
- `templates/pfc5-case-handoff.yaml` — empty private handoff manifest.
- `scripts/audit_pfc5_handoff.py` — read-only integrity, path, dependency, and
  version-boundary auditor.
- `dependencies.json` — links to the PFC5 core and FISH owners.
- `agents/openai.yaml` — interface metadata.
