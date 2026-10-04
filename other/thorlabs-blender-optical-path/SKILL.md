---
name: thorlabs-blender-optical-path
description: Design new measurement paths or reconstruct, audit, and revise Blender optical-table systems from measurement requirements, 2D schematics, and provenance-bound CAD. Use for high-fidelity optics-only models, Thorlabs-compatible optomechanics, optical topology, whole-system validation, or publication renders with scoped physical evidence.
---

# Thorlabs Blender Optical Path

Turn a measurement requirement or 2D optical schematic into a physically explainable, independently auditable Blender scene.

## Load the relevant references

- Read [physical-gates.md](references/physical-gates.md) before geometry, CAD placement, or mechanical review.
- Read [evidence-contract.md](references/evidence-contract.md) before declaring any PASS or preparing a release.
- Read [history-derived-rules.md](references/history-derived-rules.md) when revising an existing scene or when old fixes may have regressed.
- Read [project-case-study.md](references/project-case-study.md) for the complete G1/G2 2D-to-3D example.
- Read [fresh-design-and-rendering.md](references/fresh-design-and-rendering.md) when the user requests a new measurement path, uses an old example as a quality reference, excludes electronics, or reports inadequate detail/beam visibility.
- Read [end-to-end-workflow.md](references/end-to-end-workflow.md) before a whole-system build or large forward test. Use its single-run ledger instead of splitting one system into independently authored modules.
- Read [multi-run-qualification.md](references/multi-run-qualification.md) before a Skill release or scale/stress campaign that must compare multiple fresh whole-system runs.

## Authority and revision rules

1. Apply system constraints first, then the newest explicit user wording or annotated screenshot, then active project rules, then this general skill, and only then older artifacts or PASS labels.
2. Freeze submitted or accepted packages. Make corrections in an active revision without overwriting frozen evidence; group related fixes before submission instead of publishing a version for every preview.
3. Keep one writer, run ID, revision root, deterministic generator lineage, saved-Blend lineage, and workflow ledger for the whole system. Use helpers only as read-only reviewers unless an isolated non-shared asset scope is explicit; never stitch independently authored modules into a whole-system claim.
4. Translate every correction into object families, world-space geometry, a measurable gate, and required evidence before editing.
5. Use `BLOCKED` or `UNVERIFIED` when real geometry or evidence is missing. File existence, imported CAD, process success, labels, AABB contact, and self-reported text are not proof.

## Core workflow

First distinguish a new measurement design from a reconstruction, an existing-scene correction, or a presentation-only rerender. Record which inputs are design authority, reusable assets, or visual references. When the user asks for a new path at the quality of an old example, derive a new topology and build from an empty scene; the old scene is not the starting model. For optics-only requests, exclude electrical/data/circuit visualization while retaining optical detectors and their mechanical supports.

1. Initialize one whole-system run spec, state ledger, and append-only event hash chain with `scripts/workflow_ledger.py`; record every gate, artifact hash, blocker, invalidation, and next authorized action there.
2. Build a machine-readable map: `schematic node -> experimental role -> real asset -> optical/fiber/electrical ports -> support path`.
3. Inventory every directed edge, branch, optional/deferred node, component, beam segment, beam height, aperture, connector, and required detector endpoint. Never invent reciprocal edges.
4. Acquire official CAD only from manifest-locked manufacturer URLs into a private cache. Verify byte count and SHA-256 before atomic placement; record part number, source URL, unit scale, bbox, local optical axis, surface normal, aperture, provenance, and redistribution boundary. Mark modeled or surrogate parts explicitly and never publish vendor geometry without an explicit grant.
5. Treat each source lock and its hashed files as one atomic input bundle. Before geometry, run a producer-to-consumer artifact preflight: every locked source byte, canonical and part-qualified CAD cache key, official drawing, and required runtime must exist at the exact path/key used by the next script. Validate structured authority inputs as typed exact sets before lookup; missing, duplicate, extra, legacy, malformed, or identity-mismatched records must produce a durable structured `BLOCKED` result rather than an exception or silently collapsed entry.
6. Publish deterministic source locks and replay them before geometry. The public scripts must reproduce the normalized semantic parameters with zero unexplained field differences; encode every override in source with a reason. For multi-state systems, every edge has exact `active_states` or a hashed deterministic expansion, and every declared state has explicit ray templates.
7. Solve optical constraints first: centers, surface normals, reflection, splitting planes, branch endpoints, and zero-radius clearance. Keep design coordinates separate from measured reopened mesh/port witnesses; constant zero errors and endpoint-family matches cannot prove aperture or first-hit acceptance.
8. Solve mechanics post-first from verified table holes through real fasteners, clamps, holders, posts, mount faces, and device interfaces.
9. Fix the shared placement or transform root cause. Prove one representative repeated assembly inside the same run before propagation, then reopen and recheck every copy.
10. Render bright audit views before beauty views. Use cutaways or transparency only to expose hidden, already-measured interfaces.
11. Complete the saved-scene, whole-system, visual, export, derived-claim, binary-sanitization, hash, and rule-compliance gates in the same ledger.

## Required semantic separation

- Treat free-space optical rays, guided fiber, and electrical/coaxial cables as different object families, materials, ports, and audit records.
- Terminate free-space light at the physical coupling surface; continue only the guided fiber from the ferrule/FC interface.
- Use open geometry for apertures and slits. A centered ray through an opaque disk is a collision, not a PASS.
- Remove duplicate surrogates and unexplained placeholders after the real or declared modeled assembly exists.

## Publication rendering

Use low-cost diagnostic previews to review device detail, beam readability, and framing. Label them as previews with physical gaps explicit. After physical gates pass, produce final editorial views with restrained metals, readable black-anodized edges, modest glass, thin emissive beam cores, soft halos, and uncluttered labels. Preserve geometry and material-slot semantics through presentation changes. Inspect component close-ups and every declared branch; whole-image sharpness, edge density, or colored-pixel totals alone do not prove fidelity or continuity. Verify the actual requested output dimensions; a 2K preview does not satisfy a 4K delivery.

Once the requested checks pass, freeze one delivery and publish once. Recheck affected dependencies after a change, identity drift, or failed test; do not restart unchanged successful gates or open additional variants for optional polish. Skill documentation releases may record limitations without granting model-release credit; see [multi-run-qualification.md](references/multi-run-qualification.md).

## Completion language

- `PASS`: every applicable active gate has fresh evidence.
- `PARTIAL/SCOPED`: only a declared subset was audited; enumerate blockers and keep final/release approval false.
- `UNVERIFIED`: required evidence is missing or cannot distinguish the claim.
- `BLOCKED`: a known requirement fails.

Never promote `PARTIAL/SCOPED` to whole-system PASS.
