---
name: 04-ai-gateway
description: >
  Use when you need central governance, observability, guardrails, or rate
  limits across LLM endpoints and MCP servers used by agents. Covers creating
  and configuring Databricks AI Gateway endpoints, enabling usage tracking,
  inference tables (UC Delta audit), rate limits, and guardrails, plus how
  deployed agent serving endpoints and Apps consume a gateway URL. Foundation
  Step 4 — ideal as a governance layer BEFORE Module 7 production deployment.
  Complements in-code guardrails and MLflow tracing; does NOT replace MLflow
  trace tables but adds a provider-level audit trail.
license: Apache-2.0
compatibility: "Requires Databricks AI Gateway (public preview in most AWS/Azure regions as of 2026-04). Requires workspace Unity Catalog and SQL Warehouse for inference tables."
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: bundle_deploy
deploy_note: "AI Gateway endpoint + inference/usage tables created via the Databricks SDK/REST (or CLI through runDatabricksCli on Genie Code); inference tables land in the per-user prefixed schema. Not modeled as a DAB resource kind in this workshop. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "1.1.0"
  domain: "genai-agents"
  pipeline_position: "F4"
  consumes: "llm_endpoints, mcp_endpoints, uc_catalog_schema, endpoint_guardrail_audit, llm_role_endpoints"
  produces: "ai_gateway_endpoint, inference_tables, usage_tracking_tables, rate_limits, inference_table_prefix"
  grounded_in: "https://docs.databricks.com/aws/en/ai-gateway/, https://docs.databricks.com/aws/en/ai-gateway/configure-ai-gateway-endpoints, https://docs.databricks.com/aws/en/ai-gateway/inference-tables, https://docs.databricks.com/aws/en/ai-gateway/usage-tracking"
---

# AI Gateway (Central Governance for LLM + MCP Endpoints)

Databricks AI Gateway is the central control plane between your agents (Apps, notebooks, serving endpoints) and LLM / MCP providers. It gives you a single URL to hit from agent code, and behind that URL you get:

- **Usage tracking** — per-user, per-token, per-endpoint counts in a UC table.
- **Inference tables** — full request/response Delta logs for audit.
- **Guardrails** — content safety, PII detection, topic restrictions.
- **Rate limits** — per-user / per-endpoint QPS ceilings.
- **Fallbacks** — route to a second provider on primary failure.

Think of it as the network-level governance layer; MLflow traces + UC OTEL tables are the application-level observability layer. Run both.

---

## When to Add AI Gateway

Add AI Gateway when **any** of these are true for your agent:

- Multiple teams or apps share LLM endpoints and you need chargeback.
- Compliance / security requires a durable audit trail of model I/O.
- You want rate-limit protection against runaway or abusive callers.
- You need uniform guardrails (PII, safety) applied regardless of which agent is calling.
- You want **provider fallback** (e.g. route to a secondary model if primary fails).

If the agent is a solo prototype used by its author, MLflow tracing alone is fine — skip this skill until you have ≥ 2 consumers.

---

## Architecture

```
┌────────────┐        ┌──────────────────────────────┐        ┌──────────────┐
│ Agent App  │───▶────│ Databricks AI Gateway        │───▶────│ LLM / MCP    │
│ (Module 5) │        │  - usage tracking             │        │ Provider     │
│ Serving    │        │  - inference tables (UC Δ)    │        │ (Foundation, │
│ endpoint   │        │  - guardrails / rate limits   │        │  3P, MCP)    │
│ (Module 7) │        │  - fallbacks                  │        └──────────────┘
└────────────┘        └──────────────────────────────┘
      │                           │
      ▼                           ▼
 MLflow traces           UC inference_tables
 (OTEL, app-level)       (provider audit, I/O)
```

Agents talk to a gateway URL instead of the raw model URL. The gateway transparently proxies OpenAI-compatible and Anthropic-compatible APIs, so existing client code (OpenAI SDK, Anthropic SDK, `openai.Agent`) keeps working by changing only the base URL.

---

## Consuming the endpoint audit

AI Gateway is **downstream** of the role-based endpoint binding in
`vibecoding-state` (Phase 1.2). Before creating any gateway endpoint,
F4 reads `state://endpoint_guardrail_audit` (populated by
`vibecoding-state.endpoint_guardrail_audit`) and the bound `endpoint`
under each `state://llm_role_endpoints.<role>`. The gateway's
`served_entities[].entity_name` MUST equal a candidate that has already
**passed** its role probe — never a name picked by hand.

```python
import yaml

state = yaml.safe_load(open("state.yaml"))
audit  = state["endpoint_guardrail_audit"]
roles  = state["llm_role_endpoints"]

primary = roles["agent_chat"]["endpoint"]
assert audit[primary]["streaming_ok"] is True, (
    f"AI Gateway refusing to bind {primary} as agent_chat primary: "
    "endpoint_guardrail_audit reports streaming_ok != true. "
    "Re-run vibecoding-state.endpoint_guardrail_audit; if no candidate "
    "passes, halt and ask the operator for a workspace-specific FMAPI "
    "candidate list (this workshop has no admin-ticket path)."
)
```

### Halt rule: no admin-ticket fallback

If `endpoint_guardrail_audit` does not have a passing candidate for a
role this gateway needs to serve, **halt** the F4 step and surface an
explicit prompt to the operator:

> No FMAPI endpoint passed the role probe for `<role>`. Provide a
> workspace-specific candidate list (workspace name + endpoint names)
> so `vibecoding-state.llm_role_endpoint_probe` can re-bind. The
> workshop deliberately has **no admin-ticket pathway** — gateway
> creation does not silently downgrade or pick "any healthy" endpoint.

Do **not** create an admin ticket, do **not** fall back to a hard-coded
default, and do **not** create the gateway with an unaudited
`served_entity`. The halt is the contract.

### Inference-table prefix and grants are F2 territory

The gateway's `inference_table_config.table_name_prefix` is a
**provider-level** prefix (e.g. `gw`, no trailing underscore — Databricks
appends the per-named-stream suffix). It is not the same as
`state://otel_table_prefix` (which is owned by
[F2](../02-experiment-tracing-and-uc-storage/SKILL.md)). Capture it
under `state://Foundation.f4_gateway.inference_table_prefix` and grant
the same `MODIFY, SELECT` privileges to the agent SP using the F2
pattern (explicit grants, not `ALL_PRIVILEGES`).

> **Validator: `gw`, not `gw_`.** The same trailing-underscore failure
> mode that bites OTel `table_prefix=` also bites the gateway
> `table_name_prefix`. Validate that the captured value does **not** end
> in `_`; the platform appends `_<name>_payload` itself, so a value of
> `gw_` produces `gw__<name>_payload` (double underscore) and breaks
> downstream queries.

---

## Creating an AI Gateway Endpoint (CLI)

Use the Databricks CLI to create a gateway in front of an existing serving endpoint:

```bash
databricks serving-endpoints create \
  --json '{
    "name": "skyloyalty-ai-gateway",
    "ai_gateway": {
      "usage_tracking_config": {"enabled": true},
      "inference_table_config": {
        "enabled": true,
        "catalog_name": "main",
        "schema_name": "skyloyalty_ops",
        "table_name_prefix": "gw"
      },
      "rate_limits": [
        {"key": "endpoint", "renewal_period": "minute", "calls": 120}
      ],
      "guardrails": {
        "input": {"pii": {"behavior": "BLOCK"}, "safety": true},
        "output": {"pii": {"behavior": "BLOCK"}, "safety": true}
      }
    },
    "config": {
      "served_entities": [{
        "name": "claude-sonnet-46",
        "entity_name": "databricks-claude-sonnet-4-6",
        "entity_version": "1",
        "workload_size": "Small",
        "scale_to_zero_enabled": true
      }]
    }
  }'
```

After creation, the gateway is reachable at:

```
https://<workspace-host>/serving-endpoints/skyloyalty-ai-gateway/invocations
```

or via OpenAI-compatible base:

```
https://<workspace-host>/serving-endpoints/skyloyalty-ai-gateway/
```

Inference tables land at `main.skyloyalty_ops.gw_<name>_payload` (Delta, UC governed) within ~30 min of first traffic.

---

## Pointing Your Agent at the Gateway

**OpenAI SDK (most common, e.g. OpenAI Agents SDK, LangChain, custom):**

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://<workspace-host>/serving-endpoints/skyloyalty-ai-gateway/",
    api_key=os.environ["DATABRICKS_TOKEN"],
)

response = client.chat.completions.create(
    model="claude-sonnet-46",  # served_entity name from the gateway config
    messages=[...],
)
```

**Model serving client (Databricks SDK):**

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
response = w.serving_endpoints.query(
    name="skyloyalty-ai-gateway",
    messages=[...],
)
```

**MLflow tracing continues to work** — the gateway is transparent. Your `@mlflow.trace` decorators and OTEL spans capture the application-level view; inference tables capture the provider-level view. Both are valuable.

---

## Inference Tables (UC Delta Audit)

Inference tables log every request/response through the gateway. Schema highlights:

| Column | Meaning |
|--------|---------|
| `databricks_request_id` | Correlates to MLflow traces if you pass it via header |
| `request_time` | UTC timestamp |
| `status_code`, `execution_time_ms` | Provider-level observability |
| `request`, `response` | Full JSON payloads (subject to PII redaction if enabled) |
| `served_entity_id`, `model_id` | Which served model handled it |

Correlate with MLflow traces by setting the `databricks_request_id` header from your agent to the MLflow trace request id:

```python
import mlflow

trace_id = mlflow.get_current_active_span().request_id if mlflow.get_current_active_span() else None
response = client.chat.completions.create(
    model="claude-sonnet-46",
    messages=[...],
    extra_headers={"databricks_request_id": trace_id} if trace_id else None,
)
```

Now `main.skyloyalty_ops.gw_*_payload.databricks_request_id` joins to MLflow's trace `request_id` for end-to-end analysis.

> **Load** [references/inference-tables-queries.md](references/inference-tables-queries.md) **if** you need SQL recipes for daily spend, top users, error rate analysis, or join-to-MLflow patterns.

---

## Usage Tracking

`usage_tracking_config.enabled = true` populates `system.ai_gateway.usage` (or a workspace-scoped UC table, depending on configuration) with per-request token counts, model, and user identity. Use for:

- Weekly chargeback reports per team / app.
- Detecting runaway agents (unexpected spike in tokens per user).
- Capacity planning for PT throughput units.

Sample query:

```sql
SELECT
  request_date,
  served_entity_id,
  COUNT(*) AS requests,
  SUM(input_tokens)  AS prompt_tokens,
  SUM(output_tokens) AS completion_tokens
FROM main.skyloyalty_ops.gw_skyloyalty_ai_gateway_usage
WHERE request_date >= current_date() - INTERVAL 7 DAYS
GROUP BY 1, 2
ORDER BY 1 DESC, requests DESC;
```

---

## Rate Limits

Rate-limit keys:

| Key | Meaning | Use when |
|-----|---------|----------|
| `endpoint` | Single bucket for the whole gateway | Protect the provider from a runaway agent |
| `user` | Per authenticated user | Multi-tenant app; prevent noisy neighbors |

Example: cap all traffic to 120 calls/min globally AND any single user to 20 calls/min:

```json
"rate_limits": [
  {"key": "endpoint", "renewal_period": "minute", "calls": 120},
  {"key": "user",     "renewal_period": "minute", "calls": 20}
]
```

When a limit trips, the gateway returns HTTP 429. Agents should backoff + retry; the MLflow trace will show a `trace.status=ERROR` span with the 429 — use that to feed a production monitoring alert.

---

## Guardrails

| Guardrail | Input side | Output side |
|-----------|-----------|-------------|
| `pii` | Blocks/redacts PII in user prompts | Blocks/redacts PII leaks in model output |
| `safety` | Filters harmful user requests | Filters harmful model responses |
| `invalid_keywords` | Blocks requests containing restricted terms | Same on output |
| `valid_topics` | Optional allowlist of permitted topics | — |

Gateway-level guardrails are **complementary** to in-code guardrails. Use the gateway for org-wide policy (e.g. no PII ever) and in-code guardrails for agent-specific domain rules (e.g. SkyLoyalty never books an award without authorization).

> **Load** [references/guardrails-setup.md](references/guardrails-setup.md) **if** you need full config options, per-endpoint override patterns, or guardrail testing recipes.

---

## Fallbacks (Provider Failover)

Configure multiple `served_entities` so traffic automatically fails over:

```json
"config": {
  "served_entities": [
    {"name": "primary",   "entity_name": "databricks-claude-sonnet-4-6", "traffic_percentage": 100},
    {"name": "secondary", "entity_name": "databricks-claude-opus-4-5",   "traffic_percentage": 0}
  ]
}
```

Set traffic split or leave secondary at 0% until a failover rule triggers. For agent workloads the common pattern is: primary at 100%; secondary as a capacity reserve for 429/5xx.

---

## MCP Servers via AI Gateway

MCP servers registered with the workspace can also be proxied through the gateway. This gives the same audit/rate-limit/guardrail benefits for tool calls. Configure by adding MCP endpoints as `served_entities` with MCP-specific payloads. See [Databricks MCP docs](https://docs.databricks.com/aws/en/ai-gateway/) for the latest payload shape.

> **Load** [references/mcp-via-gateway.md](references/mcp-via-gateway.md) **if** you need the MCP-specific config, including auth-on-behalf-of patterns.

---

## Relation to Other Observability Layers

| Layer | Purpose | Captured in |
|-------|---------|-------------|
| MLflow OTEL traces | App-level view: tool calls, span nesting, retrievals | UC `*_otel_*` tables |
| AI Gateway inference tables | Provider-level view: raw request/response, tokens, latency | UC Delta (per gateway) |
| MLflow production scorers | Quality signal on sampled traces | UC `*_otel_annotations` |
| AI Gateway usage tracking | Cost / chargeback signal | UC `system.ai_gateway.usage` or workspace-scoped |

They do not replace each other. Typical debug path: a user complaint → MLflow trace search → identify bad trace → join `databricks_request_id` to gateway inference table to see raw provider response → triage.

---

## Do's and Don'ts

|  | Do | Don't |
|---|---|---|
| **When** | Add gateway when ≥ 2 consumers, compliance needs, or rate-limit concerns. | Use for solo prototypes. |
| **URLs** | Point all agent code at the gateway URL, not the raw endpoint. | Keep some callers on the raw endpoint — your audit is incomplete. |
| **Inference tables** | Enable and route to a UC schema with clear ownership (team / app scoped). | Let inference tables land in `default` — governance is unclear. |
| **Correlation** | Pass `databricks_request_id` header tied to the MLflow trace. | Rely on approximate timestamps to join. |
| **Rate limits** | Set both `endpoint` and `user` keys; start permissive; tighten. | Set one aggressive limit then debug 429s in prod. |
| **Guardrails** | Run gateway guardrails + in-code guardrails — belt and suspenders. | Rely on a single layer for safety-critical flows. |

---

## Common Mistakes

| Mistake | Why it hurts | What to do instead |
|---------|--------------|-------------------|
| Not enabling inference tables at creation | Rebuilding audit after an incident = impossible | Enable at endpoint creation; they cost little |
| Mixed traffic (some callers direct, some through gateway) | Rate limits and usage tracking are blind to direct traffic | Update every consumer's base URL |
| Gateway guardrails disabled "for perf" | PII leaks discovered post-incident | Enable; profile latency; usually adds < 50 ms |
| No `databricks_request_id` correlation | Post-hoc debugging requires fuzzy timestamp join | Pass trace request id as header |
| Hitting only the gateway in dev, direct in staging/prod | Different code paths = different bugs | Same base URL in all envs; different gateway names per env |

---

## Validation Checklist

- [ ] Gateway endpoint created with `usage_tracking_config.enabled=true` and `inference_table_config.enabled=true`.
- [ ] Every `served_entities[].entity_name` corresponds to a candidate that **passed** its role probe in `state://endpoint_guardrail_audit` — no hand-picked endpoints.
- [ ] If no candidate passed for a required role, F4 halted and asked for a workspace-specific FMAPI candidate list (no admin-ticket fallback was attempted).
- [ ] `inference_table_config.table_name_prefix` does **not** end in an underscore (validator: `gw`, not `gw_`).
- [ ] Inference tables visible in UC within 30 min of first traffic.
- [ ] Agent app / serving endpoint uses the gateway URL as its base URL.
- [ ] `databricks_request_id` header is passed from client code, tied to MLflow trace.
- [ ] At least one rate limit is configured (`endpoint` or `user`).
- [ ] Gateway guardrails enabled for PII + safety, input + output.
- [ ] SQL warehouse access granted on inference / usage tables for the ops team.
- [ ] An SQL alert in [07-production-monitoring](../../sdlc/07-production-monitoring/SKILL.md) fires on elevated 429 / 5xx from the gateway.

---

## References

### Official documentation (Databricks)

- [AI Gateway overview](https://docs.databricks.com/aws/en/ai-gateway/)
- [Configure AI Gateway endpoints](https://docs.databricks.com/aws/en/ai-gateway/configure-ai-gateway-endpoints)
- [Inference tables](https://docs.databricks.com/aws/en/ai-gateway/inference-tables)
- [Usage tracking](https://docs.databricks.com/aws/en/ai-gateway/usage-tracking)

### Local deep-dives

| File | Topic |
|------|-------|
| [references/inference-tables-queries.md](references/inference-tables-queries.md) | SQL recipes: spend, top users, error rate, join-to-MLflow |
| [references/guardrails-setup.md](references/guardrails-setup.md) | Guardrail config, testing, per-endpoint override |
| [references/mcp-via-gateway.md](references/mcp-via-gateway.md) | MCP server routing through gateway, OBO auth |

### Related skills

[02-experiment-tracing-and-uc-storage](../02-experiment-tracing-and-uc-storage/SKILL.md) · [sdlc/06-deployment-and-automation](../../sdlc/06-deployment-and-automation/SKILL.md) · [sdlc/07-production-monitoring](../../sdlc/07-production-monitoring/SKILL.md)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-04-26 | Added "Consuming the endpoint audit" section: F4 reads `state://endpoint_guardrail_audit` and `state://llm_role_endpoints.<role>` before binding any `served_entities[].entity_name`; if no candidate passed the role probe, F4 halts and asks for a workspace-specific FMAPI candidate list (no admin-ticket fallback). Documented `gw`-not-`gw_` table-prefix validator (same trailing-underscore trap as F2 OTel). Updated CLI example to use `"gw"` instead of `"gw_"`. Validation checklist gates audit consumption + halt rule + prefix validator. Closes the rollup "AI Gateway table prefix validator (`gw`, not `gw_`)" row. |
| 1.0.0 | 2026-04-19 | Initial skill: AI Gateway creation, inference tables, usage tracking, rate limits, guardrails, MCP routing. |
