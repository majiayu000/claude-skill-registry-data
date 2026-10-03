---
name: archetype-lint
description: >
  This skill should be used when the user asks to "lint an archetype", "validate an archetype",
  "check archetype compliance", "check archetype rules compliance", or "run archetype rules". Applies
  24 normative lint rules with ERROR/WARNING/INFO severity. Supports STRICT and PERMISSIVE modes.
  Reports violations only — it does not modify files; to lint *and* remediate, use the
  `archetype-authoring` skill. Auto-invoked on lint/validate intent, and also directly invocable
  as `/archetype-lint <file or id> [strict]`.
argument-hint: "<file or id> [strict]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__terminology_resolve
---

# Archetype Lint

An openEHR archetype linting engine. Evaluate archetypes against 24 normative rules. Classify each violation as ERROR, WARNING, or INFO. ERROR means the archetype is invalid or unsafe.

## Step 1: Load Guides (MANDATORY)

```
guide_get("openehr://guides/archetypes/rules")
guide_get("openehr://guides/archetypes/structural-constraints")
guide_get("openehr://guides/archetypes/anti-patterns")
guide_get("openehr://guides/archetypes/terminology")
```

## Step 2: Determine Mode

- **STRICT**: Zero WARNING tolerance. For publication candidates and CKM submissions.
- **PERMISSIVE** (default): WARNINGs allowed with justification. For early modeling iterations.

If the user does not specify a mode, use PERMISSIVE.

## Step 3: Apply Lint Rules

The **normative rule definitions live in the `archetypes/rules` guide loaded in Step 1** — that guide is the single source of truth. If this index ever disagrees with the loaded guide, the guide wins. Use the index below for rule numbering and severity; consult the guide for each rule's full definition, rationale, and worked examples before classifying a violation.

| # | Rule | Severity | Group |
|---|------|----------|-------|
| 1 | Single Concept | ERROR | Core semantic |
| 2 | ENTRY Type Semantics | ERROR | Core semantic |
| 3 | Root RM Type Match | ERROR | Core semantic |
| 4 | Valid RM Attributes Only | ERROR | Core semantic |
| 5 | occurrences vs cardinality | ERROR | Core semantic |
| 6 | Specialisation Integrity | ERROR | Core semantic |
| 7 | Path Stability | ERROR | Core semantic |
| 8 | Term Definition Completeness | ERROR | Core semantic |
| 9 | Mandatory Data Justification | WARNING | Structural |
| 10 | Arbitrary Upper Bounds | WARNING | Structural |
| 11 | CLUSTER Semantics | WARNING | Structural |
| 12 | Slot Discipline | WARNING | Structural |
| 13 | Template Leakage | WARNING | Structural |
| 14 | Unconstrained Leaf Nodes | WARNING | ADL & AOM syntax |
| 15 | Attribute Multiplicity Compliance | ERROR | ADL & AOM syntax |
| 16 | Ontology Integrity | ERROR | ADL & AOM syntax |
| 17 | Terminology Neutrality | WARNING | Terminology |
| 18 | Semantic Binding Accuracy | WARNING | Terminology |
| 19 | Archetypable Demographics | INFO | Demographic |
| 20 | Identity vs Role Separation | ERROR | Demographic |
| 21 | Patch Version Discipline | ERROR | Versioning |
| 22 | Deprecation Handling | WARNING | Versioning |
| 23 | Prose ↔ Slot Consistency | WARNING | Documentation (guide rule D9) |
| 24 | Translation Accuracy | WARNING | Documentation (guide rule E7) |

For rule 4, verify attribute names against the RM with `type_specification_get` when uncertain.

> Offline fallback only: `skills/openehr-assistant/reference/lint-rules-complete.md` mirrors these definitions as the `clinical-modeler` agent's fallback when its read-only MCP lookups are blocked. In the main session, always prefer the loaded `archetypes/rules` guide.

### Avoid known false positives

- **`ITEM_TREE.items {0..*}` is idiomatic** — the established CKM convention for container attributes (e.g. the published `ecg_result.v1`). Do **not** flag it under rule 9 / structural-constraints when at least one contained ELEMENT is mandatory; reserve a finding for genuinely empty or all-optional containers. Flagging idiomatic `items {0..*}` is noise.
- **Unstated `occurrences`/`existence` are not violations** — ADL 1.4 defaults both to `{1..1}` when unstated. For rule 5, also check mutual consistency: the sum of sibling occurrences ranges must fit inside the container's cardinality interval (validator-tooling check `VCOC`).
- **Validity codes are tooling constructs** — mnemonics like `VARID`/`VCOC`/`VUNT` come from AOM2 and validator tooling (ADL Workbench, `archie`, CKM), not from ADL 1.4 spec text. Cite them as tool-output aids, never as "ADL 1.4 validity rules".
- **Partial terminology coverage is valid** — a `term_bindings` section need not bind every internal at-code (ADL 1.4, Term_bindings). Do **not** report unbound codes as a rule 17/18 violation; bindings are optional-but-recommended, so incomplete coverage is at most an INFO observation.

## Step 4: Generate Report

### Required Output Format

```
## Lint Report

**Archetype:** <archetype-id>
**Mode:** STRICT | PERMISSIVE
**Overall Status:** PASS | FAIL

### Violations

| # | Severity | Rule | Explanation | Suggested Fix |
|---|----------|------|-------------|---------------|
| 1 | ERROR    | R4   | Attribute `blood_pressure` is not a valid RM attribute on ITEM_TREE | Use `items` (valid RM path) |

### Summary
- ERRORs: N
- WARNINGs: N
- INFOs: N
```

**Gating logic:**
- Any ERROR -> overall status = FAIL
- STRICT mode: any WARNING -> overall status = FAIL
- PERMISSIVE mode: WARNINGs allowed if justified

## Step 5: After the Report (routing only)

This skill reports; the report's **Suggested Fix** column is the ceiling of what it provides. When the user asks for a fix plan or for fixes to be applied, route to the `archetype-authoring` skill — its fix-syntax mode for parse/structure errors, its review-remediate pipeline (minimal-diff plan, path/semantics impact, version-bump justification) for semantic findings.
