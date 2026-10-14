---
name: 04-authentication
description: >
  Use when configuring agent permissions, implementing OBO, or granting access
  to Databricks resources. Covers App Authorization (service principal), User
  Authorization (OBO), auth passthrough for Model Serving, and MCP server
  authentication. Track A Step 4.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Agent permissions / OBO / resource grants — config + grants, no bundle resource. Same model on both clients; on Genie Code run grant CLI steps through runDatabricksCli (pre-authenticated). See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "3.0.0"
  domain: "genai-agents"
  pipeline_position: "A4"
  consumes: "agent_class"
  produces: "authenticated_client, resource_permissions"
  grounded_in: "docs.databricks.com/aws/en/generative-ai/agent-framework/agent-authentication, docs.databricks.com/aws/en/generative-ai/agent-framework/agent-authentication-model-serving, docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent"
---

# Agent authentication (Databricks)

Doc-driven skill for how AI agents authenticate on **Databricks Apps** and **Model Serving**. Pair with Track A Step 2 (`agent_class`) when wiring an agent implementation to the right client and grants.

Primary sources:

- [Authentication for AI agents (Databricks Apps)](https://docs.databricks.com/aws/en/generative-ai/agent-framework/agent-authentication)
- [Authentication for AI agents (Model Serving)](https://docs.databricks.com/aws/en/generative-ai/agent-framework/agent-authentication-model-serving)

## When to Use

Use this skill whenever you are:

- Configuring **permissions** for a deployed agent (SP vs user, scopes, resources).
- Implementing **user authorization (OBO)** in agent handlers.
- Declaring **MLflow `resources`** for **automatic authentication passthrough** on Model Serving.
- Supporting **dual deployment** (Apps + Model Serving + local) with one codebase.
- Connecting to **Databricks MCP servers** or **external MCP** from an agent.

**Cross-step impact:** The auth patterns you establish here affect both
Track A evaluation and deployment (A6/A7) and the SDLC pipeline. Environment
detection (local vs Apps vs Model Serving) must work in all three contexts —
especially during [A6: Evaluation](../06-evaluation/SKILL.md) (which runs under
your CLI credentials, not OBO) and
[S6: Deployment & Automation](../../../sdlc/06-deployment-and-automation/SKILL.md)
(which provisions a system SP for production).

## Two authentication methods overview

| Method | Description | When to use |
| --- | --- | --- |
| **App authorization** | Agent uses an **auto-created service principal** with consistent permissions (formerly “SP authentication”). | **Most common.** All users share the same access; shared indexes, shared experiments, uniform behavior. |
| **User authorization** | Agent acts as the **requesting user** (OBO): downscoped token, per-request context. | **Per-user** permissions, **audit trails**, Unity Catalog row filters/column masks, fine-grained UC access. |

You can **combine** both in one agent (for example, app SP for a shared Vector Search index and user client for user-specific tables).

## App authorization (default for Databricks Apps)

- Databricks **automatically creates a service principal** when the app is created; that SP is the app identity.
- **All users** of the app share the **same** permissions granted to that SP.
- Grant the SP access via the **Databricks Apps UI** (Edit app → Configure → resources) or declaratively in **`databricks.yml`** / bundle app resources. See [Apps in bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/resources#app).

### MLflow experiment

The agent needs an MLflow experiment for traces and evaluation. Grant the SP **Can Edit** on that experiment and add it as an app resource. See [Add an MLflow experiment resource](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/mlflow).

### Minimum permissions (common resources)

Align grants with official tables; typical **minimum** expectations for agents:

| Resource | Permission |
| --- | --- |
| MLflow experiment | `Can Edit` |
| SQL warehouse | `Can Use` |
| Model Serving endpoint | `Can Query` |
| Genie space | `Can Run` |
| Vector Search index | `Can Select` |
| Unity Catalog table | `SELECT` (plus `USE SCHEMA` / `USE CATALOG` on parents) |
| Unity Catalog connection | `Use Connection` |
| Unity Catalog volume | `Can Read` or `Can Read and Write` |
| Lakebase | `Can Connect and Create` |

For the complete permission matrix (all resource types, grant methods, dependency chains), see: `references/resource-permissions.md`.

> **Bundle-kind selection:** In `databricks.yml`, warehouses, serving endpoints, and UC connections have their own top-level kinds (`sql_warehouse`, `serving_endpoint`, `connection`). UC functions/tables/schemas/models use the **`uc_securable`** kind with the right `securable_type`. Another Databricks App (e.g. when an AppKit frontend proxies to an Agent App backend) uses the **`app`** kind with `CAN_USE`. See [`03-tools-and-mcp`](../03-tools-and-mcp/SKILL.md#resource-kind-quick-reference) for the full kind-selection table and the `databricks bundle schema` verification command.

For **Model Serving** automatic passthrough, permission names and **minimum MLflow versions** per resource type differ; see the [Model Serving authentication](https://docs.databricks.com/aws/en/generative-ai/agent-framework/agent-authentication-model-serving) page.

**Prompt Registry (UC):** grant **`CREATE FUNCTION`**, **`EXECUTE`**, and **`MANAGE`** on the UC **schema** used to store prompts.

**Downstream dependencies:** If you grant access to a composite resource (for example a **Genie space**), you must also grant access to **dependent** objects (underlying tables, warehouses, UC functions, etc.). Missing downstream grants surface as **permission denied at runtime**.

**Who can attach resources:** The user adding a resource needs **Can Manage** on **both** the resource and the app (per product docs).

Security hardening: follow [App authorization](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/auth#app-authorization) for least privilege and credential handling.

For complete app authorization patterns (SP permission granting via UI/CLI/SDK, `databricks.yml` declarations, least privilege patterns, audit and rotation), see: `references/app-authorization.md`.

## User authorization (OBO) for Databricks Apps

User authorization is **Public Preview** as of product documentation; workspace admins may need to enable it.

### How it works

1. **Add API scopes** in the app so Databricks knows which APIs the app may call on behalf of users. See [Add scopes to an app](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/auth#add-scopes-to-an-app).
2. Databricks **downscopes** the user's credentials to those scopes.
3. The downscoped token is forwarded via the **`x-forwarded-access-token`** HTTP header.
4. **MLflow Agent Server** stores the token **per request** for use in agent code.

Resources reachable with user authorization (per docs) include SQL warehouses, Genie spaces, files/directories, Model Serving endpoints, Vector Search indexes, UC connections, and UC tables.

### Canonical Databricks Apps user headers

Databricks Apps sets the following canonical headers on every inbound request. Read these directly — there is no JSON-blob "user info" header.

- `x-forwarded-email` — the end user's email (canonical attribute used as MLflow `AssessmentSource.source_id`).
- `x-forwarded-preferred-username` — the user's preferred username (often equals the email).
- `x-forwarded-user` — the user's stable workspace user id.
- `x-forwarded-access-token` — the downscoped OBO token for user-scoped Databricks API calls (only present when the App declares `user_api_scopes`).

`x-forwarded-user-info` is **not** a canonical Databricks Apps header and must not be used. Earlier internal patterns assumed it existed; it does not.

### Pathway-C: outbound `x-app-user-email` from AppKit to the Agent App

When the AppKit App (frontend) is a separate Databricks App from the Agent App (backend) — the 2-Apps / Variant 4 / Pathway-C deployment — the AppKit proxy must set `x-app-user-email` on outbound requests to the Agent App. The agent uses this value as `AssessmentSource.source_id` for MLflow feedback (see [SDLC 04c-end-user-feedback](../../../sdlc/04c-end-user-feedback/SKILL.md)).

**Do not infer originating user identity from the app-to-app OAuth token.** The `Authorization: Bearer` header on the inbound agent request represents the **AppKit App service principal hop** between the two Databricks Apps, not the originating end user. If the agent calls `WorkspaceClient().current_user.me()` on that Bearer, it gets the AppKit SP — not the user — and every assessment will be attributed to the same SP UUID.

Concretely, in the Agent App's `@invoke` / `@stream` handler:

```python
from mlflow.genai import agent_server
import mlflow

@agent_server.invoke
async def handle_invoke(request: dict, http_request) -> dict:
    user_email = http_request.headers.get("x-app-user-email")  # set by AppKit proxy
    # ... run the agent ...
    mlflow.log_feedback(
        trace_id=trace_id,
        name="user_feedback",
        value=is_upvoted,
        source=mlflow.entities.AssessmentSource(
            source_type="HUMAN",
            source_id=user_email,  # NOT the SP from the Bearer
        ),
    )
```

The proxy-side wire-up (TypeScript) lives in [`apps_lakebase/skills/06d-appkit-agent-app-proxy/SKILL.md`](../../../../apps_lakebase/skills/06d-appkit-agent-app-proxy/SKILL.md) under "Header Contract".

### Declare API scopes in `app.yaml` (canonical)

Declare the scopes your agent needs in the App's `app.yaml` under
`user_api_scopes`. The set should be **least privilege** — list only the
APIs the agent actually calls on behalf of the user.

```yaml
# app.yaml — Agent App
command:
  - mlflow
  - genai
  - agent-server
  - serve
  - --module
  - agent

user_api_scopes:
  - serving.serving-endpoints      # call LLM + KA endpoints as the user
  - dashboards.genie                # call Genie spaces as the user
  - sql.statement-execution         # run SQL with user warehouse permissions
  - vectorsearch.vector-search-endpoints  # if using Vector Search
  - catalog.connections             # if calling external MCP via UC connection
```

When a Databricks App declares scopes, the user must consent the first time
they open the app. Token downscoping is enforced by Databricks — your code
just reads `x-forwarded-access-token` from the incoming request.

### Implement in code (Option B canonical)

Import the helper that matches your wrapping pattern:

```python
# Option B (canonical) — module-level @invoke / @stream on Apps:
from databricks_app.utils import get_user_workspace_client

# Option A (legacy) — class-based ResponsesAgent on Model Serving:
# from agent_server.utils import get_user_workspace_client
```

**CRITICAL:** Call **`get_user_workspace_client()` inside the request handler** (`@invoke` / `@stream` for Option B, or `predict` / `predict_stream` for Option A), **not** in `__init__` or app startup. There is **no user context** at startup; initializing early **fails** or uses the wrong identity.

```python
# Option B canonical — receive the http_request, hand it to the helper
from mlflow.genai import agent_server
from databricks_app.utils import get_user_workspace_client

@agent_server.invoke
async def handle_invoke(request: dict, http_request) -> dict:
    ws = get_user_workspace_client(http_request)   # user-scoped
    response = ws.serving_endpoints.query(
        name="my-endpoint",
        messages=request["input"],
    )
    return {"output": response.choices[0].message.content}
```

For scope design and escalation considerations, see [Scope-based security and privilege escalation](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/auth#scope-based).

For complete OBO implementation patterns (full agent class, scope walkthrough, token lifecycle, testing locally vs deployed, combining app + user auth), see: `references/user-authorization.md`.

## Automatic auth passthrough (Model Serving)

For agents **logged and served** on Model Serving, **declare dependencies** at **`mlflow.pyfunc.log_model`** time. Databricks **provisions and rotates short-lived credentials** (M2M OAuth-style) for a **system SP** tied to the model version so the agent can call declared resources—**no manual PAT wiring** for those resources.

Notes from product docs:

- Endpoint **creator** must be able to access all logged resources.
- The system SP for the model version may **not** appear in normal SP listings; it is removed if the model version is removed from the endpoint.
- Log **all downstream** dependencies (same principle as Apps).

Example pattern (trim `resources` to what your agent actually uses):

```python
from mlflow.models.resources import (
    DatabricksServingEndpoint,
    DatabricksVectorSearchIndex,
    DatabricksLakebase,
)

mlflow.pyfunc.log_model(
    python_model="/path/to/agent.py",
    resources=[
        DatabricksServingEndpoint(endpoint_name="my-llm"),
        DatabricksVectorSearchIndex(index_name="prod.docs.index"),
        DatabricksLakebase(database_instance_name="my-lakebase"),
    ],
)
```

See [log agent](https://docs.databricks.com/aws/en/generative-ai/agent-framework/log-agent) and [mlflow.pyfunc.log_model](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.pyfunc.html#mlflow.pyfunc.log_model) for full `resources` types, `AuthPolicy` / OBO on Model Serving, and MLflow version minimums per resource.

For complete Model Serving auth patterns (all resource types, AuthPolicy, system SP lifecycle, version requirements), see: `references/model-serving-auth-passthrough.md`.

## Environment detection for dual deployment

Use environment signals to pick **passthrough resources** vs **Apps OBO** vs **local development**:

```python
import os

if os.environ.get("IS_IN_DB_MODEL_SERVING_ENV"):
    # Model Serving: rely on resources declared at log_model time (and optional OBO policies)
    pass
elif os.environ.get("DATABRICKS_APP_NAME"):
    # Databricks Apps: user auth via Agent Server helper when using OBO
    from agent_server.utils import get_user_workspace_client
    client = get_user_workspace_client()
else:
    # Local / notebook: default workspace client (user or configured auth)
    from databricks.sdk import WorkspaceClient
    client = WorkspaceClient()
```

Treat this as a **pattern**; exact env vars and client construction should match your template and MLflow/Databricks versions.

For complete OBO authentication patterns (environment detection, error handling, token refresh, production learnings), see: `references/obo-authentication.md`.

## MCP server authentication

### Databricks managed MCP

- Declare **all required resources** in **`databricks.yml`** / bundle and in **MLflow `resources`** when applicable.
- Grant the app's **service principal** (app authorization) or **users** (user authorization) access to **every downstream** UC object the MCP paths touch (for example vector indexes and UC functions under the schemas used in MCP URLs).
- Product docs illustrate URL patterns under `/api/2.0/mcp/...`; ensure grants cover **each** index/schema/function namespace your agent uses.
- **Auth header source.** When constructing `MCPServerSse` inside an `@invoke`
  / `@stream` handler, pull the bearer token from the user-scoped client to
  preserve OBO end-to-end:

  ```python
  ws = get_user_workspace_client(http_request)
  ai_search_mcp = MCPServerSse(
      # AI Search (formerly Vector Search); legacy /mcp/vector-search/ prefix still works
      url=f"https://{ws.config.host}/api/2.0/mcp/ai-search/prod/docs/idx",
      headers={"Authorization": f"Bearer {ws.config.token}"},
  )
  ```

  Building MCP clients at module load uses the SP token instead — fine for
  app-authorization, wrong for user-authorization.

For managed MCP, consider **`databricks_mcp.DatabricksMCPClient().get_databricks_resources()`** (from the `databricks-mcp` package) to enumerate dependencies—see [Authentication for AI agents (Model Serving)](https://docs.databricks.com/aws/en/generative-ai/agent-framework/agent-authentication-model-serving).

### External MCP servers

- **Databricks Apps / agents** calling **external** MCP servers typically use **Bearer tokens** or **OAuth client credentials (M2M)** supplied by the external provider, stored and rotated per your platform’s secret management (not PATs for Databricks identity).
- Keep **least privilege**: scope tokens to the MCP server audience only; do not reuse workspace admin tokens for third-party MCP.

## Common mistakes

| Mistake | Impact | Fix |
| --- | --- | --- |
| Initializing OBO / `get_user_workspace_client()` at **startup** or in `__init__` | No user context; **fails** or wrong identity | Initialize **inside** `invoke` / `stream` / `predict` / `predict_stream` |
| Missing **downstream** grants (tables behind Genie, functions behind tools, etc.) | **Permission denied** at runtime | Grant SP or user access to **all** transitive dependencies |
| Using **PATs** where product expects **OAuth** (Apps user auth, passthrough) | **Authentication failures** or unsupported flows | Use **OAuth** / forwarded tokens / declared resources per deployment target |
| Logging only **top-level** resource in `resources=[...]` | Serving validation or runtime access errors | Log **every** Databricks resource the code touches |

## Validation checklist

- [ ] Chosen **app authorization**, **user authorization**, or a **documented combination** for each resource class.
- [ ] SP or user has **minimum** privilege on experiments, warehouses, endpoints, indexes, UC objects, Lakebase, volumes, connections as required.
- [ ] **Downstream** dependencies for Genie, tools, and MCP URLs are granted.
- [ ] OBO: `user_api_scopes` declared in `app.yaml` (least privilege) **or** added via the Apps UI; `get_user_workspace_client(http_request)` is only called inside `@invoke` / `@stream` handlers.
- [ ] Model Serving: **`resources`** (and **`AuthPolicy`** if using OBO) complete at **`log_model`** time.
- [ ] MCP: bundle/`databricks.yml` resources and UC grants align with **every** MCP path used.
- [ ] Dual-env code paths tested in **App**, **serving**, and **local** where applicable.

## Next Step

After passing this gate, **load and execute**
`tracks/A-custom-agent-apps/05-lakebase-memory/SKILL.md` (A5: Lakebase Memory).

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [F1: MLflow Foundation](../../../foundation/01-mlflow-genai-foundation/SKILL.md) | Environment detection patterns from F1 |
| [A3: Tools and MCP](../03-tools-and-mcp/SKILL.md) | Previous step |
| [A5: Lakebase Memory](../05-lakebase-memory/SKILL.md) | Next step |
| [A6: Evaluation](../06-evaluation/SKILL.md) | Auth in evaluation context |
| [S6: Deployment & Automation](../../../sdlc/06-deployment-and-automation/SKILL.md) | SP permissions for production deployment |

## References

- [Authentication for AI agents (Databricks Apps)](https://docs.databricks.com/aws/en/generative-ai/agent-framework/agent-authentication)
- [Authentication for AI agents (Model Serving)](https://docs.databricks.com/aws/en/generative-ai/agent-framework/agent-authentication-model-serving)
- [Author an AI agent and deploy it on Databricks Apps](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent)
- [Configure authorization in a Databricks app](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/auth)
- [Add resources to a Databricks app](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/resources)
- [App authorization (deep dive)](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/auth#app-authorization)
- [Apps in bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/resources#app)
- [MLflow Agent Server](https://mlflow.org/docs/latest/genai/serving/agent-server/)
- [mlflow.pyfunc.log_model](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.pyfunc.html#mlflow.pyfunc.log_model)
