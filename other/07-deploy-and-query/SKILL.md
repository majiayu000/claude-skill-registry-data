---
name: 07-deploy-and-query
description: >
  Use when deploying an agent to Databricks Apps and querying the deployed
  endpoint. Covers databricks apps create, sync, deploy, OAuth token auth,
  PAT limitations, curl and Python SDK query methods, and the redeploy
  workflow. Track A Step 7. Consumes evaluation results from Step 6.
  Produces a running deployed agent on Databricks Apps.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: apps
deploy_verb: apps_deploy
deploy_note: "The Track A deploy step — create/sync/deploy the agent to the Databricks Apps runtime, then query the endpoint via OAuth. On Genie Code run the create/sync/deploy CLI through runDatabricksCli (pre-authenticated); on IDE via the local CLI. The deployed app + endpoint carry the per-user prefix. See `skills/genie-code-environment` for the resolved deploy verbs."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "1.1.0"
  domain: "genai-agents"
  pipeline_position: "A7"
  consumes: "evaluation_results, authenticated_client, agent_with_tools, f2_grants_complete, otel_table_prefix, mlflow_tracing_sql_warehouse_id, app_service_principal_grants, lakebase_endpoint_uri, lakebase_cold_start_retry_policy, lakebase_pool_close_policy"
  produces: "deployed_app, app_url"
  grounded_in: "docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent#step-7-deploy-the-agent-to-databricks-apps, docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent#step-8-query-the-deployed-agent, docs.databricks.com/aws/en/dev-tools/databricks-apps/deploy"
---

# Track A Step 7: Deploy and Query

Deploy your evaluated agent to Databricks Apps and verify it works in
production.

## When to Use

- You have a working, evaluated agent from Steps 1-6.
- You are ready to deploy to Databricks Apps for team/production use.
- You need to query the deployed agent programmatically.

## Relationship to SDLC Deployment

This step does a **first manual deployment** for testing. The SDLC deployment
pipeline ([S5](../../../sdlc/05-logged-model-and-uc-registration/SKILL.md)–[S6](../../../sdlc/06-deployment-and-automation/SKILL.md))
adds model registration in Unity Catalog, champion gating, Databricks Asset
Bundles, and evaluate-then-promote CI/CD automation. Think of A7 as "get it
running" and S6 as "make it production-grade."

| Aspect | A7 (this step) | S6 (SDLC) |
|--------|----------------|-----------|
| **Scope** | First manual deploy | Automated CI/CD pipeline |
| **Method** | `databricks apps deploy` CLI | Databricks Asset Bundles + CI/CD |
| **Gating** | Manual eval check (A6) | Automated eval threshold gate (S4) |
| **Model registry** | None | UC-registered model with champion/challenger |
| **Monitoring** | Manual trace inspection | [S7: Production Monitoring](../../../sdlc/07-production-monitoring/SKILL.md) |

After completing Track A (A1-A7), proceed to the
[SDLC pipeline](../../../sdlc/01-prompt-registry/SKILL.md) to productionize
your agent.

---

## Two Deployment Paths

| Path | When to Use |
|---|---|
| **Workspace UI** | First-time setup, want the guided experience |
| **CLI** | CI/CD, repeat deployments, scripted workflows |

Both produce the same result — a running Databricks App serving your agent.

---

## Path A: Deploy via Workspace UI

1. In your Databricks workspace, click **+ New > App**.
2. Select **Agents > Agent - OpenAI Agents SDK**.
3. Create a new MLflow experiment (e.g., `openai-agents-template`).
4. Complete the setup wizard — the app deploys automatically.
5. Click the **App URL** to open the built-in chat UI.

After creating the app in the UI, download the source to your local machine
for customization:

```bash
# Copy the sync command from the app's page
databricks sync --watch . "/Users/<your-username>/agent-openai-agents-sdk"
```

This is the easiest path for first-time deployment. For subsequent updates,
use the CLI workflow below.

---

## Path B: Deploy via CLI

> **Genie Code:** run the create / sync / deploy CLI through `runDatabricksCli` (pre-authenticated) and be on the app's page; the enhanced CLI build flow is page/CWD-dependent, so the SDK `w.apps.deploy(...)` SNAPSHOT path is the reliable fallback, and verify the deployed app via the OAuth session. See `skills/genie-code-environment` §3–§4, §7.

### Step 7b-1: Create the App

If you cloned the repository locally (not via the Workspace UI), create the
app first:

```bash
databricks apps create agent-openai-agents-sdk
```

Replace `agent-openai-agents-sdk` with your app name. If you already created
the app via the Workspace UI, skip this step.

### Step 7b-2: Sync Files to Workspace

Upload your local project files to the Databricks workspace:

```bash
DATABRICKS_USERNAME=$(databricks current-user me | jq -r .userName)
databricks sync . "/Users/$DATABRICKS_USERNAME/agent-openai-agents-sdk"
```

This copies your project directory to a workspace folder under your user
namespace. The `databricks sync` command uploads all files that are not
excluded by `.gitignore` or `.databricksignore`.

### Step 7b-3: Deploy the App

```bash
databricks apps deploy agent-openai-agents-sdk \
  --source-code-path "/Workspace/Users/$DATABRICKS_USERNAME/agent-openai-agents-sdk"
```

The deploy command:
1. Reads `app.yaml` for compute size and resource declarations
2. Installs dependencies from `pyproject.toml`
3. Starts the agent on the configured compute
4. Makes the app available at `<app-name>.<workspace>.databricksapps.com`

### Step 7b-4: Verify Deployment

```bash
# Check app status
databricks apps get agent-openai-agents-sdk

# Get the app URL
databricks apps get agent-openai-agents-sdk | jq -r .url
```

Open the app URL in a browser — the built-in chat UI should load and respond
to messages.

---

## Redeployment Workflow

When you make code changes, re-sync and redeploy:

```bash
# 1. Sync updated files
databricks sync . "/Users/$DATABRICKS_USERNAME/agent-openai-agents-sdk"

# 2. Redeploy (picks up new files)
databricks apps deploy agent-openai-agents-sdk \
  --source-code-path "/Workspace/Users/$DATABRICKS_USERNAME/agent-openai-agents-sdk"
```

For iterative development, use `--watch` with sync to auto-upload on save:

```bash
databricks sync --watch . "/Users/$DATABRICKS_USERNAME/agent-openai-agents-sdk"
```

Then redeploy when ready to pick up the changes.

---

## Querying the Deployed Agent

### Authentication: OAuth Tokens (PATs Do Not Work)

Databricks Apps require **OAuth tokens** — Personal Access Tokens (PATs)
are **not supported**.

Generate an OAuth token:

```bash
# Authenticate once — IDE/CLI only (see PRE-REQUISITES §11). Genie Code: pre-authenticated, run via runDatabricksCli.

# Get a fresh token
databricks auth token --host https://<workspace>.cloud.databricks.com
```

### Query with curl

```bash
APP_URL="https://agent-openai-agents-sdk.<workspace>.databricksapps.com"
TOKEN=$(databricks auth token --host https://<workspace>.cloud.databricks.com | jq -r .access_token)

# Non-streaming
curl -X POST "$APP_URL/invocations" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "Hello, what can you do?"}]}'

# Streaming
curl -X POST "$APP_URL/invocations" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "Hello"}], "stream": true}'
```

### Query with Python (requests)

```python
import subprocess
import json
import requests

token_output = subprocess.run(
    ["databricks", "auth", "token", "--host", "https://<workspace>.cloud.databricks.com"],
    capture_output=True, text=True
)
token = json.loads(token_output.stdout)["access_token"]

app_url = "https://agent-openai-agents-sdk.<workspace>.databricksapps.com"

response = requests.post(
    f"{app_url}/invocations",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    },
    json={
        "input": [{"role": "user", "content": "What can you help me with?"}],
    },
)

print(response.json())
```

### Query with the Databricks OpenAI Client

For the most ergonomic Python experience, use the OpenAI-compatible client:

```python
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
openai_client = w.serving_endpoints.get_open_ai_client()

response = openai_client.responses.create(
    model="agent-openai-agents-sdk",
    input=[{"role": "user", "content": "Hello"}],
)
print(response.output_text)
```

For the full list of query methods, see
[Query an agent deployed on Databricks](https://docs.databricks.com/aws/en/generative-ai/agent-framework/query-agent).

---

## Sending custom_inputs to Deployed Agents

```bash
curl -X POST "$APP_URL/invocations" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "input": [{"role": "user", "content": "What were Q3 sales?"}],
    "custom_inputs": {"user_id": "analyst@acme.com", "session_id": "s-123"}
  }'
```

See `02-agent-framework/references/custom-inputs-outputs.md` for the full
`custom_inputs` / `custom_outputs` pattern.

---

## Pre-deploy: verify F2 grants and Lakebase policies

A7 is the **consumer** of two upstream contracts; it does not derive
either at deploy time.

### F2 (`02-experiment-tracing-and-uc-storage`) state must be present

Before running `databricks apps deploy`, verify the four F2 fields are
captured in state and `f2_grants_complete` is `true`. The deploy script
should fail closed if any of these are missing:

```python
state = load_state()
assert state["f2_grants_complete"] is True, (
    "Refusing to deploy: f2_grants_complete is not true. "
    "Run F2 (foundation/02-experiment-tracing-and-uc-storage) and apply the "
    "MODIFY+SELECT grants on every *_otel_* table to the app SP, then capture "
    "app_service_principal_grants[] before retrying."
)
assert state.get("otel_table_prefix"), "Missing otel_table_prefix (F2-owned)"
assert state.get("mlflow_tracing_sql_warehouse_id"), (
    "Missing mlflow_tracing_sql_warehouse_id — preflight_check_registry."
    "mlflow_tracing_sql_warehouse_id_present blocks deploy."
)
```

### Lakebase policies (if the agent uses Lakebase memory) must be present

If the agent uses Lakebase memory (Track A 05 / `agent-openai-advanced`),
A2 (`02-agent-framework`) must have captured the Lakebase client policy
in state:

```python
if state.get("uses_lakebase"):
    assert state.get("lakebase_endpoint_uri")
    policy = state.get("lakebase_cold_start_retry_policy") or {}
    assert "AdminShutdown" in policy.get("retry_on", [])
    assert "psycopg_pool.PoolClosed" in policy.get("retry_on", [])
    assert policy.get("max_attempts", 0) >= 1, (
        "preflight_check_registry.lakebase_cold_start_retry_policy_present "
        "fails — set max_attempts >= 1 in A2 before deploy."
    )
    assert state.get("lakebase_pool_close_policy")
```

The deploy script also greps the agent module for forbidden module-level
Lakebase init:

```bash
# fail closed if the agent opens a Lakebase pool at import time
if grep -nE '^[^#].*AsyncConnectionPool\(.*open=True' agent.py >/dev/null; then
  echo "Refusing to deploy: Lakebase pool opened at module import. Move into handle_invoke/handle_stream."
  exit 1
fi
```

---

## Production tracing checklist

Track A deploys agents as **Databricks Apps**, so the **Agent Framework
auto-tracing** path applies — but the canonical env-var matrix and the
**Git-folder caveat** are the same as for custom serving and apply
here too.

Before declaring the deploy "done":

- [ ] Experiment is in a **non-Git** path. Move it to `/Shared/...` if it
      currently lives under a Databricks Git folder, or trace ingestion
      will silently drop.
- [ ] `mlflow.set_experiment(...)` to that non-Git path is called
      **before** deploy.
- [ ] App service principal has **`CAN_EDIT`** on the experiment
      (Experiment → Permissions). Without it, traces 403 on first
      request.
- [ ] `MLFLOW_EXPERIMENT_ID` set in `app.yaml` (or `databricks.yml` env)
      so the deployed runtime knows where to write.
- [ ] Send one production request after deploy and confirm a trace
      appears in the **MLflow Experiment UI** (with token counts and
      `gen_ai.*` attrs if `mlflow.openai.autolog()` is enabled at module
      level).
- [ ] (UC OTEL) `MLFLOW_TRACING_SQL_WAREHOUSE_ID` set so traces also
      land in Delta tables for SQL querying.

For the full env-var matrix, the Git-folder caveat in detail, the
custom-CPU-serving variant, and the Production-Monitoring-to-Delta
pattern, see the canonical reference:

- [`foundation/02-experiment-tracing-and-uc-storage/references/prod-tracing-deployment.md`](../../../foundation/02-experiment-tracing-and-uc-storage/references/prod-tracing-deployment.md)

---

## DO / DON'T

### DO — Evaluate before every deploy

```bash
uv run agent-evaluate   # Step 6
# Only if evaluation passes:
databricks sync . "/Users/$DATABRICKS_USERNAME/agent-openai-agents-sdk"
databricks apps deploy agent-openai-agents-sdk --source-code-path ...
```

### DON'T — Deploy without syncing first

```bash
# Missing sync — deploys stale code!
databricks apps deploy agent-openai-agents-sdk --source-code-path ...
```

### DO — Use OAuth tokens for Apps

```bash
TOKEN=$(databricks auth token --host ... | jq -r .access_token)
curl -H "Authorization: Bearer $TOKEN" "$APP_URL/invocations" ...
```

### DON'T — Use Personal Access Tokens (PATs)

```bash
# PATs are NOT supported for Databricks Apps — this will fail
curl -H "Authorization: Bearer dapi..." "$APP_URL/invocations" ...
```

### DO — Check app status after deploy

```bash
databricks apps get agent-openai-agents-sdk
# Verify state is RUNNING
```

### DON'T — Assume deploy succeeded without checking

App deployment can fail silently due to missing resources, compute limits,
or dependency issues.

---

## Common Issues

| Issue | Fix |
|-------|-----|
| `403 Forbidden` on query | Using a PAT instead of OAuth token; run `databricks auth token` |
| App stuck in `STARTING` | Check compute size — only medium and large are supported |
| Deploy fails: missing resource | Ensure all resources in `app.yaml` exist and are accessible |
| `sync` uploads too many files | Add entries to `.gitignore` or `.databricksignore` |
| App URL returns 502 | App is restarting; wait 1-2 minutes after deploy |
| Changes not reflected | Re-run `databricks sync` then `databricks apps deploy` |

---

## Limitations

- Only **medium and large** compute sizes are supported for Databricks Apps.
  See [Configure compute resources](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/compute-size).
- The MLflow Review App Chat UI does not currently support agents deployed on
  Databricks Apps. Use [labeling sessions](https://docs.databricks.com/aws/en/mlflow3/genai/human-feedback/expert-feedback/label-existing-traces)
  for trace evaluation instead.

---

## Validation Gate

Deployment verifies the configured model route, not a specific provider. The core Track A path requires `provider: databricks` and does not require AI Gateway. If `provider: ai_gateway` appears, treat it as pre-provisioned configuration and verify queryability; do not create or configure Gateway here.

All must pass before proceeding to debugging:

- [ ] **Pre-deploy:** `f2_grants_complete: true` in state (F2 contract); `otel_table_prefix`, `mlflow_tracing_sql_warehouse_id`, `app_service_principal_grants[]` all present
- [ ] **Pre-deploy (if Lakebase):** `lakebase_endpoint_uri`, `lakebase_cold_start_retry_policy` (with canonical `retry_on` classes + `max_attempts >= 1`), `lakebase_pool_close_policy` all captured by A2; agent module has no module-level Lakebase init
- [ ] App deployed and accessible at its URL
- [ ] Chat UI loads and accepts messages
- [ ] Agent responds correctly to test queries via the deployed URL
- [ ] OAuth token authentication works (`databricks auth token`)
- [ ] Programmatic query via curl or Python SDK succeeds
- [ ] Traces from the deployed app appear in the MLflow experiment
- [ ] App resources (MLflow experiment, warehouse, etc.) are properly granted

## Next Step

After passing this gate, choose one of:

- **Continue Track A** — load and execute `tracks/A-custom-agent-apps/08-debugging/SKILL.md` (A8: Debugging) to learn systematic debugging for deployed agents.
- **Wire an AppKit frontend (Variant 4 canonical)** — if you are on the canonical 2-Apps path, proceed to [`apps_lakebase/skills/06d-appkit-agent-app-proxy`](../../../../apps_lakebase/skills/06d-appkit-agent-app-proxy/SKILL.md) to wire an AppKit dashboard to this Agent App with OBO forwarding. That skill reads `agent_app_url` and `agent_app_name` from state — populate both before invoking it (see "Carry forward" below).

**Carry forward** these values into subsequent steps:

| Key | Value |
|-----|-------|
| `predict_fn` | From A5 — `Runner.run_sync(agent, question).final_output` |
| `agent_app_name` | Databricks App name (alias of `app_name`; used by `06d` and walkthrough state schema) |
| `agent_app_url` | Deployed Agent App URL (alias of `app_url`; the full `https://...databricksapps.com` string used as `AGENT_APP_URL` by `06d`) |
| `app_name` | (legacy alias) — same as `agent_app_name` |
| `app_url` | (legacy alias) — same as `agent_app_url` |
| `workspace_path` | Workspace path for synced files |
| `deploy_command` | Full `databricks apps deploy` command used |
| `eval_dataset` | Path to evaluation dataset from A6 |
| `eval_results` | Baseline metrics from A6 |
| `auth_method` | SP + OBO (from A4) |
| `tracing_source` | `mlflow.openai.autolog()` (from A2) |

> **Canonical state-variable names:** The workshop walkthrough schema (Variant 4) uses `agent_app_url` and `agent_app_name`. The legacy `app_url` / `app_name` keys continue to work for backward compatibility, but new state captures SHOULD prefer the canonical names so downstream skills (`06d-appkit-agent-app-proxy`) and the AppKit wiring walkthrough pick them up without aliasing.

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [A6: Evaluation](../06-evaluation/SKILL.md) | Previous step |
| [A8: Debugging](../08-debugging/SKILL.md) | Next step |
| [S1: Prompt Registry](../../../sdlc/01-prompt-registry/SKILL.md) | SDLC entry point after Track A completes |
| [S6: Deployment & Automation](../../../sdlc/06-deployment-and-automation/SKILL.md) | SDLC: DAB bundles and CI/CD pipeline |

## References

- [Author an agent — Deploy to Databricks Apps](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent#step-7-deploy-the-agent-to-databricks-apps)
- [Author an agent — Query the deployed agent](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent#step-8-query-the-deployed-agent)
- [Query an agent deployed on Databricks](https://docs.databricks.com/aws/en/generative-ai/agent-framework/query-agent)
- [Deploy a Databricks App](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/deploy)
- [Configure compute resources for Apps](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/compute-size)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-04-26 | Added "Pre-deploy: verify F2 grants and Lakebase policies" section. A7 now consumes (does not derive) the F2 OTel contract (`f2_grants_complete`, `otel_table_prefix`, `mlflow_tracing_sql_warehouse_id`, `app_service_principal_grants[]`) and the A2 Lakebase client policy (`lakebase_endpoint_uri`, `lakebase_cold_start_retry_policy`, `lakebase_pool_close_policy`) before invoking `databricks apps deploy`. Validation gate fails closed when any contract is missing. Added grep guard against module-level `AsyncConnectionPool(...)` in `agent.py`. |
| 1.0.0 | 2026-04-11 | Initial skill: UI + CLI deploy paths, OAuth auth, query methods, redeploy workflow |
