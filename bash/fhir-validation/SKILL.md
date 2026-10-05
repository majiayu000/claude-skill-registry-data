---
name: fhir-validation
description: Validate HL7 FHIR R4 JSON resources, FHIR profile and Implementation Guide examples, and AI-created FHIR output; explain OperationOutcome and StructureDefinition issues; map defects back to FSH; and run safe validate-patch-revalidate loops. Use when the user asks for a FHIR validator, FHIR conformance check, profile validation, issue explanation, or mechanical repair. Use fhir-project-doctor for runtime/package setup and fhir-ci-quality for CI or inferred quality rules.
---

# Records FHIR Validation

Validate FHIR resources with Records and local project tooling. Prefer local or already configured execution. Do not send clinical data, patient data, FHIR server URLs, or full patient resources to external services unless the user explicitly consents for this task.

## Arguments

Treat the user request as a file, directory, JSON resource, OperationOutcome, FHIR URL, or validation goal. If no target is inferable, ask one concise question.

## Bundled Paths

Resolve `<skill-root>` to the absolute directory containing this `SKILL.md`. Resolve `<plugin-root>` two directories above `<skill-root>`. In Claude Code `${CLAUDE_PLUGIN_ROOT}` is also the plugin root; in Codex derive it from the installed skill path. Never resolve bundled scripts relative to the user's workspace.

## Fast Start

For file or directory validation, first run the deterministic detector and runtime planner when available:

```bash
node "<skill-root>/scripts/detect-fhir-project.mjs" <target-or-repo>
node "<skill-root>/scripts/plan-runtime.mjs" <target-or-repo>
```

Use their output to pick source directories, generated directories, available runtimes, privacy gates, and validation order.

Then choose the first suitable mode:

1. Records MCP tools, when available.
2. Records API, only when `RECORDS_API_URL` is configured and the privacy boundary is acceptable.
3. Records CLI, using `records validate-file <target>`.
4. Existing local profile-aware validators such as SUSHI, IG Publisher, Firely Terminal, Java validator, or HAPI when already configured and relevant.
5. Structural fallback via `scripts/validate-structural.mjs` ([scope](references/structural-validation.md)), clearly labeled as not profile-, terminology-, invariant-, or reference-aware.

## Privacy Gates

Ask for explicit consent before fetching FHIR URLs, contacting FHIR servers, sending resources to external APIs, installing validators, or using hosted/non-local validation on data that may contain PHI. Prefer local CLI validation. In summaries, include paths, issue codes, and minimal snippets; do not reproduce complete Patient resources or unnecessary identifiers.

## Repair Rules

Run validate-patch-revalidate for fixes. Patch only mechanical or clearly inferable issues. Do not invent clinical codes, identifiers, dates, references, status values, or business policy. Stop and ask for domain input when the validator is correct but the right clinical value is not present in local source data.

Generated artifacts are usually not the durable source. If an issue points at `fsh-generated/resources/*.json`, read [references/ig-workflows.md](references/ig-workflows.md) before editing. For safe/unsafe fix classification, read [references/repair-policy.md](references/repair-policy.md).

For generated FSH artifacts, prefer:

```bash
node "<skill-root>/scripts/map-generated-to-fsh.mjs" <generated-json> <project-root>
```

For PHI-sensitive summaries, prefer:

```bash
node "<skill-root>/scripts/redact-fhir-summary.mjs" <resource-json>
```

For OperationOutcome JSON or FHIR expression mapping, use the matching local helper script before free-form reasoning:

```bash
node "<skill-root>/scripts/explain-operationoutcome.mjs" <operationoutcome-json>
node "<skill-root>/scripts/map-fhir-expression.mjs" "Observation.category[0].coding[0].code"
```

## Task References

Load detail files only when the task needs them:

- IG, SUSHI, FSH, IG Publisher, Firely, HAPI, or generated-resource workflows: [references/ig-workflows.md](references/ig-workflows.md)
- OperationOutcome explanation or issue-code triage: [references/operationoutcome-map.md](references/operationoutcome-map.md)
- Safe repair boundaries and domain-input rules: [references/repair-policy.md](references/repair-policy.md)
- Runtime/package diagnosis: use the companion `$fhir-project-doctor` skill.
- Data-quality rules and CI quality gates: use the companion `$fhir-ci-quality` skill.
- Machine-readable result semantics and exit codes: [../../docs/result-contract.md](../../docs/result-contract.md)

## Output

Report:

1. Tool, mode, privacy boundary, FHIR version, validation depth, loaded profiles, and terminology mode.
2. Summary counts: errors, warnings, info, and score when available.
3. Errors first, grouped by aspect/path.
4. Safe fixes applied or recommended.
5. Remaining domain, package, terminology, or setup questions.

Always label structural fallback and Records local structural validation honestly. Do not claim full IG conformance unless a profile-aware runtime actually loaded the IG/package context.
