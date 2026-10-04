---
name: coval-resources
description: Comprehensive overview of ALL Coval platform resources, their hierarchy, relationships, API endpoints, and ID formats. Use when user asks about Coval resources, data model, how things relate, what endpoints exist, or needs context about the platform structure before making API calls.
argument-hint: "[resource-name]"
---

# Coval Platform Resource Overview

Reference for `$ARGUMENTS`. Use this to understand Coval's resource model before making API calls or exploring data.

## Resource Hierarchy

All resources are scoped to your organization (determined by your API key).

```
Agent (22-char ID)
└── Mutation (26-char ID)
Test Set (8-char ID)
└── Test Case (22-char ID)
Persona (22-char ID)
Metric (22-char ID)
Run (22-char ID)
└── Simulation (22-char ID)
    └── Metric Output (26-char ID)
Run Template (22-char ID)
└── Scheduled Run (22-char ID)
```

## Resources

### Agent
An AI system being evaluated. Represents the customer's agent configuration.
- **ID format**: 22-char string
- **Key fields**: `customer_agent_id` (unique per org), `display_name`, `model_type`, `phone_number`, `endpoint`, `metadata`, `prompt`, `language`, `test_set_ids`, `metric_ids`, `attributes`
- **Model types**: `MODEL_TYPE_VOICE`, `MODEL_TYPE_OUTBOUND_VOICE`, `MODEL_TYPE_CHAT`, `MODEL_TYPE_WEBSOCKET`, `MODEL_TYPE_API`, `MODEL_TYPE_ENDPOINT`
- **Connection types**: Inbound voice, outbound voice, OpenAI endpoint, Pipecat, LiveKit, WebSocket
- **API**: `GET/POST /v1/agents`, `GET/PATCH/DELETE /v1/agents/{agent_id}`
- **CLI**: `coval agents list|get|create|update`

### Mutation
A named configuration variant of an agent for A/B testing. Config overrides are deep-merged with the base agent's metadata at runtime.
- **ID format**: 26-char string
- **Key fields**: `display_name`, `description`, `config_overrides` (deep-merged JSON), `parameter_values` (flattened for display), `status` (ACTIVE/DELETED)
- **Relationship**: Belongs to an Agent via `agent_id`
- **Unique constraint**: One active mutation per `(agent_id, display_name)`
- **API**: `GET/POST /v1/agents/{agent_id}/mutations`, `GET/PATCH/DELETE /v1/agents/{agent_id}/mutations/{mutation_id}`
- **CLI**: `coval mutations list|get`

### Test Set
A collection of test cases that define WHAT to test (scenarios, expected behaviors).
- **ID format**: 8-char string
- **Key fields**: `display_name`, `slug`, `description`, `test_set_type`, `parameters` (JSON template variables)
- **Test set types**: DEFAULT, SCENARIO, TRANSCRIPT, AUDIO, IVR, SCRIPT
- **API**: `GET/POST /v1/test-sets`, `GET/PATCH/DELETE /v1/test-sets/{test_set_id}`
- **CLI**: `coval test-sets list|get|create|update`

### Test Case
An individual test scenario within a test set.
- **ID format**: 22-char string
- **Key fields**: `input_str` (the scenario/prompt), `input_type`, `expected_behaviors` (array of strings), `expected_output_json`, `description`, `simulation_metadata_input`
- **Input types**: `SCENARIO` (natural language task), `TRANSCRIPT` (OpenAI format conversation), `AUDIO` (pre-recorded file), `SCRIPT` (ordered lines), `IVR`, `MANUAL`
- **Relationship**: Belongs to a Test Set
- **API**: `GET/POST /v1/test-cases`, `GET/PATCH/DELETE /v1/test-cases/{test_case_id}`
- **CLI**: `coval test-cases list|get|create|update`

### Persona
Defines HOW the simulated user behaves during testing (voice, personality, interruption style).
- **ID format**: 22-char string
- **Key fields**: `display_name`, `simulated_user_prompt`, `voice_name`, `language_code`, `avatar_url`, `metadata`
- **Persona controls**: Voice selection, background noise, interruption rate (NONE/LOW/MEDIUM/HIGH), silent mode, caller phone number
- **Relationship**: Referenced by Runs and Run Templates
- **API**: `GET/POST /v1/personas`, `GET/PATCH/DELETE /v1/personas/{persona_id}`
- **CLI**: `coval personas list|get|create|update`

### Metric
Definition of an evaluation criterion and how to score it.
- **ID format**: 22-char string
- **Key fields**: `metric_name` (globally unique slug), `display_name`, `description`, `metric_metadata` (JSON config), `output_type`, `category`
- **Output types**: FLOAT, STRING, SET, BOOLEAN
- **Features**: Built-in metrics, custom LLM-based prompting, metric chaining, human review integration, expected-behavior evaluation
- **API**: `GET/POST /v1/metrics`, `GET/PATCH/DELETE /v1/metrics/{metric_id}`
- **CLI**: `coval metrics list|get|create|update`

### Run
Top-level execution entity. Launches simulations of test cases against an agent.
- **ID format**: 22-char string
- **Key fields**: `agent_id`, `persona_id`, `test_set_id`, `display_name`, `status`, `config` (JSON), `is_monitoring`, `tags`, `customer_metadata`, `scheduled_run_id`
- **Statuses**: PENDING, IN QUEUE, IN PROGRESS, COMPLETED, FAILED, CANCELLED, DELETED
- **Run types**: Simulation run (`is_monitoring=false`) vs monitoring/conversation run (`is_monitoring=true`)
- **Config options**: `iteration_count` (1-50), `concurrency` (1-100), `sub_sample_size`, `mutation_ids`
- **Total simulations** = test_cases x iterations x (1 + mutation_count)
- **API**: `GET/POST /v1/runs`, `GET/DELETE /v1/runs/{run_id}`
- **CLI**: `coval runs list|get|launch|watch|delete`

### Simulation
Result of running a single test case against an agent (one per test_case x iteration x variant).
- **ID format**: 22-char string
- **Key fields**: `run_id`, `test_case_id`, `iteration`, `mutation_id`, `mutation_name`, `transcript`, `status`, `audio_length_seconds`, `external_conversation_id`, `tool_calls`
- **Mutation tracking**: `mutation_id` and `mutation_name` identify which Mutation variant was used. Both are `null` for base agent simulations (no mutation).
- **API**: `GET /v1/simulations`, `GET/DELETE /v1/simulations/{simulation_id}`, `GET /v1/simulations/{simulation_id}/audio`
- **CLI**: `coval simulations list|get|audio|delete`
- **Filtering**: Supports `mutation_id`, `mutation_name`, `agent_id`, `run_id`, `status`, `test_case_id`, `external_conversation_id`, `create_time`

### Metric Output
Result of evaluating a single simulation with a specific metric.
- **ID format**: 26-char string
- **Key fields**: `metric_output_id`, `metric_id`, `value` (float, string, or array), `status`
- **Relationship**: Child of Simulation, references a Metric
- **API**: `GET /v1/simulations/{simulation_id}/metrics`, `GET /v1/simulations/{simulation_id}/metrics/{metric_output_id}`

### Run Template
Reusable, saved run configuration for scheduling.
- **ID format**: 22-char string
- **Key fields**: `display_name`, `agent_id`, `persona_id`, `test_set_id`, `metric_ids`, `mutation_ids`, `run_config` (JSON source of truth)
- **Soft deletion**: status=ACTIVE or DELETED
- **API**: `GET/POST /v1/run_templates`, `GET/PATCH/DELETE /v1/run_templates/{id}`

### Scheduled Run
Cron/rate-based schedule that triggers runs from a template.
- **ID format**: 22-char string
- **Key fields**: `template_id`, `schedule_expression` (cron or rate), `timezone`, `enabled`
- **Examples**: `rate(15 minutes)`, `cron(0 2 * * ? *)`
- **API**: `GET/POST /v1/scheduled_runs`, `GET/PATCH/DELETE /v1/scheduled_runs/{id}`

## ID Formats Quick Reference

| Resource | Length | Example |
|----------|--------|---------|
| Agent | 22 | `camudk3VhC3kmuvutXKLvF` |
| Mutation | 26 | `01KJ6N707FD9YEPKBSGX1KCW5V` |
| Test Set | 8 | `a1275ab2` |
| Test Case | 22 | `ac67b2c8916f41b6974084` |
| Persona | 22 | `nKexF9ZUt19tLtb3ZQsqzG` |
| Metric | 22 | `hUWu3PxY6G7fTYbLzBAwZm` |
| Run | 22 | `KNNxeP6Vfxx83K4TncVPLH` |
| Simulation | 22 | `LKuChNCLArtF8MLhBix5xY` |
| Metric Output | 26 | `01JCQR8Z9PQSTNVWXY123456` |
| Run Template | 22 | `abc123xyz789def456ghi0` |
| Scheduled Run | 22 | `xyz789abc123def456ghi0` |

## Common Workflows

### Launch an evaluation
1. Identify Agent, Test Set, Persona (list with CLI or API)
2. `POST /v1/runs` with `agent_id`, `test_set_id`, `persona_id`, optional `mutation_ids`
3. Poll `GET /v1/runs/{run_id}` or use `coval runs watch {run_id}`
4. Results: `GET /v1/simulations?filter=run_id="{run_id}"` then fetch metrics per simulation

### Compare mutations (A/B test)
1. Create mutations: `POST /v1/agents/{agent_id}/mutations` with `config_overrides`
2. Launch run with `mutation_ids` array
3. List simulations: `GET /v1/simulations?filter=run_id="{run_id}"`
4. Group by `mutation_id` (null = base agent)
5. Look up mutation names: `GET /v1/agents/{agent_id}/mutations`
6. Compare metrics across groups

### Schedule recurring evaluations
1. Create Run Template with agent, persona, test set, metrics, mutations
2. Create Scheduled Run referencing the template with a cron/rate expression
3. Runs auto-launch and reference back via `scheduled_run_id`

### Submit live conversations (monitoring)
1. `POST /v1/conversations:submit` with conversation data
2. Creates a Run with `is_monitoring=true` and single Simulation
3. Metrics evaluated in real-time

## API Conventions

- **Base URL**: `https://api.coval.dev/v1`
- **Auth**: `X-API-Key` header
- **Pagination**: `page_size` (1-1000, default 50), `page_token`, response includes `next_page_token`
- **Filtering**: AIP-160 syntax — `filter=status="COMPLETED" AND agent_id="abc123"`
- **Sorting**: `order_by=-create_time` (prefix `-` for descending)

## Tools & References

- **OpenAPI Spec**: `GET https://api.coval.dev/v1/openapi` — always fetch the latest spec before building integrations
- **CLI**: https://github.com/coval-ai/cli — install with `brew install coval-ai/tap/coval`
- **MCP Server**: https://github.com/coval-ai/mcp-server — Model Context Protocol server for LLM tool access
- **Docs**: https://docs.coval.dev
