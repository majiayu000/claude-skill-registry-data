---
name: crewai
description: Build multi-agent pipelines with CrewAI — define Agents with roles/goals/backstory, assemble them into a Crew, assign Tasks sequentially or in parallel, and wire LLM + tools per agent.
triggers:
  - "crewai"
  - "crew ai"
  - "multi agent crew"
  - "crew of agents"
  - "agent role goal backstory"
  - "crewai task"
  - "crew sequential process"
  - "crew hierarchical"
  - "crewai kickoff"
  - "agent delegation crew"
  - "crewai tool"
  - "crewai flow"
do_not_use_for:
  - Single-agent pipelines — use langgraph or pydantic-ai instead
  - Browser automation — use browser-use instead
  - LLM fine-tuning — use llamafactory instead
see_also:
  - langgraph
  - pydantic-ai
  - smolagents
---

# CrewAI — Multi-Agent Orchestration

**Source:** crewAIInc/crewAI (MIT) — role-playing autonomous AI agents

## Core Concepts

| Concept | Description |
|---------|-------------|
| `Agent` | Autonomous unit with role, goal, backstory, llm, tools |
| `Task` | Unit of work assigned to an agent with description + expected_output |
| `Crew` | Collection of agents + tasks with a process (sequential/hierarchical) |
| `Process` | `Process.sequential` (default) or `Process.hierarchical` (manager LLM routes) |
| `Flow` | Structured event-driven orchestration with `@start`, `@listen`, `@router` |

## Install

```bash
pip install crewai crewai-tools
```

## Minimal Crew

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()

researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in {topic}",
    backstory="You are an expert at finding and synthesizing information.",
    tools=[search_tool],
    verbose=True,
    llm="claude-sonnet-4-5",
)

writer = Agent(
    role="Tech Content Strategist",
    goal="Craft compelling content on {topic}",
    backstory="You transform complex research into engaging narratives.",
    verbose=True,
    llm="claude-sonnet-4-5",
)

research_task = Task(
    description="Research the latest developments in {topic}. Focus on key trends.",
    expected_output="A bullet-point summary of 5 key findings with sources.",
    agent=researcher,
)

write_task = Task(
    description="Write a 3-paragraph blog post based on the research provided.",
    expected_output="A polished blog post in markdown format.",
    agent=writer,
    context=[research_task],  # depends on research_task output
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff(inputs={"topic": "AI agent frameworks"})
print(result.raw)
```

## Hierarchical Process (Manager Routes Tasks)

```python
from crewai import Agent, Task, Crew, Process

manager = Agent(
    role="Project Manager",
    goal="Coordinate the team to deliver the project efficiently",
    backstory="Experienced PM who delegates and synthesizes work.",
    allow_delegation=True,
    llm="claude-opus-4-5",
)

dev = Agent(role="Developer", goal="Write clean code", backstory="10y Python expert")
qa  = Agent(role="QA Engineer", goal="Find bugs", backstory="Testing specialist")

crew = Crew(
    agents=[dev, qa],
    tasks=[...],
    process=Process.hierarchical,
    manager_agent=manager,
)
```

## Custom Tools

```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(description="Search query")

class MySearchTool(BaseTool):
    name: str = "Custom Search"
    description: str = "Search for information on a topic"
    args_schema: type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        # implement actual search
        return f"Results for: {query}"

agent = Agent(
    role="Researcher",
    goal="Find information",
    backstory="Expert researcher",
    tools=[MySearchTool()],
)
```

## CrewAI Flows (Structured Orchestration)

```python
from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel

class ResearchState(BaseModel):
    topic: str = ""
    research: str = ""
    quality_score: int = 0

class ResearchFlow(Flow[ResearchState]):

    @start()
    def get_topic(self):
        self.state.topic = "AI agent frameworks"

    @listen(get_topic)
    def research(self):
        # run a crew or direct LLM call
        self.state.research = run_research_crew(self.state.topic)

    @router(research)
    def check_quality(self):
        score = evaluate_quality(self.state.research)
        self.state.quality_score = score
        return "good" if score >= 7 else "redo"

    @listen("good")
    def publish(self):
        print("Publishing:", self.state.research[:200])

    @listen("redo")
    def redo_research(self):
        print("Redoing research — quality too low")
        self.research()  # retry

flow = ResearchFlow()
flow.kickoff()
```

## Memory & Context

```python
from crewai import Crew
from crewai.memory import (
    ShortTermMemory,
    LongTermMemory,
    EntityMemory,
)

crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True,                      # enables all memory types
    # or fine-grained:
    short_term_memory=ShortTermMemory(),
    long_term_memory=LongTermMemory(),  # persists across runs
    entity_memory=EntityMemory(),       # tracks entities mentioned
    embedder={"provider": "openai", "config": {"model": "text-embedding-3-small"}},
)
```

## Async & Parallel Kickoff

```python
import asyncio

async def main():
    crew = Crew(agents=[...], tasks=[...], process=Process.sequential)

    # single async run
    result = await crew.kickoff_async(inputs={"topic": "AI"})

    # parallel runs with different inputs
    inputs_list = [{"topic": "AI"}, {"topic": "ML"}, {"topic": "LLMs"}]
    results = await crew.kickoff_for_each_async(inputs=inputs_list)

asyncio.run(main())
```

## Output Handling

```python
result = crew.kickoff(inputs={"topic": "AI"})

# Access different output formats
print(result.raw)          # raw string
print(result.pydantic)     # parsed Pydantic model (if output_pydantic set on last task)
print(result.json_dict)    # dict (if output_json set)
print(result.token_usage)  # usage stats
print(result.tasks_output) # list of TaskOutput per task
```

## Task with Structured Output

```python
from pydantic import BaseModel
from crewai import Task

class ResearchReport(BaseModel):
    title: str
    findings: list[str]
    sources: list[str]

research_task = Task(
    description="Research AI trends",
    expected_output="A structured report on AI trends",
    agent=researcher,
    output_pydantic=ResearchReport,  # enforces Pydantic schema on output
)
```

## CLI

```bash
# Create new project
crewai create crew my_project

# Run the crew
crewai run

# Train on examples
crewai train -n 5 -f training_data.pkl

# Test with eval
crewai test -n 3 -m claude-sonnet-4-5

# Deploy to CrewAI Cloud
crewai deploy
```

## Anti-Fake-Pass Checks

- [ ] `crew.kickoff()` returns `CrewOutput` with `.raw` — not a plain string
- [ ] `context=[task_a]` on Task B means B waits for A's output — not parallel
- [ ] `Process.hierarchical` requires `manager_agent` or `manager_llm`
- [ ] `allow_delegation=True` on agent needed for hierarchical routing
- [ ] Memory requires an embedder config when using non-default providers
- [ ] `@router` returns a string matching a `@listen("route_name")` decorator
