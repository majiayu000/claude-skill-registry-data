---
name: validate-kb-extension
description: Walk every feature in every domain-taxonomy markdown file and assert the 5 required KB extension sections (Inclusion, Success Criteria, Failure Scenarios, Cross-Tree Refs, Experiential) are present and non-empty. Also validates that cross-tree constraints reference real feature IDs.
user-invocable: false
model: haiku
allowed-tools: Read, Glob, Grep, Bash
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# validate-kb-extension

Model-invocable skill for verifying the KB domain-taxonomy catalog conforms to the extension conventions defined in `core/components/memory/standards/rules/kb-extension.md`. Invoked by the `specify` play's pre-flight (214.5) and as the 214.4 T22 acceptance check.

## Purpose

Prevent shallow / incomplete KB entries from reaching the pipeline. A capability catalog with missing sections or dangling cross-tree constraint references produces downstream failures in `configure-capabilities`, `enrich-capabilities`, and `generate-intent-epics`. This skill is the single gate that enforces the contract.

## Input

Receive from the calling agent:
- `kb_root` (string, required) — path to `core/components/memory/knowledge/domain/` or the deployed equivalent
- `constraints_path` (string, required) — path to `_cross-tree-constraints.yaml` inside `kb_root`
- `conventions_path` (string, required) — path to `core/components/memory/standards/rules/kb-extension.md` (the contract)

## Process

### 1. Enumerate domain-taxonomy files

Glob `{kb_root}/*.md` excluding `_index.md` and any file beginning with an underscore. Each matched file is a domain (user-management, commerce, payments, personalization, search, plus any new domains added later).

### 2. For each domain file, extract features

Features are headed by `### {PREFIX}-F\d+:` where the prefix is domain-specific (UM, CM, PM, PS, SR, or any new prefix). Collect all feature IDs into an ordered list. A file with zero features is a structural failure — report and continue.

### 3. For each feature, validate the 5 required sections

Each feature must have these five H3 subsections nested under it, in any order:

- `### Inclusion`
- `### Success Criteria`
- `### Failure Scenarios`
- `### Cross-Tree Refs`
- `### Experiential`

For each section, apply the section-specific rules from `kb-extension-conventions.md`:

#### Inclusion
- Exactly one line starting with `- Default:` containing one of `mandatory`, `optional`, or `conditional` (wrapped in bold markers `**...**` is allowed).
- `Mandatory when`, `Conditional when`, and `Exclude when` lines are optional but if present must reference `project_profile.*` expressions.

#### Success Criteria
- Minimum 2 bullet entries.
- Each entry must contain QUANTIFIED content. Heuristic: match at least one of:
  - Number + unit (e.g., `500ms`, `5 seconds`, `10GB`, `95%`, `10K concurrent`)
  - Explicit comparison operator (`<`, `>`, `<=`, `>=`, `=`)
  - Named standard (WCAG 2.1 AA, SOC2, HIPAA, PCI-DSS, NIST)
- Vague entries like `fast`, `secure`, `reliable` (without a number or standard) are violations.

#### Failure Scenarios
- Minimum 2 bullet entries.
- Each entry must contain all three sub-fields in order: `Scenario:`, `Impact:`, `Mitigation:`. The sub-fields are indented bullets under the top-level entry.
- An entry missing any sub-field is a violation.

#### Cross-Tree Refs
- Either a list of entries matching `CTC-\d+` (with a human-readable parenthetical) OR the literal text `(none)`.
- Each `CTC-NNN` reference must exist in `{constraints_path}`. Dangling refs are violations.

#### Experiential
- Must contain `Usage count:` and `Last promoted:` fields at minimum.
- `Scenarios observed` and `Common mistakes` are optional but recommended.
- Bootstrap values are allowed: `Usage count: 0`, `Last promoted: never`.

### 4. Validate `_cross-tree-constraints.yaml`

- YAML must parse cleanly (use `python3 -c 'import yaml; yaml.safe_load(open(path))'`).
- Top-level key must be `constraints`, a list.
- Each constraint must have: `id` (format `CTC-\d+`), `description`, `condition`, at least one action (`implies_include` / `implies_exclude` / `implies_include_depth` / `implies_exclude_depth`), and `rationale`.
- Every feature ID referenced in `implies_include` or `implies_exclude` must resolve to a real feature found in step 2. Dangling refs are violations.

### 5. Aggregate results

Build a validation report grouped by file and feature:

```yaml
status: completed | failed
summary:
  total_files: <int>
  total_features: <int>
  passed_features: <int>
  failed_features: <int>
  constraint_count: <int>
  dangling_constraint_refs: <int>
files:
  user-management.md:
    status: pass | fail
    feature_count: <int>
    features:
      UM-F001:
        status: pass | fail
        violations:
          - section: "<section name>"
            rule: "<rule id>"
            detail: "<one-sentence explanation>"
      UM-F002: ...
  commerce.md: ...
constraints:
  status: pass | fail
  parse_ok: true | false
  dangling_refs:
    - constraint_id: "CTC-099"
      feature_id: "ZZ-F999"
      detail: "feature not found in any domain-taxonomy file"
```

## Output

Return the validation report as the skill's output contract. On ANY failure (any feature missing a section, any dangling constraint ref, any YAML parse error), the top-level `status` is `failed`. On clean validation, `status` is `completed`.

The calling agent treats `status: failed` as a structured failure — the parent play halts and cycles back to the KB-editing author with the report.

## Constraints

- NEVER modify any file. This skill is READ-ONLY.
- NEVER invoke other skills or agents. It operates directly on file contents.
- ALWAYS return a structured YAML report, even on success.
- ALWAYS read `conventions_path` first so the rules are checked against the contract — do not hard-code rules in skill logic.
- On YAML parse error in `_cross-tree-constraints.yaml`, abort the constraint-check phase and report the parse error. Feature validation continues independently.

## Version

| Field | Value |
|-------|-------|
| Version | 0.1.0 |
| Category | validation |
| Created | 2026-04-14 |
| Related | `core/components/memory/standards/rules/kb-extension.md`, `core/components/memory/standards/schemas/intent-epic.yaml`, `core/components/memory/knowledge/domain/_cross-tree-constraints.yaml` |
