---
name: a2a
description: Build multi-agent systems using Google ADK with A2A protocol, deployed on Agent Engine. Use when creating agents that communicate via A2A, building multi-tier agent hierarchies, connecting ADK agents with RemoteA2aAgent, exposing agents with to_a2a(), or deploying agent stacks to Vertex AI Agent Engine. Covers leaf agents with tools, functional agents that delegate, orchestrators that route, local testing with uvicorn, and phased cloud deployment.
---

# A2A Multi-Agent Development

Build multi-tier ADK agent systems using the A2A protocol, deployed to Agent Engine.

## Architecture Pattern

```
Level 1: Orchestrator (routes requests)
├── Level 2: Functional Agent A (delegates to leaf)
│   └── Level 3: Leaf Agent A (has tools, does work)
└── Level 2: Functional Agent B (delegates to leaf)
    └── Level 3: Leaf Agent B (has tools, does work)
```

**Key principle:** Leaf agents have tools. Functional agents delegate. Orchestrators route.

## Quick Reference

| Task | Pattern |
|------|---------|
| Create agent with tools | `Agent(name, model, instruction, tools=[func])` |
| Expose via A2A | `to_a2a(agent, port=8001)` |
| Connect to remote agent | `RemoteA2aAgent(name, agent_card=url)` |
| Delegate to sub-agent | `TransferToAgentTool` + `sub_agents=[remote]` |
| Deploy to Agent Engine | `vertexai.agent_engines.create(agent_engine=app)` |

## Creating Agents

### Leaf Agent (Level 3) - Has Tools

```python
from google.adk.agents.llm_agent import Agent

def get_data(user_id: str) -> dict:
    """Returns data for a user.

    Args:
        user_id: The ID of the user.
    """
    return {"status": "success", "user_id": user_id, "data": "..."}

root_agent = Agent(
    name="data_agent",
    model="gemini-3.7-flash",
    instruction="You are the Data Agent. Use `get_data` when asked for user data.",
    tools=[get_data]
)
```

### Functional Agent (Level 2) - Delegates to Leaf

```python
from google.adk.agents.llm_agent import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from typing import Optional
from typing_extensions import override
import os

def transfer_to_agent(agent_name: str, tool_context: ToolContext) -> None:
    """Transfer the question to another agent."""
    tool_context.actions.transfer_to_agent = agent_name

class TransferToAgentTool(FunctionTool):
    """Tool for agent-to-agent transfer with enum constraints."""

    def __init__(self, agent_names: list[str]):
        super().__init__(func=transfer_to_agent)
        self._agent_names = agent_names

    @override
    def _get_declaration(self) -> Optional[types.FunctionDeclaration]:
        function_decl = super()._get_declaration()
        if not function_decl:
            return function_decl

        if function_decl.parameters:
            schema = function_decl.parameters.properties.get('agent_name')
            if schema:
                schema.enum = self._agent_names

        if function_decl.parameters_json_schema:
            props = function_decl.parameters_json_schema.get('properties', {})
            if 'agent_name' in props:
                props['agent_name']['enum'] = self._agent_names

        return function_decl

# Connect to leaf agent via A2A
leaf_url = os.environ.get("LEAF_AGENT_URL", "http://localhost:8001")
if not leaf_url.endswith("json"):
    leaf_url = f"{leaf_url.rstrip('/')}/.well-known/agent.json"

leaf_remote = RemoteA2aAgent(
    name="leaf_helper",
    agent_card=leaf_url
)

transfer_tool = TransferToAgentTool(agent_names=["leaf_helper"])

root_agent = Agent(
    name="functional_agent",
    model="gemini-3.7-flash",
    instruction="""You are the Functional Agent.
    Delegate data requests to the leaf_helper.
    Always transfer when asked about data.""",
    tools=[transfer_tool],
    sub_agents=[leaf_remote]
)
```

### Orchestrator (Level 1) - Routes to Functional Agents

```python
# Connect to multiple functional agents
hr_url = os.environ.get("HR_AGENT_URL", "http://localhost:8003")
finance_url = os.environ.get("FINANCE_AGENT_URL", "http://localhost:8004")

hr_remote = RemoteA2aAgent(name="hr_helper", agent_card=f"{hr_url}/.well-known/agent.json")
finance_remote = RemoteA2aAgent(name="finance_helper", agent_card=f"{finance_url}/.well-known/agent.json")

transfer_tool = TransferToAgentTool(agent_names=["hr_helper", "finance_helper"])

root_agent = Agent(
    name="orchestrator_agent",
    model="gemini-3.7-flash",
    instruction="""You are the Orchestrator.
    - For HR/PTO questions, transfer to `hr_helper`.
    - For Finance/Report questions, transfer to `finance_helper`.
    Do not answer directly. Always delegate.""",
    tools=[transfer_tool],
    sub_agents=[hr_remote, finance_remote]
)
```

## Exposing Agents via A2A

Convert any ADK agent to an A2A-compatible ASGI app:

```python
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# Wrap agent for A2A
a2a_app = to_a2a(root_agent, port=8001)
```

Run with uvicorn:
```bash
uvicorn agent:a2a_app --host 0.0.0.0 --port 8001
```

Agent card available at: `http://localhost:8001/.well-known/agent.json`

## Local Testing Stack

Run all agents locally with threading:

```python
import threading
import uvicorn
from google.adk.a2a.utils.agent_to_a2a import to_a2a

def run_server(agent, port):
    app = to_a2a(agent, port=port)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

def start_stack():
    agents = [
        (leaf_agent_1, 8001),
        (leaf_agent_2, 8002),
        (functional_agent_1, 8003),
        (functional_agent_2, 8004),
        (orchestrator, 8005),
    ]

    for agent, port in agents:
        t = threading.Thread(target=run_server, args=(agent, port), daemon=True)
        t.start()
```

## A2A Client Testing

```python
import asyncio
from a2a.client.client_factory import ClientFactory
from a2a.client.client import ClientConfig
from a2a.types import AgentCard, Message, Part, TransportProtocol
import requests
import httpx

async def test_agent(url: str, query: str):
    # Fetch agent card
    card = AgentCard(**requests.get(f"{url}/.well-known/agent.json").json())

    # Create client
    config = ClientConfig(
        supported_transports=[TransportProtocol.jsonrpc],
        httpx_client=httpx.AsyncClient(timeout=120.0)
    )
    client = ClientFactory(config=config).create(card)

    # Send message
    request = Message(
        message_id="test-1",
        role="user",
        parts=[Part(text=query)]
    )

    async for response in client.send_message(request):
        print(response)

asyncio.run(test_agent("http://localhost:8005", "What is the PTO balance for user_123?"))
```

## Deploying to Agent Engine

### Deployment Utility

```python
from google.cloud import aiplatform
from vertexai.agent_engines import AdkApp
from google.adk.sessions import InMemorySessionService
import vertexai.agent_engines as vae

def deploy_agent(
    agent_object,
    name: str,
    project_id: str,
    location: str,
    staging_bucket: str,
    env_vars: dict = None,
    extra_packages: list = None
):
    requirements = [
        "google-cloud-aiplatform[agent_engines,a2a]",
        "google-adk[a2a]",
        "uvicorn",
        "fastapi",
        "a2a-sdk>=1.1"
    ]

    aiplatform.init(project=project_id, location=location, staging_bucket=staging_bucket)

    # Use InMemorySessionService to avoid httpx client issues
    session_service_builder = lambda **kwargs: InMemorySessionService()
    app = AdkApp(agent=agent_object, session_service_builder=session_service_builder)

    remote_agent = vae.create(
        agent_engine=app,
        display_name=name,
        requirements=requirements,
        env_vars=env_vars,
        extra_packages=extra_packages
    )

    return remote_agent
```

### Phased Deployment (Leaf → Functional → Orchestrator)

```python
import a2a
import os

# Bundle packages
a2a_path = os.path.dirname(a2a.__file__)
common_packages = ["./agent_system", a2a_path]

# Phase 1: Deploy leaf agents (no dependencies)
pto_remote = deploy_agent(pto_agent, "pto-agent", PROJECT, LOCATION, BUCKET,
                          extra_packages=common_packages)
quarterly_remote = deploy_agent(quarterly_agent, "quarterly-agent", PROJECT, LOCATION, BUCKET,
                                extra_packages=common_packages)

# Construct URLs from resource names
pto_url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/{pto_remote.resource_name}"
quarterly_url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/{quarterly_remote.resource_name}"

# Phase 2: Deploy functional agents (with leaf URLs as env vars)
hr_remote = deploy_agent(hr_agent, "hr-agent", PROJECT, LOCATION, BUCKET,
                         env_vars={"PTO_AGENT_URL": pto_url},
                         extra_packages=common_packages)
finance_remote = deploy_agent(finance_agent, "finance-agent", PROJECT, LOCATION, BUCKET,
                              env_vars={"QUARTERLY_AGENT_URL": quarterly_url},
                              extra_packages=common_packages)

# Phase 3: Deploy orchestrator (with functional agent URLs)
orch_remote = deploy_agent(orchestrator, "orchestrator", PROJECT, LOCATION, BUCKET,
                           env_vars={
                               "HR_AGENT_URL": hr_url,
                               "FINANCE_AGENT_URL": finance_url
                           },
                           extra_packages=common_packages)
```

## Advanced Topics

For detailed information on A2A protocol specifications, agent cards, transport protocols, and advanced patterns, see:

**[references/protocol.md](references/protocol.md)** - Comprehensive A2A protocol reference including:
- AgentCard schema and discovery mechanisms
- Transport protocols (JSON-RPC, SSE, HTTP/REST)
- Multi-agent communication patterns
- Security and best practices
- Advanced examples

## Environment Variables

```bash
# GCP Configuration
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_GENAI_USE_VERTEXAI="1"
export BUCKET="gs://your-staging-bucket"

# Agent URLs (for deployed agents)
export PTO_AGENT_URL="https://..."
export HR_AGENT_URL="https://..."
export FINANCE_AGENT_URL="https://..."
```

## Dependencies

```
google-adk[a2a]
google-cloud-aiplatform[agent_engines,a2a]
uvicorn
fastapi
a2a-sdk>=1.1
```

## Practical Lessons from Production

### Inline Data for Agent Engine

When deploying A2A agents to Agent Engine, the pickle process captures the entire agent graph. Any references to local filesystem files (YAML configs, data files) will fail at runtime because the Agent Engine container doesn't have those files.

**Solution**: Inline all configuration data directly in the deploy script:

```python
# BAD: Agent Engine can't read this at runtime
config = yaml.safe_load(open("config/settings.yaml"))

# GOOD: Inline everything
_RETAILER_NAME = "ValueFresh Market"
_PERSONAS = [{"id": "budget", "name": "Budget Shopper", "budget": 120}]
```

### Discovery Engine Integration

When an A2A agent needs to search document stores, use `DiscoveryEngineSearchTool` (not `VertexAiSearchTool`). The latter injects a Gemini retrieval tool that conflicts with the `transfer_to_agent` function tools used by A2A delegation.

```python
from google.adk.tools.discovery_engine_search_tool import DiscoveryEngineSearchTool
# Works with sub_agents and A2A transfer tools
```

### Registering on Discovery Engine for Streaming

An A2A agent deployed to Cloud Run can be registered as an external agent on Discovery Engine for the StreamAssist (conversational search) flow. The agent card URL becomes the connection point.

### Token Limits

Monitor input token counts carefully. A Discovery Engine with many data stores (especially workspace connectors like Gmail, Calendar, Jira) can push context above the 1M token limit. Use `data_store_specs` to restrict which stores are searched.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent card not found | Ensure URL ends with `/.well-known/agent.json` |
| Connection refused | Start leaf agents before functional agents |
| httpx client errors | Use `InMemorySessionService` in AdkApp |
| Deployment fails | Bundle `a2a` package in `extra_packages` |
| Transfer not working | Verify sub_agent name matches TransferToAgentTool enum |
| cloudpickle fails | Inline all data; no filesystem reads in agent code |
| Token overflow on engine | Restrict data stores with `data_store_specs` |
| No query methods at runtime | Redeploy; broken deployments don't self-heal |
| VertexAiSearchTool + transfers | Use `DiscoveryEngineSearchTool` instead |
