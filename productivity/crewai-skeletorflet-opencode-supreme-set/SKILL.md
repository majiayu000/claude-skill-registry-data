---
name: crewai
description: CrewAI framework for orchestrating multi-agent AI workflows
---

### Core Concepts
- **Agents**: Role-based autonomous entities with `role`, `goal`, `backstory`, `llm_config`
- **Tasks**: Atomic units of work assigned to agents with `description`, `expected_output`, `agent`
- **Tools**: Functions agents can call (`@tool` decorator or `Tool.from_function`) for external actions
- **Process Flow**: `Process.sequential` (chain) or `Process.hierarchical` (manager-agent routing)
- **Memory**: Short-term, long-term, and entity memory between crew runs
- **Custom Tools**: Extend base `Tool` class or use `Tool.from_function` with input schema

### Common Patterns
- `Agent(role="Researcher", goal="Find information", backstory="...", llm=llm_config)`
- `Task(description="Analyze trends", expected_output="Report", agent=researcher)`
- `Crew(agents=[researcher, writer], tasks=[research, write], process=Process.sequential).kickoff()`
- `@tool("search_tool")` decorator on functions agents can invoke
- `Tool.from_function(name="calculator", func=calc, description="Adds numbers")`
- Custom LLM: `config={"provider": "openai", "model": "gpt-4", "temperature": 0.7}`

### Best Practices
- Keep agent `goal` specific and `backstory` concise for consistent behavior
- Define `expected_output` clearly on every task to guide agent completion
- Use `Process.hierarchical` only when tasks require delegation decisions
- Enable `memory=True` on Crew for context persistence across iterations
- Pin `crewai` and `crewai-tools` versions for reproducible agent behavior
