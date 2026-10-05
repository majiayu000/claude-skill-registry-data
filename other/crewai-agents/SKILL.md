---
name: crewai-agents
description: Use when crewAI multi-agent orchestration — agents, tasks, crews, tools,
  memory, delegation. Use when working with crewai agents.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- agents
- ai-agent
- crewai
- infrastructure
- memory
- self-improvement
version: 1.0.0
category: core
---


## Overview

CrewAI is a framework for orchestrating role-playing AI agents that collaborate to complete complex tasks. Agents have roles, goals, and backstories, and work together in crews with configurable processes (sequential, hierarchical).

## Capabilities

- Define agents with roles, goals, and tools
- Create tasks with expected outputs
- Organize crews with sequential or hierarchical processes
- Add custom tools for web search, file I/O, APIs
- Enable memory for context across tasks
- Use delegation for agent-to-agent communication

## When to Use
**Trigger phrases:**
- "crewai agents"
- "CrewAI multi-agent orchestration — agents, tasks, crews, tools, memory, delegati"


- Building multi-agent systems for research, writing, or analysis
- Needing role-specialized agents collaborating on tasks
- Wanting structured task delegation with accountability
- Building autonomous workflows with human-in-the-loop options

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Agent and Crew Definition

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, FileReadTool

# Tools
search_tool = SerperDevTool()
file_tool = FileReadTool()

# Agents
researcher = Agent(
    role="Senior Research Analyst",
    goal="Find comprehensive information on the given topic",
    backstory="You are an experienced researcher with expertise in finding and synthesizing information from multiple sources.",
    tools=[search_tool],
    verbose=True,
    allow_delegation=False,
)

writer = Agent(
    role="Content Writer",
    goal="Write engaging, well-structured content based on research",
    backstory="You are a skilled writer who transforms research into compelling narratives.",
    tools=[file_tool],
    verbose=True,
    allow_delegation=False,
)

reviewer = Agent(
    role="Quality Reviewer",
    goal="Ensure content is accurate, well-structured, and meets standards",
    backstory="You are a meticulous editor with years of experience in content quality assurance.",
    verbose=True,
    allow_delegation=True,  # Can delegate back to writer
)

# Tasks
research_task = Task(
    description="Research the latest trends in AI agents for 2026",
    expected_output="A comprehensive report with key findings, trends, and data points",
    agent=researcher,
)

writing_task = Task(
    description="Write a blog post based on the research findings",
    expected_output="A 1500-word blog post with introduction, key sections, and conclusion",
    agent=writer,
    context=[research_task],  # Depends on research
)

review_task = Task(
    description="Review the blog post for accuracy and quality",
    expected_output="A quality assessment with specific improvement suggestions",
    agent=reviewer,
    context=[writing_task],
)

# Crew
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, writing_task, review_task],
    process=Process.sequential,  # Execute tasks in order
    verbose=True,
    memory=True,  # Enable shared memory
)

# Execute
result = crew.kickoff()
print(result)
```

### Custom Tools

```python
from crewai_tools import BaseTool
from pydantic import BaseModel, Field

class DatabaseQueryInput(BaseModel):
    query: str = Field(description="SQL query to execute")

class DatabaseQueryTool(BaseTool):
    name: str = "database_query"
    description: str = "Execute SQL queries against the analytics database"
    args_schema: type[BaseModel] = DatabaseQueryInput

    def _run(self, query: str) -> str:
        import pandas as pd
        df = pd.read_sql(query, con=engine)
        return df.to_string()
```

### Hierarchical Process

```python
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, writing_task, review_task],
    process=Process.hierarchical,  # Manager agent delegates
    manager_llm="gpt-4o",
    verbose=True,
)
```

### Human Input

```python
task = Task(
    description="Research and write about...",
    expected_output="...",
    agent=researcher,
    human_input=True,  # Pause for human feedback before completing
)
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| `Process.sequential` | Tasks have clear order |
| `Process.hierarchical` | Need manager to delegate dynamically |
| `allow_delegation=True` | Agent can ask other agents for help |
| `memory=True` | Share context across tasks |
| `human_input=True` | Need human approval at step |
| `context=[task]` | Task dependency |
| Custom `BaseTool` | Integrate external systems |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Agent loop (delegation cycle) | Agents delegating back and forth | Set `allow_delegation=False` on some agents |
| Task timeout | Agent stuck reasoning | Add `max_iterations` to crew |
| Tool error | External API failure | Add error handling in tool `_run` method |
| Token limit exceeded | Long conversation history | Reduce context or use `memory=False` |

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will add monitoring later" | Without monitoring, you cannot detect failures. Add it from day one. |
| "One model is enough" | Different tasks need different models. Route intelligently. |
| "Premature optimization" | Infrastructure decisions are hard to change later. Design for scale early. |