---
name: fhir-ci-quality
description: Generate or review FHIR validator CI workflows and derive candidate healthcare data-quality rules from local FHIR examples. Use when the user asks to add FHIR validation to GitHub Actions or another CI/CD system, create conformance quality gates, infer project conventions, or turn recurring validation expectations into reviewed automation.
---

# FHIR CI and Quality

Create repeatable checks without turning observed sample data into unreviewed clinical policy.

## Bundled paths

Resolve `<skill-root>` to the directory containing this `SKILL.md` and `<plugin-root>` two directories above it. Shared deterministic tools live under `<plugin-root>/skills/fhir-validation/scripts`. Never resolve them relative to the user's workspace.

## Workflow

1. Inspect the existing project scripts, package files, generated-artifact policy, and CI conventions.
2. Diagnose runtime/package readiness with `$fhir-project-doctor` before generating a workflow when the runtime is unclear.
3. Derive candidate rules and generate a starting workflow:

   ```bash
   node "<plugin-root>/skills/fhir-validation/scripts/derive-quality-rules.mjs" <resource-directory>
   node "<plugin-root>/skills/fhir-validation/scripts/generate-ci.mjs" --json --dir <resource-directory>
   ```

4. Review every inferred rule. Treat identifiers, code systems, profiles, cardinalities, and status values as domain policy unless directly required by a loaded FHIR profile.
   Write only `artifact.content` from the CI generator to the proposed workflow path.
5. Pin third-party CI dependencies, use least-privilege permissions, avoid printing full resources, and keep hosted/API validation behind explicit privacy approval.
6. Validate the workflow syntax and run the local validation command before handing it back.

## Modes

- Use local Records CLI by default.
- Add `--sushi` when the repository owns FSH and must rebuild generated resources.
- Add `--api` only when the user approves hosted validation and CI secrets are already in scope.
- Add `--upload-artifact` only for redacted or non-PHI reports.

## Output

Report runtime assumptions, privacy boundary, reviewed versus rejected candidate rules, changed CI files, and the exact local verification performed. Preserve the tools' contract and never describe inferred rules as authoritative without review.
