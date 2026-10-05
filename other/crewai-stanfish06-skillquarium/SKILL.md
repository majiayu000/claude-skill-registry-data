---
name: crewai
description: Role-based multi-agent orchestration framework for building "Crews" of collaborating LLM agents (each with a role, goal, backstory, and optional tools) that execute sequential or hierarchical task pipelines, plus event-driven "Flows" for precise, single-LLM-call orchestration. Use when composing specialized agents (e.g. a research agent + an analysis agent + a writer agent) into a declarative pipeline for complex multi-step tasks like automated literature review or multi-agent research workflows. Distinct from LangGraph's explicit state-machine graphs and smolagents' minimal tool-calling loop — CrewAI is standalone (no LangChain dependency) and expresses orchestration as roles and delegated tasks rather than a graph or a single ReAct loop.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
compatibility: Requires Python >=3.10,<3.14 and crewai 1.x. Routes most LLM providers through LiteLLM by default, so provider extras (crewai[anthropic], crewai[aws]/[bedrock], crewai[azure-ai-inference], crewai[google-genai]) are usually optional; install crewai[tools] to pull in the separate crewai-tools package of prebuilt tools (web search, file readers, code execution, etc.).
metadata: {"version": "1.0", "skill-author": "community"}
---

# CrewAI

## Overview

CrewAI is a Python framework, built from scratch independent of LangChain, for orchestrating teams of LLM agents. It has two complementary orchestration models:

- **Crews** — role-based, autonomous collaboration. You define `Agent`s (each with a `role`, `goal`, `backstory`, and optional `tools`/`llm`) and `Task`s (each with a `description`, `expected_output`, and an assigned `agent`), then wire them into a `Crew` that runs tasks either `Process.sequential` (task N's output feeds task N+1) or `Process.hierarchical` (a manager agent dynamically delegates tasks to the crew).
- **Flows** — event-driven, deterministic control. `@start()`/`@listen()`-decorated methods let you chain individual LLM calls, conditionals, and (optionally) whole Crews with precise control, when you need more determinism than a fully autonomous Crew.

Where LangGraph models orchestration explicitly as a state-machine graph, and smolagents minimizes overhead around a single tool-calling loop, CrewAI's abstraction is closer to how a human team is briefed: each agent gets a persona and a goal, and delegates/collaborates through natural-language task handoffs.

## Installation

```bash
uv pip install crewai
uv pip install "crewai[tools]"     # prebuilt tools package (web search, RAG, code exec, file I/O, ...)

# Provider extras are usually unnecessary — crewai talks to most providers via LiteLLM model strings
uv pip install "crewai[anthropic]"   # only if you need the native (non-LiteLLM) Anthropic SDK path
```

Set the relevant provider API key as an environment variable (e.g. `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`) before running — CrewAI's default `llm=` resolution picks these up automatically via LiteLLM.

Check version: `python -c "import crewai; print(crewai.__version__)"` (targets the 1.15.x series).

## When to Use vs. LangGraph / smolagents

| | CrewAI | LangGraph | smolagents |
|---|---|---|---|
| Mental model | Role-playing agents, delegated tasks | Explicit state-machine graph | Minimal single-agent tool-calling loop |
| Best for | Multi-persona pipelines (researcher → analyst → writer) | Complex branching/looping control flow you want to see explicitly | Lightweight single-agent tool use, fast prototyping |
| Determinism | Crews are more autonomous; Flows add explicit control | High (you define every edge) | Low-to-medium (ReAct loop) |

Reach for CrewAI when the natural decomposition of your problem is "a team of specialists," and for LangGraph when you need to reason precisely about every possible transition between steps.

## Core Concepts

```python
from crewai import Agent, Task, Crew, Process

researcher = Agent(
    role="Senior Research Analyst",
    goal="Find and summarize the latest findings on {topic}",
    backstory="You are an expert at scanning literature and extracting the signal from noise.",
    verbose=True,
)

writer = Agent(
    role="Technical Writer",
    goal="Turn research findings into a clear, well-structured report",
    backstory="You write for a technical but time-constrained audience.",
    verbose=True,
)

research_task = Task(
    description="Research recent developments in {topic} and list the 5 most important findings.",
    expected_output="A bulleted list of 5 findings, each with a one-sentence explanation.",
    agent=researcher,
)

writing_task = Task(
    description="Using the research findings, write a 3-paragraph summary report on {topic}.",
    expected_output="A 3-paragraph markdown report.",
    agent=writer,
    context=[research_task],   # explicitly pass research_task's output into this task's context
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff(inputs={"topic": "CRISPR base editing"})
print(result.raw)
```

`Process.hierarchical` instead assigns a manager LLM (set via `Crew(manager_llm=...)` or a dedicated manager `Agent`) that decides at runtime which agent handles which task — useful when the task breakdown isn't known ahead of time.

## Tools

```python
from crewai.tools import tool

@tool("Query internal database")
def query_db(sql: str) -> str:
    """Run a read-only SQL query against the internal research database and return rows as text."""
    return run_query(sql)

researcher = Agent(role="...", goal="...", backstory="...", tools=[query_db])
```

`crewai-tools` (via the `tools` extra) ships common prebuilt tools — web/serper search, file readers, directory readers, RAG tools, code-execution sandboxes — so custom `@tool` functions are usually only needed for internal/proprietary integrations.

## Flows: Event-Driven Control

```python
from crewai.flow.flow import Flow, start, listen

class ResearchFlow(Flow):
    @start()
    def get_topic(self):
        self.state["topic"] = "single-cell foundation models"
        return self.state["topic"]

    @listen(get_topic)
    def run_research_crew(self, topic):
        return research_crew.kickoff(inputs={"topic": topic})

    @listen(run_research_crew)
    def save_report(self, report):
        with open("report.md", "w") as f:
            f.write(report.raw)

ResearchFlow().kickoff()
```

Flows can mix single LLM calls, plain Python logic, and whole `Crew.kickoff()` calls as steps — use them when a Crew alone gives you too little control over the sequence of operations.

## Memory

Crews support short-term memory (within a run), long-term memory (persisted across runs via a local vector store), and entity memory (tracked facts about specific entities). Enable with `Crew(memory=True)`; for production use, back it with an explicit vector store config rather than the default local one so memory survives across deployments.

## Project Scaffolding

```bash
crewai create crew my_project
cd my_project
crewai run
```

This generates the JSON-first layout: agent definitions live in `agents/*.jsonc`, while tasks, process, and input defaults live in `crew.jsonc`. If you need the older Python/YAML layout with `crew.py`, `config/agents.yaml`, and `config/tasks.yaml`, create it explicitly:

```bash
crewai create crew my_project --classic
```

## Observability

CrewAI emits OpenTelemetry traces (via `opentelemetry-sdk`, bundled as a dependency) and has a hosted "Crew Control Plane" (part of the commercial AMP Suite) for tracing/monitoring in production; for local debugging, `verbose=True` on `Agent`/`Crew`/`Task` prints each agent's reasoning and tool calls to stdout.

## Common Pitfalls

- **Vague `expected_output`.** CrewAI agents use `expected_output` to judge when a task is "done" — a vague description (e.g., "a summary") produces inconsistent, sometimes incomplete outputs; be concrete about format and length ("a bulleted list of exactly 5 findings").
- **Duplicate or overlapping `role`s confuse hierarchical delegation.** In `Process.hierarchical`, the manager picks an agent by matching the task to agent roles/goals; near-identical roles across agents lead to unpredictable delegation. Keep roles distinct.
- **Missing `context=[...]` between sequential tasks.** In `Process.sequential`, CrewAI passes prior task outputs forward automatically by order, but for non-adjacent dependencies (task 3 needs task 1's output, not task 2's) you must set `context=` explicitly or the dependency is silently dropped.
- **Cost/latency compounding in long sequential crews.** Each agent call is a full LLM round-trip (sometimes with its own tool-calling sub-loop); a 5-agent sequential crew can be significantly slower/costlier than one well-prompted single-agent call — reserve multi-agent Crews for genuinely decomposable problems, not everything.
- **Tool description mutation.** Recent versions (1.15.x) intentionally stop rewriting a tool's authored description at construction time — if you're relying on CrewAI to auto-generate/adjust a tool's description for the LLM, write the description you actually want up front instead.
- **Rate limits from `verbose=True` chains during development.** Verbose mode is invaluable for debugging but doesn't reduce actual LLM calls; if you're hitting provider rate limits while iterating, that's real traffic, not a logging artifact — reduce `max_iterations`/agent count while debugging.

## Resources

- Docs: https://docs.crewai.com/
- Source: https://github.com/crewAIInc/crewAI
- crewai-tools: https://github.com/crewAIInc/crewAI-tools
- Learning platform: https://learn.crewai.com/
