---
name: 06-deployment-and-automation
description: >
  Use when deploying an agent to production or setting up CI/CD automation.
  Covers Databricks Apps deployment, Asset Bundles, service principal
  permissions, and evaluate-then-promote pipelines — even if you just
  want "deploy my agent and set up a release gate." Also use for MCP
  tool connectivity, Supervisor long-running tasks, or production trace
  linking. SDLC Step 6.
license: Apache-2.0
compatibility: "Requires Databricks workspace with MLflow 3.10+ and Unity Catalog. Scripts use uv."
clients: [ide_cli, genie_code]
bundle_resource: apps
deploy_verb: apps_deploy
deploy_note: "The production deploy skill — bundle resources via the `bundle deploy --target dev` spine plus the App deploy step. On Genie Code run every deploy CLI through runDatabricksCli (pre-authenticated); on IDE via the local CLI. CI/CD automation is the same bundle/spine on both clients. See `skills/genie-code-environment` for the deploy verbs."
coverage: full
metadata:
  last_verified: "2026-06-05"
  volatility: high
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "4.3.1"
  domain: "genai-agents"
  pipeline_position: "S6"
  consumes: "uc_model_version, champion_alias, logged_model_id"
  produces: "databricks_app, deployment_pipeline, serving_endpoint"
  grounded_in: "https://docs.databricks.com/aws/en/dev-tools/bundles/, https://docs.databricks.com/aws/en/dev-tools/databricks-apps/, https://docs.databricks.com/aws/en/generative-ai/mcp/, https://docs.databricks.com/aws/en/generative-ai/agent-bricks/multi-agent-supervisor-long-running-tasks, https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/version-tracking/link-production-traces-to-app-versions"
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-mlflow-evaluation/SKILL.md"
      relationship: "reference"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
---

# Deployment and Automation

Deploy your agent to **Databricks Apps** (a common production target) and automate
**evaluate → gate → promote → deploy** using Databricks Asset Bundles (DAB) and
your CI system.

## Upstream Lineage

This skill references Databricks Agent Skills' `databricks-mlflow-evaluation` skill for evaluate-gate-promote automation, production trace linkage, and monitoring handoff guidance. If release gates depend on eval harness semantics or upstream monitoring patterns, consult the upstream skill first, then apply this skill's Databricks Apps and Asset Bundle deployment contracts.

## When to Use

- Evaluation gates passed (SDLC Step 4) and the model is registered in Unity Catalog (Step 5).
- You need a repeatable bundle workflow (`databricks bundle deploy` / `run`), not ad-hoc workspace copies.
- You want MCP tool connectivity, Supervisor-style orchestration, or production traces linked to app versions.
- You need service principal access patterns and post-deploy verification.

---

## Versioned Resource Path Contract

Every persisted workshop artifact that can be superseded must be versioned. The CI/CD pipeline owned by this skill **reads** three of these and **emits** the fourth:

- signoffs (read): `/Volumes/<catalog>/<schema>/signoffs/v<N>/decision.md` — owned by [`04b-stakeholder-signoff`](../04b-stakeholder-signoff/SKILL.md)
- eval summaries (read): `/Volumes/<catalog>/<schema>/eval_runs/v<N>/summary.json` — owned by [`04-evaluation-runs`](../04-evaluation-runs/SKILL.md)
- prompt candidates (read): `prompts:/{catalog}.{uc_agent_schema}.system_instructions@candidate_v<N>` — owned by [`01-prompt-registry`](../01-prompt-registry/SKILL.md) / [`08b-prompt-handauthoring`](../08b-prompt-handauthoring/SKILL.md)
- deployment plans (emit): `/Volumes/<catalog>/<schema>/deployment_plans/v<N>/plan.md`

`<N>` is a monotonically increasing integer per artifact type, scoped to `(catalog, schema, artifact_type)` (or `(catalog, uc_agent_schema, prompt_name)` for prompt candidates). Resolve `<catalog>` and `<schema>` from state — never hard-code. The promote/deploy step MUST verify that the **same `<N>`** is referenced consistently across the eval summary, signoff decision, and prompt candidate before promoting; releasing against a mixed set of versions silently breaks rollback. Always write a fresh `v<N+1>` for the deployment plan; never overwrite an existing version.

---

## Production Registration Gate: Structured Signoff Consumption

The promote step MUST consume the **structured YAML front matter** in `signoffs/v<N>/decision.md` (owned by [`04b-stakeholder-signoff`](../04b-stakeholder-signoff/SKILL.md)). Substring grep on the markdown body is forbidden — narrative text legitimately mentions words like "APPROVED" or "REJECTED" in past tense or as quoted reasons.

The signoff document carries two independent decisions. Both must clear before production registration runs:

- `engineering_signoff.decision` — set to `APPROVED` or `APPROVED_WITH_CONDITIONS`.
- `stakeholder_signoff.decision` — set to `APPROVED` or `APPROVED_WITH_CONDITIONS`.

Any of `REJECTED`, missing block, or unparseable YAML blocks production registration. The single audit-tracked escape hatch is a `state_override` block in the same front matter that **captures the original decision verbatim** so reviewers can reconstruct what was bypassed.

```python
# In the CI promote step — runs BEFORE setting the @champion alias
# or calling databricks bundle deploy --target prod.
from pathlib import Path
import yaml

ALLOWED = {"APPROVED", "APPROVED_WITH_CONDITIONS"}

signoff_path = Path(f"/Volumes/{catalog}/{schema}/signoffs") / f"v{version}" / "decision.md"
text = signoff_path.read_text()
assert text.startswith("---\n"), "signoff missing YAML front matter"
_, front, _ = text.split("---\n", 2)
meta = yaml.safe_load(front) or {}

eng = (meta.get("engineering_signoff") or {}).get("decision")
biz = (meta.get("stakeholder_signoff") or {}).get("decision")

if eng not in ALLOWED or biz not in ALLOWED:
    override = meta.get("state_override") or {}
    captured_eng = (override.get("engineering_signoff") or {}).get("decision")
    captured_biz = (override.get("stakeholder_signoff") or {}).get("decision")
    if captured_eng != eng or captured_biz != biz:
        raise SystemExit(
            f"Blocked: engineering={eng}, stakeholder={biz}; no state_override "
            "captures the original decisions. Production registration aborted."
        )
# Only here may the pipeline proceed to alias promotion + bundle deploy.
```

This gate runs **before** any of the following actions:

1. Setting the `@champion` (or production) alias in Unity Catalog.
2. Issuing `databricks bundle deploy --target prod`.
3. Updating `MLFLOW_ACTIVE_MODEL_ID` in the production app environment.

If the gate raises, the entire promote step exits non-zero and CI surfaces the failure to the requester. There is no retry without first re-running the signoff workflow in [`04b-stakeholder-signoff`](../04b-stakeholder-signoff/SKILL.md).

---

## Databricks Asset Bundles (DAB)

> **Genie Code:** run every deploy command through `runDatabricksCli` (pre-authenticated), and be on the bundle's page so the CWD resolves to the bundle root. The CI/CD spine is identical on both clients. See `skills/genie-code-environment` §3–§4.

Define jobs, apps, and variables in `databricks.yml`, then deploy and run by target.

```yaml
# databricks.yml (illustrative)
bundle:
  name: my_agent_bundle

variables:
  catalog: { default: main }
  job_id_env: { default: MY_AGENT_JOB_ID }  # inject app env from bundle if needed

resources:
  jobs:
    my_eval_job:
      name: my-agent-evaluate-and-promote
      # tasks: notebook / wheel / sql — see DAB docs
  apps:
    my_agent_app:
      name: my-agent-app
      source_code_path: ./app

targets:
  dev:
    default: true
    workspace:
      host: https://<dev-workspace>.cloud.databricks.com
  staging:
    workspace:
      host: https://<staging-workspace>.cloud.databricks.com
  prod:
    workspace:
      host: https://<prod-workspace>.cloud.databricks.com
```

Workflow:

```bash
databricks bundle validate
databricks bundle deploy --target dev
databricks bundle run --target dev my_agent_app   # or job name per your bundle
```

Use **targets** for environment-specific workspace hosts, variables, and overrides (dev / staging / prod). See [Databricks Asset Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/).

---

> **Recommended default:** Deploy to **Databricks Apps** for most agents. Use **Model Serving** only when you need a pure inference endpoint without a custom UI or backend.

## Databricks Apps: `app.yaml` / `app.yml`

Declare how the app starts and which platform resources it may use.

- **`command`**: process that runs your server (for example `uvicorn` or your framework’s entrypoint).
- **`env`**: plain values and bindings. Set **`MLFLOW_ACTIVE_MODEL_ID`** to the UC logged-model identifier (or substitute from bundle variables) so production traces align with the deployed app version — see [Link production traces to app versions](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/version-tracking/link-production-traces-to-app-versions).
- **Tracing env vars**: also set `ENABLE_MLFLOW_TRACING=true`, `MLFLOW_EXPERIMENT_ID=<numeric>`, and `APP_ENVIRONMENT=production` (or `staging`) so traces flow from the deployed runtime and app code can override `mlflow.source.type` via metadata. The full env-var matrix (PAT vs OAuth, SP `CAN_EDIT` requirement, the Git-folder caveat) lives in the canonical reference: [`foundation/02-experiment-tracing-and-uc-storage/references/prod-tracing-deployment.md`](../../foundation/02-experiment-tracing-and-uc-storage/references/prod-tracing-deployment.md). For the `APP_ENVIRONMENT` override pattern and user / session metadata, see [F2c — Trace context and environments](../../foundation/02c-trace-context-and-environments/SKILL.md).
- **Resources**: attach SQL warehouse, serving endpoints, MLflow experiment, Lakebase, etc., per [Databricks Apps resources](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/resources).

Example fragment:

```yaml
command:
  - "python"
  - "-m"
  - "myapp"

env:
  MLFLOW_ACTIVE_MODEL_ID: "{{ logged_model_id }}"   # resolve via bundle / CI
  # Optional: tracing warehouse, feature flags, etc.

# resources: (warehouse, endpoints, lakebase — per product docs)
```

Replace `{{ logged_model_id }}` with your bundle variable or CI-injected value (for example the model version URI or ID your org uses).

---

## How `app.yaml` and `databricks.yml` Interact

These two files serve different purposes and are read at different times:

| File | Read by | When | Purpose |
|------|---------|------|---------|
| `app.yaml` | Apps platform | App process startup | Runtime config: command, env vars, resource bindings |
| `databricks.yml` | `databricks bundle` CLI | Deploy time | Provisioning: create/update app, experiments, jobs, permissions |

When deploying via bundles, the `config` block inside `databricks.yml` (`resources.apps.<name>.config`) **overrides** the corresponding fields in `app.yaml`. Specifically:

- `config.command` in the bundle replaces `command` in `app.yaml`
- `config.env` in the bundle replaces `env` in `app.yaml`
- `resources` in the bundle app block replaces `resources` in `app.yaml`

**Recommendation:** Use `databricks.yml` as the **source of truth** for all deployment configuration. Keep `app.yaml` as a minimal runtime fallback for local dev or standalone (non-bundle) deploys. Do **not** maintain the same env vars or resource IDs in both files — they will drift and cause confusing deployment mismatches.

**Common mistake:** Editing `app.yaml` to fix a deployed app's config, then wondering why `databricks bundle deploy` reverts the change. The bundle always writes its own `config` block.

---

## Preflight (Generic)

Before `databricks bundle deploy`, verify:

- Databricks CLI auth for the intended workspace / target.
- Unity Catalog objects referenced by the app exist (catalogs, schemas, tables, functions).
- The app’s service principal (or run-as identity) has required privileges on warehouses, catalogs, and serving endpoints.
- Attached serving endpoints respond (health / smoke inference if applicable).

Automate these checks in a small script or a DAB job step; do not assume deploy alone validates runtime access.

---

## Service Principal Permissions

After the app (or job) identity exists, grant least-privilege access. Prefer the **`databricks permissions`** CLI where supported for warehouses, catalogs, and serving endpoints (exact resource types and verbs follow current CLI docs).

Pattern:

```bash
# Illustrative — replace resource names and principal with yours
databricks permissions update sql warehouses <warehouse-id> \
  --json '{"access_control_list": [{"group_name": "<sp-or-group>", "permission_level": "CAN_USE"}]}'

databricks permissions update registered-models <full-model-name> \
  --json '{"access_control_list": [{"service_principal_name": "<app-sp-application-id>", "permission_level": "CAN_QUERY"}]}'
```

For UC SQL grants (tables, functions), use `GRANT` in SQL as needed. OTEL or trace tables need explicit `SELECT` / `MODIFY` if your app writes telemetry to UC.

---

## Verify Deployment

```python
from databricks.sdk import WorkspaceClient
from openai import OpenAI

w = WorkspaceClient()
client = OpenAI(
    base_url=f"{w.config.host}/apps/<app-name>/api",
    api_key=w.config.token,
)
response = client.chat.completions.create(
    model="my-agent",
    messages=[{"role": "user", "content": "Hello, what can you do?"}],
)
print(response.choices[0].message.content)
```

Open the App URL from deploy output in the browser to exercise the hosted UI if applicable.

---

## MCP Integration

**Model Context Protocol (MCP)** connects agents to **tools** (Unity Catalog functions, SQL warehouses, retrieval, custom backends) using a standard protocol so the model can invoke capabilities without hard-coding every integration in app code.

**Why it matters for deployment:** Tool endpoints and credentials must match the **same identity** the app uses in production (typically the app SP). If MCP reaches a warehouse or UC function, grant that identity the same way you would for in-process tool calls.

**Pattern:**

1. Declare MCP **server configs** for each tool class (per Databricks docs: transport, auth, allowed scopes).
2. Register tools with your agent definition so invocations map cleanly to MCP methods.
3. In CI, smoke-test tool calls against a dev workspace before promoting the bundle target.

Keep secrets out of source control; use workspace secrets, OIDC, or bundle variables for server URLs and tokens where applicable. See [MCP on Databricks](https://docs.databricks.com/aws/en/generative-ai/mcp/).

---

## Supervisor API: Long-Running Tasks

HTTP requests often time out before a **multi-step agent** (plan → tools → synthesis) finishes. The **Supervisor** flow lets you **start** a task, obtain a continuation token or task id, then **poll or resume** with **`task_continue_request`** until the run reaches a terminal state.

**When to use:** Long tool chains, human-in-the-loop pauses, or heavy retrieval that cannot complete inside a single synchronous response.

**Pattern:**

1. **Start** — initial request returns identifiers needed for continuation (per current API contract).
2. **Continue** — client or backend job sends `task_continue_request` with that context until done or failed.
3. **Persist** — store partial outputs if users disconnect; idempotent continues reduce duplicate side effects where the API allows.

Design UIs and APIs to show progress (“still running”) rather than blocking one HTTP call for the full workflow. See [Multi-agent Supervisor: long-running tasks](https://docs.databricks.com/aws/en/generative-ai/agent-bricks/multi-agent-supervisor-long-running-tasks).

---

## Production Trace Linking

Reiterate: set **`MLFLOW_ACTIVE_MODEL_ID`** in the app’s **`env`** (see `app.yaml` above) so MLflow GenAI tracing associates production traffic with the **active UC model / app version**. Combine with your Step 5 registration flow so CI or bundle injects the correct ID per deploy.

---

## AI Gateway Integration (Producer Side)

If your workspace has an AI Gateway fronting LLM and MCP endpoints (see [foundation/04-ai-gateway](../../foundation/04-ai-gateway/SKILL.md)), configure the deployed agent to **produce** traffic through the gateway rather than hitting provider endpoints directly.

This gives the deployed agent:

- Uniform usage tracking + inference-table audit per deploy target.
- Rate limits that protect the shared provider from a misbehaving release.
- Org-wide guardrails (PII, safety) applied before provider calls.
- Correlation between MLflow trace `request_id` and gateway inference rows.

### Point the app at the gateway via `app.yaml` env vars

```yaml
env:
  MLFLOW_ACTIVE_MODEL_ID:        "{{ logged_model_id }}"
  LLM_GATEWAY_BASE_URL:          "{{ workspace_host }}/serving-endpoints/skyloyalty-ai-gateway/"
  LLM_GATEWAY_MODEL:             "claude-sonnet-46"   # served_entity name, not endpoint
  MCP_GATEWAY_BASE_URL:          "{{ workspace_host }}/serving-endpoints/skyloyalty-mcp-gateway/"
```

Application code reads these env vars and constructs the OpenAI / Anthropic client base URL from `LLM_GATEWAY_BASE_URL`. There are no code changes beyond the base URL — the gateway speaks the same protocol as the underlying endpoint.

### Correlate MLflow trace → gateway inference row

Inside the agent, set `databricks_request_id` on every LLM / MCP call to the current MLflow trace request id:

```python
import mlflow

def gateway_headers() -> dict:
    span = mlflow.get_current_active_span()
    return {"databricks_request_id": span.request_id} if span else {}

response = client.chat.completions.create(
    model=os.environ["LLM_GATEWAY_MODEL"],
    messages=[...],
    extra_headers=gateway_headers(),
)
```

Now any production trace can be joined to its provider-level row via SQL (see [foundation/04-ai-gateway/references/inference-tables-queries.md](../../foundation/04-ai-gateway/references/inference-tables-queries.md), recipe 5).

### Per-target gateway URLs

Use bundle targets to switch gateway per environment — a single prod gateway for all prod apps; a dev gateway for the dev target:

```yaml
targets:
  dev:
    variables:
      llm_gateway_url: "https://<dev-host>/serving-endpoints/dev-ai-gateway/"
  prod:
    variables:
      llm_gateway_url: "https://<prod-host>/serving-endpoints/prod-ai-gateway/"

resources:
  apps:
    my_agent_app:
      config:
        env:
          LLM_GATEWAY_BASE_URL: ${var.llm_gateway_url}
```

### Validation after deploy

- [ ] Hit the app endpoint once; confirm a row lands in `main.<ops_schema>.gw_*_payload` within ~1 min.
- [ ] Confirm `databricks_request_id` in that row matches the MLflow trace request id for the same turn.
- [ ] Confirm usage tracking rows increment in `main.<ops_schema>.gw_*_usage`.

If any of the above fail, the app is likely still hitting the provider directly — grep the app source for raw endpoint URLs.

---

## CI/CD Automation (Generic)

Example **GitHub Actions** (or **Databricks Workflows**) sequence:

1. **Checkout / install** — Databricks CLI, bundle, and test dependencies; authenticate via OIDC to Databricks or a CI service principal.
2. **Evaluate** — run your eval job or notebook (offline metrics, online replay, or judge LLM) against the **candidate** UC model version; log results to MLflow and/or append to a UC metrics table.
3. **Gate** — script compares metrics to thresholds (quality, safety, cost, latency). Exit non-zero to block the pipeline; notify on failure.
4. **Promote** — on success, update Unity Catalog: set alias **`@champion`** (or your production alias) to the candidate version using the Registry API or a small script step.
5. **Deploy** — `databricks bundle deploy --target prod` (or staging first) with bundle variables set to the promoted **`logged_model_id`** so **`MLFLOW_ACTIVE_MODEL_ID`** in `app.yaml` matches the release.

Optional: manual approval step between promote and deploy for regulated environments. Keep tokens in GitHub secrets or Databricks-managed identity; never hard-code in `databricks.yml`. **Load** [`references/cicd-templates.md`](references/cicd-templates.md) **if** you need job YAML or `taskValues` examples.

**Serving-only path:** If the artifact is a Model Serving endpoint instead of an App, align the final step with Track C in the track reference.

---

## Deployment by Track

> **Load** [`references/deployment-by-track.md`](references/deployment-by-track.md) **if** you need Track A (Apps), Track B (Supervisor API / config-focused CI/CD), or Track C (Model Serving vs Apps) deployment paths.

> **Load** [`references/cicd-templates.md`](references/cicd-templates.md) **if** you need CI/CD YAML snippets, `taskValues`, or trigger examples.

> **Load** [`references/bundle-configuration.md`](references/bundle-configuration.md), [`references/deployment-job-patterns.md`](references/deployment-job-patterns.md), [`references/apps-deployment-patterns.md`](references/apps-deployment-patterns.md), [`references/model-serving-patterns.md`](references/model-serving-patterns.md), [`references/local-dev-loop.md`](references/local-dev-loop.md) **if** you need extended bundle, job, apps, serving, or local dev patterns. **Load** [`assets/templates/app-yaml-template.yaml`](assets/templates/app-yaml-template.yaml) and [`assets/templates/databricks-yml-template.yaml`](assets/templates/databricks-yml-template.yaml) **if** you want starter `app.yaml` / `databricks.yml` templates.

---

## DO / DON'T

| DO | DON'T |
|----|--------|
| Run preflight checks (UC exists, SP access, endpoints healthy) before deploy | Deploy without validating env and permissions |
| Use `databricks bundle validate` before `deploy` | Rely on prod workspace defaults for secrets |
| Grant SP explicit access to every resource the app touches | Assume auto-provisioned identities are fully entitled |
| Use separate **targets** for dev / staging / prod | Point prod deploys at a dev target by mistake |
| Gate release on evaluation thresholds | Ship when metrics regressed |
| Use `served_entities:` (`entity_name` / `entity_version`) in endpoint config; for AI-Gateway-style endpoints use `external_model.databricks-model-serving` (see [F4](../../foundation/04-ai-gateway/SKILL.md)) | Use legacy `served_models:` (`model_name` / `model_version`) — bundle validation rejects it with `unknown field: served_models` |

---

## Common Issues

| Issue | Fix |
|-------|-----|
| Bundle auth error | IDE/CLI: re-auth per PRE-REQUISITES §11; Genie Code: pre-authenticated — verify the target host/`--target` instead |
| App errors at runtime | `databricks apps logs <app-name>` |
| Permission denied on UC / warehouse / endpoint | SP grants + `databricks permissions` / SQL `GRANT` |
| Chat/UI unreachable | Confirm app running: `databricks apps get <app-name>` |
| Traces not linked to version | Set `MLFLOW_ACTIVE_MODEL_ID` and confirm model ID matches deployment |

---

## Validation Gate (SDLC Step 7 Readiness)

- [ ] Preflight checks pass (UC, SP, endpoints).
- [ ] `databricks bundle validate` and `databricks bundle deploy` succeed for the chosen target.
- [ ] Endpoint config uses `served_entities:` (`entity_name` / `entity_version`), not legacy `served_models:`. AI-Gateway-style endpoints use `external_model.databricks-model-serving` (see [F4](../../foundation/04-ai-gateway/SKILL.md)).
- [ ] Structured signoff parsed from `signoffs/v<N>/decision.md` YAML front matter; both `engineering_signoff.decision` and `stakeholder_signoff.decision` are `APPROVED` (or `APPROVED_WITH_CONDITIONS`), or a `state_override` captures the original decisions. Substring grep is not used.
- [ ] App reachable at workspace App URL; agent responds (UI and/or API client).
- [ ] `MLFLOW_ACTIVE_MODEL_ID` set appropriately for this release (if using trace linking).
- [ ] SP permissions verified for all data and tool paths (including MCP tools if used).
- [ ] CI/CD pipeline defined or planned: evaluate → gate → promote → deploy.

## Notes to Carry Forward

| Key | Value |
|-----|-------|
| `app_url` | Deployed Databricks App URL |
| `app_name` | Name from bundle / Apps |
| `bundle_target` | `dev` / `staging` / `prod` |
| `sp_id` | Service principal or run-as identity |
| `logged_model_id` / alias | UC model version tied to release |

---

## References (Databricks)

- [Databricks Asset Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/)
- [MCP on Databricks](https://docs.databricks.com/aws/en/generative-ai/mcp/)
- [Multi-agent Supervisor: long-running tasks](https://docs.databricks.com/aws/en/generative-ai/agent-bricks/multi-agent-supervisor-long-running-tasks)
- [Link production traces to app versions](https://docs.databricks.com/aws/en/mlflow3/genai/prompt-version-mgmt/version-tracking/link-production-traces-to-app-versions)
- [Databricks Apps](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/)
- [Add resources to a Databricks app](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/resources)
- [Apps in bundles](https://docs.databricks.com/aws/en/dev-tools/bundles/resources#app)
- [Model Serving](https://docs.databricks.com/aws/en/machine-learning/model-serving/)

### Reference files (this skill)

| File | Content |
|------|---------|
| [`references/deployment-by-track.md`](references/deployment-by-track.md) | Track A/B/C deployment paths |
| [`references/cicd-templates.md`](references/cicd-templates.md) | CI/CD YAML snippets, `taskValues`, triggers |
| [`references/apps-deployment-patterns.md`](references/apps-deployment-patterns.md) | Advanced Apps patterns |
| [`references/bundle-configuration.md`](references/bundle-configuration.md) | Full `databricks.yml` patterns |
| [`references/model-serving-patterns.md`](references/model-serving-patterns.md) | Serving deployment patterns |
| [`references/deployment-job-patterns.md`](references/deployment-job-patterns.md) | DAB job DAG, triggers |
| [`references/local-dev-loop.md`](references/local-dev-loop.md) | Local dev workflow |
| [`assets/templates/app-yaml-template.yaml`](assets/templates/app-yaml-template.yaml) | Starter `app.yaml` |
| [`assets/templates/databricks-yml-template.yaml`](assets/templates/databricks-yml-template.yaml) | Starter `databricks.yml` |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 4.3.1 | 2026-04-26 | Canonicalized `served_entities:` (`entity_name` / `entity_version`) in `references/model-serving-patterns.md` concurrency example, replacing the legacy `served_models:` block that bundle validation rejects with `unknown field: served_models`. Added DO/DON'T row and validation-checklist gate to SKILL.md, with cross-reference to F4 `external_model.databricks-model-serving` shape for AI-Gateway-style endpoints. |
| 4.3.0 | 2026-04-26 | Added Production Registration Gate: Structured Signoff Consumption section. Promote step now parses `engineering_signoff` + `stakeholder_signoff` YAML front matter from `signoffs/v<N>/decision.md`; production registration is blocked unless both decisions are `APPROVED` (or `APPROVED_WITH_CONDITIONS`) or a `state_override` captures the original decisions. Substring grep is forbidden. |
| 4.2.0 | 2026-04-26 | Added Versioned Resource Path Contract section enumerating eval_runs/v<N>, signoffs/v<N>, candidate_v<N>, deployment_plans/v<N> paths the CI/CD pipeline reads/emits, with cross-artifact version-consistency requirement before promote. |
| 4.1.0 | 2026-04-19 | Added AI Gateway integration (producer side) section: env wiring in `app.yaml`, `databricks_request_id` correlation header, per-target gateway URLs, post-deploy validation. |
| 4.0.0 | 2026-04-10 | De-coupled from repo-specific scripts. Added MCP, Supervisor API long-running tasks, and `MLFLOW_ACTIVE_MODEL_ID`. Grounded in official Databricks bundles, MCP, and deployment docs. |
| 2.0.1 | 2026-04-10 | Moved track-specific deployment and CI/CD YAML snippets to reference files; condensed inline examples. |
| 2.0.0 | 2026-04-10 | Merged deployment skills; Apps as primary target; CI/CD section added. |
