---
name: adk
description: Comprehensive guide for building AI agents using Google's Agent Development Kit (ADK). Use when building agentic systems, orchestrating multi-agent workflows, creating AI assistants with custom tools, implementing LLM-powered applications, or working with Google Gemini models. Covers agent types (LlmAgent, SequentialAgent, ParallelAgent, LoopAgent), tool integration (FunctionTool, built-in tools, MCP), session management, deployment strategies, and multi-agent coordination patterns.
---

# Agent Development Kit (ADK)

## Overview

This skill provides comprehensive guidance for building sophisticated AI agents using Google's Agent Development Kit (ADK), an open-source Python framework optimized for Gemini models but supporting any LLM. ADK enables code-first agent development with modular multi-agent systems, rich tool ecosystems, and flexible deployment options.

## How to Use This Skill

**Quick Start:** Follow the Quick Start section below for basic agent setup

**Learning & Building:**
- **Patterns & Examples:** See SKILL.md sections (Tool Integration, Multi-Agent Coordination, Common Patterns)
- **Code Snippets:** `references/examples.md` for quick copy-paste examples
- **Working Samples:** `samples/adk-samples/` for complete runnable examples
- **API Reference:** `references/core_concepts.md` for condensed API docs or `docs/adk-docs/docs/` for complete documentation

**A2A Protocol:**
- **Quick Guide:** See "Agent as Tool" and "Multi-Agent Coordination" sections in SKILL.md
- **Protocol Spec:** `samples/A2A/docs/specification.md`
- **Samples:** `samples/a2a-samples/samples/python/` for client/server examples
- **Detailed Docs:** `docs/adk-docs/docs/a2a/` for ADK-specific A2A integration

**Production Deployment:**
- **Quick Guide:** `references/deployment_best_practices.md`
- **Complete Guides:** `docs/adk-docs/docs/deploy/` for Cloud Run, Vertex AI, GKE

## When to Use ADK

Build ADK agents when you need:
- **Multi-step agentic workflows** with planning, tool use, and dynamic decision-making
- **Multi-agent systems** with specialized agents coordinating on complex tasks
- **Custom tools** that extend LLM capabilities with external APIs, databases, or computations
- **Production-grade deployment** on Google Cloud (Cloud Run, Vertex AI Agent Engine)
- **Flexible orchestration** combining deterministic workflows (Sequential, Parallel, Loop) with LLM-driven routing
- **Session persistence** and conversation memory across multiple turns

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# Install ADK
pip install google-adk
```

### Environment Setup

Create `.env` file with your API credentials:

```bash
# Option 1: Google AI Studio (free tier)
GOOGLE_API_KEY=your-api-key

# Option 2: Vertex AI (production)
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

### Minimal Agent

```python
# agent.py
from google.adk.agents import Agent

root_agent = Agent(  # Must be named 'root_agent'
    name='assistant',
    model='gemini-2.5-flash',
    description='A helpful AI assistant',
    instruction='Help users with their questions in a clear, friendly manner'
)
```

### Running Your Agent

```bash
# Interactive CLI
adk run agent_module.root_agent "Hello, how can you help me?"

# Web UI (browser-based testing)
adk web  # Access at http://localhost:8000

# API Server (REST endpoint)
adk api_server  # POST /run at http://localhost:8080
```

## Core Agent Types

### LlmAgent (Agent)
Powered by LLMs for dynamic reasoning, tool selection, and response generation.

**Key Configuration:**
```python
from google.adk.agents import LlmAgent

agent = LlmAgent(
    name='weather_bot',                    # Unique identifier
    model='gemini-2.5-flash',              # Model name
    description='Provides weather info',   # For delegation routing
    instruction='Use tools to get weather', # System prompt
    tools=[get_weather_tool],              # Available tools
    output_key='weather_data',             # Save response to state
    sub_agents=[specialist1, specialist2]  # Child agents
)
```

**When to Use:**
- Need flexible, language-driven behavior
- Dynamic tool selection based on context
- Coordination and routing to sub-agents
- Natural language understanding and generation

### SequentialAgent
Executes sub-agents in strict order. Deterministic flow without LLM.

**Example:**
```python
from google.adk.agents import SequentialAgent, LlmAgent

pipeline = SequentialAgent(
    name='content_pipeline',
    sub_agents=[
        LlmAgent(name='writer', output_key='draft'),
        LlmAgent(name='reviewer', output_key='feedback'),
        LlmAgent(name='reviser')  # Final output
    ]
)
```

**When to Use:**
- Fixed, predictable process steps
- Each step depends on previous results
- Data pipelines (ETL, processing, reporting)

### ParallelAgent
Executes sub-agents concurrently. Returns when all complete.

**Example:**
```python
from google.adk.agents import ParallelAgent

parallel = ParallelAgent(
    name='multi_source_fetch',
    sub_agents=[
        LlmAgent(name='fetch_api1', output_key='data1'),
        LlmAgent(name='fetch_api2', output_key='data2'),
        LlmAgent(name='fetch_api3', output_key='data3')
    ]
)
```

**When to Use:**
- Independent tasks that can run simultaneously
- Multiple data sources to query
- Performance-critical parallel operations

### LoopAgent
Repeats sub-agents until termination condition met.

**Example:**
```python
from google.adk.agents import LoopAgent

def is_approved(context) -> bool:
    return context.state.get('status') == 'approved'

loop = LoopAgent(
    name='refinement_loop',
    sub_agents=[generator, critic, reviser],
    termination_condition=is_approved,
    max_iterations=5
)
```

**When to Use:**
- Iterative refinement processes
- Retry logic with dynamic conditions
- Quality-driven loops (generate until threshold met)

## Tool Integration

### Function Tools

Convert Python functions to agent tools. ADK generates schema automatically from function signature.

**Critical Requirements:**
1. **Docstring:** LLM uses this to understand when/how to use the tool (MOST IMPORTANT!)
2. **Type hints:** Required for parameter schema generation
3. **Return dict:** Preferred for structured responses

**Example:**
```python
def get_weather(city: str, units: str = "celsius") -> dict:
    """
    Get current weather for a specified city.
    
    Use this tool when users ask about weather, temperature, or conditions.
    
    Args:
        city: City name (e.g., "San Francisco", "Tokyo")
        units: Temperature units - "celsius" or "fahrenheit"
    
    Returns:
        dict with temperature, condition, humidity, wind_speed
    """
    # API call or mock implementation
    return {
        "temperature": 22,
        "condition": "sunny",
        "humidity": 65,
        "city": city
    }

agent = Agent(
    name='weather_agent',
    tools=[get_weather]  # ADK auto-wraps as FunctionTool
)
```

**Best Practices:**
- **Descriptive docstrings:** Explain what, when, and why
- **Clear parameter names:** Use descriptive, obvious names
- **Type hints:** Always include for all parameters
- **Structured returns:** Return dicts with meaningful keys
- **Error handling:** Return error info in dict format

### Built-in Tools

**GoogleSearchTool:**
```python
from google.adk.tools import GoogleSearchTool

agent = Agent(
    tools=[GoogleSearchTool()]
)
```

**CodeExecutionTool:**
```python
from google.adk.tools import CodeExecutionTool

agent = Agent(
    tools=[CodeExecutionTool()]  # Execute Python in sandbox
)
```

**GoogleRagEngineTool:**
```python
from google.adk.tools import GoogleRagEngineTool

agent = Agent(
    tools=[GoogleRagEngineTool(
        data_store_id="your-data-store-id",
        project_id="your-project"
    )]
)
```

### Agent as Tool

Use specialized agents as tools for delegation:

```python
from google.adk.tools import AgentTool

specialist = LlmAgent(
    name='data_analyst',
    description='Analyzes numerical data and creates visualizations',
    instruction='Perform statistical analysis on provided data'
)

coordinator = LlmAgent(
    name='coordinator',
    tools=[AgentTool(specialist)]  # Specialist available as tool
)
```

### MCP Tools

Integrate Model Context Protocol servers as tools:

```python
from google.adk.tools.mcp import MCPToolset

mcp_tools = MCPToolset(
    server_config={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    },
    tool_filter=["read_file", "list_directory"]  # Optional: specific tools
)

agent = Agent(tools=[mcp_tools])
```

## Multi-Agent Coordination

### Coordinator Pattern

Central agent routes requests to specialists:

```python
greeter = LlmAgent(
    name='greeter',
    description='Handles greetings, introductions, and farewells',
    instruction='Greet users warmly and professionally'
)

task_executor = LlmAgent(
    name='executor',
    description='Executes user tasks and provides solutions',
    instruction='Help users accomplish their requested tasks'
)

coordinator = LlmAgent(
    name='coordinator',
    description='Routes user requests to appropriate specialist',
    instruction="""Analyze the user's request and transfer to:
    - greeter: For greetings, hellos, goodbyes
    - executor: For task requests, questions, help
    
    Transfer immediately to the appropriate agent.""",
    sub_agents=[greeter, task_executor]
)

root_agent = coordinator
```

### Pipeline Pattern

Sequential data processing with state passing:

```python
validator = LlmAgent(
    name='validator',
    instruction='Validate the input data',
    output_key='validation_status'
)

processor = LlmAgent(
    name='processor',
    instruction='Process data if {validation_status} is valid',
    output_key='result'
)

reporter = LlmAgent(
    name='reporter',
    instruction='Generate report from {result}'
)

root_agent = SequentialAgent(
    name='data_pipeline',
    sub_agents=[validator, processor, reporter]
)
```

### Fan-Out/Gather Pattern

Parallel execution with aggregation:

```python
# Fan-out: Parallel research
parallel_research = ParallelAgent(
    name='researchers',
    sub_agents=[
        LlmAgent(name='tech_research', output_key='tech_data'),
        LlmAgent(name='market_research', output_key='market_data'),
        LlmAgent(name='competitor_research', output_key='competitor_data')
    ]
)

# Gather: Synthesize results
synthesizer = LlmAgent(
    name='synthesizer',
    instruction='Synthesize: {tech_data}, {market_data}, {competitor_data}'
)

root_agent = SequentialAgent(
    name='research_workflow',
    sub_agents=[parallel_research, synthesizer]
)
```

## Session & State Management

### Shared State

Primary communication mechanism between agents:

```python
# Agent A writes to state
agent_a = LlmAgent(
    name='fetcher',
    output_key='raw_data'  # Saves response to state['raw_data']
)

# Agent B reads from state via instruction templating
agent_b = LlmAgent(
    name='processor',
    instruction='Process this data: {raw_data}'  # Reads state['raw_data']
)
```

**State Namespaces:**
- Persistent: `state['key']` - survives across conversation turns
- Temporary: `state['temp:key']` - cleared after current turn

### Session Services

**Development (InMemorySessionService):**
```python
from google.adk.sessions import InMemorySessionService
session_service = InMemorySessionService()  # Data lost on restart
```

**Production (VertexAiSessionService):**
```python
from google.adk.sessions import VertexAiSessionService
session_service = VertexAiSessionService(
    project_id="your-project",
    location="us-central1"
)
```

## Deployment

### Local Testing

```bash
# Terminal CLI
adk run agent_module.root_agent "Your query"

# Web UI (interactive testing)
adk web

# API Server (REST endpoint)
adk api_server
```

### Cloud Run

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["adk", "api_server", "--host", "0.0.0.0", "--port", "8080"]
```

Deploy:
```bash
gcloud run deploy my-agent \
  --source . \
  --platform managed \
  --region us-central1
```

### Vertex AI Agent Engine

```python
from google.cloud import aiplatform

aiplatform.init(project="your-project", location="us-central1")

reasoning_engine = aiplatform.ReasoningEngine.create(
    reasoning_engine_source="agent_module",
    requirements=["google-adk"],
    display_name="my-agent"
)
```

## Common Patterns & Best Practices

### Effective Instructions

**Good:**
```python
instruction="""You are a data analyst. When users provide data:
1. Use analyze_data tool to compute statistics
2. Use create_visualization tool for charts
3. Present findings with key insights and recommendations"""
```

**Bad:**
```python
instruction="Help with data"  # Too vague
```

### Tool Documentation

**Excellent docstring:**
```python
def search_database(query: str, max_results: int = 10) -> dict:
    """
    Search company knowledge base for relevant information.
    
    Use when users ask about:
    - Company policies, procedures, guidelines
    - Product documentation or specifications
    - Historical project information
    
    Args:
        query: Natural language search (e.g., "vacation policy")
        max_results: Number of results (default 10, max 50)
    
    Returns:
        dict with results (list), total_count (int), search_time_ms (int)
    """
```

### Error Handling in Tools

```python
def call_api(endpoint: str) -> dict:
    """Call external API with robust error handling"""
    try:
        response = requests.get(f"https://api.example.com/{endpoint}")
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.HTTPError as e:
        return {
            "success": False,
            "error": f"API error {e.response.status_code}",
            "suggestion": "Verify endpoint and retry"
        }
    except requests.RequestException as e:
        return {
            "success": False,
            "error": "Network error",
            "suggestion": "Check connectivity and retry"
        }
```

### State Management

```python
# Write state
context.state['user_preferences'] = {'theme': 'dark'}
context.state['temp:current_step'] = 'validation'  # Temporary

# Read state in instructions via templating
instruction="Process {user_preferences} for step {current_step}"

# Access in tools
def my_tool(tool_context):
    prefs = tool_context.state.get('user_preferences', {})
```

## Documentation

Official ADK and A2A documentation cloned locally:

### Core Documentation
**Base:** `.claude/skills/adk/docs/adk-docs/docs/`

**Key Topics:**
- **Agents:** `agents/` - LlmAgent, workflow agents (Sequential, Parallel, Loop), multi-agent patterns, custom agents
- **Tools:** `tools/` - Function tools, built-in tools, MCP tools, authentication, third-party integrations
- **A2A Protocol:** `a2a/` - Exposing agents via A2A, consuming remote agents, quickstarts
- **Streaming:** `streaming/` - Custom WebSocket streaming, bidirectional audio/video, configuration
- **Sessions & State:** `sessions/` - State management, memory, session services, express mode
- **Deployment:** `deploy/` - Cloud Run, Vertex AI Agent Engine, GKE deployment guides
- **Get Started:** `get-started/` - Installation, quickstart, language-specific guides
- **Context:** `context/` - Caching, compaction for managing token limits
- **MCP:** `mcp/` - Model Context Protocol integration
- **Safety:** `safety/` - Content filtering and safety configurations
- **Observability:** `observability/` - Logging, monitoring, debugging

**Use when:** Need detailed API reference, advanced patterns, deployment strategies, or troubleshooting

### A2A Protocol Specification
**Base:** `.claude/skills/adk/samples/A2A/docs/`

**Key Topics:**
- `specification.md` - Complete A2A protocol specification
- `sdk/python/` - Python SDK documentation for A2A
- `topics/` - Protocol design topics and patterns
- `tutorials/` - Step-by-step A2A implementation guides

**Use when:** Implementing A2A protocol, multi-framework orchestration, custom agent communication

## Sample Code

Cloned samples available locally for reference:

### ADK Samples
**Location:** `.claude/skills/adk/samples/adk-samples/python/agents/`

Key examples:
- `realtime-conversational-agent/` - Bidirectional audio/video streaming with Gemini Live API
- `customer-service/` - Multi-agent coordinator pattern with specialists
- `travel-concierge/` - Sequential pipeline with state passing
- `RAG/` - Google RAG Engine integration
- `data-science/` - Parallel agent execution patterns
- See `README.md` in agents directory for complete catalog

### A2A Protocol Samples
**Location:** `.claude/skills/adk/samples/a2a-samples/samples/python/`

Key directories:
- `agents/` - A2A server implementations (ADK, LangGraph, CrewAI, AG2, etc.)
  - `adk_expense_reimbursement/` - ADK agent exposed via A2A
  - `langgraph/` - LangGraph agent with A2A protocol
  - `birthday_planner_adk/` - Multi-agent ADK system with A2A
- `hosts/` - A2A client/orchestrator patterns
  - `multiagent/` - Orchestrating multiple remote A2A agents
  - `a2a_multiagent_host/` - Host coordinating remote agents
  - `cli/` - Command-line A2A client

**Use when:** Need working code examples, want to see patterns in action

## Quick Reference (Skill-Specific)

Condensed reference guides in this skill for quick lookup:

### references/core_concepts.md
Condensed API reference covering key concepts:
- All agent types with parameters and examples
- Tool system architecture and implementation
- Multi-agent patterns and communication
- Session/state management essentials
- Model configuration and authentication
- Common architectural patterns

**When to use:** Quick lookup for API signatures, common patterns. For detailed API docs, see `docs/adk-docs/docs/`

### references/deployment_best_practices.md
Production deployment essentials:
- Development workflow and project structure
- Deployment options (Cloud Run, Vertex AI, containers)
- Performance optimization strategies
- Security best practices
- Testing and debugging techniques
- Common pitfalls and solutions

**When to use:** Quick deployment guidance. For complete deployment guides, see `docs/adk-docs/docs/deploy/`

### references/examples.md
Quick-start code snippets:
- Minimal agent setup
- Agents with custom tools
- Sequential pipelines
- Parallel data gathering
- Coordinator patterns
- Loop-based refinement
- Error handling patterns

**When to use:** Quick code snippets. For complete working examples, see `samples/adk-samples/`

## Decision Guide

**Choose ADK when:**
- Building complex agentic workflows requiring multi-step reasoning
- Need multiple specialized agents coordinating on tasks
- Require production-grade deployment on Google Cloud
- Want flexibility to use Gemini, GPT, Claude, or other models
- Need persistent session management and conversation memory

**Consider alternatives when:**
- Simple single-prompt LLM calls (use SDK directly)
- No need for tools or multi-agent coordination
- Primarily using non-Google models (though ADK supports via LiteLLM)
- Seeking managed agentic platform (consider Vertex AI agents directly)

**ADK vs Other Frameworks:**
- **LangChain:** ADK is more code-first, less abstraction, tighter Google integration
- **CrewAI:** ADK offers more flexible orchestration, better Gemini integration
- **AutoGen:** ADK focuses on production deployment, modular architecture

## Key Differences from Other Agent Frameworks

ADK's unique advantages:
- **Code-first:** Define agents in pure Python with minimal abstractions
- **Flexible orchestration:** Mix deterministic workflows with LLM-driven routing
- **Production-ready:** Native Vertex AI integration, session persistence, streaming
- **Modular:** Compose agents hierarchically with clear separation of concerns
- **Tool ecosystem:** Seamless integration with Google services, MCP, LangChain tools
