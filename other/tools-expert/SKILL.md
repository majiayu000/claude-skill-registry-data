---
name: tools-expert
description: This skill should be used when selecting CrewAI built-in tools, composing agent toolchains, or creating production-ready custom tools with BaseTool or @tool, including schema validation, dependency management, caching, async support, and testing.
version: 1.0.0
tags: [crewai, tools, custom-tools, basetool, mcp]
---

# CrewAI Tools Expert

## Purpose

Enable expert-level tool decisions in CrewAI projects by prioritizing built-in tools first and creating custom tools only when a capability gap is explicit.

## When To Use

- Select tools for a new or existing agent
- Convert requirements into a minimal and reliable tool stack
- Decide between built-in tools, `@tool`, `BaseTool`, or `RagTool` patterns
- Implement custom tools with robust validation, error handling, and async support
- Integrate external APIs, MCP servers, and enterprise systems

## Operating Principles

- Prefer built-in tools before writing custom code
- Minimize tool count per agent to reduce tool-selection ambiguity
- Match tool outputs to task contracts and downstream consumers
- Validate credentials, dependencies, and failure modes early
- Keep tool outputs concise, deterministic, and directly usable by agents

## Execution Workflow

### 1) Profile the Request

- Extract inputs, expected outputs, latency constraints, security constraints, and external systems
- Classify the dominant tool domain using `references/tools-landscape.md`
- Record hard constraints such as offline execution, strict schemas, or approved vendors

### 2) Attempt Built-In Coverage

- Identify candidate tools by category from `references/tools-landscape.md`
- Confirm setup requirements (API keys, package extras, authentication)
- Compose the smallest viable built-in stack to satisfy requirements
- Cap noisy tools with `max_usage_count` when repeated calls add little value

### 3) Choose Build Path

- Use `references/selection-and-architecture.md` to choose among:
  - Built-in only
  - Hybrid (built-in + one custom tool)
  - Fully custom (rare; use only when required)
- Choose custom style:
  - Use `@tool` for lightweight, stateless transforms
  - Use `BaseTool` for configurable/stateful tools with env vars or dependencies
  - Use `RagTool` or adapter patterns for retrieval-oriented sources

### 4) Scaffold and Implement Custom Tool

- Generate starter files with `scripts/scaffold_custom_tool.py`
- Use templates in `assets/templates/` for manual edits or fast bootstrap
- Apply standards in `references/custom-tool-playbook.md`
- Enforce:
  - Explicit `args_schema` with Pydantic `Field` descriptions
  - Clear `name` and action-oriented `description`
  - Deterministic `_run` output
  - Optional `_arun` for true async I/O
  - Actionable errors without stack-trace leakage

### 5) Validate Quality

- Run the implementation checklist in `references/custom-tool-playbook.md`
- Verify tests cover:
  - Missing/invalid environment variables
  - Input validation boundaries
  - Happy path output shape
  - External failures (timeouts, HTTP errors, empty payloads)
- Confirm docs include usage, env vars, install extras, and examples

### 6) Integrate Into Agent Design

- Attach tools by role specialization, not by convenience
- Keep each agent toolset domain-coherent
- Document why each tool exists and when to call it
- Prefer orchestration with specialized worker tools for complex crews

## YAML Agent Example

```yaml
# agents.yaml
research_tools_agent:
  role: Tooling Research Analyst
  goal: Select the smallest reliable built-in CrewAI tool stack for each request.
  backstory: Expert in built-in tools, API setup constraints, and capability-gap detection.
  verbose: true
  tools:
    - SerperDevTool
    - WebsiteSearchTool
    - FileReadTool

tool_engineer_agent:
  role: CrewAI Tool Engineer
  goal: Define production-ready custom tool specs only when built-ins do not satisfy requirements.
  backstory: Specialist in BaseTool patterns, input schema design, and failure-safe integration rules.
  verbose: true
  tools:
    - DirectoryReadTool
    - FileReadTool
```

## YAML Task Example

```yaml
# tasks.yaml
tool_gap_analysis_task:
  description: >
    Evaluate whether built-in CrewAI tools can satisfy the request.
    Produce a capability matrix and justify every selected built-in tool.
  expected_output: >
    Markdown table listing selected tools, required credentials,
    setup notes, and explicit capability gaps.
  agent: research_tools_agent

custom_tool_spec_task:
  description: >
    If a capability gap exists, define a custom tool specification
    with args_schema fields, env vars, package dependencies,
    caching policy, async policy, and error-handling strategy.
  expected_output: >
    Structured spec and acceptance checklist for implementation and tests.
  agent: tool_engineer_agent
  context:
    - tool_gap_analysis_task
```

## Custom Tool Scaffolding

- Use `scripts/scaffold_custom_tool.py` when implementation boilerplate is needed.

## Resource Map

- `references/tools-landscape.md`: Built-in tool categories, quick picks, and coverage map
- `references/selection-and-architecture.md`: Built-in vs custom decision framework
- `references/custom-tool-playbook.md`: Production implementation standards
- `references/repo-notes.md`: zread findings from CrewAI tools repository and maintenance notes
- `scripts/scaffold_custom_tool.py`: Deterministic custom-tool starter generator
- `assets/templates/agents-tools-expert.yaml`: Agent template for built-in tool strategy
- `assets/templates/tasks-tools-selection.yaml`: Task template for built-in selection and gap analysis
- `assets/templates/agents-custom-tooling.yaml`: Agent template for custom-tool specification work
- `assets/templates/tasks-custom-tooling.yaml`: Task template for custom-tool implementation planning

## Source-of-Truth Notes

- Treat CrewAI docs as primary guidance, especially `https://docs.crewai.com/en/tools/overview`
- Use `references/repo-notes.md` for repository conventions validated via zread MCP
- Recheck upstream changes regularly because the historical `crewAI-tools` repository is marked deprecated and points to a maintained monorepo location
