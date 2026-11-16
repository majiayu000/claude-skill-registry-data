---
name: smolagents
description: Build lightweight AI agents with HuggingFace Smolagents — use CodeAgent (writes Python to act) or ToolCallingAgent (JSON tool calls), add built-in or custom Tools, orchestrate multi-agent pipelines with ManagedAgent, and run locally or via HF Inference API.
triggers:
  - "smolagents"
  - "smol agents"
  - "huggingface agents"
  - "code agent smolagents"
  - "smolagents tool"
  - "smolagents codeagent"
  - "smolagents toolcallingagent"
  - "smolagents managed agent"
  - "smolagents multi agent"
  - "hf agent framework"
  - "smolagents web search"
  - "transformers agents"
do_not_use_for:
  - Complex multi-agent crews with roles — use crewai instead
  - State graph agents — use langgraph instead
  - Workflow automation — use n8n-automation instead
see_also:
  - crewai
  - langgraph
  - pydantic-ai
---

# Smolagents — Lightweight HuggingFace Agents

**Source:** huggingface/smolagents (Apache 2.0) — minimal, fast, code-first agent framework

## Why Smolagents

- **CodeAgent**: writes and executes Python code as actions (more flexible than JSON tool calls)
- **Tiny footprint**: ~1K lines of core code, easy to understand and customize
- **HF-native**: works with Transformers, Inference API, Hub models
- **Multi-agent**: orchestrate agents calling other agents via `ManagedAgent`

## Install

```bash
pip install smolagents
# Optional extras
pip install smolagents[transformers]  # local models
pip install smolagents[gradio]        # Gradio UI
pip install smolagents[vision]        # multimodal
pip install smolagents[toolkit]       # built-in tools
```

## Quick Start

```python
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=HfApiModel("Qwen/Qwen2.5-72B-Instruct"),
)

result = agent.run("What are the top 3 AI news stories today?")
print(result)
```

## Models

```python
from smolagents import (
    HfApiModel,           # HuggingFace Inference API
    LiteLLMModel,         # 100+ providers via LiteLLM
    TransformersModel,    # local Transformers model
    OpenAIServerModel,    # any OpenAI-compatible endpoint
    AmazonBedrockServerModel,
)

# HuggingFace Inference API (free tier available)
model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct")

# Claude via LiteLLM
model = LiteLLMModel("anthropic/claude-sonnet-4-5", api_key="your-key")

# OpenAI
model = LiteLLMModel("openai/gpt-4o")

# Local with Transformers
model = TransformersModel(
    model_id="Qwen/Qwen2.5-7B-Instruct",
    device_map="auto",
    torch_dtype="bfloat16",
)

# Ollama (OpenAI-compatible)
model = OpenAIServerModel(
    model_id="llama3.2",
    api_base="http://localhost:11434/v1",
    api_key="ollama",
)
```

## Agent Types

### CodeAgent (default — recommended)

Writes Python code as actions. More flexible, can do multi-step computation.

```python
from smolagents import CodeAgent, LiteLLMModel

agent = CodeAgent(
    tools=[],
    model=LiteLLMModel("anthropic/claude-sonnet-4-5"),
    max_steps=10,
    verbosity_level=2,  # 0=silent, 1=steps, 2=full
)

# Agent writes and executes Python code to answer
result = agent.run("Calculate the compound interest on $10,000 at 5% for 10 years")
print(result)
```

### ToolCallingAgent (JSON tool calls)

Uses standard function-calling API. More predictable, less flexible.

```python
from smolagents import ToolCallingAgent, DuckDuckGoSearchTool, LiteLLMModel

agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool()],
    model=LiteLLMModel("anthropic/claude-sonnet-4-5"),
)

result = agent.run("Search for the latest news about LLMs")
```

## Built-in Tools

```python
from smolagents import (
    DuckDuckGoSearchTool,     # web search
    WikipediaSearchTool,      # Wikipedia
    VisitWebpageTool,         # fetch web page content
    PythonInterpreterTool,    # run Python code (for ToolCallingAgent)
    FinalAnswerTool,          # explicit answer tool
    UserInputTool,            # ask user for input
    SpeechToTextTool,         # transcribe audio
    TextToImageTool,          # generate image
)

# Combine tools
agent = CodeAgent(
    tools=[
        DuckDuckGoSearchTool(),
        VisitWebpageTool(),
        WikipediaSearchTool(),
    ],
    model=LiteLLMModel("anthropic/claude-sonnet-4-5"),
)
```

## Custom Tools

### Decorator style (simplest)

```python
from smolagents import tool

@tool
def get_stock_price(ticker: str) -> str:
    """
    Get the current stock price for a ticker symbol.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
    """
    # your implementation
    price = fetch_price(ticker)
    return f"{ticker}: ${price:.2f}"

agent = CodeAgent(tools=[get_stock_price], model=LiteLLMModel("anthropic/claude-sonnet-4-5"))
result = agent.run("What is Apple's current stock price?")
```

### Class style (for complex tools)

```python
from smolagents import Tool

class DatabaseQueryTool(Tool):
    name = "database_query"
    description = "Execute a SQL query against the company database"
    inputs = {
        "query": {
            "type": "string",
            "description": "SQL query to execute (SELECT only)",
        }
    }
    output_type = "string"

    def __init__(self, connection_string: str):
        super().__init__()
        self.conn = connect(connection_string)

    def forward(self, query: str) -> str:
        if not query.strip().upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries allowed")
        results = self.conn.execute(query).fetchall()
        return str(results)

db_tool = DatabaseQueryTool("postgresql://localhost/mydb")
agent = CodeAgent(tools=[db_tool], model=LiteLLMModel("anthropic/claude-sonnet-4-5"))
```

## Multi-Agent Orchestration

```python
from smolagents import CodeAgent, ManagedAgent, DuckDuckGoSearchTool, LiteLLMModel

model = LiteLLMModel("anthropic/claude-sonnet-4-5")

# Specialized web research agent
web_agent = CodeAgent(
    tools=[DuckDuckGoSearchTool(), VisitWebpageTool()],
    model=model,
    name="web_researcher",
    description="Expert at finding information on the web",
)

# Wrap it as a managed agent (callable by orchestrator)
managed_web = ManagedAgent(
    agent=web_agent,
    name="web_researcher",
    description="Use this agent to search the web for information",
)

# Orchestrator calls managed agents as tools
orchestrator = CodeAgent(
    tools=[managed_web],
    model=model,
)

result = orchestrator.run(
    "Research AI trends in 2025 and write a comprehensive report"
)
```

## Vision / Multimodal

```python
from smolagents import CodeAgent, LiteLLMModel
from PIL import Image

model = LiteLLMModel("anthropic/claude-opus-4-5")

agent = CodeAgent(tools=[], model=model)

# Pass image as input
image = Image.open("chart.png")
result = agent.run(
    "Analyze this chart and extract the key data points",
    images=[image],
)
```

## Memory / Context

```python
from smolagents import CodeAgent, LiteLLMModel

agent = CodeAgent(tools=[], model=LiteLLMModel("anthropic/claude-sonnet-4-5"))

# First run
agent.run("My name is Alice and I work in AI")

# Continue — agent has memory of previous run
result = agent.run("What do you know about me?")

# Reset memory
agent.memory.reset()
```

## Gradio UI

```python
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, GradioUI

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=LiteLLMModel("anthropic/claude-sonnet-4-5"),
)

GradioUI(agent).launch()
```

## Sandbox Safety (Docker/E2B)

```python
from smolagents import CodeAgent, LiteLLMModel, E2BSandbox

# Run code in isolated E2B sandbox
agent = CodeAgent(
    tools=[],
    model=LiteLLMModel("anthropic/claude-sonnet-4-5"),
    executor_type="e2b",  # requires e2b API key
)

# Or local Docker sandbox
from smolagents import LocalPythonInterpreter
agent = CodeAgent(
    tools=[],
    model=LiteLLMModel("anthropic/claude-sonnet-4-5"),
    executor_type="local",
    additional_authorized_imports=["pandas", "numpy", "matplotlib"],
)
```

## Anti-Fake-Pass Checks

- [ ] `CodeAgent` writes + executes Python — different from `ToolCallingAgent` which uses JSON
- [ ] `@tool` docstring format matters: first line = description, then `Args:` block
- [ ] `ManagedAgent` wraps an agent to make it callable as a tool by the orchestrator
- [ ] `additional_authorized_imports` needed for non-stdlib packages in local executor
- [ ] `agent.run()` returns the final answer string, not a structured object
- [ ] `verbosity_level=2` shows intermediate code steps — useful for debugging
- [ ] Memory is per-agent-instance; create new instance or call `.memory.reset()` to clear
