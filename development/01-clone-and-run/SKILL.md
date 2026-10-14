---
name: 01-clone-and-run
description: >
  Use when starting a new custom agent project on Databricks Apps. Clone the
  agent-openai-agents-sdk template, run quickstart, start the local dev server,
  verify the built-in chat UI. Track A Step 1. Produces a running local agent
  project ready for customization.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: apps
deploy_verb: apps_deploy
deploy_note: "Clone the agent template and run it. The local dev server (quickstart) is the IDE/local branch; on Genie Code there is no local dev server — deploy to the Databricks Apps runtime and test the deployed app (run the deploy CLI through runDatabricksCli, pre-authenticated). On Genie Code clone the template under the cloned repo root (`{REPO_ROOT}` = `state_file_root` from `skills/vibecoding-state`), not a bare relative path — relative paths resolve against the page CWD (see `skills/genie-code-environment` §8)."
coverage: full
metadata:
  last_verified: "2026-04-15"
  volatility: medium
  upstream_sources: []
  author: "prashanth-subrahmanyam"
  version: "2.1.0"
  domain: "genai-agents"
  pipeline_position: "A1"
  consumes: "mlflow_environment, experiment_paths"
  produces: "local_project_directory, running_local_agent, project_structure_understanding, pypi_index_url_with_fallback"
  grounded_in: "docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent, github.com/databricks/app-templates"
---

# Track A Step 1: Clone and Run

Get a working agent running locally in under 30 minutes using the official
Databricks app-templates.

## When to Use

- Starting a **new** GenAI agent project on Databricks from scratch.
- Want a working agent with built-in chat UI before writing any custom logic.
- Following the [Author an AI agent and deploy it on Databricks Apps](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent) workflow.

## Foundation Prerequisite Check

Foundation Steps F1 and F2 **must be complete** before starting Track A.
Run these checks to verify:

```bash
# F1 check: MLflow installed and autolog available
python3 -c "import mlflow; assert tuple(int(x) for x in mlflow.__version__.split('.')[:2]) >= (3,10); mlflow.openai.autolog(); print('F1: OK')" 2>/dev/null || echo "F1: FAIL"

# F2 check: MLflow experiment exists
# EXPERIMENT_PATH MUST be set to the user-and-use-case-pinned path
#   /Users/<user_email>/mlflow/<APP_NAME>-agent
# (read it from .vibecoding-state.md → mlflow_experiment_path).
# The check fails fast if EXPERIMENT_PATH is unset rather than papering over
# it with a generic /Shared/my-agent/traces default.
python3 -c "import mlflow, os; p = os.environ.get('EXPERIMENT_PATH'); assert p, 'EXPERIMENT_PATH not set — read mlflow_experiment_path from .vibecoding-state.md'; e = mlflow.get_experiment_by_name(p); assert e, f'No experiment at {p}'; print('F2: OK')" 2>/dev/null || echo "F2: FAIL"
```

**If F1 fails:** Stop. **Load and execute**
`foundation/01-mlflow-genai-foundation/SKILL.md` to set up the MLflow
environment, autolog, and environment detection.

**If F2 fails:** Stop. **Load and execute**
`foundation/02-experiment-tracing-and-uc-storage/SKILL.md` to create the
experiment, configure tracing, and set up UC OTEL storage.

Both must print `OK` before continuing. The template you clone below already
contains MLflow setup code — F1/F2 teach the concepts and provision UC
resources, and the AI agent will reconcile rather than duplicate.

## Prerequisites

Verify before starting:

```bash
databricks auth token > /dev/null 2>&1 && echo "CLI: OK" || echo "CLI: FAIL"
uv --version > /dev/null 2>&1 && echo "uv: OK" || echo "uv: MISSING"
python3 -c "import sys; assert sys.version_info >= (3,11)" && echo "Python: OK"
node --version  # Should be v20+
```

All four must pass. If `databricks auth token` fails: **IDE/CLI** — set up a profile per PRE-REQUISITES §11; **Genie Code** — not applicable (pre-authenticated; `uv`/`node` checks also differ — see `skills/genie-code-environment`).

---

## Step 1a: Pick a Template and Clone

Databricks publishes multiple agent app templates. Pick the one that matches
your agent's required capabilities — they share the same `@invoke` / `@stream`
authoring pattern (Option B from
[A2: Agent Framework](../02-agent-framework/SKILL.md)), so picking a more
advanced template is **not** harder; it just adds plumbing you'd write
yourself otherwise.

| Template | When to pick | Adds |
|---|---|---|
| [`agent-openai-agents-sdk`](https://github.com/databricks/app-templates/tree/main/agent-openai-agents-sdk) | Single-agent tool-using assistant. **Default starting point** for a custom Track A agent. | OpenAI Agents SDK + `@invoke`/`@stream` + MLflow Agent Server + chat UI |
| [`agent-openai-agents-sdk-multiagent`](https://github.com/databricks/app-templates/tree/main/agent-openai-agents-sdk-multiagent) | Triage → specialist routing (multiple sub-agents with `handoffs`). | Adds multi-agent routing scaffolding to the SDK template |
| [`agent-openai-advanced`](https://github.com/databricks/app-templates/tree/main/agent-openai-advanced) | **Canonical for SkyLoyalty walkthrough.** Need short-term and long-term Lakebase memory plus a custom-tools example. | Adds `AsyncDatabricksSession` (short-term) + `LongTermMemory` (long-term) on Lakebase, plus a richer custom-tools example |
| [`agent-langgraph-advanced`](https://github.com/databricks/app-templates/tree/main/agent-langgraph-advanced) | LangGraph-based agent (state machine, custom node graph, complex control flow). | LangGraph CheckpointSaver + DatabricksStore on Lakebase |
| [`agent-migration-from-model-serving`](https://github.com/databricks/app-templates/tree/main/agent-migration-from-model-serving) | Existing `ResponsesAgent` on Model Serving you want to lift to Databricks Apps. | Migration scaffolding from Option A → Option B |

> **Default for the canonical SkyLoyalty walkthrough:** `agent-openai-advanced`.
> It already wires the two-layer memory pattern from
> [A5: Lakebase Memory](../05-lakebase-memory/SKILL.md) and saves you the
> work of porting from `agent-openai-agents-sdk`.

### Clone the template

```bash
# Option A: Use databricks CLI (when supported)
databricks apps init --template agent-openai-advanced my-agent-app

# Option B: Direct git clone (works for any template)
git clone --depth 1 https://github.com/databricks/app-templates.git /tmp/app-templates
cp -r /tmp/app-templates/agent-openai-advanced ./my-agent-app
cd my-agent-app
rm -rf .git
git init
```

Replace `agent-openai-advanced` with whichever template you picked from the
table above, and `my-agent-app` with your project name. Use
lowercase-with-hyphens (this becomes the Databricks App name).

---

## PyPI index URL with fallback

Some workspaces sit behind a corporate proxy or firewall that blocks the
public PyPI index, and others have intermittent failures resolving
`pypi.org`. To make the clone-and-run path resilient, configure `uv` /
`pip` with a public-first, Databricks-mirror-second index list **before**
running quickstart:

```yaml
# state://Track_A.a1_clone_and_run
pypi_index_url_with_fallback:
  - https://pypi.org/simple
  - https://pypi.databricks.com/simple
```

Apply the same list to the local environment (the order matters —
`pypi.org` is primary, the Databricks mirror is the fallback):

```bash
# uv (preferred): primary + fallback indexes
export UV_INDEX_URL="https://pypi.org/simple"
export UV_EXTRA_INDEX_URL="https://pypi.databricks.com/simple"

# pip equivalent (if a sub-step shells out to pip)
export PIP_INDEX_URL="https://pypi.org/simple"
export PIP_EXTRA_INDEX_URL="https://pypi.databricks.com/simple"
```

If `uv run quickstart` fails with an index resolution error
(`Could not connect to https://pypi.org`, `403`, `ReadTimeout` from
the index), retry once with the fallback as primary:

```bash
export UV_INDEX_URL="https://pypi.databricks.com/simple"
export UV_EXTRA_INDEX_URL="https://pypi.org/simple"
uv run quickstart
```

Capture the index list under `state://Track_A.a1_clone_and_run.pypi_index_url_with_fallback`
exactly as listed above. The list MUST contain both URLs in this order
(public first, mirror second) so re-runs and CI redeploys can recover
from a transient public-PyPI outage without code changes.

---

## Step 1b: Run Quickstart

The template includes a `quickstart` script that installs dependencies and
configures the local environment:

```bash
cd my-agent-app
uv run quickstart
```

**What quickstart does:**
1. Creates a virtual environment with `uv`
2. Installs all Python dependencies from `pyproject.toml`
3. Creates a `.env` file from `.env.example` (or interactive prompts)
4. Validates Databricks CLI authentication
5. Sets up the MLflow tracking URI

**If quickstart prompts for values:**

| Prompt | What to Enter |
|--------|---------------|
| Databricks host | Your workspace URL (e.g. `https://myworkspace.cloud.databricks.com`) |
| Warehouse ID | SQL Warehouse ID from your workspace |
| LLM endpoint | Model serving endpoint name (e.g. `databricks-claude-sonnet-4-6`) |

After quickstart, verify the `.env` file was created:

```bash
cat .env
# Should contain DATABRICKS_HOST, WAREHOUSE_ID, LLM_MODEL, etc.
```

---

## Step 1c: Start the Local Dev Server

> **Genie Code:** there is no local dev server — this local-quickstart path is IDE-only. Instead deploy to the Databricks Apps runtime and test the deployed app (the platform builds it server-side). See `skills/genie-code-environment` §4.

```bash
uv run start-app
```

This starts the MLflow AgentServer locally, typically on `http://localhost:8000`.

**Expected output:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Verify the built-in chat UI

Open `http://localhost:8000` in your browser. You should see:
- A chat interface with a text input field
- Streaming responses with markdown rendering
- The ability to send messages and receive agent responses

### Verify programmatic access

In a separate terminal:

```bash
curl -X POST http://localhost:8000/invocations \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "Hello, what can you do?"}]}'
```

You should receive a JSON response with the agent's reply.

---

## Step 1d: Tour the Project Structure

Read `references/project-structure.md` to understand the generated project layout.

---

## DO / DON'T

### DO — Run quickstart before start-app

```bash
uv run quickstart    # Sets up .env, installs deps
uv run start-app     # Starts the server
```

### DON'T — Skip quickstart

```bash
uv run start-app     # Error: missing .env, no dependencies
```

### DO — Check that the agent responds before moving on

```bash
curl -s http://localhost:8000/invocations \
  -H "Content-Type: application/json" \
  -d '{"input": [{"role": "user", "content": "Hello"}]}' | python -m json.tool
```

### DON'T — Move to Foundation Step 1 without verifying the chat UI works

If the agent does not respond, use the checks in `references/troubleshooting.md`.

---

## Troubleshooting

Read `references/troubleshooting.md` if `uv quickstart` or `uv start-app` fails.

---

## Validation Gate

All must pass before proceeding:

- [ ] Project cloned and `uv run quickstart` completed without errors
- [ ] `uv run start-app` starts the server on `http://localhost:8000`
- [ ] Chat UI at `http://localhost:8000` renders and accepts input
- [ ] Agent responds to "Hello" with a coherent reply
- [ ] You can identify `agent.py`, `start_server.py`, `app.yaml`, and `databricks.yml`
- [ ] `pypi_index_url_with_fallback` captured in state with `https://pypi.org/simple` first and `https://pypi.databricks.com/simple` second

## Next Step

After passing this gate, **load and execute**
`tracks/A-custom-agent-apps/02-agent-framework/SKILL.md` (A2: Agent Framework).

## Notes to Carry Forward

Record these values for subsequent steps:

| Key | Value |
|-----|-------|
| `project_dir` | Absolute path to the project |
| `agent_file` | `agent.py` (or your agent module path) |
| `config_file` | `config.yml` |
| `app_yaml` | `app.yaml` |
| `bundle_yaml` | `databricks.yml` |
| `local_url` | `http://localhost:8000` |
| `llm_endpoint` | Model serving endpoint name from `.env` |
| `pypi_index_url_with_fallback` | `[https://pypi.org/simple, https://pypi.databricks.com/simple]` (ordered: public primary, Databricks mirror fallback) |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| [F1: MLflow Foundation](../../../foundation/01-mlflow-genai-foundation/SKILL.md) | Prerequisite — MLflow environment and autolog |
| [F2: Tracing & UC OTEL](../../../foundation/02-experiment-tracing-and-uc-storage/SKILL.md) | Prerequisite — experiment paths and trace storage |
| [A2: Agent Framework](../02-agent-framework/SKILL.md) | Next step |

## References

- [Author an AI agent and deploy it on Databricks Apps](https://docs.databricks.com/aws/en/generative-ai/agent-framework/author-agent)
- [Databricks app-templates](https://github.com/databricks/app-templates)
- [MLflow AgentServer](https://mlflow.org/docs/latest/genai/serving/agent-server/)
- [uv package manager](https://docs.astral.sh/uv/)

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2026-04-26 | Added "PyPI index URL with fallback" subsection: `pypi_index_url_with_fallback` captured as ordered `[https://pypi.org/simple, https://pypi.databricks.com/simple]` (public primary, Databricks mirror fallback). Documents `UV_INDEX_URL` / `UV_EXTRA_INDEX_URL` (and pip equivalents) plus the retry-with-mirror-as-primary recipe for transient public-PyPI outages. Validation gate + carry-forward updated. |
| 2.0.0 | 2026-04-10 | Refactored from earlier draft: template selection table, Foundation prerequisite checks, two clone paths. |
| 1.0.0 | 2026-04-10 | Initial skill: template selection, quickstart, local dev, project tour |
