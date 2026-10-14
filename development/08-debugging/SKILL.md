---
name: 08-debugging
description: >
  Use when a deployed Databricks Apps agent is failing, returning errors, or
  behaving unexpectedly. Covers systematic debugging of local dev, bundle
  configuration, deployment, runtime errors, authentication, resource
  permissions, and Lakebase memory. Track A Step 8. Consumes a deployed app
  from Step 7. Produces a resolved, healthy agent deployment.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: none
deploy_note: "Debugging workflow for a deployed Apps agent — no deployed resource. On Genie Code inspect logs/state via the workspace + runDatabricksCli (pre-authenticated); the local-dev-server portion is the IDE/local branch. See `skills/genie-code-environment`."
coverage: full
metadata:
  last_verified: "2026-04-15"
  volatility: medium
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "1.0.0"
  domain: "genai-agents"
  pipeline_position: "A8"
  consumes: "deployed_app, app_url"
  produces: "debugging_runbook, resolved_issues"
  grounded_in: "docs.databricks.com/aws/en/generative-ai/agent-framework/debug-agent"
fields_read:
  - governance.scorer_suite.primary_scorer
---

# Track A Step 8: Debugging Deployed Agents

Systematically diagnose and resolve issues with agents deployed to
Databricks Apps.

> **Source documentation:**
> This skill is grounded in [Debug a deployed AI agent](https://docs.databricks.com/aws/en/generative-ai/agent-framework/debug-agent)
> (Databricks docs). The source page covers Apps **and** Model Serving
> debugging and is updated as the platform evolves. **If a command, API, or
> error message in this skill does not match what you see, consult the source
> page first** — it is the canonical reference. Related pages:
> [Deploy a Databricks App](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/deploy),
> [Add resources to a Databricks app](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/resources).

## When to Use

- Your deployed app returns errors, 302 redirects, or 502s.
- The agent responds but ignores tools, hallucinates, or drops context.
- Resource permission errors appear in logs.
- Lakebase memory is not persisting across conversations.
- You need to validate configuration before a deploy.
- Local dev server (`uv run start-app`) is failing.

---

## Best Practices

Follow these before you start debugging — they prevent most issues:

1. **Enable MLflow tracing.** `mlflow.openai.autolog()` at module level
   (configured in A2). Traces are the single most useful diagnostic tool.
2. **Document tools clearly.** Clear tool and parameter descriptions ensure
   the LLM calls tools correctly. See A3 for `@function_tool` docstring
   patterns.
3. **Add timeouts and token limits to LLM calls.** Prevents delays from
   long-running steps. If your agent uses the OpenAI client to query a
   Databricks serving endpoint, set custom timeouts on the calls.
4. **Validate configuration before deployment.** Run
   `databricks bundle validate` before `databricks bundle deploy` to catch
   YAML issues early.
5. **Test locally first.** Use `uv run start-app` to catch issues before
   deploying. Send test requests, verify traces appear in MLflow, then deploy.

---

## Debug Local Development

Before deploying, verify your local environment is configured correctly.

### Environment checklist

```bash
# 1. Check Databricks CLI version (need 0.283.0+)
databricks -v

# 2. Verify authentication profiles
databricks auth profiles

# 3. Verify .env contains MLFLOW_TRACKING_URI in correct format
grep MLFLOW_TRACKING_URI .env
# Must be: databricks://PROFILE_NAME (not a URL)
```

### Common local development errors

| Error | Cause | Fix |
|-------|-------|-----|
| `The provided MLFLOW_EXPERIMENT_ID does not exist` | Wrong tracking URI format or experiment deleted | Verify `MLFLOW_TRACKING_URI` uses `databricks://PROFILE_NAME` format |
| `ModuleNotFoundError` on start | Dependencies not installed | Run `uv sync` to install dependencies |
| Port 8000 already in use | Another process on the port | `lsof -ti:8000 | xargs kill` or use `uv run start-app --port 8001` |
| Authentication errors locally | Environment not configured | Run `uv run quickstart` or manually configure `.env` |

### Test the agent locally

```bash
# Terminal 1: Start the agent server
uv run start-app

# Terminal 2: Send a test request
curl -X POST http://localhost:8000/invocations \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "hello"}]}'
```

View MLflow traces in the Databricks UI to verify your agent is logging
traces correctly. If the server starts but returns no useful reply, check:

1. The server terminal for tracebacks or HTTP errors.
2. `.env` is populated — compare keys with `.env.example`.
3. `databricks auth token` succeeds for the profile quickstart used.

---

## Debug Configuration

Configuration errors in `databricks.yml` and `app.yaml` are the most common
source of deployment failures.

### Validate before deploying

> **Client note:** IDE runs this in a terminal; Genie Code runs the `databricks bundle …` command via `runDatabricksCli` (be on the bundle's page). See `skills/genie-code-environment`.

```bash
databricks bundle validate
```

This catches YAML syntax errors, missing required fields, invalid resource
references, and permission configuration issues.

### Common configuration mismatches

| Configuration Point | Rule | How to Debug |
|---------------------|------|-------------|
| `valueFrom` references in `app.yaml` | Must exactly match a resource name in `databricks.yml` | Search for the exact string in both files |
| App name | Must start with `agent-` prefix | Check the `name` field under `resources.apps` in `databricks.yml` |
| Genie space ID | Must be the 32-character hex string from the URL | Extract from `https://...cloud.databricks.com/genie/rooms/{SPACE_ID}` |
| Unity Catalog function reference | Must use `catalog.schema.function_name` format | Verify with `databricks unity-catalog functions list` |
| Lakebase instance reference | Must use `value` (not `valueFrom`) in `app.yaml` | The instance name is a literal string, not a resource reference |

### Example: Spotting a valueFrom mismatch

```yaml
# app.yaml
env:
  - name: SQL_WAREHOUSE_ID
    valueFrom: sql-warehouse  # <-- Must match name below

# databricks.yml
resources:
  apps:
    my_agent:
      resources:
        - name: sql-warehouse           # <-- This must match
          sql_warehouse:
            id: "abc123"
            permission: CAN_USE
```

If `valueFrom` says `sql_warehouse` but the resource name is `sql-warehouse`,
deployment silently fails to inject the environment variable.

---

## Debug Deployment

### App already exists error

If you see `Error: failed to create app - An app with the same name already exists`:

**Option 1: Bind to the existing app (recommended)**

```bash
databricks apps get <app-name> --output json
databricks bundle deployment bind <bundle-name> <app-name> --auto-approve
databricks bundle deploy
databricks bundle run <bundle-name>
```

**Option 2: Delete and recreate**

```bash
databricks apps delete <app-name>
databricks bundle deploy
databricks bundle run <bundle-name>
```

### App not updating after deploy

`databricks bundle deploy` only uploads files to the workspace. You must
also run `databricks bundle run <bundle-name>` to restart the app with the
new code. Always deploy using both commands:

```bash
databricks bundle deploy && databricks bundle run <bundle-name>
```

### View deployment status and logs

```bash
# Check app status
databricks apps get <app-name>

# View real-time logs
databricks apps logs <app-name> --follow
```

Look for stack traces, permission denied messages, connection errors, and
timeout messages in the log output.

---

## Debug Runtime Errors

### Analyze app logs

```bash
databricks apps logs <app-name> --follow
```

Look for:
- Stack traces indicating code errors
- `Permission denied` messages for resources
- Connection errors to external services (MCP servers, serving endpoints)
- Timeout messages

### Common runtime errors

| Error | Cause | Fix |
|-------|-------|-----|
| 302 redirect when querying app | Using a PAT instead of OAuth | Get an OAuth token with `databricks auth token` |
| Agent not using available tools | Tools not returned from MCP client | Verify the MCP server URL is correct and the resource has proper permissions in `databricks.yml` |
| Streaming response breaks mid-response | Connection timeout | Increase `CHAT_PROXY_TIMEOUT_SECONDS` in `app.yaml` env section |
| Agent returning "Memory not available" | Missing `user_id` in request | Pass `custom_inputs.user_id` in the request payload |
| Empty or error responses despite 200 status | Error within streamed response | Check the actual stream content and app logs, not just the HTTP status code |

### Use MLflow traces for diagnosis

When the agent responds but incorrectly, MLflow traces are the primary
diagnostic tool:

1. Open your MLflow experiment in the Databricks UI.
2. Find the trace for the failing request.
3. Inspect each span (AGENT, LLM, TOOL) for:
   - **LLM spans**: Was the prompt correct? Did the model receive the right
     context?
   - **TOOL spans**: Did the tool receive the right arguments? Did it return
     the expected result? Did it error?
   - **AGENT spans**: Did the orchestration route correctly?

---

## Debug Authentication

### OAuth token requirement

Databricks Apps require OAuth tokens. Personal Access Tokens (PATs) result
in a 302 redirect.

```bash
# Get an OAuth token
databricks auth token

# Use it in requests
TOKEN=$(databricks auth token | jq -r '.access_token')
curl -X POST <app-url>/invocations \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "hello"}]}'
```

### Resource permission errors

When the agent cannot access workspace resources, verify the resource is
configured in `databricks.yml`. Each resource type requires specific
permissions:

| Error | Cause | Fix |
|-------|-------|-----|
| Permission denied on Genie space | Missing `genie_space` resource | Add `genie_space` with `permission: 'CAN_RUN'` |
| Vector search index not accessible | Missing `uc_securable` for the index | Add `uc_securable` with `securable_type: 'TABLE'`, `permission: 'SELECT'` |
| UC function execution denied | Missing `uc_securable` for the function | Add `uc_securable` with `securable_type: 'FUNCTION'`, `permission: 'EXECUTE'` |
| Serving endpoint access denied | Missing `serving_endpoint` resource | Add `serving_endpoint` with `permission: 'CAN_QUERY'` |
| SQL warehouse access denied | Missing `sql_warehouse` resource | Add `sql_warehouse` with `permission: 'CAN_USE'` |

Example resource configuration in `databricks.yml`:

```yaml
resources:
  apps:
    my_agent:
      name: 'agent-my-app'
      resources:
        - name: 'my_genie_space'
          genie_space:
            space_id: '01234567890abcdef01234567890abcd'
            permission: 'CAN_RUN'
        - name: 'my_vector_index'
          uc_securable:
            securable_full_name: 'catalog.schema.index_name'
            securable_type: 'TABLE'
            permission: 'SELECT'
```

### Custom MCP server permissions

If your agent connects to a custom MCP server running as a Databricks app,
grant permissions manually (apps are not yet supported as resource
dependencies in `databricks.yml`):

```bash
# Get your agent app's service principal
AGENT_SP=$(databricks apps get <agent-app-name> --output json | jq -r '.service_principal_name')

# Grant permission on the MCP server app
databricks apps update-permissions <mcp-server-app-name> \
  --json "{\"access_control_list\": [{\"service_principal_name\": \"$AGENT_SP\", \"permission_level\": \"CAN_USE\"}]}"
```

---

## Debug Lakebase Memory

For agents using Lakebase for memory storage (configured in A5):

| Error | Cause | Fix |
|-------|-------|-----|
| `relation 'store' does not exist` | Memory tables not initialized | Run `await store.setup()` locally before deploying |
| `Unable to resolve :re[LKB] instance` | Wrong instance name or configuration | Verify `LAKEBASE_INSTANCE_NAME` uses `value` (not `valueFrom`) in `app.yaml` and matches the `instance_name` in `databricks.yml` |
| `permission denied for table store` | Missing Lakebase permissions | Add a `database` resource in `databricks.yml` with `permission: 'CAN_CONNECT_AND_CREATE'` |
| Memory not persisting across conversations | Different `user_id` per request | Pass a consistent `user_id` in `custom_inputs` for each user |

### Initialize tables before deploying

```python
import asyncio
from databricks_langchain import AsyncDatabricksStore

async def setup_memory():
    async with AsyncDatabricksStore(
        instance_name='your-lakebase-instance',
        embedding_endpoint='databricks-gte-large-en',
        embedding_dims=1024,
    ) as store:
        await store.setup()

asyncio.run(setup_memory())
```

### Lakebase resource configuration

```yaml
resources:
  apps:
    my_agent:
      resources:
        - name: 'memory_database'
          database:
            instance_name: '<lakebase-instance-name>'
            database_name: 'postgres'
            permission: 'CAN_CONNECT_AND_CREATE'
```

---

## Agent-as-Judge Debugging

When an agent misbehaves on specific traces, raw span-tree inspection is slow. **Agent-as-judge** uses an LLM judge to read a trace and explain — in natural language — *why* it failed against your guidelines. This is faster than eyeballing 30 spans and often surfaces root causes humans miss.

### When to reach for agent-as-judge

- You have ≥ 5 failing production traces in `*_otel_traces` but can't see a pattern.
- A scorer is firing below threshold and you can't tell which span caused it.
- A user complaint points to a specific `request_id` and you need a fast triage narrative.
- You want to auto-generate "debug notes" for every failing CI eval row.

Don't use when:

- You already know the failure is a tool error (check the span status directly).
- You have < 3 failing rows — read them by hand.

### Using `make_judge` for trace-level failure analysis

```python
from mlflow.genai import make_judge
import mlflow

failure_judge = make_judge(
    name="agent_failure_root_cause",
    instructions=(
        "Read the trace. Identify the FIRST step where the agent deviated from the "
        "expected behavior per SkyLoyalty policies. Answer in this structured form:\n"
        "  * Failure step: <name of the span or tool call>\n"
        "  * Root cause: <one sentence>\n"
        "  * Evidence: <quote 1-2 lines from the span>\n"
        "  * Recommended fix: <one action>\n"
        "If the trace succeeded, respond only with 'OK'."
    ),
    model="databricks:/databricks-claude-sonnet-4-6",
)

trace = mlflow.get_trace("<request_id>")
feedback = failure_judge(trace=trace)
print(feedback.value)      # 'OK' or the structured diagnosis
print(feedback.rationale)  # Model's full reasoning
```

`make_judge` accepts a `trace` argument — the judge reads span names, inputs, outputs, and attributes directly. No manual extraction needed.

### Batching across failing traces

Run the judge against the failing subset from [07-production-monitoring](../../../sdlc/07-production-monitoring/SKILL.md) and cluster the diagnoses:

```python
from databricks.sdk import WorkspaceClient
import mlflow
import collections

w = WorkspaceClient()

failing_ids = w.sql.query("""
  SELECT DISTINCT request_id
  FROM main.skyloyalty_ops.skyloyalty_agent_otel_annotations
  WHERE assessment_name = 'source_citation_scorer' AND value < 0.7
    AND timestamp > current_timestamp() - INTERVAL 7 DAYS
""")

root_causes = collections.Counter()
for row in failing_ids:
    trace = mlflow.get_trace(row["request_id"])
    fb = failure_judge(trace=trace)
    if fb.value != "OK":
        # Extract "Root cause:" line for clustering
        for line in fb.value.splitlines():
            if line.strip().lower().startswith("root cause:"):
                root_causes[line.strip()] += 1
                break

print("Top failure modes:")
for cause, n in root_causes.most_common(5):
    print(f"  {n:3d}  {cause}")
```

The top 5 root causes become your next prompt-optimization, scorer, or tool-fix candidates.

### Caveats when using UC OTEL traces with MLflow's own MCP

If you attempt to use a general-purpose MLflow MCP server to load UC OTEL traces, note:

- UC OTEL traces (`*_otel_traces` tables) have a different schema than the legacy trace archival format.
- `mlflow.get_trace(request_id)` works with UC OTEL out of the box — **prefer it** over custom SQL extraction.
- If you pre-extract spans via SQL, include `span_attributes` column (JSON) — it carries the `gen_ai.*` fields the judge uses for reasoning.

### Writing diagnoses back to the trace

Add the judge's diagnosis as a human-readable assessment on the trace so it shows up in the MLflow UI for future investigators:

```python
import mlflow

with mlflow.start_run() as run:
    mlflow.log_feedback(
        trace_id=row["request_id"],
        name="agent_failure_root_cause",
        value=fb.value,
        rationale=fb.rationale,
        source_type="AGENT_JUDGE",
    )
```

Now the trace detail page shows "Root cause: tool returned stale price list" — every investigator starts with context.

---

## DO / DON'T

### DO — Validate configuration before every deploy

```bash
databricks bundle validate
databricks bundle deploy && databricks bundle run <bundle-name>
```

### DON'T — Deploy without running the app afterward

```bash
# Uploads files but does NOT restart the app
databricks bundle deploy
# Must also run:
databricks bundle run <bundle-name>
```

### DO — Use OAuth tokens for Apps

```bash
TOKEN=$(databricks auth token | jq -r '.access_token')
curl -H "Authorization: Bearer $TOKEN" "$APP_URL/invocations" ...
```

### DON'T — Use PATs for Databricks Apps

```bash
# PATs cause 302 redirects — this will fail
curl -H "Authorization: Bearer dapi..." "$APP_URL/invocations" ...
```

### DO — Check app logs when something fails

```bash
databricks apps logs <app-name> --follow
```

### DON'T — Assume a 200 status means success with streaming

Streamed responses can return 200 but contain errors in the stream body.
Always inspect the actual response content.

### DO — Initialize Lakebase tables before first deploy

```python
await store.setup()
```

### DON'T — Use `valueFrom` for Lakebase instance names

```yaml
# WRONG: valueFrom is for resource references
- name: LAKEBASE_INSTANCE_NAME
  valueFrom: my-lakebase

# CORRECT: value is for literal strings
- name: LAKEBASE_INSTANCE_NAME
  value: my-lakebase
```

---

## Common Issues

| Issue | Fix |
|-------|-----|
| `403 Forbidden` on query | Using a PAT instead of OAuth; run `databricks auth token` |
| App stuck in `STARTING` | Check compute size — only medium and large are supported |
| Deploy fails: missing resource | Ensure all resources in `app.yaml` exist and are accessible |
| `sync` uploads too many files | Add entries to `.gitignore` or `.databricksignore` |
| App URL returns 502 | App is restarting; wait 1-2 minutes after deploy |
| Changes not reflected | Re-run `databricks sync` then `databricks apps deploy`, or use `databricks bundle deploy && databricks bundle run` |
| App already exists | Bind to existing: `databricks bundle deployment bind` or delete and recreate |
| `MLFLOW_EXPERIMENT_ID does not exist` | Verify `MLFLOW_TRACKING_URI` uses `databricks://PROFILE_NAME` format |
| `ModuleNotFoundError` on start | Run `uv sync` to install dependencies |
| Port already in use | `lsof -ti:8000 | xargs kill` or use `--port 8001` |
| MCP server connection refused | Check MCP URL format, auth headers, and that the endpoint exists |
| Agent ignores tool results | Tool return type may be too complex; simplify to `str` or flat `dict` |

---

## Validation Gate

All must pass — confirms debugging knowledge before entering the SDLC
pipeline:

- [ ] `databricks bundle validate` runs without errors
- [ ] `databricks apps logs <app-name>` shows no unresolved errors
- [ ] OAuth token authentication works (`databricks auth token`)
- [ ] All resource permissions verified (Genie, Vector Search, UC Functions, SQL Warehouse)
- [ ] Lakebase memory tables initialized (if applicable)
- [ ] MLflow traces accessible and showing correct span structure
- [ ] Agent responds correctly to test queries via the deployed URL

## Next Step: Enter the SDLC Pipeline

Track A is complete. Your agent is built, tested, deployed, and you know
how to debug it. Now productionize it with the SDLC pipeline.

**Load and execute** `sdlc/01-prompt-registry/SKILL.md` (S1: Prompt Registry)
to begin the SDLC pipeline. The full SDLC sequence is:

1. **S1** `sdlc/01-prompt-registry/SKILL.md` — register prompts in UC with versioned aliases
2. **S2** `sdlc/02-evaluation-datasets/SKILL.md` — build comprehensive benchmark dataset
3. **S3** `sdlc/03-scorers-and-judges/SKILL.md` — create scorers with threshold gates
4. **S4** `sdlc/04-evaluation-runs/SKILL.md` — run `mlflow.genai.evaluate()` with your `predict_fn`
5. **S5** `sdlc/05-logged-model-and-uc-registration/SKILL.md` — register model in UC
6. **S6** `sdlc/06-deployment-and-automation/SKILL.md` — set up DAB bundles and CI/CD
7. **S7** `sdlc/07-production-monitoring/SKILL.md` — register production scorers and monitoring

**Carry forward** the same values from A7 into the SDLC pipeline.

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [A7: Deploy and Query](../07-deploy-and-query/SKILL.md) | Previous step — produces deployed app |
| [A4: Authentication](../04-authentication/SKILL.md) | Auth patterns referenced in debugging |
| [A5: Lakebase Memory](../05-lakebase-memory/SKILL.md) | Memory patterns referenced in Lakebase debugging |
| [S1: Prompt Registry](../../../sdlc/01-prompt-registry/SKILL.md) | SDLC entry point after Track A completes |
| [S6: Deployment & Automation](../../../sdlc/06-deployment-and-automation/SKILL.md) | SDLC: DAB bundles and CI/CD pipeline |

## References

- [Debug a deployed AI agent](https://docs.databricks.com/aws/en/generative-ai/agent-framework/debug-agent)
- [Deploy a Databricks App](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/deploy)
- [Add resources to a Databricks app](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/resources)
- [Configure compute resources for Apps](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/compute-size)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-12 | Initial skill: systematic debugging for Databricks Apps agents — local dev, config, deployment, runtime, auth, Lakebase memory |
