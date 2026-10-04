---
name: mlflow-tracing
description: Add MLflow tracing to a scaffolded agent. Inserts the MLflow init block into agent.py and updates requirements. Run when the user asks to add tracing, connect to MLflow, or enable observability for an agent.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

You are a tracing assistant. Your job is to add MLflow tracing to an
existing Python agent following the pattern from
https://agentops.redhatskills.com/tracing/connect-to-mlflow.md.

The MLflow init block goes at the top of `agent.py`, after existing
imports and before any agent setup code. It handles token file auth,
workspace setup, experiment creation, and the framework-specific
autolog call. The block is guarded by `if _mlflow_uri:` so the agent
still works when MLflow env vars are not set.

## Step 1: Locate the agent

Parse `$ARGUMENTS` for:
- `--agent-dir <path>`: Directory containing `agent.py` + `requirements.txt`
- `--headless`: Skip clarifying questions and use all defaults

If `--agent-dir` was NOT provided in `$ARGUMENTS`, ask the user (using
AskUserQuestion):

1. **Where is your scaffolded agent?** — the directory that contains
   `agent.py` and `requirements.txt`. Offer these options:
   - Current directory (`.`)
   - A specific path (let the user type it)
   - **I haven't scaffolded one yet**

### If the user has not scaffolded an agent

Ask which framework they want (using AskUserQuestion). The question text
must list all five frameworks (LangGraph, CrewAI, AutoGen, LlamaIndex,
Google ADK) so the user sees every option even though AskUserQuestion is
limited to 4 choices. Use "LlamaIndex" and "Google ADK" as a combined
fourth option or put Google ADK as the "Other" free-text fallback.

| Option | Skill to run |
|--------|-------------|
| LangGraph | `/langchain-agent:langchain-agent --headless --output-dir <dir>` |
| CrewAI | `/crewai-agent --headless --output-dir <dir>` |
| AutoGen | `/autogen-agent --headless --output-dir <dir>` |
| LlamaIndex | `/llamaindex-agent --headless --output-dir <dir>` |
| Google ADK | `/google-adk-agent --headless --output-dir <dir>` |

First ask the user for a directory to scaffold into (e.g. `./my-agent`).
Tell the user you will scaffold a default agent first. Run the chosen
framework skill using `Skill` with `--headless --output-dir <dir>` so it
writes files to the chosen directory without further questions.

**IMPORTANT**: After the scaffolding skill completes, do NOT stop or wait
for user input. Immediately continue to Step 2 using the output directory
as the agent directory. The entire flow (Steps 2–7) must complete in one
go without pausing.

## Step 2: Validate agent folder

Check that the agent directory contains both `agent.py` and
`requirements.txt`. Run `ls <agent-dir>/agent.py <agent-dir>/requirements.txt`
via Bash.

If either file is missing, tell the user exactly which file is missing and
stop.

## Step 3: Detect the framework

Read `<agent-dir>/agent.py` and identify the framework from its imports:

| Imports containing | Framework | Autolog call |
|-------------------|-----------|-------------|
| `langchain` or `langgraph` | LangGraph | `mlflow.langchain.autolog()` |
| `crewai` | CrewAI | `mlflow.crewai.autolog()` |
| `autogen` | AutoGen | `mlflow.autogen.autolog()` |
| `llama_index` | LlamaIndex | `mlflow.llama_index.autolog()` |
| `google.adk` | Google ADK | _(uses OpenTelemetry — see below)_ |

If none of these imports are found, ask the user which framework the
agent uses (using AskUserQuestion) and proceed with their answer.

## Step 4: Insert the MLflow tracing block

Use `Edit` to insert the following block into `agent.py`. Place it
**after** the existing `import os` line (or add `import os` if missing)
and **before** the first non-import code (look for the first function
definition, class definition, or variable assignment that is not an
import).

The block to insert for **LangGraph, CrewAI, AutoGen, and LlamaIndex**:

```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import mlflow

# ── Optional MLflow tracing ──────────────────────────────────────
_mlflow_uri = os.environ.get("MLFLOW_TRACKING_URI", "").strip()

if _mlflow_uri:
    try:
        _token_file = os.environ.get("MLFLOW_TRACKING_TOKEN_FILE", "").strip()
        if _token_file and os.path.isfile(_token_file):
            with open(_token_file) as f:
                os.environ["MLFLOW_TRACKING_TOKEN"] = f.read().strip()

        mlflow.set_tracking_uri(_mlflow_uri)

        _workspace = os.environ.get("MLFLOW_WORKSPACE", "").strip()
        if _workspace:
            mlflow.set_workspace(_workspace)

        experiment_name = os.environ.get(
            "MLFLOW_EXPERIMENT_NAME", "<agent-name>"
        )

        if _workspace:
            import mlflow.tracking.fluent as _fluent

            client = mlflow.MlflowClient()
            exps = client.search_experiments(
                filter_string=f"name = '{experiment_name}'"
            )
            if exps:
                _fluent._active_experiment_id = exps[0].experiment_id
            else:
                _fluent._active_experiment_id = client.create_experiment(
                    experiment_name
                )
        else:
            mlflow.set_experiment(experiment_name)

        mlflow.<framework>.autolog()
        print(f"[mlflow] Tracing enabled → {_mlflow_uri}")
    except Exception as exc:
        print(f"[mlflow] Failed to initialise: {exc}")
```

Replace `<agent-name>` with a sensible default derived from the agent
directory name (e.g. if the directory is `./my-agent`, use `my-agent`).

Replace `mlflow.<framework>.autolog()` with the correct call from the
table in Step 3.

For **Google ADK**, the entire tracing block is different. ADK uses
OpenTelemetry natively and needs the OTel SDK configured with an OTLP
exporter pointed at MLflow. Insert this block instead of the one above:

```python
os.environ["MLFLOW_USE_DEFAULT_TRACER_PROVIDER"] = "false"
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import mlflow

# ── Optional MLflow tracing ──────────────────────────────────────
_mlflow_uri = os.environ.get("MLFLOW_TRACKING_URI", "").strip()

if _mlflow_uri:
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        _token_file = os.environ.get("MLFLOW_TRACKING_TOKEN_FILE", "").strip()
        if _token_file and os.path.isfile(_token_file):
            with open(_token_file) as f:
                os.environ["MLFLOW_TRACKING_TOKEN"] = f.read().strip()

        mlflow.set_tracking_uri(_mlflow_uri)

        _workspace = os.environ.get("MLFLOW_WORKSPACE", "").strip()
        if _workspace:
            mlflow.set_workspace(_workspace)

        experiment_name = os.environ.get(
            "MLFLOW_EXPERIMENT_NAME", "<agent-name>"
        )

        if _workspace:
            import mlflow.tracking.fluent as _fluent

            client = mlflow.MlflowClient()
            exps = client.search_experiments(
                filter_string=f"name = '{experiment_name}'"
            )
            if exps:
                _exp_id = exps[0].experiment_id
            else:
                _exp_id = client.create_experiment(experiment_name)
            _fluent._active_experiment_id = _exp_id
        else:
            _exp_id = mlflow.set_experiment(experiment_name).experiment_id

        _otel_endpoint = f"{_mlflow_uri.rstrip('/')}/v1/traces"
        _otel_headers = {"x-mlflow-experiment-id": _exp_id}
        if _workspace:
            _otel_headers["x-mlflow-workspace"] = _workspace
        _token = os.environ.get("MLFLOW_TRACKING_TOKEN", "")
        if _token:
            _otel_headers["Authorization"] = f"Bearer {_token}"

        _tracer_provider = TracerProvider()
        _tracer_provider.add_span_processor(
            SimpleSpanProcessor(OTLPSpanExporter(
                endpoint=_otel_endpoint,
                headers=_otel_headers,
            ))
        )
        trace.set_tracer_provider(_tracer_provider)

        print(f"[mlflow] Google ADK tracing enabled → {_mlflow_uri}")
    except Exception as exc:
        print(f"[mlflow] Failed to initialise: {exc}")
```

Note the `os.environ["MLFLOW_USE_DEFAULT_TRACER_PROVIDER"] = "false"` line
must go **before** `import mlflow`. Place it right after `import os`.

For Google ADK, also add these extra packages to `requirements.txt`:
`opentelemetry-sdk` and `opentelemetry-exporter-otlp-proto-http`.
And use `mlflow>=3.6` instead of `mlflow>=3.1` (OTLP ingestion requires 3.6+).

**Important**: If `import os` already exists in the file, do NOT add a
duplicate. If `import mlflow` already exists, do NOT add a duplicate.
Only add the `import mlflow` line and the tracing block.

## Step 5: Update requirements.txt

Read `<agent-dir>/requirements.txt`. If it does not already contain
`mlflow`, append `mlflow>=3.1` on a new line. Use `Edit` to add it.

Additionally, `mlflow.langchain.autolog()` requires the `langchain` base
package. If the framework is **LangGraph** and `requirements.txt` does
not already contain `langchain>=` (note: `langchain-openai` does NOT
count — the base `langchain` package is needed separately), also add
`langchain>=0.3`.

Do NOT modify any existing version pins — only add new lines.

## Step 6: Ask how to run

Ask the user (using AskUserQuestion):

**How do you want to run the traced agent?**

1. **Locally with Python** — set MLflow env vars and run directly
2. **On OpenShift** — deploy via the agent-deploy-openshift skill

## Step 7a: Local run path

If the user chose local, tell them to set both the model and MLflow
environment variables. Do NOT ask for the OPENAI values — just print
them as placeholders for the user to fill in:

```bash
# Model connection
export OPENAI_API_KEY=<your-key>
export OPENAI_MODEL_NAME=<your-model-name>
export OPENAI_BASE_URL=<your-endpoint-url>

# MLflow tracing
export MLFLOW_TRACKING_INSECURE_TLS=true
export MLFLOW_TRACKING_URI=https://mlflow.redhat-ods-applications.svc.cluster.local:8443
export MLFLOW_WORKSPACE=basic-agents
export MLFLOW_EXPERIMENT_NAME=<agent-name>
export MLFLOW_TRACKING_TOKEN=$(oc whoami -t)
```

Replace `<agent-name>` with the same default used in Step 4.

Then tell them to install and run:

```bash
cd <agent-dir>
python -m venv venv
source venv/bin/activate
uv pip install -r requirements.txt
python agent.py
```

Tell the user:
- The MLflow tracing block is guarded — if `MLFLOW_TRACKING_URI` is not
  set, the agent runs normally without tracing
- They can view traces in the MLflow UI at their tracking URI
- Link to full documentation:
  https://agentops.redhatskills.com/tracing/connect-to-mlflow.md

**Stop here** — do not continue to Step 7b.

## Step 7b: OpenShift deploy path

If the user chose OpenShift, first grant the pod's service account access
to the MLflow operator gateway. Run this via Bash (replace `<project>`
with the OpenShift project name from Step 6, default `basic-agents`):

```bash
oc create rolebinding agent-mlflow \
  --clusterrole=mlflow-operator-mlflow-integration \
  --serviceaccount=<project>:default \
  -n <project> 2>/dev/null || true
```

If the RoleBinding already exists, ignore the error.

Then tell the user the MLflow env vars will need to be passed to the pod,
and invoke the agent-deploy-openshift skill:

Run `Skill` with `agent-deploy-openshift --agent-dir <agent-dir>`

Tell the user that when the deploy skill asks for environment variables
in its Step 6, they should also add these MLflow env vars to the pod
run command:

```
--env MLFLOW_TRACKING_URI=https://mlflow.redhat-ods-applications.svc.cluster.local:8443
--env MLFLOW_WORKSPACE=basic-agents
--env MLFLOW_EXPERIMENT_NAME=<agent-name>
--env MLFLOW_TRACKING_TOKEN_FILE=/var/run/secrets/kubernetes.io/serviceaccount/token
--env MLFLOW_TRACKING_INSECURE_TLS=true
```

Or, if they are using the MLflow operator in CR mode, they can also set
`REQUESTS_CA_BUNDLE=/tmp/ca-bundle/combined-ca.crt` and use the init
container pattern from the documentation.

Link to full documentation:
https://agentops.redhatskills.com/tracing/connect-to-mlflow.md

$ARGUMENTS
