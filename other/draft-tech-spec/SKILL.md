---
name: draft-tech-spec
description: Produce tech.yaml — project structure, library picks, build/test tooling, runtime configuration — from a features spec, technical approach, and architecture inference. Used by tech-architect in the prepare play.
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Grep, Glob
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# draft-tech-spec

Model-invocable skill for authoring `tech.yaml` — the implementation-ready technical specification.

## Purpose

Given upstream specification artifacts (features, technical-approach, architecture-inference), produce a concrete `tech.yaml` naming every library, build tool, test framework, runtime config, and project layout detail needed to begin implementation. No vague references ("a logging library") — every field names a specific technology with a rationale.

Previously authored inline by tech-architect.

## Input

| Field | Required | Description |
|-------|----------|-------------|
| `features_yaml_path` | yes | Path to features.yaml |
| `technical_approach_path` | optional | Path to technical-approach.md if drafted |
| `architecture_inference_path` | optional | Path to architecture-inference.yaml if this is a brownfield project |
| `project_profile_path` | optional | Path to project-profile.yaml for appetite / scale / compliance context |
| `ltm_architecture_path` | optional | Path to core LTM architecture knowledge |
| `output_base` | yes | Directory to write tech.yaml |

## Process

1. **Read features.yaml.** Extract product identity, behaviors, architectural invariants, scope.

2. **Read technical-approach + architecture-inference if provided.** Capture technology decisions already made upstream. In brownfield projects, PREFER continuing existing tech choices over introducing new ones.

3. **Read project profile.** Scale / compliance / security / delivery-ambition values influence library selection (e.g., high-compliance → prefer libraries with audit posture).

4. **Select specific technologies** for every required slot. Cite rationale per pick — reference LTM "When to Choose" matches when available, or cite the brownfield evidence.

5. **Emit tech.yaml:**

   ```yaml
   slug: "{from features}"
   status: DRAFT
   created_at: "{ISO-8601}"
   project_structure:
     layout: "{monorepo | single-package | ...}"
     top_level_dirs: [ ... ]
   language_runtime:
     primary: "{e.g., Python 3.12}"
     secondary: [ ... ]
   libraries:
     web_framework: { name: "...", version_pin: "...", rationale: "..." }
     orm_or_data: { ... }
     validation: { ... }
     logging: { ... }
     auth: { ... }
     # ... every slot required by features + architecture
   build_tooling:
     package_manager: { ... }
     builder: { ... }
     linter: { ... }
     formatter: { ... }
     type_checker: { ... }
   testing:
     unit: { framework, pattern }
     integration: { framework, pattern }
     e2e: { framework, pattern }
   runtime_config:
     config_source: "{env | yaml | toml | ...}"
     secret_source: "{vault | env | ...}"
   observability:
     logs: { ... }
     metrics: { ... }
     tracing: { ... }
   rationale_index:
     - decision: "{technology slot}"
       choice: "{picked}"
       source: "ltm | brownfield | profile | approach"
       reason: "{one line}"
   ```

## Output

```yaml
tech_yaml_path: "{output_base}/tech.yaml"
library_slots_filled: {n}
status: written
```

## Boundaries

- Every library / tool slot MUST be filled with a specific technology — no "TBD", no "a suitable choice", no "any {category}".
- Every choice MUST have a rationale citing a source (LTM / brownfield evidence / profile / upstream approach).
- You do not draft the implementation plan (that is `draft-implementation-plan`'s job).
