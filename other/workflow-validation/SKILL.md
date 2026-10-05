---
name: workflow-validation
description: "Validate a FlowWorkflow YAML at `plugins/flow/workflows/<id>.workflow.yaml` against `schemas/v1/workflow.schema.json` AND cross-reference the referenced skills/agents exist + every Tier 3 action is confirm-gated + no native /goal or /loop dependency is declared. Use when /flow:workflow validate is invoked, when CI runs the workflow schema gates, or when a new workflow is being authored. This skill MUST be consulted because schema validation alone catches shape errors; cross-reference validation catches the silent-correctness failures (typo'd skill name, Tier 3 escape, /goal dependency) that would otherwise ship to users."
allowed-tools: Bash, Read
agent: general-purpose
---

# Workflow Validation

## Contract

Iron law: a workflow that schema-validates but references a non-existent skill is a bug waiting to fire at runtime — cross-reference validation catches it at author time. Invoked by `/flow:workflow validate <id>` (read-only, Tier 1) and by CI workflow schema gates, with a workflow id that maps to `.flow/workflows/<id>.workflow.yaml` (project-local override) or `plugins/flow/workflows/<id>.workflow.yaml`. Returns the JSON report below on stdout with exit 0 (`pass`), 1 (any cross-reference, tier-3, or native-slash violation), or 2 (schema invalid). Permitted skips: none — every step runs in order; a schema failure stops after Step 1 with `overall: schema_invalid`.

## Output

```json
{
  "workflow_id": "start-issue",
  "source_file": "plugins/flow/workflows/start-issue.workflow.yaml",
  "schema_valid": true,
  "cross_reference_errors": [
    {
      "type": "missing_skill",
      "name": "specifcation-capture",
      "source_file": "plugins/flow/workflows/start-issue.workflow.yaml",
      "example": "required_skills:\n  - specification-capture  # correct spelling"
    }
  ],
  "tier3_violations": [],
  "native_slash_violations": [],
  "overall": "pass"
}
```

Every violation carries `source_file` (the YAML actually loaded) and `example` (a corrected YAML snippet); `commands/workflow.md:validate` prints both beneath each error.

## Steps

1. **Schema validation with the `completion_gate.requires` deprecation shim.** Load the YAML, rename legacy `completion_gate.requires` to `documented_requirements` in memory (WARN on stderr; when both are present drop the legacy field with a WARN), then `jsonschema.validate` in the same Python process — the CLI validator re-reads from disk and bypasses the shim. Canonical invocation: `references/workflow-validation-shim.md`. Failure → first error into `cross_reference_errors`, `overall: schema_invalid`, stop.
2. **Required skills**: for each `required_skills[]` entry, `[ -f "plugins/flow/skills/${skill_name}/SKILL.md" ]`. Missing → `{"type": "missing_skill", "name", "source_file", "example": "required_skills:\n  - <correct-skill-name>\n# check plugins/flow/skills/ for existing skill directory names"}`.
3. **Required agents**: for each `required_agents[]` entry, `[ -f "plugins/flow/agents/${agent_name}.md" ]`. Missing → `{"type": "missing_agent", ..., "example": "required_agents:\n  - <correct-agent-name>\n# check plugins/flow/agents/*.md for available agents"}`.
4. **Activity-level references**: walk `phases[].activities[]`; apply Step 2 to each `skill` field and Step 3 to each `agent` field.
5. **Tier classification**: in `tier_classification`, `merge` and `release` MUST be `confirm`, and `tag_push` MUST be `confirm` when present. Any set to `autonomous` or `journal` → `tier3_violations.append({"action", "value", "expected": "confirm", "source_file", "example": "tier_classification:\n  merge: confirm  # Tier 3 must be confirm — non-negotiable per the Iron Law"})`. **Hard fail** — matches `trigger-policy` Step 2; "No Irreversible Actions Without Approval" is non-negotiable, so a downgraded workflow is broken by construction, never a legitimate override.
6. **No native slash**: grep the YAML for `/goal\b`, `/loop\b`, `/schedule\b`, `/routine\b` outside `description` fields. Any invoked dependency (e.g., `command: /goal foo`) → `native_slash_violations`. Hard fail — plugins cannot invoke native slash commands.
7. **Completion gate**: `completion_gate.documented_requirements` is advisory free-text; commands enforce their own gates. Verify only presence and non-emptiness (the schema's `minItems: 1` already does). No cross-reference to activity `evidence` fields.
8. **Overall verdict**:

| Condition | overall |
|---|---|
| schema fails | `schema_invalid` (exit 2) |
| any `native_slash_violations` | `native_slash_present` (exit 1) |
| any `tier3_violations` | `tier3_invalid` (exit 1 — Iron Law) |
| any `cross_reference_errors` | `cross_reference_failed` (exit 1) |
| else | `pass` (exit 0) |

## Reuse map

- `plugins/flow/schemas/v1/workflow.schema.json` — schema validated against.
- `plugins/flow/workflows/*.workflow.yaml` — plugin-shipped workflows.
- `plugins/flow/commands/workflow.md` — the `/flow:workflow` dispatcher.
- `plugins/flow/references/workflow-validation-shim.md` — Step 1 Python.
