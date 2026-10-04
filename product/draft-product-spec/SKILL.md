---
name: draft-product-spec
description: Create a features.yaml artifact defining product identity, invariants, scope, and features with IDD fields from product intent
user-invocable: false
model: sonnet
allowed-tools: Read, Write
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# draft-product-spec

Model-invocable skill for creating product feature specifications as structured YAML.

## Purpose

Synthesize a product intent (optionally enriched by a locked vision and/or roadmap with scoped epics) into a structured `features.yaml` artifact. Writes the specification to the project STM.

The features.yaml defines WHAT the product does and how it behaves. It MUST NOT define HOW it is built. Technology choices, implementation patterns, runtime topology, library names, SDK references, database products, hosting platforms, and deployment decisions are forbidden in this artifact.

You DO create the features.yaml artifact. You do NOT validate it, produce verification scenarios, or decide what happens next.

## Output Schema

The output MUST conform to `schemas/features.yaml` in this skill's directory. Read the schema before producing output. Every field defined in the schema must be present in the output YAML. The schema is the contract — if it's in the schema, it's in the output.

## Input

Receive from agent:
- `intent` -- (required) Product intent description
- `vision_path` -- (optional) Path to a locked vision.md for enrichment
- `roadmap_path` -- (optional) Path to roadmap artifacts with scoped epics for enrichment
- `output_base` -- (required) Base path, e.g., `.garura/product/roadmap/`

## Process

1. **Resolve enrichment sources:** If `vision_path` provided, read it. If DRAFT (not LOCKED), log a warning but proceed -- the vision is not yet validated. If `roadmap_path` provided, read roadmap artifacts for epic scope. These are enrichment inputs, not gates -- the skill proceeds with whatever is available.

2. **Determine artifact path:** `{output_base}features.yaml`

3. **Check for existing artifact:** Read path. If a LOCKED features.yaml exists, return structured failure: "features.yaml is LOCKED -- drop to DRAFT first." If a DRAFT exists, overwrite (agent re-triggered DRAFT).

4. **Strip technology references:** Scan intent, vision, and roadmap inputs for technology names, library references, SDK mentions, database products, hosting platforms, deployment patterns, or implementation details. Strip all of them. features.yaml is audience-scoped to product stakeholders only -- no implementation language is permitted.

5. **Compose features.yaml:** Build the artifact conforming to the features.yaml schema. Populate every top-level field and every feature entry with all required fields. Draw from intent and available enrichment sources.

   **Top-level fields:**
   - `slug` — derived from product name
   - `status` — always `DRAFT`
   - `created_at`, `updated_at` — current ISO-8601 timestamp
   - `product_ref` — path to product.yaml if available, else empty string

   **`identity` section:** what_it_is, what_it_is_not, core_jobs, non_goals. Derived from intent and vision problem statement / value proposition.

   **`invariants` section:** Behavioral constraints that any faithful implementation must honor. These are behavioral rules, not technology constraints. Derived from vision strategic goals and intent. Each invariant gets a stable ID (INV1, INV2, ...).

   **`scope` section:** in_scope list, out_of_scope list, and deferred entries with capability + rationale. Derived from vision out-of-scope, roadmap epic boundaries, and intent constraints.

   **`features` section:** One entry per distinct feature. Each feature is a vertical slice delivering end-to-end capability. Populate all fields:
   - `id` — F1, F2, ... (stable, sequential)
   - `name` — short noun-phrase title
   - `strategic_goal_ref` — reference to strategic goal if available
   - `description` — 2-3 sentences on what this feature delivers
   - `priority` — P1, P2, or P3
   - `depends_on` — list of feature IDs this depends on (empty list if none)
   - `foundation` — true if this is a foundational investment, false otherwise
   - `blast_radius` — existing_systems, affected_workflows, integration_points, migration_required, notes. For greenfield: describe where this fits in the broader landscape. Fields may be empty lists / null if too early to assess.
   - `intent` — p1 (problem today), p2 (outcome after), p3 (strategic connection)
   - `constraints` — in_scope, out_of_scope, must_not_break
   - `success_scenarios` — list of given/when/then entries (observable outcomes, not test IDs)
   - `failure_conditions` — list of observable failure states (output states, not process events)
   - `behaviors` — list of behaviors within this feature, each with id (F{N}-B{N}), description, interaction, observable_outcome

   **DO NOT include:** effort fields, scenario ID references, test case links, or any back-reference to scenarios.yaml. Features never link to scenarios -- scenarios link back here.

6. **Write artifact:** Write features.yaml with `status: DRAFT`.

7. **Return output.**

## Output

```yaml
features_yaml:
  path: "{full path to features.yaml}"
  features_yaml_path: "{full path to features.yaml}"
  feature_count: {number of features}
  invariant_count: {number of invariants}
  status: "DRAFT"
  enrichment_used:
    vision: true | false
    roadmap: true | false
```

**IMPORTANT**: This skill produces an artifact and returns metadata. The calling agent receives this output and decides what to do next. Do NOT instruct the agent to return or stop.

## Constraints

- NEVER include technology names, SDK references, database products, hosting platforms, library names, deployment patterns, or implementation details in the output artifact
- NEVER overwrite a LOCKED features.yaml -- return structured failure
- NEVER include scenario IDs or references to scenarios.yaml in any feature field
- NEVER add an effort field -- effort does not belong in features.yaml
- ALWAYS set `status: DRAFT` in the written artifact
- ALWAYS include all top-level sections (identity, invariants, scope, features)
- ALWAYS include all IDD fields for every feature (intent, constraints, success_scenarios, failure_conditions)
- ALWAYS include blast_radius for every feature (fields may be empty but the block must be present)
- ALWAYS include behaviors for every feature (at least one behavior per feature)
- ALWAYS ensure success_scenarios use given/when/then structure with observable outcomes
- Audience is product stakeholders only -- no implementation audience language

## Version

| Field | Value |
|-------|-------|
| Version | 2.0.0 |
| Category | drafting |
