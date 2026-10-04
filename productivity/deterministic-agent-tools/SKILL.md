---
name: deterministic-agent-tools
description: Use this skill when designing mine-rs deterministic tools, JSON schemas, VFS artifacts, task tools, subagents, verifier agents, LangGraph-style orchestration, agentic workflows, or AI-native automation over mining SDK functions.
---

# Deterministic agent tools skill

Use this skill when a task involves tools for agents, structured contracts, VFS artifacts, task orchestration, subagents or verifier logic.

## Source of truth

Read these files first:

1. `docs/references/agentic-layer.md`
2. `docs/references/repository-strategy.md`
3. `docs/references/domain-capabilities.md`
4. `AGENTS.md`

## Central rule

```text
Agents reason and orchestrate.
Deterministic tools calculate and validate.
```

Agents must not invent mining calculations. They must call SDK-backed tools and explain results from structured outputs.

## Ownership

- `mine-tools` owns deterministic tool contracts and SDK-backed execution.
- `python/mine-agents` owns Python-first orchestration, prompts, task tools, subagents and graph runtime.
- Optional Rust crates may own deterministic VFS or verifier components if needed.
- The SDK must not depend on the agentic layer.

## Tool contract checklist

Every tool should define:

- Name.
- Purpose.
- Input schema.
- Output schema.
- Error schema.
- Assumptions.
- Required model/data references.
- Produced artifacts.
- Version.

## Initial tools

Prioritize:

- `inspect_model`.
- `validate_model`.
- `query_blocks`.
- `aggregate_blocks`.
- `grade_tonnage`.
- `create_scenario`.
- `evaluate_scenario`.
- `compare_scenarios`.

## Workflow procedure

1. Identify the user objective.
2. Translate the objective into deterministic tool calls.
3. Validate model/data before downstream calculations when quality matters.
4. Store intermediate outputs as VFS artifacts.
5. Run verifier checks before summarizing.
6. Produce natural-language explanations only from structured outputs.
7. If a required SDK capability does not exist, report the limitation instead of simulating it.

## VFS artifact guidance

Artifacts should be named and typed:

- Model profiles.
- Validation reports.
- Grade-tonnage curves.
- Aggregation tables.
- Scenario definitions.
- Scenario evaluations.
- Comparison reports.
- Decision logs.

## Gotchas

- Do not put LangGraph/LangChain dependencies in `mine-sdk` or `python/miners`.
- Do not let tool schemas drift from SDK behavior.
- Do not make validation optional in workflows where invalid inputs could invalidate results.
- Do not summarize unsupported claims.
