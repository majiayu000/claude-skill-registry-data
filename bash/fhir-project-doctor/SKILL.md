---
name: fhir-project-doctor
description: Inspect an HL7 FHIR, FSH/SUSHI, or Implementation Guide project for validator runtimes, FHIR package dependencies, cache state, version signals, privacy gates, and setup blockers. Use when FHIR validation cannot start, profiles or packages are missing, IG Publisher/Firely/HAPI/Records availability is unclear, or the user asks to diagnose or prepare a FHIR conformance project.
---

# FHIR Project Doctor

Diagnose the project before changing resources or installing tooling. Do not validate or repair clinical content unless the user separately asks for `$fhir-validation`.

## Bundled paths

Resolve `<skill-root>` to the directory containing this `SKILL.md` and `<plugin-root>` two directories above it. Shared deterministic tools live under `<plugin-root>/skills/fhir-validation/scripts`. Never resolve them relative to the user's workspace.

## Workflow

1. Run the detector, runtime planner, and package doctor:

   ```bash
   node "<plugin-root>/skills/fhir-validation/scripts/detect-fhir-project.mjs" <target>
   node "<plugin-root>/skills/fhir-validation/scripts/plan-runtime.mjs" <target>
   node "<plugin-root>/skills/fhir-validation/scripts/doctor-packages.mjs" <target>
   ```

2. Separate findings into project signals, runtime availability, FHIR-version compatibility, missing packages, and actions requiring consent.
3. Prefer already configured local tools. Do not install tools, download packages, contact terminology services, or access FHIR URLs without explicit consent.
4. Treat missing declared packages and mixed/unsupported FHIR versions as blockers for claims of profile-aware validation.
5. Recommend the smallest next action. Do not claim that structural fallback proves profile, invariant, terminology, canonical, or cross-document-reference conformance.

## Output

Report the selected runtime, privacy boundary, detected FHIR version(s), validation depth available, package blockers, and ordered next actions. Preserve the tools' `schemaVersion`, `tool`, `mode`, `capabilities`, `warnings`, and `nextActions` fields when summarizing.
