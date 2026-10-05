---
name: core-build
description: This skill should be used when designing CrewAI crews with YAML-first architecture. Use it to create crews, configure agents and tasks, select processes, and generate validation-ready outputs.
version: 3.1.0
tags: [crewai, agents, tasks, yaml, configuration]
---

# Core Build

Comprehensive skill for building CrewAI crews with YAML-first architecture.

## When To Use

- Create new crew projects
- Configure agents and tasks
- Define process workflows
- Bootstrap crew infrastructure
- Validate crew configurations
- Generate boilerplate code

## Quick Start Workflow

### 1. Scaffold New Project
```bash
python scripts/scaffold_crew.py my_crew
```

### 2. Configure Agents and Tasks
Edit `config/agents.yaml` and `config/tasks.yaml` using the templates.

### 3. Validate Configuration
```bash
python scripts/validate_crew.py my_crew
```

### 4. Execute Crew
```bash
python my_crew/main.py "your input here"
```

## Detailed Workflow

### Design Phase
1. **Define Purpose**: Clarify what the crew should accomplish
2. **Identify Agents**: Determine roles needed (researcher, analyst, writer, etc.)
3. **Map Tasks**: Break work into single-responsibility tasks
4. **Plan Dependencies**: Establish context flow between tasks

### Configuration Phase
1. **Create agents.yaml**: Define agent roles, goals, and backstories
2. **Create tasks.yaml**: Define task descriptions and expected outputs
3. **Set Context**: Link tasks using context dependencies
4. **Configure Tools**: Assign appropriate tools to agents

### Validation Phase
Run validation to catch errors early:
```bash
python scripts/validate_crew.py ./my_crew
```

Validates:
- YAML syntax and structure
- Required field presence
- Agent reference integrity
- Task context dependencies
- Circular dependency detection
- Type checking

### Execution Phase
Use the scaffolded `main.py` or integrate into your application:

```python
from crew import MyCrewCrew

inputs = {"topic": "your input"}
result = MyCrewCrew().crew().kickoff(inputs=inputs)
```

## Process Selection Guide

### Sequential Process
- Tasks execute in order
- Each task can access previous task outputs
- Simple and predictable

**Use for**: Data pipelines, content creation, research workflows

```python
from crewai import Process

crew = Crew(
    process=Process.sequential,
    # ...
)
```

### Hierarchical Process  
- Manager coordinates task execution
- Dynamic task assignment
- Built-in quality review

**Use for**: Complex projects, quality-critical work, multi-agent collaboration

```python
from crewai import Process

crew = Crew(
    process=Process.hierarchical,
    manager_llm="gpt-4",
    # ...
)
```

## Common Patterns

### Research → Analysis → Report
```yaml
# agents.yaml
researcher:
  role: Research Specialist
  goal: Gather comprehensive information

analyst:
  role: Data Analyst
  goal: Extract insights and patterns

# tasks.yaml
research_task:
  description: Research {topic}
  agent: researcher
  
analysis_task:
  description: Analyze findings
  agent: analyst
  context:
    - research_task
```

### Multi-Agent Collaboration
Specialized agents working on different aspects simultaneously.

### Review Loop Pattern
Iterative improvement with feedback cycles and revisions.

See `references/guides/patterns.md` for complete pattern library.

## Decorator Reference

### @CrewBase
Marks the class as a CrewBase configuration class.

```python
@CrewBase
class MyCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
```

### @agent
Defines an agent method that returns an Agent instance.

```python
@agent
def researcher(self) -> Agent:
    return Agent(config=self.agents_config['researcher'])
```

### @task
Defines a task method that returns a Task instance.

```python
@task
def research_task(self) -> Task:
    return Task(config=self.tasks_config['research_task'])
```

### @crew
Defines the crew method that returns the Crew instance.

```python
@crew
def crew(self) -> Crew:
    return Crew(agents=self.agents, tasks=self.tasks)
```

### @before_kickoff
Runs before crew execution starts.

```python
@before_kickoff
def before_kickoff_function(self, inputs):
    print(f"Starting with inputs: {inputs}")
    return inputs
```

### @after_kickoff
Runs after crew execution completes.

```python
@after_kickoff
def after_kickoff_function(self, result):
    print(f"Completed with result: {result}")
    return result
```

## Tool Usage

### scaffold_crew.py
Scaffolds a new crew project from templates.

```bash
# Create in current directory
python scripts/scaffold_crew.py my_crew

# Create in specific directory
python scripts/scaffold_crew.py my_crew --path ./crews
```

### validate_crew.py
Validates crew configuration files.

```bash
# Validate a crew
python scripts/validate_crew.py ./my_crew

# With detailed output
python scripts/validate_crew.py ./my_crew --verbose
```

### generate_config.py
Interactive configuration generator.

```bash
# Generate interactively
python scripts/generate_config.py

# Choose agent, task, or full crew setup
```

## Asset Templates

### Starter Project
- `assets/starter/` - Complete working crew template
  - `config/agents.yaml` - Researcher and analyst agents
  - `config/tasks.yaml` - Research and analysis tasks
  - `crew.py` - Full CrewBase class
  - `main.py` - CLI entry point
  - `.env.example` - Environment template
  - `README.md` - Project documentation

### Configuration Templates
- `assets/templates/agents-basic.yaml` - Starter agent configuration
- `assets/templates/agents-advanced.yaml` - All agent parameters
- `assets/templates/tasks-basic.yaml` - Starter task configuration
- `assets/templates/tasks-advanced.yaml` - All task parameters

## Reference Documentation

### API Documentation
- `references/api/agents.md` - Complete agent attribute reference
- `references/api/tasks.md` - Complete task attribute reference
- `references/api/crews.md` - Complete crew attribute reference

### Guides
- `references/guides/best-practices.md` - Design principles and guidelines
- `references/guides/patterns.md` - Common crew architecture patterns

### External Resources
- `references/external.md` - Official documentation links

## Troubleshooting

### Common Issues

**Missing required fields**
```
Error: Agent 'name' missing required field 'role'
```
Solution: Add all required fields (role, goal, backstory)

**Agent not found**
```
Error: Task references unknown agent 'wrong_name'
```
Solution: Ensure agent name in tasks.yaml matches agents.yaml

**Circular dependency**
```
Error: Circular dependency detected
```
Solution: Remove the circular reference in task context

**YAML syntax error**
```
Error: YAML parse error at line 5
```
Solution: Check indentation (use 2 spaces) and syntax

### Validation Always Passes First
Always run `validate_crew.py` before execution to catch errors early.

### Debugging Tips
1. Enable verbose mode: `verbose: true`
2. Check context dependencies are correct
3. Validate agent names match exactly
4. Use markdown formatting for readability
5. Test with simple inputs first

## Mastery Steps

1. **Study Templates**: Review `assets/starter/` to understand structure
2. **Configure Agents**: Use `references/api/agents.md` for options
3. **Define Tasks**: Use `references/api/tasks.md` for configuration
4. **Validate**: Run `scripts/validate_crew.py` to check for errors
5. **Test**: Execute with sample inputs and refine
6. **Iterate**: Use patterns from `references/guides/patterns.md` for complex crews

## File Structure

```
core-build/
├── SKILL.md                           # This file
├── assets/
│   ├── starter/                       # Complete working project
│   │   ├── config/
│   │   │   ├── agents.yaml           # Starter agent config
│   │   │   └── tasks.yaml            # Starter task config
│   │   ├── crew.py                   # CrewBase implementation
│   │   ├── main.py                   # CLI entry point
│   │   ├── .env.example              # Environment template
│   │   └── README.md                 # Project documentation
│   └── templates/                     # Standalone templates
│       ├── agents-basic.yaml         # Basic agent config
│       ├── agents-advanced.yaml      # Advanced agent reference
│       ├── tasks-basic.yaml          # Basic task config
│       └── tasks-advanced.yaml       # Advanced task reference
├── references/
│   ├── api/                           # API documentation
│   │   ├── agents.md                 # Agent attributes
│   │   ├── tasks.md                  # Task attributes
│   │   └── crews.md                  # Crew attributes
│   ├── guides/                        # How-to guides
│   │   ├── best-practices.md         # Best practices
│   │   └── patterns.md               # Architecture patterns
│   └── external.md                   # Official docs links
└── scripts/                           # Executable tools
    ├── scaffold_crew.py              # Project scaffolding
    ├── validate_crew.py              # Configuration validation
    └── generate_config.py            # Interactive config generator
```

## Coding-Agent Guidelines

- Design crews with contracts over prose; keep prompts out of inline Python constructors
- Enforce single-purpose tasks with explicit expected outputs and context dependencies
- Make process choice explicit and justified for reproducibility
- Produce artifacts that are directly reusable by downstream Flows
- Always validate configurations before execution
- Use templates as starting points, customize for specific needs
- Follow naming conventions: snake_case for files, descriptive names for agents/tasks
- Document assumptions and constraints in task descriptions
- Test with edge cases and validate error handling
