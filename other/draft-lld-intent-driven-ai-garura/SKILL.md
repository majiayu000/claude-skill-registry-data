---
name: draft-lld
description: Create a tech.yaml artifact with project structure, libraries, data model, components, design decisions, and feature mapping from features and architecture specifications
user-invocable: false
model: sonnet
allowed-tools: Read, Write
---

# draft-lld

Model-invocable skill for creating low-level design specifications as structured YAML.

## Purpose

Transform a features specification and architecture specification into a `tech.yaml` artifact. Captures the implementation-level detail: how the logical architecture breaks down into buildable components, which libraries are used, what the data model looks like, and how features map to components.

This skill produces ONLY `tech.yaml`. Execution order, implementation phases, scenario gates, and phase sequencing are produced by a separate skill and live in `plan.yaml`.

You DO create the tech.yaml artifact. You do NOT validate it, produce plan.yaml, or decide what happens next.

## Output Schema

The output MUST conform to `schemas/tech.yaml` in this skill's directory. Read the schema before producing output. Every field defined in the schema must be present in the output YAML. The schema is the contract — if it's in the schema, it's in the output.

## Input

Receive from agent:
- `features_yaml_path` — (required) Path to features.yaml
- `architecture_yaml_path` — (required) Path to architecture.yaml
- `output_base` — (required) Base path for output, e.g., `.garura/product/architecture/`

## Process

1. **Read inputs:** Load features.yaml and architecture.yaml. Extract: feature list with behaviors, system architecture (deployment units, topology), technology stack (concrete selections), platforms, integrations, NFRs, and design principles.

2. **Determine artifact path:** `{output_base}/tech.yaml`

3. **Check for existing artifact:** Read path. If LOCKED, return structured failure: "tech.yaml is LOCKED -- drop to DRAFT first." If DRAFT exists, overwrite (agent re-triggered DRAFT).

4. **Compose tech.yaml:** Build the artifact conforming to the tech.yaml schema. Every section must be populated. Derive all content from features.yaml and architecture.yaml -- do not invent new technology choices.

   **Top-level fields:**
   - `slug` — from features.yaml slug
   - `status` — always `DRAFT`
   - `created_at`, `updated_at` — current ISO-8601 timestamp
   - `features_ref` — path to features.yaml
   - `architecture_ref` — path to architecture.yaml

   **`project_structure` section:**
   - `directories` — list of directory paths with purpose annotations. Cover all deployment units from architecture.yaml. Each directory: path, purpose.
   - `key_files` — list of significant configuration, entrypoint, and shared files. Each file: path, purpose.
   Structure must be consistent with the component definitions written later in this same artifact.

   **`libraries` section:** Implementation-level library selections -- the concrete packages and modules used within the stack chosen in architecture.yaml. Stack-level choices (React, Python) live in architecture.yaml; this is the next level down (e.g., zustand for state, pydantic for validation, zod for schemas). For each library: name, version (or version range), purpose, component (which core component uses it), rationale.

   **`data_model` section:**
   - `entities` — list of entities with fields (name, type, constraints) and indexes
   - `relationships` — list of entity relationship descriptions
   - `migration_notes` — strategy for schema evolution
   Skip this section only if the product has no persistent data layer -- set to null with a comment.

   **`components` section:** One entry per major buildable unit (server, client, worker, service, shared library, module). For each component:
   - `name` — component name (e.g., api-server, web-client, worker, shared-lib)
   - `type` — server | client | worker | service | library | module
   - `responsibility` — single responsibility description
   - `interfaces` — list of public interfaces, methods, or endpoints
   - `dependencies` — list of other components or external dependencies
   - `key_files` — list of key file paths within this component
   - `libraries` — list of library names from the libraries section used by this component
   - `internal_structure` — description of how this component is organized internally (e.g., routes/, services/, models/, middleware/ subdirectories)
   Components must be consistent with deployment units in architecture.yaml and directory structure in project_structure.

   **`design_decisions` section:** Implementation-level decisions not captured in architecture.yaml -- error handling strategy, naming conventions, config management, internal API contracts, code organization patterns. Each decision: id (DD1, DD2, ...), context, decision, consequence.

   **`feature_mapping` section:** For each feature in features.yaml, produce a mapping entry:
   - `feature_ref` — feature ID (F1, F2, ...)
   - `feature_name` — feature name from features.yaml
   - `components` — which components implement this feature
   - `data_entities` — which data entities this feature reads or writes
   - `libraries` — which libraries this feature depends on
   - `key_files` — the most important files for implementing this feature
   - `implementation_notes` — gotchas, patterns to follow, edge cases specific to this feature

5. **Validate consistency:** Before writing, verify:
   - Every file path in key_files and components is consistent with project_structure directories
   - Every library referenced in feature_mapping and components exists in the libraries section
   - Every component referenced in feature_mapping exists in the components section
   - Every entity referenced in feature_mapping exists in the data_model entities

6. **Write artifact:** Write `tech.yaml` at `{output_base}tech.yaml` with `status: DRAFT`.

7. **Return output.**

## Output

```yaml
tech_yaml:
  path: "{full path to tech.yaml}"
  tech_yaml_path: "{full path to tech.yaml}"
  sections:
    - project_structure
    - libraries
    - data_model
    - components
    - design_decisions
    - feature_mapping
  component_count: {number of components}
  feature_mapping_count: {number of features mapped}
  status: "DRAFT"
```

**IMPORTANT**: This skill produces an artifact and returns metadata. The calling agent receives this output and decides what to do next. Do NOT instruct the agent to return or stop.

## Constraints

### SCOPE (THIS SKILL)
- This skill produces ONLY `tech.yaml` -- project structure, libraries, data model, components, design decisions, feature mapping
- NEVER produce execution order, implementation phases, scenario gates, or phase sequencing in this artifact -- those belong in `plan.yaml`
- NEVER include scenario IDs (e.g., SC-CAP-001) anywhere in tech.yaml
- NEVER reference the scenarios document

### CONSISTENCY
- ALWAYS derive technology decisions from architecture.yaml -- do not invent new stack choices
- ALWAYS ensure file paths in components and feature_mapping are consistent with project_structure directories
- ALWAYS ensure libraries referenced in feature_mapping exist in the libraries section

### ARTIFACT RULES
- NEVER overwrite a LOCKED tech.yaml -- return structured failure
- ALWAYS set `status: DRAFT` in the written artifact
- ALWAYS include all six sections (project_structure, libraries, data_model, components, design_decisions, feature_mapping)
- ALWAYS produce a feature_mapping entry for every feature in features.yaml

## Version

| Field | Value |
|-------|-------|
| Version | 2.0.0 |
| Category | design |
