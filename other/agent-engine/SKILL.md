---
name: agent-engine
description: Deploy and manage AI agents on Vertex AI Agent Engine. Use when deploying ADK agents to production, configuring Agent Engine runtime, managing deployed agents, setting up sessions and memory, or integrating with A2A protocol. Covers deployment from agent objects and source files, environment configuration, scaling, sessions, memory bank, and agent management operations.
---

# Vertex AI Agent Engine

Deploy, manage, and scale AI agents in production on Google Cloud.


> **Model IDs on regional endpoints.** These samples pin `gemini-3.7-flash` rather than using the
> `gemini-flash-latest` alias. Agent Engine deploys to a region (`us-central1` above), and ADK's
> docs note the `-latest` aliases may not resolve on regional endpoints — pin an explicit version
> here. The alias is fine in the `adk` skill's local-development examples.

## Quick Reference

| Task | Pattern |
|------|---------|
| Install SDK | `pip install google-cloud-aiplatform[agent_engines,adk]` |
| Initialize client | `vertexai.Client(project, location)` |
| Deploy agent | `client.agent_engines.create(agent=app, config={...})` |
| Query agent | `remote_agent.stream_query(user_id, message)` |
| Delete agent | `remote_agent.delete(force=True)` |

## Prerequisites

```bash
# Required IAM roles
- Vertex AI User (roles/aiplatform.user)
- Storage Admin (roles/storage.admin)

# Enable APIs
gcloud services enable aiplatform.googleapis.com storage.googleapis.com
```

## Installation

```bash
pip install --upgrade google-cloud-aiplatform[agent_engines,adk]>=2.0

# For A2A support
pip install google-cloud-aiplatform[agent_engines,a2a]
```

## Initialize Client

```python
import vertexai

client = vertexai.Client(
    project="your-project-id",
    location="us-central1"
)
```

## Deploying Agents

### Method 1: From Agent Object (Interactive)

Best for development and testing.

```python
from google.adk.agents import Agent
from vertexai import agent_engines

# Create agent
def get_data(query: str) -> dict:
    """Gets data for a query.

    Args:
        query: The search query.
    """
    return {"status": "success", "data": "..."}

agent = Agent(
    model="gemini-3.7-flash",
    name="data_agent",
    instruction="You help users find data.",
    tools=[get_data]
)

# Wrap in AdkApp
app = agent_engines.AdkApp(agent=agent)

# Deploy
remote_agent = client.agent_engines.create(
    agent=app,
    config={
        "display_name": "data-agent",
        "requirements": [
            "google-cloud-aiplatform[agent_engines,adk]",
            "requests"
        ],
        "staging_bucket": "gs://your-bucket"
    }
)

print(f"Deployed: {remote_agent.resource_name}")
```

### Method 2: From Source Files (CI/CD)

Best for production deployments.

```python
remote_agent = client.agent_engines.create(
    config={
        "display_name": "production-agent",
        "source_packages": ["./agent_package"],
        "entrypoint_module": "agent_package.agent",
        "entrypoint_object": "root_agent",
        "requirements_file": "requirements.txt",
        "staging_bucket": "gs://your-bucket",
        "env_vars": {
            "API_KEY": "...",
            "DATABASE_URL": "..."
        }
    }
)
```

### Deployment Configuration Options

```python
config = {
    # Required
    "staging_bucket": "gs://your-bucket",

    # Package options
    "requirements": ["package1", "package2"],  # OR
    "requirements_file": "requirements.txt",
    "extra_packages": ["./local_package", "/path/to/dependency"],

    # Source deployment
    "source_packages": ["./agent_dir"],
    "entrypoint_module": "agent_dir.agent",
    "entrypoint_object": "root_agent",

    # Display
    "display_name": "My Agent",
    "description": "Agent description",

    # Environment
    "env_vars": {"KEY": "value"},

    # Resources
    "resource_config": {
        "min_instances": 1,
        "max_instances": 10,
        "cpu": "2",
        "memory": "4Gi"
    }
}
```

## Session Management

### Using InMemorySessionService (Development)

```python
from google.adk.sessions import InMemorySessionService
from vertexai.agent_engines import AdkApp

# Avoid httpx client issues in Agent Engine
session_service_builder = lambda **kwargs: InMemorySessionService()

app = AdkApp(
    agent=agent,
    session_service_builder=session_service_builder
)
```

### Default Session Service (Production)

Agent Engine provides managed sessions automatically when no custom service is specified.

## Querying Deployed Agents

### Synchronous Query

```python
response = remote_agent.query(
    user_id="user-123",
    message="What is the weather today?"
)
print(response)
```

### Streaming Query

```python
for event in remote_agent.stream_query(
    user_id="user-123",
    message="Explain quantum computing"
):
    print(event)
```

### Async Streaming

```python
async for event in remote_agent.async_stream_query(
    user_id="user-123",
    message="Analyze this data"
):
    print(event)
```

## Multi-Agent Deployment (A2A)

Deploying a multi-agent system that speaks A2A, including the agent card, executor
wiring, and remote-agent connections:
**[references/a2a-deployment.md](references/a2a-deployment.md)**

## Managing Agents

### List Agents

```python
agents = client.agent_engines.list()
for agent in agents:
    print(f"{agent.display_name}: {agent.resource_name}")
```

### Get Agent Details

```python
agent = client.agent_engines.get(resource_name="projects/.../agentEngines/...")
print(agent.display_name)
print(agent.create_time)
```

### Update Agent

```python
agent.update(
    display_name="Updated Agent Name",
    description="New description"
)
```

### Delete Agent

```python
# Safe delete
remote_agent.delete()

# Force delete (removes associated resources)
remote_agent.delete(force=True)
```

## Advanced Topics

For detailed information on sessions, memory bank, scaling optimization, and framework integration, see:

**[references/advanced_deployment.md](references/advanced_deployment.md)** - Comprehensive Agent Engine reference including:
- Session management patterns and lifecycle
- Memory Bank features for long-term personalization
- Runtime optimization (cold start mitigation, concurrency tuning)
- Framework integration patterns (ADK, LangChain, LangGraph, etc.)
- Security features (VPC-SC, CMEK, identity management)
- Code execution sandboxing
- Evaluation and monitoring strategies

## Environment Variables

```bash
# Required
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"

# For Vertex AI
export GOOGLE_GENAI_USE_VERTEXAI="1"

# Staging bucket
export BUCKET="gs://your-staging-bucket"
```

## Supported Frameworks

| Framework | Integration Level |
|-----------|------------------|
| ADK | Full |
| LangChain | Full |
| LangGraph | Full |
| LlamaIndex | SDK |
| AG2 | SDK |
| CrewAI | Custom Template |
| Custom | Custom Template |

## Dependencies

```
google-cloud-aiplatform[agent_engines,adk]>=2.0
google-adk[a2a]
uvicorn
fastapi
a2a-sdk>=1.1
```

## Complete example & self-contained deployment

An end-to-end deployment script, and the cloudpickle pattern for bundling an agent
without a source checkout:
**[references/advanced_deployment.md](references/advanced_deployment.md)**

## CLI Deployment (adk deploy)

Alternative to programmatic deployment:

```bash
cd src && adk deploy agent_engine \
  --project=my-project \
  --region=us-central1 \
  --staging_bucket=gs://my-bucket \
  --display_name="My Agent" \
  --trace_to_cloud \
  agent   # directory containing agent.py with root_agent
```

## Memory Bank — Practical API

Memory Bank is **auto-enabled** on Agent Engine when ADK >= 1.5.0 and `GOOGLE_CLOUD_AGENT_ENGINE_ID` env var is set (automatic in Agent Engine runtime). No deploy flags needed.

### Generate memories from conversation:

```python
client.agent_engines.memories.generate(
    name=agent_resource,
    direct_contents_source={"events": [
        {"content": {"role": "user", "parts": [{"text": "I'm allergic to peanuts."}]}},
    ]},
    scope={"user_id": "user-123"},
    config={"wait_for_completion": True},
)
```

### Generate from pre-extracted facts:

```python
client.agent_engines.memories.generate(
    name=agent_resource,
    direct_memories_source={"direct_memories": [
        {"fact": "Customer prefers organic produce"},
    ]},
    scope={"user_id": "user-123"},
)
```

### Retrieve memories (scope-based):

```python
results = client.agent_engines.memories.retrieve(
    name=agent_resource,
    scope={"user_id": "user-123"},
)
memories = list(results)
```

### Similarity search:

```python
results = client.agent_engines.memories.retrieve(
    name=agent_resource,
    scope={"user_id": "user-123"},
    similarity_search_params={"search_query": "dietary restrictions", "top_k": 3},
)
```

### Shared memory across agents:

Each agent engine has its own memory namespace. To share memories, generate/retrieve against the same agent engine resource, or use the same `user_id` scope across multiple agents.

### ADK integration (read-only):

```python
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
# Add to agent — auto-loads memories at conversation start
tools = [PreloadMemoryTool()]
```

`PreloadMemoryTool` **only reads**. To write memories, call `memory_service.add_session_to_memory(session)` explicitly after a session ends.

## ADK Evaluations on Agent Engine

Run evals against deployed agents:

```python
from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

eval_set = types.EvalSet(eval_set_id="my_eval", eval_cases=[
    types.EvalCase(
        eval_case_id="test_1",
        conversation_scenario=types.ConversationScenario(
            starting_prompt="What are the closing procedures?",
            conversation_plan="Ask for specific steps and safety checks.",
        ),
    ),
])

# Run inference then evaluate
result = client.evals.run_inference(agent=agent_resource, eval_set=eval_set,
    config=types.RunInferenceConfig(eval_run_id="run_1"))

evaluation = client.evals.evaluate(eval_set=result, metrics=[
    types.EvalMetric(metric_name="rubric_based_final_response_quality_v1"),
    types.EvalMetric(metric_name="hallucinations_v1"),
    types.EvalMetric(metric_name="safety_v1"),
    types.EvalMetric(metric_name="tool_use_quality_v1"),
], config=types.EvaluateConfig(eval_run_id="run_1"))
```

## REST API for Querying Deployed Agents

```python
import requests
import google.auth
from google.auth.transport.requests import Request

credentials, _ = google.auth.default()
credentials.refresh(Request())

url = (f"https://us-central1-aiplatform.googleapis.com/v1/"
       f"projects/{project_number}/locations/us-central1/"
       f"reasoningEngines/{agent_engine_id}:streamQuery")

resp = requests.post(url, headers={
    "Authorization": f"Bearer {credentials.token}",
    "Content-Type": "application/json",
}, json={"input": {"message": "Hello", "user_id": "user-1"}}, timeout=120)

# Response is newline-delimited JSON events
for line in resp.text.strip().split("\n"):
    event = json.loads(line)
    parts = event.get("content", {}).get("parts", [])
    for part in parts:
        if "text" in part:
            print(part["text"])
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Package not found | Add to `extra_packages` or `requirements` |
| httpx client error | Use `InMemorySessionService` |
| Deployment timeout | Increase staging bucket size, reduce dependencies |
| Agent not responding | Check logs in Cloud Console |
| A2A connection failed | Verify agent URL ends with `/.well-known/agent.json` |
| Permission denied | Add required IAM roles |
| Bucket access error | Use `gs://` prefix, ensure Storage Admin role |
| cloudpickle module not found | Inline all data in deploy script, no external imports |
| No query methods at runtime | Redeploy; broken deployments don't self-heal |
| Token overflow (>1M tokens) | Remove excess data stores from engine, reduce tool output size |
| Memories not persisting | Call `add_session_to_memory()` explicitly; PreloadMemoryTool is read-only |
| Eval not showing up | Need `client.evals.run_inference()` + `client.evals.evaluate()` calls |
