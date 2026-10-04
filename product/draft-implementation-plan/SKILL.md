---
name: draft-implementation-plan
description: Create a plan.yaml artifact — execution order of features as vertical slices with scope items, exit gates, and scenario gates
user-invocable: false
model: sonnet
allowed-tools: Read, Write
---

# draft-implementation-plan

Model-invocable skill for creating the implementation execution plan as structured YAML.

## Purpose

Transform features, architecture, tech, and scenarios specifications into a `plan.yaml` artifact. The plan sequences features as vertical slices: which feature to build first, what files to touch, how to know it works (exit gate), and which scenarios must pass before moving on (scenario gate).

Features ARE the vertical slices. Each feature delivers end-to-end capability. This skill puts them in execution order and maps each to concrete scope items with file paths.

You DO create the plan.yaml artifact. You do NOT validate it, execute the plan, or decide what happens next.

## Output Schema

The output MUST conform to `schemas/plan.yaml` in this skill's directory. Read the schema before producing output. Every field defined in the schema must be present in the output YAML. The schema is the contract — if it's in the schema, it's in the output.

## Input

Receive from agent:
- `features_yaml_path` — (required) Path to features.yaml
- `architecture_yaml_path` — (required) Path to architecture.yaml
- `tech_yaml_path` — (required) Path to tech.yaml
- `scenarios_yaml_path` — (required) Path to scenarios.yaml
- `output_base` — (required) Base path for output, e.g., `.garura/product/roadmap/`

## Process

1. **Determine artifact path:** `{output_base}/plan.yaml`

2. **Read all inputs:**
   - `features.yaml` — extract features list with IDs, names, dependencies, priorities, foundation flags
   - `architecture.yaml` — extract dependency sequence, architecture impact
   - `tech.yaml` — extract project structure, components, feature mapping (which feature uses which components/files)
   - `scenarios.yaml` — extract feature gates (which scenarios must pass per feature)

3. **Determine execution order:**
   - Foundation features first (features with `foundation: true`)
   - Respect `depends_on` — a feature cannot come before its dependencies
   - Higher priority (P1) before lower (P2, P3) when dependencies allow
   - Features with more downstream dependents earlier
   - Result: ordered list of features with rationale for each position

4. **Build prerequisites (Phase 0):**
   - Project scaffold, CI setup, base configuration
   - Derive from `tech.yaml` project structure — what must exist before any feature implementation
   - Exit gate: observable outcome (e.g., "project builds, CI green")
   - No scenario gate (Phase 0 has no scenarios)

5. **Build scope items per feature:**
   - For each feature in execution order, read `tech.yaml` feature_mapping to get:
     - Components involved
     - Key files
     - Data entities
     - Libraries
   - Create numbered scope items, each with description and key_files
   - Every scope item MUST map to specific file paths — no vague descriptions

6. **Assign exit gates:**
   - Each feature gets an observable exit gate
   - Must be testable — not internal state
   - Derive from the feature's success_scenarios in features.yaml
   - Example: "User can log in via OAuth, session persisted to database"

7. **Assign scenario gates:**
   - For each feature, read `scenarios.yaml` feature_gates to get required scenario IDs
   - Map scenario IDs to the feature's position in execution order
   - Reference by ID only — no scenario descriptions in plan.yaml (compartmentalization)
   - Every feature (except prerequisites) must have at least one scenario in its gate

8. **Build execution summary:**
   - Per-feature row: sequence, feature_ref, delivers (one-line), scope_items count, scenario_count, cumulative_scenarios
   - Totals: total_features, total_scope_items, total_scenarios

9. **Write plan.yaml** to `{output_base}/plan.yaml` conforming to schema.

## Constraints

- **Vertical slices:** Each feature in the execution order delivers end-to-end working capability
- **File path mapping:** Every scope item maps to specific files — no "implement the authentication module" without file paths
- **Compartmentalization:** Scenario IDs only in scenario_gate — no scenario descriptions, no scenario content
- **Observable exit gates:** Exit gates describe what can be observed/tested, not internal state
- **No design content:** Design decisions, data models, component specs live in tech.yaml — not here
- **Dependency respect:** Execution order must not violate feature dependencies from features.yaml

## Output

Write `plan.yaml` to `{output_base}plan.yaml`.

Return to agent:
```json
{
  "plan_yaml_path": "{output_base}/plan.yaml",
  "feature_count": "{number of features in execution order}",
  "total_scope_items": "{total scope items across all features}",
  "total_scenarios": "{total scenarios across all gates}"
}
```

## Failure Modes

Return structured failure (do not write partial file) if:
- Any input file missing or unreadable
- features.yaml has circular dependencies (cannot determine order)
- scenarios.yaml has no feature_gates (cannot assign scenario gates)
- tech.yaml has no feature_mapping (cannot determine file paths per feature)

```json
{
  "error": "{error_type}",
  "message": "{human-readable description}",
  "domain_assessment": {
    "responsible_domain": "product|tech",
    "fix_suggestion": "{what needs to happen}"
  }
}
```

## Version

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Created | 2026-03-16 |
| Schema | schemas/plan.yaml |
