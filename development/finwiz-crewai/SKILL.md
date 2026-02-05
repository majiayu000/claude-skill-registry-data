---
name: finwiz-crewai
description: "CrewAI development standards for FinWiz including agent configuration, task setup, Flow patterns, and performance optimization. Use when working with CrewAI crews, agents, tasks, or Flows."
allowed-tools: ["Read", "Edit", "Bash"]
---

# FinWiz CrewAI Development Standards

Apply these standards when working with CrewAI crews, agents, tasks, and Flows in FinWiz.

## Crew Structure (Required)

All crews must follow this exact structure:

```
src/finwiz/crews/{crew_name}/
├── {crew_name}.py          # @agent, @task, @crew decorators
└── config/
    ├── agents.yaml         # Agent configurations  
    └── tasks.yaml          # Task definitions
```

## Agent Configuration Patterns

### Standard Agent Pattern

```python
@agent
def analyst(self) -> Agent:
    return Agent(
        config=self.agents_config["analyst"],
        tools=get_stock_crew_tools(include_rag=True),
        reasoning=True,              # For complex analysis
        max_reasoning_attempts=3,    # Prevent infinite loops
        allow_delegation=False,      # Only for coordinators
        verbose=True
    )
```

### Final Reporter Pattern (CRITICAL)

```python
from finwiz.utils.agent_validators import final_reporter

@final_reporter  # Enforces empty tools
@agent
def investment_reporter(self) -> Agent:
    return Agent(
        config=self.agents_config['investment_reporter'],
        tools=[],  # MUST be empty - enforced by decorator
        verbose=True
    )
```

## Task Configuration

### Required Task Features

```yaml
# config/tasks.yaml
stock_analysis_task:
  description: "Analyze stock with quantitative metrics and risk assessment"
  expected_output: "Structured analysis with risk assessment and technical indicators"
  output_pydantic: "TenKInsight"  # Use FinWiz schema
  output_json: true               # Generate machine-readable appendix
  agent: stock_analyst
  async_execution: true           # Enable for I/O-bound tasks
```

### JSON Output Requirements (CRITICAL)

Every task with `output_json: true` MUST include:

```yaml
analysis_task:
  description: >
    Analyze {ticker} with quantitative metrics

    🚨 JSON OUTPUT REQUIREMENTS 🚨
    - Output MUST be ONLY valid JSON
    - Your ENTIRE response must be a single JSON object
    - Do NOT include any text outside the JSON
    - NO trailing commas in JSON
```

## Flow Architecture (CRITICAL)

### Structured State Pattern

```python
from pydantic import BaseModel
from crewai.flow import Flow, listen, start

class FinwizState(BaseModel):
    """Type-safe state with validation."""
    analysis_results: Dict[str, Any] = {}
    processing_success: bool = False

class FinwizFlow(Flow[FinwizState]):
    @start()
    def initialize(self) -> dict[str, Any]:
        self.state.processing_success = True
        return {"status": "initialized"}

    @listen(initialize)
    def analyze_data(self, data: dict[str, Any]) -> dict[str, Any]:
        # Direct crew instantiation (CrewAI Flow standard)
        crew = StockCrew()
        result = crew.crew().kickoff(inputs={"ticker": "AAPL"})
        
        # Update structured state
        self.state.analysis_results = result.raw
        
        # REQUIRED: Return for downstream methods
        return {"results": result.raw}
```

### Flow Rules (NON-NEGOTIABLE)

- ✅ Use `Flow[PydanticModel]` for type safety
- ✅ All Flow methods return `dict[str, Any]`
- ✅ Access state via `self.state.field_name`
- ❌ NEVER use `self.inputs` (deprecated, error-prone)

## Performance Optimization

### Agent Reasoning Decision Matrix

| Feature | Enable When | Disable When | Cost per Use |
|---------|-------------|--------------|--------------|
| `reasoning=True` | Complex multi-step, error recovery | Simple validation, high-volume | 5-15s, 1-3 calls |
| `planning=True` | 4+ agents, 6+ tasks, ≤3 runs | High-volume, single agent | Overhead × count |
| `allow_delegation=True` | Coordinators, multi-agent | Specialists, reporters | 5-15s per delegation |

### High-Volume Execution Pattern

```python
# Deep analysis per holding (runs 66+ times)
crew = Crew(
    agents=[analyst],  # Single agent
    tasks=self.tasks,  # Simple workflow
    planning=False,    # Avoid overhead
    reasoning=False,   # Fast execution
    max_rpm=20
)
```

## Critical Anti-Patterns

❌ **Flow State Management**:

- Using `self.inputs` instead of `self.state`
- Flow methods not returning `dict[str, Any]`
- Missing parameter reception in listeners

❌ **Agent Configuration**:

- Final reporters with non-empty tools
- Missing `max_reasoning_attempts` when reasoning enabled
- Enabling reasoning for high-volume executions (66+ runs)

❌ **Task Setup**:

- Missing `output_pydantic` with FinWiz schemas
- Async final task (must be synchronous)
- Hardcoded tool lists (use tool factories)

## Tool Factory Usage

```python
# Get standardized tool set
tools = get_stock_crew_tools(
    include_rag=True,           # Include RAG tools
    include_quantitative=True,  # Include quantitative analysis
    collection_suffix="stock"   # RAG collection suffix
)
```

## Common Issues & Fixes

### CrewAI Agent Input Loops

1. Check `max_reasoning_attempts` is set (default: 3)
2. Ensure task description repeats `{ticker}` explicitly
3. Verify `reasoning=False` for high-volume executions

### JSON Serialization Errors

```python
# Always use default=str
json.dumps(data, default=str)
# Or use Pydantic
model.model_dump_json(indent=2)
```

## Compliance Checklist

Before deploying CrewAI code:

- [ ] **Structured State**: Use `Flow[PydanticModel]` pattern
- [ ] **Method Returns**: All Flow methods return `dict[str, Any]`
- [ ] **Final Reporters**: Empty tools list with `@final_reporter`
- [ ] **Performance**: Consider execution volume for reasoning/planning
- [ ] **Tool Factories**: Use standardized tool assignment
- [ ] **JSON Output**: Include requirements in task descriptions
- [ ] **Rate Limiting**: Configure `max_rpm=20`

Apply these patterns consistently across all CrewAI implementations in FinWiz.
