---
name: new-module
description: Design and scaffold a new module (boundary, subdomain, recipe, contracts, ADR, profile diff, fitness tests). Manual command.
argument-hint: "<business capability the module owns>"
disable-model-invocation: true
---
Act as orchestrator using skill `orchestration`, class XL/structural. The text after the command is the capability.
Pipeline: researcher (existing code/tables for the capability) → architect (`architecture-selection` phases 3–5 for this module; no overlap with existing `purpose`; ADR + profile diff) → **G0** → planner (skeleton per recipe: projects/folders, `{M}Module`, Contracts, DbContext + schema, first slice via `New-Slice.ps1`) → **G1** → implementer → test-engineer (extend architecture tests) → reviewer.
