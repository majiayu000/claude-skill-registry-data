---
name: 00b-agent-spec-and-tool-plan
description: >
  Use when deriving a Databricks Agent Spec and Agent Tool Plan from
  docs/design_prd.md before building Track A agents. Covers web-researched MCP
  recommendations, Databricks managed MCP choices, dynamic SQL MCP catalog/schema
  inputs, optional Knowledge Assistant selection, and validation of
  docs/agent_spec.yaml plus docs/agent_tool_plan.yaml.
license: Apache-2.0
metadata:
  last_verified: "2026-06-05"
  upstream_sources: []
  volatility: high
  author: "prashanth-subrahmanyam"
  version: "1.0.0"
  domain: "genai-agents"
  pipeline_position: "F0b"
  consumes: "docs/design_prd.md"
  produces: "docs/agent_spec.yaml, docs/agent_tool_plan.yaml"
fields_read:
  - agent.system_prompt
  - agent.capabilities
  - agent.model
  - agent.must_do
  - agent.must_not_do
  - agent.benchmark_seeds.coverage_buckets
  - agent.benchmark_seeds.seed_examples
  - agent.tools
  - agent.mcp_servers
  - agent.knowledge_base_backend
  - agent.external_integrations
  - governance.scorer_suite.guidelines
  - governance.scorer_suite.custom_scorer_rules
  - governance.scorer_suite.judge_questions
  - governance.verification.smoke_test_cases
  - governance.llm_role_endpoints.llm_judge_default.endpoint
  - selected_tools
  - selected_mcp_servers
  - runtime_guardrails.tool_shaped_scorers
  - verification.tool_smoke_tests
---

# Agent Spec And Tool Plan

## Purpose

This skill bridges the AppKit/Lakebase application design phase and the Track A
agent build phase. It turns `docs/design_prd.md` into a concrete
`docs/agent_spec.yaml`, then turns the spec plus user tool choices into
`docs/agent_tool_plan.yaml`.

The skill does not create Databricks resources, install MCP connections, wire
agent code, or deploy apps. It produces planning artifacts that later prompts
consume.

## When To Use

Use this skill for:

- Creating an Agent Spec after `docs/design_prd.md` exists.
- Asking the IDE to web search for MCPs relevant to the use case.
- Selecting Databricks managed MCPs: Genie, Vector Search, SQL, UC Functions.
- Selecting external MCP candidates through managed OAuth, Marketplace, custom
  HTTP connections, or Dynamic Client Registration.
- Adding a no-prerequisite SQL MCP path over existing Unity Catalog tables by
  providing `agent_sql_catalog`, `agent_sql_schema`, and warehouse ID.
- Deciding whether a Knowledge Assistant should be created.

## Inputs

| Input | Required | Description |
|---|---|---|
| `prd_path` | yes | Usually `docs/design_prd.md`. |
| `agent_spec_path` | yes | Usually `docs/agent_spec.yaml`. |
| `agent_tool_plan_path` | yes | Usually `docs/agent_tool_plan.yaml`. |
| `agent_spec_ref` | no | Path to existing Agent Spec for downstream skills that consume it (alias of `agent_spec_path`). |
| `agent_tool_plan_ref` | no | Path to existing Tool Plan for downstream skills that consume it (alias of `agent_tool_plan_path`). |
| `agent_model` | no | Databricks serving endpoint used by the agent LLM. Defaults to `databricks-claude-sonnet-4-6`. |
| `agent_sql_catalog` | no | Catalog the SQL MCP may query. |
| `agent_sql_schema` | no | Schema the SQL MCP may query. |
| `agent_sql_warehouse_id` | no | Warehouse for SQL MCP `_meta.warehouse_id`. |
| `agent_sql_table_allowlist` | no | Tables allowed for SQL MCP; empty means schema-scope with read-only guardrails. |
| `mcp_research_mode` | no | `none`, `managed_only`, or `web_research`. |

## Agent Spec Contract

`docs/agent_spec.yaml` must follow `references/agent-spec-schema.md`.

Required top-level keys:

- `schema_version`
- `source_prd`
- `agent` (includes `must_do[]`, `must_not_do[]`, `benchmark_seeds.coverage_buckets[]`, `benchmark_seeds.seed_examples[]`)
- `tool_recommendations`
- `mcp_research`
- `knowledge_assistant`
- `governance` (includes `scorer_suite.{guidelines, custom_scorer_rules, judge_questions}`, `verification.smoke_test_cases[]`, `llm_role_endpoints.llm_judge_default.endpoint`)

The spec may recommend tools, but it must not mark every recommendation as
selected. Final selection belongs in `docs/agent_tool_plan.yaml`.

## Tool Plan Contract

`docs/agent_tool_plan.yaml` must follow `references/tool-plan-schema.md`.

Required top-level keys:

- `schema_version`
- `source_agent_spec`
- `runtime_config` (includes `llm.{provider, endpoint, api_base_url, api_mode, model_config}`)
- `selected_tools`
- `selected_mcp_servers`
- `knowledge_assistant`
- `resource_grants`
- `runtime_guardrails` (includes `tool_shaped_scorers[]` derived mechanically from `selected_tools[]`)
- `verification` (includes `tool_smoke_tests[]` — one entry per `selected_tools[]` entry)

## Eval Authoring Rule

Eval/governance content is **layered across three places**, and each place has a strict tool-awareness contract.

| Layer | Where | Tool-aware? | What lives here |
|---|---|---|---|
| Spec (generic) | `docs/agent_spec.yaml` | **No** — tools are not yet selected | `agent.must_do[]`, `agent.must_not_do[]`, `agent.benchmark_seeds.{coverage_buckets, seed_examples}`, `governance.scorer_suite.{guidelines, custom_scorer_rules, judge_questions}`, `governance.verification.smoke_test_cases[]`, `governance.llm_role_endpoints.llm_judge_default.endpoint` |
| Plan (tool-shaped) | `docs/agent_tool_plan.yaml` | **Yes** — derived mechanically from `selected_tools[]` | `verification.tool_smoke_tests[]` (one per selected tool, use-case-shaped prompt + observable signal); `runtime_guardrails.tool_shaped_scorers[]` (e.g. `ka_citation_present`, `RetrievalGroundedness`, `genie_sql_correctness`, `sql_readonly_compliance`) |
| Consumer (union) | sections 46/50/51/52 | Reads BOTH | Smoke set = Spec ∪ Plan; benchmark rows = Spec base ∪ Plan tool-shaped append; scorer suite = Spec generic ∪ Plan tool-shaped (deduped); failure-shape `tool_call_empty` only fires for tools in `selected_tools[]` |

**Authoring rules:**

1. **Section 38 (Spec)** never authors tool-shaped fields. No `ka_citation_present`, no `RetrievalGroundedness`, no `genie_*`, no `sql_*` scorer hints. No assertions like "use Genie to look up X" in seed_examples. Tools are not selected at this step.
2. **Section 39 (Plan)** mechanically derives the tool-shaped fields from `selected_tools[]` using the table in `references/tool-plan-schema.md` § *Tool-shaped Derivation Rules*. Tool families absent from `selected_tools[]` contribute zero entries.
3. **Sections 46/50/51/52 (Consumers)** read both files and union them. KA absent in the Plan ⇒ no KA scorer registered, no KA smoke test, no KA dataset row, no KA failure-shape branch.

**Validation at exit (section 39):**

- `verification.tool_smoke_tests[]` length equals `selected_tools[]` length.
- Every `runtime_guardrails.tool_shaped_scorers[]` entry maps to a tool family present in `selected_tools[]`.
- No `tool_shaped_scorers[]` entry exists for a tool family that is `selected: false` or absent.

## Runtime Model Route Rule

`docs/agent_spec.yaml` must include the backing Databricks model serving endpoint at:

```yaml
agent:
  model: "databricks-claude-sonnet-4-6"
```

`docs/agent_tool_plan.yaml` must convert that backing model into the runtime route:

```yaml
runtime_config:
  llm:
    provider: "databricks"
    endpoint: "docs/agent_spec.yaml.agent.model"
    api_base_url: null
    api_mode: "databricks_openai_compatible"
    model_config:
      endpoint_key: "llm_endpoint"
      api_base_url_key: "llm_api_base_url"
      api_mode_key: "llm_api_mode"
```

Rules:

1. Treat `agent.model` as a raw/backing Databricks serving endpoint name.
2. If the user supplies `agent_model`, copy it exactly into `agent.model`.
3. If the user does not supply `agent_model`, set `agent.model` to `databricks-claude-sonnet-4-6`.
4. Do not store vague labels such as `Claude`, `GPT`, `best model`, or `small model`.
5. Do not require AI Gateway in the core flow. Gateway can be introduced later by changing only `runtime_config.llm`.
6. The Track A agent must consume `runtime_config.llm` through `ModelConfig` as `llm_endpoint`, `llm_api_base_url`, and `llm_api_mode`, not by hardcoding any endpoint in Python.

## Dynamic SQL MCP Rule

When SQL MCP is selected, the plan must include:

```yaml
selected_mcp_servers:
  - name: sql_uc_schema_query
    server_type: sql
    url_template: "{workspace_host}/api/2.0/mcp/sql"
    auth: OBO
    meta:
      warehouse_id: "{agent_sql_warehouse_id}"
    scope:
      catalog: "{agent_sql_catalog}"
      schema: "{agent_sql_schema}"
      allowed_tables: []
    readonly: true
```

The matching tool must include guardrails:

```yaml
selected_tools:
  - kind: mcp
    name: sql_uc_schema_query
    mcp_server_ref: sql_uc_schema_query
    readonly: true
    guardrails:
      allowed_statements: ["SELECT", "DESCRIBE", "EXPLAIN"]
      forbidden_statements: ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "MERGE", "TRUNCATE"]
      require_fully_qualified_names: true
      default_catalog: "{agent_sql_catalog}"
      default_schema: "{agent_sql_schema}"
```

## Web Research Rule

If `mcp_research_mode: web_research`, use the official MCP Registry as the
authoritative discovery source before broader web search:

1. Search the public registry UI at `https://registry.modelcontextprotocol.io`.
2. Use the registry REST API documented at `https://modelcontextprotocol.io/registry/registry-aggregators#consuming-the-mcp-registry-rest-api`.
3. Prefer `GET https://registry.modelcontextprotocol.io/v0.1/servers?limit=100`
   for discovery, following `metadata.nextCursor` for additional pages.
4. Use `GET /v0.1/servers/{serverName}/versions` and
   `GET /v0.1/servers/{serverName}/versions/latest` for candidate version
   details. URL-encode `serverName`.
5. Ignore candidates with registry `status: deleted`; mark `deprecated`
   candidates as `confidence: low` unless there is no viable alternative.
6. Use general web search only to enrich registry candidates with vendor docs,
   Databricks compatibility notes, security posture, or examples.

Record findings under `mcp_research.candidates[]` with registry metadata,
source URLs, version/status, integration notes, and confidence. Do not install
or configure any MCP connection during Agent Spec creation.

## Validation

Before exiting either prompt:

1. Parse the YAML.
2. Confirm all required top-level keys exist.
3. Confirm `agent.model` is present and is not `n/a`.
4. Confirm `agent.model` does not contain spaces and does not look like a prose label.
5. Confirm every `selected_tools[].mcp_server_ref` resolves to a
   `selected_mcp_servers[].name`.
6. Confirm SQL MCP is read-only unless the user explicitly selected write access.
7. Confirm KA is either selected with a source strategy or skipped with
   `knowledge_assistant.selected: false`.
