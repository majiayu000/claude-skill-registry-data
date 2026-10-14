---
name: 03-tools-and-mcp
description: >
  Use when wiring tools into an OpenAI Agents SDK agent: local Python function
  tools, DatabricksMCPClient connections, and MCPServerSse for MCP servers.
  Track A Step 3. Builds on shared concepts from F3 (Tools and Data Access).
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Tool + MCP wiring (local function tools, DatabricksMCPClient, MCPServerSse) — code, no bundle resource. Resolves identically on both clients; on Genie Code use its built-in tool surface for ad-hoc calls and runDatabricksCli for grants. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "3.1.0"
  domain: "genai-agents"
  pipeline_position: "A3"
  consumes: "customized_agent, agent_class, mcp_server_knowledge"
  produces: "agent_with_tools, mcp_connections, resource_grants"
  grounded_in: "docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent, docs.databricks.com/aws/en/generative-ai/agent-framework/build-agent-tool, openai.github.io/openai-agents-python/tools/"
fields_read:
  - agent.tools
  - agent.mcp_servers
  - agent.knowledge_base_backend
  - docs.agent_tool_plan.selected_tools
  - docs.agent_tool_plan.selected_mcp_servers
---

# Track A Step 3: Agent SDK Tool Wiring

Wire tools into your OpenAI Agents SDK agent so it can query data, search
documents, call functions, and connect to external services.

This step focuses on **how to wire tools into the Agent class**. For
background on which MCP servers exist, how external MCP works, resource
grants, and retriever schemas, see
[F3: Tools and Data Access](../../../foundation/03-tools-and-data-access/SKILL.md).

## Tool Plan Input Contract

For the Agents Accelerator, prefer `docs/agent_tool_plan.yaml` over inferred
defaults. Wire only the tools listed in `selected_tools[]`.

Tool families not selected are skipped and recorded in verification as skipped,
not failed.

For SQL MCP, enforce the read-only guardrails from the plan before any smoke
test. Reject generated SQL containing `INSERT`, `UPDATE`, `DELETE`, `DROP`,
`ALTER`, `CREATE`, `MERGE`, or `TRUNCATE` when `readonly: true`.

Use `docs/agent_tool_plan.yaml.verification.tool_smoke_tests[]` as the source
of smoke prompts. Every selected tool must produce at least one MLflow TOOL span.

OpenAI Agents SDK SQL MCP wiring example:

```python
from agents.mcp import MCPServerSse

sql_mcp = MCPServerSse(
    url=f"{host}/api/2.0/mcp/sql",
    headers={"Authorization": f"Bearer {workspace_client.config.token}"},
)
```

## When to Use

- Your agent is running (Steps 1-2) but only generates text — it needs to
  **do things**: query data, search documents, call APIs.
- You want to connect to **Databricks managed MCP servers** or **external
  MCP servers** from an OpenAI Agents SDK agent.
- You need to add **local function tools** for custom business logic.

## Foundation Prerequisite Check

Foundation Step 3 (Tools and Data Access) should be understood before this
step. Verify:

```bash
python3 -c "from databricks_mcp import DatabricksMCPClient; print('F3: OK')" 2>/dev/null || echo "F3: FAIL — pip install databricks-mcp"
```

If F3 fails, install `databricks-mcp` and review
[F3: Tools and Data Access](../../../foundation/03-tools-and-data-access/SKILL.md).

---

## Canonical Tool Catalog (pick what your agent needs)

Track A custom agents typically combine **three classes** of tools. Pick from
this catalog based on the data your agent must reach:

| Class | What it answers | Backing skill | Wire-in pattern |
|---|---|---|---|
| **Knowledge Assistant** (managed doc Q&A with citations) | "What does our policy say about X?" | [F5: Knowledge Assistant Lifecycle](../../../foundation/05-knowledge-assistant/SKILL.md) — produces `ka_endpoint_name` | Call the KA Model Serving endpoint from a `@function_tool` (see _Wiring KA as a function tool_ below) |
| **Genie Space** (NL → SQL on UC tables, conversational analytics) | "How many active customers signed up last week?" | [`data_product_accelerator/skills/semantic-layer/03-genie-space-patterns`](../../../../data_product_accelerator/skills/semantic-layer/03-genie-space-patterns/SKILL.md) and [`04-genie-space-export-import-api`](../../../../data_product_accelerator/skills/semantic-layer/04-genie-space-export-import-api/SKILL.md) — produces `genie_space_id` | Call Genie via the Databricks SDK from a `@function_tool`, **or** wire as Genie MCP server (see F3) |
| **Unity Catalog functions** (deterministic Python or SQL functions, registered in UC) | "Compute next-tier-distance for this customer" | [F3: Tools and Data Access](../../../foundation/03-tools-and-data-access/SKILL.md) (UC Functions MCP section) | Wire as UC Functions MCP server, or call directly via the SDK |
| **Vector Search MCP** (custom retrieval pipeline) | "Custom hybrid search with re-ranker" | F3 (Vector Search MCP) | `MCPServerSse` direct wiring (see below) |
| **Local Python tools** (business logic, math, formatting) | "Compute margin", "format response" | This skill — `@function_tool` (see below) | Decorator |

> **Canonical default for the SkyLoyalty walkthrough:** Knowledge Assistant
> + Genie Space + a small set of `@function_tool` helpers. This pairing
> covers structured analytics (Genie), unstructured Q&A (KA), and bespoke
> business logic (functions) without a custom RAG stack.

### Serving-endpoint API shape per endpoint kind

Different endpoint kinds use different request shapes. The most common bug
in this skill's history is reaching for Chat Completions on every endpoint;
**KA uses Responses API and Genie uses a two-call SDK sequence**. Use this
table as the canonical wiring reference:

| Endpoint kind | Wire via | Request shape | Notes |
|---|---|---|---|
| **Knowledge Assistant** | Raw `requests.post` to `{host}/serving-endpoints/{name}/invocations` | Responses API: `{"input": [{"role": "user", "content": "..."}]}` | Parse `output[].content[].text`. Do NOT use `serving_endpoints.query(messages=...)` — KA rejects `messages` and the SDK's typing surfaces it as `'dict' object has no attribute 'as_dict'`. |
| **Foundation Model API** (Sonnet, llama-3.3, gpt-5-2) | `databricks_openai.AsyncDatabricksOpenAI` or `OpenAI(base_url=...)` | OpenAI Chat Completions: `messages=[...]` | Standard OpenAI-compatible client patterns apply. |
| **Genie Space** | SDK two-call sequence | (1) `w.genie.start_conversation_and_wait(space_id=..., content=...)` returns description + attachments[] (2) `w.genie.get_message_query_result_by_attachment(space_id, conversation_id, message_id, attachment_id)` returns rows | First call alone surfaces the SQL plan as prose, not the rows — always make both calls. See **Wiring Genie as a function tool** below. |
| **AI Gateway endpoint** | REST `POST /api/2.0/serving-endpoints` | `external_model.databricks-model-serving` shape | See [F4: AI Gateway](../../../foundation/04-ai-gateway/SKILL.md) for the create-endpoint payload. |

### Wiring KA as a function tool (Track A pattern)

KA exposes a Model Serving endpoint, but **KA serves the Responses API, not
Chat Completions.** A `serving_endpoints.query(name=..., messages=[...])`
call against a KA endpoint fails with `Invalid request: 'messages' field is
not supported` (and may surface earlier as a Python `'dict' object has no
attribute 'as_dict'` typing trap inside the SDK shim).

Call the invocations URL directly with the Responses-API request body:

```json
{"input": [{"role": "user", "content": "question"}]}
```

and parse the response as `output[].content[].text`:

```python
import os
import requests
from agents import function_tool
from databricks.sdk import WorkspaceClient

KA_ENDPOINT = os.environ["KA_ENDPOINT_NAME"]  # captured in F5

@function_tool
def search_policy_docs(query: str) -> str:
    """Search policy documents and return cited answers.

    Args:
        query: Natural-language question about loyalty program policy.
    """
    w = WorkspaceClient()
    host = w.config.host.rstrip("/")
    url = f"{host}/serving-endpoints/{KA_ENDPOINT}/invocations"

    # KA uses the Responses API: `input`, NOT Chat Completions `messages`.
    body = {"input": [{"role": "user", "content": query}]}
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {w.config.token}",
                 "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    resp.raise_for_status()
    payload = resp.json()

    # Responses API: payload["output"][i]["content"][j]["text"]
    parts = []
    for item in payload.get("output", []):
        for chunk in item.get("content", []):
            text = chunk.get("text")
            if text:
                parts.append(text)
    return "\n".join(parts) or "(no answer)"
```

> **DON'T** use `w.serving_endpoints.query(name=..., messages=[...])` against
> a KA endpoint. KA does not accept Chat Completions `messages`. Use raw
> `requests.post` with `{"input": [...]}` against the invocations URL as
> shown above. (Foundation Model API endpoints — Sonnet, llama-3.3, gpt-5-2 —
> do accept Chat Completions and can use the OpenAI-compatible client.)

Declare the KA endpoint as a `serving_endpoint` resource (`CAN_QUERY`) in
`databricks.yml` so the deployed agent has access — see the resource-kind
reference below.

### Wiring Genie as a function tool

Genie spaces require a **two-call sequence** via the SDK. The first call
returns the planner description and message metadata; the rows live on the
attachment and must be fetched in a second call. Tools that return only the
first call's output deliver SQL-as-prose to the LLM, not data.

1. `w.genie.start_conversation_and_wait(space_id=..., content=...)` — starts
   the conversation, runs the planner, and returns a `GenieMessage` whose
   `attachments[]` carry the query metadata (each attachment has an
   `attachment_id`). The message's `content`/text is the **description**, not
   the rows.
2. `w.genie.get_message_query_result_by_attachment(space_id=..., conversation_id=..., message_id=..., attachment_id=...)`
   — pulls the actual SQL execution result (rows + columns) for the chosen
   attachment.

Combine both into a single tool so the Agents SDK gets both the description
and the rows in one return value:

```python
import os
from agents import function_tool
from databricks.sdk import WorkspaceClient

GENIE_SPACE_ID = os.environ["GENIE_SPACE_ID"]  # captured during semantic-layer setup

@function_tool
def query_loyalty_analytics(question: str) -> str:
    """Answer analytics questions over loyalty data using Genie.

    Args:
        question: Natural-language analytics question (e.g. "active members by tier").
    """
    w = WorkspaceClient()

    # CALL 1: start_conversation_and_wait — planner runs, returns description.
    msg = w.genie.start_conversation_and_wait(
        space_id=GENIE_SPACE_ID,
        content=question,
    )
    description = (msg.content or "").strip()
    if not msg.attachments:
        return description or "(no answer)"

    # CALL 2: get_message_query_result_by_attachment — fetches the rows.
    attachment_id = msg.attachments[0].attachment_id
    result = w.genie.get_message_query_result_by_attachment(
        space_id=GENIE_SPACE_ID,
        conversation_id=msg.conversation_id,
        message_id=msg.message_id,
        attachment_id=attachment_id,
    )

    # Render rows as a small markdown-ish table for the LLM.
    rows_text = "(no rows)"
    sm = getattr(result, "statement_response", None)
    if sm and getattr(sm, "result", None) and getattr(sm.result, "data_array", None):
        rows = sm.result.data_array
        cols = [c.name for c in (sm.manifest.schema.columns or [])] if sm.manifest else []
        header = " | ".join(cols)
        body = "\n".join(" | ".join(str(c) for c in row) for row in rows)
        rows_text = f"{header}\n{body}" if header else body

    return f"{description}\n\n{rows_text}"
```

> **DON'T** stop after `start_conversation_and_wait`. The first call may
> return only a description (and zero attachments for refusals); always
> fetch `get_message_query_result_by_attachment` for each attachment whose
> rows you want to surface to the LLM.

Declare a `genie_space` resource in `databricks.yml`. **Bundle bindings use
`name` + `space_id`** (not a bare `id`):

```yaml
- name: genie-space
  genie_space:
    space_id: ${var.genie_space_id}
    permission: CAN_RUN
```

The outer `name:` is the resource binding (referenced by `valueFrom:` in
`app.yaml`); the inner `space_id:` is the Genie Space identifier the
platform looks up. Plus declare the underlying `sql_warehouse` the space
uses.

---

## Local Function Tools

### OpenAI Agents SDK: `@function_tool`

The simplest way to give your agent capabilities — define Python functions
and decorate them:

```python
from agents import Agent, function_tool
from datetime import datetime

@function_tool
def get_current_time() -> str:
    """Get the current date and time in ISO format."""
    return datetime.now().isoformat()

@function_tool
def calculate_metrics(revenue: float, cost: float) -> dict:
    """Calculate profit margin and ROI from revenue and cost.

    Args:
        revenue: Total revenue in dollars.
        cost: Total cost in dollars.
    """
    profit = revenue - cost
    margin = (profit / revenue * 100) if revenue > 0 else 0
    return {"profit": profit, "margin_pct": round(margin, 2)}

@function_tool
def search_knowledge_base(query: str, max_results: int = 5) -> list[dict]:
    """Search the internal knowledge base for relevant documents.

    Args:
        query: Natural language search query.
        max_results: Maximum number of results to return (default 5).
    """
    from databricks.sdk import WorkspaceClient
    w = WorkspaceClient()
    results = w.vector_search_indexes.query_index(
        index_name="prod.docs.knowledge_index",
        columns=["content", "source", "score"],
        query_text=query,
        num_results=max_results,
    )
    return [
        {"content": r["content"], "source": r["source"], "score": r["score"]}
        for r in results.result.data_array
    ]

agent = Agent(
    name="analyst",
    instructions="You are a data analyst. Use tools to answer questions accurately.",
    model="databricks-claude-sonnet-4-6",
    tools=[get_current_time, calculate_metrics, search_knowledge_base],
)
```

**Tool docstrings are critical.** The LLM uses them to decide when and how to
call each tool. Write clear descriptions with typed arguments.

---

## Wiring MCP Servers with `DatabricksMCPClient`

The `databricks-mcp` library (covered in
[F3](../../../foundation/03-tools-and-data-access/SKILL.md)) is the recommended
way to connect to managed and external MCP servers. For the OpenAI Agents SDK,
you can wire MCP tools alongside local function tools.

### Using `MCPServerSse` (Direct Wiring)

The OpenAI Agents SDK natively supports MCP via `MCPServerSse`:

```python
from agents import Agent
from agents.mcp import MCPServerSse
from databricks.sdk import WorkspaceClient

ws = WorkspaceClient()
host = ws.config.host

ai_search_mcp = MCPServerSse(
    # AI Search (formerly Vector Search); legacy /mcp/vector-search/ prefix still works
    url=f"https://{host}/api/2.0/mcp/ai-search/prod/docs/knowledge_index",
    headers={"Authorization": f"Bearer {ws.config.token}"},
)

sql_mcp = MCPServerSse(
    url=f"https://{host}/api/2.0/mcp/sql",
    headers={"Authorization": f"Bearer {ws.config.token}"},
)

github_mcp = MCPServerSse(
    url=f"https://{host}/api/2.0/mcp/external/github_connection",
    headers={"Authorization": f"Bearer {ws.config.token}"},
)

agent = Agent(
    name="analyst",
    instructions="Use tools to search documents, query data, and check code.",
    model="databricks-claude-sonnet-4-6",
    mcp_servers=[ai_search_mcp, sql_mcp, github_mcp],
)
```

### Combining Local Tools and MCP Servers

Mix `@function_tool` definitions with MCP servers:

```python
agent = Agent(
    name="analyst",
    instructions="Use tools to answer questions. Use calculate_metrics for math.",
    model="databricks-claude-sonnet-4-6",
    tools=[calculate_metrics, get_current_time],
    mcp_servers=[ai_search_mcp, sql_mcp],
)
```

### Environment-Aware Auth for MCP

Handle auth consistently across local dev and Databricks Apps:

```python
import os
from databricks.sdk import WorkspaceClient

def get_mcp_headers():
    w = WorkspaceClient()
    return {"Authorization": f"Bearer {w.config.token}"}

def get_workspace_host():
    return os.environ.get("DATABRICKS_HOST", "").rstrip("/")
```

Use `get_mcp_headers()` when constructing `MCPServerSse`. Adjust if using OBO
(see [A4: Authentication](../04-authentication/SKILL.md)).

---

## Resource Grants for Deployment

When your agent uses MCP servers or other Databricks resources, you need to
declare workspace resource attachments and UC grants.

For the complete grant matrix, `app.yaml`/`databricks.yml` examples, UC SQL
patterns, MLflow `resources` declarations, and the `get_databricks_resources()`
auto-discovery pattern, see
[F3: Resource Grants](../../../foundation/03-tools-and-data-access/references/resource-grants.md).

### Resource-kind quick reference

When declaring resources in `databricks.yml`, the kind depends on what the
resource is. **Use `uc_securable` only for UC objects that have no dedicated
top-level resource type** (functions, tables, schemas, volumes, models).
Warehouses, serving endpoints, and UC connections have their own top-level
kinds — do not wrap them in `uc_securable`.

| Resource | Bundle kind | Permission | Inner identifier field |
|----------|-------------|------------|------------------------|
| SQL warehouse | `sql_warehouse` | `CAN_USE` | `id:` |
| LLM / chat model endpoint (route from `runtime_config.llm`) | `serving_endpoint` | `CAN_QUERY` | `name:` |
| Knowledge Assistant endpoint | `serving_endpoint` | `CAN_QUERY` | `name:` (the KA's serving endpoint name) |
| Vector Search endpoint | `serving_endpoint` | `CAN_QUERY` | `name:` |
| Genie Space | `genie_space` | `CAN_RUN` | `space_id:` (NOT `id:` — see note below) |
| UC connection (external HTTP/MCP) | `connection` | `USE CONNECTION` | `name:` |
| UC function (incl. `system.ai.python_exec`) | `uc_securable` with `securable_type: FUNCTION` | `EXECUTE` (via `USAGE` + `EXECUTE` grants on the securable) | `securable_full_name:` |
| UC table / view | `uc_securable` with `securable_type: TABLE` | `SELECT` | `securable_full_name:` |
| UC schema | `uc_securable` with `securable_type: SCHEMA` | `USE_SCHEMA` | `securable_full_name:` |
| UC model | `uc_securable` with `securable_type: MODEL` | `USE_MODEL` or `EXECUTE` per scenario | `securable_full_name:` |
| Another Databricks App (backend) | `app` | `CAN_USE` — see [`06d-appkit-agent-app-proxy`](../../../../apps_lakebase/skills/06d-appkit-agent-app-proxy/references/app-resource-declaration.md) | `name:` |

> **`genie_space` resource shape:** The DAB binding takes the outer `name:`
> (the resource binding label, used by `valueFrom:` in `app.yaml`) plus the
> inner `space_id:` (the Genie Space identifier). It does **not** accept a
> bare `id:` like `sql_warehouse` does. Using `id:` silently fails
> validation in some CLI versions and leaves the app unable to resolve the
> resource at runtime. Always use `name` + `space_id`.

Model grants are derived from `docs/agent_tool_plan.yaml.runtime_config.llm`.

- When `provider == "databricks"`, grant `CAN_QUERY` on `runtime_config.llm.endpoint`.
- When `provider == "ai_gateway"`, do not create or configure Gateway. Verify the pre-provisioned endpoint and required permissions are documented, then leave provisioning to the optional Gateway hardening step.

Verify the bundle schema accepts each kind your agent needs before deploying:

> **Client note:** IDE runs this in a terminal; Genie Code runs the `databricks bundle …` command via `runDatabricksCli`. See `skills/genie-code-environment`.

```bash
# Generic "does this kind exist in my CLI's schema?"
databricks bundle schema \
  | jq '.definitions | keys[]' \
  | grep -i 'AppResource_'
```

Expected output includes `AppResource_SQL_WAREHOUSE`, `AppResource_SERVING_ENDPOINT`, `AppResource_UC_SECURABLE`, `AppResource_CONNECTION`, `AppResource_GENIE_SPACE`, and (for CLI >= 0.295.0) `AppResource_APP`. If a needed kind is missing, upgrade the CLI.

### Canonical agent-app `app.yaml` + `databricks.yml` (KA + Genie + LLM)

Most Track A agents need a triad of resources: an LLM endpoint, a KA
endpoint, and a Genie Space (with its underlying SQL warehouse). The
canonical declaration is:

```yaml
# app.yaml — Agent App
command:
  - mlflow
  - genai
  - agent-server
  - serve
  - --module
  - agent
env:
  - name: LLM_ENDPOINT
    valueFrom: llm-endpoint
  - name: KA_ENDPOINT_NAME
    valueFrom: ka-endpoint
  - name: GENIE_SPACE_ID
    valueFrom: genie-space
  - name: WAREHOUSE_ID
    valueFrom: sql-warehouse
```

```yaml
# databricks.yml — Agent App resource block
resources:
  apps:
    ${var.agent_app_name}:
      source_code_path: ./
      resources:
        - name: llm-endpoint
          serving_endpoint:
            name: databricks-claude-sonnet-4-6
            permission: CAN_QUERY
        - name: ka-endpoint
          serving_endpoint:
            name: ${var.ka_endpoint_name}
            permission: CAN_QUERY
        - name: genie-space
          genie_space:
            space_id: ${var.genie_space_id}
            permission: CAN_RUN
        - name: sql-warehouse
          sql_warehouse:
            id: ${var.warehouse_id}
            permission: CAN_USE
```

This is the resource shape the SkyLoyalty walkthrough (canonical) uses. The
`valueFrom: <resource-name>` mapping in `app.yaml` resolves to the resource's
URL or id at runtime — your agent reads `os.environ["KA_ENDPOINT_NAME"]` etc.
without hardcoding workspace identifiers.

---

## Custom Retriever Schemas

If your agent includes a custom retriever (not using AI Bridge tools like
`VectorSearchRetrieverTool`), you must declare the retriever's output schema
for AI Playground source links and evaluation judges.

For the complete pattern, see
[F3: Custom Retriever Schemas](../../../foundation/03-tools-and-data-access/references/custom-retriever-schemas.md).

**SDLC connection:** The retriever schema declared here feeds directly into the
SDLC evaluation pipeline. [S4: Evaluation Runs](../../../sdlc/04-evaluation-runs/SKILL.md)
uses `doc_uri` to run groundedness and relevance judges against your eval
dataset's `expected_retrieved_context`.

---

## Testing Tools Locally

### Interactive test

```bash
uv run start-app
# Then in browser at http://localhost:8000:
# "What time is it?" -> should invoke get_current_time
# "Calculate margin for $1M revenue and $600K cost" -> should invoke calculate_metrics
```

### Programmatic test

```python
import asyncio
from agents import Runner

async def test_tools():
    result = await Runner.run(agent, "What time is it?")
    print(f"Output: {result.final_output}")
    print(f"Tools called: {[s.name for s in result.raw_responses]}")

asyncio.run(test_tools())
```

### Verify in MLflow traces

After calling the agent, check MLflow traces for TOOL spans alongside AGENT
and LLM spans. Each tool call should appear as a distinct span with:
- Input: the tool arguments
- Output: the tool return value
- Span type: TOOL

---

## DO / DON'T

### DO — Write detailed tool docstrings with typed args

```python
@function_tool
def search_products(
    query: str,
    category: str = "all",
    max_results: int = 10,
) -> list[dict]:
    """Search the product catalog by keyword.

    Args:
        query: Natural language search query for products.
        category: Filter by product category. Use "all" for no filter.
        max_results: Maximum number of products to return.
    """
    ...
```

### DON'T — Use vague docstrings or skip type hints

```python
@function_tool
def search(q, n=10):
    """Search for stuff."""  # LLM won't know what or how to search
    ...
```

### DO — Handle tool errors gracefully

```python
@function_tool
def query_database(sql: str) -> str:
    """Execute a SQL query against the analytics warehouse."""
    try:
        result = execute_sql(sql)
        return format_results(result)
    except Exception as e:
        return f"Query failed: {str(e)}. Please try a simpler query."
```

### DON'T — Let tools raise unhandled exceptions

```python
@function_tool
def query_database(sql: str) -> str:
    """Execute a SQL query."""
    return execute_sql(sql)  # Exception crashes the agent loop
```

---

## Common Issues

| Issue | Fix |
|-------|-----|
| Tool not called by agent | Improve the tool's docstring — the LLM needs clear description of when to use it |
| `MCPServerSse` connection refused | Check MCP URL format and auth headers; verify the endpoint exists |
| `PermissionDenied` on Vector Search | Grant SP access — see [F3: Resource Grants](../../../foundation/03-tools-and-data-access/references/resource-grants.md) |
| Tool returns but agent ignores result | Check that the tool return type is `str` or simple `dict` — complex objects may confuse the LLM |
| MCP tools not appearing | Verify the MCP server URL is correct and the server is running |
| `ModuleNotFoundError` in tool | Move imports inside the tool function for serialization safety |

---

## Validation Gate

All must pass before proceeding:

- [ ] At least one local `@function_tool` added and callable by the agent
- [ ] Agent correctly invokes the tool when prompted (visible in chat and traces)
- [ ] MCP connection configured for at least one Databricks service (if applicable)
- [ ] Resource grants identified for all tools that need workspace resources
- [ ] Tool calls appear as TOOL spans in MLflow traces
- [ ] Tool errors are handled gracefully (no unhandled exceptions)
- [ ] If using custom retrievers: `mlflow.models.set_retriever_schema()` called at module level
- [ ] **KA tool uses Responses API** — request body is `{"input": [...]}` against `/serving-endpoints/{name}/invocations`, NOT `serving_endpoints.query(messages=[...])`
- [ ] **Genie tool issues both calls** — `start_conversation_and_wait` followed by `get_message_query_result_by_attachment` for each attachment whose rows are returned to the LLM
- [ ] **`databricks.yml` `genie_space` resource uses `name` + `space_id`** (not bare `id:`)

## Next Step

After passing this gate, **load and execute**
`tracks/A-custom-agent-apps/04-authentication/SKILL.md` (A4: Authentication).

## Notes to Carry Forward

| Key | Value |
|-----|-------|
| `local_tools` | List of `@function_tool` function names |
| `mcp_servers` | List of MCP server URLs configured |
| `app_yaml_resources` | Resources declared in `app.yaml` |
| `uc_grants_needed` | UC GRANT statements for deployment |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [F3: Tools and Data Access](../../../foundation/03-tools-and-data-access/SKILL.md) | Foundation — MCP servers, grants, retrievers |
| [F5: Knowledge Assistant Lifecycle](../../../foundation/05-knowledge-assistant/SKILL.md) | Tool catalog — managed doc Q&A; produces `ka_endpoint_name` |
| [Genie Space Patterns](../../../../data_product_accelerator/skills/semantic-layer/03-genie-space-patterns/SKILL.md) | Tool catalog — NL → SQL on UC tables; produces `genie_space_id` |
| [Genie Space Export/Import API](../../../../data_product_accelerator/skills/semantic-layer/04-genie-space-export-import-api/SKILL.md) | Tool catalog — versioning Genie spaces across environments |
| [A2: Agent Framework](../02-agent-framework/SKILL.md) | Previous step — produces `agent_class` |
| [A4: Authentication](../04-authentication/SKILL.md) | Next step |
| [S4: Evaluation Runs](../../../sdlc/04-evaluation-runs/SKILL.md) | Custom retriever schemas enable groundedness/relevance judges |

## References

- [Build a tool for your agent](https://docs.databricks.com/aws/en/generative-ai/agent-framework/build-agent-tool)
- [MCP servers on Databricks](https://docs.databricks.com/aws/en/generative-ai/agent-framework/mcp-server)
- [Author an agent](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent)
- [OpenAI Agents SDK — Tools](https://openai.github.io/openai-agents-python/tools/)
- [OpenAI Agents SDK — MCP](https://openai.github.io/openai-agents-python/mcp/)
- [Add resources to a Databricks app](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/resources)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.1.0 | 2026-04-26 | Document tool/data-product API shapes (Phase 3.8): KA serving uses Responses API (`{"input": [...]}`) not Chat Completions `messages`; Genie requires the two-call sequence (`start_conversation_and_wait` returns description, `get_message_query_result_by_attachment` returns rows); DAB `genie_space` resource uses `name` + `space_id`, not bare `id`. Added serving-endpoint-API-shape table covering KA / FMAPI / Genie / AI Gateway. |
| 3.0.0 | 2026-04-12 | Refactored: MCP concepts, resource grants, retriever schemas moved to F3. Focus on Agent SDK wiring with DatabricksMCPClient and MCPServerSse. |
| 2.0.0 | 2026-04-10 | Progressive disclosure: MCP config and resource grants in references/ |
| 1.0.0 | 2026-04-10 | Initial skill: function tools, MCP servers, resource grants, testing patterns |
