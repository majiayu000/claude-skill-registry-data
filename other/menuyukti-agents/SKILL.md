---
name: menuyukti-agents
description: >-
  LangGraph agents app (apps/agents): FastAPI, milestone run (preset subgraphs + eval),
  streaming chat ReAct, graphql_post. Use when adding preset graphs, routers, or agents-side GraphQL clients.
---

# Menuyukti: `apps/agents`

Python **FastAPI** service: LangChain / LangGraph and streaming chat. **`POST /milestones/{id}/run`** runs: fetch milestone context → **dedicated preset subgraph** (by `milestone.data.presetId`) → shared **eval** graph. Agents call **GraphQL over HTTP** only.

For monorepo boundaries and pnpm vs uv, see [`menuyukti-repo-orientation`](../menuyukti-repo-orientation/SKILL.md).

## Companion skills

When implementing in **`apps/agents`**, follow these skills in addition to this doc and [`.cursor/rules/langgraph.mdc`](../../../.cursor/rules/langgraph.mdc) / [`.cursor/rules/langchain.mdc`](../../../.cursor/rules/langchain.mdc):

- [`langgraph-fundamentals`](../langgraph-fundamentals/SKILL.md) — LangGraph: graphs, state, nodes, streaming, Command, Send.
- [`langchain-fundamentals`](../langchain-fundamentals/SKILL.md) — LangChain agents, tools, middleware.
- [`python-design-patterns`](../python-design-patterns/SKILL.md) — Structure, layering, composition.

## Layout

| Area           | Path                                                                                            | Role                                                                                                                                           |
| -------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Milestone run  | [`apps/agents/agents/core/milestone_run/`](../../../apps/agents/agents/core/milestone_run/)     | Outer graph, [`presets/registry.py`](../../../apps/agents/agents/core/milestone_run/presets/registry.py), per-preset subgraphs, SSE streaming. |
| Milestone eval | [`apps/agents/agents/core/milestone_eval/`](../../../apps/agents/agents/core/milestone_eval/)   | Criterion `Send` fan-out + synthesis; invoked from `finalize_eval` only.                                                                       |
| Milestone data | [`apps/agents/agents/core/milestone_data/`](../../../apps/agents/agents/core/milestone_data/)   | GraphQL upsert for milestonedata JSON.                                                                                                         |
| LLM helpers    | [`apps/agents/agents/core/llm_invoke.py`](../../../apps/agents/agents/core/llm_invoke.py)       | Retries + structured-output errors for preset/eval nodes.                                                                                      |
| Chat           | [`apps/agents/agents/core/chat/`](../../../apps/agents/agents/core/chat/)                       | `create_react_agent` + checkpointer; `CHAT_RECURSION_LIMIT`.                                                                                   |
| Format MD      | [`apps/agents/agents/core/format_markdown/`](../../../apps/agents/agents/core/format_markdown/) | Preset-driven Markdown cleanup (`POST /format-markdown`).                                                                                      |
| Routers        | [`apps/agents/routers/`](../../../apps/agents/routers/)                                         | FastAPI routes (`chat`, `milestone_run`, `format-markdown`, …).                                                                                |
| GraphQL helper | [`apps/agents/agents/graphql_base.py`](../../../apps/agents/agents/graphql_base.py)             | `graphql_post` (with retry on transient failures).                                                                                             |
| Tests          | [`apps/agents/tests/core/`](../../../apps/agents/tests/core/)                                   | Pytest for graphs, eval fan-in, stream adapter.                                                                                                |

Commands and ports: [AGENTS.md](../../../AGENTS.md).

## Registered milestone presets

These **`presetId`** values must stay aligned with web `MILESTONE_PRESET_IDS` and `register_preset_runner` in [`graph.py`](../../../apps/agents/agents/core/milestone_run/graph.py):

| `presetId`                  | Subgraph module         |
| --------------------------- | ----------------------- |
| `dates`                     | `dates/`                |
| `restaurant_campaign_brief` | `campaign_brief/`       |
| `promotion_candidates`      | `promotion_candidates/` |
| `menu_tagger`               | `menu_tagger/`          |
| `menu_clusterer`            | `menu_clusterer/`       |
| `culture_hooks`             | `culture_hooks/`        |
| `ig_profile`                | `ig_profile/`           |
| `ig_plan`                   | `ig_plan/`              |
| `ig_menu_picker`            | `ig_menu_picker/`       |
| `ig_format`                 | `ig_format/`            |
| `ig_text`                   | `ig_text/`              |
| `scheduler`                 | `scheduler/`            |

## Adding a preset

1. Create `milestone_run/<preset_id>/` with `graph.py`, `nodes.py`, `state.py`, `prompts.py` (and tests under `tests/core/test_<preset>_graph.py`).
2. Register `build_<preset>_graph` runner in [`graph.py`](../../../apps/agents/agents/core/milestone_run/graph.py) via `register_preset_runner(preset_id, _run_<preset>)`.
3. Add eval helpers in `milestone_eval/<preset>_eval.py` if deterministic criterion checks apply.
4. Extend [`output_schema.py`](../../../apps/agents/agents/core/milestone_run/output_schema.py) for `validate_skill_output`.
5. Use [`structured_ainvoke_from_run_config`](../../../apps/agents/agents/core/milestone_run/llm_from_run_config.py) for LLM structured output (retries built in).
6. **Web** — add to `MILESTONE_PRESET_IDS`, [`preset-definitions.ts`](../../../apps/web/lib/milestones/preset-definitions.ts), and preview / timeline UI components.

Legacy [`make_milestone_run_tools`](../../../apps/agents/agents/core/milestone_run/tools/__init__.py) remains for unit tests only; production runs do not use ReAct tool loops.

## Tracing and run persistence

- **LangSmith:** `LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, optional `LANGCHAIN_PROJECT`; run metadata includes `milestone_id`, `workflow_id`, `run_id`.
- **Product DB:** `startMilestoneAgentRun` / `completeMilestoneAgentRun` on GraphQL (`milestone_agent_run` table).
- **Distributed traces:** web BFF forwards `traceparent` to agents when present.

See [`apps/agents/README.md`](../../../apps/agents/README.md) for env vars.

## Checklist (agents-only)

1. **`graphql_post`** — env and headers in [`graphql_base.py`](../../../apps/agents/agents/graphql_base.py).
2. **New preset** — subgraph module + `register_preset_runner` + GraphQL client helpers if needed.
3. **Persistence** — preset `persist_result` → `milestone_data` upsert / `validate_skill_output`.
4. **Tests** — graph smoke tests + eval fan-in when touching [`milestone_eval/graph.py`](../../../apps/agents/agents/core/milestone_eval/graph.py).

## Related

| Topic             | Skill                                                                  |
| ----------------- | ---------------------------------------------------------------------- |
| GraphQL schema    | [`menuyukti-graphql`](../menuyukti-graphql/SKILL.md)                   |
| Web UI            | [`menuyukti-web`](../menuyukti-web/SKILL.md)                           |
| Analytics package | [`menuyukti-analytics`](../menuyukti-analytics/SKILL.md)               |
| Monorepo map      | [`menuyukti-repo-orientation`](../menuyukti-repo-orientation/SKILL.md) |

## Canonical docs

- [`AGENTS.md`](../../../AGENTS.md)
- [`apps/agents/README.md`](../../../apps/agents/README.md)
