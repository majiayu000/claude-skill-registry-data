---
name: design-agent-contract
description: Design, scaffold, or refactor a production agent's contract and package. Use when defining a declarative agent specification, dependencies, typed input and output, prompts, execution classes, governance tiers, capability allowlists, or package boundaries, independent of the agent framework in use.
---

# Design an Agent Contract

Create an explicit, typed agent package whose contract can be reviewed before implementation details.

## Workflow

1. Inspect repository instructions, dependency pins, existing agent packages, and test conventions.
2. Write the behavioral contract before the prompt:
   - purpose, owner, users, and non-goals;
   - input, dependency, and output types;
   - execution class and risk assessment;
   - allowed skills and tools;
   - latency, quality, and cost objectives;
   - escalation and fallback behavior.
3. Select an execution class:
   - `ephemeral` for bounded work without externally visible side effects;
   - `durable` for retries, timers, recovery, or externally visible side effects;
   - `human_governed` for consequential operations requiring approval.
4. Use `assess-agent-risk` to select a governance tier from low, medium, high,
   or critical based on scenario-level inherent risk and mandatory floors. Keep
   residual risk and launch decision separate.
5. Create a consistent package layout. Keep orchestration, tools, runtime skills, prompts, types, policy, and tests separate.
6. If the project provides scaffolding tooling, use it, then inspect and customize every generated placeholder.
7. Implement a construction function (factory) that receives configuration and dependencies explicitly. Keep module loading free of network calls and mutable runtime work.
8. Use schema-validated types for dependencies, structured output, tool inputs, and externally persisted payloads.
9. Validate the specification with the project's own validation tooling or CI, then add contract tests for construction, output validation, capability allowlists, and failure behavior.
10. Record unresolved decisions rather than silently inventing product policy.

## Required Output

Produce or update:

- a declarative agent specification or equivalent manifest;
- a typed agent factory;
- dependency and output types;
- explicit skill and tool allowlists;
- tests and an eval entry point;
- a risk assessment covering execution class, governance tier, residual risk,
  controls, evidence, and decision.

Read [the design standard](references/standard.md) before changing architecture. Use [the examples](references/examples.md) when drafting a specification or package.

## Guardrails

- Do not hide business policy in system prompts.
- Do not give an agent every registered tool by default.
- Do not use untyped dictionaries at durable or external boundaries.
- Do not couple the agent object to durable workflow code.
- Do not declare readiness without eval, observability, and operational owners.

## Completion Check

Confirm that another engineer can answer, from repository artifacts alone: what the agent does, what it may call, what it returns, how it executes, how it fails, and how it is evaluated.
