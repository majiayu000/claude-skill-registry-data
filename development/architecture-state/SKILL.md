---
name: architecture-state
description: >
  Trigger: architecture review, project state, toolchain detection,
  architecture style. Record verified architecture facts for downstream work.
license: MIT
metadata:
  author: andresnator
  version: "2.0.1"
  status: testing
---

# Architecture State

## Contract

Record current architecture facts. Do not rank problems, propose changes, inspect code style; `repo-issues` owns judgments and fitness functions.

Every claim needs `file:line`. Manifests, build files, configs, imports, deployment descriptors beat README claims; README-only facts `aspirational`.

## Inspect

- Languages, declared runtime versions.
- Build and dependency tooling, including lockfiles.
- Frameworks, platforms from dependencies.
- Modules, dependency edges from manifests, imports, or healthy code graph.
- Nested manifests, `.git` entries. Multiple independent projects require per-project facts.
- Tests, CI, existing architecture checks.

Classify each project's dominant style as `layered`, `hexagonal/ports-adapters`, `modular monolith`, `microservices`, `event-driven`, or `big-ball-of-mud`. Name evidence, strongest counter-evidence. Multi-project targets: also classify workspace composition as `monorepo`, `aggregator`, `app-plus-tooling`; never assign one project style to whole workspace.

## Output

```yaml
project_state:
  languages: [{name, version, evidence}]
  toolchain: [{tool, evidence}]
  frameworks: [{name, evidence}]
  modules: [{name, path, depends_on, evidence}]
  style: {dominant, evidence, deviations}
  tests_ci: {test_framework, ci, architecture_checks, evidence}
  workspace: {layout, evidence} # multi-project only
  projects: [{name, path, languages, toolchain, style}] # multi-project only
unknowns: []
```

No duplicate prose. Preserve uncertainty in `unknowns`; never guess missing versions, edges, styles.
