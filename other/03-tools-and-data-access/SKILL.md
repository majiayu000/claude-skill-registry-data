---
name: 03-tools-and-data-access
description: >
  Use when connecting any agent to data and external capabilities. Covers
  Databricks managed MCP servers (Vector Search, Genie, SQL, UC Functions),
  the databricks-mcp client library, _meta parameters, external MCP servers,
  code interpreter, non-MCP connections, resource grants, custom retriever
  schemas, tool cookbook (web search, SQL, file generation, HTTP), runtime
  guardrails, and end-to-end external MCP examples. Foundation Step 3.
  Consumed by all agent tracks (A, B, C).
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Agent tools + managed/external MCP servers + UC resource grants — code + grants, no bundle resource. Tooling resolves identically on both clients; on Genie Code use its built-in tool surface and run grant CLI steps through runDatabricksCli. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "1.2.0"
  domain: "genai-agents"
  pipeline_position: "F3"
  consumes: "mlflow_environment, experiment_paths"
  produces: "mcp_server_knowledge, resource_grants, retriever_schemas, databricks_mcp_client"
  grounded_in: "docs.databricks.com/aws/en/generative-ai/mcp/managed-mcp, docs.databricks.com/aws/en/generative-ai/mcp/external-mcp, docs.databricks.com/aws/en/generative-ai/agent-framework/build-agent-tool, docs.databricks.com/aws/en/generative-ai/agent-framework/mcp-server"
fields_read:
  - resources.knowledge_base_documents
  - resources.genie_spaces
  - resources.vector_search_indexes
  - agent.tools
  - agent.mcp_servers
  - agent.knowledge_base_backend
  - agent.external_integrations
---

# Tools and Data Access

Give your agent capabilities beyond text generation: query structured data,
search documents, invoke custom functions, and connect to external services.
This foundational skill covers the Databricks MCP ecosystem that all agent
tracks build on.

> **Public Preview.** MCP on Databricks is in Public Preview. Refer to the
> source documentation links in the References section for the latest server
> types, URL patterns, `_meta` parameters, and authentication methods.

## When to Use

Use this skill when you are:

- Connecting any agent to **Databricks managed MCP servers** (Vector Search,
  Genie, SQL, UC Functions).
- Adding the **code interpreter** (`system.ai.python_exec`) for dynamic
  Python execution.
- Installing **external MCP servers** (GitHub, Glean, Atlassian, or custom).
- Connecting to **external services without MCP** via the UC connections
  proxy, managed OAuth, or UC function `http_request()`.
- Using **pre-built tool recipes** (web search, SQL execution, file
  generation, HTTP API calls) from the tool cookbook — with wiring for
  all tracks (A/C via `@function_tool`, B via UC Functions).
- Adding **runtime guardrails** (input screening, output filtering) to
  protect against prompt injection, PII leaks, and toxic content.
- Configuring **resource grants** for deployed agents (Apps, Model Serving).
- Declaring **custom retriever schemas** for evaluation and AI Playground.
- Understanding which tool types exist and how they differ before wiring
  them into a specific track.

**Prerequisite:** Foundation Steps 1 and 2 must be complete (MLflow environment,
experiment paths, tracing). See
[F1](../01-mlflow-genai-foundation/SKILL.md) and
[F2](../02-experiment-tracing-and-uc-storage/SKILL.md).

---

## The `databricks-mcp` Library

The `databricks-mcp` Python package is the **recommended** way to connect to
both managed and external MCP servers on Databricks. It handles authentication,
tool discovery, tool invocation, and resource enumeration.

### Install

```bash
pip install -U "databricks-mcp" "databricks-sdk" "mcp>=1.9"
```

### Core Pattern: `DatabricksMCPClient`

```python
from databricks.sdk import WorkspaceClient
from databricks_mcp import DatabricksMCPClient

workspace_client = WorkspaceClient()
host = workspace_client.config.host

mcp_client = DatabricksMCPClient(
    server_url=f"{host}/api/2.0/mcp/functions/system/ai",
    workspace_client=workspace_client,
)

tools = mcp_client.list_tools()
print(f"Available tools: {[t.name for t in tools]}")

result = mcp_client.call_tool("system__ai__python_exec", {"code": "print(42)"})
print(result.content[0].text)
```

### OAuth Authentication

For async code or the standard MCP SDK, use `DatabricksOAuthClientProvider`:

```python
from databricks_mcp import DatabricksOAuthClientProvider
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession

async with streamablehttp_client(
    url=mcp_server_url,
    auth=DatabricksOAuthClientProvider(workspace_client),
) as (read_stream, write_stream, _):
    async with ClientSession(read_stream, write_stream) as session:
        await session.initialize()
        tools = await session.list_tools()
```

### Auto-Discovering Resources for Deployment

When logging an agent for Model Serving, `get_databricks_resources()`
enumerates every UC object the MCP server exposes — eliminating manual
resource listing:

```python
from databricks_mcp import DatabricksMCPClient

mcp_client = DatabricksMCPClient(
    server_url=f"{host}/api/2.0/mcp/functions/prod/analytics",
    workspace_client=workspace_client,
)
resources = mcp_client.get_databricks_resources()
```

Pass these resources directly to `mlflow.pyfunc.log_model(resources=...)`.
See the Resource Grants section below and
[`references/resource-grants.md`](references/resource-grants.md) for the
full pattern.

---

## Databricks Managed MCP Servers

Databricks provides four managed MCP servers. Unity Catalog permissions are
always enforced — agents and users can only access tools and data they are
allowed to.

| MCP Server | URL Pattern | OAuth Scope | Purpose |
|---|---|---|---|
| **AI Search** | `/api/2.0/mcp/ai-search/{catalog}/{schema}/{index_name}` | `ai-search` | Semantic search over indexed documents. Index must use Databricks managed embeddings. |
| **Genie Space** | `/api/2.0/mcp/genie/{genie_space_id}` | `genie` | Query a single Genie Space to analyze structured data via natural language. Read-only. |
| **Genie (cross-space)** | `/api/2.0/mcp/genie` | `genie` | Ask natural-language questions across all Genie Spaces and UC data; returns a grounded answer with a deep link. Read-only. |
| **Databricks SQL** | `/api/2.0/mcp/sql` | `sql` | Run AI-generated SQL for data pipelines and ad-hoc queries. Read and write. |
| **UC Functions** | `/api/2.0/mcp/functions/{catalog}/{schema}/{function_name}` | `unity-catalog` | Call registered Unity Catalog SQL/Python functions. |

> **Naming note:** AI Search was formerly **Vector Search**. The legacy
> `/api/2.0/mcp/vector-search/...` URL prefix and `vector-search` OAuth scope
> still work for backward compatibility, but `ai-search` is the current
> canonical name.

To view your MCP servers and their endpoint URLs, go to your workspace >
**AI Gateway** > **MCPs**.

### Polling Note

The Genie, Genie Space, and Databricks SQL MCP servers run asynchronously and
require polling for results of long-running queries (e.g. call `genie_ask`,
then poll `genie_poll_response`). Handle this in your tool invocation loop.

### Example: Customer Support Agent

```python
host = workspace_client.config.host

MANAGED_MCP_SERVER_URLS = [
    f"{host}/api/2.0/mcp/ai-search/prod/customer_support/ticket_index",
    f"{host}/api/2.0/mcp/genie/{billing_space_id}",
    f"{host}/api/2.0/mcp/functions/prod/billing/lookup_account",
]
```

This gives the agent access to unstructured data (support tickets), structured
data (billing tables via Genie), and custom business logic (account lookups).

For detailed per-server code examples, see
[`references/managed-mcp-servers.md`](references/managed-mcp-servers.md).

---

## `_meta` Parameters

The `_meta` parameter is part of the MCP specification. It lets you **preset
configuration** for deterministic behavior while keeping queries flexible for
the LLM to generate dynamically.

### SQL MCP `_meta`

| Parameter | Type | Description |
|---|---|---|
| `warehouse_id` | str | SQL warehouse ID for executing queries. If not specified, the system selects automatically. |

### Vector Search MCP `_meta`

| Parameter | Type | Description |
|---|---|---|
| `num_results` | int | Number of results to return |
| `filters` | str | JSON string of filters (e.g. `'{"updated_after": "2024-01-01"}'`) |
| `query_type` | str | `"ANN"` (default) or `"HYBRID"` (vector + keyword) |
| `columns` | str | Comma-separated column names to return |
| `columns_to_rerank` | str | Comma-separated columns for reranking |
| `include_score` | bool | Include similarity score (`"true"` / `"false"`) |
| `score_threshold` | float | Minimum similarity score filter |

### Example: Using `_meta` with the MCP SDK

```python
from mcp.types import CallToolRequest, CallToolResult

request = CallToolRequest(
    method="tools/call",
    params={
        "name": "execute_sql",
        "arguments": {
            "query": "SELECT * FROM my_catalog.my_schema.sales LIMIT 10"
        },
        "_meta": {
            "warehouse_id": "a1b2c3d4e5f67890"
        }
    }
)

response = await session.send_request(request, CallToolResult)
```

### DO / DON'T

**DO** — Use `_meta` for configuration that should be deterministic:

```python
"_meta": {
    "warehouse_id": config.get("warehouse_id"),
    "num_results": "5",
    "query_type": "HYBRID",
}
```

**DON'T** — Put the user's dynamic query in `_meta`:

```python
"_meta": {"query": user_question}  # WRONG: query is a dynamic argument
```

For complete `_meta` examples per server type, see
[`references/managed-mcp-servers.md`](references/managed-mcp-servers.md).

### Dynamic SQL MCP From Agent Tool Plan

When SQL MCP is selected through `docs/agent_tool_plan.yaml`, default to
read-only schema-scoped access:

- Pin `_meta.warehouse_id` from `selected_mcp_servers[].meta.warehouse_id`.
- Restrict generated SQL to `SELECT`, `DESCRIBE`, and `EXPLAIN`.
- Require fully qualified `catalog.schema.table` references.
- Use `selected_mcp_servers[].scope.allowed_tables` when present.
- Do not run DDL or DML unless the user explicitly changes `readonly` to false.

---

## External MCP Servers

Connect agents to third-party MCP servers through Databricks-managed proxies.
The proxy handles authentication and token management; the external server
appears as a standard MCP endpoint.

### Four Installation Methods

| Method | When to Use | Credential Management |
|---|---|---|
| **Managed OAuth** | Glean, GitHub, Atlassian (supported providers) | None — Databricks manages OAuth flows |
| **Databricks Marketplace** | Curated servers with pre-built integrations | Enter credentials during install |
| **Custom HTTP Connection** | Any MCP server (self-hosted or third-party) | Manual — provide bearer token or OAuth creds |
| **Dynamic Client Registration** | MCP servers supporting OAuth 2.0 DCR (RFC 7591) | Automatic — DCR handles registration |

### Proxy URL Pattern

After installation, every external MCP server is accessible at:

```
https://{workspace_host}/api/2.0/mcp/external/{connection_name}
```

`DatabricksMCPClient` works identically for both managed and external
(proxied) servers — add the proxy URL to your server URL list:

```python
MANAGED_MCP_SERVER_URLS = [
    f"{host}/api/2.0/mcp/functions/system/ai",
    f"{host}/api/2.0/mcp/external/github_connection",
]
```

### Per-User vs Shared Principal Authentication

| Auth Type | How It Works | Use When |
|---|---|---|
| **Shared principal** | All users share one set of credentials (bearer token, OAuth M2M, OAuth U2M shared) | External service doesn't need user-specific access |
| **Per-user (OAuth U2M Per User)** | Each user authenticates with their own credentials | Accessing user-specific resources (repos, messages, calendars) |

### Testing Before Wiring

Test external MCP servers in **AI Playground** without writing code:

1. Go to AI Playground > choose a model with the **Tools enabled** label.
2. Click **Tools > + Add tool > MCP Servers > External MCP servers**.
3. Select your UC connection and chat with the LLM.

For detailed installation walkthroughs (including Managed OAuth provider
table, Marketplace flow, DCR code, and security guidance), see
[`references/external-mcp-connections.md`](references/external-mcp-connections.md).

---

## Code Interpreter (`system.ai.python_exec`)

Databricks provides a built-in code interpreter via the `system.ai.python_exec`
Unity Catalog function. It lets agents dynamically write and execute Python
code — useful for calculations, data transformations, chart generation, or
any task better solved with code than natural language.

### Wiring

The code interpreter is available as a managed MCP tool at the UC Functions
endpoint for `system.ai`:

```python
from agents import Agent, Runner
from databricks.sdk import WorkspaceClient
from databricks_openai.agents import McpServer

workspace_client = WorkspaceClient()
host = workspace_client.config.host

async with McpServer.from_uc_function(
    catalog="system",
    schema="ai",
    function_name="python_exec",
    workspace_client=workspace_client,
    name="code-interpreter",
) as code_interpreter:
    agent = Agent(
        name="coding-agent",
        instructions="Use the python_exec tool to run code when calculations or data manipulation are needed.",
        model="databricks-claude-sonnet-4-6",
        mcp_servers=[code_interpreter],
    )
    result = await Runner.run(agent, "Calculate the first 10 Fibonacci numbers")
    print(result.final_output)
```

Alternatively, use the `DatabricksMCPClient` pattern:

```python
mcp_client = DatabricksMCPClient(
    server_url=f"{host}/api/2.0/mcp/functions/system/ai/python_exec",
    workspace_client=workspace_client,
)
result = mcp_client.call_tool("system__ai__python_exec", {"code": "print(sum(range(100)))"})
```

### Use Cases

- **Calculations:** Agent needs to compute financial metrics, statistics, or
  math that shouldn't be approximated by the LLM.
- **Data transformation:** Parse CSV/JSON, reshape data, apply business rules.
- **Chart generation:** Create matplotlib/plotly visualizations from query
  results.
- **Validation:** Run deterministic checks on data before returning answers.

### Safety Notes

- The code interpreter runs in a **sandboxed environment** — it cannot access
  the local filesystem, network, or workspace resources beyond what the
  function's identity allows.
- Execution is **stateless** — each `python_exec` call starts fresh with no
  shared memory between invocations.
- Use clear instructions to tell the agent **when** to use code execution vs.
  other tools (e.g., "Use python_exec for calculations, use SQL MCP for
  data queries").

### Resource Grant

Grant the app's service principal access to the function in `databricks.yml`:

```yaml
resources:
  apps:
    my_agent_app:
      resources:
        - name: 'python_exec'
          uc_securable:
            securable_full_name: 'system.ai.python_exec'
            securable_type: 'FUNCTION'
            permission: 'EXECUTE'
```

See [Code interpreter tools](https://docs.databricks.com/aws/en/generative-ai/agent-framework/code-interpreter-tools)
for the full reference.

---

## Non-MCP External Service Connections

Not every external service has an MCP server. For services that expose only a
REST API (Slack, Google Drive, SharePoint, or any custom API), Databricks
offers two alternative connection approaches that still use Unity Catalog
HTTP connections for secure credential management.

### UC Connections Proxy

Point the external service's own client SDK at the Databricks proxy endpoint.
Databricks authenticates the request and injects the external service's
credentials from the UC connection — your code never handles external tokens
directly.

**Proxy URL:**

```
https://{workspace_host}/api/2.0/unity-catalog/connections/{connection_name}/proxy[/sub-path]
```

**Example: Calling OpenAI through the proxy**

First, create the UC connection:

```sql
CREATE CONNECTION openai_connection TYPE HTTP
OPTIONS (
  host 'https://api.openai.com',
  base_path '/v1',
  bearer_token secret('<secret-scope>', '<secret-key>')
);
```

Then use the proxy in agent code:

```python
from databricks_openai import DatabricksOpenAI
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
client = DatabricksOpenAI(
    workspace_client=w,
    base_url=f"{w.config.host}/api/2.0/unity-catalog/connections/openai_connection/proxy/",
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

### Managed OAuth for API Tools

For Google Drive and SharePoint, Databricks manages the OAuth credentials —
no app registration required:

| Provider | Supported Scopes |
|---|---|
| **Google Drive API** | `drive.readonly`, `documents.readonly`, `spreadsheets.readonly` |
| **SharePoint API** | `Sites.Read.All` |

Create an HTTP connection with OAuth U2M Per User auth and select your provider.

### UC Function Tools with `http_request()`

Wrap REST API calls in a UC SQL function for a SQL-first approach:

```sql
CREATE OR REPLACE FUNCTION main.default.slack_post_message(
  text STRING COMMENT 'message content'
)
RETURNS STRING
COMMENT 'Posts a message to the #general Slack channel.'
RETURN (http_request(
  conn => 'slack_connection',
  method => 'POST',
  path => '/api/chat.postMessage',
  json => to_json(named_struct('channel', 'C032G2DAH3', 'text', text))
)).text
```

> **Note:** Databricks recommends MCP servers or the UC connections proxy for
> new integrations. UC function tools with `http_request` remain supported
> but are no longer the recommended approach.

### When to Use Which

| Approach | Best For |
|---|---|
| **External MCP server** | Services with an MCP server — automatic tool discovery, standard SDK |
| **Managed OAuth** | Google Drive, SharePoint — no credential management |
| **UC connections proxy** | Direct REST calls using the service's own SDK |
| **UC function `http_request()`** | SQL-based tool definitions (legacy approach) |

**Permission:** All approaches require `USE CONNECTION` on the UC HTTP
connection. See [`references/resource-grants.md`](references/resource-grants.md).

See [Connect agents to external services](https://docs.databricks.com/aws/en/generative-ai/agent-framework/external-connection-tools)
for the full reference including example notebooks for Slack, Microsoft Graph
API, and Azure AI Search.

---

## Tool Cookbook

Pre-built tool recipes for common agent capabilities that go beyond managed
MCP servers. Each recipe separates reusable core logic from track-specific
wiring — Track A/C use `@function_tool`, Track B publishes the same logic
as UC Functions.

| Recipe | What It Does |
|---|---|
| **Web search** (Tavily / Brave) | Real-time web results for current events and external info |
| **SQL execution** | Run queries with formatted markdown tables, safety checks, and row limits |
| **File generation** | Create CSV, chart PNG, or PDF artifacts and save to UC Volumes |
| **HTTP API calls** | Call any REST API through the UC connections proxy with managed auth |

Each recipe includes core logic, `@function_tool` wiring (Track A/C),
resource grants, and alternatives. The SQL execution recipe includes a
full UC Function variant for Track B.

See [`references/tool-cookbook.md`](references/tool-cookbook.md) for all
recipes.

---

## Resource Grants

Agents need two layers of permissions to access Databricks resources:

1. **App/bundle resources** — attach workspace capabilities (warehouses,
   endpoints, connections) to the app or serving endpoint.
2. **UC GRANTs** — give the service principal (or OBO user) rights on
   catalogs, schemas, tables, functions, and connections.

Both layers are typically required for MCP-backed tools.

### Grant Matrix

| Capability | App/Bundle Resource | Unity Catalog Grants |
|---|---|---|
| SQL warehouse queries | `sql_warehouse` → `CAN_USE` | Optional table/schema grants |
| LLM / chat model | `serving_endpoint` → `CAN_QUERY` | — |
| Vector Search index | Serving endpoint if required | `USE CATALOG`, `USE SCHEMA`, `SELECT` on index |
| UC Functions MCP | LLM endpoint resource | `USE CATALOG`, `USE SCHEMA`, `EXECUTE` on functions |
| Databricks SQL MCP | `sql_warehouse` → `CAN_USE` | Tables the generated SQL touches |
| External MCP (UC HTTP) | Connection + egress | `USE CONNECTION` on the UC connection |
| Genie MCP | Genie / warehouse | Space + underlying data access |
| Code interpreter (`python_exec`) | `uc_securable` with `EXECUTE` | `EXECUTE` on `system.ai.python_exec` |
| UC connections proxy (non-MCP) | Connection | `USE CONNECTION` on the UC connection |

### Auto-Discovery with `get_databricks_resources()`

Instead of manually listing every resource, use `DatabricksMCPClient` to
enumerate them:

```python
from databricks_mcp import DatabricksMCPClient
from mlflow.models.resources import DatabricksServingEndpoint

resources = [DatabricksServingEndpoint(endpoint_name="databricks-claude-sonnet-4-6")]

for mcp_url in MANAGED_MCP_SERVER_URLS:
    client = DatabricksMCPClient(server_url=mcp_url, workspace_client=ws)
    resources.extend(client.get_databricks_resources())

mlflow.pyfunc.log_model(
    python_model="agent.py",
    resources=resources,
)
```

### DO / DON'T

**DO** — Grant all downstream dependencies:

```sql
GRANT USE CATALOG ON CATALOG prod TO `<app-sp>`;
GRANT USE SCHEMA ON SCHEMA prod.docs TO `<app-sp>`;
GRANT SELECT ON TABLE prod.docs.knowledge_index TO `<app-sp>`;
```

**DON'T** — Assume MCP grants propagate without catalog/schema access:

```sql
GRANT SELECT ON TABLE prod.docs.knowledge_index TO `<app-sp>`;
-- Runtime: "permission denied for catalog prod"
```

For complete grant patterns (`app.yaml`, `databricks.yml`, UC SQL, MLflow
`resources`, and common permission symptoms), see
[`references/resource-grants.md`](references/resource-grants.md).

---

## Custom Retriever Schemas

When your agent includes a custom retriever (not using AI Bridge tools like
`VectorSearchRetrieverTool`), declare its output schema so Databricks can
display source links in AI Playground and run evaluation judges.

```python
import mlflow

mlflow.models.set_retriever_schema(
    name="my_retriever_span",
    primary_key="document_id",
    text_column="chunk_text",
    doc_uri="doc_uri",
    other_columns=["title"],
)
```

The `doc_uri` column is critical for evaluation — it is how groundedness and
relevance judges compare retrieved documents against ground truth.

| Retriever Type | Schema Required? |
|---|---|
| `databricks_openai.VectorSearchRetrieverTool` | No — AI Bridge auto-conforms |
| `databricks_langchain.VectorSearchRetrieverTool` | No — AI Bridge auto-conforms |
| Custom retriever (your own code) | **Yes** |
| Third-party retriever (LlamaIndex, etc.) | **Yes** |

**Recommendation:** Prefer AI Bridge retriever tools when possible. They
conform to the MLflow retriever schema automatically.

**SDLC connection:** The retriever schema declared here feeds into the
evaluation pipeline. [S4: Evaluation Runs](../../sdlc/04-evaluation-runs/SKILL.md)
uses `doc_uri` to run groundedness and relevance judges against your eval
dataset's `expected_retrieved_context`.

For the complete pattern with code examples and DO/DON'T, see
[`references/custom-retriever-schemas.md`](references/custom-retriever-schemas.md).

---

## Runtime Guardrails

Runtime guardrails protect your agent in real time — blocking harmful inputs
before the agent processes them and filtering sensitive data from outputs
before users see them. They complement the post-hoc evaluation judges
covered in [S3](../../sdlc/03-evaluation-datasets/SKILL.md) and
[S4](../../sdlc/04-evaluation-runs/SKILL.md).

**Key concepts:**

- **AI Gateway guardrails** — endpoint-level safety (Llama Guard) and PII
  detection (Presidio) enabled via the Serving UI. No code changes needed.
  Supported on external model and Foundation Model API endpoints (not agent
  endpoints).

- **Application-level input screening** — regex blocklists for prompt
  injection, Presidio for PII detection, and LLM-as-judge classifiers.
  Layer them fast-to-slow for minimal latency impact.

- **Application-level output filtering** — PII scrubbing, secret redaction
  (API keys, connection strings), and tone checks before the response
  reaches the user.

- **OpenAI Agents SDK guardrails** — `InputGuardrail` and `OutputGuardrail`
  classes that plug directly into the Agent lifecycle. Available in Track A.

- **DASF v3.0** — Databricks AI Security Framework with 35 agentic AI risks
  and 6 mitigation controls. The "Rule of Two" principle: an agent becomes
  vulnerable when it has access to sensitive systems, exposure to
  untrustworthy inputs, *and* ability to change state. Design agents to
  have at most two.

See [`references/runtime-guardrails.md`](references/runtime-guardrails.md)
for complete code examples, setup instructions, and the guardrails-vs-
evaluation decision table.

---

## Track-Specific Wiring

This foundational skill covers the **what** (which servers exist, how they
work, what permissions they need). Each track teaches the **how** (framework-
specific wiring):

| Track | How to Wire MCP | Where Tools Live | Skill |
|---|---|---|---|
| **A** (Custom Agent Apps) | `Agent(mcp_servers=[...])` or `@function_tool` | `agent.py` | [A3: Agent SDK Tool Wiring](../../tracks/A-custom-agent-apps/03-tools-and-mcp/SKILL.md) |
| **B** (Supervisor API) | `tools=[{"type": "genie_space", ...}]` in `responses.create()` | `config.yml` + `build_tools_from_config()` | Upstream [`databricks-agent-bricks`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-agent-bricks) |
| **C** (Model Serving) | In `predict()` code + `resources=[...]` at `log_model()` | `agent.py` | Upstream [`databricks-model-serving`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-model-serving) |

---

## Validation Gate

All must pass before proceeding to your chosen track's tool wiring step:

- [ ] `databricks-mcp` installed: `python -c "from databricks_mcp import DatabricksMCPClient; print('OK')"`
- [ ] Can list tools from at least one managed MCP server via `DatabricksMCPClient`
- [ ] Understand which of the four managed servers applies to your use case
- [ ] External MCP connections installed (if needed) and visible in Agents > MCP Servers
- [ ] Resource grant requirements identified for your agent's tools
- [ ] Custom retriever schema declared (if using a custom retriever)

## Next Step

After passing this gate, proceed to your track's tool wiring step:

- **Track A:** [A3: Agent SDK Tool Wiring](../../tracks/A-custom-agent-apps/03-tools-and-mcp/SKILL.md)
- **Track B:** Upstream [`databricks-agent-bricks`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-agent-bricks) (hosted-tool patterns: Genie, KA, UC functions)
- **Track C:** Upstream [`databricks-model-serving`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-model-serving) (ChatAgent / ResponsesAgent packaging with `resources=[...]`)

## Notes to Carry Forward

| Key | Value |
|-----|-------|
| `mcp_server_urls` | List of managed/external MCP server URLs for your agent |
| `mcp_resources` | Resources from `get_databricks_resources()` |
| `retriever_schema` | Name passed to `set_retriever_schema()` (if applicable) |
| `uc_grants_needed` | UC GRANT statements for deployment |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [F1: MLflow Foundation](../01-mlflow-genai-foundation/SKILL.md) | Prerequisite — MLflow environment |
| [F2: Tracing & UC OTEL](../02-experiment-tracing-and-uc-storage/SKILL.md) | Prerequisite — experiment paths and tracing |
| [A3: Agent SDK Tool Wiring](../../tracks/A-custom-agent-apps/03-tools-and-mcp/SKILL.md) | Track A tool wiring |
| Upstream [`databricks-agent-bricks`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-agent-bricks) | Track B (Supervisor API) tool wiring reference |
| Upstream [`databricks-model-serving`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-model-serving) | Track C (Model Serving) tool wiring reference |
| [S4: Evaluation Runs](../../sdlc/04-evaluation-runs/SKILL.md) | Uses retriever schemas for groundedness/relevance judges |

## References

- [Managed MCP servers](https://docs.databricks.com/aws/en/generative-ai/mcp/managed-mcp)
- [Meta parameters for managed MCP](https://docs.databricks.com/aws/en/generative-ai/mcp/managed-mcp-meta-param)
- [External MCP servers](https://docs.databricks.com/aws/en/generative-ai/mcp/external-mcp)
- [Connect clients to MCP servers](https://docs.databricks.com/aws/en/generative-ai/mcp/connect-external-services)
- [Build a tool for your agent](https://docs.databricks.com/aws/en/generative-ai/agent-framework/build-agent-tool)
- [MCP servers on Databricks](https://docs.databricks.com/aws/en/generative-ai/agent-framework/mcp-server)
- [Author an AI agent](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent)
- [Agent authentication (Apps)](https://docs.databricks.com/aws/en/generative-ai/agent-framework/agent-authentication)
- [Agent authentication (Model Serving)](https://docs.databricks.com/aws/en/generative-ai/agent-framework/agent-authentication-model-serving)
- [Add resources to a Databricks app](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/resources)
- [databricks-mcp on PyPI](https://pypi.org/project/databricks-mcp/)
- [OpenAI Agents SDK — MCP](https://openai.github.io/openai-agents-python/mcp/)
- [Code interpreter tools (`python_exec`)](https://docs.databricks.com/aws/en/generative-ai/agent-framework/code-interpreter-tools)
- [Connect agents to external services (non-MCP)](https://docs.databricks.com/aws/en/generative-ai/agent-framework/external-connection-tools)
- [Custom retriever schemas](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent#custom-retriever-schemas)
- [Evaluation sets](https://docs.databricks.com/aws/en/generative-ai/agent-evaluation/evaluation-set)
- [AI Gateway for serving endpoints](https://docs.databricks.com/aws/en/ai-gateway/overview-serving-endpoints)
- [DASF v3.0 — Agentic AI Security](https://www.databricks.com/blog/agentic-ai-security-new-risks-and-controls-databricks-ai-security-framework-dasf-v30)
- [OpenAI Agents SDK — Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [Microsoft Presidio](https://microsoft.github.io/presidio/)
- [Tavily Python SDK](https://docs.tavily.com/docs/python-sdk/tavily-search)
- [Brave Search API](https://brave.com/search/api/)

### Reference files (this skill)

| File | Content |
|------|---------|
| [`references/managed-mcp-servers.md`](references/managed-mcp-servers.md) | All 4 server types, `DatabricksMCPClient` examples, `_meta` parameters, polling |
| [`references/external-mcp-connections.md`](references/external-mcp-connections.md) | 4 installation methods, proxy URLs, auth types, AI Playground testing |
| [`references/resource-grants.md`](references/resource-grants.md) | Grant matrix, `app.yaml`/`databricks.yml`, UC SQL, MLflow `resources`, auto-discovery |
| [`references/custom-retriever-schemas.md`](references/custom-retriever-schemas.md) | `set_retriever_schema()`, RETRIEVER spans, AI Bridge, `doc_uri` for eval |
| [`references/tool-cookbook.md`](references/tool-cookbook.md) | Pre-built `@function_tool` templates: web search (Tavily/Brave), SQL execution, file generation, HTTP API calls |
| [`references/runtime-guardrails.md`](references/runtime-guardrails.md) | AI Gateway guardrails, input screening (regex, Presidio, LLM judge), output filtering, OpenAI SDK guardrails, DASF v3.0 |
| [`references/external-mcp-examples.md`](references/external-mcp-examples.md) | End-to-end walkthroughs: Slack (bearer token), JIRA (Managed OAuth), Brave Search (function_tool + UC proxy) |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.0 | 2026-04-12 | Added tool cookbook (4 recipes), runtime guardrails (AI Gateway + application-level + SDK), and end-to-end external MCP examples (Slack, JIRA, Brave Search). |
| 1.1.0 | 2026-04-12 | Added code interpreter (`system.ai.python_exec`) section and non-MCP external service connections (UC proxy, managed OAuth, UC function `http_request`). Updated grant matrix and references. |
| 1.0.0 | 2026-04-12 | Initial skill: managed MCP (4 servers incl SQL), databricks-mcp library, _meta params, external MCP (4 install methods), resource grants, retriever schemas. Consolidated from A3 references. |
