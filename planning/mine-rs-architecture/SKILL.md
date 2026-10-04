---
name: mine-rs-architecture
description: Use this skill when designing or changing mine-rs repository architecture, crate boundaries, package layout, dependency direction, monorepo strategy, SDK layering, or module ownership. Applies to tasks mentioning crates, repos, workspace, architecture, SDK, Python layer, agentic layer, or boundaries.
---

# mine-rs architecture skill

Use this skill when a task affects repository structure, crate boundaries, package boundaries, public APIs or dependency direction.

## Source of truth

Read these files before making architectural changes:

1. `docs/references/repository-strategy.md`
2. `docs/references/architecture.md`
3. `docs/references/roadmap.md`
4. `docs/backlog.md`
5. `AGENTS.md`

## Current decision

Keep `mine-rs` as a monorepo. Do not split into multiple repositories unless the user explicitly asks to reevaluate that decision.

Use internal separation by crate/package:

```text
crates/
├─ mine-core/
├─ mine-blockmodel/
├─ mine-indexing/
├─ mine-validation/
├─ mine-reblock/
├─ mine-io/
├─ mine-economics/
├─ mine-planning/
├─ mine-sdk/
├─ mine-tools/
├─ mine-python/
└─ mine-cli/

python/
├─ miners/
└─ mine-agents/
```

## Dependency direction

Maintain this direction:

```text
mine-core
↓
domain crates
↓
mine-sdk
↓
mine-tools
↓
mine-python / mine-cli / python/mine-agents
```

Rules:

- `mine-core` must not depend on Python, agents, CLI or LLM runtimes.
- `mine-sdk` must not depend on `mine-python` or `python/mine-agents`.
- `mine-tools` may depend on `mine-sdk`, but `mine-sdk` must not depend on agentic tools.
- `mine-python` maps Rust types/errors into Python; it must not own core mining logic.
- `python/mine-agents` consumes `miners` and tool contracts; it must not define mining calculations.

## Procedure

1. Identify which layer owns the requested behavior.
2. Check whether an existing crate/package boundary already covers it.
3. Prefer adding code to the lowest correct deterministic layer.
4. Expose through `mine-sdk` if it is part of the public Rust API.
5. Expose through `mine-python`/`python/miners` only after Rust ownership is clear.
6. Expose through `mine-tools` if the operation needs structured tool input/output.
7. Keep agentic orchestration outside SDK logic.
8. Update docs when changing a boundary or dependency rule.

## Gotchas

- Do not create a new crate just because a concept has a name. Create one when it has a stable boundary, dependencies and tests.
- Do not place LangGraph/LangChain or LLM dependencies in Rust core or Python SDK.
- Do not make examples imply APIs are implemented unless they are.
- Do not split repos early; versioned contracts are still evolving.
