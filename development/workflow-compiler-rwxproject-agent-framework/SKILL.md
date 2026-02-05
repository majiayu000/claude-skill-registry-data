---
name: workflow-compiler
description: Compile visual workflow canvas to Google ADK Python code. Use when generating executable agent code from WorkflowCanvas data structures. Supports all ADK workflow patterns.
allowed-tools: Read, Write, Grep
---

# Workflow Compilation

Compile visual workflow canvas designs to executable Google ADK Python code.

## Input Format (WorkflowCanvas)

```typescript
interface WorkflowCanvas {
  id: string;
  name: string;
  description: string;
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  rootAgentId: string;
}

interface WorkflowNode {
  id: string;
  type: 'llm' | 'sequential' | 'parallel' | 'loop' | 'condition' | 'custom';
  position: { x: number; y: number };
  data: {
    label: string;
    config: Partial<AgentConfig>;
    children?: string[];
  };
}

interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  type: 'default' | 'conditional' | 'loop';
  data?: {
    label?: string;
    condition?: string;
    outputKey?: string;
  };
}
```

## Output Format (Python ADK Code)

### Template Structure

```python
"""
Generated workflow: {workflow_name}
Description: {workflow_description}
Generated at: {timestamp}
"""

from google.adk.agents import (
    LlmAgent,
    SequentialAgent,
    ParallelAgent,
    LoopAgent,
    BaseAgent
)
from google.adk.models.lite_llm import LiteLlm

# Agent definitions
{agent_definitions}

# Workflow composition
{workflow_composition}

# Root agent export
root_agent = {root_agent_name}
```

## Compilation Rules

### LLM Agent Node

```python
# Input node
{
  "id": "research",
  "type": "llm",
  "data": {
    "label": "ResearchAgent",
    "config": {
      "modelConfig": {"provider": "gemini", "model": "gemini-2.5-flash"},
      "instruction": "Research the given topic",
      "outputKey": "research_results"
    }
  }
}

# Output code
research_agent = LlmAgent(
    name="ResearchAgent",
    model="gemini-2.5-flash",
    instruction="Research the given topic",
    output_key="research_results"
)
```

### Sequential Agent Node

```python
# Input: Container with ordered children
{
  "id": "pipeline",
  "type": "sequential",
  "data": {
    "label": "DataPipeline",
    "children": ["validate", "process", "report"]
  }
}

# Output code
data_pipeline = SequentialAgent(
    name="DataPipeline",
    sub_agents=[
        validate_agent,
        process_agent,
        report_agent
    ]
)
```

### Parallel Agent Node

```python
# Input: Container with concurrent children
{
  "id": "gatherer",
  "type": "parallel",
  "data": {
    "label": "InfoGatherer",
    "children": ["web_search", "db_search", "api_fetch"]
  }
}

# Output code
info_gatherer = ParallelAgent(
    name="InfoGatherer",
    sub_agents=[
        web_search_agent,  # output_key="web_results"
        db_search_agent,   # output_key="db_results"
        api_fetch_agent    # output_key="api_results"
    ]
)
```

### Loop Agent Node

```python
# Input: Iterative refinement
{
  "id": "refiner",
  "type": "loop",
  "data": {
    "label": "ContentRefiner",
    "config": {"maxIterations": 3},
    "children": ["critic", "reviser"]
  }
}

# Output code
content_refiner = LoopAgent(
    name="ContentRefiner",
    max_iterations=3,
    sub_agents=[
        critic_agent,
        reviser_agent
    ]
)
```

### Conditional Node (Custom)

```python
# Output: Custom BaseAgent subclass
class ConditionalRouter(BaseAgent):
    """Custom conditional routing based on state."""

    positive_agent: LlmAgent
    negative_agent: LlmAgent

    async def _run_async_impl(self, ctx):
        result = ctx.session.state.get("analysis_result", "")

        if "positive" in result.lower():
            async for event in self.positive_agent.run_async(ctx):
                yield event
        else:
            async for event in self.negative_agent.run_async(ctx):
                yield event
```

## Multi-Model Support

```python
# Gemini (native)
model="gemini-2.5-flash"

# OpenAI via LiteLLM
model=LiteLlm(model="openai/gpt-4o")

# Anthropic via LiteLLM
model=LiteLlm(model="anthropic/claude-3-haiku-20240307")

# Ollama via LiteLLM
model=LiteLlm(model="ollama_chat/llama3.2")
```

## Validation Before Compilation

1. **Root agent exists**: `rootAgentId` points to valid node
2. **No orphan nodes**: All nodes reachable from root
3. **No cycles**: DAG structure (except loops)
4. **Children exist**: All `children[]` IDs are valid
5. **Output keys unique**: Parallel agents have distinct keys

## Example Full Compilation

### Input Canvas

```json
{
  "id": "workflow-1",
  "name": "ResearchWorkflow",
  "description": "Gather and synthesize research",
  "rootAgentId": "main",
  "nodes": [
    {"id": "main", "type": "sequential", "data": {"label": "MainWorkflow", "children": ["gather", "synthesize"]}},
    {"id": "gather", "type": "parallel", "data": {"label": "InfoGatherer", "children": ["web", "db"]}},
    {"id": "web", "type": "llm", "data": {"label": "WebSearch", "config": {"outputKey": "web_results"}}},
    {"id": "db", "type": "llm", "data": {"label": "DBSearch", "config": {"outputKey": "db_results"}}},
    {"id": "synthesize", "type": "llm", "data": {"label": "Synthesizer", "config": {"instruction": "Combine {web_results} and {db_results}"}}}
  ]
}
```

### Output Code

```python
"""
Generated workflow: ResearchWorkflow
Description: Gather and synthesize research
"""

from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent

web_search = LlmAgent(
    name="WebSearch",
    model="gemini-2.5-flash",
    instruction="Search the web for relevant information",
    output_key="web_results"
)

db_search = LlmAgent(
    name="DBSearch",
    model="gemini-2.5-flash",
    instruction="Search the database for relevant records",
    output_key="db_results"
)

info_gatherer = ParallelAgent(
    name="InfoGatherer",
    sub_agents=[web_search, db_search]
)

synthesizer = LlmAgent(
    name="Synthesizer",
    model="gemini-2.5-flash",
    instruction="Combine {web_results} and {db_results} into a comprehensive summary"
)

root_agent = SequentialAgent(
    name="MainWorkflow",
    sub_agents=[info_gatherer, synthesizer]
)
```
