---
name: databricks-autonomous-operations
description: >
  End-to-end autonomous deployment and operations skill. Deploys Databricks Asset Bundles,
  runs jobs and pipelines, polls for completion, diagnoses failures, applies fixes, redeploys,
  and verifies — all without human intervention. Also serves as SDK/CLI/REST API reference.
  Use when deploying bundles, running jobs, monitoring pipelines, troubleshooting ANY failure,
  or operating in a self-healing deploy-fix-redeploy cycle. Triggers on "deploy", "bundle deploy",
  "run job", "run pipeline", "make it work", "job failed", "troubleshoot", "fix and redeploy".
metadata:
  author: prashanth subrahmanyam
  version: "3.2"
  domain: operations
  role: shared
  used_by_stages: [1, 2, 3, 4, 5, 6, 7, 8, 9]
  called_by:
    - bronze/00-bronze-layer-setup
    - silver/00-silver-layer-setup
    - gold/01-gold-layer-setup
    - semantic-layer/00-semantic-layer-setup
    - monitoring/00-observability-setup
    - ml/00-ml-pipeline-setup
    - genai-agents/00-course-orchestrator
  dependencies:
    - admin/self-improvement
  triggers:
    - "deploy"
    - "bundle deploy"
    - "bundle run"
    - "run job"
    - "run pipeline"
    - "make it work"
    - "deploy and run"
    - "deploy and fix"
    - "job failed"
    - "monitor job"
    - "troubleshoot"
    - "get-run"
    - "run output"
    - "task failed"
    - "redeploy"
    - "job status"
    - "pipeline failed"
    - "DLT error"
    - "cluster issue"
    - "monitor failed"
    - "alert failed"
    - "deploy failed"
    - "databricks-sdk"
    - "databricks-connect"
    - "CLI"
    - "INTERNAL_ERROR"
    - "UNRESOLVED_COLUMN"
    - "ModuleNotFoundError"
    - "TABLE_OR_VIEW_NOT_FOUND"
    - "ResourceAlreadyExists"
    - "PERMISSION_DENIED"
    - "self-heal"
    - "autonomous"
  last_verified: "2026-06-02"
  volatility: medium
  clients: [ide_cli, genie_code]   # CLI surface accessed via local shell (IDE) or runDatabricksCli (Genie Code)
  deploy_verb: "bundle deploy --target dev"   # deploy mechanics owned by databricks-asset-bundles (the spine)
  deploy_note: "operations/CLI reference — on Genie Code every databricks command routes via runDatabricksCli FROM THE BUNDLE EDITOR (dp_bundle_root); a blocked bundle deploy/run is a page-context signal, NEVER substitute SDK/REST creation (RULE_10); see genie-code-environment"
  coverage: all_stages
  upstream_sources:
    - name: "databricks-agent-skills"
      repo: "databricks/databricks-agent-skills"
      paths:
        - "skills/databricks-python-sdk/SKILL.md"
        - "skills/databricks-jobs/SKILL.md"
      relationship: "extended"
      last_synced: "2026-08-30"
      sync_commit: "ca92a6c"
---

# Databricks Autonomous Operations

## 1. Overview

> **Context Loading Rule:** Load this skill at **deployment time**, not during planning.
> During earlier phases, retain only this 3-step summary in working memory:
> `Deploy (bundle deploy) → Poll (get-run / pipelines get) → Verify (get-run-output)`.
> Full skill activation should happen when the first `bundle deploy` or `bundle run` is invoked.

This skill is both an **SDK/CLI/Connect reference** and an **autonomous operations playbook**. It teaches the AI agent to operate as an SRE — independently deploying, monitoring, diagnosing failures, applying fixes, redeploying, and verifying results across all Databricks resource types.

**Core Loop:** Deploy → Poll → Diagnose → Fix → Redeploy → Verify (max 3 iterations before escalation to user).

### When to Activate This Skill

- Deploying or running Databricks Asset Bundles (`bundle deploy`, `bundle run`)
- Monitoring job or pipeline runs for completion
- Troubleshooting ANY failure: jobs, DLT pipelines, monitors, alerts, clusters, Genie Spaces
- Using the Databricks Python SDK, CLI, Connect, or REST API
- Encountering error messages from Databricks services
- Operating in a self-healing deploy-fix-redeploy cycle
- Checking job/task/pipeline status or retrieving run output

**SDK Docs:** https://databricks-sdk-py.readthedocs.io/en/latest/
**GitHub:** https://github.com/databricks/databricks-sdk-py

**Runnable Examples:** See `examples/` directory for complete, copy-pasteable scripts:
- `examples/1-authentication.py` — All auth patterns (env vars, profiles, Azure SP, AccountClient, notebook context)
- `examples/2-clusters-and-jobs.py` — Cluster auto-selection, autoscaling, job CRUD, submit_and_wait, run_now_and_wait
- `examples/3-sql-and-warehouses.py` — Parameterized queries, chunked results, query_to_dataframe helper
- `examples/4-unity-catalog.py` — Tables, schemas, catalogs, volumes, file operations, pattern matching
- `examples/5-serving-and-vector-search.py` — Endpoint creation with TrafficConfig, chat/embedding queries, vector search with filters
- `examples/6-autonomous-operations.py` — Job monitoring, multi-task output retrieval, failure diagnosis, self-healing loop

---

## 2. Environment & Authentication

> **Client routing (RULE_1/2/4 — read once, applies to every command in this skill).** This skill is the
> CLI/SDK operations surface; the same operations run on both clients via different channels — **deploy
> mechanics are owned by `databricks-asset-bundles` (the spine); reference it rather than re-deriving them.**
> - **IDE (Cursor):** the local `databricks` CLI; auth via `databricks auth login` / `~/.databrickscfg`;
>   `databricks-connect` is available for local Spark.
> - **Genie Code has *three* execution paths — try them in order; "blocked on one path ≠ impossible":**
>   1. **`runDatabricksCli`** — the allow-listed, pre-authenticated CLI path (no `auth login`). The path
>      for `bundle validate` / `summary` / `deploy --target dev` and read verbs. `--version`/`help`/
>      `auth token`/`aitools`/`apps validate`/`apps manifest` are hard-blocked; `apps deploy` is
>      **unreliable here** (page-dependent + CWD-defeated). Use a `bundle validate` behavior probe instead
>      of a numeric `--version` compare.
>   2. **Python SDK** (`WorkspaceClient` via `executeCode`) — the **most capable** path: it **bypasses the
>      CLI allow-list** and is the reliable way to `w.apps.deploy(...)`, retrieve `w.config.token`, and poll
>      deployment/run state. **Caveat:** the SDK has **no bundle-deploy equivalent** (`bundle deploy` is a
>      composite client-side operation) — keep `bundle deploy` on `runDatabricksCli`.
>   3. **Native tools** (`createAsset`/`readTable`/…) for governed asset operations.
>
>   No local Spark on Genie Code (use workspace **serverless**; `databricks-connect` is IDE-only). Full
>   allow-list / CWD / FUSE / escape-hatch detail is in the **`genie-code-environment`** skill — load it on
>   demand. The CLI command examples below run via path 1 on Genie Code (local shell on the IDE); where a
>   verb is CLI-blocked, reach for the SDK (path 2).
>
> **⛔ The carve-out the "fall to the SDK" rule does NOT cover — `bundle deploy`/`run` and resource creation.**
> "Blocked ≠ impossible, try the SDK" is for **read-only / ad-hoc** ops (polling, inspecting schemas, lineage,
> token retrieval, `apps deploy`). It is **NOT** a license to substitute the SDK/REST for the bundle. When
> `bundle deploy`/`run` is blocked, that is a **page-context signal, not a dead end**: the verb is gated to the
> **bundle-folder page**, which on Genie Code you reach by opening the **"Open in bundle editor"** affordance on
> the `dp_bundle_root` folder (the bundle editor's CWD *is* the bundle root, where `validate`/`deploy`/`run` are
> pre-approved). **FIELD-CONFIRMED:** the same `bundle deploy` that returned "blocked by safety guardrails" /
> "`databricks.yml` not found" from a file/notebook page returned "Deployment complete!" and `bundle run …
> SUCCESS` from the bundle editor. So the fix is **navigate to the bundle editor**, never `w.jobs.create()` /
> `POST /api/2.1/jobs/create` / `POST /api/2.0/pipelines` / `CREATE TABLE` via `executeCode`. Creating
> jobs/pipelines/tables directly is the **RULE_10 authoring-discipline violation** — it produces live,
> un-versioned state that diverges from the bundle and is the exact regression this spine prevents. If
> `bundle deploy`/`run` **still** fails *from the bundle editor*, STOP and report the blocker — the SDK/REST
> creation route is an **escape hatch only on explicit operator authorization.** Surface a clickable
> bundle-editor link: `file_id = w.workspace.get_status("<dp_bundle_root>/databricks.yml").object_id`,
> `folder_id = w.workspace.get_status("<dp_bundle_root>").object_id`, link =
> `{w.config.host}/editor/files/{file_id}?o={w.get_workspace_id()}&contextId=folder%3A{folder_id}`. Detail in
> `genie-code-environment` §3/§8.

### Setup

- SDK: `uv pip install databricks-sdk`; **Connect (IDE-only):** `uv pip install databricks-connect` —
  not used on Genie Code (serverless; no local Spark)
- CLI version: **>= 0.278.0** on the IDE (`databricks --version`); on Genie Code the version is not
  introspectable (use a `bundle validate` behavior probe)
- Config (IDE): `~/.databrickscfg` or env vars `DATABRICKS_HOST`, `DATABRICKS_TOKEN`; Genie Code is
  pre-authenticated in-session

### Quick Auth

```python
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()                    # Auto-detect (env, config file, or notebook)
w = WorkspaceClient(profile="MY_PROFILE") # Named profile
```

- **Token expired? (IDE path)** `databricks auth login --host <url> --profile <name>` — N/A on Genie Code
  (pre-authenticated)
- **Profile-based CLI:** `DATABRICKS_CONFIG_PROFILE=<name> databricks <command>`
- **Full auth patterns** (Azure SP, AccountClient, etc.): see `references/sdk-api-reference.md`

---

## 3. SDK API Quick Reference

**Full code examples and patterns:** `references/sdk-api-reference.md`
**Runnable scripts:** `examples/` directory (see file listing in Section 1)

| API | Key Operations | Critical Notes |
|-----|---------------|----------------|
| **Clusters** | `list`, `get`, `create_and_wait`, `ensure_cluster_is_running`, `start`, `stop` | Use `select_spark_version()` and `select_node_type()` |
| **Jobs** | `list`, `run_now_and_wait`, `submit_and_wait`, `get_run`, `get_run_output`, `cancel_run` | `get_run_output` needs **task** `run_id`, not parent job `run_id` |
| **SQL Execution** | `execute_statement` with `wait_timeout` | Use `StatementParameterListItem` for parameterized queries |
| **Warehouses** | `list`, `start`, `stop`, `create_and_wait` | Use `auto_stop_mins` to control costs |
| **Unity Catalog** | `tables.list`, `tables.get`, `tables.exists`, `catalogs.list`, `schemas.list` | `list_summaries` for fast pattern matching |
| **Volumes/Files** | `files.upload`, `files.download`, `files.list_directory_contents` | Path format: `/Volumes/catalog/schema/volume/file` |
| **Serving** | `create_and_wait`, `query` (custom/chat/embeddings), `get_open_ai_client` | `scale_to_zero_enabled` for cost control |
| **Vector Search** | `query_index`, `upsert_data_vector_index`, `sync_index` | Use `filters_json` for filtered queries |
| **Pipelines** | `list_pipelines`, `get`, `start_update`, `stop_and_wait`, `list_pipeline_events` | Events contain error details for troubleshooting |
| **Monitors** | `quality_monitors.get`, `delete`, `update`, `run_refresh` | Update MUST include ALL `custom_metrics` |
| **Alerts V2** | `alerts_v2.create_alert`, `update_alert`, `delete_alert` | Update requires full `update_mask` |
| **Secrets** | `create_scope`, `put_secret`, `get_secret` | Use for API keys, tokens |

### Critical Patterns

- **Async apps (FastAPI):** SDK is synchronous — wrap with `asyncio.to_thread()`
- **Long-running ops:** Use `_and_wait()` variants with `timeout=timedelta(...)`
- **Error handling:** `from databricks.sdk.errors import NotFound, PermissionDenied, ResourceAlreadyExists`
- **Direct REST:** `w.api_client.do(method="GET", path="/api/2.0/...")`

---

## 4. CLI Operations Reference

### Command Matrix

| Category | Command | Purpose |
|----------|---------|---------|
| **Bundle** | `databricks bundle validate` | Pre-deploy validation (catches ~80% of errors) |
| **Bundle** | `databricks bundle deploy -t <target>` | Deploy all resources |
| **Bundle** | `databricks bundle run -t <target> <job>` | Start a job run |
| **Bundle** | `databricks bundle destroy -t <target>` | Cleanup all resources |
| **Jobs** | `databricks jobs get-run <RUN_ID> --output json` | Get run status |
| **Jobs** | `databricks jobs get-run-output <TASK_RUN_ID> --output json` | Get task notebook output |
| **Jobs** | `databricks jobs list-runs --job-id <JOB_ID> --output json` | List recent runs |
| **Jobs** | `databricks jobs cancel-run <RUN_ID>` | Cancel running job |
| **Pipelines** | `databricks pipelines get <PIPELINE_ID> --output json` | Get pipeline status |
| **Pipelines** | `databricks pipelines get-update <PID> <UID> --output json` | Get update details |
| **Pipelines** | `databricks pipelines list-pipeline-events <PID> --output json` | Get events/errors |
| **Pipelines** | `databricks pipelines start-update <PIPELINE_ID>` | Start pipeline update |
| **Clusters** | `databricks clusters get <CLUSTER_ID> --output json` | Get cluster status |
| **Clusters** | `databricks clusters events <CLUSTER_ID> --output json` | Get cluster events |
| **Warehouses** | `databricks warehouses get <WH_ID> --output json` | Get warehouse status |
| **Auth** (IDE only) | `databricks auth login --host <url> --profile <name>` | Re-authenticate (Genie Code is pre-authenticated) |
| **Workspace** | `databricks workspace export <path> --format SOURCE` | Export notebook |
| **Apps** | `databricks apps logs <app-name>` | App deployment/runtime logs |

### Key jq Patterns

See `references/cli-jq-patterns.md` for the complete catalog. Most critical:

```bash
# Job state
databricks jobs get-run <RUN_ID> --output json | jq '.state'

# Task summary for multi-task jobs
databricks jobs get-run <RUN_ID> --output json | jq '.tasks[] | {task: .task_key, run_id: .run_id, result: .state.result_state}'

# Failed tasks only
databricks jobs get-run <RUN_ID> --output json | jq '.tasks[] | select(.state.result_state == "FAILED") | {task: .task_key, error: .state.state_message, url: .run_page_url}'

# Task output (MUST use task run_id, not parent job run_id)
databricks jobs get-run-output <TASK_RUN_ID> --output json | jq -r '.notebook_output.result // "No output"'
```

---

## 5. Autonomous Deploy-Run-Fix Playbook

**This is the core workflow. Follow these steps whenever deploying a bundle, running a job, or operating autonomously.**

### Step 0: Discover Bundle Resources

Before deploying, understand what's in the bundle:

```bash
# Read databricks.yml to find targets and included resources
# Then read resource YAML files under resources/ directory
# Identify: jobs (atomic/composite/orchestrator), pipelines, dashboards, alerts
```

Determine the **target** (`dev`, `staging`, `prod`) from the user or default to `dev`.

### Step 0.5: Resolve Workspace Identity

Before ANY deployment, confirm you are targeting the correct workspace:

1. **Check `databricks.yml`** for `workspace.host` and `profile` under the target
2. **Check active profile:** `databricks auth env --profile <name>` — verify host matches intent
3. **If multiple profiles exist** in `~/.databrickscfg`, do NOT auto-select — present options to user
4. **If `databricks.yml` has no profile set**, ask the user which workspace to target
5. **Scan repo context before creating a new `databricks.yml`:** `Glob` for `**/databricks.yml` across the repository. If an existing bundle config specifies `host` or `profile`, surface those as the **suggested default** in your question to the user. Example: "Your existing app config at `apps_lakebase/databricks.yml` uses profile `azure-demo` → host `https://adb-xxx.azuredatabricks.net/`. Should I use that same workspace for this bundle?"
6. **When `bundle validate` reports "multiple profiles matched"** the host, include the repo-context hint in your question rather than listing all candidates blindly. Example: "Multiple profiles match this host. Your `apps_lakebase/databricks.yml` uses profile `azure-demo` — should I use that, or a different one?"

**CLI profile inheritance warning:** Raw `databricks api` calls do NOT inherit the profile from `databricks.yml`. Always pass `-p <profile>` explicitly when using `databricks api`.

**If deployed to wrong workspace** → see Step 7.5 for cleanup.

### Step 1: Validate & Deploy

> **Client note:** IDE runs these in a terminal. **Genie Code runs `databricks bundle …` via `runDatabricksCli`
> from the bundle editor** — open the **"Open in bundle editor"** affordance on the `dp_bundle_root` folder
> (the icon that appears next to `databricks.yml`) *before* deploying; the bundle editor's CWD is the bundle
> root, where `validate`/`deploy`/`run` are pre-approved. Surface the clickable editor link for the operator
> (see §2 carve-out). See `skills/genie-code-environment` §3.

```bash
databricks bundle validate -t <target>   # Pre-flight — catches ~80% of errors
databricks bundle deploy -t <target>     # Deploy all resources
```

**If validate fails:** Read the error, fix the YAML (see Section 6 + `skills/databricks-asset-bundles` skill), re-validate.
**If deploy is BLOCKED (≠ failed — Genie Code):** symptoms are "blocked by safety guardrails," "not in the
allow-list," or "`databricks.yml` not found." This is a **page-context** signal, not a YAML/code defect and not
a job failure. **Do not** enter the diagnose-fix loop and **do not** create resources via SDK/REST/`CREATE` as a
substitute (RULE_10 violation). Navigate to the **bundle editor** on `dp_bundle_root` and retry. Only on explicit
operator authorization is the escape hatch (§2) permitted.
**If deploy FAILS (executes, returns an error):** Common causes: auth expired (403), path resolution errors, invalid task types. See Section 6.
**`--force` clarification:** `--force` handles **Terraform state drift** only (e.g., resource deleted outside bundle). It does NOT fix API name-uniqueness conflicts. For "pipeline name already used" or "resource already exists": list and delete the conflicting resource, then redeploy without `--force`.

### Step 2: Run

**For jobs:**
```bash
databricks bundle run -t <target> <job_name>
# Output includes a Run URL like: https://<host>/#job/<JOB_ID>/run/<RUN_ID>
# EXTRACT the RUN_ID from this URL — you need it for polling
```

**For DLT pipelines:**
```bash
databricks bundle run -t <target> <pipeline_name>
# Output includes: Pipeline URL with PIPELINE_ID
# Also shows UPDATE_ID for this specific update
```

**Cursor-specific:** Use `block_until_ms: 0` to background `bundle run` immediately. Then read the terminal output file to capture the Run URL. Parse the RUN_ID or PIPELINE_ID from the URL.

### Step 3: Poll Until Terminal State

**Jobs — poll with exponential backoff (30s → 60s → 120s):**
```bash
databricks jobs get-run <RUN_ID> --output json | jq -r '.state.life_cycle_state'
# PENDING → RUNNING → TERMINATED (also: INTERNAL_ERROR, SKIPPED)
```

When `life_cycle_state == TERMINATED`, check the result:
```bash
databricks jobs get-run <RUN_ID> --output json | jq -r '.state.result_state'
# SUCCESS → go to Step 4a    FAILED → go to Step 4b
```

**DLT Pipelines — poll the latest update state:**
```bash
databricks pipelines get <PIPELINE_ID> --output json | jq -r '.latest_updates[0].state'
# COMPLETED → success    FAILED → get events for errors
```

### Step 4a: On SUCCESS — Verify & Report

```bash
# For multi-task jobs, verify all tasks succeeded:
databricks jobs get-run <RUN_ID> --output json \
  | jq '.tasks[] | {task: .task_key, result: .state.result_state}'

# Get task output (structured JSON from dbutils.notebook.exit):
databricks jobs get-run-output <TASK_RUN_ID> --output json \
  | jq -r '.notebook_output.result // "No output"'
```

Report success to user with the **Run URL** for verification.
If this was part of a multi-job deployment, proceed to the next job.

### Step 4b: On FAILURE — Diagnose

**CRITICAL for multi-task jobs:** `get-run-output` only works on the **task** `run_id`, NOT the parent job `run_id`.

```bash
# Step A: Find failed tasks and their task-level run_ids
databricks jobs get-run <JOB_RUN_ID> --output json \
  | jq '.tasks[] | select(.state.result_state == "FAILED") | {task: .task_key, run_id: .run_id, error: .state.state_message}'

# Step B: Get detailed output for EACH failed task
databricks jobs get-run-output <TASK_RUN_ID> --output json \
  | jq -r '.notebook_output.result // .error // "No output"'
```

**For DLT pipeline failures:**
```bash
databricks pipelines list-pipeline-events <PID> --output json \
  | jq '[.events[] | select(.level == "ERROR")] | .[0:5]'
```

Match the error against **Section 6** (decision tree) and `references/error-solution-matrix.md`.

### Step 5: Fix

1. **Read** the source file(s) identified from the stack trace or error message
2. **Apply fix** using editor tools (StrReplace, Write)
3. If YAML/config issue → fix the DAB YAML (consult `skills/databricks-asset-bundles` skill)
4. If dependency issue → deploy upstream assets first (see Section 6 ordering)
5. **Same-class fix rule:** Before redeploying, grep ALL files from the same generation batch for the same error pattern. If the bug was in one notebook, check sibling notebooks for identical issues. Fix all instances in one pass.

### Step 6: Redeploy & Re-run (Loop)

```bash
databricks bundle deploy -t <target>    # Redeploy with fix
databricks bundle run -t <target> <job>  # Re-run
# → Return to Step 3 (Poll)
```

**Maximum 3 iterations.** Track each iteration's error and fix.

### Step 7: Escalation (After 3 Failed Attempts)

Present to the user:
1. **All errors encountered** — with run IDs, task keys, error messages
2. **All fixes attempted** — what was changed and why
3. **Root cause hypothesis** — best guess based on evidence
4. **Run page URLs** — direct links to the Databricks UI

### Step 7.5: Cleanup After Wrong-Workspace Deploy

If resources were deployed to the wrong workspace:

1. **Inventory what was deployed:** Run `databricks bundle summary -t <target>` in the wrong workspace
2. **Destroy cleanly:** `databricks bundle destroy -t <target>` (requires user confirmation)
3. **Warn about persistent artifacts:** Tables, schemas, and data created by jobs are NOT removed by `bundle destroy` — these must be dropped manually
4. **Reconcile state:** Delete `.databricks/` state directory if switching workspaces in the same repo
5. **Redeploy to correct workspace:** Update profile/target, then restart from Step 0.5

**Trigger this step proactively** whenever the user says "use profile X" / "switch to workspace Y" / "actually deploy to Z" AND you have already deployed in the current session. Before re-deploying to the new workspace, inventory what is running in the old workspace and offer `bundle destroy` on it. **Do not silently re-deploy** — orphaned jobs in the previous workspace are exactly the failure mode this step exists to prevent.

### Step 8: Capture Learnings

After every resolved failure (or escalation), trigger `admin/self-improvement`:
- Add new error → fix mappings to `references/error-solution-matrix.md`
- Update "Top 10" table in Section 6 if this error is frequent
- **Always capture** if fix took 2+ iterations or was escalated

---

## 6. Master Troubleshooting Decision Tree

**Full error-solution tables:** `references/error-solution-matrix.md` (7 categories, 40+ patterns)
**DLT-specific troubleshooting:** `references/dlt-pipeline-troubleshooting.md`
**Diagnostic SQL queries:** `references/diagnostic-queries.md`

### Quick Decision Guide

1. **Deployment error?** → Check auth (`403`), YAML syntax, task type (`notebook_task` not `python_task`), path resolution
2. **Job runtime error?** → Get task-level output (use **task** `run_id`), match error to solution matrix
3. **DLT pipeline error?** → Get events via CLI, check upstream tables exist, verify schema
4. **Monitor/Alert error?** → Check `ResourceAlreadyExists` (delete+recreate), schema existence, `update_mask`
5. **Dependency error?** → Follow required order: Bronze → Gold Setup → Gold Merge → Semantic → Monitoring → Genie
6. **Cluster error?** → Check events via CLI, look for OOM/unreachable/timeout patterns

### Top 10 Most Common Errors (Inline)

| Error | Quick Fix |
|-------|-----------|
| `ModuleNotFoundError` | Add to `%pip install` or DAB environment spec |
| `TABLE_OR_VIEW_NOT_FOUND` | Run setup job first; check 3-part catalog.schema.table path |
| `DELTA_MULTIPLE_SOURCE_ROW_MATCHING` | Deduplicate source before MERGE |
| `Invalid access token (403)` | IDE: `databricks auth login --host <url> --profile <name>` (Genie Code is pre-authenticated — re-check the page/profile) |
| `ResourceAlreadyExists` | Delete + recreate (monitors, alerts) |
| `python_task not recognized` | Use `notebook_task` with `notebook_path` |
| `PARSE_SYNTAX_ERROR` | Read failing SQL file, fix syntax, redeploy |
| `Parameter not found` | Use `base_parameters` dict, not CLI-style `parameters` |
| `run_job_task` vs `job_task` | Use `run_job_task` (not `job_task`) |
| Genie `INTERNAL_ERROR` | Deploy semantic layer (TVFs + Metric Views) first |
| `bundle deploy` "blocked by safety guardrails" / "`databricks.yml` not found" (Genie Code) | **Page context, not a code bug** — open the **bundle editor** on `dp_bundle_root` and retry; never substitute SDK/REST job creation (RULE_10) |

---

## 7. Job Design for Monitorability

**Full patterns:** `references/job-design-patterns.md` — structured output, progress messages, fail-fast, partial success, 3-layer hierarchy.

**Key rules:**
- Every notebook must `dbutils.notebook.exit(json.dumps({...}))` with structured status
- Print `[Step N/M]` progress messages so the agent can locate failures
- Fail fast: include actionable error messages (e.g., "Run bronze_setup_job first")
- 3-layer hierarchy: atomic (`notebook_task`) → composite (`run_job_task`) → orchestrator (`run_job_task`)
- Partial success: ≥90% items succeeding = OK; fix individual failures

---

## 8. Agent Behavioral Patterns

### Background Command Pattern (Cursor-Specific)

For `databricks bundle run` or any long-running command:
1. Execute with `block_until_ms: 0` to background immediately
2. Read the terminal output file to check for completion
3. Parse RUN_ID from the output URL

### Exponential Backoff for Polling

- Normal jobs: 30s → 60s → 120s (no state change = increase interval)
- Long-running training jobs: start at 60s, max 300s
- DLT pipelines: 30s (typically faster)

### Context Capture on Every Failure

On each failure, record and maintain:
- `run_id` and `task_run_id`
- `job_name` and `task_key`
- Target environment (`dev`, `staging`, `prod`)
- Full error message
- `run_page_url` for UI access
- Iteration count (which fix attempt this is)

### Self-Healing Loop

```
Iteration 1: Deploy → Run → Monitor → [FAIL] → Diagnose → Fix → Redeploy
Iteration 2: Run → Monitor → [FAIL] → Diagnose → Fix → Redeploy
Iteration 3: Run → Monitor → [FAIL] → ESCALATE TO USER
```

### Dependency Awareness

Before deploying, verify prerequisites exist:
- **Genie Spaces** require: TVFs + Metric Views (semantic layer)
- **Monitoring** requires: Gold tables (populated)
- **Gold merge** requires: Gold tables (setup job)
- **Silver DLT** requires: Bronze tables
- **Alerts** require: Monitoring output tables
- **Always follow:** Bronze → Gold → Semantic → Monitoring → Alerts → Genie

### Partial Success Handling

Some jobs use ≥90% success thresholds:
- Alerting deployment: 27/30 alerts succeeding = OK, fix the 3 individually
- Monitoring setup: 7/8 monitors = OK, debug the 1 failure
- **Do NOT** fail the entire workflow for 1 out of N items failing

### CLI Limitations Awareness

Some diagnostics require the Databricks Workspace UI:
- Full notebook execution logs (when `get-run-output` returns truncated or empty)
- DLT pipeline data flow visualization
- Detailed Spark execution plans

**Always provide `run_page_url` to the user** when CLI output is insufficient.

### Learning Capture Pattern (Self-Improvement Integration)

After every troubleshooting session (successful or escalated), run this checklist:

```
Post-Troubleshooting Self-Improvement:
1. Was this error already in references/error-solution-matrix.md?
   ├── YES → Was the documented fix accurate? If not, update it.
   └── NO  → Add the error pattern and fix to the matrix.

2. Did the initial diagnosis match the actual root cause?
   ├── YES → No action needed.
   └── NO  → Document the misleading signals in the relevant skill.

3. How many iterations were needed?
   ├── 1 → Capture only if error was novel or non-obvious.
   ├── 2-3 → ALWAYS update the relevant skill with the fix.
   └── Escalated → Document what the user found; update skills with user's fix.

4. Is this error likely to recur?
   ├── YES → Ensure it's in Top 10 table (if frequent) or error-solution matrix.
   └── NO  → Document as a one-off note in the session, skip skill update.
```

**Skill priority for updates** (search in this order):
1. `references/error-solution-matrix.md` — error-to-fix mapping
2. `common/databricks-autonomous-operations` — troubleshooting decision tree
3. `skills/databricks-asset-bundles` — if deployment-related
4. Domain-specific skill (e.g., `gold/pipeline-workers/02-merge-patterns` for MERGE errors)
5. New skill — only if all above are irrelevant (see `admin/self-improvement` justification checklist)

### Safety: Never Retry Destructive Operations

Without explicit user confirmation, NEVER retry:
- `databricks bundle destroy`
- `DROP TABLE` / `DROP SCHEMA`
- `w.quality_monitors.delete()`
- `w.alerts_v2.delete_alert()`

### Safety: Never Substitute Direct Creation for a Blocked Bundle Deploy (RULE_10)

A **blocked** `bundle deploy`/`run` (Genie Code "safety guardrails" / "not in allow-list" / "`databricks.yml`
not found") is a **page-context** signal, never a license to create the deliverable another way. NEVER, as a
workaround for a blocked deploy:
- `w.jobs.create()` / `POST /api/2.1/jobs/create`
- `w.pipelines.create()` / `POST /api/2.0/pipelines` / `createAsset(pipeline)`
- `w.schemas.create()` / `CREATE SCHEMA` / `CREATE VOLUME` / `CREATE TABLE` to provision the deliverable

The fix is **navigate to the bundle editor** on `dp_bundle_root` and redeploy. The SDK/REST creation route is an
**escape hatch only on explicit operator authorization.** Likewise, a **failed** *job* is fixed by editing the
bundle source file under `dp_bundle_root` and **redeploying** — never by patching the live job via API/UI.

---

## References

### Reference Documents (Load on Demand)
- `references/sdk-api-reference.md` — Full SDK API with code examples for all services
- `references/error-solution-matrix.md` — Error tables for all 7 resource categories (40+ patterns)
- `references/diagnostic-queries.md` — SQL queries for investigation
- `references/dlt-pipeline-troubleshooting.md` — DLT pipeline failure patterns
- `references/cli-jq-patterns.md` — jq patterns for parsing CLI JSON output
- `references/cli-quick-reference.md` — CLI vs SDK side-by-side table
- `references/job-design-patterns.md` — Structured output, progress messages, 3-layer hierarchy

### Runnable Examples
- `examples/1-authentication.py` through `examples/6-autonomous-operations.py` (see Section 1)

### Scripts
- `scripts/monitor_multitask_job.sh` — Multi-task job monitoring shell script

### External Docs
- SDK: https://databricks-sdk-py.readthedocs.io/en/latest/
- GitHub: https://github.com/databricks/databricks-sdk-py

---

## See Also

- Authoritative upstream: [databricks-agent-skills / `databricks-core`](https://github.com/databricks/databricks-agent-skills/tree/main/skills/databricks-core) — back-up reference for canonical Databricks CLI / auth / data exploration patterns.

